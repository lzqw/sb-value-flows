#!/usr/bin/env bash
set -euo pipefail

cd /root/sb-value-flows

LOG_DIR=/root/autodl-tmp/sb-value-flows-runs/offline2online_single4090/logs
CHECKPOINT_CSV=/root/sb-value-flows/results/offline2online_checkpoint_sources.csv
RUNS_CSV=/root/sb-value-flows/results/offline2online_runs.csv
mkdir -p "$LOG_DIR"

stamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

active_main_py() {
  ps -eo pid=,comm=,args= | awk '$2 ~ /^(python|conda|main.py)/ && index($0, "main.py") { print; found = 1 } END { exit(found ? 0 : 1) }'
}

scenario_env() {
  case "$1" in
    cube-double) echo "cube-double-play-singletask-task4-v0" ;;
    puzzle-4x4) echo "puzzle-4x4-play-singletask-task3-v0" ;;
    scene) echo "scene-play-singletask-task4-v0" ;;
    *) echo "unknown" ;;
  esac
}

wait_for_idle() {
  while active_main_py >/tmp/offline2online_active_main.$$; do
    echo "[$(stamp)] waiting for active main.py:"
    cat /tmp/offline2online_active_main.$$
    sleep 300
  done
  rm -f /tmp/offline2online_active_main.$$
}

refresh_checkpoints() {
  echo "[$(stamp)] registering checkpoints"
  scripts/run_offline2online.py --mode checkpoints
}

refresh_results() {
  scripts/run_offline2online.py --mode checkpoints
  scripts/run_offline2online.py --mode collect
}

has_checkpoint() {
  local method="$1"
  local scenario="$2"
  local seed="$3"
  local env
  env="$(scenario_env "$scenario")"
  refresh_checkpoints >/dev/null
  awk -F, -v m="$method" -v e="$env" -v s="$seed" '
    NR > 1 && $1 == m && $2 == e && $3 == s && ($5 + 0) >= 500000 { found = 1 }
    END { exit(found ? 0 : 1) }
  ' "$CHECKPOINT_CSV"
}

screen_status() {
  local method="$1"
  local scenario="$2"
  local seed="$3"
  local config="$4"
  refresh_results >/dev/null
  awk -F, -v m="$method" -v sc="$scenario" -v s="$seed" -v c="$config" '
    NR > 1 && $1 == sc && $4 == m && $6 == c && $7 == s && $21 == "screening" {
      status = $10
    }
    END {
      if (status != "") {
        print status
      }
    }
  ' "$RUNS_CSV"
}

run_and_wait() {
  echo "[$(stamp)] RUN $*"
  "$@"
  sleep 5
  wait_for_idle
  scripts/run_offline2online.py --mode collect
}

ensure_pretrain() {
  local scenario="$1"
  local method="$2"
  local seed="$3"
  local config="$4"
  if has_checkpoint "$method" "$scenario" "$seed"; then
    echo "[$(stamp)] checkpoint already available for $scenario/$method/seed$seed"
    return
  fi
  run_and_wait scripts/run_offline2online.py \
    --mode pretrain \
    --stage screen \
    --scenario "$scenario" \
    --method "$method" \
    --seed "$seed" \
    --offline_steps 500000 \
    --save_interval 500000 \
    --eval_interval 50000 \
    --eval_episodes 10 \
    --log_interval 25000 \
    --config_name "$config"
  refresh_checkpoints
  if ! has_checkpoint "$method" "$scenario" "$seed"; then
    echo "[$(stamp)] ERROR no >=500k checkpoint found after pretrain for $scenario/$method/seed$seed"
    exit 1
  fi
}

run_screen() {
  local scenario="$1"
  local method="$2"
  local seed="$3"
  local config="$4"
  local status
  refresh_checkpoints
  if ! has_checkpoint "$method" "$scenario" "$seed"; then
    echo "[$(stamp)] ERROR refusing online screening without >=500k checkpoint for $scenario/$method/seed$seed"
    exit 1
  fi
  status="$(screen_status "$method" "$scenario" "$seed" "$config")"
  if [ "$status" = "completed" ] || [ "$status" = "completed_1m" ]; then
    echo "[$(stamp)] screening already complete for $scenario/$method/seed$seed/$config"
    return
  fi
  if [ -n "$status" ] && [ "$status" != "partial" ]; then
    echo "[$(stamp)] ERROR unexpected screening status for $scenario/$method/seed$seed/$config: $status"
    exit 1
  fi
  if [ "$status" = "partial" ] && ! active_main_py >/dev/null; then
    echo "[$(stamp)] ERROR found partial existing screening without active main.py for $scenario/$method/seed$seed/$config"
    echo "[$(stamp)] inspect $RUNS_CSV before forcing or replacing this run"
    exit 1
  fi
  run_and_wait scripts/run_offline2online.py \
    --mode launch \
    --stage screen \
    --scenario "$scenario" \
    --method "$method" \
    --seed "$seed" \
    --online_steps 500000 \
    --eval_interval 50000 \
    --eval_episodes 10 \
    --log_interval 25000 \
    --online_sample_ratio 1.0 \
    --config_name "$config"
}

echo "[$(stamp)] stageB queue started"
wait_for_idle

seed=2
for scenario in cube-double puzzle-4x4 scene; do
  ensure_pretrain "$scenario" ours "$seed" "ckpt500k_lam1e-3_tau0p3"
  run_screen "$scenario" ours "$seed" "restored500k_r1p0_lam1e-3_tau0p3"
done

for method in value_flows fql; do
  for scenario in cube-double puzzle-4x4 scene; do
    ensure_pretrain "$scenario" "$method" "$seed" "ckpt500k_default"
    run_screen "$scenario" "$method" "$seed" "restored500k_r1p0_default"
  done
done

scripts/run_offline2online.py --mode status
echo "[$(stamp)] stageB queue completed"

#!/usr/bin/env bash
set -euo pipefail

cd /root/sb-value-flows

LOG_DIR=/root/autodl-tmp/sb-value-flows-runs/offline2online_single4090/logs
CHECKPOINT_CSV=/root/sb-value-flows/results/offline2online_checkpoint_sources.csv
RUNS_CSV=/root/sb-value-flows/results/offline2online_runs.csv
LOCK_FILE=/tmp/offline2online_stagec_queue.lock
mkdir -p "$LOG_DIR"

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "another Stage C queue is already running"
  exit 0
fi

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

pretrain_config() {
  case "$1:$2" in
    *:ours) echo "ckpt500k_lam1e-3_tau0p3" ;;
    *) echo "ckpt500k_default" ;;
  esac
}

final_config() {
  case "$1:$2" in
    *:ours) echo "final1m_r1p0_lam1e-3_tau0p3" ;;
    *) echo "final1m_r1p0_default" ;;
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
  refresh_results >/dev/null
  awk -F, -v m="$method" -v e="$env" -v s="$seed" '
    NR > 1 && $1 == m && $2 == e && $3 == s && ($5 + 0) >= 500000 { found = 1 }
    END { exit(found ? 0 : 1) }
  ' "$CHECKPOINT_CSV"
}

has_completed_final() {
  local method="$1"
  local scenario="$2"
  local seed="$3"
  refresh_results >/dev/null
  awk -F, -v m="$method" -v sc="$scenario" -v s="$seed" '
    NR > 1 && $1 == sc && $4 == m && $7 == s && $10 == "completed_1m" && $21 == "final" { found = 1 }
    END { exit(found ? 0 : 1) }
  ' "$RUNS_CSV"
}

final_status() {
  local method="$1"
  local scenario="$2"
  local seed="$3"
  local config="$4"
  refresh_results >/dev/null
  awk -F, -v m="$method" -v sc="$scenario" -v s="$seed" -v c="$config" '
    NR > 1 && $1 == sc && $4 == m && $6 == c && $7 == s && $21 == "final" {
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
  local config
  config="$(pretrain_config "$scenario" "$method")"
  if has_checkpoint "$method" "$scenario" "$seed"; then
    echo "[$(stamp)] checkpoint already available for $scenario/$method/seed$seed"
    return
  fi
  run_and_wait scripts/run_offline2online.py \
    --mode pretrain \
    --stage final \
    --scenario "$scenario" \
    --method "$method" \
    --seed "$seed" \
    --offline_steps "${O2O_PRETRAIN_STEPS:-500000}" \
    --save_interval "${O2O_PRETRAIN_STEPS:-500000}" \
    --eval_interval "${O2O_EVAL_INTERVAL:-50000}" \
    --eval_episodes "${O2O_EVAL_EPISODES:-10}" \
    --log_interval "${O2O_LOG_INTERVAL:-25000}" \
    --config_name "$config"
  if ! has_checkpoint "$method" "$scenario" "$seed"; then
    echo "[$(stamp)] ERROR no >=500k checkpoint found after pretrain for $scenario/$method/seed$seed"
    exit 1
  fi
}

run_final() {
  local scenario="$1"
  local method="$2"
  local seed="$3"
  local config
  local status
  config="$(final_config "$scenario" "$method")"
  if has_completed_final "$method" "$scenario" "$seed"; then
    echo "[$(stamp)] final run already complete for $scenario/$method/seed$seed"
    return
  fi
  if ! has_checkpoint "$method" "$scenario" "$seed"; then
    echo "[$(stamp)] ERROR refusing final online run without >=500k checkpoint for $scenario/$method/seed$seed"
    exit 1
  fi
  status="$(final_status "$method" "$scenario" "$seed" "$config")"
  if [ "$status" = "completed_1m" ]; then
    echo "[$(stamp)] final run already complete for $scenario/$method/seed$seed/$config"
    return
  fi
  if [ -n "$status" ] && [ "$status" != "partial" ]; then
    echo "[$(stamp)] ERROR unexpected final status for $scenario/$method/seed$seed/$config: $status"
    exit 1
  fi
  if [ "$status" = "partial" ] && ! active_main_py >/dev/null; then
    echo "[$(stamp)] ERROR found partial existing final run without active main.py for $scenario/$method/seed$seed/$config"
    echo "[$(stamp)] inspect $RUNS_CSV before forcing or replacing this run"
    exit 1
  fi
  run_and_wait scripts/run_offline2online.py \
    --mode launch \
    --stage final \
    --scenario "$scenario" \
    --method "$method" \
    --seed "$seed" \
    --online_steps "${O2O_FINAL_ONLINE_STEPS:-1000000}" \
    --eval_interval "${O2O_EVAL_INTERVAL:-50000}" \
    --eval_episodes "${O2O_EVAL_EPISODES:-10}" \
    --log_interval "${O2O_LOG_INTERVAL:-25000}" \
    --online_sample_ratio "${O2O_ONLINE_SAMPLE_RATIO:-1.0}" \
    --config_name "$config"
}

echo "[$(stamp)] stageC queue started"
echo "[$(stamp)] scenarios: ${O2O_SCENARIOS:-cube-double puzzle-4x4 scene}"
echo "[$(stamp)] methods: ${O2O_METHODS:-ours value_flows fql}"
echo "[$(stamp)] seeds: ${O2O_SEEDS:-2 3}"
wait_for_idle

for seed in ${O2O_SEEDS:-2 3}; do
  for method in ${O2O_METHODS:-ours value_flows fql}; do
    for scenario in ${O2O_SCENARIOS:-cube-double puzzle-4x4 scene}; do
      ensure_pretrain "$scenario" "$method" "$seed"
      run_final "$scenario" "$method" "$seed"
    done
  done
done

scripts/run_offline2online.py --mode plot
scripts/run_offline2online.py --mode status
echo "[$(stamp)] stageC queue completed"

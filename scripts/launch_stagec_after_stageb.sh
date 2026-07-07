#!/usr/bin/env bash
set -euo pipefail

cd /root/sb-value-flows

LOG_DIR=/root/autodl-tmp/sb-value-flows-runs/offline2online_single4090/logs
LOG_FILE="$LOG_DIR/launch_stagec_after_stageb.log"
RUNS_CSV=/root/sb-value-flows/results/offline2online_runs.csv
LOCK_FILE=/tmp/offline2online_launch_stagec_after_stageb.lock
mkdir -p "$LOG_DIR"

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  exit 0
fi

stamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

active_main_py() {
  ps -eo pid=,comm=,args= | awk '$2 ~ /^(python|conda|main.py)/ && index($0, "main.py") { print; found = 1 } END { exit(found ? 0 : 1) }'
}

stageb_complete() {
  scripts/run_offline2online.py --mode collect >/dev/null
  awk -F, '
    NR > 1 && $7 == "2" && $21 == "screening" && ($10 == "completed" || $10 == "completed_1m") {
      key = $1 "/" $4
      done[key] = 1
    }
    END {
      split("cube-double/ours cube-double/value_flows cube-double/fql puzzle-4x4/ours puzzle-4x4/value_flows puzzle-4x4/fql scene/ours scene/value_flows scene/fql", req, " ")
      for (i in req) {
        if (!(req[i] in done)) {
          exit 1
        }
      }
      exit 0
    }
  ' "$RUNS_CSV"
}

{
  echo "[$(stamp)] Stage C launcher started"
  while true; do
    if active_main_py >/dev/null; then
      echo "[$(stamp)] active main.py; waiting"
      sleep 300
      continue
    fi
    if pgrep -af '[c]ontinue_offline2online_stageb.sh' >/dev/null; then
      echo "[$(stamp)] Stage B queue still active; waiting"
      sleep 300
      continue
    fi
    if pgrep -af '[c]ontinue_offline2online_stagec.sh' >/dev/null; then
      echo "[$(stamp)] Stage C already active; exiting"
      exit 0
    fi
    if stageb_complete; then
      echo "[$(stamp)] Stage B screening complete; starting Stage C"
      nohup bash scripts/continue_offline2online_stagec.sh >> "$LOG_DIR/continue_stagec_queue.log" 2>&1 &
      echo "[$(stamp)] Stage C pid $!"
      exit 0
    fi
    echo "[$(stamp)] Stage B screening not complete yet; waiting"
    sleep 300
  done
} >> "$LOG_FILE" 2>&1

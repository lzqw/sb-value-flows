#!/usr/bin/env bash
set -euo pipefail

cd /root/sb-value-flows

LOG_DIR=/root/autodl-tmp/sb-value-flows-runs/offline2online_single4090/logs
LOG_FILE="$LOG_DIR/repair_stageb_queue_once.log"
LOCK_FILE=/tmp/offline2online_repair_stageb_queue_once.lock
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

{
  echo "[$(stamp)] repair monitor started"
  while active_main_py >/dev/null; do
    echo "[$(stamp)] active main.py still running; waiting"
    sleep 300
  done
  for _ in $(seq 1 20); do
    if active_main_py >/dev/null; then
      echo "[$(stamp)] new main.py started; no repair needed"
      exit 0
    fi
    if ! pgrep -af '[c]ontinue_offline2online_stageb.sh' >/dev/null; then
      echo "[$(stamp)] stageB queue not active after idle; starting patched queue"
      nohup bash scripts/continue_offline2online_stageb.sh >> "$LOG_DIR/continue_stageb_queue.log" 2>&1 &
      echo "[$(stamp)] patched stageB queue pid $!"
      exit 0
    fi
    echo "[$(stamp)] stageB queue still active; watching for handoff"
    sleep 30
  done
  echo "[$(stamp)] stageB queue stayed active during repair window; no repair needed"
} >> "$LOG_FILE" 2>&1

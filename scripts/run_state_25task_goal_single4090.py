#!/usr/bin/env python3
"""Sequential dry-run-capable runner for the state 25-task goal queue.

Default is dry-run. Use --dry_run false only after explicit user approval.
The runner reads results/state_25task_adaptive_queue.csv and executes one
main.py at a time, skipping completed/skip rows.
"""

from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
import time
import shlex
from datetime import datetime
from pathlib import Path

REPO = Path("/root/sb-value-flows")
QUEUE = REPO / "results/state_25task_adaptive_queue.csv"
OUTPUT_BASE = Path("/root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090")
LOG_DIR = OUTPUT_BASE / "logs"


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def has_main() -> bool:
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit():
            continue
        try:
            raw = (proc / "cmdline").read_bytes()
        except OSError:
            continue
        cmd = raw.replace(b"\x00", b" ").decode("utf-8", errors="ignore")
        if "main.py" in cmd and ("python" in cmd or "conda" in cmd):
            return True
    return False


def env_vars() -> dict[str, str]:
    env = os.environ.copy()
    old_ld = env.get("LD_LIBRARY_PATH", "")
    mujoco = "/root/.mujoco/mujoco210/bin"
    env.update(
        {
            "CUDA_VISIBLE_DEVICES": "0",
            "LD_LIBRARY_PATH": f"{mujoco}:{old_ld}" if old_ld else mujoco,
            "MUJOCO_GL": "egl",
            "PYOPENGL_PLATFORM": "egl",
            "SDL_VIDEODRIVER": "dummy",
            "OGBENCH_DATA_DIR": "/root/.ogbench/data",
            "XLA_PYTHON_CLIENT_PREALLOCATE": "true",
            "XLA_PYTHON_CLIENT_MEM_FRACTION": "0.90",
            "XDG_CACHE_HOME": str(OUTPUT_BASE / "cache"),
            "HOME": "/root",
            "PATH": "/root/miniconda3/bin:" + env.get("PATH", ""),
        }
    )
    return env



def git_value(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=REPO, text=True).strip()
    except Exception:
        return "UNKNOWN"


def command_with_metadata(row: dict[str, str], cmd: str) -> str:
    return "\n".join(
        [
            f"timestamp={now()}",
            f"git_branch={git_value('branch', '--show-current')}",
            f"git_head={git_value('rev-parse', 'HEAD')}",
            f"queue_id={row.get('queue_id', '')}",
            f"env={row.get('env', '')}",
            f"config_name={row.get('config_name', '')}",
            f"seed={row.get('seed', '')}",
            f"target_steps={row.get('target_steps', '')}",
            "",
            cmd,
            "",
        ]
    )


def latest_run_dir(row: dict[str, str]) -> Path | None:
    cmd = row.get('command_preview', '')
    group = ''
    for part in shlex.split(cmd):
        if part.startswith('--wandb_run_group='):
            group = part.split('=', 1)[1]
            break
    if not group:
        return None
    seed = int(row.get('seed') or 0)
    base = OUTPUT_BASE / 'exp' / group
    dirs = sorted(base.glob(f'sd{seed:03d}_*'), key=lambda path: path.stat().st_mtime)
    return dirs[-1] if dirs else None


def attach_command_to_run_dir(row: dict[str, str], text: str) -> None:
    run_dir = latest_run_dir(row)
    if run_dir is not None:
        (run_dir / 'command.txt').write_text(text, encoding='utf-8')

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry_run", default="true")
    parser.add_argument("--max_runs", type=int, default=0, help="0 means all runnable queue rows")
    args = parser.parse_args()
    dry = str(args.dry_run).lower() in {"1", "true", "yes", "y"}
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    with QUEUE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("action_type") == "skip":
                continue
            if row.get("skip_reason"):
                print(f"SKIP unavailable: {row['env']} / {row['config_name']} :: {row.get('skip_reason','')}")
                continue
            rows.append(row)
    if args.max_runs:
        rows = rows[: args.max_runs]
    print(f"dry_run={dry} runnable_rows={len(rows)} output_base={OUTPUT_BASE}")
    for idx, row in enumerate(rows, start=1):
        cmd = row.get("command_preview", "")
        print(f"[{idx}/{len(rows)}] {row['env']} / {row['config_name']} / {row['action_type']}")
        print(cmd)
        if dry:
            continue
        if has_main():
            print("Refusing to start because main.py is already running.", file=sys.stderr)
            return 2
        cmd_path = LOG_DIR / f"queue_{row['queue_id']}.command.txt"
        command_text = command_with_metadata(row, cmd)
        cmd_path.write_text(command_text, encoding="utf-8")
        started = now()
        code = subprocess.call(cmd.split(), cwd=REPO, env=env_vars())
        attach_command_to_run_dir(row, command_text)
        with (LOG_DIR / "runner.log").open("a", encoding="utf-8") as f:
            f.write(f"{started} queue_id={row['queue_id']} exit={code} {cmd}\n")
        if code != 0:
            return code
        subprocess.call(
            [
                "/root/miniconda3/bin/conda", "run", "-n", "value-flows", "python",
                "scripts/update_results_registry.py",
                "--scan_base", str(OUTPUT_BASE),
                "--server", "single4090-new",
                "--machine_tag", "seetacloud-cqa1-31499",
                "--modality", "state",
                "--stage", "state_25task_goal",
                "--output_dir", "results",
                "--commit", "false",
            ],
            cwd=REPO,
            env=env_vars(),
        )
        time.sleep(5)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Peak-polish runner for weak cells in the completed state main table.

This is not a coverage runner. It runs the user-provided priority queue for
weak cells, one 300k job at a time by default, and stops launching further
configs for a task once the current best_peak_success reaches that task's
threshold.
"""

from __future__ import annotations

import argparse
import csv
import os
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


REPO = Path("/root/sb-value-flows")
OUTPUT_BASE = Path("/root/autodl-tmp/sb-value-flows-runs/state_main_table_peak_polish_single4090")
SAVE_ROOT = OUTPUT_BASE / "exp"
LOG_DIR = OUTPUT_BASE / "logs"
CACHE_ROOT = OUTPUT_BASE / "cache"
RESULTS_CSV = REPO / "results/state_main_table_peak_polish_runs.csv"
REPORT_MD = REPO / "reports/state_main_table_peak_polish_progress.md"
MATRIX_CSV = REPO / "results/audit_state_25task_best_peak_matrix.csv"
DOMAIN_CSV = REPO / "results/audit_state_domain_best_peak_summary.csv"
MATRIX_MD = REPO / "reports/audit_state_25task_best_peak_matrix.md"


@dataclass(frozen=True)
class RunSpec:
    env: str
    domain: str
    task_id: str
    config: str
    seed: int
    target_steps: int
    threshold: float
    threshold_op: str = ">="


PRIORITY: list[RunSpec] = [
    RunSpec("puzzle-3x3-play-singletask-task3-v0", "puzzle-3x3-play", "task3", "FullSafe", 2, 300_000, 0.70),
    RunSpec("puzzle-3x3-play-singletask-task3-v0", "puzzle-3x3-play", "task3", "R2_residual_disagree_lam0p001", 2, 300_000, 0.70),
    RunSpec("puzzle-3x3-play-singletask-task3-v0", "puzzle-3x3-play", "task3", "A2_action_std_lam0p003", 2, 300_000, 0.70),
    RunSpec("puzzle-3x3-play-singletask-task3-v0", "puzzle-3x3-play", "task3", "R3_residual_disagree_typicality_lam0p001", 2, 300_000, 0.70),
    RunSpec("cube-double-play-singletask-task1-v0", "cube-double-play", "task1", "FullSafe", 2, 300_000, 0.85),
    RunSpec("cube-double-play-singletask-task1-v0", "cube-double-play", "task1", "A2_action_std_lam0p003", 2, 300_000, 0.85),
    RunSpec("cube-double-play-singletask-task5-v0", "cube-double-play", "task5", "FullSafe", 2, 300_000, 0.70),
    RunSpec("cube-double-play-singletask-task5-v0", "cube-double-play", "task5", "R2_residual_disagree_lam0p001", 2, 300_000, 0.70),
    RunSpec("puzzle-4x4-play-singletask-task5-v0", "puzzle-4x4-play", "task5", "R2_residual_disagree_lam0p001", 2, 300_000, 0.30),
    RunSpec("scene-play-singletask-task5-v0", "scene-play", "task5", "FullSafe", 2, 300_000, 0.00, ">"),
]


TASK_FLAGS: dict[str, list[str]] = {
    "cube-double-play-singletask-task2-v0": ["--agent.discount=0.995", "--agent.confidence_weight_temp=3"],
    "cube-double-play-singletask-task3-v0": ["--agent.discount=0.995", "--agent.confidence_weight_temp=3"],
    "cube-double-play-singletask-task4-v0": ["--agent.discount=0.995", "--agent.confidence_weight_temp=3"],
    "cube-double-play-singletask-task5-v0": ["--agent.discount=0.995", "--agent.confidence_weight_temp=3"],
    "puzzle-3x3-play-singletask-task4-v0": ["--agent.bcfm_lambda=0.5", "--agent.ret_agg=min"],
    "puzzle-3x3-play-singletask-task5-v0": ["--agent.bcfm_lambda=0.5", "--agent.ret_agg=min"],
    "puzzle-4x4-play-singletask-task1-v0": ["--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=100", "--agent.q_agg=min"],
    "puzzle-4x4-play-singletask-task3-v0": ["--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=100", "--agent.q_agg=min"],
    "puzzle-4x4-play-singletask-task4-v0": ["--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=100", "--agent.q_agg=min"],
    "puzzle-4x4-play-singletask-task5-v0": ["--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=100", "--agent.q_agg=min"],
    "scene-play-singletask-task4-v0": ["--agent.ret_agg=min"],
    "scene-play-singletask-task5-v0": ["--agent.ret_agg=min"],
}


COMMON_MINIMAL_SB = [
    "--agent=agents/pm_value_flows.py",
    "--agent.pm_minimal_sb=true",
    "--agent.pm_weight_type=field_kernel_norm",
    "--agent.pm_num_continuations=4",
    "--agent.pm_field_kernel_norm_temp=0.3",
    "--agent.pm_field_kernel_min_scale=1e-6",
    "--agent.pm_actor_energy_coef=0.0",
    "--agent.pm_actor_disagree_coef=0.0",
    "--agent.pm_log_sb_diagnostics=true",
]


FULLSAFE_FLAGS = [
    "--agent=agents/pm_value_flows.py",
    "--agent.pm_weight_type=field_kernel_norm",
    "--agent.pm_num_continuations=4",
    "--agent.pm_field_kernel_norm_temp=0.3",
    "--agent.pm_field_kernel_min_scale=1e-6",
    "--agent.pm_lambda_num=0.01",
    "--agent.pm_lambda_energy=0.01",
    "--agent.pm_lambda_ess=0.01",
    "--agent.pm_actor_energy_coef=0.01",
    "--agent.pm_actor_disagree_coef=0.0",
    "--agent.pm_log_sb_diagnostics=true",
]


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def env_vars() -> dict[str, str]:
    env = os.environ.copy()
    mujoco = "/root/.mujoco/mujoco210/bin"
    old_ld = env.get("LD_LIBRARY_PATH", "")
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
            "XDG_CACHE_HOME": str(CACHE_ROOT),
            "HOME": "/root",
            "PATH": "/root/miniconda3/bin:" + env.get("PATH", ""),
        }
    )
    return env


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


def git_value(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=REPO, text=True).strip()
    except Exception:
        return "UNKNOWN"


def fnum(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def inum(value: object) -> int | None:
    number = fnum(value)
    return int(number) if number is not None else None


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def threshold_reached(value: float | None, threshold: float, op: str) -> bool:
    if value is None:
        return False
    if op == ">":
        return value > threshold
    return value >= threshold


def matrix_peak(spec: RunSpec) -> float | None:
    for row in read_csv(MATRIX_CSV):
        if row.get("domain") == spec.domain and row.get("task_id") == spec.task_id:
            return fnum(row.get("best_peak_success_any_run"))
    return None


def group_name(spec: RunSpec) -> str:
    env_part = spec.env.replace("-play-singletask-", "_").replace("-v0", "").replace("-", "_")
    return f"peakpolish_300k_{env_part}_{spec.config}_seed{spec.seed}"


def run_dir_for(spec: RunSpec) -> Path | None:
    base = SAVE_ROOT / group_name(spec)
    if not base.exists():
        return None
    dirs = sorted(base.glob(f"sd{spec.seed:03d}_*"), key=lambda path: path.stat().st_mtime)
    return dirs[-1] if dirs else None


def existing_completed_in_output(spec: RunSpec) -> bool:
    base = SAVE_ROOT / group_name(spec)
    for eval_csv in base.glob(f"sd{spec.seed:03d}_*/eval.csv"):
        rows = read_csv(eval_csv)
        if not rows:
            continue
        step = inum(rows[-1].get("step"))
        if step is not None and step >= spec.target_steps * 0.98:
            return True
    return False


def config_flags(config: str) -> list[str]:
    if config == "FullSafe":
        return FULLSAFE_FLAGS
    if config.startswith("R3"):
        return COMMON_MINIMAL_SB + [
            "--agent.pm_sb_reliability_score=flow_residual_disagree_typicality",
            "--agent.pm_sb_lambda=0.001",
            "--agent.pm_sb_reliability_normalize=std",
            "--agent.pm_sb_flow_residual_eps=0.05",
            "--agent.pm_sb_disagree_beta=0.5",
            "--agent.pm_sb_disagree_umax=3.0",
            "--agent.pm_sb_typicality_tau=1.0",
            "--agent.pm_sb_value_preserving=false",
        ]
    if config.startswith("R2"):
        return COMMON_MINIMAL_SB + [
            "--agent.pm_sb_reliability_score=flow_residual_disagree",
            "--agent.pm_sb_lambda=0.001",
            "--agent.pm_sb_reliability_normalize=std",
            "--agent.pm_sb_flow_residual_eps=0.05",
            "--agent.pm_sb_disagree_beta=0.5",
            "--agent.pm_sb_disagree_umax=3.0",
            "--agent.pm_sb_value_preserving=false",
        ]
    if config.startswith("A2"):
        return COMMON_MINIMAL_SB + [
            "--agent.pm_sb_reliability_score=action",
            "--agent.pm_sb_lambda=0.003",
            "--agent.pm_sb_reliability_normalize=std",
            "--agent.pm_sb_value_preserving=false",
        ]
    raise ValueError(f"Unsupported config: {config}")


def command(spec: RunSpec) -> list[str]:
    return [
        "conda", "run", "-n", "value-flows", "python", "main.py",
        f"--env_name={spec.env}",
        f"--seed={spec.seed}",
        f"--save_dir={SAVE_ROOT}",
        f"--wandb_run_group={group_name(spec)}",
        "--enable_wandb=0",
        f"--offline_steps={spec.target_steps}",
        "--online_steps=0",
        "--eval_interval=50000",
        "--eval_episodes=10",
        "--log_interval=25000",
        "--save_interval=999999999",
        *config_flags(spec.config),
        *TASK_FLAGS.get(spec.env, []),
    ]


def command_text(spec: RunSpec, cmd: list[str]) -> str:
    return "\n".join(
        [
            f"timestamp={now()}",
            f"git_branch={git_value('branch', '--show-current')}",
            f"git_head={git_value('rev-parse', 'HEAD')}",
            f"stage=state_main_table_peak_polish_300k",
            f"env={spec.env}",
            f"domain={spec.domain}",
            f"task_id={spec.task_id}",
            f"config_name={spec.config}",
            f"seed={spec.seed}",
            f"target_steps={spec.target_steps}",
            f"stopping_threshold={spec.threshold_op}{spec.threshold}",
            "",
            shlex.join(cmd),
            "",
        ]
    )


def refresh_state_audit_inputs() -> None:
    audit_dir = Path("/tmp/state_audit")
    audit_dir.mkdir(parents=True, exist_ok=True)
    roots = [REPO, Path("/root/autodl-tmp")]
    keywords = (
        "sb-value-flows", "value-flows", "state", "stage", "selective",
        "goodcase", "peakpolish", "puzzle", "cube", "scene", "ogbench", "single4090",
    )
    allowed_names = {"eval.csv", "train.csv", "command.txt"}
    allowed_suffixes = {".md", ".json"}
    files = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.name not in allowed_names and path.suffix not in allowed_suffixes:
                continue
            text = str(path)
            if any(token in text for token in keywords):
                files.append(text)
    files = sorted(set(files))
    (audit_dir / "all_candidate_files.txt").write_text("\n".join(files) + "\n", encoding="utf-8")
    for name, suffix in [
        ("all_eval_csv.txt", "/eval.csv"),
        ("all_train_csv.txt", "/train.csv"),
        ("all_command_txt.txt", "/command.txt"),
    ]:
        selected = [path for path in files if path.endswith(suffix)]
        (audit_dir / name).write_text("\n".join(selected) + ("\n" if selected else ""), encoding="utf-8")


def refresh_registry_and_audit() -> None:
    subprocess.call(
        [
            "/root/miniconda3/bin/conda", "run", "-n", "value-flows", "python",
            "scripts/update_results_registry.py",
            "--scan_base", str(OUTPUT_BASE),
            "--server", "single4090-new",
            "--machine_tag", "seetacloud-cqa1-31499",
            "--modality", "state",
            "--stage", "state_main_table_peak_polish_300k",
            "--output_dir", "results",
            "--commit", "false",
        ],
        cwd=REPO,
        env=env_vars(),
    )
    refresh_state_audit_inputs()
    subprocess.check_call(["/root/miniconda3/bin/python", "scripts/audit_all_state_experiments_single4090.py"], cwd=REPO, env=env_vars())


def parse_own_eval(eval_csv: Path) -> dict[str, object] | None:
    rows = read_csv(eval_csv)
    if not rows:
        return None
    last = rows[-1]
    final_step = inum(last.get("step"))
    success_points = [(inum(r.get("step")), fnum(r.get("evaluation/success") or r.get("success"))) for r in rows]
    success_points = [(step, val) for step, val in success_points if step is not None and val is not None]
    best_step, best_success = max(success_points, key=lambda item: item[1]) if success_points else ("", "")
    final_success = fnum(last.get("evaluation/success") or last.get("success"))
    drop = final_success - best_success if final_success is not None and isinstance(best_success, float) else ""
    status = "completed_300k" if final_step is not None and final_step >= 300_000 * 0.98 else "partial"
    return {
        "eval_csv": str(eval_csv),
        "train_csv": str(eval_csv.with_name("train.csv")) if eval_csv.with_name("train.csv").exists() else "",
        "command_txt": str(eval_csv.with_name("command.txt")) if eval_csv.with_name("command.txt").exists() else "",
        "final_step": final_step or "",
        "status": status,
        "final_success": final_success if final_success is not None else "",
        "final_return": last.get("evaluation/episode.return", ""),
        "final_length": last.get("evaluation/episode.length", ""),
        "best_peak_success": best_success,
        "best_peak_step": best_step,
        "drop_final_from_peak": drop,
    }


def write_progress() -> None:
    rows: list[dict[str, object]] = []
    for spec in PRIORITY:
        base = SAVE_ROOT / group_name(spec)
        for eval_csv in sorted(base.glob(f"sd{spec.seed:03d}_*/eval.csv")):
            parsed = parse_own_eval(eval_csv)
            if not parsed:
                continue
            peak = fnum(parsed.get("best_peak_success"))
            row = {
                "env": spec.env,
                "domain": spec.domain,
                "task_id": spec.task_id,
                "config_name": spec.config,
                "seed": spec.seed,
                "target_steps": spec.target_steps,
                "threshold": f"{spec.threshold_op}{spec.threshold}",
                "threshold_reached_by_run": threshold_reached(peak, spec.threshold, spec.threshold_op),
                **parsed,
            }
            rows.append(row)
    fields = [
        "env", "domain", "task_id", "config_name", "seed", "target_steps", "threshold",
        "threshold_reached_by_run", "status", "final_step", "final_success", "final_return",
        "final_length", "best_peak_success", "best_peak_step", "drop_final_from_peak",
        "eval_csv", "train_csv", "command_txt",
    ]
    write_csv(RESULTS_CSV, rows, fields)

    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# State Main Table Peak Polish Progress",
        "",
        f"- Updated: {now()}",
        f"- Output base: `{OUTPUT_BASE}`",
        f"- Runs recorded: {len(rows)}",
        "",
        "Main reporting uses `best_peak_success`. `final_success` and `drop_final_from_peak` are diagnostics.",
        "",
        "| env | config | seed | status | final_step | final_success | best_peak_success | best_peak_step | drop | threshold |",
        "|---|---|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {env} | {config_name} | {seed} | {status} | {final_step} | {final_success} | {best_peak_success} | {best_peak_step} | {drop_final_from_peak} | {threshold} |".format(**row)
        )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def next_spec() -> RunSpec | None:
    for spec in PRIORITY:
        current_peak = matrix_peak(spec)
        if threshold_reached(current_peak, spec.threshold, spec.threshold_op):
            print(f"SKIP threshold reached: {spec.domain} {spec.task_id} current_peak={current_peak} threshold={spec.threshold_op}{spec.threshold}")
            continue
        if existing_completed_in_output(spec):
            print(f"SKIP completed in peak-polish output: {spec.env} / {spec.config} / seed{spec.seed}")
            continue
        return spec
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry_run", default="true")
    parser.add_argument("--max_runs", type=int, default=1)
    args = parser.parse_args()
    dry = str(args.dry_run).lower() in {"1", "true", "yes", "y"}

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    SAVE_ROOT.mkdir(parents=True, exist_ok=True)
    for required in [MATRIX_CSV, DOMAIN_CSV, MATRIX_MD]:
        if not required.exists():
            print(f"Missing required artifact: {required}", file=sys.stderr)
            return 2

    selected: list[RunSpec] = []
    for _ in range(max(args.max_runs, 0)):
        spec = next_spec()
        if spec is None:
            break
        selected.append(spec)
        if args.max_runs:
            break

    print(f"dry_run={dry} selected={len(selected)} output_base={OUTPUT_BASE}")
    for spec in selected:
        cmd = command(spec)
        print(f"RUN {spec.env} / {spec.config} / seed{spec.seed} / {spec.target_steps}")
        print(shlex.join(cmd))
        if dry:
            continue
        if has_main():
            print("Refusing to start because main.py is already running.", file=sys.stderr)
            return 3
        text = command_text(spec, cmd)
        (LOG_DIR / "latest.command.txt").write_text(text, encoding="utf-8")
        (LOG_DIR / f"{group_name(spec)}.command.txt").write_text(text, encoding="utf-8")
        started = now()
        code = subprocess.call(cmd, cwd=REPO, env=env_vars())
        run_dir = run_dir_for(spec)
        if run_dir is not None:
            (run_dir / "command.txt").write_text(text, encoding="utf-8")
        with (LOG_DIR / "runner.log").open("a", encoding="utf-8") as f:
            f.write(f"{started} exit={code} {shlex.join(cmd)}\n")
        if code != 0:
            write_progress()
            return code
        refresh_registry_and_audit()
        write_progress()
        time.sleep(5)
    if not selected:
        write_progress()
        print("No runnable peak-polish jobs remain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

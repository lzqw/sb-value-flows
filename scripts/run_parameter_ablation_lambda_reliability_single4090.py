#!/usr/bin/env python3
"""Reliability-strength lambda ablation runner/collector for state tasks.

This runner is intentionally narrow:
- target tasks: cube-double task2, puzzle-3x3 task4
- target lambdas: 0, 0.3, 1, 3 mapped to pm_sb_lambda values
- seed: 2
- default screening horizon: 500k

It reuses existing completed_1m R3 lambda=1 data for cube-double task2 when
available, and never launches coverage or method-component ablations.
"""

from __future__ import annotations

import argparse
import csv
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


REPO = Path("/root/sb-value-flows")
OUTPUT_BASE = Path("/root/autodl-tmp/sb-value-flows-runs/parameter_ablation_lambda_reliability_single4090")
SAVE_ROOT = OUTPUT_BASE / "exp"
LOG_DIR = OUTPUT_BASE / "logs"
CACHE_ROOT = OUTPUT_BASE / "cache"

RESULTS_CSV = REPO / "results/parameter_ablation_lambda_reliability_runs.csv"
REPORT_MD = REPO / "reports/parameter_ablation_lambda_reliability_selection.md"
FIG_DIR = REPO / "reports/figures/parameter_ablation"
FIG_SVG = FIG_DIR / "lambda_reliability_state_ablation.svg"
FIG_PDF = FIG_DIR / "lambda_reliability_state_ablation.pdf"
AUDIT_CSV = REPO / "results/audit_all_state_runs_single4090.csv"
BASELINE_CSV = REPO / "results/valueflow_task_baselines.csv"


@dataclass(frozen=True)
class LambdaSpec:
    env: str
    domain: str
    task_id: str
    task_label: str
    lambda_label: str
    pm_sb_lambda: float
    seed: int = 2
    target_steps: int = 500_000


LAMBDA_VALUES = [
    ("0", 0.0),
    ("0.3", 3e-4),
    ("1", 1e-3),
    ("3", 3e-3),
]

TASKS = [
    ("cube-double-play-singletask-task2-v0", "cube-double-play", "task2", "Cube-double task2"),
    ("puzzle-3x3-play-singletask-task4-v0", "puzzle-3x3-play", "task4", "Puzzle-3x3 task4"),
]

PRIORITY = [
    LambdaSpec(env, domain, task_id, label, lambda_label, value)
    for env, domain, task_id, label in TASKS
    for lambda_label, value in LAMBDA_VALUES
]

TASK_FLAGS: dict[str, list[str]] = {
    "cube-double-play-singletask-task2-v0": ["--agent.discount=0.995", "--agent.confidence_weight_temp=3"],
    "puzzle-3x3-play-singletask-task4-v0": ["--agent.bcfm_lambda=0.5", "--agent.ret_agg=min"],
    "puzzle-3x3-play-singletask-task5-v0": ["--agent.bcfm_lambda=0.5", "--agent.ret_agg=min"],
}

BASE_FLAGS = [
    "--agent=agents/pm_value_flows.py",
    "--agent.pm_minimal_sb=true",
    "--agent.pm_weight_type=field_kernel_norm",
    "--agent.pm_num_continuations=4",
    "--agent.pm_field_kernel_norm_temp=0.3",
    "--agent.pm_field_kernel_min_scale=1e-6",
    "--agent.pm_actor_energy_coef=0.0",
    "--agent.pm_actor_disagree_coef=0.0",
    "--agent.pm_log_sb_diagnostics=true",
    "--agent.pm_sb_reliability_score=flow_residual_disagree_typicality",
    "--agent.pm_sb_reliability_normalize=std",
    "--agent.pm_sb_flow_residual_eps=0.05",
    "--agent.pm_sb_disagree_beta=0.5",
    "--agent.pm_sb_disagree_umax=3.0",
    "--agent.pm_sb_typicality_tau=1.0",
    "--agent.pm_sb_value_preserving=false",
]

FIELDS = [
    "task",
    "env",
    "lambda_label",
    "pm_sb_lambda",
    "seed",
    "target_steps",
    "final_step",
    "status",
    "run_kind",
    "final_success",
    "best_peak_success",
    "best_peak_step",
    "drop",
    "eval_csv",
    "train_csv",
    "command_txt",
    "run_dir",
    "used_in_paper_figure",
    "notes",
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
            cmd = (proc / "cmdline").read_bytes().replace(b"\x00", b" ").decode("utf-8", errors="ignore")
        except OSError:
            continue
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


def group_name(spec: LambdaSpec) -> str:
    env_part = spec.env.replace("-play-singletask-", "_").replace("-v0", "").replace("-", "_")
    lam_part = spec.lambda_label.replace(".", "p")
    return f"lambda_rel_500k_{env_part}_lam{lam_part}_seed{spec.seed}"


def output_run_dirs(spec: LambdaSpec) -> list[Path]:
    base = SAVE_ROOT / group_name(spec)
    if not base.exists():
        return []
    return sorted(base.glob(f"sd{spec.seed:03d}_*"), key=lambda path: path.stat().st_mtime)


def parse_eval(eval_csv: Path) -> dict[str, object] | None:
    rows = read_csv(eval_csv)
    if not rows:
        return None
    fields = rows[0].keys()

    def col(candidates: list[str]) -> str | None:
        lower = {field.lower(): field for field in fields}
        for candidate in candidates:
            if candidate.lower() in lower:
                return lower[candidate.lower()]
        for field in fields:
            lf = field.lower()
            for candidate in candidates:
                if candidate.lower() in lf:
                    return field
        return None

    step_col = col(["step", "env_step", "global_step", "total_steps"])
    success_col = col(["evaluation/success", "eval/success", "success_rate", "success"])
    return_col = col(["evaluation/episode.return", "evaluation/return", "eval/return", "return"])
    length_col = col(["evaluation/episode.length", "evaluation/length", "eval/length", "length"])
    if not step_col or not success_col:
        return None
    last = rows[-1]
    points: list[tuple[int, float, dict[str, str]]] = []
    for row in rows:
        step = inum(row.get(step_col))
        success = fnum(row.get(success_col))
        if step is not None and success is not None:
            points.append((step, success, row))
    if not points:
        return None
    best_step, best_success, best_row = max(points, key=lambda item: item[1])
    final_step = inum(last.get(step_col))
    final_success = fnum(last.get(success_col))
    drop = final_success - best_success if final_success is not None else ""
    return {
        "final_step": final_step,
        "final_success": final_success,
        "best_peak_success": best_success,
        "best_peak_step": best_step,
        "drop": drop,
        "return_final": fnum(last.get(return_col)) if return_col else "",
        "length_final": fnum(last.get(length_col)) if length_col else "",
        "points": points,
    }


def status_for(final_step: int | None, target_steps: int) -> tuple[str, str]:
    if final_step is None:
        return "failed", "failed"
    if final_step >= 980_000:
        return "completed_1m", "completed_1m"
    if final_step >= target_steps * 0.98 and target_steps == 500_000:
        return "screening_500k", "screening_500k"
    if final_step >= target_steps * 0.98:
        return "completed", "completed"
    return "partial", "partial"


def command(spec: LambdaSpec) -> list[str]:
    return [
        "conda",
        "run",
        "-n",
        "value-flows",
        "python",
        "main.py",
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
        *BASE_FLAGS,
        f"--agent.pm_sb_lambda={spec.pm_sb_lambda:g}",
        *TASK_FLAGS.get(spec.env, []),
    ]


def command_text(spec: LambdaSpec, cmd: list[str]) -> str:
    return "\n".join(
        [
            f"timestamp={now()}",
            f"git_branch={git_value('branch', '--show-current')}",
            f"git_head={git_value('rev-parse', 'HEAD')}",
            "stage=parameter_ablation_lambda_reliability",
            f"env={spec.env}",
            f"domain={spec.domain}",
            f"task_id={spec.task_id}",
            "base_config=R3_flow_residual_disagree_typicality_fixed",
            f"lambda_label={spec.lambda_label}",
            f"pm_sb_lambda={spec.pm_sb_lambda:g}",
            f"seed={spec.seed}",
            f"target_steps={spec.target_steps}",
            "",
            shlex.join(cmd),
            "",
        ]
    )


def output_completed(spec: LambdaSpec) -> bool:
    for run_dir in output_run_dirs(spec):
        parsed = parse_eval(run_dir / "eval.csv")
        if not parsed:
            continue
        final_step = parsed["final_step"]
        if isinstance(final_step, int) and final_step >= spec.target_steps * 0.98:
            return True
    return False


def existing_completed_1m_for_lambda(spec: LambdaSpec) -> bool:
    """Reuse known global completed_1m R3 lambda=1 data for matching tasks."""
    if spec.lambda_label != "1":
        return False
    for row in read_csv(AUDIT_CSV):
        if row.get("env") != spec.env or row.get("status") != "completed_1m":
            continue
        if row.get("config_name") != "R3_residual_disagree_typicality_lam0p001":
            continue
        if row.get("seed") != str(spec.seed):
            continue
        drop = fnum(row.get("drop_final_from_peak"))
        if drop is not None and drop >= -0.05:
            return True
    return False


def runnable_specs() -> list[LambdaSpec]:
    remaining = []
    for spec in PRIORITY:
        if output_completed(spec):
            print(f"SKIP output completed: {spec.env} lambda={spec.lambda_label} seed{spec.seed}")
            continue
        if existing_completed_1m_for_lambda(spec):
            print(f"SKIP reusable completed_1m: {spec.env} lambda={spec.lambda_label} seed{spec.seed}")
            continue
        remaining.append(spec)
    return remaining


def refresh_state_audit_inputs() -> None:
    audit_dir = Path("/tmp/state_audit")
    audit_dir.mkdir(parents=True, exist_ok=True)
    roots = [REPO, Path("/root/autodl-tmp")]
    keywords = (
        "sb-value-flows",
        "value-flows",
        "state",
        "stage",
        "selective",
        "goodcase",
        "peakpolish",
        "lambda",
        "ablation",
        "puzzle",
        "cube",
        "scene",
        "single4090",
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
            "/root/miniconda3/bin/conda",
            "run",
            "-n",
            "value-flows",
            "python",
            "scripts/update_results_registry.py",
            "--scan_base",
            str(OUTPUT_BASE),
            "--server",
            "single4090-new",
            "--machine_tag",
            "seetacloud-cqa1-31499",
            "--modality",
            "state",
            "--stage",
            "parameter_ablation_lambda_reliability",
            "--output_dir",
            "results",
            "--commit",
            "false",
        ],
        cwd=REPO,
        env=env_vars(),
    )
    refresh_state_audit_inputs()
    subprocess.call(["/root/miniconda3/bin/python", "scripts/audit_all_state_experiments_single4090.py"], cwd=REPO, env=env_vars())


def collect_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    seen: set[tuple[str, str, str, str]] = set()

    for spec in PRIORITY:
        for run_dir in output_run_dirs(spec):
            eval_csv = run_dir / "eval.csv"
            parsed = parse_eval(eval_csv)
            if not parsed:
                continue
            status, kind = status_for(parsed["final_step"], spec.target_steps)
            key = (spec.env, spec.lambda_label, str(spec.seed), str(eval_csv))
            seen.add(key)
            records.append(
                {
                    "task": spec.task_label,
                    "env": spec.env,
                    "lambda_label": spec.lambda_label,
                    "pm_sb_lambda": f"{spec.pm_sb_lambda:g}",
                    "seed": spec.seed,
                    "target_steps": spec.target_steps,
                    "final_step": parsed["final_step"],
                    "status": status,
                    "run_kind": kind,
                    "final_success": parsed["final_success"],
                    "best_peak_success": parsed["best_peak_success"],
                    "best_peak_step": parsed["best_peak_step"],
                    "drop": parsed["drop"],
                    "eval_csv": str(eval_csv),
                    "train_csv": str(run_dir / "train.csv") if (run_dir / "train.csv").exists() else "",
                    "command_txt": str(run_dir / "command.txt") if (run_dir / "command.txt").exists() else "",
                    "run_dir": str(run_dir),
                    "used_in_paper_figure": status in {"completed_1m", "screening_500k"},
                    "notes": "screening data; extend to 1M before final paper use" if kind == "screening_500k" else "",
                }
            )

    # Reuse existing completed_1m R3 lambda=1 records when stable.
    for row in read_csv(AUDIT_CSV):
        env = row.get("env")
        if env not in {task[0] for task in TASKS}:
            continue
        if row.get("status") != "completed_1m":
            continue
        if row.get("config_name") != "R3_residual_disagree_typicality_lam0p001":
            continue
        if row.get("seed") != "2":
            continue
        drop = fnum(row.get("drop_final_from_peak"))
        if drop is None or drop < -0.05:
            continue
        task_label = next(task[3] for task in TASKS if task[0] == env)
        eval_csv = row.get("eval_csv", "")
        key = (env, "1", row.get("seed", ""), eval_csv)
        if key in seen:
            continue
        records.append(
            {
                "task": task_label,
                "env": env,
                "lambda_label": "1",
                "pm_sb_lambda": "0.001",
                "seed": row.get("seed", ""),
                "target_steps": row.get("target_steps", ""),
                "final_step": row.get("final_step", ""),
                "status": row.get("status", ""),
                "run_kind": "completed_1m",
                "final_success": row.get("final_success", ""),
                "best_peak_success": row.get("best_peak_success", ""),
                "best_peak_step": row.get("best_peak_step", ""),
                "drop": row.get("drop_final_from_peak", ""),
                "eval_csv": eval_csv,
                "train_csv": row.get("train_csv", ""),
                "command_txt": row.get("command_txt", ""),
                "run_dir": str(Path(eval_csv).parent) if eval_csv else "",
                "used_in_paper_figure": True,
                "notes": "reused existing completed_1m R3 lambda=1 run",
            }
        )

    order = {(spec.env, spec.lambda_label): i for i, spec in enumerate(PRIORITY)}
    records.sort(key=lambda row: (order.get((str(row.get("env")), str(row.get("lambda_label"))), 999), str(row.get("run_kind"))))
    return records


def load_eval_curve(eval_csv: str) -> list[tuple[float, float]]:
    parsed_rows = read_csv(Path(eval_csv))
    if not parsed_rows:
        return []
    fields = parsed_rows[0].keys()

    def col(candidates: list[str]) -> str | None:
        lower = {field.lower(): field for field in fields}
        for candidate in candidates:
            if candidate.lower() in lower:
                return lower[candidate.lower()]
        for field in fields:
            lf = field.lower()
            for candidate in candidates:
                if candidate.lower() in lf:
                    return field
        return None

    step_col = col(["step", "env_step", "global_step", "total_steps"])
    success_col = col(["evaluation/success", "eval/success", "success_rate", "success"])
    if not step_col or not success_col:
        return []
    curve = []
    for row in parsed_rows:
        step = fnum(row.get(step_col))
        success = fnum(row.get(success_col))
        if step is not None and success is not None:
            curve.append((step, success * 100.0))
    return sorted(curve)


def baseline_map() -> dict[str, float]:
    values = {}
    for row in read_csv(BASELINE_CSV):
        env = row.get("env", "")
        val = fnum(row.get("valueflow_success_mean"))
        if val is not None:
            values[env] = val * 100.0
    values.setdefault("cube-double-play-singletask-task2-v0", 76.0)
    values.setdefault("puzzle-3x3-play-singletask-task4-v0", 84.0)
    values.setdefault("puzzle-3x3-play-singletask-task5-v0", 58.0)
    return values


def write_report_and_plot(records: list[dict[str, object]]) -> None:
    write_csv(RESULTS_CSV, records, FIELDS)
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Lambda Reliability Parameter Ablation Selection",
        "",
        f"- Updated: {now()}",
        "- Ablation parameter: `pm_sb_lambda` with fixed R3-style flow-residual-disagree-typicality reliability.",
        "- Lambda mapping: lambda=0 -> `pm_sb_lambda=0`; lambda=0.3 -> `3e-4`; lambda=1 -> `1e-3`; lambda=3 -> `3e-3`.",
        "- 500k runs are screening data and are labeled as such; completed 1M runs are preferred for paper-final use.",
        "- No collapse tasks are included.",
        "",
        "| Task | Lambda | pm_sb_lambda | Seed | Final step | Status | Run kind | Final | Best peak | Peak step | Drop | Used in figure | Run dir |",
        "|---|---:|---:|---:|---:|---|---|---:|---:|---:|---:|---|---|",
    ]
    for row in records:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row.get("task", "")),
                    str(row.get("lambda_label", "")),
                    str(row.get("pm_sb_lambda", "")),
                    str(row.get("seed", "")),
                    str(row.get("final_step", "")),
                    str(row.get("status", "")),
                    str(row.get("run_kind", "")),
                    str(row.get("final_success", "")),
                    str(row.get("best_peak_success", "")),
                    str(row.get("best_peak_step", "")),
                    str(row.get("drop", "")),
                    str(row.get("used_in_paper_figure", "")),
                    f"`{row.get('run_dir', '')}`",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Outputs",
            "",
            "- `results/parameter_ablation_lambda_reliability_runs.csv`",
            "- `reports/figures/parameter_ablation/lambda_reliability_state_ablation.svg`",
            "- `reports/figures/parameter_ablation/lambda_reliability_state_ablation.pdf`",
        ]
    )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.ticker import FuncFormatter, MultipleLocator
    except Exception as exc:
        print(f"plot skipped: {exc}")
        return

    panels = [TASKS[0], TASKS[1]]
    colors = {"0": "#4C78A8", "0.3": "#72B7B2", "1": "#F58518", "3": "#E45756"}
    baselines = baseline_map()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.5,
            "axes.labelsize": 9,
            "axes.titlesize": 10,
            "legend.fontsize": 7.5,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )

    def xfmt(x: float, _pos: object) -> str:
        return str(int(x / 1000))

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 2.65), sharey=True, constrained_layout=True)
    for ax, (env, _domain, _task_id, title) in zip(axes, panels):
        any_curve = False
        for lambda_label, _value in LAMBDA_VALUES:
            group = [
                row
                for row in records
                if row.get("env") == env
                and row.get("lambda_label") == lambda_label
                and row.get("used_in_paper_figure") in {True, "True", "true"}
                and row.get("eval_csv")
            ]
            if not group:
                continue
            curves = [load_eval_curve(str(row["eval_csv"])) for row in group]
            curves = [curve for curve in curves if curve]
            if not curves:
                continue
            any_curve = True
            if len(curves) > 1:
                common_steps = sorted(set.intersection(*(set(step for step, _ in curve) for curve in curves)))
                if not common_steps:
                    common_steps = [step for step, _ in curves[0]]
                grid = np.array(common_steps, dtype=float)
                vals = []
                for curve in curves:
                    xs = np.array([step for step, _ in curve], dtype=float)
                    ys = np.array([succ for _, succ in curve], dtype=float)
                    vals.append(np.interp(grid, xs, ys))
                arr = np.vstack(vals)
                ax.plot(grid, arr.mean(axis=0), color=colors[lambda_label], linewidth=2.0, label=f"lambda={lambda_label} (n={len(curves)})")
                ax.fill_between(grid, arr.mean(axis=0) - arr.std(axis=0), arr.mean(axis=0) + arr.std(axis=0), color=colors[lambda_label], alpha=0.18, linewidth=0)
            else:
                curve = curves[0]
                suffix = "screen" if group[0].get("run_kind") == "screening_500k" else "1M"
                ax.plot(
                    [step for step, _ in curve],
                    [succ for _, succ in curve],
                    color=colors[lambda_label],
                    linewidth=1.8,
                    marker="o",
                    markersize=3.0,
                    label=f"lambda={lambda_label} ({suffix})",
                )
        if baselines.get(env) is not None:
            ax.axhline(baselines[env], color="#3A3A3A", linestyle=(0, (4, 3)), linewidth=1.0, label="Value Flows")
        ax.set_title(title if any_curve else f"{title} (pending)")
        ax.set_xlabel("Steps (x1000)")
        ax.set_xlim(0, 1_000_000)
        ax.set_ylim(0, 100)
        ax.xaxis.set_major_locator(MultipleLocator(200000))
        ax.xaxis.set_major_formatter(FuncFormatter(xfmt))
        ax.yaxis.set_major_locator(MultipleLocator(20))
        ax.grid(True, color="#D9D9D9", linewidth=0.6, alpha=0.8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(frameon=False, loc="lower right")
    axes[0].set_ylabel("Success Rate")
    fig.savefig(FIG_SVG, bbox_inches="tight")
    fig.savefig(FIG_PDF, bbox_inches="tight")
    plt.close(fig)


def run_one(spec: LambdaSpec) -> int:
    if has_main():
        print("Refusing to start because main.py is already running.", file=sys.stderr)
        return 2
    SAVE_ROOT.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    cmd = command(spec)
    print(f"RUN {spec.env} lambda={spec.lambda_label} pm_sb_lambda={spec.pm_sb_lambda:g} seed{spec.seed} target={spec.target_steps}")
    print(shlex.join(cmd))
    code = subprocess.call(cmd, cwd=REPO, env=env_vars())
    run_dirs = output_run_dirs(spec)
    if run_dirs:
        (run_dirs[-1] / "command.txt").write_text(command_text(spec, cmd), encoding="utf-8")
    refresh_registry_and_audit()
    records = collect_records()
    write_report_and_plot(records)
    return code


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry_run", default="true")
    parser.add_argument("--max_runs", type=int, default=1)
    parser.add_argument("--plot_only", default="false")
    args = parser.parse_args()
    dry_run = str(args.dry_run).lower() == "true"
    plot_only = str(args.plot_only).lower() == "true"

    if plot_only:
        records = collect_records()
        write_report_and_plot(records)
        print(f"records={len(records)}")
        print(f"results={RESULTS_CSV}")
        print(f"report={REPORT_MD}")
        return 0

    remaining = runnable_specs()
    selected = remaining[: args.max_runs]
    print(f"dry_run={dry_run} selected={len(selected)} output_base={OUTPUT_BASE}")
    for spec in selected:
        print(
            f"NEXT {spec.env} / lambda={spec.lambda_label} / pm_sb_lambda={spec.pm_sb_lambda:g} / seed{spec.seed} / {spec.target_steps}"
        )
        print(shlex.join(command(spec)))
    if dry_run or not selected:
        if not selected:
            records = collect_records()
            write_report_and_plot(records)
            print("No runnable lambda-ablation jobs remain.")
        return 0
    for spec in selected:
        code = run_one(spec)
        if code != 0:
            return code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

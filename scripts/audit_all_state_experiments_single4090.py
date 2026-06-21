#!/usr/bin/env python3
"""Audit all single4090 state-based experiments with final and best-peak views.

This script is read-only with respect to experiment directories. It scans the
file list produced at /tmp/state_audit/all_eval_csv.txt and supplements it with
lightweight CSV result files in the repository.
"""

from __future__ import annotations

import csv
import json
import math
import os
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean


REPO = Path("/root/sb-value-flows")
RESULTS = REPO / "results"
REPORTS = REPO / "reports"
AUDIT_DIR = Path("/tmp/state_audit")
EVAL_LIST = AUDIT_DIR / "all_eval_csv.txt"
TRAIN_LIST = AUDIT_DIR / "all_train_csv.txt"
COMMAND_LIST = AUDIT_DIR / "all_command_txt.txt"

NOW = datetime.now().isoformat(timespec="seconds")

DOMAINS = {
    "cube-double-play": [0.97, 0.76, 0.73, 0.30, 0.69],
    "cube-triple-play": [0.59, 0.00, 0.07, 0.00, 0.02],
    "puzzle-3x3-play": [0.99, 0.98, 0.97, 0.84, 0.58],
    "puzzle-4x4-play": [0.36, 0.27, 0.30, 0.28, 0.13],
    "scene-play": [0.99, 0.97, 0.94, 0.07, 0.00],
}

TASKS: list[dict[str, object]] = []
for domain, baselines in DOMAINS.items():
    for idx, vf in enumerate(baselines, start=1):
        task_id = f"task{idx}"
        TASKS.append(
            {
                "domain": domain,
                "task_id": task_id,
                "env": f"{domain}-singletask-{task_id}-v0",
                "vf_baseline": vf,
            }
        )

BASELINE_BY_ENV = {str(t["env"]): float(t["vf_baseline"]) for t in TASKS}
DOMAIN_BY_ENV = {str(t["env"]): str(t["domain"]) for t in TASKS}
TASK_BY_ENV = {str(t["env"]): str(t["task_id"]) for t in TASKS}

LIGHTWEIGHT_CSVS = [
    RESULTS / "experiment_runs.csv",
    RESULTS / "eval_curves_index.csv",
    RESULTS / "task_scoreboard.csv",
    RESULTS / "single4090_selective_state_runs_latest.csv",
    RESULTS / "single4090_selective_stageB_1m_latest.csv",
    RESULTS / "single4090_stageB_after_migration_runs.csv",
    RESULTS / "single4090_stageB_task3_R2_seed_extension.csv",
    RESULTS / "state_goodcase_harvest_single4090.csv",
    RESULTS / "state_25task_coverage_matrix.csv",
]

LIGHTWEIGHT_REPORTS = [
    RESULTS / "current_results_snapshot.md",
    RESULTS / "task_scoreboard.md",
    REPORTS / "single4090_selective_state_progress.md",
    REPORTS / "single4090_stageB_after_migration_report.md",
    REPORTS / "single4090_stageB_task3_R2_seed_extension_report.md",
    REPORTS / "state_goodcase_harvest_single4090_progress.md",
    REPORTS / "state_25task_coverage_matrix.md",
    REPORTS / "state_domain_summary_table.md",
]

SUCCESS_COLUMNS = [
    "evaluation/success",
    "eval/success",
    "metrics/success",
    "success",
    "success_rate",
    "eval_success",
]
RETURN_COLUMNS = [
    "evaluation/return",
    "evaluation/episode.return",
    "eval/return",
    "episode_return",
    "return",
    "score",
    "normalized_score",
]
LENGTH_COLUMNS = [
    "evaluation/length",
    "evaluation/episode.length",
    "eval/length",
    "episode_length",
    "length",
]
STEP_COLUMNS = ["step", "env_step", "global_step", "total_steps", "gradient_step", "training/step"]

KNOWN_CONFIGS = [
    "R3_residual_disagree_typicality_lam0p001",
    "R2_residual_disagree_lam0p001",
    "A2_action_std_lam0p003",
    "A1_action_std_lam0p001",
    "MinimalSB_lam0p001",
    "MinimalSB_lam0p003",
    "MinimalSB_lam0p0003",
    "P0_particle",
    "FullSafe-light",
    "FullSafe",
    "ActorGeo",
    "R3",
    "R2",
    "A2",
    "A1",
    "P0",
]

RUN_FIELDS = [
    "run_id",
    "server",
    "machine_tag",
    "root_path",
    "eval_csv",
    "train_csv",
    "command_txt",
    "domain",
    "task_id",
    "env",
    "config_name",
    "method_group",
    "seed",
    "target_steps",
    "final_step",
    "status",
    "final_success",
    "final_return",
    "final_length",
    "best_peak_success",
    "best_peak_step",
    "best_peak_return",
    "best_peak_length",
    "peak_after_500k_success",
    "peak_after_500k_step",
    "drop_final_from_peak",
    "trajectory_short",
    "has_train_csv",
    "has_command_txt",
    "has_checkpoint",
    "notes",
    "source_kind",
    "source_file",
]


def read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]


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


def fnum(value: object) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "null"}:
        return None
    try:
        out = float(text)
    except ValueError:
        return None
    return None if math.isnan(out) else out


def inum(value: object) -> int | None:
    value = fnum(value)
    return None if value is None else int(value)


def fmt(value: object, digits: int = 3) -> str:
    value = fnum(value)
    if value is None:
        return ""
    return f"{value:.{digits}f}".rstrip("0").rstrip(".")


def find_col(cols: list[str], candidates: list[str]) -> str | None:
    lower = {c.lower(): c for c in cols}
    for cand in candidates:
        if cand.lower() in lower:
            return lower[cand.lower()]
    for col in cols:
        lc = col.lower()
        for cand in candidates:
            if cand.lower() in lc:
                return col
    return None


def infer_env(text: str) -> tuple[str, str, str]:
    normalized = text.replace("_", "-")
    for domain in DOMAINS:
        pattern = rf"{re.escape(domain)}-singletask-task([1-5])-v0"
        match = re.search(pattern, normalized, re.IGNORECASE)
        if match:
            task = f"task{match.group(1)}"
            return f"{domain}-singletask-{task}-v0", domain, task
    # Common shortened paths such as cube_double_task2.
    short = [
        ("cube-double-play", r"cube[-_]?double.*?task[-_]?([1-5])"),
        ("cube-triple-play", r"cube[-_]?triple.*?task[-_]?([1-5])"),
        ("puzzle-3x3-play", r"puzzle[-_]?3x3.*?task[-_]?([1-5])"),
        ("puzzle-4x4-play", r"puzzle[-_]?4x4.*?task[-_]?([1-5])"),
        ("scene-play", r"scene.*?task[-_]?([1-5])"),
    ]
    for domain, pattern in short:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            task = f"task{match.group(1)}"
            return f"{domain}-singletask-{task}-v0", domain, task
    return "", "", ""


def infer_config(text: str) -> str:
    lower = text.lower()
    for cfg in KNOWN_CONFIGS:
        if cfg.lower() in lower:
            return cfg
    # Fallback to the directory above sdXXX timestamp.
    parts = Path(text).parts
    for part in reversed(parts):
        if "sd00" in part or part == "eval.csv":
            continue
        if any(token in part.lower() for token in ["task", "stage", "goodcase", "fullsafe", "actorgeo"]):
            return part
    return "UNKNOWN"


def method_group(config: str) -> str:
    if not config:
        return ""
    if config.startswith("R3"):
        return "R3"
    if config.startswith("R2"):
        return "R2"
    if config.startswith("A2"):
        return "A2"
    if config.startswith("A1"):
        return "A1"
    if config.startswith("P0"):
        return "P0"
    if config.startswith("MinimalSB"):
        return "MinimalSB"
    return config.split("_")[0]


def infer_seed(text: str) -> str:
    for pattern in [r"seed[-_]?(\d+)", r"sd(\d+)", r"/s(\d+)/"]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return str(int(match.group(1)))
    return ""


def infer_target(final_step: int | None, text: str) -> int | str:
    lower = text.lower()
    if "1000000" in lower or "1m" in lower:
        return 1_000_000
    if "300000" in lower or "300k" in lower:
        return 300_000
    if final_step is None:
        return ""
    if final_step >= 980_000:
        return 1_000_000
    if final_step >= 295_000:
        return 300_000
    return final_step


def status_from_step(final_step: int | None, target: int | str) -> str:
    if final_step is None:
        return "unknown"
    target_int = int(target) if str(target).isdigit() else 0
    if target_int >= 980_000 and final_step >= int(target_int * 0.98):
        return "completed_1m"
    if target_int >= 295_000 and final_step >= int(target_int * 0.98) and final_step < 980_000:
        return "completed_300k"
    if final_step < 10_000:
        return "smoke"
    if final_step >= 980_000:
        return "completed_1m"
    if final_step >= 295_000:
        return "completed_300k"
    return "partial"


def root_path_for(path: Path) -> str:
    text = str(path)
    for root in [
        "/root/autodl-tmp/sb-value-flows-runs",
        "/root/sb-value-flows/exp",
        "/root/sb-value-flows",
        "/root/autodl-tmp",
        "/tmp",
    ]:
        if text.startswith(root):
            return root
    return "/" + (path.parts[1] if len(path.parts) > 1 else "")


def sibling(path: Path, name: str) -> str:
    candidate = path.with_name(name)
    return str(candidate) if candidate.exists() else ""


def command_for(eval_path: Path) -> str:
    here = eval_path.parent
    for parent in [here, *here.parents]:
        if parent == parent.parent:
            break
        candidate = parent / "command.txt"
        if candidate.exists():
            return str(candidate)
        if str(parent).count("/") < 3:
            break
    return ""


def has_checkpoint(eval_path: Path) -> bool:
    run_dir = eval_path.parent
    patterns = ["*.ckpt", "checkpoint*", "*.pkl", "*.msgpack", "agent_*"]
    for pattern in patterns:
        if any(run_dir.glob(pattern)):
            return True
    return False


def short_traj(points: list[tuple[int, float | None]]) -> str:
    if not points:
        return ""
    selected = []
    for idx, (step, val) in enumerate(points):
        if idx == 0 or idx == len(points) - 1 or step % 100_000 == 0:
            selected.append((step, val))
    if len(selected) > 16:
        selected = selected[:7] + [(-1, None)] + selected[-8:]
    out = []
    for step, val in selected:
        if step == -1:
            out.append("...")
        else:
            label = f"{step // 1000}k" if step >= 1000 else str(step)
            out.append(f"{label}:{fmt(val)}")
    return " -> ".join(out)


def run_id_for(env: str, config: str, seed: str, target: int | str, eval_csv: str) -> str:
    suffix = Path(eval_csv).parent.name
    base = f"single4090__audit__{env or 'UNKNOWN'}__{config or 'UNKNOWN'}__seed{seed or 'UNKNOWN'}__{target or 'UNKNOWN'}__{suffix}"
    return re.sub(r"[^A-Za-z0-9_.=-]+", "_", base)


def parse_eval(eval_csv: str) -> dict[str, object] | None:
    path = Path(eval_csv)
    try:
        rows = read_csv(path)
    except Exception as exc:
        return {
            "eval_csv": eval_csv,
            "status": "unknown",
            "notes": f"read_error={exc}",
            "source_kind": "eval_csv",
            "source_file": eval_csv,
        }
    if not rows:
        return None
    cols = list(rows[0].keys())
    step_col = find_col(cols, STEP_COLUMNS)
    succ_col = find_col(cols, SUCCESS_COLUMNS)
    ret_col = find_col(cols, RETURN_COLUMNS)
    len_col = find_col(cols, LENGTH_COLUMNS)
    notes = []
    if succ_col is None and ret_col is not None:
        notes.append("no_success_column;best_peak_uses_return")
    metric_col = succ_col or ret_col
    metric_kind = "success" if succ_col else "return"
    points: list[dict[str, float | int | None]] = []
    for idx, row in enumerate(rows):
        step = inum(row.get(step_col)) if step_col else idx + 1
        metric = fnum(row.get(metric_col)) if metric_col else None
        ret = fnum(row.get(ret_col)) if ret_col else None
        length = fnum(row.get(len_col)) if len_col else None
        points.append({"step": step, "metric": metric, "return": ret, "length": length})
    last = points[-1]
    final_step = int(last["step"]) if last["step"] is not None else None
    target = infer_target(final_step, eval_csv)
    status = status_from_step(final_step, target)
    metric_points = [p for p in points if p["metric"] is not None]
    if metric_points:
        best = max(metric_points, key=lambda p: float(p["metric"]))
    else:
        best = {"step": "", "metric": None, "return": None, "length": None}
    after_500 = [p for p in metric_points if p["step"] is not None and int(p["step"]) >= 500_000]
    peak_after = max(after_500, key=lambda p: float(p["metric"])) if after_500 else None
    final_metric = last["metric"]
    best_metric = best["metric"]
    env, domain, task_id = infer_env(eval_csv)
    config = infer_config(eval_csv)
    seed = infer_seed(eval_csv)
    train_csv = sibling(path, "train.csv")
    command_txt = command_for(path)
    if not env:
        notes.append("env_unknown")
    if metric_kind == "return":
        final_success = ""
        best_peak_success = ""
        peak_after_success = ""
    else:
        final_success = final_metric
        best_peak_success = best_metric
        peak_after_success = peak_after["metric"] if peak_after else ""
    drop = ""
    if metric_kind == "success" and final_metric is not None and best_metric is not None:
        drop = float(final_metric) - float(best_metric)
    run = {
        "run_id": run_id_for(env, config, seed, target, eval_csv),
        "server": "single4090-new",
        "machine_tag": "seetacloud-cqa1-31499",
        "root_path": root_path_for(path),
        "eval_csv": eval_csv,
        "train_csv": train_csv,
        "command_txt": command_txt,
        "domain": domain,
        "task_id": task_id,
        "env": env,
        "config_name": config,
        "method_group": method_group(config),
        "seed": seed,
        "target_steps": target,
        "final_step": final_step or "",
        "status": status,
        "final_success": final_success,
        "final_return": last["return"] if ret_col else "",
        "final_length": last["length"] if len_col else "",
        "best_peak_success": best_peak_success,
        "best_peak_step": best["step"] or "",
        "best_peak_return": best["return"] or "",
        "best_peak_length": best["length"] or "",
        "peak_after_500k_success": peak_after_success,
        "peak_after_500k_step": peak_after["step"] if peak_after else "",
        "drop_final_from_peak": drop,
        "trajectory_short": short_traj([(int(p["step"]), p["metric"]) for p in points if p["step"] is not None]),
        "has_train_csv": bool(train_csv),
        "has_command_txt": bool(command_txt),
        "has_checkpoint": has_checkpoint(path),
        "notes": ";".join(notes),
        "source_kind": "eval_csv",
        "source_file": eval_csv,
    }
    return run


def first(row: dict[str, str], names: list[str]) -> str:
    for name in names:
        if name in row and str(row[name]).strip():
            return str(row[name]).strip()
    return ""


def parse_lightweight_csv(path: Path) -> list[dict[str, object]]:
    out = []
    for row in read_csv(path):
        env = first(row, ["env"])
        if env not in BASELINE_BY_ENV:
            continue
        final_step = inum(first(row, ["final_step"]))
        final = fnum(first(row, ["success_final", "best_300k_success"]))
        best = fnum(first(row, ["success_best", "best_success", "best_overall_success"]))
        if final_step is None and final is None and best is None:
            continue
        eval_csv = first(row, ["eval_csv", "best_300k_eval_csv", "best_known_300k_eval_csv", "best_known_1M_eval_csv"])
        config = first(row, ["config_name", "config", "best_overall_config", "best_300k_config"])
        seed = first(row, ["seed", "best_overall_seed", "best_300k_seed"])
        target = inum(first(row, ["target_steps"])) or infer_target(final_step, eval_csv)
        status = first(row, ["status"])
        if status.upper() == "COMPLETED":
            status2 = status_from_step(final_step, target)
        elif final_step is not None:
            status2 = status_from_step(final_step, target)
        else:
            status2 = "unknown"
        peak_after = fnum(first(row, ["success_peak_after_500k", "peak_after_500k"]))
        best_step = inum(first(row, ["best_step"]))
        drop = ""
        if final is not None and best is not None:
            drop = final - best
        out.append(
            {
                "run_id": first(row, ["run_id"]) or run_id_for(env, config, seed, target, eval_csv or str(path)),
                "server": first(row, ["server"]) or "single4090-new",
                "machine_tag": first(row, ["machine_tag"]) or "seetacloud-cqa1-31499",
                "root_path": root_path_for(Path(eval_csv)) if eval_csv else "",
                "eval_csv": eval_csv,
                "train_csv": first(row, ["train_csv"]),
                "command_txt": first(row, ["command_txt"]),
                "domain": DOMAIN_BY_ENV[env],
                "task_id": TASK_BY_ENV[env],
                "env": env,
                "config_name": config,
                "method_group": method_group(config),
                "seed": seed,
                "target_steps": target,
                "final_step": final_step or "",
                "status": status2,
                "final_success": final if final is not None else "",
                "final_return": first(row, ["return_final", "final_return"]),
                "final_length": first(row, ["length_final", "final_length"]),
                "best_peak_success": best if best is not None else final if final is not None else "",
                "best_peak_step": best_step or final_step or "",
                "best_peak_return": "",
                "best_peak_length": "",
                "peak_after_500k_success": peak_after if peak_after is not None else "",
                "peak_after_500k_step": first(row, ["peak_step_after_500k", "peak_after_500k_step"]),
                "drop_final_from_peak": drop,
                "trajectory_short": first(row, ["trajectory", "success_trajectory"]),
                "has_train_csv": bool(first(row, ["train_csv"])),
                "has_command_txt": bool(first(row, ["command_txt"])),
                "has_checkpoint": "",
                "notes": f"lightweight_source={path.relative_to(REPO)}",
                "source_kind": "lightweight_csv",
                "source_file": str(path.relative_to(REPO)),
            }
        )
    return out


def dedupe_runs(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_key: dict[str, dict[str, object]] = {}
    for row in rows:
        eval_csv = str(row.get("eval_csv") or "")
        key = eval_csv if eval_csv else str(row.get("run_id"))
        existing = by_key.get(key)
        if existing is None:
            by_key[key] = row
            continue
        # Prefer eval_csv parsed rows because they contain full peak/trajectory.
        if existing.get("source_kind") != "eval_csv" and row.get("source_kind") == "eval_csv":
            by_key[key] = row
    return list(by_key.values())


def completed(row: dict[str, object]) -> bool:
    return str(row.get("status")) in {"completed_1m", "completed_300k"}


def sort_score(row: dict[str, object], field: str) -> tuple[float, int]:
    value = fnum(row.get(field))
    step = inum(row.get("final_step")) or 0
    return (-1.0 if value is None else value, step)


def best(rows: list[dict[str, object]], field: str) -> dict[str, object] | None:
    valid = [r for r in rows if fnum(r.get(field)) is not None]
    if not valid:
        return None
    return max(valid, key=lambda r: sort_score(r, field))


def build_matrices(runs: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    state_runs = [r for r in runs if r.get("env") in BASELINE_BY_ENV]
    by_env: dict[str, list[dict[str, object]]] = defaultdict(list)
    for run in state_runs:
        by_env[str(run["env"])].append(run)
    matrix = []
    for task in TASKS:
        env = str(task["env"])
        vf = float(task["vf_baseline"])
        rows = by_env.get(env, [])
        completed_rows = [r for r in rows if completed(r)]
        peak = best(rows, "best_peak_success")
        final = best(completed_rows, "final_success")
        peak_success = fnum(peak.get("best_peak_success")) if peak else None
        final_success = fnum(final.get("final_success")) if final else None
        if not rows:
            coverage = "no_data"
        elif not completed_rows:
            coverage = "partial_only"
        elif any(r.get("status") == "completed_1m" for r in completed_rows):
            coverage = "has_1m"
        else:
            coverage = "has_300k"
        if peak_success is not None and final_success is not None and peak_success - final_success >= 0.30:
            action = "collapse: consider state_stable_v1; keep best peak as best-eval diagnostic"
        elif peak_success is not None and peak_success >= vf:
            action = "best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation"
        elif coverage == "no_data":
            action = "missing: run 300k coverage"
        else:
            action = "covered but below VF; lower priority unless domain coverage requires it"
        matrix.append(
            {
                "domain": task["domain"],
                "task_id": task["task_id"],
                "env": env,
                "vf_baseline": vf,
                "best_peak_success_any_run": peak_success if peak else "",
                "best_peak_step_any_run": peak.get("best_peak_step", "") if peak else "",
                "best_peak_config": peak.get("config_name", "") if peak else "",
                "best_peak_seed": peak.get("seed", "") if peak else "",
                "best_peak_eval_csv": peak.get("eval_csv", "") if peak else "",
                "best_final_success_any_completed_run": final_success if final else "",
                "best_final_config": final.get("config_name", "") if final else "",
                "best_final_seed": final.get("seed", "") if final else "",
                "best_final_eval_csv": final.get("eval_csv", "") if final else "",
                "best_peak_minus_vf": "" if peak_success is None else peak_success - vf,
                "best_final_minus_vf": "" if final_success is None else final_success - vf,
                "coverage_status": coverage,
                "recommended_next_action": action,
                "run_count": len(rows),
                "completed_run_count": len(completed_rows),
            }
        )
    summary = []
    for domain in DOMAINS:
        rows = [r for r in matrix if r["domain"] == domain]
        peak_vals = [fnum(r["best_peak_success_any_run"]) for r in rows if fnum(r["best_peak_success_any_run"]) is not None]
        final_vals = [fnum(r["best_final_success_any_completed_run"]) for r in rows if fnum(r["best_final_success_any_completed_run"]) is not None]
        summary.append(
            {
                "domain": domain,
                "tasks": 5,
                "domain_best_peak_mean": fmt(mean(peak_vals)) if peak_vals else "",
                "domain_best_peak_mean_missing_as_zero": fmt(sum(peak_vals) / 5.0),
                "domain_best_peak_available_tasks": len(peak_vals),
                "domain_best_final_mean": fmt(mean(final_vals)) if final_vals else "",
                "domain_best_final_mean_missing_as_zero": fmt(sum(final_vals) / 5.0),
                "domain_best_final_available_tasks": len(final_vals),
                "missing_peak_tasks": ";".join(str(r["task_id"]) for r in rows if fnum(r["best_peak_success_any_run"]) is None),
                "missing_final_tasks": ";".join(str(r["task_id"]) for r in rows if fnum(r["best_final_success_any_completed_run"]) is None),
            }
        )
    collapses = []
    for row in state_runs:
        final = fnum(row.get("final_success"))
        peak = fnum(row.get("best_peak_success"))
        if final is None or peak is None:
            continue
        vf = BASELINE_BY_ENV.get(str(row.get("env")), 0.0)
        is_collapse = peak - final >= 0.30
        severe = peak >= 0.50 and final <= vf + 0.05 and peak - final >= 0.30
        if not (is_collapse or severe):
            continue
        collapses.append(
            {
                **{k: row.get(k, "") for k in RUN_FIELDS},
                "vf_baseline": vf,
                "collapse": is_collapse,
                "severe_collapse": severe,
                "recommended_fix": "use state_stable_v1; lower actor lr after peak; actor anchor; SB weight cap/logit clip/uniform mix; save best checkpoint but do not call it final",
            }
        )
    collapses.sort(key=lambda r: (fnum(r.get("best_peak_success")) or -1, -(fnum(r.get("final_success")) or 0)), reverse=True)
    return matrix, summary, collapses


def build_plot_data(runs: list[dict[str, object]]) -> list[dict[str, object]]:
    out = []
    state_runs = [r for r in runs if r.get("env") in BASELINE_BY_ENV and r.get("eval_csv")]
    for run in state_runs:
        path = Path(str(run["eval_csv"]))
        if not path.exists():
            continue
        rows = read_csv(path)
        if not rows:
            continue
        cols = list(rows[0].keys())
        step_col = find_col(cols, STEP_COLUMNS)
        succ_col = find_col(cols, SUCCESS_COLUMNS)
        ret_col = find_col(cols, RETURN_COLUMNS)
        len_col = find_col(cols, LENGTH_COLUMNS)
        points = []
        for idx, row in enumerate(rows):
            step = inum(row.get(step_col)) if step_col else idx + 1
            success = fnum(row.get(succ_col)) if succ_col else None
            ret = fnum(row.get(ret_col)) if ret_col else None
            length = fnum(row.get(len_col)) if len_col else None
            points.append((step, success, ret, length))
        valid = [p for p in points if p[1] is not None]
        best_step = None
        if valid:
            best_step = max(valid, key=lambda p: float(p[1]))[0]
        final_step = points[-1][0]
        for step, success, ret, length in points:
            out.append(
                {
                    "domain": run.get("domain", ""),
                    "task_id": run.get("task_id", ""),
                    "env": run.get("env", ""),
                    "config": run.get("config_name", ""),
                    "seed": run.get("seed", ""),
                    "step": step,
                    "success": "" if success is None else success,
                    "return": "" if ret is None else ret,
                    "length": "" if length is None else length,
                    "eval_csv": run.get("eval_csv", ""),
                    "is_best_peak": bool(best_step is not None and step == best_step),
                    "is_final": bool(step == final_step),
                    "vf_baseline": BASELINE_BY_ENV.get(str(run.get("env")), ""),
                }
            )
    return out


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = ["| " + " | ".join(fields) + " |", "|" + "|".join(["---"] * len(fields)) + "|"]
    for row in rows:
        vals = []
        for field in fields:
            vals.append(str(row.get(field, "")).replace("\n", " "))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def write_reports(
    runs: list[dict[str, object]],
    matrix: list[dict[str, object]],
    summary: list[dict[str, object]],
    collapses: list[dict[str, object]],
    file_counts: dict[str, int],
    missing_sources: list[str],
) -> None:
    status_counts = Counter(str(r.get("status")) for r in runs)
    root_counts = Counter(str(r.get("root_path")) for r in runs)
    peak_top = sorted([r for r in runs if fnum(r.get("best_peak_success")) is not None], key=lambda r: fnum(r.get("best_peak_success")) or -1, reverse=True)[:10]
    final_top = sorted([r for r in runs if completed(r) and fnum(r.get("final_success")) is not None], key=lambda r: fnum(r.get("final_success")) or -1, reverse=True)[:10]
    no_data = [r for r in matrix if r["coverage_status"] == "no_data"]
    report = [
        "# Audit All Single4090 State Experiments",
        "",
        f"Updated: {NOW}",
        "",
        "No training is launched by this audit. It reports both final-row and best-peak result views.",
        "",
        "## Result Definitions",
        "",
        "- `final_success` = success in the last row of eval.csv.",
        "- `best_peak_success` = highest success across all eval checkpoints in eval.csv.",
        "- `best_peak_step` = step where the highest success occurred.",
        "- `peak_after_500k_success` = highest success among eval rows with step >= 500k.",
        "- `drop_final_from_peak` = `final_success - best_peak_success`.",
        "- Partial runs keep their best peak diagnostics, but their final row is not treated as completed final.",
        "",
        "## File Scan",
        "",
        f"- Candidate files: {file_counts.get('candidate', 0)}",
        f"- eval.csv: {file_counts.get('eval', 0)}",
        f"- train.csv: {file_counts.get('train', 0)}",
        f"- command.txt: {file_counts.get('command', 0)}",
        f"- Unique audited runs: {len(runs)}",
        f"- Missing lightweight sources: {', '.join(missing_sources) if missing_sources else 'none'}",
        "",
        "## Status Counts",
        "",
    ]
    for key, value in status_counts.most_common():
        report.append(f"- {key}: {value}")
    report += ["", "## Root Path Counts", ""]
    for key, value in root_counts.most_common():
        report.append(f"- `{key}`: {value}")
    report += [
        "",
        "## Domain Summary",
        "",
        md_table(summary, ["domain", "domain_best_peak_mean", "domain_best_peak_mean_missing_as_zero", "domain_best_final_mean", "domain_best_final_mean_missing_as_zero", "domain_best_peak_available_tasks", "domain_best_final_available_tasks"]),
        "",
        "## Top 10 Best Peak Runs",
        "",
        md_table(peak_top, ["env", "config_name", "seed", "status", "best_peak_success", "best_peak_step", "final_success", "drop_final_from_peak", "eval_csv"]),
        "",
        "## Top 10 Final Completed Runs",
        "",
        md_table(final_top, ["env", "config_name", "seed", "status", "final_success", "best_peak_success", "best_peak_step", "eval_csv"]),
        "",
        "## Top 10 Collapse Cases",
        "",
        md_table(collapses[:10], ["env", "config_name", "seed", "status", "final_success", "best_peak_success", "best_peak_step", "drop_final_from_peak", "recommended_fix"]),
        "",
        "## No Data Tasks",
        "",
    ]
    if no_data:
        for row in no_data:
            report.append(f"- {row['env']}")
    else:
        report.append("- None.")
    report.append("")
    (REPORTS / "audit_all_state_experiments_single4090.md").write_text("\n".join(report), encoding="utf-8")

    matrix_report = [
        "# State 25-Task Best-Peak Matrix",
        "",
        f"Updated: {NOW}",
        "",
        "This matrix separates best-peak success from completed final success. Best peak is eligible for best-eval reporting; final remains the traditional last-row view.",
        "",
        md_table(matrix, ["domain", "task_id", "vf_baseline", "best_peak_success_any_run", "best_peak_config", "best_peak_seed", "best_peak_minus_vf", "best_final_success_any_completed_run", "best_final_config", "best_final_seed", "best_final_minus_vf", "coverage_status", "recommended_next_action"]),
        "",
    ]
    (REPORTS / "audit_state_25task_best_peak_matrix.md").write_text("\n".join(matrix_report), encoding="utf-8")

    summary_report = [
        "# State Domain Best-Peak Summary",
        "",
        f"Updated: {NOW}",
        "",
        "Domain means are computed once using per-task best peak and once using per-task best completed final. Missing-as-zero variants are included for full-domain accounting.",
        "",
        md_table(summary, ["domain", "tasks", "domain_best_peak_mean", "domain_best_peak_mean_missing_as_zero", "domain_best_peak_available_tasks", "domain_best_final_mean", "domain_best_final_mean_missing_as_zero", "domain_best_final_available_tasks", "missing_peak_tasks", "missing_final_tasks"]),
        "",
    ]
    (REPORTS / "audit_state_domain_best_peak_summary.md").write_text("\n".join(summary_report), encoding="utf-8")

    collapse_report = [
        "# State Collapse Cases",
        "",
        f"Updated: {NOW}",
        "",
        "Collapse is flagged when best_peak_success - final_success >= 0.30. Severe collapse is also flagged when best_peak_success >= 0.50 and final_success <= VF + 0.05.",
        "",
        md_table(collapses, ["env", "config_name", "seed", "status", "vf_baseline", "final_success", "best_peak_success", "best_peak_step", "drop_final_from_peak", "collapse", "severe_collapse", "recommended_fix", "eval_csv"]),
        "",
    ]
    (REPORTS / "audit_state_collapse_cases.md").write_text("\n".join(collapse_report), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    eval_paths = read_lines(EVAL_LIST)
    all_runs = []
    for path in eval_paths:
        run = parse_eval(path)
        if run is not None:
            all_runs.append(run)
    missing_sources = []
    for path in LIGHTWEIGHT_CSVS:
        if not path.exists():
            missing_sources.append(str(path.relative_to(REPO)))
            continue
        all_runs.extend(parse_lightweight_csv(path))
    for path in LIGHTWEIGHT_REPORTS:
        if not path.exists():
            missing_sources.append(str(path.relative_to(REPO)))
    runs = dedupe_runs(all_runs)
    # Keep only state envs for state result tables, but audit_all keeps unknown rows too.
    state_runs = [r for r in runs if r.get("env") in BASELINE_BY_ENV]
    state_runs.sort(key=lambda r: (str(r.get("env")), str(r.get("config_name")), str(r.get("seed")), str(r.get("eval_csv"))))
    peak_table = sorted(state_runs, key=lambda r: fnum(r.get("best_peak_success")) or -1, reverse=True)
    final_table = sorted([r for r in state_runs if completed(r)], key=lambda r: fnum(r.get("final_success")) or -1, reverse=True)
    matrix, summary, collapses = build_matrices(state_runs)
    plot_data = build_plot_data(state_runs)

    write_csv(RESULTS / "audit_all_state_runs_single4090.csv", state_runs, RUN_FIELDS)
    write_csv(RESULTS / "audit_state_best_peak_table.csv", peak_table, RUN_FIELDS)
    write_csv(RESULTS / "audit_state_final_table.csv", final_table, RUN_FIELDS)
    matrix_fields = [
        "domain",
        "task_id",
        "env",
        "vf_baseline",
        "best_peak_success_any_run",
        "best_peak_step_any_run",
        "best_peak_config",
        "best_peak_seed",
        "best_peak_eval_csv",
        "best_final_success_any_completed_run",
        "best_final_config",
        "best_final_seed",
        "best_final_eval_csv",
        "best_peak_minus_vf",
        "best_final_minus_vf",
        "coverage_status",
        "recommended_next_action",
        "run_count",
        "completed_run_count",
    ]
    write_csv(RESULTS / "audit_state_25task_best_peak_matrix.csv", matrix, matrix_fields)
    summary_fields = [
        "domain",
        "tasks",
        "domain_best_peak_mean",
        "domain_best_peak_mean_missing_as_zero",
        "domain_best_peak_available_tasks",
        "domain_best_final_mean",
        "domain_best_final_mean_missing_as_zero",
        "domain_best_final_available_tasks",
        "missing_peak_tasks",
        "missing_final_tasks",
    ]
    write_csv(RESULTS / "audit_state_domain_best_peak_summary.csv", summary, summary_fields)
    collapse_fields = RUN_FIELDS + ["vf_baseline", "collapse", "severe_collapse", "recommended_fix"]
    write_csv(RESULTS / "audit_state_collapse_cases.csv", collapses, collapse_fields)
    plot_fields = ["domain", "task_id", "env", "config", "seed", "step", "success", "return", "length", "eval_csv", "is_best_peak", "is_final", "vf_baseline"]
    write_csv(RESULTS / "plot_data_state_curves.csv", plot_data, plot_fields)
    file_counts = {
        "candidate": len(read_lines(AUDIT_DIR / "all_candidate_files.txt")),
        "eval": len(eval_paths),
        "train": len(read_lines(TRAIN_LIST)),
        "command": len(read_lines(COMMAND_LIST)),
    }
    write_reports(state_runs, matrix, summary, collapses, file_counts, missing_sources)
    print(json.dumps({
        "candidate_files": file_counts["candidate"],
        "eval_csv": file_counts["eval"],
        "train_csv": file_counts["train"],
        "command_txt": file_counts["command"],
        "unique_state_runs": len(state_runs),
        "matrix_rows": len(matrix),
        "collapse_cases": len(collapses),
        "plot_points": len(plot_data),
    }, indent=2))


if __name__ == "__main__":
    main()

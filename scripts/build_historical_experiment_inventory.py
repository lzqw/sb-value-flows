#!/usr/bin/env python3
"""Build a conservative inventory of historical experiment artifacts.

This script is read-only with respect to raw experiment directories. It scans
for eval/train/command/report files, summarizes eval.csv final rows, and marks
whether each eval file is already represented in the lightweight registry.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import shlex
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


KEYWORDS = [
    "fullsafe",
    "table3",
    "actor",
    "actorgeo",
    "light",
    "overnight",
    "bestseed",
    "puzzle",
    "minimal",
    "reliability",
    "visual_bigtable",
    "visual_matched",
    "bad_task_repair",
]

SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "wandb",
    "cache",
    "xla_cache",
    "tmp",
    "checkpoint",
    "checkpoints",
}

SUCCESS_COLUMNS = ["evaluation/success", "eval/success", "success"]
RETURN_COLUMNS = [
    "evaluation/episode.return",
    "evaluation/return",
    "eval/return",
    "return",
    "score",
    "evaluation/score",
    "normalized_score",
]
LENGTH_COLUMNS = ["evaluation/episode.length", "evaluation/length", "eval/length", "length"]
STEP_COLUMNS = ["step", "env_step", "gradient_step", "training/step"]

CONFIG_NAMES = [
    "R3_residual_disagree_typicality_lam0p001",
    "R2_residual_disagree_lam0p001",
    "A2_action_std_lam0p003",
    "A1_action_std_lam0p001",
    "MinimalSB_lam0p001",
    "MinimalSB_lam0p0003",
    "MinimalSB_lam0p003",
    "P0_particle",
    "P0",
    "FullSafe",
    "FullSafe_light",
    "PM_FullSafe_light",
    "ActorGeo",
]

FIELDS = [
    "record_type",
    "machine",
    "storage_root",
    "experiment_line",
    "matched_keywords",
    "path",
    "run_dir",
    "eval_csv",
    "train_csv",
    "command_txt",
    "flags_json",
    "related_reports",
    "env",
    "domain",
    "task_id",
    "stage",
    "protocol",
    "config_name",
    "seed",
    "target_steps",
    "target_source",
    "final_step",
    "status",
    "success_final",
    "return_final",
    "length_final",
    "success_best",
    "best_step",
    "success_peak_after_500k",
    "peak_step_after_500k",
    "curve_points",
    "in_registry",
    "registry_run_id",
    "registry_status",
    "registry_protocol",
    "timestamp_start",
    "mtime",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo_root", default="/root/sb-value-flows")
    parser.add_argument("--runs_root", default="/root/autodl-tmp/sb-value-flows-runs")
    parser.add_argument("--csv_output", default="results/historical_experiment_inventory.csv")
    parser.add_argument("--md_output", default="reports/historical_experiment_inventory.md")
    parser.add_argument("--machine", default="single4090")
    return parser.parse_args()


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def path_str(path: Path | None) -> str:
    return str(path.resolve()) if path is not None and path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})


def float_value(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        val = float(value)
    except Exception:
        return None
    if math.isnan(val):
        return None
    return val


def number_or_blank(value: Any) -> str:
    val = float_value(value)
    if val is None:
        return ""
    return f"{val:.6g}"


def int_or_blank(value: Any) -> str:
    val = float_value(value)
    if val is None:
        return ""
    return str(int(val))


def first(row: dict[str, str], columns: list[str]) -> str:
    for column in columns:
        value = row.get(column, "")
        if value != "":
            return value
    return ""


def step_value(row: dict[str, str]) -> float | None:
    return float_value(first(row, STEP_COLUMNS))


def success_value(row: dict[str, str]) -> float | None:
    return float_value(first(row, SUCCESS_COLUMNS))


def return_value(row: dict[str, str]) -> float | None:
    return float_value(first(row, RETURN_COLUMNS))


def length_value(row: dict[str, str]) -> float | None:
    return float_value(first(row, LENGTH_COLUMNS))


def iter_interesting_files(roots: list[Path]) -> tuple[list[Path], list[Path], list[Path], list[Path]]:
    evals: list[Path] = []
    trains: list[Path] = []
    commands: list[Path] = []
    reports: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for current, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".ipynb_checkpoints")]
            cur = Path(current)
            for name in files:
                lower = name.lower()
                path = cur / name
                if lower == "eval.csv":
                    evals.append(path)
                elif lower == "train.csv":
                    trains.append(path)
                elif lower == "command.txt":
                    commands.append(path)
                elif lower == "report.md" or ("report" in lower and lower.endswith(".md")):
                    reports.append(path)
    return sorted(evals), sorted(trains), sorted(commands), sorted(reports)


def find_nearby(start: Path, roots: list[Path], names: list[str], max_parents: int = 6) -> Path | None:
    current = start
    root_resolved = [r.resolve() for r in roots if r.exists()]
    for _ in range(max_parents):
        for name in names:
            candidate = current / name
            if candidate.exists():
                return candidate
        if current.parent == current:
            break
        if current.resolve() in root_resolved:
            break
        current = current.parent
    return None


def load_json(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {}


def parse_command(path: Path | None) -> dict[str, str]:
    if path is None or not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        parts = shlex.split(text)
    except Exception:
        parts = text.split()
    parsed: dict[str, str] = {}
    for part in parts:
        if not part.startswith("--"):
            continue
        key_value = part[2:].split("=", 1)
        if len(key_value) == 2:
            parsed[key_value[0]] = key_value[1]
    return parsed


def matched_keywords(path: Path) -> list[str]:
    text = str(path).lower()
    return [keyword for keyword in KEYWORDS if keyword in text]


def experiment_line_for(path: Path) -> str:
    hits = matched_keywords(path)
    if not hits:
        parts = path.parts
        if "exp" in parts:
            idx = parts.index("exp")
            if idx + 1 < len(parts):
                return parts[idx + 1]
        return "unclassified"
    if "bad_task_repair" in hits:
        return "bad_task_repair"
    if "visual_matched" in hits:
        return "visual_matched"
    if "visual_bigtable" in hits:
        return "visual_bigtable"
    if "table3" in hits:
        return "table3"
    if "fullsafe" in hits:
        return "fullsafe"
    if "actorgeo" in hits or "actor" in hits:
        return "actor"
    if "bestseed" in hits:
        return "bestseed"
    if "reliability" in hits:
        return "reliability"
    if "minimal" in hits:
        return "minimal"
    if "puzzle" in hits:
        return "puzzle"
    return hits[0]


def storage_root_for(path: Path, repo_root: Path, runs_root: Path) -> str:
    resolved = path.resolve()
    if runs_root.exists() and resolved.is_relative_to(runs_root.resolve()):
        return str(runs_root.resolve())
    if repo_root.exists() and resolved.is_relative_to(repo_root.resolve()):
        return str(repo_root.resolve())
    return str(path.anchor)


def derive_domain_task(env: str) -> tuple[str, str]:
    match = re.match(r"(.+)-singletask-(task\d+)-v\d+$", env)
    if match:
        return match.group(1), match.group(2)
    return "", ""


def infer_env(path: Path, command: dict[str, str], flags: dict[str, Any]) -> str:
    for source in (command, flags):
        value = source.get("env_name") if isinstance(source, dict) else None
        if value:
            return str(value)
    text = str(path)
    match = re.search(r"([A-Za-z0-9-]+-singletask-task\d+-v\d+)", text)
    if match:
        return match.group(1)
    short = re.search(r"(cube_double|cube_triple|puzzle_3x3|puzzle_4x4|scene)_task(\d+)", text)
    if short:
        domain = short.group(1).replace("_", "-") + "-play"
        return f"{domain}-singletask-task{short.group(2)}-v0"
    return ""


def infer_seed(path: Path, command: dict[str, str], flags: dict[str, Any]) -> str:
    for source in (command, flags):
        value = source.get("seed") if isinstance(source, dict) else None
        if value not in (None, ""):
            return str(value)
    match = re.search(r"(?:seed|sd)(\d{1,3})", str(path))
    return str(int(match.group(1))) if match else ""


def infer_stage(path: Path, command: dict[str, str], flags: dict[str, Any]) -> str:
    group = command.get("wandb_run_group") or str(flags.get("wandb_run_group") or "")
    text = group + " " + str(path)
    for candidate in [
        "stageA_300k",
        "stageB_seed2_1m",
        "stageB_seedext_1m",
        "stageB_selective_1m",
        "visual_v6_stageA_300k",
        "visual_v6_stageB_1m",
        "visual_v7_matched_1m",
        "selective_state_tuning",
    ]:
        if candidate in text:
            return candidate
    if "300k" in text:
        return "stageA_300k"
    if "1m" in text.lower() or "1000000" in text:
        return "stageB_1m"
    return ""


def infer_config(path: Path, command: dict[str, str], flags: dict[str, Any]) -> str:
    group = command.get("wandb_run_group") or str(flags.get("wandb_run_group") or "")
    text = group + " " + str(path)
    for config in sorted(CONFIG_NAMES, key=len, reverse=True):
        if config in text:
            return config
    if "pm_fullsafe_light" in text.lower() or "fullsafe_light" in text.lower():
        return "PM_FullSafe_light"
    if "fullsafe" in text.lower():
        return "FullSafe"
    if "actorgeo" in text.lower() or "actor_geo" in text.lower():
        return "ActorGeo"
    return ""


def infer_target(path: Path, command: dict[str, str], flags: dict[str, Any]) -> tuple[str, str]:
    for source_name, source in [("command", command), ("flags", flags)]:
        for key in ["offline_steps", "target_steps", "max_steps"]:
            value = source.get(key) if isinstance(source, dict) else None
            parsed = float_value(value)
            if parsed is not None and parsed > 0:
                return str(int(parsed)), f"{source_name}:{key}"
    text = str(path).lower()
    if "300k" in text:
        return "300000", "path:300k"
    if "1m" in text or "1000000" in text:
        return "1000000", "path:1m"
    match = re.search(r"(\d{6,8})[_-]?steps", text)
    if match:
        return str(int(match.group(1))), "path:steps"
    return "", "unknown"


def protocol_for(stage: str, target_steps: str, status: str) -> str:
    if status == "PARTIAL":
        return "partial"
    target = int(target_steps) if target_steps.isdigit() else 0
    if "visual_v7_matched" in stage:
        return "1m_matched_visual"
    if "300k" in stage or target == 300_000:
        return "300k_screening"
    if "1m" in stage.lower() or target >= 980_000:
        return "1m_confirmation"
    return ""


def registry_lookup(repo_root: Path) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    rows = read_csv(repo_root / "results" / "experiment_runs.csv")
    by_eval: dict[str, dict[str, str]] = {}
    by_run_dir: dict[str, dict[str, str]] = {}
    for row in rows:
        eval_csv = row.get("eval_csv", "")
        run_dir = row.get("run_dir", "")
        if eval_csv:
            by_eval[str(Path(eval_csv).resolve())] = row
        if run_dir:
            by_run_dir[str(Path(run_dir).resolve())] = row
    return by_eval, by_run_dir


def summarize_eval(eval_csv: Path, repo_root: Path, runs_root: Path, registry_eval: dict[str, dict[str, str]], registry_run_dir: dict[str, dict[str, str]]) -> dict[str, Any]:
    run_dir = eval_csv.parent
    roots = [repo_root, runs_root]
    train_csv = find_nearby(run_dir, roots, ["train.csv"])
    command_txt = find_nearby(run_dir, roots, ["command.txt"])
    flags_json = find_nearby(run_dir, roots, ["flags.json", "config.json"])
    command = parse_command(command_txt)
    flags = load_json(flags_json)
    rows = read_csv(eval_csv)
    notes: list[str] = []

    env = infer_env(eval_csv, command, flags)
    domain, task_id = derive_domain_task(env)
    stage = infer_stage(eval_csv, command, flags)
    config = infer_config(eval_csv, command, flags)
    seed = infer_seed(eval_csv, command, flags)
    target_steps, target_source = infer_target(eval_csv, command, flags)

    final_row = rows[-1] if rows else {}
    final_step = step_value(final_row)
    success_final = success_value(final_row)
    return_final = return_value(final_row)
    length_final = length_value(final_row)

    best_success = None
    best_step = None
    peak_after_500k = None
    peak_step_after_500k = None
    for row in rows:
        success = success_value(row)
        step = step_value(row)
        if success is None:
            continue
        if best_success is None or success > best_success:
            best_success = success
            best_step = step
        if step is not None and step >= 500_000:
            if peak_after_500k is None or success > peak_after_500k:
                peak_after_500k = success
                peak_step_after_500k = step

    if not rows or final_step is None:
        status = "FAILED"
        if not rows:
            notes.append("empty_or_unreadable_eval_csv")
    else:
        target = int(target_steps) if target_steps.isdigit() else 0
        if target > 0:
            status = "COMPLETED" if final_step >= target * 0.98 else "PARTIAL"
        else:
            status = "PARTIAL"
            notes.append("target_steps_unknown")

    registry_row = registry_eval.get(str(eval_csv.resolve())) or registry_run_dir.get(str(run_dir.resolve())) or {}
    in_registry = bool(registry_row)
    protocol = protocol_for(stage, target_steps, status)
    if not config:
        notes.append("config_unparsed")
    if not env:
        notes.append("env_unparsed")

    return {
        "record_type": "eval",
        "machine": "single4090",
        "storage_root": storage_root_for(eval_csv, repo_root, runs_root),
        "experiment_line": experiment_line_for(eval_csv),
        "matched_keywords": ";".join(matched_keywords(eval_csv)),
        "path": path_str(eval_csv),
        "run_dir": path_str(run_dir),
        "eval_csv": path_str(eval_csv),
        "train_csv": path_str(train_csv),
        "command_txt": path_str(command_txt),
        "flags_json": path_str(flags_json),
        "related_reports": "",
        "env": env,
        "domain": domain,
        "task_id": task_id,
        "stage": stage,
        "protocol": protocol,
        "config_name": config,
        "seed": seed,
        "target_steps": target_steps,
        "target_source": target_source,
        "final_step": int_or_blank(final_step),
        "status": status,
        "success_final": number_or_blank(success_final),
        "return_final": number_or_blank(return_final),
        "length_final": number_or_blank(length_final),
        "success_best": number_or_blank(best_success),
        "best_step": int_or_blank(best_step),
        "success_peak_after_500k": number_or_blank(peak_after_500k),
        "peak_step_after_500k": int_or_blank(peak_step_after_500k),
        "curve_points": str(len(rows)),
        "in_registry": "yes" if in_registry else "no",
        "registry_run_id": registry_row.get("run_id", ""),
        "registry_status": registry_row.get("status", ""),
        "registry_protocol": registry_row.get("protocol", ""),
        "timestamp_start": timestamp_from_path(run_dir),
        "mtime": datetime.fromtimestamp(eval_csv.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        "notes": ";".join(notes),
    }


def timestamp_from_path(path: Path) -> str:
    match = re.search(r"_(\d{8})_(\d{6})$", path.name)
    if not match:
        return ""
    date, time = match.groups()
    return f"{date[:4]}-{date[4:6]}-{date[6:]} {time[:2]}:{time[2:4]}:{time[4:]}"


def report_has_nearby_eval(report: Path, eval_dirs: set[Path]) -> bool:
    resolved = report.resolve()
    for eval_dir in eval_dirs:
        try:
            resolved.relative_to(eval_dir)
            return True
        except ValueError:
            pass
        try:
            eval_dir.relative_to(resolved.parent)
            return True
        except ValueError:
            pass
    return False


def report_row(report: Path, repo_root: Path, runs_root: Path) -> dict[str, Any]:
    return {
        "record_type": "report_without_eval",
        "machine": "single4090",
        "storage_root": storage_root_for(report, repo_root, runs_root),
        "experiment_line": experiment_line_for(report),
        "matched_keywords": ";".join(matched_keywords(report)),
        "path": path_str(report),
        "run_dir": "",
        "eval_csv": "",
        "train_csv": "",
        "command_txt": "",
        "flags_json": "",
        "related_reports": path_str(report),
        "env": infer_env(report, {}, {}),
        "domain": "",
        "task_id": "",
        "stage": infer_stage(report, {}, {}),
        "protocol": "",
        "config_name": infer_config(report, {}, {}),
        "seed": infer_seed(report, {}, {}),
        "target_steps": "",
        "target_source": "",
        "final_step": "",
        "status": "MISSING_EVAL",
        "success_final": "",
        "return_final": "",
        "length_final": "",
        "success_best": "",
        "best_step": "",
        "success_peak_after_500k": "",
        "peak_step_after_500k": "",
        "curve_points": "",
        "in_registry": "no",
        "registry_run_id": "",
        "registry_status": "",
        "registry_protocol": "",
        "timestamp_start": "",
        "mtime": datetime.fromtimestamp(report.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        "notes": "report file found but no nearby eval.csv",
    }


def table(lines: list[str], headers: list[str], rows: list[list[Any]]) -> None:
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        lines.append("| " + " | ".join(str(x) for x in row) + " |")


def generate_markdown(path: Path, rows: list[dict[str, Any]], eval_count: int, train_count: int, command_count: int, report_count: int) -> None:
    eval_rows = [r for r in rows if r["record_type"] == "eval"]
    report_rows = [r for r in rows if r["record_type"] == "report_without_eval"]
    status_counts = Counter(r["status"] for r in eval_rows)
    registry_counts = Counter(r["in_registry"] for r in eval_rows)
    by_storage_line = Counter((r["storage_root"], r["experiment_line"]) for r in eval_rows)
    by_line_status = Counter((r["experiment_line"], r["status"]) for r in eval_rows)
    partials = [r for r in eval_rows if r["status"] == "PARTIAL"]
    completed = [r for r in eval_rows if r["status"] == "COMPLETED"]
    new_rows = [r for r in eval_rows if r["in_registry"] == "no"]

    lines = [
        "# Historical Experiment Inventory",
        "",
        f"Generated: {now()}",
        "",
        "This inventory is a read-only scan of historical experiment artifacts. Completed status is assigned only when the eval final step reaches at least 98% of an inferred target step. Peak success is retained for diagnostics and is not used as final success.",
        "",
        "## Summary",
        "",
    ]
    table(
        lines,
        ["item", "count"],
        [
            ["eval.csv found", eval_count],
            ["train.csv found", train_count],
            ["command.txt found", command_count],
            ["report markdown files found", report_count],
            ["inventory rows", len(rows)],
            ["eval rows in registry", registry_counts.get("yes", 0)],
            ["eval rows not in registry", registry_counts.get("no", 0)],
            ["completed eval rows", status_counts.get("COMPLETED", 0)],
            ["partial eval rows", status_counts.get("PARTIAL", 0)],
            ["failed eval rows", status_counts.get("FAILED", 0)],
            ["report files without eval", len(report_rows)],
        ],
    )

    lines += ["", "## By Storage Root And Experiment Line", ""]
    table(
        lines,
        ["storage_root", "experiment_line", "eval_count"],
        [[root, line, count] for (root, line), count in sorted(by_storage_line.items())],
    )

    lines += ["", "## By Experiment Line And Status", ""]
    table(
        lines,
        ["experiment_line", "status", "eval_count"],
        [[line, status, count] for (line, status), count in sorted(by_line_status.items())],
    )

    lines += ["", "## New Discoveries Not In Registry", ""]
    table(
        lines,
        ["status", "experiment_line", "env", "config", "seed", "final_step", "success_final", "eval_csv"],
        [
            [r["status"], r["experiment_line"], r["env"], r["config_name"], r["seed"], r["final_step"], r["success_final"], r["eval_csv"]]
            for r in new_rows
        ],
    )

    lines += ["", "## Partial Eval Rows", ""]
    table(
        lines,
        ["experiment_line", "env", "config", "seed", "final_step", "target_steps", "success_final", "eval_csv"],
        [
            [r["experiment_line"], r["env"], r["config_name"], r["seed"], r["final_step"], r["target_steps"], r["success_final"], r["eval_csv"]]
            for r in partials
        ],
    )

    lines += ["", "## Completed Eval Rows", ""]
    table(
        lines,
        ["experiment_line", "env", "config", "seed", "final_step", "success_final", "in_registry", "eval_csv"],
        [
            [r["experiment_line"], r["env"], r["config_name"], r["seed"], r["final_step"], r["success_final"], r["in_registry"], r["eval_csv"]]
            for r in completed
        ],
    )

    lines += ["", "## Report Files Without Nearby Eval", ""]
    table(
        lines,
        ["experiment_line", "report", "mtime"],
        [[r["experiment_line"], r["path"], r["mtime"]] for r in report_rows],
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root)
    runs_root = Path(args.runs_root)
    roots = [repo_root, runs_root]
    evals, trains, commands, reports = iter_interesting_files(roots)
    registry_eval, registry_run_dir = registry_lookup(repo_root)
    rows = [summarize_eval(path, repo_root, runs_root, registry_eval, registry_run_dir) for path in evals]
    eval_dirs = {Path(row["run_dir"]).resolve() for row in rows if row.get("run_dir")}
    for report in reports:
        if not report_has_nearby_eval(report, eval_dirs):
            rows.append(report_row(report, repo_root, runs_root))
    rows.sort(key=lambda r: (r["record_type"], r["storage_root"], r["experiment_line"], r["path"]))
    csv_output = repo_root / args.csv_output
    md_output = repo_root / args.md_output
    write_csv(csv_output, rows)
    generate_markdown(md_output, rows, len(evals), len(trains), len(commands), len(reports))

    eval_rows = [r for r in rows if r["record_type"] == "eval"]
    print(f"eval_csv_found={len(evals)}")
    print(f"train_csv_found={len(trains)}")
    print(f"command_txt_found={len(commands)}")
    print(f"report_md_found={len(reports)}")
    print(f"inventory_rows={len(rows)}")
    print(f"completed={sum(1 for r in eval_rows if r['status'] == 'COMPLETED')}")
    print(f"partial={sum(1 for r in eval_rows if r['status'] == 'PARTIAL')}")
    print(f"failed={sum(1 for r in eval_rows if r['status'] == 'FAILED')}")
    print(f"in_registry={sum(1 for r in eval_rows if r['in_registry'] == 'yes')}")
    print(f"not_in_registry={sum(1 for r in eval_rows if r['in_registry'] == 'no')}")
    print(f"csv_output={csv_output}")
    print(f"md_output={md_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

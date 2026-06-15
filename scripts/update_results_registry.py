#!/usr/bin/env python3
"""Build and update lightweight experiment result registries.

The registry stores one row per run, plus curve-file indexes and task-level
scoreboards. It intentionally records paths to raw experiment files without
copying or committing those raw files.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import shlex
import statistics
import subprocess
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


BASELINE_FIELDS = [
    "env",
    "domain",
    "task_id",
    "modality",
    "valueflow_success_mean",
    "valueflow_success_std",
    "source",
    "notes",
]

EXPERIMENT_FIELDS = [
    "run_id",
    "server",
    "machine_tag",
    "modality",
    "stage",
    "protocol",
    "env",
    "domain",
    "task_id",
    "method_group",
    "config_name",
    "seed",
    "target_steps",
    "final_step",
    "status",
    "success_final",
    "return_final",
    "length_final",
    "success_best",
    "best_step",
    "success_peak_after_500k",
    "peak_step_after_500k",
    "valueflow_success_mean",
    "delta_vs_valueflow",
    "eval_csv",
    "train_csv",
    "command_txt",
    "run_dir",
    "output_base",
    "local_backup_path",
    "git_branch",
    "git_head",
    "timestamp_start",
    "timestamp_update",
    "notes",
]

CURVE_FIELDS = [
    "run_id",
    "server",
    "env",
    "config_name",
    "seed",
    "protocol",
    "status",
    "eval_csv",
    "train_csv",
    "run_dir",
    "curve_points",
    "final_step",
    "success_final",
    "success_best",
    "best_step",
    "local_backup_path",
    "notes",
]

SCOREBOARD_FIELDS = [
    "env",
    "domain",
    "task_id",
    "modality",
    "valueflow_success_mean",
    "valueflow_success_std",
    "best_300k_success",
    "best_300k_config",
    "best_300k_seed",
    "best_300k_run_id",
    "best_300k_eval_csv",
    "best_300k_delta",
    "best_1m_success_mean",
    "best_1m_success_std",
    "best_1m_success_seeds",
    "best_1m_config",
    "best_1m_run_ids",
    "best_1m_eval_csvs",
    "best_1m_delta",
    "best_overall_success",
    "best_overall_protocol",
    "best_overall_config",
    "best_overall_seed",
    "best_overall_run_id",
    "conclusion",
    "last_update",
]

DEFAULT_BASELINES = [
    ("cube-double-play-singletask-task1-v0", "cube-double-play", "task1", "state", "0.97", "0.01", "Value Flow paper", "state-based"),
    ("cube-double-play-singletask-task2-v0", "cube-double-play", "task2", "state", "0.76", "0.07", "Value Flow paper", "state-based"),
    ("cube-double-play-singletask-task3-v0", "cube-double-play", "task3", "state", "0.73", "0.04", "Value Flow paper", "state-based"),
    ("cube-double-play-singletask-task4-v0", "cube-double-play", "task4", "state", "0.30", "0.05", "Value Flow paper", "state-based"),
    ("cube-double-play-singletask-task5-v0", "cube-double-play", "task5", "state", "0.69", "0.05", "Value Flow paper", "state-based"),
    ("cube-triple-play-singletask-task1-v0", "cube-triple-play", "task1", "state", "0.59", "0.12", "Value Flow paper", "state-based"),
    ("cube-triple-play-singletask-task2-v0", "cube-triple-play", "task2", "state", "0.00", "0.00", "Value Flow paper", "state-based"),
    ("cube-triple-play-singletask-task3-v0", "cube-triple-play", "task3", "state", "0.07", "0.03", "Value Flow paper", "state-based"),
    ("cube-triple-play-singletask-task4-v0", "cube-triple-play", "task4", "state", "0.00", "0.00", "Value Flow paper", "state-based"),
    ("cube-triple-play-singletask-task5-v0", "cube-triple-play", "task5", "state", "0.02", "0.01", "Value Flow paper", "state-based"),
    ("puzzle-3x3-play-singletask-task1-v0", "puzzle-3x3-play", "task1", "state", "0.99", "0.00", "Value Flow paper", "state-based"),
    ("puzzle-3x3-play-singletask-task2-v0", "puzzle-3x3-play", "task2", "state", "0.98", "0.02", "Value Flow paper", "state-based"),
    ("puzzle-3x3-play-singletask-task3-v0", "puzzle-3x3-play", "task3", "state", "0.97", "0.01", "Value Flow paper", "state-based"),
    ("puzzle-3x3-play-singletask-task4-v0", "puzzle-3x3-play", "task4", "state", "0.84", "0.24", "Value Flow paper", "state-based"),
    ("puzzle-3x3-play-singletask-task5-v0", "puzzle-3x3-play", "task5", "state", "0.58", "0.39", "Value Flow paper", "state-based"),
    ("puzzle-4x4-play-singletask-task1-v0", "puzzle-4x4-play", "task1", "state", "0.36", "0.04", "Value Flow paper", "state-based"),
    ("puzzle-4x4-play-singletask-task2-v0", "puzzle-4x4-play", "task2", "state", "0.27", "0.04", "Value Flow paper", "state-based"),
    ("puzzle-4x4-play-singletask-task3-v0", "puzzle-4x4-play", "task3", "state", "0.30", "0.04", "Value Flow paper", "state-based"),
    ("puzzle-4x4-play-singletask-task4-v0", "puzzle-4x4-play", "task4", "state", "0.28", "0.05", "Value Flow paper", "state-based"),
    ("puzzle-4x4-play-singletask-task5-v0", "puzzle-4x4-play", "task5", "state", "0.13", "0.02", "Value Flow paper", "state-based"),
    ("scene-play-singletask-task1-v0", "scene-play", "task1", "state", "0.99", "0.00", "Value Flow paper", "state-based"),
    ("scene-play-singletask-task2-v0", "scene-play", "task2", "state", "0.97", "0.01", "Value Flow paper", "state-based"),
    ("scene-play-singletask-task3-v0", "scene-play", "task3", "state", "0.94", "0.02", "Value Flow paper", "state-based"),
    ("scene-play-singletask-task4-v0", "scene-play", "task4", "state", "0.07", "0.04", "Value Flow paper", "state-based"),
    ("scene-play-singletask-task5-v0", "scene-play", "task5", "state", "0.00", "0.00", "Value Flow paper", "state-based"),
]

CONFIG_NAMES = [
    "R3_residual_disagree_typicality_lam0p001",
    "R2_residual_disagree_lam0p001",
    "A2_action_std_lam0p003",
    "A1_action_std_lam0p001",
    "MinimalSB_lam0p001",
    "MinimalSB_lam0p0003",
    "P0_particle",
]

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scan_base", required=True)
    parser.add_argument("--server", required=True)
    parser.add_argument("--machine_tag", required=True)
    parser.add_argument("--modality", required=True)
    parser.add_argument("--stage", default="auto")
    parser.add_argument("--output_dir", default="results")
    parser.add_argument("--commit", default="false")
    return parser.parse_args()


def now_string() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def run_git(args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def number_or_blank(value: Any) -> str:
    if value is None or value == "":
        return ""
    try:
        val = float(value)
    except Exception:
        return ""
    if math.isnan(val):
        return ""
    return f"{val:.6g}"


def int_or_blank(value: Any) -> str:
    if value is None or value == "":
        return ""
    try:
        return str(int(float(value)))
    except Exception:
        return ""


def get_first(row: dict[str, str], names: list[str]) -> str:
    for name in names:
        if name in row and row[name] != "":
            return row[name]
    return ""


def float_value(value: Any) -> float | None:
    try:
        val = float(value)
    except Exception:
        return None
    if math.isnan(val):
        return None
    return val


def derive_domain_task(env: str) -> tuple[str, str]:
    match = re.match(r"(.+)-singletask-(task\d+)-v\d+$", env)
    if match:
        return match.group(1), match.group(2)
    match = re.match(r"(.+)_(task\d+)$", env)
    if match:
        return match.group(1).replace("_", "-") + "-play", match.group(2)
    return "UNKNOWN", "UNKNOWN"


def env_short_to_full(env_short: str) -> str:
    match = re.match(r"(cube_double|cube_triple|puzzle_3x3|puzzle_4x4|scene)_task(\d+)$", env_short)
    if not match:
        return env_short if env_short else "UNKNOWN"
    domain = match.group(1).replace("_", "-") + "-play"
    return f"{domain}-singletask-task{match.group(2)}-v0"


def env_full_to_short(env: str) -> str:
    match = re.match(r"(.+)-play-singletask-(task\d+)-v\d+$", env)
    if not match:
        return env.replace("-", "_")
    return f"{match.group(1).replace('-', '_')}_{match.group(2)}"


def method_group(config_name: str) -> str:
    if config_name.startswith("P0"):
        return "P0"
    if config_name.startswith("MinimalSB"):
        return "MinimalSB"
    if config_name.startswith("A1"):
        return "A1_action_std"
    if config_name.startswith("A2"):
        return "A2_action_std"
    if config_name.startswith("R2"):
        return "R2_residual_disagree"
    if config_name.startswith("R3"):
        return "R3_residual_disagree_typicality"
    return "UNKNOWN"


def parse_stage_env_config_seed(run_group: str, default_stage: str) -> dict[str, Any]:
    result: dict[str, Any] = {"stage": default_stage if default_stage != "auto" else "UNKNOWN", "env": "UNKNOWN", "config_name": "UNKNOWN", "seed": ""}
    match = re.match(r"(.+)_seed(\d+)$", run_group)
    if not match:
        return result
    prefix, seed = match.groups()
    result["seed"] = seed

    stage_candidates = [
        "stageA_300k",
        "stageB_seed2_1m",
        "stageB_seedext_1m",
        "visual_v6_stageA_300k",
        "visual_v6_stageB_1m",
        "visual_v7_matched_1m",
    ]
    stage = None
    rest = prefix
    for candidate in sorted(stage_candidates, key=len, reverse=True):
        if prefix.startswith(candidate + "_"):
            stage = candidate
            rest = prefix[len(candidate) + 1 :]
            break
    if stage is None and default_stage != "auto":
        stage = default_stage
    if stage is not None:
        result["stage"] = stage

    for config_name in CONFIG_NAMES:
        suffix = "_" + config_name
        if rest.endswith(suffix):
            env_short = rest[: -len(suffix)]
            result["env"] = env_short_to_full(env_short)
            result["config_name"] = config_name
            return result
    return result


def parse_command_txt(path: Path | None) -> dict[str, str]:
    if path is None or not path.exists():
        return {}
    try:
        text = path.read_text(errors="replace")
    except Exception:
        return {}
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


def load_json(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(errors="replace"))
    except Exception:
        return {}


def find_nearby(start: Path, scan_base: Path, names: list[str]) -> Path | None:
    current = start
    scan_base = scan_base.resolve()
    for _ in range(5):
        for name in names:
            candidate = current / name
            if candidate.exists():
                return candidate
        if current.resolve() == scan_base or current.parent == current:
            break
        current = current.parent
    return None


def infer_target_steps(stage: str, flags: dict[str, Any], command: dict[str, str], rows: list[dict[str, str]]) -> int:
    for source in (command, flags):
        for key in ("offline_steps", "target_steps"):
            if key in source and source[key] not in (None, ""):
                try:
                    return int(float(source[key]))
                except Exception:
                    pass
    if "300k" in stage:
        return 300_000
    if "1m" in stage.lower() or "1M" in stage:
        return 1_000_000
    final_step = step_value(rows[-1]) if rows else None
    return int(final_step or 0)


def protocol_for(stage: str, target_steps: int, status: str) -> str:
    if status == "PARTIAL":
        return "partial"
    if "visual_v7_matched" in stage:
        return "1m_matched_visual"
    if "300k" in stage or target_steps == 300_000:
        return "300k_screening"
    if target_steps >= 980_000 or "1m" in stage.lower():
        return "1m_confirmation"
    return "UNKNOWN"


def step_value(row: dict[str, str]) -> float | None:
    return float_value(get_first(row, STEP_COLUMNS))


def success_value(row: dict[str, str]) -> float | None:
    return float_value(get_first(row, SUCCESS_COLUMNS))


def return_value(row: dict[str, str]) -> float | None:
    return float_value(get_first(row, RETURN_COLUMNS))


def length_value(row: dict[str, str]) -> float | None:
    return float_value(get_first(row, LENGTH_COLUMNS))


def parse_timestamp_from_run_dir(run_dir: Path) -> str:
    match = re.search(r"_(\d{8})_(\d{6})$", run_dir.name)
    if not match:
        return ""
    date, time = match.groups()
    return f"{date[:4]}-{date[4:6]}-{date[6:]} {time[:2]}:{time[2:4]}:{time[4:]}"


def path_string(path: Path | None) -> str:
    return str(path.resolve()) if path is not None and path.exists() else ""


def merge_baselines(path: Path) -> list[dict[str, str]]:
    rows = read_csv(path)
    by_key: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        env = row.get("env", "")
        modality = row.get("modality", "")
        if env:
            by_key[(env, modality)] = {field: row.get(field, "") for field in BASELINE_FIELDS}
    for values in DEFAULT_BASELINES:
        row = dict(zip(BASELINE_FIELDS, values))
        by_key[(row["env"], row["modality"])] = row
    merged = sorted(by_key.values(), key=lambda r: (r["domain"], r["task_id"], r["modality"]))
    write_csv(path, BASELINE_FIELDS, merged)
    return merged


def baseline_lookup(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {(row.get("env", ""), row.get("modality", "")): row for row in rows if row.get("env")}


def load_eval_rows(eval_csv: Path) -> tuple[list[dict[str, str]], str]:
    try:
        with eval_csv.open(newline="") as f:
            return list(csv.DictReader(f)), ""
    except Exception as exc:
        return [], f"failed_to_read_eval:{exc}"


def collect_scan_rows(args: argparse.Namespace, baselines: dict[tuple[str, str], dict[str, str]]) -> list[dict[str, Any]]:
    scan_base = Path(args.scan_base)
    git_branch = run_git(["branch", "--show-current"])
    git_head = run_git(["rev-parse", "HEAD"])
    timestamp_update = now_string()
    raw_rows: list[dict[str, Any]] = []

    for eval_csv in sorted(scan_base.rglob("eval.csv")):
        run_dir = eval_csv.parent
        group_dir = run_dir.parent
        train_csv = find_nearby(run_dir, scan_base, ["train.csv"])
        command_txt = find_nearby(run_dir, scan_base, ["command.txt"])
        config_json = find_nearby(run_dir, scan_base, ["config.json", "flags.json"])
        status_txt = find_nearby(run_dir, scan_base, ["status.txt"])
        command = parse_command_txt(command_txt)
        flags = load_json(config_json)
        rows, read_error = load_eval_rows(eval_csv)

        parsed = parse_stage_env_config_seed(group_dir.name, args.stage)
        env = command.get("env_name") or str(flags.get("env_name") or parsed["env"])
        config_name = parsed["config_name"]
        seed = command.get("seed") or str(flags.get("seed") if flags.get("seed") is not None else parsed["seed"])
        stage = parsed["stage"]
        wandb_group = command.get("wandb_run_group") or str(flags.get("wandb_run_group") or "")
        if wandb_group:
            parsed_from_wandb = parse_stage_env_config_seed(wandb_group, args.stage)
            if stage == "UNKNOWN":
                stage = parsed_from_wandb["stage"]
            if env == "UNKNOWN":
                env = parsed_from_wandb["env"]
            if config_name == "UNKNOWN":
                config_name = parsed_from_wandb["config_name"]
            if not seed:
                seed = str(parsed_from_wandb["seed"])
        if args.stage != "auto" and (stage == "UNKNOWN" or stage.startswith("visual_")):
            stage = args.stage

        domain, task_id = derive_domain_task(env)
        target_steps = infer_target_steps(stage, flags, command, rows)
        final_row = rows[-1] if rows else {}
        final_step = step_value(final_row)
        success_final = success_value(final_row)
        return_final = return_value(final_row)
        length_final = length_value(final_row)
        status = "FAILED"
        if rows and final_step is not None:
            status = "COMPLETED" if target_steps and final_step >= target_steps * 0.98 else "PARTIAL"
        if status_txt is not None:
            status_text = status_txt.read_text(errors="replace").strip().upper()
            if "RUNNING" in status_text and status == "PARTIAL":
                status = "RUNNING"

        best_success = None
        best_step = None
        peak_after_500k = None
        peak_step_after_500k = None
        for row in rows:
            cur_success = success_value(row)
            cur_step = step_value(row)
            if cur_success is None:
                continue
            if best_success is None or cur_success > best_success:
                best_success = cur_success
                best_step = cur_step
            if cur_step is not None and cur_step >= 500_000:
                if peak_after_500k is None or cur_success > peak_after_500k:
                    peak_after_500k = cur_success
                    peak_step_after_500k = cur_step

        protocol = protocol_for(stage, target_steps, status)
        vf_row = baselines.get((env, args.modality), {})
        vf_mean = float_value(vf_row.get("valueflow_success_mean"))
        delta = success_final - vf_mean if success_final is not None and vf_mean is not None else None
        base_run_id = f"{args.server}__{stage}__{env}__{config_name}__seed{seed}__{target_steps}"
        notes = read_error
        if status_txt is not None:
            notes = (notes + "; " if notes else "") + status_txt.read_text(errors="replace").strip().replace("\n", " ")[:200]

        raw_rows.append(
            {
                "_base_run_id": base_run_id,
                "_run_leaf": run_dir.name,
                "run_id": base_run_id,
                "server": args.server,
                "machine_tag": args.machine_tag,
                "modality": args.modality,
                "stage": stage,
                "protocol": protocol,
                "env": env,
                "domain": domain,
                "task_id": task_id,
                "method_group": method_group(config_name),
                "config_name": config_name,
                "seed": seed,
                "target_steps": str(target_steps),
                "final_step": int_or_blank(final_step),
                "status": status,
                "success_final": number_or_blank(success_final),
                "return_final": number_or_blank(return_final),
                "length_final": number_or_blank(length_final),
                "success_best": number_or_blank(best_success),
                "best_step": int_or_blank(best_step),
                "success_peak_after_500k": number_or_blank(peak_after_500k),
                "peak_step_after_500k": int_or_blank(peak_step_after_500k),
                "valueflow_success_mean": number_or_blank(vf_mean),
                "delta_vs_valueflow": number_or_blank(delta),
                "eval_csv": path_string(eval_csv),
                "train_csv": path_string(train_csv),
                "command_txt": path_string(command_txt),
                "run_dir": str(run_dir.resolve()),
                "output_base": str(scan_base.resolve()),
                "local_backup_path": "",
                "git_branch": git_branch,
                "git_head": git_head,
                "timestamp_start": parse_timestamp_from_run_dir(run_dir),
                "timestamp_update": timestamp_update,
                "notes": notes,
                "_mtime": str(eval_csv.stat().st_mtime),
            }
        )

    base_counts = Counter(row["_base_run_id"] for row in raw_rows)
    for row in raw_rows:
        if base_counts[row["_base_run_id"]] > 1:
            row["run_id"] = f"{row['_base_run_id']}__{row['_run_leaf']}"
        row.pop("_base_run_id", None)
        row.pop("_run_leaf", None)
        row.pop("_mtime", None)
    return raw_rows


def merge_experiment_runs(path: Path, scanned_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    existing = read_csv(path)
    by_id = {row.get("run_id", ""): row for row in existing if row.get("run_id")}
    for row in scanned_rows:
        by_id[row["run_id"]] = {field: row.get(field, "") for field in EXPERIMENT_FIELDS}
    rows = list(by_id.values())
    rows.sort(key=lambda r: (r.get("server", ""), r.get("stage", ""), r.get("env", ""), r.get("config_name", ""), r.get("seed", ""), r.get("timestamp_start", ""), r.get("run_id", "")))
    write_csv(path, EXPERIMENT_FIELDS, rows)
    return rows


def write_curve_index(path: Path, experiment_rows: list[dict[str, Any]]) -> None:
    rows = []
    for row in experiment_rows:
        curve_points = ""
        eval_path = Path(row.get("eval_csv", ""))
        if eval_path.exists():
            try:
                with eval_path.open(newline="") as f:
                    curve_points = str(sum(1 for _ in csv.DictReader(f)))
            except Exception:
                curve_points = ""
        rows.append(
            {
                "run_id": row.get("run_id", ""),
                "server": row.get("server", ""),
                "env": row.get("env", ""),
                "config_name": row.get("config_name", ""),
                "seed": row.get("seed", ""),
                "protocol": row.get("protocol", ""),
                "status": row.get("status", ""),
                "eval_csv": row.get("eval_csv", ""),
                "train_csv": row.get("train_csv", ""),
                "run_dir": row.get("run_dir", ""),
                "curve_points": curve_points,
                "final_step": row.get("final_step", ""),
                "success_final": row.get("success_final", ""),
                "success_best": row.get("success_best", ""),
                "best_step": row.get("best_step", ""),
                "local_backup_path": row.get("local_backup_path", ""),
                "notes": row.get("notes", ""),
            }
        )
    write_csv(path, CURVE_FIELDS, rows)


def row_float(row: dict[str, Any], field: str) -> float | None:
    return float_value(row.get(field, ""))


def completed(row: dict[str, Any]) -> bool:
    return row.get("status") == "COMPLETED"


def sample_std(values: list[float]) -> float:
    if len(values) <= 1:
        return 0.0
    return statistics.stdev(values)


def semicolon(values: list[str]) -> str:
    return ";".join(str(v) for v in values if str(v) != "")


def build_scoreboard(experiment_rows: list[dict[str, Any]], baseline_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    baseline_by_key = baseline_lookup(baseline_rows)
    keys = set(baseline_by_key)
    for row in experiment_rows:
        if row.get("env") and row.get("modality"):
            keys.add((row["env"], row["modality"]))

    rows: list[dict[str, Any]] = []
    last_update = now_string()
    by_key: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in experiment_rows:
        by_key[(row.get("env", ""), row.get("modality", ""))].append(row)

    for env, modality in sorted(keys):
        runs = by_key.get((env, modality), [])
        baseline = baseline_by_key.get((env, modality), {})
        domain, task_id = derive_domain_task(env)
        vf_mean = row_float(baseline, "valueflow_success_mean")
        vf_std = row_float(baseline, "valueflow_success_std")

        completed_runs = [r for r in runs if completed(r) and row_float(r, "success_final") is not None]
        screening = [
            r
            for r in completed_runs
            if r.get("protocol") == "300k_screening" or int(float(r.get("target_steps") or 0)) == 300_000
        ]
        best_300k = max(screening, key=lambda r: row_float(r, "success_final") or -1, default=None)

        one_m = [
            r
            for r in completed_runs
            if int(float(r.get("target_steps") or 0)) >= 980_000 and r.get("protocol") != "300k_screening"
        ]
        by_config: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for run in one_m:
            by_config[run.get("config_name", "UNKNOWN")].append(run)
        best_config = None
        best_config_runs: list[dict[str, Any]] = []
        best_mean = None
        best_std = None
        for config_name, config_runs in by_config.items():
            vals = [row_float(r, "success_final") for r in config_runs]
            vals = [v for v in vals if v is not None]
            if not vals:
                continue
            mean = statistics.mean(vals)
            std = sample_std(vals)
            if best_mean is None or mean > best_mean:
                best_config = config_name
                best_config_runs = sorted(config_runs, key=lambda r: (int(float(r.get("seed") or 0)), r.get("run_id", "")))
                best_mean = mean
                best_std = std

        best_overall = max(completed_runs, key=lambda r: row_float(r, "success_final") or -1, default=None)

        def delta(value: float | None) -> str:
            return number_or_blank(value - vf_mean) if value is not None and vf_mean is not None else ""

        if best_mean is None:
            conclusion = "No completed 1M result"
        elif vf_mean is None:
            conclusion = "No baseline for comparison"
        elif best_mean > vf_mean:
            if (best_std or 0) > 0.15 or best_mean - vf_mean <= 0.05:
                conclusion = "Weak or seed-unstable positive"
            else:
                conclusion = "Above Value Flow baseline"
        elif best_300k is not None and (row_float(best_300k, "success_final") or 0) >= vf_mean:
            conclusion = "300k signal did not hold at 1M"
        else:
            conclusion = "Below Value Flow baseline"

        rows.append(
            {
                "env": env,
                "domain": baseline.get("domain") or domain,
                "task_id": baseline.get("task_id") or task_id,
                "modality": modality,
                "valueflow_success_mean": number_or_blank(vf_mean),
                "valueflow_success_std": number_or_blank(vf_std),
                "best_300k_success": number_or_blank(row_float(best_300k or {}, "success_final")),
                "best_300k_config": (best_300k or {}).get("config_name", ""),
                "best_300k_seed": (best_300k or {}).get("seed", ""),
                "best_300k_run_id": (best_300k or {}).get("run_id", ""),
                "best_300k_eval_csv": (best_300k or {}).get("eval_csv", ""),
                "best_300k_delta": delta(row_float(best_300k or {}, "success_final")),
                "best_1m_success_mean": number_or_blank(best_mean),
                "best_1m_success_std": number_or_blank(best_std),
                "best_1m_success_seeds": semicolon([r.get("seed", "") for r in best_config_runs]),
                "best_1m_config": best_config or "",
                "best_1m_run_ids": semicolon([r.get("run_id", "") for r in best_config_runs]),
                "best_1m_eval_csvs": semicolon([r.get("eval_csv", "") for r in best_config_runs]),
                "best_1m_delta": delta(best_mean),
                "best_overall_success": number_or_blank(row_float(best_overall or {}, "success_final")),
                "best_overall_protocol": (best_overall or {}).get("protocol", ""),
                "best_overall_config": (best_overall or {}).get("config_name", ""),
                "best_overall_seed": (best_overall or {}).get("seed", ""),
                "best_overall_run_id": (best_overall or {}).get("run_id", ""),
                "conclusion": conclusion,
                "last_update": last_update,
            }
        )
    return rows


def short_paths(paths: str) -> str:
    if not paths:
        return ""
    pieces = paths.split(";")
    shortened = []
    for piece in pieces:
        parts = Path(piece).parts
        shortened.append("/".join(parts[-4:]) if len(parts) >= 4 else piece)
    return "<br>".join(shortened)


def md_row(row: dict[str, Any]) -> list[str]:
    mean = row.get("best_1m_success_mean", "")
    std = row.get("best_1m_success_std", "")
    mean_std = f"{mean} +/- {std}" if mean else ""
    return [
        row.get("env", ""),
        row.get("valueflow_success_mean", ""),
        row.get("best_300k_success", ""),
        mean_std,
        row.get("best_1m_config", ""),
        row.get("best_1m_success_seeds", ""),
        row.get("best_1m_delta", ""),
        row.get("best_1m_run_ids", ""),
        short_paths(row.get("best_1m_eval_csvs", "")),
    ]


def markdown_table(rows: list[list[str]], headers: list[str]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    return "\n".join(lines)


def write_scoreboard_md(path: Path, scoreboard_rows: list[dict[str, Any]]) -> None:
    headers = ["env", "VF baseline", "best 300k", "best 1M mean +/- std", "config", "seeds", "delta", "run ids", "eval paths"]

    def f(row: dict[str, Any], name: str) -> float | None:
        return float_value(row.get(name, ""))

    strong = []
    weak = []
    failed = []
    for row in scoreboard_rows:
        vf = f(row, "valueflow_success_mean")
        mean = f(row, "best_1m_success_mean")
        std = f(row, "best_1m_success_std") or 0.0
        best_300k = f(row, "best_300k_success")
        if vf is None or mean is None:
            continue
        if mean > vf and mean - vf > 0.05 and std <= 0.15:
            strong.append(row)
        elif mean > vf:
            weak.append(row)
        elif best_300k is not None and best_300k >= vf:
            failed.append(row)

    lines = [
        "# Task Scoreboard",
        "",
        f"Last update: {now_string()}",
        "",
        "All comparisons use completed final eval rows. Peak success and best-in-run values are retained in CSV for diagnostics, but they do not replace final success.",
        "",
        "## Strong Positives",
        "",
        "1M mean > Value Flow baseline with modest seed variance.",
        "",
        markdown_table([md_row(r) for r in strong], headers) if strong else "_None._",
        "",
        "## Weak / Unstable Positives",
        "",
        "1M mean is above baseline but the margin is small or seed variance is large.",
        "",
        markdown_table([md_row(r) for r in weak], headers) if weak else "_None._",
        "",
        "## Failed / False Positives",
        "",
        "300k screening looked competitive, but completed 1M final success is below the Value Flow baseline.",
        "",
        markdown_table([md_row(r) for r in failed], headers) if failed else "_None._",
        "",
    ]
    path.write_text("\n".join(lines) + "\n")


def maybe_commit(enabled: str, output_dir: Path) -> None:
    if enabled.lower() not in {"true", "1", "yes"}:
        return
    files = [
        output_dir / "valueflow_task_baselines.csv",
        output_dir / "experiment_runs.csv",
        output_dir / "task_scoreboard.csv",
        output_dir / "task_scoreboard.md",
        output_dir / "eval_curves_index.csv",
    ]
    subprocess.check_call(["git", "add", *map(str, files)])
    subprocess.check_call(["git", "commit", "-m", "Update experiment results registry"])


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    baseline_path = output_dir / "valueflow_task_baselines.csv"
    experiment_path = output_dir / "experiment_runs.csv"
    curve_path = output_dir / "eval_curves_index.csv"
    scoreboard_path = output_dir / "task_scoreboard.csv"
    scoreboard_md_path = output_dir / "task_scoreboard.md"

    baseline_rows = merge_baselines(baseline_path)
    baselines = baseline_lookup(baseline_rows)
    scanned_rows = collect_scan_rows(args, baselines)
    experiment_rows = merge_experiment_runs(experiment_path, scanned_rows)
    write_curve_index(curve_path, experiment_rows)
    scoreboard_rows = build_scoreboard(experiment_rows, baseline_rows)
    write_csv(scoreboard_path, SCOREBOARD_FIELDS, scoreboard_rows)
    write_scoreboard_md(scoreboard_md_path, scoreboard_rows)
    maybe_commit(args.commit, output_dir)

    print(f"scanned_eval_csv={len(scanned_rows)}")
    print(f"experiment_runs={len(experiment_rows)}")
    print(f"scoreboard_tasks={len(scoreboard_rows)}")
    print(f"output_dir={output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

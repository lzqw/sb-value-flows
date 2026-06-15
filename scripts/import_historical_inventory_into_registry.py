#!/usr/bin/env python3
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

import update_results_registry as reg

INV = Path("results/historical_experiment_inventory.csv")
EXP = Path("results/experiment_runs.csv")
CURVES = Path("results/eval_curves_index.csv")
BASE = Path("results/valueflow_task_baselines.csv")
SCORE = Path("results/task_scoreboard.csv")
SCORE_MD = Path("results/task_scoreboard.md")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})


def main() -> int:
    inventory = read_csv(INV)
    existing = read_csv(EXP)
    existing_eval = {r.get("eval_csv", "") for r in existing if r.get("eval_csv")}
    existing_ids = {r.get("run_id", "") for r in existing if r.get("run_id")}
    added = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for item in inventory:
        eval_csv = item.get("eval_csv", "")
        if not eval_csv or eval_csv in existing_eval:
            continue
        run_id_base = "4090d__historical__" + "__".join([
            item.get("experiment_line", "unknown") or "unknown",
            item.get("env", "UNKNOWN") or "UNKNOWN",
            item.get("config_name", "UNKNOWN") or "UNKNOWN",
            "seed" + (item.get("seed", "") or "unknown"),
            item.get("target_steps", "0") or "0",
        ])
        run_id = run_id_base
        n = 2
        while run_id in existing_ids:
            run_id = f"{run_id_base}__{n}"
            n += 1
        existing_ids.add(run_id)
        existing_eval.add(eval_csv)
        row = {
            "run_id": run_id,
            "server": "4090d",
            "machine_tag": "4090d",
            "modality": "visual" if "visual" in eval_csv else "state",
            "stage": "historical_inventory_4090d",
            "protocol": item.get("protocol", ""),
            "env": item.get("env", ""),
            "domain": item.get("domain", ""),
            "task_id": item.get("task_id", ""),
            "method_group": reg.method_group(item.get("config_name", "")),
            "config_name": item.get("config_name", ""),
            "seed": item.get("seed", ""),
            "target_steps": item.get("target_steps", ""),
            "final_step": item.get("final_step", ""),
            "status": item.get("status", ""),
            "success_final": item.get("success_final", ""),
            "return_final": item.get("return_final", ""),
            "length_final": item.get("length_final", ""),
            "success_best": item.get("success_best", ""),
            "best_step": item.get("best_step", ""),
            "success_peak_after_500k": item.get("success_peak_after_500k", ""),
            "peak_step_after_500k": item.get("peak_step_after_500k", ""),
            "valueflow_success_mean": "",
            "delta_vs_valueflow": "",
            "eval_csv": eval_csv,
            "train_csv": item.get("train_csv", ""),
            "command_txt": item.get("command_txt", ""),
            "run_dir": item.get("run_dir", ""),
            "output_base": item.get("source_root", ""),
            "local_backup_path": "",
            "git_branch": "",
            "git_head": "",
            "timestamp_start": "",
            "timestamp_update": now,
            "notes": "imported_from_historical_inventory; line=" + item.get("experiment_line", "") + "; matched_keywords=" + item.get("matched_keywords", ""),
        }
        added.append(row)
    merged = existing + added
    merged.sort(key=lambda r: (r.get("server", ""), r.get("stage", ""), r.get("env", ""), r.get("config_name", ""), r.get("seed", ""), r.get("run_id", "")))
    write_csv(EXP, reg.EXPERIMENT_FIELDS, merged)
    reg.write_curve_index(CURVES, merged)
    baselines = reg.merge_baselines(BASE)
    scoreboard = reg.build_scoreboard(merged, baselines)
    reg.write_csv(SCORE, reg.SCOREBOARD_FIELDS, scoreboard)
    reg.write_scoreboard_md(SCORE_MD, scoreboard)
    print({"inventory_rows": len(inventory), "existing_before": len(existing), "added": len(added), "experiment_runs_after": len(merged)})
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

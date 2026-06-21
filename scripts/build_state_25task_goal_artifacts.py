#!/usr/bin/env python3
"""Build state 25-task coverage, summary, queue, and reports from audit CSVs."""

from __future__ import annotations

import csv
import os
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean


REPO = Path("/root/sb-value-flows")
RESULTS = REPO / "results"
REPORTS = REPO / "reports"
OUTPUT_BASE = Path("/root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090")
NOW = datetime.now().isoformat(timespec="seconds")

DOMAINS = {
    "cube-double-play": [0.97, 0.76, 0.73, 0.30, 0.69],
    "cube-triple-play": [0.59, 0.00, 0.07, 0.00, 0.02],
    "puzzle-3x3-play": [0.99, 0.98, 0.97, 0.84, 0.58],
    "puzzle-4x4-play": [0.36, 0.27, 0.30, 0.28, 0.13],
    "scene-play": [0.99, 0.97, 0.94, 0.07, 0.00],
}

TASKS: list[dict[str, object]] = []
for domain, values in DOMAINS.items():
    for idx, vf in enumerate(values, start=1):
        task_id = f"task{idx}"
        TASKS.append(
            {
                "domain": domain,
                "task_id": task_id,
                "env": f"{domain}-singletask-{task_id}-v0",
                "VF_baseline": vf,
            }
        )

LOCKED_SKIP = {
    "cube-double-play-singletask-task2-v0": "locked strong 1M R3/FullSafe; do not repeat ordinary tuning",
    "cube-double-play-singletask-task3-v0": "locked strong 1M A2; do not repeat ordinary tuning",
    "cube-double-play-singletask-task4-v0": "locked positive 1M A1; do not repeat ordinary tuning",
    "puzzle-4x4-play-singletask-task2-v0": "locked weak positive MinimalSB; do not repeat ordinary tuning",
}

FORBIDDEN_EXTENSIONS = {
    "puzzle-4x4-play-singletask-task3-v0": "do not run R2 seed1/extra ordinary seed extension without new confirmation",
}

MISSING_HIGH_BASELINE = 0.90


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
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
        return float(text)
    except ValueError:
        return None


def fmt(value: object, digits: int = 3) -> str:
    number = fnum(value)
    if number is None:
        return ""
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = ["| " + " | ".join(fields) + " |", "|" + "|".join(["---"] * len(fields)) + "|"]
    for row in rows:
        vals = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def run_score(row: dict[str, str], field: str) -> tuple[float, float]:
    value = fnum(row.get(field))
    step = fnum(row.get("final_step")) or 0.0
    return ((-1.0 if value is None else value), step)


def best_row(rows: list[dict[str, str]], field: str) -> dict[str, str] | None:
    valid = [row for row in rows if fnum(row.get(field)) is not None]
    if not valid:
        return None
    return max(valid, key=lambda row: run_score(row, field))


def method_flags(config: str) -> list[str]:
    base = [
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
    if config.startswith("R3"):
        return base + [
            "--agent.pm_sb_reliability_score=flow_residual_disagree_typicality",
            "--agent.pm_sb_lambda=0.001",
            "--agent.pm_sb_reliability_normalize=std",
            "--agent.pm_sb_flow_residual_eps=0.05",
            "--agent.pm_sb_disagree_beta=0.5",
            "--agent.pm_sb_disagree_umax=3.0",
            "--agent.pm_sb_value_preserving=false",
        ]
    if config.startswith("R2"):
        return base + [
            "--agent.pm_sb_reliability_score=flow_residual_disagree",
            "--agent.pm_sb_lambda=0.001",
            "--agent.pm_sb_reliability_normalize=std",
            "--agent.pm_sb_flow_residual_eps=0.05",
            "--agent.pm_sb_disagree_beta=0.5",
            "--agent.pm_sb_disagree_umax=3.0",
            "--agent.pm_sb_value_preserving=false",
        ]
    if config.startswith("A2"):
        return base + [
            "--agent.pm_sb_reliability_score=action",
            "--agent.pm_sb_lambda=0.003",
            "--agent.pm_sb_reliability_normalize=std",
            "--agent.pm_sb_value_preserving=false",
        ]
    if config.startswith("A1"):
        return base + [
            "--agent.pm_sb_reliability_score=action",
            "--agent.pm_sb_lambda=0.001",
            "--agent.pm_sb_reliability_normalize=std",
            "--agent.pm_sb_value_preserving=false",
        ]
    return base + [
        "--agent.pm_sb_reliability_score=action",
        "--agent.pm_sb_lambda=0.0",
        "--agent.pm_sb_reliability_normalize=none",
        "--agent.pm_sb_value_preserving=false",
    ]


def command_preview(env: str, config: str, seed: int, steps: int, action: str) -> str:
    group = "state25_" + "_".join(
        [
            action,
            env.replace("-play-singletask-", "_").replace("-v0", "").replace("-", "_"),
            config,
            f"seed{seed}",
        ]
    )
    parts = [
        "conda", "run", "-n", "value-flows", "python", "main.py",
        f"--env_name={env}",
        f"--seed={seed}",
        f"--save_dir={OUTPUT_BASE / 'exp'}",
        f"--wandb_run_group={group}",
        "--enable_wandb=0",
        f"--offline_steps={steps}",
        "--online_steps=0",
        "--eval_interval=50000",
        "--eval_episodes=10",
        "--log_interval=25000",
        "--save_interval=999999999",
    ] + method_flags(config)
    return " ".join(parts)


def build_matrix(runs: list[dict[str, str]]) -> list[dict[str, object]]:
    by_env: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in runs:
        by_env[row.get("env", "")].append(row)
    matrix: list[dict[str, object]] = []
    for task in TASKS:
        env = str(task["env"])
        vf = float(task["VF_baseline"])
        rows = by_env.get(env, [])
        completed_300k = [r for r in rows if r.get("status") == "completed_300k"]
        completed_1m = [r for r in rows if r.get("status") == "completed_1m"]
        completed = completed_300k + completed_1m
        best_300k = best_row(completed_300k, "final_success")
        best_1m = best_row(completed_1m, "final_success")
        best_peak = best_row(rows, "best_peak_success")
        best_final = best_row(completed, "final_success")
        peak_after = best_row([r for r in rows if fnum(r.get("peak_after_500k_success")) is not None], "peak_after_500k_success")
        best_peak_value = fnum(best_peak.get("best_peak_success")) if best_peak else None
        best_final_value = fnum(best_final.get("final_success")) if best_final else None
        best_1m_value = fnum(best_1m.get("final_success")) if best_1m else None
        best_300k_value = fnum(best_300k.get("final_success")) if best_300k else None
        has_task_collapse = (
            best_peak_value is not None
            and best_final_value is not None
            and best_peak_value - best_final_value >= 0.30
        )
        if not rows:
            status = "no_data"
        elif best_1m and has_task_collapse:
            status = "collapsed"
        elif best_1m:
            status = "1M_completed"
        elif best_300k and best_300k_value is not None and best_300k_value >= vf + (0.10 if vf >= 0.05 else 0.10):
            status = "candidate"
        elif best_300k:
            status = "300k_only"
        else:
            status = "partial"
        if env in LOCKED_SKIP:
            action = f"Skip: {LOCKED_SKIP[env]}"
        elif status == "no_data":
            if vf >= MISSING_HIGH_BASELINE:
                action = "Priority 4: high-baseline coverage only; run at most P0 and R2 300k."
            else:
                action = "Priority 1: no final row; run P0 and R2 300k coverage."
        elif status == "candidate":
            action = "Priority 3: good 300k final; consider 1M good-case confirmation."
        elif status == "collapsed":
            action = "Priority 2: collapse diagnostic; prefer state_stable_v1 before ordinary rerun."
        elif best_1m:
            action = "Covered by completed 1M final row; do not repeat unless explicitly requested."
        else:
            action = "Covered by completed 300k final row; lower priority unless domain coverage requires it."
        matrix.append(
            {
                "domain": task["domain"],
                "task_id": task["task_id"],
                "env": env,
                "VF_baseline": fmt(vf),
                "best_known_300k_final": fmt(best_300k_value),
                "best_known_300k_config": best_300k.get("config_name", "") if best_300k else "",
                "best_known_300k_seed": best_300k.get("seed", "") if best_300k else "",
                "best_known_1M_final": fmt(best_1m_value),
                "best_known_1M_config": best_1m.get("config_name", "") if best_1m else "",
                "best_known_1M_seed": best_1m.get("seed", "") if best_1m else "",
                "best_success": fmt(best_peak_value),
                "best_step": best_peak.get("best_peak_step", "") if best_peak else "",
                "peak_after_500k": fmt(peak_after.get("peak_after_500k_success")) if peak_after else "",
                "status": status,
                "recommended_next_action": action,
                "best_known_300k_eval_csv": best_300k.get("eval_csv", "") if best_300k else "",
                "best_known_1M_eval_csv": best_1m.get("eval_csv", "") if best_1m else "",
                "best_peak_eval_csv": best_peak.get("eval_csv", "") if best_peak else "",
            }
        )
    return matrix


def build_domain_summary(matrix: list[dict[str, object]]) -> list[dict[str, object]]:
    out = []
    for domain in DOMAINS:
        rows = [row for row in matrix if row["domain"] == domain]
        vf_avg = mean(float(row["VF_baseline"]) for row in rows)
        one_m_vals = [fnum(row["best_known_1M_final"]) for row in rows if fnum(row["best_known_1M_final"]) is not None]
        coverage_vals = []
        candidate_vals = []
        cov_missing = []
        one_m_missing = []
        for row in rows:
            one_m = fnum(row["best_known_1M_final"])
            k300 = fnum(row["best_known_300k_final"])
            if one_m is None:
                one_m_missing.append(str(row["task_id"]))
            if one_m is not None:
                coverage_vals.append(one_m)
            elif k300 is not None:
                coverage_vals.append(k300)
            else:
                cov_missing.append(str(row["task_id"]))
            candidates = [v for v in [one_m, k300] if v is not None]
            if candidates:
                candidate_vals.append(max(candidates))
        out.append(
            {
                "domain": domain,
                "tasks": 5,
                "valueflow_average": fmt(vf_avg),
                "one_m_only_average": fmt(mean(one_m_vals)) if one_m_vals else "",
                "one_m_completed_tasks": len(one_m_vals),
                "one_m_missing_tasks": ";".join(one_m_missing),
                "coverage_average_draft": fmt(mean(coverage_vals)) if coverage_vals else "",
                "coverage_available_tasks": len(coverage_vals),
                "coverage_missing_tasks": ";".join(cov_missing),
                "candidate_average_internal": fmt(mean(candidate_vals)) if candidate_vals else "",
                "candidate_available_tasks": len(candidate_vals),
            }
        )
    return out


def build_queue(matrix: list[dict[str, object]]) -> list[dict[str, object]]:
    queue = []

    def add(priority, env, action_type, config, seed, target, reason, stable=False, skip_reason=""):
        queue.append(
            {
                "queue_id": len(queue) + 1,
                "priority": priority,
                "env": env,
                "domain": next(row["domain"] for row in matrix if row["env"] == env),
                "task_id": next(row["task_id"] for row in matrix if row["env"] == env),
                "action_type": action_type,
                "config_name": config,
                "seed": seed,
                "target_steps": target,
                "reason": reason,
                "requires_state_stable_v1": str(bool(stable)).lower(),
                "skip_reason": skip_reason,
                "command_preview": "" if action_type == "skip" else command_preview(env, config, int(seed or 2), int(target or 300000), action_type),
            }
        )

    for row in matrix:
        env = str(row["env"])
        vf = fnum(row["VF_baseline"]) or 0.0
        status = str(row["status"])
        if env in LOCKED_SKIP:
            continue
        if status == "no_data":
            priority = 4 if vf >= MISSING_HIGH_BASELINE else 1
            reason = "high-baseline coverage only" if priority == 4 else "missing coverage"
            add(priority, env, "300k_coverage", "P0_particle", 2, 300000, reason)
            add(priority, env, "300k_coverage", "R2_residual_disagree_lam0p001", 2, 300000, reason)
        elif status == "candidate":
            config = str(row["best_known_300k_config"] or "P0_particle")
            add(3, env, "1m_goodcase_confirmation", config, row["best_known_300k_seed"] or 2, 1000000, "good completed 300k final; confirm final row at 1M")
        elif status == "collapsed":
            config = str(row["best_known_1M_config"] or row["best_known_300k_config"] or "P0_particle")
            add(2, env, "state_stable_v1_diagnostic", config, row["best_known_1M_seed"] or row["best_known_300k_seed"] or 2, 300000, "best/peak high but final row dropped; do not use peak as final", True, "state_stable_v1 flags not implemented in current code")

    for env, reason in LOCKED_SKIP.items():
        add(99, env, "skip", "", "", "", reason, False, reason)
    for env, reason in FORBIDDEN_EXTENSIONS.items():
        add(99, env, "skip", "", "", "", reason, False, reason)
    queue.sort(key=lambda row: (int(row["priority"]), int(row["queue_id"])))
    for idx, row in enumerate(queue, start=1):
        row["queue_id"] = idx
    return queue


def write_reports(matrix: list[dict[str, object]], summary: list[dict[str, object]], queue: list[dict[str, object]]) -> None:
    counts = Counter(str(row["status"]) for row in matrix)
    has_1m = sum(1 for row in matrix if row["best_known_1M_final"])
    has_300k_only = sum(1 for row in matrix if row["best_known_300k_final"] and not row["best_known_1M_final"])
    no_data = sum(1 for row in matrix if row["status"] == "no_data")
    candidate_rows = [row for row in matrix if row["status"] == "candidate"]
    collapse_rows = [row for row in matrix if row["status"] == "collapsed"]
    cov_fields = [
        "domain", "task_id", "env", "VF_baseline", "best_known_300k_final",
        "best_known_300k_config", "best_known_300k_seed", "best_known_1M_final",
        "best_known_1M_config", "best_known_1M_seed", "best_success", "best_step",
        "peak_after_500k", "status", "recommended_next_action",
    ]
    lines = [
        "# State 25-Task Coverage Matrix",
        "",
        f"Updated: {NOW}",
        "",
        "Final values use eval.csv last rows only. Best/peak columns are diagnostics and are not used as final performance.",
        "",
        "## Coverage Counts",
        "",
        f"- Tasks with completed 1M final: {has_1m}",
        f"- Tasks with only completed 300k final: {has_300k_only}",
        f"- No-data tasks: {no_data}",
        f"- Status counts: {dict(counts)}",
        "",
        "## Matrix",
        "",
        md_table(matrix, cov_fields),
        "",
    ]
    (REPORTS / "state_25task_coverage_matrix.md").write_text("\n".join(lines), encoding="utf-8")

    summ_fields = [
        "domain", "tasks", "valueflow_average", "one_m_only_average",
        "one_m_completed_tasks", "one_m_missing_tasks", "coverage_average_draft",
        "coverage_available_tasks", "coverage_missing_tasks",
        "candidate_average_internal", "candidate_available_tasks",
    ]
    summary_text = [
        "# State Domain Summary Table",
        "",
        f"Updated: {NOW}",
        "",
        "Draft Table-1 style state-domain summary. The 1M-only average uses completed 1M final rows only. The coverage average uses completed 1M final when available and otherwise completed 300k final. The candidate average uses each task's best current final row and is for internal screening only.",
        "",
        md_table(summary, summ_fields),
        "",
    ]
    (REPORTS / "state_domain_summary_table.md").write_text("\n".join(summary_text), encoding="utf-8")
    latex_lines = [
        "% Auto-generated draft state-domain summary. Final rows only; no best/peak in averages.",
        "\\begin{tabular}{lrrrrrr}",
        "\\hline",
        "Domain & VF & 1M Avg & 1M n & Coverage Avg & Coverage n & Candidate Avg \\\\",
        "\\hline",
    ]
    for row in summary:
        latex_lines.append(
            f"{row['domain']} & {row['valueflow_average']} & {row['one_m_only_average']} & {row['one_m_completed_tasks']} & {row['coverage_average_draft']} & {row['coverage_available_tasks']} & {row['candidate_average_internal']} \\\\"
        )
    latex_lines += ["\\hline", "\\end{tabular}", ""]
    (REPORTS / "state_domain_summary_table_latex.tex").write_text("\n".join(latex_lines), encoding="utf-8")

    q_fields = [
        "queue_id", "priority", "env", "domain", "task_id", "action_type",
        "config_name", "seed", "target_steps", "reason",
        "requires_state_stable_v1", "skip_reason", "command_preview",
    ]
    preview = []
    for row in queue:
        if row["action_type"] == "skip":
            continue
        preview.append(f"### {row['queue_id']}. {row['env']} / {row['config_name']}\n\n```bash\n{row['command_preview']}\n```")
        if len(preview) >= 12:
            break
    q_text = [
        "# State 25-Task Adaptive Queue",
        "",
        f"Updated: {NOW}",
        "",
        "Generated for planning only. No training is launched by this generator. Rows requiring state_stable_v1 are skipped by the runner until flags are implemented.",
        "",
        md_table(queue, q_fields[:-1]),
        "",
        "## Next Command Previews",
        "",
        "\n\n".join(preview) if preview else "No runnable commands.",
        "",
    ]
    (REPORTS / "state_25task_adaptive_queue.md").write_text("\n".join(q_text), encoding="utf-8")

    progress = [
        "# State 25-Task Goal Progress",
        "",
        f"Updated: {NOW}",
        "",
        "- No training was launched by this artifact generation step.",
        "- state_stable_v1 was not triggered as a run; collapse tasks are queued as requiring stable support.",
        "- Final values use eval.csv last rows only; best/peak values remain diagnostic.",
        "",
        "## Current Counts",
        "",
        f"- Tasks with completed 1M final: {has_1m}",
        f"- Tasks with only completed 300k final: {has_300k_only}",
        f"- No-data tasks: {no_data}",
        f"- Status counts: {dict(counts)}",
        "",
        "## Top Good-Case Candidates",
        "",
    ]
    if candidate_rows:
        for row in candidate_rows:
            progress.append(f"- {row['env']}: {row['best_known_300k_config']} final {row['best_known_300k_final']} vs VF {row['VF_baseline']}")
    else:
        progress.append("- None from current final-row matrix.")
    progress += ["", "## Collapse Diagnostics", ""]
    if collapse_rows:
        for row in collapse_rows:
            progress.append(f"- {row['env']}: best {row['best_success']} @ {row['best_step']}, best 1M final {row['best_known_1M_final']}; {row['recommended_next_action']}")
    else:
        progress.append("- None.")
    progress += ["", "## Domain Coverage Averages", "", md_table(summary, ["domain", "coverage_average_draft", "coverage_available_tasks", "coverage_missing_tasks"]), ""]
    (REPORTS / "state_25task_goal_progress.md").write_text("\n".join(progress), encoding="utf-8")


def main() -> int:
    runs = read_csv(RESULTS / "audit_all_state_runs_single4090.csv")
    if not runs:
        raise SystemExit("Missing results/audit_all_state_runs_single4090.csv; run the audit first.")
    matrix = build_matrix(runs)
    summary = build_domain_summary(matrix)
    queue = build_queue(matrix)
    coverage_fields = [
        "domain", "task_id", "env", "VF_baseline", "best_known_300k_final",
        "best_known_300k_config", "best_known_300k_seed", "best_known_1M_final",
        "best_known_1M_config", "best_known_1M_seed", "best_success", "best_step",
        "peak_after_500k", "status", "recommended_next_action",
        "best_known_300k_eval_csv", "best_known_1M_eval_csv", "best_peak_eval_csv",
    ]
    summary_fields = [
        "domain", "tasks", "valueflow_average", "one_m_only_average",
        "one_m_completed_tasks", "one_m_missing_tasks", "coverage_average_draft",
        "coverage_available_tasks", "coverage_missing_tasks",
        "candidate_average_internal", "candidate_available_tasks",
    ]
    queue_fields = [
        "queue_id", "priority", "env", "domain", "task_id", "action_type",
        "config_name", "seed", "target_steps", "reason",
        "requires_state_stable_v1", "skip_reason", "command_preview",
    ]
    write_csv(RESULTS / "state_25task_coverage_matrix.csv", matrix, coverage_fields)
    write_csv(RESULTS / "state_domain_summary_table.csv", summary, summary_fields)
    write_csv(RESULTS / "state_25task_adaptive_queue.csv", queue, queue_fields)
    write_reports(matrix, summary, queue)
    print({
        "matrix_rows": len(matrix),
        "queue_rows": len(queue),
        "has_1m": sum(1 for row in matrix if row["best_known_1M_final"]),
        "only_300k": sum(1 for row in matrix if row["best_known_300k_final"] and not row["best_known_1M_final"]),
        "no_data": sum(1 for row in matrix if row["status"] == "no_data"),
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

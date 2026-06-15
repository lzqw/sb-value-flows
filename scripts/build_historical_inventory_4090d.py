#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

ROOTS = [Path("/root/sb-value-flows"), Path("/root/autodl-tmp/sb-value-flows-runs")]
KEYWORDS = [
    "fullsafe", "table3", "actor", "actorgeo", "light", "overnight", "bestseed", "puzzle",
    "minimal", "reliability", "visual_bigtable", "visual_matched", "bad_task_repair",
]
SUCCESS_COLUMNS = ["evaluation/success", "eval/success", "success"]
RETURN_COLUMNS = ["evaluation/episode.return", "evaluation/return", "eval/return", "return", "score", "evaluation/score", "normalized_score", "evaluation/normalized_score"]
LENGTH_COLUMNS = ["evaluation/episode.length", "evaluation/length", "eval/length", "length"]
STEP_COLUMNS = ["step", "env_step", "gradient_step", "training/step"]

FIELDS = [
    "machine", "source_root", "experiment_line", "matched_keywords", "status", "protocol", "env", "domain", "task_id", "config_name", "seed",
    "target_steps", "final_step", "success_final", "return_final", "length_final", "success_best", "best_step", "success_peak_after_500k", "peak_step_after_500k",
    "eval_csv", "train_csv", "command_txt", "report_files", "run_dir", "curve_points", "already_in_registry", "registry_run_ids", "notes",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    try:
        with path.open(newline="") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def get_first(row: dict[str, str], names: list[str]) -> str:
    for name in names:
        if name in row and row[name] != "":
            return row[name]
    return ""


def fval(v: Any) -> float | None:
    try:
        x = float(v)
    except Exception:
        return None
    if math.isnan(x):
        return None
    return x


def fmt(v: Any) -> str:
    x = fval(v)
    return "" if x is None else f"{x:.6g}"


def ifmt(v: Any) -> str:
    x = fval(v)
    return "" if x is None else str(int(x))


def find_up(start: Path, stop: Path, names: list[str], max_depth: int = 8) -> Path | None:
    cur = start
    stop = stop.resolve()
    for _ in range(max_depth):
        for name in names:
            p = cur / name
            if p.exists():
                return p
        if cur.resolve() == stop or cur.parent == cur:
            break
        cur = cur.parent
    return None


def find_reports_near(start: Path, stop: Path) -> list[Path]:
    reports = []
    cur = start
    stop = stop.resolve()
    for _ in range(8):
        if cur.exists():
            reports.extend([p for p in cur.glob("*.md") if "report" in p.name.lower()])
            rdir = cur / "reports"
            if rdir.exists():
                reports.extend([p for p in rdir.glob("*.md") if "report" in p.name.lower()])
        if cur.resolve() == stop or cur.parent == cur:
            break
        cur = cur.parent
    return sorted(set(reports))[:20]


def parse_command(path: Path | None) -> dict[str, str]:
    if not path or not path.exists():
        return {}
    text = path.read_text(errors="replace")
    parts = re.findall(r"--([^=\s]+)=([^\s]+)", text)
    return {k: v.strip("\"'") for k, v in parts}


def derive_domain_task(env: str) -> tuple[str, str]:
    m = re.match(r"(.+)-singletask-(task\d+)-v\d+$", env or "")
    if m:
        return m.group(1), m.group(2)
    return "", ""


def infer_env_from_path(path: Path) -> str:
    s = str(path)
    m = re.search(r"((?:visual-)?[A-Za-z0-9x]+(?:-[A-Za-z0-9x]+)*-singletask-task\d+-v\d+)", s)
    return m.group(1) if m else ""


def infer_config(path: Path, cmd: dict[str, str]) -> str:
    s = str(path)
    configs = [
        "R3_flow_residual_disagree_typicality_std_lam0p001", "R2_flow_residual_disagree_std_lam0p001",
        "A2_action_std_lam0p003", "A1_action_std_lam0p001", "P0_particle", "MinimalSB",
        "FullSafe", "fullsafe", "ActorGeo", "actor", "origin", "baseline",
    ]
    for c in configs:
        if c in s:
            return c
    if cmd.get("agent.pm_sb_reliability_score"):
        score = cmd.get("agent.pm_sb_reliability_score")
        lam = cmd.get("agent.pm_sb_lambda", "")
        return f"pm_{score}_lam{lam}" if lam else f"pm_{score}"
    return ""


def infer_seed(path: Path, cmd: dict[str, str]) -> str:
    if cmd.get("seed"):
        return cmd["seed"]
    for pat in [r"sd(\d+)_", r"seed(\d+)", r"_s(\d+)(?:_|/)"]:
        m = re.search(pat, str(path))
        if m:
            return m.group(1)
    return ""


def infer_target_steps(path: Path, cmd: dict[str, str], final_step: float | None) -> int:
    if cmd.get("offline_steps"):
        try:
            return int(float(cmd["offline_steps"]))
        except Exception:
            pass
    s = str(path).lower()
    if "300k" in s:
        return 300000
    if "1000000" in s or "1m" in s:
        return 1000000
    return int(final_step or 0)


def classify_line(path: Path) -> tuple[str, str]:
    s = str(path).lower()
    matched = [kw for kw in KEYWORDS if kw.lower() in s]
    if "visual_matched" in s:
        line = "visual_matched"
    elif "visual_bigtable" in s:
        line = "visual_bigtable"
    elif "fullsafe" in s:
        line = "fullsafe"
    elif "table3" in s:
        line = "table3"
    elif "bestseed" in s:
        line = "bestseed"
    elif "minimal" in s:
        line = "minimal_sb"
    elif "reliability" in s:
        line = "reliability"
    elif "bad_task_repair" in s:
        line = "bad_task_repair"
    elif "puzzle" in s:
        line = "puzzle"
    else:
        line = "other"
    return line, ";".join(matched)


def protocol_from_target(target: int, status: str, path: Path) -> str:
    if status == "PARTIAL":
        return "partial"
    s = str(path).lower()
    if target == 300000 or "300k" in s:
        return "300k_screening"
    if target >= 980000 or "1m" in s:
        return "1m"
    if target <= 5000:
        return "smoke"
    return "unknown"


def registry_index(path: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    if not path.exists():
        return out
    for row in csv.DictReader(path.open()):
        ev = row.get("eval_csv", "")
        if ev:
            out[ev].append(row.get("run_id", ""))
    return out


def scan() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    reg = registry_index(Path("results/experiment_runs.csv"))
    rows = []
    reports_without_eval = []
    eval_parents = set()
    for root in ROOTS:
        if not root.exists():
            continue
        for eval_csv in sorted(root.rglob("eval.csv")):
            if any(x in str(eval_csv) for x in ["/wandb/", "/cache/", "/xla_cache/", "/__pycache__/"]):
                continue
            eval_parents.add(eval_csv.parent)
            data = read_csv(eval_csv)
            run_dir = eval_csv.parent
            train_csv = find_up(run_dir, root, ["train.csv"])
            command_txt = find_up(run_dir, root, ["command.txt"])
            cmd = parse_command(command_txt)
            final = data[-1] if data else {}
            final_step = fval(get_first(final, STEP_COLUMNS))
            success_final = fval(get_first(final, SUCCESS_COLUMNS))
            return_final = fval(get_first(final, RETURN_COLUMNS))
            length_final = fval(get_first(final, LENGTH_COLUMNS))
            best_success = None
            best_step = None
            peak500 = None
            peak500_step = None
            for row in data:
                succ = fval(get_first(row, SUCCESS_COLUMNS))
                step = fval(get_first(row, STEP_COLUMNS))
                if succ is None:
                    continue
                if best_success is None or succ > best_success:
                    best_success, best_step = succ, step
                if step is not None and step >= 500000:
                    if peak500 is None or succ > peak500:
                        peak500, peak500_step = succ, step
            target = infer_target_steps(eval_csv, cmd, final_step)
            if not data:
                status = "FAILED"
            elif target and final_step is not None and final_step >= target * 0.98:
                status = "COMPLETED"
            else:
                status = "PARTIAL"
            env = cmd.get("env_name") or infer_env_from_path(eval_csv)
            domain, task = derive_domain_task(env)
            line, matched = classify_line(eval_csv)
            reports = find_reports_near(run_dir, root)
            eval_key = str(eval_csv.resolve())
            rows.append({
                "machine": "4090d",
                "source_root": str(root),
                "experiment_line": line,
                "matched_keywords": matched,
                "status": status,
                "protocol": protocol_from_target(target, status, eval_csv),
                "env": env,
                "domain": domain,
                "task_id": task,
                "config_name": infer_config(eval_csv, cmd),
                "seed": infer_seed(eval_csv, cmd),
                "target_steps": target,
                "final_step": ifmt(final_step),
                "success_final": fmt(success_final),
                "return_final": fmt(return_final),
                "length_final": fmt(length_final),
                "success_best": fmt(best_success),
                "best_step": ifmt(best_step),
                "success_peak_after_500k": fmt(peak500),
                "peak_step_after_500k": ifmt(peak500_step),
                "eval_csv": eval_key,
                "train_csv": str(train_csv.resolve()) if train_csv else "",
                "command_txt": str(command_txt.resolve()) if command_txt else "",
                "report_files": ";".join(str(p.resolve()) for p in reports),
                "run_dir": str(run_dir.resolve()),
                "curve_points": len(data),
                "already_in_registry": "yes" if eval_key in reg else "no",
                "registry_run_ids": ";".join(reg.get(eval_key, [])),
                "notes": "",
            })
        for report in sorted(root.rglob("*.md")):
            if any(x in str(report) for x in ["/wandb/", "/cache/", "/xla_cache/", "/__pycache__/"]):
                continue
            name = report.name.lower()
            s = str(report).lower()
            if "report" not in name and not any(kw.lower() in s for kw in KEYWORDS):
                continue
            has_eval_near = any(parent in eval_parents for parent in [report.parent, report.parent.parent if report.parent.parent else report.parent])
            if not has_eval_near:
                line, matched = classify_line(report)
                reports_without_eval.append({
                    "machine": "4090d", "source_root": str(root), "experiment_line": line, "matched_keywords": matched,
                    "report": str(report.resolve()), "size": report.stat().st_size, "mtime": datetime.fromtimestamp(report.stat().st_mtime).isoformat(timespec="seconds"),
                })
    return rows, reports_without_eval


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def md_table(rows: list[list[Any]], headers: list[str]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(x).replace("\n", " ") for x in row) + " |")
    return "\n".join(lines)


def main() -> int:
    rows, reports = scan()
    rows.sort(key=lambda r: (r["experiment_line"], r["env"], r["config_name"], r["seed"], r["eval_csv"]))
    write_csv(Path("results/historical_experiment_inventory.csv"), rows, FIELDS)
    report_fields = ["machine", "source_root", "experiment_line", "matched_keywords", "report", "size", "mtime"]
    write_csv(Path("results/historical_reports_without_eval.csv"), reports, report_fields)

    by_line = Counter(r["experiment_line"] for r in rows)
    by_root = Counter(r["source_root"] for r in rows)
    by_status = Counter(r["status"] for r in rows)
    by_reg = Counter(r["already_in_registry"] for r in rows)
    partials = [r for r in rows if r["status"] == "PARTIAL"]
    completed = [r for r in rows if r["status"] == "COMPLETED"]
    new_rows = [r for r in rows if r["already_in_registry"] == "no"]

    lines = [
        "# Historical Experiment Inventory",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Summary",
        "",
        f"- eval.csv found: {len(rows)}",
        f"- completed: {len(completed)}",
        f"- partial: {len(partials)}",
        f"- failed/empty: {by_status.get('FAILED', 0)}",
        f"- already in registry: {by_reg.get('yes', 0)}",
        f"- newly discovered/not in registry: {by_reg.get('no', 0)}",
        f"- reports without nearby eval.csv: {len(reports)}",
        "",
        "## By Source Root",
        "",
        md_table([[k, v] for k, v in sorted(by_root.items())], ["source root", "eval.csv"]),
        "",
        "## By Experiment Line",
        "",
        md_table([[k, v] for k, v in sorted(by_line.items())], ["line", "eval.csv"]),
        "",
        "## By Status",
        "",
        md_table([[k, v] for k, v in sorted(by_status.items())], ["status", "count"]),
        "",
        "## Partial Runs",
        "",
        md_table([[r['experiment_line'], r['env'], r['config_name'], r['seed'], r['final_step'], r['target_steps'], r['success_final'], r['success_best'], r['eval_csv']] for r in partials[:80]], ["line", "env", "config", "seed", "final", "target", "success", "best", "eval.csv"]),
        "",
        "## Newly Discovered Not In Registry",
        "",
        md_table([[r['experiment_line'], r['status'], r['env'], r['config_name'], r['seed'], r['final_step'], r['success_final'], r['eval_csv']] for r in new_rows[:120]], ["line", "status", "env", "config", "seed", "step", "success", "eval.csv"]),
        "",
        "## Reports Without Nearby Eval CSV",
        "",
        md_table([[r['experiment_line'], r['report'], r['size']] for r in reports[:120]], ["line", "report", "size"]),
        "",
        "## Notes",
        "",
        "Partial runs are inventory entries only and must not be treated as final results. Peak success is diagnostic only and does not replace the final eval row.",
    ]
    Path("reports").mkdir(exist_ok=True)
    Path("reports/historical_experiment_inventory.md").write_text("\n".join(lines) + "\n")
    print({"eval_csv": len(rows), "completed": len(completed), "partial": len(partials), "new": len(new_rows), "reports_without_eval": len(reports), "by_line": dict(by_line), "by_status": dict(by_status), "by_registry": dict(by_reg)})
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

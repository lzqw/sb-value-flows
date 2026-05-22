import argparse
import json
import math
from pathlib import Path

import pandas as pd


RUN_NAMES = [
    "E_value_flows_baseline",
    "A_uniform_pm",
    "B_kernel_pm",
    "C_kernel_reliability_pm",
    "D_full_pm",
]

TRAIN_METRICS = [
    "training/critic/critic_loss",
    "training/critic/bcfm_loss",
    "training/critic/dcfm_loss",
    "training/critic/dcfm_loss_raw",
    "training/critic/dcfm_loss_weighted",
    "training/critic/pm/ess",
    "training/critic/pm/weight_entropy",
    "training/critic/pm/weight_max",
    "training/critic/pm/weight_min",
    "training/critic/pm/kernel_sq_dist",
    "training/critic/pm/rel_weight",
    "training/critic/pm/reliability_penalty",
    "training/critic/pm/u_num",
    "training/critic/pm/energy",
    "training/actor/q",
    "training/actor/q_geo",
    "training/actor/q_loss",
    "training/actor/actor_energy",
    "training/actor/actor_disagree",
    "training/actor/actor_loss",
    "training/time/total_time",
    "time/total_time",
]

EVAL_METRICS = [
    "evaluation/return",
    "evaluation/success",
    "evaluation/episode.return",
    "evaluation/episode.length",
]


def to_float(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def fmt(value):
    value = to_float(value)
    if value is None:
        return "MISSING"
    if math.isnan(value) or math.isinf(value):
        return str(value)
    return f"{value:.6g}"


def read_csv_loose(path):
    if not path.exists():
        return None
    lines = path.read_text().splitlines()
    if not lines:
        return pd.DataFrame()

    header = lines[0]
    expected_commas = header.count(",")
    rows = []
    current = ""
    for line in lines[1:]:
        current = line if not current else current + " " + line
        if current.count(",") >= expected_commas:
            rows.append(current)
            current = ""
    if current:
        rows.append(current)

    text = "\n".join([header, *rows])
    from io import StringIO

    return pd.read_csv(StringIO(text), engine="python", on_bad_lines="skip")


def latest_seed_dirs(run_dir):
    if not run_dir.exists():
        return []
    by_seed = {}
    for path in run_dir.glob("sd*"):
        if not path.is_dir():
            continue
        seed = path.name.split("_", 1)[0]
        if seed not in by_seed or path.name > by_seed[seed].name:
            by_seed[seed] = path
    return [by_seed[k] for k in sorted(by_seed)]


def last_row(df):
    if df is None or df.empty:
        return None
    return df.iloc[-1].to_dict()


def read_flags(seed_dir):
    path = seed_dir / "flags.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}


def has_bad_number(row):
    if not row:
        return False
    for value in row.values():
        number = to_float(value)
        if number is not None and (math.isnan(number) or math.isinf(number) or abs(number) > 1e6):
            return True
    return False


def check_close(value, target, tol=0.05):
    value = to_float(value)
    return value is not None and abs(value - target) <= tol


def check_le(a, b):
    a = to_float(a)
    b = to_float(b)
    return a is not None and b is not None and a <= b + 1e-6


def check_ge_zero(value):
    value = to_float(value)
    return value is not None and value >= -1e-6


def aggregate_rows(rows, metrics):
    values = {}
    for metric in metrics:
        nums = [to_float(row.get(metric)) for row in rows if row]
        nums = [num for num in nums if num is not None]
        if nums:
            values[metric] = (sum(nums) / len(nums), len(nums))
    return values


def status_map(path):
    if not path or not Path(path).exists():
        return {}
    data = {}
    for line in Path(path).read_text().splitlines():
        parts = line.split()
        if len(parts) < 3 or parts[0] not in {"SUCCESS", "FAILED"}:
            continue
        run_name = parts[1]
        seed = parts[2].split("=", 1)[-1] if "=" in parts[2] else parts[2]
        data[(run_name, seed)] = line
        if seed.isdigit():
            data[(run_name, f"{int(seed):03d}")] = line
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="exp/pm_short_ablation")
    parser.add_argument("--status", default="logs/pm_short_ablation/status.txt")
    parser.add_argument("--out", default="reports/pm_short_ablation_report.md")
    args = parser.parse_args()

    root = Path(args.root)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    statuses = status_map(args.status)

    results = {}
    seen_envs = set()
    seen_steps = set()
    lines = [
        "# PM Short Ablation Report",
        "",
        f"- Root: `{root}`",
        f"- Status: `{args.status}`",
        "- Seeds: `0`",
        "",
        "## Run Status",
        "",
        "| Run | Seed | Status | Directory |",
        "| --- | --- | --- | --- |",
    ]

    for run_name in RUN_NAMES:
        dirs = latest_seed_dirs(root / run_name)
        if not dirs:
            lines.append(f"| {run_name} | MISSING | MISSING | MISSING |")
            results[run_name] = []
            continue
        results[run_name] = []
        for seed_dir in dirs:
            seed = seed_dir.name.split("_", 1)[0].replace("sd", "")
            status = statuses.get((run_name, seed), "UNKNOWN")
            lines.append(f"| {run_name} | {seed} | {status} | `{seed_dir}` |")
            train = read_csv_loose(seed_dir / "train.csv")
            ev = read_csv_loose(seed_dir / "eval.csv")
            flags = read_flags(seed_dir)
            if flags.get("env_name"):
                seen_envs.add(flags["env_name"])
            if flags.get("offline_steps") is not None:
                seen_steps.add(str(flags["offline_steps"]))
            results[run_name].append((seed, seed_dir, train, ev, flags))

    env_text = ", ".join(f"`{env}`" for env in sorted(seen_envs)) or "`antmaze-large-navigate-v0`"
    step_text = ", ".join(f"`{step}`" for step in sorted(seen_steps)) or "`1000`"
    lines.insert(5, f"- Environment used: {env_text}")
    lines.insert(6, f"- Offline steps: {step_text} (reduced from 2000 because the local JAX/MuJoCo compile path is slow for five ablation runs)")

    lines += ["", "## Final Train Metrics", ""]
    for run_name, entries in results.items():
        lines += [f"### {run_name}", ""]
        if not entries:
            lines += ["MISSING", ""]
            continue
        final_rows = []
        for seed, seed_dir, train, _, _ in entries:
            row = last_row(train)
            final_rows.append(row)
            lines += [f"Seed `{seed}` from `{seed_dir}`:", ""]
            if row is None:
                lines += ["MISSING train.csv", ""]
                continue
            lines += ["| Metric | Final |", "| --- | --- |"]
            for metric in TRAIN_METRICS:
                lines.append(f"| `{metric}` | {fmt(row.get(metric))} |")
            lines.append("")
        if len(entries) > 1:
            agg = aggregate_rows(final_rows, TRAIN_METRICS)
            lines += ["Aggregate final train mean across seeds:", "", "| Metric | Mean | N |", "| --- | --- | --- |"]
            for metric in TRAIN_METRICS:
                if metric in agg:
                    mean, count = agg[metric]
                    lines.append(f"| `{metric}` | {fmt(mean)} | {count} |")
                else:
                    lines.append(f"| `{metric}` | MISSING | 0 |")
            lines.append("")

    lines += ["", "## Final Eval Metrics", ""]
    for run_name, entries in results.items():
        lines += [f"### {run_name}", ""]
        if not entries:
            lines += ["MISSING", ""]
            continue
        final_rows = []
        eval_columns = set()
        for seed, seed_dir, _, ev, _ in entries:
            row = last_row(ev)
            final_rows.append(row)
            lines += [f"Seed `{seed}` from `{seed_dir}`:", ""]
            if ev is None:
                lines += ["MISSING eval.csv", ""]
                continue
            eval_columns.update(ev.columns)
            lines += [f"Eval columns: `{', '.join(ev.columns)}`", ""]
            if row is None:
                lines += ["No eval rows", ""]
                continue
            lines += ["| Metric | Final |", "| --- | --- |"]
            for metric in EVAL_METRICS:
                lines.append(f"| `{metric}` | {fmt(row.get(metric))} |")
            for metric in ev.columns:
                if metric not in EVAL_METRICS:
                    lines.append(f"| `{metric}` | {fmt(row.get(metric))} |")
            lines.append("")
        if len(entries) > 1:
            ordered_eval_metrics = [m for m in EVAL_METRICS if m in eval_columns] + sorted(eval_columns - set(EVAL_METRICS))
            agg = aggregate_rows(final_rows, ordered_eval_metrics)
            lines += ["Aggregate final eval mean across seeds:", "", "| Metric | Mean | N |", "| --- | --- | --- |"]
            for metric in ordered_eval_metrics:
                if metric in agg:
                    mean, count = agg[metric]
                    lines.append(f"| `{metric}` | {fmt(mean)} | {count} |")
                else:
                    lines.append(f"| `{metric}` | MISSING | 0 |")
            lines.append("")

    def first_train_row(run_name):
        entries = results.get(run_name) or []
        if not entries:
            return None
        return last_row(entries[0][2])

    lines += ["", "## Sanity Checks", "", "| Check | Result |", "| --- | --- |"]
    row = first_train_row("A_uniform_pm")
    lines.append(f"| A ess close to 4 | {check_close(row.get('training/critic/pm/ess') if row else None, 4.0)} |")
    lines.append(f"| A weight_max close to 0.25 | {check_close(row.get('training/critic/pm/weight_max') if row else None, 0.25)} |")
    lines.append(f"| A weight_min close to 0.25 | {check_close(row.get('training/critic/pm/weight_min') if row else None, 0.25)} |")

    row = first_train_row("B_kernel_pm")
    lines.append(f"| B ess <= 4 | {check_le(row.get('training/critic/pm/ess') if row else None, 4.0)} |")
    lines.append(f"| B weight_max >= 0.25 | {check_le(0.25, row.get('training/critic/pm/weight_max') if row else None)} |")

    row = first_train_row("C_kernel_reliability_pm")
    lines.append(f"| C rel_weight <= 1 | {check_le(row.get('training/critic/pm/rel_weight') if row else None, 1.0)} |")
    lines.append(
        f"| C weighted DCFM <= raw DCFM | "
        f"{check_le(row.get('training/critic/dcfm_loss_weighted') if row else None, row.get('training/critic/dcfm_loss_raw') if row else None)} |"
    )

    row = first_train_row("D_full_pm")
    lines.append(f"| D q_geo <= q | {check_le(row.get('training/actor/q_geo') if row else None, row.get('training/actor/q') if row else None)} |")
    lines.append(f"| D actor_energy >= 0 | {check_ge_zero(row.get('training/actor/actor_energy') if row else None)} |")
    lines.append(f"| D actor_disagree >= 0 | {check_ge_zero(row.get('training/actor/actor_disagree') if row else None)} |")

    eval_scores = {}
    for run_name, entries in results.items():
        if not entries:
            continue
        ev_row = last_row(entries[0][3])
        if not ev_row:
            continue
        for key in ("evaluation/success", "evaluation/return", "evaluation/episode.return"):
            value = to_float(ev_row.get(key))
            if value is not None:
                eval_scores[run_name] = (key, value)
                break
    best = "MISSING"
    if eval_scores:
        best_run, (best_key, best_value) = max(eval_scores.items(), key=lambda item: item[1][1])
        best = f"`{best_run}` by `{best_key}` = {best_value:.6g}"

    missing_logs = []
    bad_numbers = []
    for run_name, entries in results.items():
        if not entries:
            missing_logs.append(run_name)
            continue
        train_row = last_row(entries[0][2])
        eval_row = last_row(entries[0][3])
        if train_row is None:
            missing_logs.append(f"{run_name}: train")
        if eval_row is None:
            missing_logs.append(f"{run_name}: eval")
        if has_bad_number(train_row) or has_bad_number(eval_row):
            bad_numbers.append(run_name)

    lines += [
        "",
        "## Preliminary Interpretation",
        "",
        "1. Kernel posterior: compare `B_kernel_pm` with `A_uniform_pm`; kernel is active when ESS is below 4 or max weight exceeds 0.25.",
        "2. Reliability weighting: `C_kernel_reliability_pm` is active when rel_weight is <= 1 and weighted DCFM is <= raw DCFM.",
        "3. Actor geometry: `D_full_pm` is active when `q_geo <= q` and geometry penalties are non-negative.",
        f"4. Best short-run performance: {best}.",
        f"5. NaN/loss/log issues: missing={missing_logs or 'none'}, bad_numbers={bad_numbers or 'none'}.",
        "6. Next step: repeat with more seeds and longer runs after confirming the short-run sanity checks remain stable.",
        "",
    ]

    out.write_text("\n".join(lines) + "\n")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

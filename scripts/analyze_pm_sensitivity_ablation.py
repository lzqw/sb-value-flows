import argparse
import json
import math
from pathlib import Path

import pandas as pd


RUN_SPECS = [
    ("KERNEL_bw_1p0", "kernel", {"bandwidth": 1.0}),
    ("KERNEL_bw_0p3", "kernel", {"bandwidth": 0.3}),
    ("KERNEL_bw_0p1", "kernel", {"bandwidth": 0.1}),
    ("KERNEL_bw_0p03", "kernel", {"bandwidth": 0.03}),
    ("REL_0p03", "reliability", {"lambda": 0.03}),
    ("REL_0p1", "reliability", {"lambda": 0.1}),
    ("REL_0p3", "reliability", {"lambda": 0.3}),
    ("ACTOR_E_0p01", "actor_energy", {"actor_energy_coef": 0.01}),
    ("ACTOR_E_0p03", "actor_energy", {"actor_energy_coef": 0.03}),
    ("ACTOR_E_0p1", "actor_energy", {"actor_energy_coef": 0.1}),
]

TRAIN_METRICS = [
    "training/critic/critic_loss",
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
    "training/actor/actor_energy_penalty",
    "training/actor/actor_loss",
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
    from io import StringIO

    return pd.read_csv(StringIO("\n".join([header, *rows])), engine="python", on_bad_lines="skip")


def read_flags(seed_dir):
    path = seed_dir / "flags.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}


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


def row_value(row, key):
    return to_float(row.get(key)) if row else None


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


def has_bad_number(row):
    if not row:
        return False
    for value in row.values():
        number = to_float(value)
        if number is not None and (math.isnan(number) or math.isinf(number) or abs(number) > 1e6):
            return True
    return False


def is_non_uniform(row):
    ess = row_value(row, "training/critic/pm/ess")
    weight_max = row_value(row, "training/critic/pm/weight_max")
    weight_min = row_value(row, "training/critic/pm/weight_min")
    kernel_sq_dist = row_value(row, "training/critic/pm/kernel_sq_dist")
    if ess is None or weight_max is None or weight_min is None:
        return "MISSING"
    moved = ess < 3.95 or weight_max > 0.255 or weight_min < 0.245 or (kernel_sq_dist is not None and kernel_sq_dist > 1e-6)
    return "yes" if moved else "no"


def reliability_strength(row):
    rel_weight = row_value(row, "training/critic/pm/rel_weight")
    ratio = weighted_raw_ratio(row)
    if rel_weight is None and ratio is None:
        return "MISSING"
    if (rel_weight is not None and rel_weight < 0.5) or (ratio is not None and ratio < 0.5):
        return "too strong"
    return "ok"


def actor_strength(row):
    q = row_value(row, "training/actor/q")
    q_geo = row_value(row, "training/actor/q_geo")
    actor_loss = row_value(row, "training/actor/actor_loss")
    if q is None or q_geo is None:
        return "MISSING"
    gap = q_geo - q
    if gap < -0.25 or (actor_loss is not None and abs(actor_loss) > 1e3):
        return "too strong"
    return "ok"


def weighted_raw_ratio(row):
    weighted = row_value(row, "training/critic/dcfm_loss_weighted")
    raw = row_value(row, "training/critic/dcfm_loss_raw")
    if weighted is None or raw is None or abs(raw) < 1e-12:
        return None
    return weighted / raw


def choose_recommendations(results):
    kernel_rows = [(spec["bandwidth"], results[name]["train_row"]) for name, kind, spec in RUN_SPECS if kind == "kernel"]
    non_uniform = [(bw, row) for bw, row in kernel_rows if is_non_uniform(row) == "yes" and not has_bad_number(row)]
    recommended_bw = non_uniform[0][0] if non_uniform else 0.1

    rel_rows = [(spec["lambda"], results[name]["train_row"]) for name, kind, spec in RUN_SPECS if kind == "reliability"]
    ok_rel = [(lam, row) for lam, row in rel_rows if reliability_strength(row) == "ok" and not has_bad_number(row)]
    recommended_lambda = ok_rel[0][0] if ok_rel else 0.1

    actor_rows = [(spec["actor_energy_coef"], results[name]["train_row"]) for name, kind, spec in RUN_SPECS if kind == "actor_energy"]
    ok_actor = [(coef, row) for coef, row in actor_rows if actor_strength(row) == "ok" and not has_bad_number(row)]
    recommended_actor = ok_actor[0][0] if ok_actor else 0.03
    return recommended_bw, recommended_lambda, recommended_actor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="exp/pm_sensitivity_ablation")
    parser.add_argument("--status", default="logs/pm_sensitivity_ablation/status.txt")
    parser.add_argument("--out", default="reports/pm_sensitivity_ablation_report.md")
    args = parser.parse_args()

    root = Path(args.root)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    statuses = status_map(args.status)

    results = {}
    seen_envs = set()
    seen_steps = set()
    lines = [
        "# PM Sensitivity Ablation Report",
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

    for run_name, kind, spec in RUN_SPECS:
        entries = []
        dirs = latest_seed_dirs(root / run_name)
        if not dirs:
            lines.append(f"| {run_name} | MISSING | MISSING | MISSING |")
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
            entries.append((seed, seed_dir, train, ev, flags))
        train_row = last_row(entries[0][2]) if entries else None
        eval_row = last_row(entries[0][3]) if entries else None
        results[run_name] = {
            "kind": kind,
            "spec": spec,
            "entries": entries,
            "train_row": train_row,
            "eval_row": eval_row,
        }

    env_text = ", ".join(f"`{env}`" for env in sorted(seen_envs)) or "`antmaze-large-navigate-v0`"
    step_text = ", ".join(f"`{step}`" for step in sorted(seen_steps)) or "`1000`"
    lines.insert(5, f"- Environment used: {env_text}")
    lines.insert(6, f"- Offline steps: {step_text} (reduced from 2000 because ten local JAX/MuJoCo short runs are slow)")

    lines += ["", "## Kernel Bandwidth Sweep", ""]
    lines += [
        "| Run | Bandwidth | ESS | Entropy | Weight Max | Weight Min | Kernel Sq Dist | Non-Uniform? |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for run_name, kind, spec in RUN_SPECS:
        if kind != "kernel":
            continue
        row = results[run_name]["train_row"]
        lines.append(
            f"| {run_name} | {spec['bandwidth']} | "
            f"{fmt(row_value(row, 'training/critic/pm/ess'))} | "
            f"{fmt(row_value(row, 'training/critic/pm/weight_entropy'))} | "
            f"{fmt(row_value(row, 'training/critic/pm/weight_max'))} | "
            f"{fmt(row_value(row, 'training/critic/pm/weight_min'))} | "
            f"{fmt(row_value(row, 'training/critic/pm/kernel_sq_dist'))} | {is_non_uniform(row)} |"
        )

    lines += ["", "## Reliability Lambda Sweep", ""]
    lines += [
        "| Run | Lambda | Rel Weight | Reliability Penalty | DCFM Raw | DCFM Weighted | Weighted/Raw | Too Strong? |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for run_name, kind, spec in RUN_SPECS:
        if kind != "reliability":
            continue
        row = results[run_name]["train_row"]
        lines.append(
            f"| {run_name} | {spec['lambda']} | "
            f"{fmt(row_value(row, 'training/critic/pm/rel_weight'))} | "
            f"{fmt(row_value(row, 'training/critic/pm/reliability_penalty'))} | "
            f"{fmt(row_value(row, 'training/critic/dcfm_loss_raw'))} | "
            f"{fmt(row_value(row, 'training/critic/dcfm_loss_weighted'))} | "
            f"{fmt(weighted_raw_ratio(row))} | {reliability_strength(row)} |"
        )

    lines += ["", "## Actor Energy Sweep", ""]
    lines += [
        "| Run | Actor Energy Coef | q | q_geo | q_geo_minus_q | Actor Energy | Actor Loss | Too Strong? |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for run_name, kind, spec in RUN_SPECS:
        if kind != "actor_energy":
            continue
        row = results[run_name]["train_row"]
        q = row_value(row, "training/actor/q")
        q_geo = row_value(row, "training/actor/q_geo")
        q_gap = q_geo - q if q is not None and q_geo is not None else None
        lines.append(
            f"| {run_name} | {spec['actor_energy_coef']} | "
            f"{fmt(q)} | {fmt(q_geo)} | {fmt(q_gap)} | "
            f"{fmt(row_value(row, 'training/actor/actor_energy'))} | "
            f"{fmt(row_value(row, 'training/actor/actor_loss'))} | {actor_strength(row)} |"
        )

    lines += ["", "## Final Train Metrics", ""]
    for run_name, _, _ in RUN_SPECS:
        row = results[run_name]["train_row"]
        lines += [f"### {run_name}", ""]
        if row is None:
            lines += ["MISSING train.csv", ""]
            continue
        lines += ["| Metric | Final |", "| --- | --- |"]
        for metric in TRAIN_METRICS:
            lines.append(f"| `{metric}` | {fmt(row.get(metric))} |")
        lines.append("")

    lines += ["", "## Final Eval Metrics", ""]
    for run_name, _, _ in RUN_SPECS:
        data = results[run_name]
        entries = data["entries"]
        row = data["eval_row"]
        lines += [f"### {run_name}", ""]
        if not entries or entries[0][3] is None:
            lines += ["MISSING eval.csv", ""]
            continue
        ev = entries[0][3]
        lines += [f"Eval columns: `{', '.join(ev.columns)}`", ""]
        if row is None:
            lines += ["No eval rows", ""]
            continue
        lines += ["| Metric | Final |", "| --- | --- |"]
        for metric in EVAL_METRICS:
            lines.append(f"| `{metric}` | {fmt(row.get(metric))} |")
        lines.append("")

    bad_runs = []
    missing = []
    for run_name, data in results.items():
        if not data["entries"]:
            missing.append(run_name)
        if data["train_row"] is None:
            missing.append(f"{run_name}: train")
        if data["eval_row"] is None:
            missing.append(f"{run_name}: eval")
        if has_bad_number(data["train_row"]) or has_bad_number(data["eval_row"]):
            bad_runs.append(run_name)

    rec_bw, rec_lambda, rec_actor = choose_recommendations(results)
    lines += [
        "",
        "## Preliminary Interpretation",
        "",
        f"1. Recommended `pm_kernel_bandwidth`: `{rec_bw}` from this short-run sweep.",
        f"2. Recommended `pm_lambda_*` initial value: `{rec_lambda}`.",
        f"3. Recommended `pm_actor_energy_coef`: `{rec_actor}`.",
        "4. `pm_actor_disagree_coef`: keep at `0.0` for the next run unless a dedicated disagree sweep shows a stable benefit.",
        f"5. NaN/loss explosion/log issues: missing={missing or 'none'}, bad_numbers={bad_runs or 'none'}.",
        "6. Next longer-run experiment: run the recommended kernel/reliability/actor settings against uniform PM and value_flows baseline with at least 3 seeds and 10k+ offline steps.",
        "",
    ]

    out.write_text("\n".join(lines) + "\n")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

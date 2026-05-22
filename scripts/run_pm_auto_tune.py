import argparse
import math
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


TRAIN_METRICS = [
    "training/critic/critic_loss",
    "training/critic/dcfm_loss_raw",
    "training/critic/dcfm_loss_weighted",
    "training/critic/pm/ess",
    "training/critic/pm/weight_entropy",
    "training/critic/pm/weight_max",
    "training/critic/pm/weight_min",
    "training/critic/pm/kernel_sq_dist",
    "training/critic/pm/kernel_sq_dist_std",
    "training/critic/pm/kernel_logits_std",
    "training/critic/pm/z_pre_k_std",
    "training/critic/pm/action_candidate_std",
    "training/critic/pm/target_vector_field_k_std",
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
]


@dataclass
class RunSpec:
    round_idx: int
    run_name: str
    kind: str
    params: dict
    agent: str = "agents/pm_value_flows.py"


def to_float(value):
    if value is None:
        return None
    try:
        value = float(str(value).strip())
    except ValueError:
        return None
    return value


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


def latest_seed_dir(root, run_name):
    run_dir = root / run_name
    if not run_dir.exists():
        return None
    dirs = [path for path in run_dir.glob("sd*") if path.is_dir()]
    if not dirs:
        return None
    return sorted(dirs, key=lambda path: path.name)[-1]


def last_row(df):
    if df is None or df.empty:
        return None
    return df.iloc[-1].to_dict()


def row_value(row, key):
    return to_float(row.get(key)) if row else None


def weighted_raw_ratio(row):
    weighted = row_value(row, "training/critic/dcfm_loss_weighted")
    raw = row_value(row, "training/critic/dcfm_loss_raw")
    if weighted is None or raw is None or abs(raw) < 1e-12:
        return None
    return weighted / raw


def q_geo_minus_q(row):
    q = row_value(row, "training/actor/q")
    q_geo = row_value(row, "training/actor/q_geo")
    if q is None or q_geo is None:
        return None
    return q_geo - q


def has_bad_number(row):
    if not row:
        return False
    for value in row.values():
        number = to_float(value)
        if number is not None and (math.isnan(number) or math.isinf(number) or abs(number) > 1e6):
            return True
    return False


def eval_score(eval_row):
    if not eval_row:
        return 0.0
    score = 0.0
    success = row_value(eval_row, "evaluation/success")
    ret = row_value(eval_row, "evaluation/return")
    episode_ret = row_value(eval_row, "evaluation/episode.return")
    if success is not None:
        score += 100.0 * success
    if ret is not None:
        score += ret
    if episode_ret is not None:
        score += episode_ret
    return score


def heuristic_score(result):
    if result["status"] != "SUCCESS":
        return -1e9
    train_row = result["train_row"]
    eval_row = result["eval_row"]
    critic_loss = row_value(train_row, "training/critic/critic_loss")
    if critic_loss is not None and (math.isnan(critic_loss) or math.isinf(critic_loss)):
        return -1e9

    score = eval_score(eval_row)
    if not has_bad_number(train_row) and not has_bad_number(eval_row):
        score += 10
    if critic_loss is not None and math.isfinite(critic_loss):
        score += 5

    if result["spec"].agent.endswith("pm_value_flows.py"):
        rel_weight = row_value(train_row, "training/critic/pm/rel_weight")
        if rel_weight is not None and 0.5 <= rel_weight <= 1.0:
            score += 5
        if rel_weight is not None and rel_weight < 0.4:
            score -= 20

        ratio = weighted_raw_ratio(train_row)
        if ratio is not None and ratio <= 1.0 + 1e-6:
            score += 5

        actor_energy = row_value(train_row, "training/actor/actor_energy")
        if actor_energy is not None and actor_energy >= -1e-6:
            score += 3
        q_gap = q_geo_minus_q(train_row)
        if q_gap is not None and q_gap <= 1e-6:
            score += 3
        if q_gap is not None and q_gap < -0.2:
            score -= 20

    return score


def analyze_run(root, spec, status):
    seed_dir = latest_seed_dir(root, spec.run_name)
    train = read_csv_loose(seed_dir / "train.csv") if seed_dir else None
    ev = read_csv_loose(seed_dir / "eval.csv") if seed_dir else None
    result = {
        "spec": spec,
        "status": status,
        "seed_dir": seed_dir,
        "train_row": last_row(train),
        "eval_row": last_row(ev),
        "eval_columns": list(ev.columns) if ev is not None else [],
    }
    result["score"] = heuristic_score(result)
    return result


def pm_params(weight_type="kernel", bandwidth=0.1, lam=0.03, actor_energy_coef=0.01, actor_disagree_coef=0.0):
    params = {
        "pm_weight_type": weight_type,
        "pm_num_continuations": 4,
        "pm_lambda_num": lam,
        "pm_lambda_energy": lam,
        "pm_lambda_ess": lam,
        "pm_actor_energy_coef": actor_energy_coef,
        "pm_actor_disagree_coef": actor_disagree_coef,
    }
    if weight_type == "kernel":
        params["pm_kernel_bandwidth"] = bandwidth
    return params


def key_params_text(spec):
    if spec.agent.endswith("value_flows.py") and not spec.agent.endswith("pm_value_flows.py"):
        return "--agent=agents/value_flows.py"
    parts = [f"{key}={value}" for key, value in sorted(spec.params.items())]
    return ", ".join(parts)


def eval_metrics_text(row):
    if not row:
        return "MISSING"
    parts = []
    for key, value in row.items():
        if key == "step":
            continue
        number = to_float(value)
        if number is not None:
            parts.append(f"{key}={fmt(number)}")
    return "; ".join(parts[:8]) if parts else "MISSING"


def command_for_spec(args, spec, effective_offline_steps):
    cmd = shlex.split(args.python_bin) + [
        "main.py",
        f"--env_name={args.env_name}",
        f"--seed={args.seed}",
        f"--save_dir={args.save_root}",
        f"--wandb_run_group={spec.run_name}",
        "--enable_wandb=0",
        f"--offline_steps={effective_offline_steps}",
        f"--online_steps={args.online_steps}",
        f"--log_interval={args.log_interval}",
        f"--eval_interval={args.eval_interval}",
        f"--eval_episodes={args.eval_episodes}",
        "--save_interval=999999999",
        f"--agent={spec.agent}",
    ]
    if spec.agent.endswith("pm_value_flows.py"):
        for key, value in spec.params.items():
            cmd.append(f"--agent.{key}={value}")
    return cmd


def run_one(args, spec, effective_offline_steps):
    log_root = Path(args.log_root)
    log_root.mkdir(parents=True, exist_ok=True)
    log_path = log_root / f"{spec.run_name}.log"
    cmd = command_for_spec(args, spec, effective_offline_steps)
    with log_path.open("w") as log_file:
        log_file.write("$ " + " ".join(shlex.quote(part) for part in cmd) + "\n\n")
        log_file.flush()
        proc = subprocess.run(cmd, stdout=log_file, stderr=subprocess.STDOUT, check=False)
    status = "SUCCESS" if proc.returncode == 0 else "FAILED"
    return status, proc.returncode, log_path


def choose_best(results, candidates):
    ranked = [results[spec.run_name] for spec in candidates if spec.run_name in results]
    ranked = [result for result in ranked if result["status"] == "SUCCESS"]
    if not ranked:
        return None
    return max(ranked, key=lambda result: result["score"])


def kernel_is_uniform(row):
    ess = row_value(row, "training/critic/pm/ess")
    weight_max = row_value(row, "training/critic/pm/weight_max")
    k = 4.0
    if ess is None or weight_max is None:
        return True
    return ess > 0.95 * k and weight_max < 1.0 / k + 0.02


def choose_kernel(results, specs):
    successful = [results[spec.run_name] for spec in specs if results.get(spec.run_name, {}).get("status") == "SUCCESS"]
    if not successful:
        return None
    preferred = []
    for result in successful:
        row = result["train_row"]
        ess = row_value(row, "training/critic/pm/ess")
        weight_max = row_value(row, "training/critic/pm/weight_max")
        if ess is not None and weight_max is not None and ess >= 2.0 and weight_max <= 0.8:
            preferred.append(result)
    return max(preferred or successful, key=lambda result: result["score"])


def choose_reliability(results, specs):
    successful = [results[spec.run_name] for spec in specs if results.get(spec.run_name, {}).get("status") == "SUCCESS"]
    if not successful:
        return None
    preferred = []
    for result in successful:
        row = result["train_row"]
        rel_weight = row_value(row, "training/critic/pm/rel_weight")
        ratio = weighted_raw_ratio(row)
        if rel_weight is None:
            continue
        if rel_weight < 0.5 or rel_weight > 0.97:
            continue
        if ratio is not None and 0.75 <= ratio <= 0.95:
            preferred.append(result)
    return max(preferred or successful, key=lambda result: result["score"])


def choose_actor(results, specs):
    successful = [results[spec.run_name] for spec in specs if results.get(spec.run_name, {}).get("status") == "SUCCESS"]
    if not successful:
        return None
    preferred = []
    for result in successful:
        gap = q_geo_minus_q(result["train_row"])
        if gap is not None and -0.05 <= gap <= -0.005:
            preferred.append(result)
    acceptable = []
    for result in successful:
        gap = q_geo_minus_q(result["train_row"])
        if gap is not None and gap >= -0.1 and abs(gap) >= 1e-4:
            acceptable.append(result)
    return max(preferred or acceptable or successful, key=lambda result: result["score"])


def best_pm_result(results):
    pm_results = [
        result
        for result in results.values()
        if result["status"] == "SUCCESS" and result["spec"].agent.endswith("pm_value_flows.py")
    ]
    if not pm_results:
        return None
    return max(pm_results, key=lambda result: result["score"])


def full_pm_flags(params):
    ordered = [
        "--agent=agents/pm_value_flows.py",
        f"--agent.pm_weight_type={params.get('pm_weight_type', 'kernel')}",
        f"--agent.pm_num_continuations={params.get('pm_num_continuations', 4)}",
        f"--agent.pm_kernel_bandwidth={params.get('pm_kernel_bandwidth', 0.1)}",
        f"--agent.pm_lambda_num={params.get('pm_lambda_num', 0.0)}",
        f"--agent.pm_lambda_energy={params.get('pm_lambda_energy', 0.0)}",
        f"--agent.pm_lambda_ess={params.get('pm_lambda_ess', 0.0)}",
        f"--agent.pm_actor_energy_coef={params.get('pm_actor_energy_coef', 0.0)}",
        f"--agent.pm_actor_disagree_coef={params.get('pm_actor_disagree_coef', 0.0)}",
    ]
    return ordered


def build_report(args, effective_offline_steps, reductions_note, rounds, decisions, results, status_lines, failed_logs):
    lines = [
        "# PM Auto-Tune Report",
        "",
        "## Experiment Budget",
        "",
        f"- env_name: `{args.env_name}`",
        f"- max_rounds: `{args.max_rounds}`",
        f"- requested_offline_steps: `{args.offline_steps}`",
        f"- effective_offline_steps: `{effective_offline_steps}`",
        f"- online_steps: `{args.online_steps}`",
        f"- eval_episodes: `{args.eval_episodes}`",
        f"- seed: `{args.seed}`",
        f"- timestamp: `{time.strftime('%Y-%m-%d %H:%M:%S')}`",
        f"- note: {reductions_note}",
        "",
        "## Round-by-round Results",
        "",
    ]
    for round_idx, specs in enumerate(rounds):
        lines += [
            f"### Round {round_idx}",
            "",
            "| run_name | status | key params | critic_loss | ess | weight_max | rel_weight | weighted/raw | q | q_geo | q_geo_minus_q | actor_energy | eval metrics | score |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |",
        ]
        for spec in specs:
            result = results.get(spec.run_name)
            if not result:
                continue
            row = result["train_row"]
            lines.append(
                f"| {spec.run_name} | {result['status']} | {key_params_text(spec)} | "
                f"{fmt(row_value(row, 'training/critic/critic_loss'))} | "
                f"{fmt(row_value(row, 'training/critic/pm/ess'))} | "
                f"{fmt(row_value(row, 'training/critic/pm/weight_max'))} | "
                f"{fmt(row_value(row, 'training/critic/pm/rel_weight'))} | "
                f"{fmt(weighted_raw_ratio(row))} | "
                f"{fmt(row_value(row, 'training/actor/q'))} | "
                f"{fmt(row_value(row, 'training/actor/q_geo'))} | "
                f"{fmt(q_geo_minus_q(row))} | "
                f"{fmt(row_value(row, 'training/actor/actor_energy'))} | "
                f"{eval_metrics_text(result['eval_row'])} | {fmt(result['score'])} |"
            )
        lines.append("")

    lines += ["## Decisions After Each Round", ""]
    for decision in decisions:
        lines.append(f"- {decision}")
    lines.append("")

    best = best_pm_result(results)
    best_params = best["spec"].params if best else pm_params()
    lines += [
        "## Best Configuration Under Current Budget",
        "",
        "This is the best configuration under the bounded short-run budget, not a claim of global optimality.",
        "",
        "```bash",
        " ".join(full_pm_flags(best_params)),
        "```",
        "",
        f"- best_run: `{best['spec'].run_name if best else 'MISSING'}`",
        f"- best_score: `{fmt(best['score'] if best else None)}`",
        "",
        "## Failure / Risk Analysis",
        "",
    ]
    bad_runs = [name for name, result in results.items() if has_bad_number(result["train_row"]) or has_bad_number(result["eval_row"])]
    failed_runs = [line for line in status_lines if "FAILED" in line]
    kernel_results = [result for result in results.values() if result["spec"].kind == "kernel"]
    kernel_uniform = all(kernel_is_uniform(result["train_row"]) for result in kernel_results) if kernel_results else True
    actor_too_strong = [
        name for name, result in results.items() if (q_geo_minus_q(result["train_row"]) is not None and q_geo_minus_q(result["train_row"]) < -0.1)
    ]
    reliability_too_strong = [
        name for name, result in results.items() if (row_value(result["train_row"], "training/critic/pm/rel_weight") is not None and row_value(result["train_row"], "training/critic/pm/rel_weight") < 0.5)
    ]
    lines += [
        f"- NaN or loss explosion: `{bad_runs or 'none'}`",
        f"- Failed runs: `{failed_runs or 'none'}`",
        f"- Kernel still uniform in kernel diagnostics: `{kernel_uniform}`",
        f"- Actor penalty too strong runs: `{actor_too_strong or 'none'}`",
        f"- Reliability too strong runs: `{reliability_too_strong or 'none'}`",
        "",
        "## Eval CSV Fields",
        "",
    ]
    for name, result in results.items():
        lines.append(f"- `{name}`: `{', '.join(result['eval_columns']) if result['eval_columns'] else 'MISSING'}`")
    lines += [
        "",
        "## Status Summary",
        "",
        "```text",
        *status_lines,
        "```",
        "",
        "## Next Suggested Longer Run",
        "",
        "```bash",
        "python main.py \\",
        f"  --env_name={args.env_name} \\",
        f"  --seed={args.seed} \\",
        "  --save_dir=exp/pm_auto_tune_longer \\",
        "  --wandb_run_group=PM_auto_tune_best_10k \\",
        "  --enable_wandb=0 \\",
        "  --offline_steps=10000 \\",
        f"  --online_steps={args.online_steps} \\",
        f"  --eval_episodes={args.eval_episodes} \\",
        "  --save_interval=999999999 \\",
        "  " + " \\\n  ".join(full_pm_flags(best_params)),
        "```",
        "",
    ]
    if failed_logs:
        lines += ["## Failed Log Tails", ""]
        for path, tail in failed_logs.items():
            lines += [f"### {path}", "", "```text", tail, "```", ""]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env_name", default="antmaze-large-navigate-v0")
    parser.add_argument("--save_root", default="exp/pm_auto_tune")
    parser.add_argument("--log_root", default="logs/pm_auto_tune")
    parser.add_argument("--report_path", default="reports/pm_auto_tune_report.md")
    parser.add_argument("--max_rounds", type=int, default=4)
    parser.add_argument("--offline_steps", type=int, default=2000)
    parser.add_argument("--online_steps", type=int, default=0)
    parser.add_argument("--log_interval", type=int, default=500)
    parser.add_argument("--eval_interval", type=int, default=1000)
    parser.add_argument("--eval_episodes", type=int, default=5)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--python_bin", default="conda run -n value-flows python")
    args = parser.parse_args()

    max_rounds = max(0, min(args.max_rounds, 4))
    effective_offline_steps = args.offline_steps
    reductions_note = "No automatic reduction."
    if args.offline_steps > 1000:
        effective_offline_steps = 1000
        reductions_note = "Reduced offline_steps from 2000 to 1000 because a full 4-round local JAX/MuJoCo loop has up to 17 runs."

    Path(args.save_root).mkdir(parents=True, exist_ok=True)
    Path(args.log_root).mkdir(parents=True, exist_ok=True)
    Path(args.report_path).parent.mkdir(parents=True, exist_ok=True)

    rounds = []
    decisions = []
    results = {}
    status_lines = []
    failed_logs = {}
    consecutive_failures = 0

    round0 = [
        RunSpec(0, "R0_VF_baseline", "baseline", {}, agent="agents/value_flows.py"),
        RunSpec(0, "R0_PM_uniform", "uniform", pm_params(weight_type="uniform", lam=0.0, actor_energy_coef=0.0)),
        RunSpec(0, "R0_PM_kernel_default", "default", pm_params(bandwidth=0.1, lam=0.03, actor_energy_coef=0.01)),
    ]
    planned_rounds = [round0]

    for round_idx in range(max_rounds):
        if round_idx >= len(planned_rounds):
            break
        specs = planned_rounds[round_idx]
        rounds.append(specs)
        for spec in specs:
            status, exit_code, log_path = run_one(args, spec, effective_offline_steps)
            status_line = f"{status} {spec.run_name} exit_code={exit_code} log={log_path}"
            print(status_line, flush=True)
            status_lines.append(status_line)
            result = analyze_run(Path(args.save_root), spec, status)
            results[spec.run_name] = result
            if status == "FAILED":
                consecutive_failures += 1
                failed_logs[str(log_path)] = "\n".join(log_path.read_text(errors="replace").splitlines()[-80:])
            else:
                consecutive_failures = 0
            if consecutive_failures >= 3:
                decisions.append("Stopped early after 3 consecutive run failures.")
                report = build_report(args, effective_offline_steps, reductions_note, rounds, decisions, results, status_lines, failed_logs)
                Path(args.report_path).write_text(report)
                print(f"Wrote {args.report_path}", flush=True)
                return 1

        if round_idx == 0 and max_rounds > 1:
            default = results.get("R0_PM_kernel_default")
            row = default["train_row"] if default else None
            if kernel_is_uniform(row):
                bws = [0.1, 0.03, 0.01, 0.003]
                decisions.append("After Round 0, kernel weights were close to uniform, so Round 1 tries smaller bandwidth values.")
            else:
                bw = 0.1
                bws = [bw / 3, bw, bw * 3]
                decisions.append("After Round 0, kernel weights showed separation, so Round 1 searches around the current bandwidth.")
            planned_rounds.append(
                [RunSpec(1, f"R1_KERNEL_bw_{str(bw).replace('.', 'p')}", "kernel", pm_params(bandwidth=bw, lam=0.03, actor_energy_coef=0.01)) for bw in bws]
            )

        if round_idx == 1 and max_rounds > 2:
            best_kernel = choose_kernel(results, specs)
            best_bw = best_kernel["spec"].params.get("pm_kernel_bandwidth", 0.1) if best_kernel else 0.1
            decisions.append(f"After Round 1, selected bandwidth `{best_bw}` by score with sanity constraints; Round 2 tests reliability lambdas at that bandwidth.")
            lambdas = [0.0, 0.01, 0.03, 0.1, 0.3]
            planned_rounds.append(
                [
                    RunSpec(2, f"R2_REL_{str(lam).replace('.', 'p')}", "reliability", pm_params(bandwidth=best_bw, lam=lam, actor_energy_coef=0.01))
                    for lam in lambdas
                ]
            )

        if round_idx == 2 and max_rounds > 3:
            best_rel = choose_reliability(results, specs)
            if best_rel:
                best_bw = best_rel["spec"].params.get("pm_kernel_bandwidth", 0.1)
                best_lam = best_rel["spec"].params.get("pm_lambda_num", 0.03)
            else:
                best_bw = 0.1
                best_lam = 0.03
            decisions.append(f"After Round 2, selected lambda `{best_lam}` at bandwidth `{best_bw}`; Round 3 tests actor energy coefficients.")
            coefs = [0.0, 0.003, 0.01, 0.03, 0.1]
            planned_rounds.append(
                [
                    RunSpec(3, f"R3_ACTOR_E_{str(coef).replace('.', 'p')}", "actor", pm_params(bandwidth=best_bw, lam=best_lam, actor_energy_coef=coef))
                    for coef in coefs
                ]
            )

        if round_idx == 3:
            best_actor = choose_actor(results, specs)
            if best_actor:
                coef = best_actor["spec"].params.get("pm_actor_energy_coef", 0.0)
                decisions.append(f"After Round 3, selected actor energy coefficient `{coef}` under the short-run heuristic.")

    report = build_report(args, effective_offline_steps, reductions_note, rounds, decisions, results, status_lines, failed_logs)
    Path(args.report_path).write_text(report)
    print(f"Wrote {args.report_path}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

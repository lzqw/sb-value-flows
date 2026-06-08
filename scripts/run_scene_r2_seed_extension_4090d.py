#!/usr/bin/env python3
import csv
import json
import math
import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path("/root/sb-value-flows")
LOG_DIR = ROOT / "logs/scene_r2_seed_extension_4090d"
EXP_DIR = ROOT / "exp/scene_r2_seed_extension_4090d"
REPORT = ROOT / "reports/scene_r2_seed_extension_4090d_report.md"
CONDA = "/root/miniconda3/bin/conda"
STATUS = LOG_DIR / "status.txt"

LOG_DIR.mkdir(parents=True, exist_ok=True)
EXP_DIR.mkdir(parents=True, exist_ok=True)
REPORT.parent.mkdir(parents=True, exist_ok=True)

ENVS = [f"scene-play-singletask-task{i}-v0" for i in range(1, 6)]
SEEDS = [0, 1]
STEPS = 1_000_000
CONFIG = "R2_flow_residual_disagree_std_lam0p001"

SEED2_RESULTS = {
    "scene-play-singletask-task1-v0": {"success": 1.0, "return": -111.2, "length": 79.4, "selected_eval_csv": "/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task1-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task1-v0_seed2/sd002_20260606_142510/eval.csv"},
    "scene-play-singletask-task2-v0": {"success": 1.0, "return": -380.7, "length": 212.0, "selected_eval_csv": "/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task2-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task2-v0_seed2/sd002_20260606_183923/eval.csv"},
    "scene-play-singletask-task3-v0": {"success": 1.0, "return": -348.2, "length": 176.8, "selected_eval_csv": "/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task3-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task3-v0_seed2/sd002_20260606_225507/eval.csv"},
    "scene-play-singletask-task4-v0": {"success": 0.0, "return": -769.7, "length": 750.0, "selected_eval_csv": "/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task4-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task4-v0_seed2/sd002_20260607_031022/eval.csv"},
    "scene-play-singletask-task5-v0": {"success": 0.0, "return": -882.2, "length": 750.0, "selected_eval_csv": "/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task5-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task5-v0_seed2/sd002_20260607_073207/eval.csv"},
}

PAPER = {
    "scene-play-singletask-task1-v0": (0.99, "99 +/- 0"),
    "scene-play-singletask-task2-v0": (0.97, "97 +/- 1"),
    "scene-play-singletask-task3-v0": (0.94, "94 +/- 2"),
    "scene-play-singletask-task4-v0": (0.07, "7 +/- 4"),
    "scene-play-singletask-task5-v0": (0.00, "0 +/- 0"),
}

COMMON_FLAGS = [
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

R2_FLAGS = [
    "--agent.pm_sb_reliability_score=flow_residual_disagree",
    "--agent.pm_sb_lambda=0.001",
    "--agent.pm_sb_reliability_normalize=std",
    "--agent.pm_sb_flow_residual_eps=0.05",
    "--agent.pm_sb_disagree_beta=0.5",
    "--agent.pm_sb_disagree_umax=3.0",
    "--agent.pm_sb_value_preserving=false",
    "--agent.ret_agg=min",
]

METRIC_KEYS = {
    "success": ["evaluation/success", "eval/success", "success"],
    "return": ["evaluation/return", "eval/return", "return", "evaluation/episode.return", "eval/episode.return", "episode.return"],
    "length": ["evaluation/length", "eval/length", "length", "evaluation/episode.length", "eval/episode.length", "episode.length"],
}

DIAG_KEYS = [
    "pm/weight_max",
    "pm/ess",
    "pm/reliability_mean",
    "pm/reliability_std",
    "pm/flow_residual_mean",
    "pm/flow_residual_std",
    "pm/disagree_mean",
    "pm/disagree_std",
]


@dataclass(frozen=True)
class Task:
    env: str
    seed: int


def ts():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def run_dir(t: Task):
    return EXP_DIR / f"{CONFIG}_{t.env}_seed{t.seed}_{STEPS}"


def run_log(t: Task, gpu: int):
    return LOG_DIR / f"{CONFIG}_{t.env}_seed{t.seed}_gpu{gpu}.log"


def count_rows(path: Path):
    if not path:
        return 0
    try:
        with path.open(errors="ignore", newline="") as f:
            return max(0, sum(1 for _ in f) - 1)
    except Exception:
        return -1


def select_csv(run_path: Path, name: str):
    candidates = [p for p in run_path.rglob(name) if p.is_file()]
    if not candidates:
        return None, []
    scored = [(count_rows(p), p.stat().st_mtime, p) for p in candidates]
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return scored[0][2], [str(x[2]) for x in scored]


def read_final_row(path: Path):
    with path.open(errors="ignore", newline="") as f:
        rows = list(csv.DictReader(f))
    return rows[-1] if rows else None


def get_num(row, keys):
    for key in keys:
        if key in row and row[key] not in ("", None):
            try:
                return float(row[key])
            except Exception:
                pass
    return math.nan


def fmt(x):
    if isinstance(x, float):
        if math.isnan(x):
            return "nan"
        return f"{x:.6g}"
    return str(x)


def mean_std(values):
    vals = [v for v in values if isinstance(v, (int, float)) and not math.isnan(v)]
    if not vals:
        return math.nan, math.nan
    mean = sum(vals) / len(vals)
    std = (sum((v - mean) ** 2 for v in vals) / len(vals)) ** 0.5
    return mean, std


def command(t: Task):
    cmd = [
        "python",
        "main.py",
        f"--env_name={t.env}",
        f"--seed={t.seed}",
        f"--save_dir={run_dir(t)}",
        f"--wandb_run_group=scene_r2_seed_ext_{t.env}_seed{t.seed}",
        "--enable_wandb=0",
        f"--offline_steps={STEPS}",
        "--online_steps=0",
        "--eval_interval=50000",
        "--eval_episodes=10",
        "--log_interval=25000",
        "--save_interval=999999999",
    ] + COMMON_FLAGS + R2_FLAGS
    agent_idx = cmd.index("--agent=agents/pm_value_flows.py")
    if any(x.startswith("--agent.") for x in cmd[:agent_idx]):
        raise RuntimeError("CONFIG_ERROR: --agent.* before --agent=agents/pm_value_flows.py")
    return cmd


def log_status(total, completed, failed, warning, running, remaining):
    current = " ".join(f"GPU{g}={t.env}:seed{t.seed}" for g, t in sorted(running.items())) or "none"
    with STATUS.open("a") as f:
        f.write(
            f"[{ts()}] total={total} completed={completed} failed={failed} warning={warning} "
            f"running={len(running)} remaining={remaining} | {current}\n"
        )


def launch(t: Task, gpu: int):
    rd = run_dir(t)
    rd.mkdir(parents=True, exist_ok=True)
    full_cmd = [CONDA, "run", "-n", "value-flows"] + command(t)
    env = os.environ.copy()
    env.update(
        {
            "CUDA_VISIBLE_DEVICES": str(gpu),
            "LD_LIBRARY_PATH": "/root/.mujoco/mujoco210/bin:" + env.get("LD_LIBRARY_PATH", ""),
            "MUJOCO_GL": "egl",
            "PYOPENGL_PLATFORM": "egl",
            "SDL_VIDEODRIVER": "dummy",
            "OGBENCH_DATA_DIR": "/root/.ogbench/data",
            "HOME": "/root",
            "XDG_CACHE_HOME": "/root/.cache",
            "XLA_PYTHON_CLIENT_PREALLOCATE": "true",
            "XLA_PYTHON_CLIENT_MEM_FRACTION": "0.90",
        }
    )
    lp = run_log(t, gpu)
    with lp.open("w") as f:
        f.write("COMMAND: " + " ".join(full_cmd) + "\n")
        f.flush()
        return subprocess.Popen(full_cmd, cwd=ROOT, env=env, stdout=f, stderr=subprocess.STDOUT)


def parse_result(t: Task, returncode: int):
    rd = run_dir(t)
    eval_csv, eval_candidates = select_csv(rd, "eval.csv")
    train_csv, train_candidates = select_csv(rd, "train.csv")
    result = {
        "env": t.env,
        "seed": t.seed,
        "config": CONFIG,
        "steps": STEPS,
        "run_dir": str(rd),
        "selected_eval_csv": str(eval_csv) if eval_csv else "",
        "selected_train_csv": str(train_csv) if train_csv else "",
        "all_eval_csv_candidates": eval_candidates,
        "all_train_csv_candidates": train_candidates,
        "returncode": returncode,
        "eval_rows": count_rows(eval_csv) if eval_csv else 0,
        "train_rows": count_rows(train_csv) if train_csv else 0,
        "success": math.nan,
        "return": math.nan,
        "length": math.nan,
        "status": "FAILED",
        "error_tail": "",
    }
    final_eval = read_final_row(eval_csv) if eval_csv else None
    final_train = read_final_row(train_csv) if train_csv else None
    if final_eval:
        result["success"] = get_num(final_eval, METRIC_KEYS["success"])
        result["return"] = get_num(final_eval, METRIC_KEYS["return"])
        result["length"] = get_num(final_eval, METRIC_KEYS["length"])
        for key in DIAG_KEYS:
            result[key] = get_num(final_eval, [key])
            if math.isnan(result[key]) and final_train:
                result[key] = get_num(final_train, [key])
        log_text = ""
        for p in LOG_DIR.glob(f"{CONFIG}_{t.env}_seed{t.seed}_gpu*.log"):
            try:
                log_text += p.read_text(errors="ignore")[-8000:]
            except Exception:
                pass
        bad = any(x in log_text for x in ["Traceback", "RuntimeError", "CUDA_ERROR_OUT_OF_MEMORY", "RESOURCE_EXHAUSTED", "NaN"])
        if returncode == 0 and not bad:
            result["status"] = "COMPLETE"
        else:
            result["status"] = "COMPLETE_WITH_WARNING"
            result["error_tail"] = log_text[-2000:]
    return result


def seed2_rows():
    rows = []
    for env, vals in SEED2_RESULTS.items():
        row = {
            "env": env,
            "seed": 2,
            "config": CONFIG,
            "steps": STEPS,
            "run_dir": "",
            "selected_eval_csv": vals["selected_eval_csv"],
            "selected_train_csv": "",
            "all_eval_csv_candidates": [vals["selected_eval_csv"]],
            "all_train_csv_candidates": [],
            "returncode": 0,
            "eval_rows": 21,
            "train_rows": 40,
            "success": vals["success"],
            "return": vals["return"],
            "length": vals["length"],
            "status": "EXISTING_SEED2",
            "error_tail": "",
        }
        rows.append(row)
    return rows


def git_output(args):
    try:
        return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()
    except Exception as exc:
        return repr(exc)


def write_report(results, failures):
    all_rows = list(results) + seed2_rows()
    lines = [
        "# Scene R2 3-Seed Extension 4090D",
        "",
        "Results use final-row `evaluation/success` from the selected `eval.csv` only.",
        "Seeds 0 and 1 are newly run here; seed 2 is merged from `scene_5task_1m_4090d_v1`.",
        "",
        "## Setup",
        f"- config: `{CONFIG}`",
        "- paper VF scene domain: 0.59 +/- 0.04",
        "- protocol note: this is a 3-seed evidence extension, not full 8-seed official protocol.",
        "",
        "## Per-Seed Results",
        "| seed | task | paper VF | success | return | length | weight_max | ess | rel_mean | rel_std | flow_res_mean | flow_res_std | disagree_mean | disagree_std | selected_eval_csv | status |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for r in sorted(all_rows, key=lambda x: (x["seed"], x["env"])):
        _base, label = PAPER.get(r["env"], (math.nan, ""))
        lines.append(
            f"| {r['seed']} | {r['env']} | {label} | {fmt(r['success'])} | {fmt(r['return'])} | {fmt(r['length'])} | "
            f"{fmt(r.get('pm/weight_max', math.nan))} | {fmt(r.get('pm/ess', math.nan))} | "
            f"{fmt(r.get('pm/reliability_mean', math.nan))} | {fmt(r.get('pm/reliability_std', math.nan))} | "
            f"{fmt(r.get('pm/flow_residual_mean', math.nan))} | {fmt(r.get('pm/flow_residual_std', math.nan))} | "
            f"{fmt(r.get('pm/disagree_mean', math.nan))} | {fmt(r.get('pm/disagree_std', math.nan))} | "
            f"`{r['selected_eval_csv']}` | {r['status']} |"
        )
    lines += ["", "## Task-Level 3-Seed Aggregate", "| task | paper VF | seed values | mean | std | gap vs paper |", "|---|---:|---|---:|---:|---:|"]
    for env in ENVS:
        vals = [r["success"] for r in all_rows if r["env"] == env]
        m, s = mean_std(vals)
        base, label = PAPER[env]
        gap = m - base if not math.isnan(m) else math.nan
        lines.append(f"| {env} | {label} | {', '.join(fmt(v) for v in vals)} | {fmt(m)} | {fmt(s)} | {fmt(gap)} |")
    seed_domain = {}
    for seed in [0, 1, 2]:
        vals = [r["success"] for r in all_rows if r["seed"] == seed]
        seed_domain[seed] = sum(vals) / len(vals) if len(vals) == 5 else math.nan
    domain_m, domain_s = mean_std(list(seed_domain.values()))
    strong = sum(1 for v in seed_domain.values() if not math.isnan(v) and v >= 0.58)
    lines += [
        "",
        "## Domain-Level Aggregate",
        "| seed | domain mean success |",
        "|---:|---:|",
    ]
    for seed in [0, 1, 2]:
        lines.append(f"| {seed} | {fmt(seed_domain[seed])} |")
    lines += [
        "",
        f"- 3-seed domain mean/std: {fmt(domain_m)} / {fmt(domain_s)}",
        "- paper VF scene domain: 0.59 +/- 0.04",
        f"- seeds with domain mean >= 0.58: {strong}/3",
        f"- criterion `at least 2/3 seeds >= 0.58`: {'PASS' if strong >= 2 else 'FAIL'}",
        "",
        "## Failed / Warned Runs",
    ]
    flagged = [r for r in results if r["status"] not in ("COMPLETE", "SKIPPED_COMPLETE")]
    if not flagged and not failures:
        lines.append("- none")
    for failure in failures:
        lines.append(f"- {failure}")
    for r in flagged:
        lines.append(f"### {r['env']} seed={r['seed']} status={r['status']}")
        lines.append(f"- run_dir: `{r['run_dir']}`")
        lines.append(f"- selected_eval_csv: `{r['selected_eval_csv']}`")
        lines.append(f"- eval candidates: `{r['all_eval_csv_candidates']}`")
        if r.get("error_tail"):
            lines.append("```")
            lines.append(r["error_tail"][-2000:])
            lines.append("```")
    lines += [
        "",
        "## Git",
        f"- branch: `{git_output(['git', 'branch', '--show-current'])}`",
        f"- HEAD: `{git_output(['git', 'rev-parse', 'HEAD'])}`",
        "```",
        git_output(["git", "status", "--short"]),
        "```",
        "",
    ]
    REPORT.write_text("\n".join(lines))


def commit_and_push():
    subprocess.run(["git", "add", str(REPORT.relative_to(ROOT)), "scripts/run_scene_r2_seed_extension_4090d.py"], cwd=ROOT)
    commit = subprocess.run(
        ["git", "commit", "-m", "Add scene R2 three-seed extension results"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    (LOG_DIR / "git_commit.log").write_text(commit.stdout + commit.stderr)
    if commit.returncode != 0:
        return f"git commit failed: {commit.stdout} {commit.stderr}"
    push = subprocess.run(["git", "push", "origin", "HEAD:results/scene-r2-3seed-4090d"], cwd=ROOT, text=True, capture_output=True)
    (LOG_DIR / "git_push.log").write_text(push.stdout + push.stderr)
    if push.returncode != 0:
        return f"git push failed: {push.stdout} {push.stderr}"
    return ""


def main():
    pending = [Task(env, seed) for seed in SEEDS for env in ENVS]
    total = len(pending)
    running = {}
    procs = {}
    results = []
    failures = []
    completed = failed = warning = 0
    log_status(total, completed, failed, warning, running, len(pending))
    last_status = 0
    while pending or procs:
        for gpu, proc in list(procs.items()):
            if proc.poll() is None:
                continue
            task = running.pop(gpu)
            procs.pop(gpu)
            res = parse_result(task, proc.returncode)
            results.append(res)
            if res["status"] in ("COMPLETE", "SKIPPED_COMPLETE"):
                completed += 1
            elif res["status"] == "COMPLETE_WITH_WARNING":
                warning += 1
            else:
                failed += 1
            write_report(results, failures)
            log_status(total, completed, failed, warning, running, len(pending))
        for gpu in [0, 1]:
            if gpu in procs or not pending:
                continue
            task = pending.pop(0)
            existing = parse_result(task, 0)
            if existing["selected_eval_csv"] and existing["eval_rows"] > 0:
                existing["status"] = "SKIPPED_COMPLETE"
                results.append(existing)
                completed += 1
                write_report(results, failures)
                log_status(total, completed, failed, warning, running, len(pending))
                continue
            try:
                proc = launch(task, gpu)
            except Exception as exc:
                failures.append(f"launch failed {task}: {exc!r}")
                failed += 1
                continue
            running[gpu] = task
            procs[gpu] = proc
            log_status(total, completed, failed, warning, running, len(pending))
        if time.time() - last_status > 300:
            log_status(total, completed, failed, warning, running, len(pending))
            last_status = time.time()
        time.sleep(30)
    write_report(results, failures)
    err = commit_and_push()
    if err:
        failures.append(err)
        write_report(results, failures)
    log_status(total, completed, failed, warning, running, 0)


if __name__ == "__main__":
    main()

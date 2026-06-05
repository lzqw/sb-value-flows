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
LOG_DIR = ROOT / "logs/bestseed_5task_push_4090d_v2"
EXP_DIR = ROOT / "exp/bestseed_5task_push_4090d_v2"
REPORT = ROOT / "reports/bestseed_5task_push_4090d_v2_report.md"
TRACKING = ROOT / "reports/valueflows_task_level_tracking.md"
MANIFEST = Path("/root/.ogbench/data/manifest_after_hardlink_4090d.json")
CONDA = "/root/miniconda3/bin/conda"
LOG_DIR.mkdir(parents=True, exist_ok=True)
EXP_DIR.mkdir(parents=True, exist_ok=True)
REPORT.parent.mkdir(parents=True, exist_ok=True)
STATUS = LOG_DIR / "status.txt"

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

CONFIG_FLAGS = {
    "A1_action_std_lam0p001": [
        "--agent.pm_sb_reliability_score=action",
        "--agent.pm_sb_lambda=0.001",
        "--agent.pm_sb_reliability_normalize=std",
        "--agent.pm_sb_value_preserving=false",
    ],
    "R2_flow_residual_disagree_std_lam0p001": [
        "--agent.pm_sb_reliability_score=flow_residual_disagree",
        "--agent.pm_sb_lambda=0.001",
        "--agent.pm_sb_reliability_normalize=std",
        "--agent.pm_sb_flow_residual_eps=0.05",
        "--agent.pm_sb_disagree_beta=0.5",
        "--agent.pm_sb_disagree_umax=3.0",
        "--agent.pm_sb_value_preserving=false",
    ],
    "R3_flow_residual_disagree_typicality_std_lam0p001": [
        "--agent.pm_sb_reliability_score=flow_residual_disagree_typicality",
        "--agent.pm_sb_lambda=0.001",
        "--agent.pm_sb_reliability_normalize=std",
        "--agent.pm_sb_flow_residual_eps=0.05",
        "--agent.pm_sb_disagree_beta=0.5",
        "--agent.pm_sb_disagree_umax=3.0",
        "--agent.pm_sb_typicality_tau=1.0",
        "--agent.pm_sb_value_preserving=false",
    ],
}

ENV_FLAGS = {
    "cube-triple": ["--agent.discount=0.995", "--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=0.03"],
    "cube-double": ["--agent.discount=0.995", "--agent.confidence_weight_temp=3"],
    "scene": ["--agent.ret_agg=min"],
}

PAPER = {
    "cube-triple-play-singletask-task1-v0": (0.59, "59 +/- 12"),
    "cube-triple-play-singletask-task2-v0": (0.00, "0 +/- 0"),
    "cube-triple-play-singletask-task3-v0": (0.07, "7 +/- 3"),
    "cube-triple-play-singletask-task4-v0": (0.00, "0 +/- 0"),
    "cube-triple-play-singletask-task5-v0": (0.02, "2 +/- 1"),
    "cube-double-play-singletask-task1-v0": (0.97, "97 +/- 1"),
    "cube-double-play-singletask-task2-v0": (0.76, "76 +/- 7"),
    "cube-double-play-singletask-task3-v0": (0.73, "73 +/- 4"),
    "cube-double-play-singletask-task4-v0": (0.30, "30 +/- 5"),
    "cube-double-play-singletask-task5-v0": (0.69, "69 +/- 5"),
    "scene-play-singletask-task1-v0": (0.99, "99 +/- 0"),
    "scene-play-singletask-task2-v0": (0.97, "97 +/- 1"),
    "scene-play-singletask-task3-v0": (0.94, "94 +/- 2"),
    "scene-play-singletask-task4-v0": (0.07, "7 +/- 4"),
    "scene-play-singletask-task5-v0": (0.00, "0 +/- 0"),
}

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
    "pm/typicality_mean",
    "pm/typicality_std",
    "pm/proj_delta_mean",
    "pm/cov_y_action",
    "pm/corr_y_action",
]


@dataclass(frozen=True)
class Task:
    queue: str
    env: str
    config: str
    seed: int
    steps: int


def ts():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def domain(env):
    return "-".join(env.split("-")[:2])


def run_dir(t: Task):
    return EXP_DIR / t.queue / f"{t.config}_{t.env}_seed{t.seed}_{t.steps}"


def run_log(t: Task, gpu: int):
    return LOG_DIR / f"{t.queue}_{t.config}_{t.env}_seed{t.seed}_gpu{gpu}.log"


def count_rows(path: Path):
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
    if not rows:
        return None
    return rows[-1]


def get_num(row, keys):
    for key in keys:
        if key in row and row[key] not in ("", None):
            try:
                return float(row[key])
            except Exception:
                pass
    return math.nan


def command(t: Task):
    cmd = [
        "python",
        "main.py",
        f"--env_name={t.env}",
        f"--seed={t.seed}",
        f"--save_dir={run_dir(t)}",
        f"--wandb_run_group=bestseed_5task_v2_{t.queue}_{t.config}_{t.env}_seed{t.seed}",
        "--enable_wandb=0",
        f"--offline_steps={t.steps}",
        "--online_steps=0",
        "--eval_interval=50000",
        "--eval_episodes=10",
        "--log_interval=25000",
        "--save_interval=999999999",
    ] + COMMON_FLAGS + CONFIG_FLAGS[t.config] + ENV_FLAGS.get(domain(t.env), [])
    agent_idx = cmd.index("--agent=agents/pm_value_flows.py")
    if any(x.startswith("--agent.") for x in cmd[:agent_idx]):
        raise RuntimeError("CONFIG_ERROR: --agent.* before --agent=agents/pm_value_flows.py")
    return cmd


def log_status(total, completed, failed, warning, running, remaining):
    current = " ".join(f"GPU{g}={t.queue}:{t.config}:{t.env}:seed{t.seed}" for g, t in sorted(running.items())) or "none"
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
        proc = subprocess.Popen(full_cmd, cwd=ROOT, env=env, stdout=f, stderr=subprocess.STDOUT)
    return proc


def parse_result(t: Task, returncode: int):
    rd = run_dir(t)
    eval_csv, eval_candidates = select_csv(rd, "eval.csv")
    train_csv, train_candidates = select_csv(rd, "train.csv")
    result = {
        "queue": t.queue,
        "env": t.env,
        "config": t.config,
        "seed": t.seed,
        "steps": t.steps,
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
    final_row = None
    if eval_csv:
        try:
            final_row = read_final_row(eval_csv)
        except Exception as exc:
            result["error_tail"] = repr(exc)
    if final_row:
        result["success"] = get_num(final_row, METRIC_KEYS["success"])
        result["return"] = get_num(final_row, METRIC_KEYS["return"])
        result["length"] = get_num(final_row, METRIC_KEYS["length"])
        for k in DIAG_KEYS:
            result[k] = get_num(final_row, [k])
        log_text = ""
        for p in LOG_DIR.glob(f"{t.queue}_{t.config}_{t.env}_seed{t.seed}_gpu*.log"):
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
    result["collapse"] = bool(not math.isnan(result.get("pm/weight_max", math.nan)) and result["pm/weight_max"] > 0.95)
    return result


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


def git_output(args):
    try:
        return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()
    except Exception as exc:
        return repr(exc)


def write_report(results, failures):
    complete = sum(1 for x in json.load(open(MANIFEST)).get("envs", []) if x.get("num_files", 0) >= 2)
    lines = [
        "# 4090D Best-Seed Five-Task Reliability SB v2",
        "",
        "These are best-seed / 300k screening results, not full 8-seed official protocol.",
        "",
        "## Data Status",
        f"- manifest path: `{MANIFEST}`",
        f"- env complete: {complete}/25",
        "- hardlink note: singletask task1..5 names are hardlinks to the corresponding base play datasets.",
        "",
        "## CSV Finder Fix",
        "- The old runner checked only `run_dir/eval.csv`, but `main.py` writes under nested `run_dir/.../sdXXX_*/eval.csv` directories.",
        "- v2 recursively scans `run_dir.rglob('eval.csv')`, chooses the file with the most rows, then latest mtime.",
        "- All CSV candidates and selected CSV paths are recorded per run.",
        "",
        "## Queue A: cube-triple R2 seed2 1M",
        "| task | paper VF | success | gap | return | length | selected_eval_csv | status |",
        "|---|---:|---:|---:|---:|---:|---|---|",
    ]
    qa = sorted([r for r in results if r["queue"] == "queueA_cube_triple_5task_1m"], key=lambda r: r["env"])
    for r in qa:
        base, label = PAPER.get(r["env"], (math.nan, ""))
        gap = r["success"] - base if not math.isnan(r["success"]) and not math.isnan(base) else math.nan
        lines.append(
            f"| {r['env']} | {label} | {fmt(r['success'])} | {fmt(gap)} | {fmt(r['return'])} | {fmt(r['length'])} | `{r['selected_eval_csv']}` | {r['status']} |"
        )
    m, s = mean_std([r["success"] for r in qa])
    lines += ["", f"- cube-triple 5-task mean/std: {fmt(m)} / {fmt(s)}", "- paper domain baseline: 14 +/- 3", ""]
    lines += [
        "## Queue B: cube-double / scene 300k screening",
        "| domain | task | config | paper VF | success | gap | return | length | weight_max | ess | rel_mean | rel_std | flow_res_mean | disagree_mean | typicality_mean | collapse | selected_eval_csv | status |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]
    qb = sorted([r for r in results if r["queue"] == "queueB_screen_300k"], key=lambda r: (domain(r["env"]), r["env"], r["config"]))
    for r in qb:
        base, label = PAPER.get(r["env"], (math.nan, ""))
        gap = r["success"] - base if not math.isnan(r["success"]) and not math.isnan(base) else math.nan
        lines.append(
            f"| {domain(r['env'])} | {r['env']} | {r['config']} | {label} | {fmt(r['success'])} | {fmt(gap)} | {fmt(r['return'])} | {fmt(r['length'])} | "
            f"{fmt(r.get('pm/weight_max', math.nan))} | {fmt(r.get('pm/ess', math.nan))} | {fmt(r.get('pm/reliability_mean', math.nan))} | "
            f"{fmt(r.get('pm/reliability_std', math.nan))} | {fmt(r.get('pm/flow_residual_mean', math.nan))} | {fmt(r.get('pm/disagree_mean', math.nan))} | "
            f"{fmt(r.get('pm/typicality_mean', math.nan))} | {r['collapse']} | `{r['selected_eval_csv']}` | {r['status']} |"
        )
    lines += ["", "## Best Configs", ""]
    for dom in ["cube-double", "scene"]:
        lines.append(f"### {dom}")
        rows = [r for r in qb if domain(r["env"]) == dom and r["status"] != "FAILED" and not r["collapse"]]
        for env in sorted(set(r["env"] for r in rows)):
            erows = [r for r in rows if r["env"] == env]
            if erows:
                best = max(erows, key=lambda r: (r["success"], r["return"]))
                lines.append(f"- {env}: {best['config']} success={fmt(best['success'])} return={fmt(best['return'])}")
        configs = sorted(set(r["config"] for r in rows))
        for cfg in configs:
            vals = [r["success"] for r in rows if r["config"] == cfg]
            mm, ss = mean_std(vals)
            lines.append(f"- domain config avg {cfg}: {fmt(mm)} / {fmt(ss)}")
        lines.append("")
    lines += ["## Failed / Warned Runs", ""]
    flagged = [r for r in results if r["status"] != "COMPLETE"]
    if not flagged and not failures:
        lines.append("- none")
    for f in failures:
        lines.append(f"- {f}")
    for r in flagged:
        lines.append(f"### {r['env']} {r['config']} seed={r['seed']} status={r['status']}")
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


def update_tracking_and_push(results):
    now = ts()
    existing = TRACKING.read_text(errors="ignore") if TRACKING.exists() else "# ValueFlows Task-Level Tracking\n"
    lines = [
        "",
        f"## 4090D best-seed five-task reliability SB v2 ({now})",
        "",
        f"Report: `{REPORT.relative_to(ROOT)}`",
        "",
        "| env | paper VF | method/config | seed | steps | success | return | length | gap | machine | selected_eval_csv | status |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]
    for r in sorted(results, key=lambda x: (x["queue"], x["env"], x["config"])):
        base, label = PAPER.get(r["env"], (math.nan, ""))
        gap = r["success"] - base if not math.isnan(r["success"]) and not math.isnan(base) else math.nan
        method = "R2" if "R2_" in r["config"] else "R3" if "R3_" in r["config"] else "A1"
        lines.append(
            f"| {r['env']} | {label} | {method}/{r['config']} | {r['seed']} | {r['steps']} | {fmt(r['success'])} | "
            f"{fmt(r['return'])} | {fmt(r['length'])} | {fmt(gap)} | 4090D | `{r['selected_eval_csv']}` | {r['status']} |"
        )
    TRACKING.write_text(existing.rstrip() + "\n" + "\n".join(lines) + "\n")
    subprocess.run(["git", "add", "reports/valueflows_task_level_tracking.md", str(REPORT.relative_to(ROOT)), "scripts/run_bestseed_5task_push_4090d_v2.py"], cwd=ROOT)
    commit = subprocess.run(["git", "commit", "-m", "Update 4090D five-task best-seed results with robust CSV parsing"], cwd=ROOT, text=True, capture_output=True)
    (LOG_DIR / "git_commit.log").write_text(commit.stdout + commit.stderr)
    if commit.returncode != 0:
        return f"git commit failed: {commit.stdout} {commit.stderr}"
    push = subprocess.run(["git", "push", "origin", "HEAD:results/bestseed-5task-4090d-v2"], cwd=ROOT, text=True, capture_output=True)
    (LOG_DIR / "git_push.log").write_text(push.stdout + push.stderr)
    if push.returncode != 0:
        return f"git push failed: {push.stdout} {push.stderr}"
    return ""


def main():
    queue_a = [
        Task("queueA_cube_triple_5task_1m", f"cube-triple-play-singletask-task{i}-v0", "R2_flow_residual_disagree_std_lam0p001", 2, 1_000_000)
        for i in range(1, 6)
    ]
    queue_b = []
    for prefix in ["cube-double-play", "scene-play"]:
        for i in range(1, 6):
            env = f"{prefix}-singletask-task{i}-v0"
            for cfg in ["A1_action_std_lam0p001", "R2_flow_residual_disagree_std_lam0p001", "R3_flow_residual_disagree_typicality_std_lam0p001"]:
                queue_b.append(Task("queueB_screen_300k", env, cfg, 2, 300_000))
    total = len(queue_a) + len(queue_b)
    pending_a = list(queue_a)
    pending_b = list(queue_b)
    running = {}
    procs = {}
    results = []
    failures = []
    completed = failed = warning = 0
    log_status(total, completed, failed, warning, running, len(pending_a) + len(pending_b))
    last_status = 0
    while pending_a or pending_b or procs:
        for gpu, proc in list(procs.items()):
            if proc.poll() is None:
                continue
            task = running.pop(gpu)
            procs.pop(gpu)
            res = parse_result(task, proc.returncode)
            results.append(res)
            if res["status"] == "COMPLETE":
                completed += 1
            elif res["status"] == "COMPLETE_WITH_WARNING":
                warning += 1
            else:
                failed += 1
            write_report(results, failures)
            log_status(total, completed, failed, warning, running, len(pending_a) + len(pending_b))
        for gpu in [0, 1]:
            if gpu in procs:
                continue
            task = None
            if pending_a:
                task = pending_a.pop(0)
            elif pending_b:
                task = pending_b.pop(0)
            if task is None:
                continue
            existing = parse_result(task, 0)
            if existing["selected_eval_csv"] and existing["eval_rows"] > 0:
                existing["status"] = "SKIPPED_COMPLETE"
                results.append(existing)
                completed += 1
                write_report(results, failures)
                log_status(total, completed, failed, warning, running, len(pending_a) + len(pending_b))
                continue
            try:
                proc = launch(task, gpu)
            except Exception as exc:
                failures.append(f"launch failed {task}: {exc!r}")
                failed += 1
                continue
            running[gpu] = task
            procs[gpu] = proc
            log_status(total, completed, failed, warning, running, len(pending_a) + len(pending_b))
        if time.time() - last_status > 300:
            log_status(total, completed, failed, warning, running, len(pending_a) + len(pending_b))
            last_status = time.time()
        time.sleep(30)
    write_report(results, failures)
    err = update_tracking_and_push(results)
    if err:
        failures.append(err)
        write_report(results, failures)
    log_status(total, completed, failed, warning, running, 0)


if __name__ == "__main__":
    main()

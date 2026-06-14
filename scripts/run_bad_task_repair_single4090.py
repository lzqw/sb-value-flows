#!/usr/bin/env python3
"""Bad-task repair and positive-mining sweep on a single 4090."""

from __future__ import annotations

import csv
import math
import os
import shlex
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


EXP = "bad_task_repair_single4090"
REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "run_bad_task_repair_single4090.py"
SAVE_ROOT = REPO_ROOT / "exp" / EXP
LOG_ROOT = REPO_ROOT / "logs" / EXP
REPORT_PATH = REPO_ROOT / "reports" / f"{EXP}_report.md"
TRACKING_PATH = REPO_ROOT / "reports" / "valueflows_task_level_tracking.md"
STATUS_PATH = LOG_ROOT / "status.txt"
DATA_ROOT = Path("/root/.ogbench/data")
MUJOCO_BIN = "/root/.mujoco/mujoco210/bin"
CONDA_BIN = "/root/miniconda3/bin/conda"
RESULT_BRANCH = "results/bad-task-repair-single4090"
EXPECTED_HEAD = "8beb46e642965e399802e40e6cf94a5238cdfad6"
RESUME = os.environ.get("BAD_TASK_REPAIR_RESUME", "").lower() in {"1", "true", "yes"}

SCREEN_STEPS = 300_000
CONFIRM_STEPS = 1_000_000
SCREEN_SEED = 2
CONFIRM_SEED = 2
EXTENSION_SEEDS = [0, 1]

AGENT_FLAG = "--agent=agents/pm_value_flows.py"
COMMON_AGENT_FLAGS = [
    "--agent.pm_minimal_sb=true",
    "--agent.pm_weight_type=field_kernel_norm",
    "--agent.pm_num_continuations=4",
    "--agent.pm_field_kernel_norm_temp=0.3",
    "--agent.pm_field_kernel_min_scale=1e-6",
    "--agent.pm_actor_energy_coef=0.0",
    "--agent.pm_actor_disagree_coef=0.0",
    "--agent.pm_log_sb_diagnostics=true",
]

CONFIGS: list[tuple[str, list[str]]] = [
    (
        "P0_particle",
        [
            "--agent.pm_sb_reliability_score=action",
            "--agent.pm_sb_lambda=0.0",
            "--agent.pm_sb_reliability_normalize=none",
            "--agent.pm_sb_value_preserving=false",
        ],
    ),
    (
        "MinimalSB_lam0p0003",
        [
            "--agent.pm_sb_reliability_score=action",
            "--agent.pm_sb_lambda=0.0003",
            "--agent.pm_sb_reliability_normalize=none",
            "--agent.pm_sb_value_preserving=false",
        ],
    ),
    (
        "MinimalSB_lam0p001",
        [
            "--agent.pm_sb_reliability_score=action",
            "--agent.pm_sb_lambda=0.001",
            "--agent.pm_sb_reliability_normalize=none",
            "--agent.pm_sb_value_preserving=false",
        ],
    ),
    (
        "A1_action_std_lam0p001",
        [
            "--agent.pm_sb_reliability_score=action",
            "--agent.pm_sb_lambda=0.001",
            "--agent.pm_sb_reliability_normalize=std",
            "--agent.pm_sb_value_preserving=false",
        ],
    ),
    (
        "A2_action_std_lam0p003",
        [
            "--agent.pm_sb_reliability_score=action",
            "--agent.pm_sb_lambda=0.003",
            "--agent.pm_sb_reliability_normalize=std",
            "--agent.pm_sb_value_preserving=false",
        ],
    ),
    (
        "R2_residual_disagree_lam0p001",
        [
            "--agent.pm_sb_reliability_score=flow_residual_disagree",
            "--agent.pm_sb_lambda=0.001",
            "--agent.pm_sb_reliability_normalize=std",
            "--agent.pm_sb_flow_residual_eps=0.05",
            "--agent.pm_sb_disagree_beta=0.5",
            "--agent.pm_sb_disagree_umax=3.0",
            "--agent.pm_sb_value_preserving=false",
        ],
    ),
    (
        "R3_residual_disagree_typicality_lam0p001",
        [
            "--agent.pm_sb_reliability_score=flow_residual_disagree_typicality",
            "--agent.pm_sb_lambda=0.001",
            "--agent.pm_sb_reliability_normalize=std",
            "--agent.pm_sb_flow_residual_eps=0.05",
            "--agent.pm_sb_disagree_beta=0.5",
            "--agent.pm_sb_disagree_umax=3.0",
            "--agent.pm_sb_typicality_tau=1.0",
            "--agent.pm_sb_value_preserving=false",
        ],
    ),
]
CONFIG_FLAGS = dict(CONFIGS)


@dataclass(frozen=True)
class TaskSpec:
    env: str
    paper: float
    current_success: float | None
    current_return: float | None
    current_length: float | None
    official_flags: tuple[str, ...]
    low_paper_positive: bool = False


TASKS: list[TaskSpec] = [
    TaskSpec("puzzle-3x3-play-singletask-task3-v0", 0.97, 0.1, -1120.3, 473.8, ("--agent.bcfm_lambda=0.5", "--agent.ret_agg=min")),
    TaskSpec("scene-play-singletask-task4-v0", 0.07, 0.0, None, None, ("--agent.ret_agg=min",), True),
    TaskSpec("cube-double-play-singletask-task2-v0", 0.76, 0.0, None, None, ("--agent.discount=0.995", "--agent.confidence_weight_temp=3")),
    TaskSpec("cube-double-play-singletask-task3-v0", 0.73, 0.0, None, None, ("--agent.discount=0.995", "--agent.confidence_weight_temp=3")),
    TaskSpec("cube-double-play-singletask-task4-v0", 0.30, 0.0, None, None, ("--agent.discount=0.995", "--agent.confidence_weight_temp=3")),
    TaskSpec("puzzle-4x4-play-singletask-task5-v0", 0.13, 0.0, None, None, ("--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=100", "--agent.q_agg=min"), True),
    TaskSpec("puzzle-4x4-play-singletask-task2-v0", 0.27, 0.0, None, None, ("--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=100", "--agent.q_agg=min")),
    TaskSpec("puzzle-4x4-play-singletask-task4-v0", 0.28, 0.0, None, None, ("--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=100", "--agent.q_agg=min")),
    TaskSpec("cube-triple-play-singletask-task3-v0", 0.07, 0.0, None, None, ("--agent.discount=0.995", "--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=0.03"), True),
]
TASK_BY_ENV = {task.env: task for task in TASKS}

MINIMAL_SB_SEED2 = {
    "puzzle-3x3-play-singletask-task1-v0": 1.0,
    "puzzle-3x3-play-singletask-task2-v0": 1.0,
    "puzzle-3x3-play-singletask-task3-v0": 0.1,
    "puzzle-3x3-play-singletask-task4-v0": 1.0,
    "puzzle-3x3-play-singletask-task5-v0": 1.0,
}

SUCCESS_KEYS = ["evaluation/success", "eval/success", "success"]
RETURN_KEYS = ["evaluation/return", "eval/return", "return", "evaluation/episode.return", "eval/episode.return", "episode.return"]
LENGTH_KEYS = ["evaluation/length", "eval/length", "length", "evaluation/episode.length", "eval/episode.length", "episode.length"]
DIAG_KEYS = [
    "pm/weight_max",
    "pm/ess",
    "pm/action_mean",
    "pm/action_std",
    "pm/proj_delta_mean",
    "pm/corr_y_action",
    "pm/cov_y_action",
    "pm/reliability_mean",
    "pm/reliability_std",
    "pm/flow_residual_mean",
    "pm/flow_residual_std",
    "pm/disagree_mean",
    "pm/disagree_std",
    "pm/typicality_mean",
    "pm/typicality_std",
]


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def rel(path: Path | str | None) -> str:
    if not path:
        return ""
    p = Path(path)
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def status(line: str) -> None:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    with STATUS_PATH.open("a", encoding="utf-8") as f:
        f.write(f"[{now()}] {line}\n")


def run_text(cmd: list[str], timeout: int = 120) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=timeout)
        return proc.returncode, proc.stdout
    except Exception as exc:  # noqa: BLE001
        return 999, f"ERROR {cmd}: {exc}"


def shell_join(cmd: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in cmd)


def to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fmt(value: Any) -> str:
    val = to_float(value)
    if val is None:
        return ""
    if math.isnan(val):
        return "nan"
    if math.isinf(val):
        return "inf" if val > 0 else "-inf"
    return f"{val:.6g}"


def mean(vals: list[float]) -> float | None:
    clean = [v for v in vals if not math.isnan(v) and not math.isinf(v)]
    return sum(clean) / len(clean) if clean else None


def std(vals: list[float]) -> float | None:
    clean = [v for v in vals if not math.isnan(v) and not math.isinf(v)]
    if not clean:
        return None
    if len(clean) == 1:
        return 0.0
    m = sum(clean) / len(clean)
    return math.sqrt(sum((v - m) ** 2 for v in clean) / (len(clean) - 1))


def read_csv_rows(path: Path | None) -> list[dict[str, str]]:
    if path is None or not path.exists():
        return []
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        return list(csv.DictReader(f))


def select_csv(run_dir: Path | None, patterns: list[str]) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    if run_dir is None or not run_dir.exists():
        return None, []
    paths: list[Path] = []
    seen: set[Path] = set()
    for pattern in patterns:
        for path in run_dir.rglob(pattern):
            if path.is_file() and path not in seen:
                paths.append(path)
                seen.add(path)
    candidates: list[dict[str, Any]] = []
    for path in paths:
        rows = read_csv_rows(path)
        candidates.append(
            {
                "path": path,
                "rows": len(rows),
                "mtime": path.stat().st_mtime,
                "mtime_str": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "data": rows,
            }
        )
    if not candidates:
        return None, []
    return max(candidates, key=lambda item: (item["rows"], item["mtime"])), candidates


def pick(row: dict[str, str], keys: list[str]) -> str:
    for key in keys:
        if row.get(key, "") != "":
            return row[key]
    return ""


def last_nonempty(rows: list[dict[str, str]], keys: list[str]) -> str:
    for row in reversed(rows):
        value = pick(row, keys)
        if value != "":
            return value
    return ""


def diag_value(rows: list[dict[str, str]], name: str) -> str:
    suffix = name.split("/", 1)[1]
    return last_nonempty(
        rows,
        [
            f"training/critic/pm/{suffix}",
            f"training/pm/{suffix}",
            f"training/critic/{name}",
            name,
        ],
    )


def make_env() -> dict[str, str]:
    env = os.environ.copy()
    old_ld = env.get("LD_LIBRARY_PATH", "")
    env.update(
        {
            "CUDA_VISIBLE_DEVICES": "0",
            "LD_LIBRARY_PATH": f"{MUJOCO_BIN}:{old_ld}" if old_ld else MUJOCO_BIN,
            "MUJOCO_GL": "egl",
            "PYOPENGL_PLATFORM": "egl",
            "SDL_VIDEODRIVER": "dummy",
            "OGBENCH_DATA_DIR": str(DATA_ROOT),
            "XLA_PYTHON_CLIENT_PREALLOCATE": "true",
            "XLA_PYTHON_CLIENT_MEM_FRACTION": "0.90",
            "HOME": "/root",
            "XDG_CACHE_HOME": "/root/.cache",
            "PATH": "/root/miniconda3/bin:" + env.get("PATH", ""),
        }
    )
    return env


def assert_agent_order(flags: list[str]) -> None:
    agent_idx = flags.index(AGENT_FLAG)
    bad = [(idx, flag) for idx, flag in enumerate(flags) if flag.startswith("--agent.") and idx < agent_idx]
    if bad:
        raise RuntimeError(f"{AGENT_FLAG} must appear before all --agent.* flags; bad={bad}")


def slug_env(env: str) -> str:
    return env.replace("-play-singletask-", "-").replace("-v0", "").replace("-", "_")


def group_name(stage: str, env: str, config: str, seed: int) -> str:
    return f"{stage}_{slug_env(env)}_{config}_seed{seed}"


def newest_run_dir(stage: str, env: str, config: str, seed: int, start_time: float | None = None) -> Path | None:
    root = SAVE_ROOT / group_name(stage, env, config, seed)
    if not root.exists():
        return None
    dirs = [p for p in root.iterdir() if p.is_dir() and p.name.startswith(f"sd{seed:03d}_")]
    if start_time is not None:
        recent = [p for p in dirs if p.stat().st_mtime >= start_time - 2]
        if recent:
            dirs = recent
    return max(dirs, key=lambda p: p.stat().st_mtime) if dirs else None


def run_dirs(stage: str, env: str, config: str, seed: int) -> list[Path]:
    root = SAVE_ROOT / group_name(stage, env, config, seed)
    if not root.exists():
        return []
    dirs = [p for p in root.iterdir() if p.is_dir() and p.name.startswith(f"sd{seed:03d}_")]
    return sorted(dirs, key=lambda p: p.stat().st_mtime)


def build_flags(stage: str, task: TaskSpec, config: str, seed: int, steps: int) -> list[str]:
    flags = [
        f"--env_name={task.env}",
        f"--seed={seed}",
        f"--save_dir={SAVE_ROOT}",
        f"--wandb_run_group={group_name(stage, task.env, config, seed)}",
        "--enable_wandb=0",
        f"--offline_steps={steps}",
        "--online_steps=0",
        "--eval_interval=50000",
        "--eval_episodes=10",
        "--log_interval=25000",
        "--save_interval=999999999",
        AGENT_FLAG,
        *task.official_flags,
        *COMMON_AGENT_FLAGS,
        *CONFIG_FLAGS[config],
    ]
    assert_agent_order(flags)
    return flags


def summarize(
    stage: str,
    task: TaskSpec,
    config: str,
    seed: int,
    steps: int,
    run_dir: Path | None,
    log_path: Path,
    returncode: int,
    duration: float,
    command: list[str],
) -> dict[str, Any]:
    selected_eval, eval_candidates = select_csv(run_dir, ["eval.csv"])
    selected_train, train_candidates = select_csv(run_dir, ["train.csv"])
    eval_rows = selected_eval["data"] if selected_eval else []
    train_rows = selected_train["data"] if selected_train else []
    final_eval = eval_rows[-1] if eval_rows else {}
    success = pick(final_eval, SUCCESS_KEYS)
    ret = pick(final_eval, RETURN_KEYS)
    length = pick(final_eval, LENGTH_KEYS)
    if final_eval and returncode == 0:
        run_status = "COMPLETE"
    elif final_eval and returncode != 0:
        run_status = "COMPLETE_WITH_WARNING"
    elif returncode == 0:
        run_status = "CSV_MISSING"
    else:
        run_status = "FAILED"
    result: dict[str, Any] = {
        "stage": stage,
        "env": task.env,
        "config": config,
        "seed": seed,
        "steps": steps,
        "paper": task.paper,
        "current_success": task.current_success,
        "status": run_status,
        "returncode": returncode,
        "duration_sec": duration,
        "run_dir": rel(run_dir),
        "log_path": rel(log_path),
        "command": shell_join(command),
        "selected_eval_csv": rel(selected_eval["path"]) if selected_eval else "",
        "selected_eval_rows": selected_eval["rows"] if selected_eval else 0,
        "selected_train_csv": rel(selected_train["path"]) if selected_train else "",
        "selected_train_rows": selected_train["rows"] if selected_train else 0,
        "eval_candidates": [
            {"path": rel(item["path"]), "rows": item["rows"], "mtime": item["mtime_str"]}
            for item in sorted(eval_candidates, key=lambda x: str(x["path"]))
        ],
        "train_candidates": [
            {"path": rel(item["path"]), "rows": item["rows"], "mtime": item["mtime_str"]}
            for item in sorted(train_candidates, key=lambda x: str(x["path"]))
        ],
        "final_step": pick(final_eval, ["step"]),
        "success": success,
        "return": ret,
        "length": length,
    }
    succ = to_float(success)
    result["gap_vs_paper"] = (succ - task.paper) if succ is not None else None
    result["success_improvement"] = (succ - task.current_success) if succ is not None and task.current_success is not None else None
    ret_val = to_float(ret)
    len_val = to_float(length)
    result["return_improvement"] = (ret_val - task.current_return) if ret_val is not None and task.current_return is not None else None
    result["length_delta"] = (len_val - task.current_length) if len_val is not None and task.current_length is not None else None
    for key in DIAG_KEYS:
        result[key] = diag_value(train_rows, key)
    weight_max = to_float(result.get("pm/weight_max"))
    result["collapse"] = bool(weight_max is not None and weight_max > 0.95)
    return result


def log_tail(path: str, lines: int = 80) -> str:
    if not path:
        return ""
    p = REPO_ROOT / path
    if not p.exists():
        return ""
    return "\n".join(p.read_text(encoding="utf-8", errors="replace").splitlines()[-lines:])


def run_one(stage: str, task: TaskSpec, config: str, seed: int, steps: int) -> dict[str, Any]:
    flags = build_flags(stage, task, config, seed, steps)
    cmd = [CONDA_BIN, "run", "-n", "value-flows", "python", "main.py", *flags]
    log_path = LOG_ROOT / f"{group_name(stage, task.env, config, seed)}.log"
    status(f"START {stage} env={task.env} config={config} seed={seed} steps={steps}")
    start = time.time()
    with log_path.open("w", encoding="utf-8", errors="replace") as f:
        f.write("COMMAND: " + shell_join(cmd) + "\n")
        f.write("COMMAND_ORDER_RULE: --agent=agents/pm_value_flows.py appears before all --agent.* flags\n")
        f.write("NO_PM_ACTION_NORMALIZE_FLAG\n")
        f.flush()
        proc = subprocess.run(cmd, cwd=REPO_ROOT, stdout=f, stderr=subprocess.STDOUT, env=make_env())
    result = summarize(stage, task, config, seed, steps, newest_run_dir(stage, task.env, config, seed, start), log_path, proc.returncode, time.time() - start, cmd)
    status(
        f"{result['status']} {stage} env={task.env} config={config} seed={seed} "
        f"success={fmt(result.get('success'))} return={fmt(result.get('return'))} length={fmt(result.get('length'))} "
        f"collapse={result.get('collapse')} selected_eval_csv={result.get('selected_eval_csv')}"
    )
    return result


def result_is_complete(result: dict[str, Any], steps: int) -> bool:
    step = to_float(result.get("final_step"))
    return bool(result.get("selected_eval_csv")) and step is not None and step >= steps


def existing_complete_result(stage: str, task: TaskSpec, config: str, seed: int, steps: int) -> dict[str, Any] | None:
    results: list[dict[str, Any]] = []
    flags = build_flags(stage, task, config, seed, steps)
    cmd = [CONDA_BIN, "run", "-n", "value-flows", "python", "main.py", *flags]
    log_path = LOG_ROOT / f"{group_name(stage, task.env, config, seed)}.log"
    for run_dir in run_dirs(stage, task.env, config, seed):
        result = summarize(stage, task, config, seed, steps, run_dir, log_path, 0, 0.0, cmd)
        if result_is_complete(result, steps):
            result["status"] = "COMPLETE"
            result["resume_reused"] = True
            results.append(result)
    if not results:
        return None

    def sort_key(result: dict[str, Any]) -> tuple[float, int, float]:
        eval_path = result.get("selected_eval_csv", "")
        mtime = 0.0
        if eval_path:
            path = REPO_ROOT / eval_path
            if path.exists():
                mtime = path.stat().st_mtime
        final_step = to_float(result.get("final_step"))
        return (final_step if final_step is not None else -1.0, int(result.get("selected_eval_rows", 0)), mtime)

    return max(results, key=sort_key)


def run_or_reuse(stage: str, task: TaskSpec, config: str, seed: int, steps: int) -> dict[str, Any]:
    if RESUME:
        result = existing_complete_result(stage, task, config, seed, steps)
        if result is not None:
            status(
                f"RESUME_SKIP {stage} env={task.env} config={config} seed={seed} "
                f"success={fmt(result.get('success'))} return={fmt(result.get('return'))} length={fmt(result.get('length'))} "
                f"selected_eval_csv={result.get('selected_eval_csv')}"
            )
            return result
    return run_one(stage, task, config, seed, steps)


def no_other_jobs() -> tuple[bool, str]:
    code, out = run_text(["ps", "-eo", "pid,ppid,etime,stat,cmd"], timeout=60)
    if code != 0:
        return False, out
    own = os.getpid()
    parent = os.getppid()
    busy: list[str] = []
    for line in out.splitlines()[1:]:
        parts = line.strip().split(None, 4)
        if len(parts) < 5:
            continue
        try:
            pid = int(parts[0])
            ppid = int(parts[1])
        except ValueError:
            continue
        cmd = parts[4]
        if pid in {own, parent} or ppid in {own, parent}:
            continue
        if EXP in cmd:
            continue
        if "main.py" in cmd or ("run_" in cmd and ".py" in cmd) or "runner" in cmd:
            if "tensorboard" not in cmd.lower():
                busy.append(line)
    return not busy, "\n".join(busy)


def gpu_idle() -> tuple[bool, str]:
    code, out = run_text(["nvidia-smi", "--query-gpu=memory.used,utilization.gpu", "--format=csv,noheader,nounits"], timeout=60)
    if code != 0:
        return False, out
    parts = out.strip().splitlines()[0].split(",")
    mem = int(parts[0].strip())
    util = int(parts[1].strip())
    return mem < 1000 and util < 10, f"memory.used={mem} MiB utilization.gpu={util}%"


def preflight() -> bool:
    status("PREFLIGHT_START")
    if RESUME:
        status("RESUME_MODE enabled: existing completed runs will be reused; incomplete runs will be rerun in new timestamp dirs")
    branch = run_text(["git", "branch", "--show-current"])[1].strip()
    head = run_text(["git", "rev-parse", "HEAD"])[1].strip()
    diff = run_text(["git", "diff", "--stat", "HEAD", "origin/codex/fix-reliability-calibrated-sb-code"])[1].strip()
    status(f"GIT branch={branch} head={head} origin_diff_stat={diff or 'EMPTY'}")
    if branch != "reliability-calibrated-sb" or head != EXPECTED_HEAD or diff:
        status("ABORT wrong reliability branch state")
        return False
    jobs_ok, jobs_msg = no_other_jobs()
    status("PROCESS_IDLE " + ("ok" if jobs_ok else jobs_msg))
    if not jobs_ok:
        return False
    gpu_ok, gpu_msg = gpu_idle()
    status("GPU_IDLE " + gpu_msg)
    if not gpu_ok:
        return False
    if SAVE_ROOT.exists() and any(SAVE_ROOT.iterdir()) and not RESUME:
        status(f"ABORT output exp dir already has contents: {rel(SAVE_ROOT)}")
        return False
    if REPORT_PATH.exists() and not RESUME:
        status(f"ABORT report already exists: {rel(REPORT_PATH)}")
        return False
    return True


def best_screen_results(results: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    best: dict[str, dict[str, Any]] = {}
    for result in results:
        if result["stage"] != "stageA_300k" or result["status"] not in {"COMPLETE", "COMPLETE_WITH_WARNING"}:
            continue
        env = result["env"]
        current = best.get(env)
        key = (
            to_float(result.get("success")) if to_float(result.get("success")) is not None else -1e9,
            to_float(result.get("return")) if to_float(result.get("return")) is not None else -1e9,
            -(to_float(result.get("length")) if to_float(result.get("length")) is not None else 1e9),
        )
        if current is None:
            best[env] = result
            continue
        cur_key = (
            to_float(current.get("success")) if to_float(current.get("success")) is not None else -1e9,
            to_float(current.get("return")) if to_float(current.get("return")) is not None else -1e9,
            -(to_float(current.get("length")) if to_float(current.get("length")) is not None else 1e9),
        )
        if key > cur_key:
            best[env] = result
    return best


def qualifies_for_confirm(task: TaskSpec, result: dict[str, Any]) -> tuple[bool, str]:
    success = to_float(result.get("success"))
    ret_improve = to_float(result.get("return_improvement"))
    len_delta = to_float(result.get("length_delta"))
    succ_improve = to_float(result.get("success_improvement"))
    ret = to_float(result.get("return"))
    length = to_float(result.get("length"))
    if success is not None and success >= 0.5:
        return True, "A: success >= 0.5"
    if succ_improve is not None and succ_improve >= 0.2:
        return True, "B: success improved >= 0.2"
    if task.low_paper_positive and success is not None and success >= 0.2:
        return True, "C: low-paper positive signal success >= 0.2"
    if ret_improve is not None and len_delta is not None and ret_improve >= 100 and len_delta <= -50:
        return True, "D: return and length improved"
    if task.current_return is None and success is not None and success > 0 and ret is not None and length is not None and length < 500:
        return True, "positive mining: nonzero success with finite progress"
    return False, "not selected"


def qualifies_for_seed_extension(task: TaskSpec, result: dict[str, Any]) -> tuple[bool, str]:
    success = to_float(result.get("success"))
    if success is None:
        return False, "missing success"
    if success >= task.paper:
        return True, "1M success >= paper baseline"
    if success >= 0.5:
        return True, "1M success >= 0.5"
    if task.low_paper_positive and success >= 0.2:
        return True, "low-paper task and 1M success >= 0.2"
    return False, "not extended"


def candidate_list(candidates: list[dict[str, Any]]) -> str:
    if not candidates:
        return "None"
    return "<br>".join(f"{x['path']} (rows={x['rows']}, mtime={x['mtime']})" for x in candidates)


def aggregate(rows: list[dict[str, Any]], env: str, config: str, key: str) -> tuple[float | None, float | None, int]:
    vals = [
        to_float(row.get(key))
        for row in rows
        if row["stage"] in {"stageB_seed2_1m", "stageB_seedext_1m"} and row["env"] == env and row["config"] == config and row["status"] in {"COMPLETE", "COMPLETE_WITH_WARNING"}
    ]
    clean = [v for v in vals if v is not None]
    return mean(clean), std(clean), len(clean)


def generate_report(results: list[dict[str, Any]], selected: dict[str, tuple[dict[str, Any], str]] | None = None, final_note: str = "") -> None:
    selected = selected or {}
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    branch = run_text(["git", "branch", "--show-current"])[1].strip()
    head = run_text(["git", "rev-parse", "HEAD"])[1].strip()
    git_status = run_text(["git", "status", "--short"])[1].rstrip()
    nvidia = run_text(["nvidia-smi"])[1].rstrip()
    best = best_screen_results(results)
    lines = [
        "# Bad-Task Repair Single4090",
        "",
        f"Generated: {now()}",
        "",
        "Screening results are for positive mining. This is not the full official 8-seed protocol. Bad seed behavior during exploration does not directly falsify a method.",
        "",
        "## Setup",
        "",
        f"- branch: {branch}",
        f"- HEAD: {head}",
        "- required source: origin/codex/fix-reliability-calibrated-sb-code",
        "- no pm_action_normalize flag is used",
        "- all --agent.* flags are after --agent=agents/pm_value_flows.py",
        "- Stage A: 9 tasks x 7 configs x seed2 x 300k",
        "- Stage B: selected best config per task, seed2 x 1M; optional seeds 0,1 extension",
        "- result rule: final selected eval.csv last row only; no mean, no max, no best checkpoint",
        "- CSV finder: recursive run_dir/**/eval.csv and run_dir/**/train.csv; most rows, then newest mtime",
    ]
    if final_note:
        lines.append(f"- final note: {final_note}")
    lines += [
        "",
        "## Existing Minimal SB Seed2 Reference",
        "",
        "| task | success |",
        "|---|---:|",
    ]
    for env, success in MINIMAL_SB_SEED2.items():
        lines.append(f"| {env} | {success:.3g} |")
    lines += [
        "| domain mean | 0.82 |",
        "",
        "## Stage A 300k Screening",
        "",
        "| env | config | status | success | return | length | paper baseline | gap vs paper | selected_eval_csv |",
        "|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for result in [r for r in results if r["stage"] == "stageA_300k"]:
        lines.append(
            f"| {result['env']} | {result['config']} | {result['status']} | {fmt(result.get('success'))} | {fmt(result.get('return'))} | "
            f"{fmt(result.get('length'))} | {fmt(result.get('paper'))} | {fmt(result.get('gap_vs_paper'))} | {result.get('selected_eval_csv')} |"
        )
    lines += [
        "",
        "## Best Config Per Task",
        "",
        "| env | best config | success | return | length | selected for 1M | reason |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for task in TASKS:
        row = best.get(task.env)
        if row is None:
            lines.append(f"| {task.env} |  |  |  |  | False | no completed Stage A result |")
            continue
        pick_info = selected.get(task.env)
        lines.append(
            f"| {task.env} | {row['config']} | {fmt(row.get('success'))} | {fmt(row.get('return'))} | {fmt(row.get('length'))} | "
            f"{bool(pick_info)} | {pick_info[1] if pick_info else 'not selected'} |"
        )
    lines += [
        "",
        "## Stage B 1M Confirmation",
        "",
        "| env | config | seed | status | success | return | length | paper baseline | gap vs paper | selected_eval_csv |",
        "|---|---|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for result in [r for r in results if r["stage"] in {"stageB_seed2_1m", "stageB_seedext_1m"}]:
        lines.append(
            f"| {result['env']} | {result['config']} | {result['seed']} | {result['status']} | {fmt(result.get('success'))} | "
            f"{fmt(result.get('return'))} | {fmt(result.get('length'))} | {fmt(result.get('paper'))} | {fmt(result.get('gap_vs_paper'))} | "
            f"{result.get('selected_eval_csv')} |"
        )
    lines += [
        "",
        "## 3-Seed Extension Aggregate",
        "",
        "| env | config | n | success mean | success std | return mean | return std | length mean | length std |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for env, config in sorted({(r["env"], r["config"]) for r in results if r["stage"] in {"stageB_seed2_1m", "stageB_seedext_1m"}}):
        succ_m, succ_s, n = aggregate(results, env, config, "success")
        ret_m, ret_s, _ = aggregate(results, env, config, "return")
        len_m, len_s, _ = aggregate(results, env, config, "length")
        lines.append(f"| {env} | {config} | {n} | {fmt(succ_m)} | {fmt(succ_s)} | {fmt(ret_m)} | {fmt(ret_s)} | {fmt(len_m)} | {fmt(len_s)} |")
    lines += [
        "",
        "## Diagnostics",
        "",
        "| stage | env | config | seed | " + " | ".join(DIAG_KEYS) + " | collapse |",
        "|---|---|---|---:|" + "|".join(["---:"] * len(DIAG_KEYS)) + "|---|",
    ]
    for result in results:
        values = " | ".join(fmt(result.get(key)) for key in DIAG_KEYS)
        lines.append(f"| {result['stage']} | {result['env']} | {result['config']} | {result['seed']} | {values} | {result.get('collapse')} |")
    lines += [
        "",
        "## CSV Candidates",
        "",
        "| stage | env | config | seed | selected_eval_csv | all eval candidates | selected_train_csv | all train candidates |",
        "|---|---|---|---:|---|---|---|---|",
    ]
    for result in results:
        lines.append(
            f"| {result['stage']} | {result['env']} | {result['config']} | {result['seed']} | {result.get('selected_eval_csv')} | "
            f"{candidate_list(result.get('eval_candidates', []))} | {result.get('selected_train_csv')} | {candidate_list(result.get('train_candidates', []))} |"
        )
    failed = [r for r in results if r["status"] not in {"COMPLETE", "COMPLETE_WITH_WARNING"}]
    lines += ["", "## Failed Or Warning Summary", ""]
    if not failed:
        lines.append("No failed or warning runs.")
    else:
        lines.append("| stage | env | config | run_dir | status | error tail | eval candidates |")
        lines.append("|---|---|---|---|---|---|---|")
        for row in failed:
            tail = log_tail(row.get("log_path", ""), 30).replace("\n", "<br>")
            lines.append(f"| {row['stage']} | {row['env']} | {row['config']} | {row.get('run_dir')} | {row['status']} | {tail} | {candidate_list(row.get('eval_candidates', []))} |")
    lines += [
        "",
        "## Final Recommendations",
        "",
    ]
    positive = []
    continue_seed = []
    stop = []
    for task in TASKS:
        selected_row = selected.get(task.env)
        stage_b = [r for r in results if r["env"] == task.env and r["stage"] in {"stageB_seed2_1m", "stageB_seedext_1m"} and r["status"] in {"COMPLETE", "COMPLETE_WITH_WARNING"}]
        if stage_b:
            best_b = max(stage_b, key=lambda r: (to_float(r.get("success")) or -1, to_float(r.get("return")) or -1e9))
            succ = to_float(best_b.get("success"))
            if succ is not None and (succ >= 0.5 or (task.low_paper_positive and succ >= 0.2) or (task.current_success is not None and succ - task.current_success >= 0.2)):
                positive.append(f"- {task.env}: keep {best_b['config']} as positive result, success={fmt(succ)}.")
            if len(stage_b) < 3 and succ is not None and succ > 0:
                continue_seed.append(f"- {task.env}: consider more seeds for {best_b['config']}.")
        elif selected_row:
            continue_seed.append(f"- {task.env}: selected for 1M but no complete confirmation yet.")
        else:
            stop.append(f"- {task.env}: no Stage A signal; deprioritize for now.")
    lines += ["### Positive Results", *(positive or ["None yet."])]
    lines += ["", "### Needs More Seeds", *(continue_seed or ["None."])]
    lines += ["", "### Stop Or Deprioritize", *(stop or ["None."])]
    lines += [
        "",
        "## nvidia-smi",
        "```text",
        nvidia,
        "```",
        "",
        "## git status --short",
        "```text",
        git_status,
        "```",
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_tracking(results: list[dict[str, Any]], selected: dict[str, tuple[dict[str, Any], str]]) -> None:
    TRACKING_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Value Flows task-level tracking table",
        "",
        "This file tracks task-level baselines from the Value Flows paper and current server repair runs.",
        "",
        "## Bad-Task Repair Single4090",
        "",
        "Screening results are for positive mining and are not the full official 8-seed protocol.",
        "",
        "| stage | env | config | seed | steps | success | return | length | paper baseline | gap vs paper | current success | selected_eval_csv | status | report |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]
    for row in results:
        lines.append(
            f"| {row['stage']} | {row['env']} | {row['config']} | {row['seed']} | {row['steps']} | {fmt(row.get('success'))} | "
            f"{fmt(row.get('return'))} | {fmt(row.get('length'))} | {fmt(row.get('paper'))} | {fmt(row.get('gap_vs_paper'))} | "
            f"{fmt(row.get('current_success'))} | {row.get('selected_eval_csv')} | {row['status']} | {rel(REPORT_PATH)} |"
        )
    lines += [
        "",
        "## Stage B Selection",
        "",
        "| env | selected config | reason |",
        "|---|---|---|",
    ]
    for task in TASKS:
        info = selected.get(task.env)
        lines.append(f"| {task.env} | {info[0]['config'] if info else ''} | {info[1] if info else 'not selected'} |")
    TRACKING_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def finalize_git(results: list[dict[str, Any]], selected: dict[str, tuple[dict[str, Any], str]]) -> str:
    generate_tracking(results, selected)
    generate_report(results, selected, final_note="FINALIZING_GIT")
    for key, value in [("user.name", "single4090-results"), ("user.email", "single4090-results@local")]:
        code, out = run_text(["git", "config", "--get", key], timeout=60)
        if code != 0 or not out.strip():
            run_text(["git", "config", key, value], timeout=60)
    paths = [rel(TRACKING_PATH), rel(REPORT_PATH), rel(SCRIPT_PATH)]
    code, out = run_text(["git", "add", *paths], timeout=120)
    status(f"GIT_ADD returncode={code} output={out.strip().replace(chr(10), ' | ')}")
    if code != 0:
        return "GIT_ADD_FAILED"
    code, out = run_text(["git", "commit", "-m", "Update bad-task repair screening results", "--", *paths], timeout=120)
    status(f"GIT_COMMIT returncode={code} output={out.strip().replace(chr(10), ' | ')}")
    if code != 0 and "nothing to commit" not in out.lower():
        return "GIT_COMMIT_FAILED"
    code, out = run_text(["git", "push", "origin", f"HEAD:{RESULT_BRANCH}"], timeout=600)
    status(f"GIT_PUSH returncode={code} output={out.strip().replace(chr(10), ' | ')}")
    if code != 0:
        return "GIT_PUSH_FAILED_NO_FORCE_PUSH"
    return "GIT_PUSH_OK"


def main() -> int:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    status("RUNNER_START bad-task repair single4090")
    results: list[dict[str, Any]] = []
    selected: dict[str, tuple[dict[str, Any], str]] = {}
    if not preflight():
        generate_report(results, selected, final_note="PREFLIGHT_ABORT")
        status("RUNNER_ABORT preflight failed")
        return 2
    SAVE_ROOT.mkdir(parents=True, exist_ok=RESUME)
    generate_report(results, selected)

    for task in TASKS:
        for config, _ in CONFIGS:
            result = run_or_reuse("stageA_300k", task, config, SCREEN_SEED, SCREEN_STEPS)
            results.append(result)
            generate_report(results, selected)

    best = best_screen_results(results)
    for task in TASKS:
        row = best.get(task.env)
        if not row:
            continue
        ok, reason = qualifies_for_confirm(task, row)
        if ok:
            selected[task.env] = (row, reason)
    generate_report(results, selected)
    status("STAGE_B_SELECTED " + (",".join(f"{env}:{info[0]['config']}" for env, info in selected.items()) if selected else "none"))

    for task in TASKS:
        info = selected.get(task.env)
        if not info:
            continue
        config = info[0]["config"]
        result = run_or_reuse("stageB_seed2_1m", task, config, CONFIRM_SEED, CONFIRM_STEPS)
        results.append(result)
        generate_report(results, selected)
        extend, reason = qualifies_for_seed_extension(task, result)
        status(f"SEED_EXTENSION_DECISION env={task.env} config={config} extend={extend} reason={reason}")
        if extend:
            for seed in EXTENSION_SEEDS:
                ext_result = run_or_reuse("stageB_seedext_1m", task, config, seed, CONFIRM_STEPS)
                results.append(ext_result)
                generate_report(results, selected)

    final_note = finalize_git(results, selected)
    generate_report(results, selected, final_note=final_note)
    status(f"RUNNER_DONE report={rel(REPORT_PATH)} finalization={final_note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

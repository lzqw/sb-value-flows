#!/usr/bin/env python3
"""Selective hard-task state tuning runner for one RTX 4090.

The default mode is a dry run. It reads the registry, skips already repaired
or high-baseline tasks, and emits a concrete plan without launching main.py.
Actual training requires both --dry_run false and --confirm_start true.
"""

from __future__ import annotations

import argparse
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


REPO_ROOT = Path(__file__).resolve().parents[1]
EXP_NAME = "selective_state_tuning_single4090"
OUTPUT_BASE = Path("/root/autodl-tmp/sb-value-flows-runs") / EXP_NAME
SAVE_ROOT = OUTPUT_BASE / "exp"
LOG_ROOT = OUTPUT_BASE / "logs"
REPORT_ROOT = OUTPUT_BASE / "reports"
TMP_ROOT = OUTPUT_BASE / "tmp"
CACHE_ROOT = OUTPUT_BASE / "cache"
XLA_CACHE_ROOT = OUTPUT_BASE / "xla_cache"

REPO_REPORT = REPO_ROOT / "reports" / f"{EXP_NAME}_plan.md"
STATUS_REPORT = REPORT_ROOT / "selective_state_tuning_status.md"
STATUS_LOG = LOG_ROOT / "status.txt"

BASELINE_CSV = REPO_ROOT / "results" / "valueflow_task_baselines.csv"
RUNS_CSV = REPO_ROOT / "results" / "experiment_runs.csv"
CURVES_CSV = REPO_ROOT / "results" / "eval_curves_index.csv"
SCOREBOARD_CSV = REPO_ROOT / "results" / "task_scoreboard.csv"
SCOREBOARD_MD = REPO_ROOT / "results" / "task_scoreboard.md"
UPDATE_REGISTRY = REPO_ROOT / "scripts" / "update_results_registry.py"

CONDA_BIN = "/root/miniconda3/bin/conda"
PYTHON_BIN = "/root/miniconda3/envs/value-flows/bin/python"
MUJOCO_BIN = "/root/.mujoco/mujoco210/bin"
DATA_ROOT = Path("/root/.ogbench/data")
AGENT_FLAG = "--agent=agents/pm_value_flows.py"

SCREEN_STEPS = 300_000
CONFIRM_STEPS = 1_000_000
SCREEN_SEED = 2
CONFIRM_SEEDS = [0, 1, 2]

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
CONFIG_NAMES = [name for name, _ in CONFIGS]

TASK_FLAGS: dict[str, list[str]] = {
    "cube-double-play-singletask-task2-v0": ["--agent.discount=0.995", "--agent.confidence_weight_temp=3"],
    "cube-double-play-singletask-task3-v0": ["--agent.discount=0.995", "--agent.confidence_weight_temp=3"],
    "cube-double-play-singletask-task4-v0": ["--agent.discount=0.995", "--agent.confidence_weight_temp=3"],
    "cube-double-play-singletask-task5-v0": ["--agent.discount=0.995", "--agent.confidence_weight_temp=3"],
    "cube-triple-play-singletask-task2-v0": ["--agent.discount=0.995", "--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=0.03"],
    "cube-triple-play-singletask-task3-v0": ["--agent.discount=0.995", "--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=0.03"],
    "cube-triple-play-singletask-task4-v0": ["--agent.discount=0.995", "--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=0.03"],
    "cube-triple-play-singletask-task5-v0": ["--agent.discount=0.995", "--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=0.03"],
    "puzzle-3x3-play-singletask-task4-v0": ["--agent.bcfm_lambda=0.5", "--agent.ret_agg=min"],
    "puzzle-3x3-play-singletask-task5-v0": ["--agent.bcfm_lambda=0.5", "--agent.ret_agg=min"],
    "puzzle-4x4-play-singletask-task1-v0": ["--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=100", "--agent.q_agg=min"],
    "puzzle-4x4-play-singletask-task3-v0": ["--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=100", "--agent.q_agg=min"],
    "puzzle-4x4-play-singletask-task4-v0": ["--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=100", "--agent.q_agg=min"],
    "puzzle-4x4-play-singletask-task5-v0": ["--agent.bcfm_lambda=3", "--agent.confidence_weight_temp=100", "--agent.q_agg=min"],
    "scene-play-singletask-task4-v0": ["--agent.ret_agg=min"],
    "scene-play-singletask-task5-v0": ["--agent.ret_agg=min"],
}

PRIORITY_1_UNSTABLE = [
    "scene-play-singletask-task4-v0",
    "puzzle-4x4-play-singletask-task4-v0",
    "puzzle-4x4-play-singletask-task5-v0",
]

PRIORITY_2_LOW_BASELINE = [
    "cube-triple-play-singletask-task2-v0",
    "cube-triple-play-singletask-task3-v0",
    "cube-triple-play-singletask-task4-v0",
    "cube-triple-play-singletask-task5-v0",
    "puzzle-4x4-play-singletask-task1-v0",
    "puzzle-4x4-play-singletask-task3-v0",
]

PRIORITY_3_IF_CAPACITY = [
    "scene-play-singletask-task5-v0",
    "cube-double-play-singletask-task5-v0",
    "puzzle-3x3-play-singletask-task4-v0",
    "puzzle-3x3-play-singletask-task5-v0",
]

FIRST_BATCH_ORDER = [
    "cube-triple-play-singletask-task2-v0",
    "cube-triple-play-singletask-task3-v0",
    "cube-triple-play-singletask-task4-v0",
    "cube-triple-play-singletask-task5-v0",
]

EXPLICIT_SKIP = {
    "cube-double-play-singletask-task2-v0": "skip: already strong positive with R3 1M 3-seed mean about 0.83 > VF 0.76",
    "cube-double-play-singletask-task3-v0": "skip: already strong positive with A2 1M 3-seed mean about 0.83 > VF 0.73",
    "cube-double-play-singletask-task4-v0": "skip: already positive with A1 1M 3-seed mean about 0.40 > VF 0.30",
    "puzzle-4x4-play-singletask-task2-v0": "skip: weak positive MinimalSB_lam0p001 1M mean about 0.33 > VF 0.27; wait for a real stable mode",
}

EASY_SKIP = {
    "cube-double-play-singletask-task1-v0": "skip: high Value Flow baseline easy task, not a repair target",
    "scene-play-singletask-task1-v0": "skip: high Value Flow baseline easy task, not a repair target",
    "scene-play-singletask-task2-v0": "skip: high Value Flow baseline easy task, not a repair target",
    "scene-play-singletask-task3-v0": "skip: high Value Flow baseline easy task, not a repair target",
    "puzzle-3x3-play-singletask-task1-v0": "skip: high Value Flow baseline easy task, not a repair target",
    "puzzle-3x3-play-singletask-task2-v0": "skip: high Value Flow baseline easy task, not a repair target",
    "puzzle-3x3-play-singletask-task3-v0": "skip: high Value Flow baseline easy task, not a repair target",
}


@dataclass(frozen=True)
class PlannedRun:
    stage: str
    protocol: str
    env: str
    config: str
    seed: int
    target_steps: int
    reason: str
    command: list[str]


@dataclass
class TaskDecision:
    env: str
    priority: str
    baseline: float | None
    best_300k: str
    best_1m: str
    conclusion: str
    action: str
    reason: str
    pending_stage_a: list[PlannedRun]
    pending_stage_b: list[PlannedRun]
    stage_b_note: str = ""


def parse_bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        val = float(value)
    except Exception:
        return None
    return None if math.isnan(val) else val


def fmt(value: Any) -> str:
    val = to_float(value)
    if val is None:
        return ""
    return f"{val:.6g}"


def shell_join(parts: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in parts)


def run_text(cmd: list[str], timeout: int = 120) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=timeout)
        return proc.returncode, proc.stdout
    except Exception as exc:  # noqa: BLE001
        return 999, f"ERROR: {exc}"


def ensure_dirs() -> None:
    for path in [SAVE_ROOT, LOG_ROOT, REPORT_ROOT, TMP_ROOT, CACHE_ROOT, XLA_CACHE_ROOT, REPO_REPORT.parent]:
        path.mkdir(parents=True, exist_ok=True)


def write_status(message: str) -> None:
    ensure_dirs()
    with STATUS_LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{now()}] {message}\n")


def git_value(args: list[str]) -> str:
    code, out = run_text(["git", *args], timeout=60)
    return out.strip() if code == 0 else ""


def slug_env(env: str) -> str:
    return env.replace("-play-singletask-", "-").replace("-v0", "").replace("-", "_")


def group_name(stage: str, env: str, config: str, seed: int) -> str:
    return f"{stage}_{slug_env(env)}_{config}_seed{seed}"


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
            "XDG_CACHE_HOME": str(CACHE_ROOT),
            "HOME": "/root",
            "PATH": "/root/miniconda3/bin:" + env.get("PATH", ""),
        }
    )
    return env


def assert_agent_order(flags: list[str]) -> None:
    agent_idx = flags.index(AGENT_FLAG)
    bad = [(idx, flag) for idx, flag in enumerate(flags) if flag.startswith("--agent.") and idx < agent_idx]
    if bad:
        raise RuntimeError(f"{AGENT_FLAG} must appear before all --agent.* flags; bad={bad}")


def build_flags(stage: str, env: str, config: str, seed: int, steps: int) -> list[str]:
    if config not in CONFIG_FLAGS:
        raise KeyError(f"unknown config: {config}")
    flags = [
        f"--env_name={env}",
        f"--seed={seed}",
        f"--save_dir={SAVE_ROOT}",
        f"--wandb_run_group={group_name(stage, env, config, seed)}",
        "--enable_wandb=0",
        f"--offline_steps={steps}",
        "--online_steps=0",
        "--eval_interval=50000",
        "--eval_episodes=10",
        "--log_interval=25000",
        "--save_interval=999999999",
        AGENT_FLAG,
        *TASK_FLAGS.get(env, []),
        *COMMON_AGENT_FLAGS,
        *CONFIG_FLAGS[config],
    ]
    assert_agent_order(flags)
    return flags


def build_command(stage: str, env: str, config: str, seed: int, steps: int) -> list[str]:
    return [CONDA_BIN, "run", "-n", "value-flows", "python", "main.py", *build_flags(stage, env, config, seed, steps)]


def command_for_report(run: PlannedRun) -> str:
    prefix = [
        "CUDA_VISIBLE_DEVICES=0",
        "MUJOCO_GL=egl",
        "PYOPENGL_PLATFORM=egl",
        "SDL_VIDEODRIVER=dummy",
        f"OGBENCH_DATA_DIR={DATA_ROOT}",
        f"XDG_CACHE_HOME={CACHE_ROOT}",
        "XLA_PYTHON_CLIENT_PREALLOCATE=true",
        "XLA_PYTHON_CLIENT_MEM_FRACTION=0.90",
    ]
    return " ".join(prefix) + " " + shell_join(run.command)


def priority_for(env: str) -> str:
    if env in PRIORITY_1_UNSTABLE:
        return "P1 unstable"
    if env in PRIORITY_2_LOW_BASELINE:
        return "P2 low-baseline or uncovered"
    if env in PRIORITY_3_IF_CAPACITY:
        return "P3 if capacity"
    return "out of scope"


def ordered_candidates() -> list[str]:
    return [*PRIORITY_1_UNSTABLE, *PRIORITY_2_LOW_BASELINE, *PRIORITY_3_IF_CAPACITY]


def command_sort_key(run: PlannedRun) -> tuple[int, int, int, int, str]:
    if run.env in FIRST_BATCH_ORDER:
        batch = 0
        env_order = FIRST_BATCH_ORDER.index(run.env)
    elif run.env in PRIORITY_2_LOW_BASELINE:
        batch = 1
        env_order = PRIORITY_2_LOW_BASELINE.index(run.env)
    elif run.env in PRIORITY_1_UNSTABLE:
        batch = 2
        env_order = PRIORITY_1_UNSTABLE.index(run.env)
    elif run.env in PRIORITY_3_IF_CAPACITY:
        batch = 3
        env_order = PRIORITY_3_IF_CAPACITY.index(run.env)
    else:
        batch = 9
        env_order = 0
    stage_order = 0 if run.stage == "stageA_300k" else 1
    config_order = CONFIG_NAMES.index(run.config) if run.config in CONFIG_NAMES else 99
    return (stage_order, batch, env_order, config_order, run.config)


def registry_completed(runs: list[dict[str, str]], env: str, config: str, seed: int, target_steps: int) -> bool:
    for row in runs:
        if row.get("env") != env or row.get("config_name") != config:
            continue
        if row.get("seed") != str(seed) or row.get("target_steps") != str(target_steps):
            continue
        if row.get("status") == "COMPLETED":
            final_step = to_float(row.get("final_step"))
            if final_step is not None and final_step >= target_steps * 0.98:
                return True
    return False


def completed_stage_a_rows(runs: list[dict[str, str]], env: str) -> list[dict[str, str]]:
    rows = []
    for row in runs:
        if row.get("env") != env or row.get("status") != "COMPLETED":
            continue
        if row.get("seed") != str(SCREEN_SEED):
            continue
        if row.get("target_steps") == str(SCREEN_STEPS) or row.get("protocol") == "300k_screening":
            rows.append(row)
    return rows


def best_stage_a_configs(runs: list[dict[str, str]], env: str) -> list[dict[str, str]]:
    by_config: dict[str, dict[str, str]] = {}
    for row in completed_stage_a_rows(runs, env):
        config = row.get("config_name", "")
        if not config:
            continue
        cur_success = to_float(row.get("success_final"))
        old_success = to_float(by_config.get(config, {}).get("success_final"))
        if config not in by_config or (cur_success if cur_success is not None else -1) > (old_success if old_success is not None else -1):
            by_config[config] = row
    rows = list(by_config.values())
    rows.sort(key=lambda r: (to_float(r.get("success_final")) if to_float(r.get("success_final")) is not None else -1), reverse=True)
    if not rows:
        return []
    selected = [rows[0]]
    if len(rows) > 1:
        top1 = to_float(rows[0].get("success_final")) or 0.0
        top2 = to_float(rows[1].get("success_final")) or 0.0
        if abs(top1 - top2) <= 0.1:
            selected.append(rows[1])
    return selected


def all_screening_complete(runs: list[dict[str, str]], env: str) -> bool:
    return all(registry_completed(runs, env, config, SCREEN_SEED, SCREEN_STEPS) for config in CONFIG_NAMES)


def detect_stable_mode() -> tuple[bool, str]:
    candidates = [
        REPO_ROOT / "agents" / "pm_value_flows.py",
        REPO_ROOT / "main.py",
        REPO_ROOT / "utilis" / "default_config.py",
        REPO_ROOT / "utilis" / "config.py",
    ]
    patterns = ["pm_sb_stable", "pm_stable", "stable_mode", "sb_stable"]
    hits: list[str] = []
    for path in candidates:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in patterns:
            if pattern in text:
                hits.append(f"{path.relative_to(REPO_ROOT)}:{pattern}")
    if hits:
        return True, "stable mode detected: " + ", ".join(hits)
    return False, "stable mode unavailable: no pm_sb_stable/pm_stable/stable_mode/sb_stable flag found"


def build_plan() -> tuple[list[TaskDecision], list[dict[str, str]], dict[str, Any]]:
    baselines = [r for r in read_csv(BASELINE_CSV) if r.get("modality") == "state"]
    runs = read_csv(RUNS_CSV)
    scoreboard = {r.get("env", ""): r for r in read_csv(SCOREBOARD_CSV) if r.get("modality") == "state"}
    baseline_by_env = {r["env"]: r for r in baselines if r.get("env")}
    stable_available, stable_note = detect_stable_mode()

    candidate_set = set(ordered_candidates())
    decisions: list[TaskDecision] = []
    skipped: list[dict[str, str]] = []

    for env in sorted(baseline_by_env):
        baseline = to_float(baseline_by_env[env].get("valueflow_success_mean"))
        sb = scoreboard.get(env, {})
        best_1m = to_float(sb.get("best_1m_success_mean"))
        reason = ""
        if env in EXPLICIT_SKIP:
            reason = EXPLICIT_SKIP[env]
        elif env in EASY_SKIP:
            reason = EASY_SKIP[env]
        elif best_1m is not None and baseline is not None and best_1m >= baseline:
            reason = f"skip: completed 1M mean {best_1m:.3g} >= VF baseline {baseline:.3g}"
        elif env not in candidate_set:
            reason = "skip: not in current selective hard-task queue"
        if reason:
            skipped.append(
                {
                    "env": env,
                    "baseline": fmt(baseline),
                    "best_300k": sb.get("best_300k_success", ""),
                    "best_1m": sb.get("best_1m_success_mean", ""),
                    "reason": reason,
                }
            )
            continue

        pending_stage_a: list[PlannedRun] = []
        for config in CONFIG_NAMES:
            if registry_completed(runs, env, config, SCREEN_SEED, SCREEN_STEPS):
                continue
            pending_stage_a.append(
                PlannedRun(
                    stage="stageA_300k",
                    protocol="300k_screening",
                    env=env,
                    config=config,
                    seed=SCREEN_SEED,
                    target_steps=SCREEN_STEPS,
                    reason="missing completed Stage A 300k final row",
                    command=build_command("stageA_300k", env, config, SCREEN_SEED, SCREEN_STEPS),
                )
            )

        pending_stage_b: list[PlannedRun] = []
        stage_b_note = ""
        if env in PRIORITY_1_UNSTABLE and not stable_available:
            stage_b_note = "held: unstable task and stable variant unavailable; do 300k curves first"
        elif not all_screening_complete(runs, env):
            stage_b_note = "waiting: complete Stage A screening pool first"
        else:
            selected = best_stage_a_configs(runs, env)
            if not selected:
                stage_b_note = "waiting: no completed Stage A config"
            else:
                for row in selected:
                    config = row.get("config_name", "")
                    for seed in CONFIRM_SEEDS:
                        if registry_completed(runs, env, config, seed, CONFIRM_STEPS):
                            continue
                        pending_stage_b.append(
                            PlannedRun(
                                stage="stageB_selective_1m",
                                protocol="1m_confirmation",
                                env=env,
                                config=config,
                                seed=seed,
                                target_steps=CONFIRM_STEPS,
                                reason="selected top Stage A config for 1M confirmation",
                                command=build_command("stageB_selective_1m", env, config, seed, CONFIRM_STEPS),
                            )
                        )
                if not pending_stage_b:
                    stage_b_note = "no pending 1M seeds for selected top configs"

        action = "pending"
        if not pending_stage_a and not pending_stage_b:
            action = "watch"
        if stage_b_note.startswith("held"):
            action = "screen_only"

        decisions.append(
            TaskDecision(
                env=env,
                priority=priority_for(env),
                baseline=baseline,
                best_300k=sb.get("best_300k_success", ""),
                best_1m=sb.get("best_1m_success_mean", ""),
                conclusion=sb.get("conclusion", ""),
                action=action,
                reason="candidate hard task",
                pending_stage_a=sorted(pending_stage_a, key=command_sort_key),
                pending_stage_b=sorted(pending_stage_b, key=command_sort_key),
                stage_b_note=stage_b_note,
            )
        )

    decisions.sort(key=lambda d: (0 if d.env in PRIORITY_2_LOW_BASELINE else 1 if d.env in PRIORITY_1_UNSTABLE else 2, ordered_candidates().index(d.env)))
    meta = {
        "stable_available": stable_available,
        "stable_note": stable_note,
        "registry_runs": len(runs),
        "state_baselines": len(baselines),
        "scoreboard_state_tasks": len(scoreboard),
    }
    return decisions, skipped, meta


def all_pending(decisions: list[TaskDecision]) -> list[PlannedRun]:
    runs: list[PlannedRun] = []
    for decision in decisions:
        runs.extend(decision.pending_stage_a)
        runs.extend(decision.pending_stage_b)
    return sorted(runs, key=command_sort_key)


def generate_report(decisions: list[TaskDecision], skipped: list[dict[str, str]], meta: dict[str, Any], dry_run: bool) -> str:
    branch = git_value(["branch", "--show-current"])
    head = git_value(["rev-parse", "HEAD"])
    status_short = git_value(["status", "--short"])
    pending = all_pending(decisions)
    pending_stage_a = [r for r in pending if r.stage == "stageA_300k"]
    pending_stage_b = [r for r in pending if r.stage != "stageA_300k"]
    unstable = [d for d in decisions if d.env in PRIORITY_1_UNSTABLE]
    next_runs = pending[:10]

    lines = [
        "# Selective State Tuning Single4090 Plan",
        "",
        f"Generated: {now()}",
        f"Dry run: {dry_run}",
        "",
        "## Guardrails",
        "",
        "- This is task-wise hard-task tuning, not full 25-task brute-force tuning and not formal ablation.",
        "- Completed means eval.csv final row with final_step >= target_steps * 0.98.",
        "- Partial runs do not count as completed, and peak/best success is not used as final success.",
        "- Actual training requires --dry_run false --confirm_start true.",
        "",
        "## Setup",
        "",
        f"- branch: {branch}",
        f"- HEAD: {head}",
        f"- output base: {OUTPUT_BASE}",
        f"- exp dir: {SAVE_ROOT}",
        f"- repo report: {REPO_REPORT}",
        f"- status report: {STATUS_REPORT}",
        f"- registry runs: {meta['registry_runs']}",
        f"- state baselines: {meta['state_baselines']}",
        f"- state scoreboard tasks: {meta['scoreboard_state_tasks']}",
        f"- stable mode: {meta['stable_note']}",
        "- config pool: " + ", ".join(CONFIG_NAMES),
        "- note: the existing bad-task repair pool contains MinimalSB_lam0p0003; no separate MinimalSB_lam0p003 config was found.",
        "",
        "## Registry Files",
        "",
        f"- {RUNS_CSV}",
        f"- {CURVES_CSV}",
        f"- {SCOREBOARD_CSV}",
        f"- {SCOREBOARD_MD}",
        f"- {BASELINE_CSV}",
        "",
        "## Candidate Tasks",
        "",
        "| priority | env | VF baseline | best 300k | best 1M mean | conclusion | action | Stage A pending | Stage B pending | Stage B note |",
        "|---|---|---:|---:|---:|---|---|---:|---:|---|",
    ]
    for d in decisions:
        lines.append(
            f"| {d.priority} | {d.env} | {fmt(d.baseline)} | {d.best_300k} | {d.best_1m} | {d.conclusion} | "
            f"{d.action} | {len(d.pending_stage_a)} | {len(d.pending_stage_b)} | {d.stage_b_note} |"
        )

    lines += [
        "",
        "## Skipped Tasks",
        "",
        "| env | VF baseline | best 300k | best 1M mean | reason |",
        "|---|---:|---:|---:|---|",
    ]
    for row in skipped:
        lines.append(f"| {row['env']} | {row['baseline']} | {row['best_300k']} | {row['best_1m']} | {row['reason']} |")

    lines += [
        "",
        "## Unstable Queue",
        "",
        "| env | best 300k | best 1M mean | plan |",
        "|---|---:|---:|---|",
    ]
    for d in unstable:
        plan = d.stage_b_note or "stable mode available; select top configs after Stage A"
        lines.append(f"| {d.env} | {d.best_300k} | {d.best_1m} | {plan} |")

    lines += [
        "",
        "## Pending Stage A Runs",
        "",
        "| env | config | seed | target_steps | reason |",
        "|---|---|---:|---:|---|",
    ]
    for run in pending_stage_a:
        lines.append(f"| {run.env} | {run.config} | {run.seed} | {run.target_steps} | {run.reason} |")
    if not pending_stage_a:
        lines.append("|  |  |  |  | none |")

    lines += [
        "",
        "## Pending Stage B Runs",
        "",
        "| env | config | seed | target_steps | reason |",
        "|---|---|---:|---:|---|",
    ]
    for run in pending_stage_b:
        lines.append(f"| {run.env} | {run.config} | {run.seed} | {run.target_steps} | {run.reason} |")
    if not pending_stage_b:
        lines.append("|  |  |  |  | none currently; waiting for Stage A or stable mode |")

    lines += [
        "",
        "## Next 10 Commands",
        "",
    ]
    if not next_runs:
        lines.append("No pending commands.")
    else:
        for idx, run in enumerate(next_runs, 1):
            lines += [
                f"### {idx}. {run.stage} {run.env} {run.config} seed{run.seed}",
                "",
                "```bash",
                command_for_report(run),
                "```",
                "",
            ]

    lines += [
        "## Counts",
        "",
        f"- candidate tasks: {len(decisions)}",
        f"- skipped tasks: {len(skipped)}",
        f"- pending Stage A runs: {len(pending_stage_a)}",
        f"- pending Stage B runs: {len(pending_stage_b)}",
        f"- total pending runs: {len(pending)}",
        "",
        "## Suggested Launch Order",
        "",
        "1. First batch: cube-triple task2, task3, task4, task5.",
        "2. Second batch: puzzle-4x4 task1/task3 plus unstable 300k curve collection.",
        "3. Capacity batch: scene task5, cube-double task5, puzzle-3x3 task4/task5.",
        "",
        "## Git Status At Planning Time",
        "",
        "```text",
        status_short,
        "```",
    ]
    return "\n".join(lines) + "\n"


def write_reports(text: str) -> None:
    ensure_dirs()
    REPO_REPORT.write_text(text, encoding="utf-8")
    STATUS_REPORT.write_text(text, encoding="utf-8")


def no_training_running() -> tuple[bool, str]:
    code, out = run_text(["ps", "-eo", "pid,ppid,etime,stat,cmd"], timeout=60)
    if code != 0:
        return False, out
    busy = []
    own = os.getpid()
    parent = os.getppid()
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
        if "main.py" in cmd or ("run_" in cmd and "single4090" in cmd and ".py" in cmd):
            if "tensorboard" not in cmd.lower():
                busy.append(line)
    return not busy, "\n".join(busy)


def gpu_idle() -> tuple[bool, str]:
    code, out = run_text(["nvidia-smi", "--query-gpu=memory.used,utilization.gpu", "--format=csv,noheader,nounits"], timeout=60)
    if code != 0:
        return False, out
    first = out.strip().splitlines()[0].split(",")
    mem = int(first[0].strip())
    util = int(first[1].strip())
    return mem < 1000 and util < 10, f"memory.used={mem}MiB util={util}%"


def newest_run_dir(stage: str, env: str, config: str, seed: int, start_time: float) -> Path | None:
    root = SAVE_ROOT / group_name(stage, env, config, seed)
    if not root.exists():
        return None
    candidates = [p for p in root.iterdir() if p.is_dir() and p.name.startswith(f"sd{seed:03d}_") and p.stat().st_mtime >= start_time - 2]
    if not candidates:
        candidates = [p for p in root.iterdir() if p.is_dir() and p.name.startswith(f"sd{seed:03d}_")]
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None


def write_command_txt(run_dir: Path | None, command: list[str]) -> None:
    if run_dir is None:
        return
    (run_dir / "command.txt").write_text(shell_join(command) + "\n", encoding="utf-8")


def update_registry() -> None:
    commands = [
        [
            PYTHON_BIN,
            str(UPDATE_REGISTRY),
            "--scan_base",
            str(SAVE_ROOT),
            "--server",
            "single4090",
            "--machine_tag",
            "single4090-selective",
            "--modality",
            "state",
            "--stage",
            "selective_state_tuning",
            "--output_dir",
            "results",
            "--commit",
            "false",
        ],
        [
            PYTHON_BIN,
            str(UPDATE_REGISTRY),
            "--scan_base",
            "exp/bad_task_repair_single4090",
            "--server",
            "single4090",
            "--machine_tag",
            "seeta-codex",
            "--modality",
            "state",
            "--stage",
            "auto",
            "--output_dir",
            "results",
            "--commit",
            "false",
        ],
    ]
    for cmd in commands:
        code, out = run_text(cmd, timeout=600)
        write_status(f"REGISTRY_UPDATE returncode={code} cmd={shell_join(cmd)} output={out.strip().replace(chr(10), ' | ')}")


def run_planned(run: PlannedRun) -> int:
    log_path = LOG_ROOT / f"{group_name(run.stage, run.env, run.config, run.seed)}.log"
    write_status(f"START {run.stage} env={run.env} config={run.config} seed={run.seed} steps={run.target_steps}")
    start = time.time()
    with log_path.open("w", encoding="utf-8", errors="replace") as f:
        f.write("COMMAND: " + shell_join(run.command) + "\n")
        f.write("COMMAND_ORDER_RULE: --agent=agents/pm_value_flows.py appears before all --agent.* flags\n")
        f.flush()
        proc = subprocess.run(run.command, cwd=REPO_ROOT, stdout=f, stderr=subprocess.STDOUT, env=make_env())
    run_dir = newest_run_dir(run.stage, run.env, run.config, run.seed, start)
    write_command_txt(run_dir, run.command)
    update_registry()
    write_status(
        f"DONE returncode={proc.returncode} duration_sec={time.time() - start:.1f} "
        f"run_dir={run_dir if run_dir else ''} log={log_path}"
    )
    return proc.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry_run", default="true")
    parser.add_argument("--confirm_start", default="false")
    parser.add_argument("--max_runs", type=int, default=0, help="Maximum runs to launch when dry_run=false. 0 means all pending runs.")
    parser.add_argument("--only_envs", default="", help="Comma-separated env allowlist for actual launches.")
    parser.add_argument("--first_batch_only", default="false", help="Limit actual launches to cube-triple task2-task5.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dry_run = parse_bool(args.dry_run)
    confirm_start = parse_bool(args.confirm_start)
    first_batch_only = parse_bool(args.first_batch_only)
    ensure_dirs()
    decisions, skipped, meta = build_plan()
    report = generate_report(decisions, skipped, meta, dry_run=dry_run)
    write_reports(report)

    pending = all_pending(decisions)
    print(f"candidate_tasks={len(decisions)}")
    print(f"skipped_tasks={len(skipped)}")
    print(f"pending_stageA={sum(1 for r in pending if r.stage == 'stageA_300k')}")
    print(f"pending_stageB={sum(1 for r in pending if r.stage != 'stageA_300k')}")
    print(f"total_pending_runs={len(pending)}")
    print(f"output_base={OUTPUT_BASE}")
    print(f"repo_report={REPO_REPORT}")
    print(f"status_report={STATUS_REPORT}")
    print(meta["stable_note"])
    print("next_10:")
    for run in pending[:10]:
        print(f"- {run.stage} {run.env} {run.config} seed={run.seed} steps={run.target_steps}")

    if dry_run:
        write_status("DRY_RUN complete; no training launched")
        return 0
    if not confirm_start:
        write_status("ABORT actual launch requested without --confirm_start true")
        print("ABORT: actual training requires --confirm_start true")
        return 2
    jobs_ok, jobs_msg = no_training_running()
    if not jobs_ok:
        print("ABORT: another training process appears active")
        print(jobs_msg)
        return 3
    gpu_ok, gpu_msg = gpu_idle()
    if not gpu_ok:
        print("ABORT: GPU is not idle")
        print(gpu_msg)
        return 4

    allow_envs = {x.strip() for x in args.only_envs.split(",") if x.strip()}
    launch = pending
    if allow_envs:
        launch = [r for r in launch if r.env in allow_envs]
    if first_batch_only:
        launch = [r for r in launch if r.env in FIRST_BATCH_ORDER]
    if args.max_runs > 0:
        launch = launch[: args.max_runs]
    if not launch:
        print("No runs selected for launch.")
        return 0

    write_status(f"LAUNCH_START count={len(launch)}")
    for run in launch:
        rc = run_planned(run)
        if rc != 0:
            write_status(f"STOP_AFTER_FAILURE env={run.env} config={run.config} seed={run.seed} returncode={rc}")
            return rc
    write_status("LAUNCH_DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

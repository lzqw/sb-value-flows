#!/usr/bin/env python3
"""Dry-run plan for visual_stable_v8 on 4090D.

This script intentionally does not launch training by default. It writes a
human-readable plan, exact commands, and status files for a small diagnostic
visual-stability experiment designed to test whether late-training collapse can
be reduced relative to visual_matched_4090d_v7.
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path

RUN_BASE = Path("/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d")
EXP_DIR = RUN_BASE / "exp"
LOG_DIR = RUN_BASE / "logs"
REPORT_DIR = RUN_BASE / "reports"
CHECKPOINT_DIR = RUN_BASE / "checkpoints"
STATUS_PATH = REPORT_DIR / "visual_stable_v8_status.md"
REPO_PLAN_PATH = Path("/root/sb-value-flows/reports/visual_stable_v8_plan.md")

TASKS = [
    {
        "env": "visual-antmaze-medium-navigate-singletask-task1-v0",
        "reason": "v7 best 0.78 -> final 0.20, drop -0.58",
    },
    {
        "env": "visual-antmaze-medium-navigate-singletask-task2-v0",
        "reason": "v7 best 0.82 -> final 0.02, drop -0.80",
    },
    {
        "env": "visual-antmaze-medium-navigate-singletask-task4-v0",
        "reason": "v7 best 0.86 -> final 0.40, drop -0.46",
    },
]

COMMON_FLAGS = [
    "--agent=agents/pm_value_flows.py",
    "--agent.encoder=impala_small",
    "--agent.batch_size=256",
    "--agent.num_samples=16",
    "--agent.num_flow_steps=10",
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
]

STABLE_FLAGS = [
    "--agent.visual_stable_mode=true",
    "--agent.save_eval_checkpoints=true",
    "--agent.visual_freeze_encoder_after_step=300000",
    "--agent.visual_actor_lr_decay_after_step=300000",
    "--agent.visual_actor_lr_decay_mult=0.3",
    "--agent.visual_critic_lr_decay_after_step=300000",
    "--agent.visual_critic_lr_decay_mult=0.5",
    "--agent.visual_second_lr_decay_after_step=500000",
    "--agent.visual_second_actor_lr_decay_mult=0.3",
    "--agent.visual_second_critic_lr_decay_mult=0.5",
    "--agent.actor_ema_anchor_start_step=300000",
    "--agent.actor_ema_anchor_coef=0.01",
    "--agent.actor_ema_tau=0.995",
    "--agent.pm_sb_weight_uniform_mix=0.05",
    "--agent.pm_sb_weight_logit_clip=5.0",
    "--agent.pm_sb_weight_max=0.7",
]

BASE_FLAGS = [
    "--seed=2",
    "--offline_steps=1000000",
    "--online_steps=0",
    "--eval_interval=100000",
    "--eval_episodes=50",
    "--log_interval=25000",
    "--save_interval=999999999",
    "--enable_wandb=0",
]


def run_name(env: str) -> str:
    return f"visual_stable_v8_R2_stable_{env}_seed2_1m"


def command_for(env: str) -> list[str]:
    name = run_name(env)
    run_dir = EXP_DIR / name
    ckpt_dir = CHECKPOINT_DIR / name
    return [
        "python",
        "main.py",
        f"--env_name={env}",
        f"--save_dir={run_dir}",
        f"--wandb_run_group={name}",
        *BASE_FLAGS,
        *COMMON_FLAGS,
        f"--agent.checkpoint_dir={ckpt_dir}",
        *R2_FLAGS,
        *STABLE_FLAGS,
    ]


def shell_command(cmd: list[str], gpu: int) -> str:
    env = {
        "CUDA_VISIBLE_DEVICES": str(gpu),
        "OGBENCH_DATA_DIR": "/root/autodl-tmp/ogbench/data",
        "TMPDIR": str(RUN_BASE / "tmp"),
        "XDG_CACHE_HOME": str(RUN_BASE / "cache"),
        "XLA_CACHE_DIR": str(RUN_BASE / "xla_cache"),
        "WANDB_DIR": str(RUN_BASE / "wandb"),
        "MUJOCO_GL": "egl",
        "PYOPENGL_PLATFORM": "egl",
        "SDL_VIDEODRIVER": "dummy",
        "XLA_PYTHON_CLIENT_PREALLOCATE": "true",
        "XLA_PYTHON_CLIENT_MEM_FRACTION": "0.90",
    }
    prefix = " ".join(f"{k}={v}" for k, v in env.items())
    return prefix + " " + " ".join(cmd)


def render_report() -> str:
    now = datetime.now().isoformat(timespec="seconds")
    lines = [
        "# Visual Stable v8 Dry-Run Plan",
        "",
        f"Generated: {now}",
        "",
        "## Scope",
        "",
        "This is a dry-run plan only. It does not launch `main.py` or start training.",
        "The goal is to test whether visual-specific stability mechanisms reduce `best-in-run success - final success` collapse seen in visual v7.",
        "",
        "## Baseline Diagnosis From v7",
        "",
        "- visual-antmaze-medium R2 completed 5-task final mean: 0.212",
        "- visual-antmaze-medium R2 best-in-run mean: 0.792",
        "- conclusion: strong early learning, severe late-training collapse; diagnostic only, not a final-performance positive.",
        "",
        "## Planned Diagnostic Runs",
        "",
        "| env | config | seed | steps | reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for task in TASKS:
        lines.append(f"| {task['env']} | R2_stable | 2 | 1M | {task['reason']} |")
    lines += [
        "",
        "## R2_stable Changes vs v7 R2",
        "",
        "- Save checkpoints at every eval interval, plus best-eval and final checkpoints. Best checkpoint is diagnostic only; final result remains final eval.csv last row.",
        "- Actor learning rate decay after 300k: x0.3; second decay after 500k: x0.3.",
        "- Critic learning rate decay after 300k: x0.5; second decay after 500k: x0.5.",
        "- Encoder freeze or encoder LR x0.1 after 300k, depending on implementation support.",
        "- Actor EMA anchor from 300k with coef 0.01 and tau 0.995.",
        "- SB/reliability weight stabilization: uniform mix 0.05, logit clip 5.0, max cap 0.7 with renormalization.",
        "- Eval remains paper-like: eval_interval 100k, eval_episodes 50, batch_size 256, num_samples 16, num_flow_steps 10.",
        "",
        "## Late-Collapse Metrics",
        "",
        "Each run report must include: success_final, success_best, best_step, peak_after_500k, drop_from_best = final - best, and the full eval trajectory.",
        "The target improvement is reduced negative drop, not merely a higher early peak.",
        "",
        "## Code Modification Requirement",
        "",
        "Actual training requires agent support for the visual_stable flags listed below. If the current worktree does not implement a flag, training must stop before launch and report the unsupported flag. This dry-run intentionally does not validate runtime flag support by launching training.",
        "",
        "## Output Directories",
        "",
        f"- RUN_BASE: `{RUN_BASE}`",
        f"- EXP_DIR: `{EXP_DIR}`",
        f"- LOG_DIR: `{LOG_DIR}`",
        f"- REPORT_DIR: `{REPORT_DIR}`",
        f"- CHECKPOINT_DIR: `{CHECKPOINT_DIR}`",
        "",
        "## Exact Commands",
        "",
    ]
    for i, task in enumerate(TASKS):
        gpu = i % 2
        lines.append(f"### {task['env']} on GPU{gpu}")
        lines.append("")
        lines.append("```bash")
        lines.append(shell_command(command_for(task["env"]), gpu))
        lines.append("```")
        lines.append("")
    lines += [
        "## Confirmation Gate",
        "",
        "Do not start these runs until explicitly confirmed by the user. The dry-run script refuses to train unless invoked with `--confirm_train true`, which is intentionally not used in this plan.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry_run", default="true")
    parser.add_argument("--confirm_train", default="false")
    args = parser.parse_args()

    for path in [EXP_DIR, LOG_DIR, REPORT_DIR, CHECKPOINT_DIR, RUN_BASE / "tmp", RUN_BASE / "cache", RUN_BASE / "xla_cache", RUN_BASE / "wandb"]:
        path.mkdir(parents=True, exist_ok=True)

    report = render_report()
    REPO_PLAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPO_PLAN_PATH.write_text(report)
    STATUS_PATH.write_text(report)

    print("visual_stable_v8 dry-run")
    print(f"dry_run={args.dry_run}")
    print(f"confirm_train={args.confirm_train}")
    print(f"planned_runs={len(TASKS)}")
    print(f"repo_plan={REPO_PLAN_PATH}")
    print(f"status_report={STATUS_PATH}")
    print(f"run_base={RUN_BASE}")
    print("commands:")
    for i, task in enumerate(TASKS):
        print(f"[{i}] gpu={i % 2} env={task['env']} reason={task['reason']}")
        print(shell_command(command_for(task["env"]), i % 2))

    if args.confirm_train.lower() == "true":
        raise SystemExit("Refusing to train from dry-run planner. Use a separate reviewed launcher after explicit approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

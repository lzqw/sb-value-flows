#!/usr/bin/env python3
from __future__ import annotations

import os
import shlex
import subprocess
from datetime import datetime
from pathlib import Path

REPO = Path('/root/sb-value-flows')
RUN_BASE = Path('/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8p1_repair_4090d')
EXP_DIR = RUN_BASE / 'exp'
LOG_DIR = RUN_BASE / 'logs'
TMP_DIR = RUN_BASE / 'tmp'
CACHE_DIR = RUN_BASE / 'cache'
XLA_CACHE_DIR = RUN_BASE / 'xla_cache'
WANDB_DIR = RUN_BASE / 'wandb'
PYTHON = '/root/miniconda3/bin/conda'

COMMON_FLAGS = [
    '--agent=agents/pm_value_flows.py',
    '--agent.encoder=impala_small',
    '--agent.batch_size=256',
    '--agent.num_samples=16',
    '--agent.num_flow_steps=10',
    '--agent.pm_minimal_sb=true',
    '--agent.pm_weight_type=field_kernel_norm',
    '--agent.pm_num_continuations=4',
    '--agent.pm_field_kernel_norm_temp=0.3',
    '--agent.pm_field_kernel_min_scale=1e-6',
    '--agent.pm_actor_energy_coef=0.0',
    '--agent.pm_actor_disagree_coef=0.0',
    '--agent.pm_log_sb_diagnostics=true',
    '--agent.pm_sb_reliability_score=flow_residual_disagree',
    '--agent.pm_sb_lambda=0.001',
    '--agent.pm_sb_reliability_normalize=std',
    '--agent.pm_sb_flow_residual_eps=0.05',
    '--agent.pm_sb_disagree_beta=0.5',
    '--agent.pm_sb_disagree_umax=3.0',
    '--agent.pm_sb_value_preserving=false',
    '--agent.visual_stable_mode=true',
    '--agent.save_eval_checkpoints=true',
    '--agent.visual_freeze_encoder_after_step=300000',
]

STRONG_FLAGS = [
    '--agent.visual_actor_lr_decay_after_step=300000',
    '--agent.visual_actor_lr_decay_mult=0.09',
    '--agent.visual_critic_lr_decay_after_step=300000',
    '--agent.visual_critic_lr_decay_mult=0.25',
    '--agent.visual_second_lr_decay_after_step=600000',
    '--agent.visual_second_actor_lr_decay_mult=0.3333333333',
    '--agent.visual_second_critic_lr_decay_mult=0.4',
    '--agent.actor_ema_anchor_start_step=300000',
    '--agent.actor_ema_anchor_coef=0.02',
    '--agent.actor_ema_tau=0.995',
    '--agent.pm_sb_weight_uniform_mix=0.10',
    '--agent.pm_sb_weight_logit_clip=3.0',
    '--agent.pm_sb_weight_max=0.5',
]

RETENTION_REPAIR_FLAGS = [
    '--agent.visual_actor_lr_decay_after_step=300000',
    '--agent.visual_actor_lr_decay_mult=0.06',
    '--agent.visual_critic_lr_decay_after_step=300000',
    '--agent.visual_critic_lr_decay_mult=0.20',
    '--agent.visual_second_lr_decay_after_step=600000',
    '--agent.visual_second_actor_lr_decay_mult=0.25',
    '--agent.visual_second_critic_lr_decay_mult=0.30',
    '--agent.actor_ema_anchor_start_step=300000',
    '--agent.actor_ema_anchor_coef=0.03',
    '--agent.actor_ema_tau=0.995',
    '--agent.pm_sb_weight_uniform_mix=0.15',
    '--agent.pm_sb_weight_logit_clip=2.5',
    '--agent.pm_sb_weight_max=0.45',
]

JOBS = [
    {
        'name': 'visual_stable_v8p1_task2_R2stableStrong_seed3_confirm',
        'env': 'visual-antmaze-medium-navigate-singletask-task2-v0',
        'seed': 3,
        'gpu': 0,
        'flags': STRONG_FLAGS,
        'reason': 'seed3 confirmation for task2 collapse observed in seed2',
    },
    {
        'name': 'visual_stable_v8p1_task4_R2retentionRepair_seed2',
        'env': 'visual-antmaze-medium-navigate-singletask-task4-v0',
        'seed': 2,
        'gpu': 1,
        'flags': RETENTION_REPAIR_FLAGS,
        'reason': 'retention repair for task4 final below v7 and large peak-to-final drop',
    },
]


def mkdirs() -> None:
    for p in [EXP_DIR, LOG_DIR, TMP_DIR, CACHE_DIR, XLA_CACHE_DIR, WANDB_DIR]:
        p.mkdir(parents=True, exist_ok=True)


def running_main() -> str:
    p = subprocess.run("ps -eo pid,ppid,etime,stat,cmd | grep -E 'main.py' | grep -v grep || true", shell=True, text=True, capture_output=True)
    return p.stdout.strip()


def env_for(gpu: int) -> dict[str, str]:
    env = os.environ.copy()
    env.update({
        'CUDA_VISIBLE_DEVICES': str(gpu),
        'OGBENCH_DATA_DIR': '/root/autodl-tmp/ogbench/data',
        'TMPDIR': str(TMP_DIR),
        'XDG_CACHE_HOME': str(CACHE_DIR),
        'XLA_CACHE_DIR': str(XLA_CACHE_DIR),
        'WANDB_DIR': str(WANDB_DIR),
        'MUJOCO_GL': 'egl',
        'PYOPENGL_PLATFORM': 'egl',
        'SDL_VIDEODRIVER': 'dummy',
        'LD_LIBRARY_PATH': '/root/.mujoco/mujoco210/bin:' + env.get('LD_LIBRARY_PATH', ''),
        'XLA_PYTHON_CLIENT_PREALLOCATE': 'true',
        'XLA_PYTHON_CLIENT_MEM_FRACTION': '0.90',
    })
    return env


def command(job: dict) -> list[str]:
    run_dir = EXP_DIR / job['name']
    ckpt_dir = RUN_BASE / 'checkpoints' / job['name']
    return [
        PYTHON, 'run', '-n', 'value-flows', 'python', 'main.py',
        f"--env_name={job['env']}",
        f'--save_dir={run_dir}',
        f"--wandb_run_group={job['name']}",
        f"--seed={job['seed']}",
        '--offline_steps=1000000',
        '--online_steps=0',
        '--eval_interval=100000',
        '--eval_episodes=50',
        '--log_interval=25000',
        '--save_interval=999999999',
        '--enable_wandb=0',
        *COMMON_FLAGS,
        f'--agent.checkpoint_dir={ckpt_dir}',
        *job['flags'],
    ]


def main() -> int:
    mkdirs()
    status = LOG_DIR / 'launch_status.txt'
    already = running_main()
    if already:
        status.write_text('BLOCKED existing main.py process\n' + already + '\n')
        print(status.read_text())
        return 2
    lines = [f'launch_time={datetime.now().isoformat(timespec="seconds")}']
    for job in JOBS:
        run_dir = EXP_DIR / job['name']
        log_dir = LOG_DIR / job['name']
        run_dir.mkdir(parents=True, exist_ok=True)
        log_dir.mkdir(parents=True, exist_ok=True)
        cmd = command(job)
        (log_dir / 'command.txt').write_text(' '.join(shlex.quote(x) for x in cmd) + '\n')
        (log_dir / 'reason.txt').write_text(job['reason'] + '\n')
        log = (log_dir / 'formal.log').open('w')
        proc = subprocess.Popen(cmd, cwd=REPO, env=env_for(job['gpu']), stdout=log, stderr=subprocess.STDOUT)
        (log_dir / 'formal.pid').write_text(str(proc.pid) + '\n')
        lines.append(f"{job['name']} gpu={job['gpu']} pid={proc.pid} log={log_dir / 'formal.log'}")
    status.write_text('\n'.join(lines) + '\n')
    print(status.read_text())
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

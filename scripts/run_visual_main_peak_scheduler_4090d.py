#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
import os
import re
import shlex
import subprocess
import time
from pathlib import Path

REPO = Path('/root/sb-value-flows')
RUN_BASE = Path('/root/autodl-tmp/sb-value-flows-runs/visual_main_peak_coverage_4090d')
EXP_DIR = RUN_BASE / 'exp'
LOG_DIR = RUN_BASE / 'logs'
TMP_DIR = RUN_BASE / 'tmp'
CACHE_DIR = RUN_BASE / 'cache'
XLA_CACHE_DIR = RUN_BASE / 'xla_cache'
WANDB_DIR = RUN_BASE / 'wandb'
OGBENCH_DATA_DIR = Path('/root/autodl-tmp/ogbench/data')
STATUS_PATH = LOG_DIR / 'scheduler_status.txt'
PYTHON = '/root/miniconda3/bin/conda'

PRIORITY = [
    ('visual-scene-play', 0.45),
    ('visual-puzzle-3x3-play', 0.25),
    ('visual-cube-double-play', 0.15),
    ('visual-antmaze-teleport-navigate', 0.15),
]
TASKS = [f'task{i}' for i in range(1, 6)]

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
    '--agent.save_eval_checkpoints=false',
    '--agent.visual_freeze_encoder_after_step=300000',
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


def ensure_dirs() -> None:
    for p in [EXP_DIR, LOG_DIR, TMP_DIR, CACHE_DIR, XLA_CACHE_DIR, WANDB_DIR, RUN_BASE / 'checkpoints']:
        p.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    ensure_dirs()
    line = f'[{time.strftime("%F %T")}] {msg}'
    print(line, flush=True)
    with STATUS_PATH.open('a') as f:
        f.write(line + '\n')


def shell(cmd: str) -> str:
    p = subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if p.returncode != 0:
        log(f'command failed rc={p.returncode}: {cmd}\n{p.stdout[-2000:]}')
    return p.stdout


def refresh_audit() -> None:
    shell("mkdir -p /tmp/visual_audit && find /root/autodl-tmp/sb-value-flows-runs /root/sb-value-flows -type f \\( -name 'eval.csv' -o -name 'train.csv' -o -name 'command.txt' \\) 2>/dev/null | sort > /tmp/visual_audit/all_candidate_files.txt")
    shell("grep '/eval.csv$' /tmp/visual_audit/all_candidate_files.txt > /tmp/visual_audit/all_eval_csv.txt || true")
    shell("grep '/train.csv$' /tmp/visual_audit/all_candidate_files.txt > /tmp/visual_audit/all_train_csv.txt || true")
    shell("grep '/command.txt$' /tmp/visual_audit/all_candidate_files.txt > /tmp/visual_audit/all_command_txt.txt || true")
    subprocess.run(['python3', 'scripts/audit_all_visual_experiments_4090d.py'], cwd=REPO, check=False)
    subprocess.run(['python3', 'scripts/plot_visual_best_peak_curves.py'], cwd=REPO, check=False)
    if (REPO / 'scripts/generate_visual_main_peak_reports.py').exists():
        subprocess.run(['python3', 'scripts/generate_visual_main_peak_reports.py'], cwd=REPO, check=False)


def fnum(x: str | None) -> float:
    try:
        if x in (None, ''):
            return math.nan
        return float(x)
    except Exception:
        return math.nan


def read_audit() -> list[dict[str, str]]:
    path = REPO / 'results/audit_all_visual_runs_4090d.csv'
    if not path.exists():
        return []
    with path.open(newline='') as f:
        return list(csv.DictReader(f))


def selected_cells(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str] | None]:
    out = {}
    for domain, _target in PRIORITY:
        for task in TASKS:
            candidates = [r for r in rows if r.get('visual_domain') == domain and r.get('task_id') == task and not math.isnan(fnum(r.get('best_peak_success')))]
            candidates.sort(key=lambda r: (fnum(r.get('best_peak_success')), fnum(r.get('final_success')), fnum(r.get('final_step'))), reverse=True)
            out[(domain, task)] = candidates[0] if candidates else None
    return out


def has_peak_sweep_attempt(rows: list[dict[str, str]], domain: str, task: str) -> bool:
    marker = '/visual_main_peak_coverage_4090d/'
    for row in rows:
        if row.get('visual_domain') != domain or row.get('task_id') != task:
            continue
        if marker in row.get('root_path', '') or marker in row.get('eval_csv', ''):
            return True
    return False


def active_envs() -> set[str]:
    out = shell("ps -eo args | grep -E 'main.py' | grep -v grep || true")
    envs = set()
    for line in out.splitlines():
        m = re.search(r'--env_name=([^ ]+)', line)
        if m:
            envs.add(m.group(1))
    return envs


def free_gpus() -> list[int]:
    out = shell("nvidia-smi --query-gpu=index,memory.used --format=csv,noheader,nounits")
    gpus = []
    for line in out.splitlines():
        parts = [p.strip() for p in line.split(',')]
        if len(parts) < 2:
            continue
        try:
            idx = int(parts[0]); used = int(parts[1])
        except Exception:
            continue
        if used < 1000:
            gpus.append(idx)
    return gpus


def ensure_data_links(domain: str) -> None:
    train = OGBENCH_DATA_DIR / f'{domain}-v0.npz'
    val = OGBENCH_DATA_DIR / f'{domain}-v0-val.npz'
    if not train.exists() or not val.exists():
        log(f'data base missing for {domain}: {train.exists()} {val.exists()}')
        return
    for task in TASKS:
        env = f'{domain}-singletask-{task}-v0'
        for suffix, src in [('.npz', train), ('-val.npz', val)]:
            dst = OGBENCH_DATA_DIR / f'{env}{suffix}'
            if dst.exists():
                continue
            try:
                os.link(src, dst)
            except Exception:
                try:
                    os.symlink(src, dst)
                except Exception as exc:
                    log(f'failed to link {dst}: {exc!r}')


def safe_name(text: str) -> str:
    return re.sub(r'[^A-Za-z0-9_.-]+', '_', text)


def build_command(domain: str, task: str, gpu: int) -> tuple[str, list[str], Path, Path]:
    env_name = f'{domain}-singletask-{task}-v0'
    stamp = time.strftime('%Y%m%d_%H%M%S')
    run_name = safe_name(f'{domain}_{task}_R2stableStrong_peak500k_seed2_{stamp}')
    run_dir = EXP_DIR / run_name
    log_dir = LOG_DIR / run_name
    ckpt_dir = RUN_BASE / 'checkpoints' / run_name
    cmd = [
        PYTHON, 'run', '-n', 'value-flows', 'python', 'main.py',
        f'--env_name={env_name}',
        f'--save_dir={run_dir}',
        f'--wandb_run_group={run_name}',
        '--seed=2',
        '--offline_steps=500000',
        '--online_steps=0',
        '--eval_interval=50000',
        '--eval_episodes=50',
        '--log_interval=25000',
        '--save_interval=999999999',
        '--enable_wandb=0',
        *COMMON_FLAGS,
        f'--agent.checkpoint_dir={ckpt_dir}',
    ]
    return run_name, cmd, run_dir, log_dir


def launch(domain: str, task: str, gpu: int) -> None:
    ensure_data_links(domain)
    run_name, cmd, run_dir, log_dir = build_command(domain, task, gpu)
    run_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update({
        'CUDA_VISIBLE_DEVICES': str(gpu),
        'OGBENCH_DATA_DIR': str(OGBENCH_DATA_DIR),
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
    command_text = ' '.join(shlex.quote(x) for x in cmd) + '\n'
    (log_dir / 'command.txt').write_text(command_text)
    (run_dir / 'command.txt').write_text(command_text)
    (log_dir / 'reason.txt').write_text(f'auto scheduled peak sweep for {domain} {task}\n')
    log_file = (log_dir / 'formal.log').open('w')
    proc = subprocess.Popen(cmd, cwd=REPO, env=env, stdout=log_file, stderr=subprocess.STDOUT)
    (log_dir / 'formal.pid').write_text(str(proc.pid) + '\n')
    log(f'LAUNCHED {run_name} domain={domain} task={task} gpu={gpu} pid={proc.pid}')


def choose_jobs(rows: list[dict[str, str]], active: set[str], slots: int) -> list[tuple[str, str]]:
    cells = selected_cells(rows)
    chosen: list[tuple[str, str]] = []
    for domain, target in PRIORITY:
        vals = []
        for task in TASKS:
            row = cells[(domain, task)]
            if row is not None and not math.isnan(fnum(row.get('best_peak_success'))):
                vals.append(fnum(row.get('best_peak_success')))
        mean = sum(vals) / len(vals) if vals else math.nan
        meets = len(vals) == 5 and not math.isnan(mean) and mean >= target
        log(f'ROW {domain}: covered={len(vals)}/5 mean={mean if not math.isnan(mean) else "nan"} target={target} meets={meets}')
        # Current objective prioritizes finishing 5-task coverage across domains.
        # Once all tasks in a row have a usable peak, move to the next domain even
        # if the row is below target; the peak gap remains visible in reports.
        if len(vals) == 5:
            continue
        candidates = []
        for task in TASKS:
            env = f'{domain}-singletask-{task}-v0'
            if env in active:
                continue
            row = cells[(domain, task)]
            attempted = 1 if has_peak_sweep_attempt(rows, domain, task) else 0
            peak = fnum(row.get('best_peak_success')) if row else math.nan
            if row is None or math.isnan(peak):
                candidates.append((0, attempted, -1.0, task))
            elif peak < target:
                candidates.append((1, attempted, peak, task))
        candidates.sort(key=lambda x: (x[0], x[1], x[2]))
        for _kind, _attempted, _peak, task in candidates:
            chosen.append((domain, task))
            if len(chosen) >= slots:
                return chosen
        return chosen
    return chosen


def main() -> int:
    ensure_dirs()
    refresh_audit()
    active = active_envs()
    gpus = free_gpus()
    log(f'active_envs={sorted(active)} free_gpus={gpus}')
    if not gpus:
        return 0
    rows = read_audit()
    jobs = choose_jobs(rows, active, len(gpus))
    if not jobs:
        log('no jobs selected')
        return 0
    for gpu, (domain, task) in zip(gpus, jobs):
        launch(domain, task, gpu)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

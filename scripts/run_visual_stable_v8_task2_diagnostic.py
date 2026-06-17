#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

RUN_BASE = Path('/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_task2_diagnostic')
EXP_DIR = RUN_BASE / 'exp'
LOG_DIR = RUN_BASE / 'logs'
REPORT_DIR = RUN_BASE / 'reports'
TMP_DIR = RUN_BASE / 'tmp'
CACHE_DIR = RUN_BASE / 'cache'
XLA_CACHE_DIR = RUN_BASE / 'xla_cache'
WANDB_DIR = RUN_BASE / 'wandb'
REPO = Path('/root/sb-value-flows')
REPORT_PATH = REPORT_DIR / 'visual_stable_v8_task2_diagnostic_report.md'
REPO_REPORT_PATH = REPO / 'reports/visual_stable_v8_task2_diagnostic_report.md'
STATUS_PATH = LOG_DIR / 'status.txt'
COMMAND_PATH = LOG_DIR / 'command.txt'
RUN_LOG = LOG_DIR / 'task2_main.log'
ENV_NAME = 'visual-antmaze-medium-navigate-singletask-task2-v0'
RUN_NAME = 'visual_stable_v8_task2_R2_stable_seed2_1m'
RUN_DIR = EXP_DIR / RUN_NAME
TARGET_STEPS = 1_000_000


def mkdirs() -> None:
    for p in [EXP_DIR, LOG_DIR, REPORT_DIR, TMP_DIR, CACHE_DIR, XLA_CACHE_DIR, WANDB_DIR, RUN_DIR]:
        p.mkdir(parents=True, exist_ok=True)


def base_env() -> dict[str, str]:
    env = os.environ.copy()
    env.update({
        'CUDA_VISIBLE_DEVICES': '0',
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


def command() -> list[str]:
    return [
        '/root/miniconda3/bin/conda', 'run', '-n', 'value-flows', 'python', 'main.py',
        f'--env_name={ENV_NAME}',
        f'--save_dir={RUN_DIR}',
        f'--wandb_run_group={RUN_NAME}',
        '--seed=2',
        '--offline_steps=1000000',
        '--online_steps=0',
        '--eval_interval=100000',
        '--eval_episodes=50',
        '--log_interval=25000',
        '--save_interval=999999999',
        '--enable_wandb=0',
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
        f'--agent.checkpoint_dir={RUN_BASE / "checkpoints" / RUN_NAME}',
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
        '--agent.visual_actor_lr_decay_after_step=300000',
        '--agent.visual_actor_lr_decay_mult=0.3',
        '--agent.visual_critic_lr_decay_after_step=300000',
        '--agent.visual_critic_lr_decay_mult=0.5',
        '--agent.visual_second_lr_decay_after_step=500000',
        '--agent.visual_second_actor_lr_decay_mult=0.3',
        '--agent.visual_second_critic_lr_decay_mult=0.5',
        '--agent.actor_ema_anchor_start_step=300000',
        '--agent.actor_ema_anchor_coef=0.01',
        '--agent.actor_ema_tau=0.995',
        '--agent.pm_sb_weight_uniform_mix=0.05',
        '--agent.pm_sb_weight_logit_clip=5.0',
        '--agent.pm_sb_weight_max=0.7',
    ]


def write_status(text: str) -> None:
    STATUS_PATH.write_text(text)


def find_csv(root: Path, name: str) -> Path | None:
    candidates = [p for p in root.rglob(name) if p.is_file()]
    if not candidates:
        return None
    def score(p: Path):
        try:
            rows = sum(1 for _ in p.open())
        except Exception:
            rows = 0
        return (rows, p.stat().st_mtime)
    return sorted(candidates, key=score, reverse=True)[0]


def read_rows(path: Path | None) -> list[dict[str, str]]:
    if path is None or not path.exists():
        return []
    with path.open(newline='') as f:
        return list(csv.DictReader(f))


def f(row: dict[str, str], keys: list[str]):
    for k in keys:
        if k in row and row[k] != '':
            try:
                return float(row[k])
            except Exception:
                return None
    return None


def summarize_eval(eval_csv: Path | None) -> dict:
    rows = read_rows(eval_csv)
    if not rows:
        return {'status': 'NO_EVAL'}
    traj = []
    best = None
    best_step = None
    peak500 = None
    peak500_step = None
    for r in rows:
        step = f(r, ['step', 'training/step'])
        succ = f(r, ['evaluation/success', 'eval/success', 'success'])
        if step is not None and succ is not None:
            traj.append((int(step), succ))
            if best is None or succ > best:
                best, best_step = succ, int(step)
            if step >= 500000 and (peak500 is None or succ > peak500):
                peak500, peak500_step = succ, int(step)
    last = rows[-1]
    final_step = int(f(last, ['step', 'training/step']) or 0)
    final_success = f(last, ['evaluation/success', 'eval/success', 'success'])
    final_return = f(last, ['evaluation/episode.return', 'evaluation/return', 'eval/return', 'return'])
    final_length = f(last, ['evaluation/episode.length', 'evaluation/length', 'eval/length', 'length'])
    status = 'COMPLETED' if final_step >= TARGET_STEPS * 0.98 else 'PARTIAL_OR_FAILED'
    return {
        'status': status,
        'final_step': final_step,
        'final_success': final_success,
        'final_return': final_return,
        'final_length': final_length,
        'best_success': best,
        'best_step': best_step,
        'peak_after_500k': peak500,
        'peak_after_500k_step': peak500_step,
        'drop_from_best': None if final_success is None or best is None else final_success - best,
        'trajectory': traj,
    }


def summarize_train(train_csv: Path | None) -> dict:
    rows = read_rows(train_csv)
    if not rows:
        return {}
    last = rows[-1]
    keys = [
        'training/stable/actor_lr', 'training/stable/critic_lr', 'training/stable/encoder_frozen',
        'training/actor/actor_anchor_loss', 'training/actor/actor_anchor_gate',
        'training/critic/stable/sb_weight_mean', 'training/critic/stable/sb_weight_std',
        'training/critic/stable/sb_weight_max', 'training/critic/stable/sb_weight_top10_mass',
        'training/critic/pm/reliability_mean', 'training/critic/pm/reliability_std',
        'training/critic/pm/flow_residual_mean', 'training/critic/pm/flow_residual_std',
        'training/critic/pm/disagree_mean', 'training/critic/pm/disagree_std',
    ]
    return {k: last.get(k, '') for k in keys if k in last}


def render_report(returncode: int, started: str, ended: str) -> str:
    eval_csv = find_csv(RUN_DIR, 'eval.csv')
    train_csv = find_csv(RUN_DIR, 'train.csv')
    es = summarize_eval(eval_csv)
    ts = summarize_train(train_csv)
    ckpts = sorted(str(p) for p in RUN_DIR.rglob('params_*.pkl'))
    traj = es.get('trajectory') or []
    traj_txt = ', '.join(f'{step//1000}k:{succ:.3g}' if step >= 1000 else f'{step}:{succ:.3g}' for step, succ in traj)
    lines = [
        '# Visual Stable v8 Task2 Diagnostic', '',
        'This is a single-task diagnostic run, not a full visual benchmark.', '',
        '## Scope', '',
        f'- env: `{ENV_NAME}`',
        '- config: `R2_stable`',
        '- seed: 2',
        '- target steps: 1,000,000',
        '- eval interval: 100k',
        '- eval episodes: 50',
        '- ordinary visual v7 continued: no',
        '- task1/task4 launched: no',
        '- formal result uses final eval.csv last row only; best checkpoint is diagnostic only', '',
        '## Timing', '',
        f'- started: {started}',
        f'- ended: {ended}',
        f'- process return code: {returncode}', '',
        '## Final Metrics', '',
        f'- status: {es.get("status")}',
        f'- final_step: {es.get("final_step")}',
        f'- final_success: {es.get("final_success")}',
        f'- final_return: {es.get("final_return")}',
        f'- final_length: {es.get("final_length")}',
        f'- best_success: {es.get("best_success")} @ {es.get("best_step")}',
        f'- peak_after_500k: {es.get("peak_after_500k")} @ {es.get("peak_after_500k_step")}',
        f'- drop_from_best: {es.get("drop_from_best")}', '',
        '## Success Trajectory', '',
        f'`{traj_txt}`', '',
        '## CSV Paths', '',
        f'- selected_eval_csv: `{eval_csv}`',
        f'- selected_train_csv: `{train_csv}`', '',
        '## Stable Diagnostics Final Train Row', '',
    ]
    if ts:
        for k, v in ts.items():
            lines.append(f'- `{k}`: {v}')
    else:
        lines.append('- No train diagnostics found.')
    lines += ['', '## Checkpoints', '', f'- checkpoint files: {len(ckpts)}', '- best checkpoint is diagnostic only and is not used as final result.', '', '## Command', '', '```bash', ' '.join(command()), '```', '']
    return '\n'.join(lines)


def update_registry_and_push() -> None:
    update = REPO / 'scripts/update_results_registry.py'
    if update.exists():
        subprocess.run([
            'python', str(update),
            '--scan_base', str(EXP_DIR),
            '--server', '4090d',
            '--machine_tag', '4090d',
            '--modality', 'visual',
            '--stage', 'visual_stable_v8_task2_1m',
            '--output_dir', 'results',
            '--commit', 'false',
        ], cwd=REPO, check=False)
    subprocess.run(['git', 'config', 'user.name', '4090d-results'], cwd=REPO, check=False)
    subprocess.run(['git', 'config', 'user.email', '4090d-results@local'], cwd=REPO, check=False)
    add_paths = [
        'reports/visual_stable_v8_task2_diagnostic_report.md',
        'scripts/run_visual_stable_v8_task2_diagnostic.py',
        'results/experiment_runs.csv',
        'results/eval_curves_index.csv',
        'results/task_scoreboard.csv',
        'results/task_scoreboard.md',
        'results/valueflow_task_baselines.csv',
    ]
    subprocess.run(['git', 'add', *add_paths], cwd=REPO, check=False)
    subprocess.run(['git', 'commit', '-m', 'Add visual stable v8 task2 diagnostic result'], cwd=REPO, check=False)
    subprocess.run(['git', 'push', 'origin', 'HEAD:results/visual-stable-v8-task2-diagnostic'], cwd=REPO, check=False)


def main() -> int:
    mkdirs()
    cmd = command()
    COMMAND_PATH.write_text(' '.join(cmd) + '\n')
    started = datetime.now().isoformat(timespec='seconds')
    write_status(f'status=RUNNING\nstarted={started}\nenv={ENV_NAME}\nrun_dir={RUN_DIR}\ncommand_path={COMMAND_PATH}\n')
    with RUN_LOG.open('w') as log:
        proc = subprocess.run(cmd, cwd=REPO, env=base_env(), stdout=log, stderr=subprocess.STDOUT)
    ended = datetime.now().isoformat(timespec='seconds')
    report = render_report(proc.returncode, started, ended)
    REPORT_PATH.write_text(report)
    REPO_REPORT_PATH.write_text(report)
    write_status(f'status=FINISHED\nreturncode={proc.returncode}\nstarted={started}\nended={ended}\nreport={REPORT_PATH}\nrepo_report={REPO_REPORT_PATH}\n')
    update_registry_and_push()
    return proc.returncode

if __name__ == '__main__':
    raise SystemExit(main())

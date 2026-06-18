#!/usr/bin/env python3
from __future__ import annotations

import csv
import os
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

REPO = Path('/root/sb-value-flows')
ENV_NAME = 'visual-antmaze-medium-navigate-singletask-task2-v0'
CONFIG_NAME = 'R2_stable_strong'
SEED = 2
TARGET_STEPS = 1_000_000
RUN_BASE = Path('/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_1_strong_4090d')
EXP_DIR = RUN_BASE / 'exp'
LOG_DIR = RUN_BASE / 'logs'
REPORT_DIR = RUN_BASE / 'reports'
TMP_DIR = RUN_BASE / 'tmp'
CACHE_DIR = RUN_BASE / 'cache'
XLA_CACHE_DIR = RUN_BASE / 'xla_cache'
WANDB_DIR = RUN_BASE / 'wandb'
RUN_NAME = 'visual_medium_task2_R2_stable_strong_seed2_1m'
SMOKE_NAME = 'smoke_visual_medium_task2_R2_stable_strong_seed2_1000'
FORMAL_RUN_DIR = EXP_DIR / RUN_NAME
SMOKE_RUN_DIR = EXP_DIR / SMOKE_NAME
STATUS_PATH = LOG_DIR / 'status.txt'
DRYRUN_PATH = LOG_DIR / 'dryrun_task2_strong.txt'
SMOKE_LOG = LOG_DIR / 'smoke_task2_strong.log'
FORMAL_LOG = LOG_DIR / 'formal_task2_strong.log'
COMMAND_PATH = LOG_DIR / 'command.txt'
PID_PATH = LOG_DIR / 'formal.pid'
PROGRESS_PATH = REPORT_DIR / 'task2_progress.md'
REPO_PROGRESS_PATH = REPO / 'reports/visual_stable_v8_1_strong_task2_progress.md'
DIAG_REPORT_PATH = REPORT_DIR / 'visual_stable_v8_1_strong_task2_diagnostic.md'
REPO_DIAG_REPORT_PATH = REPO / 'reports/visual_stable_v8_1_strong_task2_diagnostic.md'
DIAG_CSV_PATH = REPO / 'results/visual_stable_v8_1_strong_task2.csv'
PREV_REPORT_PATH = REPO / 'reports/visual_stable_v8_task2_diagnostic.md'
PREV_CSV_PATH = REPO / 'results/visual_stable_v8_task2_diagnostic.csv'
PREV_RUN = Path('/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_task2_diagnostic/exp/visual_stable_v8_task2_R2_stable_seed2_1m')

COMMON_AGENT_FLAGS = [
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
]
R2_FLAGS = [
    '--agent.pm_sb_reliability_score=flow_residual_disagree',
    '--agent.pm_sb_lambda=0.001',
    '--agent.pm_sb_reliability_normalize=std',
    '--agent.pm_sb_flow_residual_eps=0.05',
    '--agent.pm_sb_disagree_beta=0.5',
    '--agent.pm_sb_disagree_umax=3.0',
    '--agent.pm_sb_value_preserving=false',
]
STRONG_FLAGS = [
    '--agent.visual_stable_mode=true',
    '--agent.save_eval_checkpoints=true',
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


def mkdirs() -> None:
    for p in [EXP_DIR, LOG_DIR, REPORT_DIR, TMP_DIR, CACHE_DIR, XLA_CACHE_DIR, WANDB_DIR, REPO / 'reports', REPO / 'results']:
        p.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now().isoformat(timespec='seconds')


def write_status(text: str) -> None:
    STATUS_PATH.write_text(text)


def env_for(gpu: int = 0) -> dict[str, str]:
    e = os.environ.copy()
    e.update({
        'CUDA_VISIBLE_DEVICES': str(gpu),
        'OGBENCH_DATA_DIR': '/root/autodl-tmp/ogbench/data',
        'TMPDIR': str(TMP_DIR),
        'XDG_CACHE_HOME': str(CACHE_DIR),
        'XLA_CACHE_DIR': str(XLA_CACHE_DIR),
        'WANDB_DIR': str(WANDB_DIR),
        'MUJOCO_GL': 'egl',
        'PYOPENGL_PLATFORM': 'egl',
        'SDL_VIDEODRIVER': 'dummy',
        'LD_LIBRARY_PATH': '/root/.mujoco/mujoco210/bin:' + e.get('LD_LIBRARY_PATH', ''),
        'XLA_PYTHON_CLIENT_PREALLOCATE': 'true',
        'XLA_PYTHON_CLIENT_MEM_FRACTION': '0.90',
    })
    return e


def main_running() -> str:
    p = subprocess.run("ps -eo pid,ppid,etime,stat,cmd | grep -E 'main.py' | grep -v grep || true", shell=True, text=True, capture_output=True)
    return p.stdout.strip()


def disk_ok() -> bool:
    return shutil.disk_usage('/root/autodl-tmp').free > 20 * 1024**3


def cmd(run_dir: Path, run_name: str, steps: int, eval_episodes: int, smoke: bool) -> list[str]:
    return [
        '/root/miniconda3/bin/conda', 'run', '-n', 'value-flows', 'python', 'main.py',
        f'--env_name={ENV_NAME}',
        f'--save_dir={run_dir}',
        f'--wandb_run_group={run_name}',
        f'--seed={SEED}',
        f'--offline_steps={steps}',
        '--online_steps=0',
        '--eval_interval=100000' if not smoke else '--eval_interval=1000',
        f'--eval_episodes={eval_episodes}',
        '--log_interval=25000' if not smoke else '--log_interval=500',
        '--save_interval=999999999',
        '--enable_wandb=0',
        *COMMON_AGENT_FLAGS,
        f'--agent.checkpoint_dir={RUN_BASE / "checkpoints" / run_name}',
        *R2_FLAGS,
        *STRONG_FLAGS,
    ]


def find_csv(root: Path, name: str) -> Path | None:
    files = [p for p in root.rglob(name) if p.is_file()]
    if not files:
        return None
    def score(p: Path):
        try:
            rows = sum(1 for _ in p.open())
        except Exception:
            rows = 0
        return (rows, p.stat().st_mtime)
    return sorted(files, key=score, reverse=True)[0]


def read_csv(path: Path | None) -> list[dict[str, str]]:
    if path is None or not path.exists():
        return []
    with path.open(newline='') as f:
        return list(csv.DictReader(f))


def val(row: dict[str, str], keys: list[str]) -> float | None:
    for k in keys:
        if k in row and row[k] != '':
            try:
                return float(row[k])
            except Exception:
                pass
    return None


def summarize(run_root: Path, target_steps: int = TARGET_STEPS) -> dict:
    eval_csv = find_csv(run_root, 'eval.csv')
    train_csv = find_csv(run_root, 'train.csv')
    rows = read_csv(eval_csv)
    traj = []
    best = None
    best_step = None
    peak500 = None
    peak500_step = None
    for r in rows:
        step = int(val(r, ['step', 'training/step']) or 0)
        succ = val(r, ['evaluation/success', 'eval/success', 'success'])
        ret = val(r, ['evaluation/episode.return', 'evaluation/return', 'eval/return', 'return'])
        length = val(r, ['evaluation/episode.length', 'evaluation/length', 'eval/length', 'length'])
        traj.append((step, succ, ret, length))
        if succ is not None and (best is None or succ > best):
            best = succ; best_step = step
        if step >= 500000 and succ is not None and (peak500 is None or succ > peak500):
            peak500 = succ; peak500_step = step
    last = traj[-1] if traj else (0, None, None, None)
    train_rows = read_csv(train_csv)
    tlast = train_rows[-1] if train_rows else {}
    diag_keys = [
        'training/stable/actor_lr','training/stable/critic_lr','training/stable/encoder_frozen',
        'training/actor/actor_anchor_loss','training/actor/actor_anchor_gate',
        'training/critic/stable/sb_weight_mean','training/critic/stable/sb_weight_std','training/critic/stable/sb_weight_max','training/critic/stable/sb_weight_top10_mass',
        'training/critic/pm/reliability_mean','training/critic/pm/reliability_std',
        'training/critic/pm/flow_residual_mean','training/critic/pm/flow_residual_std',
        'training/critic/pm/disagree_mean','training/critic/pm/disagree_std',
        'training/visual_stable/actor_lr_mult','training/visual_stable/critic_lr_mult','training/visual_stable/target_tau',
    ]
    diagnostics = {k: tlast.get(k, '') for k in diag_keys if k in tlast}
    return {
        'eval_csv': str(eval_csv) if eval_csv else '',
        'train_csv': str(train_csv) if train_csv else '',
        'final_step': last[0],
        'final_success': last[1],
        'final_return': last[2],
        'final_length': last[3],
        'best_success': best,
        'best_step': best_step,
        'peak_after_500k': peak500,
        'peak_after_500k_step': peak500_step,
        'drop_from_best': None if best is None or last[1] is None else last[1] - best,
        'final_best_ratio': None if best in (None, 0) or last[1] is None else last[1] / best,
        'status': 'COMPLETED' if last[0] >= target_steps * 0.98 else 'PARTIAL_OR_FAILED',
        'trajectory': traj,
        'diagnostics': diagnostics,
    }


def traj_text(traj) -> str:
    parts = []
    for step, succ, ret, length in traj:
        label = '1M' if step == 1000000 else ('0' if step <= 1 else f'{step//1000}k')
        parts.append(f'{label}:{succ}')
    return ', '.join(parts)


def write_previous_v8_report() -> None:
    s = summarize(PREV_RUN)
    PREV_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PREV_CSV_PATH.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['env','config','seed','target_steps','status','final_step','final_success','best_success','best_step','peak_after_500k','peak_after_500k_step','drop_from_best','eval_csv','train_csv'])
        w.writeheader()
        w.writerow({
            'env': ENV_NAME, 'config': 'R2_stable', 'seed': SEED, 'target_steps': TARGET_STEPS,
            **{k: s.get(k) for k in ['status','final_step','final_success','best_success','best_step','peak_after_500k','peak_after_500k_step','drop_from_best','eval_csv','train_csv']},
        })
    text = f"""# Visual Stable v8 Task2 Diagnostic

Previous completed diagnostic run.

## Result

- Env: `{ENV_NAME}`
- Config: `R2_stable`
- Seed: 2
- Status: {s.get('status')}
- Final success: {s.get('final_success')} @ {s.get('final_step')}
- Best success: {s.get('best_success')} @ {s.get('best_step')}
- Peak after 500k: {s.get('peak_after_500k')} @ {s.get('peak_after_500k_step')}
- Drop from best: {s.get('drop_from_best')}

## Comparison

- v7 task2 / R2: best 0.82, final 0.02.
- v8 task2 / R2_stable: best 0.74, final {s.get('final_success')}.
- Conclusion: v8 improves retention versus v7, but late collapse remains.
- This is diagnostic, not a final positive.
- Do not use best checkpoint as final.
- Do not expand task1/task4 under current `R2_stable`.
- Next config: `R2_stable_strong`.

## Trajectory

`{traj_text(s.get('trajectory'))}`

## CSV Paths

- eval: `{s.get('eval_csv')}`
- train: `{s.get('train_csv')}`
"""
    PREV_REPORT_PATH.write_text(text)


def dry_run() -> bool:
    c = cmd(FORMAL_RUN_DIR, RUN_NAME, TARGET_STEPS, 50, smoke=False)
    shell = ' '.join(c)
    text = f"""visual_stable_v8_1_strong dry-run
planned_runs=1
env={ENV_NAME}
config={CONFIG_NAME}
seed={SEED}
target_steps={TARGET_STEPS}
output_base={RUN_BASE}

Required strong flags:
pm_sb_weight_uniform_mix=0.10
pm_sb_weight_logit_clip=3.0
pm_sb_weight_max=0.5
actor_anchor_coef=0.02
visual_actor_lr_decay_after_step=300000
visual_actor_lr_decay_mult=0.09
visual_critic_lr_decay_after_step=300000
visual_critic_lr_decay_mult=0.25
visual_second_lr_decay_after_step=600000
visual_second_actor_lr_decay_mult=0.3333333333
visual_second_critic_lr_decay_mult=0.4
save_eval_checkpoints=true

Command:
{shell}
"""
    DRYRUN_PATH.write_text(text)
    checks = [
        'visual-antmaze-medium-navigate-singletask-task2-v0' in text,
        'task1' not in text and 'task4' not in text,
        '--agent=agents/pm_value_flows.py' in text,
        text.index('--agent=agents/pm_value_flows.py') < text.index('--agent.encoder=impala_small'),
        '--agent.pm_sb_weight_uniform_mix=0.10' in text,
        '--agent.pm_sb_weight_logit_clip=3.0' in text,
        '--agent.pm_sb_weight_max=0.5' in text,
        '--agent.actor_ema_anchor_coef=0.02' in text,
        '--agent.visual_second_lr_decay_after_step=600000' in text,
        '--agent.save_eval_checkpoints=true' in text,
    ]
    return all(checks)


def run_smoke() -> bool:
    c = cmd(SMOKE_RUN_DIR, SMOKE_NAME, 1000, 2, smoke=True)
    with SMOKE_LOG.open('w') as log:
        rc = subprocess.run(c, cwd=REPO, env=env_for(0), stdout=log, stderr=subprocess.STDOUT).returncode
    if rc != 0:
        return False
    s = summarize(SMOKE_RUN_DIR, target_steps=1000)
    ckpts = list(SMOKE_RUN_DIR.rglob('params_*.pkl'))
    return bool(s.get('eval_csv') and s.get('train_csv') and ckpts and s.get('final_step', 0) >= 1000)


def render_progress(s: dict, title: str, running: bool = True) -> str:
    lines = [f'# {title}', '', f'Generated: {now()}', '', f'- env: `{ENV_NAME}`', f'- config: `{CONFIG_NAME}`', '- seed: 2', f'- status: {s.get("status")}', f'- final/current step: {s.get("final_step")}', f'- final/current success: {s.get("final_success")}', f'- best success: {s.get("best_success")} @ {s.get("best_step")}', f'- peak_after_500k: {s.get("peak_after_500k")} @ {s.get("peak_after_500k_step")}', f'- drop_from_best: {s.get("drop_from_best")}', f'- final/best ratio: {s.get("final_best_ratio")}', '', '## Trajectory', '', '| step | success | return | length |', '|---:|---:|---:|---:|']
    for step, succ, ret, length in s.get('trajectory') or []:
        label = '1M' if step == 1000000 else ('0' if step <= 1 else f'{step//1000}k')
        lines.append(f'| {label} | {succ} | {ret} | {length} |')
    lines += ['', '## Stable Diagnostics Latest Train Row', '']
    for k, v in (s.get('diagnostics') or {}).items():
        lines.append(f'- `{k}`: {v}')
    lines += ['', '## CSV Paths', '', f'- eval: `{s.get("eval_csv")}`', f'- train: `{s.get("train_csv")}`', '']
    return '\n'.join(lines)


def monitor_formal(proc: subprocess.Popen) -> int:
    while proc.poll() is None:
        s = summarize(FORMAL_RUN_DIR)
        PROGRESS_PATH.write_text(render_progress(s, 'Visual Stable v8.1 Strong Task2 Progress'))
        REPO_PROGRESS_PATH.write_text(PROGRESS_PATH.read_text())
        write_status(f'status=RUNNING_FORMAL\npid={proc.pid}\nupdated={now()}\nlatest_step={s.get("final_step")}\nlatest_success={s.get("final_success")}\nrun_dir={FORMAL_RUN_DIR}\n')
        time.sleep(300)
    rc = proc.returncode
    s = summarize(FORMAL_RUN_DIR)
    PROGRESS_PATH.write_text(render_progress(s, 'Visual Stable v8.1 Strong Task2 Progress', running=False))
    REPO_PROGRESS_PATH.write_text(PROGRESS_PATH.read_text())
    return rc


def run_formal() -> int:
    c = cmd(FORMAL_RUN_DIR, RUN_NAME, TARGET_STEPS, 50, smoke=False)
    COMMAND_PATH.write_text(' '.join(c) + '\n')
    with (LOG_DIR / 'formal_task2_strong.log').open('w') as log:
        proc = subprocess.Popen(c, cwd=REPO, env=env_for(0), stdout=log, stderr=subprocess.STDOUT)
    (LOG_DIR / 'formal.pid').write_text(str(proc.pid) + '\n')
    return monitor_formal(proc)


def write_final_report(returncode: int) -> None:
    s = summarize(FORMAL_RUN_DIR)
    rows = [{
        'env': ENV_NAME, 'config': CONFIG_NAME, 'seed': SEED, 'target_steps': TARGET_STEPS,
        'returncode': returncode,
        **{k: s.get(k) for k in ['status','final_step','final_success','final_return','final_length','best_success','best_step','peak_after_500k','peak_after_500k_step','drop_from_best','final_best_ratio','eval_csv','train_csv']},
    }]
    with DIAG_CSV_PATH.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    comparison = f"""- v7 R2 task2: best 0.82, final 0.02
- v8 R2_stable task2: best 0.74, final 0.26, peak_after_500k 0.56, drop -0.48
- v8.1 R2_stable_strong task2: best {s.get('best_success')}, final {s.get('final_success')}, peak_after_500k {s.get('peak_after_500k')}, drop {s.get('drop_from_best')}
"""
    solved = 'unknown until completed'
    if s.get('status') == 'COMPLETED':
        final = s.get('final_success') or 0.0
        drop = s.get('drop_from_best') or 0.0
        if final >= 0.5 and drop >= -0.25:
            solved = 'substantially mitigated; consider task1/task4 expansion cautiously'
        elif final > 0.26:
            solved = 'mitigated versus v8, but not solved'
        else:
            solved = 'not solved'
    text = render_progress(s, 'Visual Stable v8.1 Strong Task2 Diagnostic', running=False)
    text += f"\n## Comparisons\n\n{comparison}\n## Interpretation\n\n- Return code: {returncode}\n- Collapse assessment: {solved}\n- Expand task1/task4: {'yes, cautiously' if 'substantially' in solved else 'no'}\n- Best checkpoint remains diagnostic only; final uses eval.csv last row.\n"
    DIAG_REPORT_PATH.write_text(text)
    REPO_DIAG_REPORT_PATH.write_text(text)


def update_registry_commit_push() -> None:
    update = REPO / 'scripts/update_results_registry.py'
    if update.exists():
        subprocess.run(['python', str(update), '--scan_base', str(EXP_DIR), '--server', '4090d', '--machine_tag', '4090d-visual-stable-strong', '--modality', 'visual', '--stage', 'visual_stable_v8_1_strong', '--output_dir', 'results', '--commit', 'false'], cwd=REPO, check=False)
    subprocess.run(['git', 'config', 'user.name', '4090d-results'], cwd=REPO, check=False)
    subprocess.run(['git', 'config', 'user.email', '4090d-results@local'], cwd=REPO, check=False)
    paths = [
        'scripts/run_visual_stable_v8_1_strong_task2_4090d.py',
        'reports/visual_stable_v8_task2_diagnostic.md',
        'results/visual_stable_v8_task2_diagnostic.csv',
        'reports/visual_stable_v8_1_strong_task2_diagnostic.md',
        'results/visual_stable_v8_1_strong_task2.csv',
        'reports/visual_stable_v8_1_strong_task2_progress.md',
        'results/task_scoreboard.csv',
        'results/task_scoreboard.md',
        'results/experiment_runs.csv',
        'results/eval_curves_index.csv',
    ]
    subprocess.run(['git', 'add', *paths], cwd=REPO, check=False)
    subprocess.run(['git', 'commit', '-m', 'Add visual stable v8.1 strong task2 diagnostic result'], cwd=REPO, check=False)
    subprocess.run(['git', 'push', 'origin', 'HEAD:results/visual-stable-v8-1-strong-task2'], cwd=REPO, check=False)


def main() -> int:
    mkdirs()
    write_status(f'status=STARTING\nupdated={now()}\n')
    if main_running():
        write_status('status=BLOCKED_MAIN_RUNNING\n' + main_running() + '\n')
        return 2
    if not disk_ok():
        write_status('status=BLOCKED_DISK\n')
        return 3
    write_previous_v8_report()
    # Optional v8 registry scan requested by user.
    update = REPO / 'scripts/update_results_registry.py'
    if update.exists():
        subprocess.run(['python', str(update), '--scan_base', '/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/exp', '--server', '4090d', '--machine_tag', '4090d-visual-stable', '--modality', 'visual', '--stage', 'visual_stable_v8', '--output_dir', 'results', '--commit', 'false'], cwd=REPO, check=False)
    if not dry_run():
        write_status('status=FAILED_DRY_RUN\n')
        return 4
    write_status(f'status=RUNNING_SMOKE\nupdated={now()}\n')
    if not run_smoke():
        write_status(f'status=FAILED_SMOKE\nupdated={now()}\nlog={SMOKE_LOG}\n')
        return 5
    if main_running():
        write_status('status=BLOCKED_MAIN_RUNNING_AFTER_SMOKE\n' + main_running() + '\n')
        return 6
    write_status(f'status=LAUNCHING_FORMAL\nupdated={now()}\n')
    rc = run_formal()
    write_final_report(rc)
    update_registry_commit_push()
    write_status(f'status=FINISHED\nreturncode={rc}\nupdated={now()}\nreport={DIAG_REPORT_PATH}\nrepo_report={REPO_DIAG_REPORT_PATH}\n')
    return rc

if __name__ == '__main__':
    raise SystemExit(main())

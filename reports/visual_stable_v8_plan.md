# Visual Stable v8 Dry-Run Plan

Generated: 2026-06-16T14:58:17

## Scope

This is a dry-run plan only. It does not launch `main.py` or start training.
The goal is to test whether visual-specific stability mechanisms reduce `best-in-run success - final success` collapse seen in visual v7.

## Baseline Diagnosis From v7

- visual-antmaze-medium R2 completed 5-task final mean: 0.212
- visual-antmaze-medium R2 best-in-run mean: 0.792
- conclusion: strong early learning, severe late-training collapse; diagnostic only, not a final-performance positive.

## Planned Diagnostic Runs

| env | config | seed | steps | reason |
| --- | --- | --- | --- | --- |
| visual-antmaze-medium-navigate-singletask-task1-v0 | R2_stable | 2 | 1M | v7 best 0.78 -> final 0.20, drop -0.58 |
| visual-antmaze-medium-navigate-singletask-task2-v0 | R2_stable | 2 | 1M | v7 best 0.82 -> final 0.02, drop -0.80 |
| visual-antmaze-medium-navigate-singletask-task4-v0 | R2_stable | 2 | 1M | v7 best 0.86 -> final 0.40, drop -0.46 |

## R2_stable Changes vs v7 R2

- Save checkpoints at every eval interval, plus best-eval and final checkpoints. Best checkpoint is diagnostic only; final result remains final eval.csv last row.
- Actor learning rate decay after 300k: x0.3; second decay after 500k: x0.3.
- Critic learning rate decay after 300k: x0.5; second decay after 500k: x0.5.
- Encoder freeze or encoder LR x0.1 after 300k, depending on implementation support.
- Actor EMA anchor from 300k with coef 0.01 and tau 0.995.
- SB/reliability weight stabilization: uniform mix 0.05, logit clip 5.0, max cap 0.7 with renormalization.
- Eval remains paper-like: eval_interval 100k, eval_episodes 50, batch_size 256, num_samples 16, num_flow_steps 10.

## Late-Collapse Metrics

Each run report must include: success_final, success_best, best_step, peak_after_500k, drop_from_best = final - best, and the full eval trajectory.
The target improvement is reduced negative drop, not merely a higher early peak.

## Code Modification Requirement

Actual training requires agent support for the visual_stable flags listed below. If the current worktree does not implement a flag, training must stop before launch and report the unsupported flag. This dry-run intentionally does not validate runtime flag support by launching training.

## Output Directories

- RUN_BASE: `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d`
- EXP_DIR: `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/exp`
- LOG_DIR: `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/logs`
- REPORT_DIR: `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/reports`
- CHECKPOINT_DIR: `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/checkpoints`

## Exact Commands

### visual-antmaze-medium-navigate-singletask-task1-v0 on GPU0

```bash
CUDA_VISIBLE_DEVICES=0 OGBENCH_DATA_DIR=/root/autodl-tmp/ogbench/data TMPDIR=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/tmp XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/cache XLA_CACHE_DIR=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/xla_cache WANDB_DIR=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/wandb MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 python main.py --env_name=visual-antmaze-medium-navigate-singletask-task1-v0 --save_dir=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/exp/visual_stable_v8_R2_stable_visual-antmaze-medium-navigate-singletask-task1-v0_seed2_1m --wandb_run_group=visual_stable_v8_R2_stable_visual-antmaze-medium-navigate-singletask-task1-v0_seed2_1m --seed=2 --offline_steps=1000000 --online_steps=0 --eval_interval=100000 --eval_episodes=50 --log_interval=25000 --save_interval=999999999 --enable_wandb=0 --agent=agents/pm_value_flows.py --agent.encoder=impala_small --agent.batch_size=256 --agent.num_samples=16 --agent.num_flow_steps=10 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.checkpoint_dir=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/checkpoints/visual_stable_v8_R2_stable_visual-antmaze-medium-navigate-singletask-task1-v0_seed2_1m --agent.pm_sb_reliability_score=flow_residual_disagree --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_value_preserving=false --agent.visual_stable_mode=true --agent.save_eval_checkpoints=true --agent.visual_freeze_encoder_after_step=300000 --agent.visual_actor_lr_decay_after_step=300000 --agent.visual_actor_lr_decay_mult=0.3 --agent.visual_critic_lr_decay_after_step=300000 --agent.visual_critic_lr_decay_mult=0.5 --agent.visual_second_lr_decay_after_step=500000 --agent.visual_second_actor_lr_decay_mult=0.3 --agent.visual_second_critic_lr_decay_mult=0.5 --agent.actor_ema_anchor_start_step=300000 --agent.actor_ema_anchor_coef=0.01 --agent.actor_ema_tau=0.995 --agent.pm_sb_weight_uniform_mix=0.05 --agent.pm_sb_weight_logit_clip=5.0 --agent.pm_sb_weight_max=0.7
```

### visual-antmaze-medium-navigate-singletask-task2-v0 on GPU1

```bash
CUDA_VISIBLE_DEVICES=1 OGBENCH_DATA_DIR=/root/autodl-tmp/ogbench/data TMPDIR=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/tmp XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/cache XLA_CACHE_DIR=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/xla_cache WANDB_DIR=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/wandb MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 python main.py --env_name=visual-antmaze-medium-navigate-singletask-task2-v0 --save_dir=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/exp/visual_stable_v8_R2_stable_visual-antmaze-medium-navigate-singletask-task2-v0_seed2_1m --wandb_run_group=visual_stable_v8_R2_stable_visual-antmaze-medium-navigate-singletask-task2-v0_seed2_1m --seed=2 --offline_steps=1000000 --online_steps=0 --eval_interval=100000 --eval_episodes=50 --log_interval=25000 --save_interval=999999999 --enable_wandb=0 --agent=agents/pm_value_flows.py --agent.encoder=impala_small --agent.batch_size=256 --agent.num_samples=16 --agent.num_flow_steps=10 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.checkpoint_dir=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/checkpoints/visual_stable_v8_R2_stable_visual-antmaze-medium-navigate-singletask-task2-v0_seed2_1m --agent.pm_sb_reliability_score=flow_residual_disagree --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_value_preserving=false --agent.visual_stable_mode=true --agent.save_eval_checkpoints=true --agent.visual_freeze_encoder_after_step=300000 --agent.visual_actor_lr_decay_after_step=300000 --agent.visual_actor_lr_decay_mult=0.3 --agent.visual_critic_lr_decay_after_step=300000 --agent.visual_critic_lr_decay_mult=0.5 --agent.visual_second_lr_decay_after_step=500000 --agent.visual_second_actor_lr_decay_mult=0.3 --agent.visual_second_critic_lr_decay_mult=0.5 --agent.actor_ema_anchor_start_step=300000 --agent.actor_ema_anchor_coef=0.01 --agent.actor_ema_tau=0.995 --agent.pm_sb_weight_uniform_mix=0.05 --agent.pm_sb_weight_logit_clip=5.0 --agent.pm_sb_weight_max=0.7
```

### visual-antmaze-medium-navigate-singletask-task4-v0 on GPU0

```bash
CUDA_VISIBLE_DEVICES=0 OGBENCH_DATA_DIR=/root/autodl-tmp/ogbench/data TMPDIR=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/tmp XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/cache XLA_CACHE_DIR=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/xla_cache WANDB_DIR=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/wandb MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 python main.py --env_name=visual-antmaze-medium-navigate-singletask-task4-v0 --save_dir=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/exp/visual_stable_v8_R2_stable_visual-antmaze-medium-navigate-singletask-task4-v0_seed2_1m --wandb_run_group=visual_stable_v8_R2_stable_visual-antmaze-medium-navigate-singletask-task4-v0_seed2_1m --seed=2 --offline_steps=1000000 --online_steps=0 --eval_interval=100000 --eval_episodes=50 --log_interval=25000 --save_interval=999999999 --enable_wandb=0 --agent=agents/pm_value_flows.py --agent.encoder=impala_small --agent.batch_size=256 --agent.num_samples=16 --agent.num_flow_steps=10 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.checkpoint_dir=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/checkpoints/visual_stable_v8_R2_stable_visual-antmaze-medium-navigate-singletask-task4-v0_seed2_1m --agent.pm_sb_reliability_score=flow_residual_disagree --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_value_preserving=false --agent.visual_stable_mode=true --agent.save_eval_checkpoints=true --agent.visual_freeze_encoder_after_step=300000 --agent.visual_actor_lr_decay_after_step=300000 --agent.visual_actor_lr_decay_mult=0.3 --agent.visual_critic_lr_decay_after_step=300000 --agent.visual_critic_lr_decay_mult=0.5 --agent.visual_second_lr_decay_after_step=500000 --agent.visual_second_actor_lr_decay_mult=0.3 --agent.visual_second_critic_lr_decay_mult=0.5 --agent.actor_ema_anchor_start_step=300000 --agent.actor_ema_anchor_coef=0.01 --agent.actor_ema_tau=0.995 --agent.pm_sb_weight_uniform_mix=0.05 --agent.pm_sb_weight_logit_clip=5.0 --agent.pm_sb_weight_max=0.7
```

## Confirmation Gate

Do not start these runs until explicitly confirmed by the user. The dry-run script refuses to train unless invoked with `--confirm_train true`, which is intentionally not used in this plan.

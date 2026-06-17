# Visual Stable v8 Task2 Diagnostic

This is a single-task diagnostic run, not a full visual benchmark.

## Scope

- env: `visual-antmaze-medium-navigate-singletask-task2-v0`
- config: `R2_stable`
- seed: 2
- target steps: 1,000,000
- eval interval: 100k
- eval episodes: 50
- ordinary visual v7 continued: no
- task1/task4 launched: no
- formal result uses final eval.csv last row only; best checkpoint is diagnostic only

## Timing

- started: 2026-06-16T16:26:44
- ended: 2026-06-17T18:53:48
- process return code: 0

## Final Metrics

- status: COMPLETED
- final_step: 1000000
- final_success: 0.26
- final_return: -902.96
- final_length: 903.22
- best_success: 0.74 @ 100000
- peak_after_500k: 0.56 @ 500000
- drop_from_best: -0.48

## Success Trajectory

`1:0, 100k:0.74, 200k:0.58, 300k:0.56, 400k:0.5, 500k:0.56, 600k:0.48, 700k:0.28, 800k:0.28, 900k:0.3, 1000k:0.26`

## CSV Paths

- selected_eval_csv: `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_task2_diagnostic/exp/visual_stable_v8_task2_R2_stable_seed2_1m/visual_stable_v8_task2_R2_stable_seed2_1m/sd002_20260616_162650/eval.csv`
- selected_train_csv: `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_task2_diagnostic/exp/visual_stable_v8_task2_R2_stable_seed2_1m/visual_stable_v8_task2_R2_stable_seed2_1m/sd002_20260616_162650/train.csv`

## Stable Diagnostics Final Train Row

- `training/stable/actor_lr`: 2.7000002e-05
- `training/stable/critic_lr`: 7.5e-05
- `training/stable/encoder_frozen`: 1.0
- `training/actor/actor_anchor_loss`: 1.5919676
- `training/actor/actor_anchor_gate`: 1.0
- `training/critic/stable/sb_weight_mean`: 0.24999976
- `training/critic/stable/sb_weight_std`: 0.16811672
- `training/critic/stable/sb_weight_max`: 0.6001536
- `training/critic/stable/sb_weight_top10_mass`: 0.99999905
- `training/critic/pm/reliability_mean`: 9773.4795
- `training/critic/pm/reliability_std`: 78429.664
- `training/critic/pm/flow_residual_mean`: 726.36163
- `training/critic/pm/flow_residual_std`: 790.61707
- `training/critic/pm/disagree_mean`: 0.23877706
- `training/critic/pm/disagree_std`: 0.71543527

## Checkpoints

- checkpoint files: 14
- best checkpoint is diagnostic only and is not used as final result.

## Command

```bash
/root/miniconda3/bin/conda run -n value-flows python main.py --env_name=visual-antmaze-medium-navigate-singletask-task2-v0 --save_dir=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_task2_diagnostic/exp/visual_stable_v8_task2_R2_stable_seed2_1m --wandb_run_group=visual_stable_v8_task2_R2_stable_seed2_1m --seed=2 --offline_steps=1000000 --online_steps=0 --eval_interval=100000 --eval_episodes=50 --log_interval=25000 --save_interval=999999999 --enable_wandb=0 --agent=agents/pm_value_flows.py --agent.encoder=impala_small --agent.batch_size=256 --agent.num_samples=16 --agent.num_flow_steps=10 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.checkpoint_dir=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_task2_diagnostic/checkpoints/visual_stable_v8_task2_R2_stable_seed2_1m --agent.pm_sb_reliability_score=flow_residual_disagree --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_value_preserving=false --agent.visual_stable_mode=true --agent.save_eval_checkpoints=true --agent.visual_freeze_encoder_after_step=300000 --agent.visual_actor_lr_decay_after_step=300000 --agent.visual_actor_lr_decay_mult=0.3 --agent.visual_critic_lr_decay_after_step=300000 --agent.visual_critic_lr_decay_mult=0.5 --agent.visual_second_lr_decay_after_step=500000 --agent.visual_second_actor_lr_decay_mult=0.3 --agent.visual_second_critic_lr_decay_mult=0.5 --agent.actor_ema_anchor_start_step=300000 --agent.actor_ema_anchor_coef=0.01 --agent.actor_ema_tau=0.995 --agent.pm_sb_weight_uniform_mix=0.05 --agent.pm_sb_weight_logit_clip=5.0 --agent.pm_sb_weight_max=0.7
```

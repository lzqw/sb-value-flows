# Visual Stable v8.1 Progress

Generated: 2026-06-20 17:26:52

Final result uses only the last eval.csv row. Best/peak/checkpoints are diagnostics only.

## Process

```
 50299      1       01:17 S    /root/miniconda3/bin/python /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=visual-antmaze-medium-navigate-singletask-task1-v0 --save_dir=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8p1_4090d/exp/visual_stable_v8p1_task1_R2stableStrong_seed2 --wandb_run_group=visual_stable_v8p1_task1_R2stableStrong_seed2 --seed=2 --offline_steps=1000000 --online_steps=0 --eval_interval=100000 --eval_episodes=50 --log_interval=25000 --save_interval=999999999 --enable_wandb=0 --agent=agents/pm_value_flows.py --agent.encoder=impala_small --agent.batch_size=256 --agent.num_samples=16 --agent.num_flow_steps=10 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.checkpoint_dir=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8p1_4090d/checkpoints/visual_stable_v8p1_task1_R2stableStrong_seed2 --agent.pm_sb_reliability_score=flow_residual_disagree --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_value_preserving=false --agent.visual_stable_mode=true --agent.save_eval_checkpoints=true --agent.visual_freeze_encoder_after_step=300000 --agent.visual_actor_lr_decay_after_step=300000 --agent.visual_actor_lr_decay_mult=0.09 --agent.visual_critic_lr_decay_after_step=300000 --agent.visual_critic_lr_decay_mult=0.25 --agent.visual_second_lr_decay_after_step=600000 --agent.visual_second_actor_lr_decay_mult=0.3333333333 --agent.visual_second_critic_lr_decay_mult=0.4 --agent.actor_ema_anchor_start_step=300000 --agent.actor_ema_anchor_coef=0.02 --agent.actor_ema_tau=0.995 --agent.pm_sb_weight_uniform_mix=0.10 --agent.pm_sb_weight_logit_clip=3.0 --agent.pm_sb_weight_max=0.5
 50308  50299       01:17 S    /usr/bin/bash /root/autodl-tmp/sb-value-flows-runs/visual_stable_v8p1_4090d/tmp/tmp_0p85m2z
 50316  50308       01:15 Rl   python main.py --env_name=visual-antmaze-medium-navigate-singletask-task1-v0 --save_dir=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8p1_4090d/exp/visual_stable_v8p1_task1_R2stableStrong_seed2 --wandb_run_group=visual_stable_v8p1_task1_R2stableStrong_seed2 --seed=2 --offline_steps=1000000 --online_steps=0 --eval_interval=100000 --eval_episodes=50 --log_interval=25000 --save_interval=999999999 --enable_wandb=0 --agent=agents/pm_value_flows.py --agent.encoder=impala_small --agent.batch_size=256 --agent.num_samples=16 --agent.num_flow_steps=10 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.checkpoint_dir=/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8p1_4090d/checkpoints/visual_stable_v8p1_task1_R2stableStrong_seed2 --agent.pm_sb_reliability_score=flow_residual_disagree --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_value_preserving=false --agent.visual_stable_mode=true --agent.save_eval_checkpoints=true --agent.visual_freeze_encoder_after_step=300000 --agent.visual_actor_lr_decay_after_step=300000 --agent.visual_actor_lr_decay_mult=0.09 --agent.visual_critic_lr_decay_after_step=300000 --agent.visual_critic_lr_decay_mult=0.25 --agent.visual_second_lr_decay_after_step=600000 --agent.visual_second_actor_lr_decay_mult=0.3333333333 --agent.visual_second_critic_lr_decay_mult=0.4 --agent.actor_ema_anchor_start_step=300000 --agent.actor_ema_anchor_coef=0.02 --agent.actor_ema_tau=0.995 --agent.pm_sb_weight_uniform_mix=0.10 --agent.pm_sb_weight_logit_clip=3.0 --agent.pm_sb_weight_max=0.5
 51041  51030       00:00 Ss   bash -c cd /root/sb-value-flows || exit 1; python3 /tmp/update_visual_v8p1_progress.py; python3 /root/sb-value-flows-registry-4090d/scripts/update_results_registry.py --scan_base /root/autodl-tmp/sb-value-flows-runs/visual_stable_v8p1_4090d --server 4090d --machine_tag 4090d-visual-stable-v8p1 --modality visual --stage visual_stable_v8p1 --output_dir results --commit false || true; python3 /root/sb-value-flows-registry-4090d/scripts/update_results_registry.py --scan_base /root/autodl-tmp/sb-value-flows-runs/visual_stable_v8p1_task4_R2stableStrong_seed2_4090d/exp --server 4090d --machine_tag 4090d-visual-stable-v8p1 --modality visual --stage visual_stable_v8p1 --output_dir results --commit false || true; git status --short results/visual_stable_v8p1_runs.csv reports/visual_stable_v8p1_progress.md results/experiment_runs.csv results/eval_curves_index.csv results/task_scoreboard.csv results/task_scoreboard.md
```

## GPU

```
0, 160, 0
1, 22037, 0
```

## Summary

| task | status | final step | final | best | peak after 500k | drop | run_dir |
|---|---|---:|---:|---|---|---:|---|
| task2 | COMPLETED | 1000000 | 0.4 | 0.74 @ 300000 | 0.56 @ 600000 | -0.33999999999999997 | `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_1_strong_4090d/exp/visual_medium_task2_R2_stable_strong_seed2_1m` |
| task4 | COMPLETED | 1000000 | 0.34 | 0.82 @ 100000 | 0.46 @ 900000 | -0.4799999999999999 | `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8p1_task4_R2stableStrong_seed2_4090d/exp/visual_medium_task4_R2_stable_strong_seed2_1m` |
| task1 | NO_EVAL |  |  |  @  |  @  |  | `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8p1_4090d/exp/visual_stable_v8p1_task1_R2stableStrong_seed2` |

## Interpretation

- task2 completed: v8.1 strong mitigated collapse but did not fully solve it.
- task4 was already completed in the legacy v8p1 task4 directory and was not rerun.
- task1 is the only newly launched run in this step.
- ordinary visual matched v7 was not continued.

## Trajectories

### task2

`1:0; 100000:0.5; 200000:0.62; 300000:0.74; 400000:0.56; 500000:0.48; 600000:0.56; 700000:0.38; 800000:0.3; 900000:0.1; 1000000:0.4`

### task4

`1:0; 100000:0.82; 200000:0.24; 300000:0.48; 400000:0.58; 500000:0.44; 600000:0.4; 700000:0.34; 800000:0.24; 900000:0.46; 1000000:0.34`

### task1

``


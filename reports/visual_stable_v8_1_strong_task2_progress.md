# Visual Stable v8.1 Strong Task2 Progress

Generated: 2026-06-19T01:39:01

- env: `visual-antmaze-medium-navigate-singletask-task2-v0`
- config: `R2_stable_strong`
- seed: 2
- status: COMPLETED
- final/current step: 1000000
- final/current success: 0.4
- best success: 0.74 @ 300000
- peak_after_500k: 0.56 @ 600000
- drop_from_best: -0.33999999999999997
- final/best ratio: 0.5405405405405406

## Trajectory

| step | success | return | length |
|---:|---:|---:|---:|
| 0 | 0.0 | -1000.0 | 1000.0 |
| 100k | 0.5 | -790.54 | 791.04 |
| 200k | 0.62 | -671.34 | 671.96 |
| 300k | 0.74 | -644.94 | 645.68 |
| 400k | 0.56 | -715.56 | 716.12 |
| 500k | 0.48 | -794.28 | 794.76 |
| 600k | 0.56 | -712.2 | 712.76 |
| 700k | 0.38 | -865.16 | 865.54 |
| 800k | 0.3 | -867.84 | 868.14 |
| 900k | 0.1 | -958.02 | 958.12 |
| 1M | 0.4 | -848.28 | 848.68 |

## Stable Diagnostics Latest Train Row

- `training/stable/actor_lr`: 9.000001e-06
- `training/stable/critic_lr`: 3.0000001e-05
- `training/stable/encoder_frozen`: 1.0
- `training/actor/actor_anchor_loss`: 0.24015187
- `training/actor/actor_anchor_gate`: 1.0
- `training/critic/stable/sb_weight_mean`: 0.24999976
- `training/critic/stable/sb_weight_std`: 0.12893221
- `training/critic/stable/sb_weight_max`: 0.53121877
- `training/critic/stable/sb_weight_top10_mass`: 0.99999905
- `training/critic/pm/reliability_mean`: 8213.863
- `training/critic/pm/reliability_std`: 68636.09
- `training/critic/pm/flow_residual_mean`: 705.49664
- `training/critic/pm/flow_residual_std`: 745.9846
- `training/critic/pm/disagree_mean`: 0.3514269
- `training/critic/pm/disagree_std`: 0.93861437
- `training/visual_stable/actor_lr_mult`: 0.030000001
- `training/visual_stable/critic_lr_mult`: 0.1
- `training/visual_stable/target_tau`: 0.005

## CSV Paths

- eval: `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_1_strong_4090d/exp/visual_medium_task2_R2_stable_strong_seed2_1m/visual_medium_task2_R2_stable_strong_seed2_1m/sd002_20260617_230839/eval.csv`
- train: `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_1_strong_4090d/exp/visual_medium_task2_R2_stable_strong_seed2_1m/visual_medium_task2_R2_stable_strong_seed2_1m/sd002_20260617_230839/train.csv`

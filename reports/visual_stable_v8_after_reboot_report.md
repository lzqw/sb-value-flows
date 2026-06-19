# Visual Stable v8 After Reboot Report

Generated: 2026-06-19 10:51:01

## Environment

- main.py running now: no
- GPU state:
```
0, 0, 0
1, 0, 0
```

## Interpretation Rules

Final result is the last eval.csv row only. Best/peak/checkpoints are diagnostics only. Smoke and partial/interrupted runs are not formal positives.

## Comparison

- v7 task2 / R2: best 0.82 @200k -> final 0.02 @1M.
- v8 task2 / R2_stable: final 0.26 @1M, best 0.74 @100k, peak_after_500k 0.56 @500k, drop -0.48.
- v8.1 task2 / R2_stable_strong: see table below.

## Runs

| config | kind | status | final_step | final | best | peak_after_500k | drop | ckpts | eval_csv |
|---|---|---|---:|---:|---|---|---:|---:|---|
| R2_stable_strong | formal | COMPLETED | 1000000 | 0.4 | 0.74@300000 | 0.56@600000 | -0.33999999999999997 | 16 | `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_1_strong_4090d/exp/visual_medium_task2_R2_stable_strong_seed2_1m/visual_medium_task2_R2_stable_strong_seed2_1m/sd002_20260617_230839/eval.csv` |
| R2_stable | formal | COMPLETED | 1000000 | 0.26 | 0.74@100000 | 0.56@500000 | -0.48 | 14 | `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_task2_diagnostic/exp/visual_stable_v8_task2_R2_stable_seed2_1m/visual_stable_v8_task2_R2_stable_seed2_1m/sd002_20260616_162650/eval.csv` |
| R2_stable_strong | smoke | SMOKE_COMPLETED | 1000 | 0.0 | 0.0@1 | @ | 0.0 | 5 | `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_1_strong_4090d/exp/smoke_visual_medium_task2_R2_stable_strong_seed2_1000/smoke_visual_medium_task2_R2_stable_strong_seed2_1000/sd002_20260617_230334/eval.csv` |

## v8.1 Strong Full Trajectory

- trajectory: `1:0; 100000:0.5; 200000:0.62; 300000:0.74; 400000:0.56; 500000:0.48; 600000:0.56; 700000:0.38; 800000:0.3; 900000:0.1; 1000000:0.4`
- latest stable diagnostics: `{"training/critic/pm/disagree_mean": "0.3514269", "training/critic/pm/disagree_std": "0.93861437", "training/critic/pm/flow_residual_mean": "705.49664", "training/critic/pm/flow_residual_std": "745.9846", "training/critic/pm/reliability_mean": "8213.863", "training/critic/pm/reliability_std": "68636.09", "training/critic/stable/sb_weight_max": "0.53121877", "training/critic/stable/sb_weight_mean": "0.24999976", "training/critic/stable/sb_weight_std": "0.12893221", "training/critic/stable/sb_weight_top10_mass": "0.99999905", "training/stable/actor_lr": "9.000001e-06", "training/stable/critic_lr": "3.0000001e-05", "training/stable/encoder_frozen": "1.0", "training/visual_stable/actor_lr_mult": "0.030000001", "training/visual_stable/critic_lr_mult": "0.1", "training/visual_stable/target_tau": "0.005", "validation/critic/pm/disagree_mean": "5.978641", "validation/critic/pm/disagree_std": "38.20172", "validation/critic/pm/flow_residual_mean": "558.69196", "validation/critic/pm/flow_residual_std": "637.512", "validation/critic/pm/reliability_mean": "13536.457", "validation/critic/pm/reliability_std": "170750.72", "validation/critic/stable/sb_weight_max": "0.52830464", "validation/critic/stable/sb_weight_mean": "0.24999976", "validation/critic/stable/sb_weight_std": "0.13594656", "validation/critic/stable/sb_weight_top10_mass": "0.99999905", "validation/stable/actor_lr": "0.0003", "validation/stable/critic_lr": "0.0003", "validation/stable/encoder_frozen": "0.0", "validation/visual_stable/actor_lr_mult": "1.0", "validation/visual_stable/critic_lr_mult": "1.0"}`
- latest checkpoint: `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_1_strong_4090d/exp/visual_medium_task2_R2_stable_strong_seed2_1m/visual_medium_task2_R2_stable_strong_seed2_1m/sd002_20260617_230839/checkpoints/final/params_1000000.pkl`
- resume decision: completed before reboot; no restart needed.

## Decision

The v8.1 strong task2 formal run is completed if final_step >= 980000. If completed, do not resume or rerun.

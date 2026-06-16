# Visual v7 Interrupted Trajectory Report

Focus: visual_matched_4090d_v7. Final values use the last row only; peaks diagnose training collapse.

- v7 eval.csv files: 10
- completed: 6
- partial/interrupted: 4

## Summary Table

| env | config | seed | final_step | status | success_final | success_best | best_step | drop_from_best | success_peak_after_500k | peak_step_after_500k |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| visual-antmaze-medium-navigate-singletask-task1-v0 | R2_flow_residual_disagree_std_lam0p001 | 2 | 200000 | PARTIAL_OR_INTERRUPTED | 0.8 | 0.8 | 200000 | 0 |  |  |
| visual-antmaze-medium-navigate-singletask-task1-v0 | R2_flow_residual_disagree_std_lam0p001 | 2 | 1000000 | COMPLETED | 0.2 | 0.78 | 200000 | -0.58 | 0.5 | 500000 |
| visual-antmaze-medium-navigate-singletask-task2-v0 | R2_flow_residual_disagree_std_lam0p001 | 2 | 200000 | PARTIAL_OR_INTERRUPTED | 0.48 | 0.48 | 200000 | 0 |  |  |
| visual-antmaze-medium-navigate-singletask-task2-v0 | R2_flow_residual_disagree_std_lam0p001 | 2 | 1000000 | COMPLETED | 0.02 | 0.82 | 200000 | -0.8 | 0.24 | 700000 |
| visual-antmaze-medium-navigate-singletask-task3-v0 | R2_flow_residual_disagree_std_lam0p001 | 2 | 1000000 | COMPLETED | 0.32 | 0.8 | 100000 | -0.48 | 0.58 | 500000 |
| visual-antmaze-medium-navigate-singletask-task4-v0 | R2_flow_residual_disagree_std_lam0p001 | 2 | 1000000 | COMPLETED | 0.4 | 0.86 | 100000 | -0.46 | 0.4 | 1000000 |
| visual-antmaze-medium-navigate-singletask-task5-v0 | R2_flow_residual_disagree_std_lam0p001 | 2 | 1000000 | COMPLETED | 0.12 | 0.7 | 300000 | -0.58 | 0.3 | 600000 |
| visual-antmaze-teleport-navigate-singletask-task1-v0 | A1_action_std_lam0p001 | 2 | 1000000 | COMPLETED | 0.06 | 0.16 | 200000 | -0.1 | 0.06 | 1000000 |
| visual-antmaze-teleport-navigate-singletask-task2-v0 | A1_action_std_lam0p001 | 2 | 400000 | PARTIAL_OR_INTERRUPTED | 0.14 | 0.14 | 400000 | 0 |  |  |
| visual-antmaze-teleport-navigate-singletask-task3-v0 | A1_action_std_lam0p001 | 2 | 400000 | PARTIAL_OR_INTERRUPTED | 0.3 | 0.32 | 100000 | -0.02 |  |  |

## Trajectories

### visual-antmaze-medium-navigate-singletask-task1-v0 / R2_flow_residual_disagree_std_lam0p001 / seed 2 / PARTIAL_OR_INTERRUPTED

- final_step: 200000
- success_final: 0.8
- success_best: 0.8 @ 200000
- drop_from_best: 0
- peak_after_500k:  @ 
- trajectory: `0:0 -> 100k:0.58 -> 200k:0.8`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/visual_matched_4090d_v7/exp/domain_visual-antmaze-medium-navigate_visual-antmaze-medium-navigate-singletask-task1-v0_R2_flow_residual_disagree_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/domain_visual-antmaze-medium-navigate_visual-antmaze-medium-navigate-singletask-task1-v0_R2_flow_residual_disagree_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/sd002_20260611_205229/eval.csv`

### visual-antmaze-medium-navigate-singletask-task1-v0 / R2_flow_residual_disagree_std_lam0p001 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.2
- success_best: 0.78 @ 200000
- drop_from_best: -0.58
- peak_after_500k: 0.5 @ 500000
- trajectory: `0:0 -> 100k:0.74 -> 200k:0.78 -> 300k:0.68 -> 400k:0.54 -> 500k:0.5 -> 600k:0.24 -> 700k:0.3 -> 800k:0.16 -> 900k:0.24 -> 1M:0.2`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/visual_matched_4090d_v7/exp/domain_visual-antmaze-medium-navigate_visual-antmaze-medium-navigate-singletask-task1-v0_R2_flow_residual_disagree_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/domain_visual-antmaze-medium-navigate_visual-antmaze-medium-navigate-singletask-task1-v0_R2_flow_residual_disagree_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/sd002_20260612_092355/eval.csv`

### visual-antmaze-medium-navigate-singletask-task2-v0 / R2_flow_residual_disagree_std_lam0p001 / seed 2 / PARTIAL_OR_INTERRUPTED

- final_step: 200000
- success_final: 0.48
- success_best: 0.48 @ 200000
- drop_from_best: 0
- peak_after_500k:  @ 
- trajectory: `0:0 -> 100k:0.22 -> 200k:0.48`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/visual_matched_4090d_v7/exp/domain_visual-antmaze-medium-navigate_visual-antmaze-medium-navigate-singletask-task2-v0_R2_flow_residual_disagree_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/domain_visual-antmaze-medium-navigate_visual-antmaze-medium-navigate-singletask-task2-v0_R2_flow_residual_disagree_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/sd002_20260611_205229/eval.csv`

### visual-antmaze-medium-navigate-singletask-task2-v0 / R2_flow_residual_disagree_std_lam0p001 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.02
- success_best: 0.82 @ 200000
- drop_from_best: -0.8
- peak_after_500k: 0.24 @ 700000
- trajectory: `0:0 -> 100k:0.48 -> 200k:0.82 -> 300k:0.6 -> 400k:0.22 -> 500k:0.2 -> 600k:0.18 -> 700k:0.24 -> 800k:0.18 -> 900k:0.06 -> 1M:0.02`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/visual_matched_4090d_v7/exp/domain_visual-antmaze-medium-navigate_visual-antmaze-medium-navigate-singletask-task2-v0_R2_flow_residual_disagree_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/domain_visual-antmaze-medium-navigate_visual-antmaze-medium-navigate-singletask-task2-v0_R2_flow_residual_disagree_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/sd002_20260612_092355/eval.csv`

### visual-antmaze-medium-navigate-singletask-task3-v0 / R2_flow_residual_disagree_std_lam0p001 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.32
- success_best: 0.8 @ 100000
- drop_from_best: -0.48
- peak_after_500k: 0.58 @ 500000
- trajectory: `0:0 -> 100k:0.8 -> 200k:0.76 -> 300k:0.6 -> 400k:0.52 -> 500k:0.58 -> 600k:0.56 -> 700k:0.52 -> 800k:0.36 -> 900k:0.46 -> 1M:0.32`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/visual_matched_4090d_v7/exp/domain_visual-antmaze-medium-navigate_visual-antmaze-medium-navigate-singletask-task3-v0_R2_flow_residual_disagree_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/domain_visual-antmaze-medium-navigate_visual-antmaze-medium-navigate-singletask-task3-v0_R2_flow_residual_disagree_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/sd002_20260613_115731/eval.csv`

### visual-antmaze-medium-navigate-singletask-task4-v0 / R2_flow_residual_disagree_std_lam0p001 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.4
- success_best: 0.86 @ 100000
- drop_from_best: -0.46
- peak_after_500k: 0.4 @ 1000000
- trajectory: `0:0 -> 100k:0.86 -> 200k:0.84 -> 300k:0.66 -> 400k:0.36 -> 500k:0.38 -> 600k:0.22 -> 700k:0.3 -> 800k:0.22 -> 900k:0.22 -> 1M:0.4`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/visual_matched_4090d_v7/exp/domain_visual-antmaze-medium-navigate_visual-antmaze-medium-navigate-singletask-task4-v0_R2_flow_residual_disagree_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/domain_visual-antmaze-medium-navigate_visual-antmaze-medium-navigate-singletask-task4-v0_R2_flow_residual_disagree_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/sd002_20260613_115731/eval.csv`

### visual-antmaze-medium-navigate-singletask-task5-v0 / R2_flow_residual_disagree_std_lam0p001 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.12
- success_best: 0.7 @ 300000
- drop_from_best: -0.58
- peak_after_500k: 0.3 @ 600000
- trajectory: `0:0 -> 100k:0.26 -> 200k:0.4 -> 300k:0.7 -> 400k:0.46 -> 500k:0.2 -> 600k:0.3 -> 700k:0.12 -> 800k:0.18 -> 900k:0.22 -> 1M:0.12`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/visual_matched_4090d_v7/exp/domain_visual-antmaze-medium-navigate_visual-antmaze-medium-navigate-singletask-task5-v0_R2_flow_residual_disagree_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/domain_visual-antmaze-medium-navigate_visual-antmaze-medium-navigate-singletask-task5-v0_R2_flow_residual_disagree_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/sd002_20260614_143015/eval.csv`

### visual-antmaze-teleport-navigate-singletask-task1-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.06
- success_best: 0.16 @ 200000
- drop_from_best: -0.1
- peak_after_500k: 0.06 @ 1000000
- trajectory: `0:0 -> 100k:0.1 -> 200k:0.16 -> 300k:0.06 -> 400k:0.1 -> 500k:0.04 -> 600k:0.04 -> 700k:0.04 -> 800k:0 -> 900k:0 -> 1M:0.06`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/visual_matched_4090d_v7/exp/domain_visual-antmaze-teleport-navigate_visual-antmaze-teleport-navigate-singletask-task1-v0_A1_action_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/domain_visual-antmaze-teleport-navigate_visual-antmaze-teleport-navigate-singletask-task1-v0_A1_action_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/sd002_20260614_143015/eval.csv`

### visual-antmaze-teleport-navigate-singletask-task2-v0 / A1_action_std_lam0p001 / seed 2 / PARTIAL_OR_INTERRUPTED

- final_step: 400000
- success_final: 0.14
- success_best: 0.14 @ 400000
- drop_from_best: 0
- peak_after_500k:  @ 
- trajectory: `0:0 -> 100k:0.08 -> 200k:0.08 -> 300k:0.12 -> 400k:0.14`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/visual_matched_4090d_v7/exp/domain_visual-antmaze-teleport-navigate_visual-antmaze-teleport-navigate-singletask-task2-v0_A1_action_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/domain_visual-antmaze-teleport-navigate_visual-antmaze-teleport-navigate-singletask-task2-v0_A1_action_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/sd002_20260615_170130/eval.csv`

### visual-antmaze-teleport-navigate-singletask-task3-v0 / A1_action_std_lam0p001 / seed 2 / PARTIAL_OR_INTERRUPTED

- final_step: 400000
- success_final: 0.3
- success_best: 0.32 @ 100000
- drop_from_best: -0.02
- peak_after_500k:  @ 
- trajectory: `0:0 -> 100k:0.32 -> 200k:0.28 -> 300k:0.32 -> 400k:0.3`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/visual_matched_4090d_v7/exp/domain_visual-antmaze-teleport-navigate_visual-antmaze-teleport-navigate-singletask-task3-v0_A1_action_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/domain_visual-antmaze-teleport-navigate_visual-antmaze-teleport-navigate-singletask-task3-v0_A1_action_std_lam0p001_seed2_1m_paper_like_b256_s16_f10/sd002_20260615_170130/eval.csv`


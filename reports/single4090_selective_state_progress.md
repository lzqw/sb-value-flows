# Single4090 Selective State Progress

Generated: 2026-06-17T01:44:48

Final values use the last eval.csv row only. Best values are diagnostics and do not replace final success.

## Overall

- runs found: 22
- completed: 21
- interrupted: 1
- failed: 0

## Completed Runs

| env | config | seed | final_step | final | best | VF baseline | exceeds VF | collapse diagnostic |
|---|---|---:|---:|---:|---:|---:|---|---|
| puzzle-3x3-play-singletask-task5-v0 | A1_action_std_lam0p001 | 2 | 300000 | 0.4 | 0.4 | 0.58 | False | False |
| puzzle-3x3-play-singletask-task5-v0 | A2_action_std_lam0p003 | 2 | 300000 | 0.1 | 0.1 | 0.58 | False | False |
| puzzle-3x3-play-singletask-task5-v0 | MinimalSB_lam0p001 | 2 | 300000 | 0 | 0.1 | 0.58 | False | False |
| puzzle-3x3-play-singletask-task5-v0 | MinimalSB_lam0p003 | 2 | 300000 | 0.2 | 0.2 | 0.58 | False | False |
| puzzle-3x3-play-singletask-task5-v0 | P0_particle | 2 | 300000 | 0 | 0 | 0.58 | False | False |
| puzzle-3x3-play-singletask-task5-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 0 | 0 | 0.58 | False | False |
| puzzle-3x3-play-singletask-task5-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 0.3 | 0.4 | 0.58 | False | False |
| puzzle-4x4-play-singletask-task1-v0 | A1_action_std_lam0p001 | 2 | 300000 | 0.4 | 0.4 | 0.36 | True | False |
| puzzle-4x4-play-singletask-task1-v0 | A2_action_std_lam0p003 | 2 | 300000 | 0.5 | 0.5 | 0.36 | True | False |
| puzzle-4x4-play-singletask-task1-v0 | MinimalSB_lam0p001 | 2 | 300000 | 0.3 | 0.4 | 0.36 | False | False |
| puzzle-4x4-play-singletask-task1-v0 | MinimalSB_lam0p003 | 2 | 300000 | 0.3 | 0.4 | 0.36 | False | False |
| puzzle-4x4-play-singletask-task1-v0 | P0_particle | 2 | 300000 | 0.5 | 0.5 | 0.36 | True | False |
| puzzle-4x4-play-singletask-task1-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 0.2 | 0.5 | 0.36 | False | True |
| puzzle-4x4-play-singletask-task1-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 0.3 | 0.4 | 0.36 | False | False |
| puzzle-4x4-play-singletask-task3-v0 | A1_action_std_lam0p001 | 2 | 300000 | 0.4 | 0.4 | 0.3 | True | False |
| puzzle-4x4-play-singletask-task3-v0 | A2_action_std_lam0p003 | 2 | 300000 | 0.3 | 0.7 | 0.3 | True | True |
| puzzle-4x4-play-singletask-task3-v0 | MinimalSB_lam0p001 | 2 | 300000 | 0.3 | 0.4 | 0.3 | True | False |
| puzzle-4x4-play-singletask-task3-v0 | MinimalSB_lam0p003 | 2 | 300000 | 0.1 | 0.4 | 0.3 | False | True |
| puzzle-4x4-play-singletask-task3-v0 | P0_particle | 2 | 300000 | 0.2 | 0.6 | 0.3 | False | True |
| puzzle-4x4-play-singletask-task3-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 0.5 | 0.8 | 0.3 | True | True |
| puzzle-4x4-play-singletask-task3-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 0.1 | 0.3 | 0.3 | False | False |

## Partial / Interrupted Runs

| env | config | seed | final_step | final | best | eval_csv |
|---|---|---:|---:|---:|---:|---|
| puzzle-4x4-play-singletask-task3-v0 | MinimalSB_lam0p001 | 2 | 100000 | 0 | 0 | `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task3_MinimalSB_lam0p001_seed2/sd002_20260616_034310/eval.csv` |

## Full Trajectories

### puzzle-3x3-play-singletask-task5-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.4
- success_best: 0.4 @ 300000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0.1 -> 300000:0.4`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_3x3_task5_A1_action_std_lam0p001_seed2/sd002_20260616_204333/eval.csv`

### puzzle-3x3-play-singletask-task5-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 300000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_3x3_task5_A2_action_std_lam0p003_seed2/sd002_20260616_215841/eval.csv`

### puzzle-3x3-play-singletask-task5-v0 / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.1 @ 150000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_3x3_task5_MinimalSB_lam0p001_seed2/sd002_20260616_192833/eval.csv`

### puzzle-3x3-play-singletask-task5-v0 / MinimalSB_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.2 @ 300000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0.2`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_3x3_task5_MinimalSB_lam0p003_seed2/sd002_20260616_181326/eval.csv`

### puzzle-3x3-play-singletask-task5-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0 @ 1
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_3x3_task5_P0_particle_seed2/sd002_20260616_165821/eval.csv`

### puzzle-3x3-play-singletask-task5-v0 / R2_residual_disagree_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0 @ 1
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_3x3_task5_R2_residual_disagree_lam0p001_seed2/sd002_20260616_231347/eval.csv`

### puzzle-3x3-play-singletask-task5-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.4 @ 200000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.4 -> 250000:0.3 -> 300000:0.3`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_3x3_task5_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260617_002927/eval.csv`

### puzzle-4x4-play-singletask-task1-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.4
- success_best: 0.4 @ 250000
- trajectory: `1:0 -> 50000:0 -> 100000:0.1 -> 150000:0.3 -> 200000:0.3 -> 250000:0.4 -> 300000:0.4`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task1_A1_action_std_lam0p001_seed2/sd002_20260615_201119/eval.csv`

### puzzle-4x4-play-singletask-task1-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.5
- success_best: 0.5 @ 300000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.3 -> 250000:0.4 -> 300000:0.5`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task1_A2_action_std_lam0p003_seed2/sd002_20260615_212615/eval.csv`

### puzzle-4x4-play-singletask-task1-v0 / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.4 @ 150000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.4 -> 200000:0.3 -> 250000:0.2 -> 300000:0.3`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task1_MinimalSB_lam0p001_seed2/sd002_20260615_185554/eval.csv`

### puzzle-4x4-play-singletask-task1-v0 / MinimalSB_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.4 @ 200000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.3 -> 200000:0.4 -> 250000:0.3 -> 300000:0.3`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task1_MinimalSB_lam0p003_seed2/sd002_20260615_174043/eval.csv`

### puzzle-4x4-play-singletask-task1-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.5
- success_best: 0.5 @ 300000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0.2 -> 250000:0.4 -> 300000:0.5`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task1_P0_particle_seed2/sd002_20260615_162552/eval.csv`

### puzzle-4x4-play-singletask-task1-v0 / R2_residual_disagree_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.5 @ 250000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.3 -> 250000:0.5 -> 300000:0.2`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task1_R2_residual_disagree_lam0p001_seed2/sd002_20260615_224116/eval.csv`

### puzzle-4x4-play-singletask-task1-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.4 @ 200000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.4 -> 250000:0.3 -> 300000:0.3`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task1_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260615_235715/eval.csv`

### puzzle-4x4-play-singletask-task3-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.4
- success_best: 0.4 @ 300000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.1 -> 250000:0.3 -> 300000:0.4`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task3_A1_action_std_lam0p001_seed2/sd002_20260616_115218/eval.csv`

### puzzle-4x4-play-singletask-task3-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.7 @ 250000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0.5 -> 250000:0.7 -> 300000:0.3`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task3_A2_action_std_lam0p003_seed2/sd002_20260616_130825/eval.csv`

### puzzle-4x4-play-singletask-task3-v0 / MinimalSB_lam0p001 / seed 2 / INTERRUPTED

- final_step: 100000
- success_final: 0
- success_best: 0 @ 1
- trajectory: `1:0 -> 50000:0 -> 100000:0`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task3_MinimalSB_lam0p001_seed2/sd002_20260616_034310/eval.csv`

### puzzle-4x4-play-singletask-task3-v0 / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.4 @ 200000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.4 -> 250000:0.4 -> 300000:0.3`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task3_MinimalSB_lam0p001_seed2/sd002_20260616_103625/eval.csv`

### puzzle-4x4-play-singletask-task3-v0 / MinimalSB_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.4 @ 250000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0.2 -> 250000:0.4 -> 300000:0.1`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task3_MinimalSB_lam0p003_seed2/sd002_20260616_022811/eval.csv`

### puzzle-4x4-play-singletask-task3-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.6 @ 200000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.4 -> 200000:0.6 -> 250000:0.3 -> 300000:0.2`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task3_P0_particle_seed2/sd002_20260616_011303/eval.csv`

### puzzle-4x4-play-singletask-task3-v0 / R2_residual_disagree_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.5
- success_best: 0.8 @ 250000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0.6 -> 250000:0.8 -> 300000:0.5`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task3_R2_residual_disagree_lam0p001_seed2/sd002_20260616_142426/eval.csv`

### puzzle-4x4-play-singletask-task3-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.3 @ 200000
- trajectory: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0.3 -> 250000:0.3 -> 300000:0.1`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task3_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260616_154111/eval.csv`


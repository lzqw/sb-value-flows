# Single4090 Interrupted Run Summary

This report summarizes single4090 state-based eval.csv files from the beginning of the tracked runs through the interruption point. Final values use the last eval.csv row only. Peak values are diagnostic only and are not used as final results.

## Overall

- Total eval.csv: 176
- COMPLETED: 173
- PARTIAL: 2
- INTERRUPTED: 1
- FAILED: 0
- Generated at: 2026-06-16T09:36:05
- No training was launched by this summary job.

## By Source Family

| source_family | eval_csv |
|---|---|
| actorgeo | 3 |
| bad_task_repair_single4090 | 79 |
| bestseed | 5 |
| fullsafe | 3 |
| minimal | 18 |
| puzzle3x3 | 1 |
| puzzle4x4 | 26 |
| reliability | 10 |
| selective_state_tuning_single4090 | 10 |
| table3 | 21 |

## Selective Tuning Runs Before Interruption

| env | config | seed | target_steps | final_step | status | success_final | success_best | best_step | trajectory_full |
|---|---|---|---|---|---|---|---|---|---|
| puzzle-4x4-play-singletask-task1-v0 | A1_action_std_lam0p001 | 2 | 300000 | 300000 | COMPLETED | 0.4 | 0.4 | 250000 | 1:0 -> 50000:0 -> 100000:0.1 -> 150000:0.3 -> 200000:0.3 -> 250000:0.4 -> 300000:0.4 |
| puzzle-4x4-play-singletask-task1-v0 | A2_action_std_lam0p003 | 2 | 300000 | 300000 | COMPLETED | 0.5 | 0.5 | 300000 | 1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.3 -> 250000:0.4 -> 300000:0.5 |
| puzzle-4x4-play-singletask-task1-v0 | MinimalSB_lam0p001 | 2 | 300000 | 300000 | COMPLETED | 0.3 | 0.4 | 150000 | 1:0 -> 50000:0 -> 100000:0 -> 150000:0.4 -> 200000:0.3 -> 250000:0.2 -> 300000:0.3 |
| puzzle-4x4-play-singletask-task1-v0 | MinimalSB_lam0p003 | 2 | 300000 | 300000 | COMPLETED | 0.3 | 0.4 | 200000 | 1:0 -> 50000:0 -> 100000:0 -> 150000:0.3 -> 200000:0.4 -> 250000:0.3 -> 300000:0.3 |
| puzzle-4x4-play-singletask-task1-v0 | P0_particle | 2 | 300000 | 300000 | COMPLETED | 0.5 | 0.5 | 300000 | 1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0.2 -> 250000:0.4 -> 300000:0.5 |
| puzzle-4x4-play-singletask-task1-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 300000 | COMPLETED | 0.2 | 0.5 | 250000 | 1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.3 -> 250000:0.5 -> 300000:0.2 |
| puzzle-4x4-play-singletask-task1-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 300000 | COMPLETED | 0.3 | 0.4 | 200000 | 1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.4 -> 250000:0.3 -> 300000:0.3 |
| puzzle-4x4-play-singletask-task3-v0 | MinimalSB_lam0p001 | 2 | 300000 | 100000 | INTERRUPTED | 0 | 0 | 1 | 1:0 -> 50000:0 -> 100000:0 |
| puzzle-4x4-play-singletask-task3-v0 | MinimalSB_lam0p003 | 2 | 300000 | 300000 | COMPLETED | 0.1 | 0.4 | 250000 | 1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0.2 -> 250000:0.4 -> 300000:0.1 |
| puzzle-4x4-play-singletask-task3-v0 | P0_particle | 2 | 300000 | 300000 | COMPLETED | 0.2 | 0.6 | 200000 | 1:0 -> 50000:0 -> 100000:0 -> 150000:0.4 -> 200000:0.6 -> 250000:0.3 -> 300000:0.2 |

## Interrupted Runs

| env | config | seed | target_steps | final_step | status | success_final | success_best | eval_csv |
|---|---|---|---|---|---|---|---|---|
| puzzle-4x4-play-singletask-task3-v0 | MinimalSB_lam0p001 | 2 | 300000 | 100000 | INTERRUPTED | 0 | 0 | /root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task3_MinimalSB_lam0p001_seed2/sd002_20260616_034310/eval.csv |

## Completed Run Finals

| source_family | env | config | seed | target_steps | final_step | success_final | success_best | best_step |
|---|---|---|---|---|---|---|---|---|
| actorgeo | UNKNOWN | ActorGeo | 0 | 1000000 | 1000000 | 0.1 | 0.4 | 650000 |
| actorgeo | UNKNOWN | ActorGeo | 1 | 1000000 | 1000000 | 0 | 0.3 | 100000 |
| actorgeo | UNKNOWN | ActorGeo | 2 | 1000000 | 1000000 | 0.1 | 0.3 | 250000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task2-v0 | A1_action_std_lam0p001 | 2 | 300000 | 300000 | 0.1 | 0.1 | 250000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task2-v0 | A2_action_std_lam0p003 | 2 | 300000 | 300000 | 0.3 | 0.3 | 300000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task2-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 300000 | 0.3 | 0.3 | 300000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task2-v0 | MinimalSB_lam0p001 | 2 | 300000 | 300000 | 0.3 | 0.3 | 300000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task2-v0 | P0_particle | 2 | 300000 | 300000 | 0.2 | 0.2 | 300000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task2-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 300000 | 0.2 | 0.2 | 250000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task2-v0 | R3_residual_disagree_typicality_lam0p001 | 0 | 1000000 | 1000000 | 0.7 | 0.9 | 450000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task2-v0 | R3_residual_disagree_typicality_lam0p001 | 1 | 1000000 | 1000000 | 0.9 | 0.9 | 650000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task2-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 300000 | 0.4 | 0.4 | 300000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task2-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 1000000 | 1000000 | 0.9 | 0.9 | 1000000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task3-v0 | A1_action_std_lam0p001 | 2 | 300000 | 300000 | 0.4 | 0.4 | 300000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task3-v0 | A2_action_std_lam0p003 | 0 | 1000000 | 1000000 | 0.8 | 1 | 700000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task3-v0 | A2_action_std_lam0p003 | 1 | 1000000 | 1000000 | 0.8 | 1 | 800000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task3-v0 | A2_action_std_lam0p003 | 2 | 300000 | 300000 | 0.5 | 0.5 | 300000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task3-v0 | A2_action_std_lam0p003 | 2 | 1000000 | 1000000 | 0.9 | 1 | 900000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task3-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 300000 | 0.4 | 0.4 | 300000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task3-v0 | MinimalSB_lam0p001 | 2 | 300000 | 300000 | 0.4 | 0.4 | 300000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task3-v0 | P0_particle | 2 | 300000 | 300000 | 0.1 | 0.2 | 250000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task3-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 300000 | 0.3 | 0.3 | 200000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task3-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 300000 | 0.2 | 0.2 | 300000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task4-v0 | A1_action_std_lam0p001 | 0 | 1000000 | 1000000 | 0.4 | 0.5 | 500000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task4-v0 | A1_action_std_lam0p001 | 1 | 1000000 | 1000000 | 0.3 | 0.4 | 650000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task4-v0 | A1_action_std_lam0p001 | 2 | 300000 | 300000 | 0.3 | 0.3 | 300000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task4-v0 | A1_action_std_lam0p001 | 2 | 1000000 | 1000000 | 0.5 | 0.7 | 800000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task4-v0 | A2_action_std_lam0p003 | 2 | 300000 | 300000 | 0.2 | 0.2 | 300000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task4-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 300000 | 0 | 0 | 1 |
| bad_task_repair_single4090 | cube-double-play-singletask-task4-v0 | MinimalSB_lam0p001 | 2 | 300000 | 300000 | 0.1 | 0.1 | 300000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task4-v0 | P0_particle | 2 | 300000 | 300000 | 0.1 | 0.1 | 150000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task4-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 300000 | 0.1 | 0.1 | 200000 |
| bad_task_repair_single4090 | cube-double-play-singletask-task4-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 300000 | 0.1 | 0.1 | 300000 |
| bad_task_repair_single4090 | cube-triple-play-singletask-task3-v0 | A1_action_std_lam0p001 | 2 | 300000 | 300000 | 0.1 | 0.1 | 300000 |
| bad_task_repair_single4090 | cube-triple-play-singletask-task3-v0 | A2_action_std_lam0p003 | 2 | 300000 | 300000 | 0 | 0 | 1 |
| bad_task_repair_single4090 | cube-triple-play-singletask-task3-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 300000 | 0 | 0 | 1 |
| bad_task_repair_single4090 | cube-triple-play-singletask-task3-v0 | MinimalSB_lam0p001 | 2 | 300000 | 300000 | 0 | 0 | 1 |
| bad_task_repair_single4090 | cube-triple-play-singletask-task3-v0 | P0_particle | 2 | 300000 | 300000 | 0 | 0 | 1 |
| bad_task_repair_single4090 | cube-triple-play-singletask-task3-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 300000 | 0 | 0 | 1 |
| bad_task_repair_single4090 | cube-triple-play-singletask-task3-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 300000 | 0 | 0 | 1 |
| bad_task_repair_single4090 | puzzle-3x3-play-singletask-task3-v0 | A1_action_std_lam0p001 | 2 | 300000 | 300000 | 0 | 0.1 | 200000 |
| bad_task_repair_single4090 | puzzle-3x3-play-singletask-task3-v0 | A2_action_std_lam0p003 | 2 | 300000 | 300000 | 0.1 | 0.1 | 200000 |
| bad_task_repair_single4090 | puzzle-3x3-play-singletask-task3-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 300000 | 0.1 | 0.2 | 150000 |
| bad_task_repair_single4090 | puzzle-3x3-play-singletask-task3-v0 | MinimalSB_lam0p001 | 2 | 300000 | 300000 | 0 | 0.3 | 150000 |
| bad_task_repair_single4090 | puzzle-3x3-play-singletask-task3-v0 | P0_particle | 2 | 300000 | 300000 | 0.2 | 0.4 | 250000 |
| bad_task_repair_single4090 | puzzle-3x3-play-singletask-task3-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 300000 | 0 | 0.1 | 100000 |
| bad_task_repair_single4090 | puzzle-3x3-play-singletask-task3-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 300000 | 0 | 0 | 1 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task2-v0 | A1_action_std_lam0p001 | 2 | 300000 | 300000 | 0.1 | 0.1 | 300000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task2-v0 | A2_action_std_lam0p003 | 2 | 300000 | 300000 | 0.2 | 0.2 | 300000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task2-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 300000 | 0.1 | 0.4 | 100000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task2-v0 | MinimalSB_lam0p001 | 0 | 1000000 | 1000000 | 0.4 | 0.6 | 950000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task2-v0 | MinimalSB_lam0p001 | 1 | 1000000 | 1000000 | 0.1 | 0.6 | 900000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task2-v0 | MinimalSB_lam0p001 | 2 | 300000 | 300000 | 0.2 | 0.5 | 250000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task2-v0 | MinimalSB_lam0p001 | 2 | 1000000 | 1000000 | 0.5 | 0.5 | 600000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task2-v0 | P0_particle | 2 | 300000 | 300000 | 0 | 0.3 | 250000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task2-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 300000 | 0 | 0 | 1 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task2-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 300000 | 0 | 0.2 | 100000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task4-v0 | A1_action_std_lam0p001 | 2 | 300000 | 300000 | 0.1 | 0.1 | 250000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task4-v0 | A2_action_std_lam0p003 | 2 | 300000 | 300000 | 0.2 | 0.3 | 200000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task4-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 300000 | 0.3 | 0.3 | 300000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task4-v0 | MinimalSB_lam0p001 | 2 | 300000 | 300000 | 0.3 | 0.3 | 300000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task4-v0 | P0_particle | 2 | 300000 | 300000 | 0.1 | 0.5 | 200000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task4-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 300000 | 0.3 | 0.3 | 300000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task4-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 300000 | 0.5 | 0.5 | 300000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task4-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 1000000 | 1000000 | 0.1 | 0.5 | 850000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task5-v0 | A1_action_std_lam0p001 | 2 | 300000 | 300000 | 0 | 0.1 | 200000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task5-v0 | A2_action_std_lam0p003 | 2 | 300000 | 300000 | 0.1 | 0.1 | 200000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task5-v0 | A2_action_std_lam0p003 | 2 | 1000000 | 1000000 | 0 | 0.2 | 250000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task5-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 300000 | 0.1 | 0.1 | 150000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task5-v0 | MinimalSB_lam0p001 | 2 | 300000 | 300000 | 0 | 0.1 | 150000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task5-v0 | P0_particle | 2 | 300000 | 300000 | 0.1 | 0.1 | 200000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task5-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 300000 | 0 | 0.2 | 200000 |
| bad_task_repair_single4090 | puzzle-4x4-play-singletask-task5-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 300000 | 0.1 | 0.2 | 250000 |
| bad_task_repair_single4090 | scene-play-singletask-task4-v0 | A1_action_std_lam0p001 | 2 | 300000 | 300000 | 0 | 0.7 | 150000 |
| bad_task_repair_single4090 | scene-play-singletask-task4-v0 | A2_action_std_lam0p003 | 2 | 300000 | 300000 | 0 | 0.9 | 100000 |
| bad_task_repair_single4090 | scene-play-singletask-task4-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 300000 | 0.2 | 0.8 | 100000 |
| bad_task_repair_single4090 | scene-play-singletask-task4-v0 | MinimalSB_lam0p001 | 2 | 300000 | 300000 | 0.1 | 0.7 | 200000 |
| bad_task_repair_single4090 | scene-play-singletask-task4-v0 | P0_particle | 2 | 300000 | 300000 | 0.4 | 0.6 | 100000 |
| bad_task_repair_single4090 | scene-play-singletask-task4-v0 | P0_particle | 2 | 1000000 | 1000000 | 0 | 0.9 | 100000 |
| bad_task_repair_single4090 | scene-play-singletask-task4-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 300000 | 0.1 | 0.7 | 250000 |
| bad_task_repair_single4090 | scene-play-singletask-task4-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 300000 | 0.2 | 0.8 | 100000 |
| bestseed | UNKNOWN | bestseed | 5 | 1000000 | 1000000 | 1 | 1 | 100000 |
| bestseed | UNKNOWN | bestseed | 5 | 1000000 | 1000000 | 1 | 1 | 400000 |
| bestseed | UNKNOWN | bestseed | 5 | 1000000 | 1000000 | 0.1 | 0.1 | 650000 |
| bestseed | UNKNOWN | bestseed | 5 | 1000000 | 1000000 | 1 | 1 | 850000 |
| bestseed | UNKNOWN | bestseed | 5 | 1000000 | 1000000 | 1 | 1 | 1000000 |
| fullsafe | UNKNOWN | FullSafe | 0 | 1000000 | 1000000 | 0.2 | 0.2 | 350000 |
| fullsafe | UNKNOWN | FullSafe | 1 | 1000000 | 1000000 | 0 | 0.2 | 50000 |
| fullsafe | UNKNOWN | FullSafe | 2 | 1000000 | 1000000 | 0.2 | 0.4 | 800000 |
| minimal | UNKNOWN | MinimalSB_lam0p0003 | 2 | 300000 | 300000 | 0 | 0.1 | 200000 |
| minimal | UNKNOWN | MinimalSB_lam0p001 | 2 | 300000 | 300000 | 0 | 0.2 | 150000 |
| minimal | UNKNOWN | P0_particle | 0 | 1000000 | 1000000 | 0.3 | 0.7 | 850000 |
| minimal | UNKNOWN | P0_particle | 1 | 1000000 | 1000000 | 0.7 | 1 | 850000 |
| minimal | UNKNOWN | P0_particle | 2 | 1000000 | 1000000 | 0.3 | 0.6 | 850000 |
| minimal | UNKNOWN | P0_particle | 3 | 1000000 | 1000000 | 1 | 1 | 850000 |
| minimal | UNKNOWN | P0_particle | 4 | 1000000 | 1000000 | 0 | 0.3 | 200000 |
| minimal | UNKNOWN | P0_particle | 5 | 1000000 | 1000000 | 0 | 0.2 | 750000 |
| minimal | UNKNOWN | P0_particle | 6 | 1000000 | 1000000 | 0.1 | 0.2 | 700000 |
| minimal | UNKNOWN | P0_particle | 7 | 1000000 | 1000000 | 0.5 | 0.5 | 1000000 |
| minimal | UNKNOWN | S1_sb_lam0p001_seed0 | 0 | 1000000 | 1000000 | 0.2 | 0.6 | 700000 |
| minimal | UNKNOWN | S1_sb_lam0p001_seed1 | 1 | 1000000 | 1000000 | 1 | 1 | 850000 |
| minimal | UNKNOWN | S1_sb_lam0p001_seed2 | 2 | 1000000 | 1000000 | 1 | 1 | 900000 |
| minimal | UNKNOWN | S1_sb_lam0p001_seed3 | 3 | 1000000 | 1000000 | 1 | 1 | 800000 |
| minimal | UNKNOWN | S1_sb_lam0p001_seed4 | 4 | 1000000 | 1000000 | 0.2 | 0.6 | 550000 |
| minimal | UNKNOWN | S1_sb_lam0p001_seed5 | 5 | 1000000 | 1000000 | 1 | 1 | 1000000 |
| minimal | UNKNOWN | S1_sb_lam0p001_seed6 | 6 | 1000000 | 1000000 | 0.1 | 0.2 | 350000 |
| minimal | UNKNOWN | S1_sb_lam0p001_seed7 | 7 | 1000000 | 1000000 | 0.2 | 0.2 | 900000 |
| puzzle3x3 | UNKNOWN | screen300k_P0_seed2 | 2 | 300000 | 300000 | 0 | 0.1 | 100000 |
| puzzle4x4 | UNKNOWN | stageA_V0_light_default_seed0 | 0 | 300000 | 300000 | 0.6 | 0.6 | 300000 |
| puzzle4x4 | UNKNOWN | stageA_V1_actor_0p003_seed0 | 0 | 300000 | 300000 | 0.4 | 0.4 | 300000 |
| puzzle4x4 | UNKNOWN | stageA_V2_actor_0p0_seed0 | 0 | 300000 | 300000 | 0.3 | 0.3 | 300000 |
| puzzle4x4 | UNKNOWN | stageA_V3_energy_0p001_seed0 | 0 | 300000 | 300000 | 0.2 | 0.3 | 250000 |
| puzzle4x4 | UNKNOWN | stageA_V4_no_energy_rel_seed0 | 0 | 300000 | 300000 | 0.1 | 0.2 | 200000 |
| puzzle4x4 | UNKNOWN | stageA_V6_temp_0p5_seed0 | 0 | 300000 | 300000 | 0 | 0.2 | 200000 |
| puzzle4x4 | UNKNOWN | stageA_V7_temp_0p1_seed0 | 0 | 300000 | 300000 | 0.2 | 0.5 | 250000 |
| puzzle4x4 | UNKNOWN | stageA_W0_current_seed0 | 0 | 300000 | 300000 | 0.3 | 0.4 | 200000 |
| puzzle4x4 | UNKNOWN | stageA_W1_bcfm1_seed0 | 0 | 300000 | 300000 | 0.2 | 0.2 | 300000 |
| puzzle4x4 | UNKNOWN | stageA_W2_bcfm2_seed0 | 0 | 300000 | 300000 | 0.2 | 0.2 | 300000 |
| puzzle4x4 | UNKNOWN | stageA_W3_bcfm5_seed0 | 0 | 300000 | 300000 | 0 | 0.4 | 250000 |
| puzzle4x4 | UNKNOWN | stageA_W4_temp50_seed0 | 0 | 300000 | 300000 | 0.4 | 0.4 | 200000 |
| puzzle4x4 | UNKNOWN | stageA_W5_temp200_seed0 | 0 | 300000 | 300000 | 0.2 | 0.6 | 250000 |
| puzzle4x4 | UNKNOWN | stageA_W6_qmean_seed0 | 0 | 300000 | 300000 | 0.2 | 0.2 | 300000 |
| puzzle4x4 | UNKNOWN | stageB_V0_light_default_seed0 | 0 | 1000000 | 1000000 | 0.2 | 0.4 | 450000 |
| puzzle4x4 | UNKNOWN | stageB_V0_light_default_seed1 | 1 | 1000000 | 1000000 | 0 | 0.5 | 400000 |
| puzzle4x4 | UNKNOWN | stageB_V0_light_default_seed2 | 2 | 1000000 | 1000000 | 0.3 | 0.3 | 350000 |
| puzzle4x4 | UNKNOWN | stageB_V1_actor_0p003_seed0 | 0 | 1000000 | 1000000 | 0.3 | 0.4 | 450000 |
| puzzle4x4 | UNKNOWN | stageB_V1_actor_0p003_seed1 | 1 | 1000000 | 1000000 | 0.3 | 0.5 | 200000 |
| puzzle4x4 | UNKNOWN | stageB_V1_actor_0p003_seed2 | 2 | 1000000 | 1000000 | 0.1 | 0.6 | 850000 |
| puzzle4x4 | UNKNOWN | stageB_W0_current_seed0 | 0 | 1000000 | 1000000 | 0.1 | 0.4 | 400000 |
| puzzle4x4 | UNKNOWN | stageB_W0_current_seed1 | 1 | 1000000 | 1000000 | 0 | 0.4 | 250000 |
| puzzle4x4 | UNKNOWN | stageB_W0_current_seed2 | 2 | 1000000 | 1000000 | 0.1 | 0.5 | 300000 |
| puzzle4x4 | UNKNOWN | stageB_W4_temp50_seed0 | 0 | 1000000 | 1000000 | 0.1 | 0.5 | 200000 |
| puzzle4x4 | UNKNOWN | stageB_W4_temp50_seed1 | 1 | 1000000 | 1000000 | 0.1 | 0.3 | 450000 |
| puzzle4x4 | UNKNOWN | stageB_W4_temp50_seed2 | 2 | 1000000 | 1000000 | 0.5 | 0.5 | 1000000 |
| reliability | UNKNOWN | A1_action_std_lam0p001 | 0 | 300000 | 300000 | 0.1 | 0.1 | 300000 |
| reliability | UNKNOWN | A2_action_std_lam0p003 | 0 | 300000 | 300000 | 0.1 | 0.1 | 300000 |
| reliability | UNKNOWN | P0_particle | 0 | 300000 | 300000 | 0 | 0 | 1 |
| reliability | UNKNOWN | R2_flow_residual_disagree_std_lam0p001 | 0 | 300000 | 300000 | 0 | 0.1 | 200000 |
| reliability | UNKNOWN | R3_flow_residual_disagree_typicality_std_lam0p001 | 0 | 300000 | 300000 | 0 | 0.1 | 150000 |
| reliability | UNKNOWN | reliability | 0 | 300000 | 300000 | 0.3 | 0.3 | 200000 |
| reliability | UNKNOWN | reliability | 0 | 300000 | 300000 | 0 | 0.1 | 250000 |
| reliability | UNKNOWN | reliability | 0 | 300000 | 300000 | 0 | 0 | 1 |
| reliability | UNKNOWN | reliability | 0 | 300000 | 300000 | 0 | 0.1 | 150000 |
| selective_state_tuning_single4090 | puzzle-4x4-play-singletask-task1-v0 | A1_action_std_lam0p001 | 2 | 300000 | 300000 | 0.4 | 0.4 | 250000 |
| selective_state_tuning_single4090 | puzzle-4x4-play-singletask-task1-v0 | A2_action_std_lam0p003 | 2 | 300000 | 300000 | 0.5 | 0.5 | 300000 |
| selective_state_tuning_single4090 | puzzle-4x4-play-singletask-task1-v0 | MinimalSB_lam0p001 | 2 | 300000 | 300000 | 0.3 | 0.4 | 150000 |
| selective_state_tuning_single4090 | puzzle-4x4-play-singletask-task1-v0 | MinimalSB_lam0p003 | 2 | 300000 | 300000 | 0.3 | 0.4 | 200000 |
| selective_state_tuning_single4090 | puzzle-4x4-play-singletask-task1-v0 | P0_particle | 2 | 300000 | 300000 | 0.5 | 0.5 | 300000 |
| selective_state_tuning_single4090 | puzzle-4x4-play-singletask-task1-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 300000 | 0.2 | 0.5 | 250000 |
| selective_state_tuning_single4090 | puzzle-4x4-play-singletask-task1-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 300000 | 0.3 | 0.4 | 200000 |
| selective_state_tuning_single4090 | puzzle-4x4-play-singletask-task3-v0 | MinimalSB_lam0p003 | 2 | 300000 | 300000 | 0.1 | 0.4 | 250000 |
| selective_state_tuning_single4090 | puzzle-4x4-play-singletask-task3-v0 | P0_particle | 2 | 300000 | 300000 | 0.2 | 0.6 | 200000 |
| table3 | cube-double-play-singletask-task2-v0 | FullSafe | 0 | 1000000 | 1000000 | 0.8 | 0.9 | 650000 |
| table3 | cube-double-play-singletask-task2-v0 | FullSafe | 1 | 1000000 | 1000000 | 0.9 | 0.9 | 900000 |
| table3 | cube-double-play-singletask-task2-v0 | FullSafe | 2 | 1000000 | 1000000 | 1 | 1 | 750000 |
| table3 | cube-triple-play-singletask-task1-v0 | ActorGeo | 0 | 1000000 | 1000000 | 0.6 | 0.9 | 850000 |
| table3 | cube-triple-play-singletask-task1-v0 | ActorGeo | 1 | 1000000 | 1000000 | 0.6 | 0.9 | 850000 |
| table3 | cube-triple-play-singletask-task1-v0 | ActorGeo | 2 | 1000000 | 1000000 | 0.4 | 0.8 | 500000 |
| table3 | cube-triple-play-singletask-task1-v0 | FullSafe | 0 | 1000000 | 1000000 | 0 | 0.8 | 850000 |
| table3 | cube-triple-play-singletask-task1-v0 | FullSafe | 1 | 1000000 | 1000000 | 0.3 | 0.7 | 250000 |
| table3 | cube-triple-play-singletask-task1-v0 | FullSafe | 2 | 1000000 | 1000000 | 0.5 | 0.9 | 850000 |
| table3 | puzzle-3x3-play-singletask-task4-v0 | ActorGeo | 0 | 1000000 | 1000000 | 0.7 | 0.7 | 1000000 |
| table3 | puzzle-3x3-play-singletask-task4-v0 | ActorGeo | 1 | 1000000 | 1000000 | 1 | 1 | 1000000 |
| table3 | puzzle-3x3-play-singletask-task4-v0 | ActorGeo | 2 | 1000000 | 1000000 | 0.2 | 0.3 | 400000 |
| table3 | puzzle-3x3-play-singletask-task4-v0 | FullSafe | 0 | 1000000 | 1000000 | 0.7 | 0.7 | 950000 |
| table3 | puzzle-3x3-play-singletask-task4-v0 | FullSafe | 1 | 1000000 | 1000000 | 0.9 | 1 | 850000 |
| table3 | puzzle-4x4-play-singletask-task4-v0 | FullSafe | 0 | 1000000 | 1000000 | 0.3 | 0.6 | 350000 |
| table3 | puzzle-4x4-play-singletask-task4-v0 | FullSafe | 1 | 300000 | 700000 | 0 | 0.4 | 300000 |
| table3 | puzzle-4x4-play-singletask-task4-v0 | FullSafe | 1 | 1000000 | 1000000 | 0 | 0.5 | 700000 |
| table3 | puzzle-4x4-play-singletask-task4-v0 | FullSafe | 2 | 1000000 | 1000000 | 0.2 | 0.4 | 200000 |
| table3 | scene-play-singletask-task2-v0 | FullSafe | 0 | 1000000 | 1000000 | 1 | 1 | 200000 |
| table3 | scene-play-singletask-task2-v0 | FullSafe | 1 | 1000000 | 1000000 | 1 | 1 | 50000 |
| table3 | scene-play-singletask-task2-v0 | FullSafe | 2 | 1000000 | 1000000 | 1 | 1 | 150000 |

## Full Success Trajectories

### actorgeo / UNKNOWN / ActorGeo / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.1
- success_best: 0.4 @ 650000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.1 -> 250000:0 -> 300000:0.1 -> 350000:0.1 -> 400000:0.1 -> 450000:0.2 -> 500000:0.1 -> 550000:0 -> 600000:0.2 -> 650000:0.4 -> 700000:0.1 -> 750000:0 -> 800000:0.1 -> 850000:0.2 -> 900000:0 -> 950000:0.3 -> 1000000:0.1`
- eval_csv: `/root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_ActorGeo_seed0/sd000_20260525_100350/eval.csv`

### actorgeo / UNKNOWN / ActorGeo / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0
- success_best: 0.3 @ 100000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.3 -> 150000:0 -> 200000:0.2 -> 250000:0 -> 300000:0.1 -> 350000:0 -> 400000:0.1 -> 450000:0.1 -> 500000:0.2 -> 550000:0 -> 600000:0.1 -> 650000:0.1 -> 700000:0.1 -> 750000:0 -> 800000:0.2 -> 850000:0 -> 900000:0 -> 950000:0.1 -> 1000000:0`
- eval_csv: `/root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_ActorGeo_seed1/sd001_20260525_180814/eval.csv`

### actorgeo / UNKNOWN / ActorGeo / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.1
- success_best: 0.3 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.1 -> 150000:0 -> 200000:0 -> 250000:0.3 -> 300000:0.1 -> 350000:0 -> 400000:0.2 -> 450000:0.2 -> 500000:0.1 -> 550000:0 -> 600000:0.2 -> 650000:0 -> 700000:0.3 -> 750000:0.3 -> 800000:0.1 -> 850000:0 -> 900000:0.1 -> 950000:0 -> 1000000:0.1`
- eval_csv: `/root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_ActorGeo_seed2/sd002_20260526_021340/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task2-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task2_A1_action_std_lam0p001_seed2/sd002_20260609_071050/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task2-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.3 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.3`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task2_A2_action_std_lam0p003_seed2/sd002_20260609_082343/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task2-v0 / MinimalSB_lam0p0003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.3 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0.3`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task2_MinimalSB_lam0p0003_seed2/sd002_20260609_044414/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task2-v0 / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.3 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0 -> 300000:0.3`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task2_MinimalSB_lam0p001_seed2/sd002_20260609_055808/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task2-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.2 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task2_P0_particle_seed2/sd002_20260609_033015/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task2-v0 / R2_residual_disagree_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.2 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.1 -> 250000:0.2 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task2_R2_residual_disagree_lam0p001_seed2/sd002_20260609_093631/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task2-v0 / R3_residual_disagree_typicality_lam0p001 / seed 0 / PARTIAL

- final_step: 900000
- success_final: 0.8
- success_best: 0.9 @ 650000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.5 -> 350000:0.3 -> 400000:0.6 -> 450000:0.4 -> 500000:0.5 -> 550000:0.5 -> 600000:0.7 -> 650000:0.9 -> 700000:0.8 -> 750000:0.6 -> 800000:0.9 -> 850000:0.8 -> 900000:0.8`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task2_R3_residual_disagree_typicality_lam0p001_seed0/sd000_20260612_002941/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task2-v0 / R3_residual_disagree_typicality_lam0p001 / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.7
- success_best: 0.9 @ 450000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0.1 -> 300000:0.5 -> 350000:0.5 -> 400000:0.5 -> 450000:0.9 -> 500000:0.8 -> 550000:0.3 -> 600000:0.5 -> 650000:0.8 -> 700000:0.9 -> 750000:0.8 -> 800000:0.7 -> 850000:0.9 -> 900000:0.6 -> 950000:0.8 -> 1000000:0.7`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task2_R3_residual_disagree_typicality_lam0p001_seed0/sd000_20260612_093350/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task2-v0 / R3_residual_disagree_typicality_lam0p001 / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0.9
- success_best: 0.9 @ 650000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0.1 -> 400000:0.4 -> 450000:0.7 -> 500000:0.3 -> 550000:0.4 -> 600000:0.7 -> 650000:0.9 -> 700000:0.7 -> 750000:0.7 -> 800000:0.9 -> 850000:0.8 -> 900000:0.8 -> 950000:0.8 -> 1000000:0.9`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task2_R3_residual_disagree_typicality_lam0p001_seed1/sd001_20260612_133305/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task2-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.4
- success_best: 0.4 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0.2 -> 300000:0.4`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task2_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260609_104958/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task2-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.9
- success_best: 0.9 @ 1000000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.4 -> 350000:0.3 -> 400000:0.3 -> 450000:0.8 -> 500000:0.6 -> 550000:0.8 -> 600000:0.6 -> 650000:0.8 -> 700000:0.7 -> 750000:0.8 -> 800000:0.6 -> 850000:0.8 -> 900000:0.8 -> 950000:0.8 -> 1000000:0.9`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_cube_double_task2_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260611_203011/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task3-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.4
- success_best: 0.4 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.4`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task3_A1_action_std_lam0p001_seed2/sd002_20260609_154329/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task3-v0 / A2_action_std_lam0p003 / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.8
- success_best: 1 @ 700000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1 -> 350000:0.1 -> 400000:0 -> 450000:0.5 -> 500000:0.5 -> 550000:0.8 -> 600000:0.8 -> 650000:0.7 -> 700000:1 -> 750000:0.7 -> 800000:0.6 -> 850000:0.6 -> 900000:0.7 -> 950000:0.9 -> 1000000:0.8`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task3_A2_action_std_lam0p003_seed0/sd000_20260612_213228/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task3-v0 / A2_action_std_lam0p003 / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0.8
- success_best: 1 @ 800000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0 -> 350000:0.2 -> 400000:0.2 -> 450000:0.7 -> 500000:0.5 -> 550000:0.3 -> 600000:0.8 -> 650000:0.5 -> 700000:0.8 -> 750000:0.6 -> 800000:1 -> 850000:0.7 -> 900000:1 -> 950000:0.5 -> 1000000:0.8`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task3_A2_action_std_lam0p003_seed1/sd001_20260613_013227/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task3-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.5
- success_best: 0.5 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.2 -> 300000:0.5`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task3_A2_action_std_lam0p003_seed2/sd002_20260609_165639/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task3-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.9
- success_best: 1 @ 900000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0.1 -> 300000:0.3 -> 350000:0.6 -> 400000:0.6 -> 450000:0.3 -> 500000:0.7 -> 550000:0.8 -> 600000:0.6 -> 650000:0.8 -> 700000:0.5 -> 750000:0.8 -> 800000:0.6 -> 850000:0.6 -> 900000:1 -> 950000:0.7 -> 1000000:0.9`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_cube_double_task3_A2_action_std_lam0p003_seed2/sd002_20260612_173301/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task3-v0 / MinimalSB_lam0p0003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.4
- success_best: 0.4 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0.4`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task3_MinimalSB_lam0p0003_seed2/sd002_20260609_131645/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task3-v0 / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.4
- success_best: 0.4 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0.4`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task3_MinimalSB_lam0p001_seed2/sd002_20260609_142949/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task3-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.2 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.2 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task3_P0_particle_seed2/sd002_20260609_120343/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task3-v0 / R2_residual_disagree_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.3 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.3 -> 250000:0.1 -> 300000:0.3`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task3_R2_residual_disagree_lam0p001_seed2/sd002_20260609_181003/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task3-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.2 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task3_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260609_192330/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task4-v0 / A1_action_std_lam0p001 / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.4
- success_best: 0.5 @ 500000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0 -> 300000:0.2 -> 350000:0 -> 400000:0 -> 450000:0.1 -> 500000:0.5 -> 550000:0.5 -> 600000:0 -> 650000:0.3 -> 700000:0.3 -> 750000:0.5 -> 800000:0.1 -> 850000:0.5 -> 900000:0.1 -> 950000:0.2 -> 1000000:0.4`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task4_A1_action_std_lam0p001_seed0/sd000_20260613_093038/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task4-v0 / A1_action_std_lam0p001 / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0.3
- success_best: 0.4 @ 650000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.2 -> 300000:0 -> 350000:0.2 -> 400000:0.3 -> 450000:0.3 -> 500000:0.2 -> 550000:0.1 -> 600000:0.3 -> 650000:0.4 -> 700000:0.2 -> 750000:0.2 -> 800000:0.3 -> 850000:0.3 -> 900000:0.1 -> 950000:0.2 -> 1000000:0.3`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task4_A1_action_std_lam0p001_seed1/sd001_20260613_133019/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task4-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.3 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.3`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task4_A1_action_std_lam0p001_seed2/sd002_20260610_001658/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task4-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.5
- success_best: 0.7 @ 800000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1 -> 350000:0 -> 400000:0.2 -> 450000:0.3 -> 500000:0.1 -> 550000:0.2 -> 600000:0.3 -> 650000:0.3 -> 700000:0.5 -> 750000:0.4 -> 800000:0.7 -> 850000:0.4 -> 900000:0.1 -> 950000:0.4 -> 1000000:0.5`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_cube_double_task4_A1_action_std_lam0p001_seed2/sd002_20260613_053127/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task4-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.2 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task4_A2_action_std_lam0p003_seed2/sd002_20260610_013010/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task4-v0 / MinimalSB_lam0p0003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0 @ 1
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task4_MinimalSB_lam0p0003_seed2/sd002_20260609_215014/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task4-v0 / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task4_MinimalSB_lam0p001_seed2/sd002_20260609_230316/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task4-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 150000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0 -> 250000:0 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task4_P0_particle_seed2/sd002_20260609_203700/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task4-v0 / R2_residual_disagree_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task4_R2_residual_disagree_lam0p001_seed2/sd002_20260610_024319/eval.csv`

### bad_task_repair_single4090 / cube-double-play-singletask-task4-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task4_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260610_035647/eval.csv`

### bad_task_repair_single4090 / cube-triple-play-singletask-task3-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_triple_task3_A1_action_std_lam0p001_seed2/sd002_20260611_111742/eval.csv`

### bad_task_repair_single4090 / cube-triple-play-singletask-task3-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0 @ 1
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_triple_task3_A2_action_std_lam0p003_seed2/sd002_20260611_123319/eval.csv`

### bad_task_repair_single4090 / cube-triple-play-singletask-task3-v0 / MinimalSB_lam0p0003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0 @ 1
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_triple_task3_MinimalSB_lam0p0003_seed2/sd002_20260611_084632/eval.csv`

### bad_task_repair_single4090 / cube-triple-play-singletask-task3-v0 / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0 @ 1
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_triple_task3_MinimalSB_lam0p001_seed2/sd002_20260611_100156/eval.csv`

### bad_task_repair_single4090 / cube-triple-play-singletask-task3-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0 @ 1
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_triple_task3_P0_particle_seed2/sd002_20260611_073057/eval.csv`

### bad_task_repair_single4090 / cube-triple-play-singletask-task3-v0 / R2_residual_disagree_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0 @ 1
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_triple_task3_R2_residual_disagree_lam0p001_seed2/sd002_20260611_134956/eval.csv`

### bad_task_repair_single4090 / cube-triple-play-singletask-task3-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0 @ 1
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_triple_task3_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260611_150701/eval.csv`

### bad_task_repair_single4090 / puzzle-3x3-play-singletask-task3-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.1 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_A1_action_std_lam0p001_seed2/sd002_20260608_134900/eval.csv`

### bad_task_repair_single4090 / puzzle-3x3-play-singletask-task3-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_A2_action_std_lam0p003_seed2/sd002_20260608_150345/eval.csv`

### bad_task_repair_single4090 / puzzle-3x3-play-singletask-task3-v0 / MinimalSB_lam0p0003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.2 @ 150000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0 -> 250000:0 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_MinimalSB_lam0p0003_seed2/sd002_20260608_112126/eval.csv`

### bad_task_repair_single4090 / puzzle-3x3-play-singletask-task3-v0 / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.3 @ 150000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.3 -> 200000:0 -> 250000:0.1 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_MinimalSB_lam0p001_seed2/sd002_20260608_123522/eval.csv`

### bad_task_repair_single4090 / puzzle-3x3-play-singletask-task3-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.4 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.1 -> 250000:0.4 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_P0_particle_seed2/sd002_20260608_100720/eval.csv`

### bad_task_repair_single4090 / puzzle-3x3-play-singletask-task3-v0 / R2_residual_disagree_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.1 @ 100000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.1 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_R2_residual_disagree_lam0p001_seed2/sd002_20260608_161801/eval.csv`

### bad_task_repair_single4090 / puzzle-3x3-play-singletask-task3-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0 @ 1
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260608_173222/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task2-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task2_A1_action_std_lam0p001_seed2/sd002_20260610_174334/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task2-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.2 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0 -> 250000:0 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task2_A2_action_std_lam0p003_seed2/sd002_20260610_185833/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task2-v0 / MinimalSB_lam0p0003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.4 @ 100000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.4 -> 150000:0 -> 200000:0.2 -> 250000:0 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task2_MinimalSB_lam0p0003_seed2/sd002_20260610_151334/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task2-v0 / MinimalSB_lam0p001 / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.4
- success_best: 0.6 @ 950000
- trajectory_full: `1:0 -> 50000:0.1 -> 100000:0 -> 150000:0.2 -> 200000:0 -> 250000:0.1 -> 300000:0.3 -> 350000:0.4 -> 400000:0.2 -> 450000:0.4 -> 500000:0.3 -> 550000:0.4 -> 600000:0.2 -> 650000:0.2 -> 700000:0.3 -> 750000:0.1 -> 800000:0.1 -> 850000:0.3 -> 900000:0.2 -> 950000:0.6 -> 1000000:0.4`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_puzzle_4x4_task2_MinimalSB_lam0p001_seed0/sd000_20260614_014306/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task2-v0 / MinimalSB_lam0p001 / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0.1
- success_best: 0.6 @ 900000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.2 -> 150000:0.3 -> 200000:0 -> 250000:0.1 -> 300000:0.1 -> 350000:0 -> 400000:0 -> 450000:0.4 -> 500000:0.2 -> 550000:0.1 -> 600000:0 -> 650000:0.2 -> 700000:0 -> 750000:0.4 -> 800000:0.2 -> 850000:0 -> 900000:0.6 -> 950000:0 -> 1000000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_puzzle_4x4_task2_MinimalSB_lam0p001_seed1/sd001_20260614_055017/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task2-v0 / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.5 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.1 -> 150000:0 -> 200000:0 -> 250000:0.5 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task2_MinimalSB_lam0p001_seed2/sd002_20260610_162826/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task2-v0 / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.5
- success_best: 0.5 @ 600000
- trajectory_full: `1:0 -> 50000:0.1 -> 100000:0.2 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0.4 -> 350000:0.1 -> 400000:0.2 -> 450000:0.1 -> 500000:0.2 -> 550000:0.2 -> 600000:0.5 -> 650000:0.5 -> 700000:0.5 -> 750000:0.4 -> 800000:0.2 -> 850000:0.1 -> 900000:0.4 -> 950000:0.3 -> 1000000:0.5`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_puzzle_4x4_task2_MinimalSB_lam0p001_seed2/sd002_20260613_213740/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task2-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.3 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.1 -> 150000:0 -> 200000:0 -> 250000:0.3 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task2_P0_particle_seed2/sd002_20260610_135827/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task2-v0 / R2_residual_disagree_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0 @ 1
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task2_R2_residual_disagree_lam0p001_seed2/sd002_20260610_201338/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task2-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.2 @ 100000
- trajectory_full: `1:0 -> 50000:0.1 -> 100000:0.2 -> 150000:0 -> 200000:0 -> 250000:0.2 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task2_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260610_212924/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task4-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task4_A1_action_std_lam0p001_seed2/sd002_20260611_022959/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task4-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.3 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.1 -> 150000:0.1 -> 200000:0.3 -> 250000:0.3 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task4_A2_action_std_lam0p003_seed2/sd002_20260611_034451/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task4-v0 / MinimalSB_lam0p0003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.3 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.1 -> 250000:0.1 -> 300000:0.3`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task4_MinimalSB_lam0p0003_seed2/sd002_20260611_000009/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task4-v0 / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.3 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0 -> 250000:0.1 -> 300000:0.3`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task4_MinimalSB_lam0p001_seed2/sd002_20260611_011518/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task4-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.5 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.5 -> 250000:0.3 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task4_P0_particle_seed2/sd002_20260610_224514/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task4-v0 / R2_residual_disagree_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.3 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.2 -> 250000:0.1 -> 300000:0.3`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task4_R2_residual_disagree_lam0p001_seed2/sd002_20260611_045940/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task4-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.5
- success_best: 0.5 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.3 -> 300000:0.5`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task4_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260611_061504/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task4-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.1
- success_best: 0.5 @ 850000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0.1 -> 300000:0.1 -> 350000:0.2 -> 400000:0.3 -> 450000:0.1 -> 500000:0 -> 550000:0.2 -> 600000:0.4 -> 650000:0.1 -> 700000:0.2 -> 750000:0.4 -> 800000:0 -> 850000:0.5 -> 900000:0.3 -> 950000:0.1 -> 1000000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_puzzle_4x4_task4_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260614_095700/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task5-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.1 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0.1 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task5_A1_action_std_lam0p001_seed2/sd002_20260610_085659/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task5-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0.1 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task5_A2_action_std_lam0p003_seed2/sd002_20260610_101149/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task5-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0
- success_best: 0.2 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0 -> 250000:0.2 -> 300000:0 -> 350000:0 -> 400000:0.1 -> 450000:0 -> 500000:0.1 -> 550000:0.1 -> 600000:0 -> 650000:0 -> 700000:0 -> 750000:0 -> 800000:0 -> 850000:0 -> 900000:0 -> 950000:0 -> 1000000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_puzzle_4x4_task5_A2_action_std_lam0p003_seed2/sd002_20260613_173157/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task5-v0 / MinimalSB_lam0p0003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 150000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.1 -> 250000:0.1 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task5_MinimalSB_lam0p0003_seed2/sd002_20260610_062557/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task5-v0 / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.1 @ 150000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.1 -> 250000:0.1 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task5_MinimalSB_lam0p001_seed2/sd002_20260610_074115/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task5-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task5_P0_particle_seed2/sd002_20260610_051047/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task5-v0 / R2_residual_disagree_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.2 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.2 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task5_R2_residual_disagree_lam0p001_seed2/sd002_20260610_112702/eval.csv`

### bad_task_repair_single4090 / puzzle-4x4-play-singletask-task5-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.2 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.2 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task5_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260610_124302/eval.csv`

### bad_task_repair_single4090 / scene-play-singletask-task4-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.7 @ 150000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.2 -> 150000:0.7 -> 200000:0.6 -> 250000:0.2 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_scene_task4_A1_action_std_lam0p001_seed2/sd002_20260608_223033/eval.csv`

### bad_task_repair_single4090 / scene-play-singletask-task4-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.9 @ 100000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.9 -> 150000:0.1 -> 200000:0.2 -> 250000:0.1 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_scene_task4_A2_action_std_lam0p003_seed2/sd002_20260608_234523/eval.csv`

### bad_task_repair_single4090 / scene-play-singletask-task4-v0 / MinimalSB_lam0p0003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.8 @ 100000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.8 -> 150000:0.5 -> 200000:0.3 -> 250000:0.2 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_scene_task4_MinimalSB_lam0p0003_seed2/sd002_20260608_200119/eval.csv`

### bad_task_repair_single4090 / scene-play-singletask-task4-v0 / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.7 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.3 -> 150000:0.2 -> 200000:0.7 -> 250000:0.7 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_scene_task4_MinimalSB_lam0p001_seed2/sd002_20260608_211603/eval.csv`

### bad_task_repair_single4090 / scene-play-singletask-task4-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.4
- success_best: 0.6 @ 100000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.6 -> 150000:0.2 -> 200000:0.3 -> 250000:0.5 -> 300000:0.4`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_scene_task4_P0_particle_seed2/sd002_20260608_184656/eval.csv`

### bad_task_repair_single4090 / scene-play-singletask-task4-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0
- success_best: 0.9 @ 100000
- trajectory_full: `1:0 -> 50000:0.2 -> 100000:0.9 -> 150000:0.1 -> 200000:0.4 -> 250000:0.4 -> 300000:0.1 -> 350000:0 -> 400000:0.2 -> 450000:0 -> 500000:0 -> 550000:0.1 -> 600000:0.1 -> 650000:0.1 -> 700000:0.1 -> 750000:0 -> 800000:0 -> 850000:0 -> 900000:0 -> 950000:0 -> 1000000:0`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_scene_task4_P0_particle_seed2/sd002_20260611_162414/eval.csv`

### bad_task_repair_single4090 / scene-play-singletask-task4-v0 / R2_residual_disagree_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.7 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.3 -> 150000:0 -> 200000:0.2 -> 250000:0.7 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_scene_task4_R2_residual_disagree_lam0p001_seed2/sd002_20260609_010005/eval.csv`

### bad_task_repair_single4090 / scene-play-singletask-task4-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.8 @ 100000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.8 -> 150000:0.1 -> 200000:0.2 -> 250000:0.2 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_scene_task4_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260609_021528/eval.csv`

### bestseed / UNKNOWN / bestseed / seed 5 / COMPLETED

- final_step: 1000000
- success_final: 1
- success_best: 1 @ 100000
- trajectory_full: `1:0 -> 50000:0.9 -> 100000:1 -> 150000:1 -> 200000:1 -> 250000:1 -> 300000:1 -> 350000:1 -> 400000:1 -> 450000:1 -> 500000:1 -> 550000:0.9 -> 600000:1 -> 650000:1 -> 700000:1 -> 750000:1 -> 800000:1 -> 850000:1 -> 900000:1 -> 950000:1 -> 1000000:1`
- eval_csv: `/root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task1_S1_sb_lam0p001_seed2/sd002_20260606_142934/eval.csv`

### bestseed / UNKNOWN / bestseed / seed 5 / COMPLETED

- final_step: 1000000
- success_final: 1
- success_best: 1 @ 400000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0.5 -> 350000:0.7 -> 400000:1 -> 450000:0.8 -> 500000:0.9 -> 550000:0.8 -> 600000:0.8 -> 650000:1 -> 700000:1 -> 750000:1 -> 800000:1 -> 850000:0.9 -> 900000:1 -> 950000:1 -> 1000000:1`
- eval_csv: `/root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task2_S1_sb_lam0p001_seed2/sd002_20260606_182634/eval.csv`

### bestseed / UNKNOWN / bestseed / seed 5 / COMPLETED

- final_step: 1000000
- success_final: 0.1
- success_best: 0.1 @ 650000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0 -> 400000:0 -> 450000:0 -> 500000:0 -> 550000:0 -> 600000:0 -> 650000:0.1 -> 700000:0 -> 750000:0 -> 800000:0 -> 850000:0 -> 900000:0 -> 950000:0 -> 1000000:0.1`
- eval_csv: `/root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task3_S1_sb_lam0p001_seed2/sd002_20260606_222604/eval.csv`

### bestseed / UNKNOWN / bestseed / seed 5 / COMPLETED

- final_step: 1000000
- success_final: 1
- success_best: 1 @ 850000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1 -> 350000:0 -> 400000:0 -> 450000:0.1 -> 500000:0.2 -> 550000:0.2 -> 600000:0.4 -> 650000:0.3 -> 700000:0.4 -> 750000:0.9 -> 800000:0.9 -> 850000:1 -> 900000:0.9 -> 950000:1 -> 1000000:1`
- eval_csv: `/root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task4_S1_sb_lam0p001_seed2/sd002_20260607_022834/eval.csv`

### bestseed / UNKNOWN / bestseed / seed 5 / COMPLETED

- final_step: 1000000
- success_final: 1
- success_best: 1 @ 1000000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.3 -> 200000:0.1 -> 250000:0.3 -> 300000:0.3 -> 350000:0.5 -> 400000:0.1 -> 450000:0.2 -> 500000:0.3 -> 550000:0.2 -> 600000:0.3 -> 650000:0.5 -> 700000:0.8 -> 750000:0.4 -> 800000:0.5 -> 850000:0.3 -> 900000:0.9 -> 950000:0.8 -> 1000000:1`
- eval_csv: `/root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task5_S1_sb_lam0p001_seed2/sd002_20260607_063032/eval.csv`

### fullsafe / UNKNOWN / FullSafe / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.2
- success_best: 0.2 @ 350000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0 -> 300000:0 -> 350000:0.2 -> 400000:0 -> 450000:0 -> 500000:0 -> 550000:0 -> 600000:0 -> 650000:0.1 -> 700000:0 -> 750000:0 -> 800000:0.2 -> 850000:0.2 -> 900000:0.2 -> 950000:0.1 -> 1000000:0.2`
- eval_csv: `/root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_FullSafe_seed0/sd000_20260525_140611/eval.csv`

### fullsafe / UNKNOWN / FullSafe / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0
- success_best: 0.2 @ 50000
- trajectory_full: `1:0 -> 50000:0.2 -> 100000:0 -> 150000:0.1 -> 200000:0.1 -> 250000:0.1 -> 300000:0 -> 350000:0.1 -> 400000:0.1 -> 450000:0 -> 500000:0.1 -> 550000:0 -> 600000:0.1 -> 650000:0.2 -> 700000:0.1 -> 750000:0 -> 800000:0 -> 850000:0.1 -> 900000:0 -> 950000:0.1 -> 1000000:0`
- eval_csv: `/root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_FullSafe_seed1/sd001_20260525_221133/eval.csv`

### fullsafe / UNKNOWN / FullSafe / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.2
- success_best: 0.4 @ 800000
- trajectory_full: `1:0 -> 50000:0.1 -> 100000:0.2 -> 150000:0 -> 200000:0.1 -> 250000:0.1 -> 300000:0.1 -> 350000:0 -> 400000:0.2 -> 450000:0.3 -> 500000:0 -> 550000:0.2 -> 600000:0.1 -> 650000:0.1 -> 700000:0.1 -> 750000:0.1 -> 800000:0.4 -> 850000:0.1 -> 900000:0.2 -> 950000:0.1 -> 1000000:0.2`
- eval_csv: `/root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_FullSafe_seed2/sd002_20260526_061530/eval.csv`

### minimal / UNKNOWN / MinimalSB_lam0p0003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.1 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/puzzle3x3_task3_repair_single4090_v1/screen300k_MinimalSB_lam0p0003_seed2/sd002_20260607_121217/eval.csv`

### minimal / UNKNOWN / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.2 @ 150000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/puzzle3x3_task3_repair_single4090_v1/screen300k_MinimalSB_lam0p001_seed2/sd002_20260607_132608/eval.csv`

### minimal / UNKNOWN / P0_particle / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.3
- success_best: 0.7 @ 850000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0.1 -> 400000:0 -> 450000:0 -> 500000:0 -> 550000:0 -> 600000:0.1 -> 650000:0 -> 700000:0.4 -> 750000:0 -> 800000:0.2 -> 850000:0.7 -> 900000:0.2 -> 950000:0.5 -> 1000000:0.3`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/P0_particle_seed0/sd000_20260602_103605/eval.csv`

### minimal / UNKNOWN / P0_particle / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0.7
- success_best: 1 @ 850000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0 -> 400000:0 -> 450000:0 -> 500000:0.7 -> 550000:0.3 -> 600000:0.2 -> 650000:0.5 -> 700000:0.5 -> 750000:0.6 -> 800000:0.9 -> 850000:1 -> 900000:0.8 -> 950000:0.7 -> 1000000:0.7`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/P0_particle_seed1/sd001_20260602_143822/eval.csv`

### minimal / UNKNOWN / P0_particle / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.3
- success_best: 0.6 @ 850000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1 -> 350000:0 -> 400000:0.1 -> 450000:0.1 -> 500000:0 -> 550000:0.1 -> 600000:0.3 -> 650000:0.1 -> 700000:0.2 -> 750000:0.1 -> 800000:0.3 -> 850000:0.6 -> 900000:0 -> 950000:0.1 -> 1000000:0.3`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/P0_particle_seed2/sd002_20260602_184301/eval.csv`

### minimal / UNKNOWN / P0_particle / seed 3 / COMPLETED

- final_step: 1000000
- success_final: 1
- success_best: 1 @ 850000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0 -> 400000:0 -> 450000:0.1 -> 500000:0.5 -> 550000:0.7 -> 600000:0.7 -> 650000:0.7 -> 700000:0.7 -> 750000:0.6 -> 800000:0.8 -> 850000:1 -> 900000:0.8 -> 950000:0.9 -> 1000000:1`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed3/sd003_20260605_061635/eval.csv`

### minimal / UNKNOWN / P0_particle / seed 4 / COMPLETED

- final_step: 1000000
- success_final: 0
- success_best: 0.3 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.3 -> 250000:0.1 -> 300000:0 -> 350000:0.1 -> 400000:0.1 -> 450000:0 -> 500000:0 -> 550000:0 -> 600000:0 -> 650000:0 -> 700000:0 -> 750000:0.2 -> 800000:0.1 -> 850000:0 -> 900000:0 -> 950000:0 -> 1000000:0`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed4/sd004_20260605_102001/eval.csv`

### minimal / UNKNOWN / P0_particle / seed 5 / COMPLETED

- final_step: 1000000
- success_final: 0
- success_best: 0.2 @ 750000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1 -> 350000:0 -> 400000:0 -> 450000:0.1 -> 500000:0 -> 550000:0.1 -> 600000:0.1 -> 650000:0 -> 700000:0.1 -> 750000:0.2 -> 800000:0 -> 850000:0.1 -> 900000:0.1 -> 950000:0 -> 1000000:0`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed5/sd005_20260605_142338/eval.csv`

### minimal / UNKNOWN / P0_particle / seed 6 / COMPLETED

- final_step: 1000000
- success_final: 0.1
- success_best: 0.2 @ 700000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0 -> 400000:0.1 -> 450000:0 -> 500000:0 -> 550000:0 -> 600000:0 -> 650000:0 -> 700000:0.2 -> 750000:0.1 -> 800000:0 -> 850000:0.2 -> 900000:0.1 -> 950000:0.2 -> 1000000:0.1`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed6/sd006_20260605_182702/eval.csv`

### minimal / UNKNOWN / P0_particle / seed 7 / COMPLETED

- final_step: 1000000
- success_final: 0.5
- success_best: 0.5 @ 1000000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0 -> 400000:0 -> 450000:0 -> 500000:0 -> 550000:0.1 -> 600000:0 -> 650000:0.1 -> 700000:0.1 -> 750000:0.2 -> 800000:0.3 -> 850000:0.2 -> 900000:0.2 -> 950000:0.1 -> 1000000:0.5`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed7/sd007_20260605_223009/eval.csv`

### minimal / UNKNOWN / S1_sb_lam0p001_seed0 / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.2
- success_best: 0.6 @ 700000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0 -> 400000:0 -> 450000:0 -> 500000:0.1 -> 550000:0 -> 600000:0 -> 650000:0.2 -> 700000:0.6 -> 750000:0.1 -> 800000:0.3 -> 850000:0.3 -> 900000:0.3 -> 950000:0.6 -> 1000000:0.2`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/S1_sb_lam0p001_seed0/sd000_20260602_224525/eval.csv`

### minimal / UNKNOWN / S1_sb_lam0p001_seed1 / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 1
- success_best: 1 @ 850000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1 -> 350000:0.4 -> 400000:0 -> 450000:0 -> 500000:0.2 -> 550000:0.2 -> 600000:0.2 -> 650000:0.5 -> 700000:0.7 -> 750000:0.9 -> 800000:0.8 -> 850000:1 -> 900000:1 -> 950000:1 -> 1000000:1`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/S1_sb_lam0p001_seed1/sd001_20260603_024723/eval.csv`

### minimal / UNKNOWN / S1_sb_lam0p001_seed2 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 1
- success_best: 1 @ 900000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0 -> 400000:0.1 -> 450000:0 -> 500000:0 -> 550000:0 -> 600000:0.2 -> 650000:0.5 -> 700000:0.6 -> 750000:0.4 -> 800000:0.8 -> 850000:0.9 -> 900000:1 -> 950000:1 -> 1000000:1`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/S1_sb_lam0p001_seed2/sd002_20260603_065051/eval.csv`

### minimal / UNKNOWN / S1_sb_lam0p001_seed3 / seed 3 / COMPLETED

- final_step: 1000000
- success_final: 1
- success_best: 1 @ 800000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0 -> 400000:0.1 -> 450000:0.3 -> 500000:0.3 -> 550000:0.1 -> 600000:0.2 -> 650000:0.6 -> 700000:0.8 -> 750000:0.8 -> 800000:1 -> 850000:0.9 -> 900000:1 -> 950000:1 -> 1000000:1`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed3/sd003_20260604_100455/eval.csv`

### minimal / UNKNOWN / S1_sb_lam0p001_seed4 / seed 4 / COMPLETED

- final_step: 1000000
- success_final: 0.2
- success_best: 0.6 @ 550000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0.2 -> 400000:0.2 -> 450000:0.1 -> 500000:0.4 -> 550000:0.6 -> 600000:0.3 -> 650000:0.3 -> 700000:0.4 -> 750000:0.2 -> 800000:0.2 -> 850000:0.1 -> 900000:0.1 -> 950000:0.1 -> 1000000:0.2`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed4/sd004_20260604_140603/eval.csv`

### minimal / UNKNOWN / S1_sb_lam0p001_seed5 / seed 5 / COMPLETED

- final_step: 1000000
- success_final: 1
- success_best: 1 @ 1000000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.1 -> 150000:0.1 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0.1 -> 400000:0.1 -> 450000:0 -> 500000:0.2 -> 550000:0.1 -> 600000:0.6 -> 650000:0.5 -> 700000:0.4 -> 750000:0.7 -> 800000:0.8 -> 850000:0.8 -> 900000:0.6 -> 950000:0.7 -> 1000000:1`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed5/sd005_20260604_180842/eval.csv`

### minimal / UNKNOWN / S1_sb_lam0p001_seed6 / seed 6 / COMPLETED

- final_step: 1000000
- success_final: 0.1
- success_best: 0.2 @ 350000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0.2 -> 400000:0.1 -> 450000:0 -> 500000:0 -> 550000:0 -> 600000:0.2 -> 650000:0.2 -> 700000:0.1 -> 750000:0.1 -> 800000:0 -> 850000:0.2 -> 900000:0.1 -> 950000:0.1 -> 1000000:0.1`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed6/sd006_20260604_221117/eval.csv`

### minimal / UNKNOWN / S1_sb_lam0p001_seed7 / seed 7 / COMPLETED

- final_step: 1000000
- success_final: 0.2
- success_best: 0.2 @ 900000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0 -> 300000:0 -> 350000:0 -> 400000:0 -> 450000:0.1 -> 500000:0.1 -> 550000:0 -> 600000:0 -> 650000:0 -> 700000:0 -> 750000:0 -> 800000:0.1 -> 850000:0 -> 900000:0.2 -> 950000:0 -> 1000000:0.2`
- eval_csv: `/root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed7/sd007_20260605_021352/eval.csv`

### puzzle3x3 / UNKNOWN / screen300k_P0_seed2 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.1 @ 100000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.1 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/puzzle3x3_task3_repair_single4090_v1/screen300k_P0_seed2/sd002_20260607_105834/eval.csv`

### puzzle4x4 / UNKNOWN / stageA_V0_light_default_seed0 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.6
- success_best: 0.6 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0.1 -> 250000:0.4 -> 300000:0.6`
- eval_csv: `/root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V0_light_default_seed0/sd000_20260530_130211/eval.csv`

### puzzle4x4 / UNKNOWN / stageA_V1_actor_0p003_seed0 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.4
- success_best: 0.4 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.1 -> 150000:0.1 -> 200000:0.2 -> 250000:0.2 -> 300000:0.4`
- eval_csv: `/root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V1_actor_0p003_seed0/sd000_20260530_141848/eval.csv`

### puzzle4x4 / UNKNOWN / stageA_V2_actor_0p0_seed0 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.3 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0 -> 250000:0.2 -> 300000:0.3`
- eval_csv: `/root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V2_actor_0p0_seed0/sd000_20260530_153559/eval.csv`

### puzzle4x4 / UNKNOWN / stageA_V3_energy_0p001_seed0 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.3 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.2 -> 250000:0.3 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V3_energy_0p001_seed0/sd000_20260530_165349/eval.csv`

### puzzle4x4 / UNKNOWN / stageA_V4_no_energy_rel_seed0 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.2 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.2 -> 250000:0.1 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V4_no_energy_rel_seed0/sd000_20260530_181043/eval.csv`

### puzzle4x4 / UNKNOWN / stageA_V6_temp_0p5_seed0 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.2 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.2 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V6_temp_0p5_seed0/sd000_20260530_204055/eval.csv`

### puzzle4x4 / UNKNOWN / stageA_V7_temp_0p1_seed0 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.5 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.3 -> 250000:0.5 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V7_temp_0p1_seed0/sd000_20260530_215618/eval.csv`

### puzzle4x4 / UNKNOWN / stageA_W0_current_seed0 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.4 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.1 -> 150000:0.1 -> 200000:0.4 -> 250000:0.3 -> 300000:0.3`
- eval_csv: `/root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W0_current_seed0/sd000_20260531_235504/eval.csv`

### puzzle4x4 / UNKNOWN / stageA_W1_bcfm1_seed0 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.2 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0.1 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W1_bcfm1_seed0/sd000_20260601_010946/eval.csv`

### puzzle4x4 / UNKNOWN / stageA_W2_bcfm2_seed0 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.2 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.1 -> 250000:0 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W2_bcfm2_seed0/sd000_20260601_022446/eval.csv`

### puzzle4x4 / UNKNOWN / stageA_W3_bcfm5_seed0 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.4 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.2 -> 250000:0.4 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W3_bcfm5_seed0/sd000_20260601_033930/eval.csv`

### puzzle4x4 / UNKNOWN / stageA_W4_temp50_seed0 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.4
- success_best: 0.4 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.4 -> 250000:0.2 -> 300000:0.4`
- eval_csv: `/root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W4_temp50_seed0/sd000_20260601_045418/eval.csv`

### puzzle4x4 / UNKNOWN / stageA_W5_temp200_seed0 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.6 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.2 -> 250000:0.6 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W5_temp200_seed0/sd000_20260601_060858/eval.csv`

### puzzle4x4 / UNKNOWN / stageA_W6_qmean_seed0 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.2 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.2`
- eval_csv: `/root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W6_qmean_seed0/sd000_20260601_072342/eval.csv`

### puzzle4x4 / UNKNOWN / stageB_V0_light_default_seed0 / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.2
- success_best: 0.4 @ 450000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.3 -> 250000:0.2 -> 300000:0.2 -> 350000:0.3 -> 400000:0.2 -> 450000:0.4 -> 500000:0.2 -> 550000:0.4 -> 600000:0 -> 650000:0.4 -> 700000:0.1 -> 750000:0.2 -> 800000:0.4 -> 850000:0.2 -> 900000:0 -> 950000:0.1 -> 1000000:0.2`
- eval_csv: `/root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V0_light_default_seed0/sd000_20260530_231113/eval.csv`

### puzzle4x4 / UNKNOWN / stageB_V0_light_default_seed1 / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0
- success_best: 0.5 @ 400000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0.2 -> 300000:0.2 -> 350000:0.2 -> 400000:0.5 -> 450000:0.2 -> 500000:0.3 -> 550000:0.2 -> 600000:0.2 -> 650000:0.1 -> 700000:0 -> 750000:0 -> 800000:0 -> 850000:0.1 -> 900000:0 -> 950000:0 -> 1000000:0`
- eval_csv: `/root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V0_light_default_seed1/sd001_20260531_031709/eval.csv`

### puzzle4x4 / UNKNOWN / stageB_V0_light_default_seed2 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.3
- success_best: 0.3 @ 350000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.1 -> 150000:0.1 -> 200000:0 -> 250000:0.1 -> 300000:0.1 -> 350000:0.3 -> 400000:0.1 -> 450000:0 -> 500000:0 -> 550000:0.1 -> 600000:0 -> 650000:0.3 -> 700000:0.1 -> 750000:0 -> 800000:0 -> 850000:0.2 -> 900000:0.1 -> 950000:0 -> 1000000:0.3`
- eval_csv: `/root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V0_light_default_seed2/sd002_20260531_072216/eval.csv`

### puzzle4x4 / UNKNOWN / stageB_V1_actor_0p003_seed0 / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.3
- success_best: 0.4 @ 450000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.3 -> 250000:0 -> 300000:0.1 -> 350000:0 -> 400000:0 -> 450000:0.4 -> 500000:0.2 -> 550000:0.2 -> 600000:0 -> 650000:0.2 -> 700000:0.1 -> 750000:0.3 -> 800000:0.3 -> 850000:0 -> 900000:0 -> 950000:0.3 -> 1000000:0.3`
- eval_csv: `/root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V1_actor_0p003_seed0/sd000_20260531_112724/eval.csv`

### puzzle4x4 / UNKNOWN / stageB_V1_actor_0p003_seed1 / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0.3
- success_best: 0.5 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.5 -> 250000:0.1 -> 300000:0.3 -> 350000:0.3 -> 400000:0.1 -> 450000:0.2 -> 500000:0.4 -> 550000:0.2 -> 600000:0.4 -> 650000:0.2 -> 700000:0.1 -> 750000:0.2 -> 800000:0.1 -> 850000:0.1 -> 900000:0.1 -> 950000:0.4 -> 1000000:0.3`
- eval_csv: `/root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V1_actor_0p003_seed1/sd001_20260531_153428/eval.csv`

### puzzle4x4 / UNKNOWN / stageB_V1_actor_0p003_seed2 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.1
- success_best: 0.6 @ 850000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0.5 -> 300000:0.1 -> 350000:0.2 -> 400000:0.4 -> 450000:0.2 -> 500000:0.1 -> 550000:0.2 -> 600000:0.2 -> 650000:0.2 -> 700000:0 -> 750000:0.1 -> 800000:0 -> 850000:0.6 -> 900000:0.2 -> 950000:0.5 -> 1000000:0.1`
- eval_csv: `/root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V1_actor_0p003_seed2/sd002_20260531_194155/eval.csv`

### puzzle4x4 / UNKNOWN / stageB_W0_current_seed0 / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.1
- success_best: 0.4 @ 400000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0.2 -> 250000:0.1 -> 300000:0 -> 350000:0.1 -> 400000:0.4 -> 450000:0.2 -> 500000:0.4 -> 550000:0.4 -> 600000:0 -> 650000:0.1 -> 700000:0.2 -> 750000:0.3 -> 800000:0.1 -> 850000:0.1 -> 900000:0 -> 950000:0.1 -> 1000000:0.1`
- eval_csv: `/root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W0_current_seed0/sd000_20260601_205753/eval.csv`

### puzzle4x4 / UNKNOWN / stageB_W0_current_seed1 / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0
- success_best: 0.4 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0.4 -> 300000:0.1 -> 350000:0.1 -> 400000:0.2 -> 450000:0.2 -> 500000:0.2 -> 550000:0.1 -> 600000:0 -> 650000:0 -> 700000:0 -> 750000:0 -> 800000:0 -> 850000:0 -> 900000:0 -> 950000:0 -> 1000000:0`
- eval_csv: `/root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W0_current_seed1/sd001_20260602_010332/eval.csv`

### puzzle4x4 / UNKNOWN / stageB_W0_current_seed2 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.1
- success_best: 0.5 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0 -> 250000:0.2 -> 300000:0.5 -> 350000:0.2 -> 400000:0.4 -> 450000:0.3 -> 500000:0.3 -> 550000:0.2 -> 600000:0.3 -> 650000:0.2 -> 700000:0.4 -> 750000:0 -> 800000:0 -> 850000:0.2 -> 900000:0.3 -> 950000:0 -> 1000000:0.1`
- eval_csv: `/root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W0_current_seed2/sd002_20260602_050918/eval.csv`

### puzzle4x4 / UNKNOWN / stageB_W4_temp50_seed0 / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.1
- success_best: 0.5 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0.5 -> 250000:0.4 -> 300000:0.1 -> 350000:0.4 -> 400000:0.3 -> 450000:0.1 -> 500000:0 -> 550000:0.4 -> 600000:0.1 -> 650000:0.2 -> 700000:0.3 -> 750000:0.1 -> 800000:0 -> 850000:0 -> 900000:0.1 -> 950000:0 -> 1000000:0.1`
- eval_csv: `/root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W4_temp50_seed0/sd000_20260601_083824/eval.csv`

### puzzle4x4 / UNKNOWN / stageB_W4_temp50_seed1 / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0.1
- success_best: 0.3 @ 450000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0.1 -> 300000:0.1 -> 350000:0 -> 400000:0 -> 450000:0.3 -> 500000:0.2 -> 550000:0.1 -> 600000:0 -> 650000:0 -> 700000:0 -> 750000:0 -> 800000:0 -> 850000:0 -> 900000:0 -> 950000:0 -> 1000000:0.1`
- eval_csv: `/root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W4_temp50_seed1/sd001_20260601_124531/eval.csv`

### puzzle4x4 / UNKNOWN / stageB_W4_temp50_seed2 / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.5
- success_best: 0.5 @ 1000000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.1 -> 250000:0.2 -> 300000:0.1 -> 350000:0.2 -> 400000:0.2 -> 450000:0.3 -> 500000:0.3 -> 550000:0.1 -> 600000:0.3 -> 650000:0.1 -> 700000:0 -> 750000:0 -> 800000:0 -> 850000:0.1 -> 900000:0.1 -> 950000:0.2 -> 1000000:0.5`
- eval_csv: `/root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W4_temp50_seed2/sd002_20260601_165143/eval.csv`

### reliability / UNKNOWN / A1_action_std_lam0p001 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_A1_action_std_lam0p001_seed0/sd000_20260603_175838/eval.csv`

### reliability / UNKNOWN / A2_action_std_lam0p003 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.1 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1`
- eval_csv: `/root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_A2_action_std_lam0p003_seed0/sd000_20260603_191232/eval.csv`

### reliability / UNKNOWN / P0_particle / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0 @ 1
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_P0_particle_seed0/sd000_20260603_153103/eval.csv`

### reliability / UNKNOWN / R2_flow_residual_disagree_std_lam0p001 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.1 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_R2_flow_residual_disagree_std_lam0p001_seed0/sd000_20260603_214048/eval.csv`

### reliability / UNKNOWN / R3_flow_residual_disagree_typicality_std_lam0p001 / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.1 @ 150000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_R3_flow_residual_disagree_typicality_std_lam0p001_seed0/sd000_20260603_225503/eval.csv`

### reliability / UNKNOWN / reliability / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.3 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.3 -> 250000:0 -> 300000:0.3`
- eval_csv: `/root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V5_no_reliability_seed0/sd000_20260530_192614/eval.csv`

### reliability / UNKNOWN / reliability / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.1 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_A0_action_raw_lam0p001_seed0/sd000_20260603_164451/eval.csv`

### reliability / UNKNOWN / reliability / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0 @ 1
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_R1_flow_residual_std_lam0p001_seed0/sd000_20260603_202634/eval.csv`

### reliability / UNKNOWN / reliability / seed 0 / COMPLETED

- final_step: 300000
- success_final: 0
- success_best: 0.1 @ 150000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0 -> 250000:0.1 -> 300000:0`
- eval_csv: `/root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_R4_flow_residual_disagree_typicality_mean_lam0p001_seed0/sd000_20260604_000934/eval.csv`

### reliability / UNKNOWN / reliability / seed 3 / PARTIAL

- final_step: 100000
- success_final: 0
- success_best: 0.1 @ 10000
- trajectory_full: `1:0 -> 10000:0.1 -> 20000:0 -> 30000:0 -> 40000:0 -> 50000:0.1 -> 60000:0.1 -> 70000:0 -> 80000:0.1 -> 90000:0.1 -> 100000:0`
- eval_csv: `/root/sb-value-flows/exp/pm_medium_component_4090/V3_PM_reliability_only/sd003_20260524_004008/eval.csv`

### selective_state_tuning_single4090 / puzzle-4x4-play-singletask-task1-v0 / A1_action_std_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.4
- success_best: 0.4 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.1 -> 150000:0.3 -> 200000:0.3 -> 250000:0.4 -> 300000:0.4`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task1_A1_action_std_lam0p001_seed2/sd002_20260615_201119/eval.csv`

### selective_state_tuning_single4090 / puzzle-4x4-play-singletask-task1-v0 / A2_action_std_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.5
- success_best: 0.5 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.3 -> 250000:0.4 -> 300000:0.5`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task1_A2_action_std_lam0p003_seed2/sd002_20260615_212615/eval.csv`

### selective_state_tuning_single4090 / puzzle-4x4-play-singletask-task1-v0 / MinimalSB_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.4 @ 150000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.4 -> 200000:0.3 -> 250000:0.2 -> 300000:0.3`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task1_MinimalSB_lam0p001_seed2/sd002_20260615_185554/eval.csv`

### selective_state_tuning_single4090 / puzzle-4x4-play-singletask-task1-v0 / MinimalSB_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.4 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.3 -> 200000:0.4 -> 250000:0.3 -> 300000:0.3`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task1_MinimalSB_lam0p003_seed2/sd002_20260615_174043/eval.csv`

### selective_state_tuning_single4090 / puzzle-4x4-play-singletask-task1-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.5
- success_best: 0.5 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0.2 -> 250000:0.4 -> 300000:0.5`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task1_P0_particle_seed2/sd002_20260615_162552/eval.csv`

### selective_state_tuning_single4090 / puzzle-4x4-play-singletask-task1-v0 / R2_residual_disagree_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.5 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.3 -> 250000:0.5 -> 300000:0.2`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task1_R2_residual_disagree_lam0p001_seed2/sd002_20260615_224116/eval.csv`

### selective_state_tuning_single4090 / puzzle-4x4-play-singletask-task1-v0 / R3_residual_disagree_typicality_lam0p001 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.3
- success_best: 0.4 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.4 -> 250000:0.3 -> 300000:0.3`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task1_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260615_235715/eval.csv`

### selective_state_tuning_single4090 / puzzle-4x4-play-singletask-task3-v0 / MinimalSB_lam0p001 / seed 2 / INTERRUPTED

- final_step: 100000
- success_final: 0
- success_best: 0 @ 1
- trajectory_full: `1:0 -> 50000:0 -> 100000:0`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task3_MinimalSB_lam0p001_seed2/sd002_20260616_034310/eval.csv`

### selective_state_tuning_single4090 / puzzle-4x4-play-singletask-task3-v0 / MinimalSB_lam0p003 / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.1
- success_best: 0.4 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.2 -> 200000:0.2 -> 250000:0.4 -> 300000:0.1`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task3_MinimalSB_lam0p003_seed2/sd002_20260616_022811/eval.csv`

### selective_state_tuning_single4090 / puzzle-4x4-play-singletask-task3-v0 / P0_particle / seed 2 / COMPLETED

- final_step: 300000
- success_final: 0.2
- success_best: 0.6 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.4 -> 200000:0.6 -> 250000:0.3 -> 300000:0.2`
- eval_csv: `/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp/stageA_300k_puzzle_4x4_task3_P0_particle_seed2/sd002_20260616_011303/eval.csv`

### table3 / cube-double-play-singletask-task2-v0 / FullSafe / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.8
- success_best: 0.9 @ 650000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.4 -> 350000:0.5 -> 400000:0.4 -> 450000:0.7 -> 500000:0.6 -> 550000:0.6 -> 600000:0.8 -> 650000:0.9 -> 700000:0.8 -> 750000:0.9 -> 800000:0.8 -> 850000:0.9 -> 900000:0.7 -> 950000:0.7 -> 1000000:0.8`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-double-play-singletask-task2-v0_pm_fullsafe_official_highmem/sd000_20260526_110014/eval.csv`

### table3 / cube-double-play-singletask-task2-v0 / FullSafe / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0.9
- success_best: 0.9 @ 900000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0 -> 300000:0.1 -> 350000:0.2 -> 400000:0.1 -> 450000:0.2 -> 500000:0.2 -> 550000:0.7 -> 600000:0.4 -> 650000:0.7 -> 700000:0.7 -> 750000:0.8 -> 800000:0.6 -> 850000:0.8 -> 900000:0.9 -> 950000:0.8 -> 1000000:0.9`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-double-play-singletask-task2-v0_pm_fullsafe_official_highmem/sd001_20260526_150201/eval.csv`

### table3 / cube-double-play-singletask-task2-v0 / FullSafe / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 1
- success_best: 1 @ 750000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0.2 -> 300000:0.3 -> 350000:0.4 -> 400000:0.7 -> 450000:0.1 -> 500000:0.6 -> 550000:0.6 -> 600000:0.8 -> 650000:0.8 -> 700000:0.8 -> 750000:1 -> 800000:0.3 -> 850000:0.5 -> 900000:0.4 -> 950000:0.8 -> 1000000:1`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-double-play-singletask-task2-v0_pm_fullsafe_official_highmem/sd002_20260526_190350/eval.csv`

### table3 / cube-triple-play-singletask-task1-v0 / ActorGeo / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.6
- success_best: 0.9 @ 850000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.2 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0 -> 350000:0 -> 400000:0.1 -> 450000:0.4 -> 500000:0.1 -> 550000:0.2 -> 600000:0.2 -> 650000:0.3 -> 700000:0.5 -> 750000:0.7 -> 800000:0.8 -> 850000:0.9 -> 900000:0.7 -> 950000:0.9 -> 1000000:0.6`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/cube-triple-play-singletask-task1-v0_pm_actorgeo_problem_envs_4090/sd000_20260527_194651/eval.csv`

### table3 / cube-triple-play-singletask-task1-v0 / ActorGeo / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0.6
- success_best: 0.9 @ 850000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.1 -> 150000:0 -> 200000:0.4 -> 250000:0.2 -> 300000:0.2 -> 350000:0.2 -> 400000:0 -> 450000:0.2 -> 500000:0.2 -> 550000:0.3 -> 600000:0.6 -> 650000:0.5 -> 700000:0.2 -> 750000:0.3 -> 800000:0.5 -> 850000:0.9 -> 900000:0.6 -> 950000:0.7 -> 1000000:0.6`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/cube-triple-play-singletask-task1-v0_pm_actorgeo_problem_envs_4090/sd001_20260527_235654/eval.csv`

### table3 / cube-triple-play-singletask-task1-v0 / ActorGeo / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.4
- success_best: 0.8 @ 500000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.2 -> 300000:0.1 -> 350000:0.3 -> 400000:0.4 -> 450000:0.1 -> 500000:0.8 -> 550000:0.3 -> 600000:0.2 -> 650000:0.4 -> 700000:0.5 -> 750000:0.7 -> 800000:0.8 -> 850000:0.8 -> 900000:0.8 -> 950000:0.5 -> 1000000:0.4`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/cube-triple-play-singletask-task1-v0_pm_actorgeo_problem_envs_4090/sd002_20260528_040416/eval.csv`

### table3 / cube-triple-play-singletask-task1-v0 / FullSafe / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0
- success_best: 0.8 @ 850000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0.1 -> 400000:0 -> 450000:0 -> 500000:0 -> 550000:0.1 -> 600000:0 -> 650000:0 -> 700000:0.2 -> 750000:0 -> 800000:0.3 -> 850000:0.8 -> 900000:0.1 -> 950000:0.2 -> 1000000:0`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-triple-play-singletask-task1-v0_pm_fullsafe_official_highmem/sd000_20260526_230623/eval.csv`

### table3 / cube-triple-play-singletask-task1-v0 / FullSafe / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0.3
- success_best: 0.7 @ 250000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.2 -> 150000:0.4 -> 200000:0.2 -> 250000:0.7 -> 300000:0.3 -> 350000:0.2 -> 400000:0.5 -> 450000:0.3 -> 500000:0.3 -> 550000:0.3 -> 600000:0.3 -> 650000:0.5 -> 700000:0.2 -> 750000:0.3 -> 800000:0.6 -> 850000:0.4 -> 900000:0.7 -> 950000:0.7 -> 1000000:0.3`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-triple-play-singletask-task1-v0_pm_fullsafe_official_highmem/sd001_20260527_031556/eval.csv`

### table3 / cube-triple-play-singletask-task1-v0 / FullSafe / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.5
- success_best: 0.9 @ 850000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0.1 -> 350000:0.1 -> 400000:0 -> 450000:0.3 -> 500000:0.4 -> 550000:0.2 -> 600000:0.5 -> 650000:0.4 -> 700000:0.5 -> 750000:0.7 -> 800000:0.7 -> 850000:0.9 -> 900000:0.7 -> 950000:0.8 -> 1000000:0.5`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-triple-play-singletask-task1-v0_pm_fullsafe_official_highmem/sd002_20260527_072316/eval.csv`

### table3 / puzzle-3x3-play-singletask-task4-v0 / ActorGeo / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.7
- success_best: 0.7 @ 1000000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1 -> 350000:0 -> 400000:0.1 -> 450000:0.1 -> 500000:0.1 -> 550000:0.2 -> 600000:0.3 -> 650000:0.1 -> 700000:0.3 -> 750000:0.1 -> 800000:0.2 -> 850000:0.1 -> 900000:0.3 -> 950000:0.5 -> 1000000:0.7`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/puzzle-3x3-play-singletask-task4-v0_pm_actorgeo_problem_envs_4090/sd000_20260528_081013/eval.csv`

### table3 / puzzle-3x3-play-singletask-task4-v0 / ActorGeo / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 1
- success_best: 1 @ 1000000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0.1 -> 350000:0 -> 400000:0 -> 450000:0.2 -> 500000:0.1 -> 550000:0 -> 600000:0.1 -> 650000:0.1 -> 700000:0.4 -> 750000:0.3 -> 800000:0.2 -> 850000:0.7 -> 900000:0.4 -> 950000:0.8 -> 1000000:1`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/puzzle-3x3-play-singletask-task4-v0_pm_actorgeo_problem_envs_4090/sd001_20260528_121505/eval.csv`

### table3 / puzzle-3x3-play-singletask-task4-v0 / ActorGeo / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.2
- success_best: 0.3 @ 400000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0.1 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0.1 -> 400000:0.3 -> 450000:0 -> 500000:0 -> 550000:0.2 -> 600000:0.1 -> 650000:0.3 -> 700000:0 -> 750000:0 -> 800000:0.1 -> 850000:0.1 -> 900000:0 -> 950000:0 -> 1000000:0.2`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/puzzle-3x3-play-singletask-task4-v0_pm_actorgeo_problem_envs_4090/sd002_20260528_161947/eval.csv`

### table3 / puzzle-3x3-play-singletask-task4-v0 / FullSafe / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.7
- success_best: 0.7 @ 950000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0.1 -> 300000:0 -> 350000:0.1 -> 400000:0.1 -> 450000:0 -> 500000:0.4 -> 550000:0.2 -> 600000:0 -> 650000:0.1 -> 700000:0.5 -> 750000:0 -> 800000:0.4 -> 850000:0.4 -> 900000:0.6 -> 950000:0.7 -> 1000000:0.7`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/puzzle-3x3-play-singletask-task4-v0_pm_fullsafe_official_highmem/sd000_20260527_113023/eval.csv`

### table3 / puzzle-3x3-play-singletask-task4-v0 / FullSafe / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0.9
- success_best: 1 @ 850000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0 -> 250000:0 -> 300000:0 -> 350000:0 -> 400000:0 -> 450000:0.1 -> 500000:0.2 -> 550000:0.4 -> 600000:0.2 -> 650000:0.1 -> 700000:0.7 -> 750000:0.9 -> 800000:0.8 -> 850000:1 -> 900000:1 -> 950000:0.8 -> 1000000:0.9`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/puzzle-3x3-play-singletask-task4-v0_pm_fullsafe_official_highmem/sd001_20260527_153622/eval.csv`

### table3 / puzzle-4x4-play-singletask-task4-v0 / FullSafe / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 0.3
- success_best: 0.6 @ 350000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0.3 -> 300000:0.4 -> 350000:0.6 -> 400000:0.1 -> 450000:0.1 -> 500000:0.1 -> 550000:0.1 -> 600000:0.1 -> 650000:0 -> 700000:0 -> 750000:0.2 -> 800000:0.4 -> 850000:0.3 -> 900000:0.2 -> 950000:0 -> 1000000:0.3`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/puzzle-4x4-play-singletask-task4-v0_pm_fullsafe_light_remaining_single4090/sd000_20260528_220734/eval.csv`

### table3 / puzzle-4x4-play-singletask-task4-v0 / FullSafe / seed 1 / COMPLETED

- final_step: 700000
- success_final: 0
- success_best: 0.4 @ 300000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0.1 -> 200000:0.1 -> 250000:0.1 -> 300000:0.4 -> 350000:0 -> 400000:0.1 -> 450000:0.1 -> 500000:0 -> 550000:0.2 -> 600000:0.3 -> 650000:0.2 -> 700000:0`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/puzzle-4x4-play-singletask-task4-v0_pm_fullsafe_light_remaining_single4090/sd001_20260529_021519/eval.csv`

### table3 / puzzle-4x4-play-singletask-task4-v0 / FullSafe / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 0
- success_best: 0.5 @ 700000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.1 -> 250000:0 -> 300000:0.2 -> 350000:0 -> 400000:0.3 -> 450000:0.3 -> 500000:0.4 -> 550000:0.3 -> 600000:0.2 -> 650000:0.3 -> 700000:0.5 -> 750000:0.1 -> 800000:0.1 -> 850000:0.1 -> 900000:0.1 -> 950000:0 -> 1000000:0`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/puzzle-4x4-play-singletask-task4-v0_pm_fullsafe_light_remaining_single4090/sd001_20260529_100238/eval.csv`

### table3 / puzzle-4x4-play-singletask-task4-v0 / FullSafe / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 0.2
- success_best: 0.4 @ 200000
- trajectory_full: `1:0 -> 50000:0 -> 100000:0 -> 150000:0 -> 200000:0.4 -> 250000:0.3 -> 300000:0.2 -> 350000:0.1 -> 400000:0.3 -> 450000:0.1 -> 500000:0.4 -> 550000:0 -> 600000:0.3 -> 650000:0.2 -> 700000:0.4 -> 750000:0.2 -> 800000:0.1 -> 850000:0 -> 900000:0.2 -> 950000:0 -> 1000000:0.2`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/puzzle-4x4-play-singletask-task4-v0_pm_fullsafe_light_remaining_single4090/sd002_20260529_140824/eval.csv`

### table3 / scene-play-singletask-task2-v0 / FullSafe / seed 0 / COMPLETED

- final_step: 1000000
- success_final: 1
- success_best: 1 @ 200000
- trajectory_full: `1:0 -> 50000:0.8 -> 100000:0.7 -> 150000:0.9 -> 200000:1 -> 250000:1 -> 300000:1 -> 350000:1 -> 400000:1 -> 450000:1 -> 500000:1 -> 550000:1 -> 600000:1 -> 650000:1 -> 700000:1 -> 750000:1 -> 800000:1 -> 850000:1 -> 900000:1 -> 950000:1 -> 1000000:1`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/scene-play-singletask-task2-v0_pm_fullsafe_light_remaining_single4090/sd000_20260529_181552/eval.csv`

### table3 / scene-play-singletask-task2-v0 / FullSafe / seed 1 / COMPLETED

- final_step: 1000000
- success_final: 1
- success_best: 1 @ 50000
- trajectory_full: `1:0 -> 50000:1 -> 100000:0.9 -> 150000:0.8 -> 200000:0.9 -> 250000:1 -> 300000:0.9 -> 350000:1 -> 400000:1 -> 450000:1 -> 500000:0.9 -> 550000:1 -> 600000:1 -> 650000:1 -> 700000:1 -> 750000:1 -> 800000:0.9 -> 850000:1 -> 900000:1 -> 950000:1 -> 1000000:1`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/scene-play-singletask-task2-v0_pm_fullsafe_light_remaining_single4090/sd001_20260529_221332/eval.csv`

### table3 / scene-play-singletask-task2-v0 / FullSafe / seed 2 / COMPLETED

- final_step: 1000000
- success_final: 1
- success_best: 1 @ 150000
- trajectory_full: `1:0 -> 50000:0.7 -> 100000:0.9 -> 150000:1 -> 200000:1 -> 250000:1 -> 300000:1 -> 350000:0.9 -> 400000:1 -> 450000:1 -> 500000:1 -> 550000:1 -> 600000:1 -> 650000:1 -> 700000:1 -> 750000:1 -> 800000:1 -> 850000:1 -> 900000:1 -> 950000:0.9 -> 1000000:1`
- eval_csv: `/root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/scene-play-singletask-task2-v0_pm_fullsafe_light_remaining_single4090/sd002_20260530_021208/eval.csv`


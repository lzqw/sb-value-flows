# State 25-Task Coverage Matrix

Updated: 2026-06-21T13:33:54

Final values use the last eval.csv row only. Best and peak values are diagnostics and are not used as final performance.

## Coverage Counts

- 1M completed tasks: 6
- Candidate tasks: 1
- Collapsed tasks: 3
- 300k-only tasks: 5
- No-data tasks: 10
- Missing optional source files: none

## Matrix

| domain | task_id | env | VF_baseline | best_known_300k_final | best_known_300k_config | best_known_300k_seed | best_known_1M_final | best_known_1M_config | best_known_1M_seed | best_success | best_step | peak_after_500k | status | recommended_next_action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube-double-play | task1 | cube-double-play-singletask-task1-v0 | 0.97 |  |  |  |  |  |  |  |  |  | no_data | Priority 4: high-baseline coverage only; run at most P0 and R2 300k. |
| cube-double-play | task2 | cube-double-play-singletask-task2-v0 | 0.76 | 0.4 | R3_residual_disagree_typicality_lam0p001 | 2 | 0.9 | R3_residual_disagree_typicality_lam0p001 | 2 | 0.9 | 1000000 | 0.9 | 1M_completed | Locked: has useful completed 1M final; do not repeat ordinary tuning. |
| cube-double-play | task3 | cube-double-play-singletask-task3-v0 | 0.73 | 0.5 | A2_action_std_lam0p003 | 2 | 0.9 | A2_action_std_lam0p003 | 2 | 1.0 | 900000 | 1.0 | 1M_completed | Locked: has useful completed 1M final; do not repeat ordinary tuning. |
| cube-double-play | task4 | cube-double-play-singletask-task4-v0 | 0.3 | 0.3 | A1_action_std_lam0p001 | 2 | 0.5 | A1_action_std_lam0p001 | 2 | 0.7 | 800000 | 0.7 | 1M_completed | Locked: has useful completed 1M final; do not repeat ordinary tuning. |
| cube-double-play | task5 | cube-double-play-singletask-task5-v0 | 0.69 |  |  |  |  |  |  |  |  |  | no_data | Priority 1: no final row; run 300k coverage with P0 and R2. |
| cube-triple-play | task1 | cube-triple-play-singletask-task1-v0 | 0.59 |  |  |  |  |  |  |  |  |  | no_data | Priority 1: no final row; run 300k coverage with P0 and R2. |
| cube-triple-play | task2 | cube-triple-play-singletask-task2-v0 | 0.0 | 0.0 | A1_action_std_lam0p001 | 2 |  |  |  | 0.0 | 1 |  | 300k_only | 300k final exists but is not a good-case; keep for coverage, lower priority. |
| cube-triple-play | task3 | cube-triple-play-singletask-task3-v0 | 0.07 | 0.2 | R2_residual_disagree_lam0p001 | 2 |  |  |  | 0.2 | 300000 |  | candidate | Priority 3: good 300k final; consider 1M good-case confirmation. |
| cube-triple-play | task4 | cube-triple-play-singletask-task4-v0 | 0.0 | 0.0 | A1_action_std_lam0p001 | 2 |  |  |  | 0.0 | 1 |  | 300k_only | 300k final exists but is not a good-case; keep for coverage, lower priority. |
| cube-triple-play | task5 | cube-triple-play-singletask-task5-v0 | 0.02 | 0.0 | A1_action_std_lam0p001 | 2 |  |  |  | 0.0 | 1 |  | 300k_only | 300k final exists but is not a good-case; keep for coverage, lower priority. |
| puzzle-3x3-play | task1 | puzzle-3x3-play-singletask-task1-v0 | 0.99 |  |  |  |  |  |  |  |  |  | no_data | Priority 4: high-baseline coverage only; run at most P0 and R2 300k. |
| puzzle-3x3-play | task2 | puzzle-3x3-play-singletask-task2-v0 | 0.98 |  |  |  |  |  |  |  |  |  | no_data | Priority 4: high-baseline coverage only; run at most P0 and R2 300k. |
| puzzle-3x3-play | task3 | puzzle-3x3-play-singletask-task3-v0 | 0.97 | 0.2 | P0_particle | 2 |  |  |  | 0.4 | 250000 |  | 300k_only | 300k final exists but is not a good-case; keep for coverage, lower priority. |
| puzzle-3x3-play | task4 | puzzle-3x3-play-singletask-task4-v0 | 0.84 |  |  |  |  |  |  |  |  |  | no_data | Priority 1: no final row; run 300k coverage with P0 and R2. |
| puzzle-3x3-play | task5 | puzzle-3x3-play-singletask-task5-v0 | 0.58 | 0.4 | A1_action_std_lam0p001 | 2 |  |  |  | 0.4 | 300000 |  | 300k_only | 300k final exists but is not a good-case; keep for coverage, lower priority. |
| puzzle-4x4-play | task1 | puzzle-4x4-play-singletask-task1-v0 | 0.36 | 0.5 | A2_action_std_lam0p003 | 2 | 0.3 | A2_action_std_lam0p003 | 2 | 0.7 | 300000 | 0.5 | collapsed | Completed 1M final is weak/collapsed; prefer state_stable_v1 diagnostic, no seed extension. |
| puzzle-4x4-play | task2 | puzzle-4x4-play-singletask-task2-v0 | 0.27 | 0.2 | A2_action_std_lam0p003 | 2 | 0.5 | MinimalSB_lam0p001 | 2 | 0.6 | 950000 | 0.6 | 1M_completed | Locked: has useful completed 1M final; do not repeat ordinary tuning. |
| puzzle-4x4-play | task3 | puzzle-4x4-play-singletask-task3-v0 | 0.3 | 0.5 | R2_residual_disagree_lam0p001 | 2 | 0.4 | R2_residual_disagree_lam0p001 | 2 | 0.8 | 250000 | 0.7 | 1M_completed | Locked: has useful completed 1M final; do not repeat ordinary tuning. |
| puzzle-4x4-play | task4 | puzzle-4x4-play-singletask-task4-v0 | 0.28 | 0.5 | R3_residual_disagree_typicality_lam0p001 | 2 | 0.1 | R3_residual_disagree_typicality_lam0p001 | 2 | 0.5 | 850000 | 0.5 | collapsed | Completed 1M final is weak/collapsed; prefer state_stable_v1 diagnostic, no seed extension. |
| puzzle-4x4-play | task5 | puzzle-4x4-play-singletask-task5-v0 | 0.13 | 0.1 | A2_action_std_lam0p003 | 2 | 0.0 | A2_action_std_lam0p003 | 2 | 0.2 | 250000 | 0.1 | 1M_completed | Completed 1M exists; record final row and use curve diagnostics. |
| scene-play | task1 | scene-play-singletask-task1-v0 | 0.99 |  |  |  |  |  |  |  |  |  | no_data | Priority 4: high-baseline coverage only; run at most P0 and R2 300k. |
| scene-play | task2 | scene-play-singletask-task2-v0 | 0.97 |  |  |  |  |  |  |  |  |  | no_data | Priority 4: high-baseline coverage only; run at most P0 and R2 300k. |
| scene-play | task3 | scene-play-singletask-task3-v0 | 0.94 |  |  |  |  |  |  |  |  |  | no_data | Priority 4: high-baseline coverage only; run at most P0 and R2 300k. |
| scene-play | task4 | scene-play-singletask-task4-v0 | 0.07 | 0.4 | P0_particle | 2 | 0.0 | P0_particle | 2 | 0.9 | 100000 | 0.1 | collapsed | Completed 1M final is weak/collapsed; prefer state_stable_v1 diagnostic, no seed extension. |
| scene-play | task5 | scene-play-singletask-task5-v0 | 0.0 |  |  |  |  |  |  |  |  |  | no_data | Priority 1: no final row; run 300k coverage with P0 and R2. |

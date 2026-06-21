# State 25-Task Coverage Matrix

Updated: 2026-06-21T14:51:18

Final values use eval.csv last rows only. Best/peak columns are diagnostics and are not used as final performance.

## Coverage Counts

- Tasks with completed 1M final: 16
- Tasks with only completed 300k final: 4
- No-data tasks: 5
- Status counts: {'no_data': 5, '1M_completed': 13, 'collapsed': 3, '300k_only': 3, 'candidate': 1}

## Matrix

| domain | task_id | env | VF_baseline | best_known_300k_final | best_known_300k_config | best_known_300k_seed | best_known_1M_final | best_known_1M_config | best_known_1M_seed | best_success | best_step | peak_after_500k | status | recommended_next_action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube-double-play | task1 | cube-double-play-singletask-task1-v0 | 0.97 |  |  |  |  |  |  |  |  |  | no_data | Missing coverage priority 2: run one primary 300k before duplicate configs. |
| cube-double-play | task2 | cube-double-play-singletask-task2-v0 | 0.76 | 0.8 | R3_residual_disagree_typicality_lam0p001 | 0 | 1 | FullSafe | 2 | 1 | 750000 | 1 | 1M_completed | Skip: locked strong 1M R3/FullSafe; do not repeat ordinary tuning |
| cube-double-play | task3 | cube-double-play-singletask-task3-v0 | 0.73 | 0.5 | A2_action_std_lam0p003 | 2 | 0.9 | A2_action_std_lam0p003 | 2 | 1 | 700000 | 1 | 1M_completed | Skip: locked strong 1M A2; do not repeat ordinary tuning |
| cube-double-play | task4 | cube-double-play-singletask-task4-v0 | 0.3 | 0.3 | A1_action_std_lam0p001 | 2 | 0.5 | A1_action_std_lam0p001 | 2 | 0.7 | 800000 | 0.7 | 1M_completed | Skip: locked positive 1M A1; do not repeat ordinary tuning |
| cube-double-play | task5 | cube-double-play-singletask-task5-v0 | 0.69 |  |  |  |  |  |  |  |  |  | no_data | Missing coverage priority 1: run one primary 300k before duplicate configs. |
| cube-triple-play | task1 | cube-triple-play-singletask-task1-v0 | 0.59 |  |  |  | 0.6 | ActorGeo | 0 | 0.9 | 850000 | 0.9 | collapsed | Priority 2: collapse diagnostic; prefer state_stable_v1 before ordinary rerun. |
| cube-triple-play | task2 | cube-triple-play-singletask-task2-v0 | 0 | 0 | A1_action_std_lam0p001 | 2 |  |  |  | 0 | 1 |  | 300k_only | Covered by completed 300k final row; lower priority unless domain coverage requires it. |
| cube-triple-play | task3 | cube-triple-play-singletask-task3-v0 | 0.07 | 0.2 | R2_residual_disagree_lam0p001 | 2 |  |  |  | 0.2 | 300000 |  | candidate | Priority 3: good 300k final; consider 1M good-case confirmation. |
| cube-triple-play | task4 | cube-triple-play-singletask-task4-v0 | 0 | 0 | A1_action_std_lam0p001 | 2 |  |  |  | 0 | 1 |  | 300k_only | Covered by completed 300k final row; lower priority unless domain coverage requires it. |
| cube-triple-play | task5 | cube-triple-play-singletask-task5-v0 | 0.02 | 0 | A1_action_std_lam0p001 | 2 |  |  |  | 0 | 1 |  | 300k_only | Covered by completed 300k final row; lower priority unless domain coverage requires it. |
| puzzle-3x3-play | task1 | puzzle-3x3-play-singletask-task1-v0 | 0.99 |  |  |  | 1 | P0 | 5 | 1 | 100000 | 1 | 1M_completed | Covered by completed 1M final row; do not repeat unless explicitly requested. |
| puzzle-3x3-play | task2 | puzzle-3x3-play-singletask-task2-v0 | 0.98 |  |  |  | 1 | P0 | 5 | 1 | 400000 | 1 | 1M_completed | Covered by completed 1M final row; do not repeat unless explicitly requested. |
| puzzle-3x3-play | task3 | puzzle-3x3-play-singletask-task3-v0 | 0.97 | 0.2 | P0_particle | 2 | 0.1 | P0 | 5 | 0.4 | 250000 | 0.1 | 1M_completed | Covered by completed 1M final row; do not repeat unless explicitly requested. |
| puzzle-3x3-play | task4 | puzzle-3x3-play-singletask-task4-v0 | 0.84 |  |  |  | 1 | ActorGeo | 1 | 1 | 1000000 | 1 | 1M_completed | Covered by completed 1M final row; do not repeat unless explicitly requested. |
| puzzle-3x3-play | task5 | puzzle-3x3-play-singletask-task5-v0 | 0.58 | 0.4 | A1_action_std_lam0p001 | 2 | 1 | P0 | 5 | 1 | 1000000 | 1 | 1M_completed | Covered by completed 1M final row; do not repeat unless explicitly requested. |
| puzzle-4x4-play | task1 | puzzle-4x4-play-singletask-task1-v0 | 0.36 | 0.5 | A2_action_std_lam0p003 | 2 | 0.3 | A2_action_std_lam0p003 | 2 | 0.7 | 300000 | 0.5 | 1M_completed | Covered by completed 1M final row; do not repeat unless explicitly requested. |
| puzzle-4x4-play | task2 | puzzle-4x4-play-singletask-task2-v0 | 0.27 | 0.2 | A2_action_std_lam0p003 | 2 | 0.5 | MinimalSB_lam0p001 | 2 | 0.6 | 950000 | 0.6 | 1M_completed | Skip: locked weak positive MinimalSB; do not repeat ordinary tuning |
| puzzle-4x4-play | task3 | puzzle-4x4-play-singletask-task3-v0 | 0.3 | 0.5 | R2_residual_disagree_lam0p001 | 2 | 0.4 | R2_residual_disagree_lam0p001 | 2 | 0.8 | 250000 | 0.7 | collapsed | Priority 2: collapse diagnostic; prefer state_stable_v1 before ordinary rerun. |
| puzzle-4x4-play | task4 | puzzle-4x4-play-singletask-task4-v0 | 0.28 | 0.5 | R3_residual_disagree_typicality_lam0p001 | 2 | 0.3 | FullSafe | 0 | 0.6 | 350000 | 0.5 | 1M_completed | Covered by completed 1M final row; do not repeat unless explicitly requested. |
| puzzle-4x4-play | task5 | puzzle-4x4-play-singletask-task5-v0 | 0.13 | 0.1 | A2_action_std_lam0p003 | 2 | 0 | A2_action_std_lam0p003 | 2 | 0.2 | 250000 | 0.1 | 1M_completed | Covered by completed 1M final row; do not repeat unless explicitly requested. |
| scene-play | task1 | scene-play-singletask-task1-v0 | 0.99 |  |  |  |  |  |  |  |  |  | no_data | Missing coverage priority 4: run one primary 300k before duplicate configs. |
| scene-play | task2 | scene-play-singletask-task2-v0 | 0.97 |  |  |  | 1 | FullSafe | 0 | 1 | 200000 | 1 | 1M_completed | Covered by completed 1M final row; do not repeat unless explicitly requested. |
| scene-play | task3 | scene-play-singletask-task3-v0 | 0.94 |  |  |  |  |  |  |  |  |  | no_data | Missing coverage priority 5: run one primary 300k before duplicate configs. |
| scene-play | task4 | scene-play-singletask-task4-v0 | 0.07 | 0.4 | P0_particle | 2 | 0 | P0_particle | 2 | 0.9 | 100000 | 0.1 | collapsed | Priority 2: collapse diagnostic; prefer state_stable_v1 before ordinary rerun. |
| scene-play | task5 | scene-play-singletask-task5-v0 | 0 |  |  |  |  |  |  |  |  |  | no_data | Missing coverage priority 3: run one primary 300k before duplicate configs. |

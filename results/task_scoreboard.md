# Task Scoreboard

Final comparisons use completed final eval rows only. Peak values are not used as final results.

| env | modality | valueflow_success_mean | best_300k_success | best_300k_config | best_1m_success_mean | best_1m_success_std | best_1m_config | best_1m_delta | conclusion |
|---|---|---|---|---|---|---|---|---|---|
| cube-double-play-singletask-task1-v0 | state | 0.97 |  |  |  |  |  |  | No completed 1M result |
| cube-double-play-singletask-task2-v0 | state | 0.76 | 0.4 | R3_residual_disagree_typicality_lam0p001 | 0.833333 | 0.11547 | R3_residual_disagree_typicality_lam0p001 | 0.0733333 | Above Value Flow baseline |
| cube-double-play-singletask-task3-v0 | state | 0.73 | 0.5 | A2_action_std_lam0p003 | 0.833333 | 0.057735 | A2_action_std_lam0p003 | 0.103333 | Above Value Flow baseline |
| cube-double-play-singletask-task4-v0 | state | 0.3 | 0.3 | A1_action_std_lam0p001 | 0.4 | 0.1 | A1_action_std_lam0p001 | 0.1 | Above Value Flow baseline |
| cube-double-play-singletask-task5-v0 | state | 0.69 |  |  |  |  |  |  | No completed 1M result |
| cube-triple-play-singletask-task1-v0 | state | 0.59 |  |  |  |  |  |  | No completed 1M result |
| cube-triple-play-singletask-task2-v0 | state | 0 |  |  |  |  |  |  | No completed 1M result |
| cube-triple-play-singletask-task3-v0 | state | 0.07 | 0.1 | A1_action_std_lam0p001 |  |  |  |  | No completed 1M result |
| cube-triple-play-singletask-task4-v0 | state | 0 |  |  |  |  |  |  | No completed 1M result |
| cube-triple-play-singletask-task5-v0 | state | 0.02 |  |  |  |  |  |  | No completed 1M result |
| puzzle-3x3-play-singletask-task1-v0 | state | 0.99 |  |  |  |  |  |  | No completed 1M result |
| puzzle-3x3-play-singletask-task2-v0 | state | 0.98 |  |  |  |  |  |  | No completed 1M result |
| puzzle-3x3-play-singletask-task3-v0 | state | 0.97 | 0.2 | P0_particle |  |  |  |  | No completed 1M result |
| puzzle-3x3-play-singletask-task4-v0 | state | 0.84 |  |  |  |  |  |  | No completed 1M result |
| puzzle-3x3-play-singletask-task5-v0 | state | 0.58 |  |  |  |  |  |  | No completed 1M result |
| puzzle-4x4-play-singletask-task1-v0 | state | 0.36 | 0.5 | A2_action_std_lam0p003 |  |  |  |  | No completed 1M result |
| puzzle-4x4-play-singletask-task2-v0 | state | 0.27 | 0.2 | A2_action_std_lam0p003 | 0.333333 | 0.208167 | MinimalSB_lam0p001 | 0.0633333 | Weak or seed-unstable positive |
| puzzle-4x4-play-singletask-task3-v0 | state | 0.3 | 0.2 | P0_particle |  |  |  |  | No completed 1M result |
| puzzle-4x4-play-singletask-task4-v0 | state | 0.28 | 0.5 | R3_residual_disagree_typicality_lam0p001 | 0.1 | 0 | R3_residual_disagree_typicality_lam0p001 | -0.18 | 300k signal did not hold at 1M |
| puzzle-4x4-play-singletask-task5-v0 | state | 0.13 | 0.1 | A2_action_std_lam0p003 | 0 | 0 | A2_action_std_lam0p003 | -0.13 | Below Value Flow baseline |
| scene-play-singletask-task1-v0 | state | 0.99 |  |  |  |  |  |  | No completed 1M result |
| scene-play-singletask-task2-v0 | state | 0.97 |  |  |  |  |  |  | No completed 1M result |
| scene-play-singletask-task3-v0 | state | 0.94 |  |  |  |  |  |  | No completed 1M result |
| scene-play-singletask-task4-v0 | state | 0.07 | 0.4 | P0_particle | 0 | 0 | P0_particle | -0.07 | 300k signal did not hold at 1M |
| scene-play-singletask-task5-v0 | state | 0 |  |  |  |  |  |  | No completed 1M result |
| visual-antmaze-medium-navigate-singletask-task1-v0 | visual | 0.77 | 0.3 | R2_flow_residual_disagree_std_lam0p001 | 0.2 | 0 | R2_flow_residual_disagree_std_lam0p001 | -0.57 | Below Value Flow baseline |
| visual-antmaze-medium-navigate-singletask-task2-v0 | visual | 0.75 | 0.6 | R2_flow_residual_disagree_std_lam0p001 | 0.02 | 0 | R2_flow_residual_disagree_std_lam0p001 | -0.73 | Below Value Flow baseline |
| visual-antmaze-medium-navigate-singletask-task3-v0 | visual | 0.81 | 0.2 | A1_action_std_lam0p001 | 0.32 | 0 | R2_flow_residual_disagree_std_lam0p001 | -0.49 | Below Value Flow baseline |
| visual-antmaze-medium-navigate-singletask-task4-v0 | visual | 0.71 | 0.3 | A1_action_std_lam0p001 | 0.4 | 0 | R2_flow_residual_disagree_std_lam0p001 | -0.31 | Below Value Flow baseline |
| visual-antmaze-medium-navigate-singletask-task5-v0 | visual | 0.7 | 0.1 | A1_action_std_lam0p001 | 0.12 | 0 | R2_flow_residual_disagree_std_lam0p001 | -0.58 | Below Value Flow baseline |
| visual-antmaze-teleport-navigate-singletask-task1-v0 | visual | 0.1 | 0.1 | A1_action_std_lam0p001 | 0.08 | 0.0282843 | A1_action_std_lam0p001 | -0.02 | Below Value Flow baseline |
| visual-antmaze-teleport-navigate-singletask-task2-v0 | visual | 0.17 | 0 | A1_action_std_lam0p001 | 0.2 | 0 | R2_flow_residual_disagree_std_lam0p001 | 0.03 | Above Value Flow baseline |
| visual-antmaze-teleport-navigate-singletask-task3-v0 | visual | 0.16 | 0.3 | A1_action_std_lam0p001 | 0 | 0 | A1_action_std_lam0p001 | -0.16 | Below Value Flow baseline |
| visual-antmaze-teleport-navigate-singletask-task4-v0 | visual | 0.16 | 0.1 | R2_flow_residual_disagree_std_lam0p001 | 0.3 | 0 | R2_flow_residual_disagree_std_lam0p001 | 0.14 | Above Value Flow baseline |
| visual-antmaze-teleport-navigate-singletask-task5-v0 | visual | 0.08 | 0.1 | R2_flow_residual_disagree_std_lam0p001 | 0 | 0 | R2_flow_residual_disagree_std_lam0p001 | -0.08 | Below Value Flow baseline |
| visual-cube-double-play-singletask-task1-v0 | visual | 0.35 | 0.3 | A1_action_std_lam0p001 | 0.1 | 0 | A1_action_std_lam0p001 | -0.25 | Below Value Flow baseline |
| visual-cube-double-play-singletask-task2-v0 | visual | 0.04 | 0 | A1_action_std_lam0p001 | 0 | 0 | R2_flow_residual_disagree_std_lam0p001 | -0.04 | Below Value Flow baseline |
| visual-cube-double-play-singletask-task3-v0 | visual | 0.11 | 0 | A1_action_std_lam0p001 | 0.1 | 0 | R2_flow_residual_disagree_std_lam0p001 | -0.01 | Below Value Flow baseline |
| visual-cube-double-play-singletask-task4-v0 | visual | 0.02 | 0 | A1_action_std_lam0p001 | 0 | 0 | R2_flow_residual_disagree_std_lam0p001 | -0.02 | Below Value Flow baseline |
| visual-cube-double-play-singletask-task5-v0 | visual | 0.13 | 0 | A1_action_std_lam0p001 | 0 | 0 | R2_flow_residual_disagree_std_lam0p001 | -0.13 | Below Value Flow baseline |
| visual-puzzle-3x3-play-singletask-task1-v0 | visual | 0.93 |  |  |  |  |  |  | No completed 1M result |
| visual-puzzle-3x3-play-singletask-task2-v0 | visual | 0.12 |  |  |  |  |  |  | No completed 1M result |
| visual-puzzle-3x3-play-singletask-task3-v0 | visual | 0.03 |  |  |  |  |  |  | No completed 1M result |
| visual-puzzle-3x3-play-singletask-task4-v0 | visual | 0.06 |  |  |  |  |  |  | No completed 1M result |
| visual-puzzle-3x3-play-singletask-task5-v0 | visual | 0.02 |  |  |  |  |  |  | No completed 1M result |
| visual-scene-play-singletask-task1-v0 | visual | 0.99 | 1 | R2_flow_residual_disagree_std_lam0p001 |  |  |  |  | Stage-A only / no completed 1M confirmation |
| visual-scene-play-singletask-task2-v0 | visual | 0.4 | 0 | A1_action_std_lam0p001 |  |  |  |  | Stage-A only / no completed 1M confirmation |
| visual-scene-play-singletask-task3-v0 | visual | 0.66 | 0 | A1_action_std_lam0p001 |  |  |  |  | Stage-A only / no completed 1M confirmation |
| visual-scene-play-singletask-task4-v0 | visual | 0.1 | 0.1 | R2_flow_residual_disagree_std_lam0p001 |  |  |  |  | Stage-A only / no completed 1M confirmation |
| visual-scene-play-singletask-task5-v0 | visual | 0 | 0 | A1_action_std_lam0p001 |  |  |  |  | Stage-A only / no completed 1M confirmation |

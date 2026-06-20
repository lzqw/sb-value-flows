# Task Scoreboard

Last update: 2026-06-20 19:09:53

All comparisons use completed final eval rows. Peak success and best-in-run values are retained in CSV for diagnostics, but they do not replace final success.

## Strong Positives

1M mean > Value Flow baseline with modest seed variance.

| env | VF baseline | best 300k | best 1M mean +/- std | config | seeds | delta | run ids | eval paths |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cube-double-play-singletask-task2-v0 | 0.76 | 0.4 | 0.833333 +/- 0.11547 | R3_residual_disagree_typicality_lam0p001 | 0;1;2 | 0.0733333 | single4090__stageB_seedext_1m__cube-double-play-singletask-task2-v0__R3_residual_disagree_typicality_lam0p001__seed0__1000000__sd000_20260612_093350;single4090__stageB_seedext_1m__cube-double-play-singletask-task2-v0__R3_residual_disagree_typicality_lam0p001__seed1__1000000;single4090__stageB_seed2_1m__cube-double-play-singletask-task2-v0__R3_residual_disagree_typicality_lam0p001__seed2__1000000 | bad_task_repair_single4090/stageB_seedext_1m_cube_double_task2_R3_residual_disagree_typicality_lam0p001_seed0/sd000_20260612_093350/eval.csv<br>bad_task_repair_single4090/stageB_seedext_1m_cube_double_task2_R3_residual_disagree_typicality_lam0p001_seed1/sd001_20260612_133305/eval.csv<br>bad_task_repair_single4090/stageB_seed2_1m_cube_double_task2_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260611_203011/eval.csv |
| cube-double-play-singletask-task3-v0 | 0.73 | 0.5 | 0.833333 +/- 0.057735 | A2_action_std_lam0p003 | 0;1;2 | 0.103333 | single4090__stageB_seedext_1m__cube-double-play-singletask-task3-v0__A2_action_std_lam0p003__seed0__1000000;single4090__stageB_seedext_1m__cube-double-play-singletask-task3-v0__A2_action_std_lam0p003__seed1__1000000;single4090__stageB_seed2_1m__cube-double-play-singletask-task3-v0__A2_action_std_lam0p003__seed2__1000000 | bad_task_repair_single4090/stageB_seedext_1m_cube_double_task3_A2_action_std_lam0p003_seed0/sd000_20260612_213228/eval.csv<br>bad_task_repair_single4090/stageB_seedext_1m_cube_double_task3_A2_action_std_lam0p003_seed1/sd001_20260613_013227/eval.csv<br>bad_task_repair_single4090/stageB_seed2_1m_cube_double_task3_A2_action_std_lam0p003_seed2/sd002_20260612_173301/eval.csv |
| cube-double-play-singletask-task4-v0 | 0.3 | 0.3 | 0.4 +/- 0.1 | A1_action_std_lam0p001 | 0;1;2 | 0.1 | single4090__stageB_seedext_1m__cube-double-play-singletask-task4-v0__A1_action_std_lam0p001__seed0__1000000;single4090__stageB_seedext_1m__cube-double-play-singletask-task4-v0__A1_action_std_lam0p001__seed1__1000000;single4090__stageB_seed2_1m__cube-double-play-singletask-task4-v0__A1_action_std_lam0p001__seed2__1000000 | bad_task_repair_single4090/stageB_seedext_1m_cube_double_task4_A1_action_std_lam0p001_seed0/sd000_20260613_093038/eval.csv<br>bad_task_repair_single4090/stageB_seedext_1m_cube_double_task4_A1_action_std_lam0p001_seed1/sd001_20260613_133019/eval.csv<br>bad_task_repair_single4090/stageB_seed2_1m_cube_double_task4_A1_action_std_lam0p001_seed2/sd002_20260613_053127/eval.csv |
| puzzle-4x4-play-singletask-task3-v0 | 0.3 | 0.5 | 0.4 +/- 0 | R2_residual_disagree_lam0p001 | 2 | 0.1 | single4090__selective_state_stageB_1m__puzzle-4x4-play-singletask-task3-v0__R2_residual_disagree_lam0p001__seed2__1000000 | exp/stageB_1m_puzzle_4x4_task3_R2_residual_disagree_lam0p001_seed2/sd002_20260618_072723/eval.csv |

## Weak / Unstable Positives

1M mean is above baseline but the margin is small or seed variance is large.

| env | VF baseline | best 300k | best 1M mean +/- std | config | seeds | delta | run ids | eval paths |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| puzzle-4x4-play-singletask-task2-v0 | 0.27 | 0.2 | 0.333333 +/- 0.208167 | MinimalSB_lam0p001 | 0;1;2 | 0.0633333 | single4090__stageB_seedext_1m__puzzle-4x4-play-singletask-task2-v0__MinimalSB_lam0p001__seed0__1000000;single4090__stageB_seedext_1m__puzzle-4x4-play-singletask-task2-v0__MinimalSB_lam0p001__seed1__1000000;single4090__stageB_seed2_1m__puzzle-4x4-play-singletask-task2-v0__MinimalSB_lam0p001__seed2__1000000 | bad_task_repair_single4090/stageB_seedext_1m_puzzle_4x4_task2_MinimalSB_lam0p001_seed0/sd000_20260614_014306/eval.csv<br>bad_task_repair_single4090/stageB_seedext_1m_puzzle_4x4_task2_MinimalSB_lam0p001_seed1/sd001_20260614_055017/eval.csv<br>bad_task_repair_single4090/stageB_seed2_1m_puzzle_4x4_task2_MinimalSB_lam0p001_seed2/sd002_20260613_213740/eval.csv |

## Failed / False Positives

Completed 1M final success is below the Value Flow baseline after a Stage A selection or confirmation attempt.

| env | VF baseline | best 300k | best 1M mean +/- std | config | seeds | delta | run ids | eval paths |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| puzzle-4x4-play-singletask-task1-v0 | 0.36 | 0.5 | 0.3 +/- 0 | A2_action_std_lam0p003 | 2 | -0.06 | single4090__selective_state_stageB_1m__puzzle-4x4-play-singletask-task1-v0__A2_action_std_lam0p003__seed2__1000000 | exp/stageB_1m_puzzle_4x4_task1_A2_action_std_lam0p003_seed2/sd002_20260618_031757/eval.csv |
| puzzle-4x4-play-singletask-task4-v0 | 0.28 | 0.5 | 0.1 +/- 0 | R3_residual_disagree_typicality_lam0p001 | 2 | -0.18 | single4090__stageB_seed2_1m__puzzle-4x4-play-singletask-task4-v0__R3_residual_disagree_typicality_lam0p001__seed2__1000000 | bad_task_repair_single4090/stageB_seed2_1m_puzzle_4x4_task4_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260614_095700/eval.csv |
| puzzle-4x4-play-singletask-task5-v0 | 0.13 | 0.1 | 0 +/- 0 | A2_action_std_lam0p003 | 2 | -0.13 | single4090__stageB_seed2_1m__puzzle-4x4-play-singletask-task5-v0__A2_action_std_lam0p003__seed2__1000000 | bad_task_repair_single4090/stageB_seed2_1m_puzzle_4x4_task5_A2_action_std_lam0p003_seed2/sd002_20260613_173157/eval.csv |
| scene-play-singletask-task4-v0 | 0.07 | 0.4 | 0 +/- 0 | P0_particle | 2 | -0.07 | single4090__stageB_seed2_1m__scene-play-singletask-task4-v0__P0_particle__seed2__1000000 | bad_task_repair_single4090/stageB_seed2_1m_scene_task4_P0_particle_seed2/sd002_20260611_162414/eval.csv |

## Stage-A Only / No 1M Confirmation

Tasks with completed 300k screening results but no completed 1M confirmation in the registry.

| env | VF baseline | best 300k | config | seed | delta | run id | eval path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cube-triple-play-singletask-task2-v0 | 0 | 0 | A1_action_std_lam0p001 | 2 | 0 | single4090-new__state_goodcase_harvest_300k__cube-triple-play-singletask-task2-v0__A1_action_std_lam0p001__seed2__300000 | exp/goodcase300k_cube_triple_task2_A1_action_std_lam0p001_seed2/sd002_20260619_173909/eval.csv |
| cube-triple-play-singletask-task3-v0 | 0.07 | 0.2 | R2_residual_disagree_lam0p001 | 2 | 0.13 | single4090-new__state_goodcase_harvest_300k__cube-triple-play-singletask-task3-v0__R2_residual_disagree_lam0p001__seed2__300000 | exp/goodcase300k_cube_triple_task3_R2_residual_disagree_lam0p001_seed2/sd002_20260620_113121/eval.csv |
| cube-triple-play-singletask-task4-v0 | 0 | 0 | A1_action_std_lam0p001 | 2 | 0 | single4090-new__state_goodcase_harvest_300k__cube-triple-play-singletask-task4-v0__A1_action_std_lam0p001__seed2__300000 | exp/goodcase300k_cube_triple_task4_A1_action_std_lam0p001_seed2/sd002_20260619_224649/eval.csv |
| cube-triple-play-singletask-task5-v0 | 0.02 | 0 | A1_action_std_lam0p001 | 2 | -0.02 | single4090-new__state_goodcase_harvest_300k__cube-triple-play-singletask-task5-v0__A1_action_std_lam0p001__seed2__300000 | exp/goodcase300k_cube_triple_task5_A1_action_std_lam0p001_seed2/sd002_20260620_050930/eval.csv |
| puzzle-3x3-play-singletask-task3-v0 | 0.97 | 0.2 | P0_particle | 2 | -0.77 | single4090__stageA_300k__puzzle-3x3-play-singletask-task3-v0__P0_particle__seed2__300000 | bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_P0_particle_seed2/sd002_20260608_100720/eval.csv |
| puzzle-3x3-play-singletask-task5-v0 | 0.58 | 0.4 | A1_action_std_lam0p001 | 2 | -0.18 | single4090__stageA_300k__puzzle-3x3-play-singletask-task5-v0__A1_action_std_lam0p001__seed2__300000 | exp/stageA_300k_puzzle_3x3_task5_A1_action_std_lam0p001_seed2/sd002_20260616_204333/eval.csv |


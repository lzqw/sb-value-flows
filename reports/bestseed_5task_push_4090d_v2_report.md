# 4090D Best-Seed Five-Task Reliability SB v2

These are best-seed / 300k screening results, not full 8-seed official protocol.

## Data Status
- manifest path: `/root/.ogbench/data/manifest_after_hardlink_4090d.json`
- env complete: 25/25
- hardlink note: singletask task1..5 names are hardlinks to the corresponding base play datasets.

## CSV Finder Fix
- The old runner checked only `run_dir/eval.csv`, but `main.py` writes under nested `run_dir/.../sdXXX_*/eval.csv` directories.
- v2 recursively scans `run_dir.rglob('eval.csv')`, chooses the file with the most rows, then latest mtime.
- All CSV candidates and selected CSV paths are recorded per run.

## Queue A: cube-triple R2 seed2 1M
| task | paper VF | success | gap | return | length | selected_eval_csv | status |
|---|---:|---:|---:|---:|---:|---|---|
| cube-triple-play-singletask-task1-v0 | 59 +/- 12 | 0.7 | 0.11 | -574 | 574.7 | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueA_cube_triple_5task_1m/R2_flow_residual_disagree_std_lam0p001_cube-triple-play-singletask-task1-v0_seed2_1000000/bestseed_5task_v2_queueA_cube_triple_5task_1m_R2_flow_residual_disagree_std_lam0p001_cube-triple-play-singletask-task1-v0_seed2/sd002_20260604_202549/eval.csv` | COMPLETE |
| cube-triple-play-singletask-task2-v0 | 0 +/- 0 | 0 | 0 | -3000 | 1000 | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueA_cube_triple_5task_1m/R2_flow_residual_disagree_std_lam0p001_cube-triple-play-singletask-task2-v0_seed2_1000000/bestseed_5task_v2_queueA_cube_triple_5task_1m_R2_flow_residual_disagree_std_lam0p001_cube-triple-play-singletask-task2-v0_seed2/sd002_20260604_202548/eval.csv` | COMPLETE |
| cube-triple-play-singletask-task3-v0 | 7 +/- 3 | 0 | -0.07 | -2302.4 | 1000 | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueA_cube_triple_5task_1m/R2_flow_residual_disagree_std_lam0p001_cube-triple-play-singletask-task3-v0_seed2_1000000/bestseed_5task_v2_queueA_cube_triple_5task_1m_R2_flow_residual_disagree_std_lam0p001_cube-triple-play-singletask-task3-v0_seed2/sd002_20260605_005432/eval.csv` | COMPLETE |
| cube-triple-play-singletask-task4-v0 | 0 +/- 0 | 0 | 0 | -2847.3 | 1000 | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueA_cube_triple_5task_1m/R2_flow_residual_disagree_std_lam0p001_cube-triple-play-singletask-task4-v0_seed2_1000000/bestseed_5task_v2_queueA_cube_triple_5task_1m_R2_flow_residual_disagree_std_lam0p001_cube-triple-play-singletask-task4-v0_seed2/sd002_20260605_005803/eval.csv` | COMPLETE |
| cube-triple-play-singletask-task5-v0 | 2 +/- 1 | 0.1 | 0.08 | -2514.9 | 947.4 | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueA_cube_triple_5task_1m/R2_flow_residual_disagree_std_lam0p001_cube-triple-play-singletask-task5-v0_seed2_1000000/bestseed_5task_v2_queueA_cube_triple_5task_1m_R2_flow_residual_disagree_std_lam0p001_cube-triple-play-singletask-task5-v0_seed2/sd002_20260605_052016/eval.csv` | COMPLETE |

- cube-triple 5-task mean/std: 0.16 / 0.272764
- paper domain baseline: 14 +/- 3

## Queue B: cube-double / scene 300k screening
| domain | task | config | paper VF | success | gap | return | length | weight_max | ess | rel_mean | rel_std | flow_res_mean | disagree_mean | typicality_mean | collapse | selected_eval_csv | status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| cube-double | cube-double-play-singletask-task1-v0 | A1_action_std_lam0p001 | 97 +/- 1 | 1 | 0.03 | -161.1 | 162.1 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/A1_action_std_lam0p001_cube-double-play-singletask-task1-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_A1_action_std_lam0p001_cube-double-play-singletask-task1-v0_seed2/sd002_20260605_053047/eval.csv` | COMPLETE |
| cube-double | cube-double-play-singletask-task1-v0 | R2_flow_residual_disagree_std_lam0p001 | 97 +/- 1 | 0.9 | -0.07 | -202.3 | 203.2 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R2_flow_residual_disagree_std_lam0p001_cube-double-play-singletask-task1-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R2_flow_residual_disagree_std_lam0p001_cube-double-play-singletask-task1-v0_seed2/sd002_20260605_065051/eval.csv` | COMPLETE |
| cube-double | cube-double-play-singletask-task1-v0 | R3_flow_residual_disagree_typicality_std_lam0p001 | 97 +/- 1 | 0.8 | -0.17 | -202.1 | 202.9 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R3_flow_residual_disagree_typicality_std_lam0p001_cube-double-play-singletask-task1-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R3_flow_residual_disagree_typicality_std_lam0p001_cube-double-play-singletask-task1-v0_seed2/sd002_20260605_081126/eval.csv` | COMPLETE |
| cube-double | cube-double-play-singletask-task2-v0 | A1_action_std_lam0p001 | 76 +/- 7 | 0.3 | -0.46 | -718.6 | 396.3 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/A1_action_std_lam0p001_cube-double-play-singletask-task2-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_A1_action_std_lam0p001_cube-double-play-singletask-task2-v0_seed2/sd002_20260605_093200/eval.csv` | COMPLETE |
| cube-double | cube-double-play-singletask-task2-v0 | R2_flow_residual_disagree_std_lam0p001 | 76 +/- 7 | 0.2 | -0.56 | -772.4 | 442.7 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R2_flow_residual_disagree_std_lam0p001_cube-double-play-singletask-task2-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R2_flow_residual_disagree_std_lam0p001_cube-double-play-singletask-task2-v0_seed2/sd002_20260605_094401/eval.csv` | COMPLETE |
| cube-double | cube-double-play-singletask-task2-v0 | R3_flow_residual_disagree_typicality_std_lam0p001 | 76 +/- 7 | 0.3 | -0.46 | -762.5 | 395.1 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R3_flow_residual_disagree_typicality_std_lam0p001_cube-double-play-singletask-task2-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R3_flow_residual_disagree_typicality_std_lam0p001_cube-double-play-singletask-task2-v0_seed2/sd002_20260605_105235/eval.csv` | COMPLETE |
| cube-double | cube-double-play-singletask-task3-v0 | A1_action_std_lam0p001 | 73 +/- 4 | 0 | -0.73 | -955.9 | 500 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/A1_action_std_lam0p001_cube-double-play-singletask-task3-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_A1_action_std_lam0p001_cube-double-play-singletask-task3-v0_seed2/sd002_20260605_110234/eval.csv` | COMPLETE |
| cube-double | cube-double-play-singletask-task3-v0 | R2_flow_residual_disagree_std_lam0p001 | 73 +/- 4 | 0.5 | -0.23 | -613 | 329 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R2_flow_residual_disagree_std_lam0p001_cube-double-play-singletask-task3-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R2_flow_residual_disagree_std_lam0p001_cube-double-play-singletask-task3-v0_seed2/sd002_20260605_121339/eval.csv` | COMPLETE |
| cube-double | cube-double-play-singletask-task3-v0 | R3_flow_residual_disagree_typicality_std_lam0p001 | 73 +/- 4 | 0.4 | -0.33 | -661.1 | 368.6 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R3_flow_residual_disagree_typicality_std_lam0p001_cube-double-play-singletask-task3-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R3_flow_residual_disagree_typicality_std_lam0p001_cube-double-play-singletask-task3-v0_seed2/sd002_20260605_122109/eval.csv` | COMPLETE |
| cube-double | cube-double-play-singletask-task4-v0 | A1_action_std_lam0p001 | 30 +/- 5 | 0.1 | -0.2 | -912.5 | 481.8 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/A1_action_std_lam0p001_cube-double-play-singletask-task4-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_A1_action_std_lam0p001_cube-double-play-singletask-task4-v0_seed2/sd002_20260605_133443/eval.csv` | COMPLETE |
| cube-double | cube-double-play-singletask-task4-v0 | R2_flow_residual_disagree_std_lam0p001 | 30 +/- 5 | 0.1 | -0.2 | -934.1 | 469.2 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R2_flow_residual_disagree_std_lam0p001_cube-double-play-singletask-task4-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R2_flow_residual_disagree_std_lam0p001_cube-double-play-singletask-task4-v0_seed2/sd002_20260605_134014/eval.csv` | COMPLETE |
| cube-double | cube-double-play-singletask-task4-v0 | R3_flow_residual_disagree_typicality_std_lam0p001 | 30 +/- 5 | 0.1 | -0.2 | -887.3 | 479.5 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R3_flow_residual_disagree_typicality_std_lam0p001_cube-double-play-singletask-task4-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R3_flow_residual_disagree_typicality_std_lam0p001_cube-double-play-singletask-task4-v0_seed2/sd002_20260605_145548/eval.csv` | COMPLETE |
| cube-double | cube-double-play-singletask-task5-v0 | A1_action_std_lam0p001 | 69 +/- 5 | 0.7 | 0.01 | -479.8 | 291.7 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/A1_action_std_lam0p001_cube-double-play-singletask-task5-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_A1_action_std_lam0p001_cube-double-play-singletask-task5-v0_seed2/sd002_20260605_145918/eval.csv` | COMPLETE |
| cube-double | cube-double-play-singletask-task5-v0 | R2_flow_residual_disagree_std_lam0p001 | 69 +/- 5 | 0.3 | -0.39 | -680.3 | 394.8 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R2_flow_residual_disagree_std_lam0p001_cube-double-play-singletask-task5-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R2_flow_residual_disagree_std_lam0p001_cube-double-play-singletask-task5-v0_seed2/sd002_20260605_161722/eval.csv` | COMPLETE |
| cube-double | cube-double-play-singletask-task5-v0 | R3_flow_residual_disagree_typicality_std_lam0p001 | 69 +/- 5 | 0.5 | -0.19 | -640.4 | 400.9 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R3_flow_residual_disagree_typicality_std_lam0p001_cube-double-play-singletask-task5-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R3_flow_residual_disagree_typicality_std_lam0p001_cube-double-play-singletask-task5-v0_seed2/sd002_20260605_161754/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task1-v0 | A1_action_std_lam0p001 | 99 +/- 0 | 1 | 0.01 | -92.5 | 71.1 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/A1_action_std_lam0p001_scene-play-singletask-task1-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_A1_action_std_lam0p001_scene-play-singletask-task1-v0_seed2/sd002_20260605_173657/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task1-v0 | R2_flow_residual_disagree_std_lam0p001 | 99 +/- 0 | 1 | 0.01 | -108.5 | 78.6 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task1-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task1-v0_seed2/sd002_20260605_173857/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task1-v0 | R3_flow_residual_disagree_typicality_std_lam0p001 | 99 +/- 0 | 1 | 0.01 | -107.3 | 85.6 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R3_flow_residual_disagree_typicality_std_lam0p001_scene-play-singletask-task1-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R3_flow_residual_disagree_typicality_std_lam0p001_scene-play-singletask-task1-v0_seed2/sd002_20260605_185431/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task2-v0 | A1_action_std_lam0p001 | 97 +/- 1 | 1 | 0.03 | -399.4 | 210.8 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/A1_action_std_lam0p001_scene-play-singletask-task2-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_A1_action_std_lam0p001_scene-play-singletask-task2-v0_seed2/sd002_20260605_185931/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task2-v0 | R2_flow_residual_disagree_std_lam0p001 | 97 +/- 1 | 1 | 0.03 | -425.8 | 232.5 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task2-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task2-v0_seed2/sd002_20260605_201235/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task2-v0 | R3_flow_residual_disagree_typicality_std_lam0p001 | 97 +/- 1 | 1 | 0.03 | -505 | 267 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R3_flow_residual_disagree_typicality_std_lam0p001_scene-play-singletask-task2-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R3_flow_residual_disagree_typicality_std_lam0p001_scene-play-singletask-task2-v0_seed2/sd002_20260605_202006/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task3-v0 | A1_action_std_lam0p001 | 94 +/- 2 | 0.8 | -0.14 | -606.8 | 336.5 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/A1_action_std_lam0p001_scene-play-singletask-task3-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_A1_action_std_lam0p001_scene-play-singletask-task3-v0_seed2/sd002_20260605_213110/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task3-v0 | R2_flow_residual_disagree_std_lam0p001 | 94 +/- 2 | 0.7 | -0.24 | -889.3 | 437.1 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task3-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task3-v0_seed2/sd002_20260605_214111/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task3-v0 | R3_flow_residual_disagree_typicality_std_lam0p001 | 94 +/- 2 | 0.8 | -0.14 | -698.5 | 367.3 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R3_flow_residual_disagree_typicality_std_lam0p001_scene-play-singletask-task3-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R3_flow_residual_disagree_typicality_std_lam0p001_scene-play-singletask-task3-v0_seed2/sd002_20260605_224944/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task4-v0 | A1_action_std_lam0p001 | 7 +/- 4 | 0 | -0.07 | -836.8 | 750 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/A1_action_std_lam0p001_scene-play-singletask-task4-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_A1_action_std_lam0p001_scene-play-singletask-task4-v0_seed2/sd002_20260605_230315/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task4-v0 | R2_flow_residual_disagree_std_lam0p001 | 7 +/- 4 | 0.1 | 0.03 | -952 | 722 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task4-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task4-v0_seed2/sd002_20260606_000918/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task4-v0 | R3_flow_residual_disagree_typicality_std_lam0p001 | 7 +/- 4 | 0 | -0.07 | -860.6 | 750 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R3_flow_residual_disagree_typicality_std_lam0p001_scene-play-singletask-task4-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R3_flow_residual_disagree_typicality_std_lam0p001_scene-play-singletask-task4-v0_seed2/sd002_20260606_002549/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task5-v0 | A1_action_std_lam0p001 | 0 +/- 0 | 0 | 0 | -1500 | 750 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/A1_action_std_lam0p001_scene-play-singletask-task5-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_A1_action_std_lam0p001_scene-play-singletask-task5-v0_seed2/sd002_20260606_012953/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task5-v0 | R2_flow_residual_disagree_std_lam0p001 | 0 +/- 0 | 0 | 0 | -1500 | 750 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task5-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task5-v0_seed2/sd002_20260606_014854/eval.csv` | COMPLETE |
| scene-play | scene-play-singletask-task5-v0 | R3_flow_residual_disagree_typicality_std_lam0p001 | 0 +/- 0 | 0 | 0 | -1503.4 | 750 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/bestseed_5task_push_4090d_v2/queueB_screen_300k/R3_flow_residual_disagree_typicality_std_lam0p001_scene-play-singletask-task5-v0_seed2_300000/bestseed_5task_v2_queueB_screen_300k_R3_flow_residual_disagree_typicality_std_lam0p001_scene-play-singletask-task5-v0_seed2/sd002_20260606_025057/eval.csv` | COMPLETE |

## Best Configs

### cube-double
- cube-double-play-singletask-task1-v0: A1_action_std_lam0p001 success=1 return=-161.1
- cube-double-play-singletask-task2-v0: A1_action_std_lam0p001 success=0.3 return=-718.6
- cube-double-play-singletask-task3-v0: R2_flow_residual_disagree_std_lam0p001 success=0.5 return=-613
- cube-double-play-singletask-task4-v0: R3_flow_residual_disagree_typicality_std_lam0p001 success=0.1 return=-887.3
- cube-double-play-singletask-task5-v0: A1_action_std_lam0p001 success=0.7 return=-479.8
- domain config avg A1_action_std_lam0p001: 0.42 / 0.376298
- domain config avg R2_flow_residual_disagree_std_lam0p001: 0.4 / 0.282843
- domain config avg R3_flow_residual_disagree_typicality_std_lam0p001: 0.42 / 0.231517

### scene

## Failed / Warned Runs

- none

## Git
- branch: `reliability-calibrated-sb`
- HEAD: `31b27a52fbeb39ad6e7748225ad3221772c93661`
```
M reports/bestseed_5task_push_4090d_report.md
?? reports/bestseed_5task_push_4090d_v2_report.md
?? reports/fix_2x4090_mujoco_osmesa_report.md
?? reports/fix_2x4090_value_flows_env_report.md
?? reports/fullsafe_light_seed_extension_4090d_report.md
?? reports/matched_origin_vs_fullsafe_4090d_report.md
?? reports/minimal_sb_1m_confirm_4090d_report.md
?? reports/minimal_sb_1m_diagnostic_audit_4090d.md
?? reports/minimal_sb_300k_screening_4090d_report.md
?? reports/minimal_sb_reweight_smoke_report.md
?? reports/overnight_reliability_sb_4090d_report.md
?? reports/pm_fullsafe_light_overnight_tune_4090d_report.md
?? reports/postrun_4090d_after_light_tune_report.md
?? reports/reliability_calibrated_sb_code_check_failed.md
?? reports/table3_pm_fullres_problem_envs_2x4090_report.md
?? reports/table3_pm_fullsafe_light_problem_envs_2x4090_report.md
?? reports/table3_pm_fullsafe_official_2x4090_parallel_report.md
?? reports/table3_pm_success_audit_2x4090.md
?? scripts/audit_minimal_sb_1m_diagnostics_4090d.py
?? scripts/audit_pm_success_2x4090.py
?? scripts/postrun_4090d_after_light_tune.py
?? scripts/run_bestseed_5task_push_4090d_v2.py
?? scripts/run_fullsafe_light_seed_extension_4090d.py
?? scripts/run_matched_origin_vs_fullsafe_4090d.py
?? scripts/run_minimal_sb_1m_confirm_4090d.py
?? scripts/run_minimal_sb_300k_screening_4090d.py
?? scripts/run_minimal_sb_smoke_4090d.py
?? scripts/run_overnight_reliability_sb_4090d.py
?? scripts/run_pm_fullsafe_light_overnight_tune_4090d.py
?? scripts/run_push_reliability_sb_4090d.py
?? scripts/run_table3_pm_fullres_problem_envs_2x4090.py
?? scripts/run_table3_pm_fullsafe_light_problem_envs_2x4090.py
?? scripts/run_table3_pm_fullsafe_official_2x4090_parallel.py
```

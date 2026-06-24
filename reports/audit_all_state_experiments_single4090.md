# Audit All Single4090 State Experiments

Updated: 2026-06-24T21:20:48

No training is launched by this audit. It reports both final-row and best-peak result views.

## Result Definitions

- `final_success` = success in the last row of eval.csv.
- `best_peak_success` = highest success across all eval checkpoints in eval.csv.
- `best_peak_step` = step where the highest success occurred.
- `peak_after_500k_success` = highest success among eval rows with step >= 500k.
- `drop_final_from_peak` = `final_success - best_peak_success`.
- Partial runs keep their best peak diagnostics, but their final row is not treated as completed final.

## File Scan

- Candidate files: 743
- eval.csv: 224
- train.csv: 223
- command.txt: 11
- Unique audited runs: 165
- Missing lightweight sources: none

## Status Counts

- completed_300k: 119
- completed_1m: 45
- partial: 1

## Root Path Counts

- `/root/sb-value-flows/exp`: 108
- `/root/autodl-tmp/sb-value-flows-runs`: 57

## Domain Summary

| domain | domain_best_peak_mean | domain_best_peak_mean_missing_as_zero | domain_best_final_mean | domain_best_final_mean_missing_as_zero | domain_best_peak_available_tasks | domain_best_final_available_tasks |
|---|---|---|---|---|---|---|
| cube-double-play | 0.84 | 0.84 | 0.78 | 0.78 | 5 | 5 |
| cube-triple-play | 0.22 | 0.22 | 0.16 | 0.16 | 5 | 5 |
| puzzle-3x3-play | 0.88 | 0.88 | 0.84 | 0.84 | 5 | 5 |
| puzzle-4x4-play | 0.58 | 0.58 | 0.42 | 0.42 | 5 | 5 |
| scene-play | 0.78 | 0.78 | 0.68 | 0.68 | 5 | 5 |

## Top 10 Best Peak Runs

| env | config_name | seed | status | best_peak_success | best_peak_step | final_success | drop_final_from_peak | eval_csv |
|---|---|---|---|---|---|---|---|---|
| cube-double-play-singletask-task1-v0 | FullSafe | 2 | completed_300k | 1.0 | 300000 | 1.0 | 0.0 | /root/autodl-tmp/sb-value-flows-runs/state_main_table_peak_polish_single4090/exp/peakpolish_300k_cube_double_task1_FullSafe_seed2/sd002_20260624_200707/eval.csv |
| cube-double-play-singletask-task2-v0 | FullSafe | 2 | completed_1m | 1.0 | 750000 | 1.0 | 0.0 | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-double-play-singletask-task2-v0_pm_fullsafe_official_highmem/sd002_20260526_190350/eval.csv |
| cube-double-play-singletask-task3-v0 | A2_action_std_lam0p003 | 0 | completed_1m | 1.0 | 700000 | 0.8 | -0.19999999999999996 | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task3_A2_action_std_lam0p003_seed0/sd000_20260612_213228/eval.csv |
| cube-double-play-singletask-task3-v0 | A2_action_std_lam0p003 | 1 | completed_1m | 1.0 | 800000 | 0.8 | -0.19999999999999996 | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task3_A2_action_std_lam0p003_seed1/sd001_20260613_013227/eval.csv |
| cube-double-play-singletask-task3-v0 | A2_action_std_lam0p003 | 2 | completed_1m | 1.0 | 900000 | 0.9 | -0.09999999999999998 | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_cube_double_task3_A2_action_std_lam0p003_seed2/sd002_20260612_173301/eval.csv |
| puzzle-3x3-play-singletask-task1-v0 | P0 | 5 | completed_1m | 1.0 | 100000 | 1.0 | 0.0 | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task1_S1_sb_lam0p001_seed2/sd002_20260606_142934/eval.csv |
| puzzle-3x3-play-singletask-task2-v0 | P0 | 5 | completed_1m | 1.0 | 400000 | 1.0 | 0.0 | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task2_S1_sb_lam0p001_seed2/sd002_20260606_182634/eval.csv |
| puzzle-3x3-play-singletask-task4-v0 | ActorGeo | 1 | completed_1m | 1.0 | 1000000 | 1.0 | 0.0 | /root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/puzzle-3x3-play-singletask-task4-v0_pm_actorgeo_problem_envs_4090/sd001_20260528_121505/eval.csv |
| puzzle-3x3-play-singletask-task4-v0 | FullSafe | 1 | completed_1m | 1.0 | 850000 | 0.9 | -0.09999999999999998 | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/puzzle-3x3-play-singletask-task4-v0_pm_fullsafe_official_highmem/sd001_20260527_153622/eval.csv |
| puzzle-3x3-play-singletask-task4-v0 | P0 | 5 | completed_1m | 1.0 | 850000 | 1.0 | 0.0 | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task4_S1_sb_lam0p001_seed2/sd002_20260607_022834/eval.csv |

## Top 10 Final Completed Runs

| env | config_name | seed | status | final_success | best_peak_success | best_peak_step | eval_csv |
|---|---|---|---|---|---|---|---|
| cube-double-play-singletask-task1-v0 | FullSafe | 2 | completed_300k | 1.0 | 1.0 | 300000 | /root/autodl-tmp/sb-value-flows-runs/state_main_table_peak_polish_single4090/exp/peakpolish_300k_cube_double_task1_FullSafe_seed2/sd002_20260624_200707/eval.csv |
| cube-double-play-singletask-task2-v0 | FullSafe | 2 | completed_1m | 1.0 | 1.0 | 750000 | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-double-play-singletask-task2-v0_pm_fullsafe_official_highmem/sd002_20260526_190350/eval.csv |
| puzzle-3x3-play-singletask-task1-v0 | P0 | 5 | completed_1m | 1.0 | 1.0 | 100000 | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task1_S1_sb_lam0p001_seed2/sd002_20260606_142934/eval.csv |
| puzzle-3x3-play-singletask-task2-v0 | P0 | 5 | completed_1m | 1.0 | 1.0 | 400000 | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task2_S1_sb_lam0p001_seed2/sd002_20260606_182634/eval.csv |
| puzzle-3x3-play-singletask-task4-v0 | ActorGeo | 1 | completed_1m | 1.0 | 1.0 | 1000000 | /root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/puzzle-3x3-play-singletask-task4-v0_pm_actorgeo_problem_envs_4090/sd001_20260528_121505/eval.csv |
| puzzle-3x3-play-singletask-task4-v0 | P0 | 5 | completed_1m | 1.0 | 1.0 | 850000 | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task4_S1_sb_lam0p001_seed2/sd002_20260607_022834/eval.csv |
| puzzle-3x3-play-singletask-task5-v0 | P0 | 5 | completed_1m | 1.0 | 1.0 | 1000000 | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task5_S1_sb_lam0p001_seed2/sd002_20260607_063032/eval.csv |
| scene-play-singletask-task1-v0 | P0_particle | 2 | completed_300k | 1.0 | 1.0 | 100000 | /root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090/exp/state25_300k_coverage_scene_task1_P0_particle_seed2/sd002_20260621_231247/eval.csv |
| scene-play-singletask-task2-v0 | FullSafe | 0 | completed_1m | 1.0 | 1.0 | 200000 | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/scene-play-singletask-task2-v0_pm_fullsafe_light_remaining_single4090/sd000_20260529_181552/eval.csv |
| scene-play-singletask-task2-v0 | FullSafe | 1 | completed_1m | 1.0 | 1.0 | 50000 | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/scene-play-singletask-task2-v0_pm_fullsafe_light_remaining_single4090/sd001_20260529_221332/eval.csv |

## Top 10 Collapse Cases

| env | config_name | seed | status | final_success | best_peak_success | best_peak_step | drop_final_from_peak | recommended_fix |
|---|---|---|---|---|---|---|---|---|
| scene-play-singletask-task4-v0 | A2_action_std_lam0p003 | 2 | completed_300k | 0.0 | 0.9 | 100000 | -0.9 | use state_stable_v1; lower actor lr after peak; actor anchor; SB weight cap/logit clip/uniform mix; save best checkpoint but do not call it final |
| scene-play-singletask-task4-v0 | P0_particle | 2 | completed_1m | 0.0 | 0.9 | 100000 | -0.9 | use state_stable_v1; lower actor lr after peak; actor anchor; SB weight cap/logit clip/uniform mix; save best checkpoint but do not call it final |
| scene-play-singletask-task4-v0 | A2_action_std_lam0p003 | 2 | completed_300k | 0.1 | 0.9 | 100000 | -0.8 | use state_stable_v1; lower actor lr after peak; actor anchor; SB weight cap/logit clip/uniform mix; save best checkpoint but do not call it final |
| cube-triple-play-singletask-task1-v0 | FullSafe | 2 | completed_1m | 0.5 | 0.9 | 850000 | -0.4 | use state_stable_v1; lower actor lr after peak; actor anchor; SB weight cap/logit clip/uniform mix; save best checkpoint but do not call it final |
| cube-triple-play-singletask-task1-v0 | ActorGeo | 0 | completed_1m | 0.6 | 0.9 | 850000 | -0.30000000000000004 | use state_stable_v1; lower actor lr after peak; actor anchor; SB weight cap/logit clip/uniform mix; save best checkpoint but do not call it final |
| cube-triple-play-singletask-task1-v0 | ActorGeo | 1 | completed_1m | 0.6 | 0.9 | 850000 | -0.30000000000000004 | use state_stable_v1; lower actor lr after peak; actor anchor; SB weight cap/logit clip/uniform mix; save best checkpoint but do not call it final |
| cube-triple-play-singletask-task1-v0 | FullSafe | 0 | completed_1m | 0.0 | 0.8 | 850000 | -0.8 | use state_stable_v1; lower actor lr after peak; actor anchor; SB weight cap/logit clip/uniform mix; save best checkpoint but do not call it final |
| scene-play-singletask-task4-v0 | MinimalSB_lam0p0003 | 2 | completed_300k | 0.2 | 0.8 | 100000 | -0.6000000000000001 | use state_stable_v1; lower actor lr after peak; actor anchor; SB weight cap/logit clip/uniform mix; save best checkpoint but do not call it final |
| scene-play-singletask-task4-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | completed_300k | 0.2 | 0.8 | 100000 | -0.6000000000000001 | use state_stable_v1; lower actor lr after peak; actor anchor; SB weight cap/logit clip/uniform mix; save best checkpoint but do not call it final |
| cube-triple-play-singletask-task1-v0 | ActorGeo | 2 | completed_1m | 0.4 | 0.8 | 500000 | -0.4 | use state_stable_v1; lower actor lr after peak; actor anchor; SB weight cap/logit clip/uniform mix; save best checkpoint but do not call it final |

## No Data Tasks

- None.

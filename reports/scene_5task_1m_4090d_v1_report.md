# Scene Five-Task 1M Reliability SB v1

These are best-seed single-seed 5-task 1M results, not full 8-seed official protocol.

## Data Status
- manifest path: `/root/.ogbench/data/manifest_after_hardlink_4090d.json`
- env complete: unknown
- hardlink note: singletask task1..5 names were completed by hardlinks to base play datasets where needed.

## CSV Parsing
- Results use the final row of the selected `eval.csv` only; no mean, max, or best checkpoint is used.
- The runner recursively scans each run directory, chooses the `eval.csv` with the most rows, then latest mtime.

## A1 action_std lambda=0.001
| task | paper VF | success | gap | return | length | weight_max | ess | rel_mean | rel_std | flow_res_mean | disagree_mean | typicality_mean | collapse | selected_eval_csv | status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| scene-play-singletask-task1-v0 | 99 +/- 0 | 1 | 0.01 | -142.8 | 101.5 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/A1_action_std_lam0p001_scene-play-singletask-task1-v0_seed2_1000000/scene_5task_1m_v1_A1_action_std_lam0p001_scene-play-singletask-task1-v0_seed2/sd002_20260606_142510/eval.csv` | COMPLETE |
| scene-play-singletask-task2-v0 | 97 +/- 1 | 1 | 0.03 | -363.4 | 193.7 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/A1_action_std_lam0p001_scene-play-singletask-task2-v0_seed2_1000000/scene_5task_1m_v1_A1_action_std_lam0p001_scene-play-singletask-task2-v0_seed2/sd002_20260606_184523/eval.csv` | COMPLETE |
| scene-play-singletask-task3-v0 | 94 +/- 2 | 1 | 0.06 | -409.8 | 217.1 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/A1_action_std_lam0p001_scene-play-singletask-task3-v0_seed2_1000000/scene_5task_1m_v1_A1_action_std_lam0p001_scene-play-singletask-task3-v0_seed2/sd002_20260606_230708/eval.csv` | COMPLETE |
| scene-play-singletask-task4-v0 | 7 +/- 4 | 0 | -0.07 | -770.8 | 750 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/A1_action_std_lam0p001_scene-play-singletask-task4-v0_seed2_1000000/scene_5task_1m_v1_A1_action_std_lam0p001_scene-play-singletask-task4-v0_seed2/sd002_20260607_033023/eval.csv` | COMPLETE |
| scene-play-singletask-task5-v0 | 0 +/- 0 | 0 | 0 | -897.2 | 750 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/A1_action_std_lam0p001_scene-play-singletask-task5-v0_seed2_1000000/scene_5task_1m_v1_A1_action_std_lam0p001_scene-play-singletask-task5-v0_seed2/sd002_20260607_075709/eval.csv` | COMPLETE |

- A1 action_std lambda=0.001 5-task mean/std: 0.6 / 0.489898
- paper domain baseline: 59 +/- 4

## R2 flow_residual_disagree std lambda=0.001
| task | paper VF | success | gap | return | length | weight_max | ess | rel_mean | rel_std | flow_res_mean | disagree_mean | typicality_mean | collapse | selected_eval_csv | status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| scene-play-singletask-task1-v0 | 99 +/- 0 | 1 | 0.01 | -111.2 | 79.4 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task1-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task1-v0_seed2/sd002_20260606_142510/eval.csv` | COMPLETE |
| scene-play-singletask-task2-v0 | 97 +/- 1 | 1 | 0.03 | -380.7 | 212 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task2-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task2-v0_seed2/sd002_20260606_183923/eval.csv` | COMPLETE |
| scene-play-singletask-task3-v0 | 94 +/- 2 | 1 | 0.06 | -348.2 | 176.8 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task3-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task3-v0_seed2/sd002_20260606_225507/eval.csv` | COMPLETE |
| scene-play-singletask-task4-v0 | 7 +/- 4 | 0 | -0.07 | -769.7 | 750 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task4-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task4-v0_seed2/sd002_20260607_031022/eval.csv` | COMPLETE |
| scene-play-singletask-task5-v0 | 0 +/- 0 | 0 | 0 | -882.2 | 750 | nan | nan | nan | nan | nan | nan | nan | False | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task5-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task5-v0_seed2/sd002_20260607_073207/eval.csv` | COMPLETE |

- R2 flow_residual_disagree std lambda=0.001 5-task mean/std: 0.6 / 0.489898
- paper domain baseline: 59 +/- 4

## Failed / Warned Runs

- none

## Git
- branch: `reliability-calibrated-sb`
- HEAD: `0b28f867d76211adb6c314805c25c442a5572081`
```
M reports/bestseed_5task_push_4090d_report.md
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
?? reports/scene_5task_1m_4090d_v1_report.md
?? reports/table3_pm_fullres_problem_envs_2x4090_report.md
?? reports/table3_pm_fullsafe_light_problem_envs_2x4090_report.md
?? reports/table3_pm_fullsafe_official_2x4090_parallel_report.md
?? reports/table3_pm_success_audit_2x4090.md
?? scripts/audit_minimal_sb_1m_diagnostics_4090d.py
?? scripts/audit_pm_success_2x4090.py
?? scripts/postrun_4090d_after_light_tune.py
?? scripts/run_fullsafe_light_seed_extension_4090d.py
?? scripts/run_matched_origin_vs_fullsafe_4090d.py
?? scripts/run_minimal_sb_1m_confirm_4090d.py
?? scripts/run_minimal_sb_300k_screening_4090d.py
?? scripts/run_minimal_sb_smoke_4090d.py
?? scripts/run_overnight_reliability_sb_4090d.py
?? scripts/run_pm_fullsafe_light_overnight_tune_4090d.py
?? scripts/run_push_reliability_sb_4090d.py
?? scripts/run_scene_5task_1m_4090d_v1.py
?? scripts/run_table3_pm_fullres_problem_envs_2x4090.py
?? scripts/run_table3_pm_fullsafe_light_problem_envs_2x4090.py
?? scripts/run_table3_pm_fullsafe_official_2x4090_parallel.py
```

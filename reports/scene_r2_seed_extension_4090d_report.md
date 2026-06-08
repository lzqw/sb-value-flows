# Scene R2 3-Seed Extension 4090D

Results use final-row `evaluation/success` from the selected `eval.csv` only.
Seeds 0 and 1 are newly run here; seed 2 is merged from `scene_5task_1m_4090d_v1`.

## Setup
- config: `R2_flow_residual_disagree_std_lam0p001`
- paper VF scene domain: 0.59 +/- 0.04
- protocol note: this is a 3-seed evidence extension, not full 8-seed official protocol.

## Per-Seed Results
| seed | task | paper VF | success | return | length | weight_max | ess | rel_mean | rel_std | flow_res_mean | flow_res_std | disagree_mean | disagree_std | selected_eval_csv | status |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | scene-play-singletask-task1-v0 | 99 +/- 0 | 1 | -100.6 | 77.1 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_r2_seed_extension_4090d/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task1-v0_seed0_1000000/scene_r2_seed_ext_scene-play-singletask-task1-v0_seed0/sd000_20260607_213236/eval.csv` | COMPLETE |
| 0 | scene-play-singletask-task2-v0 | 97 +/- 1 | 1 | -363.8 | 192.9 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_r2_seed_extension_4090d/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task2-v0_seed0_1000000/scene_r2_seed_ext_scene-play-singletask-task2-v0_seed0/sd000_20260607_213236/eval.csv` | COMPLETE |
| 0 | scene-play-singletask-task3-v0 | 94 +/- 2 | 1 | -495.9 | 280 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_r2_seed_extension_4090d/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task3-v0_seed0_1000000/scene_r2_seed_ext_scene-play-singletask-task3-v0_seed0/sd000_20260608_014920/eval.csv` | COMPLETE |
| 0 | scene-play-singletask-task4-v0 | 7 +/- 4 | 0.1 | -748.7 | 706.6 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_r2_seed_extension_4090d/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task4-v0_seed0_1000000/scene_r2_seed_ext_scene-play-singletask-task4-v0_seed0/sd000_20260608_015420/eval.csv` | COMPLETE |
| 0 | scene-play-singletask-task5-v0 | 0 +/- 0 | 0 | -884.1 | 750 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_r2_seed_extension_4090d/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task5-v0_seed0_1000000/scene_r2_seed_ext_scene-play-singletask-task5-v0_seed0/sd000_20260608_060605/eval.csv` | COMPLETE |
| 1 | scene-play-singletask-task1-v0 | 99 +/- 0 | 1 | -115.4 | 89.2 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_r2_seed_extension_4090d/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task1-v0_seed1_1000000/scene_r2_seed_ext_scene-play-singletask-task1-v0_seed1/sd001_20260608_062436/eval.csv` | COMPLETE |
| 1 | scene-play-singletask-task2-v0 | 97 +/- 1 | 1 | -432.5 | 241.8 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_r2_seed_extension_4090d/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task2-v0_seed1_1000000/scene_r2_seed_ext_scene-play-singletask-task2-v0_seed1/sd001_20260608_102819/eval.csv` | COMPLETE |
| 1 | scene-play-singletask-task3-v0 | 94 +/- 2 | 1 | -386 | 201.5 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_r2_seed_extension_4090d/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task3-v0_seed1_1000000/scene_r2_seed_ext_scene-play-singletask-task3-v0_seed1/sd001_20260608_104550/eval.csv` | COMPLETE |
| 1 | scene-play-singletask-task4-v0 | 7 +/- 4 | 0 | -770.5 | 750 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_r2_seed_extension_4090d/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task4-v0_seed1_1000000/scene_r2_seed_ext_scene-play-singletask-task4-v0_seed1/sd001_20260608_144231/eval.csv` | COMPLETE |
| 1 | scene-play-singletask-task5-v0 | 0 +/- 0 | 0 | -890.5 | 750 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_r2_seed_extension_4090d/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task5-v0_seed1_1000000/scene_r2_seed_ext_scene-play-singletask-task5-v0_seed1/sd001_20260608_151032/eval.csv` | COMPLETE |
| 2 | scene-play-singletask-task1-v0 | 99 +/- 0 | 1 | -111.2 | 79.4 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task1-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task1-v0_seed2/sd002_20260606_142510/eval.csv` | EXISTING_SEED2 |
| 2 | scene-play-singletask-task2-v0 | 97 +/- 1 | 1 | -380.7 | 212 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task2-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task2-v0_seed2/sd002_20260606_183923/eval.csv` | EXISTING_SEED2 |
| 2 | scene-play-singletask-task3-v0 | 94 +/- 2 | 1 | -348.2 | 176.8 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task3-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task3-v0_seed2/sd002_20260606_225507/eval.csv` | EXISTING_SEED2 |
| 2 | scene-play-singletask-task4-v0 | 7 +/- 4 | 0 | -769.7 | 750 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task4-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task4-v0_seed2/sd002_20260607_031022/eval.csv` | EXISTING_SEED2 |
| 2 | scene-play-singletask-task5-v0 | 0 +/- 0 | 0 | -882.2 | 750 | nan | nan | nan | nan | nan | nan | nan | nan | `/root/sb-value-flows/exp/scene_5task_1m_4090d_v1/R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task5-v0_seed2_1000000/scene_5task_1m_v1_R2_flow_residual_disagree_std_lam0p001_scene-play-singletask-task5-v0_seed2/sd002_20260607_073207/eval.csv` | EXISTING_SEED2 |

## Task-Level 3-Seed Aggregate
| task | paper VF | seed values | mean | std | gap vs paper |
|---|---:|---|---:|---:|---:|
| scene-play-singletask-task1-v0 | 99 +/- 0 | 1, 1, 1 | 1 | 0 | 0.01 |
| scene-play-singletask-task2-v0 | 97 +/- 1 | 1, 1, 1 | 1 | 0 | 0.03 |
| scene-play-singletask-task3-v0 | 94 +/- 2 | 1, 1, 1 | 1 | 0 | 0.06 |
| scene-play-singletask-task4-v0 | 7 +/- 4 | 0.1, 0, 0 | 0.0333333 | 0.0471405 | -0.0366667 |
| scene-play-singletask-task5-v0 | 0 +/- 0 | 0, 0, 0 | 0 | 0 | 0 |

## Domain-Level Aggregate
| seed | domain mean success |
|---:|---:|
| 0 | 0.62 |
| 1 | 0.6 |
| 2 | 0.6 |

- 3-seed domain mean/std: 0.606667 / 0.00942809
- paper VF scene domain: 0.59 +/- 0.04
- seeds with domain mean >= 0.58: 3/3
- criterion `at least 2/3 seeds >= 0.58`: PASS

## Failed / Warned Runs
- none

## Git
- branch: `reliability-calibrated-sb`
- HEAD: `4d35406c574e2f25f3de302a8d0a7cf90ad9e6f5`
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
?? reports/scene_r2_seed_extension_4090d_report.md
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
?? scripts/run_scene_r2_seed_extension_4090d.py
?? scripts/run_table3_pm_fullres_problem_envs_2x4090.py
?? scripts/run_table3_pm_fullsafe_light_problem_envs_2x4090.py
?? scripts/run_table3_pm_fullsafe_official_2x4090_parallel.py
```

# Best-seed 5-task reliability SB 4090D report

This is an optimistic best-seed / 300k screening result set, not a full 8-seed official protocol.

## Cube-triple R2 best-seed 5-task results

| env | paper VF | ours | gap | return | length | weight_max | ess | collapse | status |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|

cube-triple 5-task mean=nan std=nan
paper Value Flows cube-triple-play domain=14+-3
current task1 R2 3-seed mean=0.633333; Origin task1=0.56; Minimal SB task1=0.60

## Cube-double / scene 300k screening

| domain | env | config | paper VF | ours | gap | return | weight_max | ess | reliability_mean | reliability_std | flow_residual_mean | disagree_mean | typicality_mean | collapse | status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| cube-double | cube-double-play-singletask-task2-v0 | A1_action_std_lam0p001 | 76+-7 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | False | FAILED |
| cube-double | cube-double-play-singletask-task2-v0 | R2_flow_residual_disagree_std_lam0p001 | 76+-7 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | False | FAILED |
| cube-double | cube-double-play-singletask-task2-v0 | R3_flow_residual_disagree_typicality_std_lam0p001 | 76+-7 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | False | FAILED |
| scene-play | scene-play-singletask-task2-v0 | A1_action_std_lam0p001 | 97+-1 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | False | FAILED |
| scene-play | scene-play-singletask-task2-v0 | R2_flow_residual_disagree_std_lam0p001 | 97+-1 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | False | FAILED |
| scene-play | scene-play-singletask-task2-v0 | R3_flow_residual_disagree_typicality_std_lam0p001 | 97+-1 | nan | nan | nan | nan | nan | nan | nan | nan | nan | nan | False | FAILED |

## Best Config By Domain


## Failures / warnings

- Queue A invalid cube-triple task discovery: ['cube-triple-play-singletask-task1-v0']
- Queue B cube-double discovery incomplete: ['cube-double-play-singletask-task2-v0']
- Queue B scene discovery incomplete: ['scene-play-singletask-task2-v0']
- Task(queue='queueB_screen_300k', env='cube-double-play-singletask-task2-v0', config='R2_flow_residual_disagree_std_lam0p001', seed=2, steps=300000) returncode=0
- Task(queue='queueB_screen_300k', env='cube-double-play-singletask-task2-v0', config='A1_action_std_lam0p001', seed=2, steps=300000) returncode=0
- Task(queue='queueB_screen_300k', env='cube-double-play-singletask-task2-v0', config='R3_flow_residual_disagree_typicality_std_lam0p001', seed=2, steps=300000) returncode=0
- Task(queue='queueB_screen_300k', env='scene-play-singletask-task2-v0', config='A1_action_std_lam0p001', seed=2, steps=300000) returncode=0
- Task(queue='queueB_screen_300k', env='scene-play-singletask-task2-v0', config='R2_flow_residual_disagree_std_lam0p001', seed=2, steps=300000) returncode=0
- Task(queue='queueB_screen_300k', env='scene-play-singletask-task2-v0', config='R3_flow_residual_disagree_typicality_std_lam0p001', seed=2, steps=300000) returncode=0

## GPU / Git
```
Thu Jun  4 19:07:41 2026       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.76.05              Driver Version: 580.76.05      CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 4090 D      On  |   00000000:28:00.0 Off |                  Off |
| 30%   36C    P8             22W /  425W |       0MiB /  24564MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
|   1  NVIDIA GeForce RTX 4090 D      On  |   00000000:39:00.0 Off |                  Off |
|  0%   27C    P8             17W /  425W |       0MiB /  24564MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+

reliability-calibrated-sb

8beb46e642965e399802e40e6cf94a5238cdfad6

A  reports/valueflows_task_level_tracking.md
?? reports/bestseed_5task_push_4090d_report.md
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
?? scripts/run_bestseed_5task_push_4090d.py
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

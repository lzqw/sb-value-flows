# Puzzle-3x3 Best-Seed 5-Task Minimal SB Single4090 v3

Generated: 2026-06-07 10:31:50

This is an optimistic best-seed single-seed 5-task sweep, not the full 8-seed official protocol.

## Setup

- method: Minimal SB S1
- config: S1_sb_lam0p001
- lambda: 0.001
- seed: 2
- offline_steps: 1000000
- online_steps: 0
- eval_interval: 50000
- eval_episodes: 10
- log_interval: 25000
- save_interval: 999999999
- branch: minimal-sb-reweight
- HEAD: f241a28599877a54ecf5213b571c66d10a8c6552
- command order: --agent=agents/pm_value_flows.py appears before all --agent.* flags
- output log dir: logs/puzzle3x3_bestseed_5task_single4090_v3
- output exp dir: exp/puzzle3x3_bestseed_5task_single4090_v3
- final report: reports/puzzle3x3_bestseed_5task_single4090_v3_report.md

## Per-Task Final Results

| task | env | status | final success | success % | return | length | paper baseline % | gap % | collapse | selected_eval_csv |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | puzzle-3x3-play-singletask-task1-v0 | COMPLETE | 1 | 100.00 | -226.8 | 57.4 | 99 +/- 0 | 1.00 | False | exp/puzzle3x3_bestseed_5task_single4090_v3/task1_S1_sb_lam0p001_seed2/sd002_20260606_142934/eval.csv |
| 2 | puzzle-3x3-play-singletask-task2-v0 | COMPLETE | 1 | 100.00 | -566.7 | 214.7 | 98 +/- 2 | 2.00 | True | exp/puzzle3x3_bestseed_5task_single4090_v3/task2_S1_sb_lam0p001_seed2/sd002_20260606_182634/eval.csv |
| 3 | puzzle-3x3-play-singletask-task3-v0 | COMPLETE | 0.1 | 10.00 | -1120.3 | 473.8 | 97 +/- 1 | -87.00 | False | exp/puzzle3x3_bestseed_5task_single4090_v3/task3_S1_sb_lam0p001_seed2/sd002_20260606_222604/eval.csv |
| 4 | puzzle-3x3-play-singletask-task4-v0 | COMPLETE | 1 | 100.00 | -808.9 | 282 | 84 +/- 24 | 16.00 | False | exp/puzzle3x3_bestseed_5task_single4090_v3/task4_S1_sb_lam0p001_seed2/sd002_20260607_022834/eval.csv |
| 5 | puzzle-3x3-play-singletask-task5-v0 | COMPLETE | 1 | 100.00 | -679.7 | 235.1 | 58 +/- 39 | 42.00 | False | exp/puzzle3x3_bestseed_5task_single4090_v3/task5_S1_sb_lam0p001_seed2/sd002_20260607_063032/eval.csv |

## 5-Task Aggregate

| metric | mean | std | n |
|---|---:|---:|---:|
| success % | 82.00 | 40.25 | 5 |
| return | -680.48 | 327.378 | 5 |
| length | 252.6 | 149.699 | 5 |

## Paper Value Flows Task-Level Baseline

| task | baseline success % |
|---:|---:|
| 1 | 99 +/- 0 |
| 2 | 98 +/- 2 |
| 3 | 97 +/- 1 |
| 4 | 84 +/- 24 |
| 5 | 58 +/- 39 |
| domain | 87 +/- 13 |

## Diagnostics

| task | pm/proj_delta_mean | pm/cov_y_action | pm/corr_y_action | pm/action_mean | pm/action_std | pm/weight_max | pm/ess | collapse flag |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | -0.158016 | -244.622 | -0.730983 | 16895.2 | 8015.11 | 0.765548 | 2.48021 | False |
| 2 | -0.086579 | -73.7679 | -0.73575 | 20092.2 | 8962.98 | 0.991689 | 2.4685 | True |
| 3 | -0.113863 | -99.3125 | -0.738414 | 16337.3 | 8233.58 | 0.791326 | 2.48707 | False |
| 4 | -0.0544575 | -57.0025 | -0.753771 | 20269.2 | 8074.97 | 0.661846 | 2.47201 | False |
| 5 | -0.110049 | -85.4803 | -0.727982 | 19312.8 | 7930.19 | 0.796625 | 2.47833 | False |

## CSV Selection

| task | selected_eval_csv | all eval.csv candidates | selected_train_csv | train candidates |
|---:|---|---|---|---|
| 1 | exp/puzzle3x3_bestseed_5task_single4090_v3/task1_S1_sb_lam0p001_seed2/sd002_20260606_142934/eval.csv | exp/puzzle3x3_bestseed_5task_single4090_v3/task1_S1_sb_lam0p001_seed2/sd002_20260606_142934/eval.csv (rows=21, mtime=2026-06-06 18:26:28) | exp/puzzle3x3_bestseed_5task_single4090_v3/task1_S1_sb_lam0p001_seed2/sd002_20260606_142934/train.csv | exp/puzzle3x3_bestseed_5task_single4090_v3/task1_S1_sb_lam0p001_seed2/sd002_20260606_142934/train.csv (rows=40, mtime=2026-06-06 18:26:26) |
| 2 | exp/puzzle3x3_bestseed_5task_single4090_v3/task2_S1_sb_lam0p001_seed2/sd002_20260606_182634/eval.csv | exp/puzzle3x3_bestseed_5task_single4090_v3/task2_S1_sb_lam0p001_seed2/sd002_20260606_182634/eval.csv (rows=21, mtime=2026-06-06 22:25:58) | exp/puzzle3x3_bestseed_5task_single4090_v3/task2_S1_sb_lam0p001_seed2/sd002_20260606_182634/train.csv | exp/puzzle3x3_bestseed_5task_single4090_v3/task2_S1_sb_lam0p001_seed2/sd002_20260606_182634/train.csv (rows=40, mtime=2026-06-06 22:25:50) |
| 3 | exp/puzzle3x3_bestseed_5task_single4090_v3/task3_S1_sb_lam0p001_seed2/sd002_20260606_222604/eval.csv | exp/puzzle3x3_bestseed_5task_single4090_v3/task3_S1_sb_lam0p001_seed2/sd002_20260606_222604/eval.csv (rows=21, mtime=2026-06-07 02:28:27) | exp/puzzle3x3_bestseed_5task_single4090_v3/task3_S1_sb_lam0p001_seed2/sd002_20260606_222604/train.csv | exp/puzzle3x3_bestseed_5task_single4090_v3/task3_S1_sb_lam0p001_seed2/sd002_20260606_222604/train.csv (rows=40, mtime=2026-06-07 02:28:10) |
| 4 | exp/puzzle3x3_bestseed_5task_single4090_v3/task4_S1_sb_lam0p001_seed2/sd002_20260607_022834/eval.csv | exp/puzzle3x3_bestseed_5task_single4090_v3/task4_S1_sb_lam0p001_seed2/sd002_20260607_022834/eval.csv (rows=21, mtime=2026-06-07 06:30:27) | exp/puzzle3x3_bestseed_5task_single4090_v3/task4_S1_sb_lam0p001_seed2/sd002_20260607_022834/train.csv | exp/puzzle3x3_bestseed_5task_single4090_v3/task4_S1_sb_lam0p001_seed2/sd002_20260607_022834/train.csv (rows=40, mtime=2026-06-07 06:30:17) |
| 5 | exp/puzzle3x3_bestseed_5task_single4090_v3/task5_S1_sb_lam0p001_seed2/sd002_20260607_063032/eval.csv | exp/puzzle3x3_bestseed_5task_single4090_v3/task5_S1_sb_lam0p001_seed2/sd002_20260607_063032/eval.csv (rows=21, mtime=2026-06-07 10:31:48) | exp/puzzle3x3_bestseed_5task_single4090_v3/task5_S1_sb_lam0p001_seed2/sd002_20260607_063032/train.csv | exp/puzzle3x3_bestseed_5task_single4090_v3/task5_S1_sb_lam0p001_seed2/sd002_20260607_063032/train.csv (rows=40, mtime=2026-06-07 10:31:39) |

## Failed Or Warning Run Summary

No failed or warning runs.

## Run Commands

### task1
```text
/root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-3x3-play-singletask-task1-v0 --seed=2 --save_dir=/root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3 --wandb_run_group=task1_S1_sb_lam0p001_seed2 --enable_wandb=0 --offline_steps=1000000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=0.5 --agent.ret_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_action_normalize=none --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_lambda=0.001
```
### task2
```text
/root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-3x3-play-singletask-task2-v0 --seed=2 --save_dir=/root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3 --wandb_run_group=task2_S1_sb_lam0p001_seed2 --enable_wandb=0 --offline_steps=1000000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=0.5 --agent.ret_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_action_normalize=none --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_lambda=0.001
```
### task3
```text
/root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-3x3-play-singletask-task3-v0 --seed=2 --save_dir=/root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3 --wandb_run_group=task3_S1_sb_lam0p001_seed2 --enable_wandb=0 --offline_steps=1000000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=0.5 --agent.ret_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_action_normalize=none --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_lambda=0.001
```
### task4
```text
/root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-3x3-play-singletask-task4-v0 --seed=2 --save_dir=/root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3 --wandb_run_group=task4_S1_sb_lam0p001_seed2 --enable_wandb=0 --offline_steps=1000000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=0.5 --agent.ret_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_action_normalize=none --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_lambda=0.001
```
### task5
```text
/root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-3x3-play-singletask-task5-v0 --seed=2 --save_dir=/root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3 --wandb_run_group=task5_S1_sb_lam0p001_seed2 --enable_wandb=0 --offline_steps=1000000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=0.5 --agent.ret_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_action_normalize=none --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_lambda=0.001
```

## nvidia-smi
```text
Sun Jun  7 10:31:50 2026       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.105.08             Driver Version: 580.105.08     CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 4090        On  |   00000000:BA:00.0 Off |                  Off |
|100%   46C    P0             87W /  450W |       0MiB /  24564MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```

## git status --short
```text
AM reports/valueflows_task_level_tracking.md
?? reports/minimal_sb_puzzle3x3_1m_single4090_report.md
?? reports/minimal_sb_puzzle3x3_push_single4090_report.md
?? reports/pm_medium_1m_methods_4090_report.md
?? reports/pm_medium_300k_posterior_big_4090_report.md
?? reports/pm_medium_300k_seed3_4090_report.md
?? reports/pm_medium_component_4090_report.md
?? reports/pm_puzzle4x4_light_tune_single4090_fixflag_report.md
?? reports/pm_puzzle4x4_light_tune_single4090_report.md
?? reports/postrun_single4090_after_puzzle4x4_tune_report.md
?? reports/puzzle3x3_bestseed_5task_single4090_v3_report.md
?? reports/puzzle4x4_second_wave_single4090_final_report.md
?? reports/puzzle4x4_secondwave_single4090_report.md
?? reports/reliability_sb_puzzle3x3_overnight_single4090_report.md
?? reports/table3_pm_actorgeo_problem_envs_4090_report.md
?? reports/table3_pm_fullsafe_light_cubedouble_single4090_report.md
?? reports/table3_pm_fullsafe_light_remaining_single4090_report.md
?? reports/table3_pm_fullsafe_light_remaining_single4090_report.pre_resume_20260529_100232.md
?? reports/table3_pm_fullsafe_official_4090_highmem_ldfix_report.md
?? reports/table3_pm_success_audit_single4090.md
?? scripts/audit_pm_success_single4090.py
?? scripts/make_puzzle4x4_secondwave_final_report.py
?? scripts/postrun_single4090_after_puzzle4x4_tune.py
?? scripts/postrun_single4090_after_remaining.py
?? scripts/run_minimal_sb_puzzle3x3_1m_single4090.py
?? scripts/run_minimal_sb_puzzle3x3_push_single4090.py
?? scripts/run_pm_medium_1m_methods_4090.py
?? scripts/run_pm_medium_300k_posterior_big_4090.py
?? scripts/run_pm_medium_300k_seed3_4090.py
?? scripts/run_pm_medium_component_4090.py
?? scripts/run_pm_puzzle4x4_light_tune_single4090.py
?? scripts/run_pm_puzzle4x4_light_tune_single4090_fixflag.py
?? scripts/run_puzzle3x3_bestseed_5task_single4090_v3.py
?? scripts/run_puzzle4x4_secondwave_single4090.py
?? scripts/run_reliability_sb_puzzle3x3_overnight_single4090.py
?? scripts/run_table3_pm_actorgeo_problem_envs_4090.py
?? scripts/run_table3_pm_fullsafe_light_remaining_single4090.py
?? scripts/run_table3_pm_fullsafe_official_4090_highmem_ldfix.py
```

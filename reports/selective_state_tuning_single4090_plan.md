# Selective State Tuning Single4090 Plan

Generated: 2026-06-15 11:58:09
Dry run: True

## Guardrails

- This is task-wise hard-task tuning, not full 25-task brute-force tuning and not formal ablation.
- Completed means eval.csv final row with final_step >= target_steps * 0.98.
- Partial runs do not count as completed, and peak/best success is not used as final success.
- Actual training requires --dry_run false --confirm_start true.

## Setup

- branch: results/historical-inventory-single4090
- HEAD: 9f8221ec52eacf8a7d1f0d1efd8f9ee2d01b4e74
- output base: /root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090
- exp dir: /root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp
- repo report: /root/sb-value-flows/reports/selective_state_tuning_single4090_plan.md
- status report: /root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/reports/selective_state_tuning_status.md
- registry runs: 79
- state baselines: 25
- state scoreboard tasks: 25
- stable mode: stable mode unavailable: no pm_sb_stable/pm_stable/stable_mode/sb_stable flag found
- config pool: P0_particle, MinimalSB_lam0p003, MinimalSB_lam0p001, A1_action_std_lam0p001, A2_action_std_lam0p003, R2_residual_disagree_lam0p001, R3_residual_disagree_typicality_lam0p001
- queue policy: lock completed positives and high-baseline easy tasks; hold unstable tasks until a real stable mode exists.

## Registry Files

- /root/sb-value-flows/results/experiment_runs.csv
- /root/sb-value-flows/results/eval_curves_index.csv
- /root/sb-value-flows/results/task_scoreboard.csv
- /root/sb-value-flows/results/task_scoreboard.md
- /root/sb-value-flows/results/valueflow_task_baselines.csv

## Candidate Tasks

| priority | env | VF baseline | best 300k | best 1M mean | conclusion | action | Stage A pending | Stage B pending | Stage B note |
|---|---|---:|---:|---:|---|---|---:|---:|---|
| P1 immediate 300k screening | puzzle-4x4-play-singletask-task1-v0 | 0.36 |  |  | No completed 1M result | pending | 7 | 0 | waiting: complete Stage A screening pool first |
| P1 immediate 300k screening | puzzle-4x4-play-singletask-task3-v0 | 0.3 |  |  | No completed 1M result | pending | 7 | 0 | waiting: complete Stage A screening pool first |
| P1 immediate 300k screening | puzzle-3x3-play-singletask-task5-v0 | 0.58 |  |  | No completed 1M result | pending | 7 | 0 | waiting: complete Stage A screening pool first |
| P2 optional 1M confirmation | cube-double-play-singletask-task5-v0 | 0.69 |  |  | No completed 1M result | pending | 0 | 1 |  |
| P3 stable-hold | scene-play-singletask-task4-v0 | 0.07 | 0.4 | 0 | 300k signal did not hold at 1M | stable_hold | 0 | 0 | held: ordinary 1M collapsed or underperformed; wait for Min001/R3/A2/P0 stable variants; stable mode unavailable |
| P3 stable-hold | puzzle-4x4-play-singletask-task4-v0 | 0.28 | 0.5 | 0.1 | 300k signal did not hold at 1M | stable_hold | 0 | 0 | held: ordinary 1M collapsed or underperformed; wait for Min001/R3/A2/P0 stable variants; stable mode unavailable |
| P3 stable-hold | puzzle-4x4-play-singletask-task5-v0 | 0.13 | 0.1 | 0 | Below Value Flow baseline | stable_hold | 0 | 0 | held: ordinary 1M collapsed or underperformed; wait for Min001/R3/A2/P0 stable variants; stable mode unavailable |
| P3 stable-hold | cube-triple-play-singletask-task3-v0 | 0.07 | 0.1 |  | No completed 1M result | stable_hold | 0 | 0 | held: ordinary 1M collapsed or underperformed; wait for Min001/R3/A2/P0 stable variants; stable mode unavailable |
| P3 stable-hold | puzzle-3x3-play-singletask-task4-v0 | 0.84 |  |  | No completed 1M result | stable_hold | 0 | 0 | held: ordinary 1M collapsed or underperformed; wait for Min001/R3/A2/P0 stable variants; stable mode unavailable |

## Skipped Tasks

| env | VF baseline | best 300k | best 1M mean | reason |
|---|---:|---:|---:|---|
| cube-double-play-singletask-task1-v0 | 0.97 |  |  | skip: high Value Flow baseline 0.97 and low expected repair value |
| cube-double-play-singletask-task2-v0 | 0.76 | 0.4 | 0.833333 | skip: already strong positive with R3 1M 3-seed mean about 0.83 > VF 0.76 |
| cube-double-play-singletask-task3-v0 | 0.73 | 0.5 | 0.833333 | skip: already strong positive with A2 1M 3-seed mean about 0.83 > VF 0.73 |
| cube-double-play-singletask-task4-v0 | 0.3 | 0.3 | 0.4 | skip: already positive with A1 1M 3-seed mean about 0.40 > VF 0.30 |
| cube-triple-play-singletask-task1-v0 | 0.59 |  |  | skip: single-seed weak positive around 0.65 vs VF 0.59; not a selective repair target |
| cube-triple-play-singletask-task2-v0 | 0 |  |  | skip: matches low VF baseline 0.00; not worth ordinary tuning now |
| cube-triple-play-singletask-task4-v0 | 0 |  |  | skip: matches low VF baseline 0.00; not worth ordinary tuning now |
| cube-triple-play-singletask-task5-v0 | 0.02 |  |  | skip: temporary lock, R2 reached about 0.10 vs VF 0.02 |
| puzzle-3x3-play-singletask-task1-v0 | 0.99 |  |  | skip: high Value Flow baseline easy task, not a repair target |
| puzzle-3x3-play-singletask-task2-v0 | 0.98 |  |  | skip: high Value Flow baseline easy task, not a repair target |
| puzzle-3x3-play-singletask-task3-v0 | 0.97 | 0.2 |  | skip: high Value Flow baseline easy task, not a repair target |
| puzzle-4x4-play-singletask-task2-v0 | 0.27 | 0.2 | 0.333333 | skip: weak positive MinimalSB_lam0p001 1M mean about 0.33 > VF 0.27; wait for a real stable mode |
| scene-play-singletask-task1-v0 | 0.99 |  |  | skip: locked positive, A1 reached 1.00 vs VF 0.99 |
| scene-play-singletask-task2-v0 | 0.97 |  |  | skip: locked positive, A1 reached 1.00 vs VF 0.97 |
| scene-play-singletask-task3-v0 | 0.94 |  |  | skip: locked positive, A1 reached 1.00 vs VF 0.94 |
| scene-play-singletask-task5-v0 | 0 |  |  | skip: outside current immediate selective queue |

## Stable-Hold Queue

| env | best 300k | best 1M mean | plan |
|---|---:|---:|---|
| scene-play-singletask-task4-v0 | 0.4 | 0 | held: ordinary 1M collapsed or underperformed; wait for Min001/R3/A2/P0 stable variants; stable mode unavailable |
| puzzle-4x4-play-singletask-task4-v0 | 0.5 | 0.1 | held: ordinary 1M collapsed or underperformed; wait for Min001/R3/A2/P0 stable variants; stable mode unavailable |
| puzzle-4x4-play-singletask-task5-v0 | 0.1 | 0 | held: ordinary 1M collapsed or underperformed; wait for Min001/R3/A2/P0 stable variants; stable mode unavailable |
| cube-triple-play-singletask-task3-v0 | 0.1 |  | held: ordinary 1M collapsed or underperformed; wait for Min001/R3/A2/P0 stable variants; stable mode unavailable |
| puzzle-3x3-play-singletask-task4-v0 |  |  | held: ordinary 1M collapsed or underperformed; wait for Min001/R3/A2/P0 stable variants; stable mode unavailable |

## Pending Stage A Runs

| env | config | seed | target_steps | reason |
|---|---|---:|---:|---|
| puzzle-4x4-play-singletask-task1-v0 | P0_particle | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-4x4-play-singletask-task1-v0 | MinimalSB_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-4x4-play-singletask-task1-v0 | MinimalSB_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-4x4-play-singletask-task1-v0 | A1_action_std_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-4x4-play-singletask-task1-v0 | A2_action_std_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-4x4-play-singletask-task1-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-4x4-play-singletask-task1-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-4x4-play-singletask-task3-v0 | P0_particle | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-4x4-play-singletask-task3-v0 | MinimalSB_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-4x4-play-singletask-task3-v0 | MinimalSB_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-4x4-play-singletask-task3-v0 | A1_action_std_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-4x4-play-singletask-task3-v0 | A2_action_std_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-4x4-play-singletask-task3-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-4x4-play-singletask-task3-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-3x3-play-singletask-task5-v0 | P0_particle | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-3x3-play-singletask-task5-v0 | MinimalSB_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-3x3-play-singletask-task5-v0 | MinimalSB_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-3x3-play-singletask-task5-v0 | A1_action_std_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-3x3-play-singletask-task5-v0 | A2_action_std_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-3x3-play-singletask-task5-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |
| puzzle-3x3-play-singletask-task5-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row in immediate selective queue |

## Pending Stage B Runs

| env | config | seed | target_steps | reason |
|---|---|---:|---:|---|
| cube-double-play-singletask-task5-v0 | A1_action_std_lam0p001 | 2 | 1000000 | optional confirmation: snapshot reports strong 300k signal but no completed 1M |

## Next 10 Commands

### 1. stageA_300k puzzle-4x4-play-singletask-task1-v0 P0_particle seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-4x4-play-singletask-task1-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_puzzle_4x4_task1_P0_particle_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=3 --agent.confidence_weight_temp=100 --agent.q_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.0 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 2. stageA_300k puzzle-4x4-play-singletask-task1-v0 MinimalSB_lam0p003 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-4x4-play-singletask-task1-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_puzzle_4x4_task1_MinimalSB_lam0p003_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=3 --agent.confidence_weight_temp=100 --agent.q_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.003 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 3. stageA_300k puzzle-4x4-play-singletask-task1-v0 MinimalSB_lam0p001 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-4x4-play-singletask-task1-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_puzzle_4x4_task1_MinimalSB_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=3 --agent.confidence_weight_temp=100 --agent.q_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 4. stageA_300k puzzle-4x4-play-singletask-task1-v0 A1_action_std_lam0p001 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-4x4-play-singletask-task1-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_puzzle_4x4_task1_A1_action_std_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=3 --agent.confidence_weight_temp=100 --agent.q_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_value_preserving=false
```

### 5. stageA_300k puzzle-4x4-play-singletask-task1-v0 A2_action_std_lam0p003 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-4x4-play-singletask-task1-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_puzzle_4x4_task1_A2_action_std_lam0p003_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=3 --agent.confidence_weight_temp=100 --agent.q_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.003 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_value_preserving=false
```

### 6. stageA_300k puzzle-4x4-play-singletask-task1-v0 R2_residual_disagree_lam0p001 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-4x4-play-singletask-task1-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_puzzle_4x4_task1_R2_residual_disagree_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=3 --agent.confidence_weight_temp=100 --agent.q_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=flow_residual_disagree --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_value_preserving=false
```

### 7. stageA_300k puzzle-4x4-play-singletask-task1-v0 R3_residual_disagree_typicality_lam0p001 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-4x4-play-singletask-task1-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_puzzle_4x4_task1_R3_residual_disagree_typicality_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=3 --agent.confidence_weight_temp=100 --agent.q_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=flow_residual_disagree_typicality --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_typicality_tau=1.0 --agent.pm_sb_value_preserving=false
```

### 8. stageA_300k puzzle-4x4-play-singletask-task3-v0 P0_particle seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-4x4-play-singletask-task3-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_puzzle_4x4_task3_P0_particle_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=3 --agent.confidence_weight_temp=100 --agent.q_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.0 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 9. stageA_300k puzzle-4x4-play-singletask-task3-v0 MinimalSB_lam0p003 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-4x4-play-singletask-task3-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_puzzle_4x4_task3_MinimalSB_lam0p003_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=3 --agent.confidence_weight_temp=100 --agent.q_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.003 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 10. stageA_300k puzzle-4x4-play-singletask-task3-v0 MinimalSB_lam0p001 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=puzzle-4x4-play-singletask-task3-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_puzzle_4x4_task3_MinimalSB_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.bcfm_lambda=3 --agent.confidence_weight_temp=100 --agent.q_agg=min --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

## Counts

- candidate tasks: 9
- skipped tasks: 16
- pending Stage A runs: 21
- pending Stage B runs: 1
- total pending runs: 22

## Suggested Launch Order

1. Immediate 300k screening: puzzle-4x4 task1, puzzle-4x4 task3, puzzle-3x3 task5.
2. Optional 1M confirmation: cube-double task5 / A1_action_std_lam0p001 / seed2 only.
3. Hold until stable mode: scene task4, puzzle-4x4 task4/task5, cube-triple task3, puzzle-3x3 task4.

## Git Status At Planning Time

```text
M reports/bad_task_repair_single4090_report.md
AM reports/puzzle3x3_bestseed_5task_single4090_v3_report.md
 M reports/selective_state_tuning_single4090_plan.md
 M results/experiment_runs.csv
 M results/task_scoreboard.csv
 M results/task_scoreboard.md
 M results/valueflow_task_baselines.csv
A  scripts/run_puzzle3x3_bestseed_5task_single4090_v3.py
 M scripts/run_selective_state_tuning_single4090.py
 M scripts/update_results_registry.py
?? reports/minimal_sb_puzzle3x3_1m_single4090_report.md
?? reports/minimal_sb_puzzle3x3_push_single4090_report.md
?? reports/pm_medium_1m_methods_4090_report.md
?? reports/pm_medium_300k_posterior_big_4090_report.md
?? reports/pm_medium_300k_seed3_4090_report.md
?? reports/pm_medium_component_4090_report.md
?? reports/pm_puzzle4x4_light_tune_single4090_fixflag_report.md
?? reports/pm_puzzle4x4_light_tune_single4090_report.md
?? reports/postrun_single4090_after_puzzle4x4_tune_report.md
?? reports/puzzle3x3_task3_repair_single4090_v1_report.md
?? reports/puzzle4x4_second_wave_single4090_final_report.md
?? reports/puzzle4x4_secondwave_single4090_report.md
?? reports/reliability_sb_puzzle3x3_overnight_single4090_report.md
?? reports/source_valueflow_full_offline_eval_table.tex
?? reports/table3_pm_actorgeo_problem_envs_4090_report.md
?? reports/table3_pm_fullsafe_light_cubedouble_single4090_report.md
?? reports/table3_pm_fullsafe_light_remaining_single4090_report.md
?? reports/table3_pm_fullsafe_light_remaining_single4090_report.pre_resume_20260529_100232.md
?? reports/table3_pm_fullsafe_official_4090_highmem_ldfix_report.md
?? reports/table3_pm_success_audit_single4090.md
?? reports/valueflow_full_offline_eval_table.md
?? results/valueflow_full_offline_eval_table.csv
?? scripts/audit_pm_success_single4090.py
?? scripts/make_puzzle4x4_secondwave_final_report.py
?? scripts/parse_valueflow_full_table.py
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
?? scripts/run_puzzle3x3_task3_repair_single4090_v1.py
?? scripts/run_puzzle4x4_secondwave_single4090.py
?? scripts/run_reliability_sb_puzzle3x3_overnight_single4090.py
?? scripts/run_table3_pm_actorgeo_problem_envs_4090.py
?? scripts/run_table3_pm_fullsafe_light_remaining_single4090.py
?? scripts/run_table3_pm_fullsafe_official_4090_highmem_ldfix.py
```

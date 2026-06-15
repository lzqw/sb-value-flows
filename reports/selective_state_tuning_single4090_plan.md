# Selective State Tuning Single4090 Plan

Generated: 2026-06-15 11:02:22
Dry run: True

## Guardrails

- This is task-wise hard-task tuning, not full 25-task brute-force tuning and not formal ablation.
- Completed means eval.csv final row with final_step >= target_steps * 0.98.
- Partial runs do not count as completed, and peak/best success is not used as final success.
- Actual training requires --dry_run false --confirm_start true.

## Setup

- branch: results/full-paper-table
- HEAD: 8c1d173b4611766d7a548f26708f481371f100b3
- output base: /root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090
- exp dir: /root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp
- repo report: /root/sb-value-flows/reports/selective_state_tuning_single4090_plan.md
- status report: /root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/reports/selective_state_tuning_status.md
- registry runs: 79
- state baselines: 25
- state scoreboard tasks: 25
- stable mode: stable mode unavailable: no pm_sb_stable/pm_stable/stable_mode/sb_stable flag found
- config pool: P0_particle, MinimalSB_lam0p0003, MinimalSB_lam0p001, A1_action_std_lam0p001, A2_action_std_lam0p003, R2_residual_disagree_lam0p001, R3_residual_disagree_typicality_lam0p001
- note: the existing bad-task repair pool contains MinimalSB_lam0p0003; no separate MinimalSB_lam0p003 config was found.

## Registry Files

- /root/sb-value-flows/results/experiment_runs.csv
- /root/sb-value-flows/results/eval_curves_index.csv
- /root/sb-value-flows/results/task_scoreboard.csv
- /root/sb-value-flows/results/task_scoreboard.md
- /root/sb-value-flows/results/valueflow_task_baselines.csv

## Candidate Tasks

| priority | env | VF baseline | best 300k | best 1M mean | conclusion | action | Stage A pending | Stage B pending | Stage B note |
|---|---|---:|---:|---:|---|---|---:|---:|---|
| P2 low-baseline or uncovered | cube-triple-play-singletask-task2-v0 | 0 |  |  | No completed 1M result | pending | 7 | 0 | waiting: complete Stage A screening pool first |
| P2 low-baseline or uncovered | cube-triple-play-singletask-task3-v0 | 0.07 | 0.1 |  | No completed 1M result | pending | 0 | 6 |  |
| P2 low-baseline or uncovered | cube-triple-play-singletask-task4-v0 | 0 |  |  | No completed 1M result | pending | 7 | 0 | waiting: complete Stage A screening pool first |
| P2 low-baseline or uncovered | cube-triple-play-singletask-task5-v0 | 0.02 |  |  | No completed 1M result | pending | 7 | 0 | waiting: complete Stage A screening pool first |
| P2 low-baseline or uncovered | puzzle-4x4-play-singletask-task1-v0 | 0.36 |  |  | No completed 1M result | pending | 7 | 0 | waiting: complete Stage A screening pool first |
| P2 low-baseline or uncovered | puzzle-4x4-play-singletask-task3-v0 | 0.3 |  |  | No completed 1M result | pending | 7 | 0 | waiting: complete Stage A screening pool first |
| P1 unstable | scene-play-singletask-task4-v0 | 0.07 | 0.4 | 0 | 300k signal did not hold at 1M | screen_only | 0 | 0 | held: unstable task and stable variant unavailable; do 300k curves first |
| P1 unstable | puzzle-4x4-play-singletask-task4-v0 | 0.28 | 0.5 | 0.1 | 300k signal did not hold at 1M | screen_only | 0 | 0 | held: unstable task and stable variant unavailable; do 300k curves first |
| P1 unstable | puzzle-4x4-play-singletask-task5-v0 | 0.13 | 0.1 | 0 | Below Value Flow baseline | screen_only | 0 | 0 | held: unstable task and stable variant unavailable; do 300k curves first |
| P3 if capacity | scene-play-singletask-task5-v0 | 0 |  |  | No completed 1M result | pending | 7 | 0 | waiting: complete Stage A screening pool first |
| P3 if capacity | cube-double-play-singletask-task5-v0 | 0.69 |  |  | No completed 1M result | pending | 7 | 0 | waiting: complete Stage A screening pool first |
| P3 if capacity | puzzle-3x3-play-singletask-task4-v0 | 0.84 |  |  | No completed 1M result | pending | 7 | 0 | waiting: complete Stage A screening pool first |
| P3 if capacity | puzzle-3x3-play-singletask-task5-v0 | 0.58 |  |  | No completed 1M result | pending | 7 | 0 | waiting: complete Stage A screening pool first |

## Skipped Tasks

| env | VF baseline | best 300k | best 1M mean | reason |
|---|---:|---:|---:|---|
| cube-double-play-singletask-task1-v0 | 0.97 |  |  | skip: high Value Flow baseline easy task, not a repair target |
| cube-double-play-singletask-task2-v0 | 0.76 | 0.4 | 0.833333 | skip: already strong positive with R3 1M 3-seed mean about 0.83 > VF 0.76 |
| cube-double-play-singletask-task3-v0 | 0.73 | 0.5 | 0.833333 | skip: already strong positive with A2 1M 3-seed mean about 0.83 > VF 0.73 |
| cube-double-play-singletask-task4-v0 | 0.3 | 0.3 | 0.4 | skip: already positive with A1 1M 3-seed mean about 0.40 > VF 0.30 |
| cube-triple-play-singletask-task1-v0 | 0.59 |  |  | skip: not in current selective hard-task queue |
| puzzle-3x3-play-singletask-task1-v0 | 0.99 |  |  | skip: high Value Flow baseline easy task, not a repair target |
| puzzle-3x3-play-singletask-task2-v0 | 0.98 |  |  | skip: high Value Flow baseline easy task, not a repair target |
| puzzle-3x3-play-singletask-task3-v0 | 0.97 | 0.2 |  | skip: high Value Flow baseline easy task, not a repair target |
| puzzle-4x4-play-singletask-task2-v0 | 0.27 | 0.2 | 0.333333 | skip: weak positive MinimalSB_lam0p001 1M mean about 0.33 > VF 0.27; wait for a real stable mode |
| scene-play-singletask-task1-v0 | 0.99 |  |  | skip: high Value Flow baseline easy task, not a repair target |
| scene-play-singletask-task2-v0 | 0.97 |  |  | skip: high Value Flow baseline easy task, not a repair target |
| scene-play-singletask-task3-v0 | 0.94 |  |  | skip: high Value Flow baseline easy task, not a repair target |

## Unstable Queue

| env | best 300k | best 1M mean | plan |
|---|---:|---:|---|
| scene-play-singletask-task4-v0 | 0.4 | 0 | held: unstable task and stable variant unavailable; do 300k curves first |
| puzzle-4x4-play-singletask-task4-v0 | 0.5 | 0.1 | held: unstable task and stable variant unavailable; do 300k curves first |
| puzzle-4x4-play-singletask-task5-v0 | 0.1 | 0 | held: unstable task and stable variant unavailable; do 300k curves first |

## Pending Stage A Runs

| env | config | seed | target_steps | reason |
|---|---|---:|---:|---|
| cube-triple-play-singletask-task2-v0 | P0_particle | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task2-v0 | MinimalSB_lam0p0003 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task2-v0 | MinimalSB_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task2-v0 | A1_action_std_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task2-v0 | A2_action_std_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task2-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task2-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task4-v0 | P0_particle | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task4-v0 | MinimalSB_lam0p0003 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task4-v0 | MinimalSB_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task4-v0 | A1_action_std_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task4-v0 | A2_action_std_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task4-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task4-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task5-v0 | P0_particle | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task5-v0 | MinimalSB_lam0p0003 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task5-v0 | MinimalSB_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task5-v0 | A1_action_std_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task5-v0 | A2_action_std_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task5-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-triple-play-singletask-task5-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-4x4-play-singletask-task1-v0 | P0_particle | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-4x4-play-singletask-task1-v0 | MinimalSB_lam0p0003 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-4x4-play-singletask-task1-v0 | MinimalSB_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-4x4-play-singletask-task1-v0 | A1_action_std_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-4x4-play-singletask-task1-v0 | A2_action_std_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-4x4-play-singletask-task1-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-4x4-play-singletask-task1-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-4x4-play-singletask-task3-v0 | P0_particle | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-4x4-play-singletask-task3-v0 | MinimalSB_lam0p0003 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-4x4-play-singletask-task3-v0 | MinimalSB_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-4x4-play-singletask-task3-v0 | A1_action_std_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-4x4-play-singletask-task3-v0 | A2_action_std_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-4x4-play-singletask-task3-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-4x4-play-singletask-task3-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| scene-play-singletask-task5-v0 | P0_particle | 2 | 300000 | missing completed Stage A 300k final row |
| scene-play-singletask-task5-v0 | MinimalSB_lam0p0003 | 2 | 300000 | missing completed Stage A 300k final row |
| scene-play-singletask-task5-v0 | MinimalSB_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| scene-play-singletask-task5-v0 | A1_action_std_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| scene-play-singletask-task5-v0 | A2_action_std_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row |
| scene-play-singletask-task5-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| scene-play-singletask-task5-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-double-play-singletask-task5-v0 | P0_particle | 2 | 300000 | missing completed Stage A 300k final row |
| cube-double-play-singletask-task5-v0 | MinimalSB_lam0p0003 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-double-play-singletask-task5-v0 | MinimalSB_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-double-play-singletask-task5-v0 | A1_action_std_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-double-play-singletask-task5-v0 | A2_action_std_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-double-play-singletask-task5-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| cube-double-play-singletask-task5-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-3x3-play-singletask-task4-v0 | P0_particle | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-3x3-play-singletask-task4-v0 | MinimalSB_lam0p0003 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-3x3-play-singletask-task4-v0 | MinimalSB_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-3x3-play-singletask-task4-v0 | A1_action_std_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-3x3-play-singletask-task4-v0 | A2_action_std_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-3x3-play-singletask-task4-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-3x3-play-singletask-task4-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-3x3-play-singletask-task5-v0 | P0_particle | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-3x3-play-singletask-task5-v0 | MinimalSB_lam0p0003 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-3x3-play-singletask-task5-v0 | MinimalSB_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-3x3-play-singletask-task5-v0 | A1_action_std_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-3x3-play-singletask-task5-v0 | A2_action_std_lam0p003 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-3x3-play-singletask-task5-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |
| puzzle-3x3-play-singletask-task5-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | missing completed Stage A 300k final row |

## Pending Stage B Runs

| env | config | seed | target_steps | reason |
|---|---|---:|---:|---|
| cube-triple-play-singletask-task3-v0 | A1_action_std_lam0p001 | 0 | 1000000 | selected top Stage A config for 1M confirmation |
| cube-triple-play-singletask-task3-v0 | A1_action_std_lam0p001 | 1 | 1000000 | selected top Stage A config for 1M confirmation |
| cube-triple-play-singletask-task3-v0 | A1_action_std_lam0p001 | 2 | 1000000 | selected top Stage A config for 1M confirmation |
| cube-triple-play-singletask-task3-v0 | A2_action_std_lam0p003 | 0 | 1000000 | selected top Stage A config for 1M confirmation |
| cube-triple-play-singletask-task3-v0 | A2_action_std_lam0p003 | 1 | 1000000 | selected top Stage A config for 1M confirmation |
| cube-triple-play-singletask-task3-v0 | A2_action_std_lam0p003 | 2 | 1000000 | selected top Stage A config for 1M confirmation |

## Next 10 Commands

### 1. stageA_300k cube-triple-play-singletask-task2-v0 P0_particle seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=cube-triple-play-singletask-task2-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_cube_triple_task2_P0_particle_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.discount=0.995 --agent.bcfm_lambda=3 --agent.confidence_weight_temp=0.03 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.0 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 2. stageA_300k cube-triple-play-singletask-task2-v0 MinimalSB_lam0p0003 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=cube-triple-play-singletask-task2-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_cube_triple_task2_MinimalSB_lam0p0003_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.discount=0.995 --agent.bcfm_lambda=3 --agent.confidence_weight_temp=0.03 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.0003 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 3. stageA_300k cube-triple-play-singletask-task2-v0 MinimalSB_lam0p001 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=cube-triple-play-singletask-task2-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_cube_triple_task2_MinimalSB_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.discount=0.995 --agent.bcfm_lambda=3 --agent.confidence_weight_temp=0.03 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 4. stageA_300k cube-triple-play-singletask-task2-v0 A1_action_std_lam0p001 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=cube-triple-play-singletask-task2-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_cube_triple_task2_A1_action_std_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.discount=0.995 --agent.bcfm_lambda=3 --agent.confidence_weight_temp=0.03 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_value_preserving=false
```

### 5. stageA_300k cube-triple-play-singletask-task2-v0 A2_action_std_lam0p003 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=cube-triple-play-singletask-task2-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_cube_triple_task2_A2_action_std_lam0p003_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.discount=0.995 --agent.bcfm_lambda=3 --agent.confidence_weight_temp=0.03 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.003 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_value_preserving=false
```

### 6. stageA_300k cube-triple-play-singletask-task2-v0 R2_residual_disagree_lam0p001 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=cube-triple-play-singletask-task2-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_cube_triple_task2_R2_residual_disagree_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.discount=0.995 --agent.bcfm_lambda=3 --agent.confidence_weight_temp=0.03 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=flow_residual_disagree --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_value_preserving=false
```

### 7. stageA_300k cube-triple-play-singletask-task2-v0 R3_residual_disagree_typicality_lam0p001 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=cube-triple-play-singletask-task2-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_cube_triple_task2_R3_residual_disagree_typicality_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.discount=0.995 --agent.bcfm_lambda=3 --agent.confidence_weight_temp=0.03 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=flow_residual_disagree_typicality --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_typicality_tau=1.0 --agent.pm_sb_value_preserving=false
```

### 8. stageA_300k cube-triple-play-singletask-task4-v0 P0_particle seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=cube-triple-play-singletask-task4-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_cube_triple_task4_P0_particle_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.discount=0.995 --agent.bcfm_lambda=3 --agent.confidence_weight_temp=0.03 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.0 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 9. stageA_300k cube-triple-play-singletask-task4-v0 MinimalSB_lam0p0003 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=cube-triple-play-singletask-task4-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_cube_triple_task4_MinimalSB_lam0p0003_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.discount=0.995 --agent.bcfm_lambda=3 --agent.confidence_weight_temp=0.03 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.0003 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 10. stageA_300k cube-triple-play-singletask-task4-v0 MinimalSB_lam0p001 seed2

```bash
CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl SDL_VIDEODRIVER=dummy OGBENCH_DATA_DIR=/root/.ogbench/data XDG_CACHE_HOME=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/cache XLA_PYTHON_CLIENT_PREALLOCATE=true XLA_PYTHON_CLIENT_MEM_FRACTION=0.90 /root/miniconda3/bin/conda run -n value-flows python main.py --env_name=cube-triple-play-singletask-task4-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/selective_state_tuning_single4090/exp --wandb_run_group=stageA_300k_cube_triple_task4_MinimalSB_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.discount=0.995 --agent.bcfm_lambda=3 --agent.confidence_weight_temp=0.03 --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

## Counts

- candidate tasks: 13
- skipped tasks: 12
- pending Stage A runs: 63
- pending Stage B runs: 6
- total pending runs: 69

## Suggested Launch Order

1. First batch: cube-triple task2, task3, task4, task5.
2. Second batch: puzzle-4x4 task1/task3 plus unstable 300k curve collection.
3. Capacity batch: scene task5, cube-double task5, puzzle-3x3 task4/task5.

## Git Status At Planning Time

```text
M reports/bad_task_repair_single4090_report.md
AM reports/puzzle3x3_bestseed_5task_single4090_v3_report.md
 M results/experiment_runs.csv
 M results/task_scoreboard.csv
 M results/task_scoreboard.md
 M results/valueflow_task_baselines.csv
A  scripts/run_puzzle3x3_bestseed_5task_single4090_v3.py
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
?? scripts/run_selective_state_tuning_single4090.py
?? scripts/run_table3_pm_actorgeo_problem_envs_4090.py
?? scripts/run_table3_pm_fullsafe_light_remaining_single4090.py
?? scripts/run_table3_pm_fullsafe_official_4090_highmem_ldfix.py
```

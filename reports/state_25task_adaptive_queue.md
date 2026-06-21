# State 25-Task Adaptive Queue

Updated: 2026-06-21T13:33:54

This queue is generated for planning only. No training is launched by the generator. Entries requiring state_stable_v1 are marked because the current code does not expose those flags.

| queue_id | priority | env | action_type | config_name | seed | target_steps | reason | requires_state_stable_v1 | skip_reason |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | cube-double-play-singletask-task5-v0 | 300k_coverage | P0_particle | 2 | 300000 | missing coverage | false |  |
| 2 | 1 | cube-double-play-singletask-task5-v0 | 300k_coverage | R2_residual_disagree_lam0p001 | 2 | 300000 | missing coverage | false |  |
| 3 | 1 | cube-triple-play-singletask-task1-v0 | 300k_coverage | P0_particle | 2 | 300000 | missing coverage | false |  |
| 4 | 1 | cube-triple-play-singletask-task1-v0 | 300k_coverage | R2_residual_disagree_lam0p001 | 2 | 300000 | missing coverage | false |  |
| 5 | 1 | puzzle-3x3-play-singletask-task4-v0 | 300k_coverage | P0_particle | 2 | 300000 | missing coverage | false |  |
| 6 | 1 | puzzle-3x3-play-singletask-task4-v0 | 300k_coverage | R2_residual_disagree_lam0p001 | 2 | 300000 | missing coverage | false |  |
| 7 | 1 | scene-play-singletask-task5-v0 | 300k_coverage | P0_particle | 2 | 300000 | missing coverage | false |  |
| 8 | 1 | scene-play-singletask-task5-v0 | 300k_coverage | R2_residual_disagree_lam0p001 | 2 | 300000 | missing coverage | false |  |
| 9 | 2 | puzzle-4x4-play-singletask-task1-v0 | state_stable_v1_diagnostic | A2_action_std_lam0p003 | 2 | 300000 | best/peak high but final row dropped; do not use peak as final | true | state_stable_v1 flags not implemented in current code |
| 10 | 2 | puzzle-4x4-play-singletask-task4-v0 | state_stable_v1_diagnostic | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | best/peak high but final row dropped; do not use peak as final | true | state_stable_v1 flags not implemented in current code |
| 11 | 2 | scene-play-singletask-task4-v0 | state_stable_v1_diagnostic | P0_particle | 2 | 300000 | best/peak high but final row dropped; do not use peak as final | true | state_stable_v1 flags not implemented in current code |
| 12 | 3 | cube-triple-play-singletask-task3-v0 | 1m_goodcase_confirmation | R2_residual_disagree_lam0p001 | 2 | 1000000 | good completed 300k final; confirm final row at 1M | false |  |
| 13 | 3 | scene-play-singletask-task4-v0 | 1m_goodcase_confirmation | P0_particle | 2 | 1000000 | user-listed current good-case candidate from 300k final; historical 1M collapse risk | false |  |
| 14 | 4 | cube-double-play-singletask-task1-v0 | 300k_coverage | P0_particle | 2 | 300000 | high-baseline coverage only | false |  |
| 15 | 4 | cube-double-play-singletask-task1-v0 | 300k_coverage | R2_residual_disagree_lam0p001 | 2 | 300000 | high-baseline coverage only | false |  |
| 16 | 4 | puzzle-3x3-play-singletask-task1-v0 | 300k_coverage | P0_particle | 2 | 300000 | high-baseline coverage only | false |  |
| 17 | 4 | puzzle-3x3-play-singletask-task1-v0 | 300k_coverage | R2_residual_disagree_lam0p001 | 2 | 300000 | high-baseline coverage only | false |  |
| 18 | 4 | puzzle-3x3-play-singletask-task2-v0 | 300k_coverage | P0_particle | 2 | 300000 | high-baseline coverage only | false |  |
| 19 | 4 | puzzle-3x3-play-singletask-task2-v0 | 300k_coverage | R2_residual_disagree_lam0p001 | 2 | 300000 | high-baseline coverage only | false |  |
| 20 | 4 | scene-play-singletask-task1-v0 | 300k_coverage | P0_particle | 2 | 300000 | high-baseline coverage only | false |  |
| 21 | 4 | scene-play-singletask-task1-v0 | 300k_coverage | R2_residual_disagree_lam0p001 | 2 | 300000 | high-baseline coverage only | false |  |
| 22 | 4 | scene-play-singletask-task2-v0 | 300k_coverage | P0_particle | 2 | 300000 | high-baseline coverage only | false |  |
| 23 | 4 | scene-play-singletask-task2-v0 | 300k_coverage | R2_residual_disagree_lam0p001 | 2 | 300000 | high-baseline coverage only | false |  |
| 24 | 4 | scene-play-singletask-task3-v0 | 300k_coverage | P0_particle | 2 | 300000 | high-baseline coverage only | false |  |
| 25 | 4 | scene-play-singletask-task3-v0 | 300k_coverage | R2_residual_disagree_lam0p001 | 2 | 300000 | high-baseline coverage only | false |  |
| 26 | 99 | cube-double-play-singletask-task2-v0 | skip |  |  |  | locked strong 1M R3 | false | locked strong 1M R3 |
| 27 | 99 | cube-double-play-singletask-task3-v0 | skip |  |  |  | locked strong 1M A2 | false | locked strong 1M A2 |
| 28 | 99 | cube-double-play-singletask-task4-v0 | skip |  |  |  | locked positive 1M A1 | false | locked positive 1M A1 |
| 29 | 99 | puzzle-4x4-play-singletask-task2-v0 | skip |  |  |  | locked weak positive MinimalSB | false | locked weak positive MinimalSB |
| 30 | 99 | puzzle-4x4-play-singletask-task3-v0 | skip |  |  |  | do not run R2 seed1; seed0 failed, seed2 moderate | false | do not run R2 seed1; seed0 failed, seed2 moderate |

## Next Command Previews

### 1. cube-double-play-singletask-task5-v0 / P0_particle

```bash
conda run -n value-flows python main.py --env_name=cube-double-play-singletask-task5-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090/exp --wandb_run_group=state25_300k_coverage_cube_double_task5_P0_particle_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.0 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 2. cube-double-play-singletask-task5-v0 / R2_residual_disagree_lam0p001

```bash
conda run -n value-flows python main.py --env_name=cube-double-play-singletask-task5-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090/exp --wandb_run_group=state25_300k_coverage_cube_double_task5_R2_residual_disagree_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=flow_residual_disagree --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_value_preserving=false
```

### 3. cube-triple-play-singletask-task1-v0 / P0_particle

```bash
conda run -n value-flows python main.py --env_name=cube-triple-play-singletask-task1-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090/exp --wandb_run_group=state25_300k_coverage_cube_triple_task1_P0_particle_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.0 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 4. cube-triple-play-singletask-task1-v0 / R2_residual_disagree_lam0p001

```bash
conda run -n value-flows python main.py --env_name=cube-triple-play-singletask-task1-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090/exp --wandb_run_group=state25_300k_coverage_cube_triple_task1_R2_residual_disagree_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=flow_residual_disagree --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_value_preserving=false
```

### 5. puzzle-3x3-play-singletask-task4-v0 / P0_particle

```bash
conda run -n value-flows python main.py --env_name=puzzle-3x3-play-singletask-task4-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090/exp --wandb_run_group=state25_300k_coverage_puzzle_3x3_task4_P0_particle_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.0 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 6. puzzle-3x3-play-singletask-task4-v0 / R2_residual_disagree_lam0p001

```bash
conda run -n value-flows python main.py --env_name=puzzle-3x3-play-singletask-task4-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090/exp --wandb_run_group=state25_300k_coverage_puzzle_3x3_task4_R2_residual_disagree_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=flow_residual_disagree --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_value_preserving=false
```

### 7. scene-play-singletask-task5-v0 / P0_particle

```bash
conda run -n value-flows python main.py --env_name=scene-play-singletask-task5-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090/exp --wandb_run_group=state25_300k_coverage_scene_task5_P0_particle_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.0 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 8. scene-play-singletask-task5-v0 / R2_residual_disagree_lam0p001

```bash
conda run -n value-flows python main.py --env_name=scene-play-singletask-task5-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090/exp --wandb_run_group=state25_300k_coverage_scene_task5_R2_residual_disagree_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=flow_residual_disagree --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_value_preserving=false
```

### 9. puzzle-4x4-play-singletask-task1-v0 / A2_action_std_lam0p003

```bash
conda run -n value-flows python main.py --env_name=puzzle-4x4-play-singletask-task1-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090/exp --wandb_run_group=state25_state_stable_v1_diagnostic_puzzle_4x4_task1_A2_action_std_lam0p003_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.003 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_value_preserving=false
```

### 10. puzzle-4x4-play-singletask-task4-v0 / R3_residual_disagree_typicality_lam0p001

```bash
conda run -n value-flows python main.py --env_name=puzzle-4x4-play-singletask-task4-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090/exp --wandb_run_group=state25_state_stable_v1_diagnostic_puzzle_4x4_task4_R3_residual_disagree_typicality_lam0p001_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.0 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 11. scene-play-singletask-task4-v0 / P0_particle

```bash
conda run -n value-flows python main.py --env_name=scene-play-singletask-task4-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090/exp --wandb_run_group=state25_state_stable_v1_diagnostic_scene_task4_P0_particle_seed2 --enable_wandb=0 --offline_steps=300000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=action --agent.pm_sb_lambda=0.0 --agent.pm_sb_reliability_normalize=none --agent.pm_sb_value_preserving=false
```

### 12. cube-triple-play-singletask-task3-v0 / R2_residual_disagree_lam0p001

```bash
conda run -n value-flows python main.py --env_name=cube-triple-play-singletask-task3-v0 --seed=2 --save_dir=/root/autodl-tmp/sb-value-flows-runs/state_25task_goal_single4090/exp --wandb_run_group=state25_1m_goodcase_confirmation_cube_triple_task3_R2_residual_disagree_lam0p001_seed2 --enable_wandb=0 --offline_steps=1000000 --online_steps=0 --eval_interval=50000 --eval_episodes=10 --log_interval=25000 --save_interval=999999999 --agent=agents/pm_value_flows.py --agent.pm_minimal_sb=true --agent.pm_weight_type=field_kernel_norm --agent.pm_num_continuations=4 --agent.pm_field_kernel_norm_temp=0.3 --agent.pm_field_kernel_min_scale=1e-6 --agent.pm_actor_energy_coef=0.0 --agent.pm_actor_disagree_coef=0.0 --agent.pm_log_sb_diagnostics=true --agent.pm_sb_reliability_score=flow_residual_disagree --agent.pm_sb_lambda=0.001 --agent.pm_sb_reliability_normalize=std --agent.pm_sb_flow_residual_eps=0.05 --agent.pm_sb_disagree_beta=0.5 --agent.pm_sb_disagree_umax=3.0 --agent.pm_sb_value_preserving=false
```

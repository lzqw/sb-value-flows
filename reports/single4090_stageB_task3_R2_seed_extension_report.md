# Single4090 Task3/R2 Seed Extension Report

Generated: 2026-06-19 17:38:59

## Result

- env: puzzle-4x4-play-singletask-task3-v0
- config: R2_residual_disagree_lam0p001
- seed: 0
- target: 1M
- status: COMPLETED
- final step: 1000000
- final success: 0.0
- final return: -2375.3
- final length: 500.0
- best success: 0.5 @300000
- peak after 500k: 0.5 @550000
- drop from best: -0.5
- VF baseline: 0.30
- final vs VF: -0.3

## Trajectory

`1:0; 50000:0; 100000:0; 150000:0; 200000:0.3; 250000:0.2; 300000:0.5; 350000:0.2; 400000:0.3; 450000:0.1; 500000:0.2; 550000:0.5; 600000:0; 650000:0.1; 700000:0.3; 750000:0.1; 800000:0; 850000:0; 900000:0; 950000:0; 1000000:0`

## Diagnostics

- training/critic/pm/reliability_mean: 16833.156
- training/critic/pm/reliability_std: 49308.1
- training/critic/pm/flow_residual_mean: 110450.95
- training/critic/pm/flow_residual_std: 105561.59
- training/critic/pm/disagree_mean: 15.202335
- training/critic/pm/disagree_std: 62.852013
- training/critic/pm/weight_max: 0.62015015
- training/critic/pm/reliability_ess: 2.4336731

## Interpretation

- task3/R2 is unstable.
- seed2 final = 0.40 > VF 0.30, a moderate good-case.
- seed0 final = 0.00 < VF 0.30, failed confirmation.
- Do not start seed1.
- Best/peak indicate transient learning but cannot be used as final result.

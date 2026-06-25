# Lambda Reliability Parameter Ablation Selection

- Updated: 2026-06-26T01:14:20
- Ablation parameter: `pm_sb_lambda` with fixed R3-style flow-residual-disagree-typicality reliability.
- Lambda mapping: lambda=0 -> `pm_sb_lambda=0`; lambda=0.3 -> `3e-4`; lambda=1 -> `1e-3`; lambda=3 -> `3e-3`.
- 500k runs are screening data and are labeled as such; completed 1M runs are preferred for paper-final use.
- No collapse tasks are included.

| Task | Lambda | pm_sb_lambda | Seed | Final step | Status | Run kind | Final | Best peak | Peak step | Drop | Used in figure | Run dir |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|---:|---|---|
| Cube-double task2 | 0 | 0 | 2 | 500000 | screening_500k | screening_500k | 0.7 | 0.7 | 500000 | 0.0 | True | `/root/autodl-tmp/sb-value-flows-runs/parameter_ablation_lambda_reliability_single4090/exp/lambda_rel_500k_cube_double_task2_lam0_seed2/sd002_20260625_231139` |
| Cube-double task2 | 1 | 0.001 | 2 | 1000000 | completed_1m | completed_1m | 0.9 | 0.9 | 1000000 | 0.0 | True | `/root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_cube_double_task2_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260611_203011` |

## Outputs

- `results/parameter_ablation_lambda_reliability_runs.csv`
- `reports/figures/parameter_ablation/lambda_reliability_state_ablation.svg`
- `reports/figures/parameter_ablation/lambda_reliability_state_ablation.pdf`

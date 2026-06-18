# Single4090 Selective Stage-B 1M Progress

Updated: 2026-06-18T15:50:14

Final success uses the last eval.csv row only. Best and peak-after-500k are diagnostics only.

| task/config/seed | status | final step | final success | best success | best step | peak >=500k | drop from best | VF baseline | beats VF final |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| puzzle-4x4 task1 / P0_particle / seed 2 | COMPLETED | 1000000 | 0.3 | 0.5 | 250000 | 0.5 @ 500000 | -0.2 | 0.36 | False |
| puzzle-4x4 task1 / A2_action_std_lam0p003 / seed 2 | COMPLETED | 1000000 | 0.3 | 0.7 | 300000 | 0.5 @ 700000 | -0.39999999999999997 | 0.36 | False |
| puzzle-4x4 task3 / R2_residual_disagree_lam0p001 / seed 2 | COMPLETED | 1000000 | 0.4 | 0.7 | 850000 | 0.7 @ 850000 | -0.29999999999999993 | 0.3 | True |
| puzzle-4x4 task3 / A1_action_std_lam0p001 / seed 2 | COMPLETED | 1000000 | 0.0 | 0.5 | 250000 | 0.3 @ 500000 | -0.5 | 0.3 | False |

## Paths

- puzzle-4x4 task1 / P0_particle: `/root/autodl-tmp/sb-value-flows-runs/selective_state_stageB_1m_single4090/exp/stageB_1m_puzzle_4x4_task1_P0_particle_seed2/sd002_20260617_230708/eval.csv`
- puzzle-4x4 task1 / A2_action_std_lam0p003: `/root/autodl-tmp/sb-value-flows-runs/selective_state_stageB_1m_single4090/exp/stageB_1m_puzzle_4x4_task1_A2_action_std_lam0p003_seed2/sd002_20260618_031757/eval.csv`
- puzzle-4x4 task3 / R2_residual_disagree_lam0p001: `/root/autodl-tmp/sb-value-flows-runs/selective_state_stageB_1m_single4090/exp/stageB_1m_puzzle_4x4_task3_R2_residual_disagree_lam0p001_seed2/sd002_20260618_072723/eval.csv`
- puzzle-4x4 task3 / A1_action_std_lam0p001: `/root/autodl-tmp/sb-value-flows-runs/selective_state_stageB_1m_single4090/exp/stageB_1m_puzzle_4x4_task3_A1_action_std_lam0p001_seed2/sd002_20260618_113940/eval.csv`

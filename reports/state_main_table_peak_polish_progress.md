# State Main Table Peak Polish Progress

- Updated: 2026-06-24T18:47:36
- Output base: `/root/autodl-tmp/sb-value-flows-runs/state_main_table_peak_polish_single4090`
- Runs recorded: 3

Main reporting uses `best_peak_success`. `final_success` and `drop_final_from_peak` are diagnostics.

| env | config | seed | status | final_step | final_success | best_peak_success | best_peak_step | drop | threshold |
|---|---|---:|---|---:|---:|---:|---:|---:|---|
| puzzle-3x3-play-singletask-task3-v0 | FullSafe | 2 | completed_300k | 300000 | 0.1 | 0.1 | 200000 | 0.0 | >=0.7 |
| puzzle-3x3-play-singletask-task3-v0 | R2_residual_disagree_lam0p001 | 2 | completed_300k | 300000 | 0.0 | 0.0 | 1 | 0.0 | >=0.7 |
| puzzle-3x3-play-singletask-task3-v0 | A2_action_std_lam0p003 | 2 | completed_300k | 300000 | 0.0 | 0.0 | 1 | 0.0 | >=0.7 |

# Current Experiment Results Snapshot

Updated from single4090 local registry.

## Single4090 State-Based Results

### Overall

- Registry runs: 83
- Completed registry runs: 82
- Partial registry runs: 1
- Stage A 300k screening runs: 67 / 67 completed
- Stage B 1M confirmation runs: 15 / 15 completed
- Historical inventory: 193 eval.csv, 188 completed, 5 partial

### Main 1M Results

| Task / config | Seeds | Final success | Mean +/- std | Value Flow baseline | Status |
|---|---:|---|---:|---:|---|
| cube-double task2 / R3 | 0,1,2 | 0.7, 0.9, 0.9 | 0.833 +/- 0.115 | 0.76 | strong positive |
| cube-double task3 / A2 | 0,1,2 | 0.8, 0.8, 0.9 | 0.833 +/- 0.058 | 0.73 | strong positive |
| cube-double task4 / A1 | 0,1,2 | 0.4, 0.3, 0.5 | 0.400 +/- 0.100 | 0.30 | positive |
| puzzle-4x4 task2 / MinimalSB | 0,1,2 | 0.4, 0.1, 0.5 | 0.333 +/- 0.208 | 0.27 | weak positive |
| scene task4 / P0 | 2 | 0.0 | 0.000 | 0.07 | failed / collapsed |
| puzzle-4x4 task4 / R3 | 2 | 0.1 | 0.100 | 0.28 | failed / collapsed |
| puzzle-4x4 task5 / A2 | 2 | 0.0 | 0.000 | 0.13 | failed |

### Best 300k Signals

| Task | Best 300k | 1M outcome | Interpretation |
|---|---:|---:|---|
| scene task4 / P0 | 0.40 | 0.00 | 300k signal collapsed |
| puzzle-4x4 task4 / R3 | 0.50 | 0.10 | 300k signal collapsed |
| cube-double task3 / A2 | 0.50 | 0.83 mean | confirmed strong |
| cube-double task2 / R3 | 0.40 | 0.83 mean | confirmed strong |
| cube-double task4 / A1 | 0.30 | 0.40 mean | confirmed positive |
| puzzle-4x4 task5 / A2 | 0.10 | 0.00 | failed |
| cube-triple task3 / A1 | 0.10 | held for stable mode | weak signal only |

### Partial Runs

- Registry partial: cube-double task2 / R3 / seed0 old run stopped at 900k, success 0.8; not counted because a later completed seed0 exists.
- Historical partials: 4 older PM/table3 runs, not counted as final.

### Historical Notable Results

| Historical run family | Result | Note |
|---|---:|---|
| table3 FullSafe cube-double task2 | 0.8, 0.9, 1.0; mean 0.9 | strong historical result |
| table3 FullSafe-light scene task2 | 1.0, 1.0, 1.0 | high-baseline task but stable |
| table3 ActorGeo cube-triple task1 | mean 0.533 | close to VF 0.59 |
| bestseed puzzle-3x3 task1/2/4/5 seed2 | 1.0 | useful historical evidence |
| bestseed puzzle-3x3 task3 seed2 | 0.1 | task3 remains hard |
| minimal puzzle-3x3 task4 S1-like | mean about 0.588 over 8 seeds | signal but below VF 0.84 |

### Current Single4090 Decision

No more brute-force full-task running.

Immediate 300k queue:

- puzzle-4x4 task1
- puzzle-4x4 task3
- puzzle-3x3 task5

Optional 1M confirmation:

- cube-double task5 / A1 / seed2

Stable-hold queue:

- scene task4
- puzzle-4x4 task4
- puzzle-4x4 task5
- cube-triple task3
- puzzle-3x3 task4

### Full State Task Table

| Env | VF baseline | Best 300k | 300k config | Best 1M mean | 1M std | 1M config | Conclusion |
|---|---:|---:|---|---:|---:|---|---|
| cube-double-play-singletask-task1-v0 | 0.97 | - | - | - | - | - | No completed 1M result |
| cube-double-play-singletask-task2-v0 | 0.76 | 0.4 | R3_residual_disagree_typicality_lam0p001 | 0.833333 | 0.11547 | R3_residual_disagree_typicality_lam0p001 | Above Value Flow baseline |
| cube-double-play-singletask-task3-v0 | 0.73 | 0.5 | A2_action_std_lam0p003 | 0.833333 | 0.057735 | A2_action_std_lam0p003 | Above Value Flow baseline |
| cube-double-play-singletask-task4-v0 | 0.3 | 0.3 | A1_action_std_lam0p001 | 0.4 | 0.1 | A1_action_std_lam0p001 | Above Value Flow baseline |
| cube-double-play-singletask-task5-v0 | 0.69 | - | - | - | - | - | No completed 1M result |
| cube-triple-play-singletask-task1-v0 | 0.59 | - | - | - | - | - | No completed 1M result |
| cube-triple-play-singletask-task2-v0 | 0 | - | - | - | - | - | No completed 1M result |
| cube-triple-play-singletask-task3-v0 | 0.07 | 0.1 | A1_action_std_lam0p001 | - | - | - | No completed 1M result |
| cube-triple-play-singletask-task4-v0 | 0 | - | - | - | - | - | No completed 1M result |
| cube-triple-play-singletask-task5-v0 | 0.02 | - | - | - | - | - | No completed 1M result |
| puzzle-3x3-play-singletask-task1-v0 | 0.99 | - | - | - | - | - | No completed 1M result |
| puzzle-3x3-play-singletask-task2-v0 | 0.98 | - | - | - | - | - | No completed 1M result |
| puzzle-3x3-play-singletask-task3-v0 | 0.97 | 0.2 | P0_particle | - | - | - | No completed 1M result |
| puzzle-3x3-play-singletask-task4-v0 | 0.84 | - | - | - | - | - | No completed 1M result |
| puzzle-3x3-play-singletask-task5-v0 | 0.58 | - | - | - | - | - | No completed 1M result |
| puzzle-4x4-play-singletask-task1-v0 | 0.36 | 0.5 | P0_particle | - | - | - | No completed 1M result |
| puzzle-4x4-play-singletask-task2-v0 | 0.27 | 0.2 | A2_action_std_lam0p003 | 0.333333 | 0.208167 | MinimalSB_lam0p001 | Weak or seed-unstable positive |
| puzzle-4x4-play-singletask-task3-v0 | 0.3 | - | - | - | - | - | No completed 1M result |
| puzzle-4x4-play-singletask-task4-v0 | 0.28 | 0.5 | R3_residual_disagree_typicality_lam0p001 | 0.1 | 0 | R3_residual_disagree_typicality_lam0p001 | 300k signal did not hold at 1M |
| puzzle-4x4-play-singletask-task5-v0 | 0.13 | 0.1 | A2_action_std_lam0p003 | 0 | 0 | A2_action_std_lam0p003 | Below Value Flow baseline |
| scene-play-singletask-task1-v0 | 0.99 | - | - | - | - | - | No completed 1M result |
| scene-play-singletask-task2-v0 | 0.97 | - | - | - | - | - | No completed 1M result |
| scene-play-singletask-task3-v0 | 0.94 | - | - | - | - | - | No completed 1M result |
| scene-play-singletask-task4-v0 | 0.07 | 0.4 | P0_particle | 0 | 0 | P0_particle | 300k signal did not hold at 1M |
| scene-play-singletask-task5-v0 | 0 | - | - | - | - | - | No completed 1M result |

### Source Files on Single4090

- `/root/sb-value-flows/results/task_scoreboard.csv`
- `/root/sb-value-flows/results/historical_experiment_inventory.csv`
- `/root/sb-value-flows/reports/selective_state_tuning_single4090_plan.md`

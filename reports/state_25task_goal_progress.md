# State 25-Task Goal Progress

Updated: 2026-06-21T15:26:41

- No training was launched by this artifact generation step.
- state_stable_v1 was not triggered as a run by this artifact generation step; collapse tasks are queued with stable flags for future explicit execution.
- Final values use eval.csv last rows only; best/peak values remain diagnostic.

## Current Counts

- Tasks with completed 1M final: 16
- Tasks with only completed 300k final: 5
- No-data tasks: 4
- Status counts: {'no_data': 4, '1M_completed': 13, '300k_only': 4, 'collapsed': 3, 'candidate': 1}

## Top Good-Case Candidates

- cube-triple-play-singletask-task3-v0: R2_residual_disagree_lam0p001 final 0.2 vs VF 0.07

## Collapse Diagnostics

- cube-triple-play-singletask-task1-v0: best 0.9 @ 850000, best 1M final 0.6; Priority 2: collapse diagnostic; prefer state_stable_v1 before ordinary rerun.
- puzzle-4x4-play-singletask-task3-v0: best 0.8 @ 250000, best 1M final 0.4; Priority 2: collapse diagnostic; prefer state_stable_v1 before ordinary rerun.
- scene-play-singletask-task4-v0: best 0.9 @ 100000, best 1M final 0; Priority 2: collapse diagnostic; prefer state_stable_v1 before ordinary rerun.

## Domain Coverage Averages

| domain | coverage_average_draft | coverage_available_tasks | coverage_missing_tasks |
|---|---|---|---|
| cube-double-play | 0.725 | 4 | task1 |
| cube-triple-play | 0.16 | 5 |  |
| puzzle-3x3-play | 0.82 | 5 |  |
| puzzle-4x4-play | 0.3 | 5 |  |
| scene-play | 0.5 | 2 | task1;task3;task5 |

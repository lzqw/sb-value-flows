# State 25-Task Goal Progress

Updated: 2026-06-21T13:33:54

- No training was launched by this artifact generation step.
- state_stable_v1 was not triggered as a run; collapse tasks are queued as requiring stable support.
- Final values use eval.csv last rows only.

## Current Counts

- 1M completed tasks: 6
- 300k-only tasks: 5
- Candidate tasks: 1
- Collapsed tasks: 3
- No-data tasks: 10

## Top Candidates

- cube-triple-play-singletask-task3-v0: config R2_residual_disagree_lam0p001, target 1000000, reason good completed 300k final; confirm final row at 1M
- scene-play-singletask-task4-v0: config P0_particle, target 1000000, reason user-listed current good-case candidate from 300k final; historical 1M collapse risk

## Collapse Diagnostics

- puzzle-4x4-play-singletask-task1-v0: best 0.7 @ 300000, recommended Completed 1M final is weak/collapsed; prefer state_stable_v1 diagnostic, no seed extension.
- puzzle-4x4-play-singletask-task4-v0: best 0.5 @ 850000, recommended Completed 1M final is weak/collapsed; prefer state_stable_v1 diagnostic, no seed extension.
- scene-play-singletask-task4-v0: best 0.9 @ 100000, recommended Completed 1M final is weak/collapsed; prefer state_stable_v1 diagnostic, no seed extension.

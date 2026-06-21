# State Domain Summary Table

Updated: 2026-06-21T13:33:54

This is a draft state-domain summary for coverage planning. The 1M-only average uses completed 1M final rows only. The coverage average uses completed 1M final when available, otherwise completed 300k final. The candidate average uses each task's current best final row and is for internal screening only.

| domain | tasks | valueflow_average | one_m_only_average | one_m_completed_tasks | one_m_missing_tasks | coverage_average_draft | coverage_available_tasks | coverage_missing_tasks | candidate_average_internal | candidate_available_tasks |
|---|---|---|---|---|---|---|---|---|---|---|
| cube-double-play | 5 | 0.69 | 0.767 | 3 | task1;task5 | 0.767 | 3 | task1;task5 | 0.767 | 3 |
| cube-triple-play | 5 | 0.136 |  | 0 | task1;task2;task3;task4;task5 | 0.05 | 4 | task1 | 0.05 | 4 |
| puzzle-3x3-play | 5 | 0.872 |  | 0 | task1;task2;task3;task4;task5 | 0.3 | 2 | task1;task2;task4 | 0.3 | 2 |
| puzzle-4x4-play | 5 | 0.268 | 0.26 | 5 |  | 0.26 | 5 |  | 0.42 | 5 |
| scene-play | 5 | 0.594 | 0 | 1 | task1;task2;task3;task5 | 0 | 1 | task1;task2;task3;task5 | 0.4 | 1 |

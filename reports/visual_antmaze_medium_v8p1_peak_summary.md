# Visual Antmaze Medium v8.1 Peak-Centric Summary

Generated from `results/audit_all_visual_runs_4090d.csv` after repair/confirmation runs completed.

## Original 5-task v8.1 strong seed2 table

| task_id | seed | config_name | final_step | status | final_success | best_peak_success | best_peak_step | drop_final_from_peak | notes |
|---|---|---|---|---|---|---|---|---|---|
| task1 | 2 | R2_stable_strong | 1000000 | completed_1m | 0.52 | 0.62 | 800000 | -0.09999999999999998 |  |
| task2 | 2 | R2_stable_strong | 1000000 | completed_1m | 0.4 | 0.74 | 300000 | -0.33999999999999997 | collapse |
| task3 | 2 | R2_stable_strong | 1000000 | completed_1m | 0.48 | 0.54 | 900000 | -0.06000000000000005 |  |
| task4 | 2 | R2_stable_strong | 1000000 | completed_1m | 0.34 | 0.82 | 100000 | -0.4799999999999999 | collapse |
| task5 | 2 | R2_stable_strong | 1000000 | completed_1m | 0.2 | 0.38 | 200000 | -0.18 |  |

## Best completed v8.1 peak per task

| task_id | seed | config_name | final_step | status | final_success | best_peak_success | best_peak_step | drop_final_from_peak | notes |
|---|---|---|---|---|---|---|---|---|---|
| task1 | 2 | R2_stable_strong | 1000000 | completed_1m | 0.52 | 0.62 | 800000 | -0.09999999999999998 |  |
| task2 | 3 | R2_stable_strong | 1000000 | completed_1m | 0.16 | 0.76 | 100000 | -0.6 | collapse;severe_collapse |
| task3 | 2 | R2_stable_strong | 1000000 | completed_1m | 0.48 | 0.54 | 900000 | -0.06000000000000005 |  |
| task4 | 2 | R2_retention_repair | 1000000 | completed_1m | 0.5 | 0.86 | 100000 | -0.36 | collapse |
| task5 | 2 | R2_stable_strong | 1000000 | completed_1m | 0.2 | 0.38 | 200000 | -0.18 |  |

## Notes

- Peak is the primary usable result for this summary.
- Final success and drop are retained as stability diagnostics.
- Task2 seed3 confirms the same peak-then-drop pattern: peak 0.76, final 0.16.
- Task4 retention repair improves final over the original v8.1 strong run: 0.50 vs 0.34, with peak 0.86.

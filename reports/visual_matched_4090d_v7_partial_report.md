# Visual Matched 4090D v7 Partial Report

This report was generated while `visual_matched_4090d_v7` was still running.

## Important

Partial rows are included in `experiment_runs.csv` and `eval_curves_index.csv`, but they must not be treated as final 1M results. Only runs with final eval step >= 1,000,000 are counted as completed final results. Peak success is diagnostic only.

## Registry Snapshot

- Completed v7 rows: 4
- Partial v7 rows: 4
- Completed final rows currently available:
  - visual-antmaze-medium task1 R2: final success 0.20, best 0.78
  - visual-antmaze-medium task2 R2: final success 0.02, best 0.82
  - visual-antmaze-medium task3 R2: final success 0.32, best 0.80
  - visual-antmaze-medium task4 R2: final success 0.40, best 0.86
- Partial rows currently indexed:
  - visual-antmaze-medium task1 R2 partial 200k: success 0.80
  - visual-antmaze-medium task2 R2 partial 200k: success 0.48
  - visual-antmaze-medium task5 R2 partial 700k: success 0.12, best 0.70
  - visual-antmaze-teleport task1 A1 partial 800k: success 0.00, best 0.16

## Current Interpretation

The visual pipeline is functional after the candidate-axis fix. However, v7 matched 1M results so far show instability: several early peaks degrade by final evaluation. The visual results should therefore be used as diagnostic evidence unless the final 1M rows are completed.

## Data Location

- v6: `/root/autodl-tmp/sb-value-flows-runs/visual_bigtable_4090d_v6/`
- v7: `/root/autodl-tmp/sb-value-flows-runs/visual_matched_4090d_v7/`

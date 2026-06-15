# 4090D Visual Registry Update Summary

## Scope

This update adds 4090D visual OGBench results to the experiment registry.

Included:

- `visual_bigtable_4090d_v6`
- `visual_matched_4090d_v7` completed and partial runs
- eval.csv / train.csv path indices
- visual reports and diagnostic notes

## Counts

- v6 scanned eval.csv files: 54
- v6 registry rows: 54 completed
- v6 protocol split: 4 smoke/unknown, 40 300k screening, 10 1M confirmation
- v7 scanned eval.csv files: 8
- v7 registry rows: 4 completed, 4 partial

## Rules

- Completed final result: final eval step >= target steps * 0.98.
- Partial runs are stored in `experiment_runs.csv` and `eval_curves_index.csv`, but they are not used as final 1M results.
- Peaks are stored only for diagnostics and plotting.
- Raw experiment directories, checkpoints, cache files, and wandb files are not committed.

## Notes

The active training directory `/root/sb-value-flows` was not modified or interrupted. This registry update was committed from a separate git worktree at `/root/sb-value-flows-registry-4090d`.

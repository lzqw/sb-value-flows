# Experiment Results Registry

This registry tracks lightweight result metadata for Value Flow experiments. It is designed for GitHub review and downstream plotting without committing raw experiment directories, checkpoints, logs, or cache files.

## Files

- `results/valueflow_task_baselines.csv`: task-level Value Flow paper baselines.
- `results/experiment_runs.csv`: one row per scanned run/seed, including completed, partial, failed, and running runs when detectable.
- `results/eval_curves_index.csv`: file index for plotting curves from raw `eval.csv` and `train.csv`.
- `results/task_scoreboard.csv`: task-level aggregate scoreboard derived from `experiment_runs.csv` and baselines.
- `results/task_scoreboard.md`: GitHub-readable scoreboard summary.

## Update Command

State-based single-4090 runs:

```bash
python scripts/update_results_registry.py \
  --scan_base exp/bad_task_repair_single4090 \
  --server single4090 \
  --machine_tag seeta-codex \
  --modality state \
  --stage auto \
  --output_dir results \
  --commit false
```

Visual matched 4090D runs:

```bash
python scripts/update_results_registry.py \
  --scan_base /root/autodl-tmp/sb-value-flows-runs/visual_matched_4090d_v7/exp \
  --server 4090d \
  --machine_tag 4090d \
  --modality visual \
  --stage visual_v7_matched_1m \
  --output_dir results \
  --commit false
```

## Rules

- Completed runs require `final_step >= target_steps * 0.98`.
- Partial runs are kept in `experiment_runs.csv` but excluded from 1M aggregate winners.
- Scoreboard comparisons use final eval rows only.
- Peak success is recorded for diagnostics and curve analysis, but it does not replace final success.
- Raw `exp/`, `logs/`, checkpoints, wandb files, and caches should not be committed.

## Plotting

Use `results/eval_curves_index.csv` to find raw curve files. The full curve is intentionally left in the original `eval.csv`; this registry stores only metadata and paths.

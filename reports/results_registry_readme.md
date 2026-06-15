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

## Local Backup Paths

`local_backup_path` can be filled during a scan by mapping each remote run directory under `--scan_base` into a local backup root:

```bash
python scripts/update_results_registry.py \
  --scan_base exp/bad_task_repair_single4090 \
  --server single4090 \
  --machine_tag seeta-codex \
  --modality state \
  --stage auto \
  --output_dir results \
  --local_backup_base /home/lzqw/sb_value_flows_remote_results/single4090 \
  --commit false
```

It can also be updated later without rescanning eval files by passing a CSV map with `local_backup_path` and at least one of `run_id`, `eval_csv`, or `run_dir`:

```bash
python scripts/update_results_registry.py \
  --output_dir results \
  --local_backup_map /path/to/local_backup_map.csv \
  --update_local_backup_only true \
  --commit false
```

## Git Revision Fields

`git_branch` and `git_head` are run metadata fields. They may come from a run's saved config or command metadata, and existing rows keep the value recorded when that run was scanned. They are therefore not guaranteed to match the repository's current `HEAD` after later registry updates.

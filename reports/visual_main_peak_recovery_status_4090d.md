# Visual Main Peak Coverage Recovery Status - 2x4090D

Updated: 2026-06-27T06:54:33+08:00

## Remote State

- Host: `autodl-container-d45f429eca-cabc109d`
- Repo: `/root/sb-value-flows`
- Branch: `results/visual-main-table-peak-coverage-4090d`
- HEAD: `a5f7731`
- Active tmux sessions: none
- Active screen sessions: none
- Disk: `/root` 98% used, `/root/autodl-tmp` 99% used with about 889 MiB free
- GPUs: both 4090D GPUs are occupied at 100% utilization

## Active Runs

Two visual-scene 500k peak-sweep runs are active, one per GPU. No new launch is safe until at least one GPU is free.

| domain | task | config | seed | planned_steps | latest_train_step | latest_eval_step | latest_eval_success | run_dir | action |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| visual-scene-play | task2 | R2stableStrong_peak500k | 3 | 500000 | 50000 | 50000 | 0.0 | `/root/autodl-tmp/sb-value-flows-runs/visual_main_peak_coverage_4090d/exp/visual-scene-play_task2_R2stableStrong_peak500k_seed3_20260627_044706` | newly launched before this check; continue |
| visual-scene-play | task5 | R2stableStrong_peak500k | 3 | 500000 | 75000 | 50000 | 0.0 | `/root/autodl-tmp/sb-value-flows-runs/visual_main_peak_coverage_4090d/exp/visual-scene-play_task5_R2stableStrong_peak500k_seed3_20260627_043301` | newly launched before this check; continue |

Both runs were recovered as live `main.py` processes after reconnecting. They are not attached to tmux/screen but remain active as process trees under `conda run`.

## Current Main-Table Row Status

Latest regenerated report: `reports/visual_main_table_peak_summary.md`.

| row | completed_tasks | all_evidence_tasks | completed_best_peak_mean | all_evidence_best_peak_mean | target | status |
|---|---:|---:|---:|---:|---:|---|
| visual-scene-play | 5 | 5 | 0.324 | 0.324 | 0.45 | complete_below_threshold |
| visual-puzzle-3x3-play | 2 | 5 | 0.02 | 0.18 | 0.25 | partial_screening_coverage |
| visual-cube-double-play | 5 | 5 | 0.16 | 0.16 | 0.15 | complete_threshold_met |
| visual-antmaze-teleport-navigate | 5 | 5 | 0.36 | 0.364 | 0.15 | complete_threshold_met |

The scene row is still the priority row because it has five completed cells but remains below the required `best_peak_mean >= 0.45`. The active task2/task5 seed3 runs are the current attempt to improve that row.

## Reporting State

The following lightweight outputs were regenerated from all discovered visual runs and pushed in commit `a5f7731`:

- `results/audit_all_visual_runs_4090d.csv`
- `results/audit_visual_best_peak_table.csv`
- `results/audit_visual_final_table.csv`
- `results/audit_visual_v7_v8_v8p1_comparison.csv`
- `results/audit_visual_collapse_cases.csv`
- `results/plot_data_visual_curves.csv`
- `reports/visual_main_table_peak_summary.md`
- `reports/visual_all_domains_coverage_matrix.md`
- `reports/figures/visual_curves/*.svg`

The report generator now separates completed coverage from partial/screening evidence, so partial runs are not mixed into completed final results.

## Next Action

When the two active scene runs finish:

1. Refresh discovery lists under `/tmp/visual_audit`.
2. Regenerate all audit CSVs, markdown reports, and SVG curves.
3. Commit and push only lightweight outputs.
4. If `visual-scene-play` still remains below threshold, launch the next safe scene peak-sweep cells. Otherwise move to `visual-puzzle-3x3-play`, prioritizing completion of task1/task2/task3 to 500k or clean reruns if resume is unsafe.

Do not launch more runs while both GPUs are occupied. Do not delete old runs or raw checkpoints as part of the reporting commit.

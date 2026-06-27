# Visual Main Peak Coverage Recovery Status - 2x4090D

Updated: 2026-06-27T14:16:59

## Remote State

- Host: `autodl-container-d45f429eca-cabc109d`
- Repo: `/root/sb-value-flows`
- Branch: `results/visual-main-table-peak-coverage-4090d`
- HEAD/origin divergence after fetch: `0 0`
- Active tmux sessions: tmux unavailable
- Active screen sessions: none

### Disk

```text
Filesystem      Size  Used Avail Use% Mounted on
overlay          30G   16G   15G  52% /
/dev/md0         50G   33G   18G  66% /root/autodl-tmp
```

### GPU

```text
0, 22605 MiB, 24564 MiB, 100 %
1, 22077 MiB, 24564 MiB, 100 %
```

## Active Protected Runs

| env | latest_train_step | latest_eval_step | latest_eval_success | best_peak_success | best_peak_step | run_dir | action |
|---|---:|---:|---:|---:|---:|---|---|
| visual-scene-play-singletask-task5-v0 | 350000 | 350000 | 0.0 | 0.0 | 1 | `/root/autodl-tmp/sb-value-flows-runs/visual_main_peak_coverage_4090d/exp/visual-scene-play_task5_R2stableStrong_peak500k_seed3_20260627_043301` | continue; both GPUs busy |
| visual-scene-play-singletask-task2-v0 | 325000 | 300000 | 0.0 | 0.08 | 150000 | `/root/autodl-tmp/sb-value-flows-runs/visual_main_peak_coverage_4090d/exp/visual-scene-play_task2_R2stableStrong_peak500k_seed3_20260627_044706` | continue; both GPUs busy |

## Current Non-Medium Row Status

| row | completed_tasks | all_evidence_tasks | completed_best_peak_mean | all_evidence_best_peak_mean | target | status |
|---|---:|---:|---:|---:|---:|---|
| visual-scene-play | 5 | 5 | 0.324 | 0.324 | 0.45 | complete_below_threshold |
| visual-puzzle-3x3-play | 2 | 5 | 0.02 | 0.18 | 0.25 | partial_screening_coverage |
| visual-cube-double-play | 5 | 5 | 0.16 | 0.16 | 0.15 | complete_threshold_met |
| visual-antmaze-teleport-navigate | 5 | 5 | 0.36 | 0.364 | 0.15 | complete_threshold_met |

## Cell Classification

### visual-scene-play

| task | completed_status | completed_peak | completed_step | all_evidence_status | all_evidence_peak | all_evidence_step | action |
|---|---|---:|---:|---|---:|---:|---|
| task1 | completed_300k | 1.0 | 300000 | completed_300k | 1.0 | 300000 | row below threshold; revisit after active reruns finish |
| task2 | completed_500k | 0.12 | 500000 | completed_500k | 0.12 | 500000 | active seed3 500k rerun protected |
| task3 | completed_500k | 0.4 | 500000 | completed_500k | 0.4 | 500000 | row below threshold; revisit after active reruns finish |
| task4 | completed_300k | 0.1 | 300000 | completed_300k | 0.1 | 300000 | row below threshold; revisit after active reruns finish |
| task5 | completed_500k | 0.0 | 500000 | completed_500k | 0.0 | 500000 | active seed3 500k rerun protected |

### visual-puzzle-3x3-play

| task | completed_status | completed_peak | completed_step | all_evidence_status | all_evidence_peak | all_evidence_step | action |
|---|---|---:|---:|---|---:|---:|---|
| task1 |  |  |  | partial | 0.86 | 300000 | needs clean/resumed 300k/500k completion after GPU frees |
| task2 |  |  |  | partial | 0.0 | 200000 | needs clean/resumed 300k/500k completion after GPU frees |
| task3 |  |  |  | partial | 0.0 | 200000 | needs clean/resumed 300k/500k completion after GPU frees |
| task4 | completed_500k | 0.02 | 500000 | completed_500k | 0.02 | 500000 | covered |
| task5 | completed_500k | 0.02 | 500000 | completed_500k | 0.02 | 500000 | covered |

### visual-cube-double-play

| task | completed_status | completed_peak | completed_step | all_evidence_status | all_evidence_peak | all_evidence_step | action |
|---|---|---:|---:|---|---:|---:|---|
| task1 | completed_300k | 0.3 | 300000 | completed_300k | 0.3 | 300000 | do not rerun |
| task2 | completed_1m | 0.0 | 1000000 | completed_1m | 0.0 | 1000000 | do not rerun |
| task3 | completed_1m | 0.1 | 1000000 | completed_1m | 0.1 | 1000000 | do not rerun |
| task4 | completed_300k | 0.1 | 300000 | completed_300k | 0.1 | 300000 | do not rerun |
| task5 | completed_1m | 0.3 | 1000000 | completed_1m | 0.3 | 1000000 | do not rerun |

### visual-antmaze-teleport-navigate

| task | completed_status | completed_peak | completed_step | all_evidence_status | all_evidence_peak | all_evidence_step | action |
|---|---|---:|---:|---|---:|---:|---|
| task1 | completed_300k | 0.4 | 300000 | completed_300k | 0.4 | 300000 | do not rerun |
| task2 | completed_300k | 0.4 | 300000 | completed_300k | 0.4 | 300000 | do not rerun |
| task3 | completed_300k | 0.3 | 300000 | partial | 0.32 | 400000 | do not rerun |
| task4 | completed_1m | 0.5 | 1000000 | completed_1m | 0.5 | 1000000 | do not rerun |
| task5 | completed_300k | 0.2 | 300000 | completed_300k | 0.2 | 300000 | do not rerun |

## Reporting State

Regenerated from all discovered runs before launching anything:

- `results/audit_visual_best_peak_table.csv`
- `results/audit_visual_final_table.csv`
- `results/audit_visual_v7_v8_v8p1_comparison.csv`
- `results/audit_visual_collapse_cases.csv`
- `results/plot_data_visual_curves.csv`
- `reports/visual_main_table_peak_summary.md`
- `reports/visual_all_domains_coverage_matrix.md`
- `reports/figures/visual_curves/*.svg`

## Next Action

No new launch is safe while both 4090D GPUs are occupied. When one current scene run finishes, rerun `python3 scripts/run_visual_main_peak_scheduler_4090d.py`; it should keep work to 300k/500k peak-sweep jobs and prioritize scene until the threshold is met, then puzzle task1/task2/task3 completion.

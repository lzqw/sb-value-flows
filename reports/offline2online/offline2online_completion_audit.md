# Offline-to-online completion audit

Updated: 2026-07-08 14:41 CST

This audit tracks the original offline-to-online goal after the local Codex machine was powered off and restarted. Evidence is from the live single4090 server at `root@connect.cqa1.seetacloud.com -p 31499`, repo `/root/sb-value-flows`, branch `results/offline2online-single4090`.

## Recovery audit

- Host: `autodl-container-5f5c489a58-488668bd`.
- GPU: one NVIDIA vGPU-48GB. At recovery audit time, GPU 0 was busy with PID `598242`, using about `18482 MiB`, `100%` utilization.
- Active `main.py`: Ours pretrain on `cube-triple-play-singletask-task1-v0`, seed3, config `actorgeo500k_t0p3`, run root `/root/autodl-tmp/sb-value-flows-runs/offline2online_single4090/exp/o2o_pretrain_cube-triple-task1_ours_actorgeo500k_t0p3_seed3`. This is post-final/extra work, not a duplicate of the selected final cube-double, puzzle-4x4, or scene curves.
- Active job progress at audit: `eval.csv` reached step `400000`; `train.csv` reached step `425000`; best observed eval success `0.4`.
- Queues: no `continue_offline2online_stageb.sh`, `continue_offline2online_stagec.sh`, `launch_stagec_after_stageb.sh`, or repair queue process was active.
- Session managers: `tmux` is not installed. `screen -ls` showed only old dead sockets.
- Disk: `/` 56% used, `/autodl-pub` 95% used with 421G available, `/autodl-pub/data` 65% used with 1.5T available.
- No duplicate job was launched during this recovery pass.

## Requirement status

| Requirement | Current evidence | Status |
| --- | --- | --- |
| Remote state audited after shutdown | Live `nvidia-smi`, `ps aux | grep main.py`, `tmux ls`, `screen -ls`, `df -h`, branch, git status, queue logs, and run status were inspected on 2026-07-08. | Complete |
| Running jobs reattached/monitored or safely resumed | The only active `main.py` was identified as the post-final `cube-triple-task1` Ours pretrain seed3. It was left running and not duplicated. No Stage B/C queue was active. | Complete |
| Repository branch restored | Remote repo is on `results/offline2online-single4090`. Git status is dirty with experiment/report outputs and code changes; dirty files are intentionally retained for commit selection rather than discarded. | Complete |
| Offline-to-online runner works for our method | `main.py` supports restore, online step-0 eval, online environment interaction, online replay insertion, mixed replay via `online_sample_ratio`, metadata, and summary files. `scripts/run_offline2online.py` launches pretrain, screening, final, collect, checkpoint scan, plot, and status modes. Smoke, screening, and final Ours runs completed. | Complete |
| At least 3 selected scenarios have valid curves | `results/offline2online_runs.csv` has final `completed_1m` runs for `cube-double`, `puzzle-4x4`, and `scene`. `results/offline2online_curve_data.csv` has selected curve points for each panel. | Complete |
| Each plotted curve has at least 2 seeds | For every selected scenario and method, `seed2` and `seed3` final runs are marked `used_in_final_figure=True`. | Complete |
| Ours, Value Flows, and one additional baseline are plotted | Selected final matrix includes Ours (`pm_value_flows`), Value Flows, and FQL for all three scenarios. | Complete |
| Step 0 is the offline checkpoint evaluation | Every selected scenario/method/seed in `results/offline2online_curve_data.csv` has a selected point at step `0` and reaches step `1000000`. | Complete |
| CSV/report/figures regenerated | Regenerated lightweight artifacts include `results/offline2online_runs.csv`, `results/offline2online_curve_data.csv`, `results/offline2online_checkpoint_sources.csv`, `results/offline2online_tuning_runs.csv`, `reports/offline2online/offline2online_summary.md`, `reports/offline2online/offline2online_tuning_summary.md`, `reports/offline2online/offline2online_selected_runs.md`, and `reports/figures/offline2online/offline2online_selected3.{svg,pdf,png}`. | Complete |
| No duplicate jobs launched | `run_offline2online.py` and queue scripts guard on active `main.py`; recovery audit did not start a duplicate. | Complete |

## Final selected matrix

All selected final runs below are `completed_1m` and `used_in_final_figure=True`.

| scenario | method | seeds | online steps | curve points per seed |
| --- | --- | --- | --- | --- |
| cube-double | ours | 2, 3 | 0 to 1000000 | 22 |
| cube-double | value_flows | 2, 3 | 0 to 1000000 | 22 |
| cube-double | fql | 2, 3 | 0 to 1000000 | 22 |
| puzzle-4x4 | ours | 2, 3 | 0 to 1000000 | 22 |
| puzzle-4x4 | value_flows | 2, 3 | 0 to 1000000 | 22 |
| puzzle-4x4 | fql | 2, 3 | 0 to 1000000 | 22 |
| scene | ours | 2, 3 | 0 to 1000000 | 22 |
| scene | value_flows | 2, 3 | 0 to 1000000 | 22 |
| scene | fql | 2, 3 | 0 to 1000000 | 22 |

## Artifact check

- `reports/figures/offline2online/offline2online_selected3.png`: PNG, 2400 x 680.
- `reports/figures/offline2online/offline2online_selected3.pdf`: one-page PDF.
- `reports/figures/offline2online/offline2online_selected3.svg`: SVG figure.
- `results/offline2online_curve_data.csv`: selected final curves have step 0 and step 1000000 for all 18 scenario/method/seed combinations.
- `scripts/run_offline2online.py --mode status`: reports all 18 required final runs as `final:completed_1m`.

## Remaining note

The selected final Ours curves are valid and complete, but their measured success is weak on these three primary tasks. Later tuning/generalization runs are retained as additional evidence and are not required for the original final figure.

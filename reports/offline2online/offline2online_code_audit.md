# Offline-to-online code audit

Audit date: 2026-07-08
Branch: `results/offline2online-single4090`
Repo: `/root/sb-value-flows`

## Recovery server state

- Host: `autodl-container-5f5c489a58-488668bd`.
- GPU: one NVIDIA vGPU-48GB. At the 2026-07-08 recovery audit, the GPU was occupied by a post-final Ours pretrain job on `cube-triple-play-singletask-task1-v0`, seed3, not by a duplicate selected final run.
- Active final queues: none. Stage B and Stage C logs show Stage C completed on 2026-07-07 20:01 CST.
- Session managers: `tmux` is not installed; `screen -ls` showed only dead sockets.
- Disk: raw O2O outputs remain under `/root/autodl-tmp/sb-value-flows-runs/offline2online_single4090`.

## Existing online/offline-to-online support

`main.py` supports the mechanics needed for offline-to-online fine-tuning:

- `restore_path` / `restore_epoch` restore a saved Flax agent from an offline checkpoint.
- `offline_steps` trains from the static OGBench dataset.
- `online_steps` switches to environment interaction.
- Online transitions are inserted into replay.
- `balanced_sampling` can keep a separate online replay buffer.
- `online_sample_ratio` controls the online/offline replay mixture.
- `eval_at_step0=true` evaluates the restored offline checkpoint before online interaction.
- `eval.csv`, `train.csv`, `command.txt`, `checkpoint_metadata.json`, and `summary.json` are written for O2O runs.

The online loop uses RPG policy extraction for `value_flows` and `pm_value_flows` during online action selection and online-phase evaluation.

## O2O runner

`scripts/run_offline2online.py` provides:

- `pretrain`: create finite-save offline checkpoints for restored online runs.
- `launch`: start one online run and refuse duplicate launch while another `main.py` is active.
- `checkpoints`: scan O2O pretrain outputs for `params_*.pkl` and write `results/offline2online_checkpoint_sources.csv`.
- `collect`: parse run folders into `results/offline2online_runs.csv`, `results/offline2online_curve_data.csv`, and markdown summaries.
- `plot`: generate the selected three-panel final figure.
- `plot_progress`: generate the current progress figure.
- `status`: report the required final matrix for cube-double, puzzle-4x4, and scene across Ours, Value Flows, FQL, seeds 2 and 3.

Queue helpers:

- `scripts/continue_offline2online_stageb.sh`
- `scripts/continue_offline2online_stagec.sh`
- `scripts/repair_stageb_queue_once.sh`
- `scripts/launch_stagec_after_stageb.sh`

These scripts check for active `main.py` processes before launching the next job.

## Offline checkpoint initialization

The runner uses `results/offline2online_checkpoint_sources.csv` to map `(method, env, seed)` to a checkpoint path and restore epoch. Stage B and Stage C created fresh `>=500k` pretrain checkpoints for all selected final scenario/method/seed combinations before launching restored online runs.

No selected final curve is described as restored-from-offline unless `checkpoint_metadata.json` records a real restore source.

## Runnable comparison methods

The final comparison uses:

- Ours: `agents/pm_value_flows.py`
- Value Flows: `agents/value_flows.py`
- FQL: `agents/fql.py`

Additional runnable local baselines include IQL, IFQL, and IQN. RLPD was not found as a runnable local implementation.

## Final completion status

Current generated artifacts show the original final matrix is complete:

- `results/offline2online_runs.csv`: 73 discovered O2O runs, including 18 selected final `completed_1m` runs.
- `results/offline2online_curve_data.csv`: selected final curves for all 18 scenario/method/seed combinations, each with step 0 and step 1000000.
- `reports/offline2online/offline2online_summary.md`: regenerated run inventory.
- `reports/offline2online/offline2online_tuning_summary.md`: 20 documented Ours tuning attempts.
- `reports/offline2online/offline2online_selected_runs.md`: selected final run list.
- `reports/figures/offline2online/offline2online_selected3.svg`
- `reports/figures/offline2online/offline2online_selected3.pdf`
- `reports/figures/offline2online/offline2online_selected3.png`

`scripts/run_offline2online.py --mode status` reports all required final runs as `final:completed_1m`:

- cube-double: Ours, Value Flows, FQL, seeds 2 and 3.
- puzzle-4x4: Ours, Value Flows, FQL, seeds 2 and 3.
- scene: Ours, Value Flows, FQL, seeds 2 and 3.

The selected Ours final curves are complete but weak in measured success. Extra post-final tuning/generalization runs are retained separately and are not used in the selected final figure unless explicitly promoted later.

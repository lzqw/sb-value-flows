# Offline-to-online code audit

Audit date: 2026-07-02
Branch: `results/offline2online-single4090`
Repo: `/root/sb-value-flows`

## Server state

- GPU: one NVIDIA vGPU-48GB, idle at audit time (`0 MiB`, `0%` utilization).
- Active training: no `main.py` process was running.
- Session managers: `tmux` is not installed; `screen -ls` previously showed only dead sockets.
- Disk: output is kept under `/root/autodl-tmp/sb-value-flows-runs/offline2online_single4090` to avoid touching paper-ready ablation folders.

## Existing online/offline-to-online code

`main.py` already supported the basic mechanics needed for online fine-tuning:

- `restore_path` / `restore_epoch` can restore a saved Flax agent.
- `offline_steps` trains from the static OGBench dataset.
- `online_steps` switches to environment interaction.
- Online transitions are written to a `ReplayBuffer`.
- `balanced_sampling` creates a separate online replay buffer and can mix offline dataset samples with online samples.
- `eval.csv` and `train.csv` are written by the standard CSV loggers.

The existing online loop uses RPG policy extraction for `value_flows` and `pm_value_flows` during online action selection and online-phase evaluation.

## Missing before this pass

The repo did not have a dedicated offline-to-online orchestration script for the requested three-panel figure. The following pieces were also missing or incomplete:

- No online step-0 evaluation of a restored offline checkpoint.
- No configurable online/offline replay ratio; `balanced_sampling` was effectively fixed at half online and half offline.
- No standard `command.txt`, checkpoint metadata, or final `summary.json` for O2O runs.
- No collector/plotter for the requested Value-Flows-style curves.
- No separate O2O output tree, CSV summaries, or selected-runs report.

## Implemented O2O support

`main.py` now adds:

- `--eval_at_step0=true` to evaluate the initialized or restored agent before online interaction.
- `--online_sample_ratio` for configurable balanced replay, e.g. `1.0`, `0.75`, or `0.5` online samples per batch.
- `command.txt` in every run directory.
- `checkpoint_metadata.json` with restore source and save settings.
- `summary.json` with final success, best peak success, best step, and peak-to-final drop.

`scripts/run_offline2online.py` now provides:

- `launch`: starts one O2O run and refuses duplicate launches when another `main.py` is active.
- `pretrain`: starts an offline-only run with finite checkpoint saving so restored O2O runs can be created when old checkpoints are unavailable.
- `checkpoints`: scans O2O pretrain outputs for `params_*.pkl` and writes `results/offline2online_checkpoint_sources.csv`.
- `collect`: parses run folders into `results/offline2online_runs.csv` and `results/offline2online_curve_data.csv`.
- `plot`: generates `reports/figures/offline2online/offline2online_selected3.svg`, `.pdf`, and `.png` once final-eligible runs exist.
- `status`: reports the final matrix for cube-double, puzzle-4x4, and scene across Ours, Value Flows, FQL, seeds 2 and 3.

All O2O raw outputs are separated under:

- `/root/autodl-tmp/sb-value-flows-runs/offline2online_single4090`

Lightweight reports and summaries are under:

- `/root/sb-value-flows/reports/offline2online`
- `/root/sb-value-flows/reports/figures/offline2online`
- `/root/sb-value-flows/results/offline2online_runs.csv`
- `/root/sb-value-flows/results/offline2online_curve_data.csv`

## Offline checkpoint initialization

The runner supports checkpoint initialization through:

- `results/offline2online_checkpoint_sources.csv`

Rows map `(method, env, seed)` to `restore_path` and `restore_epoch`. If a row is present, `launch` passes those restore flags into `main.py`.

Current audit result: old experiment folders contain many useful `flags.json`, `eval.csv`, and `train.csv` files for the target or backup scenarios, but most were run with very large `save_interval` values and do not contain `params_*.pkl`. A broad checkpoint search found only a small set of saved parameter files under `exp/pm_medium_1m_methods_4090`, not matching the three requested primary O2O environments. Therefore, current primary O2O runs should either:

- run a smoke test without restore to validate online mechanics, then
- create fresh offline checkpoints for the selected method/scenario/seed combinations with a finite save interval, or
- add explicit mappings if matching checkpoints are found later.

The initial O2O checkpoint-source scan wrote an empty `results/offline2online_checkpoint_sources.csv`, confirming no O2O pretrain checkpoint has been produced yet.

No curves should be described as restored-from-offline unless `checkpoint_metadata.json` records a real `restore_path`.

## Online replay construction

For online fine-tuning:

- `balanced_sampling=1` creates an initially empty online replay buffer using one offline transition as the shape template.
- Each environment transition is inserted into the online replay buffer.
- The update batch is built from:
  - `round(batch_size * online_sample_ratio)` samples from online replay, and
  - the remainder from the offline dataset.
- `online_sample_ratio=1.0` is online-only replay after restore.
- `online_sample_ratio=0.75` and `0.5` are supported for mixed replay tuning.

If `balanced_sampling=0`, the replay buffer is initialized from the offline dataset and online transitions are appended to the same buffer.

## Runnable baselines

Available directly:

- Value Flows: `agents/value_flows.py`
- FQL: `agents/fql.py`
- IQL: `agents/iql.py`
- IFQL: `agents/ifql.py`
- IQN: `agents/iqn.py`

Not found as a runnable local implementation:

- RLPD

The minimum final comparison is configured as:

- Ours: `agents/pm_value_flows.py`
- Value Flows: `agents/value_flows.py`
- FQL: `agents/fql.py`

## Current completion status

Implementation scaffolding is in place, but the full objective is not complete yet:

- Stage A smoke still needs to finish and be validated.
- Final curves require 3 scenarios x 3 methods x 2 seeds.
- Every plotted curve still needs at least two real seeds.
- Final SVG/PDF/PNG are not valid until final-eligible runs exist.
- Ours tuning attempts still need to be recorded in `results/offline2online_tuning_runs.csv` and `reports/offline2online/offline2online_tuning_summary.md`.

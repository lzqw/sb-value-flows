# Visual Stable v8 Runtime Check

Generated: 2026-06-16T15:12:04

## Training State

- `main.py` running during final check: no
- GPU0/GPU1 after smoke: idle, 0 MiB, 0% utilization
- Formal 1M training launched: no
- Ordinary visual v7 resumed: no

## Main Snapshot Check

Confirmed `origin/main:results/current_results_snapshot.md` contains the interrupted visual v7 conclusion:

- visual-antmaze-medium R2 completed 5-task final mean = 0.212
- visual-antmaze-medium R2 best-in-run mean = 0.792
- interpretation: strong early learning, severe late-training collapse; diagnostic, not final-performance positive

## Stable Flags Implemented

Implemented and runtime-smoke-tested:

- `visual_stable_mode`: master gate; default false.
- `save_eval_checkpoints`: saves eval checkpoints, best-eval checkpoints, and final checkpoint when enabled.
- `visual_freeze_encoder_after_step`: implemented as an encoder-gradient mask in PM update after the configured step; default disabled.
- `visual_actor_lr_decay_after_step` / `visual_actor_lr_decay_mult`: implemented as actor loss multiplier schedule; default no-op.
- `visual_critic_lr_decay_after_step` / `visual_critic_lr_decay_mult`: implemented as critic loss multiplier schedule; default no-op.
- `visual_second_lr_decay_after_step` / second actor/critic multipliers: implemented as second-stage multipliers; default no-op.
- `actor_ema_anchor_*`: implemented as a behavior-anchor approximation against dataset actions after the configured step. This is not a true EMA teacher yet.
- `pm_sb_weight_uniform_mix`: implemented for PM/SB reliability weights; default 0.
- `pm_sb_weight_logit_clip`: implemented with `-1.0` sentinel disabled by default.
- `pm_sb_weight_max`: implemented with `-1.0` sentinel disabled by default.
- `checkpoint_dir`: parser-compatible string config for dry-run command recording; actual checkpoint saving uses `save_dir/checkpoints`.

## Modified Files and Functions

- `agents/pm_value_flows.py`
  - PM/SB weight clipping, uniform mixing, and max cap in critic target weighting.
  - stable diagnostics aliases for SB weight mean/std/max/top10 mass.
  - behavior-anchor approximation in `actor_loss`.
  - actor/critic first and second stage loss multiplier schedules in `total_loss`.
  - target tau schedule support.
  - encoder gradient masking in `update` through `grad_transform`.
  - default-off config entries for all stable flags.
- `utils/flax_utils.py`
  - optional `grad_transform` argument in `TrainState.apply_loss_fn`, default no-op.
- `main.py`
  - passes step into PM updates.
  - logs `evaluation/success_best_so_far`, `evaluation/best_step`, and `evaluation/drop_from_best`.
  - saves eval, best_eval, and final checkpoints when `save_eval_checkpoints=true`.
- `scripts/run_visual_stable_v8_4090d.py`
  - dry-run command order fixed: `--agent=agents/pm_value_flows.py` precedes every `--agent.*` flag.

## Dry-Run

Dry-run passed and planned exactly 3 diagnostic runs:

1. `visual-antmaze-medium-navigate-singletask-task1-v0 / R2_stable / seed2 / 1M`
2. `visual-antmaze-medium-navigate-singletask-task2-v0 / R2_stable / seed2 / 1M`
3. `visual-antmaze-medium-navigate-singletask-task4-v0 / R2_stable / seed2 / 1M`

Plan file: `/root/sb-value-flows/reports/visual_stable_v8_plan.md`
Data-disk status: `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/reports/visual_stable_v8_status.md`

## Smoke

A single runtime smoke was run only for parameter validation:

- env: `visual-antmaze-medium-navigate-singletask-task1-v0`
- config: `R2_stable`
- seed: 2
- offline_steps: 1000
- eval_episodes: 2
- batch_size: 64
- num_samples: 4
- num_flow_steps: 5
- formal result: no, not counted in scoreboard
- exit code: 0

Smoke eval CSV:

- `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/exp/smoke_visual_stable_v8_task1_r2_seed2_1000_freeze_mask/smoke_visual_stable_v8_task1_r2_seed2_1000_freeze_mask/sd002_20260616_150702/eval.csv`

Smoke train CSV:

- `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_4090d/exp/smoke_visual_stable_v8_task1_r2_seed2_1000_freeze_mask/smoke_visual_stable_v8_task1_r2_seed2_1000_freeze_mask/sd002_20260616_150702/train.csv`

Checkpoint files created: 5

- eval checkpoints: yes
- best_eval checkpoints: yes
- final checkpoint: yes

Stable diagnostics were present in `train.csv`, including:

- `training/actor/actor_anchor_loss`
- `training/actor/actor_anchor_gate`
- `training/stable/actor_lr`
- `training/stable/critic_lr`
- `training/stable/encoder_frozen`
- `training/critic/stable/sb_weight_mean`
- `training/critic/stable/sb_weight_std`
- `training/critic/stable/sb_weight_max`
- `training/critic/stable/sb_weight_top10_mass`

## Remaining Caveats

- `actor_ema_anchor_*` currently uses a behavior-anchor approximation, not a true EMA actor teacher.
- Actor/critic LR decay is implemented as separate actor/critic loss multipliers under the existing shared optimizer, not separate optimizer learning-rate schedules.
- Encoder freeze is implemented by masking encoder gradients after the threshold; the 1000-step smoke validates the code path but does not cross the 300k threshold.

## Launch Readiness

It is technically safe to launch the 3 planned visual stable 1M diagnostics after explicit user approval. The launch should be treated as diagnostic, with the caveats above recorded. No formal 1M training was started in this check.

# Visual Stable v8 Task2 Diagnostic

Previous completed diagnostic run.

## Result

- Env: `visual-antmaze-medium-navigate-singletask-task2-v0`
- Config: `R2_stable`
- Seed: 2
- Status: COMPLETED
- Final success: 0.26 @ 1000000
- Best success: 0.74 @ 100000
- Peak after 500k: 0.56 @ 500000
- Drop from best: -0.48

## Comparison

- v7 task2 / R2: best 0.82, final 0.02.
- v8 task2 / R2_stable: best 0.74, final 0.26.
- Conclusion: v8 improves retention versus v7, but late collapse remains.
- This is diagnostic, not a final positive.
- Do not use best checkpoint as final.
- Do not expand task1/task4 under current `R2_stable`.
- Next config: `R2_stable_strong`.

## Trajectory

`0:0.0, 100k:0.74, 200k:0.58, 300k:0.56, 400k:0.5, 500k:0.56, 600k:0.48, 700k:0.28, 800k:0.28, 900k:0.3, 1M:0.26`

## CSV Paths

- eval: `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_task2_diagnostic/exp/visual_stable_v8_task2_R2_stable_seed2_1m/visual_stable_v8_task2_R2_stable_seed2_1m/sd002_20260616_162650/eval.csv`
- train: `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_task2_diagnostic/exp/visual_stable_v8_task2_R2_stable_seed2_1m/visual_stable_v8_task2_R2_stable_seed2_1m/sd002_20260616_162650/train.csv`

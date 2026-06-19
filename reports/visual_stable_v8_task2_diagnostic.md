# Visual Stable v8.1 Task2 Diagnostic

Generated: 2026-06-19 12:15:07

## Result

`visual-antmaze-medium-navigate-singletask-task2-v0 / R2_stable_strong / seed2 / 1M` is completed.

- final step: 1000000
- final success: 0.4
- best success: 0.74 @ 300000
- peak after 500k: 0.56 @ 600000
- drop from best: -0.33999999999999997
- checkpoint count: 16
- eval.csv: `/root/autodl-tmp/sb-value-flows-runs/visual_stable_v8_1_strong_4090d/exp/visual_medium_task2_R2_stable_strong_seed2_1m/visual_medium_task2_R2_stable_strong_seed2_1m/sd002_20260617_230839/eval.csv`

## Trajectory

`1:0; 100000:0.5; 200000:0.62; 300000:0.74; 400000:0.56; 500000:0.48; 600000:0.56; 700000:0.38; 800000:0.3; 900000:0.1; 1000000:0.4`

## Comparison

- v7 task2 / R2: final 0.02, best 0.82 @200k.
- v8 task2 / R2_stable: final 0.26, best 0.74 @100000, peak after 500k 0.56 @500000, drop -0.48.
- v8.1 task2 / R2_stable_strong: final 0.4, best 0.74 @300000, peak after 500k 0.56 @600000, drop -0.33999999999999997.

## Interpretation

v8.1 strong clearly mitigates late collapse, but does not fully solve it. This is a diagnostic stability improvement, not yet a final visual superiority result. Final result uses only the last eval.csv row; best checkpoint and peaks are diagnostics only.

## Next Diagnostic

Run `visual-antmaze-medium-navigate-singletask-task4-v0 / R2_stable_strong / seed2 / 1M` only. Do not start task1, do not rerun task2, and do not continue ordinary v7.

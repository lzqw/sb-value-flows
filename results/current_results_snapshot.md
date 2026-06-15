# Current Results Snapshot

Generated: 2026-06-15

This is a lightweight GitHub-facing table of the current SB-Value-Flows experiment results. It is organized like the Value Flow paper table: each task is listed with the Value Flow baseline, the current best 300k screening result, and the best completed 1M result when available.

**Rules.** Completed 1M final eval rows are used for formal comparison. 300k screening, peak success, and partial runs are diagnostic only and should not replace final success.

## Overview

| item | count |
|---|---:|
| indexed runs in current inventory | 318 |
| completed runs | 313 |
| partial runs | 5 |
| single4090 runs | 79 |
| 4090D runs | 239 |
| state OGBench task rows | 25 |
| visual OGBench task rows | 25 |

## State OGBench Results

| task | Value Flow | best 300k | best completed 1M | config | seeds | delta | status |
|---|---:|---:|---:|---|---|---:|---|
| cube-double task1 | 0.97 ± 0.01 | 1.00 | — | A1 | — | — | 300k only |
| cube-double task2 | 0.76 ± 0.07 | 0.60 | **0.83 ± 0.12** | R3 | 0/1/2 | +0.07 | confirmed above VF |
| cube-double task3 | 0.73 ± 0.04 | 0.50 | **0.83 ± 0.06** | A2 | 0/1/2 | +0.10 | confirmed above VF |
| cube-double task4 | 0.30 ± 0.05 | 0.30 | **0.40 ± 0.10** | A1 | 0/1/2 | +0.10 | confirmed above VF |
| cube-double task5 | 0.69 ± 0.05 | 0.70 | — | A1 | — | — | 300k only |
| scene task1 | 0.99 ± 0.00 | 1.00 | 1.00 ± 0.00 | A1 | 2 | +0.01 | matched / weak positive |
| scene task2 | 0.97 ± 0.01 | 1.00 | 1.00 ± 0.00 | A1 | 2 | +0.03 | matched / weak positive |
| scene task3 | 0.94 ± 0.02 | 0.80 | 1.00 ± 0.00 | A1 | 2 | +0.06 | confirmed above VF |
| scene task4 | 0.07 ± 0.17 | 0.40 | 0.03 ± 0.06 | R2 | 0/1/2 | -0.04 | 300k signal did not hold at 1M |
| scene task5 | 0.00 ± 0.00 | 0.00 | 0.00 ± 0.00 | A1 | 2 | 0.00 | matched low baseline |
| puzzle-3x3 task1 | 0.99 ± 0.00 | — | — | — | — | — | not covered by completed 1M |
| puzzle-3x3 task2 | 0.98 ± 0.02 | — | — | — | — | — | not covered by completed 1M |
| puzzle-3x3 task3 | 0.97 ± 0.01 | 0.20 | — | P0 | — | — | 300k only, far below VF |
| puzzle-3x3 task4 | 0.84 ± 0.24 | 0.20 | 0.79 | FullSafe | — | -0.05 | below VF |
| puzzle-3x3 task5 | 0.58 ± 0.39 | — | — | — | — | — | not covered by completed 1M |
| puzzle-4x4 task1 | 0.36 ± 0.04 | — | — | — | — | — | not covered by completed 1M |
| puzzle-4x4 task2 | 0.27 ± 0.04 | 0.20 | 0.33 ± 0.21 | MinimalSB λ=0.001 | 0/1/2 | +0.06 | weak / seed-unstable positive |
| puzzle-4x4 task3 | 0.30 ± 0.04 | — | — | — | — | — | not covered by completed 1M |
| puzzle-4x4 task4 | 0.28 ± 0.05 | 0.50 | 0.20 | FullSafe | — | -0.08 | 300k signal did not hold at 1M |
| puzzle-4x4 task5 | 0.13 ± 0.02 | 0.10 | 0.00 | A2 | 2 | -0.13 | below VF |
| cube-triple task1 | 0.59 ± 0.12 | 1.00 | 0.65 | — | — | +0.06 | weak / seed-unstable positive |
| cube-triple task2 | 0.00 ± 0.00 | — | 0.00 | R2 | 2 | 0.00 | matched low baseline |
| cube-triple task3 | 0.07 ± 0.03 | 0.10 | 0.00 | R2 | 2 | -0.07 | 300k signal did not hold at 1M |
| cube-triple task4 | 0.00 ± 0.00 | — | 0.00 | R2 | 2 | 0.00 | matched low baseline |
| cube-triple task5 | 0.02 ± 0.01 | — | 0.10 | R2 | 2 | +0.08 | confirmed above VF |

## Visual OGBench Results

The visual results below combine the visual v6/v7 inventory with the Value Flow visual baselines from the paper table. Several v7 matched runs show high early peaks but lower final 1M success, so partial and peak rows are not counted as final.

| task | Value Flow | best 300k | best completed 1M | config | delta | status |
|---|---:|---:|---:|---|---:|---|
| visual-antmaze-medium task1 | 0.77 ± 0.04 | 0.30 | 0.20 | R2 | -0.57 | below VF |
| visual-antmaze-medium task2 | 0.75 ± 0.05 | 0.60 | 0.02 | R2 | -0.73 | below VF |
| visual-antmaze-medium task3 | 0.81 ± 0.07 | 0.20 | 0.32 | R2 | -0.49 | below VF |
| visual-antmaze-medium task4 | 0.71 ± 0.06 | 0.30 | 0.40 | R2 | -0.31 | below VF |
| visual-antmaze-medium task5 | 0.70 ± 0.26 | 0.10 | — | — | — | partial / no completed 1M |
| visual-antmaze-teleport task1 | 0.10 ± 0.04 | 0.10 | 0.10 | A1 | 0.00 | matched VF |
| visual-antmaze-teleport task2 | 0.17 ± 0.05 | 0.00 | 0.20 | R2 | +0.03 | weak positive |
| visual-antmaze-teleport task3 | 0.16 ± 0.03 | 0.30 | 0.00 | A1 | -0.16 | below VF |
| visual-antmaze-teleport task4 | 0.16 ± 0.05 | 0.10 | 0.30 | R2 | +0.14 | positive |
| visual-antmaze-teleport task5 | 0.08 ± 0.02 | 0.10 | 0.00 | R2 | -0.08 | below VF |
| visual-cube-double task1 | 0.35 ± 0.02 | 0.30 | 0.10 | A1 | -0.25 | below VF |
| visual-cube-double task2 | 0.04 ± 0.02 | 0.00 | 0.00 | R2 | -0.04 | below VF |
| visual-cube-double task3 | 0.11 ± 0.02 | 0.00 | 0.10 | R2 | -0.01 | near VF |
| visual-cube-double task4 | 0.02 ± 0.01 | 0.00 | 0.00 | R2 | -0.02 | below VF |
| visual-cube-double task5 | 0.13 ± 0.03 | 0.00 | 0.00 | R2 | -0.13 | below VF |
| visual-scene task1 | 0.99 ± 0.00 | 1.00 | — | — | — | 300k only |
| visual-scene task2 | 0.40 ± 0.27 | 0.00 | — | — | — | no completed 1M |
| visual-scene task3 | 0.66 ± 0.01 | 0.00 | — | — | — | no completed 1M |
| visual-scene task4 | 0.10 ± 0.06 | 0.10 | — | — | — | no completed 1M |
| visual-scene task5 | 0.00 ± 0.00 | 0.00 | — | — | — | no completed 1M |
| visual-puzzle-3x3 task1 | 0.93 ± 0.05 | — | — | — | — | not covered |
| visual-puzzle-3x3 task2 | 0.12 ± 0.01 | — | — | — | — | not covered |
| visual-puzzle-3x3 task3 | 0.03 ± 0.01 | — | — | — | — | not covered |
| visual-puzzle-3x3 task4 | 0.06 ± 0.02 | — | — | — | — | not covered |
| visual-puzzle-3x3 task5 | 0.02 ± 0.00 | — | — | — | — | not covered |

## Current Takeaways

| category | tasks |
|---|---|
| strong state positives | cube-double task2/R3, cube-double task3/A2, cube-double task4/A1, scene task3/A1, cube-triple task5/R2 |
| weak or unstable state positives | puzzle-4x4 task2/MinimalSB, cube-triple task1, scene task1/task2 |
| state failures / unstable | scene task4, puzzle-4x4 task4, puzzle-4x4 task5, cube-triple task3 |
| visual diagnostic signal | visual-antmaze-medium has early high peaks but weak final 1M; visual-teleport task2/task4 show local positives |

## Notes for Plotting

The full raw curves remain in the original `eval.csv` files on the training machines. This snapshot is a lightweight table for the main branch. For plotting, use the corresponding registry files or historical inventory to map each task/config/seed to its `eval.csv` path.
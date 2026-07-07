# Offline-to-online queue status

Updated: 2026-07-03 03:11:10 CST

## Current active job

- Scenario: cube-double
- Method: ours
- Seed: 2
- Stage: screening
- Config: restored500k_r1p0_lam1e-3_tau0p3
- Online budget: 500000
- Latest observed train step: 175000
- Latest observed online step: 150000
- Latest observed success: 0.0
- Summary: not written yet; job is still running
- GPU: 18493 MiB used, about 67% utilization
- Disk: `/` 56% used, `/root/autodl-tmp` 1% used

## Active run directory

/root/autodl-tmp/sb-value-flows-runs/offline2online_single4090/exp/o2o_screen_cube-double_ours_restored500k_r1p0_lam1e-3_tau0p3_seed2/o2o_screen_cube-double_ours_restored500k_r1p0_lam1e-3_tau0p3_seed2/sd002_20260703_020942

## Active log

/root/autodl-tmp/sb-value-flows-runs/offline2online_single4090/logs/o2o_screen_cube-double_ours_restored500k_r1p0_lam1e-3_tau0p3_seed2.log

## Queue process

scripts/continue_offline2online_stageb.sh is still active and waiting for the current main.py job before launching the next Stage B job.

## Queue repair guard

- Stage B script was patched to skip an already completed screening run instead of exiting on an existing run directory.
- One-shot repair monitor is running remotely: `/root/sb-value-flows/scripts/repair_stageb_queue_once.sh`
- Repair monitor log: `/root/autodl-tmp/sb-value-flows-runs/offline2online_single4090/logs/repair_stageb_queue_once.log`
- Purpose: if the old Stage B process exits after the manually launched run completes, restart the patched Stage B queue once.

## Prepared next-stage automation

- Stage C script prepared locally: `/home/lzqw/offline2online_local/scripts/continue_offline2online_stagec.sh`
- Stage C script copied to remote: `/root/sb-value-flows/scripts/continue_offline2online_stagec.sh`
- Stage C status: not started. It is intended for the final 1M curves after Stage B screening/tuning selection.
- Stage C launcher copied to remote: `/root/sb-value-flows/scripts/launch_stagec_after_stageb.sh`
- Stage C launcher log: `/root/autodl-tmp/sb-value-flows-runs/offline2online_single4090/logs/launch_stagec_after_stageb.log`
- Stage C launcher status: running and waiting for Stage B screening completion plus idle GPU.
- Latest launcher heartbeat: 2026-07-03 03:07:05 CST, active `main.py` detected.

## Completion audit

- Local audit: `/home/lzqw/offline2online_local/reports/offline2online/offline2online_completion_audit.md`
- Remote audit: `/root/sb-value-flows/reports/offline2online/offline2online_completion_audit.md`

## Current progress figure

This is a diagnostic progress figure from actual runs collected so far, not the final selected3 figure.

- Remote SVG: `/root/sb-value-flows/reports/figures/offline2online/offline2online_progress_current.svg`
- Remote PDF: `/root/sb-value-flows/reports/figures/offline2online/offline2online_progress_current.pdf`
- Remote PNG: `/root/sb-value-flows/reports/figures/offline2online/offline2online_progress_current.png`
- Local SVG: `/home/lzqw/offline2online_local/reports/figures/offline2online/offline2online_progress_current.svg`
- Local PDF: `/home/lzqw/offline2online_local/reports/figures/offline2online/offline2online_progress_current.pdf`
- Local PNG: `/home/lzqw/offline2online_local/reports/figures/offline2online/offline2online_progress_current.png`

## Goal status

Not complete. The final requirement still needs three scenarios, ours + Value Flows + FQL/IQL, two seeds per plotted curve, final figures, CSV reports, markdown reports, and lightweight commit/push.

# Offline-to-online completion audit

Updated: 2026-07-03 03:11:10 CST

This audit tracks the original goal requirements without narrowing the scope.

| Requirement | Current evidence | Status |
| --- | --- | --- |
| Working offline-to-online implementation for our method | `main.py` supports restore, step-0 eval, online replay, mixed replay ratio, metadata, and summary; `scripts/run_offline2online.py` launches and collects runs. Smoke restored run completed. | Partial but functionally exercised |
| Three selected scenarios have valid curves | Only cube-double has live screening curve data so far. puzzle-4x4 and scene have no online run data yet. | Incomplete |
| Each plotted curve has at least 2 seeds | No final plotted curve is eligible yet. Current live run is cube-double / ours / seed2 only. | Incomplete |
| Ours, Value Flows, and FQL/IQL plotted per scenario | Only Ours has any online data so far; Value Flows and FQL are queued but not yet run. | Incomplete |
| Ours tuned to advantage or strong competitiveness | Stage B screening is still in progress; no cross-method comparison is available yet. | Incomplete |
| Final SVG/PDF/PNG generated | Only diagnostic `offline2online_progress_current.*` exists. Final `offline2online_selected3.*` is not generated because final eligibility is not met. | Incomplete |
| CSV and markdown reports document selected and rejected runs | CSVs and markdown reports exist and now include current run inventory, but final selected/rejected documentation is incomplete until final runs finish. | Partial |
| Lightweight outputs committed and pushed | Not committed or pushed yet; final artifacts do not exist. | Incomplete |

## Current active run

- Scenario: cube-double
- Method: ours
- Seed: 2
- Stage: screening
- Config: restored500k_r1p0_lam1e-3_tau0p3
- Train step: 175000 / 500000
- Latest eval step: 150000
- Latest eval success: 0.0
- Summary: not written yet

## Queue state

- Stage B queue is running and waiting for the current `main.py`.
- Stage B repair guard is running.
- Stage C launcher is running and waiting for Stage B completion; latest heartbeat at 2026-07-03 03:07:05 CST.

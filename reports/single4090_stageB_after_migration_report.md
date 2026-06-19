# Single4090 Stage-B After Migration Report

Generated: 2026-06-19T10:53:30
Host: `autodl-container-5f5c489a58-488668bd`
Server tag: `single4090-new / seetacloud-cqa1-31499`
Date on server: `Fri Jun 19 10:53:30 CST 2026`

## Environment

- Project directory: `/root/sb-value-flows`
- Expected run data directory: `/root/autodl-tmp/sb-value-flows-runs`
- Expected run data directory exists: `False`
- GPU: `NVIDIA vGPU-48GB, 0, 24564, 0, 27`
- Current training process: none detected for `main.py`
- SSH password handling: no password was written to scripts, reports, command files, or git files.

## Source Of Results

- Raw Stage-B eval.csv found on new server: 0
- Lightweight Stage-B registry rows found: 4 from `/root/sb-value-flows/results/single4090_selective_stageB_1m_latest.csv`
- The raw paths recorded in the registry point to `/root/autodl-tmp/sb-value-flows-runs/...`, but that directory is absent on the migrated server.
- Therefore, final values below are the synced registry/latest CSV values, not a fresh raw eval.csv reparse on this machine.
- Final still means the last eval row from the original completed run; best/peak are diagnostic only.

## Summary

- Related Stage-B rows: 4
- Completed rows: 4
- Partial/interrupted rows: 0
- Checkpoints found on new server: 0

## Runs

| run | status | final step | final success | best | peak >=500k | VF | final vs VF | raw eval present | checkpoint | decision |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| puzzle-4x4 task1 / P0_particle / seed 2 | COMPLETED | 1000000 | 0.3 | 0.5 @ 250000 | 0.5 @ 500000 | 0.36 | below | False | False | completed_below_vf_do_not_rerun_do_not_expand_seeds |
| puzzle-4x4 task1 / A2_action_std_lam0p003 / seed 2 | COMPLETED | 1000000 | 0.3 | 0.7 @ 300000 | 0.5 @ 700000 | 0.36 | below | False | False | completed_below_vf_do_not_rerun_do_not_expand_seeds |
| puzzle-4x4 task3 / R2_residual_disagree_lam0p001 / seed 2 | COMPLETED | 1000000 | 0.4 | 0.7 @ 850000 | 0.7 @ 850000 | 0.3 | above | False | False | completed_final_0p4_moderate_positive_no_more_than_A1_control_already_present |
| puzzle-4x4 task3 / A1_action_std_lam0p001 / seed 2 | COMPLETED | 1000000 | 0.0 | 0.5 @ 250000 | 0.3 @ 500000 | 0.3 | below | False | False | completed_control_failed_do_not_expand_ordinary_stageB |

## Decisions

- `puzzle-4x4 task1 / P0` and `puzzle-4x4 task1 / A2` are completed 1M runs with final success `0.30`, below VF `0.36`. Do not rerun them and do not expand seed0/seed1.
- `puzzle-4x4 task3 / R2` is recorded as completed at 1M with final success `0.40`, above VF `0.30` but below the strong-pass threshold `0.45`; the A1 stability control is already present in the synced results.
- `puzzle-4x4 task3 / A1` is recorded as completed at 1M with final success `0.00`; do not continue ordinary Stage-B expansion.
- No raw checkpoint was found on the new server, and no rerun was started.

## Process Snapshot

```text
827    806       10:17 S    /root/miniconda3/bin/python /root/miniconda3/bin/jupyter-lab --allow-root --config=/init/jupyter/jupyter_config.py
   829    806       10:17 Sl   /root/miniconda3/bin/python /root/miniconda3/bin/tensorboard --host 0.0.0.0 --port 6007 --logdir /root/tf-logs
   900    829       10:16 Sl   /root/miniconda3/lib/python3.12/site-packages/tensorboard_data_server/bin/server --logdir=/root/tf-logs --reload=5 --samples-per-plugin= --port=0 --port-file=/tmp/tensorboard_data_server_xcwhggdd/port --die-after-stdin --error-file=/tmp/tensorboard_data_server_xcwhggdd/startup_error
  1840   1829       00:00 Ss   bash -c cd /root/sb-value-flows || exit 1; /root/miniconda3/bin/python /tmp/make_single4090_stageB_after_migration_report.py; echo "===== REPORT ====="; sed -n "1,220p" reports/single4090_stageB_after_migration_report.md
  1841   1840       00:00 S    /root/miniconda3/bin/python /tmp/make_single4090_stageB_after_migration_report.py
```

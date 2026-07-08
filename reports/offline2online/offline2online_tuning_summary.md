# Offline-to-online tuning summary

- documented tuning attempts: 20
- tuning CSV: `/root/sb-value-flows/results/offline2online_tuning_runs.csv`

Tuning attempts are appended to the CSV and retained even when rejected.

| scenario | method | config_name | seed | online_sample_ratio | pm_sb_lambda | tau_post | online_steps | final_success | best_peak_success | decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| scene | ours | tune_r0p5_lam1e-3_tau0p3 | 2 | 0.5 | 1e-3 | 0.3 | 500000 | 0.0 | 0.0 | rejected |
| scene | ours | tune_r0p5_lam1e-3_tau0p3 | 2 | 0.5 | 1e-3 | 0.3 | 500000 | 0.0 | 0.0 | rejected_low_success |
| cube-double | ours | probe_rs_step1_normq_r0p002_lr3e-5_lam1e-3_tau0p3 | 2 | 0.002 | 1e-3 | 0.3 | 1 | 0.1 | 0.4 | rejected_low_success |
| cube-double | ours | probe_rs_step1_normq_r0p002_lr3e-5_lam1e-3_tau0p3 | 3 | 0.002 | 1e-3 | 0.3 | 1 | 0.25 | 0.25 | rejected_low_success |
| cube-double | ours | tune_rs_50k_normq_r0p002_lr3e-5_lam1e-3_tau0p3 | 2 | 0.002 | 1e-3 | 0.3 | 50000 | 0.15 | 0.3 | rejected_low_success |
| cube-double | ours | tune_rs_50k_normq_r0p002_lr3e-5_lam1e-3_tau0p3 | 3 | 0.002 | 1e-3 | 0.3 | 50000 | 0.25 | 0.35 | rejected_low_success |
| puzzle-4x4 | ours | probe_rs_step1_normq_r0p002_lr3e-5_lam1e-3_tau0p3 | 2 | 0.002 | 1e-3 | 0.3 | 1 | 0.65 | 0.65 | accepted_short_screen |
| puzzle-4x4 | ours | probe_rs_step1_normq_r0p002_lr3e-5_lam1e-3_tau0p3 | 3 | 0.002 | 1e-3 | 0.3 | 1 | 0.0 | 0.0 | rejected_low_success |
| puzzle-4x4 | ours | tune_rs_50k_normq_r0p002_lr3e-5_lam1e-3_tau0p3 | 2 | 0.002 | 1e-3 | 0.3 | 50000 | 0.1 | 0.75 | rejected_collapse |
| puzzle-4x4 | ours | tune_rs_50k_normq_r0p002_lr3e-5_lam1e-3_tau0p3 | 3 | 0.002 | 1e-3 | 0.3 | 50000 | 0.2 | 0.2 | rejected_low_success |
| scene | ours | tune_paramsonly_stable_50k_normq_r0p1_lr1e-4_lam1e-3_tau0p3 | 2 | 0.1 | 1e-3 | 0.3 | 50000 | 0.0 | 0.85 | rejected_collapse |
| scene | ours | tune_paramsonly_stable_step1_normq_r0p1_lr1e-4_lam1e-3_tau0p3 | 2 | 0.1 | 1e-3 | 0.3 | 1 | 0.65 | 0.65 | accepted_short_screen |
| scene | ours | tune_rs_50k_normq_r0p002_lr3e-5_lam1e-3_tau0p3 | 2 | 0.002 | 1e-3 | 0.3 | 50000 | 0.8 | 0.95 | accepted_short_screen |
| scene | ours | tune_rs_50k_normq_r0p002_lr3e-5_lam1e-3_tau0p3 | 3 | 0.002 | 1e-3 | 0.3 | 50000 | 0.0 | 0.0 | rejected_low_success |
| scene | ours | tune_rs_50k_normq_r0p01_lr3e-5_lam1e-3_tau0p3 | 2 | 0.01 | 1e-3 | 0.3 | 50000 | 0.2 | 0.85 | rejected_collapse |
| scene | ours | tune_rs_50k_normq_r0p0_lr3e-5_lam1e-3_tau0p3 | 2 | 0.0 | 1e-3 | 0.3 | 50000 | 0.6 | 0.75 | diagnostic_no_online_replay |
| scene | ours | tune_rs_50k_normq_r0p1_lr1e-4_lam1e-3_tau0p3 | 2 | 0.1 | 1e-3 | 0.3 | 50000 | 0.0 | 0.9 | rejected_collapse |
| scene | ours | tune_rs_50k_r0p1_lr1e-4_lam1e-3_tau0p3 | 2 | 0.1 | 1e-3 | 0.3 | 50000 | 0.0 | 0.85 | rejected_collapse |
| scene | ours | tune_rs_50k_r0p5_lam1e-3_tau0p3 | 2 | 0.5 | 1e-3 | 0.3 | 50000 | 0.0 | 0.95 | rejected_collapse |
| scene | ours | tune_rs_step0_r0p5_lam1e-3_tau0p3 | 2 | 0.5 | 1e-3 | 0.3 | 1 | 0.65 | 0.85 | accepted_short_screen |

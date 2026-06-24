# State 25-Task Best-Peak Matrix

Updated: 2026-06-24T16:11:36

This matrix separates best-peak success from completed final success. Best peak is eligible for best-eval reporting; final remains the traditional last-row view.

| domain | task_id | vf_baseline | best_peak_success_any_run | best_peak_config | best_peak_seed | best_peak_minus_vf | best_final_success_any_completed_run | best_final_config | best_final_seed | best_final_minus_vf | coverage_status | recommended_next_action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cube-double-play | task1 | 0.97 | 0.7 | P0_particle | 2 | -0.27 | 0.7 | P0_particle | 2 | -0.27 | has_300k | covered but below VF; lower priority unless domain coverage requires it |
| cube-double-play | task2 | 0.76 | 1.0 | FullSafe | 2 | 0.24 | 1.0 | FullSafe | 2 | 0.24 | has_1m | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| cube-double-play | task3 | 0.73 | 1.0 | A2_action_std_lam0p003 | 0 | 0.27 | 0.9 | A2_action_std_lam0p003 | 2 | 0.17000000000000004 | has_1m | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| cube-double-play | task4 | 0.3 | 0.7 | A1_action_std_lam0p001 | 2 | 0.39999999999999997 | 0.5 | A1_action_std_lam0p001 | 2 | 0.2 | has_1m | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| cube-double-play | task5 | 0.69 | 0.5 | P0_particle | 2 | -0.18999999999999995 | 0.5 | P0_particle | 2 | -0.18999999999999995 | has_300k | covered but below VF; lower priority unless domain coverage requires it |
| cube-triple-play | task1 | 0.59 | 0.9 | ActorGeo | 0 | 0.31000000000000005 | 0.6 | ActorGeo | 0 | 0.010000000000000009 | has_1m | collapse: consider state_stable_v1; keep best peak as best-eval diagnostic |
| cube-triple-play | task2 | 0.0 | 0.0 | A1_action_std_lam0p001 | 2 | 0.0 | 0.0 | A1_action_std_lam0p001 | 2 | 0.0 | has_300k | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| cube-triple-play | task3 | 0.07 | 0.2 | R2_residual_disagree_lam0p001 | 2 | 0.13 | 0.2 | R2_residual_disagree_lam0p001 | 2 | 0.13 | has_300k | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| cube-triple-play | task4 | 0.0 | 0.0 | A1_action_std_lam0p001 | 2 | 0.0 | 0.0 | A1_action_std_lam0p001 | 2 | 0.0 | has_300k | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| cube-triple-play | task5 | 0.02 | 0.0 | A1_action_std_lam0p001 | 2 | -0.02 | 0.0 | A1_action_std_lam0p001 | 2 | -0.02 | has_300k | covered but below VF; lower priority unless domain coverage requires it |
| puzzle-3x3-play | task1 | 0.99 | 1.0 | P0 | 5 | 0.010000000000000009 | 1.0 | P0 | 5 | 0.010000000000000009 | has_1m | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| puzzle-3x3-play | task2 | 0.98 | 1.0 | P0 | 5 | 0.020000000000000018 | 1.0 | P0 | 5 | 0.020000000000000018 | has_1m | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| puzzle-3x3-play | task3 | 0.97 | 0.4 | P0_particle | 2 | -0.57 | 0.2 | P0_particle | 2 | -0.77 | has_1m | covered but below VF; lower priority unless domain coverage requires it |
| puzzle-3x3-play | task4 | 0.84 | 1.0 | ActorGeo | 1 | 0.16000000000000003 | 1.0 | ActorGeo | 1 | 0.16000000000000003 | has_1m | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| puzzle-3x3-play | task5 | 0.58 | 1.0 | P0 | 5 | 0.42000000000000004 | 1.0 | P0 | 5 | 0.42000000000000004 | has_1m | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| puzzle-4x4-play | task1 | 0.36 | 0.7 | A2_action_std_lam0p003 | 2 | 0.33999999999999997 | 0.5 | A2_action_std_lam0p003 | 2 | 0.14 | has_1m | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| puzzle-4x4-play | task2 | 0.27 | 0.6 | MinimalSB_lam0p001 | 0 | 0.32999999999999996 | 0.5 | MinimalSB_lam0p001 | 2 | 0.22999999999999998 | has_1m | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| puzzle-4x4-play | task3 | 0.3 | 0.8 | R2_residual_disagree_lam0p001 | 2 | 0.5 | 0.5 | R2_residual_disagree_lam0p001 | 2 | 0.2 | has_1m | collapse: consider state_stable_v1; keep best peak as best-eval diagnostic |
| puzzle-4x4-play | task4 | 0.28 | 0.6 | FullSafe | 0 | 0.31999999999999995 | 0.5 | R3_residual_disagree_typicality_lam0p001 | 2 | 0.21999999999999997 | has_1m | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| puzzle-4x4-play | task5 | 0.13 | 0.2 | A2_action_std_lam0p003 | 2 | 0.07 | 0.1 | A2_action_std_lam0p003 | 2 | -0.03 | has_1m | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| scene-play | task1 | 0.99 | 1.0 | P0_particle | 2 | 0.010000000000000009 | 1.0 | P0_particle | 2 | 0.010000000000000009 | has_300k | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| scene-play | task2 | 0.97 | 1.0 | FullSafe | 0 | 0.030000000000000027 | 1.0 | FullSafe | 0 | 0.030000000000000027 | has_1m | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| scene-play | task3 | 0.94 | 1.0 | P0_particle | 2 | 0.06000000000000005 | 1.0 | P0_particle | 2 | 0.06000000000000005 | has_300k | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |
| scene-play | task4 | 0.07 | 0.9 | P0_particle | 2 | 0.8300000000000001 | 0.4 | P0_particle | 2 | 0.33 | has_1m | collapse: consider state_stable_v1; keep best peak as best-eval diagnostic |
| scene-play | task5 | 0.0 | 0.0 | P0_particle | 2 | 0.0 | 0.0 | P0_particle | 2 | 0.0 | has_300k | best_peak reaches/exceeds VF; consider best-eval reporting or 1M confirmation |

# Historical Experiment Inventory

Generated: 2026-06-15 11:13:35

This inventory is a read-only scan of historical experiment artifacts. Completed status is assigned only when the eval final step reaches at least 98% of an inferred target step. Peak success is retained for diagnostics and is not used as final success.

## Summary

| item | count |
|---|---|
| eval.csv found | 193 |
| train.csv found | 192 |
| command.txt found | 0 |
| report markdown files found | 20 |
| inventory rows | 213 |
| eval rows in registry | 79 |
| eval rows not in registry | 114 |
| completed eval rows | 188 |
| partial eval rows | 5 |
| failed eval rows | 0 |
| report files without eval | 20 |

## By Storage Root And Experiment Line

| storage_root | experiment_line | eval_count |
|---|---|---|
| /root/sb-value-flows | actor | 9 |
| /root/sb-value-flows | bad_task_repair | 79 |
| /root/sb-value-flows | bestseed | 5 |
| /root/sb-value-flows | fullsafe | 3 |
| /root/sb-value-flows | minimal | 18 |
| /root/sb-value-flows | pm_medium_300k_posterior_big_4090 | 16 |
| /root/sb-value-flows | pm_medium_300k_seed3_4090 | 5 |
| /root/sb-value-flows | pm_medium_component_4090 | 5 |
| /root/sb-value-flows | puzzle | 22 |
| /root/sb-value-flows | reliability | 10 |
| /root/sb-value-flows | table3 | 21 |

## By Experiment Line And Status

| experiment_line | status | eval_count |
|---|---|---|
| actor | COMPLETED | 9 |
| bad_task_repair | COMPLETED | 78 |
| bad_task_repair | PARTIAL | 1 |
| bestseed | COMPLETED | 5 |
| fullsafe | COMPLETED | 3 |
| minimal | COMPLETED | 18 |
| pm_medium_300k_posterior_big_4090 | COMPLETED | 14 |
| pm_medium_300k_posterior_big_4090 | PARTIAL | 2 |
| pm_medium_300k_seed3_4090 | COMPLETED | 4 |
| pm_medium_300k_seed3_4090 | PARTIAL | 1 |
| pm_medium_component_4090 | COMPLETED | 5 |
| puzzle | COMPLETED | 22 |
| reliability | COMPLETED | 10 |
| table3 | COMPLETED | 20 |
| table3 | PARTIAL | 1 |

## New Discoveries Not In Registry

| status | experiment_line | env | config | seed | final_step | success_final | eval_csv |
|---|---|---|---|---|---|---|---|
| COMPLETED | actor | antmaze-medium-navigate-v0 | ActorGeo | 0 | 1000000 | 0.1 | /root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_ActorGeo_seed0/sd000_20260525_100350/eval.csv |
| COMPLETED | actor | antmaze-medium-navigate-v0 | ActorGeo | 1 | 1000000 | 0 | /root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_ActorGeo_seed1/sd001_20260525_180814/eval.csv |
| COMPLETED | actor | antmaze-medium-navigate-v0 | ActorGeo | 2 | 1000000 | 0.1 | /root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_ActorGeo_seed2/sd002_20260526_021340/eval.csv |
| COMPLETED | actor | antmaze-medium-navigate-v0 |  | 3 | 100000 | 0 | /root/sb-value-flows/exp/pm_medium_component_4090/V4_PM_actor_only/sd003_20260524_010754/eval.csv |
| COMPLETED | actor | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.4 | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V1_actor_0p003_seed0/sd000_20260530_141848/eval.csv |
| COMPLETED | actor | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.3 | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V2_actor_0p0_seed0/sd000_20260530_153559/eval.csv |
| COMPLETED | actor | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 1000000 | 0.3 | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V1_actor_0p003_seed0/sd000_20260531_112724/eval.csv |
| COMPLETED | actor | puzzle-4x4-play-singletask-task4-v0 |  | 1 | 1000000 | 0.3 | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V1_actor_0p003_seed1/sd001_20260531_153428/eval.csv |
| COMPLETED | actor | puzzle-4x4-play-singletask-task4-v0 |  | 2 | 1000000 | 0.1 | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V1_actor_0p003_seed2/sd002_20260531_194155/eval.csv |
| COMPLETED | bestseed | puzzle-3x3-play-singletask-task1-v0 |  | 2 | 1000000 | 1 | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task1_S1_sb_lam0p001_seed2/sd002_20260606_142934/eval.csv |
| COMPLETED | bestseed | puzzle-3x3-play-singletask-task2-v0 |  | 2 | 1000000 | 1 | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task2_S1_sb_lam0p001_seed2/sd002_20260606_182634/eval.csv |
| COMPLETED | bestseed | puzzle-3x3-play-singletask-task3-v0 |  | 2 | 1000000 | 0.1 | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task3_S1_sb_lam0p001_seed2/sd002_20260606_222604/eval.csv |
| COMPLETED | bestseed | puzzle-3x3-play-singletask-task4-v0 |  | 2 | 1000000 | 1 | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task4_S1_sb_lam0p001_seed2/sd002_20260607_022834/eval.csv |
| COMPLETED | bestseed | puzzle-3x3-play-singletask-task5-v0 |  | 2 | 1000000 | 1 | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task5_S1_sb_lam0p001_seed2/sd002_20260607_063032/eval.csv |
| COMPLETED | fullsafe | antmaze-medium-navigate-v0 | FullSafe | 0 | 1000000 | 0.2 | /root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_FullSafe_seed0/sd000_20260525_140611/eval.csv |
| COMPLETED | fullsafe | antmaze-medium-navigate-v0 | FullSafe | 1 | 1000000 | 0 | /root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_FullSafe_seed1/sd001_20260525_221133/eval.csv |
| COMPLETED | fullsafe | antmaze-medium-navigate-v0 | FullSafe | 2 | 1000000 | 0.2 | /root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_FullSafe_seed2/sd002_20260526_061530/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 0 | 1000000 | 0.3 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/P0_particle_seed0/sd000_20260602_103605/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 1 | 1000000 | 0.7 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/P0_particle_seed1/sd001_20260602_143822/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 2 | 1000000 | 0.3 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/P0_particle_seed2/sd002_20260602_184301/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 |  | 0 | 1000000 | 0.2 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/S1_sb_lam0p001_seed0/sd000_20260602_224525/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 |  | 1 | 1000000 | 1 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/S1_sb_lam0p001_seed1/sd001_20260603_024723/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 |  | 2 | 1000000 | 1 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/S1_sb_lam0p001_seed2/sd002_20260603_065051/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 3 | 1000000 | 1 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed3/sd003_20260605_061635/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 4 | 1000000 | 0 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed4/sd004_20260605_102001/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 5 | 1000000 | 0 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed5/sd005_20260605_142338/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 6 | 1000000 | 0.1 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed6/sd006_20260605_182702/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 7 | 1000000 | 0.5 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed7/sd007_20260605_223009/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 |  | 3 | 1000000 | 1 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed3/sd003_20260604_100455/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 |  | 4 | 1000000 | 0.2 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed4/sd004_20260604_140603/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 |  | 5 | 1000000 | 1 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed5/sd005_20260604_180842/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 |  | 6 | 1000000 | 0.1 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed6/sd006_20260604_221117/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task4-v0 |  | 7 | 1000000 | 0.2 | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed7/sd007_20260605_021352/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task3-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 0 | /root/sb-value-flows/exp/puzzle3x3_task3_repair_single4090_v1/screen300k_MinimalSB_lam0p0003_seed2/sd002_20260607_121217/eval.csv |
| COMPLETED | minimal | puzzle-3x3-play-singletask-task3-v0 | MinimalSB_lam0p001 | 2 | 300000 | 0 | /root/sb-value-flows/exp/puzzle3x3_task3_repair_single4090_v1/screen300k_MinimalSB_lam0p001_seed2/sd002_20260607_132608/eval.csv |
| PARTIAL | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 4 | 1 | 0 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M0_origin_value_flows_seed4/sd004_20260524_142956/eval.csv |
| PARTIAL | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 4 | 225000 | 0.1 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M0_origin_value_flows_seed4/sd004_20260524_143235/eval.csv |
| COMPLETED | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 5 | 300000 | 0 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M0_origin_value_flows_seed5/sd005_20260524_201228/eval.csv |
| COMPLETED | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 6 | 300000 | 0.1 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M0_origin_value_flows_seed6/sd006_20260525_020108/eval.csv |
| COMPLETED | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 4 | 300000 | 0 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M1_PM_uniform_seed4/sd004_20260524_151011/eval.csv |
| COMPLETED | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 5 | 300000 | 0 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M1_PM_uniform_seed5/sd005_20260524_210002/eval.csv |
| COMPLETED | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 6 | 300000 | 0.1 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M1_PM_uniform_seed6/sd006_20260525_024859/eval.csv |
| COMPLETED | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 4 | 300000 | 0 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M2_PM_posterior_t0p5_seed4/sd004_20260524_162519/eval.csv |
| COMPLETED | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 5 | 300000 | 0 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M2_PM_posterior_t0p5_seed5/sd005_20260524_221522/eval.csv |
| COMPLETED | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 6 | 300000 | 0.1 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M2_PM_posterior_t0p5_seed6/sd006_20260525_040428/eval.csv |
| COMPLETED | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 4 | 300000 | 0 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M3_PM_posterior_t0p3_seed4/sd004_20260524_174144/eval.csv |
| COMPLETED | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 5 | 300000 | 0.1 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M3_PM_posterior_t0p3_seed5/sd005_20260524_233030/eval.csv |
| COMPLETED | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 6 | 300000 | 0.1 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M3_PM_posterior_t0p3_seed6/sd006_20260525_052049/eval.csv |
| COMPLETED | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 4 | 300000 | 0 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M4_PM_posterior_t0p1_seed4/sd004_20260524_185708/eval.csv |
| COMPLETED | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 5 | 300000 | 0.1 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M4_PM_posterior_t0p1_seed5/sd005_20260525_004552/eval.csv |
| COMPLETED | pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 6 | 300000 | 0 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M4_PM_posterior_t0p1_seed6/sd006_20260525_063621/eval.csv |
| COMPLETED | pm_medium_300k_seed3_4090 | antmaze-medium-navigate-v0 |  | 3 | 300000 | 0 | /root/sb-value-flows/exp/pm_medium_300k_seed3_4090/L0_origin_value_flows/sd003_20260524_083551/eval.csv |
| COMPLETED | pm_medium_300k_seed3_4090 | antmaze-medium-navigate-v0 |  | 3 | 300000 | 0 | /root/sb-value-flows/exp/pm_medium_300k_seed3_4090/L1_PM_uniform/sd003_20260524_092336/eval.csv |
| PARTIAL | pm_medium_300k_seed3_4090 | antmaze-medium-navigate-v0 |  | 3 | 175000 | 0 | /root/sb-value-flows/exp/pm_medium_300k_seed3_4090/L2_PM_posterior_only/sd003_20260524_103841/eval.csv |
| COMPLETED | pm_medium_300k_seed3_4090 | antmaze-medium-navigate-v0 |  | 3 | 300000 | 0.1 | /root/sb-value-flows/exp/pm_medium_300k_seed3_4090/L2_PM_posterior_only/sd003_20260524_112939/eval.csv |
| COMPLETED | pm_medium_300k_seed3_4090 | antmaze-medium-navigate-v0 |  | 3 | 300000 | 0 | /root/sb-value-flows/exp/pm_medium_300k_seed3_4090/L3_PM_full_safe/sd003_20260524_124446/eval.csv |
| COMPLETED | pm_medium_component_4090 | antmaze-medium-navigate-v0 |  | 3 | 100000 | 0 | /root/sb-value-flows/exp/pm_medium_component_4090/V0_origin_value_flows/sd003_20260523_232636/eval.csv |
| COMPLETED | pm_medium_component_4090 | antmaze-medium-navigate-v0 |  | 3 | 100000 | 0.2 | /root/sb-value-flows/exp/pm_medium_component_4090/V1_PM_uniform/sd003_20260523_234500/eval.csv |
| COMPLETED | pm_medium_component_4090 | antmaze-medium-navigate-v0 |  | 3 | 100000 | 0 | /root/sb-value-flows/exp/pm_medium_component_4090/V2_PM_posterior_only/sd003_20260524_001235/eval.csv |
| COMPLETED | pm_medium_component_4090 | antmaze-medium-navigate-v0 |  | 3 | 100000 | 0.1 | /root/sb-value-flows/exp/pm_medium_component_4090/V5_PM_full_safe/sd003_20260524_013537/eval.csv |
| COMPLETED | pm_medium_component_4090 | antmaze-medium-navigate-v0 |  | 3 | 100000 | 0 | /root/sb-value-flows/exp/pm_medium_component_4090/V6_PM_full_sharp/sd003_20260524_020314/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.6 | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V0_light_default_seed0/sd000_20260530_130211/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.2 | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V3_energy_0p001_seed0/sd000_20260530_165349/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.1 | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V4_no_energy_rel_seed0/sd000_20260530_181043/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0 | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V6_temp_0p5_seed0/sd000_20260530_204055/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.2 | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V7_temp_0p1_seed0/sd000_20260530_215618/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 1000000 | 0.2 | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V0_light_default_seed0/sd000_20260530_231113/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 1 | 1000000 | 0 | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V0_light_default_seed1/sd001_20260531_031709/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 2 | 1000000 | 0.3 | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V0_light_default_seed2/sd002_20260531_072216/eval.csv |
| COMPLETED | puzzle | puzzle-3x3-play-singletask-task3-v0 | P0 | 2 | 300000 | 0 | /root/sb-value-flows/exp/puzzle3x3_task3_repair_single4090_v1/screen300k_P0_seed2/sd002_20260607_105834/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.3 | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W0_current_seed0/sd000_20260531_235504/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.2 | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W1_bcfm1_seed0/sd000_20260601_010946/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.2 | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W2_bcfm2_seed0/sd000_20260601_022446/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0 | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W3_bcfm5_seed0/sd000_20260601_033930/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.4 | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W4_temp50_seed0/sd000_20260601_045418/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.2 | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W5_temp200_seed0/sd000_20260601_060858/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.2 | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W6_qmean_seed0/sd000_20260601_072342/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 1000000 | 0.1 | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W0_current_seed0/sd000_20260601_205753/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 1 | 1000000 | 0 | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W0_current_seed1/sd001_20260602_010332/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 2 | 1000000 | 0.1 | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W0_current_seed2/sd002_20260602_050918/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 1000000 | 0.1 | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W4_temp50_seed0/sd000_20260601_083824/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 1 | 1000000 | 0.1 | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W4_temp50_seed1/sd001_20260601_124531/eval.csv |
| COMPLETED | puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 2 | 1000000 | 0.5 | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W4_temp50_seed2/sd002_20260601_165143/eval.csv |
| COMPLETED | reliability | antmaze-medium-navigate-v0 |  | 3 | 100000 | 0 | /root/sb-value-flows/exp/pm_medium_component_4090/V3_PM_reliability_only/sd003_20260524_004008/eval.csv |
| COMPLETED | reliability | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.3 | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V5_no_reliability_seed0/sd000_20260530_192614/eval.csv |
| COMPLETED | reliability | puzzle-3x3-play-singletask-task4-v0 |  | 0 | 300000 | 0 | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_A0_action_raw_lam0p001_seed0/sd000_20260603_164451/eval.csv |
| COMPLETED | reliability | puzzle-3x3-play-singletask-task4-v0 | A1_action_std_lam0p001 | 0 | 300000 | 0.1 | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_A1_action_std_lam0p001_seed0/sd000_20260603_175838/eval.csv |
| COMPLETED | reliability | puzzle-3x3-play-singletask-task4-v0 | A2_action_std_lam0p003 | 0 | 300000 | 0.1 | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_A2_action_std_lam0p003_seed0/sd000_20260603_191232/eval.csv |
| COMPLETED | reliability | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 0 | 300000 | 0 | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_P0_particle_seed0/sd000_20260603_153103/eval.csv |
| COMPLETED | reliability | puzzle-3x3-play-singletask-task4-v0 |  | 0 | 300000 | 0 | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_R1_flow_residual_std_lam0p001_seed0/sd000_20260603_202634/eval.csv |
| COMPLETED | reliability | puzzle-3x3-play-singletask-task4-v0 |  | 0 | 300000 | 0 | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_R2_flow_residual_disagree_std_lam0p001_seed0/sd000_20260603_214048/eval.csv |
| COMPLETED | reliability | puzzle-3x3-play-singletask-task4-v0 |  | 0 | 300000 | 0 | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_R3_flow_residual_disagree_typicality_std_lam0p001_seed0/sd000_20260603_225503/eval.csv |
| COMPLETED | reliability | puzzle-3x3-play-singletask-task4-v0 |  | 0 | 300000 | 0 | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_R4_flow_residual_disagree_typicality_mean_lam0p001_seed0/sd000_20260604_000934/eval.csv |
| COMPLETED | table3 | cube-triple-play-singletask-task1-v0 | ActorGeo | 0 | 1000000 | 0.6 | /root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/cube-triple-play-singletask-task1-v0_pm_actorgeo_problem_envs_4090/sd000_20260527_194651/eval.csv |
| COMPLETED | table3 | cube-triple-play-singletask-task1-v0 | ActorGeo | 1 | 1000000 | 0.6 | /root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/cube-triple-play-singletask-task1-v0_pm_actorgeo_problem_envs_4090/sd001_20260527_235654/eval.csv |
| COMPLETED | table3 | cube-triple-play-singletask-task1-v0 | ActorGeo | 2 | 1000000 | 0.4 | /root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/cube-triple-play-singletask-task1-v0_pm_actorgeo_problem_envs_4090/sd002_20260528_040416/eval.csv |
| COMPLETED | table3 | puzzle-3x3-play-singletask-task4-v0 | ActorGeo | 0 | 1000000 | 0.7 | /root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/puzzle-3x3-play-singletask-task4-v0_pm_actorgeo_problem_envs_4090/sd000_20260528_081013/eval.csv |
| COMPLETED | table3 | puzzle-3x3-play-singletask-task4-v0 | ActorGeo | 1 | 1000000 | 1 | /root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/puzzle-3x3-play-singletask-task4-v0_pm_actorgeo_problem_envs_4090/sd001_20260528_121505/eval.csv |
| COMPLETED | table3 | puzzle-3x3-play-singletask-task4-v0 | ActorGeo | 2 | 1000000 | 0.2 | /root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/puzzle-3x3-play-singletask-task4-v0_pm_actorgeo_problem_envs_4090/sd002_20260528_161947/eval.csv |
| COMPLETED | table3 | puzzle-4x4-play-singletask-task4-v0 | PM_FullSafe_light | 0 | 1000000 | 0.3 | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/puzzle-4x4-play-singletask-task4-v0_pm_fullsafe_light_remaining_single4090/sd000_20260528_220734/eval.csv |
| PARTIAL | table3 | puzzle-4x4-play-singletask-task4-v0 | PM_FullSafe_light | 1 | 700000 | 0 | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/puzzle-4x4-play-singletask-task4-v0_pm_fullsafe_light_remaining_single4090/sd001_20260529_021519/eval.csv |
| COMPLETED | table3 | puzzle-4x4-play-singletask-task4-v0 | PM_FullSafe_light | 1 | 1000000 | 0 | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/puzzle-4x4-play-singletask-task4-v0_pm_fullsafe_light_remaining_single4090/sd001_20260529_100238/eval.csv |
| COMPLETED | table3 | puzzle-4x4-play-singletask-task4-v0 | PM_FullSafe_light | 2 | 1000000 | 0.2 | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/puzzle-4x4-play-singletask-task4-v0_pm_fullsafe_light_remaining_single4090/sd002_20260529_140824/eval.csv |
| COMPLETED | table3 | scene-play-singletask-task2-v0 | PM_FullSafe_light | 0 | 1000000 | 1 | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/scene-play-singletask-task2-v0_pm_fullsafe_light_remaining_single4090/sd000_20260529_181552/eval.csv |
| COMPLETED | table3 | scene-play-singletask-task2-v0 | PM_FullSafe_light | 1 | 1000000 | 1 | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/scene-play-singletask-task2-v0_pm_fullsafe_light_remaining_single4090/sd001_20260529_221332/eval.csv |
| COMPLETED | table3 | scene-play-singletask-task2-v0 | PM_FullSafe_light | 2 | 1000000 | 1 | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/scene-play-singletask-task2-v0_pm_fullsafe_light_remaining_single4090/sd002_20260530_021208/eval.csv |
| COMPLETED | table3 | cube-double-play-singletask-task2-v0 | FullSafe | 0 | 1000000 | 0.8 | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-double-play-singletask-task2-v0_pm_fullsafe_official_highmem/sd000_20260526_110014/eval.csv |
| COMPLETED | table3 | cube-double-play-singletask-task2-v0 | FullSafe | 1 | 1000000 | 0.9 | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-double-play-singletask-task2-v0_pm_fullsafe_official_highmem/sd001_20260526_150201/eval.csv |
| COMPLETED | table3 | cube-double-play-singletask-task2-v0 | FullSafe | 2 | 1000000 | 1 | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-double-play-singletask-task2-v0_pm_fullsafe_official_highmem/sd002_20260526_190350/eval.csv |
| COMPLETED | table3 | cube-triple-play-singletask-task1-v0 | FullSafe | 0 | 1000000 | 0 | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-triple-play-singletask-task1-v0_pm_fullsafe_official_highmem/sd000_20260526_230623/eval.csv |
| COMPLETED | table3 | cube-triple-play-singletask-task1-v0 | FullSafe | 1 | 1000000 | 0.3 | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-triple-play-singletask-task1-v0_pm_fullsafe_official_highmem/sd001_20260527_031556/eval.csv |
| COMPLETED | table3 | cube-triple-play-singletask-task1-v0 | FullSafe | 2 | 1000000 | 0.5 | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-triple-play-singletask-task1-v0_pm_fullsafe_official_highmem/sd002_20260527_072316/eval.csv |
| COMPLETED | table3 | puzzle-3x3-play-singletask-task4-v0 | FullSafe | 0 | 1000000 | 0.7 | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/puzzle-3x3-play-singletask-task4-v0_pm_fullsafe_official_highmem/sd000_20260527_113023/eval.csv |
| COMPLETED | table3 | puzzle-3x3-play-singletask-task4-v0 | FullSafe | 1 | 1000000 | 0.9 | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/puzzle-3x3-play-singletask-task4-v0_pm_fullsafe_official_highmem/sd001_20260527_153622/eval.csv |

## Partial Eval Rows

| experiment_line | env | config | seed | final_step | target_steps | success_final | eval_csv |
|---|---|---|---|---|---|---|---|
| bad_task_repair | cube-double-play-singletask-task2-v0 | R3_residual_disagree_typicality_lam0p001 | 0 | 900000 | 1000000 | 0.8 | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task2_R3_residual_disagree_typicality_lam0p001_seed0/sd000_20260612_002941/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 4 | 1 | 300000 | 0 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M0_origin_value_flows_seed4/sd004_20260524_142956/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 4 | 225000 | 300000 | 0.1 | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M0_origin_value_flows_seed4/sd004_20260524_143235/eval.csv |
| pm_medium_300k_seed3_4090 | antmaze-medium-navigate-v0 |  | 3 | 175000 | 300000 | 0 | /root/sb-value-flows/exp/pm_medium_300k_seed3_4090/L2_PM_posterior_only/sd003_20260524_103841/eval.csv |
| table3 | puzzle-4x4-play-singletask-task4-v0 | PM_FullSafe_light | 1 | 700000 | 1000000 | 0 | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/puzzle-4x4-play-singletask-task4-v0_pm_fullsafe_light_remaining_single4090/sd001_20260529_021519/eval.csv |

## Completed Eval Rows

| experiment_line | env | config | seed | final_step | success_final | in_registry | eval_csv |
|---|---|---|---|---|---|---|---|
| actor | antmaze-medium-navigate-v0 | ActorGeo | 0 | 1000000 | 0.1 | no | /root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_ActorGeo_seed0/sd000_20260525_100350/eval.csv |
| actor | antmaze-medium-navigate-v0 | ActorGeo | 1 | 1000000 | 0 | no | /root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_ActorGeo_seed1/sd001_20260525_180814/eval.csv |
| actor | antmaze-medium-navigate-v0 | ActorGeo | 2 | 1000000 | 0.1 | no | /root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_ActorGeo_seed2/sd002_20260526_021340/eval.csv |
| actor | antmaze-medium-navigate-v0 |  | 3 | 100000 | 0 | no | /root/sb-value-flows/exp/pm_medium_component_4090/V4_PM_actor_only/sd003_20260524_010754/eval.csv |
| actor | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.4 | no | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V1_actor_0p003_seed0/sd000_20260530_141848/eval.csv |
| actor | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.3 | no | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V2_actor_0p0_seed0/sd000_20260530_153559/eval.csv |
| actor | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 1000000 | 0.3 | no | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V1_actor_0p003_seed0/sd000_20260531_112724/eval.csv |
| actor | puzzle-4x4-play-singletask-task4-v0 |  | 1 | 1000000 | 0.3 | no | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V1_actor_0p003_seed1/sd001_20260531_153428/eval.csv |
| actor | puzzle-4x4-play-singletask-task4-v0 |  | 2 | 1000000 | 0.1 | no | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V1_actor_0p003_seed2/sd002_20260531_194155/eval.csv |
| bad_task_repair | cube-double-play-singletask-task2-v0 | A1_action_std_lam0p001 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task2_A1_action_std_lam0p001_seed2/sd002_20260609_071050/eval.csv |
| bad_task_repair | cube-double-play-singletask-task2-v0 | A2_action_std_lam0p003 | 2 | 300000 | 0.3 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task2_A2_action_std_lam0p003_seed2/sd002_20260609_082343/eval.csv |
| bad_task_repair | cube-double-play-singletask-task2-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 0.3 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task2_MinimalSB_lam0p0003_seed2/sd002_20260609_044414/eval.csv |
| bad_task_repair | cube-double-play-singletask-task2-v0 | MinimalSB_lam0p001 | 2 | 300000 | 0.3 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task2_MinimalSB_lam0p001_seed2/sd002_20260609_055808/eval.csv |
| bad_task_repair | cube-double-play-singletask-task2-v0 | P0_particle | 2 | 300000 | 0.2 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task2_P0_particle_seed2/sd002_20260609_033015/eval.csv |
| bad_task_repair | cube-double-play-singletask-task2-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 0.2 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task2_R2_residual_disagree_lam0p001_seed2/sd002_20260609_093631/eval.csv |
| bad_task_repair | cube-double-play-singletask-task2-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 0.4 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task2_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260609_104958/eval.csv |
| bad_task_repair | cube-double-play-singletask-task3-v0 | A1_action_std_lam0p001 | 2 | 300000 | 0.4 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task3_A1_action_std_lam0p001_seed2/sd002_20260609_154329/eval.csv |
| bad_task_repair | cube-double-play-singletask-task3-v0 | A2_action_std_lam0p003 | 2 | 300000 | 0.5 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task3_A2_action_std_lam0p003_seed2/sd002_20260609_165639/eval.csv |
| bad_task_repair | cube-double-play-singletask-task3-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 0.4 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task3_MinimalSB_lam0p0003_seed2/sd002_20260609_131645/eval.csv |
| bad_task_repair | cube-double-play-singletask-task3-v0 | MinimalSB_lam0p001 | 2 | 300000 | 0.4 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task3_MinimalSB_lam0p001_seed2/sd002_20260609_142949/eval.csv |
| bad_task_repair | cube-double-play-singletask-task3-v0 | P0_particle | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task3_P0_particle_seed2/sd002_20260609_120343/eval.csv |
| bad_task_repair | cube-double-play-singletask-task3-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 0.3 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task3_R2_residual_disagree_lam0p001_seed2/sd002_20260609_181003/eval.csv |
| bad_task_repair | cube-double-play-singletask-task3-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 0.2 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task3_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260609_192330/eval.csv |
| bad_task_repair | cube-double-play-singletask-task4-v0 | A1_action_std_lam0p001 | 2 | 300000 | 0.3 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task4_A1_action_std_lam0p001_seed2/sd002_20260610_001658/eval.csv |
| bad_task_repair | cube-double-play-singletask-task4-v0 | A2_action_std_lam0p003 | 2 | 300000 | 0.2 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task4_A2_action_std_lam0p003_seed2/sd002_20260610_013010/eval.csv |
| bad_task_repair | cube-double-play-singletask-task4-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task4_MinimalSB_lam0p0003_seed2/sd002_20260609_215014/eval.csv |
| bad_task_repair | cube-double-play-singletask-task4-v0 | MinimalSB_lam0p001 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task4_MinimalSB_lam0p001_seed2/sd002_20260609_230316/eval.csv |
| bad_task_repair | cube-double-play-singletask-task4-v0 | P0_particle | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task4_P0_particle_seed2/sd002_20260609_203700/eval.csv |
| bad_task_repair | cube-double-play-singletask-task4-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task4_R2_residual_disagree_lam0p001_seed2/sd002_20260610_024319/eval.csv |
| bad_task_repair | cube-double-play-singletask-task4-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_double_task4_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260610_035647/eval.csv |
| bad_task_repair | cube-triple-play-singletask-task3-v0 | A1_action_std_lam0p001 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_triple_task3_A1_action_std_lam0p001_seed2/sd002_20260611_111742/eval.csv |
| bad_task_repair | cube-triple-play-singletask-task3-v0 | A2_action_std_lam0p003 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_triple_task3_A2_action_std_lam0p003_seed2/sd002_20260611_123319/eval.csv |
| bad_task_repair | cube-triple-play-singletask-task3-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_triple_task3_MinimalSB_lam0p0003_seed2/sd002_20260611_084632/eval.csv |
| bad_task_repair | cube-triple-play-singletask-task3-v0 | MinimalSB_lam0p001 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_triple_task3_MinimalSB_lam0p001_seed2/sd002_20260611_100156/eval.csv |
| bad_task_repair | cube-triple-play-singletask-task3-v0 | P0_particle | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_triple_task3_P0_particle_seed2/sd002_20260611_073057/eval.csv |
| bad_task_repair | cube-triple-play-singletask-task3-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_triple_task3_R2_residual_disagree_lam0p001_seed2/sd002_20260611_134956/eval.csv |
| bad_task_repair | cube-triple-play-singletask-task3-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_cube_triple_task3_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260611_150701/eval.csv |
| bad_task_repair | puzzle-3x3-play-singletask-task3-v0 | A1_action_std_lam0p001 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_A1_action_std_lam0p001_seed2/sd002_20260608_134900/eval.csv |
| bad_task_repair | puzzle-3x3-play-singletask-task3-v0 | A2_action_std_lam0p003 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_A2_action_std_lam0p003_seed2/sd002_20260608_150345/eval.csv |
| bad_task_repair | puzzle-3x3-play-singletask-task3-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_MinimalSB_lam0p0003_seed2/sd002_20260608_112126/eval.csv |
| bad_task_repair | puzzle-3x3-play-singletask-task3-v0 | MinimalSB_lam0p001 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_MinimalSB_lam0p001_seed2/sd002_20260608_123522/eval.csv |
| bad_task_repair | puzzle-3x3-play-singletask-task3-v0 | P0_particle | 2 | 300000 | 0.2 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_P0_particle_seed2/sd002_20260608_100720/eval.csv |
| bad_task_repair | puzzle-3x3-play-singletask-task3-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_R2_residual_disagree_lam0p001_seed2/sd002_20260608_161801/eval.csv |
| bad_task_repair | puzzle-3x3-play-singletask-task3-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_3x3_task3_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260608_173222/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task2-v0 | A1_action_std_lam0p001 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task2_A1_action_std_lam0p001_seed2/sd002_20260610_174334/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task2-v0 | A2_action_std_lam0p003 | 2 | 300000 | 0.2 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task2_A2_action_std_lam0p003_seed2/sd002_20260610_185833/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task2-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task2_MinimalSB_lam0p0003_seed2/sd002_20260610_151334/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task2-v0 | MinimalSB_lam0p001 | 2 | 300000 | 0.2 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task2_MinimalSB_lam0p001_seed2/sd002_20260610_162826/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task2-v0 | P0_particle | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task2_P0_particle_seed2/sd002_20260610_135827/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task2-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task2_R2_residual_disagree_lam0p001_seed2/sd002_20260610_201338/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task2-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task2_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260610_212924/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task4-v0 | A1_action_std_lam0p001 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task4_A1_action_std_lam0p001_seed2/sd002_20260611_022959/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task4-v0 | A2_action_std_lam0p003 | 2 | 300000 | 0.2 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task4_A2_action_std_lam0p003_seed2/sd002_20260611_034451/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task4-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 0.3 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task4_MinimalSB_lam0p0003_seed2/sd002_20260611_000009/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task4-v0 | MinimalSB_lam0p001 | 2 | 300000 | 0.3 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task4_MinimalSB_lam0p001_seed2/sd002_20260611_011518/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task4-v0 | P0_particle | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task4_P0_particle_seed2/sd002_20260610_224514/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task4-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 0.3 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task4_R2_residual_disagree_lam0p001_seed2/sd002_20260611_045940/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task4-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 0.5 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task4_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260611_061504/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task5-v0 | A1_action_std_lam0p001 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task5_A1_action_std_lam0p001_seed2/sd002_20260610_085659/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task5-v0 | A2_action_std_lam0p003 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task5_A2_action_std_lam0p003_seed2/sd002_20260610_101149/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task5-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task5_MinimalSB_lam0p0003_seed2/sd002_20260610_062557/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task5-v0 | MinimalSB_lam0p001 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task5_MinimalSB_lam0p001_seed2/sd002_20260610_074115/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task5-v0 | P0_particle | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task5_P0_particle_seed2/sd002_20260610_051047/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task5-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task5_R2_residual_disagree_lam0p001_seed2/sd002_20260610_112702/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task5-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_puzzle_4x4_task5_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260610_124302/eval.csv |
| bad_task_repair | scene-play-singletask-task4-v0 | A1_action_std_lam0p001 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_scene_task4_A1_action_std_lam0p001_seed2/sd002_20260608_223033/eval.csv |
| bad_task_repair | scene-play-singletask-task4-v0 | A2_action_std_lam0p003 | 2 | 300000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_scene_task4_A2_action_std_lam0p003_seed2/sd002_20260608_234523/eval.csv |
| bad_task_repair | scene-play-singletask-task4-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 0.2 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_scene_task4_MinimalSB_lam0p0003_seed2/sd002_20260608_200119/eval.csv |
| bad_task_repair | scene-play-singletask-task4-v0 | MinimalSB_lam0p001 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_scene_task4_MinimalSB_lam0p001_seed2/sd002_20260608_211603/eval.csv |
| bad_task_repair | scene-play-singletask-task4-v0 | P0_particle | 2 | 300000 | 0.4 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_scene_task4_P0_particle_seed2/sd002_20260608_184656/eval.csv |
| bad_task_repair | scene-play-singletask-task4-v0 | R2_residual_disagree_lam0p001 | 2 | 300000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_scene_task4_R2_residual_disagree_lam0p001_seed2/sd002_20260609_010005/eval.csv |
| bad_task_repair | scene-play-singletask-task4-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 300000 | 0.2 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageA_300k_scene_task4_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260609_021528/eval.csv |
| bad_task_repair | cube-double-play-singletask-task2-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 1000000 | 0.9 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_cube_double_task2_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260611_203011/eval.csv |
| bad_task_repair | cube-double-play-singletask-task3-v0 | A2_action_std_lam0p003 | 2 | 1000000 | 0.9 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_cube_double_task3_A2_action_std_lam0p003_seed2/sd002_20260612_173301/eval.csv |
| bad_task_repair | cube-double-play-singletask-task4-v0 | A1_action_std_lam0p001 | 2 | 1000000 | 0.5 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_cube_double_task4_A1_action_std_lam0p001_seed2/sd002_20260613_053127/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task2-v0 | MinimalSB_lam0p001 | 2 | 1000000 | 0.5 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_puzzle_4x4_task2_MinimalSB_lam0p001_seed2/sd002_20260613_213740/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task4-v0 | R3_residual_disagree_typicality_lam0p001 | 2 | 1000000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_puzzle_4x4_task4_R3_residual_disagree_typicality_lam0p001_seed2/sd002_20260614_095700/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task5-v0 | A2_action_std_lam0p003 | 2 | 1000000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_puzzle_4x4_task5_A2_action_std_lam0p003_seed2/sd002_20260613_173157/eval.csv |
| bad_task_repair | scene-play-singletask-task4-v0 | P0_particle | 2 | 1000000 | 0 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seed2_1m_scene_task4_P0_particle_seed2/sd002_20260611_162414/eval.csv |
| bad_task_repair | cube-double-play-singletask-task2-v0 | R3_residual_disagree_typicality_lam0p001 | 0 | 1000000 | 0.7 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task2_R3_residual_disagree_typicality_lam0p001_seed0/sd000_20260612_093350/eval.csv |
| bad_task_repair | cube-double-play-singletask-task2-v0 | R3_residual_disagree_typicality_lam0p001 | 1 | 1000000 | 0.9 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task2_R3_residual_disagree_typicality_lam0p001_seed1/sd001_20260612_133305/eval.csv |
| bad_task_repair | cube-double-play-singletask-task3-v0 | A2_action_std_lam0p003 | 0 | 1000000 | 0.8 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task3_A2_action_std_lam0p003_seed0/sd000_20260612_213228/eval.csv |
| bad_task_repair | cube-double-play-singletask-task3-v0 | A2_action_std_lam0p003 | 1 | 1000000 | 0.8 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task3_A2_action_std_lam0p003_seed1/sd001_20260613_013227/eval.csv |
| bad_task_repair | cube-double-play-singletask-task4-v0 | A1_action_std_lam0p001 | 0 | 1000000 | 0.4 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task4_A1_action_std_lam0p001_seed0/sd000_20260613_093038/eval.csv |
| bad_task_repair | cube-double-play-singletask-task4-v0 | A1_action_std_lam0p001 | 1 | 1000000 | 0.3 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_cube_double_task4_A1_action_std_lam0p001_seed1/sd001_20260613_133019/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task2-v0 | MinimalSB_lam0p001 | 0 | 1000000 | 0.4 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_puzzle_4x4_task2_MinimalSB_lam0p001_seed0/sd000_20260614_014306/eval.csv |
| bad_task_repair | puzzle-4x4-play-singletask-task2-v0 | MinimalSB_lam0p001 | 1 | 1000000 | 0.1 | yes | /root/sb-value-flows/exp/bad_task_repair_single4090/stageB_seedext_1m_puzzle_4x4_task2_MinimalSB_lam0p001_seed1/sd001_20260614_055017/eval.csv |
| bestseed | puzzle-3x3-play-singletask-task1-v0 |  | 2 | 1000000 | 1 | no | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task1_S1_sb_lam0p001_seed2/sd002_20260606_142934/eval.csv |
| bestseed | puzzle-3x3-play-singletask-task2-v0 |  | 2 | 1000000 | 1 | no | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task2_S1_sb_lam0p001_seed2/sd002_20260606_182634/eval.csv |
| bestseed | puzzle-3x3-play-singletask-task3-v0 |  | 2 | 1000000 | 0.1 | no | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task3_S1_sb_lam0p001_seed2/sd002_20260606_222604/eval.csv |
| bestseed | puzzle-3x3-play-singletask-task4-v0 |  | 2 | 1000000 | 1 | no | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task4_S1_sb_lam0p001_seed2/sd002_20260607_022834/eval.csv |
| bestseed | puzzle-3x3-play-singletask-task5-v0 |  | 2 | 1000000 | 1 | no | /root/sb-value-flows/exp/puzzle3x3_bestseed_5task_single4090_v3/task5_S1_sb_lam0p001_seed2/sd002_20260607_063032/eval.csv |
| fullsafe | antmaze-medium-navigate-v0 | FullSafe | 0 | 1000000 | 0.2 | no | /root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_FullSafe_seed0/sd000_20260525_140611/eval.csv |
| fullsafe | antmaze-medium-navigate-v0 | FullSafe | 1 | 1000000 | 0 | no | /root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_FullSafe_seed1/sd001_20260525_221133/eval.csv |
| fullsafe | antmaze-medium-navigate-v0 | FullSafe | 2 | 1000000 | 0.2 | no | /root/sb-value-flows/exp/pm_medium_1m_methods_4090/M1M_PM_FullSafe_seed2/sd002_20260526_061530/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 0 | 1000000 | 0.3 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/P0_particle_seed0/sd000_20260602_103605/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 1 | 1000000 | 0.7 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/P0_particle_seed1/sd001_20260602_143822/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 2 | 1000000 | 0.3 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/P0_particle_seed2/sd002_20260602_184301/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 |  | 0 | 1000000 | 0.2 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/S1_sb_lam0p001_seed0/sd000_20260602_224525/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 |  | 1 | 1000000 | 1 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/S1_sb_lam0p001_seed1/sd001_20260603_024723/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 |  | 2 | 1000000 | 1 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_1m_single4090/S1_sb_lam0p001_seed2/sd002_20260603_065051/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 3 | 1000000 | 1 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed3/sd003_20260605_061635/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 4 | 1000000 | 0 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed4/sd004_20260605_102001/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 5 | 1000000 | 0 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed5/sd005_20260605_142338/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 6 | 1000000 | 0.1 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed6/sd006_20260605_182702/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 7 | 1000000 | 0.5 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/P0_particle_seed7/sd007_20260605_223009/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 |  | 3 | 1000000 | 1 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed3/sd003_20260604_100455/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 |  | 4 | 1000000 | 0.2 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed4/sd004_20260604_140603/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 |  | 5 | 1000000 | 1 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed5/sd005_20260604_180842/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 |  | 6 | 1000000 | 0.1 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed6/sd006_20260604_221117/eval.csv |
| minimal | puzzle-3x3-play-singletask-task4-v0 |  | 7 | 1000000 | 0.2 | no | /root/sb-value-flows/exp/minimal_sb_puzzle3x3_push_single4090/S1_sb_lam0p001_seed7/sd007_20260605_021352/eval.csv |
| minimal | puzzle-3x3-play-singletask-task3-v0 | MinimalSB_lam0p0003 | 2 | 300000 | 0 | no | /root/sb-value-flows/exp/puzzle3x3_task3_repair_single4090_v1/screen300k_MinimalSB_lam0p0003_seed2/sd002_20260607_121217/eval.csv |
| minimal | puzzle-3x3-play-singletask-task3-v0 | MinimalSB_lam0p001 | 2 | 300000 | 0 | no | /root/sb-value-flows/exp/puzzle3x3_task3_repair_single4090_v1/screen300k_MinimalSB_lam0p001_seed2/sd002_20260607_132608/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 5 | 300000 | 0 | no | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M0_origin_value_flows_seed5/sd005_20260524_201228/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 6 | 300000 | 0.1 | no | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M0_origin_value_flows_seed6/sd006_20260525_020108/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 4 | 300000 | 0 | no | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M1_PM_uniform_seed4/sd004_20260524_151011/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 5 | 300000 | 0 | no | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M1_PM_uniform_seed5/sd005_20260524_210002/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 6 | 300000 | 0.1 | no | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M1_PM_uniform_seed6/sd006_20260525_024859/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 4 | 300000 | 0 | no | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M2_PM_posterior_t0p5_seed4/sd004_20260524_162519/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 5 | 300000 | 0 | no | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M2_PM_posterior_t0p5_seed5/sd005_20260524_221522/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 6 | 300000 | 0.1 | no | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M2_PM_posterior_t0p5_seed6/sd006_20260525_040428/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 4 | 300000 | 0 | no | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M3_PM_posterior_t0p3_seed4/sd004_20260524_174144/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 5 | 300000 | 0.1 | no | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M3_PM_posterior_t0p3_seed5/sd005_20260524_233030/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 6 | 300000 | 0.1 | no | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M3_PM_posterior_t0p3_seed6/sd006_20260525_052049/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 4 | 300000 | 0 | no | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M4_PM_posterior_t0p1_seed4/sd004_20260524_185708/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 5 | 300000 | 0.1 | no | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M4_PM_posterior_t0p1_seed5/sd005_20260525_004552/eval.csv |
| pm_medium_300k_posterior_big_4090 | antmaze-medium-navigate-v0 |  | 6 | 300000 | 0 | no | /root/sb-value-flows/exp/pm_medium_300k_posterior_big_4090/M4_PM_posterior_t0p1_seed6/sd006_20260525_063621/eval.csv |
| pm_medium_300k_seed3_4090 | antmaze-medium-navigate-v0 |  | 3 | 300000 | 0 | no | /root/sb-value-flows/exp/pm_medium_300k_seed3_4090/L0_origin_value_flows/sd003_20260524_083551/eval.csv |
| pm_medium_300k_seed3_4090 | antmaze-medium-navigate-v0 |  | 3 | 300000 | 0 | no | /root/sb-value-flows/exp/pm_medium_300k_seed3_4090/L1_PM_uniform/sd003_20260524_092336/eval.csv |
| pm_medium_300k_seed3_4090 | antmaze-medium-navigate-v0 |  | 3 | 300000 | 0.1 | no | /root/sb-value-flows/exp/pm_medium_300k_seed3_4090/L2_PM_posterior_only/sd003_20260524_112939/eval.csv |
| pm_medium_300k_seed3_4090 | antmaze-medium-navigate-v0 |  | 3 | 300000 | 0 | no | /root/sb-value-flows/exp/pm_medium_300k_seed3_4090/L3_PM_full_safe/sd003_20260524_124446/eval.csv |
| pm_medium_component_4090 | antmaze-medium-navigate-v0 |  | 3 | 100000 | 0 | no | /root/sb-value-flows/exp/pm_medium_component_4090/V0_origin_value_flows/sd003_20260523_232636/eval.csv |
| pm_medium_component_4090 | antmaze-medium-navigate-v0 |  | 3 | 100000 | 0.2 | no | /root/sb-value-flows/exp/pm_medium_component_4090/V1_PM_uniform/sd003_20260523_234500/eval.csv |
| pm_medium_component_4090 | antmaze-medium-navigate-v0 |  | 3 | 100000 | 0 | no | /root/sb-value-flows/exp/pm_medium_component_4090/V2_PM_posterior_only/sd003_20260524_001235/eval.csv |
| pm_medium_component_4090 | antmaze-medium-navigate-v0 |  | 3 | 100000 | 0.1 | no | /root/sb-value-flows/exp/pm_medium_component_4090/V5_PM_full_safe/sd003_20260524_013537/eval.csv |
| pm_medium_component_4090 | antmaze-medium-navigate-v0 |  | 3 | 100000 | 0 | no | /root/sb-value-flows/exp/pm_medium_component_4090/V6_PM_full_sharp/sd003_20260524_020314/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.6 | no | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V0_light_default_seed0/sd000_20260530_130211/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.2 | no | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V3_energy_0p001_seed0/sd000_20260530_165349/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.1 | no | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V4_no_energy_rel_seed0/sd000_20260530_181043/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0 | no | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V6_temp_0p5_seed0/sd000_20260530_204055/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.2 | no | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V7_temp_0p1_seed0/sd000_20260530_215618/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 1000000 | 0.2 | no | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V0_light_default_seed0/sd000_20260530_231113/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 1 | 1000000 | 0 | no | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V0_light_default_seed1/sd001_20260531_031709/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 2 | 1000000 | 0.3 | no | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageB_V0_light_default_seed2/sd002_20260531_072216/eval.csv |
| puzzle | puzzle-3x3-play-singletask-task3-v0 | P0 | 2 | 300000 | 0 | no | /root/sb-value-flows/exp/puzzle3x3_task3_repair_single4090_v1/screen300k_P0_seed2/sd002_20260607_105834/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.3 | no | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W0_current_seed0/sd000_20260531_235504/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.2 | no | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W1_bcfm1_seed0/sd000_20260601_010946/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.2 | no | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W2_bcfm2_seed0/sd000_20260601_022446/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0 | no | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W3_bcfm5_seed0/sd000_20260601_033930/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.4 | no | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W4_temp50_seed0/sd000_20260601_045418/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.2 | no | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W5_temp200_seed0/sd000_20260601_060858/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.2 | no | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageA_W6_qmean_seed0/sd000_20260601_072342/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 1000000 | 0.1 | no | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W0_current_seed0/sd000_20260601_205753/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 1 | 1000000 | 0 | no | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W0_current_seed1/sd001_20260602_010332/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 2 | 1000000 | 0.1 | no | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W0_current_seed2/sd002_20260602_050918/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 1000000 | 0.1 | no | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W4_temp50_seed0/sd000_20260601_083824/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 1 | 1000000 | 0.1 | no | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W4_temp50_seed1/sd001_20260601_124531/eval.csv |
| puzzle | puzzle-4x4-play-singletask-task4-v0 |  | 2 | 1000000 | 0.5 | no | /root/sb-value-flows/exp/puzzle4x4_secondwave_single4090/stageB_W4_temp50_seed2/sd002_20260601_165143/eval.csv |
| reliability | antmaze-medium-navigate-v0 |  | 3 | 100000 | 0 | no | /root/sb-value-flows/exp/pm_medium_component_4090/V3_PM_reliability_only/sd003_20260524_004008/eval.csv |
| reliability | puzzle-4x4-play-singletask-task4-v0 |  | 0 | 300000 | 0.3 | no | /root/sb-value-flows/exp/pm_puzzle4x4_light_tune_single4090_fixflag/stageA_V5_no_reliability_seed0/sd000_20260530_192614/eval.csv |
| reliability | puzzle-3x3-play-singletask-task4-v0 |  | 0 | 300000 | 0 | no | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_A0_action_raw_lam0p001_seed0/sd000_20260603_164451/eval.csv |
| reliability | puzzle-3x3-play-singletask-task4-v0 | A1_action_std_lam0p001 | 0 | 300000 | 0.1 | no | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_A1_action_std_lam0p001_seed0/sd000_20260603_175838/eval.csv |
| reliability | puzzle-3x3-play-singletask-task4-v0 | A2_action_std_lam0p003 | 0 | 300000 | 0.1 | no | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_A2_action_std_lam0p003_seed0/sd000_20260603_191232/eval.csv |
| reliability | puzzle-3x3-play-singletask-task4-v0 | P0_particle | 0 | 300000 | 0 | no | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_P0_particle_seed0/sd000_20260603_153103/eval.csv |
| reliability | puzzle-3x3-play-singletask-task4-v0 |  | 0 | 300000 | 0 | no | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_R1_flow_residual_std_lam0p001_seed0/sd000_20260603_202634/eval.csv |
| reliability | puzzle-3x3-play-singletask-task4-v0 |  | 0 | 300000 | 0 | no | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_R2_flow_residual_disagree_std_lam0p001_seed0/sd000_20260603_214048/eval.csv |
| reliability | puzzle-3x3-play-singletask-task4-v0 |  | 0 | 300000 | 0 | no | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_R3_flow_residual_disagree_typicality_std_lam0p001_seed0/sd000_20260603_225503/eval.csv |
| reliability | puzzle-3x3-play-singletask-task4-v0 |  | 0 | 300000 | 0 | no | /root/sb-value-flows/exp/reliability_sb_puzzle3x3_overnight_single4090/phaseA_R4_flow_residual_disagree_typicality_mean_lam0p001_seed0/sd000_20260604_000934/eval.csv |
| table3 | cube-triple-play-singletask-task1-v0 | ActorGeo | 0 | 1000000 | 0.6 | no | /root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/cube-triple-play-singletask-task1-v0_pm_actorgeo_problem_envs_4090/sd000_20260527_194651/eval.csv |
| table3 | cube-triple-play-singletask-task1-v0 | ActorGeo | 1 | 1000000 | 0.6 | no | /root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/cube-triple-play-singletask-task1-v0_pm_actorgeo_problem_envs_4090/sd001_20260527_235654/eval.csv |
| table3 | cube-triple-play-singletask-task1-v0 | ActorGeo | 2 | 1000000 | 0.4 | no | /root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/cube-triple-play-singletask-task1-v0_pm_actorgeo_problem_envs_4090/sd002_20260528_040416/eval.csv |
| table3 | puzzle-3x3-play-singletask-task4-v0 | ActorGeo | 0 | 1000000 | 0.7 | no | /root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/puzzle-3x3-play-singletask-task4-v0_pm_actorgeo_problem_envs_4090/sd000_20260528_081013/eval.csv |
| table3 | puzzle-3x3-play-singletask-task4-v0 | ActorGeo | 1 | 1000000 | 1 | no | /root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/puzzle-3x3-play-singletask-task4-v0_pm_actorgeo_problem_envs_4090/sd001_20260528_121505/eval.csv |
| table3 | puzzle-3x3-play-singletask-task4-v0 | ActorGeo | 2 | 1000000 | 0.2 | no | /root/sb-value-flows/exp/table3_pm_actorgeo_problem_envs_4090/puzzle-3x3-play-singletask-task4-v0_pm_actorgeo_problem_envs_4090/sd002_20260528_161947/eval.csv |
| table3 | puzzle-4x4-play-singletask-task4-v0 | PM_FullSafe_light | 0 | 1000000 | 0.3 | no | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/puzzle-4x4-play-singletask-task4-v0_pm_fullsafe_light_remaining_single4090/sd000_20260528_220734/eval.csv |
| table3 | puzzle-4x4-play-singletask-task4-v0 | PM_FullSafe_light | 1 | 1000000 | 0 | no | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/puzzle-4x4-play-singletask-task4-v0_pm_fullsafe_light_remaining_single4090/sd001_20260529_100238/eval.csv |
| table3 | puzzle-4x4-play-singletask-task4-v0 | PM_FullSafe_light | 2 | 1000000 | 0.2 | no | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/puzzle-4x4-play-singletask-task4-v0_pm_fullsafe_light_remaining_single4090/sd002_20260529_140824/eval.csv |
| table3 | scene-play-singletask-task2-v0 | PM_FullSafe_light | 0 | 1000000 | 1 | no | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/scene-play-singletask-task2-v0_pm_fullsafe_light_remaining_single4090/sd000_20260529_181552/eval.csv |
| table3 | scene-play-singletask-task2-v0 | PM_FullSafe_light | 1 | 1000000 | 1 | no | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/scene-play-singletask-task2-v0_pm_fullsafe_light_remaining_single4090/sd001_20260529_221332/eval.csv |
| table3 | scene-play-singletask-task2-v0 | PM_FullSafe_light | 2 | 1000000 | 1 | no | /root/sb-value-flows/exp/table3_pm_fullsafe_light_remaining_single4090/scene-play-singletask-task2-v0_pm_fullsafe_light_remaining_single4090/sd002_20260530_021208/eval.csv |
| table3 | cube-double-play-singletask-task2-v0 | FullSafe | 0 | 1000000 | 0.8 | no | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-double-play-singletask-task2-v0_pm_fullsafe_official_highmem/sd000_20260526_110014/eval.csv |
| table3 | cube-double-play-singletask-task2-v0 | FullSafe | 1 | 1000000 | 0.9 | no | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-double-play-singletask-task2-v0_pm_fullsafe_official_highmem/sd001_20260526_150201/eval.csv |
| table3 | cube-double-play-singletask-task2-v0 | FullSafe | 2 | 1000000 | 1 | no | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-double-play-singletask-task2-v0_pm_fullsafe_official_highmem/sd002_20260526_190350/eval.csv |
| table3 | cube-triple-play-singletask-task1-v0 | FullSafe | 0 | 1000000 | 0 | no | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-triple-play-singletask-task1-v0_pm_fullsafe_official_highmem/sd000_20260526_230623/eval.csv |
| table3 | cube-triple-play-singletask-task1-v0 | FullSafe | 1 | 1000000 | 0.3 | no | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-triple-play-singletask-task1-v0_pm_fullsafe_official_highmem/sd001_20260527_031556/eval.csv |
| table3 | cube-triple-play-singletask-task1-v0 | FullSafe | 2 | 1000000 | 0.5 | no | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/cube-triple-play-singletask-task1-v0_pm_fullsafe_official_highmem/sd002_20260527_072316/eval.csv |
| table3 | puzzle-3x3-play-singletask-task4-v0 | FullSafe | 0 | 1000000 | 0.7 | no | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/puzzle-3x3-play-singletask-task4-v0_pm_fullsafe_official_highmem/sd000_20260527_113023/eval.csv |
| table3 | puzzle-3x3-play-singletask-task4-v0 | FullSafe | 1 | 1000000 | 0.9 | no | /root/sb-value-flows/exp/table3_pm_fullsafe_official_4090_highmem_ldfix/puzzle-3x3-play-singletask-task4-v0_pm_fullsafe_official_highmem/sd001_20260527_153622/eval.csv |

## Report Files Without Nearby Eval

| experiment_line | report | mtime |
|---|---|---|
| bad_task_repair | /root/sb-value-flows/reports/bad_task_repair_single4090_report.md | 2026-06-14 14:05:07 |
| bestseed | /root/sb-value-flows/reports/puzzle3x3_bestseed_5task_single4090_v3_report.md | 2026-06-07 10:31:50 |
| minimal | /root/sb-value-flows/reports/minimal_sb_puzzle3x3_1m_single4090_report.md | 2026-06-03 10:52:42 |
| minimal | /root/sb-value-flows/reports/minimal_sb_puzzle3x3_push_single4090_report.md | 2026-06-06 02:32:26 |
| puzzle | /root/sb-value-flows/reports/pm_puzzle4x4_light_tune_single4090_fixflag_report.md | 2026-05-31 23:46:54 |
| puzzle | /root/sb-value-flows/reports/pm_puzzle4x4_light_tune_single4090_report.md | 2026-05-30 06:15:34 |
| puzzle | /root/sb-value-flows/reports/postrun_single4090_after_puzzle4x4_tune_report.md | 2026-06-02 09:14:04 |
| puzzle | /root/sb-value-flows/reports/puzzle3x3_task3_repair_single4090_v1_report.md | 2026-06-07 14:40:08 |
| puzzle | /root/sb-value-flows/reports/puzzle4x4_second_wave_single4090_final_report.md | 2026-06-02 09:55:04 |
| puzzle | /root/sb-value-flows/reports/puzzle4x4_secondwave_single4090_report.md | 2026-06-02 09:14:04 |
| reliability | /root/sb-value-flows/reports/reliability_sb_puzzle3x3_overnight_single4090_report.md | 2026-06-04 01:25:01 |
| table3 | /root/sb-value-flows/reports/table3_pm_actorgeo_problem_envs_4090_report.md | 2026-05-28 20:24:36 |
| table3 | /root/sb-value-flows/reports/table3_pm_fullsafe_light_cubedouble_single4090_report.md | 2026-05-30 06:14:32 |
| table3 | /root/sb-value-flows/reports/table3_pm_fullsafe_light_remaining_single4090_report.md | 2026-05-30 06:12:30 |
| table3 | /root/sb-value-flows/reports/table3_pm_fullsafe_light_remaining_single4090_report.pre_resume_20260529_100232.md | 2026-05-29 10:02:32 |
| table3 | /root/sb-value-flows/reports/table3_pm_fullsafe_official_4090_highmem_ldfix_report.md | 2026-05-27 15:36:17 |
| unclassified | /root/sb-value-flows/reports/pm_medium_1m_methods_4090_report.md | 2026-05-26 10:21:45 |
| unclassified | /root/sb-value-flows/reports/pm_medium_300k_posterior_big_4090_report.md | 2026-05-25 07:51:24 |
| unclassified | /root/sb-value-flows/reports/pm_medium_300k_seed3_4090_report.md | 2026-05-24 14:01:10 |
| unclassified | /root/sb-value-flows/reports/pm_medium_component_4090_report.md | 2026-05-24 02:30:49 |

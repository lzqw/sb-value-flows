#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="${ENV_NAME:-antmaze-large-navigate-v0}"
OFFLINE_STEPS="${OFFLINE_STEPS:-1000}"
ONLINE_STEPS="${ONLINE_STEPS:-0}"
LOG_INTERVAL="${LOG_INTERVAL:-500}"
EVAL_INTERVAL="${EVAL_INTERVAL:-1000}"
EVAL_EPISODES="${EVAL_EPISODES:-5}"
SEEDS="${SEEDS:-0}"
PYTHON_BIN="${PYTHON_BIN:-conda run -n value-flows python}"

LOG_DIR="logs/pm_short_ablation"
SAVE_ROOT="exp/pm_short_ablation"
mkdir -p "${LOG_DIR}" reports "${SAVE_ROOT}"

STATUS_FILE="${LOG_DIR}/status.txt"
: > "${STATUS_FILE}"

run_one() {
    local run_name="$1"
    local seed="$2"
    shift 2
    local log_file="${LOG_DIR}/${run_name}_seed${seed}.log"

    echo "RUN ${run_name} seed=${seed}" | tee -a "${STATUS_FILE}"
    set +e
    ${PYTHON_BIN} main.py \
        --env_name="${ENV_NAME}" \
        --seed="${seed}" \
        --save_dir="${SAVE_ROOT}" \
        --wandb_run_group="${run_name}" \
        --enable_wandb=0 \
        --offline_steps="${OFFLINE_STEPS}" \
        --online_steps="${ONLINE_STEPS}" \
        --log_interval="${LOG_INTERVAL}" \
        --eval_interval="${EVAL_INTERVAL}" \
        --eval_episodes="${EVAL_EPISODES}" \
        --save_interval=999999999 \
        "$@" > "${log_file}" 2>&1
    local exit_code=$?
    set -e

    if [[ "${exit_code}" -eq 0 ]]; then
        echo "SUCCESS ${run_name} seed=${seed} exit_code=${exit_code} log=${log_file}" | tee -a "${STATUS_FILE}"
    else
        echo "FAILED ${run_name} seed=${seed} exit_code=${exit_code} log=${log_file}" | tee -a "${STATUS_FILE}"
    fi
}

for seed in ${SEEDS}; do
    run_one "E_value_flows_baseline" "${seed}" \
        --agent=agents/value_flows.py

    run_one "A_uniform_pm" "${seed}" \
        --agent=agents/pm_value_flows.py \
        --agent.pm_weight_type=uniform \
        --agent.pm_num_continuations=4 \
        --agent.pm_kernel_bandwidth=1.0 \
        --agent.pm_lambda_num=0.0 \
        --agent.pm_lambda_energy=0.0 \
        --agent.pm_lambda_ess=0.0 \
        --agent.pm_actor_energy_coef=0.0 \
        --agent.pm_actor_disagree_coef=0.0

    run_one "B_kernel_pm" "${seed}" \
        --agent=agents/pm_value_flows.py \
        --agent.pm_weight_type=kernel \
        --agent.pm_num_continuations=4 \
        --agent.pm_kernel_bandwidth=1.0 \
        --agent.pm_lambda_num=0.0 \
        --agent.pm_lambda_energy=0.0 \
        --agent.pm_lambda_ess=0.0 \
        --agent.pm_actor_energy_coef=0.0 \
        --agent.pm_actor_disagree_coef=0.0

    run_one "C_kernel_reliability_pm" "${seed}" \
        --agent=agents/pm_value_flows.py \
        --agent.pm_weight_type=kernel \
        --agent.pm_num_continuations=4 \
        --agent.pm_kernel_bandwidth=1.0 \
        --agent.pm_lambda_num=0.1 \
        --agent.pm_lambda_energy=0.1 \
        --agent.pm_lambda_ess=0.1 \
        --agent.pm_actor_energy_coef=0.0 \
        --agent.pm_actor_disagree_coef=0.0

    run_one "D_full_pm" "${seed}" \
        --agent=agents/pm_value_flows.py \
        --agent.pm_weight_type=kernel \
        --agent.pm_num_continuations=4 \
        --agent.pm_kernel_bandwidth=1.0 \
        --agent.pm_lambda_num=0.1 \
        --agent.pm_lambda_energy=0.1 \
        --agent.pm_lambda_ess=0.1 \
        --agent.pm_actor_energy_coef=0.1 \
        --agent.pm_actor_disagree_coef=0.1
done

echo "Status written to ${STATUS_FILE}"

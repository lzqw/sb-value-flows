#!/usr/bin/env python3
"""Run puzzle-3x3 5-task Minimal SB best-seed sweep on a single 4090."""

from __future__ import annotations

import csv
import json
import math
import os
import shlex
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any


EXP = "puzzle3x3_bestseed_5task_single4090_v3"
REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "run_puzzle3x3_bestseed_5task_single4090_v3.py"
SAVE_ROOT = REPO_ROOT / "exp" / EXP
LOG_ROOT = REPO_ROOT / "logs" / EXP
REPORT_PATH = REPO_ROOT / "reports" / f"{EXP}_report.md"
TRACKING_PATH = REPO_ROOT / "reports" / "valueflows_task_level_tracking.md"
STATUS_PATH = LOG_ROOT / "status.txt"
DATA_ROOT = Path("/root/.ogbench/data")
MANIFEST_PATH = DATA_ROOT / "manifest_after_hardlink_single4090.json"
MUJOCO_BIN = "/root/.mujoco/mujoco210/bin"
CONDA_BIN = "/root/miniconda3/bin/conda"

EXPECTED_BRANCH = "minimal-sb-reweight"
EXPECTED_HEAD = "f241a28599877a54ecf5213b571c66d10a8c6552"
RESULT_BRANCH = "results/puzzle3x3-5task-single4090-v3"

METHOD = "Minimal SB S1"
CONFIG = "S1_sb_lam0p001"
SB_LAMBDA = "0.001"
SEED = 2
OFFLINE_STEPS = 1_000_000

AGENT_FLAG = "--agent=agents/pm_value_flows.py"
OFFICIAL_FLAGS = ["--agent.bcfm_lambda=0.5", "--agent.ret_agg=min"]
COMMON_FLAGS = [
    "--agent.pm_minimal_sb=true",
    "--agent.pm_weight_type=field_kernel_norm",
    "--agent.pm_num_continuations=4",
    "--agent.pm_field_kernel_norm_temp=0.3",
    "--agent.pm_field_kernel_min_scale=1e-6",
    "--agent.pm_action_normalize=none",
    "--agent.pm_actor_energy_coef=0.0",
    "--agent.pm_actor_disagree_coef=0.0",
    "--agent.pm_log_sb_diagnostics=true",
]

TASKS = [
    (1, "puzzle-3x3-play-singletask-task1-v0"),
    (2, "puzzle-3x3-play-singletask-task2-v0"),
    (3, "puzzle-3x3-play-singletask-task3-v0"),
    (4, "puzzle-3x3-play-singletask-task4-v0"),
    (5, "puzzle-3x3-play-singletask-task5-v0"),
]

PAPER_BASELINE = {
    1: (99.0, 0.0),
    2: (98.0, 2.0),
    3: (97.0, 1.0),
    4: (84.0, 24.0),
    5: (58.0, 39.0),
}
PAPER_DOMAIN = (87.0, 13.0)

SUCCESS_KEYS = ["evaluation/success", "eval/success", "success"]
RETURN_KEYS = [
    "evaluation/return",
    "eval/return",
    "return",
    "evaluation/episode.return",
    "eval/episode.return",
    "episode.return",
]
LENGTH_KEYS = [
    "evaluation/length",
    "eval/length",
    "length",
    "evaluation/episode.length",
    "eval/episode.length",
    "episode.length",
]
DIAG_KEYS = [
    "pm/proj_delta_mean",
    "pm/cov_y_action",
    "pm/corr_y_action",
    "pm/action_mean",
    "pm/action_std",
    "pm/weight_max",
    "pm/ess",
]


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def rel(path: Path | str | None) -> str:
    if not path:
        return ""
    p = Path(path)
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def status(line: str) -> None:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    with STATUS_PATH.open("a", encoding="utf-8") as f:
        f.write(f"[{now()}] {line}\n")


def run_text(cmd: list[str], timeout: int = 120, env: dict[str, str] | None = None) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout
    except Exception as exc:  # noqa: BLE001
        return 999, f"ERROR {' '.join(cmd)}: {exc}"


def shell_join(cmd: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in cmd)


def to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def fmt(value: Any, digits: int = 6) -> str:
    val = to_float(value)
    if val is None:
        return ""
    if math.isnan(val):
        return "nan"
    if math.isinf(val):
        return "inf" if val > 0 else "-inf"
    return f"{val:.{digits}g}"


def fmt_pct(value: Any) -> str:
    val = to_float(value)
    return "" if val is None else f"{val:.2f}"


def mean(values: list[float]) -> float | None:
    vals = [v for v in values if not math.isnan(v) and not math.isinf(v)]
    return sum(vals) / len(vals) if vals else None


def std(values: list[float]) -> float | None:
    vals = [v for v in values if not math.isnan(v) and not math.isinf(v)]
    if not vals:
        return None
    if len(vals) == 1:
        return 0.0
    m = sum(vals) / len(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))


def success_to_pct(value: Any) -> float | None:
    val = to_float(value)
    if val is None:
        return None
    return val * 100.0 if abs(val) <= 1.000001 else val


def read_csv_rows(path: Path | None) -> list[dict[str, str]]:
    if path is None or not path.exists():
        return []
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        return list(csv.DictReader(f))


def select_csv(run_dir: Path | None, patterns: list[str]) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    if run_dir is None or not run_dir.exists():
        return None, []
    paths: list[Path] = []
    seen: set[Path] = set()
    for pattern in patterns:
        for path in run_dir.rglob(pattern):
            if path.is_file() and path not in seen:
                paths.append(path)
                seen.add(path)
    candidates: list[dict[str, Any]] = []
    for path in paths:
        rows = read_csv_rows(path)
        candidates.append(
            {
                "path": path,
                "rows": len(rows),
                "mtime": path.stat().st_mtime,
                "mtime_str": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "data": rows,
            }
        )
    if not candidates:
        return None, []
    selected = max(candidates, key=lambda item: (item["rows"], item["mtime"]))
    return selected, candidates


def value_from(row: dict[str, str], keys: list[str]) -> str:
    for key in keys:
        value = row.get(key)
        if value not in (None, ""):
            return value
    return ""


def last_nonempty(rows: list[dict[str, str]], keys: list[str]) -> str:
    for row in reversed(rows):
        value = value_from(row, keys)
        if value != "":
            return value
    return ""


def diag_value(train_rows: list[dict[str, str]], name: str) -> str:
    suffix = name.split("/", 1)[1]
    keys = [
        f"training/critic/pm/{suffix}",
        f"training/pm/{suffix}",
        f"training/critic/{name}",
        name,
    ]
    return last_nonempty(train_rows, keys)


def make_env() -> dict[str, str]:
    env = os.environ.copy()
    old_ld = env.get("LD_LIBRARY_PATH", "")
    env.update(
        {
            "CUDA_VISIBLE_DEVICES": "0",
            "LD_LIBRARY_PATH": f"{MUJOCO_BIN}:{old_ld}" if old_ld else MUJOCO_BIN,
            "MUJOCO_GL": "egl",
            "PYOPENGL_PLATFORM": "egl",
            "SDL_VIDEODRIVER": "dummy",
            "OGBENCH_DATA_DIR": str(DATA_ROOT),
            "XLA_PYTHON_CLIENT_PREALLOCATE": "true",
            "XLA_PYTHON_CLIENT_MEM_FRACTION": "0.90",
            "HOME": "/root",
            "XDG_CACHE_HOME": "/root/.cache",
            "PATH": "/root/miniconda3/bin:" + env.get("PATH", ""),
        }
    )
    return env


def assert_agent_order(flags: list[str]) -> None:
    try:
        agent_idx = flags.index(AGENT_FLAG)
    except ValueError as exc:
        raise RuntimeError(f"missing {AGENT_FLAG}") from exc
    bad = [(idx, flag) for idx, flag in enumerate(flags) if flag.startswith("--agent.") and idx < agent_idx]
    if bad:
        raise RuntimeError(f"{AGENT_FLAG} must appear before all --agent.* flags; bad={bad}")


def group_name(task_id: int) -> str:
    return f"task{task_id}_{CONFIG}_seed{SEED}"


def build_flags(task_id: int, env_name: str) -> list[str]:
    flags = [
        f"--env_name={env_name}",
        f"--seed={SEED}",
        f"--save_dir={SAVE_ROOT}",
        f"--wandb_run_group={group_name(task_id)}",
        "--enable_wandb=0",
        f"--offline_steps={OFFLINE_STEPS}",
        "--online_steps=0",
        "--eval_interval=50000",
        "--eval_episodes=10",
        "--log_interval=25000",
        "--save_interval=999999999",
        AGENT_FLAG,
        *OFFICIAL_FLAGS,
        *COMMON_FLAGS,
        f"--agent.pm_sb_lambda={SB_LAMBDA}",
    ]
    assert_agent_order(flags)
    return flags


def newest_run_dir(task_id: int, start_time: float | None = None) -> Path | None:
    root = SAVE_ROOT / group_name(task_id)
    if not root.exists():
        return None
    dirs = [p for p in root.iterdir() if p.is_dir() and p.name.startswith(f"sd{SEED:03d}_")]
    if start_time is not None:
        recent = [p for p in dirs if p.stat().st_mtime >= start_time - 2]
        if recent:
            dirs = recent
    return max(dirs, key=lambda p: p.stat().st_mtime) if dirs else None


def summarize_run(
    task_id: int,
    env_name: str,
    run_dir: Path | None,
    log_path: Path,
    returncode: int,
    duration: float,
    command: list[str],
) -> dict[str, Any]:
    selected_eval, eval_candidates = select_csv(run_dir, ["*.eval.csv", "eval.csv"])
    selected_train, train_candidates = select_csv(run_dir, ["train.csv"])
    eval_rows = selected_eval["data"] if selected_eval else []
    train_rows = selected_train["data"] if selected_train else []
    final_eval = eval_rows[-1] if eval_rows else {}

    success = value_from(final_eval, SUCCESS_KEYS)
    ret = value_from(final_eval, RETURN_KEYS)
    length = value_from(final_eval, LENGTH_KEYS)

    if final_eval and returncode == 0:
        run_status = "COMPLETE"
    elif final_eval and returncode != 0:
        run_status = "COMPLETE_WITH_WARNING"
    elif returncode == 0:
        run_status = "CSV_MISSING"
    else:
        run_status = "FAILED"

    result: dict[str, Any] = {
        "task": task_id,
        "env": env_name,
        "method": METHOD,
        "config": CONFIG,
        "seed": SEED,
        "lambda": SB_LAMBDA,
        "status": run_status,
        "returncode": returncode,
        "duration_sec": duration,
        "run_dir": rel(run_dir),
        "log_path": rel(log_path),
        "command": shell_join(command),
        "selected_eval_csv": rel(selected_eval["path"]) if selected_eval else "",
        "selected_eval_rows": selected_eval["rows"] if selected_eval else 0,
        "selected_train_csv": rel(selected_train["path"]) if selected_train else "",
        "selected_train_rows": selected_train["rows"] if selected_train else 0,
        "eval_candidates": [
            {"path": rel(item["path"]), "rows": item["rows"], "mtime": item["mtime_str"]}
            for item in sorted(eval_candidates, key=lambda x: str(x["path"]))
        ],
        "train_candidates": [
            {"path": rel(item["path"]), "rows": item["rows"], "mtime": item["mtime_str"]}
            for item in sorted(train_candidates, key=lambda x: str(x["path"]))
        ],
        "success": success,
        "success_pct": success_to_pct(success),
        "return": ret,
        "length": length,
    }
    for key in DIAG_KEYS:
        result[key] = diag_value(train_rows, key)
    weight_max = to_float(result.get("pm/weight_max"))
    result["collapse"] = bool(weight_max is not None and weight_max > 0.95)
    base_mean, _ = PAPER_BASELINE[task_id]
    success_pct = result["success_pct"]
    result["gap"] = (success_pct - base_mean) if success_pct is not None else None
    return result


def run_one(task_id: int, env_name: str) -> dict[str, Any]:
    flags = build_flags(task_id, env_name)
    cmd = [CONDA_BIN, "run", "-n", "value-flows", "python", "main.py", *flags]
    log_path = LOG_ROOT / f"task{task_id}_seed{SEED}.log"
    status(f"START task{task_id} env={env_name} method={METHOD} lambda={SB_LAMBDA} seed={SEED}")
    start = time.time()
    with log_path.open("w", encoding="utf-8", errors="replace") as f:
        f.write("COMMAND: " + shell_join(cmd) + "\n")
        f.write("COMMAND_ORDER_RULE: --agent=agents/pm_value_flows.py appears before all --agent.* flags\n")
        f.write("METHOD: Minimal SB S1\n")
        f.write("SB_LAMBDA: 0.001\n")
        f.write("SEED: 2\n")
        f.write("OFFLINE_STEPS: 1000000\n")
        f.write("ENVIRONMENT:\n")
        for key in [
            "LD_LIBRARY_PATH",
            "MUJOCO_GL",
            "PYOPENGL_PLATFORM",
            "SDL_VIDEODRIVER",
            "OGBENCH_DATA_DIR",
            "XLA_PYTHON_CLIENT_PREALLOCATE",
            "XLA_PYTHON_CLIENT_MEM_FRACTION",
        ]:
            f.write(f"  {key}={make_env().get(key, '')}\n")
        f.flush()
        proc = subprocess.run(cmd, cwd=REPO_ROOT, stdout=f, stderr=subprocess.STDOUT, env=make_env())
    duration = time.time() - start
    run_dir = newest_run_dir(task_id, start)
    result = summarize_run(task_id, env_name, run_dir, log_path, proc.returncode, duration, cmd)
    status(
        " ".join(
            [
                result["status"],
                f"task{task_id}",
                f"returncode={proc.returncode}",
                f"success={fmt(result.get('success'))}",
                f"success_pct={fmt_pct(result.get('success_pct'))}",
                f"return={fmt(result.get('return'))}",
                f"length={fmt(result.get('length'))}",
                f"collapse={result.get('collapse')}",
                f"selected_eval_csv={result.get('selected_eval_csv')}",
            ]
        )
    )
    return result


def git_info() -> dict[str, str]:
    branch = run_text(["git", "branch", "--show-current"])[1].strip()
    head = run_text(["git", "rev-parse", "HEAD"])[1].strip()
    status_short = run_text(["git", "status", "--short"])[1].rstrip()
    return {"branch": branch, "head": head, "status": status_short}


def gpu_snapshot() -> str:
    return run_text(["nvidia-smi"], timeout=120)[1].rstrip()


def no_other_jobs() -> tuple[bool, str]:
    code, out = run_text(["ps", "-eo", "pid,ppid,etime,stat,cmd"], timeout=60)
    if code != 0:
        return False, out
    own = os.getpid()
    parent = os.getppid()
    busy: list[str] = []
    for line in out.splitlines()[1:]:
        parts = line.strip().split(None, 4)
        if len(parts) < 5:
            continue
        try:
            pid = int(parts[0])
            ppid = int(parts[1])
        except ValueError:
            continue
        cmd = parts[4]
        if pid in {own, parent} or ppid in {own, parent}:
            continue
        if EXP in cmd:
            continue
        if "main.py" in cmd:
            busy.append(line)
        elif "run_" in cmd and ".py" in cmd:
            busy.append(line)
        elif "runner" in cmd and "tensorboard" not in cmd.lower():
            busy.append(line)
    return not busy, "\n".join(busy)


def gpu_idle() -> tuple[bool, str]:
    code, out = run_text(
        [
            "nvidia-smi",
            "--query-gpu=memory.used,utilization.gpu",
            "--format=csv,noheader,nounits",
        ],
        timeout=60,
    )
    if code != 0:
        return False, out
    first = out.strip().splitlines()[0].split(",")
    if len(first) < 2:
        return False, out
    mem = int(first[0].strip())
    util = int(first[1].strip())
    return mem < 1000 and util < 10, f"memory.used={mem} MiB utilization.gpu={util}%"


def validate_manifest() -> tuple[bool, str]:
    if not MANIFEST_PATH.exists():
        return False, f"manifest missing: {MANIFEST_PATH}"
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("envs"), list):
        entries = data["envs"]
    elif isinstance(data, list):
        entries = data
    else:
        return False, f"unsupported manifest structure: {type(data).__name__}"
    by_env = {item.get("env_id"): item for item in entries if isinstance(item, dict)}
    missing: list[str] = []
    for _, env_name in TASKS:
        item = by_env.get(env_name)
        if not item or item.get("num_files", 0) == 0:
            missing.append(env_name)
    if missing:
        return False, "missing puzzle-3x3 entries: " + ", ".join(missing)
    zero = [item for item in entries if isinstance(item, dict) and item.get("num_files", 0) == 0]
    return True, f"manifest entries={len(entries)} zero_file_entries={len(zero)}"


def preflight() -> bool:
    ok_manifest, manifest_msg = validate_manifest()
    status(f"MANIFEST {manifest_msg}")
    if not ok_manifest:
        return False

    info = git_info()
    status(f"GIT branch={info['branch']} head={info['head']}")
    if info["branch"] != EXPECTED_BRANCH or info["head"] != EXPECTED_HEAD:
        status(f"ABORT wrong git state expected {EXPECTED_BRANCH} {EXPECTED_HEAD}")
        return False

    if SAVE_ROOT.exists() and any(SAVE_ROOT.iterdir()):
        status(f"ABORT output exp dir already has contents: {rel(SAVE_ROOT)}")
        return False
    if REPORT_PATH.exists():
        status(f"ABORT report already exists: {rel(REPORT_PATH)}")
        return False

    jobs_ok, jobs_msg = no_other_jobs()
    status("PROCESS_IDLE " + ("ok" if jobs_ok else jobs_msg))
    if not jobs_ok:
        return False

    gpu_ok, gpu_msg = gpu_idle()
    status("GPU_IDLE " + gpu_msg)
    if not gpu_ok:
        return False
    return True


def aggregate_values(results: list[dict[str, Any]], key: str) -> tuple[float | None, float | None]:
    vals = [to_float(r.get(key)) for r in results if r.get(key) not in (None, "")]
    clean = [v for v in vals if v is not None]
    return mean(clean), std(clean)


def markdown_candidate_list(candidates: list[dict[str, Any]]) -> str:
    if not candidates:
        return "None"
    return "<br>".join(f"{item['path']} (rows={item['rows']}, mtime={item['mtime']})" for item in candidates)


def generate_report(results: list[dict[str, Any]], final_note: str = "") -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    info = git_info()
    succ_mean, succ_std = aggregate_values(results, "success_pct")
    ret_mean, ret_std = aggregate_values(results, "return")
    len_mean, len_std = aggregate_values(results, "length")
    nvidia = gpu_snapshot()
    failed = [r for r in results if r.get("status") not in {"COMPLETE"}]

    lines = [
        "# Puzzle-3x3 Best-Seed 5-Task Minimal SB Single4090 v3",
        "",
        f"Generated: {now()}",
        "",
        "This is an optimistic best-seed single-seed 5-task sweep, not the full 8-seed official protocol.",
        "",
        "## Setup",
        "",
        f"- method: {METHOD}",
        f"- config: {CONFIG}",
        f"- lambda: {SB_LAMBDA}",
        f"- seed: {SEED}",
        f"- offline_steps: {OFFLINE_STEPS}",
        "- online_steps: 0",
        "- eval_interval: 50000",
        "- eval_episodes: 10",
        "- log_interval: 25000",
        "- save_interval: 999999999",
        f"- branch: {info['branch']}",
        f"- HEAD: {info['head']}",
        "- command order: --agent=agents/pm_value_flows.py appears before all --agent.* flags",
        f"- output log dir: {rel(LOG_ROOT)}",
        f"- output exp dir: {rel(SAVE_ROOT)}",
        f"- final report: {rel(REPORT_PATH)}",
    ]
    if final_note:
        lines += [f"- finalization: {final_note}"]

    lines += [
        "",
        "## Per-Task Final Results",
        "",
        "| task | env | status | final success | success % | return | length | paper baseline % | gap % | collapse | selected_eval_csv |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    by_task = {r["task"]: r for r in results}
    for task_id, env_name in TASKS:
        r = by_task.get(task_id)
        base_mean, base_std = PAPER_BASELINE[task_id]
        if r is None:
            lines.append(f"| {task_id} | {env_name} | PENDING |  |  |  |  | {base_mean:.0f} +/- {base_std:.0f} |  |  |  |")
            continue
        lines.append(
            f"| {task_id} | {env_name} | {r['status']} | {fmt(r.get('success'))} | "
            f"{fmt_pct(r.get('success_pct'))} | {fmt(r.get('return'))} | {fmt(r.get('length'))} | "
            f"{base_mean:.0f} +/- {base_std:.0f} | {fmt_pct(r.get('gap'))} | {r.get('collapse')} | {r.get('selected_eval_csv')} |"
        )

    lines += [
        "",
        "## 5-Task Aggregate",
        "",
        "| metric | mean | std | n |",
        "|---|---:|---:|---:|",
        f"| success % | {fmt_pct(succ_mean)} | {fmt_pct(succ_std)} | {len([r for r in results if r.get('success_pct') is not None])} |",
        f"| return | {fmt(ret_mean)} | {fmt(ret_std)} | {len([r for r in results if r.get('return') not in (None, '')])} |",
        f"| length | {fmt(len_mean)} | {fmt(len_std)} | {len([r for r in results if r.get('length') not in (None, '')])} |",
        "",
        "## Paper Value Flows Task-Level Baseline",
        "",
        "| task | baseline success % |",
        "|---:|---:|",
    ]
    for task_id in range(1, 6):
        base_mean, base_std = PAPER_BASELINE[task_id]
        lines.append(f"| {task_id} | {base_mean:.0f} +/- {base_std:.0f} |")
    lines.append(f"| domain | {PAPER_DOMAIN[0]:.0f} +/- {PAPER_DOMAIN[1]:.0f} |")

    lines += [
        "",
        "## Diagnostics",
        "",
        "| task | " + " | ".join(DIAG_KEYS) + " | collapse flag |",
        "|---:|" + "|".join(["---:"] * len(DIAG_KEYS)) + "|---|",
    ]
    for task_id, _ in TASKS:
        r = by_task.get(task_id)
        if r is None:
            lines.append(f"| {task_id} | " + " | ".join([""] * len(DIAG_KEYS)) + " |  |")
            continue
        vals = " | ".join(fmt(r.get(key)) for key in DIAG_KEYS)
        lines.append(f"| {task_id} | {vals} | {r.get('collapse')} |")

    lines += [
        "",
        "## CSV Selection",
        "",
        "| task | selected_eval_csv | all eval.csv candidates | selected_train_csv | train candidates |",
        "|---:|---|---|---|---|",
    ]
    for task_id, _ in TASKS:
        r = by_task.get(task_id)
        if r is None:
            lines.append(f"| {task_id} |  |  |  |  |")
            continue
        lines.append(
            f"| {task_id} | {r.get('selected_eval_csv')} | {markdown_candidate_list(r.get('eval_candidates', []))} | "
            f"{r.get('selected_train_csv')} | {markdown_candidate_list(r.get('train_candidates', []))} |"
        )

    lines += [
        "",
        "## Failed Or Warning Run Summary",
        "",
    ]
    if not failed:
        lines.append("No failed or warning runs.")
    else:
        lines.append("| task | status | returncode | log | selected_eval_csv |")
        lines.append("|---:|---|---:|---|---|")
        for r in failed:
            lines.append(
                f"| {r['task']} | {r['status']} | {r['returncode']} | {r.get('log_path')} | {r.get('selected_eval_csv')} |"
            )

    lines += [
        "",
        "## Run Commands",
        "",
    ]
    for r in results:
        lines += [f"### task{r['task']}", "```text", r["command"], "```"]

    lines += [
        "",
        "## nvidia-smi",
        "```text",
        nvidia,
        "```",
        "",
        "## git status --short",
        "```text",
        info["status"],
        "```",
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_tracking(results: list[dict[str, Any]]) -> None:
    TRACKING_PATH.parent.mkdir(parents=True, exist_ok=True)
    succ_mean, succ_std = aggregate_values(results, "success_pct")
    lines = [
        "# Value Flows task-level tracking table",
        "",
        "This file tracks task-level baselines from the Value Flows paper and current server runs.",
        "",
        "This is an optimistic best-seed single-seed 5-task sweep, not the full 8-seed official protocol.",
        "",
        "## Puzzle-3x3 Minimal SB S1 Seed2 1M",
        "",
        "| task | env | method | lambda | seed | steps | success % | return | length | paper baseline % | gap % | machine | report path | selected_eval_csv | status |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|",
    ]
    by_task = {r["task"]: r for r in results}
    for task_id, env_name in TASKS:
        r = by_task.get(task_id)
        base_mean, base_std = PAPER_BASELINE[task_id]
        if r is None:
            lines.append(
                f"| {task_id} | {env_name} | {METHOD} | {SB_LAMBDA} | {SEED} | {OFFLINE_STEPS} |  |  |  | "
                f"{base_mean:.0f} +/- {base_std:.0f} |  | single4090 | {rel(REPORT_PATH)} |  | PENDING |"
            )
            continue
        lines.append(
            f"| {task_id} | {env_name} | {METHOD} | {SB_LAMBDA} | {SEED} | {OFFLINE_STEPS} | "
            f"{fmt_pct(r.get('success_pct'))} | {fmt(r.get('return'))} | {fmt(r.get('length'))} | "
            f"{base_mean:.0f} +/- {base_std:.0f} | {fmt_pct(r.get('gap'))} | single4090 | "
            f"{rel(REPORT_PATH)} | {r.get('selected_eval_csv')} | {r.get('status')} |"
        )
    lines += [
        "",
        "## Aggregate",
        "",
        "| domain | method | lambda | seed | steps | success mean % | success std % | paper domain % | gap mean % | machine | report path | status |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]
    gap_mean = (succ_mean - PAPER_DOMAIN[0]) if succ_mean is not None else None
    status_value = "COMPLETE" if results and all(r.get("status") == "COMPLETE" for r in results) else "WARNING_OR_INCOMPLETE"
    lines.append(
        f"| puzzle-3x3-play | {METHOD} | {SB_LAMBDA} | {SEED} | {OFFLINE_STEPS} | {fmt_pct(succ_mean)} | "
        f"{fmt_pct(succ_std)} | {PAPER_DOMAIN[0]:.0f} +/- {PAPER_DOMAIN[1]:.0f} | {fmt_pct(gap_mean)} | "
        f"single4090 | {rel(REPORT_PATH)} | {status_value} |"
    )
    TRACKING_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def finalize_git(results: list[dict[str, Any]]) -> str:
    generate_tracking(results)
    generate_report(results)
    allowed = {rel(TRACKING_PATH), rel(REPORT_PATH), rel(SCRIPT_PATH)}
    staged = run_text(["git", "diff", "--cached", "--name-only"])[1].splitlines()
    extra = [path for path in staged if path and path not in allowed]
    if extra:
        msg = "SKIP_COMMIT unrelated staged files: " + ", ".join(extra)
        status(msg)
        return msg

    add_cmd = ["git", "add", rel(TRACKING_PATH), rel(REPORT_PATH), rel(SCRIPT_PATH)]
    code, out = run_text(add_cmd, timeout=120)
    status("GIT_ADD returncode={} output={}".format(code, out.strip().replace("\n", " | ")))
    if code != 0:
        return "GIT_ADD_FAILED"

    commit_cmd = ["git", "commit", "-m", "Update puzzle-3x3 five-task Minimal SB best-seed results"]
    code, out = run_text(commit_cmd, timeout=120)
    status("GIT_COMMIT returncode={} output={}".format(code, out.strip().replace("\n", " | ")))
    if code != 0 and "nothing to commit" not in out.lower():
        return "GIT_COMMIT_FAILED"

    push_cmd = ["git", "push", "origin", f"HEAD:{RESULT_BRANCH}"]
    code, out = run_text(push_cmd, timeout=600)
    status("GIT_PUSH returncode={} output={}".format(code, out.strip().replace("\n", " | ")))
    if code != 0:
        return "GIT_PUSH_FAILED_NO_FORCE_PUSH"
    return "GIT_PUSH_OK"


def main() -> int:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    status("RUNNER_START puzzle-3x3 best-seed 5-task Minimal SB v3")
    results: list[dict[str, Any]] = []

    if not preflight():
        generate_report(results, final_note="PREFLIGHT_ABORT")
        status("RUNNER_ABORT preflight failed")
        return 2

    SAVE_ROOT.mkdir(parents=True, exist_ok=False)
    generate_report(results)
    for task_id, env_name in TASKS:
        result = run_one(task_id, env_name)
        results.append(result)
        generate_tracking(results)
        generate_report(results)

    final_note = finalize_git(results)
    generate_report(results, final_note=final_note)
    status(f"RUNNER_DONE report={rel(REPORT_PATH)} tracking={rel(TRACKING_PATH)} finalization={final_note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

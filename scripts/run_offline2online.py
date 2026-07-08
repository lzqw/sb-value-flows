#!/root/miniconda3/bin/python
"""Offline-to-online experiment runner and collector for single4090.

This script keeps offline-to-online outputs separate from the completed
parameter-ablation artifacts. It can launch one run, collect all runs into CSVs,
and plot Value-Flows-style curves for the selected three state scenarios.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO = Path("/root/sb-value-flows")
OUTPUT_BASE = Path("/root/autodl-tmp/sb-value-flows-runs/offline2online_single4090")
SAVE_ROOT = OUTPUT_BASE / "exp"
LOG_DIR = OUTPUT_BASE / "logs"
CACHE_ROOT = OUTPUT_BASE / "cache"

RESULTS_CSV = REPO / "results/offline2online_runs.csv"
CURVE_CSV = REPO / "results/offline2online_curve_data.csv"
TUNING_CSV = REPO / "results/offline2online_tuning_runs.csv"
REPORT_DIR = REPO / "reports/offline2online"
FIG_DIR = REPO / "reports/figures/offline2online"
SUMMARY_MD = REPORT_DIR / "offline2online_summary.md"
SELECTED_MD = REPORT_DIR / "offline2online_selected_runs.md"
BASELINE_MD = REPORT_DIR / "baseline_availability.md"
CHECKPOINT_SOURCES_CSV = REPO / "results/offline2online_checkpoint_sources.csv"


@dataclass(frozen=True)
class Scenario:
    key: str
    panel: str
    env: str
    flags: tuple[str, ...] = ()


@dataclass(frozen=True)
class Method:
    key: str
    label: str
    agent: str
    flags: tuple[str, ...] = ()
    needs_rpg: bool = False


SCENARIOS = {
    "cube-double": Scenario(
        "cube-double",
        "cube-double task4",
        "cube-double-play-singletask-task4-v0",
        ("--agent.discount=0.995", "--agent.confidence_weight_temp=3"),
    ),
    "puzzle-4x4": Scenario(
        "puzzle-4x4",
        "puzzle-4x4 task3",
        "puzzle-4x4-play-singletask-task3-v0",
        ("--agent.bcfm_lambda=0.5", "--agent.ret_agg=min"),
    ),
    "scene": Scenario(
        "scene",
        "scene task4",
        "scene-play-singletask-task4-v0",
        ("--agent.bcfm_lambda=0.5", "--agent.ret_agg=min"),
    ),
    "cube-double-task2": Scenario(
        "cube-double-task2",
        "cube-double task2",
        "cube-double-play-singletask-task2-v0",
        ("--agent.discount=0.995", "--agent.confidence_weight_temp=3"),
    ),
    "puzzle-4x4-task2": Scenario(
        "puzzle-4x4-task2",
        "puzzle-4x4 task2",
        "puzzle-4x4-play-singletask-task2-v0",
        ("--agent.bcfm_lambda=0.5", "--agent.ret_agg=min"),
    ),
    "cube-triple-task1": Scenario(
        "cube-triple-task1",
        "cube-triple task1",
        "cube-triple-play-singletask-task1-v0",
        ("--agent.discount=0.995", "--agent.confidence_weight_temp=3"),
    ),
}

METHODS = {
    "ours": Method(
        "ours",
        "Ours",
        "agents/pm_value_flows.py",
        (
            "--agent.pm_minimal_sb=true",
            "--agent.pm_num_continuations=4",
            "--agent.pm_field_kernel_min_scale=1e-6",
            "--agent.pm_actor_energy_coef=0.0",
            "--agent.pm_actor_disagree_coef=0.0",
            "--agent.pm_log_sb_diagnostics=true",
            "--agent.pm_sb_reliability_score=flow_residual_disagree_typicality",
            "--agent.pm_sb_reliability_normalize=std",
            "--agent.pm_sb_flow_residual_eps=0.05",
            "--agent.pm_sb_disagree_beta=0.5",
            "--agent.pm_sb_disagree_umax=3.0",
            "--agent.pm_sb_typicality_tau=1.0",
            "--agent.pm_sb_value_preserving=false",
        ),
        True,
    ),
    "value_flows": Method("value_flows", "Value Flows", "agents/value_flows.py", (), True),
    "fql": Method("fql", "FQL", "agents/fql.py"),
    "iql": Method("iql", "IQL", "agents/iql.py"),
}

STAGE_STEPS = {"smoke": 50_000, "screen": 500_000, "final": 1_000_000}
DEFAULT_FINAL_SCENARIOS = ("cube-double", "puzzle-4x4", "scene")
FINAL_METHODS = ("ours", "value_flows", "fql")
FINAL_SEEDS = (2, 3)

CHECKPOINT_FIELDS = ["method", "env", "seed", "restore_path", "restore_epoch", "run_dir", "params_file", "source"]
TUNING_FIELDS = [
    "scenario",
    "env",
    "method",
    "config_name",
    "seed",
    "online_sample_ratio",
    "pm_sb_lambda",
    "tau_post",
    "online_steps",
    "final_success",
    "best_peak_success",
    "best_peak_step",
    "drop",
    "run_dir",
    "decision",
    "notes",
]

FIELDS = [
    "scenario",
    "panel",
    "env",
    "method",
    "method_label",
    "config_name",
    "seed",
    "online_steps",
    "final_step",
    "status",
    "final_success",
    "best_peak_success",
    "best_peak_step",
    "drop",
    "run_dir",
    "eval_csv",
    "train_csv",
    "command_txt",
    "checkpoint_source",
    "used_in_final_figure",
    "run_stage",
    "notes",
]


def ensure_dirs() -> None:
    for path in [SAVE_ROOT, LOG_DIR, CACHE_ROOT, RESULTS_CSV.parent, REPORT_DIR, FIG_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def env_vars() -> dict[str, str]:
    env = os.environ.copy()
    mujoco = "/root/.mujoco/mujoco210/bin"
    old_ld = env.get("LD_LIBRARY_PATH", "")
    env.update(
        {
            "CUDA_VISIBLE_DEVICES": "0",
            "LD_LIBRARY_PATH": f"{mujoco}:{old_ld}" if old_ld else mujoco,
            "MUJOCO_GL": "egl",
            "PYOPENGL_PLATFORM": "egl",
            "SDL_VIDEODRIVER": "dummy",
            "OGBENCH_DATA_DIR": "/root/.ogbench/data",
            "XDG_CACHE_HOME": str(CACHE_ROOT),
            "HOME": "/root",
            "PATH": "/root/miniconda3/bin:" + env.get("PATH", ""),
        }
    )
    return env


def has_active_main() -> bool:
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit():
            continue
        try:
            comm = (proc / "comm").read_text().strip()
            cmd = (proc / "cmdline").read_bytes().replace(b"\x00", b" ").decode(errors="ignore")
        except OSError:
            continue
        if (comm.startswith("python") or comm.startswith("conda") or comm == "main.py") and any(Path(part).name == "main.py" for part in cmd.split()):
            return True
    return False


def load_checkpoint_sources() -> dict[tuple[str, str, int], tuple[str, str]]:
    if not CHECKPOINT_SOURCES_CSV.exists():
        return {}
    out: dict[tuple[str, str, int], tuple[str, str]] = {}
    with CHECKPOINT_SOURCES_CSV.open(newline="") as f:
        for row in csv.DictReader(f):
            try:
                seed = int(row["seed"])
            except Exception:
                continue
            out[(row["method"], row["env"], seed)] = (row["restore_path"], row["restore_epoch"])
    return out


def config_flags(method: Method, scenario: Scenario, args: argparse.Namespace) -> list[str]:
    flags = [f"--agent={method.agent}"]
    flags += list(method.flags)
    for flag in scenario.flags:
        if method.key in {"fql", "iql"} and flag.split("=", 1)[0] not in {"--agent.discount"}:
            continue
        flags.append(flag)
    if method.key == "ours":
        flags += [
            f"--agent.pm_weight_type={args.pm_weight_type}",
            f"--agent.pm_field_kernel_norm_temp={args.tau_post}",
            f"--agent.pm_sb_lambda={args.pm_sb_lambda}",
        ]
    if args.lr is not None:
        flags.append(f"--agent.lr={args.lr}")
    for flag in args.agent_flag:
        prefix = "--agent." if not flag.startswith("--agent.") else ""
        flags.append(f"{prefix}{flag}")
    return flags


def run_name(stage: str, scenario: Scenario, method: Method, seed: int, config_name: str) -> str:
    return f"o2o_{stage}_{scenario.key}_{method.key}_{config_name}_seed{seed}"


def final_scenario_keys(args: argparse.Namespace) -> tuple[str, ...]:
    raw = getattr(args, "final_scenarios", "") or ",".join(DEFAULT_FINAL_SCENARIOS)
    keys = tuple(k.strip() for k in raw.split(",") if k.strip())
    unknown = [k for k in keys if k not in SCENARIOS]
    if unknown:
        raise SystemExit(f"Unknown final scenario(s): {unknown}")
    return keys


def build_command(args: argparse.Namespace, scenario: Scenario, method: Method, seed: int) -> tuple[list[str], Path]:
    config_name = args.config_name
    name = run_name(args.stage, scenario, method, seed, config_name)
    save_dir = SAVE_ROOT / name
    checkpoint_sources = load_checkpoint_sources()
    restore = checkpoint_sources.get((method.key, scenario.env, seed))
    cmd = [
        "/root/miniconda3/bin/conda",
        "run",
        "-n",
        "value-flows",
        "python",
        "main.py",
        f"--env_name={scenario.env}",
        f"--seed={seed}",
        f"--save_dir={save_dir}",
        f"--wandb_run_group={name}",
        "--enable_wandb=0",
        "--offline_steps=0",
        f"--online_steps={args.online_steps}",
        f"--eval_interval={args.eval_interval}",
        f"--eval_episodes={args.eval_episodes}",
        f"--log_interval={args.log_interval}",
        "--save_interval=999999999",
        "--eval_at_step0=true",
        "--balanced_sampling=1",
        f"--online_sample_ratio={args.online_sample_ratio}",
    ]
    if args.policy_extraction:
        cmd.append(f"--policy_extraction={args.policy_extraction}")
    if args.restore_params_only:
        cmd.append("--restore_params_only=true")
    if restore:
        cmd += [f"--restore_path={restore[0]}", f"--restore_epoch={restore[1]}"]
    cmd += config_flags(method, scenario, args)
    return cmd, save_dir


def build_pretrain_command(args: argparse.Namespace, scenario: Scenario, method: Method, seed: int) -> tuple[list[str], Path]:
    config_name = args.config_name
    name = run_name("pretrain", scenario, method, seed, config_name)
    save_dir = SAVE_ROOT / name
    cmd = [
        "/root/miniconda3/bin/conda",
        "run",
        "-n",
        "value-flows",
        "python",
        "main.py",
        f"--env_name={scenario.env}",
        f"--seed={seed}",
        f"--save_dir={save_dir}",
        f"--wandb_run_group={name}",
        "--enable_wandb=0",
        f"--offline_steps={args.offline_steps}",
        "--online_steps=0",
        f"--eval_interval={args.eval_interval}",
        f"--eval_episodes={args.eval_episodes}",
        f"--log_interval={args.log_interval}",
        f"--save_interval={args.save_interval or args.offline_steps}",
    ]
    cmd += config_flags(method, scenario, args)
    return cmd, save_dir


def start_process(cmd: list[str], log_path: Path) -> subprocess.Popen:
    with log_path.open("w") as log:
        return subprocess.Popen(
            cmd,
            cwd=REPO,
            env=env_vars(),
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )


def launch(args: argparse.Namespace) -> None:
    ensure_dirs()
    if has_active_main() and not args.force:
        raise SystemExit("A main.py process is already active; refusing to launch a duplicate job.")
    scenario = SCENARIOS[args.scenario]
    method = METHODS[args.method]
    cmd, save_dir = build_command(args, scenario, method, args.seed)
    existing = find_latest_run_dir(save_dir)
    if existing and (existing / "eval.csv").exists() and not args.force:
        raise SystemExit(f"Existing run found: {existing}")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{save_dir.name}.log"
    if args.dry_run:
        print(shlex.join(cmd))
        print(f"log: {log_path}")
        return
    proc = start_process(cmd, log_path)
    print(f"PID {proc.pid}")
    print(f"LOG {log_path}")
    print(f"RUN_ROOT {save_dir}")


def pretrain(args: argparse.Namespace) -> None:
    ensure_dirs()
    if has_active_main() and not args.force:
        raise SystemExit("A main.py process is already active; refusing to launch a duplicate job.")
    scenario = SCENARIOS[args.scenario]
    method = METHODS[args.method]
    cmd, save_dir = build_pretrain_command(args, scenario, method, args.seed)
    existing = find_latest_run_dir(save_dir)
    if existing and list(existing.glob("params_*.pkl")) and not args.force:
        raise SystemExit(f"Existing checkpoint run found: {existing}")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{save_dir.name}.log"
    if args.dry_run:
        print(shlex.join(cmd))
        print(f"log: {log_path}")
        return
    proc = start_process(cmd, log_path)
    print(f"PID {proc.pid}")
    print(f"LOG {log_path}")
    print(f"RUN_ROOT {save_dir}")


def find_latest_run_dir(save_root: Path) -> Path | None:
    if not save_root.exists():
        return None
    candidates = [p for p in save_root.rglob("eval.csv")]
    if not candidates:
        return None
    return max((p.parent for p in candidates), key=lambda p: p.stat().st_mtime)


def parse_eval(eval_csv: Path) -> tuple[list[dict[str, str]], dict[str, str]]:
    if not eval_csv.exists():
        return [], {}
    with eval_csv.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return rows, {}
    last = rows[-1]
    best = -1.0
    best_step = ""
    for row in rows:
        try:
            val = float(row.get("evaluation/success", "nan"))
        except ValueError:
            continue
        if val > best:
            best = val
            best_step = row.get("step", "")
    try:
        final = float(last.get("evaluation/success", "nan"))
    except ValueError:
        final = float("nan")
    summary = {
        "final_step": last.get("step", ""),
        "final_success": str(final),
        "best_peak_success": str(best),
        "best_peak_step": best_step,
        "drop": str(final - best),
    }
    return rows, summary


def metadata_from_run_dir(run_dir: Path) -> dict[str, str]:
    flags_path = run_dir / "flags.json"
    if not flags_path.exists():
        return {}
    try:
        data = json.loads(flags_path.read_text())
    except Exception:
        return {}
    agent = data.get("agent") if isinstance(data.get("agent"), dict) else {}
    env_name = data.get("env_name", "")
    method = agent.get("agent_name", "")
    return {
        "env": env_name,
        "method_agent": method,
        "seed": str(data.get("seed", "")),
        "offline_steps": str(data.get("offline_steps", "")),
        "online_steps": str(data.get("online_steps", "")),
        "restore_path": str(data.get("restore_path", "") or ""),
        "restore_epoch": str(data.get("restore_epoch", "") or ""),
    }


def method_from_agent(agent_name: str) -> Method | None:
    if agent_name == "pm_value_flows":
        return METHODS["ours"]
    return next((m for m in METHODS.values() if m.key == agent_name), None)


def stage_from_name(name: str) -> str:
    if "o2o_final_" in name:
        return "final"
    if "o2o_screen_" in name:
        return "screening"
    if "o2o_smoke_" in name:
        return "smoke"
    if "o2o_pretrain_" in name:
        return "pretrain"
    return "unknown"


def config_from_name(name: str, stage: str, scenario: Scenario | None, method: Method | None, seed: str) -> str:
    if scenario is None or method is None or not seed or stage == "unknown":
        return "unknown"
    prefix_stage = "screen" if stage == "screening" else stage
    prefix = f"o2o_{prefix_stage}_{scenario.key}_{method.key}_"
    suffix = f"_seed{seed}"
    if name.startswith(prefix) and name.endswith(suffix):
        return name[len(prefix):-len(suffix)]
    return "unknown"


def run_status(stage: str, final_step: int, target_online_steps: int, target_offline_steps: int, run_dir: Path) -> str:
    if stage == "pretrain":
        params = run_dir / f"params_{target_offline_steps}.pkl"
        if target_offline_steps and final_step >= target_offline_steps and params.exists():
            return "completed_pretrain"
        return "partial"
    if target_online_steps >= 1_000_000 and final_step >= target_online_steps:
        return "completed_1m"
    if target_online_steps and final_step >= target_online_steps:
        return "completed"
    return "partial"


def collect(args: argparse.Namespace) -> list[dict[str, str]]:
    ensure_dirs()
    rows: list[dict[str, str]] = []
    final_scenarios = set(final_scenario_keys(args))
    for eval_csv in sorted(SAVE_ROOT.rglob("eval.csv")):
        run_dir = eval_csv.parent
        root = eval_csv.parents[2] if len(eval_csv.parents) > 2 else run_dir
        name = root.name
        meta = metadata_from_run_dir(run_dir)
        scenario = next((s for s in SCENARIOS.values() if s.env == meta.get("env")), None)
        method = next((m for m in METHODS.values() if m.key in name), None) or method_from_agent(
            meta.get("method_agent", "")
        )
        eval_rows, summary = parse_eval(eval_csv)
        final_step = int(float(summary.get("final_step") or 0))
        target_steps = int(float(meta.get("online_steps") or 0))
        target_offline_steps = int(float(meta.get("offline_steps") or 0))
        stage = stage_from_name(name)
        status = run_status(stage, final_step, target_steps, target_offline_steps, run_dir)
        config_name = config_from_name(name, stage, scenario, method, meta.get("seed", ""))
        row = {
            "scenario": scenario.key if scenario else "",
            "panel": scenario.panel if scenario else "",
            "env": meta.get("env", ""),
            "method": method.key if method else meta.get("method_agent", ""),
            "method_label": method.label if method else meta.get("method_agent", ""),
            "config_name": config_name,
            "seed": meta.get("seed", ""),
            "online_steps": meta.get("online_steps", ""),
            "final_step": summary.get("final_step", ""),
            "status": status,
            "final_success": summary.get("final_success", ""),
            "best_peak_success": summary.get("best_peak_success", ""),
            "best_peak_step": summary.get("best_peak_step", ""),
            "drop": summary.get("drop", ""),
            "run_dir": str(run_dir),
            "eval_csv": str(eval_csv),
            "train_csv": str(run_dir / "train.csv"),
            "command_txt": str(run_dir / "command.txt"),
            "checkpoint_source": meta.get("restore_path", ""),
            "used_in_final_figure": "False",
            "run_stage": stage,
            "notes": "",
        }
        rows.append(row)

    final_seed_sets: dict[tuple[str, str], set[str]] = {}
    for row in rows:
        if (
            row["scenario"] in final_scenarios
            and row["method"] in FINAL_METHODS
            and row["seed"] in {str(s) for s in FINAL_SEEDS}
            and row["status"] == "completed_1m"
            and row["run_stage"] == "final"
        ):
            final_seed_sets.setdefault((row["scenario"], row["method"]), set()).add(row["seed"])
    eligible = {key for key, seeds in final_seed_sets.items() if {str(s) for s in FINAL_SEEDS}.issubset(seeds)}
    for row in rows:
        row["used_in_final_figure"] = str(
            (row["scenario"], row["method"]) in eligible
            and row["seed"] in {str(s) for s in FINAL_SEEDS}
            and row["status"] == "completed_1m"
            and row["run_stage"] == "final"
        )

    curve_rows: list[dict[str, str]] = []
    used_by_run_dir = {row["run_dir"]: row["used_in_final_figure"] for row in rows}
    meta_by_run_dir = {row["run_dir"]: row for row in rows}
    for eval_csv in sorted(SAVE_ROOT.rglob("eval.csv")):
        run_dir = str(eval_csv.parent)
        eval_rows, _ = parse_eval(eval_csv)
        row = meta_by_run_dir.get(run_dir)
        if row is None:
            continue
        for erow in eval_rows:
            curve_rows.append(
                {
                    "scenario": row["scenario"],
                    "panel": row["panel"],
                    "env": row["env"],
                    "method": row["method"],
                    "method_label": row["method_label"],
                    "seed": row["seed"],
                    "step": erow.get("step", ""),
                    "success": erow.get("evaluation/success", ""),
                    "run_dir": run_dir,
                    "used_in_final_figure": used_by_run_dir.get(run_dir, "False"),
                }
            )
    write_csv(RESULTS_CSV, FIELDS, rows)
    write_csv(
        CURVE_CSV,
        ["scenario", "panel", "env", "method", "method_label", "seed", "step", "success", "run_dir", "used_in_final_figure"],
        curve_rows,
    )
    write_reports(rows)
    print(f"runs={len(rows)} written={RESULTS_CSV}")
    return rows


def collect_checkpoints(_: argparse.Namespace) -> list[dict[str, str]]:
    ensure_dirs()
    by_key: dict[tuple[str, str, str], dict[str, str]] = {}
    for params_file in sorted(SAVE_ROOT.rglob("params_*.pkl")):
        run_dir = params_file.parent
        meta = metadata_from_run_dir(run_dir)
        if not meta:
            continue
        scenario = next((s for s in SCENARIOS.values() if s.env == meta.get("env")), None)
        method = method_from_agent(meta.get("method_agent", ""))
        if scenario is None or method is None:
            continue
        epoch = params_file.stem.removeprefix("params_")
        key = (method.key, scenario.env, meta.get("seed", ""))
        row = {
            "method": method.key,
            "env": scenario.env,
            "seed": meta.get("seed", ""),
            "restore_path": str(run_dir),
            "restore_epoch": epoch,
            "run_dir": str(run_dir),
            "params_file": str(params_file),
            "source": "offline2online_pretrain",
        }
        previous = by_key.get(key)
        try:
            epoch_value = int(epoch)
            previous_epoch = int(previous["restore_epoch"]) if previous else -1
        except Exception:
            epoch_value = -1
            previous_epoch = -1
        if previous is None or epoch_value > previous_epoch or (
            epoch_value == previous_epoch and params_file.stat().st_mtime > Path(previous["params_file"]).stat().st_mtime
        ):
            by_key[key] = row
    rows = [by_key[k] for k in sorted(by_key)]
    write_csv(CHECKPOINT_SOURCES_CSV, CHECKPOINT_FIELDS, rows)
    print(f"checkpoints={len(rows)} written={CHECKPOINT_SOURCES_CSV}")
    for row in rows:
        print(f"{row['method']:12s} seed{row['seed']} {row['env']} -> {row['params_file']}")
    return rows


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> list[str]:
    if not rows:
        return ["No rows yet.", ""]
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    lines = [header, sep]
    for row in rows:
        vals = [str(row.get(field, "")).replace("|", "\\|") for field in fields]
        lines.append("| " + " | ".join(vals) + " |")
    lines.append("")
    return lines


def write_reports(rows: list[dict[str, str]]) -> None:
    final = [r for r in rows if r.get("used_in_final_figure") == "True"]
    summary_lines = [
        "# Offline-to-online summary",
        "",
        f"- collected runs: {len(rows)}",
        f"- final-figure eligible runs: {len(final)}",
        f"- output base: `{OUTPUT_BASE}`",
        f"- results CSV: `{RESULTS_CSV}`",
        f"- curve CSV: `{CURVE_CSV}`",
        "",
        "This file is regenerated by `scripts/run_offline2online.py --mode collect`.",
        "",
        "## Current run inventory",
        "",
    ]
    inventory_fields = [
        "scenario",
        "method",
        "config_name",
        "seed",
        "run_stage",
        "status",
        "final_step",
        "final_success",
        "best_peak_success",
        "best_peak_step",
        "used_in_final_figure",
    ]
    summary_lines += markdown_table(rows, inventory_fields)
    SUMMARY_MD.write_text("\n".join(summary_lines))

    lines = ["# Offline-to-online selected runs", ""]
    if not final:
        lines += [
            "No final-figure runs are eligible yet. Eligibility requires `run_stage=final`, "
            "`status=completed_1m`, and both seed2/seed3 for each plotted method/scenario.",
            "",
            "## Current non-final runs",
            "",
        ]
        lines += markdown_table([r for r in rows if r.get("run_stage") != "pretrain"], inventory_fields)
    for row in final:
        lines.append(
            f"- {row['scenario']} / {row['method']} / seed{row['seed']}: "
            f"final={row['final_success']} best={row['best_peak_success']}@{row['best_peak_step']} "
            f"drop={row['drop']} run=`{row['run_dir']}`"
        )
    SELECTED_MD.write_text("\n".join(lines) + "\n")
    BASELINE_MD.write_text(
        "\n".join(
            [
                "# Baseline availability",
                "",
                "- Value Flows: available as `agents/value_flows.py`.",
                "- FQL: available as `agents/fql.py`.",
                "- IQL: available as `agents/iql.py`.",
                "- IFQL: available as `agents/ifql.py`, not part of the minimum final set by default.",
                "- RLPD: no runnable local implementation found in this repo audit.",
                "- IQN: available as `agents/iqn.py`, optional.",
                "",
            ]
        )
    )
    if not TUNING_CSV.exists():
        write_csv(TUNING_CSV, TUNING_FIELDS, [])
    tuning_summary = REPORT_DIR / "offline2online_tuning_summary.md"
    tuning_rows = []
    if TUNING_CSV.exists():
        with TUNING_CSV.open(newline="") as f:
            tuning_rows = list(csv.DictReader(f))
    tuning_lines = [
        "# Offline-to-online tuning summary",
        "",
        f"- documented tuning attempts: {len(tuning_rows)}",
        f"- tuning CSV: `{TUNING_CSV}`",
        "",
        "Tuning attempts are appended to the CSV and retained even when rejected.",
        "",
    ]
    if tuning_rows:
        tuning_lines += markdown_table(
            tuning_rows,
            [
                "scenario",
                "method",
                "config_name",
                "seed",
                "online_sample_ratio",
                "pm_sb_lambda",
                "tau_post",
                "online_steps",
                "final_success",
                "best_peak_success",
                "decision",
            ],
        )
    tuning_summary.write_text("\n".join(tuning_lines))


def plot(args: argparse.Namespace) -> None:
    rows = collect(args)
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except Exception as exc:
        raise SystemExit(f"matplotlib/numpy unavailable: {exc}")
    curve_rows: list[dict[str, str]]
    with CURVE_CSV.open(newline="") as f:
        curve_rows = [r for r in csv.DictReader(f) if r.get("used_in_final_figure") == "True"]
    save_curve_figure(plt, np, curve_rows, "offline2online_selected3", final_scenario_keys(args))
    print(FIG_DIR / "offline2online_selected3.png")


def select_progress_runs(rows: list[dict[str, str]], scenario_keys: tuple[str, ...] = DEFAULT_FINAL_SCENARIOS) -> set[str]:
    stage_rank = {"final": 3, "screening": 2, "smoke": 1}
    selected: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        if row["scenario"] not in scenario_keys or row["method"] not in FINAL_METHODS:
            continue
        if row["run_stage"] == "pretrain" or row["status"] not in {"partial", "completed", "completed_1m"}:
            continue
        key = (row["scenario"], row["method"], row["seed"])
        current = selected.get(key)
        rank = (
            stage_rank.get(row["run_stage"], 0),
            int(float(row.get("online_steps") or 0)),
            int(float(row.get("final_step") or 0)),
        )
        current_rank = (
            stage_rank.get(current["run_stage"], 0),
            int(float(current.get("online_steps") or 0)),
            int(float(current.get("final_step") or 0)),
        ) if current else (-1, -1, -1)
        if rank > current_rank:
            selected[key] = row
    return {row["run_dir"] for row in selected.values()}


def plot_progress(args: argparse.Namespace) -> None:
    rows = collect(args)
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except Exception as exc:
        raise SystemExit(f"matplotlib/numpy unavailable: {exc}")
    selected_run_dirs = select_progress_runs(rows, final_scenario_keys(args))
    with CURVE_CSV.open(newline="") as f:
        curve_rows = [r for r in csv.DictReader(f) if r.get("run_dir") in selected_run_dirs]
    save_curve_figure(plt, np, curve_rows, "offline2online_progress_current", final_scenario_keys(args))
    print(FIG_DIR / "offline2online_progress_current.png")


def save_curve_figure(
    plt, np, curve_rows: list[dict[str, str]], stem: str, scenario_keys: tuple[str, ...] = DEFAULT_FINAL_SCENARIOS
) -> None:
    scenarios = [SCENARIOS[k] for k in scenario_keys]
    methods = [METHODS[k] for k in FINAL_METHODS]
    fig, axes = plt.subplots(1, len(scenarios), figsize=(12, 3.4), sharey=True)
    colors = {"ours": "#1f77b4", "value_flows": "#2ca02c", "fql": "#d62728", "iql": "#9467bd"}
    max_step = 1000
    for row in curve_rows:
        try:
            max_step = max(max_step, int(float(row["step"])))
        except Exception:
            continue
    x_max = max_step / 1000.0
    for ax, scenario in zip(axes, scenarios):
        ax.set_title(scenario.panel)
        ax.set_xlabel("Online Steps (x1000)")
        ax.set_xlim(0, x_max)
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.25)
        plotted = False
        for method in methods:
            grouped: dict[int, list[float]] = {}
            for row in curve_rows:
                if row["scenario"] != scenario.key or row["method"] != method.key:
                    continue
                try:
                    step = int(float(row["step"]))
                    success = float(row["success"]) * 100.0
                except Exception:
                    continue
                grouped.setdefault(step, []).append(success)
            if not grouped:
                continue
            steps = np.array(sorted(grouped))
            vals = [np.array(grouped[s], dtype=float) for s in steps]
            means = np.array([v.mean() for v in vals])
            stds = np.array([v.std() for v in vals])
            x = steps / 1000.0
            ax.plot(x, means, label=method.label, color=colors.get(method.key))
            ax.fill_between(x, means - stds, means + stds, color=colors.get(method.key), alpha=0.18)
            plotted = True
        if not plotted:
            ax.text(0.5, 0.5, "no data yet", transform=ax.transAxes, ha="center", va="center", color="#777777")
        if ax is axes[0]:
            ax.set_ylabel("Success Rate")
    handles, labels = [], []
    for ax in axes:
        ax_handles, ax_labels = ax.get_legend_handles_labels()
        for handle, label in zip(ax_handles, ax_labels):
            if label not in labels:
                handles.append(handle)
                labels.append(label)
    if handles:
        fig.legend(handles, labels, frameon=False, loc="lower center", ncol=len(handles), bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout()
    for ext in ["svg", "pdf", "png"]:
        fig.savefig(FIG_DIR / f"{stem}.{ext}", dpi=200)
    plt.close(fig)


def status(args: argparse.Namespace) -> None:
    rows = collect(args)
    stage_rank = {"final": 3, "screening": 2, "smoke": 1}
    for scenario_key in final_scenario_keys(args):
        for method_key in FINAL_METHODS:
            for seed in FINAL_SEEDS:
                found = [
                    r for r in rows
                    if r["scenario"] == scenario_key and r["method"] == method_key and r["seed"] == str(seed)
                    and r["run_stage"] != "pretrain"
                ]
                found.sort(
                    key=lambda r: (
                        stage_rank.get(r["run_stage"], 0),
                        int(float(r.get("online_steps") or 0)),
                        int(float(r.get("final_step") or 0)),
                    )
                )
                state = f"{found[-1]['run_stage']}:{found[-1]['status']}" if found else "missing"
                print(f"{scenario_key:12s} {method_key:12s} seed{seed}: {state}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["launch", "pretrain", "checkpoints", "collect", "plot", "plot_progress", "status"], default="status")
    parser.add_argument("--stage", choices=["smoke", "screen", "final"], default="smoke")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="cube-double")
    parser.add_argument("--method", choices=sorted(METHODS), default="ours")
    parser.add_argument("--seed", type=int, default=2)
    parser.add_argument("--online_steps", type=int, default=None)
    parser.add_argument("--offline_steps", type=int, default=300_000)
    parser.add_argument("--save_interval", type=int, default=None)
    parser.add_argument("--eval_interval", type=int, default=50_000)
    parser.add_argument("--eval_episodes", type=int, default=10)
    parser.add_argument("--log_interval", type=int, default=25_000)
    parser.add_argument("--online_sample_ratio", type=float, default=1.0)
    parser.add_argument("--pm_sb_lambda", type=float, default=1e-3)
    parser.add_argument("--tau_post", type=float, default=0.3)
    parser.add_argument("--pm_weight_type", default="field_kernel_norm")
    parser.add_argument("--lr", type=float, default=None)
    parser.add_argument("--agent_flag", action="append", default=[], help="Additional key=value flag passed as --agent.key=value.")
    parser.add_argument("--policy_extraction", choices=["rs", "rpg"], default=None)
    parser.add_argument("--restore_params_only", action="store_true")
    parser.add_argument("--config_name", default="default")
    parser.add_argument("--final_scenarios", default=",".join(DEFAULT_FINAL_SCENARIOS))
    parser.add_argument("--dry_run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.online_steps is None:
        args.online_steps = STAGE_STEPS[args.stage]
    return args


def main() -> None:
    args = parse_args()
    ensure_dirs()
    if args.mode == "launch":
        launch(args)
    elif args.mode == "pretrain":
        pretrain(args)
    elif args.mode == "checkpoints":
        collect_checkpoints(args)
    elif args.mode == "collect":
        collect(args)
    elif args.mode == "plot":
        plot(args)
    elif args.mode == "plot_progress":
        plot_progress(args)
    elif args.mode == "status":
        status(args)


if __name__ == "__main__":
    main()

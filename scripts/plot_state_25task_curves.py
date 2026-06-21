#!/usr/bin/env python3
"""Plot selected state 25-task curves from audit plot data.

Reads results/plot_data_state_curves.csv, which is generated from raw eval.csv
files by scripts/audit_all_state_experiments_single4090.py.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


REPO = Path("/root/sb-value-flows")
PLOT_DATA = REPO / "results/plot_data_state_curves.csv"
OUT = REPO / "reports/figures/state_25task_curves"

GROUPS = {
    "cube_double_positive": [
        "cube-double-play-singletask-task2-v0",
        "cube-double-play-singletask-task3-v0",
        "cube-double-play-singletask-task4-v0",
    ],
    "puzzle4x4_collapse": [
        "puzzle-4x4-play-singletask-task1-v0",
        "puzzle-4x4-play-singletask-task3-v0",
        "puzzle-4x4-play-singletask-task4-v0",
    ],
    "scene_task4": ["scene-play-singletask-task4-v0"],
    "cube_triple_task3": ["cube-triple-play-singletask-task3-v0"],
}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def fnum(value: str) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


def run_label(env: str, config: str, seed: str) -> str:
    task = env.replace("-play-singletask-", " ").replace("-v0", "")
    return f"{task} {config} s{seed}"


def select_runs(rows: list[dict[str, str]], envs: list[str]) -> list[tuple[tuple[str, str, str, str], list[dict[str, str]]]]:
    by_run: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row.get("env") not in envs:
            continue
        key = (row.get("env", ""), row.get("config", ""), row.get("seed", ""), row.get("eval_csv", ""))
        by_run[key].append(row)
    scored = []
    for key, points in by_run.items():
        points.sort(key=lambda row: fnum(row.get("step", "")) or -1)
        successes = [fnum(row.get("success", "")) for row in points if fnum(row.get("success", "")) is not None]
        steps = [fnum(row.get("step", "")) for row in points if fnum(row.get("step", "")) is not None]
        if not successes:
            continue
        peak = max(successes)
        final = successes[-1]
        final_step = max(steps) if steps else 0
        scored.append((key[0], peak, final, final_step, key, points))
    selected = []
    for env in envs:
        candidates = [item for item in scored if item[0] == env]
        candidates.sort(key=lambda item: (item[1], item[2], item[3]), reverse=True)
        selected.extend((item[4], item[5]) for item in candidates[:3])
    return selected


def plot_group(name: str, envs: list[str]) -> bool:
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        (OUT / f"{name}.missing_matplotlib.txt").write_text(str(exc), encoding="utf-8")
        return False
    rows = read_csv(PLOT_DATA)
    runs = select_runs(rows, envs)
    if not runs:
        (OUT / f"{name}.no_curves.txt").write_text("No matching audit plot data found.\n", encoding="utf-8")
        return False
    fig, ax = plt.subplots(figsize=(9.4, 5.4))
    for key, points in runs:
        env, config, seed, _ = key
        xy = []
        for row in points:
            step = fnum(row.get("step", ""))
            success = fnum(row.get("success", ""))
            if step is not None and success is not None:
                xy.append((step / 1000.0, success))
        if not xy:
            continue
        xs = [x for x, _ in xy]
        ys = [y for _, y in xy]
        best_idx = max(range(len(ys)), key=lambda idx: ys[idx])
        vf = fnum(points[0].get("vf_baseline", ""))
        drop = ys[-1] - ys[best_idx]
        label = f"{run_label(env, config, seed)} final={ys[-1]:.2f} peak={ys[best_idx]:.2f} drop={drop:.2f}"
        ax.plot(xs, ys, marker="o", linewidth=1.5, markersize=3.5, label=label)
        ax.scatter([xs[best_idx]], [ys[best_idx]], marker="*", s=54, zorder=4)
        ax.scatter([xs[-1]], [ys[-1]], marker="s", s=34, zorder=4)
        if vf is not None:
            ax.axhline(vf, linestyle="--", linewidth=0.9, alpha=0.22)
    ax.set_title(name.replace("_", " "))
    ax.set_xlabel("Step (k)")
    ax.set_ylabel("Success")
    ax.set_ylim(-0.03, 1.03)
    ax.grid(True, alpha=0.22)
    ax.legend(fontsize=6.8)
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.png", dpi=180)
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)
    return True


def main() -> int:
    results = [(name, plot_group(name, envs)) for name, envs in GROUPS.items()]
    summary = "\n".join(f"{name}: {'ok' if ok else 'missing'}" for name, ok in results) + "\n"
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "plot_summary.txt").write_text(summary, encoding="utf-8")
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

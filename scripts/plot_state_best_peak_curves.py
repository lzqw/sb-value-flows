#!/usr/bin/env python3
"""Plot state best-peak/final success curves from audit plot data."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


REPO = Path("/root/sb-value-flows")
PLOT_DATA = REPO / "results/plot_data_state_curves.csv"
OUT = REPO / "reports/figures/state_curves"

GROUPS = {
    "cube_double_task2_task3_task4": [
        "cube-double-play-singletask-task2-v0",
        "cube-double-play-singletask-task3-v0",
        "cube-double-play-singletask-task4-v0",
    ],
    "puzzle4x4_all_tasks": [
        "puzzle-4x4-play-singletask-task1-v0",
        "puzzle-4x4-play-singletask-task2-v0",
        "puzzle-4x4-play-singletask-task3-v0",
        "puzzle-4x4-play-singletask-task4-v0",
        "puzzle-4x4-play-singletask-task5-v0",
    ],
    "puzzle3x3_task5": ["puzzle-3x3-play-singletask-task5-v0"],
    "cube_triple_task3": ["cube-triple-play-singletask-task3-v0"],
    "scene_task4": ["scene-play-singletask-task4-v0"],
}


def fnum(value: str):
    try:
        return float(value)
    except Exception:
        return None


def read_rows():
    if not PLOT_DATA.exists():
        return []
    with PLOT_DATA.open(newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def select_representative_runs(rows, envs):
    by_run = defaultdict(list)
    for row in rows:
        if row["env"] not in envs:
            continue
        key = (row["env"], row["config"], row["seed"], row["eval_csv"])
        by_run[key].append(row)
    scored = []
    for key, points in by_run.items():
        peak = max((fnum(p["success"]) for p in points if fnum(p["success"]) is not None), default=-1)
        final = fnum(points[-1]["success"])
        final = -1 if final is None else final
        steps = max((fnum(p["step"]) for p in points if fnum(p["step"]) is not None), default=0)
        scored.append((key[0], peak, final, steps, key, points))
    # Keep top two curves per env by peak then final.
    selected = []
    for env in envs:
        env_scored = [x for x in scored if x[0] == env]
        env_scored.sort(key=lambda x: (x[1], x[2], x[3]), reverse=True)
        selected.extend(env_scored[:2])
    return selected


def plot_group(name, envs):
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        (OUT / f"{name}.missing_matplotlib.txt").write_text(str(exc), encoding="utf-8")
        return False
    rows = read_rows()
    runs = select_representative_runs(rows, envs)
    if not runs:
        (OUT / f"{name}.no_data.txt").write_text("No curve data found.\n", encoding="utf-8")
        return False
    fig, ax = plt.subplots(figsize=(9.0, 5.2))
    for env, peak, final, _, key, points in runs:
        config = key[1]
        seed = key[2]
        xs = [fnum(p["step"]) / 1000 for p in points if fnum(p["step"]) is not None and fnum(p["success"]) is not None]
        ys = [fnum(p["success"]) for p in points if fnum(p["step"]) is not None and fnum(p["success"]) is not None]
        if not xs:
            continue
        vf = fnum(points[0]["vf_baseline"])
        best_idx = max(range(len(ys)), key=lambda i: ys[i])
        label = f"{env.replace('-play-singletask-', ' ').replace('-v0', '')} {config} s{seed} final={ys[-1]:.2f} peak={ys[best_idx]:.2f}"
        ax.plot(xs, ys, marker="o", linewidth=1.5, markersize=3.5, label=label)
        ax.scatter([xs[best_idx]], [ys[best_idx]], s=42, marker="*", zorder=4)
        ax.scatter([xs[-1]], [ys[-1]], s=34, marker="s", zorder=4)
        if vf is not None:
            ax.axhline(vf, linestyle="--", linewidth=0.9, alpha=0.25)
    ax.set_title(name.replace("_", " "))
    ax.set_xlabel("Step (k)")
    ax.set_ylabel("Success")
    ax.set_ylim(-0.03, 1.03)
    ax.grid(True, alpha=0.22)
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.png", dpi=180)
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)
    return True


def main():
    results = []
    for name, envs in GROUPS.items():
        results.append((name, plot_group(name, envs)))
    summary = "\n".join(f"{name}: {'ok' if ok else 'missing'}" for name, ok in results) + "\n"
    (OUT / "plot_summary.txt").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()

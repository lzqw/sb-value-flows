#!/usr/bin/env python3
"""Plot selected state 25-task success curves.

The script reads generated coverage files and existing eval.csv paths. It
generates PNG and PDF figures under reports/figures/state_25task_curves.
"""

from __future__ import annotations

import csv
from pathlib import Path

REPO = Path("/root/sb-value-flows")
OUT = REPO / "reports/figures/state_25task_curves"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def fnum(v: str):
    try:
        return float(v)
    except Exception:
        return None


def eval_curve(path: str):
    rows = read_csv(Path(path))
    points = []
    for r in rows:
        step = fnum(r.get("step", "") or r.get("env_step", "") or r.get("training/step", ""))
        succ = fnum(r.get("evaluation/success", "") or r.get("eval/success", "") or r.get("success", ""))
        if step is not None and succ is not None:
            points.append((step, succ))
    return points


def add_paths_from_runs(selections):
    runs = []
    for p in [
        REPO / "results/experiment_runs.csv",
        REPO / "results/state_goodcase_harvest_single4090.csv",
        REPO / "results/single4090_selective_state_runs_latest.csv",
        REPO / "results/single4090_selective_stageB_1m_latest.csv",
        REPO / "results/single4090_stageB_task3_R2_seed_extension.csv",
    ]:
        runs.extend(read_csv(p))
    out = []
    for label, env_pat, cfg_pat, vf in selections:
        matches = []
        for r in runs:
            env = r.get("env", "")
            cfg = r.get("config_name", "") or r.get("config", "")
            path = r.get("eval_csv", "")
            if env == env_pat and cfg_pat in cfg and path:
                try:
                    final = float(r.get("success_final", "-1"))
                    step = float(r.get("final_step", "0"))
                except Exception:
                    final, step = -1.0, 0.0
                matches.append((step, final, path, cfg))
        if matches:
            matches.sort(reverse=True)
            out.append((label, matches[0][2], vf))
    return out


def plot_group(name: str, selections):
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        (OUT / f"{name}.missing_matplotlib.txt").write_text(str(exc), encoding="utf-8")
        return False
    curves = add_paths_from_runs(selections)
    if not curves:
        (OUT / f"{name}.no_curves.txt").write_text("No matching eval.csv paths found.\n", encoding="utf-8")
        return False
    fig, ax = plt.subplots(figsize=(8, 4.8))
    for label, path, vf in curves:
        pts = eval_curve(path)
        if not pts:
            continue
        xs = [x / 1000 for x, _ in pts]
        ys = [y for _, y in pts]
        best = max(ys)
        best_step = xs[ys.index(best)]
        final = ys[-1]
        drop = best - final
        ax.plot(xs, ys, marker="o", linewidth=1.8, label=f"{label} final={final:.2f} best={best:.2f} drop={drop:.2f}")
        ax.axhline(vf, linestyle="--", linewidth=1.0, alpha=0.35)
        ax.text(xs[-1], vf, f"VF {vf:.2f}", fontsize=8, va="bottom")
        ax.scatter([best_step], [best], s=28)
    ax.set_title(name.replace("_", " "))
    ax.set_xlabel("Step (k)")
    ax.set_ylabel("Success")
    ax.set_ylim(-0.03, 1.03)
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.png", dpi=180)
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)
    return True


def main():
    groups = {
        "cube_double_positive": [
            ("task2 R3", "cube-double-play-singletask-task2-v0", "R3", 0.76),
            ("task3 A2", "cube-double-play-singletask-task3-v0", "A2", 0.73),
            ("task4 A1", "cube-double-play-singletask-task4-v0", "A1", 0.30),
        ],
        "puzzle4x4_collapse": [
            ("task1 P0", "puzzle-4x4-play-singletask-task1-v0", "P0", 0.36),
            ("task3 R2", "puzzle-4x4-play-singletask-task3-v0", "R2", 0.30),
            ("task4 R3", "puzzle-4x4-play-singletask-task4-v0", "R3", 0.28),
        ],
        "scene_task4": [
            ("A1", "scene-play-singletask-task4-v0", "A1", 0.07),
            ("A2", "scene-play-singletask-task4-v0", "A2", 0.07),
            ("R2", "scene-play-singletask-task4-v0", "R2", 0.07),
            ("P0", "scene-play-singletask-task4-v0", "P0", 0.07),
        ],
        "cube_triple_task3": [
            ("R2", "cube-triple-play-singletask-task3-v0", "R2", 0.07),
        ],
    }
    ok = []
    for name, selections in groups.items():
        ok.append((name, plot_group(name, selections)))
    summary = "\n".join(f"{name}: {'ok' if flag else 'missing'}" for name, flag in ok) + "\n"
    (OUT / "plot_summary.txt").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()

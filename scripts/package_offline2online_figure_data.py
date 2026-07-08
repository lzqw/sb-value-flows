#!/usr/bin/env python3
"""Package lightweight data for the offline-to-online Figure 6-style curves."""

from __future__ import annotations

import csv
import shutil
import zipfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
RESULTS_CSV = REPO / "results/offline2online_runs.csv"
CURVE_CSV = REPO / "results/offline2online_curve_data.csv"
EXPORT_DIR = REPO / "exports/offline2online_selected_runs"
ZIP_PATH = REPO / "exports/offline2online_figure_data_lightweight.zip"

SCENARIOS = ("cube-double", "puzzle-4x4", "scene")
METHODS = ("ours", "value_flows", "fql")
SEEDS = ("2", "3")
MAX_TRAIN_BYTES = 5 * 1024 * 1024
MAX_PACKAGE_FILE_BYTES = 10 * 1024 * 1024
FORBIDDEN_PARTS = {
    "wandb",
    "__pycache__",
    ".cache",
    "cache",
}
FORBIDDEN_SUFFIXES = {
    ".pkl",
    ".ckpt",
    ".pt",
    ".pth",
    ".npy",
    ".npz",
    ".log",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def selected_runs(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    selected = [
        r
        for r in rows
        if r.get("scenario") in SCENARIOS
        and r.get("method") in METHODS
        and r.get("seed") in SEEDS
        and r.get("run_stage") == "final"
        and r.get("status") == "completed_1m"
        and r.get("used_in_final_figure") == "True"
    ]
    expected = {(s, m, seed) for s in SCENARIOS for m in METHODS for seed in SEEDS}
    found = {(r["scenario"], r["method"], r["seed"]) for r in selected}
    if found != expected or len(selected) != 18:
        missing = sorted(expected - found)
        extra = sorted(found - expected)
        raise SystemExit(f"selected final matrix mismatch: count={len(selected)} missing={missing} extra={extra}")
    for scenario in SCENARIOS:
        for method in METHODS:
            seeds = sorted(r["seed"] for r in selected if r["scenario"] == scenario and r["method"] == method)
            if seeds != ["2", "3"]:
                raise SystemExit(f"{scenario}/{method} seeds are {seeds}, expected ['2', '3']")
    return sorted(selected, key=lambda r: (r["scenario"], r["method"], int(r["seed"])))


def validate_curves(curves: list[dict[str, str]]) -> None:
    for scenario in SCENARIOS:
        for method in METHODS:
            for seed in SEEDS:
                rows = [
                    r
                    for r in curves
                    if r.get("scenario") == scenario
                    and r.get("method") == method
                    and r.get("seed") == seed
                    and r.get("used_in_final_figure") == "True"
                ]
                steps = {int(float(r["online_step"])) for r in rows if r.get("online_step")}
                if 0 not in steps or 1_000_000 not in steps:
                    raise SystemExit(f"{scenario}/{method}/seed{seed} missing step 0 or 1000000")
                for row in rows:
                    rate = float(row["success_rate"])
                    if not 0.0 <= rate <= 100.0:
                        raise SystemExit(f"success_rate outside 0-100: {scenario}/{method}/seed{seed}: {rate}")


def safe_name(row: dict[str, str]) -> str:
    return f"{row['scenario']}__{row['method']}__seed{row['seed']}"


def copy_if_exists(src: Path, dst: Path) -> None:
    if src.exists() and src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def copy_selected_raw(rows: list[dict[str, str]]) -> None:
    if EXPORT_DIR.exists():
        shutil.rmtree(EXPORT_DIR)
    EXPORT_DIR.mkdir(parents=True)
    for row in rows:
        run_dir = Path(row["run_dir"])
        dst_dir = EXPORT_DIR / safe_name(row)
        dst_dir.mkdir(parents=True)
        copy_if_exists(run_dir / "eval.csv", dst_dir / "eval.csv")
        train = run_dir / "train.csv"
        if train.exists() and train.stat().st_size <= MAX_TRAIN_BYTES:
            copy_if_exists(train, dst_dir / "train.csv")
        copy_if_exists(run_dir / "command.txt", dst_dir / "command.txt")
        config_path = Path(row.get("config_path") or run_dir / "flags.json")
        if config_path.exists():
            copy_if_exists(config_path, dst_dir / "config.json")
        copy_if_exists(run_dir / "summary.json", dst_dir / "summary.json")


def files_for_zip() -> list[Path]:
    paths: list[Path] = [
        RESULTS_CSV,
        CURVE_CSV,
        REPO / "scripts/plot_offline2online.py",
        REPO / "scripts/run_offline2online.py",
    ]
    paths.extend(sorted((REPO / "reports/offline2online").glob("*.md")))
    fig_dir = REPO / "reports/figures/offline2online"
    paths.extend(fig_dir / f"offline2online_selected3.{ext}" for ext in ("svg", "pdf", "png"))
    paths.extend(sorted(EXPORT_DIR.rglob("*")))
    return [p for p in paths if p.is_file()]


def validate_package_files(paths: list[Path]) -> None:
    for path in paths:
        rel = path.relative_to(REPO)
        parts = set(rel.parts)
        if parts & FORBIDDEN_PARTS:
            raise SystemExit(f"forbidden cache/wandb path in package: {rel}")
        if path.suffix in FORBIDDEN_SUFFIXES:
            raise SystemExit(f"forbidden large/raw artifact suffix in package: {rel}")
        if path.stat().st_size > MAX_PACKAGE_FILE_BYTES:
            raise SystemExit(f"package file too large: {rel} ({path.stat().st_size} bytes)")


def write_zip(paths: list[Path]) -> None:
    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(paths, key=lambda p: p.relative_to(REPO).as_posix()):
            arcname = path.relative_to(REPO).as_posix()
            info = zipfile.ZipInfo(arcname)
            info.date_time = (2026, 7, 8, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o644 & 0xFFFF) << 16
            with path.open("rb") as f:
                zf.writestr(info, f.read())


def main() -> None:
    runs = read_csv(RESULTS_CSV)
    curves = read_csv(CURVE_CSV)
    selected = selected_runs(runs)
    validate_curves(curves)
    copy_selected_raw(selected)
    paths = files_for_zip()
    validate_package_files(paths)
    write_zip(paths)
    print(f"selected_runs={len(selected)}")
    print(f"package_files={len(paths)}")
    print(f"zip={ZIP_PATH}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Regenerate the selected offline-to-online three-panel figure."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def main() -> None:
    cmd = [sys.executable, str(REPO / "scripts/run_offline2online.py"), "--mode", "plot"]
    raise SystemExit(subprocess.call(cmd, cwd=REPO))


if __name__ == "__main__":
    main()

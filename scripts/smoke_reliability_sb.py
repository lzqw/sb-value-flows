"""Lightweight smoke checks for reliability-calibrated SB configuration flags.

This script intentionally does not start training. In minimal environments where
runtime ML dependencies such as Flax are not installed, it falls back to a source
check so CI shells can still verify that the reliability-SB flags were added.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REQUIRED_FLAGS = [
    'pm_minimal_sb',
    'pm_sb_lambda',
    'pm_sb_reliability_score',
    'pm_sb_flow_residual_eps',
    'pm_sb_disagree_beta',
    'pm_sb_disagree_umax',
    'pm_sb_typicality_tau',
    'pm_sb_reliability_eps',
    'pm_sb_reliability_normalize',
    'pm_sb_value_preserving',
    'pm_sb_vp_kappa',
    'pm_sb_vp_eta_clip',
    'pm_log_sb_diagnostics',
]


def source_flag_check():
    source = (ROOT / 'agents' / 'pm_value_flows.py').read_text()
    missing = [flag for flag in REQUIRED_FLAGS if flag not in source]
    if missing:
        raise SystemExit(f'Missing reliability SB flags in source: {missing}')


def main():
    try:
        from agents.pm_value_flows import PMValueFlowsAgent, get_config
    except ModuleNotFoundError as exc:
        source_flag_check()
        print(
            'Reliability SB source flag check passed; '
            f'skipped runtime import because dependency is unavailable: {exc.name}'
        )
        return

    config = get_config()
    missing = [flag for flag in REQUIRED_FLAGS if flag not in config]
    if missing:
        raise SystemExit(f'Missing reliability SB flags: {missing}')
    if PMValueFlowsAgent is None:
        raise SystemExit('PMValueFlowsAgent import failed')
    print('Reliability SB smoke import/config check passed.')


if __name__ == '__main__':
    main()

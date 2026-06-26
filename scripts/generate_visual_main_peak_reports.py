#!/usr/bin/env python3
from __future__ import annotations

import csv
import math
from pathlib import Path

RESULTS = Path('results')
REPORTS = Path('reports')
DOMAINS = [
    'visual-antmaze-medium-navigate',
    'visual-scene-play',
    'visual-puzzle-3x3-play',
    'visual-cube-double-play',
    'visual-antmaze-teleport-navigate',
]
TASKS = [f'task{i}' for i in range(1, 6)]
THRESHOLDS = {
    'visual-scene-play': 0.45,
    'visual-puzzle-3x3-play': 0.25,
    'visual-cube-double-play': 0.15,
    'visual-antmaze-teleport-navigate': 0.15,
}
COLS = [
    'domain', 'task', 'method_group', 'config_name', 'seed', 'status', 'final_step',
    'final_success', 'best_peak_success', 'best_peak_step', 'drop_final_from_peak',
    'eval_csv', 'command_txt',
]
COMPLETE_STATUSES = {'completed_300k', 'completed_500k', 'completed_1m'}


def fnum(value: str | None) -> float:
    try:
        if value in (None, ''):
            return math.nan
        return float(value)
    except Exception:
        return math.nan


def read_rows() -> list[dict[str, str]]:
    with (RESULTS / 'audit_all_visual_runs_4090d.csv').open(newline='') as f:
        return list(csv.DictReader(f))


def select_best(
    rows: list[dict[str, str]],
    *,
    completed_only: bool = False,
) -> dict[tuple[str, str], dict[str, str] | None]:
    out = {}
    for domain in DOMAINS:
        for task in TASKS:
            candidates = [
                r for r in rows
                if r.get('visual_domain') == domain
                and r.get('task_id') == task
                and not math.isnan(fnum(r.get('best_peak_success')))
            ]
            if completed_only:
                candidates = [r for r in candidates if r.get('status') in COMPLETE_STATUSES]
            candidates.sort(
                key=lambda r: (
                    fnum(r.get('best_peak_success')),
                    fnum(r.get('final_success')),
                    fnum(r.get('final_step')),
                ),
                reverse=True,
            )
            out[(domain, task)] = candidates[0] if candidates else None
    return out


def cell_record(domain: str, task: str, row: dict[str, str] | None) -> dict[str, str]:
    if row is None:
        return {
            'domain': domain,
            'task': task,
            'method_group': '',
            'config_name': '',
            'seed': '',
            'status': 'missing',
            'final_step': '',
            'final_success': '',
            'best_peak_success': '',
            'best_peak_step': '',
            'drop_final_from_peak': '',
            'eval_csv': '',
            'command_txt': '',
        }
    return {
        'domain': domain,
        'task': task,
        'method_group': row.get('method_group', ''),
        'config_name': row.get('config_name', ''),
        'seed': row.get('seed', ''),
        'status': row.get('status', ''),
        'final_step': row.get('final_step', ''),
        'final_success': row.get('final_success', ''),
        'best_peak_success': row.get('best_peak_success', ''),
        'best_peak_step': row.get('best_peak_step', ''),
        'drop_final_from_peak': row.get('drop_final_from_peak', ''),
        'eval_csv': row.get('eval_csv', ''),
        'command_txt': row.get('command_txt', ''),
    }


def md_table(records: list[dict[str, str]], cols: list[str]) -> str:
    lines = ['| ' + ' | '.join(cols) + ' |', '|' + '|'.join(['---'] * len(cols)) + '|']
    for record in records:
        lines.append('| ' + ' | '.join(str(record.get(c, '')) for c in cols) + ' |')
    return '\n'.join(lines)


def main() -> None:
    REPORTS.mkdir(exist_ok=True)
    rows = read_rows()
    selected_all = select_best(rows)
    selected_completed = select_best(rows, completed_only=True)
    records_all = [
        cell_record(domain, task, selected_all[(domain, task)])
        for domain in DOMAINS
        for task in TASKS
    ]
    records_completed = [
        cell_record(domain, task, selected_completed[(domain, task)])
        for domain in DOMAINS
        for task in TASKS
    ]

    matrix_lines = [
        '# Visual All-Domains Coverage Matrix',
        '',
        'Main value is `best_peak_success`; final and drop are diagnostics.',
        'Completed coverage counts only `completed_300k`, `completed_500k`, and `completed_1m` rows.',
        'Partial rows are retained separately as screening/recovery evidence and are not mixed into completed final results.',
        '',
    ]
    summary_records = []
    for domain in DOMAINS:
        domain_all = [r for r in records_all if r['domain'] == domain]
        domain_completed = [r for r in records_completed if r['domain'] == domain]
        vals_all = [fnum(r.get('best_peak_success')) for r in domain_all if not math.isnan(fnum(r.get('best_peak_success')))]
        vals_completed = [
            fnum(r.get('best_peak_success'))
            for r in domain_completed
            if not math.isnan(fnum(r.get('best_peak_success')))
        ]
        mean_all = sum(vals_all) / len(vals_all) if vals_all else math.nan
        mean_completed = sum(vals_completed) / len(vals_completed) if vals_completed else math.nan
        target = THRESHOLDS.get(domain, '')
        covered_all = len(vals_all)
        covered_completed = len(vals_completed)
        meets = bool(target != '' and covered_completed == 5 and not math.isnan(mean_completed) and mean_completed >= float(target))
        if target == '':
            row_status = 'reference_row'
        elif covered_completed == 5 and meets:
            row_status = 'complete_threshold_met'
        elif covered_completed == 5:
            row_status = 'complete_below_threshold'
        elif covered_all == 5:
            row_status = 'partial_screening_coverage'
        elif covered_all > 0:
            row_status = 'incomplete_partial'
        else:
            row_status = 'no_data'
        summary_records.append({
            'domain': domain,
            'completed_tasks': str(covered_completed),
            'all_evidence_tasks': str(covered_all),
            'completed_best_peak_mean': '' if math.isnan(mean_completed) else f'{mean_completed:.6g}',
            'all_evidence_best_peak_mean': '' if math.isnan(mean_all) else f'{mean_all:.6g}',
            'target': str(target),
            'meets_target': str(meets),
            'row_status': row_status,
        })
        matrix_lines += [
            f'## {domain}',
            '',
            f'- completed_tasks: {covered_completed}/5',
            f'- all_evidence_tasks: {covered_all}/5',
            f'- completed_best_peak_mean: {"" if math.isnan(mean_completed) else f"{mean_completed:.6g}"}',
            f'- all_evidence_best_peak_mean: {"" if math.isnan(mean_all) else f"{mean_all:.6g}"}',
            f'- target: {target}',
            f'- meets_target: {meets}',
            f'- row_status: `{row_status}`',
            '',
            '### Completed Cells',
            '',
        ]
        matrix_lines.append(md_table(domain_completed, COLS))
        matrix_lines += ['', '### All Evidence Cells', '']
        matrix_lines.append(md_table(domain_all, COLS))
        matrix_lines.append('')

    main_lines = [
        '# Visual Main Table Peak Summary',
        '',
        'Best-Eval / Peak Success table selected from all discovered visual runs.',
        'Completed coverage excludes partial/screening rows; those rows are shown separately as recovery evidence.',
        '',
    ]
    main_lines.append(md_table(summary_records, [
        'domain',
        'completed_tasks',
        'all_evidence_tasks',
        'completed_best_peak_mean',
        'all_evidence_best_peak_mean',
        'target',
        'meets_target',
        'row_status',
    ]))
    main_lines.append('')
    main_lines.append('## Completed Selected Cells')
    main_lines.append('')
    main_lines.append(md_table(records_completed, COLS))
    main_lines.append('')
    main_lines.append('## All-Evidence Selected Cells')
    main_lines.append('')
    main_lines.append(md_table(records_all, COLS))
    main_lines.append('')

    (REPORTS / 'visual_all_domains_coverage_matrix.md').write_text('\n'.join(matrix_lines))
    (REPORTS / 'visual_main_table_peak_summary.md').write_text('\n'.join(main_lines))
    print(REPORTS / 'visual_all_domains_coverage_matrix.md')
    print(REPORTS / 'visual_main_table_peak_summary.md')


if __name__ == '__main__':
    main()

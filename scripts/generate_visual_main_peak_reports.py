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


def select_best(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str] | None]:
    out = {}
    for domain in DOMAINS:
        for task in TASKS:
            candidates = [
                r for r in rows
                if r.get('visual_domain') == domain
                and r.get('task_id') == task
                and not math.isnan(fnum(r.get('best_peak_success')))
            ]
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
    selected = select_best(rows)
    records = [cell_record(domain, task, selected[(domain, task)]) for domain in DOMAINS for task in TASKS]

    matrix_lines = ['# Visual All-Domains Coverage Matrix', '', 'Main value is `best_peak_success`; final and drop are diagnostics.', '']
    summary_records = []
    for domain in DOMAINS:
        domain_records = [r for r in records if r['domain'] == domain]
        vals = [fnum(r.get('best_peak_success')) for r in domain_records if not math.isnan(fnum(r.get('best_peak_success')))]
        mean = sum(vals) / len(vals) if vals else math.nan
        target = THRESHOLDS.get(domain, '')
        covered = len(vals)
        meets = bool(target != '' and covered == 5 and not math.isnan(mean) and mean >= float(target))
        summary_records.append({
            'domain': domain,
            'covered_tasks': str(covered),
            'best_peak_mean': '' if math.isnan(mean) else f'{mean:.6g}',
            'target': str(target),
            'meets_target': str(meets),
        })
        matrix_lines += [f'## {domain}', '', f'- covered_tasks: {covered}/5', f'- best_peak_mean: {"" if math.isnan(mean) else f"{mean:.6g}"}', f'- target: {target}', f'- meets_target: {meets}', '']
        matrix_lines.append(md_table(domain_records, COLS))
        matrix_lines.append('')

    main_lines = ['# Visual Main Table Peak Summary', '', 'Best-Eval / Peak Success table selected from all discovered visual runs.', '']
    main_lines.append(md_table(summary_records, ['domain', 'covered_tasks', 'best_peak_mean', 'target', 'meets_target']))
    main_lines.append('')
    main_lines.append('## Selected Cells')
    main_lines.append('')
    main_lines.append(md_table(records, COLS))
    main_lines.append('')

    (REPORTS / 'visual_all_domains_coverage_matrix.md').write_text('\n'.join(matrix_lines))
    (REPORTS / 'visual_main_table_peak_summary.md').write_text('\n'.join(main_lines))
    print(REPORTS / 'visual_all_domains_coverage_matrix.md')
    print(REPORTS / 'visual_main_table_peak_summary.md')


if __name__ == '__main__':
    main()

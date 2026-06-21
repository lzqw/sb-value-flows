#!/usr/bin/env python3
from __future__ import annotations
import csv, math, re, subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

REPO=Path('/root/sb-value-flows'); TMP=Path('/tmp/visual_audit')
RESULTS=REPO/'results'; REPORTS=REPO/'reports'; FIGDIR=REPORTS/'figures'/'visual_curves'
RESULTS.mkdir(exist_ok=True); REPORTS.mkdir(exist_ok=True); FIGDIR.mkdir(parents=True, exist_ok=True)
SUCCESS_COLS=['evaluation/success','eval/success','metrics/success','success','success_rate']
RETURN_COLS=['evaluation/episode.return','evaluation/return','eval/return','episode_return','return','score','normalized_score']
LENGTH_COLS=['evaluation/episode.length','evaluation/length','eval/length','length']
STEP_COLS=['step','env_step','global_step','total_steps','training/step']
VISUAL_DOMAINS=['visual-antmaze-medium-navigate','visual-antmaze-teleport-navigate','visual-cube-double-play','visual-scene-play','visual-puzzle-3x3-play']
OUT_ALL=RESULTS/'audit_all_visual_runs_4090d.csv'

def read_lines(path: Path):
    return [x.strip() for x in path.read_text(errors='ignore').splitlines() if x.strip()] if path.exists() else []

def read_csv(path: Path):
    with path.open(newline='', errors='ignore') as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, rows: list[dict[str, Any]]):
    keys=[]
    for r in rows:
        for k in r.keys():
            if k not in keys: keys.append(k)
    with path.open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)

def find_col(cols, candidates):
    lower={str(c).lower(): c for c in cols}
    for cand in candidates:
        if cand.lower() in lower: return lower[cand.lower()]
    for c in cols:
        lc=str(c).lower()
        for cand in candidates:
            if cand.lower() in lc: return c
    return None

def fnum(x):
    try:
        if x is None or x == '': return math.nan
        return float(x)
    except Exception: return math.nan

def infer_domain_task_env(path: Path):
    sl=str(path).lower().replace('_','-')
    m_medium = (re.search(r'visual[-_]medium[-_]task[-_]?(\d+)', str(path).lower()) or re.search(r'visual[-_]stable[-_]v8p?1?[-_]task[-_]?(\d+)', str(path).lower()) or re.search(r'visual[-_]stable[-_]v8[-_]task[-_]?(\d+)', str(path).lower()))
    if m_medium:
        task = f'task{m_medium.group(1)}'
        d = 'visual-antmaze-medium-navigate'
        return d, task, f'{d}-singletask-{task}-v0'
    for d in VISUAL_DOMAINS:
        if d in sl:
            m=re.search(re.escape(d)+r'.*?task-?(\d+)', sl) or re.search(r'task-?(\d+).*?'+re.escape(d), sl)
            task=f'task{m.group(1)}' if m else 'unknown'
            env=f'{d}-singletask-{task}-v0' if task!='unknown' else d
            return d, task, env
    return '', '', ''

def infer_seed(path: Path):
    s=str(path)
    for pat in [r'seed[_-]?(\d+)', r'sd(\d+)', r'/s(\d+)/']:
        m=re.search(pat, s, re.I)
        if m: return str(int(m.group(1)))
    return ''

def infer_config(path: Path):
    s=str(path).lower()
    if 'r2_stable_strong' in s or 'r2stablestrong' in s: return 'R2_stable_strong'
    if 'r2_stable' in s: return 'R2_stable'
    if 'value_flows' in s and 'pm_' not in s: return 'baseline_value_flows'
    if 'r3' in s: return 'R3'
    if 'r2' in s or 'flow_residual_disagree' in s: return 'R2'
    if 'a2' in s: return 'A2'
    if 'a1' in s or 'action_std' in s: return 'A1'
    if 'p0' in s or 'particle' in s: return 'P0'
    return path.parents[2].name if len(path.parents)>2 else path.parent.name

def infer_method(path: Path, config: str):
    s=str(path).lower()
    if 'visual_matched_4090d_v7' in s: return 'v7'
    if 'visual_stable_v8_1_strong' in s or 'visual_stable_v8p1' in s or 'r2_stable_strong' in s or 'r2stablestrong' in s: return 'v8p1'
    if 'visual_stable_v8' in s or 'visual_stable_v8_task2' in s: return 'v8'
    if 'visual_bigtable_4090d_v6' in s: return 'v6'
    if 'visual_bigtable_4090d_v5' in s: return 'v5_smoke'
    if 'visual_bigtable_4090d_v4' in s: return 'v4'
    return 'other_visual'

def infer_target(path: Path, final_step: int):
    s=str(path).lower()
    if 'smoke' in s or '_1000' in s: return 1000
    if '300000' in s or '300k' in s or 'stagea' in s: return 300000
    if '1000000' in s or '1m' in s or 'matched' in s or 'stageb' in s or 'v7' in s or 'v8' in s: return 1000000
    if final_step>=900000: return 1000000
    if final_step>=250000: return 300000
    return ''

def status_for(path: Path, final_step: int, target):
    s=str(path).lower()
    if 'smoke' in s or target==1000: return 'smoke'
    if target and isinstance(target,int) and final_step>=target*0.98: return 'completed_1m' if target>=1000000 else 'completed_300k'
    if final_step>0: return 'partial'
    return 'unknown'

def find_related(path: Path, kind: str):
    run_root=path.parent.parent if path.parent.name.startswith('sd') else path.parent
    try: c=list(run_root.rglob(kind))
    except Exception: c=[]
    if c:
        c.sort(key=lambda p:p.stat().st_mtime if p.exists() else 0, reverse=True); return str(c[0])
    return ''

def ckpt_info(path: Path):
    run_root=path.parent.parent if path.parent.name.startswith('sd') else path.parent
    roots=[run_root, run_root.parent, Path(str(run_root).replace('/exp/','/checkpoints/'))]
    files=[]
    for r in roots:
        if r.exists():
            try:
                for p in r.rglob('*'):
                    if p.is_file() and any(x in str(p).lower() for x in ['checkpoint','ckpt','best','final']): files.append(p)
            except Exception: pass
    names='\n'.join(str(p).lower() for p in files[:200])
    return len(files), 'best' in names, 'final' in names

def latest_diag(train_csv: str):
    if not train_csv or not Path(train_csv).exists(): return ''
    try:
        rows=read_csv(Path(train_csv));
        if not rows: return ''
        last=rows[-1]; parts=[]
        for c,v in list(last.items()):
            lc=c.lower()
            if any(k in lc for k in ['stable/','actor_lr','critic_lr','encoder_frozen','anchor','sb_weight','reliability','flow_residual','disagree','weight_max','ess']):
                fv=fnum(v); parts.append(f'{c}={fv:.6g}' if not math.isnan(fv) else f'{c}={v}')
            if len(parts)>=40: break
        return '; '.join(parts)
    except Exception as e: return f'train_read_error={e}'

def compact(rows, step_col, succ_col):
    out=[]
    for r in rows:
        st=int(fnum(r.get(step_col))) if step_col else 0; sv=fnum(r.get(succ_col))
        if st<=1 or st%100000==0 or r is rows[-1]:
            label='1' if st<=1 else ('1M' if st==1000000 else f'{st//1000}k')
            out.append(f'{label}:{sv:.3g}')
    if len(out)>24: out=out[:12]+['...']+out[-12:]
    return ' -> '.join(out)

def md_table(rows, cols, n=None):
    rows=rows[:n] if n else rows
    if not rows: return '_No rows._\n'
    def esc(x): return '' if x is None else str(x).replace('\n',' ')
    s='| '+' | '.join(cols)+' |\n| '+' | '.join(['---']*len(cols))+' |\n'
    for r in rows: s+='| '+' | '.join(esc(r.get(c,'')) for c in cols)+' |\n'
    return s

def main():
    all_rows=[]; curve=[]
    for line in read_lines(TMP/'all_eval_csv.txt'):
        p=Path(line); domain,task,env=infer_domain_task_env(p)
        if not domain: continue
        try: rows=read_csv(p)
        except Exception as e:
            all_rows.append({'eval_csv':str(p),'status':'read_failed','notes':repr(e)}); continue
        if not rows: continue
        cols=list(rows[0].keys()); step_col=find_col(cols,STEP_COLS); succ_col=find_col(cols,SUCCESS_COLS); ret_col=find_col(cols,RETURN_COLS); len_col=find_col(cols,LENGTH_COLS)
        if not succ_col: continue
        last=rows[-1]; final_step=int(fnum(last.get(step_col))) if step_col else len(rows)
        final_success=fnum(last.get(succ_col)); final_return=fnum(last.get(ret_col)) if ret_col else math.nan; final_length=fnum(last.get(len_col)) if len_col else math.nan
        best_i=max(range(len(rows)), key=lambda i: fnum(rows[i].get(succ_col))); best=rows[best_i]
        best_success=fnum(best.get(succ_col)); best_step=int(fnum(best.get(step_col))) if step_col else best_i; best_return=fnum(best.get(ret_col)) if ret_col else math.nan; best_length=fnum(best.get(len_col)) if len_col else math.nan
        peak500_success=math.nan; peak500_step=math.nan
        if step_col:
            ix=[i for i,r in enumerate(rows) if fnum(r.get(step_col))>=500000]
            if ix:
                bi=max(ix, key=lambda i:fnum(rows[i].get(succ_col))); peak500_success=fnum(rows[bi].get(succ_col)); peak500_step=int(fnum(rows[bi].get(step_col)))
        target=infer_target(p, final_step); status=status_for(p, final_step, target); config=infer_config(p); method=infer_method(p,config); seed=infer_seed(p)
        train_csv=find_related(p,'train.csv'); cmd=find_related(p,'command.txt'); ckcnt, hasbest, hasfinal=ckpt_info(p)
        drop=final_success-best_success if not math.isnan(final_success) and not math.isnan(best_success) else math.nan
        notes=[]
        if best_success-final_success>=0.30: notes.append('collapse')
        if best_success>=0.50 and final_success<=0.20: notes.append('severe_collapse')
        if status=='partial': notes.append('partial_not_final')
        run_root=str(p.parent.parent if p.parent.name.startswith('sd') else p.parent)
        run_id=re.sub(r'[^A-Za-z0-9_.-]+','_',run_root.replace('/root/autodl-tmp/sb-value-flows-runs/','').replace('/root/sb-value-flows/','repo/'))[-220:]
        rec={'run_id':run_id,'server':'4090d','root_path':run_root,'eval_csv':str(p),'train_csv':train_csv,'command_txt':cmd,'visual_domain':domain,'task_id':task,'env':env,'config_name':config,'method_group':method,'seed':seed,'target_steps':target,'final_step':final_step,'status':status,'final_success':final_success,'final_return':final_return,'final_length':final_length,'best_peak_success':best_success,'best_peak_step':best_step,'best_peak_return':best_return,'best_peak_length':best_length,'peak_after_500k_success':peak500_success,'peak_after_500k_step':peak500_step,'drop_final_from_peak':drop,'trajectory_short':compact(rows,step_col,succ_col),'has_checkpoint':ckcnt>0,'checkpoint_count':ckcnt,'has_best_checkpoint':hasbest,'has_final_checkpoint':hasfinal,'latest_stable_diagnostics':latest_diag(train_csv),'notes':';'.join(notes),'mtime':datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec='seconds')}
        all_rows.append(rec)
        if step_col:
            for r in rows:
                curve.append({'run_id':run_id,'method_group':method,'visual_domain':domain,'task_id':task,'env':env,'config_name':config,'seed':seed,'status':status,'step':int(fnum(r.get(step_col))),'success':fnum(r.get(succ_col)),'return':fnum(r.get(ret_col)) if ret_col else math.nan,'length':fnum(r.get(len_col)) if len_col else math.nan,'eval_csv':str(p)})
    all_rows.sort(key=lambda r:(r.get('method_group',''),r.get('visual_domain',''),r.get('task_id',''),r.get('config_name',''),str(r.get('seed','')),int(r.get('final_step') or 0),r.get('mtime','')))
    write_csv(RESULTS/'audit_all_visual_runs_4090d.csv', all_rows); write_csv(RESULTS/'plot_data_visual_curves.csv', curve)
    best=sorted(all_rows,key=lambda r:fnum(r.get('best_peak_success')), reverse=True); final=sorted(all_rows,key=lambda r:fnum(r.get('final_success')), reverse=True)
    write_csv(RESULTS/'audit_visual_best_peak_table.csv', best); write_csv(RESULTS/'audit_visual_final_table.csv', final)
    collapse=[r for r in all_rows if fnum(r.get('best_peak_success'))-fnum(r.get('final_success'))>=0.30 or (fnum(r.get('best_peak_success'))>=0.50 and fnum(r.get('final_success'))<=0.20)]
    collapse.sort(key=lambda r:fnum(r.get('drop_final_from_peak'))); write_csv(RESULTS/'audit_visual_collapse_cases.csv', collapse)
    comp=[]
    focus=[r for r in all_rows if r.get('visual_domain') in ['visual-antmaze-medium-navigate','visual-antmaze-teleport-navigate']]
    for key in sorted(set((r['visual_domain'],r['task_id']) for r in focus)):
        g=[r for r in focus if (r['visual_domain'],r['task_id'])==key]; out={'visual_domain':key[0],'task':key[1]}
        for mg in ['v7','v8','v8p1']:
            gm=[r for r in g if r.get('method_group')==mg]
            if not gm:
                out[f'{mg}_final']=''; out[f'{mg}_best_peak']=''; out[f'{mg}_drop']=''; out[f'{mg}_status']='no_data'; out[f'{mg}_eval_csv']=''
            else:
                gm.sort(key=lambda r:(1 if 'R2' in str(r.get('config_name')) else 0, int(r.get('target_steps') or 0), int(r.get('final_step') or 0), r.get('mtime','')), reverse=True)
                r=gm[0]; out[f'{mg}_final']=r['final_success']; out[f'{mg}_best_peak']=r['best_peak_success']; out[f'{mg}_drop']=r['drop_final_from_peak']; out[f'{mg}_status']=r['status']; out[f'{mg}_eval_csv']=r['eval_csv']
        finals={mg:fnum(out.get(f'{mg}_final')) for mg in ['v7','v8','v8p1'] if not math.isnan(fnum(out.get(f'{mg}_final')))}; peaks={mg:fnum(out.get(f'{mg}_best_peak')) for mg in ['v7','v8','v8p1'] if not math.isnan(fnum(out.get(f'{mg}_best_peak')))}
        out['best_method_by_final']=max(finals,key=finals.get) if finals else 'no_data'; out['best_method_by_peak']=max(peaks,key=peaks.get) if peaks else 'no_data'; comp.append(out)
    write_csv(RESULTS/'audit_visual_v7_v8_v8p1_comparison.csv', comp)
    counts={}
    for r in all_rows: counts[(r.get('method_group'),r.get('status'))]=counts.get((r.get('method_group'),r.get('status')),0)+1
    count_rows=[{'method_group':k[0],'status':k[1],'count':v} for k,v in sorted(counts.items())]
    proc=subprocess.getoutput("ps -eo pid,ppid,etime,stat,cmd | grep -E 'main.py|visual|4090d|runner|python' | grep -v grep || true")
    gpu=subprocess.getoutput('nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader,nounits || true')
    scanned={'candidate_files':len(read_lines(TMP/'all_candidate_files.txt')),'eval_csv':len(read_lines(TMP/'all_eval_csv.txt')),'train_csv':len(read_lines(TMP/'all_train_csv.txt')),'command_txt':len(read_lines(TMP/'all_command_txt.txt')),'parsed_visual_runs':len(all_rows)}
    light=['results/current_results_snapshot.md','results/experiment_runs.csv','results/eval_curves_index.csv','results/task_scoreboard.csv','results/task_scoreboard.md','results/4090d_interrupted_runs.csv','results/visual_stable_v8_after_reboot_runs.csv','results/visual_stable_v8p1_runs.csv','reports/4090d_interrupted_from_start_report.md','reports/visual_v7_interrupted_trajectory_report.md','reports/visual_stable_v8_after_reboot_report.md','reports/visual_stable_v8_task2_diagnostic.md','reports/visual_stable_v8p1_progress.md']
    light_rows=[{'file':p,'status':'present' if (REPO/p).exists() else 'missing'} for p in light]
    medium=[r for r in all_rows if r.get('visual_domain')=='visual-antmaze-medium-navigate']; medium_final=sorted(medium,key=lambda r:(r.get('task_id'),r.get('method_group'),-fnum(r.get('final_success'))))
    with (REPORTS/'audit_all_visual_experiments_4090d.md').open('w') as f:
        f.write('# 4090D Visual Experiment Audit\n\n')
        f.write(f'Generated: {datetime.now().isoformat(timespec="seconds")}\n\n')
        f.write('## Scope and Semantics\n\n- `final_success` is the success in the last row of `eval.csv`.\n- `best_peak_success` is the maximum success over all eval checkpoints in the run.\n- `drop_final_from_peak = final_success - best_peak_success`.\n- Partial and smoke runs keep best peak diagnostics but are not completed final results.\n\n')
        f.write('## Runtime State\n\n```text\n'+proc+'\n```\n\n## GPU\n\n```text\n'+gpu+'\n```\n\n')
        f.write('## Counts\n\n'+''.join(f'- {k}: {v}\n' for k,v in scanned.items())+'\n')
        f.write('## Existing Lightweight Result Files\n\n'+md_table(light_rows,['file','status'])+'\n')
        f.write('## Method/Status Counts\n\n'+md_table(count_rows,['method_group','status','count'])+'\n')
        f.write('## Medium Final Table\n\n'+md_table(medium_final,['task_id','method_group','config_name','status','final_step','final_success','best_peak_success','best_peak_step','drop_final_from_peak','eval_csv']))
        f.write('\n## Top Final Runs\n\n'+md_table(final,['visual_domain','task_id','method_group','config_name','status','final_step','final_success','best_peak_success','drop_final_from_peak','eval_csv'],20))
        f.write('\n## Top Best-Peak Runs\n\n'+md_table(best,['visual_domain','task_id','method_group','config_name','status','final_step','final_success','best_peak_success','best_peak_step','drop_final_from_peak','eval_csv'],20))
    with (REPORTS/'audit_visual_best_peak_table.md').open('w') as f:
        f.write('# Visual Best-Peak Table\n\nBest peak is a first-class diagnostic/best-eval column. Final row is retained separately.\n\n'+md_table(best,['visual_domain','task_id','method_group','config_name','status','final_success','best_peak_success','best_peak_step','peak_after_500k_success','drop_final_from_peak','eval_csv'],100))
    with (REPORTS/'audit_visual_v7_v8_v8p1_comparison.md').open('w') as f: f.write('# Visual v7 vs v8 vs v8.1 Comparison\n\n'+md_table(comp,list(comp[0].keys()) if comp else []))
    with (REPORTS/'audit_visual_collapse_cases.md').open('w') as f: f.write('# Visual Collapse Cases\n\nCollapse is `best_peak_success - final_success >= 0.30`; severe collapse is `best_peak_success >= 0.50 and final_success <= 0.20`.\n\n'+md_table(collapse,['visual_domain','task_id','method_group','config_name','status','final_step','final_success','best_peak_success','best_peak_step','peak_after_500k_success','drop_final_from_peak','notes','eval_csv'],100))
    print('parsed_visual_runs',len(all_rows)); print('collapse_cases',len(collapse)); print('counts',count_rows)
if __name__=='__main__': main()

#!/usr/bin/env python3
import csv, math, os, subprocess, time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path('/root/sb-value-flows')
LOG_DIR = ROOT / 'logs/bestseed_5task_push_4090d'
EXP_DIR = ROOT / 'exp/bestseed_5task_push_4090d'
REPORT = ROOT / 'reports/bestseed_5task_push_4090d_report.md'
TRACKING = ROOT / 'reports/valueflows_task_level_tracking.md'
CONDA = '/root/miniconda3/bin/conda'
LOG_DIR.mkdir(parents=True, exist_ok=True); EXP_DIR.mkdir(parents=True, exist_ok=True); REPORT.parent.mkdir(parents=True, exist_ok=True)
STATUS = LOG_DIR / 'status.txt'

COMMON = [
 '--agent=agents/pm_value_flows.py',
 '--agent.pm_minimal_sb=true', '--agent.pm_weight_type=field_kernel_norm', '--agent.pm_num_continuations=4',
 '--agent.pm_field_kernel_norm_temp=0.3', '--agent.pm_field_kernel_min_scale=1e-6',
 '--agent.pm_actor_energy_coef=0.0', '--agent.pm_actor_disagree_coef=0.0', '--agent.pm_log_sb_diagnostics=true']
CONFIGS = {
 'A1_action_std_lam0p001': ['--agent.pm_sb_reliability_score=action','--agent.pm_sb_lambda=0.001','--agent.pm_sb_reliability_normalize=std','--agent.pm_sb_value_preserving=false'],
 'R2_flow_residual_disagree_std_lam0p001': ['--agent.pm_sb_reliability_score=flow_residual_disagree','--agent.pm_sb_lambda=0.001','--agent.pm_sb_reliability_normalize=std','--agent.pm_sb_flow_residual_eps=0.05','--agent.pm_sb_disagree_beta=0.5','--agent.pm_sb_disagree_umax=3.0','--agent.pm_sb_value_preserving=false'],
 'R3_flow_residual_disagree_typicality_std_lam0p001': ['--agent.pm_sb_reliability_score=flow_residual_disagree_typicality','--agent.pm_sb_lambda=0.001','--agent.pm_sb_reliability_normalize=std','--agent.pm_sb_flow_residual_eps=0.05','--agent.pm_sb_disagree_beta=0.5','--agent.pm_sb_disagree_umax=3.0','--agent.pm_sb_typicality_tau=1.0','--agent.pm_sb_value_preserving=false'],
}
ENV_FLAGS = {
 'cube-triple': ['--agent.discount=0.995','--agent.bcfm_lambda=3','--agent.confidence_weight_temp=0.03'],
 'cube-double': ['--agent.discount=0.995','--agent.confidence_weight_temp=3'],
 'scene': ['--agent.ret_agg=min'],
}
PAPER = {
 'cube-triple-play-singletask-task1-v0': '59+-12', 'cube-triple-play-singletask-task2-v0': '0+-0', 'cube-triple-play-singletask-task3-v0': '7+-3', 'cube-triple-play-singletask-task4-v0': '0+-0', 'cube-triple-play-singletask-task5-v0': '2+-1',
 'cube-double-play-singletask-task1-v0': '97+-1', 'cube-double-play-singletask-task2-v0': '76+-7', 'cube-double-play-singletask-task3-v0': '73+-4', 'cube-double-play-singletask-task4-v0': '30+-5', 'cube-double-play-singletask-task5-v0': '69+-5',
 'scene-play-singletask-task1-v0': '99+-0', 'scene-play-singletask-task2-v0': '97+-1', 'scene-play-singletask-task3-v0': '94+-2', 'scene-play-singletask-task4-v0': '7+-4', 'scene-play-singletask-task5-v0': '0+-0',
}
DIAGS = ['pm/weight_max','pm/ess','pm/reliability_mean','pm/reliability_std','pm/flow_residual_mean','pm/flow_residual_std','pm/disagree_mean','pm/disagree_std','pm/typicality_mean','pm/typicality_std','pm/proj_delta_mean','pm/cov_y_action','pm/corr_y_action']

@dataclass(frozen=True)
class Task:
    queue: str; env: str; config: str; seed: int; steps: int

running, results, failures = {}, [], []

def now(): return time.strftime('%Y-%m-%d %H:%M:%S')
def domain(env): return '-'.join(env.split('-')[:2])
def env_flags(env): return ENV_FLAGS.get(domain(env), [])
def data_exists(env): return Path(f'/root/.ogbench/data/{env}.npz').exists() and Path(f'/root/.ogbench/data/{env}-val.npz').exists()
def discover(dom):
    a=[f'{dom}-play-singletask-task{i}-v0' for i in range(1,6)]
    if all(data_exists(x) for x in a): return a
    b=[f'{dom}-play-singletask-task{i}-v0' for i in range(0,5)]
    if all(data_exists(x) for x in b): return b
    return [x for x in a if data_exists(x)]

def run_dir(t): return EXP_DIR / t.queue / f'{t.config}_{t.env}_seed{t.seed}_{t.steps}'
def log_path(t,g): return LOG_DIR / f'{t.queue}_{t.config}_{t.env}_seed{t.seed}_gpu{g}.log'
def complete(t):
    e=run_dir(t)/'eval.csv'; tr=run_dir(t)/'train.csv'
    return e.exists() and tr.exists() and sum(1 for _ in open(e, errors='ignore')) >= (21 if t.steps==1000000 else 7)

def cmd(t):
    c=['python','main.py',f'--env_name={t.env}',f'--seed={t.seed}',f'--save_dir={run_dir(t)}',f'--wandb_run_group=bestseed_5task_{t.queue}_{t.config}_{t.env}_seed{t.seed}','--enable_wandb=0',f'--offline_steps={t.steps}','--online_steps=0','--eval_interval=50000','--eval_episodes=10','--log_interval=25000','--save_interval=999999999'] + COMMON + CONFIGS[t.config] + env_flags(t.env)
    agent_i = c.index('--agent=agents/pm_value_flows.py')
    if any(x.startswith('--agent.') for x in c[:agent_i]): raise RuntimeError('CONFIG_ERROR agent flag ordering')
    if any('pm_action_normalize' in x for x in c): raise RuntimeError('CONFIG_ERROR forbidden pm_action_normalize')
    return c

def metric(t, status):
    rd=run_dir(t); e=rd/'eval.csv'; tr=rd/'train.csv'; row={}
    if e.exists():
        with open(e, newline='', errors='ignore') as f:
            rows=list(csv.DictReader(f)); row=rows[-1] if rows else {}
    def num(k):
        try: return float(row.get(k,''))
        except Exception: return math.nan
    out={'queue':t.queue,'env':t.env,'config':t.config,'seed':t.seed,'steps':t.steps,'status':status,'run_dir':str(rd),'train_rows':0,'eval_rows':0,'success':num('evaluation/success'),'return':num('evaluation/episode.return'),'length':num('evaluation/episode.length')}
    for p,k in [(tr,'train_rows'),(e,'eval_rows')]:
        if p.exists(): out[k]=max(0, sum(1 for _ in open(p, errors='ignore'))-1)
    for k in DIAGS: out[k]=num(k)
    wm=out.get('pm/weight_max', math.nan); out['collapse']=bool(not math.isnan(wm) and wm>0.95)
    txt=''; lp=LOG_DIR / f'{t.queue}_{t.config}_{t.env}_seed{t.seed}_gpu0.log'
    for cand in LOG_DIR.glob(f'{t.queue}_{t.config}_{t.env}_seed{t.seed}_gpu*.log'):
        try: txt += cand.read_text(errors='ignore')[-4000:]
        except Exception: pass
    if any(x in txt for x in ['Traceback','CUDA_ERROR_OUT_OF_MEMORY','RESOURCE_EXHAUSTED','NaN','nan']): out['log_warning']='yes'
    else: out['log_warning']=''
    return out

def status(total, done, failed, pending):
    cur=' '.join(f'gpu{k}={v.queue}:{v.config}:{v.env}:seed{v.seed}' for k,v in running.items()) or 'none'
    with open(STATUS,'a') as f: f.write(f'[{now()}] total={total} completed={done} failed={failed} running={len(running)} remaining={pending} | {cur}\n')

def launch(t,g):
    rd=run_dir(t); rd.mkdir(parents=True, exist_ok=True); lp=log_path(t,g)
    env=os.environ.copy(); env.update({'CUDA_VISIBLE_DEVICES':str(g),'LD_LIBRARY_PATH':'/root/.mujoco/mujoco210/bin:'+env.get('LD_LIBRARY_PATH',''),'MUJOCO_GL':'egl','PYOPENGL_PLATFORM':'egl','SDL_VIDEODRIVER':'dummy','OGBENCH_DATA_DIR':'/root/.ogbench/data','HOME':'/root','XDG_CACHE_HOME':'/root/.cache','XLA_PYTHON_CLIENT_PREALLOCATE':'true','XLA_PYTHON_CLIENT_MEM_FRACTION':'0.90'})
    full=[CONDA,'run','-n','value-flows']+cmd(t)
    with open(lp,'w') as f:
        f.write('COMMAND: '+' '.join(full)+'\n')
        p=subprocess.Popen(full,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
    running[g]=t; return p

def report():
    def fmt(x): return 'nan' if x is None or (isinstance(x,float) and math.isnan(x)) else f'{x:.6g}' if isinstance(x,float) else str(x)
    lines=['# Best-seed 5-task reliability SB 4090D report','', 'This is an optimistic best-seed / 300k screening result set, not a full 8-seed official protocol.','']
    lines += ['## Cube-triple R2 best-seed 5-task results','','| env | paper VF | ours | gap | return | length | weight_max | ess | collapse | status |','|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
    ct=[r for r in results if r['queue']=='queueA_cube_triple_5task_1m']
    vals=[]
    for r in sorted(ct, key=lambda x:x['env']):
        s=r['success']; vals.append(s if not math.isnan(s) else None); p=PAPER.get(r['env'],''); base=float(p.split('+-')[0])/100 if p else math.nan; gap=s-base if not math.isnan(s) and not math.isnan(base) else math.nan
        lines.append(f"| {r['env']} | {p} | {fmt(s)} | {fmt(gap)} | {fmt(r['return'])} | {fmt(r['length'])} | {fmt(r['pm/weight_max'])} | {fmt(r['pm/ess'])} | {r['collapse']} | {r['status']} |")
    clean=[v for v in vals if v is not None]
    mean=sum(clean)/len(clean) if clean else math.nan; std=(sum((x-mean)**2 for x in clean)/len(clean))**0.5 if clean else math.nan
    lines += ['', f'cube-triple 5-task mean={fmt(mean)} std={fmt(std)}', 'paper Value Flows cube-triple-play domain=14+-3', 'current task1 R2 3-seed mean=0.633333; Origin task1=0.56; Minimal SB task1=0.60', '']
    lines += ['## Cube-double / scene 300k screening','','| domain | env | config | paper VF | ours | gap | return | weight_max | ess | reliability_mean | reliability_std | flow_residual_mean | disagree_mean | typicality_mean | collapse | status |','|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|']
    for r in sorted([x for x in results if x['queue']=='queueB_screen_300k'], key=lambda x:(domain(x['env']),x['env'],x['config'])):
        p=PAPER.get(r['env'],''); base=float(p.split('+-')[0])/100 if p else math.nan; gap=r['success']-base if not math.isnan(r['success']) and not math.isnan(base) else math.nan
        lines.append(f"| {domain(r['env'])} | {r['env']} | {r['config']} | {p} | {fmt(r['success'])} | {fmt(gap)} | {fmt(r['return'])} | {fmt(r['pm/weight_max'])} | {fmt(r['pm/ess'])} | {fmt(r['pm/reliability_mean'])} | {fmt(r['pm/reliability_std'])} | {fmt(r['pm/flow_residual_mean'])} | {fmt(r['pm/disagree_mean'])} | {fmt(r['pm/typicality_mean'])} | {r['collapse']} | {r['status']} |")
    lines += ['', '## Best Config By Domain','']
    for dom in ['cube-double','scene']:
        rows=[r for r in results if r['queue']=='queueB_screen_300k' and domain(r['env'])==dom and not r['collapse'] and not math.isnan(r['success'])]
        by={}
        for r in rows: by.setdefault(r['config'],[]).append(r['success'])
        if by:
            best=max(by.items(), key=lambda kv: sum(kv[1])/len(kv[1])); lines.append(f'- {dom}: {best[0]} mean={fmt(sum(best[1])/len(best[1]))}')
    lines += ['', '## Failures / warnings','']
    lines += [f"- {f}" for f in failures] or ['- none']
    lines += ['', '## GPU / Git','```']
    for c in [['nvidia-smi'], ['git','branch','--show-current'], ['git','rev-parse','HEAD'], ['git','status','--short']]:
        try: lines.append(subprocess.check_output(c,cwd=ROOT,text=True,stderr=subprocess.STDOUT)[:5000])
        except Exception as e: lines.append(str(e))
    lines += ['```','']
    REPORT.write_text('\n'.join(lines))

def update_tracking_and_push():
    stamp=now(); block=['',f'## 4090D best-seed five-task reliability SB update ({stamp})','',f'Report: `{REPORT.relative_to(ROOT)}`','', 'This section is generated after the best-seed / 300k screening sweep and is not an official 8-seed protocol.','']
    for r in results: block.append(f"- {r['queue']} | {r['env']} | {r['config']} | seed={r['seed']} | steps={r['steps']} | success={r['success']} | return={r['return']} | collapse={r['collapse']} | status={r['status']}")
    with open(TRACKING,'a') as f: f.write('\n'.join(block)+'\n')
    subprocess.run(['git','add',str(TRACKING.relative_to(ROOT)),str(REPORT.relative_to(ROOT)),'scripts/run_bestseed_5task_push_4090d.py'],cwd=ROOT)
    subprocess.run(['git','commit','-m','Update best-seed five-task reliability SB results'],cwd=ROOT)
    p=subprocess.run(['git','push','origin','HEAD:results/bestseed-5task-4090d'],cwd=ROOT,text=True,capture_output=True)
    with open(LOG_DIR/'git_push.log','w') as f: f.write(p.stdout+p.stderr)
    if p.returncode != 0: failures.append('git push failed; no force push attempted; see git_push.log')

# Build tasks.
ct=discover('cube-triple')
if len(ct) != 5: failures.append(f'Queue A invalid cube-triple task discovery: {ct}')
queue_a=[Task('queueA_cube_triple_5task_1m',e,'R2_flow_residual_disagree_std_lam0p001',2,1000000) for e in ct[:5]] if len(ct)==5 else []
queue_b=[]
for dom in ['cube-double','scene']:
    envs=discover(dom)
    if len(envs)!=5: failures.append(f'Queue B {dom} discovery incomplete: {envs}')
    for e in envs[:5]:
        for cfg in ['A1_action_std_lam0p001','R2_flow_residual_disagree_std_lam0p001','R3_flow_residual_disagree_typicality_std_lam0p001']:
            queue_b.append(Task('queueB_screen_300k',e,cfg,2,300000))

total=len(queue_a)+len(queue_b); done=failed=0; procs={}; status(total,done,failed,total)
while queue_a or queue_b or procs:
    for g,p in list(procs.items()):
        if p.poll() is not None:
            t=running.pop(g); procs.pop(g); st='OK' if p.returncode==0 and complete(t) else 'FAILED'; results.append(metric(t,st)); done += st=='OK'; failed += st!='OK';
            if st!='OK': failures.append(f'{t} returncode={p.returncode}')
            report(); status(total,done,failed,len(queue_a)+len(queue_b))
    for g in [0,1]:
        if g in procs: continue
        nxt=None
        if queue_a: nxt=queue_a.pop(0)
        elif queue_b: nxt=queue_b.pop(0)
        if nxt:
            if complete(nxt): results.append(metric(nxt,'SKIPPED_COMPLETE')); done += 1; status(total,done,failed,len(queue_a)+len(queue_b)); continue
            procs[g]=launch(nxt,g); status(total,done,failed,len(queue_a)+len(queue_b))
    time.sleep(30)
report(); update_tracking_and_push(); report(); status(total,done,failed,0)

#!/usr/bin/env python3
from pathlib import Path
import csv, html
ROOT = Path('/root/sb-value-flows')
DATA = ROOT / 'results' / 'plot_data_visual_curves.csv'
OUT = ROOT / 'reports' / 'figures' / 'visual_curves'
OUT.mkdir(parents=True, exist_ok=True)
COLORS = ['#1f77b4','#d62728','#2ca02c','#9467bd','#ff7f0e','#17becf','#8c564b','#e377c2']
DOMAINS = [
    'visual-antmaze-medium-navigate',
    'visual-scene-play',
    'visual-puzzle-3x3-play',
    'visual-cube-double-play',
    'visual-antmaze-teleport-navigate',
]
TASKS = [f'task{i}' for i in range(1, 6)]

def rows():
    with DATA.open(newline='') as f: return list(csv.DictReader(f))
def fnum(x):
    try: return float(x)
    except Exception: return None
def label(r): return f"{r['method_group']} / {r['config_name']} / seed{r['seed']}"
def sx(x, xmin, xmax, w=760, l=80): return l + (x-xmin)/(xmax-xmin or 1)*w
def sy(y, h=360, t=40): return t + (1-y)*h
def plot_group(rs, title, filename):
    groups={}
    for r in rs: groups.setdefault(r['run_id'], []).append(r)
    xmin=0; xmax=max([fnum(r['step']) or 0 for r in rs] + [1000000])
    width=920; height=500
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>']
    parts.append(f'<text x="80" y="25" font-family="Arial" font-size="16">{html.escape(title)}</text>')
    # axes/grid
    for y in [0,0.25,0.5,0.75,1.0]:
        yy=sy(y); parts.append(f'<line x1="80" y1="{yy:.1f}" x2="840" y2="{yy:.1f}" stroke="#ddd"/>')
        parts.append(f'<text x="45" y="{yy+4:.1f}" font-family="Arial" font-size="11">{y:.2g}</text>')
    parts.append('<line x1="80" y1="400" x2="840" y2="400" stroke="#333"/><line x1="80" y1="40" x2="80" y2="400" stroke="#333"/>')
    for step in range(0, int(xmax)+1, 200000):
        xx=sx(step,xmin,xmax); parts.append(f'<line x1="{xx:.1f}" y1="400" x2="{xx:.1f}" y2="405" stroke="#333"/>')
        lab='0' if step==0 else ('1M' if step==1000000 else f'{step//1000}k')
        parts.append(f'<text x="{xx-12:.1f}" y="420" font-family="Arial" font-size="11">{lab}</text>')
    for idx,(rid,g) in enumerate(sorted(groups.items(), key=lambda kv: label(kv[1][0]))):
        g=sorted(g,key=lambda r:fnum(r['step']) or 0); color=COLORS[idx%len(COLORS)]
        pts=[]
        ys=[]
        for r in g:
            x=fnum(r['step']); y=fnum(r['success'])
            if x is None or y is None: continue
            pts.append(f'{sx(x,xmin,xmax):.1f},{sy(y):.1f}'); ys.append((x,y))
        if not pts: continue
        parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2"/>')
        best=max(ys,key=lambda p:p[1]); final=ys[-1]
        parts.append(f'<circle cx="{sx(best[0],xmin,xmax):.1f}" cy="{sy(best[1]):.1f}" r="6" fill="{color}" stroke="black"/>')
        parts.append(f'<rect x="{sx(final[0],xmin,xmax)-5:.1f}" y="{sy(final[1])-5:.1f}" width="10" height="10" fill="{color}" stroke="black"/>')
        ly=445+idx*15
        parts.append(f'<line x1="80" y1="{ly}" x2="105" y2="{ly}" stroke="{color}" stroke-width="2"/><text x="112" y="{ly+4}" font-family="Arial" font-size="11">{html.escape(label(g[0]))} best={best[1]:.2g}@{int(best[0])} final={final[1]:.2g}</text>')
    parts.append('</svg>')
    (OUT/filename).write_text('\n'.join(parts))

def main():
    allr=rows(); made=[]
    for old in OUT.glob('*.svg'):
        old.unlink()
    for domain in DOMAINS:
        for task in TASKS:
            fn=f"{domain.replace('visual-','').replace('-','_')}_{task}_curves.svg"
            title=f"{domain} {task}: Best-Eval / Peak Success"
            sub=[r for r in allr if r['visual_domain']==domain and r['task_id']==task]
            if not sub:
                continue
            sub.sort(key=lambda r:(r.get('method_group',''), r.get('config_name',''), r.get('seed',''), fnum(r.get('step')) or 0))
            plot_group(sub,title,fn); made.append(fn)
    (OUT/'README.md').write_text('# Visual Curve Figures\n\nSVG line plots. Circles mark best peak; squares mark final/latest eval.\n\n'+'\n'.join(f'- `{m}`' for m in made)+'\n')
    print('generated',len(made),'svg figures')
    for m in made: print(OUT/m)
if __name__=='__main__': main()

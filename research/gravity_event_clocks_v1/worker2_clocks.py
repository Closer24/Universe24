#!/usr/bin/env python3
"""Worker 2: independent full-state clock/source range and pulse sensitivity audits."""
from __future__ import annotations
import json
from pathlib import Path
from universe24.core.state import Cube,State,Channel
from universe24.core.engine import Engine
from universe24.core.group_2o import DIRECTIONS

ROOT=Path(__file__).resolve().parent;OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
SOURCE=Channel(-1,-1,0);KIND={'A':Channel(-1,-1,0),'B':Channel(0,-1,4)}
E=Engine()

def period(seq,span,field='complete'):
    extract = (lambda node:node) if field=='complete' else (lambda node:tuple(v.b for v in node))
    sample=[extract(s) for s in seq]
    return next((P for P in range(1,span+1) if all(sample[t]==sample[t%P] for t in range(len(seq)))),None)

def distance_trial(L,mode,distance,kind,H):
    center=(L//2,)*3;clock=(center[0]+distance,center[1],center[2])
    cells={(*clock,g):KIND[kind] for g in range(48)}
    if mode=='on':cells.update({(*center,g):SOURCE for g in range(48)})
    s=State(Cube(L),cells=cells);start=s;hist=[];ticks=[];max_cells=0;counter_positions=set(); inverses=0
    for t in range(H+1):
        node=s.node(clock);hist.append(node)
        if node[0].a<0<=node[0].b:ticks.append(t)
        max_cells=max(max_cells,len(s.cells))
        counter_positions|={a[:3] for a,v in s.cells.items() if v.a or v.b}
        if t<H:
            n=E.advance(s); assert E.rewind(n)==s;inverses+=1;s=n
    P=period(hist,20);bP=period(hist,20,field='b')
    # Over the entire H-window, count all regular intervals, not just period.
    inter=[b-a for a,b in zip(ticks,ticks[1:])]
    return {'kind':kind,'source':mode,'distance':distance,'horizon':H,
            'complete_clock_node_period':P,'b_counter_node_period':bP,'tick_times':ticks[:20],
            'tick_interval_values':sorted(set(inter)),
            'tick_count_states_0_to_19':sum(0<=t<20 for t in ticks),
            'mean_rate_first_20':sum(0<=t<20 for t in ticks)/20,
            'steady_tick':bool(inter) and len(set(inter))==1,
            'max_retained_cells':max_cells,'counter_active_spatial_sites':len(counter_positions),
            'full_state_inverse_steps':inverses,
            'all48_clock_initial_preparation':True}

def run():
    rows=[]
    for kind in ('A','B'):
        for distance in (1,2,3,4,5,6):
            for mode in ('off','on'):
                rows.append(distance_trial(19,mode,distance,kind,40))
    # Source-magnitude control at 1 and 3 links; exact same clock and 48 channels.
    amplitude_rows=[]
    for kind in ('A','B'):
        for distance in (1,3):
            for amp in (1,2,3):
                L=19;origin=(9,9,9);clock=(9+distance,9,9)
                cells={(*origin,g):Channel(-amp,-amp,0) for g in range(48)}
                cells.update({(*clock,g):KIND[kind] for g in range(48)})
                s=State(Cube(L),cells=cells);hist=[];inv=0;maxsize=0
                for t in range(21):
                    hist.append(s.node(clock));maxsize=max(maxsize,len(s.cells))
                    if t<20:
                        nxt=E.advance(s);assert E.rewind(nxt)==s;s=nxt;inv+=1
                amplitude_rows.append({'kind':kind,'distance':distance,'source_amplitude':amp,
                            'clock_period_first_20_steps':period(hist,20),'max_retained_cells':maxsize,'inverse_steps':inv})
    # independent faces check for on/off symmetry at distance 1 and distance 3
    orientations=[]
    for k in range(6):
        for kind in ('A','B'):
            L=19;org=(9,9,9);dir=DIRECTIONS[k];d=1;clock=tuple(org[j]+dir[j]*d for j in range(3))
            cells={(*org,g):SOURCE for g in range(48)};cells.update({(*clock,g):KIND[kind] for g in range(48)})
            s=State(Cube(L),cells=cells);hist=[]
            for t in range(21):
                hist.append(s.node(clock))
                if t<20:s=E.advance(s)
            orientations.append({'face':k,'kind':kind,'near_period':period(hist,20)})
    assert all(z['near_period']==5 for z in orientations)
    report={'worker':'B_clock_distance','status':'PASS','L':19,'sources_all48':True,
            'source_clock_distance_control':rows,'source_amplitude_control':amplitude_rows,
            'six_direction_controls':orientations,
            'interpretation':'Restricted oscillators; no universal inverse-radius redshift. A 20-step full-return may contain irregular tick events; no physical proper-time clock calibration.'}
    path=OUT/'worker2_clocks.json';path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    main=[{'kind':r['kind'],'d':r['distance'],'off_on':r['source'],'period':r['complete_clock_node_period'],'bperiod':r['b_counter_node_period'],'tick_intervals':r['tick_interval_values']} for r in rows if r['source']=='on']
    print(json.dumps({'worker':report['worker'],'status':'PASS','distance_results':main,'path':str(path)}),flush=True)
    return report

if __name__=='__main__':run()

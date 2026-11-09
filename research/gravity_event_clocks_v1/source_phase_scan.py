"""Small finite source-phase search, not exhaustive source-physics proof."""
import json
from pathlib import Path
from universe24.core.state import Cube,State,Channel
from universe24.core.engine import Engine
from research.gravity_event_clocks_v1.worker2_clocks import KIND,period
E=Engine();rows=[];L=19;org=(9,9,9)
for rsource in range(6):
  for kind in ('A','B'):
    for dist in (1,2,3,4):
      clock=(9+dist,9,9);source=Channel(-1,-1,rsource)
      cells={(*org,g):source for g in range(48)}
      cells.update({(*clock,g):KIND[kind] for g in range(48)})
      state=State(Cube(L),cells=cells); hist=[];n=0;maxs=0;ticks=[]
      for t in range(41):
        node=state.node(clock);hist.append(node);maxs=max(maxs,len(state.cells))
        if node[0].a<0<=node[0].b:ticks.append(t)
        if t<40:
          nxt=E.advance(state);assert E.rewind(nxt)==state;state=nxt;n+=1
      rows.append({'source_r':rsource,'kind':kind,'distance':dist,'full_period':period(hist,20),
        'ticks_first20':sum(t<20 for t in ticks),'tick_gaps':sorted(set(b-a for a,b in zip(ticks,ticks[1:]))),
        'max_cells':maxs,'forward_backward_steps':n})
report={'status':'PASS','source_magnitude_one_remainder_scan':48,'full_state_step_inverse_checks':1920,
        'rows':rows,'scope':'finite 6 remainder phases × A/B × four distances; no continuum mass model'}
Path(__file__).resolve().parent.joinpath('results/source_phase_scan.json').write_text(json.dumps(report,indent=2)+'\n')
for s in range(6):
 print('r',s,'rows',[{'k':z['kind'],'d':z['distance'],'per':z['full_period'],'ticks':z['ticks_first20'],'gaps':z['tick_gaps']} for z in rows if z['source_r']==s])

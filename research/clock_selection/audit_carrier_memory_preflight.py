"""Independent complete preparations for conditional-carrier terminal memory."""
import itertools,json
from pathlib import Path
from research.clock_selection.audit import Snapshot,DIRECTIONS,coupling,file_digest,native_digest,ROOT
from research.clock_selection.audit_v2 import expected_initial as controller_initial,footprints
SHA='9c69e4c30e337e1bee1554415106112f137145d199303c44a16ee57467efc8e4'
PHASES=((0,1),(1,0),(0,-1),(-1,0))

def planned():
 return [dict(id=f'carrier-memory-L{L}-p{phase}-{mask}',side=L,receiver_phase=phase,control=mask,clock_remainder=0,phase=0,writer_delay=2,gap=38,stage='encounter',guide_target_channel=0,compensation_direction=None,clock_present=True) for L,phase,mask in itertools.product((393,425),range(4),('00','10','01','11'))]

def region(case,name,t=0):
 c=case['side']//2;dx=0 if name=='controller' else 20;p=((0 if name=='controller' else case['receiver_phase'])+t)%4;center=(c+dx,c+1,c);nodes=(center,*(tuple(center[j]+d[j] for j in range(3)) for d in DIRECTIONS));cells={(*n,g):(0,0,2) for n in nodes for g in range(48)};cells[(*center,2)]=(*PHASES[p],0);cp=coupling((1,1,1))
 for d,node in enumerate(nodes[1:]):
  g=next(g for g in range(48) if cp.ports[d^1][g]==2);cells[(*node,g)]=(0,0,(0 if d==3 else 2)+2*cp.weights[d^1][g]*(0,1,1,0)[p])
 cells[(center[0],center[1]-1,center[2],14)]=(0,0,4)
 return cells

def initial(case):
 seed=controller_initial(case);cells=dict(seed.cells);c=case['side']//2
 for g in (0,14):assert cells.pop((c+20,c,c,g))==(0,0,0 if g==0 else 4)
 for a,v in region(case,'receiver').items():
  assert a not in cells or cells[a]==v,('Conflicting receiver initial state',a)
  cells[a]=v
 return Snapshot(case['side'],seed.background,cells)

def preparation(cases):
 seed={case['control']:initial(case) for case in cases};case=cases[0];c=case['side']//2;allowed=footprints(case);addresses=set().union(*(s.cells for s in seed.values()));tests=[]
 for i,name in enumerate(('writer','probe')):
  for other in '01':
   off='0'+other if i==0 else other+'0';on='1'+other if i==0 else other+'1';diff={a for a in addresses if seed[off].at(a)!=seed[on].at(a)};expected=lambda a:(0,0,0 if a[1:3]==(c,c) and a[3]==0 else 4 if a[1:3]==(c,c) and a[3]==14 else 2);assert diff<=allowed[name] and all(seed[off].at(a)==expected(a) for a in allowed[name]);tests.append(dict(source=name,other=other,changed_addresses=len(diff),outside_footprint_equal=True,absent_footprint_pristine=True))
 margins=[min(min(q,case['side']-1-q) for a,v in s.cells.items() if any(v[:2]) for q in a[:3]) for s in seed.values()];assert all(m>120 for m in margins)
 return dict(side=case['side'],receiver_phase=case['receiver_phase'],footprint_checks=tests,complete_interfaces_compatible=True,initial_active_margins=margins)

def review():
 from research.clock_selection import carrier_memory as prod
 p=json.loads(prod.PROTOCOL.read_text());assert file_digest(prod.PROTOCOL)==SHA;assert file_digest(prod.__file__)=='899cc00bb1bd1b9b8b3e891555a164139b9086cb0b21eefbdf18787320ea6c18';assert file_digest(ROOT/'research/clock_selection/carrier_memory_budget.py')=='fa02185c1c424dd687a920238a7df89c4a336c6ce4c05133c28e27aa6a2495d5';cases=planned();assert [c for group in prod.groups(p) for c in group]==cases;rows=[];groups=[];cp=coupling((1,1,1))
 for case in cases:
  actual=prod.assemble(prod.spec(case,p)).initial;expected=initial(case);assert expected==Snapshot(case['side'],tuple(actual.background),{a:tuple(v) for a,v in actual.cells.items()})
  for name in ('controller','receiver'):
   assert all(expected.at(a)==v for a,v in region(case,name).items())
   if case['control']=='00':
    for t in range(4):
     before,after=region(case,name,t),region(case,name,t+1)
     for a,v in before.items():
      u=sum(cp.weights[d][a[3]]*before.get(tuple(a[j]+delta[j] for j in range(3))+(cp.ports[d][a[3]],),(0,0,2))[1] for d,delta in enumerate(DIRECTIONS));ell,r=divmod(2*u+v[2],6);assert after[a]==(v[1],ell-v[0],r)
  rows.append(dict(case=case,initial_sha256=native_digest(expected),complete_initial_equal=True))
 for i in range(0,32,4):groups.append(preparation(cases[i:i+4]))
 assert groups==prod.preflight(p)['groups'];report=dict(passed=True,new_native_trajectories=0,protocol_sha256=SHA,producer_sha256=file_digest(prod.__file__),wrapper_sha256=file_digest(ROOT/'research/clock_selection/carrier_memory_budget.py'),auditor_sha256=file_digest(__file__),cases=rows,groups=groups,readout_review='Complete unmasked input/outlet boxes and fixedC windows; terminal336 region must differ from each00/10/01 with a nonzero fixed phase, all masks quiet. Weaker11-vs10 result cannot promote primary failure.',timing_review='Whole-wrapper240CPU accounting; native checkpoint now precedes decoding/observation; exact source archive retained. Native runtime outcomes remain untested in this preflight.')
 out=ROOT/'research/clock_selection/evidence/independent_audit/carrier_memory_preflight.json'
 with out.open('x') as f:json.dump(report,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps(dict(passed=True,complete_initials=len(rows),new_native_trajectories=0)))
if __name__=='__main__':review()

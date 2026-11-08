"""Independent static preparation review for route-to-clock composition."""
import itertools,json
from pathlib import Path
from research.clock_selection.audit import Snapshot,DIRECTIONS,coupling,file_digest,native_digest,ROOT,source_control
SHA='d0c2883260705631121be1efcd3111581d3db349ceac3d4e8f4bf02718d8a95b'
PHASES=((0,1),(1,0),(0,-1),(-1,0));PAIRS={'O':(4,0),'N':(2,2),'R':(0,4)}

def planned():
 out=[]
 for stage in ('bare','primary','clock_off'):
  for L in (289,321):
   configs=[(0,['OR','NO']),(0,['NO','OR'])]
   if stage=='primary':configs.extend((d,[pat,pat]) for d,pat in ((-1,'OR'),(-1,'NO'),(1,'OR'),(1,'NO')))
   for phase,(d,patterns) in itertools.product((1,2) if stage=='primary' else (1,),configs):
    name=f'route-clock-L{L}-{stage}-p{phase}-d{d}-'+''.join(patterns)
    out.extend(dict(id=name,stage=stage,side=L,phase=phase,isolated_direction=d,patterns=patterns,source_present=present) for present in (False,True))
 return out

def directions(case):return (case['isolated_direction'],) if case['isolated_direction'] else (-1,1)
def clock_region(case,d,t=0):
 c=case['side']//2;center=(c+8*d,c+1,c);cp=coupling((1,1,1));nodes=(center,*(tuple(center[j]+delta[j] for j in range(3)) for delta in DIRECTIONS));cells={(*n,g):(0,0,2) for n in nodes for g in range(48)};phase=(case['phase']+t)%4 if case['stage']=='primary' else case['phase'];ab=PHASES[phase] if case['stage']=='primary' else (0,0);cells[(*center,2)]=(*ab,0)
 for dd,node in enumerate(nodes[1:]):
  h=next(h for h in range(48) if cp.ports[dd^1][h]==2);cells[(*node,h)]=(0,0,2+2*cp.weights[dd^1][h]*(0,1,1,0)[phase])
 cells[(center[0],center[1]-1,center[2],14)]=(0,0,0)
 return cells

def initial(case):
 L=case['side'];c=L//2;cells={}
 def put(a,v):
  assert a not in cells or cells[a]==v,('initial overlap',a,cells.get(a),v)
  cells[a]=v
 for g,sg in ((0,1),(14,-1)):put((c,c,c,g),(0,sg if case['source_present'] else 0,2))
 for d in directions(case):
  pattern=case['patterns'][0 if d==-1 else 1]
  for j in range(1,9):
   pair=PAIRS[pattern[j-2]] if j in (2,3) else PAIRS['O']
   for g,r in zip((0,14),pair):put((c+j*d,c,c,g),(0,0,r))
  if case['stage']!='bare':
   for a,v in clock_region(case,d).items():put(a,v)
 return Snapshot(L,(0,0,2),cells)

def review():
 from research.clock_selection import route_clock as prod
 p=json.loads(prod.PROTOCOL.read_text());assert file_digest(prod.PROTOCOL)==SHA;assert file_digest(prod.__file__)=='c3b4676d5e9e940888e83c323b425d03352698f7106f0c8ca39c31f58f32b19a';assert file_digest(ROOT/'research/clock_selection/route_clock_budget.py')=='d90584d670064c963a5875cf4b867f5f9b93993a812eeb01f5e532cb3e4cf0eb'
 cases=planned();assert [c for pair in prod.planned_pairs(p) for c in pair]==cases;rows=[];seeds={};cp=coupling((1,1,1))
 for case in cases:
  native=prod.assemble(prod.spec(case,p)).initial;expected=initial(case);assert expected==Snapshot(case['side'],tuple(native.background),{a:tuple(v) for a,v in native.cells.items()});seeds[case['id'],case['source_present']]=expected
  margin=min((min(x,case['side']-1-x) for a,v in expected.cells.items() if any(v[:2]) for x in a[:3]),default=None);assert margin is None or margin>80
  if not case['source_present'] and case['stage']=='primary':
   for d in directions(case):
    for t in range(4):
     before=clock_region(case,d,t);after=clock_region(case,d,t+1)
     for address,v in before.items():
      u=sum(cp.weights[dd][address[3]]*before.get(tuple(address[j]+delta[j] for j in range(3))+(cp.ports[dd][address[3]],),(0,0,2))[1] for dd,delta in enumerate(DIRECTIONS));ell,r=divmod(2*u+v[2],6);assert after[address]==(v[1],ell-v[0],r)
  rows.append(dict(case=case,initial_sha256=native_digest(expected),complete_initial_equal=True,active_margin=margin))
 for off,on in zip(cases[::2],cases[1::2]):
  c=off['side']//2;source_control(seeds[on['id'],True],seeds[off['id'],False],[(c,c,c,g) for g in (0,14)])
 for case in cases:
  if case['stage']!='clock_off':continue
  active=dict(case,stage='primary');other=dict(case,phase=2);assert initial(case)==initial(other);source_control(initial(active),initial(case),[(*[case['side']//2+8*d,case['side']//2+1,case['side']//2],2) for d in directions(case)])
 report=dict(passed=True,new_native_trajectories=0,protocol_sha256=SHA,producer_sha256=file_digest(prod.__file__),wrapper_sha256=file_digest(ROOT/'research/clock_selection/route_clock_budget.py'),auditor_sha256=file_digest(__file__),cases=rows,null_scope='Four exact analytic center/halo phase identities checked without Engine evolution; full null trajectories remain a capture/audit predicate.',budget_review='Dedicated wrapper measures child user/system CPU plus its own process CPU through archive hashing. Child hard/soft limits and reserve are consistent with300CPU; captured native data is saved before observation. Receipt timing is an actual at-receipt measurement, not a promise of successful completion.')
 out=ROOT/'research/clock_selection/evidence/independent_audit/route_clock_preflight.json'
 with out.open('x') as f:json.dump(report,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps(dict(passed=True,complete_initials=len(rows),new_native_trajectories=0)))
if __name__=='__main__':review()

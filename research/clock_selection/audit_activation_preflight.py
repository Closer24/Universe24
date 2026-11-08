"""Independent complete initial construction for resting-clock activation."""
import itertools,json
from pathlib import Path
from research.clock_selection.audit import Snapshot,DIRECTIONS,coupling,file_digest,native_digest,ROOT
from research.clock_selection.audit_two_outlet import packet
SHA='69888ee350bc2d26904cdbdc48711d1c082f5f4cd216c926c3caa167207eff75'

def planned():
 return [dict(id=f'activation-L{L}-rc{rc}-rh{rh}-s{int(present)}',side=L,center_remainder=rc,halo_remainder=rh,source_present=present) for L,rc,rh,present in itertools.product((225,257),(0,2,4),(0,2,4),(False,True))]
def geometry(case):
 c=case['side']//2;center=(c,c+1,c);nodes=(center,*(tuple(center[j]+delta[j] for j in range(3)) for delta in DIRECTIONS));return c,center,nodes

def initial(case):
 L=case['side'];c,center,nodes=geometry(case);cp=coupling((1,1,1));cells={(*n,g):(0,0,2) for n in nodes for g in range(48)};cells[(*center,2)]=(0,0,case['center_remainder'])
 for d,node in enumerate(nodes[1:]):
  g=next(g for g in range(48) if cp.ports[d^1][g]==2);cells[(*node,g)]=(0,0,0 if d==3 else case['halo_remainder'])
 cells[(c,c,c,14)]=(0,0,4)
 def put(a,v):
  assert a not in cells or cells[a]==v,('conflicting static preparation',a)
  cells[a]=v
 for x in range(L):
  if x==c or (case['source_present'] and c-18<=x<c-14):continue
  for g,r in ((0,0),(14,4)):put((x,c,c,g),(0,0,r))
 if case['source_present']:
  for a,v in packet('X',(c-18,c,c)).items():put(a,v)
 return Snapshot(L,(0,0,2),cells)

def check(case):
 on=initial(dict(case,source_present=True));off=initial(dict(case,source_present=False));c,center,nodes=geometry(case);region=[(*n,g) for n in nodes for g in range(48)];allowed=set(packet('X',(c-18,c,c)));diff={a for a in on.cells.keys()|off.cells.keys() if on.at(a)!=off.at(a)}
 def pristine(a):return (0,0,0 if a[1:3]==(c,c) and a[3]==0 else 4 if a[1:3]==(c,c) and a[3]==14 else 2)
 return dict(outside_source_footprint_equal=diff<=allowed,changed_addresses=len(diff),source_absent_pristine=all(off.at(a)==pristine(a) for a in allowed),all336_initial_counter_pairs_zero=all(not any(on.at(a)[:2]) and not any(off.at(a)[:2]) for a in region))

def review():
 from research.clock_selection import activation as prod
 p=json.loads(prod.PROTOCOL.read_text());assert file_digest(prod.PROTOCOL)==SHA;assert file_digest(prod.__file__)=='a1bc69c6b72ccb75a9f92e3f2a155d52104d1ac5b9acdcbc3d19b29cc0d77ec0';assert file_digest(ROOT/'research/clock_selection/activation_budget.py')=='677a22a0f3a93ab127497d42eabde0f6ae91663789461e5b9b968933b6e96046';assert list(prod.cases(p))==planned();rows=[]
 for case in planned():
  expected=initial(case);actual=prod.prepare(case).initial;assert expected==Snapshot(case['side'],tuple(actual.background),{a:tuple(v) for a,v in actual.cells.items()});comparison=check(case);assert comparison==prod.preparation_check(case) and all(v for k,v in comparison.items() if k!='changed_addresses');margin=min((min(q,case['side']-1-q) for a,v in expected.cells.items() if any(v[:2]) for q in a[:3]),default=None);assert margin is None or margin>80
  if not case['source_present']:assert all(not any(v[:2]) for v in expected.cells.values())
  rows.append(dict(case=case,initial_sha256=native_digest(expected),source_check=comparison,strict_margin=margin))
 report=dict(passed=True,new_native_trajectories=0,protocol_sha256=SHA,producer_sha256=file_digest(prod.__file__),wrapper_sha256=file_digest(ROOT/'research/clock_selection/activation_budget.py'),auditor_sha256=file_digest(__file__),cases=rows,retention_review='Complete native captures are saved atomically before decoding/observation; captured-but-unobserved IDs and CPU interruption remain explicit.',predicate_scope='Registered first native center activation plus complete late336-triple quiet orbit, source-off stationarity and full incoming templates; no physical-light inference.')
 out=ROOT/'research/clock_selection/evidence/independent_audit/activation_preflight.json'
 with out.open('x') as f:json.dump(report,f,indent=2,sort_keys=True);f.write('\n')
 print(json.dumps(dict(passed=True,complete_initials=len(rows),new_native_trajectories=0)))
if __name__=='__main__':review()

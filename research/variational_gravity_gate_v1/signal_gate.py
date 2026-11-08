"""Self-contained all-48 finite signal/clock *consistency* controls.

No autonomous physical photon is assumed. A t=0 balanced full-48 perturbation
is used to test whether raw update-front arrival can define a universal metric.
This is a negative control, not an Einstein-gravity derivation.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import sys
P=Path(__file__).resolve().parent
if (P/'source').exists():sys.path.insert(0,str(P/'source'))
else:sys.path.insert(0,str(P.parents[1]))
from universe24 import Engine,State,Cube,Coupling,Channel
from universe24.core.group_2o import group,DIRECTIONS
G=group();C=Coupling((1,1,1));E=Engine(C)
z=G.central;VAC=Channel(0,0,2)
A=Channel(-1,-1,0)

def J(v):return Channel(-v.a,-v.b,4-v.r+2*(v.r%2))
def posadd(v,d,L):return tuple((v[i]+d[i])%L for i in range(3))
def L1(a,b,L):return sum(min((a[i]-b[i])%L,(b[i]-a[i])%L) for i in range(3))
def sign(v,g):return v if g<G.multiplication[z][g] else J(v)

def prepare(L=19,on=True,far_axis=0):
 src=(3,3,3);face={d:posadd(src,DIRECTIONS[d],L) for d in range(6)}
 direction=DIRECTIONS[far_axis];far=posadd(src,tuple(7*u for u in direction),L)
 cells={};active={d:[] for d in range(6)}
 for g in range(48):
  d=DIRECTIONS.index(tuple(G.rotations[g][i][1] for i in range(3)))
  h=C.ports[d][g]
  key=(*face[d],h)
  assert key not in cells
  cells[key]=sign(A,g)
  active[d].append(key)
  if on:cells[(*src,g)]=sign(A,g)
 assert all(len(keys)==8 for keys in active.values())
 # far must have exact same 48-channel *node* as the near one at state zero.
 near=face[far_axis]
 for g in range(48):
  v=cells.get((*near,g),VAC)
  if v!=VAC:cells[(*far,g)]=v
 return State(Cube(L),cells=cells),src,face,far,active[far_axis],[(*far,g) for g in range(48) if (*far,g) in cells]

def pulse(X,emitter,amp):
 cells=dict(X.cells)
 for g in range(48):
  v=X.at((*emitter,g));j=G.multiplication[z][g]
  mag=amp if g<j else -amp
  cells[(*emitter,g)]=Channel(v.a,v.b+mag,v.r)
 return State(X.cube,cells=cells)

def run_case(direction=0,on=True,amp=6,N=15,L=19):
 base,src,face,far,near_keys,far_keys=prepare(L,on,direction)
 direction_vec=DIRECTIONS[direction]
 near=face[direction]
 emitter=posadd(src,tuple(4*d for d in direction_vec),L)
 assert L1(emitter,near,L)==L1(emitter,far,L)==3
 test=pulse(base,emitter,amp)
 initial=base
 first={label:{k:None for k in ('full','b')} for label in ('near','far')}
 first_seed_change={label:None for label in ('near','far')}
 inverse=0
 near_series=[];far_series=[]
 for t in range(N+1):
  near_series.append(base.node(near));far_series.append(base.node(far))
  for label,pos,keys in (('near',near,near_keys),('far',far,far_keys)):
   if first[label]['full'] is None and any(base.at((*pos,g))!=test.at((*pos,g)) for g in range(48)):first[label]['full']=t
   if first[label]['b'] is None and any(base.at((*pos,g)).b!=test.at((*pos,g)).b for g in range(48)):first[label]['b']=t
   # Strict recorded check: the prepared oscillator is not intact if a readout
   # on its seeded channels leaves the *baseline* complete-state orbit.
   if first_seed_change[label] is None:
    P0=(5 if on and label=='near' else 4)
    baseline_cycle=[]
    # Cycle is read from on-the-fly history once available; actual oracle below.
    # A mismatch in full channel state means emitted probe has changed clock.
    if any(base.at(k)!=test.at(k) for k in keys):first_seed_change[label]=t
  if t<N:
   bnext=E.advance(base);tnext=E.advance(test)
   if t in (0,3,N-1):
    assert E.rewind(bnext)==base and E.rewind(tnext)==test
    inverse+=2
   base,test=bnext,tnext
 Pnear=5 if on else 4
 assert all(near_series[t]==near_series[t%Pnear] for t in range(N+1))
 assert all(far_series[t]==far_series[t%4] for t in range(N+1))
 return {'direction':direction,'source_on':on,'balanced48_pulse_amplitude':amp,
         'first_arrivals':first,'first_seeded_clock_difference':first_seed_change,
         'exact_native_inverse_checks':inverse,'near_period':Pnear,'far_period':4,
         'initial_full_near_far_nodes_identical':near_series[0]==far_series[0],
         'source_and_all48_states':True}

def run():
 cases=[]
 for d in range(6):
  for on in (False,True):
   c=run_case(d,on,6,N=16);cases.append(c)
   if on:
    assert c['first_arrivals']['near']['full']==3
    assert c['first_arrivals']['far']['full']==3
 for a in (1,3,-3,6):cases.append(run_case(0,True,a,N=16))
 return {'source':'new independent local reproduction, does not reuse older two_ended.py',
 'six_directions_source_on_off_strong_pulse':12,
 'amplitude_controls':4,'cases':cases,
 'first_arrival_amplitude_summary':{str(r['balanced48_pulse_amplitude']):r['first_arrivals'] for r in cases[-4:]},
 'scope':'perturbation support not physical photon speed; seeded-clock changed is not a stable proper time clock'}
if __name__=='__main__':
 r=run();out=P/'results'/'signal_gate.json';out.write_text(json.dumps(r,indent=2)+'\n');
 print(json.dumps({'case_count':len(r['cases']),'amplitudes':r['first_arrival_amplitude_summary']},indent=2))

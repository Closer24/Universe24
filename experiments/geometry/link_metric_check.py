"""Exact polynomial check and dispersion audit; no source/default edits."""
from pathlib import Path
import sys, json, math, argparse
import numpy as np
from fractions import Fraction
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out',type=Path,default=Path('runs/geometry/link_metric_check.json'))
args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from universe24.core import Tensor,Engine,State,check_reciprocity
from universe24.layers.gravity import lap_potential,gradient_terms,SIX
Q=2**24+1;P=2**12;D=6*Q;w=Q-1;k=Fraction(w,2*P);c2=2*w/D
pot=lap_potential(-k,'F',[('chi',(0,0,0)),('chi',(0,0,0))])
tensor=Tensor(['F','chi'],gradient_terms(pot,what='weak-static canonical KG correction'),Q=Q,strict_support=True)
engine=Engine(tensor,Q);L=4
b=(np.arange(2*L**3).reshape(2,L**3)%37)-18
state=State(L,b-1,b,np.full_like(b,D//2-1))
def lap(x):
 return sum(x[state.lattice.shift_index(d)] for d in SIX)-6*x
u=engine.inputs(state)
expected_F=-int(k)*lap(b[1].astype(object)**2)
expected_chi=-2*int(k)*b[1]*lap(b[0])
assert np.array_equal(u[0],expected_F)
assert np.array_equal(u[1],expected_chi)
assert check_reciprocity(tensor).ok
assert engine.rewind(engine.run(state,20),20).same_as(state)
rows=[]
for U in (1/256,1/64,-1/64):
 N=math.sqrt(1-2*U);C=1-4*U;A=N/math.sqrt(C)
 for magnitude in (.1,.4,.8):
  for direction in ('axis','diagonal'):
   kv=np.array([magnitude,0,0]) if direction=='axis' else np.full(3,magnitude/math.sqrt(3))
   def speed(C):
    omega=math.acos(1-c2*C*sum(1-np.cos(kv)))
    group=c2*C*np.sin(kv)/math.sin(omega)
    return omega,float(np.linalg.norm(group))
   om0,v0=speed(1);om,v=speed(C)
   # Exact analytic slow-clock branch with the public gate's lightest mass.
   mu=2*P
   wc0=math.acos(1-mu/D);wc=math.acos(1-mu*N*N/D)
   raw_clock_ratio=wc/wc0
   relative_speed=(v/v0)/raw_clock_ratio
   rows.append({'U':U,'k':magnitude,'direction':direction,'omega':om,
    'flat_group_speed':v0,'group_speed':v,'group_speed_ratio':v/v0,
    'slow_limit_speed_ratio':math.sqrt(C),'raw_clock_ratio':raw_clock_ratio,
    'speed_per_clock_ratio':relative_speed,'metric_prediction_1_over_A':1/A,
    'relative_metric_error':relative_speed/(1/A)-1})
out={'scope':'Exact correction coefficients plus remainder-free dispersion; group speeds not measured packet arrivals',
 'Q':Q,'P':P,'D':D,'w':w,'c0_squared':c2,
 'correction':{'potential':'-w/(2P) sum F Lap(chi^2)','rank':tensor.rank,
  'support_violations':tensor.support_violations(),'reciprocity':check_reciprocity(tensor).ok,
  'exact_polynomial_equalities':True,'exact_rewind_20':True,'tensor_fingerprint':tensor.fingerprint},
 'dispersion_rows':rows}
args.out.parent.mkdir(parents=True,exist_ok=True)
args.out.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'correction':out['correction'],'U_1over64_rows':[r for r in rows if r['U']==1/64]},indent=2))

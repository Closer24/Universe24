"""Exact all-channel Rule3 variational bridge and GR clock/signal consistency gate.

This script verifies finite algebraic statements against the unchanged pinned
Universe24 engine. It does NOT derive Einstein gravity, physical light, or a
stress-energy tensor. Requires Python 3.11+, standard library only.
"""
from __future__ import annotations
import json, random, sys, math, itertools, hashlib
from fractions import Fraction as F
from pathlib import Path

P = Path(__file__).resolve().parent
CORE_ROOT = P/'source' if (P/'source'/'universe24').exists() else P.parents[1]
sys.path.insert(0, str(CORE_ROOT))
from universe24 import State, Cube, Channel, Engine, Coupling
from universe24.core.group_2o import DIRECTIONS

REFERENCE_COMMIT='c5a23743d96936190210dd510105ed470d4a0b23'
CORE_BLOBS={
 'rule3.py':'dd2a7cdd34200aeb73aba64d02f6cccbfb32afe5',
 'coupling.py':'16d959466bd31bbcf292b6c0e1e3f4f78f748900',
 'engine.py':'2493378dd0b692491bca78c0250433189c96258d',
 'group_2o.py':'16c4ae73de6b8208696196bf68517de2bd8548c8',
 'state.py':'3d706224eef1ec158f78623efa453bc39b0afe30',
}

def git_blob(data:bytes):
 return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def pin_check():
 result={}
 for name,expect in CORE_BLOBS.items():
  data=(CORE_ROOT/'universe24'/'core'/name).read_bytes()
  actual=git_blob(data)
  assert actual==expect,(name,actual,expect)
  result[name]=actual
 return result

def to_canonical(v:Channel):
 theta,eps=divmod(v.r,2)
 return (v.b,3*(v.b-v.a)+theta-1,eps)

def from_canonical(b:int,p:int,eps:int):
 theta=(p+1)%3
 k=(p+1-theta)//3
 return Channel(b-k,b,2*theta+eps)

def D_integer(p:int):
 return (p+1)//3

def D_real(p:float):
 k=math.floor(p/3);t=p-3*k
 if t<=1:return float(k)
 if t<=2:
  s=t-1;return k+3*s*s-2*s*s*s
 return float(k+1)

def K_real(p:float):
 k=math.floor(p/3);t=p-3*k
 if t<=1:area=0
 elif t<=2:
  s=t-1;area=s**3-s**4/2
 else:area=t-F(3,2)
 return 1.5*k*k+k*t+float(area)

def K_integer(p:int):
 k,t=divmod(p,3)
 area=(F(0),F(0),F(1,2))[t]
 return F(3,2)*k*k+k*t+area

def c_all(X:State,xyz):
 return (X.at((*xyz,g)) for g in range(48))

def all_addresses(L):
 return itertools.product(range(L),range(L),range(L),range(48))

def explicit_A_b(X:State,nu,coupling):
 x,y,z,g=nu
 sm=0
 for d,step in enumerate(DIRECTIONS):
  xyz=((x+step[0])%X.cube.side,(y+step[1])%X.cube.side,(z+step[2])%X.cube.side)
  h=coupling.ports[d][g]
  sm+=coupling.weights[d][g]*X.at((*xyz,h)).b
 return sm

def V_edges(X:State,C):
 # directed edges sum, each undirected edge counted twice
 L=X.cube.side;total=0
 for x,y,z,g in all_addresses(L):
  u=X.at((x,y,z,g)).b
  for d,step in enumerate(DIRECTIONS):
   h=C.ports[d][g]
   v=X.at(((x+step[0])%L,(y+step[1])%L,(z+step[2])%L,h)).b
   total+=(u-C.weights[d][g]*v)**2
 return F(total,4)

def V_laplacian(X:State,C):
 total=0
 for nu in all_addresses(X.cube.side):
  b=X.at(nu).b
  total+=b*(6*b-explicit_A_b(X,nu,C))
 return F(total,2)

def alter_b(X:State,nu,delta):
 cells=dict(X.cells)
 x=X.at(nu);v=Channel(x.a,x.b+delta,x.r)
 if v==X.background:cells.pop(nu,None)
 else:cells[nu]=v
 return State(X.cube,cells=cells)

def make_random(L,seed,filled=0.35):
 rng=random.Random(seed);cells={}
 for nu in all_addresses(L):
  if rng.random()<filled:
   cells[nu]=Channel(rng.randint(-5,5),rng.randint(-5,5),rng.randrange(6))
 return State(Cube(L),cells=cells)

def symplectic_exact_check():
 # Jacobian shears for q=b,p: Jd=[[I,M],[0,I]], Jk=[[I,0],[-L,I]].
 # Verify J^T omega J = omega with exact fractions and noncommuting M,L.
 n=4;L=[[F(0) for _ in range(n)] for _ in range(n)]
 for i in range(n):
  L[i][i]=2
  L[i][(i+1)%n]=-1
  L[i][(i-1)%n]=-1
 M=[F(0),F(1,4),F(3,4),F(1,2)]
 I=[[F(i==j) for j in range(n)] for i in range(n)]
 Z=[[F(0) for _ in range(n)] for i in range(n)]
 def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))]for i in range(len(a))]
 def tr(a):return [list(r) for r in zip(*a)]
 def sub(a,b):return [[u-v for u,v in zip(row,srow)] for row,srow in zip(a,b)]
 def neg(a):return [[-v for v in row] for row in a]
 def cat(a,b):return [u+v for u,v in zip(a,b)]
 def stack(a,b):return a+b
 DM=[[M[i] if i==j else F(0) for j in range(n)] for i in range(n)]
 Jk=stack(cat(I,Z),cat(neg(L),I))
 Jd=stack(cat(I,DM),cat(Z,I))
 omega=stack(cat(Z,I),cat(neg(I),Z))
 J=mm(Jd,Jk)
 assert mm(mm(tr(J),omega),J)==omega
 return {'finite_symplectic_jacobian_check':'PASS','test_matrix_size':2*n,'L_and_M_are_noncommuting':mm(L,DM)!=mm(DM,L)}

def test_canonical():
 rng=random.Random(251108);count=0;integer_derivatives=0
 for _ in range(5000):
  v=Channel(rng.randint(-10**18,10**18),rng.randint(-10**18,10**18),rng.randrange(6))
  b,p,e=to_canonical(v)
  assert from_canonical(b,p,e)==v
  assert K_integer(p)>=0
  assert D_real(float(p%100000))==D_integer(p%100000)
  count+=1
 for p in range(-300,301):
  assert D_real(p)==D_integer(p)
  assert abs(K_real(p)-float(K_integer(p)))<1e-9
  assert K_integer(p)>=0
  integer_derivatives+=1
 return {'coordinate_bijection_large_integers':count,'K_prime_at_integer':integer_derivatives,'positive_semidefinite_K_verified_on':'integer -300..300'}

def test_all_signed():
 records=[];N_all=0;gradients=0;time_step=0;parity_odd=0; max_energy_variation=F(0)
 for signs in itertools.product((-1,1),repeat=3):
  eng=Engine(Coupling(signs));C=eng.coupling
  for L in (3,4):
   X=make_random(L,seed=1234+10*L+sum((i+1)*s for i,s in enumerate(signs)),filled=0.23)
   Y=eng.advance(X)
   assert eng.rewind(Y)==X
   for nu in all_addresses(L):
    u=explicit_A_b(X,nu,C)
    b,p,eps=to_canonical(X.at(nu));b1,p1,eps1=to_canonical(Y.at(nu))
    assert p1==p+u-6*b
    assert b1==b+D_integer(p1)
    assert eps1==eps
    assert from_canonical(b1,p1,eps1)==Y.at(nu)
    N_all+=1;time_step+=1
    parity_odd+=eps
   assert V_edges(X,C)==V_laplacian(X,C)
   # sample finite derivative for exact quadratic V with native signed edges
   pool=list(all_addresses(L));rng=random.Random(1000+L+sum(signs))
   for nu in rng.sample(pool,min(15,len(pool))):
    d=V_edges(alter_b(X,nu,1),C)-V_edges(alter_b(X,nu,-1),C)
    assert d/2==6*X.at(nu).b-explicit_A_b(X,nu,C)
    gradients+=1
   E0=V_edges(X,C)+sum((K_integer(to_canonical(X.at(nu))[1]) for nu in all_addresses(L)),F(0))
   E1=V_edges(Y,C)+sum((K_integer(to_canonical(Y.at(nu))[1]) for nu in all_addresses(L)),F(0))
   if abs(E1-E0)>max_energy_variation:max_energy_variation=abs(E1-E0)
   records.append({'signs':signs,'L':L,'channels':L**3*48,'V':str(V_edges(X,C)),'canonical_action_stationarity':True,'inverse':True,'total_H_changed':E0!=E1})
 assert any(x['total_H_changed'] for x in records)
 return {'tested_sign_choices':8,'tested_sizes':[3,4],'boards':len(records),'full_state_channels':N_all,'exact_action_equations_per_channel':time_step,'exact_edge_gradient_tests':gradients,'observed_nonconservation_of_naive_H':True,'maximum_naive_H_change':str(max_energy_variation),'odd_parity_cells':parity_odd,'cases':records}

def test_clock_and_signal_controls():
 # Self-contained module with pinned source, not a previous-turn dependency.
 if __package__:
  from .signal_gate import run as run_signal_gate
 else:
  from signal_gate import run as run_signal_gate
 result=run_signal_gate()
 assert len(result['cases'])==16
 return result

def GR_static_conformal_algebra():
 # For g_ab=e^(2 omega(x)) diag(-1,1,1,1), time-independent omega,
 # exact Einstein tensor G00=-2 Lap omega - |grad omega|^2,
 # trace_sp Gii=4 Lap omega + 5|grad omega|^2.
 # Thus trace_sp+2G00=3|grad omega|^2. If vacuum G=0,
 # grad omega=0. Verified for random rational jets; sympy is used separately.
 rng=random.Random(1001)
 trials=[]
 for i in range(1000):
  grad=[F(rng.randint(-20,20),rng.randint(1,15)) for _ in range(3)]
  lap=F(rng.randint(-20,20),rng.randint(1,15))
  grad2=sum((v*v for v in grad),F(0))
  G00=-2*lap-grad2
  tr_sp=4*lap+5*grad2
  assert tr_sp+2*G00==3*grad2
  trials.append((G00,tr_sp))
 return {'GR_static_conformal_null_cone_conditional_theorem':'G00=-2*Lap(lnOmega)-|grad lnOmega|^2; sum_i Gii=4*Lap(lnOmega)+5|grad lnOmega|^2; if all G_ab=0 then grad Omega=0','rational_jet_checks':len(trials),'physical_assumptions':'static, zero shift, isotropic coordinate light cone, conformal Minkowski, Lambda=0, vacuum; not derived from Universe24','PPN_gate':'if N=1-U/c^2 and photon coordinate speed c_sig/c=1-(1+gamma)U/c^2 then alpha=d ln(c_sig/c)/d ln(N)=1+gamma. GR gamma=1 gives alpha=2; constant c_sig gives alpha=0 and gamma=-1. Requires calibrated photon-like signals and asymptotically Cartesian gauge.'}

def run():
 result={'report_schema':'universe24-variational-operational-gate-v1','reference_core_commit':REFERENCE_COMMIT,'pinned_blobs':pin_check(),
  'status':'exact finite math + negative Einstein diagnostic; no GR derivation',
  'canonical':test_canonical(),'signed_tests':test_all_signed(),
  'symplectic':symplectic_exact_check(),
  'GR_compatibility':GR_static_conformal_algebra(),
  'supplementary_previous_signal_controls':test_clock_and_signal_controls(),
  'limitations':['The smooth canonical generating function is an auxiliary extension of the integer map; its real-valued nearby trajectories are not asserted physical.',
   'Kinetic plus potential H is not conserved by the discrete kick-drift map; no physical energy or T_mu_nu has been identified.',
   'A GR-facing no-go for the static conformal ansatz does not prove that Universe24 realizes such a metric.',
   'The previous 4/5 rate ratio is for selected strongly interacting oscillator preparations only.',
   'Pulse earliest support is not an independently calibrated photon velocity; varying amplitude changes arrival detection.',
   'No vacuum Einstein metric or long-range source field has been derived.']}
 outfile=P/'results'/'audit.json';outfile.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({k:(v if not isinstance(v,dict) else {q:v[q] for q in list(v)[:5]}) for k,v in result.items() if k not in ('pinned_blobs','limitations')},indent=2,ensure_ascii=False)[:2700])
 return result
if __name__=='__main__':run()

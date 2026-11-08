"""Independent matrix-pattern and scalar oracle; no production group or engine imports."""
from itertools import product
from research.reference.algebra import algebra,coupling,DIRECTIONS
from research.component_review.audit import Snapshot


def conjugate_remainder(r):
 assert type(r) is int and 0<=r<6
 return 4-r+2*(r%2)


def pattern(name,x,y,z,g):
 if name=='uniform':return 1
 if name=='period3':return (1,-1,0)[x%3]
 if name=='period4':return (1,0,-1,0)[x%4]
 if name=='internal':return algebra().rotations[g][1][1]
 raise ValueError(name)


def eigenvalue(name):return {'uniform':6,'period3':3,'period4':4,'internal':4}[name]

def side(name):return 4 if name=='period4' else 3

def state(name,a,b,r):
 L=side(name);cells={}
 for x,y,z,g in product(range(L),range(L),range(L),range(48)):
  v=pattern(name,x,y,z,g);triple=(a,b,r) if v==1 else (-a,-b,conjugate_remainder(r)) if v==-1 else (0,0,2)
  if triple!=(0,0,2):cells[(x,y,z,g)]=triple
 return Snapshot(L,(0,0,2),cells)


def step(triple,lam):
 a,b,r=triple;ell,s=divmod(2*lam*b+r,6)
 return (b,ell-a,s),ell


def orbit(name,a,b,r,H):
 triples=[(a,b,r)];quotients=[]
 for _ in range(H):
  nxt,ell=step(triples[-1],eigenvalue(name));triples.append(nxt);quotients.append(ell)
 return triples,quotients


def operator_checks():
 rows=[];cp=coupling((1,1,1))
 for name in ('uniform','period3','period4','internal'):
  L=side(name);counts={-1:0,0:0,1:0}
  for x,y,z,g in product(range(L),range(L),range(L),range(48)):
   v=pattern(name,x,y,z,g);counts[v]+=1;actual=sum(cp.weights[d][g]*pattern(name,(x+delta[0])%L,(y+delta[1])%L,(z+delta[2])%L,cp.ports[d][g]) for d,delta in enumerate(DIRECTIONS));assert actual==eigenvalue(name)*v
  rows.append(dict(pattern=name,side=L,full_addresses=48*L**3,eigenvalue=eigenvalue(name),coefficient_counts={str(k):v for k,v in counts.items()},operator_equality=True))
 v=[algebra().rotations[g][1][1] for g in range(48)];cp=coupling((1,-1,1));assert all(sum(cp.weights[d][g]*v[cp.ports[d][g]] for d in range(6))==0 for g in range(48));return rows,dict(signs=[1,-1,1],pattern='R_yy',eigenvalue=0,nonzero_channels=16,zero_channels=32,scope='Exact operator check only; no signed native trajectories in this batch.')


def internal_operator_family_checks():
 rows=[];rot=algebra().rotations
 for signs in product((-1,1),repeat=3):
  cp=coupling(signs)
  for body_axis,world_axis in product(range(3),repeat=2):
   v=[r[world_axis][body_axis] for r in rot];lam=2*signs[0]+(2*signs[1] if body_axis==1 else 0)+(2*signs[2] if body_axis==2 else 0)
   assert all(sum(cp.weights[d][g]*v[cp.ports[d][g]] for d in range(6))==lam*v[g] for g in range(48));assert v.count(1)==v.count(-1)==8 and v.count(0)==32
   rows.append(dict(signs=list(signs),body_axis=body_axis,world_axis=world_axis,eigenvalue=lam,operator_equality=True))
 return rows

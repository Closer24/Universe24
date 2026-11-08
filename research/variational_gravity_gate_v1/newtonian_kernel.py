"""Optional numpy Fourier audit of the exact all-48 scalar Poisson operator.

The inverse of a linear operator is NOT asserted to be an actual self-sustained
Rule3 gravitational source. This file is a mathematical Newtonian-limit test.
"""
from __future__ import annotations
import json,sys,math
from pathlib import Path
P=Path(__file__).resolve().parent
if (P/'source').exists():sys.path.insert(0,str(P/'source'))
else:sys.path.insert(0,str(P.parents[1]))
from universe24 import State,Cube,Channel,Engine,Coupling
from universe24.core.group_2o import group,DIRECTIONS
import numpy as np

G=group();C=Coupling((1,1,1));E=Engine(C)

def all48_scalar_check(L=4):
 rng=np.random.default_rng(1945)
 B=rng.integers(-5,6,size=(L,L,L),dtype=np.int64)
 cells={}
 for xyz in np.ndindex((L,L,L)):
  for g in range(48):
   b=int(B[xyz]);v=Channel(0,b,2)
   if v!=Channel(0,0,2):cells[(*xyz,g)]=v
 X=State(Cube(L),cells=cells)
 z=np.zeros_like(B)
 for axis in range(3):z+=np.roll(B,-1,axis)+np.roll(B,1,axis)
 checked=0
 for xyz in np.ndindex((L,L,L)):
  for g in range(48):
   u=sum(C.weights[d][g]*X.at((*tuple((xyz[i]+DIRECTIONS[d][i])%L for i in range(3)),C.ports[d][g])).b for d in range(6))
   assert u==int(z[xyz]);checked+=1
 return {'L':L,'all48_channel_input_equal_scalar_stencil':True,'checked_receiver_channels':checked}

def fourier_G(L):
 grid=np.fft.fftfreq(L)*2*np.pi
 kx,ky,kz=np.meshgrid(grid,grid,grid,indexing='ij')
 lap=6-2*(np.cos(kx)+np.cos(ky)+np.cos(kz))
 recip=np.zeros_like(lap)
 mask=lap>1e-10
 recip[mask]=1/lap[mask]
 field=np.fft.ifftn(recip).real
 residual=6*field
 for ax in range(3):residual-=np.roll(field,1,ax)+np.roll(field,-1,ax)
 ideal=np.full((L,L,L),-1/L**3,dtype=float);ideal[(0,0,0)]+=1
 err=float(np.max(np.abs(residual-ideal)))
 assert err<3e-12
 data=[]
 for r in (2,3,4,5,6,8,10,12,16):
  if r>L/3:continue
  raw=float(field[(r,0,0)])
  rawxy=float(field[(r,r,0)])
  distxy=math.sqrt(2)*r
  data.append({'r':r,'axis_G':raw,'r_G':r*raw,'diag_G':rawxy,'diag_distance':distxy,'diag_rG':distxy*rawxy})
 # Fit G(r)=a*(1/r)+b on axial samples 5<=r<=L/8 to isolate finite torus zero-mode shift
 sample=[(1/r,float(field[(r,0,0)])) for r in range(5,round(L/8)+1)]
 if len(sample)>2:
  x=np.array([p[0] for p in sample]);y=np.array([p[1] for p in sample]);a,b=np.polyfit(x,y,1)
  slope=float(a);constant=float(b)
 else:slope=constant=None
 return {'L':L,'Laplacian_G_equals_delta_minus_uniform_exact_fourier_error':err,
         'zero_mean':float(field.mean()),'G0':float(field[0,0,0]),
         'point_samples':data,'fit_a_over_r_plus_b':{'a':slope,'b':constant,'continuum_expected_a':1/(4*np.pi),'relative_a_error':(slope*4*np.pi-1) if slope is not None else None},
         'important':'This is the inverse linear spatial Laplacian only; no physical source, clock, or Einstein metric was generated.'}

def run():
 checked=all48_scalar_check(L=4)
 rows=[fourier_G(L) for L in (64,96,128)]
 r={'exact_stencil':checked,'periodic_green':rows,
 'analytic_infinite_volume':'G(x)=(2pi)^-3 integral exp(i k.x)/(6-2 sum_i cos ki) dk, G(r)=1/(4 pi r)+O(r^-3) along large-r directions',
 'science_scope':'necessary Newtonian operator substrate; no autonomous mass source or 1/r Rule3 solution established'}
 (P/'results'/'newtonian_kernel.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({'exact':checked,'fit':[(a['L'],a['fit_a_over_r_plus_b']) for a in rows],'max_errors':[a['Laplacian_G_equals_delta_minus_uniform_exact_fourier_error'] for a in rows]},indent=2))
 return r
if __name__=='__main__':run()

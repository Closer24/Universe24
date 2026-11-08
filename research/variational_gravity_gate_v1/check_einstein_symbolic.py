"""Optional independent SymPy 4D curvature check, not a Universe24 simulation.

For g=exp(2 omega(z)) * diag(-1,1,1,1), calculate exact Ricci and
Einstein tensors and compare against the asserted conformal formulas.
"""
from pathlib import Path
import json
import sympy as s
T,X,Y,Z=s.symbols('t x y z',real=True)
coords=(T,X,Y,Z)
om=s.Function('omega')(Z)
scale=s.exp(2*om)
g=s.diag(-scale,scale,scale,scale)
ginv=g.inv()
N=4
Gamma=[[[s.simplify(s.Rational(1,2)*sum(ginv[a,j]*(s.diff(g[j,b],coords[c])+s.diff(g[j,c],coords[b])-s.diff(g[b,c],coords[j])) for j in range(N)))for c in range(N)]for b in range(N)]for a in range(N)]
R=[[s.simplify(sum(s.diff(Gamma[a][b][c],coords[a])-s.diff(Gamma[a][b][a],coords[c])+sum(Gamma[a][a][j]*Gamma[j][b][c]-Gamma[a][c][j]*Gamma[j][b][a] for j in range(N)) for a in range(N))) for c in range(N)]for b in range(N)]
scalar=s.simplify(sum(ginv[a,a]*R[a][a] for a in range(N)))
E=[[s.simplify(R[a][b]-s.Rational(1,2)*g[a,b]*scalar)for b in range(N)]for a in range(N)]
res={
 'G00':str(E[0][0]),'G11':str(E[1][1]),'G22':str(E[2][2]),'G33':str(E[3][3]),
 'Ricci_scalar':str(scalar),
 'proof_of_static_vacuum_obstruction':'G11+G22+G33+2 G00 =3(omega_z)^2; vacuum => omega_z=0',
 'SymPy_version':s.__version__}
w=s.diff(om,Z);h=s.diff(om,Z,2)
assert s.simplify(E[0][0]-(-2*h-w*w))==0
assert s.simplify(E[1][1]-(2*h+w*w))==0
assert s.simplify(E[2][2]-(2*h+w*w))==0
assert s.simplify(E[3][3]-3*w*w)==0
assert s.simplify(E[1][1]+E[2][2]+E[3][3]+2*E[0][0]-3*w*w)==0
assert s.simplify(scalar+6*s.exp(-2*om)*(h+w*w))==0
p=Path(__file__).parent/'results'/'einstein_symbolic.json';p.write_text(json.dumps(res,indent=2,ensure_ascii=False)+'\n');print(json.dumps(res,indent=2))

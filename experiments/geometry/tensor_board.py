"""Passive exact tensor readout for the declared pp-wave chart, not a new engine.

python experiments/geometry/tensor_board.py --out runs/geometry/tensor_board
Requires the n=2 vacuum and electrovac histories described in the two experiment docs.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import argparse
from fractions import Fraction as Q
import hashlib
import json
import numpy as np
from universe24.core.lattice import lattice

PAIRS=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
LABELS=('u','v','x','y')


def point(A=0,B=0,E1=0,E2=0,x=0,y=0,trace_override=None):
    """All covariant tensors from a plane-wave metric and an independent F.

    Exact Fractions. The curvature rule is separately checked against all 256
    components obtained by differentiating the metric in the symbolic test.
    A trace override is for the deliberately incorrect-metric control only.
    """
    A,B,E1,E2,x,y=map(Q,(A,B,E1,E2,x,y))
    rho=E1*E1+E2*E2
    C=-rho/2 if trace_override is None else Q(trace_override)
    H=(A+C)*x*x+2*B*x*y+(-A+C)*y*y
    g=[[Q(0) for _ in range(4)] for __ in range(4)]
    g[0][0]=H;g[0][1]=g[1][0]=Q(-1);g[2][2]=g[3][3]=Q(1)
    inverse=[[Q(0) for _ in range(4)] for __ in range(4)]
    inverse[1][1]=-H;inverse[0][1]=inverse[1][0]=Q(-1);inverse[2][2]=inverse[3][3]=Q(1)
    R={}
    K=((-A-C,-B),(-B,A-C))
    for i in range(2):
        for j in range(2):
            for a,b,sign1 in ((0,i+2,1),(i+2,0,-1)):
                for c,d,sign2 in ((0,j+2,1),(j+2,0,-1)):
                    R[a,b,c,d]=sign1*sign2*K[i][j]
    ricci=[[Q(0) for _ in range(4)] for __ in range(4)]
    for (a,b,c,d),value in R.items():ricci[b][d]+=inverse[a][c]*value
    scalar=sum(inverse[a][b]*ricci[a][b] for a in range(4) for b in range(4))
    G=[[ricci[a][b]-g[a][b]*scalar/2 for b in range(4)] for a in range(4)]
    F=[[Q(0) for _ in range(4)] for __ in range(4)]
    F[0][2]=E1;F[2][0]=-E1;F[0][3]=E2;F[3][0]=-E2
    active=[(a,b,F[a][b]) for a in range(4) for b in range(4) if F[a][b]]
    stress=[[Q(0) for _ in range(4)] for __ in range(4)]
    invariant=Q(0)
    for a,c,v1 in active:
        for b,d,v2 in active:
            stress[a][b]+=v1*inverse[c][d]*v2
            invariant+=v1*inverse[a][b]*inverse[c][d]*v2
    for a in range(4):
        for b in range(4):stress[a][b]-=g[a][b]*invariant/4
    residual=[[G[a][b]-stress[a][b] for b in range(4)] for a in range(4)]
    W={}
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    W[a,b,c,d]=R.get((a,b,c,d),Q(0))-(g[a][c]*ricci[b][d]-g[a][d]*ricci[b][c]-g[b][c]*ricci[a][d]+g[b][d]*ricci[a][c])/2+scalar*(g[a][c]*g[b][d]-g[a][d]*g[b][c])/6
    return dict(metric=g,inverse=inverse,riemann=R,ricci=ricci,scalar=scalar,
                einstein=G,stress=stress,maxwell=F,weyl=W,residual=residual,
                fields=dict(A=A,B=B,E1=E1,E2=E2,C=C,rho=rho,H=H))


def bivector(tensor):
    """Exact 6x6 representation; antisymmetry recovers all 256 entries."""
    return [[tensor.get((a,b,c,d),Q(0)) for c,d in PAIRS] for a,b in PAIRS]


def encode(value):
    if isinstance(value,Q):return str(value)
    if isinstance(value,dict):return {k:encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [encode(v) for v in value]
    return value


def from_snapshot(snapshot,P,coordinates,L,sector):
    i,j,k=coordinates
    node=lattice(L).index(i,j,k)
    p,q=Q(int(snapshot[1,0,node]),P),Q(int(snapshot[1,2,node]),P)
    x=Q(3*(2*i-(L-1)),L);y=Q(3*(2*j-(L-1)),L)
    fields=dict(A=p,B=q) if sector=='vacuum' else dict(E1=p,E2=q)
    return point(**fields,x=x,y=y)


def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    definitions=[('vacuum','גל כבידה בריק','pp_wave/mixed_n2.npz',16384,'vacuum'),
                 ('linear','קרינה קווית','electrovac/linear_n2_sign1_amp1.npz',512,'electrovac'),
                 ('circular','קרינה מעגלית','electrovac/circular_n2_sign1_amp1.npz',512,'electrovac'),
                 ('flat','שטוח','electrovac/flat_n2_sign1_amp1.npz',512,'electrovac')]
    cases=[]; checked=0;source_hashes={}
    for key,name,path,P,sector in definitions:
        full=ROOT/'runs/geometry'/path;source_hashes[path]=hashlib.sha256(full.read_bytes()).hexdigest()
        with np.load(full,allow_pickle=False) as trace:
            states=trace['states'];profile=trace['profile'];L=6;n=2
            assert states.shape[0]==13 and states.shape[-1]==L**3
            phases=[]
            for tick,snapshot in enumerate(states):
                rows=[]
                for z in range(L):
                    base=from_snapshot(snapshot,P,(0,0,z),L,sector)
                    for x in range(L):
                        for y in range(L):
                            sample=from_snapshot(snapshot,P,(x,y,z),L,sector)
                            assert all(v==0 for row in sample['residual'] for v in row)
                            assert sample['scalar']==0
                            checked+=1
                    node=lattice(L).index(0,0,z)
                    raw=[[int(snapshot[field,gear,node]) for gear in range(4)] for field in range(3)]
                    fields={k:v for k,v in base['fields'].items() if k!='H'}
                    rows.append(encode(dict(fields=fields,raw=raw,ricci=base['ricci'],einstein=base['einstein'],
                        stress=base['stress'],maxwell=base['maxwell'],residual=base['residual'],
                        riemann=bivector(base['riemann']),weyl=bivector(base['weyl']),scalar=base['scalar'])))
                phases.append(rows)
            cases.append(dict(key=key,name=name,sector=sector,P=P,L=L,n=n,steps=12,phases=phases))
    # A bad metric must fail the observer; T is not set equal to G.
    bad=point(E1=Q(1,8),trace_override=0)
    assert bad['residual'][0][0]==-Q(1,64)
    result=dict(schema='tensor-board-v1',coordinates=list(LABELS),bivectors=['uv','ux','uy','vx','vy','xy'],
        cases=cases,audit=dict(exact_node_time_checks=checked,all_16_residuals_zero=True,
        flat_metric_nonzero_field_control='-1/64',arithmetic='Exact rational readout from stored integer fields'),
        chart=dict(x='3*(2*i-(L-1))/L',y='3*(2*j-(L-1))/L',u='(tick+2*k)/n',
        interpretation='Declared local Brinkmann chart samples; computational lattice slice is not an established physical simultaneous slice.'),
        source_hashes=source_hashes,
        limitations=['All tensor components of these chosen plane-wave metrics, not all solutions of general relativity.',
        'Readout only: no new metric dynamics, probe backreaction, or operational clock calibration.'])
    (out/'board.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n')
    (out/'audit.json').write_text(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result['audit']))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'runs/geometry/tensor_board')
    run(parser.parse_args().out)

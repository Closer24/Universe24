"""Exact two-sublattice restriction of the unsourced even-cube metric stencil.

This is a passive research experiment, not a default or engine change.
Run from a checkout:
  python experiments/geometry/carry_locked_metric.py --steps 1000000
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from universe24.core import Engine,State
from universe24.core.tensor import compose
from universe24.layers.gravity import build_metric

Q=2**33+1
D=6*Q
w=Q-1


def forward(state):
    a,b,r=state
    inputs=(6*b[0]+6*w*b[1],6*b[1]+6*w*b[0])
    qr=[divmod(2*u+z,D) for u,z in zip(inputs,r)]
    return (b,(qr[0][0]-a[0],qr[1][0]-a[1]),(qr[0][1],qr[1][1]))


def backward(state):
    newa,newb,newr=state
    b=newa
    inputs=(6*b[0]+6*w*b[1],6*b[1]+6*w*b[0])
    r=tuple((rp-2*u)%D for rp,u in zip(newr,inputs))
    a=tuple((2*u+z-rp)//D-bp for u,z,rp,bp in zip(inputs,r,newr,newb))
    return (a,b,r)


def state_hash(state):
    return hashlib.sha256(json.dumps(state,separators=(',',':')).encode()).hexdigest()


def run(steps):
    if type(steps) is not int or steps < 1:
        raise ValueError('steps must be a positive integer')
    # All sites of a parity have identical values; each has six opposite-parity
    # neighbors. Hence this reduction is an invariant subspace of every even L.
    tensor=compose(build_metric(Q=Q,components=('h00',)))
    engine=Engine(tensor,Q)
    cases=[]
    for amplitude,velocity in ((512,0),(18345,0),(289784,0),(512,1)):
        seed=((-amplitude+velocity,amplitude-velocity),(amplitude,-amplitude),(D//2-1,D//2-1))
        parity=np.asarray([(-1)**sum(x) for x in np.ndindex(4,4,4)],dtype=object)
        arrays=[np.asarray([[v[0] if p==1 else v[1] for p in parity]],dtype=object) for v in seed]
        actual=State(4,*arrays)
        actual_seed=actual.copy()
        reduced=seed
        for _ in range(32):
            actual=engine.step(actual);reduced=forward(reduced)
            for field,v in zip(('a','b','r'),reduced):
                expected=np.asarray([[v[0] if p==1 else v[1] for p in parity]],dtype=object)
                assert np.array_equal(getattr(actual,field),expected)
        for _ in range(32):actual=engine.inverse_step(actual)
        assert all(np.array_equal(getattr(actual,k),getattr(actual_seed,k)) for k in ('a','b','r'))
        state=seed;peak=amplitude;min_abs=amplitude;samples=[]
        r0=D//2-1
        # This is a sufficient interval, not a claim of indefinite linear growth.
        guaranteed_through=None if velocity==0 else 2*((r0-24*amplitude)//(24*velocity))+1
        formula_verified_steps=0
        for t in range(1,steps+1):
            state=forward(state)
            peak=max(peak,abs(state[1][0]));min_abs=min(min_abs,abs(state[1][0]))
            assert state[1][0]+state[1][1]==0
            if guaranteed_through is None or t<=guaranteed_through:
                expected_b=(-1)**t*(amplitude+velocity*t)
                expected_r=r0-12*velocity*t if t%2==0 else r0+24*amplitude+12*velocity*(t-1)
                assert state[1]==(expected_b,-expected_b)
                assert state[2]==(expected_r,2*r0-expected_r)
                formula_verified_steps+=1
            if t%max(1,steps//100)==0 or t==steps:
                samples.append(dict(step=t,demodulated_corner=(-1)**t*state[1][0]))
        final=state
        for _ in range(steps):state=backward(state)
        assert state==seed
        cases.append(dict(amplitude=amplitude,initial_velocity_parameter=velocity,
                          seed=seed,final=final,steps=steps,exact_rewind=True,
                          seed_sha256=state_hash(seed),final_sha256=state_hash(final),
                          formula_verified_steps=formula_verified_steps,
                          proved_linear_formula_through=guaranteed_through,
                          min_abs_corner=min_abs,peak_abs_corner=peak,
                          engine_prefix_steps=32,engine_prefix_exact=True,
                          engine_prefix_inverse_exact=True,samples=samples))
    result=dict(schema='free-corner-control-v1',Q=Q,D=D,w=w,
                beta=-D+12,even_cube=True,
                scope='Exact parity-uniform restriction of free scalar metric stencil, no sources or portals. Finite horizon, not all-time boundedness proof.',
                cases=cases)
    result['tensor_fingerprint']=tensor.fingerprint
    result['implementation_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['reproduction']='python experiments/geometry/carry_locked_metric.py --steps 1000000'
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--steps',type=int,default=1_000_000)
    parser.add_argument('--out',type=Path,default=ROOT/'runs/carry-locked-metric/report.json')
    args=parser.parse_args()
    result=run(args.steps)
    path=args.out
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([dict(amplitude=c['amplitude'],velocity=c['initial_velocity_parameter'],peak=c['peak_abs_corner'],steps=c['steps'],exact_rewind=c['exact_rewind']) for c in result['cases']],indent=2))


if __name__=='__main__':main()

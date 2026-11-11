"""Export exact fixed-six tensor, seed, state and official-event fixtures.

These fixtures describe the current law. They replace no historical acceptance
record and assert no quantum or gravitational interpretation.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.core.lattice import DIRECTIONS, ZERO
from universe24.demos.reference_model.run_reference import build
from universe24.observe.reference_model import state_hash


def fixture(name, tensor, initial, steps):
    engine = Engine(tensor)
    state = initial
    indices = np.arange(tensor.G)
    hashes, clicks = [state_hash(state, indices)], []
    for step in range(1, steps+1):
        following = engine.step(state)
        clicks.append(engine.clicks(state, following, step).select('official').rows())
        hashes.append(state_hash(following, indices))
        state = following
    return dict(name=name,D=6,L=initial.L,steps=steps,tensor=tensor.to_dict(),
                dynamics_fingerprint=tensor.dynamics_fingerprint,
                initial=initial.to_dict(),final=state.to_dict(),
                state_sha256_per_update=hashes,official_clicks_per_update=clicks,
                state_hash_format='universe24-state-values-v2',
                click_row_format=['step','xyz','gear_index','kind','quotient','label'],
                rewind_returns_initial=engine.rewind(state,steps).same_as(initial))


def main(out_dir):
    out_dir=Path(out_dir)
    out_dir.mkdir(parents=True,exist_ok=True)
    _,reference,_,seed,_=build(3,'pulse',13)
    wave=Tensor(['wave'],[('wave',1,(('wave',d,'b'),)) for d in DIRECTIONS])
    rng=np.random.default_rng(47)
    a=rng.integers(-4,5,size=(1,27));b=rng.integers(-4,5,size=(1,27))
    r=rng.integers(0,6,size=(1,27))
    bigint=Tensor(['counter'],[('counter',3,(('counter',ZERO,'b'),))])
    amplitude=1<<80
    huge=State(3,[[0]*27],[[amplitude]*27],[[0]*27])
    jobs=[('reference_pulse',reference,seed,20),
          ('scalar_wave_random',wave,State(3,a,b,r),12),
          ('bigint_periodic_clock',bigint,huge,12)]
    index=[]
    for name,tensor,state,steps in jobs:
        data=fixture(name,tensor,state,steps)
        path=out_dir/(name+'.json')
        path.write_text(json.dumps(data,separators=(',',':'))+'\n')
        index.append(dict(file=path.name,G=tensor.G,steps=steps,
                          final_hash=data['state_sha256_per_update'][-1],
                          exact_rewind=data['rewind_returns_initial']))
    report=dict(D=6,fixtures=index)
    (out_dir/'INDEX.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    target=Path(sys.argv[1]) if len(sys.argv)>1 else Path('runs/fixed-six-fixtures')
    print(json.dumps(main(target),indent=2))

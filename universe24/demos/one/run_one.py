"""Run Universe24, the fixed-divisor-six model with a complete seed and passive records.

Every forward update is Engine.step. A resource gate may stop the run after a
complete step; it never modifies state. Previous field/cosmic presets are not
inherited by this new construction.
"""
from __future__ import annotations

import argparse
import gzip
import json
import math
from pathlib import Path
import time

import numpy as np

from ...core import Engine
from ...core.tensor import compose
from ...layers.one import one_system
from ...observe.one import state_hash
from ...prepare.one import one_seed


def forward(engine, state, steps):
    for tick in range(1, steps + 1):
        state = engine.step(state)
        yield tick, state


def build(L, bang="pulse", rng_seed=13, system_kw=None):
    system = one_system(**(system_kw or {}))
    tensor = compose(*system.blocks)
    engine = Engine(tensor)
    seed, preparation = one_seed(system, tensor, L, bang=bang, rng_seed=rng_seed)
    return system, tensor, engine, seed, preparation


def run(args):
    if args.tmax < 1 or not math.isfinite(args.budget) or args.budget <= 0 or args.max_bits < 1:
        raise ValueError("positive horizon, finite wall budget and bit limit required")
    system, tensor, engine, seed, preparation = build(args.L, args.bang, args.rng)
    rows, events, hashes = [], [], []
    state, completed = seed, 0
    peak_bits = seed.max_abs().bit_length()
    indices = np.arange(tensor.G)
    initial_hash = state_hash(seed, indices)
    start = time.monotonic()
    stop = "initial_counter_bit_limit" if peak_bits > args.max_bits else "requested_horizon"
    if stop == "requested_horizon":
        for tick, following in forward(engine, seed, args.tmax):
            completed = tick
            log = engine.clicks(state, following, tick).select("official")
            ell = following.b.astype(object) + state.a.astype(object)
            if not np.array_equal(6*ell, 2*engine.inputs(state)+state.r-following.r):
                raise AssertionError("integer division ledger failed")
            digest = state_hash(following, indices)
            bits = following.max_abs().bit_length()
            peak_bits = max(peak_bits, bits)
            rows.append(dict(step=tick, official_records=len(log),
                             signed_quotient_sum=sum(map(int, log.quotient)),
                             counter_bits=bits, state_hash=digest))
            events.extend(log.rows())
            hashes.append([tick,digest])
            state = following
            if bits > args.max_bits:
                stop = "counter_bit_limit"
                break
            if time.monotonic()-start >= args.budget:
                stop = "forward_wall_budget"
                break
    elapsed = time.monotonic()-start
    rewind = None
    if args.rewind:
        rewind = dict(exact=engine.rewind(state,completed).same_as(seed), updates=completed)
        if not rewind["exact"]:
            raise AssertionError("complete seed was not recovered")
    return dict(meta=dict(project="Universe24",tag=args.tag,model="fixed-divisor-six reference construction",D=6,
                    L=args.L,G=tensor.G,rank=tensor.rank,monomials=len(tensor.monomials),
                    designations=len(tensor.designations),fingerprint=tensor.fingerprint,
                    dynamics_fingerprint=tensor.dynamics_fingerprint,
                    initial_state_hash=initial_hash,state_hash_format="universe24-state-values-v2",
                    seed=preparation),
                t_end=completed, requested_steps=args.tmax, stop_reason=stop,
                wall_forward_s=elapsed, maximum_counter_bits=peak_bits,rewind=rewind,
                final_state_hash=state_hash(state,indices), engine_stats=dict(engine.stats),
                rows=rows,hashes=hashes,_events=events,
                physics_status="No quantum, gravitational, particle or cosmological claim follows from this run.")


def compare(left,right):
    for key in ("fingerprint","state_hash_format"):
        if not left.get("meta",{}).get(key) or left["meta"][key] != right.get("meta",{}).get(key):
            raise ValueError("comparison requires the same law and state hash format")
    count = min(len(left["hashes"]),len(right["hashes"]))
    return dict(updates_compared=count,identical_updates=sum(
        left["hashes"][i] == right["hashes"][i] for i in range(count)))


def main(argv=None):
    parser=argparse.ArgumentParser(prog="universe24", description=__doc__)
    parser.add_argument("--L",type=int,default=3)
    parser.add_argument("--bang",choices=("pulse","standing","none"),default="pulse",
                        help="initial preparation; this name does not assert a cosmological bang")
    parser.add_argument("--rng",type=int,default=13)
    parser.add_argument("--tmax",type=int,default=20)
    parser.add_argument("--budget",type=float,default=120)
    parser.add_argument("--max-bits",type=int,default=256)
    parser.add_argument("--tag",default="demo")
    parser.add_argument("--out",required=True)
    parser.add_argument("--rewind",action="store_true")
    parser.add_argument("--compare")
    args=parser.parse_args(argv)
    result=run(args)
    directory=Path(args.out)
    directory.mkdir(parents=True,exist_ok=True)
    events=result.pop("_events")
    if args.compare:
        result["comparison"]=compare(json.loads(Path(args.compare).read_text()),result)
    with gzip.open(directory/(args.tag+"_events.json.gz"),"wt") as handle:
        json.dump(events,handle)
    (directory/(args.tag+".json")).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({key:result[key] for key in ("t_end","stop_reason","maximum_counter_bits","rewind")},indent=2))
    return result


if __name__ == "__main__":
    main()

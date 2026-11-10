"""M1: the c2 instability mechanism map (MECHANISM test: prescribed STATIC links; not shipped). Exact integers.

A prescribed static ZQ8 link field is realised by link gears whose input is u = D W only (so a = b = W never
changes) and by c2's terms INTO L0, designated one-way ("prescribed static link, mechanism test only"); the links do
not feel the reference (no reaction), which is exactly what a prescribed field is. Run from the repository root:
    OMP_NUM_THREADS=1 nice -n 10 python -m universe24.demos.gauge.c2_mechanism
Writes demos/gauge/M1_mechanism.json.
"""
from __future__ import annotations

import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ...core.engine import Engine, State
from ...core.lattice import lattice
from ...core.reciprocity import check_reciprocity
from ...core.tensor import Block, compose
from ...layers.links import Q8_ORDER, build_c2
from ...layers.reference import build_reference
from ...prepare import vacuum_state

HERE = Path(__file__).resolve().parent
WHY = "prescribed static link field (MECHANISM test M1 only; not shipped): the link does not react"


def static_link_block(Q: int) -> Block:
    full = build_c2(Q=Q, kappa=Q, lam=0)
    terms = []
    for t in full.terms:
        target, coeff, factors = t[0], t[1], t[2]
        if target.startswith("ref."):
            terms.append((target, coeff, factors, {"designated_one_way": WHY}))
        elif len(factors) == 1:                      # u_W = D W (free zero mode): the link stays static
            terms.append((target, coeff, factors))
    return Block(full.gears, tuple(terms), name="c2s", vacuum=dict(full.vacuum),
                 params={**full.params, "static": True}, doc="M1 prescribed static ZQ8 links", Q=Q)


def bits(arr) -> int:
    return max((abs(int(v)).bit_length() for v in np.asarray(arr).ravel()), default=0)


def run(Q, L, links: dict, steps=1000, cap=64, seed=8):
    ref = build_reference(Q=Q)
    st = static_link_block(Q)
    T = compose(ref, st, q_lattice=("ref.*",))
    E = Engine(T, Q)
    lat = lattice(L)
    s = vacuum_state(T, Q, L, ref, st)
    a, b, r = s.a.astype(object), s.b.astype(object), s.r.astype(object)
    rng = random.Random(seed)
    for g in range(48):
        i = T.gear_index(f"ref.R{g:02d}")
        for n in range(lat.N):
            if rng.random() < 0.1:
                a[i, n] = rng.randint(-3, 3)
                b[i, n] = rng.randint(-3, 3)
                r[i, n] = Q * rng.randrange(6)
    for (xyz, axis), U in links.items():
        n = lat.index(*xyz)
        for c, q in enumerate(Q8_ORDER):
            gname = f"c2s.W{'xyz'[axis]}_{q.replace('-', 'm')}"
            w = U.get(q, 0) - (1 if q == "1" else 0)
            a[T.gear_index(gname), n] = w
            b[T.gear_index(gname), n] = w
    s = State(L, a, b, r)
    rr = [T.gear_index(f"ref.R{g:02d}") for g in range(48)]
    lr = [i for i, nm in enumerate(T.names) if nm.startswith("c2s.")]
    w0 = s.b[lr].copy()
    hist_bits = []
    hit = None
    for t in range(steps):
        s = E.step(s)
        bb = bits(s.b[rr])
        if t < 10 or t % 25 == 24:
            hist_bits.append((t + 1, bb))
        if bb > cap:
            hit = t + 1
            break
    static_ok = bool(np.array_equal(s.b[lr], w0))
    return {"blow_up_at(>%d bits)" % cap: hit, "max_ref_bits_final": bits(s.b[rr]), "links_stayed_static": static_ok,
            "bits_series": hist_bits}


def main():
    Q, L = 4095, 4
    x0 = ((1, 1, 1), 0)
    unitary = {
        "vacuum [1] (frozen board)": {},
        "[i]": {x0: {"i": 1}},
        "[-1]": {x0: {"-1": 1}},
        "-[1]": {x0: {"1": -1}},
        "holonomy set i,j,k,-1": {x0: {"i": 1}, ((2, 1, 1), 1): {"j": 1}, ((1, 2, 1), 0): {"k": 1},
                                  ((1, 1, 2), 2): {"-1": 1}},
        "cut 0": {x0: {}},
    }
    nonunitary = {
        "[1]+[i]": {x0: {"1": 1, "i": 1}},
        "[1]+[-1]": {x0: {"1": 1, "-1": 1}},
        "[1]-[-1]": {x0: {"1": 1, "-1": -1}},
        "2[1]": {x0: {"1": 2}},
        "3[1]": {x0: {"1": 3}},
    }
    out = {"unitary": {}, "nonunitary": {}}
    blk = static_link_block(Q)
    rep = check_reciprocity(compose(build_reference(Q=Q), blk, q_lattice=("ref.*",)))
    out["reciprocity_with_designation"] = {"ok": rep.ok, "designated": len(rep.designated)}
    t0 = time.time()
    for name, cfg in unitary.items():
        out["unitary"][name] = run(Q, L, cfg)
    for name, cfg in nonunitary.items():
        out["nonunitary"][name] = run(Q, L, cfg)
    frozen = out["unitary"]["vacuum [1] (frozen board)"]["max_ref_bits_final"]
    out["verdict"] = {
        "frozen_final_bits": frozen,
        "unitary_bounded": all(v["blow_up_at(>64 bits)"] is None and v["max_ref_bits_final"] <= frozen + 3
                               for v in out["unitary"].values()),
        "nonunitary_blow_up_times": {k: v["blow_up_at(>64 bits)"] for k, v in out["nonunitary"].items()}}
    out["stamp_utc"] = datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")
    out["seconds"] = round(time.time() - t0, 1)
    (HERE / "M1_mechanism.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps(out["verdict"]), out["reciprocity_with_designation"], out["seconds"])
    for grp in ("unitary", "nonunitary"):
        for k, v in out[grp].items():
            print(grp, k, {kk: vv for kk, vv in v.items() if kk != "bits_series"}, v["bits_series"][-3:])


if __name__ == "__main__":
    main()

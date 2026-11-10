"""RUN Z (pre-registered in NOTES_system.md, PRE-REGISTRATION v2 DEFAULT): c2 as ZQ8 with one OD4 spring per simple
component (layers/c2_zq8.py) on the package, fine links under l0_offset = Q - 1, handed class (1,-1,1) vs +++.

Run from the repository root:
    OMP_NUM_THREADS=1 nice -n 10 python -m universe24.demos.system.zq8_c2 ARM SIGNS [T] [seeds]
ARM: A (today's L0, weight Q, kappa A = Q, A = 20857) | B (form-C L0, weight Q - 1, A = 2^14) | B2 (A = 2^15,
exploratory addendum). SIGNS: ppp | pmp.
"""
from __future__ import annotations

import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ...core.engine import OBJ, Engine, State
from ...core.reversors import uniform
from ...core.tensor import compose
from ...layers.c2_zq8 import CHARACTERS, H_PAIRS, build_c2_zq8
from ...layers.gravity_l0c import build_l0c
from ...layers.reference import build_reference
from ...layers.system import with_vacuum
from ...observe.gauge import C2View

OUT = Path(__file__).resolve().parents[2] / "results" / "system"
Q = (1 << 33) + 1
L = 4
LAM = 2                      # T2 (C2-TUNE final, manager 13:01); RUN Z itself ran lam = 4
RUNAWAY_BITS = 40
SIGNS = {"ppp": (1, 1, 1), "pmp": (1, -1, 1)}


def stamp():
    return datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")


def build(arm: str, bs):
    if arm == "A":
        A = 20857
        ref = with_vacuum(build_reference(Q=Q, body_signs=bs, name="ref"), 3 * Q - 1, {"l0_offset": Q - 1})
        c2 = build_c2_zq8(Q=Q, kappa=Q // A, lam=LAM, body_signs=bs, port_weight=Q, name="c2")
    else:
        A = 1 << 15 if arm == "B2" else 1 << 14
        ref = build_l0c(Q=Q, body_signs=bs, name="ref")
        c2 = build_c2_zq8(Q=Q, kappa=(Q - 1) // A, lam=LAM, body_signs=bs, port_weight=Q - 1, name="c2")
    T = compose(ref, c2)
    return A, ref, c2, T


def initial(T, E, A, seed):
    vac = E.vacuum(L, {n: 3 * Q - 1 for n in T.names})
    rng = random.Random(seed)
    amp = A // 128
    a, b = vac.a.astype(OBJ), vac.b.astype(OBJ)
    for i, n in enumerate(T.names):
        if n.startswith("ref."):
            for x in range(vac.N):
                a[i, x] = rng.randint(-amp, amp)
                b[i, x] = rng.randint(-amp, amp)
    return vac, State(L, a, b, vac.r.astype(OBJ)), amp


def _ratio(x: int, y: int) -> float:
    x = int(x)
    return x / y if x.bit_length() < 900 else float("inf")


def readout(T, s, A, amp):
    b = s.b.astype(OBJ)
    out = {}
    rows = {k: [T.gear_index(f"c2.W{'xyz'[k]}_{c}") for c in ("1", "i", "j", "k", "m1", "mi", "mj", "mk")]
            for k in range(3)}
    wmax = 0
    comp = {n: 0.0 for n in CHARACTERS}
    comp["H"] = 0.0
    udef = {n: 0.0 for n in CHARACTERS}
    for k in range(3):
        W = [b[r] for r in rows[k]]
        wmax = max(wmax, max(int(abs(v)) for w in W for v in w))
        for n, sig in CHARACTERS.items():
            chi = sum(sg * w for sg, w in zip(sig, W))
            comp[n] = max(comp[n], _ratio(max(abs(int(v)) for v in chi), A))
            udef[n] = max(udef[n], _ratio(max(abs(abs(int(v) + A) - A) for v in chi), A))   # ||chi(U)| - A| / A
        h2 = sum((W[p] + (A if p == 0 else 0) - W[m]) ** 2 for p, m in H_PAIRS)
        hm = max(int(v) for v in h2)
        comp["H"] = max(comp["H"], float("inf") if hm.bit_length() > 1800 else
                        max(abs(float(np.sqrt(float(v))) - A) for v in h2) / A)
    refrows = [i for i, n in enumerate(T.names) if n.startswith("ref.")]
    out["max_W_over_A"] = _ratio(wmax, A)
    out["max_component_dev_over_A"] = {k: round(v, 6) for k, v in comp.items()}      # eps: |chi(W)|/A (from [1])
    out["eps_unitarity_defect"] = {k: round(v, 6) for k, v in udef.items()}          # ||chi(U)| - A|/A
    out["max_L0_b_over_amp"] = _ratio(max(int(abs(v)) for r in refrows for v in b[r]), amp)
    out["max_bits"] = int(s.max_abs()).bit_length()
    return out


def exactness(T, E, A, s0):
    res = {}
    h = E.run(s0, 20)
    res["rewind20"] = E.rewind(h, 20).same_as(s0)
    X = uniform(T, Q, "Mp")
    res["Mp_mirror_n6"] = X(E.run(X(E.run(s0, 6)), 6)).same_as(s0)
    V = C2View(T, {"algebra": "ZQ8", "Q": Q, "ref": "ref", "A": A}, "c2")
    rng = random.Random(5)
    kf = [rng.choice(V.Q8) for _ in range(s0.N)]
    lhs = E.run(V.gauge_map_zq8(s0, kf), 10)
    rhs = V.gauge_map_zq8(E.run(s0, 10), kf)
    res["local_Q8_covariance_10"] = lhs.same_as(rhs)
    return res


def run(arm: str, signs: str, Tmax: int = 10000, seeds=(1, 2, 3)) -> dict:
    bs = SIGNS[signs]
    A, ref, c2, T = build(arm, bs)
    E = Engine(T, Q)
    res = {"arm": arm, "body_signs": bs, "Q": Q, "L": L, "lam": LAM, "A": A, "kappa": c2.params["kappa"],
           "port_weight": c2.params["port_weight"], "stiffness_over_D": c2.params["stiffness_over_D"],
           "monomials": len(T), "runs": {}}
    vac, s0, amp = initial(T, E, A, seeds[0])
    res["vacuum_fixed_20"] = E.run(vac, 20).same_as(vac)
    res["exactness"] = exactness(T, E, A, s0)
    for sd in seeds:
        t0 = time.time()
        _, s, amp = initial(T, E, A, sd)
        samples = [{"t": 0, **readout(T, s, A, amp)}]
        status, t_run = "BOUNDED", None
        for t in range(1, Tmax + 1):
            s = E.step(s)
            big = int(s.max_abs())                       # every update: the cubic spring's runaway is doubly exponential
            if big.bit_length() > RUNAWAY_BITS:
                status, t_run = "RUNAWAY", t
                samples.append({"t": t, **readout(T, s, A, amp)})
                break
            if t % 10 == 0:
                wr = readout(T, s, A, amp) if t % 500 == 0 else None
                if wr and wr["max_W_over_A"] > 4:
                    status, t_run = "RUNAWAY", t
                    samples.append({"t": t, **readout(T, s, A, amp)})
                    break
                if wr is None and t % 100 == 0:
                    w = readout(T, s, A, amp)
                    if w["max_W_over_A"] > 4:
                        status, t_run = "RUNAWAY", t
                        samples.append({"t": t, **w})
                        break
                if wr:
                    samples.append({"t": t, **wr})
                    print(arm, signs, sd, t, wr["max_W_over_A"], wr["max_L0_b_over_amp"], round(time.time() - t0, 1),
                          flush=True)
        res["runs"][sd] = {"status": status, "t_runaway": t_run, "amp": amp, "seconds": round(time.time() - t0, 1),
                           "engine_stats": dict(E.stats), "samples": samples,
                           "worst": {"max_W_over_A": max(x["max_W_over_A"] for x in samples),
                                     "max_L0_b_over_amp": max(x["max_L0_b_over_amp"] for x in samples)}}
        print(arm, signs, sd, status, t_run, flush=True)
    res["stamp_utc"] = stamp()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"Z_{arm}_{signs}.json").write_text(json.dumps(res, indent=1, default=str))
    return res


if __name__ == "__main__":
    arm, signs = sys.argv[1], sys.argv[2]
    Tmax = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
    seeds = tuple(int(x) for x in sys.argv[4].split(",")) if len(sys.argv) > 4 else (1, 2, 3)
    run(arm, signs, Tmax, seeds)

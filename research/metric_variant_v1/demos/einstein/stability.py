"""E4 T8 (Study 28, pre-registered in s28/EINF-A_NOTES.md §2): stability and exact reversibility of ONE + EINSTEIN.

The composed tensor einstein_system(one_system(), on=True) is run with the ONE seed (prepare/one.one_seed, J-pure bang, data
only) by Engine.step ONLY; the same seed is run on the base (einstein OFF) for comparison. Read-only readouts every update:
max bits of the state, the uniform means of metric.h00 (F), a1, a2, a3 (U units: /2P) and the max |a_g|. Finally the whole
run is REWOUND (audit map) and compared bit for bit with the seed. Criteria (pre-registered): bounded (max bits <= 60) for
>= 300 updates; rewind exact; the uniform-mode drift of a2, a3 is REPORTED (expected ~ t^2 from a sign-definite source).
Usage (mirror only): python -m research.metric_variant_v1.demos.einstein.stability OUT.json [L] [T] [jpure|s2star|jpure+l0]
       [A_l0] [default|v1|coupled]
"jpure+l0": the J-pure ONE seed PLUS an L0 lump (seed data, amplitude A_l0 = 2^11 so that the closed-board uniform lapse
drift stays small over 600 updates at L = 6), to exercise einL0 / einbeta inside ONE.
Also reported: the max |b| of L0 (ref.*) - with the J-pure bang L0 stays dark (exactly 0), so einL0 is idle there.
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np

from ...core.engine import Engine
from ...core.tensor import compose
from ...layers.einstein import einstein_system
from ...layers.one import one_system
from ...prepare.one import one_seed


def _mean(s, T, nm):
    return float(np.mean(s.b[T.gear_index(nm)].astype(float)))


def _add_l0_lump(s0, T, L, A, Q, sigma=1.5, rng_seed=3):
    """SEED DATA ONLY: add an L0 lump (Gaussian envelope x a fixed random 48-vector, a = b) at the centre, so that the
    Einstein L0 blocks are exercised inside ONE (the ONE bangs leave L0 exactly dark)."""
    from ...core.engine import State
    rng = np.random.default_rng(rng_seed)
    v = rng.normal(size=48)
    v /= np.sqrt((v * v).sum())
    c = L // 2
    xs = np.arange(L)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    env = np.exp(-((X - c) ** 2 + (Y - c) ** 2 + (Z - c) ** 2) / (2.0 * sigma ** 2)).ravel()
    a, b, r = s0.a.astype(object).copy(), s0.b.astype(object).copy(), s0.r.astype(object).copy()
    for i in range(48):
        g = T.gear_index(f"ref.R{i:02d}")
        val = np.array([int(x) for x in np.rint(A * v[i] * env)], dtype=object)
        b[g] = b[g] + val
        a[g] = a[g] + val
    return State(L, a, b, r)


def run(L: int = 4, T_steps: int = 400, bang: str = "jpure", A_l0: int = 1 << 11, base_kind: str = "default"):
    """base_kind: "default" (whatever one_system() returns), "v1" (couple_doublet=False) or "coupled" (couple_doublet=True)."""
    out = {"L": L, "T": T_steps, "bang": bang, "A_l0": A_l0 if bang.endswith("+l0") else None, "base_kind": base_kind}
    base = {"default": lambda: one_system(), "v1": lambda: one_system(couple_doublet=False),
            "coupled": lambda: one_system(couple_doublet=True)}[base_kind]()
    for label, S in (("einstein_on", einstein_system(base, on=True)), ("base_off", base)):
        T = compose(*S.blocks)
        E = Engine(T, S.Q)
        s0, rep = one_seed(S, T, L, bang=bang.split("+")[0])
        if bang.endswith("+l0"):
            s0 = _add_l0_lump(s0, T, L, A_l0, S.Q)
        P = S.info["P"]
        s = s0
        bits, Fm, a1m, a2m, a3m, amax, l0max = [], [], [], [], [], [], []
        l0 = [T.gear_index(f"ref.R{i:02d}") for i in range(48)]
        names = T.names
        t0 = time.time()
        for t in range(1, T_steps + 1):
            s = E.step(s)
            bits.append(s.max_abs().bit_length())
            Fm.append(_mean(s, T, "metric.h00") / (2 * P))
            l0max.append(int(np.max(np.abs(s.b[l0].astype(object)))))
            if label == "einstein_on":
                a1m.append(_mean(s, T, "metric.a1") / (2 * P))
                a2m.append(_mean(s, T, "metric.a2") / (2 * P))
                a3m.append(_mean(s, T, "metric.a3") / (2 * P))
                amax.append(max(int(np.max(np.abs(s.b[T.gear_index(f"metric.{g}")].astype(object))))
                                for g in ("a1", "a2", "a3")))
            if bits[-1] > 200:
                break
        sec = time.time() - t0
        back = E.rewind(s, len(bits))
        res = {"fingerprint": T.dynamics_fingerprint, "monomials": len(T.monomials), "rank": T.rank,
               "updates": len(bits), "max_bits": max(bits), "bits_every_50": bits[::50] + [bits[-1]],
               "U_mean_F_every_50": Fm[::50] + [Fm[-1]], "seconds": round(sec, 1),
               "max_abs_L0_every_50": l0max[::50] + [l0max[-1]],
               "rewind_exact": bool(back.same_as(s0)), "int64_steps": E.stats["int64_steps"],
               "pyint_steps": E.stats["pyint_steps"]}
        if a1m:
            res.update({"U_mean_a1_every_50": a1m[::50] + [a1m[-1]], "U_mean_a2_every_50": a2m[::50] + [a2m[-1]],
                        "U_mean_a3_every_50": a3m[::50] + [a3m[-1]], "max_abs_a_every_50": amax[::50] + [amax[-1]]})
        out[label] = res
    on = out["einstein_on"]
    out["verdict"] = {"bounded_max_bits_le_60_for_ge_300": on["updates"] >= min(300, T_steps) and on["max_bits"] <= 60,
                      "rewind_exact": on["rewind_exact"] and out["base_off"]["rewind_exact"]}
    return out


if __name__ == "__main__":
    path = sys.argv[1]
    L = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    Tn = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    bang = sys.argv[4] if len(sys.argv) > 4 else "jpure"
    A_l0 = int(sys.argv[5]) if len(sys.argv) > 5 else 1 << 11
    base_kind = sys.argv[6] if len(sys.argv) > 6 else "default"
    res = run(L, Tn, bang, A_l0, base_kind)
    with open(path, "w") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res["verdict"]), res["einstein_on"]["max_bits"], res["einstein_on"]["seconds"])

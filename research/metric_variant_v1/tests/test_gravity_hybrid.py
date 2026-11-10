"""HYBRID gravity source tests H1 (exactness) and H2 (reversor), pre-registered in NOTES_gravity_hybrid.md.
Run: OMP_NUM_THREADS=1 nice -n 19 python -m unittest research.metric_variant_v1.tests.test_gravity_hybrid -v
Writes results/gravity_hybrid/H1.json and H2.json. H2 is a REPORT (its pre-registered prediction is FAIL); the unittest
asserts only the exactness items and that the reversor outcome was recorded."""
from __future__ import annotations

import json
import random
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ..core.engine import OBJ, Engine, State
from ..core.tensor import compose
from ..layers.gravity_hybrid import HYB_ACT_WHY, HYB_WHY, apply_hybrid, build_hybrid_source

HANDS_OFF = {"chiral": False, "electroweak": False}   # the hands-OFF v2 default (R1): the system Study 10 analysed
from ..layers.system import default_system
from ..observe.seed import r_star
from ..prepare.gravity_hybrid import hybrid_source_total, with_hybrid_datum
from ..prepare.seed import l0_dark_seed, l0_rstar_vector, m0_band_vector, s2_star
from ..prepare.system import system_vacuum

OUT = Path(__file__).resolve().parent.parent / "results" / "gravity_hybrid"
X0, A_SEED = (2, 2, 2), 1 << 12


def stamp():
    return datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")


def designated_count(T, why=None):
    if why is None:
        return len(T.designations)
    return sum(1 for v in T.designations.values() if why in v)


def h1() -> dict:
    t0 = time.time()
    S0 = default_system(**HANDS_OFF)
    H = apply_hybrid(S0)
    Q = H.Q
    T = compose(*H.blocks)
    T0 = compose(*S0.blocks)
    hs = H.by_name("hsrc")
    out = {"stamp_start": stamp(), "Q": Q, "G": T.G}
    # (a)-(c)
    deg = max(m.degree for m in T.monomials)
    hs_mons = [m for m in T.monomials if T.names[m.target] == "metric.h00" and m.degree == 2 and
               any(T.names[f.gear].split(".")[0] in ("ref", "matter") for f in m.factors)]
    out["a_integers_compose_ok"] = True
    out["b_designations"] = {"composed_total": designated_count(T), "default_total": designated_count(T0),
                             "hsrc_HYB_WHY": designated_count(T, HYB_WHY[:40]),
                             "lapse_action_HYB_ACT_WHY": designated_count(T, HYB_ACT_WHY[:40]),
                             "hsrc_block_terms": len(hs.terms)}
    out["c_rank_max_degree_plus_1"] = deg + 1
    out["c_hsrc_monomials"] = {"n": len(hs_mons), "degrees": sorted({m.degree for m in hs_mons}),
                               "a_reads": sum(1 for m in hs_mons if any(f.field == "a" for f in m.factors)),
                               "max_offset_norm": max(sum(abs(c) for c in f.offset) for m in hs_mons for f in m.factors)}
    out["c_inverse_stages"] = [len(s) for s in T.stages]
    # (d) vacuum: (i) hsrc alone with its inputs, (ii) composed
    L = 3
    alone_blocks = [H.by_name("ref"), H.by_name("matter"), H.by_name("metric"), hs]
    Ta = compose(*alone_blocks)
    Ea = Engine(Ta, Q)
    from ..prepare import vacuum_state
    va = vacuum_state(Ta, Q, L, *alone_blocks)
    s = va
    for _ in range(20):
        s = Ea.step(s)
    out["d_vacuum_alone_20"] = s.same_as(va)
    E = Engine(T, Q)
    vac = system_vacuum(H, T, L)
    s = vac
    for _ in range(20):
        s = E.step(s)
    out["d_vacuum_composed_20"] = s.same_as(vac)
    # (e) rewind of a random small state
    rng = random.Random(11)
    a, b = vac.a.astype(OBJ).copy(), vac.b.astype(OBJ).copy()
    for i, nm in enumerate(T.names):
        ns = nm.split(".")[0]
        amp = (1 << 10) if ns == "matter" else (20 if ns == "ref" else 0)
        if amp:
            a[i] = [rng.randint(-amp, amp) for _ in range(vac.N)]
            b[i] = [rng.randint(-amp, amp) for _ in range(vac.N)]
    s0 = State(L, a, b, vac.r)
    s = s0
    for _ in range(20):
        s = E.step(s)
    for _ in range(20):
        s = E.inverse_step(s)
    out["e_rewind_20_20"] = s.same_as(s0)
    out["datum_check_total"] = hybrid_source_total(s0, T, Q)
    out["seconds"] = round(time.time() - t0, 1)
    out["stamp_end"] = stamp()
    return out


def seeds(S, T, vac):
    bs = S.info["body_signs"]
    c_link = (2 * X0[0], 2 * X0[1] + 1, 2 * X0[2])
    c_node = tuple(2 * x for x in X0)
    vb = None
    for band in range(9):
        try:
            vb = l0_rstar_vector(bs, m0_band_vector(bs, band, 64))
            break
        except (ValueError, IndexError):
            continue
    return {"S2*": (s2_star(vac, T, X0, A_SEED), c_link),
            "L0_rstar_e0": (l0_dark_seed(vac, T, X0, A_SEED, v=l0_rstar_vector(bs)), c_node),
            "L0_rstar_band": (l0_dark_seed(vac, T, X0, 1, v=vb), c_node)}


def bounce(S, L=6, tmax=6) -> dict:
    T = compose(*S.blocks)
    Q = S.Q
    E = Engine(T, Q)
    vac = system_vacuum(S, T, L)
    off, bs = S.info["l0_offset"], S.info["body_signs"]
    res = {}
    for name, (s0, c2) in seeds(S, T, vac).items():
        row = {"R*_fixed": r_star(s0, T, Q, c2, l0_offset=off, body_signs=bs).same_as(s0), "per_t": []}
        fwd, bwd = s0, s0
        for t in range(1, tmax + 1):
            fwd, bwd = E.step(fwd), E.inverse_step(bwd)
            img = r_star(fwd, T, Q, c2, l0_offset=off, body_signs=bs)
            ok = bwd.same_as(img)
            mism = {}
            if not ok:
                for arr in ("a", "b", "r"):
                    d = np.asarray(getattr(bwd, arr), dtype=object) != np.asarray(getattr(img, arr), dtype=object)
                    for g in np.flatnonzero(d.any(axis=1)):
                        nm = T.names[g]
                        mism[nm] = mism.get(nm, 0) + int(d[g].sum())
            row["per_t"].append({"t": t, "exact": ok, "n_mismatch": sum(mism.values()),
                                 "mismatch_gears": dict(sorted(mism.items(), key=lambda kv: -kv[1])[:8])})
        res[name] = row
    return res


def h2() -> dict:
    t0 = time.time()
    out = {"stamp_start": stamp()}
    out["control_default"] = bounce(default_system(**HANDS_OFF))
    out["hybrid"] = bounce(apply_hybrid(default_system(**HANDS_OFF)))
    out["seconds"] = round(time.time() - t0, 1)
    out["stamp_end"] = stamp()
    return out


class TestGravityHybrid(unittest.TestCase):
    def test_h1_exactness(self):
        r = h1()
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "H1.json").write_text(json.dumps(r, indent=1, default=str))
        self.assertTrue(r["d_vacuum_alone_20"])
        self.assertTrue(r["d_vacuum_composed_20"])
        self.assertTrue(r["e_rewind_20_20"])
        self.assertLessEqual(r["c_rank_max_degree_plus_1"], 4)
        self.assertEqual(r["c_hsrc_monomials"]["degrees"], [2])
        self.assertLessEqual(r["c_hsrc_monomials"]["max_offset_norm"], 1)

    def test_h2_reversor_report(self):
        r = h2()
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "H2.json").write_text(json.dumps(r, indent=1, default=str))
        # control: the plain v2 default must keep its exact bounce (= SD6)
        for name, row in r["control_default"].items():
            self.assertTrue(all(x["exact"] for x in row["per_t"]), name)
        self.assertIn("hybrid", r)


if __name__ == "__main__":
    unittest.main()

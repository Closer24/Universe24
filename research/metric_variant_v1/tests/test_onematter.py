"""ONE-MATTER option (A) tests O1-O5 (pre-registered in NOTES_system.md, 10:48:34 UTC; re-run at the v2 Q = 2^33 + 1 with
A = 2^16, kd = hop/A = 2^15, kw = wilson/A = 2^14, mass = MASS_DEFAULT: "PRE-REGISTRATION v2 DEFAULT").
Writes results/system/O*.json.
Run: OMP_NUM_THREADS=1 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_onematter -v"""
from __future__ import annotations

import json
import random
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ..core.engine import OBJ, Engine, State
from ..core.reciprocity import check_reciprocity
from ..core.reversors import GearwiseMap, GroupLinearMap, uniform
from ..core.tensor import compose
from ..layers.onematter import build_one_matter, link_names, matter_gears
from ..observe.audit import frozen_equivalence
from ..observe.onematter import OneMatterView, random_unit
from ..prepare import vacuum_state
from ..layers.system import HOP, MASS_DEFAULT, Q_DEFAULT, WILSON

OUT = Path(__file__).resolve().parent.parent / "results" / "system"
Q = Q_DEFAULT
A = 1 << 16                      # B1-GAUGE default_regime(2^33 + 1)
KD, KW = HOP // A, WILSON // A   # 2^15, 2^14
L = 3


def write(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    data = {**data, "stamp_utc": datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")}
    (OUT / f"{name}.json").write_text(json.dumps(data, indent=1, default=str))


def random_state(T, om, seed, matter_amp=64, link_noise=8):
    rng = random.Random(seed)
    s = vacuum_state(T, Q, L, *om.blocks)
    a, b, r = s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ)
    N = L ** 3
    for i, nm in enumerate(T.names):
        amp = matter_amp if nm.startswith("q") else link_noise
        a[i] = [rng.randint(-amp, amp) for _ in range(N)]
        b[i] = [rng.randint(-amp, amp) for _ in range(N)]
        r[i] = [rng.randrange(6 * Q) for _ in range(N)]
    return State(L, a, b, r)


def kramers(T):
    """K o M' on the 48 matter gears (K = 1_2 (x) R_j (x) 1_2 per pair), M' on Re W, JM on Im W."""
    from ..layers.matter import K16
    from ..layers.matter import matter_names
    Km = [[int(v) for v in row] for row in K16]
    maps = None
    for ns in ("q0", "q1", "q2"):
        names = [f"{ns}.{n}" for n in matter_names("pair")]
        Kmap = GroupLinearMap(T, Q, names, Km, neg_r="Mp", name=f"K_{ns}")
        maps = Kmap if maps is None else Kmap @ maps
    choices = {}
    for nm in T.names:
        if nm.startswith("q"):
            choices[nm] = "Mp"
        elif nm.startswith("u6."):
            choices[nm] = "JM" if nm.endswith("i") else "Mp"
    G = GearwiseMap(T, Q, choices)
    N = GearwiseMap(T, Q, {nm: "Jp" for nm in T.names if nm.startswith("q")})
    return maps @ G, N


class OneMatterTests(unittest.TestCase):
    def test_O1_to_O5(self):
        t0 = time.time()
        out = {}
        for lam, spring in ((0, "frobenius"), (4, "matrix")):
            om = build_one_matter(Q=Q, lam=lam, spring=spring, A=A, kd=KD, kw=KW, mass=MASS_DEFAULT)
            T = compose(*om.blocks)
            rep = check_reciprocity(T)
            cen = T.census()
            out[f"O1_lam{lam}_{spring}"] = {"Q": T.Q, "G": T.G, "monomials": len(T), "rank": T.rank, "reciprocal": rep.ok,
                                   "designated": len(rep.designated), "b_only": T.b_only, "constants": T.has_constant,
                                   "by_degree": cen["by_degree"], "support_violations": len(T.support_violations())}
            self.assertTrue(rep.ok and T.Q == Q and T.b_only and not T.has_constant)
        om = build_one_matter(Q=Q, lam=4, spring="matrix", A=A, kd=KD, kw=KW, mass=MASS_DEFAULT)
        T = compose(*om.blocks)
        E = Engine(T, Q)
        vac = vacuum_state(T, Q, L, *om.blocks)
        out["O2_vacuum_fixed_20"] = E.run(vac, 20).same_as(vac)
        base_T = compose(*om.blocks[:3])
        rng = random.Random(5)
        N = L ** 3
        ba = np.array([[rng.randint(-1000, 1000) for _ in range(N)] for _ in range(base_T.G)], dtype=OBJ)
        bb = np.array([[rng.randint(-1000, 1000) for _ in range(N)] for _ in range(base_T.G)], dtype=OBJ)
        br = np.array([[rng.randrange(6 * Q) for _ in range(N)] for _ in range(base_T.G)], dtype=OBJ)
        out["O2_frozen"] = frozen_equivalence(om.blocks[:3], om.blocks[3:], Q, State(L, ba, bb, br), 20)
        # O3 Noether for the 14 listed generators
        V = OneMatterView(T, Q, A)
        s0 = random_state(T, om, 11)
        n = 8
        hist = E.run(s0, n, history=True)
        g = V.gauss_check(hist)
        out["O3_noether"] = {**g, "generators": [l for l, _ in V.alg.generators]}
        self.assertEqual(g["failures"], 0)
        # matter-only vs total colour / isospin / EM over the run (flow into the links)
        flows = {}
        for lab, X in V.alg.generators:
            mat = [int(sum(V.charge(h, X, "matter"))) for h in hist[1:]]
            tot = [int(sum(V.charge(h, X, "all"))) for h in hist[1:]]
            sc = max(1, max(abs(v) for v in mat))
            flows[lab] = {"matter_swing": (max(mat) - min(mat)) / sc, "total_drift": (max(tot) - min(tot)) / sc}
        out["O3_flows"] = flows
        # O4 covariance (integer subgroups): monomial U(6) units and product units
        cov = {}
        FT = hist[-1]
        for kind in ("u6", "product"):
            rr = random.Random(7)
            gf = [random_unit(rr, kind) for _ in range(N)]
            lhs = E.run(V.gauge_map(s0, gf), n)
            rhs = V.gauge_map(FT, gf)
            cov[kind] = lhs.same_as(rhs)
            self.assertTrue(cov[kind])
        out["O4_covariance"] = cov
        # O5 rewind + mirrors
        out["O5_rewind"] = E.rewind(FT, n).same_as(s0)
        Mp = uniform(T, Q, "Mp")
        out["O5_plain_Mp"] = Mp(E.run(Mp(FT), n)).same_as(s0)
        X, Nc = kramers(T)
        out["O5_kramers_XFXF_eq_N"] = X(E.run(X(E.run(s0, n)), n)).same_as(Nc(s0))
        out["O5_vacuum_fixed_by_Mp_and_X"] = [Mp(vac).same_as(vac), X(vac).same_as(vac)]
        self.assertTrue(out["O5_rewind"] and out["O5_plain_Mp"] and out["O5_kramers_XFXF_eq_N"])
        out["seconds"] = round(time.time() - t0, 1)
        write("O1-O5_onematter_Q2p33", out)


if __name__ == "__main__":
    unittest.main()

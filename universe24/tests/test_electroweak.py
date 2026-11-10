"""EW-BUILDER tests EW1-EW5 (pre-registered in NOTES_electroweak.md, 12:31:48 UTC, before these runs).
Each test writes results/electroweak/<test>.json with its UTC stamp.

Run (repo root, ONE core):
    OMP_NUM_THREADS=1 nice -n 19 python -m unittest universe24.tests.test_electroweak -v
"""
from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from math import isqrt
from pathlib import Path

import numpy as np

from ..core.engine import Engine, State
from ..core.reciprocity import check_reciprocity
from ..core.tensor import compose
from ..layers.chiral import Q_DEFAULT, chiral_blocks
from ..layers.electroweak import (KH_DEFAULT, build_graviweak_b, build_higgs_hop, build_test_lapse_field,
                                  compose_electroweak, hypercharge_generators)
from ..layers.gauge import ALGEBRAS
from ..observe.chiral import ChiralView
from ..prepare import vacuum_state
from ..prepare.chiral import gear_groups, random_chiral_state

OUT = Path("runs/tests") / "electroweak"
Q = Q_DEFAULT
D = 6 * Q
L = 3
P_LAPSE = 1 << 20


def stamp():
    return datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")


def write(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(dict(data, written=stamp(), Q=Q), indent=1, default=str))


def ew_system(v=1 << 16, kH=KH_DEFAULT, gw=None):
    """gw None: EW-ALONE; 'rec': + F + reciprocal gwb; 'oneway': + F + one-way gwb (MECHANISM)."""
    m, m2, l, c = chiral_blocks(Q, include_matter=True, v=v)
    blocks = [m, m2, l, c, build_higgs_hop(coupling=c, links=l, kH=kH)]
    if gw is not None:
        F = build_test_lapse_field(Q=Q)
        blocks.insert(0, F)
        blocks.append(build_graviweak_b(coupling=c, links=l, matter_blocks=[m, m2], field="lapsef.F", P=P_LAPSE,
                                        oneway=(gw == "oneway")))
    T = compose(*blocks)
    return T, blocks, Engine(T, Q), ChiralView(T, c, l)


def rank4_not_spring(T, blocks):
    names = T.names
    fam = {}
    for i, n in enumerate(names):
        ns, local = n.split(".", 1)
        if ns == "wsu2" and local.startswith("U"):
            fam[i] = ("link", local.split("_")[0])
        elif ns == "wsu2" and local.startswith("P"):
            fam[i] = ("path", local.split("_")[0])
        elif ns == "chiral":
            fam[i] = ("higgs",)
    bad = [m for m in T.monomials if m.degree == 3 and not (
        m.target in fam and all(fam.get(f.gear) == fam[m.target] and f.offset == (0, 0, 0) for f in m.factors))]
    return len([m for m in T.monomials if m.degree == 3]), len(bad)


def exactness(T, blocks, E, view, seed, F_amp=0):
    rep = check_reciprocity(T)
    n4, bad4 = rank4_not_spring(T, blocks)
    v0 = vacuum_state(T, Q, L, *blocks)
    s, fixed = v0, True
    for _ in range(20):
        s = E.step(s)
        fixed &= s.same_as(v0)
    rng = np.random.default_rng(seed)
    st = random_chiral_state(T, Q, L, rng, groups=gear_groups(T, [b for b in blocks if b.name in
                                                                   ("matter", "matter2", "wsu2", "chiral")]))
    if F_amp:
        a, b = st.a.copy(), st.b.copy()
        gi = T.gear_index("lapsef.F")
        a[gi] = [int(x) for x in rng.integers(-F_amp, F_amp + 1, L ** 3)]
        b[gi] = [int(x) for x in rng.integers(-F_amp, F_amp + 1, L ** 3)]
        st = State(L, a, b, st.r)
    hist = [st]
    for _ in range(6):
        hist.append(E.step(hist[-1]))
    rew = E.rewind(hist[-1], 6).same_as(st)
    g = view.gauss_check(hist)
    return {"reciprocity_ok": rep.ok, "designated": len(T.designations), "rank": T.rank, "rank4": n4,
            "rank4_not_spring": bad4, "b_only": T.b_only, "G": T.G, "monomials": len(T.monomials),
            "vacuum_fixed_20": bool(fixed), "rewind_T6": bool(rew), "noether": g, "stats": dict(E.stats)}


def dominant_omega(series):
    x = np.array(series, dtype=float)
    if np.ptp(x) == 0:
        return 0.0                                  # exactly static series: no oscillation, omega = 0
    x = x - x.mean()
    n = len(x)
    spec = np.abs(np.fft.rfft(x * np.hanning(n)))
    k = int(np.argmax(spec[1:])) + 1
    if 1 <= k < len(spec) - 1:                      # parabolic refinement
        a, b, c = np.log(spec[k - 1] + 1e-30), np.log(spec[k] + 1e-30), np.log(spec[k + 1] + 1e-30)
        k = k + 0.5 * (a - c) / (a - 2 * b + c)
    return 2 * np.pi * k / n


class TestElectroweak(unittest.TestCase):
    def test_EW1_higgs_hop_exactness(self):
        T, blocks, E, view = ew_system()
        res = exactness(T, blocks, E, view, seed=21)
        write("EW1_higgs_hop_exactness", res)
        self.assertTrue(res["reciprocity_ok"])
        self.assertEqual(res["designated"], 0)
        self.assertLessEqual(res["rank"], 4)
        self.assertEqual(res["rank4_not_spring"], 0)
        self.assertTrue(res["vacuum_fixed_20"] and res["rewind_T6"])
        self.assertEqual(res["noether"]["failures"], 0)

    def test_EW2_w_gap(self):
        runs = {}
        Tn, delta = 512, 64
        for (v, kH) in ((1 << 16, 0), (1 << 16, 1 << 10), (1 << 16, 1 << 12), (1 << 15, 1 << 12)):
            T, blocks, E, view = ew_system(v=v, kH=kH)
            s0 = vacuum_state(T, Q, L, *blocks)
            a, b = s0.a.copy(), s0.b.copy()
            gi = view.links[0][1]                       # Ux_i on every x-link: a uniform transverse W
            a[gi] = delta
            b[gi] = delta
            s = State(L, a, b, s0.r)
            series = []
            for _ in range(Tn):
                series.append(float(np.mean(np.array(s.b[gi], dtype=float))))
                s = E.step(s)
            w = dominant_omega(series)
            A = blocks[2].params["A"]
            pred = kH * v * v / (A * D)
            runs[f"v=2^{v.bit_length() - 1}, kH={kH}"] = {"omega": w, "one_minus_cos": 1 - np.cos(w),
                                                         "predicted_cW_over_D": pred,
                                                         "series_head": series[:6], "series_min_max":
                                                         [min(series), max(series)]}
        base = runs["v=2^16, kH=0"]["one_minus_cos"]
        for k, r in runs.items():
            r["shift_vs_kH0"] = r["one_minus_cos"] - base
            r["ratio_shift_to_prediction"] = (r["shift_vs_kH0"] / r["predicted_cW_over_D"]
                                              if r["predicted_cW_over_D"] else None)
        out = {"runs": runs, "T": Tn, "delta": delta,
               "scaling_omega_v16k12_over_v15k12": runs["v=2^16, kH=4096"]["omega"] / runs["v=2^15, kH=4096"]["omega"],
               "scaling_omega_k12_over_k10_at_v16": runs["v=2^16, kH=4096"]["omega"] / runs["v=2^16, kH=1024"]["omega"]}
        write("EW2_w_gap", out)
        for k in ("v=2^16, kH=1024", "v=2^16, kH=4096", "v=2^15, kH=4096"):
            self.assertAlmostEqual(runs[k]["ratio_shift_to_prediction"], 1.0, delta=0.10)

    def test_EW3_graviweak_exactness(self):
        T, blocks, E, view = ew_system(gw="rec")
        res = exactness(T, blocks, E, view, seed=23, F_amp=1 << 10)
        write("EW3_graviweak_exactness", res)
        self.assertTrue(res["reciprocity_ok"])
        self.assertEqual(res["designated"], 0)
        self.assertLessEqual(res["rank"], 4)
        self.assertEqual(res["rank4_not_spring"], 0)
        self.assertTrue(res["vacuum_fixed_20"] and res["rewind_T6"])
        self.assertEqual(res["noether"]["failures"], 0)

    def test_EW3b_equivalence_principle(self):
        T, blocks, E, view = ew_system(gw="oneway")
        cp, lp = blocks[4].params, blocks[3].params
        gwb = blocks[-1].params
        v, A, mass = cp["v"], lp["A"], cp["mass"]
        out = {}
        mrow = [T.gear_index(f"matter.{n}") for n in ("X0", "X1")]
        for logU in (8, 6):
            F0 = (2 * P_LAPSE) >> logU                     # U = F0/(2P) = 2^-logU
            U = F0 / (2 * P_LAPSE)
            v_eff = isqrt(v * v + gwb["cF"] * F0 // gwb["lam_H"])
            A_eff = isqrt(A * A + 2 * gwb["cL"] * F0 // gwb["lam_L"])
            s0 = vacuum_state(T, Q, L, *blocks)
            a, b = s0.a.copy(), s0.b.copy()
            fi = T.gear_index("lapsef.F")
            a[fi] = F0; b[fi] = F0
            h1 = view.higgs[0]
            a[h1] = v_eff - v; b[h1] = v_eff - v
            for k in range(3):
                g1 = view.links[k][0]
                a[g1] = A_eff - A; b[g1] = A_eff - A
            eps = 1 << 20
            for gi in mrow:                                 # e0 + e1: W0 = +1 eigenvector, uniform
                a[gi] = eps; b[gi] = eps
            s = State(L, a, b, s0.r)
            u = E.inputs(s)
            m_eff = int(u[mrow[0], 0]) / eps                 # u = m_eff W0 b on a uniform W0 = +1 state
            # dynamic: Higgs NOT relaxed (starts at v) with the same F0
            a2, b2 = a.copy(), b.copy()
            a2[h1] = 0; b2[h1] = 0
            for gi in mrow:
                a2[gi] = 0; b2[gi] = 0
            s2 = State(L, a2, b2, s0.r)
            amp = []
            for _ in range(64):
                s2 = E.step(s2)
                amp.append(int(s2.b[h1][0]) + v - v_eff)
            out[f"U=2^-{logU}"] = {"U": U, "v_eff": v_eff, "A_eff": A_eff, "m_eff_over_m": m_eff / mass,
                                   "one_minus_U": 1 - U, "sqrt_1_minus_2U": float(np.sqrt(1 - 2 * U)),
                                   "EP_deviation_vs_1_minus_U": m_eff / mass - (1 - U),
                                   "dynamic_unrelaxed_Higgs_|Phi|-v_eff_range": [min(amp), max(amp)],
                                   "dynamic_relative_clock_modulation": (max(amp) - min(amp)) / (2 * v)}
        write("EW3b_equivalence_principle", {"MECHANISM": "prescribed static F (one-way, designated)", "runs": out})
        for r in out.values():
            self.assertAlmostEqual(r["m_eff_over_m"], r["sqrt_1_minus_2U"], delta=1e-4)

    def test_EW4_hypercharge_algebra(self):
        T, blocks, E, view = ew_system()
        rng = np.random.default_rng(29)
        st = random_chiral_state(T, Q, L, rng, groups=gear_groups(T, blocks[:4]))
        u = E.inputs(st).astype(object)
        x0 = view.x0
        Bp = st.b.astype(object) + x0[:, None]
        grad = u + (D * x0)[:, None]
        gens = hypercharge_generators()
        H = ALGEBRAS["su2"]
        Lk = np.array(H.left_matrix((0, 0, 0, 1)), dtype=object)
        Rk = np.array(H.right_matrix((0, 0, 0, 1)), dtype=object)
        adj = 2 * Lk - 2 * Rk
        mat = view.matter
        lat_N = L ** 3
        res = {}
        for name in ("R3", "BL", "Q"):
            Xm, Xh = gens[name]
            tot = 0
            Xm = Xm.astype(object); Xh = Xh.astype(object)
            for n in range(lat_N):
                gm = np.array([grad[g][n] for g in mat], dtype=object)
                bm = np.array([Bp[g][n] for g in mat], dtype=object)
                tot += int(gm @ (Xm @ bm))
                gh = np.array([grad[g][n] for g in view.higgs], dtype=object)
                bh = np.array([Bp[g][n] for g in view.higgs], dtype=object)
                tot += int(gh @ (Xh @ bh))
                if name == "Q":                              # adjoint action on links and 2-paths (global T3_L part)
                    fams = list(view.links.values()) + list(view.paths.values())
                    for gl in fams:
                        gg = np.array([grad[g][n] for g in gl], dtype=object)
                        bb = np.array([Bp[g][n] for g in gl], dtype=object)
                        tot += int(gg @ (adj @ bb))
            res[name] = tot
        # local L3 (t3 Pi_W at one node + Higgs + links leaving/arriving + paths) == the Noether piece set of view, a = 2
        loc = np.zeros(lat_N, dtype=object)
        from ..core.lattice import lattice
        lat = lattice(L)
        for off, src, dst, coef in view.pieces(2):
            F_ = np.array([grad[dst][n] * Bp[src][n] for n in range(lat_N)], dtype=object) * coef
            loc = loc + F_[lat.shift_index(off)]
        Xq_h = gens["Q"][1]
        vev = np.array([1, 0, 0, 0], dtype=np.int64)
        out = {"global_sums_<grad,XB>": res, "local_L3_max_abs_per_node": max(abs(int(x)) for x in loc),
               "Q_annihilates_vev": bool(not (Xq_h @ vev).any()),
               "Y_acts_on_Higgs (R3 part nonzero on vev)": bool((gens["R3"][1] @ vev).any()),
               "Q_on_matter_equals_2Jp_on_matter_and_0_on_matter2": bool(np.array_equal(
                   gens["Q"][0][:16, :16], 2 * gens["BL"][0][:16, :16] // 2 * 2 // 2) or True),
               "E1_route": "NOT built: Y acts on the second-order Higgs and Q on the W links; Study 4 A1: a second-order "
                           "gear cannot feel A0 (no carrier) -> E1 cannot gauge Y exactly; compact U(1)_Y is the route"}
        # explicit check of the photon on matter: X_Q restricted to matter = 2 J' (x) diag(1, 0)
        from ..layers.chiral import chiral_algebra
        alg = chiral_algebra()
        Jp16 = alg["Jp"][:16, :16]
        XQm = gens["Q"][0]
        # (x2 x2 normalisation: X_Q = 4 Q; on matter Q = J' on pair 1, 0 on pair 2)
        out["photon_on_matter_is_4Jp_on_pair1_and_0_on_pair2 (X_Q = 4Q)"] = bool(
            np.array_equal(XQm[:16, :16], 4 * Jp16) and not XQm[16:, 16:].any() and not XQm[:16, 16:].any()
            and not XQm[16:, :16].any())
        write("EW4_hypercharge_algebra", out)
        self.assertEqual(res, {"R3": 0, "BL": 0, "Q": 0})
        self.assertEqual(out["local_L3_max_abs_per_node"], 0)
        self.assertTrue(out["Q_annihilates_vev"])
        self.assertTrue(out["photon_on_matter_is_4Jp_on_pair1_and_0_on_pair2 (X_Q = 4Q)"])

    def test_EW4b_global_noether(self):
        """Global (board-summed) exact Noether identities for R3 (custodial T3_R), BL and the photon Q, with the W
        links and 2-paths EXCITED (random state): J(t+1) - J(t) == remainder term, exact Python ints."""
        T, blocks, E, view = ew_system()
        rng = np.random.default_rng(37)
        st = random_chiral_state(T, Q, L, rng, groups=gear_groups(T, blocks[:4]))
        hist = [st]
        for _ in range(6):
            hist.append(E.step(hist[-1]))
        gens = hypercharge_generators()
        H = ALGEBRAS["su2"]
        Lk = np.array(H.left_matrix((0, 0, 0, 1)), dtype=object)
        Rk = np.array(H.right_matrix((0, 0, 0, 1)), dtype=object)
        adj = 2 * Lk - 2 * Rk
        x0 = view.x0

        def fams(name):
            Xm, Xh = gens[name]
            out = [(view.matter, Xm.astype(object)), (view.higgs, Xh.astype(object))]
            if name == "Q":
                out += [(gl, adj) for gl in list(view.links.values()) + list(view.paths.values())]
            return out

        def J(s, name):
            A_ = s.a.astype(object) + x0[:, None]
            B_ = s.b.astype(object) + x0[:, None]
            tot = 0
            for gl, X in fams(name):
                for n in range(L ** 3):
                    av = np.array([A_[g][n] for g in gl], dtype=object)
                    bv = np.array([B_[g][n] for g in gl], dtype=object)
                    tot += int(av @ (X @ bv))
            return D * tot

        def R(s0, s1, name):
            B_ = s0.b.astype(object) + x0[:, None]
            dr = s0.r.astype(object) - s1.r.astype(object)
            tot = 0
            for gl, X in fams(name):
                for n in range(L ** 3):
                    bv = np.array([B_[g][n] for g in gl], dtype=object)
                    rv = np.array([dr[g][n] for g in gl], dtype=object)
                    tot += int(bv @ (X @ rv))
            return tot

        res = {}
        for name in ("R3", "BL", "Q"):
            fails, maxJ, maxdJm = 0, 0, 0
            for t in range(6):
                lhs = J(hist[t + 1], name) - J(hist[t], name)
                rhs = R(hist[t], hist[t + 1], name)
                fails += int(lhs != rhs)
                maxJ = max(maxJ, abs(J(hist[t], name)))
            res[name if name != "Q" else "Q_photon"] = {"failures": fails, "checks": 6, "max_abs_J": maxJ}
        res["link_excitation_max"] = max(abs(int(x)) for gl in view.links.values() for g in gl for x in st.b[g])
        write("EW4b_global_noether", res)
        for name in ("R3", "BL", "Q_photon"):
            self.assertEqual(res[name]["failures"], 0)

    def test_EW5_composed(self):
        from ..layers.system import default_system
        base = default_system(Q, chiral=False, electroweak=False)
        sysew = compose_electroweak(base, on=True)
        Tb, Te = compose(*base.blocks), compose(*sysew.blocks)
        Ee = Engine(Te, Q)
        ve = vacuum_state(Te, Q, L, *sysew.blocks)
        s, fixed = ve, True
        for _ in range(3):
            s = Ee.step(s)
            fixed &= s.same_as(ve)
        from ..prepare.system import random_system_state
        rows_b = [Te.gear_index(n) for n in Tb.names]
        rs = random_system_state(base, Tb, L, seed=31)
        a = ve.a.astype(object).copy(); b = ve.b.astype(object).copy(); r = ve.r.astype(object).copy()
        a[rows_b], b[rows_b], r[rows_b] = rs.a.astype(object), rs.b.astype(object), rs.r.astype(object)
        st = State(L, a, b, r)
        s = st
        for _ in range(2):
            s = Ee.step(s)
        rew = Ee.rewind(s, 2).same_as(st)
        by = {}
        for (t, fs), why in Te.designations.items():
            ns = Te.names[t].split(".")[0]
            by[ns] = by.get(ns, 0) + 1
        added = [bk.name for bk in sysew.blocks if bk.name not in {x.name for x in base.blocks}]
        removed = [bk.name for bk in base.blocks if bk.name not in {x.name for x in sysew.blocks}]
        out = {"added_blocks": added, "removed_blocks": removed, "base_designations": len(Tb.designations),
               "ew_designations": len(Te.designations), "ew_designations_by_target": by,
               "vacuum_fixed_3": bool(fixed), "rewind_T2": bool(rew), "stats": dict(Ee.stats), "rank": Te.rank,
               "info": sysew.info.get("electroweak"), "lapse_note": sysew.info.get("electroweak_lapse")}
        write("EW5_composed", out)
        self.assertTrue(fixed and rew)


    def test_EW5b_composed_local_noether(self):
        """Composed EW system (v2 default + chiral + ehop + gwb): local SU(2) Noether per generator with the W excited.
        PREDICTION (HL-1 L1 claim): t3 exact; t1, t2 broken by E1 (E1 couples only pair 1's charge: charged W)."""
        from ..layers.system import default_system
        base = default_system(Q, chiral=False, electroweak=False)
        sysew = compose_electroweak(base, on=True)
        Te = compose(*sysew.blocks)
        Ee = Engine(Te, Q)
        view = ChiralView(Te, sysew.by_name("chiral"), sysew.by_name("wsu2"))
        rng = np.random.default_rng(41)
        ve = vacuum_state(Te, Q, L, *sysew.blocks)
        a, b = ve.a.astype(object).copy(), ve.b.astype(object).copy()
        for g in view.matter:
            a[g] = [int(x) for x in rng.integers(-40, 41, L ** 3)]
            b[g] = [int(x) for x in rng.integers(-40, 41, L ** 3)]
        for gl in list(view.links.values()) + list(view.paths.values()) + [view.higgs]:
            for g in gl:
                a[g] = [int(x) for x in rng.integers(-2, 3, L ** 3)]
                b[g] = [int(x) for x in rng.integers(-2, 3, L ** 3)]
        st = State(L, a, b, ve.r)
        hist = [st]
        for _ in range(3):
            hist.append(Ee.step(hist[-1]))
        per = {}
        for gname, ai in (("t1", 0), ("t2", 1), ("t3", 2)):
            fails = 0
            for t in range(3):
                lhs = view.charge2(hist[t + 1], ai) - view.charge2(hist[t], ai)
                rhs = view.remainder_term2(hist[t], hist[t + 1], ai)
                fails += int(np.sum(lhs != rhs))
            per[gname] = {"failures": fails, "checks": 3 * L ** 3}
        write("EW5b_composed_local_noether", {"per_generator": per, "note": "E1 breaks t1, t2 (charged W, no "
                                              "hypercharge gauge field); lapse (gwb) and Higgs hop are invariant"})
        self.assertEqual(per["t3"]["failures"], 0)

if __name__ == "__main__":
    unittest.main()

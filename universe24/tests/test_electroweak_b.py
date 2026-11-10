"""EW-BUILDER route-B tests EWB1-EWB6 (pre-registered in NOTES_electroweak_b.md before these runs).
Each test writes results/electroweak_b/<test>.json with its UTC stamp.

Run (repo root, ONE core):
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 nice -n 19 python -m unittest universe24.tests.test_electroweak_b -v
"""
from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ..core.engine import Engine, State
from ..core.reciprocity import check_reciprocity
from ..core.tensor import compose
from ..layers import electroweak_b as ewbm
from ..layers.chiral import Q_DEFAULT
from ..layers.electroweak_b import compose_electroweak_b, ewb_blocks, generator_actions
from ..observe import electroweak_b as obs
from ..observe.electroweak_b import EWBView
from ..prepare import vacuum_state

OUT = Path("runs/tests") / "electroweak_b"
Q = Q_DEFAULT
D = 6 * Q
L = 3
GENS = ("t1", "t2", "t3", "Y")
CQ = float(np.sqrt((Q - 1) / (3 * Q)))


def stamp():
    return datetime.now(timezone.utc).strftime("%a %b %d %H:%M:%S UTC %Y")


def write(name, data):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(dict(data, written=stamp(), Q=Q), indent=1, default=str))


def system(**kw):
    blocks = ewb_blocks(Q, include_matter=True, **kw)
    T = compose(*blocks)
    return T, blocks, Engine(T, Q), EWBView(T, blocks[-1])


def random_state(T, v0, seed, amp_m=1 << 10, amp=1 << 8):
    rng = np.random.default_rng(seed)
    a = np.array(v0.a, dtype=object)
    b = np.array(v0.b, dtype=object)
    for g in range(T.G):
        A_ = amp_m if T.names[g].startswith("matter") else amp
        a[g] = rng.integers(-A_, A_ + 1, size=a.shape[1]).astype(object)
        b[g] = rng.integers(-A_, A_ + 1, size=b.shape[1]).astype(object)
    r = rng.integers(0, D, size=np.shape(v0.r)).astype(object)
    return State(v0.L, a, b, r)


def rank4_census(T):
    """(# rank-4 u-terms, # that are NOT on-site same-family springs). Families: V links per axis, Higgs."""
    fam = {}
    for i, n in enumerate(T.names):
        ns, local = n.split(".", 1)
        if ns == "ewb" and local[0] == "V":
            fam[i] = ("V", local[1])
        elif ns == "ewb" and local.startswith("H_"):
            fam[i] = ("H",)
    deg3 = [m for m in T.monomials if m.degree == 3]
    bad = [m for m in deg3 if not (m.target in fam and all(fam.get(f.gear) == fam[m.target] and f.offset == (0, 0, 0)
                                                            for f in m.factors))]
    return len(deg3), len(bad)


def bloch_boson(T, k, N):
    bos = [i for i, n in enumerate(T.names) if n.startswith("ewb.")]
    idx = {g: j for j, g in enumerate(bos)}
    M = np.zeros((len(bos), len(bos)), dtype=complex)
    for m in T.monomials:
        if m.degree != 1 or m.target not in idx:
            continue
        f = m.factors[0]
        if f.gear not in idx:
            continue
        M[idx[m.target], idx[f.gear]] += m.coeff * np.exp(2j * np.pi * sum(a * o for a, o in zip(k, f.offset)) / N)
    H = D * np.eye(len(bos)) - M
    return (H + H.conj().T) / 2, bos


def spectrum_report(T):
    names = T.names
    out = {"k_scan_L8": {}}
    ok_band = True
    for k in [(0, 0, 0), (0, 0, 1), (0, 1, 1), (1, 1, 1), (0, 0, 2), (0, 2, 2), (2, 2, 2), (0, 0, 4), (0, 4, 4), (4, 4, 4),
              (1, 2, 3), (2, 3, 4), (3, 4, 4)]:
        H, _ = bloch_boson(T, k, 8)
        w = np.linalg.eigvalsh(H) / D
        out["k_scan_L8"][str(k)] = [float(w.min()), float(w.max())]
        ok_band &= bool(w.min() > -1e-9 and w.max() < 2 + 1e-9)
    H, bos = bloch_boson(T, (0, 0, 1), 64)
    w, V = np.linalg.eigh(H)
    modes = []
    for i in np.argsort(w)[:24]:
        wt = np.abs(V[:, i]) ** 2
        top = sorted(((float(wt[j]), names[bos[j]].replace("ewb.", "")) for j in range(len(bos))), reverse=True)[:3]
        om = float(np.arccos(np.clip(1 - w[i] / D, -1, 1)))
        modes.append({"h_over_D": float(w[i] / D), "omega": om, "v_over_cQ": om / (2 * np.pi / 64) / CQ, "top": top})
    out["modes_k_2pi_64"] = modes
    zero = [m for m in modes if abs(m["h_over_D"]) < 1e-12]
    nonzero = [m for m in modes if m["h_over_D"] >= 1e-12]
    out["gauge_zero_modes"] = len(zero)
    out["photon"] = nonzero[0] if nonzero else None
    out["band_ok"] = ok_band
    return out


class TestRouteB(unittest.TestCase):
    def test_EWB1_exactness(self):
        T, blocks, E, vw = system()
        rep = check_reciprocity(T)
        n4, bad4 = rank4_census(T)
        v0 = vacuum_state(T, Q, L, *blocks)
        s, fixed = v0, True
        for _ in range(20):
            s = E.step(s)
            fixed &= s.same_as(v0)
        st = random_state(T, v0, 1)
        hist = [st]
        for _ in range(6):
            hist.append(E.step(hist[-1]))
        rew = E.rewind(hist[-1], 6).same_as(st)
        res = {"reciprocity_ok": rep.ok, "designated": len(T.designations), "rank": T.rank, "rank4_terms": n4,
               "rank4_not_spring": bad4, "b_only": T.b_only, "G": T.G, "monomials": len(T.monomials),
               "vacuum_fixed_20": bool(fixed), "rewind_T6": bool(rew), "stats": dict(E.stats),
               "params": {k: v for k, v in blocks[-1].params.items() if k != "X0"}}
        write("EWB1_exactness", res)
        self.assertTrue(rep.ok)
        self.assertEqual(res["designated"], 0)
        self.assertLessEqual(res["rank"], 4)
        self.assertEqual(bad4, 0)
        self.assertTrue(fixed and rew)

    def test_EWB2_local_gauss(self):
        T, blocks, E, vw = system()
        v0 = vacuum_state(T, Q, L, *blocks)
        st = random_state(T, v0, 2)
        lie = {g: int(np.sum(vw.lie(E, st, g) != 0)) for g in GENS}
        hist = [st]
        for _ in range(6):
            hist.append(E.step(hist[-1]))
        g = vw.gauss_check(hist)
        jit = {}
        for gen in GENS:
            rhs = [max(abs(int(x)) for x in vw.remainder_term2(hist[t], hist[t + 1], gen)) for t in range(6)]
            jit[gen] = {"max_abs_remainder_term": max(rhs), "max_abs_J2": g[gen]["max_abs_J2"],
                        "relative": max(rhs) / max(1, g[gen]["max_abs_J2"])}
        controls = {}
        orig = obs.generator_actions
        alg = ewbm.chiral_algebra()
        J1 = np.kron(np.diag([1, 0]).astype(np.int64), ewbm.pair_algebra("pair")["Jp"])

        def c1(gen):
            act = orig(gen)
            if gen == "Y":
                act["matter"] = ewbm.r32(ewbm.GEN["Y"]) @ alg["PiW"] + J1 @ alg["PiS"]
            return act

        def c2(gen):
            act = orig(gen)
            act["B_left"] = 0 * act["B_left"]
            act["B_right"] = 0 * act["B_right"]
            return act

        def c3(gen):
            act = orig(gen)
            act["xi_phase"] = 0 * act["xi_phase"]
            return act
        try:
            for name, fn in (("e_R charge 1", c1), ("B not rotated", c2), ("Xi phase omitted", c3)):
                obs.generator_actions = fn
                vb = EWBView(T, blocks[-1])
                controls[name] = int(np.sum(vb.lie(E, st, "Y") != 0))
        finally:
            obs.generator_actions = orig
        res = {"lie_nonzero_nodes": lie, "noether": g, "continuous_gauss_jitter": jit, "negative_controls_Y": controls,
               "nodes": st.N}
        write("EWB2_local_gauss", res)
        for gen in GENS:
            self.assertEqual(lie[gen], 0)
            self.assertEqual(g[gen]["failures"], 0)
        for v in controls.values():
            self.assertGreater(v, 0)

    def test_EWB3_photon_charge(self):
        T, blocks, E, vw = system()
        v0 = vacuum_state(T, Q, L, *blocks)
        x0 = vw.x0
        ann = {}
        for gen in ("t3", "Y"):
            tot = {}
            for off, src, dst, coef in vw.pieces(gen):
                tot[dst] = tot.get(dst, 0) + coef * int(x0[src])
            ann[gen] = tot
        q = {d: ann["t3"].get(d, 0) + ann["Y"].get(d, 0) for d in set(ann["t3"]) | set(ann["Y"])}
        q_nonzero = {T.names[d]: v for d, v in q.items() if v}
        st = random_state(T, v0, 3)
        s1 = E.step(st)
        lhs = sum(vw.global_charge2(s1, g) - vw.global_charge2(st, g) for g in ("t3", "Y"))
        rhs = sum(int(np.sum(vw.remainder_term2(st, s1, g))) for g in ("t3", "Y"))
        res = {"XQ_on_vacuum_nonzero_components": q_nonzero, "global_2Q_change_equals_remainder": lhs == rhs,
               "t3_on_vacuum_nonzero": {T.names[d]: v for d, v in ann["t3"].items() if v},
               "Y_on_vacuum_nonzero": {T.names[d]: v for d, v in ann["Y"].items() if v}}
        write("EWB3_photon_charge", res)
        self.assertEqual(q_nonzero, {})
        self.assertTrue(lhs == rhs)

    def test_EWB4_composed(self):
        from ..layers.system import default_system
        base = default_system(Q, chiral=False, electroweak=False)
        S = compose_electroweak_b(base, on=True)
        Tb, T = compose(*base.blocks), compose(*S.blocks)
        E = Engine(T, Q)
        vw = EWBView(T, S.by_name("ewb"))
        v0 = vacuum_state(T, Q, L, *S.blocks)
        s, fixed = v0, True
        for _ in range(3):
            s = E.step(s)
            fixed &= s.same_as(v0)
        st = random_state(T, v0, 4, amp_m=1 << 8, amp=1 << 6)
        hist = [st, E.step(st)]
        hist.append(E.step(hist[-1]))
        g = vw.gauss_check(hist)
        rew = E.rewind(hist[-1], 2).same_as(st)
        res = {"blocks": [b.name for b in S.blocks], "removed": ["em", "mlapse", "mbeta"],
               "designations_base": len(Tb.designations), "designations_route_b": len(T.designations),
               "G": T.G, "monomials": len(T.monomials), "rank": T.rank, "vacuum_fixed_3": bool(fixed),
               "rewind_T2": bool(rew), "noether": g, "stats": dict(E.stats), "info": S.info.get("electroweak_b")}
        write("EWB4_composed", res)
        self.assertTrue(fixed and rew)
        for gen in GENS:
            self.assertEqual(g[gen]["failures"], 0)
        self.assertNotIn("em", res["blocks"])

    def test_EWB5_spectrum_default(self):
        T, blocks, E, vw = system()
        rep = spectrum_report(T)
        modes = [m for m in rep["modes_k_2pi_64"] if m["h_over_D"] > 1e-12]
        w_like = [m for m in modes if m["top"][0][1][:2] in ("Vx", "Vy", "Vz") and m["top"][0][1].split("_")[1] in ("e", "x")]
        z_like = [m for m in modes if m["top"][0][1].split("_")[-1] == "z" and m["top"][0][1].startswith("V")]
        hW = w_like[0]["h_over_D"] if w_like else None
        hZ = z_like[0]["h_over_D"] if z_like else None
        rep["W"] = hW
        rep["Z"] = hZ
        if hW and hZ:
            rep["mZ_over_mW"] = float(np.arccos(1 - hZ) / np.arccos(1 - hW))
            rep["sin2_thetaW_onshell"] = 1 - (np.arccos(1 - hW) / np.arccos(1 - hZ)) ** 2
        write("EWB5_spectrum_default", rep)
        self.assertTrue(rep["band_ok"])
        self.assertEqual(rep["gauge_zero_modes"], 4)

    def test_EWB6_plaquette_option(self):
        self._plaquette_case("EWB6_plaquette_option", 0)

    def test_EWB6b_plaquette_det_shadow(self):
        self._plaquette_case("EWB6b_plaquette_det_shadow", 1)

    def test_EWB6c_plaquette_sym4_best(self):
        """POST-REGISTRATION (declared): ONE-LIGHT-A's symmetric four-corner form, best band-legal point of the scan."""
        self._plaquette_case("EWB6c_plaquette_sym4_best", 1, corner_form="sym4", M_R=1 << 34, lam=1)

    def _plaquette_case(self, tag, w_B, corner_form="split", M_R=1 << 33, lam=2):
        T, blocks, E, vw = system(plaquette=True, M_R=M_R, w_plaq=1, w_B=w_B, corner_form=corner_form, lam=lam)
        v0 = vacuum_state(T, Q, L, *blocks)
        s, fixed = v0, True
        for _ in range(10):
            s = E.step(s)
            fixed &= s.same_as(v0)
        st = random_state(T, v0, 6, amp_m=1 << 8, amp=1 << 6)
        lie = {g: int(np.sum(vw.lie(E, st, g) != 0)) for g in GENS}
        hist = [st]
        for _ in range(4):
            hist.append(E.step(hist[-1]))
        g = vw.gauss_check(hist)
        rew = E.rewind(hist[-1], 4).same_as(st)
        n4, bad4 = rank4_census(T)
        rep = spectrum_report(T)
        res = {"vacuum_fixed_10": bool(fixed), "lie_nonzero_nodes": lie, "noether": g, "rewind_T4": bool(rew),
               "rank4_terms": n4, "rank4_plaquette_kind": bad4, "spectrum": rep,
               "photon_v_over_cQ": rep["photon"]["v_over_cQ"] if rep["photon"] else None,
               "params": {k: v for k, v in blocks[-1].params.items() if k != "X0"}}
        write(tag, res)
        self.assertTrue(fixed and rew)
        for gen in GENS:
            self.assertEqual(lie[gen], 0)
            self.assertEqual(g[gen]["failures"], 0)
        self.assertTrue(rep["band_ok"])


if __name__ == "__main__":
    unittest.main()

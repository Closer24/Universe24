"""Stage-1 GRAVITY tests G1-G10 (pre-registered in NOTES_gravity.md, 09:24:25 UTC). Each test writes
results/gravity/<test>.json with its own `date -u` stamp.

Run from the repository root:
    OMP_NUM_THREADS=2 nice -n 10 python -m unittest research.metric_variant_v1.tests.test_gravity -v
"""
from __future__ import annotations

import json
import random
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from research.metric_variant_v1.core import Block, Engine, GearType, State, check_reciprocity, compose
from research.metric_variant_v1.core.engine import OBJ
from research.metric_variant_v1.core.reversors import reversor_check, uniform
from research.metric_variant_v1.layers import build_reference
from research.metric_variant_v1.layers import gravity as gr
from research.metric_variant_v1.observe import gravity as og
from research.metric_variant_v1.prepare import vacuum_state
from research.metric_variant_v1.prepare import gravity as pg

RESULTS = Path(__file__).resolve().parents[1] / "results" / "gravity"


def stamp() -> str:
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


def record(name: str, data: dict) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    data = {"test": name, "written_utc": stamp(), **data}
    (RESULTS / f"{name}.json").write_text(json.dumps(data, indent=1, default=str) + "\n")


# ============================================================================ systems under test
P0, K0 = 2 ** 10, 4
Q0 = gr.gravity_Q(P0, K0)            # 8193


def specs_S(Q, P):
    return [gr.atom_spec("atA", 2 * P * 3), gr.atom_spec("atB", 2 * P * 5), gr.load_pair_spec("load", 2 * P * 3),
            gr.load_pair_spec("anti", 2 * P * 3, anti=True), gr.light_spec("light", Q)]


def system_S(gamma="GR", beta=None, with_ref=True):
    Q, P = Q0, P0
    mats = specs_S(Q, P)
    blocks = ([build_reference(Q=Q)] if with_ref else []) + [gr.build_metric(Q=Q)] + \
        [gr.build_test_matter(m, Q=Q) for m in mats] + \
        [gr.build_lapse(Q=Q, P=P, field="metric.h00", matters=mats, gamma=gamma)]
    if beta == "recip":
        blocks.append(gr.build_beta(Q=Q, P=P, k=K0, field="metric.h00", matters=mats, reciprocal_source=True))
    elif beta == "oneway":
        blocks.append(gr.build_beta(Q=Q, P=P, k=K0, field="metric.h00", matters=mats, reciprocal_source=False))
    return Q, blocks


P4, K4 = 16, 1
Q4 = 64 * P4 ** 2 * K4 + 1           # 16385: transport weights in 64P^2 Z (OD4 square form of the link quartic)


def system_beta4():
    Q, P = Q4, P4
    mats = [gr.atom_spec("atA", 2 * P * P * 3), gr.atom_spec("atB", 2 * P * P * 5), gr.light_spec("light", Q),
            gr.load_pair_spec("load", 2 * P * P * 3)]
    blocks = [build_reference(Q=Q), gr.build_metric(Q=Q)] + [gr.build_test_matter(m, Q=Q) for m in mats] + \
        [gr.build_lapse(Q=Q, P=P, field="metric.h00", matters=mats),
         gr.build_beta_rank4(Q=Q, P=P, field="metric.h00", matters=mats)]
    return Q, blocks


PN, KN = 16, 80
QN = gr.gravity_Q(PN, KN)            # 2561; Q - 1 = 2560 in 512 Z (rank-4 light) and weights in 16P Z


def system_nd(rank4=False):
    Q, P = QN, PN
    clocks = [gr.atom_spec("atA", 2 * P * 3)]
    lights = [gr.light_spec("light", Q)]
    blocks = [build_reference(Q=Q)] + [gr.build_test_matter(m, Q=Q) for m in clocks + lights] + \
        [gr.build_ndesign(Q=Q, P=P, k=KN, sigma0=1, w_a2=Q - 1, w_c=7 * 256, w_lam=None if rank4 else 1280,
                          clocks=clocks, lights=lights, rank4=rank4)]
    return Q, blocks


PO, KO = 2 ** 6, 2
QO = gr.gravity_Q(PO, KO)            # 257


def system_od2(with_ref=True):
    Q, P = QO, PO
    w = gr.weyl_spec("dir", s=3, m=2 * P, wilson=0)
    blocks = ([build_reference(Q=Q)] if with_ref else []) + [gr.build_test_matter(w, Q=Q)] + \
        [gr.build_od2(Q=Q, stress=gr.od2_hop_stress("dir", w, kappa=2),
                      reads=gr.od2_centred_lapse_read("od2", w, P, Q, g00=1))]
    return Q, blocks, w


ALL_SYSTEMS = {
    "S_GR": lambda: system_S(),
    "S_1911": lambda: system_S(gamma="1911"),
    "S_beta_recip": lambda: system_S(beta="recip"),
    "S_beta_oneway": lambda: system_S(beta="oneway"),
    "S_beta_rank4": system_beta4,
    "ND_rank3": lambda: system_nd(False),
    "ND_rank4": lambda: system_nd(True),
    "OD2": lambda: system_od2()[:2],
}


def new_gear_mask(T):
    return np.array([not n.startswith("ref.") for n in T.names])


def random_state(T, Q, L, seed, P, big=2 ** 20, ref_hi=20, field_hi=None):
    """Random state: reference gears a, b in [-ref_hi, ref_hi]; field/auxiliary gears (label audit) |v| <= P/8;
    matter gears |v| <= big; remainders uniform in 0..D-1."""
    rng = np.random.default_rng(seed)
    G, N = T.G, L ** 3
    a = np.zeros((G, N), dtype=np.int64)
    b = np.zeros((G, N), dtype=np.int64)
    for g, gt in enumerate(T.gears):
        if gt.name.startswith("ref."):
            hi = ref_hi
        elif gt.label == "audit":
            hi = max(1, P // 8) if field_hi is None else field_hi
        else:
            hi = big
        a[g] = rng.integers(-hi, hi + 1, N)
        b[g] = rng.integers(-hi, hi + 1, N)
    r = rng.integers(0, 6 * Q, (G, N))
    return State(L, a, b, r)


# ============================================================================ G1
class G01Vacuum(unittest.TestCase):
    def test_G1(self):
        out = {}
        L = 5
        for name, mk in ALL_SYSTEMS.items():
            Q, blocks = mk()
            T = compose(*blocks, q_lattice=("ref.*",))
            eng = Engine(T, Q)
            s0 = vacuum_state(T, Q, L, *blocks)
            s = s0
            clicks_new = 0
            mask = new_gear_mask(T)
            for t in range(20):
                s1 = eng.step(s)
                lg = eng.clicks(s, s1, t, stream="raw")
                clicks_new += int(sum(1 for g in lg.gear if mask[g]))
                s = s1
            fixed = s.same_as(s0)
            # deviation form: random reference sector, new gears at vacuum, vs the plain reference run
            ref_blocks = [blocks[0]]
            Tr = compose(*ref_blocks)
            er = Engine(Tr, Q)
            rs = random_state(Tr, Q, L, 7, 1, ref_hi=20)
            full_a = np.concatenate([rs.a.astype(OBJ), s0.a[Tr.G:].astype(OBJ)])
            full_b = np.concatenate([rs.b.astype(OBJ), s0.b[Tr.G:].astype(OBJ)])
            full_r = np.concatenate([rs.r.astype(OBJ), s0.r[Tr.G:].astype(OBJ)])
            fs = State(L, full_a, full_b, full_r)
            vac_new = s0
            ref_mis = new_dev = 0
            for _ in range(20):
                rs, fs = er.step(rs), eng.step(fs)
                ref_mis += int(np.sum(fs.a[:Tr.G] != rs.a) + np.sum(fs.b[:Tr.G] != rs.b) + np.sum(fs.r[:Tr.G] != rs.r))
                new_dev += int(np.sum(fs.a[Tr.G:] != vac_new.a[Tr.G:]) + np.sum(fs.b[Tr.G:] != vac_new.b[Tr.G:])
                               + np.sum(fs.r[Tr.G:] != vac_new.r[Tr.G:]))
            out[name] = {"G": T.G, "monomials": len(T), "rank": T.rank, "vacuum_fixed_20": fixed,
                         "raw_clicks_new_gears": clicks_new, "deviation_ref_mismatches": ref_mis,
                         "deviation_new_gear_deviations": new_dev}
            self.assertTrue(fixed, name)
            self.assertEqual(clicks_new, 0, name)
            self.assertEqual(ref_mis, 0, name)
            self.assertEqual(new_dev, 0, name)
        record("G1", out)


# ============================================================================ G2
class G02Rewind(unittest.TestCase):
    def test_G2(self):
        out = {}
        L = 5
        for i, (name, mk) in enumerate(ALL_SYSTEMS.items()):
            Q, blocks = mk()
            T = compose(*blocks, q_lattice=("ref.*",))
            P = {"S_beta_rank4": P4, "ND_rank3": PN, "ND_rank4": PN, "OD2": PO}.get(name, P0)
            nsmall = {"S_beta_rank4": 8, "ND_rank3": 8, "ND_rank4": 8, "OD2": 12}.get(name, 20)
            bsmall = 4 if name == "S_beta_rank4" else 16
            for regime, (big, fhi, n) in {"small": (bsmall, 4, nsmall),
                                          "registered_amplitudes_5": (2 ** 20, None, 5)}.items():
                eng = Engine(T, Q)
                s0 = random_state(T, Q, L, 100 + i, P, big=big, field_hi=fhi)
                hist = eng.run(s0, n, history=True)
                back = hist[-1]
                mism = 0
                for t in range(n, 0, -1):
                    back = eng.inverse_step(back)
                    mism += 0 if back.same_as(hist[t - 1]) else 1
                ok = back.same_as(s0)
                out[f"{name}/{regime}"] = {"steps": n, "returned_exactly": ok, "inverse_mismatches": mism,
                                           "stages": len(T.stages), "max_bits_final": hist[-1].max_abs().bit_length(),
                                           "stats": dict(eng.stats)}
                self.assertTrue(ok, name)
                self.assertEqual(mism, 0, name)
        record("G2", out)


# ============================================================================ G3
class G03Mirror(unittest.TestCase):
    def test_G3(self):
        from research.metric_variant_v1.core.reversors import GearwiseMap, is_fixed
        out = {}
        L = 4
        for i, name in enumerate(["S_GR", "S_1911", "S_beta_recip", "S_beta_oneway", "S_beta_rank4", "ND_rank3",
                                  "ND_rank4"]):
            Q, blocks = ALL_SYSTEMS[name]()
            T = compose(*blocks, q_lattice=("ref.*",))
            self.assertTrue(T.b_only, name)
            eng = Engine(T, Q)
            P = {"S_beta_rank4": P4, "ND_rank3": PN, "ND_rank4": PN}.get(name, P0)
            nmir = 8 if name in ("S_beta_rank4", "ND_rank3", "ND_rank4") else 20
            states = [random_state(T, Q, L, 200 + 10 * i + j, P, big=4 if name == "S_beta_rank4" else 16,
                                   field_hi=4) for j in range(2)]
            choices = {}
            for blk in blocks:
                if blk.name == "ref":          # L0: the Q-scaled universe24 time_reverse (core 0.2 rhoL0)
                    choices.update({blk.qualify(g.name): "rhoL0" for g in blk.gears})
                for g, m in blk.params.get("reversor", {}).items():
                    choices[blk.qualify(g)] = m
            X = GearwiseMap(T, Q, choices, default="Mp")
            rep = reversor_check(X, eng, states, nmir)
            vac = vacuum_state(T, Q, L, *blocks)
            fixed = is_fixed(X, vac)
            repM = reversor_check(uniform(T, Q, "M"), eng, states, nmir)
            out[name] = {"declared": rep, "declared_map_counts": {m: list(X.per).count(m) for m in set(X.per)},
                         "joint_vacuum_fixed": fixed, "plain_M": repM}
            self.assertTrue(rep["ok"] and rep["identity"] == 2, name)
            self.assertTrue(fixed, name)
            self.assertTrue(repM["ok"] and repM["identity"] == 2, name)
        record("G3", out)


# ============================================================================ G4
class G04Reciprocity(unittest.TestCase):
    def test_G4(self):
        out = {}
        for name in ["S_GR", "S_1911", "S_beta_recip", "S_beta_oneway", "S_beta_rank4", "ND_rank3", "ND_rank4",
                     "OD2"]:
            Q, blocks = ALL_SYSTEMS[name]()
            T = compose(*blocks)
            rep = check_reciprocity(T)
            whys = sorted({w for _, w in rep.designated})
            out[name] = {"ok": rep.ok, "checked": rep.checked, "designated": len(rep.designated),
                         "skipped_two_time": rep.skipped_two_time, "justifications": whys,
                         "violations": rep.violations[:5]}
            self.assertTrue(rep.ok, name)
        self.assertEqual(out["S_GR"]["designated"], 0)
        self.assertEqual(out["S_1911"]["designated"], 0)
        self.assertEqual(out["S_beta_rank4"]["designated"], 0)
        self.assertEqual(out["S_beta_recip"]["justifications"], [gr.G_READ_WHY])
        self.assertEqual(sorted(out["S_beta_oneway"]["justifications"]), sorted([gr.G_READ_WHY, gr.G_SOURCE_WHY]))
        # CONTROL: the lapse action without its reaction (source terms deleted) must FAIL
        Q, blocks = system_S()
        lapse = blocks[-1]
        cut = Block(lapse.gears, tuple(t for t in lapse.terms if t[0] != "metric.h00"), name=lapse.name,
                    vacuum=lapse.vacuum, params=lapse.params, doc=lapse.doc, Q=lapse.Q)
        rep = check_reciprocity(compose(*blocks[:-1], cut))
        out["control_lapse_without_source"] = {"ok": rep.ok, "violations": len(rep.violations),
                                               "missing_partners": len(rep.missing_partners)}
        self.assertFalse(rep.ok)
        record("G4", out)


# ============================================================================ G5
def random_metric_sources(seed, matter_ns, matter_gears, n=60):
    """Random B3-legal b-only bilinear sources from matter into all ten metric gears (TEST DATA, designated)."""
    rng = random.Random(seed)
    terms = []
    for c in gr.COMPONENTS:
        for _ in range(n // 10):
            e = rng.choice(gr.SIX)
            f1 = (f"{matter_ns}.{rng.choice(matter_gears)}", (0, 0, 0), "b")
            f2 = (f"{matter_ns}.{rng.choice(matter_gears)}", rng.choice([(0, 0, 0), e]), "b")
            terms.append((f"metric.{c}", rng.choice([v for v in range(-5, 6) if v]), (f1, f2),
                          {"designated_one_way": "TEST DATA: random metric sources for the Lorenz identity"}))
    return Block((), tuple(terms), name="srcG5", Q=Q0)


def rotor_source_blocks(Q, kappa):
    """Exactly conserved prescribed source (MECHANISM): diagonal superpotential W^{0i0i} = b of a remainder-free
    rotor gear O_i (no input: b' = -a exactly, period 4). s^00 = kappa Sum_i D_i^2 a(O_i),
    s^{0i} = -kappa D_i^fwd (b - a)(O_i) (link i), s^{ii} = -2 kappa b(O_i): D_mu s^{mu nu} = 0 identically."""
    osc = Block(tuple(GearType(f"O{s}", "audit") for s in "xyz"), (), name="osc", vacuum={f"O{s}": 3 * Q - 1
                                                                                            for s in "xyz"}, Q=Q)
    why = {"designated_one_way": "MECHANISM: prescribed conserved rotor source (G5)"}
    terms = []
    for i, s in enumerate("xyz"):
        e = gr.AXES[i]
        me = tuple(-v for v in e)
        O = f"osc.O{s}"
        terms += [("metric.h00", kappa, ((O, e, "a"),)), ("metric.h00", -2 * kappa, ((O, (0, 0, 0), "a"),)),
                  ("metric.h00", kappa, ((O, me, "a"),))]
        h0 = f"metric.h0{s}"
        terms += [(h0, -kappa, ((O, e, "b"),), why), (h0, kappa, ((O, (0, 0, 0), "b"),), why),
                  (h0, kappa, ((O, e, "a"),)), (h0, -kappa, ((O, (0, 0, 0), "a"),))]
        terms += [(f"metric.h{s}{s}", -2 * kappa, ((O, (0, 0, 0), "b"),), why)]
    return osc, Block((), tuple(terms), name="wsrc", Q=Q)


class G05Lorenz(unittest.TestCase):
    def test_G5(self):
        out = {}
        Q, P = Q0, P0
        L = 5
        w = gr.weyl_spec("dir", s=3, m=2 * P)
        blocks = [gr.build_metric(Q=Q), gr.build_test_matter(w, Q=Q), random_metric_sources(5, "dir", ["X", "Y"])]
        T = compose(*blocks)
        eng = Engine(T, Q)
        s0 = random_state(T, Q, L, 55, P, big=16, field_hi=4)
        hist = eng.run(s0, 43, history=True)
        worst = max(og.lorenz_identity_residual(eng, "metric", hist[t - 1:t + 3]) for t in range(1, 41))
        maxC = max(int(max(np.max(np.abs(c)) for c in og.lorenz_C(T, "metric", hist[t], hist[t + 1])))
                   for t in range(40))
        out["random_sources"] = {"updates_checked": 40, "max_identity_residual": worst, "max_abs_C": maxC}
        self.assertEqual(worst, 0)
        # exactly conserved rotor source, C = 0 initial data (fields start at vacuum, source W = 0 for t <= 0)
        osc, wsrc = rotor_source_blocks(Q, kappa=1000)
        blocks2 = [gr.build_metric(Q=Q), osc, wsrc]
        T2 = compose(*blocks2)
        e2 = Engine(T2, Q)
        s = vacuum_state(T2, Q, 8, *blocks2)
        # rotor quadrupole at the centre: O_x = A, O_y = -A, started as (a, b) = (0, A): W(-1) = 0
        s = State(8, s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ))
        n = 4 * 64 + 4 * 8 + 4
        s.b[T2.gear_index("osc.Ox"), n] = 10 ** 6
        s.b[T2.gear_index("osc.Oy"), n] = -10 ** 6
        hist2 = e2.run(s, 63, history=True)
        div = max(og.source_divergence(e2, "metric", hist2[t], hist2[t + 1]) for t in range(1, 61))
        res2 = max(og.lorenz_identity_residual(e2, "metric", hist2[t - 1:t + 3]) for t in range(1, 60))
        maxC2 = [int(max(np.max(np.abs(c)) for c in og.lorenz_C(T2, "metric", hist2[t], hist2[t + 1])))
                 for t in (10, 30, 60)]
        maxh = [int(max(np.max(np.abs(og.arr(hist2[t], T2, f"metric.{c}"))) for c in gr.COMPONENTS))
                for t in (10, 30, 60)]
        out["rotor_conserved_source"] = {"max_source_divergence_t1_60": div, "max_identity_residual": res2,
                                         "max_abs_C_at_10_30_60": maxC2, "max_abs_h_at_10_30_60": maxh}
        self.assertEqual(div, 0)
        self.assertEqual(res2, 0)
        record("G5", out)


def driven_source_blocks(Q, kappa):
    """G5b: exactly conserved source with W(-1) = W(0) = 0: rotors V_i (no input) drive remainder-free gears O_i
    (u = 3Q b(V_i): O(t+1) + O(t-1) = V(t)); W^{0i0i} = O_i, s^00 = kappa Sum D_i^2 a(O_i),
    s^{0i} = -kappa D_i^fwd (b - a)(O_i), s^{ii} = kappa (b(V_i) - 2 b(O_i)) (MECHANISM)."""
    gears = tuple(GearType(f"{p}{s}", "audit") for p in "VO" for s in "xyz")
    why = {"designated_one_way": "MECHANISM: prescribed conserved driven source (G5b)"}
    drv = tuple((f"O{s}", 3 * Q, ((f"V{s}", (0, 0, 0), "b"),), why) for s in "xyz")
    osc = Block(gears, drv, name="osc", vacuum={g.name: 3 * Q - 1 for g in gears}, Q=Q)
    terms = []
    for i, s in enumerate("xyz"):
        e = gr.AXES[i]
        me = tuple(-v for v in e)
        O, V = f"osc.O{s}", f"osc.V{s}"
        terms += [("metric.h00", kappa, ((O, e, "a"),)), ("metric.h00", -2 * kappa, ((O, (0, 0, 0), "a"),)),
                  ("metric.h00", kappa, ((O, me, "a"),))]
        h0 = f"metric.h0{s}"
        terms += [(h0, -kappa, ((O, e, "b"),), why), (h0, kappa, ((O, (0, 0, 0), "b"),), why),
                  (h0, kappa, ((O, e, "a"),)), (h0, -kappa, ((O, (0, 0, 0), "a"),))]
        terms += [(f"metric.h{s}{s}", kappa, ((V, (0, 0, 0), "b"),), why),
                  (f"metric.h{s}{s}", -2 * kappa, ((O, (0, 0, 0), "b"),), why)]
    return osc, Block((), tuple(terms), name="wsrc", Q=Q)


class G05bLorenzC0(unittest.TestCase):
    def test_G5b(self):
        Q = Q0
        osc, wsrc = driven_source_blocks(Q, kappa=1000)
        blocks = [gr.build_metric(Q=Q), osc, wsrc]
        T = compose(*blocks)
        eng = Engine(T, Q)
        L = 8
        s = vacuum_state(T, Q, L, *blocks)
        s = State(L, s.a.astype(OBJ), s.b.astype(OBJ), s.r.astype(OBJ))
        n = (4 * L + 4) * L + 4
        s.b[T.gear_index("osc.Vx"), n] = 10 ** 6
        s.b[T.gear_index("osc.Vy"), n] = -10 ** 6
        s = State(L, s.a, s.b, s.r)
        hist = eng.run(s, 63, history=True)
        div = max(og.source_divergence(eng, "metric", hist[t], hist[t + 1]) for t in range(0, 61))
        res = max(og.lorenz_identity_residual(eng, "metric", hist[t - 1:t + 3]) for t in range(1, 60))
        C = [int(max(np.max(np.abs(c)) for c in og.lorenz_C(T, "metric", hist[t], hist[t + 1]))) for t in range(61)]
        maxh = int(max(np.max(np.abs(og.arr(hist[60], T, f"metric.{c}"))) for c in gr.COMPONENTS))
        record("G5b", {"max_source_divergence": div, "max_identity_residual": res, "C_at_0": C[0],
                       "max_abs_C_0_60": max(C), "C_every_10": C[::10], "max_abs_h_t60": maxh})
        self.assertEqual(div, 0)
        self.assertEqual(res, 0)


# ============================================================================ G6
class G06Gauss(unittest.TestCase):
    def test_G6(self):
        Q, blocks = system_S(with_ref=False)
        T = compose(*blocks)
        eng = Engine(T, Q)
        L = 12
        s = vacuum_state(T, Q, L, *blocks)
        c = (6, 6, 6)
        s = pg.with_load(s, T, "load", Q, 2 * P0 * 3, c, 1.5, 2 ** 10)
        s = pg.with_clocks(s, T, "atA.c", Q, 2 * P0 * 3, [(9, 6, 6)], 2 ** 6)
        hist = eng.run(s, 32, history=True)
        res = {}
        for h in (1, 2, 3):
            m = og.box_mask(L, c, h)
            res[h] = max(og.gauss_residual(eng, "metric.h00", hist[t - 1:t + 2], m) for t in range(1, 31))
        # time-summed (period-mean) form over the window t = 1..30, computed independently from the endpoints
        m = og.box_mask(L, c, 2)
        F = [og.arr(x, T, "metric.h00") for x in hist]
        lhs = 6 * Q * int(np.sum((F[31] - F[30] - F[1] + F[0])[m])) - 2 * (Q - 1) * sum(og.flux(F[t], m)
                                                                                        for t in range(1, 31))
        src = sum(2 * int(np.sum(og.sources(eng, hist[t], ["metric.h00"])["metric.h00"][m])) for t in range(1, 31))
        rr = int(np.sum((og.arr(hist[1], T, "metric.h00", "r") - og.arr(hist[31], T, "metric.h00", "r"))[m]))
        summed = abs(lhs - src - rr)
        flux_mean = sum(og.flux(F[t], m) for t in range(1, 31)) / 30
        src_mean = src / 2 / 30
        record("G6", {"per_update_residual_by_halfwidth": res, "summed_residual": summed,
                      "mean_flux_x(Q-1)": flux_mean * (Q - 1), "mean_source": src_mean})
        for h in (1, 2, 3):
            self.assertEqual(res[h], 0)
        self.assertEqual(summed, 0)


# ============================================================================ G7
class G07OD2(unittest.TestCase):
    def test_G7(self):
        Q, blocks, w = system_od2(with_ref=False)
        T = compose(*blocks)
        eng = Engine(T, Q)
        L = 5
        out = {"stages": [[T.names[g] for g in st] for st in T.stages]}
        s0 = random_state(T, Q, L, 77, PO, big=16, field_hi=4)
        NT = 14
        hist = eng.run(s0, NT, history=True)
        acc = [f"od2.h0{c}" for c in "xyz"] + ["od2.h00"]
        rconst = all(np.array_equal(hist[t].r[T.gear_index(n)], hist[0].r[T.gear_index(n)]) for t in range(NT + 1)
                     for n in acc)
        C = [og.od2_constants(T, "od2", hist[t], hist[t + 1]) for t in range(NT)]
        cdev = max(int(np.max(np.abs(C[t][nu] - C[0][nu]))) for t in range(NT) for nu in range(4))
        out["random_data"] = {"accumulator_r_constant": rconst, "max_C_change": cdev,
                              "max_abs_C": max(int(np.max(np.abs(x))) for x in C[0])}
        self.assertTrue(rconst)
        self.assertEqual(cdev, 0)
        # prepared constraint-satisfying data
        sp = pg.od2_prepare_constraints(s0, T, "od2")
        hp = eng.run(sp, NT, history=True)
        Cp = max(int(np.max(np.abs(x))) for t in range(NT) for x in og.od2_constants(T, "od2", hp[t], hp[t + 1]))
        out["prepared"] = {"max_abs_C_updates": Cp, "updates": NT, "max_bits": hp[-1].max_abs().bit_length()}
        self.assertEqual(Cp, 0)
        # (d) dressed Hamiltonian identity: D_t^2 B00(t) = Div0[ Div(2s(t) + dr(t)) ] (prepared data: C = 0)
        hij = [f"od2.h{a}{b}" for a, b in ("xx", "xy", "xz", "yy", "yz", "zz")]

        def g(st, n, f="b"):
            return og.arr(st, T, n, f)

        def B00(t):
            return og.box(Q, g(hp[t - 1], "od2.h00"), g(hp[t], "od2.h00"), g(hp[t + 1], "od2.h00"))

        def comp(i, j):
            a_, b_ = sorted((i, j))
            return f"od2.h{'xyz'[a_]}{'xyz'[b_]}"
        worst = 0
        for t in range(2, NT - 3):
            src = og.sources(eng, hp[t], hij)
            Y = {n: 2 * src[n] + g(hp[t], n, "r") - g(hp[t + 1], n, "r") for n in hij}
            divs = []
            for i in range(3):
                d = og.sh(Y[comp(i, i)], gr.AXES[i]) - Y[comp(i, i)]
                for j in range(3):
                    if j != i:
                        d = d + Y[comp(j, i)] - og.sh(Y[comp(j, i)], tuple(-v for v in gr.AXES[j]))
                divs.append(d)
            rhs = sum(divs[i] - og.sh(divs[i], tuple(-v for v in gr.AXES[i])) for i in range(3))
            lhs = B00(t + 2) - 2 * B00(t + 1) + B00(t)
            worst = max(worst, int(np.max(np.abs(lhs - rhs))))
        out["hamiltonian_dressed_identity_max_residual"] = worst
        self.assertEqual(worst, 0)
        record("G7", out)


# ============================================================================ G8
class G08Tmunu(unittest.TestCase):
    def test_G8(self):
        Q, mu = 51, 3
        spec = gr.kg_spec("kg", Q, mu)
        blk = gr.build_test_matter(spec, Q=Q)
        T = compose(blk)
        eng = Engine(T, Q)
        L = 6
        rng = np.random.default_rng(8)
        s = State(L, rng.integers(-10 ** 5, 10 ** 5, (1, L ** 3)), rng.integers(-10 ** 5, 10 ** 5, (1, L ** 3)),
                  rng.integers(0, 6 * Q, (1, L ** 3)))
        hist = eng.run(s, 12, history=True)
        worst_e = worst_p = 0
        for t in range(0, 10):
            re, rp = og.tmunu_residuals(Q, Q - 1, 6 - mu, hist[t], hist[t + 1], hist[t + 2], hist[t + 3], T, "kg.K")
            worst_e, worst_p = max(worst_e, re), max(worst_p, rp)
        record("G8", {"Q": Q, "mu": mu, "windows": 10, "max_energy_residual": worst_e,
                      "max_momentum_residual": worst_p})
        self.assertEqual(worst_e, 0)
        self.assertEqual(worst_p, 0)


# ============================================================================ G9
class G09Support(unittest.TestCase):
    def test_G9(self):
        """support_violations() per block: each block's own terms in a tensor with all the system's gears."""
        out = {}
        for name, mk in ALL_SYSTEMS.items():
            Q, blocks = mk()
            per_block = {}
            for blk in blocks:
                only = [Block(b.gears, b.terms if b is blk else (), name=b.name, vacuum=b.vacuum, Q=b.Q)
                        for b in blocks]
                rep = og.support_report(compose(*only))
                if rep:
                    per_block[blk.name] = {"total": sum(rep.values()),
                                           "families": {f"{k[0]} <- {list(k[1])}": v for k, v in sorted(rep.items())}}
            out[name] = per_block
        record("G9", out)


# ============================================================================ G10
class G10StaggeredReversor(unittest.TestCase):
    def test_G10(self):
        Q, blocks, w = system_od2(with_ref=False)
        T = compose(*blocks)
        eng = Engine(T, Q)
        L = 4
        out = {}
        for mm in ("M", "Mp"):
            X = og.od2_staggered_reversor(T, Q, "od2", {"dir.X": mm, "dir.Y": mm})
            states = [random_state(T, Q, L, 300 + j, PO, big=16, field_hi=4) for j in range(10)]
            negm = uniform(T, Q, "id")
            from research.metric_variant_v1.core.reversors import GearwiseMap
            Z = GearwiseMap(T, Q, {"dir.X": "J", "dir.Y": "J"})
            rep1 = reversor_check(X, eng, states, 1)
            rep = reversor_check(X, eng, states, 12, central=[("matter_sign", Z)])
            out[mm] = {"n1": rep1, "n12": rep}
        record("G10", out)
        # outcome reported either way (CONJECTURE test); no assertion


if __name__ == "__main__":
    unittest.main()

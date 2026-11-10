"""Stage-0 tests T0.8-T0.10 (reciprocity checker, compose/namespaces, links-frozen hook); pre-registered in NOTES.md.

Run from the repository root:
    python -m unittest research.metric_variant_v1.tests.test_layers -v
"""
from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from research.metric_variant_v1.core import (Block, Engine, GearType, State, Tensor, build, check_reciprocity,
                                             compose, reference_block)
from research.metric_variant_v1.core.lattice import DIRECTIONS, OFFSETS, ZERO
from research.metric_variant_v1.layers import build_reference
from research.metric_variant_v1.observe.audit import frozen_equivalence
from research.metric_variant_v1.prepare import insert_reference, vacuum_state
from research.metric_variant_v1.tests import randgen
from research.metric_variant_v1.tests.test_core import record, ref_random_state


def gradient_terms(potential, signs=None):
    """u_g = s_g dPhi/db_g for Phi = sum_x sum_P phi_P P(x); P = list of (gear, offset) (B3-local)."""
    terms = []
    for phi, P in potential:
        for g, p in sorted(set(P)):
            n = P.count((g, p))
            rest = [(gg, tuple(o[i] - p[i] for i in range(3))) for gg, o in P]
            rest.remove((g, ZERO))
            s = 1 if signs is None else signs.get(g, 1)
            terms.append((g, s * n * phi, tuple((gg, o, "b") for gg, o in rest)))
    return terms


def random_potential(seed, names, n_terms=25, max_degree=4):
    rng = random.Random(seed)
    pot = []
    for _ in range(n_terms):
        k = rng.randint(2, max_degree)
        offs = randgen._local_offsets(rng, k)
        pot.append((rng.choice([v for v in range(-9, 10) if v]), [(rng.choice(names), o) for o in offs]))
    return pot


class T08Reciprocity(unittest.TestCase):
    def test_T08(self):
        out = {}
        # (a) reference block, Q = 1 and 7
        for Q in (1, 7):
            rep = check_reciprocity(build(reference_block(Q)))
            out[f"a_reference_Q{Q}"] = (rep.ok, rep.checked)
            self.assertTrue(rep.ok)
            self.assertEqual(rep.checked, 288)
        # (f) all eight body-sign choices
        for signs in [(sx, sy, sz) for sx in (1, -1) for sy in (1, -1) for sz in (1, -1)]:
            rep = check_reciprocity(build(reference_block(1, signs)))
            out[f"f_reference_signs_{signs}"] = rep.ok
            self.assertTrue(rep.ok, signs)
        # (b) symmetric random linear part
        names = [f"g{i}" for i in range(6)]
        for seed in range(5):
            T = Tensor(names, randgen.symmetric_linear_terms(random.Random(seed), names, 7, 6, 12))
            rep = check_reciprocity(T)
            out[f"b_sym_linear_seed{seed}"] = (rep.ok, rep.checked)
            self.assertTrue(rep.ok)
            self.assertGreater(rep.checked, 0)
        # (c) gradient of a random cubic+quartic potential; (d) delete one partner
        for seed in range(5):
            T = Tensor(names, gradient_terms(random_potential(100 + seed, names)))
            rep = check_reciprocity(T)
            out[f"c_gradient_seed{seed}"] = (rep.ok, rep.checked, T.rank)
            self.assertTrue(rep.ok, rep.violations[:3])
            # a monomial that HAS a partner: its potential monomial has >= 2 distinct variables (a self-term such as
            # dPhi/db of b^3 is its own partner; deleting it leaves an exact gradient, which the checker accepts)
            victim = random.Random(seed).choice([m for m in T.monomials if m.degree >= 1 and
                                                 any((f.gear, f.offset) != (m.target, ZERO) for f in m.factors)])
            T2 = Tensor(names, [m for m in T.monomials if m is not victim])
            rep2 = check_reciprocity(T2)
            out[f"d_delete_one_seed{seed}"] = (rep2.ok, len(rep2.violations), len(rep2.missing_partners))
            self.assertFalse(rep2.ok)
            self.assertGreaterEqual(len(rep2.missing_partners), 1)
            # the listed violations are exactly the surviving members of the victim's class
            from research.metric_variant_v1.core.reciprocity import _canon
            vcls = _canon([(victim.target, ZERO)] + [(f.gear, f.offset) for f in victim.factors])
            same = [m for m in T2.monomials if m.degree >= 1 and
                    _canon([(m.target, ZERO)] + [(f.gear, f.offset) for f in m.factors]) == vcls]
            self.assertEqual(len(rep2.violations), len(same))
        # (d') deleting a self-partnered monomial (single distinct variable) leaves an exact gradient
        T = Tensor(["g0"], gradient_terms([(4, [("g0", ZERO)] * 3)]))
        self.assertEqual(len(T), 1)
        self.assertTrue(check_reciprocity(T).ok)
        self.assertTrue(check_reciprocity(Tensor(["g0"], [])).ok)
        out["d_prime_self_term"] = True
        # (e) one-way detector term
        det = [("det", 3, (("m", ZERO, "b"), ("m", ZERO, "b")))]
        rep = check_reciprocity(Tensor(["m", "det"], det))
        out["e_detector_undesignated"] = rep.ok
        self.assertFalse(rep.ok)
        des = [("det", 3, (("m", ZERO, "b"), ("m", ZERO, "b")), {"designated_one_way": "passive |psi|^2 detector"})]
        T = Tensor(["m", "det"], des)
        rep = check_reciprocity(T)
        out["e_detector_designated"] = (rep.ok, rep.designated)
        self.assertTrue(rep.ok)
        self.assertEqual(Tensor.from_dict(T.to_dict()), T)
        # (g) field signs: Phi = 5 b0 b1, u0 = +dPhi/db0, u1 = -dPhi/db1
        terms = [("p0", 5, (("p1", ZERO, "b"),)), ("p1", -5, (("p0", ZERO, "b"),))]
        rep_plain = check_reciprocity(Tensor(["p0", "p1"], terms))
        rep_signed = check_reciprocity(Tensor([GearType("p0"), GearType("p1", sign=-1, sign_why="T0.8(g) test")],
                                              terms))
        out["g_field_sign"] = (rep_plain.ok, rep_signed.ok)
        self.assertFalse(rep_plain.ok)
        self.assertTrue(rep_signed.ok)
        self.assertEqual(rep_signed.negative_sign_gears, [("p1", "T0.8(g) test")])
        record("T0.8", {"cases": {k: str(v) for k, v in out.items()}})


class T09Compose(unittest.TestCase):
    def test_T09(self):
        A = Block((GearType("x"), GearType("y")), (("x", 2, (("y", (1, 0, 0), "b"),)),), name="A")
        B = Block((GearType("z", "audit"),), (("z", 1, (("A.x", ZERO, "b"), ("z", ZERO, "b"))),
                                               ("A.y", 3, (("z", (0, 0, -1), "b"),))), name="B")
        T = compose(A, B)
        self.assertEqual(T.names, ("A.x", "A.y", "B.z"))
        self.assertEqual(len(T), 3)
        with self.assertRaises(ValueError):
            compose(Block((GearType("p.q"),), (), name="C"))
        with self.assertRaises(ValueError):
            compose(A, Block((GearType("w"),), (("w", 1, (("A.nope", ZERO, "b"),)),), name="D"))
        with self.assertRaises(ValueError):
            compose(A, Block((GearType("w"),), (), name="A"))
        ref_ns = compose(build_reference(Q=1, name="ref"))
        ref_plain = build(reference_block(1))
        self.assertTrue(ref_ns.same_dynamics(ref_plain))
        self.assertEqual(ref_ns.dynamics_fingerprint, ref_plain.dynamics_fingerprint)
        self.assertEqual(ref_ns.names[0], "ref.R00")
        s0 = randgen.random_state(9, 48, 4, 6, -30, 30)
        e1, e2 = Engine(ref_ns, 1), Engine(ref_plain, 1)
        s1, s2 = s0, s0
        bad = 0
        for _ in range(10):
            s1, s2 = e1.step(s1), e2.step(s2)
            bad += 0 if s1.same_as(s2) else 1
        self.assertEqual(bad, 0)
        record("T0.9", {"names": list(T.names), "reference_namespaced_same_dynamics": True, "run_mismatches": bad})


def link_stub(Q, kappa, name="links", pairs=((0, 5), (3, 17), (11, 40))):
    """TEST STUB (not the G9-c design): three Yee link gears W0, W1, W2 per node; potential
    Phi = kappa*Q * sum_k sum_(h,g) b[W_k](x) b[ref.R_h](x) b[ref.R_g](x + e_k): reciprocal rank-3 hopping."""
    gears = tuple(GearType(f"W{k}", "audit", link=k) for k in range(3))
    pot = []
    for k in range(3):
        e = DIRECTIONS[2 * k]
        for h, g in pairs:
            pot.append((kappa * Q, [(f"{name}.W{k}", ZERO), (f"ref.R{h:02d}", ZERO), (f"ref.R{g:02d}", e)]))
    terms = [t for t in gradient_terms(pot) if t[1] != 0]
    local = []
    for target, c, facs in terms:
        local.append((target, c, facs))
    return Block(gears, tuple(local), name=name, vacuum={f"W{k}": 3 * Q for k in range(3)},
                 params={"Q": Q, "kappa": kappa}, doc="test stub for the links-frozen hook")


class T10LinksFrozen(unittest.TestCase):
    def test_T10(self):
        Q, L, steps = 7, 4, 30
        ref = build_reference(Q=Q, name="ref")
        rs = ref_random_state(1010, L, -20, 20)
        t_ref = compose(ref)
        base_state = insert_reference(vacuum_state(t_ref, Q, L, ref), t_ref, rs, Q)
        out = {}
        for kappa in (0, 1):
            stub = link_stub(Q, kappa)
            # the kappa = 1 control is a rank-3 coupling without a spring: its values grow doubly exponentially, so it
            # runs only 2 updates (a difference appears at update 1)
            res = frozen_equivalence((ref,), (stub,), Q, base_state, steps if kappa == 0 else 2)
            rep = check_reciprocity(compose(ref, stub))
            out[f"kappa={kappa}"] = {**res, "reciprocal": rep.ok, "link_gear_links": [0, 1, 2]}
            if kappa == 0:
                self.assertTrue(res["frozen"], res)
                self.assertEqual(res["monomials_full"], res["monomials_base"])
            else:
                self.assertFalse(res["frozen"], res)
                self.assertGreater(res["monomials_full"], res["monomials_base"])
            self.assertTrue(rep.ok)
        record("T0.10", out)


if __name__ == "__main__":
    unittest.main()

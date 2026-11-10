"""Stage 0.2 review items (pre-registered in NOTES.md): T0.14 ONE Q (R1) and field-sign justifications (R2);
T0.15 the L0 mirror rho_L0 (R-M2 theorem) with the Q-lattice validator.

Run from the repository root:
    python -m unittest research.metric_variant_v1.tests.test_stage02_review -v
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

from research.metric_variant_v1.core import (Engine, GearType, State, Tensor, build, check_reciprocity, compose,
                                             reference_block, reference_names)
from research.metric_variant_v1.core.engine import OBJ
from research.metric_variant_v1.core.lattice import DIRECTIONS, ZERO
from research.metric_variant_v1.core.reversors import (GearwiseMap, is_fixed, remainder_map, reversor_check)
from research.metric_variant_v1.core.tensor import Block
from research.metric_variant_v1.layers import build_reference
from research.metric_variant_v1.prepare import vacuum_state
from research.metric_variant_v1.tests import randgen
from research.metric_variant_v1.tests.test_core import record
from universe24.observation.diagnostics import time_reverse
from universe24.core.state import Channel, Cube, State as RefState


class T14OneQAndSigns(unittest.TestCase):
    def test_T14a_one_Q(self):
        out = {}
        ref7 = build_reference(Q=7, name="ref")
        t7 = compose(ref7)
        self.assertEqual(t7.Q, 7)
        with self.assertRaises(ValueError):
            Engine(t7, 5)
        out["Q7_block_under_Engine_Q5"] = "raises"
        with self.assertRaises(ValueError):
            compose(ref7, Block((GearType("x"),), (), name="new", Q=5))
        out["compose_Q7_with_Q5"] = "raises"
        with self.assertRaises(ValueError):
            vacuum_state(t7, 5, 4, ref7)
        with self.assertRaises(ValueError):
            vacuum_state(compose(Block((GearType("x"),), (), name="n0")), 5, 4, ref7)
        out["vacuum_state_mismatch"] = "raises"
        Engine(t7, 7)
        vacuum_state(t7, 7, 4, ref7)
        free = Block((GearType("x"),), (("x", 3, (("ref.R00", ZERO, "b"),)),), name="new")   # Q-independent
        t = compose(ref7, free)
        self.assertEqual(t.Q, 7)
        self.assertEqual(Tensor.from_dict(t.to_dict()).Q, 7)
        out["Q_None_block_with_Q7"] = "tensor.Q = 7"
        raw = Tensor(["g"], [("g", 1, (("g", DIRECTIONS[0], "b"),))])
        for Q in (1, 5, 9):
            Engine(raw, Q)
        out["undeclared_tensor_any_Q"] = "runs"
        self.assertEqual(build(reference_block(3)).Q, 3)
        record("T0.14a", out)

    def test_T14b_field_signs(self):
        out = {}
        with self.assertRaises(ValueError):
            GearType("p", sign=-1)
        with self.assertRaises(ValueError):
            Tensor([{"name": "p", "sign": -1}], [])
        with self.assertRaises(ValueError):
            Tensor.from_dict({"format": "metric_variant_v1/tensor/1", "gears": [{"name": "p", "sign": -1}],
                              "monomials": []})
        out["sign_-1_without_justification"] = "raises (GearType, dict input, from_dict)"
        gears = [GearType("a0"), GearType("a1", sign=-1, sign_why="time-like component (test)"),
                 GearType("a2"), GearType("a3", sign=-1, sign_why="second test reason")]
        terms = [("a0", 4, (("a1", ZERO, "b"),)), ("a1", -4, (("a0", ZERO, "b"),)),
                 ("a2", 1, (("a3", ZERO, "b"),)), ("a3", -1, (("a2", ZERO, "b"),))]
        T = Tensor(gears, terms)
        rep = check_reciprocity(T)
        self.assertTrue(rep.ok)
        self.assertEqual(rep.negative_sign_gears, [("a1", "time-like component (test)"), ("a3", "second test reason")])
        self.assertEqual(check_reciprocity(build(reference_block(1))).negative_sign_gears, [])
        self.assertEqual(Tensor.from_dict(T.to_dict()), T)
        out["report_lists"] = rep.negative_sign_gears
        record("T0.14b", out)


def two_layer_system(Q, seed, back_mult=None, n_new=4):
    """L0 (reference, Q-scaled) + a new b-only node layer with couplings both ways. Back-coupling coefficients are
    multiples of Q unless back_mult is given (control)."""
    rng = random.Random(seed)
    new = [f"n{i}" for i in range(n_new)]
    terms = randgen.symmetric_linear_terms(rng, new, Q, 6, pairs=2 * n_new)
    refs = list(reference_names())
    for t in new:
        for _ in range(3):
            o = randgen._local_offsets(rng, 2)
            terms.append((t, rng.choice((-3, -2, -1, 1, 2, 3)), (("ref." + rng.choice(refs), o[0], "b"),
                                                                  (rng.choice(new), o[1], "b"))))
    back = []
    for _ in range(12):
        o = randgen._local_offsets(rng, 2)
        c = rng.choice((-2, -1, 1, 2)) * (Q if back_mult is None else back_mult)
        back.append(("ref." + rng.choice(refs), c, (("new." + rng.choice(new), o[0], "b"),
                                                    ("ref." + rng.choice(refs), o[1], "b"))))
    blk = Block(tuple(GearType(n, "audit") for n in new), tuple(terms), name="new", Q=Q,
                vacuum={n: 3 * Q - 1 for n in new})
    return build_reference(Q=Q, name="ref"), blk, Block((), tuple(back), Q=Q)


class T15RhoL0(unittest.TestCase):
    def test_T15a_rho_map(self):
        out = {}
        for Q in (1, 3, 7):
            D = 6 * Q
            r = np.arange(D, dtype=object)
            rho = remainder_map("rhoL0", r, D)
            self.assertTrue(all(0 <= v < D for v in rho))
            self.assertTrue(np.array_equal(remainder_map("rhoL0", rho, D), r))       # involution
            tr = [time_reverse(RefState(Cube(3), Channel(0, 0, k))).background.r for k in range(6)]
            self.assertEqual([int(remainder_map("rhoL0", np.array([Q * k], dtype=object), D)[0]) for k in range(6)],
                             [Q * v for v in tr])
            self.assertEqual(int(remainder_map("rhoL0", np.array([2 * Q], dtype=object), D)[0]), 2 * Q)
            out[f"Q{Q}"] = {"involution": True, "equals_Q_time_reverse": True, "fixes_2Q": True,
                            "Mp_of_2Q": int(remainder_map("Mp", np.array([2 * Q], dtype=object), D)[0])}
        record("T0.15a", out)

    def test_T15b_joint_reversor(self):
        out = {}
        L, n = 4, 12
        for Q in (1, 3, 7):
            ref, new, back = two_layer_system(Q, 1500 + Q)
            T = compose(ref, new, back, q_lattice=("ref.*",))      # validator passes
            eng = Engine(T, Q)
            choices = {nm: ("rhoL0" if nm.startswith("ref.") else "Mp") for nm in T.names}
            X = GearwiseMap(T, Q, choices)
            vac = vacuum_state(T, Q, L, ref, new)
            states = []
            for k in range(3):
                s = randgen.random_state(1600 + 10 * Q + k, T.G, L, 6 * Q, -9, 9)
                if k < 2:          # L0 remainders on the Q-lattice
                    r = s.r.astype(OBJ)
                    r[:48] = Q * randgen.random_state(1700 + k, 48, L, 6, 0, 0).r.astype(OBJ)
                    s = State(L, s.a, s.b, r)
                states.append(s)
            chk = reversor_check(X, eng, states, n)
            self.assertEqual(chk["identity"], 3, (Q, chk))
            self.assertTrue(is_fixed(X, vac))
            lattice_ok = True
            s = states[0]
            for _ in range(n):
                s = eng.step(s)
                lattice_ok &= bool(np.all(s.r[:48] % Q == 0))
            self.assertTrue(lattice_ok)
            # control 1: R' on L0 does not fix the vacuum for Q > 1
            Xp = GearwiseMap(T, Q, {nm: "Mp" for nm in T.names})
            vac_fixed_Mp = is_fixed(Xp, vac)
            self.assertEqual(vac_fixed_Mp, Q == 1)
            # control 2: a back-coupling coefficient not = 0 mod Q
            ctrl = None
            if Q > 1:
                ref2, new2, back2 = two_layer_system(Q, 1500 + Q, back_mult=1)
                with self.assertRaises(ValueError):
                    compose(ref2, new2, back2, q_lattice=("ref.*",))
                T2 = compose(ref2, new2, back2)
                self.assertGreater(len(T2.q_lattice_violations(("ref.*",))), 0)
                X2 = GearwiseMap(T2, Q, {nm: ("rhoL0" if nm.startswith("ref.") else "Mp") for nm in T2.names})
                ctrl = reversor_check(X2, Engine(T2, Q), states, n)
                self.assertGreater(ctrl["failures"], 0)
            out[f"Q{Q}"] = {"monomials": len(T), "reversor": chk, "joint_vacuum_fixed": True,
                            "L0_remainders_stay_on_Q_lattice": lattice_ok, "Mp_on_L0_fixes_vacuum": vac_fixed_Mp,
                            "control_back_coupling_not_mod_Q": ctrl}
        record("T0.15b", out)


if __name__ == "__main__":
    unittest.main()

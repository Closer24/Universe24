"""Exact resolution embedding: histories, staged inverse and passive clicks."""
from __future__ import annotations

import unittest

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.core.tensor import GearType, compose
from universe24.layers.resolution import lift_tensor
from universe24.prepare.resolution import lift_state, unlift_state

ZERO = (0, 0, 0)
PLUS_X = (1, 0, 0)


def nonlinear_fixture(Q=5):
    """Includes constants, degrees 1..3, a face link and three inverse stages."""
    f = lambda g, field="b", offset=ZERO: (g, offset, field)
    gears = [GearType("root"),
             GearType("middle", sign=-1, sign_why="metadata preservation fixture"),
             GearType("leaf", label="audit", link=0), GearType("fixed")]
    quadratic = (f("root", "a", PLUS_X), f("root"))
    terms = [("root", 1, ()),
             ("root", 3 * Q - 1, (f("root"),)),
             ("root", 1, (f("root", offset=PLUS_X),)),
             ("middle", 3 * Q, (f("middle"),)),
             ("middle", -1, quadratic),
             ("leaf", 3 * Q, (f("leaf"),)),
             ("leaf", 1, (f("root", "a"), f("middle", "a"), f("root"))),
             ("fixed", 6 * Q, (f("fixed"),))]
    tensor = Tensor(gears, terms, Q=Q,
                    designated_one_way=[("middle", quadratic, "test-only declared feedforward term")])
    rng = np.random.default_rng(934)
    a = rng.integers(-2, 3, size=(4, 27))
    b = rng.integers(-2, 3, size=(4, 27))
    r = rng.integers(0, 6 * Q, size=(4, 27))
    a[3] = b[3] = 1
    r[3] = 6 * Q - 1
    return tensor, State(3, a, b, r)


class ResolutionTests(unittest.TestCase):
    def assert_clicks_equal(self, left, right):
        self.assertEqual(left.rows(), right.rows())
        np.testing.assert_array_equal(left.changed, right.changed)
        np.testing.assert_array_equal(left.quotient, right.quotient)
        np.testing.assert_array_equal(left.kind, right.kind)

    def test_nonlinear_history_inverse_and_clicks_commute(self):
        for Q in (1, 5):
            for factor in (2, 2 ** 90 + 3):
                with self.subTest(Q=Q, factor=factor):
                    tensor, seed = nonlinear_fixture(Q)
                    lifted = lift_tensor(tensor, factor)
                    self.assertEqual(tensor.rank, 4)
                    self.assertGreater(len(tensor.stages), 1)
                    self.assertEqual(lifted.stages, tensor.stages)
                    source_engine = Engine(tensor, Q)
                    lifted_engine = Engine(lifted, factor * Q)
                    source, scaled = seed, lift_state(seed, tensor, factor)
                    source_history, scaled_history = [source], [scaled]
                    for tick in range(1, 9):
                        next_source = source_engine.step(source)
                        next_scaled = lifted_engine.step(scaled)
                        self.assertTrue(next_scaled.same_as(lift_state(next_source, tensor, factor)))
                        self.assertTrue(unlift_state(next_scaled, tensor, factor).same_as(next_source))
                        for stream in ("official", "raw"):
                            self.assert_clicks_equal(
                                source_engine.clicks(source, next_source, tick, stream),
                                lifted_engine.clicks(scaled, next_scaled, tick, stream))
                        # Fixed nonzero quotient rows are suppressed only in the
                        # official stream, identically before and after lifting.
                        raw = lifted_engine.clicks(scaled, next_scaled, tick, "raw")
                        self.assertTrue(np.any(~raw.changed))
                        source, scaled = next_source, next_scaled
                        source_history.append(source)
                        scaled_history.append(scaled)
                    for previous_source, previous_scaled in zip(
                            reversed(source_history[:-1]), reversed(scaled_history[:-1])):
                        source = source_engine.inverse_step(source)
                        scaled = lifted_engine.inverse_step(scaled)
                        self.assertTrue(source.same_as(previous_source))
                        self.assertTrue(scaled.same_as(previous_scaled))
                        self.assertTrue(scaled.same_as(lift_state(source, tensor, factor)))

    def test_metadata_source_and_identity_factor_preserved(self):
        tensor, seed = nonlinear_fixture()
        source_json, original_seed = tensor.to_json(), seed.copy()
        lifted = lift_tensor(tensor, 7)
        self.assertEqual(lifted.gears, tensor.gears)
        self.assertEqual(lifted.designations, tensor.designations)
        self.assertEqual(lifted.census(), tensor.census())
        self.assertEqual(lifted.support_violations(), [
            m for m in lifted.monomials if (m.target, m.factors) in
            {(n.target, n.factors) for n in tensor.support_violations()}])
        self.assertEqual(lifted.rank, tensor.rank)
        self.assertEqual(lifted.Q, 7 * tensor.Q)
        for old, new in zip(tensor.monomials, lifted.monomials):
            self.assertEqual((new.target, new.factors), (old.target, old.factors))
            self.assertEqual(new.coeff, 7 * old.coeff)
        self.assertEqual(lift_tensor(tensor, 1), tensor)
        lifted_seed = lift_state(seed, tensor, 1)
        self.assertTrue(lifted_seed.same_as(seed))
        for original, copy in zip((seed.a, seed.b, seed.r),
                                  (lifted_seed.a, lifted_seed.b, lifted_seed.r)):
            self.assertFalse(np.shares_memory(original, copy))
        self.assertEqual(tensor.to_json(), source_json)
        self.assertTrue(seed.same_as(original_seed))

    def test_explicit_Q_required_for_unannotated_tensor(self):
        annotated, seed = nonlinear_fixture()
        tensor = Tensor(annotated.gears, annotated.monomials)
        with self.assertRaises(ValueError):
            lift_tensor(tensor, 2)
        with self.assertRaises(ValueError):
            lift_state(seed, tensor, 2)
        lifted = lift_tensor(tensor, 2, Q=5)
        scaled = lift_state(seed, tensor, 2, Q=5)
        self.assertEqual(lifted.Q, 10)
        self.assertTrue(unlift_state(scaled, tensor, 2, Q=5).same_as(seed))
        self.assertTrue(Engine(lifted, 10).step(scaled).same_as(
            lift_state(Engine(tensor, 5).step(seed), tensor, 2, Q=5)))

    def test_invalid_factor_Q_state_and_image_rejected(self):
        tensor, seed = nonlinear_fixture()
        for factor in (0, -1, True, 2.0, "2", None):
            for fn in (lambda: lift_tensor(tensor, factor),
                       lambda: lift_state(seed, tensor, factor),
                       lambda: unlift_state(seed, tensor, factor)):
                with self.subTest(factor=factor), self.assertRaises(ValueError):
                    fn()
        for Q in (0, -1, True, 5.0, 6):
            for fn in (lambda: lift_tensor(tensor, 2, Q=Q),
                       lambda: lift_state(seed, tensor, 2, Q=Q),
                       lambda: unlift_state(seed, tensor, 2, Q=Q)):
                with self.subTest(Q=Q), self.assertRaises(ValueError):
                    fn()
        with self.assertRaises(TypeError):
            lift_tensor(None, 2)
        for fn in (lift_state, unlift_state):
            with self.assertRaises(TypeError):
                fn(None, tensor, 2)
            wrong_G = State(3, seed.a[:1], seed.b[:1], seed.r[:1])
            with self.assertRaises(ValueError):
                fn(wrong_G, tensor, 2)
        for value in (-1, 30):
            bad = seed.copy()
            bad.r[0, 0] = value
            with self.assertRaises(ValueError):
                lift_state(bad, tensor, 2)
        for value in (-1, 60, 1):
            bad = lift_state(seed, tensor, 2)
            bad.r[0, 0] = value
            with self.assertRaises(ValueError):
                unlift_state(bad, tensor, 2)

    def test_new_interaction_can_leave_the_embedding(self):
        tensor = Tensor(["node"], [], Q=1)
        seed = State(3, [[0] * 27], [[0] * 27], [[0] * 27])
        lifted = lift_tensor(tensor, 3)
        # An unscaled constant is new dynamics, not part of the exact lift.
        coupled = Tensor(lifted.gears, [("node", 1, ())], Q=lifted.Q)
        scaled = lift_state(seed, tensor, 3)
        coupled_next = Engine(coupled, coupled.Q).step(scaled)
        self.assertEqual(int(coupled_next.r[0, 0]), 2)
        with self.assertRaises(ValueError):
            unlift_state(coupled_next, tensor, 3)

    def test_default_tensor_frozen_seed_and_history(self):
        from universe24.layers.one import one_system
        from universe24.prepare.one import one_seed

        system = one_system()
        tensor = compose(*system.blocks)
        fingerprint = tensor.fingerprint
        seed, _ = one_seed(system, tensor, 3, bang="none")
        factor = 2
        lifted = lift_tensor(tensor, factor)
        source_engine, scaled_engine = Engine(tensor, system.Q), Engine(lifted, factor * system.Q)
        source, scaled = seed, lift_state(seed, tensor, factor)
        self.assertEqual(int(scaled.r[0, 0]), factor * (3 * system.Q - 1))
        self.assertNotEqual(int(scaled.r[0, 0]), 3 * factor * system.Q - 1)
        for tick in range(1, 4):
            source_next, scaled_next = source_engine.step(source), scaled_engine.step(scaled)
            self.assertTrue(scaled_next.same_as(lift_state(source_next, tensor, factor)))
            self.assert_clicks_equal(source_engine.clicks(source, source_next, tick),
                                     scaled_engine.clicks(scaled, scaled_next, tick))
            source, scaled = source_next, scaled_next
        self.assertTrue(scaled_engine.rewind(scaled, 3).same_as(lift_state(seed, tensor, factor)))
        self.assertEqual(tensor.fingerprint, fingerprint)
        self.assertEqual(compose(*one_system().blocks), tensor)


if __name__ == "__main__":
    unittest.main()

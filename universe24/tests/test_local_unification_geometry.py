"""Exact tests for the source-coupled finite-chart geometry extension."""
from copy import deepcopy
from fractions import Fraction
import unittest

import numpy as np

from universe24.core import Engine
from validation.local_unification import geometry


class LocalUnificationGeometryTests(unittest.TestCase):
    def test_all_symbolic_einstein_balance_and_affine_components(self):
        proof = geometry.symbolic_certificate()
        self.assertTrue(proof["all_exact_residuals_zero"])
        self.assertEqual(proof["Einstein_component_identities"], 16)
        self.assertEqual(proof["covariant_balance_identities"], 4)
        self.assertEqual(proof["affine_null_geodesic_components"], 8)

    def test_exact_spline_source_identity_is_not_sample_differencing(self):
        q = [0, 1, 0, 2, 1, 0, 0, 1, 0]
        coefficients = geometry.antiderivative(q, height=100)
        for x in (Fraction(5, 2), Fraction(3), Fraction(13, 4), Fraction(5)):
            self.assertEqual(
                geometry.reconstruct(coefficients, x, derivative=2),
                -geometry.reconstruct(q, x, degree=1))
            self.assertGreater(geometry.reconstruct(coefficients, x), 0)
            self.assertGreaterEqual(geometry.reconstruct(q, x, degree=1), 0)
        self.assertEqual(geometry.b3(1), Fraction(1, 6))
        self.assertEqual(geometry.b3(0), Fraction(2, 3))
        self.assertNotEqual(geometry.reconstruct(coefficients, 3), coefficients[3])

    def test_same_twelve_channel_engine_has_causal_source_chart_and_inverse(self):
        law, seed, protocol = geometry.prepare_fixture(L=11, steps=2)
        self.assertEqual(law.G, 12)
        self.assertEqual(law.rank-1, 3)
        self.assertEqual(law.support_violations(), [])
        engine = Engine(law)
        state, ideal = seed, seed.b.copy()
        coords = geometry._axis_coordinate(seed.L, protocol["direction"])
        for tick in range(3):
            safe = (coords >= tick+1) & (coords <= seed.L-2-tick)
            self.assertTrue(np.array_equal(state.b[:, safe], ideal[:, safe]))
            self.assertFalse(any(geometry.profile_constraints(state)[:, safe].flat))
            if tick % 2 == 0:
                output = geometry.readout(state, tick, protocol)
                self.assertEqual(output["source_curvature_residual"], (0, 0))
                self.assertGreater(output["R"], 0)
            if tick < 2:
                following = engine.step(state)
                self.assertTrue(engine.inverse_step(following).same_as(state))
                self.assertTrue(np.array_equal(following.r, seed.r))
                state = following
                ideal = geometry.ideal_step(ideal, seed.L)
        self.assertTrue(engine.rewind(state, 2).same_as(seed))
        wrong = Engine(geometry.build_tensor(source_coupling=False))
        broken = wrong.run(seed, 2)
        self.assertTrue(wrong.rewind(broken, 2).same_as(seed))
        with self.assertRaisesRegex(ValueError, "source/curvature"):
            geometry.readout(broken, 2, protocol)

    def test_scope_and_exact_input_validation(self):
        law, seed, protocol = geometry.prepare_fixture(L=11, steps=2)
        with self.assertRaises(ValueError):
            geometry.prepare_fixture(L=9, steps=2)
        for tick in (True, 1, 4):
            with self.assertRaises(ValueError):
                geometry.readout(seed, tick, protocol)
        for coordinate in (0, 2, 5.0, True):
            with self.assertRaises(ValueError):
                geometry.readout(seed, 0, protocol, coordinate=coordinate)
        bad = seed.copy()
        bad.b[8, 0] += 1
        with self.assertRaisesRegex(ValueError, "plane-symmetric"):
            geometry.readout(bad, 0, protocol)
        bad = seed.copy()
        bad.a[0, 0] += 1
        with self.assertRaises(ValueError):
            geometry.readout(bad, 0, protocol)
        for bad_value in (1.5, True):
            bad = seed.copy()
            bad.b = bad.b.astype(object)
            bad.b[8, 0] = bad_value
            with self.assertRaises(ValueError):
                geometry.readout(bad, 0, protocol)
            with self.assertRaises(ValueError):
                geometry.reconstruct([bad_value], 0)
        for name, value in (("microsteps", True), ("ticks_per_macro", True),
                            ("safe_coefficient_margin", 1),
                            ("collision_coupled", 1)):
            bad_protocol = deepcopy(protocol)
            bad_protocol[name] = value
            with self.assertRaises(ValueError):
                geometry.readout(seed, 0, bad_protocol)
        bad_protocol = deepcopy(protocol)
        bad_protocol["initial_profiles"][0][0] = 0.5
        with self.assertRaises(ValueError):
            geometry.readout(seed, 0, bad_protocol)

    def test_global_periodic_positive_source_is_impossible_for_this_ansatz(self):
        _, seed, protocol = geometry.prepare_fixture(L=11, steps=2)
        grid = seed.lattice
        plus, minus = grid.shift_index((1, 0, 0)), grid.shift_index((-1, 0, 0))
        for row, rails in ((8, (0, 2)), (9, (1, 3)), (10, (4, 6)), (11, (5, 7))):
            f = seed.b[row]
            self.assertEqual(sum(f[plus]-2*f+f[minus]), 0)
            self.assertGreater(sum(seed.b[rails[0]]+seed.b[rails[1]]), 0)
        self.assertTrue(any(geometry.profile_constraints(seed).flat))

    def test_source_intervention_and_same_stress_collision_control(self):
        law, seed, protocol = geometry.prepare_fixture(L=11, steps=2)
        _, changed_seed, changed_protocol = geometry.prepare_fixture(
            L=11, steps=2, remove_first_record=True)
        original = geometry.readout(seed, 0, protocol)
        changed = geometry.readout(changed_seed, 0, changed_protocol)
        self.assertNotEqual(original["R"], changed["R"])
        self.assertNotEqual(original["G_uu"], changed["G_uu"])
        # Fixed geometry here deliberately violates the physical constraint:
        # this checks a literal source term in the runtime, not another solution.
        mechanical = changed_seed.copy()
        for field in ("a", "b", "r"):
            getattr(mechanical, field)[8:] = getattr(seed, field)[8:]
        engine = Engine(law)
        changed_next = engine.step(mechanical)
        self.assertFalse(np.array_equal(engine.step(seed).b[8:], changed_next.b[8:]))
        self.assertTrue(engine.inverse_step(changed_next).same_as(mechanical))
        off_law, off_seed, off_protocol = geometry.prepare_fixture(
            L=11, steps=2, coupled=False)
        self.assertTrue(np.array_equal(seed.b, off_seed.b))
        on, off = engine.run(seed, 2), Engine(off_law).run(off_seed, 2)
        self.assertTrue(np.array_equal(on.b[8:], off.b[8:]))
        self.assertFalse(np.array_equal(on.b[:8], off.b[:8]))
        self.assertEqual(geometry.readout(on, 2, protocol),
                         geometry.readout(off, 2, off_protocol))

    def test_all_face_orientations_preserve_physical_chart(self):
        for direction in ((1, 0, 0), (-1, 0, 0), (0, 1, 0),
                          (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            with self.subTest(direction=direction):
                law, seed, protocol = geometry.prepare_fixture(
                    L=11, steps=2, direction=direction)
                engine = Engine(law)
                end = engine.run(seed, 2)
                self.assertEqual(geometry.readout(end, 2, protocol)[
                    "source_curvature_residual"], (0, 0))
                self.assertTrue(engine.rewind(end, 2).same_as(seed))


if __name__ == "__main__":
    unittest.main()

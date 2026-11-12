"""Independent finite-state certificate and physical-scope counterexamples."""
import unittest
import numpy as np

from universe24.core import Engine
from validation.selection.acceptance import (
    TABLE, STATES, independent_gate, independent_prepare,
    finite_ring_certificate, source_identity_audit,
)
from validation.selection.clocks import build_native_gate


class SelectionAcceptanceTests(unittest.TestCase):
    def test_literal_three_cycle_retains_carriers_not_total_hamming(self):
        self.assertEqual(TABLE[(0, 0, 1)], (1, 1, 0))
        self.assertEqual(TABLE[TABLE[TABLE[(0, 0, 1)]]], (0, 0, 1))
        self.assertEqual(len(set(TABLE.values())), 8)
        self.assertTrue(all(sum(state[1:])==sum(TABLE[state][1:]) for state in STATES))
        self.assertNotEqual(sum((0, 0, 1)), sum(TABLE[(0, 0, 1)]))

    def test_closed_ring_is_exact_finite_permutation(self):
        report = finite_ring_certificate()
        self.assertEqual(report["complete_ring_states"], 512)
        self.assertEqual(sum(int(length)*count for length,count in report["cycle_lengths"].items()), 512)
        self.assertIn("impossible", report["indefinite_strict_state_score_growth"])

    def test_independent_preparation_and_off_sector_failure(self):
        direction = (-1, 0, 0)
        table = tuple(TABLE[state] for state in STATES)
        tensor = build_native_gate(table, direction=direction)
        current = np.zeros((3, 27), dtype=object)
        current[2, 0] = 1
        seed = independent_prepare(current, 3, direction, 5)
        after = Engine(tensor).step(seed)
        self.assertTrue(np.array_equal(after.b, independent_gate(current, 3, direction)))
        self.assertTrue(np.array_equal(after.a, independent_gate(after.b, 3, direction, inverse=True)))
        zero = independent_prepare(np.zeros_like(current), 3, direction, 5)
        zero.a[0, 0] = 1
        wrong = Engine(tensor).step(zero)
        self.assertEqual(wrong.b[0, 0], -1)
        self.assertTrue(Engine(tensor).inverse_step(wrong).same_as(zero))

    def test_boolean_oracle_rejects_rounding(self):
        for invalid in (0.5, True, -1, 2):
            values = np.zeros((3, 27), dtype=object)
            values[0, 0] = invalid
            with self.assertRaises(ValueError):
                independent_gate(values, 3)

    def test_homogeneous_identity_does_not_hide_spatial_or_potential_failure(self):
        report = source_identity_audit()
        self.assertEqual(report["exact_symbolic_residuals"], [0, 0])
        self.assertEqual(report["unbounded_potential_control"], -96)
        self.assertEqual(report["inhomogeneous_zero_momentum_pressure_defect"], 1)
        self.assertEqual(report["generic_spatial_apparatus_conservation"], "failed")


if __name__ == "__main__":
    unittest.main()

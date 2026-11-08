"""Regression checks for full-coordinate balance and activity limitations."""
import unittest

from research.collective_clock_geometry.audit import (
    activity_four, counterexamples, phase_balance, reconstruct, scalar_checks,
)
from universe24 import Channel
from universe24.core.rule3 import forward


class CollectiveClockGeometryTests(unittest.TestCase):
    def test_complete_coordinates_include_negative_and_large_values(self):
        for b in (-10**40, -3, 0, 7, 10**40):
            for p in (-10**40, -7, -1, 0, 1, 8, 10**40):
                for epsilon in (0, 1):
                    triple = reconstruct(b, p, epsilon)
                    self.assertEqual(phase_balance(triple), p)
                    self.assertEqual(triple[1], b)
                    self.assertEqual(triple[2] % 2, epsilon)
                    self.assertIn(triple[2], range(6))

    def test_exact_coordinate_law_across_division_boundaries(self):
        result = scalar_checks()
        self.assertEqual(result["cases"], 4374)
        for r in range(6):
            old = Channel(-2, 1, r)
            for u in range(-8, 9):
                new = forward(old, u)
                self.assertEqual(phase_balance(new), phase_balance(old) + u - 6)

    def test_activity_retains_directional_squares_and_loses_global_sign(self):
        cells = {(1, 1, 1, 0): (2, 3, 5), (2, 1, 1, 0): (-1, 2, 0)}
        opposite = {address: (-a, -b, r) for address, (a, b, r) in cells.items()}
        measured = activity_four(cells, 3)
        self.assertEqual(measured, activity_four(opposite, 3))
        self.assertTrue(all(x >= 0 for diagonal in measured.values() for x in diagonal))
        self.assertEqual(measured[(1, 1, 1)][0], 10)
        self.assertEqual(measured[(1, 1, 1)][1:], (18, 18))

    def test_counterexamples_block_clock_phase_and_energy_overclaims(self):
        result = counterexamples()
        self.assertEqual(result["same_activity_and_initial_p"]["next_center_p"], [-6, 6])
        self.assertEqual(result["activity_not_conserved"]["V_before"], 3)
        self.assertEqual(result["activity_not_conserved"]["V_after"], 0)
        self.assertEqual(result["p_not_a_clock_phase"]["p"], 3)


if __name__ == "__main__":
    unittest.main()

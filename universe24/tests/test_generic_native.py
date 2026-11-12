"""Independent boundary cases for native packing and arithmetic observation."""
import unittest

from validation.generic_couplings.native import audit, pack, unpack


class GenericNativeTests(unittest.TestCase):
    def test_signed_coordinate_bijection_includes_every_carry(self):
        for a in (-10**40, -7, 0, 9, 10**40):
            for b in (-19, 0, 23):
                for carry in range(6):
                    self.assertEqual(unpack(*pack(a, b, carry)), (a, b, carry))

    def test_packing_rejects_invalid_or_inexact_retained_values(self):
        for carry in (-1, 6):
            with self.assertRaises(ValueError):
                pack(0, 0, carry)
        for values in ((True, 0, 0), (0, 0.5, 0), (0, 0, False)):
            with self.assertRaises(TypeError):
                pack(*values)
        with self.assertRaises(TypeError):
            unpack(0, 1.2)

    def test_actual_engine_matches_scalar_oracle_and_silent_clock_control(self):
        result = audit()
        self.assertEqual(result['channel_updates_compared'], 6480)
        self.assertEqual(result['canonical_clicks_checked'], 5430)
        self.assertEqual(result['silent_period_four_all_carries'], 'passed')
        self.assertEqual(result['packed_channel_saving'], 0)
        self.assertEqual(result['old_history_floor_fourth_difference'], -3)
        self.assertEqual(result['physics_acceptance'], 'not_established')

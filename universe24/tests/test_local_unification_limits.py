"""Independent acceptance boundaries for the chosen local law."""
import unittest
from fractions import Fraction

from validation.local_unification import limits


class LocalUnificationLimitsTests(unittest.TestCase):
    def test_local_involution_and_nonstationary_preference(self):
        result = limits.local_proof()
        self.assertEqual(len(result["truth_table"]), 16)
        self.assertEqual(result["conditional_order_drift"],
                         {"ready": Fraction(1, 2), "used": Fraction(-1, 2), "all": Fraction(0)})
        self.assertFalse(result["twelve_channel_finite_state_claim"])

    def test_actual_engine_chiral_density_translation(self):
        result = limits.free_stream_audit()
        self.assertEqual(result["Engine_transitions"], 36)
        self.assertEqual(result["exact_density_comparisons"], 972)
        self.assertFalse(result["geometry_feedback_into_packet_prefix"])

    def test_positive_kinematic_mass_requires_unbounded_free_spread(self):
        result = limits.spread_polynomial({0: 1}, {0: 1})
        self.assertEqual((result["E"], result["P"], result["Q0"], result["Q1"], result["Q2"]),
                         (2, 0, 0, 0, 4))
        cases = limits.moment_certificate()["cases"]
        self.assertEqual(cases[0]["checks"][-1]["centered_moment_times_energy"], 40000)
        self.assertEqual(cases[-1]["proof"]["Q2"], 0)
        with self.assertRaises(ValueError):
            limits.spread_polynomial({0: -1}, {0: 1})
        with self.assertRaises(ValueError):
            limits.spread_polynomial({0.0: 1}, {0: 1})

    def test_same_packet_records_do_not_fix_metric_proper_time(self):
        result = limits.clock_offset_audit()
        self.assertEqual(result["R_shift"], 400)
        self.assertEqual(result["microticks"], 2)
        for row in result["rate_comparisons"]:
            self.assertGreater(row["R"], 0)
            self.assertEqual(row["shifted_R"], row["R"]+400)
            self.assertLess(row["proper_rate_ratio_fourth_power"], 1)

    def test_scalar_geometry_offset_rejects_invalid_state_or_constant(self):
        with self.assertRaises(ValueError):
            limits.offset_geometry(None, 1)
        with self.assertRaises(ValueError):
            limits.offset_geometry(None, True)
        with self.assertRaises(ValueError):
            limits.offset_geometry(None, 0)


if __name__ == "__main__":
    unittest.main()

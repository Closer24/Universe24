"""Independent scalar and negative controls for generic coupling geometry."""
from __future__ import annotations

import json
import unittest

from universe24.core import Tensor, check_reciprocity
from validation.generic_couplings.geometry import audit, build_reciprocal_edge


class GenericGeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = audit()

    def test_axis_rejects_inexact_or_out_of_range_inputs(self):
        for value in (False, True, 0.0, "0", None):
            with self.subTest(axis=value), self.assertRaises(TypeError):
                build_reciprocal_edge(value)
        for value in (-1, 3, 999):
            with self.subTest(axis=value), self.assertRaises(ValueError):
                build_reciprocal_edge(value)

    def test_each_axis_has_real_link_support_and_reciprocal_reaction(self):
        fingerprints = set()
        for axis in range(3):
            with self.subTest(axis=axis):
                tensor = build_reciprocal_edge(axis)
                self.assertEqual(tensor.G, 3)
                self.assertEqual(tensor.gears[2].link, axis)
                self.assertEqual(len(tensor.monomials), 14)
                self.assertEqual(tensor.support_violations(), [])
                self.assertTrue(check_reciprocity(tensor).ok)
                self.assertTrue(all(m.degree == 3 for m in tensor.monomials))
                without_reaction = Tensor(tensor.gears,
                                          [m for m in tensor.monomials if m.target != 2],
                                          strict_support=True)
                self.assertFalse(check_reciprocity(without_reaction).ok)
                fingerprints.add(tensor.fingerprint)
        self.assertEqual(len(fingerprints), 3)

    def test_nonuniform_all_carry_state_matches_scalar_oracle_and_rewinds(self):
        # The audit oracle uses scalar endpoint formulas and explicit coordinates,
        # not the tensor's monomial evaluator or its vectorized gather maps.
        for result in self.report["edge_runs"]:
            with self.subTest(axis=result["axis"]):
                self.assertEqual(result["initial_carries"], list(range(6)))
                self.assertEqual(result["scalar_register_comparisons"], 1215)
                self.assertGreater(result["changed_remainder_entries"], 0)
                self.assertEqual(len(result["max_bits_per_step"]), 5)
                self.assertGreater(result["max_bits_per_step"][-1], result["max_bits_per_step"][0])
                self.assertTrue(result["full_rewind"])
                self.assertTrue(result["deleted_reaction_rejected"])

    def test_reciprocal_connection_does_not_imply_synchronization(self):
        clocks = self.report["clock_controls"]
        six = clocks["six_step_oscillator"]
        self.assertEqual(six["minimal_period"], 6)
        self.assertEqual(six["b_samples_including_initial"], [1, 1, 0, -1, -1, 0, 1])
        pair = clocks["reciprocal_nonsynchronizing_pair"]
        self.assertTrue(pair["face_connected"] and pair["reciprocity"])
        self.assertEqual(pair["minimal_period"], 3)
        self.assertFalse(pair["synchronized_histories"])
        self.assertTrue(pair["full_rewind"] and pair["all_six_carries_retained"])

    def test_covector_phase_and_null_cone_cannot_define_clock_metric(self):
        flat = self.report["flat_covector"]
        self.assertEqual(flat["rest_phase_rate"], flat["moving_phase_rate"])
        self.assertNotEqual(flat["rest_proper_rate"], flat["moving_proper_rate"])
        conformal = self.report["conformal_ambiguity"]
        self.assertTrue(conformal["same_null_set_as_minkowski"])
        self.assertEqual(conformal["ricci_scalar_at_zero"], "12")
        self.assertEqual(conformal["ricci_scalar_at_one"], "3/2")

    def test_report_is_serializable_without_promoting_physical_claims(self):
        json.dumps(self.report, allow_nan=False)
        self.assertEqual(self.report["status"], "passed")
        self.assertEqual(self.report["physical_acceptance"], "not_established")
        self.assertFalse(self.report["integrated_with_common45"])
        self.assertFalse(self.report["potential"]["discrete_energy_conservation_proved"])
        self.assertFalse(self.report["potential"]["continuous_rotation_is_generic_integer_state_symmetry"])
        self.assertEqual(self.report["clock_controls"]["physical_proper_clock"], "not_established")


if __name__ == "__main__":
    unittest.main()

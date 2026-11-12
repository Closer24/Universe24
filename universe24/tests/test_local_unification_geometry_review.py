"""Independent physical identities and source-bound native chart controls."""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from pathlib import Path
import tempfile
import unittest

from universe24.core import Engine
from universe24.system.bundle import create_bundle
from universe24.system.decoder import default_protocol
from universe24.system.runtime import run_bundle
from validation.local_unification import geometry, geometry_review as review


class GeometryReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.law, cls.seed, cls.protocol = geometry.prepare_fixture(L=11, steps=2)
        ownership = [{"index": i, "name": gear.name, "label": gear.label,
                      "owner": "source" if i < 8 else "geometry",
                      "purpose": "independent same-state chart review"}
                     for i, gear in enumerate(cls.law.gears)]
        cls.bundle = create_bundle(
            cls.law, cls.seed, channels=ownership, protocol=default_protocol(),
            model={"id": "independent-null-chart-review", "version": "1",
                   "domain": "finite plane-symmetric positive chart only"})
        cls.run_dir = Path(cls.temporary.name)/"runtime"
        run_bundle(cls.bundle, cls.run_dir, steps=2)

    def test_metric_source_and_affine_geodesics(self):
        result = review.metric_proof()
        self.assertEqual(result["einstein_residuals"], ["0"]*16)
        self.assertEqual(result["stress_divergence_residuals"], ["0"]*4)
        self.assertEqual(result["affine_null_geodesic_residuals"], ["0"]*8)
        self.assertTrue(result["wrong_source_rejected"])
        self.assertTrue(result["wrong_timelike_coordinate_rejected"])

    def test_direct_spline_derivative_and_nonconstant_source(self):
        result = review.spline_proof()
        self.assertEqual(result["interval_polynomial_residuals"], ["0"]*6)
        self.assertEqual(result["nonconstant_source_reconstruction_checks"], 41)
        self.assertEqual(review.cubic_second(Fraction(3, 2)), Fraction(1, 2))
        self.assertNotEqual(review.cubic(Fraction(0)), 1)
        self.assertEqual(review.periodic_obstruction()["finite_ring_cases"], 243)

    def test_saved_history_matches_independent_scalar_and_initial_anchor(self):
        result = review.saved_chart_review(self.run_dir, self.protocol)
        self.assertEqual(result["tensor_hash"], self.law.fingerprint)
        self.assertEqual(result["bundle_id"], self.bundle.bundle_id)
        self.assertEqual(result["full_retained_scalar_comparisons"], 2*3*12*11**3)
        self.assertGreater(result["continuous_R_lower_bound"], 0)
        self.assertGreater(result["anchored_macro_coefficient_checks"], 0)
        self.assertGreater(result["independent_rational_metric_source_readouts"], 0)
        self.assertTrue(review.scalar_step(self.seed).same_as(Engine(self.law).step(self.seed)))
        bad = dict(self.protocol, microsteps=True)
        with self.assertRaises(ValueError):
            review.saved_chart_review(self.run_dir, bad)
        bad = dict(self.protocol, microsteps=4)
        with self.assertRaises(ValueError):
            review.saved_chart_review(self.run_dir, bad)

    def test_slice_constraint_does_not_certify_complete_history(self):
        changed = self.seed.copy()
        changed.a[8, :] += 1
        # A constant change in OLD history leaves every current constraint alone.
        self.assertEqual(geometry.profile_constraints(changed).tolist(),
                         geometry.profile_constraints(self.seed).tolist())
        with self.assertRaises(ValueError):
            review._prepared_history(changed, (1, 0, 0))
        self.assertTrue(Engine(self.law).inverse_step(Engine(self.law).step(changed)).same_as(changed))

    def test_raw_exact_inputs_and_chart_boundary(self):
        for bad in (True, 1.25):
            with self.assertRaises(ValueError):
                review.cubic(bad)
            with self.assertRaises(ValueError):
                geometry.reconstruct([bad], 0)
            changed = self.seed.copy()
            changed.b[8, 0] = bad
            with self.assertRaises(ValueError):
                geometry.readout(changed, 0, self.protocol)
        changed_protocol = deepcopy(self.protocol)
        changed_protocol["microsteps"] = True
        with self.assertRaises(ValueError):
            geometry.readout(self.seed, 0, changed_protocol)
        with self.assertRaises(ValueError):
            geometry.readout(self.seed, 0, self.protocol, coordinate=0)


if __name__ == "__main__":
    unittest.main()

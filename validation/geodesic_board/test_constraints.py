"""Exact physical counterexamples must survive changes to the common law."""
from fractions import Fraction as F
import unittest

from .constraint_audit import audit_case, continuum_identity, reduced_values


class ConstraintAuditTests(unittest.TestCase):
    def test_continuum_propagation_and_exact_discrete_defects(self):
        result = continuum_identity()
        self.assertEqual(result['first_Euler_step_defects'],
                         {'massive': '-7*h**2', 'massless': '-3*h**2', 'flat': '0'})

    def test_shared_massive_engine_preserves_known_failure(self):
        result = audit_case(steps=1, final_time=F(1, 32))
        self.assertEqual(result['channels'], 45)
        self.assertEqual(result['first_constraint'], '-7/1024')
        self.assertEqual(result['exact_discrete_constraint_preservation'], 'failed')
        self.assertTrue(result['all_remainders_and_complete_rewind'])

    def test_homogeneous_audit_rejects_spatial_data(self):
        # The reduction may never validate a generic field by inspecting node 0.
        with self.assertRaisesRegex(AssertionError, 'not homogeneous'):
            reduced_values({'phi': [F(0), F(1)]})


if __name__ == '__main__':
    unittest.main()

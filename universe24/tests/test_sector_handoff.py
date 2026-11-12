"""Do not join independently delivered sectors by fingerprint or ratios alone."""
import unittest

from validation.integration_contract.sector_handoff import audit


class SectorHandoffTests(unittest.TestCase):
    def test_same_dynamics_different_retained_carry_domains(self):
        report = audit()
        self.assertEqual(report['dynamics_after_explicit_index_mapping'], 'equal')
        self.assertEqual(report['default_complete_seed_domains'], 'different; cross-projection rejected')
        self.assertEqual(report['explicit_zero_carry_domain_alignment'], 'passed')
        self.assertEqual(report['physical_acceptance'], 'not_established')


if __name__ == '__main__':
    unittest.main()

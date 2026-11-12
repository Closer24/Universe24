"""Acceptance must not turn reversible recurrence into growing complexity."""
import tempfile
import unittest
from pathlib import Path

from validation.system_acceptance.burst_growth import audit, cycle_decomposition, ring_bits
from universe24.system.runtime import verify_run


class SystemBurstGrowthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.out = Path(cls.temporary.name)/'fresh'
        cls.report = audit(cls.out)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_exhaustive_same_law_domain_and_finite_recurrence(self):
        report = self.report
        self.assertEqual(report['exhaustive_ring_states'], 512)
        self.assertEqual(report['cycle_count'], 90)
        self.assertEqual(sum(int(period)*count for period, count in
                             report['cycle_length_histogram'].items()), 512)
        self.assertEqual(report['maximum_ring_period'], 39)
        self.assertEqual(report['whole_3_cube_period_divides'], 1670760)
        self.assertEqual(report['population_results']['ready_memory']['count'], 64)
        self.assertEqual(report['independent_complete_register_comparisons'], 124416)
        self.assertEqual(report['channels'], 3)
        self.assertTrue(report['all_six_carry_classes'])

    def test_recurrent_peaks_are_real_but_do_not_pass_growth(self):
        report = self.report
        self.assertEqual(report['recurrent_peak_preparation_count'], 72)
        self.assertEqual(report['gates']['recurrent_memory_event_peaks'], 'passed')
        self.assertEqual(report['gates']['predeclared_structural_growth'], 'failed')
        self.assertEqual(report['population_results']['all_prepared_memory']['complete_cycle_window'],
                         {'passed': 0, 'failed': 72, 'blocked': 440})
        witness = report['recurrent_witness']
        self.assertEqual(witness['code'], 77)
        self.assertEqual(witness['complete_cycle_window']['episode_steps'], [4, 10, 16, 22])
        self.assertEqual(witness['complete_cycle_window']['scores_at_episodes'], [0, 0, 0, 0])
        verified = verify_run(self.out/'recurrent-witness-run')
        self.assertEqual(verified['tensor_hash'], report['tensor_hash'])
        self.assertEqual(verified['run_id'], witness['run_id'])

    def test_preselected_pulse_and_wrong_history_controls_remain_visible(self):
        report = self.report
        self.assertEqual(report['representative']['period'], 5)
        self.assertEqual(report['representative']['complete_recurrence_ticks'], [5, 10, 15, 20])
        self.assertEqual(report['gates']['preselected_single_pulse_strict_peaks'], 'blocked')
        self.assertTrue(report['negative_controls']['wrong_old_history_rejected_despite_same_current'])
        self.assertTrue(report['negative_controls']['wrong_history_still_reversible'])
        self.assertEqual(report['physical_acceptance'], 'not_established')
        self.assertEqual(report['gates']['physical_cosmological_bursts'], 'not_identified')
        with self.assertRaises(ValueError):
            audit(self.out)

    def test_orbit_claim_rejects_lossy_map_and_invalid_population_member(self):
        with self.assertRaises(ValueError):
            cycle_decomposition([0]*512)
        for invalid in (True, 1.0, -1, 512):
            with self.assertRaises(ValueError):
                ring_bits(invalid)


if __name__ == '__main__':
    unittest.main()

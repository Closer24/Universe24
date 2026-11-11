"""Separate actual causal clicks, conditional sampling and a Born reference."""
from collections import Counter
from fractions import Fraction
from itertools import product
import unittest

from validation.quantum.bell_cone_audit import audit, trial
from validation.quantum.born_reference import (interference, probabilities, measure,
    singlet_amplitudes, quantum_reference, stochastic_local_bound, router_calibration)
from universe24.core import Engine
from universe24.layers.causal_wave import with_causal_wave


class BellBornReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report, cls.records = audit(distance=2)

    def test_actual_arrivals_source_independence_and_remote_choice(self):
        self.assertGreater(self.report['detector_separation'], self.report['measurement_deadline'])
        self.assertEqual(sum(len(rows) for rows in self.records.values()), 44)
        for case in self.report['cases'].values():
            self.assertTrue(case['all_cones_and_rewinds_verified'])
            self.assertTrue(case['independent_setting_enumeration'])
            self.assertTrue(case['local_results_independent_of_remote_setting'])
            self.assertTrue(case['no_click_before_arrival'])
        for rows in self.records.values():
            for label in {row['source_label'] for row in rows}:
                group = [r for r in rows if r['source_label'] == label]
                self.assertEqual(len({r['source_triples_sha256'] for r in group}), 1)
                for side, setting in product((0, 1), repeat=2):
                    same_local = [r['detectors'][side] for r in group if r['settings'][side] == setting]
                    self.assertEqual(same_local[0], same_local[1])

    def test_C2_selection_control_cannot_be_mislabeled_Bell_success(self):
        readers = self.report['cases']['selection_stress']['readers']
        self.assertEqual(readers['all_arrival_clicks']['S'], '1')
        self.assertEqual(readers['C2_all_emissions']['S'], '3/2')
        conditional = readers['C2_coincidences_only']
        self.assertEqual(conditional['S'], '4')
        self.assertTrue(conditional['selected_marginals_nonsignalling'])
        for cell in conditional['cells'].values():
            self.assertEqual((cell['emitted'], cell['included']), (8, 2))
        self.assertFalse(self.report['physical_Bell_violation_demonstrated'])

    def test_missing_conditional_cells_are_undefined(self):
        reader = self.report['cases']['shared_sign']['readers']['C2_coincidences_only']
        self.assertIsNone(reader['S'])
        self.assertIsNone(reader['selected_marginals_nonsignalling'])
        self.assertEqual(reader['cells']['01']['included'], 0)
        self.assertIsNone(reader['cells']['01']['E'])

    def test_no_packet_does_not_fabricate_arrival_clicks(self):
        row = trial(Engine(with_causal_wave()), 2, (0, 0), (0, 1))
        self.assertEqual(row['first_clicks'], [None, None])
        for detector in row['detectors']:
            self.assertFalse(detector['click'])
            self.assertFalse(detector['C2'])
            self.assertEqual(detector['before'], detector['after'])

    def test_stochastic_local_choices_obey_same_bound(self):
        result = stochastic_local_bound()
        self.assertEqual(result['models_checked'], 625)
        self.assertEqual(result['maximum_expected_CHSH'], '2')
        self.assertEqual(self.report['local_response_tables']['CHSH_values'], [-2, 2])

    def test_coherent_addition_and_relative_phase_precede_squaring(self):
        self.assertEqual(probabilities(interference((1, 0), (1, 0)))[0], (4, 0))
        self.assertEqual(probabilities(interference((1, 0), (0, 1)))[0], (2, 2))
        self.assertEqual(probabilities(interference((1, 0), (-1, 0)))[0], (0, 4))
        self.assertEqual(probabilities(interference((2, 0), (1, 0)))[1],
                         (Fraction(9, 10), Fraction(1, 10)))
        for x, y in product((0, 1), repeat=2):
            amplitudes = singlet_amplitudes(x, y)
            phased = tuple((-imag, real) for real, imag in amplitudes)
            self.assertEqual(probabilities(amplitudes), probabilities(phased))

    def test_random_draw_occurs_only_at_measurement_and_retains_amplitudes(self):
        class Tickets:
            def __init__(self):
                self.calls = 0
            def randrange(self, stop):
                value = self.calls % stop
                self.calls += 1
                return value
        amplitudes = interference((2, 0), (1, 0))
        tickets = Tickets()
        for _ in range(8):
            self.assertIsNone(measure(amplitudes, tickets, ready=False))
        self.assertEqual(tickets.calls, 0)
        counts = Counter()
        for _ in range(10):
            result = measure(amplitudes, tickets, ready=True)
            self.assertEqual(result['amplitudes'], amplitudes)
            counts[result['outcome']] += 1
        self.assertEqual(counts, {0: 9, 1: 1})
        self.assertEqual(tickets.calls, 10)

    def test_joint_reference_against_independent_singlet_dot_products(self):
        records = []
        reference = quantum_reference([2, 2], samples_per_setting=100, record_sink=records.append)
        self.assertEqual(len(records), 400)
        alice = ((0, 1), (1, 0))
        bob = ((Fraction(3, 5), Fraction(4, 5)), (-Fraction(3, 5), Fraction(4, 5)))
        for x, y in product((0, 1), repeat=2):
            expected = -sum(a*b for a, b in zip(alice[x], bob[y]))
            cell = reference['cells'][f'{x}{y}']
            self.assertEqual(Fraction(cell['E']), expected)
            self.assertEqual(sum(map(Fraction, cell['probabilities'])), 1)
            self.assertEqual(sum(cell['sample_counts']), 100)
            replayed = Counter()
            for row in records:
                if row['settings'] != [x, y]:
                    continue
                cumulative = 0
                for outcome, weight in enumerate(cell['weights']):
                    cumulative += weight
                    if row['ticket'] < cumulative:
                        self.assertEqual(row['outcome'], outcome)
                        replayed[outcome] += 1
                        break
                self.assertEqual(row['measurement_microtick'], 2)
            self.assertEqual([replayed[i] for i in range(4)], cell['sample_counts'])
        self.assertEqual(reference['exact_CHSH'], '14/5')
        self.assertTrue(reference['exact_marginals_nonsignalling'])
        self.assertTrue(reference['joint_sampler_uses_both_settings'])
        self.assertFalse(reference['feeds_Engine'])

    def test_existing_square_input_is_not_a_Born_click_probability(self):
        result = router_calibration()
        self.assertEqual(result['G'], 7)
        self.assertEqual(result['amplitude_arrival_microtick'], 2)
        self.assertEqual(result['detector_readout_microtick'], 3)
        self.assertEqual(result['strict_support_violations'], 0)
        for case in result['cases']:
            self.assertTrue(case['no_early_detector_clicks'])
            for frame in case['amplitude_trace']:
                self.assertEqual(frame['arm_a'], list(case['arm_a']) if frame['microtick'] == 2 else [0, 0])
                self.assertEqual(frame['arm_b'], list(case['arm_b']) if frame['microtick'] == 2 else [0, 0])
        unequal = next(c for c in result['cases'] if c['case'] == 'unequal_arms')
        self.assertEqual(unequal['quadratic_inputs'], (9, 1))
        self.assertEqual(unequal['Born_reference_probabilities'], ['9/10', '1/10'])
        self.assertEqual(unequal['actual_clicks'], [36, 12])
        self.assertEqual(unequal['share_of_all_clicks'], ['3/4', '1/4'])
        self.assertEqual(unequal['double_click_trials'], 12)
        self.assertFalse(result['Born_click_law_derived'])
        self.assertTrue(all(c['all_rewinds_exact'] for c in result['cases']))


if __name__ == '__main__':
    unittest.main()

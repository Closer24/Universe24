"""Compact assembly, sourced interaction and explicit failed physical gates."""
from fractions import Fraction
import unittest

import numpy as np

from experiments.geometry.team48.candidate import build
from experiments.geometry.team48.integer_sign_lift import prepare, physical_slices
from experiments.geometry.team48.matter_charged_audit import engine_checks, pr39_comparison
from experiments.geometry.team48.constraints_audit import linearized_null_beam_engine
from experiments.geometry.team48.numerical_milne import run as milne_failure
from experiments.geometry.team48.integer_staggered_audit import check_candidate, check_rejections
from universe24.core import Engine


class Team48Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models = {name: build(name) for name in ('scalar_dust', 'maxwell', 'charged')}

    def test_named_allocation_and_hard_budget(self):
        for name, expected in (('scalar_dust', 32), ('maxwell', 38), ('charged', 41)):
            candidate = self.models[name]
            manifest = candidate.manifest()
            self.assertEqual(manifest['channels'], expected)
            self.assertEqual(manifest['available_channels'], 48-expected)
            indices = [i for block in manifest['blocks'] for i in block['indices']]
            self.assertEqual(sorted(indices+[manifest['phase_index']]), list(range(expected)))
            self.assertEqual(manifest['integer_entries_per_node'], 3*expected)
            self.assertEqual(manifest['metric_owners'], 1)
            self.assertEqual(candidate.program.tensor.support_violations(), [])
            self.assertLessEqual(candidate.program.tensor.rank, 4)
            self.assertFalse(manifest['full_nonlinear_einstein_gate'])
            self.assertFalse(manifest['constraints_preserved'])

    def test_flat_physical_solution_and_complete_phase_rewind(self):
        for candidate in self.models.values():
            program = candidate.program
            physical = np.zeros((len(program.fields), 27), dtype=object)
            for axis in range(3):
                physical[program.fields.index(f'B{axis}{axis}')] = 1
            remainders = np.arange(program.tensor.G*27).reshape(program.tensor.G, 27) % 6
            initial = prepare(program, physical, physical, L=3, remainders=remainders)
            engine, state = Engine(program.tensor), initial
            for _ in range(5):
                state = engine.step(state)
                previous, current = physical_slices(program, state)
                np.testing.assert_array_equal(previous, physical)
                np.testing.assert_array_equal(current, physical)
                np.testing.assert_array_equal(state.r, initial.r)
            self.assertTrue(engine.rewind(state, 5).same_as(initial))

    def test_pr39_source_equations_reused_exactly(self):
        result = pr39_comparison()
        self.assertTrue(result['all_35_rhs_identical_under_field_renaming'])
        self.assertTrue(result['shared_constraints_and_stress_identical'])

    def test_charged_current_conjugation_and_positive_dust(self):
        result = engine_checks()
        self.assertEqual(result['channels'], 41)
        self.assertTrue(result['integer_engine_charge_conjugation_commutes'])
        self.assertTrue(result['signed_dust_crosses_plus_one_to_minus_one'])
        self.assertTrue(result['dust_density_stays_one'])
        self.assertEqual(result['electric_field_current_contribution_after_one_step'], -6)
        self.assertFalse(result['fixture_is_constrained_Einstein_data'])

    def test_unsupported_refinement_and_source_parameters_rejected(self):
        with self.assertRaisesRegex(ValueError, 'noninteger coefficient'):
            build(dt=Fraction(1, 2), dx=Fraction(1, 2))
        with self.assertRaises(TypeError):
            build(coupling=0.5)
        with self.assertRaises(ValueError):
            build(mass_squared=-1)

    def test_positive_linearized_source_control(self):
        report = linearized_null_beam_engine()
        self.assertEqual(report['gears'], 7)
        self.assertEqual(report['density_sum'], 0)
        self.assertTrue(report['complete_state_rewind'])
        self.assertEqual(report['frozen_density_control_H_M_reduction'][:2], [12, 6])

    def test_consistent_milne_pair_exposes_metric_gate(self):
        report = milne_failure()
        self.assertEqual(report['samples'][2]['B00'], 0)
        self.assertEqual(report['samples'][0]['B00'], 1)

    def test_positive44_actual_integer_map_and_scope(self):
        result = check_candidate()
        self.assertEqual(result['channels'], 44)
        self.assertEqual(result['integer_entries_per_node'], 132)
        self.assertTrue(result['all_three_wronskians_flip_exactly'])
        self.assertTrue(result['complete_rewind'])
        self.assertFalse(result['generic_hamiltonian_momentum_constraint_preservation'])
        self.assertFalse(result['normalized_wronskian_vanishes_under_controlled_refinement'])
        assembled = build('charged_positive', mass_squared=1)
        self.assertEqual(assembled.program.tensor.G, 44)
        self.assertEqual(assembled.manifest()['available_channels'], 4)

    def test_staggered_compiler_rejects_incompatible_cubic(self):
        self.assertTrue(check_rejections()['self_cubic_rejected_for_both_offsets'])


if __name__ == '__main__':
    unittest.main()

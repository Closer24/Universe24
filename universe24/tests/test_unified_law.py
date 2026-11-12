"""Acceptance boundaries for the single homogeneous constrained candidate."""
from fractions import Fraction as F
import unittest

from validation.unified_law import common, constrained_coordinates
from validation.completion import common45
from universe24.core import Engine


class UnifiedLawTests(unittest.TestCase):
    def test_compiled_law_has_one_complete_six_channel_state(self):
        program = common.build()
        self.assertEqual(program.tensor.G, 6)
        self.assertEqual(program.tensor.rank-1, 3)
        self.assertEqual(program.tensor.support_violations(), [])
        self.assertEqual(program.fields, constrained_coordinates.FIELDS)
        self.assertFalse(any(factor.field == 'a' for term in program.tensor.monomials
                             for factor in term.factors))
        common.build(dt=F(1, 32))
        common.build(dt=F(1))
        for bad in (0.1, 0.03125, True):
            with self.assertRaises(TypeError):
                common.build(dt=bad)

    def test_actual_history_preserves_new_physical_constraint(self):
        data = common.trace(steps=3)
        self.assertEqual(data['physical'][0]['k'], F(-1, 2))
        self.assertEqual(data['physical'][0]['phi'], F(1))
        for physical in data['physical']:
            self.assertEqual(constrained_coordinates.constraint(physical), 0)
            self.assertLessEqual(physical['k'], 0)
        self.assertTrue(all(right['beta'] <= left['beta'] for left, right in
                            zip(data['physical'], data['physical'][1:])))
        self.assertNotEqual(data['physical'][-1]['phi'], data['physical'][0]['phi'])

    def test_different_old_law_remains_failed_and_metadata_rejects_it(self):
        program = common45.build45()
        seed = common45.weak_seed(program)
        old_after = common45.decode_fields(program, Engine(program.tensor).step(seed))
        residual = (6*old_after['K00']**2-old_after['Pi_phi']**2
                    -old_after['phi']**2-2*old_after['dust_amplitude']**2)
        self.assertEqual(residual, F(-403, 40960000))
        with self.assertRaises(ValueError):
            common.make_bundle(program, seed)
        selected = common.build()
        altered = common.prepare(selected)
        altered.r[0, 0] = (int(altered.r[0, 0])+1) % 6
        with self.assertRaises(ValueError):
            common.make_bundle(selected, altered)

    def test_zero_constraint_does_not_waive_source_equations(self):
        result = constrained_coordinates.symbolic_audit()
        self.assertTrue(result['all_five_pushforward_equations'])
        self.assertTrue(result['wrong_spinor_dynamics_rejected_despite_zero_constraint'])


if __name__ == '__main__':
    unittest.main()

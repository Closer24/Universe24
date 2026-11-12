"""Cross-team identity and negative physics gates belong in ordinary CI."""
from fractions import Fraction as F
import unittest

import numpy as np

from universe24.core import Engine
from validation.completion import constraint_closure
from validation.geometry.team48 import refinement_integer_projective as projective
from validation.integration_contract.massive45 import check_handoff


class IntegrationContractTests(unittest.TestCase):
    def test_massive45_handoff_dt_64(self):
        result = check_handoff(F(1, 64))
        self.assertEqual(result['first_step_H'], '-403/40960000')
        self.assertEqual(result['discrete_Einstein_constraint'], 'failed')

    def test_massive45_handoff_dt_32(self):
        result = check_handoff(F(1, 32))
        self.assertEqual(result['first_step_H'], '-403/10240000')
        self.assertEqual(result['discrete_Einstein_constraint'], 'failed')

    def test_cayley_target_does_not_hide_second_tick_history_defect(self):
        program, _, _ = constraint_closure.build_history_lift()
        values = np.array([[-1]*27, [0]*27, [2]*27, [1]*27], dtype=object)
        carries = np.array([[(channel+node) % 6 for node in range(27)]
                            for channel in range(5)], dtype=object)
        seed = projective.prepare(program, values, L=3, denominator=4, remainders=carries)
        engine = Engine(program.tensor)
        first = engine.step(seed)
        second = engine.step(first)
        def measured(state):
            k, p, phi, dust = projective.readout(program, state)[:, 0]
            return 6*k*k-p*p-phi*phi-2*dust*dust
        self.assertEqual(measured(seed), 0)
        self.assertEqual(measured(first), 0)
        self.assertNotEqual(measured(second), 0)
        self.assertTrue(np.array_equal(second.r, carries))
        self.assertTrue(engine.inverse_step(second).same_as(first))
        self.assertTrue(engine.rewind(second, 2).same_as(seed))


if __name__ == '__main__':
    unittest.main()

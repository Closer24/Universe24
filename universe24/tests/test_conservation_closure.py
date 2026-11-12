"""Physical acceptance boundaries for the native anisotropic research law."""
from fractions import Fraction as F
import unittest

import numpy as np
import mpmath as mp

from universe24.core import Engine
from validation.conservation_closure import common


class ConservationClosureTests(unittest.TestCase):
    def test_same_tensor_exact_anisotropic_endpoint_at_three_resolutions(self):
        tensors, endpoints = set(), []
        for N in (24, 48, 96):
            data = common.trace(N)
            tensors.add(data['tensor_sha256'])
            r = data['readouts'][-1]
            endpoints.append((r['V'], r['U'], r['tau']))
            self.assertTrue(all(x['Q'] == 0 for x in data['readouts']))
            self.assertEqual(len(set(r['H'])), 3)
            self.assertLessEqual(max(data['bits']), 17)
            self.assertTrue(Engine(data['program'].tensor).rewind(
                data['states'][-1], N//8).same_as(data['seed']))
        self.assertEqual(len(tensors), 1)
        self.assertEqual(endpoints, [(F(2185, 768), F(67, 16), F(1, 8))]*3)

    def test_history_intervention_changes_momentum_and_is_not_repaired(self):
        program = common.build()
        seed = common.prepare(program)
        changed = seed.copy()
        changed.a[0] -= 1
        before, after = (common.read_conserved(program, s) for s in (seed, changed))
        self.assertEqual(before['V'], after['V'])
        self.assertNotEqual(before['U'], after['U'])
        self.assertNotEqual(after['Q'], 0)
        with self.assertRaises(ValueError):
            common.make_bundle(program, changed)
        engine = Engine(program.tensor)
        for _ in range(3):
            changed = engine.step(changed)
            self.assertEqual(common.read_conserved(program, changed)['Q'], after['Q'])

    def test_all_carry_classes_rewind_with_identical_physical_evolution(self):
        program = common.build()
        endpoints = []
        for carry in range(6):
            seed = common.prepare(program, remainders=[[carry]*27 for _ in range(8)])
            engine = Engine(program.tensor)
            after = engine.step(seed)
            self.assertTrue(np.array_equal(after.r, seed.r))
            self.assertTrue(engine.inverse_step(after).same_as(seed))
            r = common.read_conserved(program, after)
            endpoints.append((r['V'], r['U'], r['Q']))
        self.assertEqual(len(set(endpoints)), 1)

    def test_metric_and_scalar_do_not_read_counter_as_trajectory_lookup(self):
        program = common.build()
        seed = common.prepare(program)
        shifted = seed.copy()
        shifted.a[5] += 1000
        shifted.b[5] += 1000
        first, second = (common.physical(program, state) for state in (seed, shifted))
        self.assertNotEqual(first['tau'], second['tau'])
        for key in ('a', 'metric', 'phi', 'I', 'H', 'rho'):
            self.assertEqual(first[key], second[key])

    def test_shear_is_a_source_charge_and_cannot_be_erased_from_constraint(self):
        program = common.build()
        seed = common.prepare(program)
        erased = seed.copy()
        erased.a[6:8] = 0
        erased.b[6:8] = 0
        self.assertEqual(common.read_conserved(program, seed)['Q'], 0)
        self.assertEqual(common.read_conserved(program, erased)['Q'], 3)
        with self.assertRaises(ValueError):
            common.make_bundle(program, erased)

    def test_future_anchor_near_branch_has_finite_passive_geometry(self):
        program = common.build(10**160)
        seed = common.prepare(program, V=1, U=10**80)
        seed.a[3] = seed.b[3] = 4*program.N*(10**80+1)
        result = common.physical(program, seed, dps=60)
        self.assertTrue(mp.isfinite(result['I']))
        self.assertLess(result['I'], 0)
        self.assertTrue(all(mp.isfinite(a) and a > 0 for a in result['a']))
        self.assertNotEqual(result['Q'], 0)
        with self.assertRaises(ValueError):
            common.make_bundle(program, seed)

    def test_complete_allocation_and_exact_type_guards(self):
        program = common.build()
        self.assertEqual(program.tensor.G, 8)
        self.assertEqual(len(program.tensor), 9)
        self.assertEqual(program.tensor.rank-1, 1)
        self.assertTrue(program.tensor.b_only)
        self.assertFalse(program.tensor.support_violations())
        for value in (True, 24.0, F(24)):
            with self.assertRaises(TypeError):
                common.build(value)
        for kwargs in ({'S': (1, 1, 1)}, {'S': (1.0, -1, 0)},
                       {'D': 0}, {'P': 0}, {'V': 1.0},
                       {'remainders': [[6]*27 for _ in range(8)]}):
            with self.assertRaises((TypeError, ValueError)):
                common.prepare(program, **kwargs)
        with self.assertRaises(ValueError):
            common.prepare(common.build(1))


if __name__ == '__main__':
    unittest.main()

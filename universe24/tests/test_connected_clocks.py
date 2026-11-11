"""Integration audits for a fixed experimental tensor, not physical claims."""
from dataclasses import FrozenInstanceError
import unittest

import numpy as np

from universe24.core import Engine
from universe24.tools.connected_clocks import (PRESET, build_candidate, paired_control,
                                               perturb_seed)


class ConnectedClocksTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tensor, cls.seed, cls.network, cls.manifest = build_candidate(L=3, rng_seed=13)

    def test_composition_preserves_one_divisor_rank_and_exact_inverse(self):
        tensor, seed = self.tensor, self.seed
        self.assertEqual(tensor.G, 389)
        self.assertEqual(tensor.rank, 4)
        self.assertEqual(tensor.Q, self.manifest['source_Q'] * PRESET.resolution_factor)
        self.assertEqual(self.manifest['tensor_fingerprint'], tensor.fingerprint)
        self.assertGreater(self.manifest['physical_support_violations'], 0)
        engine = Engine(tensor, tensor.Q)
        self.assertTrue(engine.rewind(engine.run(seed, 4), 4).same_as(seed))
        with self.assertRaises(FrozenInstanceError):
            PRESET.clock_amplitude = 1

    def test_interventions_change_only_declared_initial_registers(self):
        original = self.seed.copy()
        forward, manifest = perturb_seed(self.tensor, self.seed, direction='forward')
        np.testing.assert_array_equal(forward.a, self.seed.a)
        np.testing.assert_array_equal(forward.b, self.seed.b)
        changed = set(map(tuple, np.argwhere(forward.r != self.seed.r)))
        expected = {(self.tensor.gear_index('cosmic.'+name), 0) for name in ('dp', 'dm')}
        self.assertEqual(changed, expected)
        self.assertEqual(manifest['fields'], ['r'])
        reverse, _ = perturb_seed(self.tensor, self.seed, direction='reverse')
        np.testing.assert_array_equal(reverse.a, self.seed.a)
        np.testing.assert_array_equal(reverse.r, self.seed.r)
        self.assertEqual(set(map(tuple, np.argwhere(reverse.b != self.seed.b))),
                         {(self.tensor.gear_index('matter.X0'), 0)})
        self.assertTrue(self.seed.same_as(original))

    def test_feedback_control_records_and_exact_matched_pair_identity(self):
        result = paired_control(self.tensor, self.seed, steps=6)
        self.assertEqual(result['exact_rewinds'], [True, True])
        self.assertTrue(result['matched_remainders'])
        self.assertTrue(result['matched_quotient_difference_equals_reader_intensity'])
        self.assertEqual(result['outside_storage_cone'], 0)
        self.assertEqual(result['first_namespace_difference']['state']['clocknet'], 2)
        self.assertEqual(result['completed_steps'], 6)
        self.assertTrue(result['caller_seed_unchanged'])
        self.assertEqual(result['sector_counter_bounds']['matter']['initial'], [512, 512])

    def test_validation_and_initial_resource_gate_do_not_take_an_update(self):
        for L in (1, 2, True):
            with self.assertRaisesRegex(ValueError, 'at least 3'):
                build_candidate(L=L)
        result = paired_control(self.tensor, self.seed, steps=3, max_counter_bits=1)
        self.assertEqual(result['completed_steps'], 0)
        self.assertEqual(result['stop_reason'], 'initial_counter_bit_limit')
        self.assertEqual(result['exact_rewinds'], [True, True])
        self.assertTrue(result['caller_seed_unchanged'])
        self.assertTrue(all(not times for times in result['first_namespace_difference'].values()))

    def test_bridge_off_and_strict_realization_are_explicit_different_tensors(self):
        off, off_seed, _, off_manifest = build_candidate(L=3, rng_seed=13, bridge=False)
        self.assertFalse(off_manifest['bridge_enabled'])
        self.assertNotEqual(off.fingerprint, self.tensor.fingerprint)
        self.assertTrue(off_seed.same_as(self.seed))
        report = paired_control(off, off_seed, steps=6)
        self.assertEqual(set(report['first_namespace_difference']['state']), {'cosmic'})
        strict, strict_seed, network, manifest = build_candidate(
            L=3, rng_seed=13, strict_edge_stiffness=PRESET.resolution_factor)
        self.assertEqual(strict.rank, 4)
        self.assertEqual(strict.G, 479)
        self.assertEqual(strict.support_violations(), [])
        self.assertEqual(len(manifest['link_mediators']), 90)
        self.assertEqual(strict.names[network.clock_index()], 'clocknet.master')
        engine = Engine(strict, strict.Q)
        self.assertTrue(engine.rewind(engine.run(strict_seed, 3), 3).same_as(strict_seed))


if __name__ == '__main__':
    unittest.main()

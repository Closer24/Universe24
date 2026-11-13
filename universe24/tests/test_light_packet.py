"""Independent Rule3 comparisons and adversarial light-interpretation controls."""
from pathlib import Path
import tempfile
import unittest

import numpy as np

from universe24.core import Engine, Tensor
from universe24.system.bundle import BundleError, create_bundle
from universe24.system.runtime import run_bundle
from universe24.runtime import main, status
from validation.system_smoke import scalar_step
from validation.light_packet.model import export_inputs, ideal, make_bundle, tensor
from validation.light_packet.audit import collect, inspect


class LightPacketTests(unittest.TestCase):
    def test_fixed_tensor_and_independent_scalar_oracle(self):
        bundle = make_bundle(L=5, steps=4, order=2, center=2, interface=3)
        law = bundle.tensor
        self.assertEqual(law.fingerprint, '256db395ebfd0456d72fb6bd7c65754896f984c3b4724f5462d6ac0dce96b177')
        self.assertEqual(law.G, 18)
        self.assertEqual(len(law.monomials), 162)
        self.assertEqual(max(len(term.factors) for term in law.monomials), 2)
        self.assertTrue(all(f.field == 'b' for m in law.monomials for f in m.factors))
        state = bundle.seed
        engine = Engine(law)
        for _ in range(4):
            after = engine.step(state)
            self.assertTrue(after.same_as(scalar_step(law, state)))
            self.assertTrue(np.array_equal(after.b, ideal(state.b, state.L)))
            self.assertTrue(np.array_equal(after.r, state.r))
            self.assertTrue(engine.inverse_step(after).same_as(state))
            state = after
        self.assertTrue(engine.rewind(state, 4).same_as(bundle.seed))

    def test_main_prepare_run_verify_and_declared_horizon(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            bundle = make_bundle(L=5, steps=4, order=2, center=2, interface=3)
            inputs = export_inputs(bundle, out / 'inputs')
            args = ['prepare']
            for name in ('tensor', 'seed', 'channels', 'protocol', 'model'):
                args += ['--' + name, str(inputs / (name + '.json'))]
            main(args + ['--out', str(out / 'bundle')])
            result = main(['run', '--bundle', str(out / 'bundle'), '--steps', '4', '--out', str(out / 'run')])
            replay = main(['verify', '--run', str(out / 'run')])
            self.assertEqual(result, replay)
            observation = inspect(out / 'run')
            self.assertTrue(observation['exact_prepared_sector'])
            self.assertEqual(observation['click_classes']['C1'], 0)
            self.assertEqual(observation['click_classes']['C2'], 0)
            self.assertEqual(observation['physical_gates']['photon_identification'], 'blocked')
            self.assertIsNone(status()['accepted_physical_model'])
            with self.assertRaises(SystemExit) as ctx:
                main(['verify', '--run', str(out / 'run'), '--require-physics'])
            self.assertEqual(ctx.exception.code, 1)
            run_bundle(bundle, out / 'short', 2)
            with self.assertRaisesRegex(ValueError, 'horizon'):
                inspect(out / 'short')

    def test_retained_history_not_just_field_values_defines_sector(self):
        bundle = make_bundle(L=5, steps=4, order=2, center=2, interface=3)
        altered = bundle.seed
        altered.a[1, 0] += 1
        after = Engine(bundle.tensor).step(altered)
        self.assertFalse(np.array_equal(after.b, ideal(altered.b, altered.L)))
        with tempfile.TemporaryDirectory() as tmp:
            wrong = create_bundle(bundle.tensor, altered, channels=bundle.channels,
                                  protocol=bundle.protocol, model=bundle.model)
            run_bundle(wrong, Path(tmp) / 'wrong', 4)
            with self.assertRaisesRegex(ValueError, 'complete bundle'):
                inspect(Path(tmp) / 'wrong')

    def test_new_bundle_still_rejects_algebra_and_budget_violations(self):
        for term in [(0, 1, [(0, (1, 1, 0), 'b')]),
                     (0, 1, [(0, (1, 0, 0), 'b'), (0, (-1, 0, 0), 'b')]),
                     (0, 1, [(0, (0, 0, 0), 'b')] * 4),
                     (0, 1, [(0, (0, 0, 0), 'a')])]:
            with self.assertRaises(ValueError):
                Tensor(['bad'], [term], strict_support=True)
        from universe24.core import State
        law = Tensor([f'g{i}' for i in range(49)], [])
        state = State(3, np.zeros((49, 27), dtype=int), np.zeros((49, 27), dtype=int), np.zeros((49, 27), dtype=int))
        with self.assertRaises(BundleError):
            create_bundle(law, state, channels=[], protocol={}, model={})
        for kw in ({'steps': True}, {'steps': 3}, {'amplitude': 1.5}, {'precision': 0}):
            with self.assertRaises(ValueError):
                make_bundle(**kw)

    def test_compact_saved_controls_preserve_negative_physical_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = collect(Path(tmp) / 'audit', L=9, steps=6, order=2, center=3, interface=5)
            self.assertTrue(report['comparisons']['same_tensor'])
            self.assertEqual(report['comparisons']['amplitude_x2_energy_x4_same_click_counts'], 'passed')
            self.assertEqual(report['controls']['vacuum']['click_count'], 0)
            low = report['controls']['low_precision']
            self.assertFalse(low['exact_prepared_sector'])
            self.assertGreater(low['click_classes']['C1'] + low['click_classes']['C2'], 0)
            self.assertEqual(report['physical_gates']['general_physical_acceptance'], 'blocked')


if __name__ == '__main__':
    unittest.main()

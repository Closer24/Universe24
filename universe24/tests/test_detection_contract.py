"""Installed retained detector: symmetry, conservative exchange and saved records."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from universe24.core import Engine, State
from universe24.core.symmetry import act, require_equivariant
from universe24.detection import (detector_tensor, make_detector_bundle, sector_map,
                                  roles, energy_account, observe_detector_run)
from universe24.runtime import main
from universe24.system.bundle import create_bundle
from universe24.system.runtime import run_bundle
from validation.system_smoke import scalar_step


class DetectionContractTests(unittest.TestCase):
    def test_exact_uniform_tensor_and_full_state_covariance(self):
        law = detector_tensor()
        self.assertEqual(law.G, 48)
        self.assertEqual(len(law.monomials), 624)
        self.assertEqual({m.target for m in law.monomials}, set(range(48)))
        self.assertEqual(max(len(m.factors) for m in law.monomials), 2)
        require_equivariant(law)
        rng = np.random.default_rng(7113)
        state = State(3, rng.integers(-4, 5, (48, 27)), rng.integers(-4, 5, (48, 27)),
                      rng.integers(0, 6, (48, 27)))
        engine = Engine(law)
        expected = engine.step(state)
        self.assertTrue(expected.same_as(scalar_step(law, state)))
        for k in range(48):
            self.assertTrue(engine.step(act(state, k)).same_as(act(expected, k)))
        self.assertTrue(engine.inverse_step(expected).same_as(state))

    def test_all_orientations_preserve_random_exchange_sectors_and_big_integers(self):
        rng = np.random.default_rng(7114)
        engine = Engine(detector_tensor())
        for root in range(48):
            bundle = make_detector_bundle(L=3, root=root, light_position=0, arm_position=1)
            values = bundle.seed.b.astype(object).copy()
            ports = roles(root)
            values[ports['light']] = rng.integers(-4, 5, 27).astype(object) * (1 << 70)
            values[ports['memory']] = rng.integers(-4, 5, 27).astype(object) * (1 << 70)
            values[ports['arming']] = rng.integers(0, 2, 27)
            initial = State(3, sector_map(values, 3, root, inverse=True), values, bundle.seed.r)
            state, account = initial, energy_account(initial, root)
            for _ in range(6):
                expected = sector_map(state.b, 3, root)
                state = engine.step(state)
                np.testing.assert_array_equal(state.b, expected)
                np.testing.assert_array_equal(state.a, sector_map(state.b, 3, root, inverse=True))
                np.testing.assert_array_equal(state.r, initial.r)
                current = energy_account(state, root)
                for key in ('light_plus_memory', 'arming', 'selector'):
                    self.assertEqual(current[key], account[key])
            self.assertTrue(engine.rewind(state, 6).same_as(initial))

    def test_capture_is_retained_then_released_when_arming_returns(self):
        bundle = make_detector_bundle(L=9, light_position=1, arm_position=4, amplitude=2)
        engine, state = Engine(bundle.tensor), bundle.seed
        for step in range(1, 13):
            state = engine.step(state)
            account = energy_account(state, 0)
            self.assertEqual(account['light_plus_memory'], 324)
            self.assertEqual(account['memory'], 324 if 2 <= step < 11 else 0)
        self.assertTrue(engine.rewind(state, 12).same_as(bundle.seed))

    def test_all_arming_opportunities_include_no_transfer_controls(self):
        with tempfile.TemporaryDirectory() as tmp:
            reports = {}
            for name, options in (('capture', {}), ('vacuum', {'amplitude': 0}),
                                  ('unarmed', {'armed': False}), ('double_amplitude', {'amplitude': 2})):
                bundle = make_detector_bundle(L=5, light_position=0, arm_position=3, **options)
                out = Path(tmp) / name
                run_bundle(bundle, out, 8 if name == 'capture' else 3)
                reports[name] = observe_detector_run(out)
            capture = reports['capture']
            self.assertEqual(capture['outcomes'], dict(capture=25, release=25, exchange=0, no_transfer=150))
            self.assertEqual({e['step'] for e in capture['events']}, {2, 7})
            self.assertTrue(all(e['arithmetic_event_id'] for e in capture['events']))
            self.assertEqual(reports['vacuum']['events'], [])
            self.assertGreater(reports['vacuum']['arithmetic_click_count'], 0)
            self.assertEqual(reports['vacuum']['outcomes']['no_transfer'], 75)
            self.assertEqual(reports['unarmed']['events'], [])
            self.assertEqual(reports['unarmed']['arming_opportunities'], 0)
            double = reports['double_amplitude']
            self.assertEqual(double['outcomes']['capture'], 25)
            self.assertEqual({e['energy_to_memory'] for e in double['events']}, {'4'})
            self.assertTrue(all(e['photon_number'] is None for e in double['events']))

    def test_installed_cli_and_interpretation_cannot_be_spoofed(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            root = Path(tmp)
            main(['prepare-detector', '--size', '5', '--light-position', '0', '--arm-position', '3',
                  '--out', str(root / 'input')])
            result = main(['run', '--bundle', str(root / 'input'), '--steps', '3', '--out', str(root / 'run')])
            self.assertEqual(result, main(['verify', '--run', str(root / 'run')]))
            observed = main(['detect', '--run', str(root / 'run'), '--out', str(root / 'observed.json')])
            self.assertEqual(observed['outcomes']['capture'], 25)
            self.assertEqual(len(json.loads((root / 'observed.json').read_text())['events']), 25)
            with self.assertRaises(SystemExit):
                main(['verify', '--run', str(root / 'run'), '--require-physics'])
            with self.assertRaises(SystemExit):
                main(['detect', '--run', str(root / 'run'), '--out', str(root / 'observed.json')])
            bundle = make_detector_bundle(L=3, light_position=0, arm_position=1)
            model = dict(bundle.model, preparation=dict(bundle.model['preparation'], amplitude=2))
            spoofed = create_bundle(bundle.tensor, bundle.seed, channels=bundle.channels,
                                    protocol=bundle.protocol, model=model)
            run_bundle(spoofed, root / 'spoofed', 1)
            with self.assertRaisesRegex(ValueError, 'interpretation differs'):
                observe_detector_run(root / 'spoofed')

    def test_invalid_preparations_and_non_boolean_arming_rejected(self):
        for options in ({'root': True}, {'root': 48}, {'amplitude': -1}, {'amplitude': 1.5},
                        {'armed': 1}, {'light_position': 13}):
            with self.assertRaises(ValueError):
                make_detector_bundle(**options)
        bundle = make_detector_bundle(L=3, light_position=0, arm_position=1)
        values = bundle.seed.b.astype(object).copy()
        values[roles(0)['arming'], 0] = 2
        with self.assertRaisesRegex(ValueError, 'Boolean'):
            sector_map(values, 3, 0)


if __name__ == '__main__':
    unittest.main()

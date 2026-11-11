"""Supported public interface and independent mechanical acceptance controls."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.runtime import main
from universe24.system.bundle import canonical_bytes, create_bundle
from validation.system_smoke import fixture, scalar_step


class OneSystemCLITests(unittest.TestCase):
    def call(self, args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return main(args)

    def test_default_is_honest_status_not_hidden_model_selection(self):
        result = self.call([])
        self.assertIsNone(result['accepted_physical_model'])
        self.assertEqual(result['maximum_channels_per_node'], 48)
        self.assertEqual(result['full_physics_acceptance'], 'blocked')
        for option in ('--causal-wave', '--probe-experiment', '--no-communication', '--max-channels', '--case'):
            with self.assertRaises(SystemExit) as error:
                self.call([option])
            self.assertEqual(error.exception.code, 2)

    def test_prepare_run_verify_and_unearned_physics_rejection(self):
        bundle = fixture()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inputs = dict(tensor=bundle.tensor.to_dict(), seed=bundle.seed.to_dict(),
                          channels=list(bundle.channels), protocol=bundle.protocol, model=bundle.model)
            args = ['prepare']
            for key, value in inputs.items():
                path = root / (key + '.json')
                path.write_bytes(canonical_bytes(value))
                args += ['--' + key, str(path)]
            args += ['--out', str(root / 'input')]
            prepared = self.call(args)
            self.assertEqual(prepared['bundle_id'], bundle.bundle_id)
            report = self.call(['run', '--bundle', str(root / 'input'), '--steps', '4', '--out', str(root / 'run')])
            self.assertEqual(report, self.call(['verify', '--run', str(root / 'run')]))
            with self.assertRaises(SystemExit) as error:
                self.call(['verify', '--run', str(root / 'run'), '--require-physics'])
            self.assertEqual(error.exception.code, 1)
            # Hidden retained input is not silently dropped by CLI preparation.
            inputs['seed']['hidden_clock'] = 4
            (root / 'seed.json').write_bytes(canonical_bytes(inputs['seed']))
            args[-1] = str(root / 'invalid')
            with self.assertRaises(SystemExit) as error:
                self.call(args)
            self.assertEqual(error.exception.code, 2)
            self.assertFalse((root / 'invalid').exists())

    def test_exact_48_boundary_and_independent_scalar_oracle(self):
        for count in (48, 49):
            tensor = Tensor(['g' + str(i) for i in range(count)], [])
            seed = State(3, [[1] * 27] * count, [[-1] * 27] * count, [[n % 6 for n in range(27)]] * count)
            metadata = dict(channels=[dict(index=i, name=g.name, label=g.label, owner='fixture', purpose='boundary')
                                      for i, g in enumerate(tensor.gears)],
                            protocol=fixture().protocol, model=fixture().model)
            if count == 49:
                with self.assertRaisesRegex(ValueError, '48'):
                    create_bundle(tensor, seed, **metadata)
                continue
            bundle = create_bundle(tensor, seed, **metadata)
            engine = Engine(bundle.tensor)
            current = expected = bundle.seed
            for _ in range(4):
                current = engine.step(current)
                expected = scalar_step(tensor, expected)
                self.assertTrue(current.same_as(expected))
            self.assertTrue(engine.rewind(current, 4).same_as(seed))
        bundle = fixture()
        current = expected = bundle.seed
        engine = Engine(bundle.tensor)
        for _ in range(8):
            current = engine.step(current)
            expected = scalar_step(bundle.tensor, expected)
            self.assertTrue(current.same_as(expected))

    def test_perturbing_every_retained_component_obeys_face_causal_bound(self):
        tensor = fixture().tensor
        L = 7
        seed = State(L, *[np.zeros((tensor.G, L**3), dtype=np.int64) for _ in range(3)])
        engine = Engine(tensor)
        origin = (3, 3, 3)
        index = (origin[0] * L + origin[1]) * L + origin[2]
        for field in ('a', 'b', 'r'):
            for gear in range(tensor.G):
                left = seed.copy()
                right = seed.copy()
                getattr(right, field)[gear, index] = 1
                for tick in range(1, 4):
                    left, right = engine.step(left), engine.step(right)
                    difference = np.any((left.a != right.a) | (left.b != right.b) | (left.r != right.r), axis=0)
                    for node in np.flatnonzero(difference):
                        xyz = (node // (L * L), (node // L) % L, node % L)
                        distance = sum(min(abs(xyz[k] - origin[k]), L - abs(xyz[k] - origin[k])) for k in range(3))
                        self.assertLessEqual(distance, tick)

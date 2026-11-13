"""Installed light preparation, exact 2O covariance and main runtime contracts."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest

import numpy as np

from universe24.core import Engine
from universe24.core.symmetry import act, require_equivariant
from universe24.light import light_tensor, make_light_bundle, orientations, electromagnetic_fields
from universe24.runtime import main
from universe24.system.bundle import load_bundle
from validation.system_smoke import scalar_step


class NativeLightContractTests(unittest.TestCase):
    def test_all_channels_have_dynamics_and_exact_polynomial_covariance(self):
        law = light_tensor()
        self.assertEqual(law.G, 48)
        self.assertEqual(len(law.monomials), 96)
        self.assertEqual({m.target for m in law.monomials}, set(range(48)))
        self.assertTrue(all(len(m.factors) == 1 and m.coeff == 3 for m in law.monomials))
        require_equivariant(law)
        state = make_light_bundle(L=5, order=2, center=2).seed
        engine = Engine(law)
        for k in range(48):
            self.assertTrue(engine.step(act(state, k)).same_as(act(engine.step(state), k)))

    def test_all_six_directions_and_both_polarizations_translate_exactly(self):
        law = light_tensor()
        for axis in range(3):
            for sign in (-1, 1):
                for polarization in range(3):
                    if axis == polarization:
                        continue
                    bundle = make_light_bundle(L=5, axis=axis, sign=sign, polarization=polarization, order=2, center=2)
                    seed = bundle.seed
                    state = seed.copy()
                    engine = Engine(law)
                    carrier = bundle.model['preparation']['carrier']
                    for tick in range(1, 13):
                        state = engine.step(state)
                        expected = np.roll(seed.b[carrier].reshape(5, 5, 5), sign * tick, axis=axis).reshape(-1)
                        self.assertTrue(np.array_equal(state.b[carrier], expected))
                        self.assertTrue(np.array_equal(state.r, seed.r))
                        e, b = electromagnetic_fields(state)
                        self.assertTrue(all(v == 0 for v in e[axis]))
                        self.assertTrue(all(v == 0 for v in sum(e[i] * b[i] for i in range(3))))
                        self.assertTrue(all(v == 0 for v in sum(e[i] ** 2 - b[i] ** 2 for i in range(3))))
                    self.assertTrue(engine.rewind(state, 12).same_as(seed))
        self.assertTrue(Engine(law).step(seed).same_as(scalar_step(law, seed)))

    def test_main_prepares_declared_candidate_and_replays_full_state(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            root = Path(tmp)
            main(['prepare-light', '--size', '5', '--order', '2', '--center', '2', '--out', str(root / 'bundle')])
            bundle = load_bundle(root / 'bundle')
            self.assertEqual(bundle.model_contract['status'], 'passed')
            self.assertEqual(bundle.model_contract['role'], 'universe-candidate')
            self.assertEqual({c['owner'] for c in bundle.channels}, {'native-light'})
            run = main(['run', '--bundle', str(root / 'bundle'), '--steps', '4', '--out', str(root / 'run')])
            self.assertEqual(run, main(['verify', '--run', str(root / 'run')]))
            with self.assertRaises(SystemExit) as error:
                main(['verify', '--run', str(root / 'run'), '--require-physics'])
            self.assertEqual(error.exception.code, 1)

    def test_longitudinal_and_inexact_preparations_are_rejected(self):
        for kwargs in ({'polarization': 0}, {'axis': True}, {'sign': 0}, {'amplitude': 1.5}, {'order': 3}):
            with self.assertRaises(ValueError):
                make_light_bundle(**kwargs)


if __name__ == '__main__':
    unittest.main()

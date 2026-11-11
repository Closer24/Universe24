"""Fixed-six reference default, checked independently of historical presets."""
import inspect
import unittest
import numpy as np
from universe24.core import Engine, State, compose
from universe24.layers.one import one_system, build_cosmic, cosmic_params
from universe24.layers.reference import build_reference
from universe24.prepare.one import one_seed

class DefaultTests(unittest.TestCase):
    def test_default_is_explicit_reference_only(self):
        system=one_system(communication=False); tensor=compose(*system.blocks)
        self.assertEqual(tensor.G,48)
        self.assertEqual(len(tensor),288)
        self.assertEqual([b.name for b in system.blocks],['ref'])
        self.assertEqual(tensor.support_violations(),[])
        self.assertEqual(system.info['body_signs'],(1,-1,1))
        self.assertEqual(system.info['D'],6)
        self.assertIn('no emergent physics asserted',system.info['scope'])
        self.assertEqual(tensor.fingerprint,compose(build_reference(body_signs=(1,-1,1))).fingerprint)

    def test_integer_seed_and_inverse(self):
        system=one_system(communication=False); tensor=compose(*system.blocks); engine=Engine(tensor)
        for bang in ('pulse','standing','none'):
            seed,_=one_seed(system,tensor,3,bang=bang)
            self.assertTrue(np.all((seed.r>=0)&(seed.r<6)))
            forward=engine.run(seed,12)
            self.assertTrue(engine.rewind(forward,12).same_as(seed))
        self.assertTrue(engine.run(one_seed(system,tensor,3,bang='none')[0],12).same_as(one_seed(system,tensor,3,bang='none')[0]))

    def test_no_automatic_old_calibration(self):
        for fn in (build_cosmic,cosmic_params):
            with self.assertRaises(NotImplementedError):fn()
        with self.assertRaises(ValueError):one_system(couple_doublet=True)
        with self.assertRaises(ValueError):one_system(cosmic=True)
        self.assertEqual(list(inspect.signature(Engine).parameters),['tensor'])

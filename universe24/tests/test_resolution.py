"""Nonidentity divisor lifts are deliberately unavailable."""
import unittest
from universe24.core import Tensor, Engine
from universe24.layers.resolution import lift_tensor
from universe24.prepare.resolution import lift_state,unlift_state

class ResolutionRemovalTests(unittest.TestCase):
    def test_only_identity_is_accepted(self):
        tensor=Tensor(['x'],[]);seed=Engine(tensor).vacuum(3,[0])
        self.assertIs(lift_tensor(tensor,1),tensor)
        self.assertTrue(lift_state(seed,tensor,1).same_as(seed))
        self.assertTrue(unlift_state(seed,tensor,1).same_as(seed))
        for factor in (0,-1,2,7,True,1.0):
            for fn in (lambda:lift_tensor(tensor,factor),lambda:lift_state(seed,tensor,factor),lambda:unlift_state(seed,tensor,factor)):
                with self.assertRaises(ValueError):fn()

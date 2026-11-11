"""Explicit composition under the common fixed-six law."""
import unittest
import numpy as np
from universe24.core import Engine, State, compose
from universe24.core.tensor import Block, GearType
from universe24.layers.system import default_system, with_vacuum

class SystemTests(unittest.TestCase):
    def test_extra_block_is_explicit_and_uses_same_engine(self):
        clock=Block((GearType('c'),),(('c',3,(('c',(0,0,0),'b'),)),),name='clock',vacuum={'c':2})
        system=default_system(extra_blocks=(clock,));tensor=compose(*system.blocks);e=Engine(tensor)
        self.assertEqual(tensor.G,49)
        a=np.zeros((49,27),dtype=int);b=a.copy();b[-1]=7
        seed=State(3,a,b,np.zeros_like(a))
        self.assertTrue(e.run(seed,6).same_as(seed))
        self.assertTrue(e.rewind(e.run(seed,5),5).same_as(seed))
    def test_vacuum_is_remainder_not_hidden_divisor(self):
        block=default_system().by_name('ref')
        changed=with_vacuum(block,5)
        self.assertEqual(set(changed.vacuum.values()),{5})
        self.assertEqual(changed.terms,block.terms)
        for bad in (-1,6,True,1.5):
            with self.assertRaises(ValueError):with_vacuum(block,bad)

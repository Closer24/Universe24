"""Focused guards for odd signed remainders and invariant-family observations."""
import json
import time
import unittest
from research.invariant_families_v1 import run as study
from universe24 import Channel
from universe24.core.rule3 import forward


class InvariantFamilyGuards(unittest.TestCase):
    def test_odd_signed_remainder_is_not_even_complement(self):
        self.assertEqual(study.J((0,1,1)),(0,-1,5))
        positive=forward(Channel(0,1,1),4)
        negative=forward(Channel(0,-1,5),-4)
        self.assertEqual(positive,Channel(1,1,3))
        self.assertEqual(negative,Channel(-1,-1,3))
        self.assertEqual(tuple(negative),study.J(positive))
        self.assertNotEqual(forward(Channel(0,-1,3),-4),negative)

    def test_lambda_three_oracle_has_exact_six_step_return(self):
        case={'a':0,'b':1,'r':5,'lambda':3,'steps':6}
        self.assertEqual(study.scalar_trace(case),[(0,1,5),(1,1,5),(1,0,5),(0,-1,5),(-1,-1,5),(-1,0,5),(0,1,5)])

    def test_stationary_nonzero_quotient_does_not_create_click(self):
        p=json.loads(study.PROTOCOL.read_text())
        case={'id':'stationary-observer-fixture','pattern':'uniform','side':3,'lambda':6,'a':1,'b':1,'r':2,'steps':2}
        state=study.initial(case,p)
        observed=study.observe(case,[state,state,state],p,time.process_time()+10)
        self.assertTrue(observed['all_registered_oracles_pass'])
        self.assertEqual(observed['all_C'],[])
        self.assertTrue(all(value==6 for values in observed['all_native_input_sums'] for value in values))

if __name__=='__main__':unittest.main()

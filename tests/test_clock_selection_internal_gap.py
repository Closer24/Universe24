"""Exact-oracle boundaries and native click guard for the internal-mode study."""
import json
import unittest
from research.clock_selection import internal_gap_demo as d

class InternalGapContractTests(unittest.TestCase):
    def setUp(self):
        self.p=json.loads(d.PROTOCOL.read_text())

    def test_oracle_refuses_unproved_post_horizon_extension(self):
        case=next(d.planned(self.p))
        with self.assertRaises(ValueError):d.oracle(case,case['duration']+1,self.p)

    def test_stationary_offset_has_nonzero_quotient_but_no_native_click(self):
        case=next(case for case in d.planned(self.p) if case['mode']=='uniform_only')
        state=d.initial(case,self.p)
        observation=d.observe(case,[state]*(case['duration']+1),self.p)
        self.assertTrue(observation['all_triples_match_oracle'])
        self.assertTrue(observation['all_event_addresses_classes_quotients_match'])
        self.assertEqual(observation['all_C'],[])
        self.assertEqual(divmod(2*6+2,6),(2,2))

    def test_negative_mode_entries_preserve_euclidean_remainder(self):
        case=next(d.planned(self.p));old,new=d.oracle(case,2,self.p),d.oracle(case,3,self.p)
        self.assertLess(old[0].b,0)
        ell,remainder=divmod(4*old[0].b+2,6)
        self.assertEqual(remainder,2)
        self.assertEqual(tuple(new[0]),(old[0].b,ell-old[0].a,2))

    def test_inert_parity_includes_zero_vector_channels(self):
        plus=next(case for case in d.planned(self.p) if case['mode']=='gap_plus')
        parity=next(case for case in d.planned(self.p) if case['mode']=='gap_plus_parity')
        positive,odd=d.initial(plus,self.p),d.initial(parity,self.p)
        self.assertEqual(tuple(positive.at((0,0,0,1))),(0,0,2))
        self.assertEqual(tuple(odd.at((0,0,0,1))),(0,0,3))
        self.assertEqual(len(odd.cells),48*parity['side']**3)
        for t in range(plus['duration']+1):
            for a,b in zip(d.oracle(plus,t,self.p),d.oracle(parity,t,self.p)):
                self.assertEqual((a.a,a.b),(b.a,b.b))
                self.assertEqual(b.r-a.r,1)

if __name__=='__main__':unittest.main()

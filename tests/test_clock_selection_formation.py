"""Formation contract regressions: full interfaces and nonempty bridges."""
import json
import unittest
from universe24 import Cube, State
from research.clock_selection import structure_formation as f

class FormationContractTests(unittest.TestCase):
    def test_adjacent_prejoined_cores_are_not_two_isolated_clocks(self):
        with self.assertRaises(ValueError):
            f.prepared(225, 1, 1, '11')

    def test_complete_shared_halo_identity_is_not_just_center_identity(self):
        board=f.prepared(225,2,-1,'11')
        first,second,_=f.geometry(225,2)
        self.assertTrue(f.matches(board.initial,first,0))
        self.assertTrue(f.matches(board.initial,second,2))
        from universe24 import Channel
        cells=dict(board.initial.cells)
        shared=f.add(first,(1,0,0))
        cells[(*shared,0)]=Channel(0,0,4)
        altered=State(board.initial.cube,cells=cells)
        self.assertEqual(board.initial.at((*first,0)),altered.at((*first,0)))
        self.assertFalse(f.matches(altered,first,0))
        self.assertFalse(f.matches(altered,second,2))

    def test_empty_recurrent_region_is_not_a_recurrent_bridge(self):
        protocol=json.loads(f.PROTOCOL.read_text())
        case={'side':225,'distance':2,'second_sign':1,'control':'00'}
        quiet=State(Cube(225))
        observation=f.observe(case,[quiet]*97,protocol)
        self.assertEqual(observation['hold_periods'],list(range(1,17)))
        self.assertFalse(observation['hold_nonzero'])
        self.assertEqual(observation['recurrent_bridge_periods'],[])
        self.assertIsNone(observation['first_bridge_counter_activity'])

if __name__=='__main__':
    unittest.main()

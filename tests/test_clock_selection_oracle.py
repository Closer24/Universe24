"""Independent full-state checks for templates and simultaneous raw events."""
import unittest
from research.clock_selection.audit import Snapshot,all_events
from research.clock_selection.audit_structure import template,object_matches
from research.clock_selection.audit_division import geometry
from research.component_review.audit import advance,rewind


class ClockSelectionOracleTests(unittest.TestCase):
    def test_entire_pair_template_has_exact_period_five(self):
        origin=(10,10,10)
        states=[]
        for phase in range(5):
            cells={(*(a[j]+origin[j] for j in range(3)),a[3]):v for a,v in template('pair',phase)}
            states.append(Snapshot(25,(0,0,2),cells))
        for phase,state in enumerate(states):
            self.assertEqual(advance(state,(1,1,1)),states[(phase+1)%5])
            self.assertEqual(rewind(states[(phase+1)%5],(1,1,1)),state)
            self.assertTrue(object_matches(state,origin,'pair',phase))
        self.assertEqual(len({s.canonical().__repr__() for s in states}),5)

    def test_hidden_halo_remainder_invalidates_complete_object(self):
        origin=(10,10,10)
        cells={(*(a[j]+origin[j] for j in range(3)),a[3]):v for a,v in template('single',0)}
        state=Snapshot(25,(0,0,2),cells)
        self.assertTrue(object_matches(state,origin,'single',0))
        cells[(11,10,10,47)]=(0,0,3)
        self.assertFalse(object_matches(Snapshot(25,(0,0,2),cells),origin,'single',0))

    def test_one_initial_donor_produces_six_simultaneous_C0(self):
        center,neighbors=geometry(29)
        initial=Snapshot(29,(0,0,2),{center:(0,3,2)})
        after=advance(initial,(1,1,1));events=all_events([initial,after])[0]
        self.assertEqual({tuple(e['address']) for e in events},set(neighbors))
        self.assertEqual(len(events),6)
        self.assertTrue(all(e['kind']==0 and e['quotient']=='1' for e in events))
        self.assertEqual(rewind(after,(1,1,1)),initial)


if __name__=='__main__':unittest.main()

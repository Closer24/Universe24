"""Complete null identity and source-caused activation observer regressions."""
import json
import unittest
from universe24 import State,Channel
from research.experiments.run import assemble
from research.clock_selection import route_clock as r

class RouteClockContractTests(unittest.TestCase):
    def setUp(self):self.p=json.loads(r.PROTOCOL.read_text())

    def test_full_null_identity_includes_the_modified_contact_companion(self):
        case=next(pair[0] for pair in r.planned_pairs(self.p) if pair[0]['stage']=='primary')
        base=assemble(r.spec(case,self.p)).initial;states=[]
        for t in range(81):
            cells=dict(base.cells)
            for direction in r.sides(case):
                origin=r.center(case,direction)
                for a,v in r.clock_cells((case['phase']+t)%4).items():cells[(*r.add(origin,a[:3]),a[3])]=Channel(*v)
            states.append(State(base.cube,cells=cells))
        observed=r.observe(case,states,self.p)
        self.assertTrue(all(x['complete_canonical_null_orbit'] for x in observed['clocks'].values()))
        self.assertTrue(all(x['primary_unit_r0_quiet'] for x in observed['clocks'].values()))
        origin=r.center(case,-1);contact=(origin[0],origin[1]-1,origin[2],14)
        changed=[]
        for state in states:
            cells=dict(state.cells);cells[contact]=Channel(0,0,2);changed.append(State(state.cube,cells=cells))
        wrong=r.observe(case,changed,self.p)
        self.assertFalse(wrong['clocks']['-1']['complete_canonical_null_orbit'])

    def test_an_invented_counter_jump_without_input_is_not_activation_evidence(self):
        case=next(pair[0] for pair in r.planned_pairs(self.p) if pair[0]['stage']=='clock_off')
        initial=assemble(r.spec(case,self.p)).initial;origin=r.center(case,-1)
        cells=dict(initial.cells);cells[(*origin,2)]=Channel(0,1,0)
        jumped=State(initial.cube,cells=cells)
        observed=r.observe(case,[initial]+[jumped]*80,self.p)
        activation=observed['clocks']['-1']['first_activation']
        self.assertIsNotNone(activation)
        self.assertFalse(activation['zero_to_counter_guard_consistent'])
        self.assertEqual(activation['u'],0)

if __name__=='__main__':unittest.main()

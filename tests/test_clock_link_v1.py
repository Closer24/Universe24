import unittest

from research.clock_link_v1 import assemble_clock_link, echo_parity, target_record
from research.clock_link_v1.exact import closed_state
from universe24 import State, Cube, Engine, Coupling


class ClockLinkContractTests(unittest.TestCase):
    def test_documented_round_trip(self):
        p = assemble_clock_link(distance=14,side=17,origin=(1,1,1))
        states = list(p.engine.evolve(p.initial,60))
        self.assertEqual(states[60],p.initial)
        self.assertEqual(echo_parity(states[30].at((1,1,1,0))),1)
        self.assertEqual(target_record(states[16].at((15,1,1,0))),4)
        self.assertEqual(target_record(states[43].at((15,1,1,0))),4)
        self.assertEqual(target_record(states[44].at((15,1,1,0))),1)

    def test_smallest_theorem_case_on_minimum_cube(self):
        e = Engine(Coupling((1,1,1)))
        state = State(Cube(5),cells=closed_state(2,0,5,origin=(1,1,1)))
        initial = state
        for t in range(13):
            self.assertEqual({a:tuple(v) for a,v in state.cells.items()},
                             closed_state(2,t,5,origin=(1,1,1)))
            if t < 12:
                state = e.advance(state)
        self.assertEqual(state,initial)

    def test_delay_is_complete_state_delay(self):
        p = assemble_clock_link(distance=14,side=31,origin=(1,1,1))
        delayed = assemble_clock_link(distance=14,side=31,origin=(1,1,1),delay=1)
        self.assertEqual(delayed.engine.advance(delayed.initial),p.initial)

    def test_source_absence_and_undefined_readout(self):
        p = assemble_clock_link(distance=14,source_present=False)
        self.assertEqual(p.engine.advance(p.initial),p.initial)
        self.assertIsNone(echo_parity((0,0,2)))

    def test_declared_geometry_and_retention_domain(self):
        for params in ({'distance':12},{'distance':15},{'distance':True},
                       {'distance':14,'side':16},
                       {'distance':14,'side':32,'terminated':False,'control_extent':30}):
            with self.subTest(params=params), self.assertRaises(ValueError):
                assemble_clock_link(**params)
        assemble_clock_link(distance=14,side=17,origin=(1,1,1))


if __name__=='__main__':
    unittest.main()

"""Periodic carrier templates and initial controls, without encounter simulation."""
import json
import unittest
from universe24 import Channel, State
from research.experiments.run import assemble
from research.clock_selection.recurrence import PROTOCOL, cases, case_spec, packet_matches, translated


class RecurrencePreparationTests(unittest.TestCase):
    def test_periodic_template_includes_hidden_channel_remainders(self):
        p=json.loads(PROTOCOL.read_text());case=next(cases(p));side=case['side'];c=side//2
        state=assemble(case_spec(case,p)).initial
        # Translation here creates a fresh initial placement, not runtime motion.
        moved=translated(state,side-1-(c-16))
        self.assertTrue(packet_matches(moved,side-1,c,c))
        cells=dict(moved.cells);cells[(0,c,c,47)]=Channel(0,0,3)
        corrupted=State(moved.cube,moved.background,cells)
        self.assertFalse(packet_matches(corrupted,side-1,c,c))

    def test_all_registered_initial_remainders_match_within_controls(self):
        p=json.loads(PROTOCOL.read_text());groups={};prepared=0
        for case in cases(p):
            state=assemble(case_spec(case,p)).initial;prepared+=1
            if not case['pristine']:groups.setdefault(case['side'],[]).append(state)
        self.assertEqual(prepared,20)
        for group in groups.values():
            addresses=set().union(*(s.cells for s in group))
            self.assertTrue(all(len({s.at(a).r for s in group})==1 for a in addresses))


if __name__=='__main__':unittest.main()

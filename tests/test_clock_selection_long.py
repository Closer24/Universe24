"""Recording limits must cover the approved horizon without changing the board."""
import json
import unittest

from research.clock_selection import recurrence, recurrence_long
from research.experiments.run import assemble


class LongRecurrencePreparationTests(unittest.TestCase):
    def test_complete_frame_budget_and_initial_state_match_original_preparation(self):
        p=json.loads(recurrence_long.PROTOCOL.read_text())
        for case in recurrence_long.cases(p):
            spec=recurrence_long.case_spec(case,p)
            short_spec=recurrence.case_spec(case,p)
            self.assertEqual(spec["budget"]["max_frames"],32*case["side"]+41)
            self.assertEqual(spec["steps"]+1,spec["budget"]["max_frames"])
            self.assertEqual(assemble(spec).initial,assemble(short_spec).initial)
            self.assertEqual(spec["budget"]["max_cells"],500000)


if __name__=="__main__":unittest.main()

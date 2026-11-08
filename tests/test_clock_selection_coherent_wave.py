"""Failed coherent-sector observations must retain actual hidden channels."""
import importlib.util
import json
import unittest
from universe24 import Channel,Cube,State
from research.clock_selection.coherent_wave import PROTOCOL,observe


@unittest.skipUnless(importlib.util.find_spec("mpmath"),"Optional mpmath1.3.0 interval preparation dependency")
class CoherentWaveObservationTests(unittest.TestCase):
    def test_noncoherent_hidden_event_and_odd_remainder_are_not_copied_from_channel_zero(self):
        p=json.loads(PROTOCOL.read_text());case={"side":7,"n":[1,0,0],"amplitude":1000}
        before=State(Cube(7),Channel(0,0,2),{})
        after=State(before.cube,before.background,{(0,0,0,47):Channel(0,1,4),(0,0,0,46):Channel(0,0,3)})
        result=observe(case,p,[before,after])
        self.assertFalse(result["all48_coherent"])
        self.assertFalse(result["remainder_parity_preserved"])
        self.assertEqual(result["all_C"],[[1,0,0,0,47,1,"1"]])


if __name__=="__main__":unittest.main()

"""Milestone regressions for exact event-wave and remainder parity identities."""
import unittest
from universe24.core.state import Cube,State,Channel
from universe24.core.engine import Engine
from universe24.core.coupling import Coupling
from research.gravity_event_clocks_v1.worker1_algebra import p

class GravityEventClockMilestoneTests(unittest.TestCase):
    def test_exact_wave_and_balance_each_signed_coupling(self):
        for signs in ((1,1,1),(-1,-1,-1),(1,-1,1)):
            engine=Engine(Coupling(signs));cube=Cube(3)
            cells={(1,1,1,g):Channel(-3+g%5,1-g%4,(g+2)%6) for g in range(48)}
            state=State(cube,cells=cells)
            following=engine.advance(state)
            self.assertEqual(engine.rewind(following),state)
            sums=engine.input_sums(state)
            for a in state.cells.keys()|following.cells.keys()|sums.keys():
                v,w=state.at(a),following.at(a);lap=6*v.b-sums.get(a,0)
                self.assertEqual(6*(w.b-2*v.b+v.a)+2*lap+w.r-v.r,0)
                self.assertEqual(p(w)-p(v),-lap)
    def test_remainder_parity_is_dynamically_decoupled(self):
        for signs in ((1,1,1),(-1,1,-1)):
            eng=Engine(Coupling(signs));cube=Cube(3)
            cells={(1,1,1,g):Channel(g%7-3,2-g%6,g%6) for g in range(48)}
            twin={addr:Channel(v.a,v.b,v.r^1) for addr,v in cells.items()}
            a,b=State(cube,cells=cells),State(cube,cells=twin)
            for _ in range(6):
                for addr in a.cells.keys()|b.cells.keys():
                    va,vb=a.at(addr),b.at(addr)
                    self.assertEqual((va.a,va.b,va.r//2),(vb.a,vb.b,vb.r//2))
                a,b=eng.advance(a),eng.advance(b)
    def test_signed_spectrum_receipt_scope(self):
        import json
        from pathlib import Path
        path=Path(__file__).resolve().parents[1]/"research"/"gravity_event_clocks_v1"/"results"/"worker3_einstein.json"
        obj=json.loads(path.read_text())
        self.assertTrue(obj["status"]=="PASS")
        self.assertEqual(obj["full48_internal_spectrum"]["unique_lambda6_multiplicity"],1)
        self.assertIn("not",obj["science_scope"].lower())

if __name__=="__main__": unittest.main()

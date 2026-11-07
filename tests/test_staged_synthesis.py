"""Exact SMT semantics and independent full-state agreement, not research search."""
import importlib.util
import json
import unittest

from research.staged_blocks import synthesis as syn
from research.component_review import audit as independent
from universe24 import Coupling, Cube, State


HAS_Z3=importlib.util.find_spec("z3") is not None


@unittest.skipUnless(HAS_Z3,"Optional z3-solver==4.15.4.0 is not installed")
class ExactSynthesisTests(unittest.TestCase):
    def test_zero_counter_reduction_for_every_valid_remainder(self):
        import z3
        solver=z3.SolverFor("QF_LIA")
        remainder=z3.Int("arbitrary_valid_initial_remainder")
        solver.add(remainder>=0,remainder<6)
        actual=syn.add_rule3_constraints(solver,(z3.IntVal(0),z3.IntVal(0),remainder),z3.IntVal(0),"stationary")
        solver.add(z3.Or(actual[0]!=0,actual[1]!=0,actual[2]!=remainder))
        self.assertEqual(solver.check(),z3.unsat)

    def test_signed_and_large_division_is_unique(self):
        import z3
        for a,b,r,u in ((0,0,0,-1),(7,-9,5,-100),(-10**80,10**90,0,-10**100),
                        (10**80,-10**90,5,10**100),(0,0,4,1),(0,0,2,-1)):
            with self.subTest(a=a,r=r,u=u):
                solver=z3.SolverFor("QF_LIA")
                actual=syn.add_rule3_constraints(solver,tuple(z3.IntVal(v) for v in (a,b,r)),z3.IntVal(u),"test")
                quotient,remainder=divmod(2*u+r,6)
                expected=(b,quotient-a,remainder)
                self.assertEqual(solver.check(),z3.sat)
                model=solver.model()
                self.assertEqual(tuple(model.eval(v).as_long() for v in actual),expected)
                solver.add(z3.Or(*[value!=want for value,want in zip(actual,expected)]))
                self.assertEqual(solver.check(),z3.unsat)

    def test_full_periodic_state_matches_independent_matrix_oracle(self):
        import z3
        coupling=Coupling((1,-1,1))
        initial=State(Cube(3),cells={(0,0,0,0):(1,-1,4),(2,0,0,14):(-1,1,0),
                                   (1,2,0,7):(0,2,2),(0,2,1,25):(0,0,0)})
        active={a for a,v in initial.cells.items() if v.a or v.b}
        all_addresses={(x,y,z,g) for x in range(3) for y in range(3) for z in range(3) for g in range(48)}
        observations={t:all_addresses for t in range(4)}
        forward=syn.forward_cones(3,coupling.ports,active,3)
        needed=syn.dependency_cones(3,coupling.ports,forward,observations)
        solver=z3.SolverFor("QF_LIA")
        encoded=syn.ExactConeEncoding(solver,initial,coupling,{},forward,needed,prefix="matrix").build()
        self.assertEqual(solver.check(),z3.sat)
        model=solver.model()
        oracle=independent.from_state(initial)
        for t in range(4):
            for address in all_addresses:
                actual=tuple(model.eval(v).as_long() for v in encoded.state(t,address))
                self.assertEqual(actual,oracle.at(address),(t,address))
            if t<3:
                following=independent.advance(oracle,(1,-1,1))
                self.assertEqual(independent.rewind(following,(1,-1,1)),oracle)
                oracle=following

class StructuralSynthesisTests(unittest.TestCase):
    def test_apparatus_is_shared_and_receiver_cannot_be_preloaded(self):
        p=json.loads(syn.DEFAULT_PROTOCOL.read_text())
        values=[(0,2,4)[i%3] for i in range(22)]
        on=syn.assemble(syn.spec_for(p,values,True)).initial
        off=syn.assemble(syn.spec_for(p,values,False)).initial
        self.assertTrue(all(v.a==v.b==0 for v in off.cells.values()))
        for address in set(on.cells)|set(off.cells):
            self.assertEqual(on.at(address).r,off.at(address).r)
        self.assertEqual([on.at((*p["receiver"],g)).r for g in (0,14)],[4,2])
        oracle=independent.from_state(off)
        self.assertEqual(independent.advance(oracle),oracle)
        bad=json.loads(json.dumps(p))
        bad["unknown_remainder_addresses"][0]=[*p["receiver"],0]
        with self.assertRaises(ValueError):syn.validate_protocol(bad)

    def test_complete_causal_preflight_and_cap(self):
        p=json.loads(syn.DEFAULT_PROTOCOL.read_text())
        prepared,absent,forward,needed,details=syn.preflight(p)
        self.assertEqual(details["encoded_channel_updates"],24776)
        self.assertEqual(len(needed[-1]),48)
        for t in range(1,len(needed)):
            for address in needed[t]:
                parents=[address]+[prepared.initial.cube.adjacent(address,d,prepared.engine.coupling.ports[d][address[3]]) for d in range(6)]
                for parent in parents:
                    self.assertTrue(parent in needed[t-1] or parent not in forward[t-1])
        bad=json.loads(json.dumps(p));bad["budget"]["max_channel_updates"]=24775
        with self.assertRaises(syn.EncodingLimit):syn.preflight(bad)


if __name__=="__main__":
    unittest.main()

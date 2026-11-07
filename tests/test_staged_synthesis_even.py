"""Parity-coordinate equivalence and complete physical-state replay tests."""
import importlib.util
import json
import unittest

from research.staged_blocks import synthesis as base
from research.staged_blocks import synthesis_even as even
from research.component_review import audit as independent
from universe24 import Coupling,Cube,State


@unittest.skipUnless(importlib.util.find_spec("z3") is not None,"Optional z3-solver is unavailable")
class EvenEncodingTests(unittest.TestCase):
    def test_symbolic_bijection_including_unbounded_signed_inputs(self):
        import z3
        a,b,u,s=z3.Ints("equiv_a equiv_b equiv_u equiv_s")
        solver=z3.SolverFor("QF_LIA")
        solver.add(s>=0,s<=2)
        physical=base.add_rule3_constraints(solver,(a,b,2*s),u,"physical")
        scaled=even.add_even_rule3_constraints(solver,(a,b,s),u,"scaled")
        solver.add(z3.Or(physical[0]!=scaled[0],physical[1]!=scaled[1],physical[2]!=2*scaled[2]))
        self.assertEqual(solver.check(),z3.unsat)

    def test_full_periodic_physical_states_match_matrix_oracle(self):
        import z3
        coupling=Coupling((1,-1,1))
        initial=State(Cube(3),cells={(0,0,0,0):(1,-1,4),(2,0,0,14):(-1,1,0),
                                   (1,2,0,7):(0,2,2),(0,2,1,25):(0,0,0)})
        active={a for a,v in initial.cells.items() if v.a or v.b}
        addresses={(x,y,z,g) for x in range(3) for y in range(3) for z in range(3) for g in range(48)}
        forward=base.forward_cones(3,coupling.ports,active,3)
        needed=base.dependency_cones(3,coupling.ports,forward,{t:addresses for t in range(4)})
        solver=z3.SolverFor("QF_LIA")
        encoded=even.EvenConeEncoding(solver,initial,coupling,{},forward,needed).build()
        self.assertEqual(solver.check(),z3.sat)
        model=solver.model();oracle=independent.from_state(initial)
        for t in range(4):
            for address in addresses:
                actual=tuple(model.eval(v).as_long() for v in encoded.physical_state(t,address))
                self.assertEqual(actual,oracle.at(address),(t,address))
            if t<3:oracle=independent.advance(oracle,(1,-1,1))


class EvenProtocolTests(unittest.TestCase):
    def test_no_physical_family_or_observer_change(self):
        p=json.loads(even.DEFAULT_PROTOCOL.read_text())
        even.validate_equivalent_family(p)
        bad=json.loads(json.dumps(p));bad["pending_pair"]=[0,4]
        with self.assertRaises(ValueError):even.validate_equivalent_family(bad)
        bad=json.loads(json.dumps(p));bad["source"][0]+=1
        with self.assertRaises(ValueError):even.validate_equivalent_family(bad)


if __name__=="__main__":unittest.main()

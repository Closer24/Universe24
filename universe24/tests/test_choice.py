"""Integer carrier and detector polynomials; no Born or Bell claim."""
import unittest
import numpy as np
from universe24.core import Engine,State,compose
from universe24.layers.choice import build_clock_ring,build_fibre,build_born_router,build_which_path_W
class ChoicePolynomialTests(unittest.TestCase):
    def test_ring_exact_period_six(self):
        tensor=compose(build_clock_ring());e=Engine(tensor)
        b=np.arange(tensor.G*27).reshape(tensor.G,27)-17
        seed=State(3,b+3,b,np.arange(tensor.G*27).reshape(tensor.G,27)%6)
        self.assertTrue(e.run(seed,6).same_as(seed))
    def test_fibre_carries_exact_translated_integer_profile(self):
        tensor=compose(build_fibre());e=Engine(tensor);L=4
        b=np.zeros((1,L**3),dtype=int);b[0,0]=5
        dummy=State(L,b,b,np.zeros_like(b));shift=dummy.lattice.shift_index((1,0,0))
        seed=State(L,b[:,shift],b,np.zeros_like(b))
        next_state=e.step(seed)
        np.testing.assert_array_equal(next_state.b,b[:,dummy.lattice.shift_index((-1,0,0))])
        self.assertTrue(e.rewind(e.run(seed,8),8).same_as(seed))
    def test_detector_input_equals_squared_arm_formula(self):
        one=build_clock_ring(name='a');two=build_clock_ring(name='b')
        arms=[[f'{ns}.X{i}' for i in range(3)] for ns in ('a','b')]
        router=build_born_router(kappa=2,arm1=arms[0],arm2=arms[1])
        tensor=compose(one,two,router);e=Engine(tensor)
        b=np.arange(tensor.G*27).reshape(tensor.G,27)%7-3
        s=State(3,b,b,np.zeros_like(b));u=e.inputs(s)
        for name,sgn,weight in [('dP',1,2),('dM',-1,-2)]:
            expected=weight*np.sum((b[:3]+sgn*b[3:6])**2,axis=0)
            np.testing.assert_array_equal(u[tensor.gear_index('router.'+name)],expected)
        self.assertTrue(e.rewind(e.run(s,4),4).same_as(s))
    def test_which_path_is_explicit_fixed_six_coupling(self):
        arm=build_clock_ring(name='arm');w=build_which_path_W(arm=[f'arm.X{i}' for i in range(3)],N=3)
        tensor=compose(arm,w);e=Engine(tensor);s=e.vacuum(3,[0]*tensor.G)
        s.b[:]=1
        self.assertTrue(e.inverse_step(e.step(s)).same_as(s))

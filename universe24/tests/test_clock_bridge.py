"""Exact algebra and scoped feedback controls for the optional clock bridge."""
import unittest
import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.core.reciprocity import check_reciprocity
from universe24.layers.clock_bridge import build_clock_record_bridge

ZERO = (0,0,0)


def fixture(kappa=12):
    Q=17;D=6*Q
    names=['clock.local','record.positive','record.negative','load.positive','load.negative','reader.scalar']
    c,p,m,lp,lm,reader=names
    f=lambda n:(n,ZERO,'b')
    bridge=build_clock_record_bridge(Q=Q,clock=c,positive=p,negative=m,kappa=kappa,include_free_clock=True)
    terms=[(p,3,(f(reader),f(reader),f(lp))),
           (m,-3,(f(reader),f(reader),f(lm)))]
    terms += [(g,D,(f(g),)) for g in (lp,lm,reader)]
    tensor=Tensor(names,terms+list(bridge.terms),Q=Q,strict_support=True)
    a=np.zeros((6,27),dtype=np.int64);b=a.copy();r=a.copy()+D//2-1
    b[0]=4
    for g,value in ((3,5),(4,12),(5,1)):
        a[g]=value;b[g]=value
    r[1:3]=0
    seed=State(3,a,b,r)
    return tensor,Engine(tensor,Q),seed


class ClockBridgeTests(unittest.TestCase):
    def test_bridge_is_generic_reciprocal_local_tensor_data(self):
        b=build_clock_record_bridge(Q=17,clock='alpha',positive='beta',negative='gamma',
                                   kappa=12,include_free_clock=True)
        t=Tensor(['alpha','beta','gamma'],b.terms,Q=17,strict_support=True)
        self.assertEqual(t.rank,2)
        self.assertTrue(t.b_only)
        self.assertEqual(t.support_violations(),[])
        self.assertTrue(check_reciprocity(t).ok)
        self.assertEqual(len(t.designations),0)
        e=Engine(t,17);a=np.arange(81,dtype=np.int64).reshape(3,27)-40
        s=State(3,a,a+7,(a+40)%102)
        u=e.inputs(s)
        np.testing.assert_array_equal(u[0],51*s.b[0]-12*(s.b[1]+s.b[2]))
        np.testing.assert_array_equal(u[1],-12*s.b[0])
        np.testing.assert_array_equal(u[2],-12*s.b[0])

    def test_shared_token_can_change_future_clock_with_unchanged_loads(self):
        observed={}
        for kappa in (0,12):
            tensor,e,initial=fixture(kappa)
            other=initial.copy();other.r[1:3]=90
            s,v=initial,other
            first_record=first_clock=None
            max_counter=0
            carry_p=np.zeros(27,dtype=object);sum_input_p=np.zeros(27,dtype=object)
            for tick in range(1,1001):
                n,w=e.step(s),e.step(v)
                ell_p=n.b[1]+s.a[1];ell_m=n.b[2]+s.a[2]
                # I=1 and static loads sum to Q; common bridge force cancels.
                np.testing.assert_array_equal(ell_p-ell_m,np.ones(27,dtype=np.int64))
                np.testing.assert_array_equal(n.r[1],n.r[2])
                carry_p+=ell_p
                sum_input_p+=2*(3*5-kappa*s.b[0])
                if first_record is None and not np.array_equal(n.b[1:3],w.b[1:3]):first_record=tick
                if first_clock is None and not np.array_equal(n.b[0],w.b[0]):first_clock=tick
                max_counter=max(max_counter,n.max_abs(),w.max_abs())
                s,v=n,w
            np.testing.assert_array_equal(e.D*carry_p,sum_input_p+initial.r[1]-s.r[1])
            self.assertTrue(e.rewind(s,1000).same_as(initial))
            self.assertTrue(e.rewind(v,1000).same_as(other))
            # A declared finite-horizon numerical control, not global stability.
            self.assertLess(max_counter,64)
            observed[kappa]=(first_record,first_clock)
        self.assertEqual(observed[0],(1,None))
        self.assertEqual(observed[12],(1,2))

    def test_large_integer_bridge_uses_same_inverse(self):
        Q=1<<80
        b=build_clock_record_bridge(Q=Q,clock='clock',positive='left',negative='right',
                                   kappa=Q,include_free_clock=True)
        t=Tensor(['clock','left','right'],b.terms,Q=Q)
        e=Engine(t,Q);a=np.array([[2**90]*27,[-2**85]*27,[3]*27],dtype=object)
        s=State(3,a,-a,[[0]*27,[1]*27,[6*Q-1]*27])
        self.assertTrue(e.rewind(e.run(s,12),12).same_as(s))

    def test_rejects_invalid_builder_data(self):
        valid=dict(Q=17,clock='c',positive='p',negative='m',kappa=12)
        for key,value in [('Q',0),('Q',True),('kappa',-1),('kappa',0.5),
                          ('clock',''),('positive','c')]:
            with self.assertRaises(ValueError):build_clock_record_bridge(**dict(valid,**{key:value}))
        with self.assertRaises(TypeError):
            build_clock_record_bridge(**valid,include_free_clock=1)

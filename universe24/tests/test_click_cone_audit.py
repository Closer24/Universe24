"""Check modular C2 semantics and non-vacuous event-cone/complexity controls."""
import unittest
import numpy as np
from universe24.core import Engine, State, Tensor
from universe24.demos.communication.run_communication import build
from experiments.cosmology.click_cone_audit import (
    trace, event_cone, communication_case, c2_periodic_case, reception_control,
)


class ClickConeTests(unittest.TestCase):
    def test_all_remainders_signed_and_big_inputs_obey_class_and_record_rule(self):
        inputs=[-(1<<80)-1,-7,-2,-1,0,1,2,3,7,(1<<80)+1]
        names=[f'x{i}' for i in range(len(inputs))]
        tensor=Tensor(names,[(name,u,()) for name,u in zip(names,inputs)])
        zero=np.zeros((len(inputs),27),dtype=object)
        remainders=np.tile(np.arange(27)%6,(len(inputs),1))
        seed=State(3,zero,zero.copy(),remainders)
        engine=Engine(tensor);after=engine.step(seed)
        log=engine.clicks(seed,after)
        events={(int(g),int(n)):(int(k),int(q)) for g,n,k,q in
                zip(log.gear,log.node,log.kind,log.quotient)}
        for g,u in enumerate(inputs):
            for n in range(27):
                q,r=divmod(2*u+n%6,6)
                self.assertEqual(int(after.r[g,n]),r)
                if q:
                    self.assertEqual(events[(g,n)],(u%3,q))
                else:
                    self.assertNotIn((g,n),events)
        self.assertTrue(engine.inverse_step(after).same_as(seed))

    def test_changed_c2_records_obey_cone_from_complete_initial_support(self):
        _,tensor,_,seed,_=build(7,'none',model='reference')
        changed=seed.copy();changed.b[0,seed.lattice.index(3,3,3)]=17
        result=event_cone(tensor,seed,changed,3)
        self.assertGreater(len(result['C2_points']),0)
        self.assertTrue(all(p['distance']<=p['update'] for p in result['C2_points']))
        self.assertTrue(result['exact_rewind'])
        tensor,pulse=communication_case(3,L=7);_,quiet=communication_case(0,L=7)
        prepared=event_cone(tensor,quiet,pulse,3)
        self.assertEqual(len(prepared['initial_changed_sites']),7)
        self.assertGreater(len(prepared['C2_points']),0)

    def test_message_payload_changes_c2_onset_without_an_event_callback(self):
        for amplitude,first in ((1,2),(3,3),(9,4)):
            tensor,seed=communication_case(amplitude)
            result=trace(tensor,seed,6)
            self.assertEqual(result['first_C2_update'],first)
            self.assertEqual(result['carrier_C2'],0)
            self.assertTrue(result['observation_free_replay_matches'])
        tensor,seed=communication_case(3,False)
        self.assertEqual(trace(tensor,seed,6)['counts']['C2'],0)
        self.assertTrue(reception_control()['receiver_remainders_identical'])

    def test_c2_can_repeat_with_identical_full_state_and_c0_can_spread_patterns(self):
        tensor,seed=c2_periodic_case(3)
        result=trace(tensor,seed,12)
        self.assertEqual(result['full_state_returns'],[3,6,9,12])
        self.assertEqual(result['counts'],{'C0':0,'C1':0,'C2':216})
        _,tensor,_,seed,_=build(5,'pulse',model='reference')
        spread=trace(tensor,seed,1)
        self.assertEqual(spread['counts']['C2'],0)
        self.assertGreater(spread['samples'][1]['site_pattern_types'],spread['samples'][0]['site_pattern_types'])

    def test_multiple_of_three_tensor_preserves_every_remainder(self):
        tensor=Tensor(['ref.x','ref.y'],[
            ('ref.x',3,(('ref.y',(1,0,0),'b'),('ref.x',(0,0,0),'b'))),
            ('ref.y',-6,(('ref.x',(0,0,0),'b'),)),('ref.x',3,())],strict_support=True)
        engine=Engine(tensor)
        a=np.arange(54).reshape(2,27)-20;b=-a;r=np.arange(54).reshape(2,27)%6
        state=State(3,a,b,r)
        for _ in range(3):
            following=engine.step(state)
            np.testing.assert_array_equal(following.r,state.r)
            self.assertTrue(all(int(k)==0 for k in engine.clicks(state,following).kind))
            state=following

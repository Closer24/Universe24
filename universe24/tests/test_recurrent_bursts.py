"""Guard against treating amplitude growth or carrier echoes as new complexity."""
import tempfile
from pathlib import Path
import json
import gzip
import unittest
import numpy as np

from universe24.core import State, Engine, Tensor
from universe24.demos.communication.run_communication import build
from experiments.cosmology.recurrent_bursts import (
    ReassemblyTracker, structural_snapshot, progressive_reassemblies,
    candidate_tensor, run_case, FAMILIES,
)


class BurstAuditTests(unittest.TestCase):
    def test_scale_invariance_rejects_magnitude_as_complexity(self):
        b = np.zeros((2,125), dtype=object)
        b[0,0], b[0,3], b[1,3] = 2,-3,1
        s = State(5, b.copy(), b, np.zeros_like(b))
        row, signatures = structural_snapshot(s, [0,1])
        grown = State(5, s.a.astype(object) * (1 << 80), s.b.astype(object) * (1 << 80), s.r)
        other, signatures2 = structural_snapshot(grown, [0,1])
        for key in ('compact','dispersed','site_pattern_types','edge_pattern_types',
                    'persistent_pattern_types','normalized_fingerprint'):
            self.assertEqual(row[key], other[key], key)
        self.assertEqual(signatures, signatures2)
        self.assertNotEqual(row['reference_mass'], other['reference_mass'])

    def test_compact_ball_and_persistence_are_exact(self):
        b = np.zeros((1,343), dtype=int)
        state = State(7,b,b.copy(),b.copy())
        origin=state.lattice.index(3,3,3)
        state.b[0,origin]=1
        row, signatures = structural_snapshot(state,[0])
        self.assertTrue(row['compact'])
        self.assertFalse(row['dispersed'])
        self.assertEqual(row['persistent_pattern_types'],0)
        stable,_=structural_snapshot(state,[0],(signatures,signatures))
        self.assertEqual(stable['persistent_pattern_types'],1)
        state.b[:]=1
        spread,_=structural_snapshot(state,[0])
        self.assertFalse(spread['compact'])
        self.assertTrue(spread['dispersed'])

    def test_hysteresis_requires_departure_before_another_burst(self):
        tracker=ReassemblyTracker()
        for tick in range(5):
            tracker.observe(dict(update=tick,compact=True,dispersed=False))
        self.assertEqual(tracker.events,[])
        tracker.observe(dict(update=5,compact=False,dispersed=True))
        tracker.observe(dict(update=6,compact=False,dispersed=False))
        tracker.observe(dict(update=7,compact=True,dispersed=False))
        self.assertEqual([r['update'] for r in tracker.events],[7])

    def test_growth_requires_persistent_structure_and_all_cycle_comparisons(self):
        def event(s,e,p):
            return dict(site_pattern_types=s,edge_pattern_types=e,persistent_pattern_types=p)
        positive=[event(i,i+1,1) for i in range(1,5)]
        self.assertTrue(progressive_reassemblies(positive))
        self.assertFalse(progressive_reassemblies([event(4,5,1)]*4))
        self.assertFalse(progressive_reassemblies([event(i,i+1,0) for i in range(1,5)]))
        self.assertFalse(progressive_reassemblies([event(1,2,1),event(2,3,1),event(1,4,1),event(3,5,1)]))
        self.assertFalse(progressive_reassemblies(positive[:3]))

    def test_actual_periodic_shell_has_bursts_but_no_growth(self):
        report=run_case(L=7,steps=70,family='periodic_control')
        self.assertGreaterEqual(len(report['reference_reassemblies']),4)
        self.assertEqual(report['full_state_returns'],list(range(7,71,7)))
        self.assertTrue(report['gates']['recurrent_reference_bursts'])
        self.assertFalse(report['gates']['growing_structural_proxies'])
        self.assertFalse(report['user_goal_demonstrated'])
        self.assertIsNone(report['gates']['feedback_attribution_demonstrated'])
        self.assertIsNone(report['gates']['stagnation_trigger_demonstrated'])
        self.assertTrue(report['exact_rewind'])

    def test_current_default_carrier_echo_is_not_reference_reassembly(self):
        report=run_case(L=5,steps=25)
        self.assertEqual(report['carrier_focus_updates'],[5,10,15,20,25])
        self.assertEqual(report['reference_reassemblies'],[])
        self.assertTrue(report['exact_rewind'])
        self.assertFalse(report['user_goal_demonstrated'])

    def test_feedback_is_local_changes_carriers_and_remains_reversible(self):
        _,base,_,empty,_=build(5,'none')
        origin=empty.lattice.index(2,2,2)
        target=empty.lattice.index(3,2,2)
        for family in FAMILIES:
            tensor=candidate_tensor(base,family,1)
            engine=Engine(tensor)
            seed=empty.copy()
            seed.b[48,origin]=3
            changed=seed.copy()
            changed.b[0,target]=3
            before,after=engine.step(seed),engine.step(changed)
            self.assertNotEqual(int(before.b[48,origin]),int(after.b[48,origin]))
            self.assertEqual(tensor.support_violations(),[])
            self.assertTrue(engine.inverse_step(after).same_as(changed))
        control=Engine(base)
        np.testing.assert_array_equal(control.step(seed).b[48:],control.step(changed).b[48:])

    def test_resource_stop_retains_exact_complete_step_and_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            result=run_case(steps=20,family='cubic',coefficient=1,max_bits=12,out=directory)
            self.assertEqual(result['stop_reason'],'counter_bit_limit')
            self.assertLess(result['completed_updates'],20)
            root=Path(directory)
            tensor=Tensor.from_json((root/'tensor.json').read_text())
            with gzip.open(root/'initial.json.gz','rt') as f: seed=State.from_dict(json.load(f))
            with gzip.open(root/'final.json.gz','rt') as f: final=State.from_dict(json.load(f))
            engine=Engine(tensor)
            self.assertTrue(engine.run(seed,result['completed_updates']).same_as(final))
            self.assertTrue(engine.rewind(final,result['completed_updates']).same_as(seed))
            self.assertFalse(result['user_goal_demonstrated'])

    def test_disconnected_and_empty_controls_stay_reference_silent(self):
        for options in ({'family':'disconnected'},{'amplitude':0}):
            report=run_case(steps=12,**options)
            self.assertEqual(report['maximum_site_pattern_types'],0)
            self.assertEqual(report['reference_reassemblies'],[])
            self.assertTrue(report['exact_rewind'])

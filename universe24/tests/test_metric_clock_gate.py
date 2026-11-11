"""Physical distinction: equal dispersion factors need not give equal clock rates."""
from dataclasses import replace
import unittest

import numpy as np

from universe24.core import Engine
from universe24.tools.metric_clock_gate import ClockGateConfig,build_gate_tensor,prepare_gate,run_gate


class MetricClockGateTests(unittest.TestCase):
    def test_existing_reader_and_prescribed_background_are_exact(self):
        c=ClockGateConfig();tensor=build_gate_tensor(c);engine=Engine(tensor,c.Q)
        self.assertEqual(tensor.rank,3)
        self.assertEqual(tensor.support_violations(),[])
        self.assertEqual(len(tensor.designations),len(c.mass_multipliers))
        flat=prepare_gate(tensor,c,0)
        for F in c.fields:
            state=prepare_gate(tensor,c,F)
            np.testing.assert_array_equal(state.a[1:],flat.a[1:])
            np.testing.assert_array_equal(state.b[1:],flat.b[1:])
            np.testing.assert_array_equal(state.r,flat.r)
            u=engine.inputs(state)
            np.testing.assert_array_equal(u[0],np.full(state.N,6*c.Q*F,dtype=object))
            for n in c.mass_multipliers:
                g=tensor.gear_index(f'clock{n}.c')
                expected=(6*c.Q-2*c.P*n+2*n*F)*state.b[g]
                np.testing.assert_array_equal(u[g],expected)
            after=engine.run(state,12)
            np.testing.assert_array_equal(after.a[0],state.a[0])
            np.testing.assert_array_equal(after.b[0],state.b[0])
            self.assertTrue(engine.rewind(after,12).same_as(state))

    def test_raw_relational_gate_separates_slow_and_fast_clocks(self):
        report=run_gate(ClockGateConfig(steps=8192))
        self.assertTrue(report['manifest']['same_tensor_all_cases'])
        for case in report['cases']:
            self.assertEqual(case['steps'],8192)
            self.assertTrue(case['exact_rewind'] and case['static_field_exact'])
            self.assertTrue(case['relational_first_pair_gate'])
            self.assertTrue(case['sine_dispersion_gate'])
            self.assertLessEqual(case['peak_counter_bits'],25)
            if case['F']:
                self.assertFalse(case['relational_all_clock_gate'])
                pair=next(p for p in case['relational_clock_pairs'] if p['A']==1 and p['B']==4096)
                self.assertGreater(abs(pair['minus_one']),1e-4)
            else:
                self.assertTrue(case['relational_all_clock_gate'])

    def test_inadequate_observation_is_inconclusive_not_a_pass(self):
        report=run_gate(ClockGateConfig(steps=2))
        for case in report['cases']:
            self.assertFalse(case['relational_all_clock_gate'])
            self.assertFalse(case['relational_first_pair_gate'])
            self.assertTrue(all(p['double_ratio'] is None for p in case['relational_clock_pairs']))
            self.assertEqual(case['relational_status'],'inconclusive_insufficient_crossings')

    def test_guard_at_final_requested_update_cannot_pass(self):
        c=ClockGateConfig(Q=3,P=1,amplitude=31,mass_multipliers=(1,2),
                          fields=(0,),steps=32,counter_limit=34)
        case=run_gate(c)['cases'][0]
        self.assertEqual(case['steps'],c.steps)
        self.assertEqual(case['peak_counter_magnitude'],c.counter_limit)
        self.assertTrue(case['exact_rewind'])
        self.assertFalse(case['guard_pass'])
        self.assertEqual(case['stop_reason'],'counter_limit')
        self.assertFalse(case['relational_all_clock_gate'])
        self.assertFalse(case['relational_first_pair_gate'])
        self.assertFalse(case['sine_dispersion_gate'])
        self.assertEqual(case['relational_status'],'incomplete_or_guard_failure')

    def test_invalid_flat_control_cannot_validate_another_complete_case(self):
        # Actual rounding reaches the flat guard after enough cycles to estimate
        # rates; the nonzero-field trajectory remains below the guard throughout.
        c=ClockGateConfig(Q=3,P=2,steps=128,amplitude=23,
                          mass_multipliers=(1,2),fields=(0,1),
                          tolerance=10,counter_limit=27)
        report=run_gate(c)
        flat,other=report['cases']
        self.assertEqual(flat['steps'],22)
        self.assertFalse(flat['guard_pass'])
        self.assertTrue(all(item['raw_omega'] is not None for item in flat['clocks'].values()))
        self.assertEqual(other['steps'],c.steps)
        self.assertTrue(other['guard_pass'] and other['exact_rewind'])
        self.assertFalse(report['flat_control_valid'])
        self.assertFalse(other['flat_control_valid'])
        self.assertTrue(other['relational_clock_pairs'][0]['within_tolerance'])
        self.assertIsNotNone(other['relational_clock_pairs'][0]['double_ratio'])
        self.assertFalse(other['relational_clock_pairs'][0]['pass'])
        self.assertFalse(other['relational_all_clock_gate'])
        self.assertFalse(other['relational_first_pair_gate'])
        self.assertFalse(other['sine_dispersion_gate'])
        self.assertEqual(other['relational_status'],'invalid_flat_control')

    def test_rejects_invalid_preparations(self):
        c=ClockGateConfig()
        for kwargs in ({'Q':2},{'steps':0},{'fields':(32,0)},{'fields':(0,c.P)},
                       {'mass_multipliers':(1,1)},{'tolerance':float('nan')},
                       {'counter_limit':c.amplitude},{'amplitude':1,'counter_limit':16,'fields':(0,32)}):
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):
                build_gate_tensor(replace(c,**kwargs))


if __name__=='__main__':
    unittest.main()

"""Sourced Einstein-Maxwell sector: physics controls and exact integer audits."""
import math
import unittest
import numpy as np
from experiments.geometry.electrovac_geometry import audit
from experiments.geometry.electrovac_solution import (build,profiles,prepare,reference,
    run_case,reciprocal_control,continuity_residual,expected)
from universe24.core import Engine


class TestElectrovac(unittest.TestCase):
    def test_independent_source_and_full_equations(self):
        result=audit()
        for key in ('all_16_Einstein_Maxwell_residuals_zero','all_Maxwell_divergences_zero',
                    'all_exterior_derivatives_zero','all_stress_divergences_zero',
                    'charged_and_neutral_worldline_equations_verified',
                    'flat_metric_with_nonzero_field_rejected'):
            self.assertTrue(result[key])

    def test_constant_field_against_closed_form(self):
        _,p=build(1); ref=reference(p,profiles(p,'constant'),64)
        t=np.arange(p['steps']+1)/p['n']; omega=1/math.sqrt(128)
        neutral=np.cos(omega*t)+np.sin(omega*t)/(16*omega)
        charged=neutral-16*(1-np.cos(omega*t))
        np.testing.assert_allclose(ref[:,0,0],neutral,atol=1e-10,rtol=0)
        np.testing.assert_allclose(ref[:,2,0],charged,atol=1e-10,rtol=0)

    def test_flat_control_and_official_decode(self):
        row=run_case(1,'flat')
        self.assertEqual(row['charged_max_error'],0)
        self.assertEqual(row['neutral_max_error'],0)
        self.assertTrue(row['official_only_decoder_exact'])
        self.assertTrue(row['all_rewinds_exact'])

    def test_em_sign_reversal_changes_charge_not_gravity(self):
        positive=run_case(1,'circular'); negative=run_case(1,'circular',polarity=-1)
        self.assertEqual(positive['final_positions'][:4],negative['final_positions'][:4])
        self.assertEqual(positive['peak_Tuu'],negative['peak_Tuu'])
        self.assertGreater(abs(positive['final_positions'][5]-negative['final_positions'][5]),1)

    def test_field_amplitude_squared_sources_gravity(self):
        base=run_case(1,'circular'); doubled=run_case(1,'circular',amplitude=2)
        self.assertEqual(doubled['peak_Tuu'],4*base['peak_Tuu'])
        self.assertLess(doubled['final_positions'][0],base['final_positions'][0])

    def test_integer_local_continuity_and_no_test_body_backreaction(self):
        tensor,p=build(1); profile=profiles(p,'circular'); seed=prepare(p,profile)
        control=seed.copy();control.a[4:]=0;control.b[4:]=0
        engine=Engine(tensor,p['Q'])
        for tick in range(1,7):
            next_state=engine.step(seed); next_control=engine.step(control)
            self.assertTrue(all(v==0 for v in continuity_residual(seed,next_state)))
            np.testing.assert_array_equal(next_state.b[:4],next_control.b[:4])
            np.testing.assert_array_equal(next_state.b[:4],expected(p,profile,tick))
            seed,control=next_state,next_control

    def test_refinement_improves_lorentz_and_gravity_motion(self):
        coarse=run_case(1,'linear');fine=run_case(2,'linear')
        for kind in ('neutral','charged'):
            self.assertLess(fine[f'{kind}_max_error'],coarse[f'{kind}_max_error']/2)

    def test_reciprocal_completion_breaks_prepared_sector(self):
        result=reciprocal_control()
        self.assertTrue(result['fully_reciprocal'])
        self.assertTrue(result['exact_rewind'])
        self.assertGreater(result['continuity_residual'],0)

    def test_preparation_is_not_automatic(self):
        tensor,p=build(1);profile=profiles(p,'circular');seed=prepare(p,profile)
        seed.a[0,0]+=1
        engine=Engine(tensor,p['Q']);after=engine.step(seed)
        self.assertFalse(np.array_equal(after.b[:4],expected(p,profile,1)))
        self.assertTrue(engine.inverse_step(after).same_as(seed))


if __name__=='__main__':unittest.main()

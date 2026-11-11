"""Scoped tests of the optional pp-wave decoder and integer tidal probes."""
import unittest
import numpy as np
from experiments.geometry.pp_wave_geometry import audit, boundary_audit
from experiments.geometry.pp_wave_solution import (build, profiles, prepare, run_case,
                                                   off_sector_control, expected_carrier)
from universe24.core import Engine


class TestPPWaveGeometry(unittest.TestCase):
    def test_full_nonlinear_geometry_and_nonvacuum_control(self):
        result=audit()
        self.assertTrue(result['all_16_full_nonlinear_vacuum_Einstein_components_zero'])
        self.assertTrue(result['contracted_Bianchi_all_four_zero'])
        self.assertEqual(result['negative_trace_control']['C_1_over_100_Guu'],'-1/50')
        self.assertEqual(result['tidal_components']['Ruxuy'],'-B')
        self.assertTrue(result['longitudinal_geodesic_and_timelike_normalization_verified'])

    def test_transverse_periodic_boundary_is_not_silently_accepted(self):
        result=boundary_audit()
        self.assertTrue(result['interior_quadratic_Laplacian_exactly_zero'])
        self.assertGreater(result['nonzero_seam_cells'],0)


class TestPPWaveDynamics(unittest.TestCase):
    def test_flat_affine_geodesics_exact_and_event_decodable(self):
        result=run_case(1,'flat')
        self.assertLess(result['maximum_position_error'],1e-12)
        self.assertTrue(result['official_only_position_decoder_exact'])
        self.assertTrue(result['exact_rewind'])

    def test_cross_polarization_and_refinement(self):
        coarse=run_case(1,'mixed'); fine=run_case(2,'mixed')
        self.assertLess(fine['maximum_position_error'],coarse['maximum_position_error']/2)
        self.assertGreater(abs(fine['final_positions'][1]),1e-3)
        self.assertEqual(fine['tidal_integer_ledger_max_residual'],0)

    def test_plus_polarization_has_no_cross_response(self):
        result=run_case(1,'plus')
        self.assertEqual(result['final_positions'][1],0)
        self.assertEqual(result['final_positions'][2],0)
        self.assertNotEqual(result['final_positions'][0],result['final_positions'][3])

    def test_carrier_does_not_read_test_body(self):
        tensor,p=build(1); seed=prepare(tensor,p,profiles(p,'mixed'))
        control=seed.copy(); control.a[4:]=0;control.b[4:]=0
        engine=Engine(tensor,p['Q'])
        for tick in range(1,7):
            seed=engine.step(seed);control=engine.step(control)
            for field in ('a','b','r'):
                np.testing.assert_array_equal(getattr(seed,field)[:4],getattr(control,field)[:4])
            np.testing.assert_array_equal(seed.b[:4],expected_carrier(p,profiles(p,'mixed'),tick))

    def test_preparation_condition_is_necessary(self):
        result=off_sector_control()
        self.assertTrue(result['prepared_transport_identity_fails'])
        self.assertTrue(result['exact_inverse_still_passes'])

    def test_protocol_rejects_undeclared_parameters(self):
        for n in (0,3,True,1.0):
            with self.assertRaises(ValueError):build(n)
        _,p=build(1)
        with self.assertRaises(ValueError):profiles(p,'unknown')


if __name__=='__main__':unittest.main()

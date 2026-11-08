"""Regression tests for read-only all-48 variational/GR consistency research.

These protect math and scope; passing is not evidence for Einstein gravity.
"""
import unittest
from research.variational_gravity_gate_v1.audit import (
    pin_check, to_canonical, from_canonical, D_integer, D_real, K_integer,
    symplectic_exact_check, test_all_signed, GR_static_conformal_algebra,
)
from research.variational_gravity_gate_v1.signal_gate import run as run_signal_gate
from universe24 import Channel


class VariationalGravityGateTests(unittest.TestCase):
    def test_unchanged_core_blobs(self):
        self.assertEqual(len(pin_check()),5)

    def test_canonical_coordinates_with_negative_and_huge_integers(self):
        for a,b in ((-10**40, 10**40),(1,-3),(0,0)):
            for r in range(6):
                state=Channel(a,b,r)
                self.assertEqual(from_canonical(*to_canonical(state)),state)

    def test_integer_tooth_interpolation(self):
        for p in range(-100,101):
            self.assertEqual(D_integer(p),D_real(p))
            self.assertGreaterEqual(K_integer(p),0)

    def test_all_48_channels_all_8_signed_tensors_and_action(self):
        result=test_all_signed()
        self.assertEqual(result['full_state_channels'],34944)
        self.assertEqual(result['exact_edge_gradient_tests'],240)
        self.assertTrue(result['observed_nonconservation_of_naive_H'])

    def test_exact_rational_symplectic_embedding(self):
        self.assertEqual(symplectic_exact_check()['finite_symplectic_jacobian_check'],'PASS')

    def test_einstein_conformal_vacuum_conditional_identity(self):
        self.assertEqual(GR_static_conformal_algebra()['rational_jet_checks'],1000)

    def test_two_ended_48_channel_pulse_does_not_define_a_photon_speed(self):
        result=run_signal_gate()
        self.assertEqual(len(result['cases']),16)
        e=result['first_arrival_amplitude_summary']
        self.assertIsNone(e['1']['near']['full'])
        self.assertEqual(e['3']['near']['full'],3)
        self.assertEqual(e['3']['far']['full'],4)
        self.assertEqual(e['-3']['near']['full'],5)
        self.assertEqual(e['-3']['far']['full'],4)
        self.assertEqual(e['6']['near']['full'],3)
        self.assertEqual(e['6']['far']['full'],3)


if __name__=='__main__':unittest.main()

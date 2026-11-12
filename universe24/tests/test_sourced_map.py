"""Regressions for the complete-history sourced FLRW research construction."""
from fractions import Fraction as F
from pathlib import Path
import tempfile
import unittest

import numpy as np

from universe24.core import Engine, GearType, Tensor
from universe24.core.lattice import ZERO
from validation.sourced_map import domain, native, physical_map, projective


class SourcedMapTests(unittest.TestCase):
    def test_one_tensor_three_resolutions_same_physical_endpoint(self):
        fingerprints, endpoints = set(), []
        for N in (24, 48, 96):
            program = native.build_native(N)
            seed = native.prepare_native(program)
            state, engine = seed, Engine(program.tensor)
            fingerprints.add(program.tensor.fingerprint)
            for _ in range(N // 8):
                old = state
                state = engine.step(old)
                self.assertTrue(state.same_as(native.scalar_step(old)))
                self.assertTrue(engine.inverse_step(state).same_as(old))
                values = native.read_conserved(program, state)
                self.assertEqual(values['invariant'], 0)
                self.assertEqual(physical_map.exact_readout(values)['constraint'], 0)
            self.assertTrue(engine.rewind(state, N // 8).same_as(seed))
            endpoints.append((values['V'], values['U'], values['tau']))
        self.assertEqual(len(fingerprints), 1)
        self.assertEqual(endpoints, [(F(355, 256), F(51, 16), F(1, 8))] * 3)

    def test_all_carries_are_retained_without_changing_physical_map(self):
        program = native.build_native(24)
        engine = Engine(program.tensor)
        for r in range(6):
            seed = native.prepare_native(program, remainders=[[r] * 27 for _ in range(6)])
            after = engine.step(seed)
            self.assertTrue(np.array_equal(seed.r, after.r))
            self.assertEqual(native.read_conserved(program, after)['invariant'], 0)
            self.assertTrue(engine.inverse_step(after).same_as(seed))

    def test_old_volume_history_has_physical_content(self):
        program = native.build_native(24)
        seed = native.prepare_native(program)
        changed = seed.copy()
        changed.a[0] -= 1
        before = native.read_conserved(program, seed)
        after = native.read_conserved(program, changed)
        self.assertEqual(before['V'], after['V'])
        self.assertNotEqual(before['U'], after['U'])
        self.assertNotEqual(after['invariant'], 0)
        with self.assertRaises(ValueError):
            physical_map.physical_decode(after)

    def test_constraint_is_not_projected_or_silently_repaired(self):
        program = native.build_native(24)
        state = native.prepare_native(program)
        state.a[0] += 1
        state.b[0] += 1
        engine = Engine(program.tensor)
        for _ in range(4):
            values = native.read_conserved(program, state)
            self.assertEqual(values['invariant'], -12)
            with self.assertRaises(ValueError):
                physical_map.exact_readout(values)
            state = engine.step(state)

    def test_disconnecting_source_breaks_constraint_but_not_rewind(self):
        program = native.build_native(24)
        seed = native.prepare_native(program)
        disconnected = Tensor(
            [GearType(name, label='audit') for name in native.NAMES],
            [(name, 6, ((name, ZERO, 'b'),)) for name in native.NAMES],
            strict_support=True,
        )
        engine = Engine(disconnected)
        after = engine.step(seed)
        self.assertNotEqual(native.read_conserved(program, after)['invariant'], 0)
        self.assertTrue(engine.inverse_step(after).same_as(seed))

    def test_actual_history_and_independent_integer_chart_agree(self):
        program = native.build_native(48)
        seed = native.prepare_native(program, V=F(1, 2), U=F(3), D=2, P=-2)
        encoded = projective.encode_initial(F(1, 2), F(3), 2, -2, 48)
        self.assertEqual(int(seed.a[0, 0]), encoded['old_volume'])
        self.assertEqual(int(seed.b[0, 0]), encoded['volume'])
        self.assertEqual(projective.constraint_numerator(
            int(seed.a[0, 0]), int(seed.b[0, 0]), 2, -2, 48), 0)

    def test_field_decoder_uses_current_state_and_retained_anchor(self):
        values = native.read_conserved(native.build_native(24),
                                       native.prepare_native(native.build_native(24)))
        first = physical_map.physical_decode(values)
        different_counter = physical_map.physical_decode(dict(values, tau=F(1000)))
        for field in physical_map.PHYSICAL_FIELDS:
            self.assertEqual(first[field], different_counter[field])
        changed_offset = physical_map.physical_decode(dict(values, phi_ref=F(7)))
        self.assertEqual(changed_offset['phi'], 7)
        self.assertEqual(changed_offset['B'], first['B'])

    def test_massive_relabel_is_rejected(self):
        program = native.build_native(24)
        values = native.read_conserved(program, native.prepare_native(program))
        with self.assertRaises(ValueError):
            physical_map.physical_decode(values, mass_squared=1)

    def test_endpoint_positivity_does_not_hide_a_singularity(self):
        certificate = domain.interval_certificate(domain.VolumePoint(1, -3, 2, 1), F(4))
        self.assertTrue(certificate['both_endpoints_positive'])
        self.assertTrue(certificate['constraint_preserved'])
        self.assertFalse(certificate['whole_interval_valid'])
        self.assertEqual(certificate['minimum_volume'], '-2')

    def test_complete_history_domain_rejects_too_coarse_preparation(self):
        with self.assertRaises(ValueError):
            native.prepare_native(native.build_native(24), P=22, U=F(27))
        seed = native.prepare_native(native.build_native(48), P=22, U=F(27))
        self.assertEqual(native.read_conserved(native.build_native(48), seed)['invariant'], 0)

    def test_selected_chart_and_exact_types_are_enforced(self):
        for value in (True, 24.0, F(24)):
            with self.assertRaises(TypeError):
                native.build_native(value)
        program = native.build_native(24)
        for kwargs in ({'D': 0}, {'P': 0}, {'U': -3}, {'V': 1.0},
                       {'remainders': [[6] * 27 for _ in range(6)]}):
            with self.assertRaises((TypeError, ValueError)):
                native.prepare_native(program, **kwargs)

    def test_all_retained_channels_fit_contract(self):
        tensor = native.build_native(96).tensor
        self.assertEqual(tensor.G, 6)
        self.assertEqual(len(tensor), 7)
        self.assertFalse(tensor.support_violations())
        self.assertTrue(tensor.b_only)
        self.assertEqual(tensor.rank - 1, 1)

    def test_near_branch_bigint_phase_decode_remains_finite(self):
        x, y = 1, 0
        for _ in range(90):
            x, y = 5*x + 12*y, 2*x + 5*y
        self.assertEqual(x*x - 6*y*y, 1)
        program = native.build_native(24*x)
        seed = native.prepare_native(program, V=F(1, 3), U=F(x), D=1, P=2*y)
        values = native.read_conserved(program, seed)
        self.assertEqual(physical_map.physical_decode(values)['phi'], 0)
        after = Engine(program.tensor).step(seed)
        decoded = physical_map.physical_decode(native.read_conserved(program, after))
        self.assertGreater(decoded['phi'], 0)
        self.assertEqual(native.read_conserved(program, after)['invariant'], 0)

    def test_saved_runtime_retains_a_shifted_coordinate_origin(self):
        from validation.sourced_map import runtime
        from universe24.system.runtime import run_bundle
        program = native.build_native(24)
        seed = native.prepare_native(program)
        seed.a[5] += 10
        seed.b[5] += 10
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'run'
            run_bundle(runtime.make_bundle(program, seed), path, 3)
            receipt, evidence = runtime.inspect_run(path)
        self.assertEqual(receipt.final_time, F(13, 24))
        self.assertEqual(evidence['restricted_exact_constraint'], 'zero at every saved physical step')
        self.assertTrue(runtime.require_same_run(receipt, receipt))
        with self.assertRaises(ValueError):
            runtime.compare_resolution(receipt, receipt)


if __name__ == '__main__':
    unittest.main()

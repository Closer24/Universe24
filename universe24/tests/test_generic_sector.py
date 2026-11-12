"""Exact invariant-sector reduction, including discarded-information guards."""
from fractions import Fraction
import unittest

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.core.lattice import ZERO
from validation.generic_couplings import sector


class GenericSectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reduction = sector.build_reduction()

    def test_actual_builder_and_independent_coefficients(self):
        self.assertEqual(self.reduction.full_tensor.G, 45)
        self.assertEqual(len(self.reduction.full_tensor), 889)
        self.assertEqual(self.reduction.tensor.to_dict(), sector.explicit_tensor().to_dict())
        self.assertEqual(len(self.reduction.tensor), 14)
        self.assertEqual(self.reduction.full_tensor.fingerprint,
                         '6ea453fa77a5a9d74af5bd4fc626cfcdc8f92942b10c301d2d00814bf4d05ba0')

    def test_complete_eight_step_orbit_and_negative_physics_control(self):
        seed = sector.prepare_seed()
        small, full = seed, sector.embed_state(self.reduction, seed)
        small_engine, full_engine = Engine(self.reduction.tensor), Engine(self.reduction.full_tensor)
        for tick in range(8):
            next_small, next_full = small_engine.step(small), full_engine.step(full)
            self.assertTrue(next_full.same_as(sector.embed_state(self.reduction, next_small)))
            self.assertTrue(sector.project_state(self.reduction, next_full).same_as(next_small))
            self.assertTrue(small_engine.inverse_step(next_small).same_as(small))
            self.assertTrue(full_engine.inverse_step(next_full).same_as(full))
            if tick == 0:
                denominator, _, curvature, phi, momentum, dust = map(int, next_small.b[:, 0])
                defect = Fraction(6*curvature*curvature-momentum*momentum-phi*phi-2*dust*dust,
                                  denominator*denominator)
                self.assertEqual(defect, -7*sector.DT**2)
            small, full = next_small, next_full
        self.assertTrue(small_engine.rewind(small, 8).same_as(seed))
        self.assertTrue(full_engine.rewind(full, 8).same_as(sector.embed_state(self.reduction, seed)))

    def test_both_histories_and_carries_are_injective(self):
        seed = sector.prepare_seed()
        seed.a[:] = np.arange(6).reshape(6, 1)-3
        seed.r[:] = np.arange(162).reshape(6, 27) % 6
        full = sector.embed_state(self.reduction, seed)
        self.assertTrue(sector.project_state(self.reduction, full).same_as(seed))
        next_small = Engine(self.reduction.tensor).step(seed)
        next_full = Engine(self.reduction.full_tensor).step(full)
        self.assertTrue(next_full.same_as(sector.embed_state(self.reduction, next_small)))
        self.assertTrue(Engine(self.reduction.full_tensor).inverse_step(next_full).same_as(full))
        self.assertTrue(np.array_equal(next_small.r, seed.r))

    def test_reject_nonhomogeneous_old_and_current_reduced_banks(self):
        for field in ('a', 'b'):
            state = sector.prepare_seed()
            getattr(state, field)[0, 1] += 1
            with self.subTest(field=field), self.assertRaises(sector.SectorError):
                sector.embed_state(self.reduction, state)

    def test_reject_equal_current_with_different_old_or_carry(self):
        for field in ('a', 'r'):
            full = sector.embed_state(self.reduction, sector.prepare_seed())
            index = self.reduction.full_tensor.gear_index('projective.B11')
            getattr(full, field)[index, :] += 1
            with self.subTest(field=field), self.assertRaises(sector.SectorError):
                sector.project_state(self.reduction, full)

    def test_reject_any_omitted_information(self):
        for field in ('a', 'b', 'r'):
            full = sector.embed_state(self.reduction, sector.prepare_seed())
            index = self.reduction.full_tensor.gear_index('projective.chi')
            getattr(full, field)[index, 0] = 1
            with self.subTest(field=field), self.assertRaises(sector.SectorError):
                sector.project_state(self.reduction, full)

    def test_reject_nonhomogeneous_full_representative(self):
        full = sector.embed_state(self.reduction, sector.prepare_seed())
        full.a[self.reduction.full_tensor.gear_index('projective.phi'), 1] = 2
        with self.assertRaises(sector.SectorError):
            sector.project_state(self.reduction, full)

    def test_reject_illegal_carries_and_wrong_channel_count(self):
        for carry in (-1, 6):
            seed = sector.prepare_seed()
            seed.r[0, 0] = carry
            with self.subTest(carry=carry), self.assertRaises(sector.SectorError):
                sector.embed_state(self.reduction, seed)
        seed = sector.prepare_seed()
        with self.assertRaises(sector.SectorError):
            sector.embed_state(self.reduction, State(seed.L, seed.a[:5], seed.b[:5], seed.r[:5]))

    def test_tampered_surviving_group_and_omitted_polynomials_rejected(self):
        source = self.reduction.full_tensor
        original = [(source.names[term.target], term.coeff,
                     tuple((source.names[factor.gear], factor.offset, factor.field) for factor in term.factors))
                    for term in source.monomials]
        # Different representatives, a newly sourced omitted field, and a
        # changed ungrouped surviving law cover three distinct closure checks.
        for target in ('projective.B11', 'projective.chi', 'projective.phi'):
            changed = Tensor(source.gears, original + [(target, 3, (('projective.denominator', ZERO, 'b'),))],
                             strict_support=True)
            with self.subTest(target=target), self.assertRaises(sector.SectorError):
                sector.build_reduction(changed)

    def test_report_keeps_scope_and_bit_cost(self):
        report = sector.audit()
        self.assertEqual(report['status'], 'passed')
        self.assertEqual(report['random_history_controls']['cases'], 8)
        self.assertEqual(report['finite_fixture']['maximum_integer_bits_by_step'][-1], 3742)
        self.assertEqual(report['arbitrary_state_compression'], 'not_claimed')
        self.assertEqual(report['physical_acceptance'], 'not_established')


if __name__ == '__main__':
    unittest.main()

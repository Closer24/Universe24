"""Load measurements stay passive, exact and distinct from physical energy."""
import itertools
import unittest

import numpy as np

from universe24.core import Engine, GearType, State, Tensor
from universe24.load import (compare_distributions, distribution_profile,
                             face_load_profile, integer_work_profile,
                             transition_load_profile)
from universe24.model import (coupling_tensor, edge_quartets, make_model_bundle,
                              prepare_occupation)


class LoadDiagnosticContracts(unittest.TestCase):
    def test_concentration_distinguishes_spreading_from_translation_or_loss(self):
        point = [12, 0, 0, 0]
        translated = [0, 0, 12, 0]
        uniform = [3, 3, 3, 3]
        a, b = distribution_profile(point), distribution_profile(uniform)
        self.assertEqual(a['participation'], {'num': 1, 'den': 1})
        self.assertEqual(b['participation'], {'num': 4, 'den': 1})
        self.assertEqual(a['normalized_concentration'], {'num': 4, 'den': 1})
        self.assertEqual(b['normalized_concentration'], {'num': 1, 'den': 1})
        move = compare_distributions(point, translated)
        self.assertEqual(move['node_load_l1_change'], 24)
        self.assertTrue(move['unchanged_concentration_at_equal_total'])
        self.assertFalse(move['more_even_at_equal_total'])
        self.assertTrue(compare_distributions(point, uniform)['more_even_at_equal_total'])
        lost = compare_distributions(point, [1, 1, 1, 1])
        self.assertFalse(lost['total_conserved'])
        self.assertIsNone(lost['sum_squares_reduction'])
        self.assertFalse(lost['more_even_at_equal_total'])

    def test_ratios_remain_exact_for_unbounded_integers_and_empty_load(self):
        weights = [1, 2, 4, 0]
        scaled = [value * (10**5000) for value in weights]
        a, b = distribution_profile(weights), distribution_profile(scaled)
        for key in ('participation', 'normalized_concentration', 'support_nodes'):
            self.assertEqual(a[key], b[key])
        self.assertEqual(a['participation'], {'num': 7, 'den': 3})
        self.assertEqual(a['variance'], {'num': 35, 'den': 16})
        empty = distribution_profile([0, 0, 0])
        self.assertTrue(empty['empty'])
        self.assertEqual(empty['support_nodes'], 0)
        self.assertEqual(empty['participation'], {'num': 0, 'den': 1})

    def test_inexact_negative_or_incomplete_distribution_inputs_are_rejected(self):
        for invalid in ([], [1, -1], [1.0], [True], [[1, 2]]):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                distribution_profile(invalid)
        with self.assertRaises(ValueError):
            compare_distributions([1, 2], [1])

    def test_big_integer_size_changes_without_changing_symbolic_schedule(self):
        bundle = make_model_bundle(L=3)
        ordinary = bundle.seed
        values = ordinary.b.astype(object).copy()
        values[0, 0] = -(1 << 200)
        large = State(3, ordinary.a.copy(), values, ordinary.r.copy())
        a = integer_work_profile(ordinary, bundle.tensor)
        b = integer_work_profile(large, bundle.tensor)
        self.assertEqual(a['canonical_scalar_schedule_per_node'], b['canonical_scalar_schedule_per_node'])
        self.assertEqual(b['magnitude_bits_max_by_node'][0], 201)
        self.assertEqual(b['negative_entries_by_node'][0], 1)
        self.assertEqual(a['magnitude_bits_sum_by_node'][1:], b['magnitude_bits_sum_by_node'][1:])
        self.assertGreater(b['magnitude_bits_sum_by_node'][0], a['magnitude_bits_sum_by_node'][0])
        self.assertEqual(a['canonical_scalar_schedule_per_node']['monomial_evaluations'], len(bundle.tensor.monomials))
        self.assertEqual(a['retained_integers_per_node'], 144)
        self.assertFalse(b['feeds_engine'])

    def test_work_metric_ignores_species_names_and_channel_permutations(self):
        bundle = make_model_bundle(L=3)
        renamed = Tensor([GearType(('light', 'matter', 'dark')[g % 3] + str(g), 'official')
                          for g in range(48)], bundle.tensor.monomials, strict_support=True)
        self.assertEqual(integer_work_profile(bundle.seed, bundle.tensor),
                         integer_work_profile(bundle.seed, renamed))
        permutation = np.arange(48)[::-1]
        state = bundle.seed
        permuted = State(state.L, state.a[permutation], state.b[permutation], state.r[permutation])
        self.assertEqual(integer_work_profile(state, bundle.tensor),
                         integer_work_profile(permuted, bundle.tensor))

    def test_node_accounts_flux_and_readouts_do_not_mutate_state(self):
        rng = np.random.default_rng(8601)
        initial = prepare_occupation(L=3, occupation=rng.integers(0, 2, (48, 27)))
        preserved = initial.copy()
        state, engine = initial, Engine(coupling_tensor())
        total = face_load_profile(state.b, state.L)['totals']['occupation']
        for _ in range(5):
            after = engine.step(state)
            profile = face_load_profile(after.b, after.L)
            transition = transition_load_profile(state, after)
            self.assertEqual(profile['totals']['occupation'], total)
            self.assertEqual(profile['totals']['occupation'] + profile['totals']['available_capacity'], 48*27)
            self.assertEqual(profile['totals']['held_occupation'] + profile['totals']['moving_occupation'], total)
            self.assertTrue(transition['node_continuity_passed'])
            self.assertTrue(transition['distribution_change']['total_conserved'])
            self.assertEqual(len(profile['per_face']), 6)
            for face in profile['per_face']:
                self.assertEqual([a+b for a,b in zip(face['occupation'],face['available_capacity'])], [8]*27)
            profile['per_node']['occupation'][0] = -999
            self.assertTrue(all(value >= 1 for value in after.b.flat))
            state = after
        self.assertTrue(initial.same_as(preserved))
        self.assertTrue(engine.rewind(state, 5).same_as(initial))

    def test_actual_single_occupation_moves_without_becoming_more_even(self):
        fields = np.zeros((48, 125), dtype=int)
        fields[0, 62] = 1
        state = prepare_occupation(L=5, occupation=fields)
        after = Engine(coupling_tensor()).step(state)
        report = transition_load_profile(state, after)
        self.assertTrue(report['node_continuity_passed'])
        self.assertEqual(report['distribution_change']['node_load_l1_change'], 2)
        self.assertTrue(report['distribution_change']['unchanged_concentration_at_equal_total'])
        self.assertFalse(report['distribution_change']['more_even_at_equal_total'])

    def test_all_sixteen_edge_words_have_exact_capacity_and_current_accounting(self):
        quartet = edge_quartets(3)[0]
        engine = Engine(coupling_tensor())
        for word in itertools.product((0,1), repeat=4):
            with self.subTest(word=word):
                fields = np.zeros((48,27), dtype=int)
                for (channel,node), value in zip(quartet,word):
                    fields[channel,node] = value
                state = prepare_occupation(L=3, occupation=fields)
                after = engine.step(state)
                before_profile = face_load_profile(state.b, 3)
                flow = transition_load_profile(state, after)
                amount = sum(word)
                moving = amount if amount < 3 else 0
                self.assertEqual(before_profile['totals']['moving_occupation'],moving)
                self.assertEqual(before_profile['totals']['held_occupation'],amount-moving)
                self.assertEqual(before_profile['blocked_quartets'],int(amount==3))
                self.assertEqual(before_profile['saturated_quartets'],int(amount==4))
                self.assertEqual(sum(flow['incoming_occupied_slots_by_node']),moving)
                self.assertEqual(sum(flow['outgoing_occupied_slots_by_node']),moving)
                self.assertTrue(flow['node_continuity_passed'])
                self.assertTrue(engine.inverse_step(after).same_as(state))

    def test_continuity_audit_exposes_an_unjustified_changed_occupation(self):
        bundle = make_model_bundle(L=3)
        after = Engine(bundle.tensor).step(bundle.seed)
        changed = after.copy()
        changed.b[0, 0] = 3 - int(changed.b[0, 0])
        report = transition_load_profile(bundle.seed, changed)
        self.assertFalse(report['node_continuity_passed'])


if __name__ == '__main__':
    unittest.main()

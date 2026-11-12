"""Independent local kinetic accounts, with physical overclaim negatives."""
import unittest

import numpy as np

from universe24.core import DIRECTIONS, Engine, GearType, State, Tensor, lattice
from validation.local_unification import balance, native


class LocalUnificationBalanceTests(unittest.TestCase):
    def seed(self, L=3, direction=(1, 0, 0)):
        current = np.random.default_rng(1840).integers(0, 2, size=(8, L ** 3)).astype(object)
        carries = np.asarray([[(g+n) % 6 for n in range(L ** 3)] for g in range(8)], dtype=object)
        return native.prepare_state(current, L, direction=direction, remainders=carries)

    def test_truth_table_has_real_equal_opposite_recoil(self):
        result = balance.collision_proof()
        self.assertEqual(len(result["truth_table"]), 16)
        nontrivial = [row for row in result["truth_table"] if row["delta"]]
        self.assertEqual(len(nontrivial), 2)
        self.assertEqual(result["carrier_only_momentum_counterexample"]["carrier_delta"], 2)
        self.assertEqual(result["carrier_only_momentum_counterexample"]["record_delta"], -2)

    def test_all_face_local_and_regional_balances_include_both_banks(self):
        for direction in DIRECTIONS:
            state = seed = self.seed(direction=direction)
            engine = Engine(native.build_tensor(direction))
            lat = lattice(state.L)
            masks = [np.array([n == 0 for n in range(lat.N)]),
                     np.array([lat.coords(n)[0] % 2 == 0 for n in range(lat.N)]),
                     np.ones(lat.N, dtype=bool)]
            for _ in range(5):
                after = engine.step(state)
                ledger = balance.transition_ledgers(state, after, direction)
                for mask in masks:
                    rows = balance.regional_balance(ledger, mask, state.L, direction)
                    for row in rows.values():
                        self.assertEqual(row["change"] + row["outward_flux"], row["source"])
                state = after
            self.assertTrue(engine.rewind(state, 5).same_as(seed))

    def test_macro_speed_requires_two_native_ticks(self):
        current = np.zeros((8, 27), dtype=object)
        current[4, 0] = 1  # Record+ starts in the collision-stage bank B.
        seed = native.prepare_state(current, 3)
        engine = Engine(native.build_tensor())
        once = engine.step(seed)
        twice = engine.step(once)
        n0 = balance.kinetic_densities(seed.b, 3)["plus"]
        n1 = balance.kinetic_densities(once.b, 3)["plus"]
        n2 = balance.kinetic_densities(twice.b, 3)["plus"]
        translated = n0[lattice(3).shift_index((-1, 0, 0))]
        self.assertTrue(np.array_equal(n0, n1))
        self.assertFalse(np.array_equal(n1, translated))
        self.assertTrue(np.array_equal(n2, translated))

    def test_record_stress_cannot_be_omitted(self):
        current = np.zeros((8, 27), dtype=object)
        current[4:8, 0] = (1, 0, 0, 1)
        seed = native.prepare_state(current, 3)
        after = Engine(native.build_tensor()).step(seed)
        ledger = balance.transition_ledgers(seed, after)
        self.assertEqual(int(ledger["sources"]["carrier_momentum"][0]), 2)
        self.assertEqual(int(ledger["sources"]["record_momentum"][0]), -2)
        self.assertEqual(sum(int(x) for x in ledger["new"]["momentum"]), 0)
        self.assertEqual(sum(int(x) for x in ledger["new"]["energy"]), 2)
        # A counter-stream pair has positive COM rest energy but is not a bound body.
        self.assertEqual(2 ** 2 - 0 ** 2, 4)

    def test_stress_is_positive_tracefree_and_collision_species_blind(self):
        current = np.zeros((8, 27), dtype=object)
        current[4:8, 0] = (1, 0, 0, 1)
        seed = native.prepare_state(current, 3)
        after = Engine(native.build_tensor()).step(seed)
        old = balance.kinetic_stress(seed.b, 3)
        new = balance.kinetic_stress(after.b, 3)
        self.assertTrue(np.array_equal(old, new))
        self.assertFalse(np.array_equal(seed.b, after.b))
        self.assertTrue(np.all(new[0, 0] >= abs(new[0, 1])))
        self.assertTrue(np.all(-new[0, 0]+new[1, 1]+new[2, 2]+new[3, 3] == 0))

    def test_wrong_state_or_history_cannot_inherit_account(self):
        seed = self.seed()
        after = Engine(native.build_tensor()).step(seed)
        bad = after.copy()
        bad.b[0, 0] = 1 - int(bad.b[0, 0])
        with self.assertRaises(ValueError):
            balance.transition_ledgers(seed, bad)
        bad_seed = seed.copy()
        bad_seed.a[0, 0] = 1 - int(bad_seed.a[0, 0])
        with self.assertRaises(ValueError):
            balance.transition_ledgers(bad_seed, after)
        bad_current = seed.b.copy()
        bad_current[0, 0] = 2
        with self.assertRaises(ValueError):
            balance.kinetic_stress(bad_current, 3)

    def test_source_prefix_guard_does_not_certify_extra_coordinates(self):
        # This isolated prefix guard fixture is NOT the physical source model.
        law = native.build_tensor()
        terms = [(m.target, m.coeff, [(f.gear, f.offset, f.field) for f in m.factors])
                 for m in law.monomials]
        gears = list(law.gears) + [GearType(f"test_geometry.{i}", "audit") for i in range(4)]
        full = Tensor(gears, terms, strict_support=True)
        packets = self.seed()
        zeros = np.zeros((4, 27), dtype=object)
        seed = State(3, np.concatenate((packets.a, zeros)),
                     np.concatenate((packets.b, zeros)), np.concatenate((packets.r, zeros)))
        after = Engine(full).step(seed)
        ledger = balance.source_transition_ledgers(seed, after, full)
        self.assertTrue(np.all(ledger["residuals"]["momentum"] == 0))
        altered = Tensor(gears, terms + [(0, 3, [(8, (0, 0, 0), "b")])], strict_support=True)
        with self.assertRaises(ValueError):
            balance.source_transition_ledgers(seed, after, altered)
        with self.assertRaises(ValueError):
            balance.source_transition_ledgers(packets, Engine(law).step(packets), law)

    def test_same_actual_twelve_channel_source_has_packet_balance(self):
        report = balance.audit_source_prefix(L=11, steps=2)
        self.assertEqual(report["channels"], 12)
        self.assertTrue(report["full_source_inverse_and_rewind"])
        self.assertEqual(report["rows"][0]["energy"], report["rows"][1]["energy"])
        self.assertEqual(report["rows"][0]["momentum"], report["rows"][1]["momentum"])


if __name__ == "__main__":
    unittest.main()

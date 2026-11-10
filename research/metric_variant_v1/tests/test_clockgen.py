"""Study 34 clock law (layers/clockgen.py, CLK-A): construction and exactness tests. NEW file; default OFF law.
Writes nothing (no results/). Small boards only (L = 3)."""
from __future__ import annotations

import unittest

import numpy as np

from ..core.engine import Engine, OBJ, State
from ..core.tensor import compose
from ..layers.clockgen import (HAND, LAPSE, build_clockgen, clockgen_system, lapse_reader_census,
                               theta_reader_census)
from ..layers.one import one_system
from ..observe.clockgen import input_difference, k0_identity, lapse_sums
from ..prepare.one import one_seed


class ClockGenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.S0 = one_system(couple_doublet=False)
        cls.T0 = compose(*cls.S0.blocks)
        cls.E0 = Engine(cls.T0, cls.S0.Q)
        cls.S1 = clockgen_system(kappa=1)
        cls.T1 = compose(*cls.S1.blocks)
        cls.E1 = Engine(cls.T1, cls.S1.Q)
        cls.S2 = clockgen_system(kappa=1, mode="param")
        cls.T2 = compose(*cls.S2.blocks)
        cls.E2 = Engine(cls.T2, cls.S2.Q)
        cls.seed, _ = one_seed(cls.S0, cls.T0, 3, bang="jpure", rng_seed=13)

    def test_census(self):
        for T in (self.T1, self.T2):
            self.assertEqual(T.names, self.T0.names)               # 0 gear types added
            self.assertEqual(len(T), len(self.T0) + 1)              # exactly one monomial added
            self.assertEqual(len(T.designations), len(self.T0.designations) + 1)
            self.assertLessEqual(T.rank, 4)
            c = theta_reader_census(T)
            self.assertTrue(c["no_matter_reads_theta"])
            self.assertEqual(c["readers_of_theta"].get(LAPSE), 1)
        self.assertEqual(lapse_reader_census(self.T1), lapse_reader_census(self.T0))

    def test_bad_args(self):
        with self.assertRaises(ValueError):
            build_clockgen(kappa=0)
        with self.assertRaises(ValueError):
            build_clockgen(mode="other")
        with self.assertRaises(ValueError):
            clockgen_system(one_kw={"couple_doublet": True})

    def test_footprint_exact(self):
        """inputs(CG) - inputs(v1) on one state: kappa * Theta on the lapse row (drive), kappa * Theta * F (param), 0 else."""
        s = self.E0.step(self.E0.step(self.seed))
        lap, th = self.T0.gear_index(LAPSE), self.T0.gear_index(HAND)
        d1 = input_difference(self.E1, self.E0, s)
        d2 = input_difference(self.E2, self.E0, s)
        thb = np.asarray(s.b[th]).astype(OBJ)
        Fb = np.asarray(s.b[lap]).astype(OBJ)
        self.assertTrue(all(int(x) == int(y) for x, y in zip(d1[lap], thb)))
        self.assertTrue(all(int(x) == int(y) * int(z) for x, y, z in zip(d2[lap], thb, Fb)))
        for d in (d1, d2):
            rest = np.delete(d, lap, axis=0)
            self.assertTrue(all(int(x) == 0 for x in np.asarray(rest).ravel()))

    def test_vacuum_fixed(self):
        vac = State(3, np.zeros((self.T1.G, 27), dtype=np.int64), np.zeros((self.T1.G, 27), dtype=np.int64),
                    np.asarray(self.seed.r).astype(np.int64).copy())
        nxt = self.E1.step(vac)
        self.assertTrue(nxt.same_as(vac))

    def test_rewind_and_identity(self):
        s, prev = self.seed, None
        for _ in range(6):
            prev, s = s, self.E1.step(s)
            self.assertTrue(k0_identity(self.E1, prev, s, self.T1))
        self.assertTrue(self.E1.rewind(s, 6).same_as(self.seed))

    def test_cosmic_block_one_way(self):
        """The hand and every cosmic gear evolve bit-identically with and without the clock law (one-way)."""
        rows = [i for i, n in enumerate(self.T0.names) if n.startswith("cosmic.")]
        a, b = self.seed, self.seed
        for _ in range(8):
            a, b = self.E0.step(a), self.E1.step(b)
            for f in ("a", "b", "r"):
                self.assertTrue(np.array_equal(np.asarray(getattr(a, f))[rows], np.asarray(getattr(b, f))[rows]))
        self.assertEqual(lapse_sums(a, self.T0)["H"], lapse_sums(b, self.T1)["H"])


class ClockComposerTests(unittest.TestCase):
    """one_system_clock: CG2 = THE opt-in candidate (Theta0 = 2^21 CHOSEN, window-fitted, owner-approved 17:00 UTC, not
    forced; h = 2^10 FORCED by the band rule), DEFAULT OFF in the package; CG1 = the additive contrast."""

    @classmethod
    def setUpClass(cls):
        from ..layers.clockgen import one_system_clock
        cls.mk = staticmethod(one_system_clock)
        cls.Sc = one_system_clock()                       # law CG2, Theta0 = 2^21
        cls.Tc = compose(*cls.Sc.blocks)
        cls.Ec = Engine(cls.Tc, cls.Sc.Q)
        cls.Sv = one_system(couple_doublet=False, theta0=1 << 21)
        cls.Tv = compose(*cls.Sv.blocks)
        cls.seed, _ = one_seed(cls.Sv, cls.Tv, 3, bang="jpure", rng_seed=13)

    def test_off_is_v1(self):
        S0 = one_system(couple_doublet=False)
        So = self.mk(law="off")
        self.assertEqual(compose(*So.blocks).dynamics_fingerprint, compose(*S0.blocks).dynamics_fingerprint)
        self.assertEqual(compose(*S0.blocks).dynamics_fingerprint[:8], "77f6d251")

    def test_constants_and_census(self):
        cp = self.Sc.info["one"]["cosmic_params"]
        D = 6 * self.Sc.Q
        self.assertEqual(cp["theta0"], 1 << 21)
        self.assertEqual(cp["h"], 1 << 10)
        self.assertEqual(24 * cp["h"] * cp["theta0"], D - 6)          # CC-A's band rule, re-derived
        self.assertEqual((cp["k_theta"], cp["g_w"]), (1 << 32, 1310))
        self.assertEqual(self.Tc.names, self.Tv.names)
        self.assertEqual(len(self.Tc), len(self.Tv) + 1)
        self.assertEqual(len(self.Tc.designations), len(self.Tv.designations) + 1)
        self.assertLessEqual(self.Tc.rank, 4)
        c = theta_reader_census(self.Tc)
        self.assertTrue(c["no_matter_reads_theta"])
        self.assertEqual(c["readers_of_theta"].get(LAPSE), 1)
        self.assertEqual(self.Tc.dynamics_fingerprint[:8], self.FP_CG2)

    FP_CG2 = "b5bff0f0"   # dynamics fingerprint of one_system_clock() (CG2, Theta0 = 2^21), Study 34 RW6 meta

    def test_vacuum_and_rewind(self):
        vac = State(3, np.zeros((self.Tc.G, 27), dtype=np.int64), np.zeros((self.Tc.G, 27), dtype=np.int64),
                    np.asarray(self.seed.r).astype(np.int64).copy())
        self.assertTrue(self.Ec.step(vac).same_as(vac))
        s = self.seed
        for _ in range(6):
            p, s = s, self.Ec.step(s)
            self.assertTrue(k0_identity(self.Ec, p, s, self.Tc))
        self.assertTrue(self.Ec.rewind(s, 6).same_as(self.seed))

    def test_bad_law(self):
        with self.assertRaises(ValueError):
            self.mk(law="CG3")
        with self.assertRaises(ValueError):
            self.mk(law="off", one_kw={"couple_doublet": True})


class ClockWindowTests(unittest.TestCase):
    """The validity window of the opt-in CG2 law (manager 17:15 UTC): L <= 6, A_c >= 840, Theta0 = 2^21; L = 8 fails."""

    def test_window(self):
        from ..layers.clockgen import CLOCK_VALIDITY, clock_window
        self.assertEqual(CLOCK_VALIDITY["theta0"], 1 << 21)
        self.assertEqual(CLOCK_VALIDITY["L_max"], 6)
        self.assertTrue(clock_window(4)["validated"])
        self.assertTrue(clock_window(6)["validated"])
        self.assertFalse(clock_window(7)["in_window"])
        self.assertFalse(clock_window(8)["in_window"])               # CLK-B K8w: pumped on the board
        self.assertFalse(clock_window(6, theta0=1 << 24)["in_window"])  # today's scale: runaway (Study 34 RC)
        self.assertFalse(clock_window(6, A_c=780)["in_window"])        # A_c below ~0.82 x 2^10
        self.assertTrue(clock_window(6, A_c=CLOCK_VALIDITY["A_c_min"])["in_window"])
        for L, lg in ((4, 23), (6, 21), (8, 20), (10, 19), (12, 18)):  # each Theta0 has a maximum safe L
            self.assertTrue(clock_window(L, theta0=1 << lg)["in_window"])
            self.assertFalse(clock_window(L, theta0=1 << (lg + 1))["in_window"])


if __name__ == "__main__":
    unittest.main()

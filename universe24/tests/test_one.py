"""ONE (Study 22, ONE-A) fast unit tests, L = 3. Nothing is written to disk.

The DEFAULT one_system() is ONE v1 (block-diagonal, dynamics fingerprint 77f6d251...; test O12). The coupled build C1,
one_system(couple_doublet=True) (the doublet's first-order potential x the hand, Theta0 = 64; 593753fa...), is OPT-IN ONLY:
a NEW LAW candidate, REJECTED by the owner (matter must not read the clock; received about 16:13 UTC, date -u), kept for
the record after its measured runaway (Study 30). Its exactness tests (O4 - O11) are kept unchanged on the explicit opt-in.
Run ONLY in a scratch mirror (manager 14:57 UTC), ONE core, e.g. from the mirror root:
    OMP_NUM_THREADS=1 nice -n 19 python -m unittest universe24.tests.test_one -v
"""
from __future__ import annotations

import ast
import hashlib
import inspect
import textwrap
import unittest

import numpy as np

from ..core.engine import OBJ, Engine, State
from ..core.tensor import compose
from ..layers.one import (COSMIC_NS, COUPLED_THETA0, THETA0_DEFAULT, build_cosmic, cosmic_params, one_system,
                          theta_reading_census)
from ..layers.system import default_system
from ..observe.one import CosmicLedger, CosmicView
from ..observe.seed import r_star_hands_on
from ..prepare.one import one_seed
from ..prepare.system import random_system_state, system_vacuum

L = 3
FIX_I_FINGERPRINT = "b51d3f2c862fb0094c7691ad38c6acc259686cdda48a4d00645330183cbfc8e8"   # s18 STAB-B FIX_S_built
ONE_V1_FINGERPRINT = "77f6d251a8adfb2e4727bd2bd5ffeaa0e2ae3538aac393fe95c497fce754acf6"  # the DEFAULT one_system() (ONE v1)
C1_FINGERPRINT = "593753fa2d42f63d840d36c18cc24288f32d81ea71d0afa5b2ccb1a9f172cb27"      # couple_doublet=True (opt-in C1)


def _h(state) -> str:
    h = hashlib.sha256()
    for arr in (state.a, state.b, state.r):
        h.update(",".join(str(int(x)) for x in np.asarray(arr).ravel()).encode())
    return h.hexdigest()


class TestOne(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.S = one_system(couple_doublet=True)              # C1: the coupled build, OPT-IN ONLY (rejected candidate)
        cls.T = compose(*cls.S.blocks)
        cls.E = Engine(cls.T, cls.S.Q)
        cls.cp = cls.S.info["one"]["cosmic_params"]
        cls.s0, cls.rep = one_seed(cls.S, cls.T, L)
        cls.S1 = one_system(couple_doublet=False)            # ONE v1, block-diagonal (= the DEFAULT, test O12)
        cls.T1 = compose(*cls.S1.blocks)

    # ------------------------------------------------------------------ law
    def test_O1_tensor_law(self):
        for T, Q in ((self.T, self.S.Q), (self.T1, self.S1.Q)):
            self.assertLessEqual(T.rank, 4)
            self.assertEqual(Q % 2, 1)
            self.assertEqual(T.Q, Q)
            cos = [m for m in T.monomials if T.names[m.target].startswith(COSMIC_NS + ".")]
            self.assertEqual(sum(1 for m in cos if T.is_designated(m)), 30)
            self.assertEqual(sorted(len(m.factors) for m in cos if m.degree == 3), [3, 3, 3, 3])
            for m in cos:                     # the hand / readers / pairs read only cosmic gears
                for f in m.factors:
                    self.assertTrue(T.names[f.gear].startswith(COSMIC_NS + "."))
        self.assertTrue(self.S.info["one"]["fix_i"] and self.S.info["one"].get("couple_doublet"))
        self.assertEqual(self.cp["theta0"], COUPLED_THETA0)
        for m in self.T1.monomials:           # v1: block-diagonal
            tc = self.T1.names[m.target].startswith(COSMIC_NS + ".")
            for f in m.factors:
                self.assertEqual(tc, self.T1.names[f.gear].startswith(COSMIC_NS + "."))
        Tp = compose(*one_system(cosmic=False).blocks)
        self.assertEqual(Tp.dynamics_fingerprint, compose(*default_system().blocks).dynamics_fingerprint)
        self.assertEqual(Tp.dynamics_fingerprint, FIX_I_FINGERPRINT)

    def test_O2_matched_pair_and_params(self):
        cp = self.cp
        self.assertEqual(2 * cp["c_pair"] * cp["load_sum"], cp["D"])           # K+ - K- = D I exactly
        self.assertLess(cp["D"] * cp["load_sum"], 1 << 60)
        self.assertLess(cp["D"] * cp["theta0"], 1 << 61)
        self.assertEqual(24 * cp["h"] * cp["theta0"], cp["D"] - 6)
        with self.assertRaises(ValueError):
            cosmic_params(self.S.Q, c_pair=5)                                    # 5 does not divide 3Q
        blk = build_cosmic(self.S.Q)
        self.assertEqual(blk.vacuum, {g: 3 * self.S.Q - 1 for g in blk.vacuum})

    def test_O3_theta_census_v1(self):
        cen = theta_reading_census(self.T1)
        self.assertEqual(cen["readers"], [])
        self.assertTrue(cen["block_diagonal"])
        for ns in ("ref", "matter", "matter2"):
            self.assertIn("cannot read Theta", cen["per_namespace"][ns]["verdict"])

    # ------------------------------------------------------------------ exactness (coupled opt-in build C1)
    def test_O4_vacuum_rewind(self):
        S, T, E = self.S, self.T, self.E
        vac = system_vacuum(S, T, L)
        self.assertTrue(E.run(vac, 3).same_as(vac))
        r0 = random_system_state(S, T, L, seed=5)
        self.assertTrue(E.rewind(E.run(r0, 3), 3).same_as(r0))
        self.assertTrue(E.rewind(E.run(self.s0, 5), 5).same_as(self.s0))

    def test_O5_cosmic_ledgers(self):
        v = CosmicView(self.T)
        led = CosmicLedger(v, self.s0, self.cp["h"], self.cp["c_pair"])
        prev = self.s0
        for _ in range(10):
            s = self.E.step(prev)
            led.update(prev, s)
            prev = s
        self.assertEqual(led.fail, {"events": 0, "lock": 0, "born": 0, "N_J": 0})
        self.assertGreater(led.events_total, 0)

    def test_O6_rstar(self):
        for bang in ("jpure", "s2star"):
            s0, rep = one_seed(self.S, self.T, L, bang=bang)
            X = r_star_hands_on(self.S, self.T, rep["c2"], L)
            self.assertTrue(X(s0).same_as(s0))
            fw = bw = s0
            for _ in range(3):
                fw, bw = self.E.step(fw), self.E.inverse_step(bw)
                self.assertTrue(X(fw).same_as(bw))

    # ------------------------------------------------------------------ the owner rule: Rule3 steps only
    def test_O7_run_loop_is_rule3_only(self):
        from ..demos.one import run_one
        src = textwrap.dedent(inspect.getsource(run_one.forward))
        fn = ast.parse(src).body[0]
        calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call)]
        names = sorted(ast.unparse(c.func) for c in calls)
        self.assertEqual(names, ["engine.step", "range"])          # nothing but Rule3 steps of the composed tensor
        stepped = [s for _, s in run_one.forward(self.E, self.s0, 4)]
        ref = self.E.run(self.s0, 4, history=True)[1:]
        self.assertTrue(all(a.same_as(b) for a, b in zip(stepped, ref)))
        before = [_h(s) for s in [self.s0] + stepped]               # measurements are read-only
        v = CosmicView(self.T)
        led = CosmicLedger(v, self.s0, self.cp["h"], self.cp["c_pair"])
        prev = self.s0
        for s in stepped:
            led.update(prev, s)
            v.hand(s)
            v.delta(s)
            self.E.clicks(prev, s)
            prev = s
        self.assertEqual(before, [_h(s) for s in [self.s0] + stepped])
        run_src = inspect.getsource(run_one.run)
        self.assertNotIn(".step(", run_src.replace("forward(E, s0, args.tmax)", ""))

    # ------------------------------------------------------------------ outcome independence + hooks
    def test_O8_history_independent_of_outcomes(self):
        s7, _ = one_seed(self.S, self.T, L, rng_seed=7)
        v = CosmicView(self.T)
        keep = np.array([v.rows[g] for g in ("Th", "M1", "M2")] + list(v.package_rows), dtype=np.intp)
        a, b = self.s0, s7
        diff_out = 0
        for _ in range(12):
            a1, b1 = self.E.step(a), self.E.step(b)
            for f in ("a", "b", "r"):
                self.assertTrue(np.array_equal(np.asarray(getattr(a1, f)[keep], dtype=OBJ),
                                               np.asarray(getattr(b1, f)[keep], dtype=OBJ)))
            self.assertTrue(np.array_equal(v.delta(a1), v.delta(b1)))
            diff_out += int(np.sum(v.quotients(a, a1, "dp") != v.quotients(b, b1, "dp")))
            a, b = a1, b1
        self.assertGreater(diff_out, 0)

    def test_O9_hooks(self):
        with self.assertRaises(NotImplementedError):
            one_system(families=3)
        S = one_system(route_b=lambda base: base)
        self.assertTrue(S.info["one"]["route_b"])
        self.assertFalse(S.info["one"].get("couple_doublet"))
        self.assertEqual(S.blocks[-1].name, COSMIC_NS)
        self.assertNotIn("gwb", [b.name for b in S.blocks])
        with self.assertRaises(NotImplementedError):
            one_system(route_b=lambda base: base, couple_doublet=True)

    # ------------------------------------------------------------------ the coupling (opt-in only; rejected candidate)
    def test_O10_coupling_opt_in(self):
        """Coupled opt-in C1: legal (rank 4), only package -> hand reads cross the boundary, E1 untouched, Theta0 grain."""
        cen = theta_reading_census(self.T)
        self.assertEqual(cen["cross_reads"]["cosmic_reads_package"], 0)
        self.assertGreater(cen["cross_reads"]["package_reads_cosmic"], 0)
        em0 = {t[:3] for t in self.S1.by_name("em").terms}
        self.assertEqual({t[:3] for t in self.S.by_name("em").terms}, em0)
        with self.assertRaises(ValueError):
            one_system(theta0=128, couple_doublet=True)          # beyond today's Yukawa grain 2^6 * 6451

    def test_O11_t3_noether_with_nonuniform_hand(self):
        """Local SU(2) Noether: t3 exact with a random NON-uniform hand (coupled opt-in C1); E1 breaks t1, t2 as before."""
        from ..observe.chiral import ChiralView
        S, T, E = self.S, self.T, self.E
        view = ChiralView(T, S.by_name("chiral"), S.by_name("wsu2"))
        rng = np.random.default_rng(41)
        ve = system_vacuum(S, T, L)
        a, b = ve.a.astype(object).copy(), ve.b.astype(object).copy()
        for g in view.matter:
            a[g] = [int(x) for x in rng.integers(-40, 41, L ** 3)]
            b[g] = [int(x) for x in rng.integers(-40, 41, L ** 3)]
        for gl in list(view.links.values()) + list(view.paths.values()) + [view.higgs]:
            for g in gl:
                a[g] = [int(x) for x in rng.integers(-2, 3, L ** 3)]
                b[g] = [int(x) for x in rng.integers(-2, 3, L ** 3)]
        th, t0 = T.gear_index(f"{COSMIC_NS}.Th"), self.cp["theta0"]
        a[th] = [int(x) for x in rng.integers(-t0, t0 + 1, L ** 3)]
        b[th] = [int(x) for x in rng.integers(-t0, t0 + 1, L ** 3)]
        hist = [State(L, a, b, ve.r)]
        for _ in range(3):
            hist.append(E.step(hist[-1]))
        fails = 0
        for t in range(3):
            lhs = view.charge2(hist[t + 1], 2) - view.charge2(hist[t], 2)
            rhs = view.remainder_term2(hist[t], hist[t + 1], 2)
            fails += int(np.sum(lhs != rhs))
        self.assertEqual(fails, 0)

    # ------------------------------------------------------------------ the default switch (Study 33)
    def test_O12_default_is_v1_and_c1_opt_in_unchanged(self):
        """DEFAULT one_system() = ONE v1 (77f6d251..., = couple_doublet=False bit for bit); the explicit opt-in
        couple_doublet=True still builds C1 exactly (593753fa...)."""
        S0 = one_system()
        T0 = compose(*S0.blocks)
        self.assertEqual(T0.dynamics_fingerprint, ONE_V1_FINGERPRINT)
        self.assertEqual(self.T1.dynamics_fingerprint, ONE_V1_FINGERPRINT)
        self.assertEqual(T0.fingerprint, self.T1.fingerprint)
        self.assertNotIn("couple_doublet", S0.info["one"])
        self.assertEqual(S0.info["one"]["cosmic_params"]["theta0"], THETA0_DEFAULT)
        self.assertEqual(self.T.dynamics_fingerprint, C1_FINGERPRINT)
        self.assertEqual(self.S.info["one"]["couple_doublet"]["theta0"], COUPLED_THETA0)


if __name__ == "__main__":
    unittest.main()

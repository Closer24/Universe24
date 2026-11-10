"""EINSTEIN layer (Study 28, EINF-A) fast unit tests (L = 3 / 4). Nothing is written to disk.

Run ONLY in a scratch mirror, ONE core, e.g. from the mirror root:
    OMP_NUM_THREADS=1 nice -n 19 python -m unittest universe24.tests.test_einstein -v
Pre-registration: scratchpad s28/EINF-A_NOTES.md §2 (T1, T2, T3a, T4 exact parts, T8 exact parts, walls).
"""
from __future__ import annotations

import math
import unittest
from fractions import Fraction

import numpy as np

from ..core.engine import OBJ, Engine, State
from ..core.reciprocity import check_reciprocity
from ..core.tensor import compose
from ..layers import gravity as gr
from ..layers.einstein import (DELTA, SIGNS, WHY_BETA, build_l0_beta_read, build_l0_dewitt, build_test_light,
                               dewitt_metric_block, einstein_system)
from ..layers.gravity_l0c import build_l0c, build_l0c_lapse, m0_matrix
from ..layers.one import one_system
from ..observe.einstein import (b3_offdiagonal_wall, dewitt_check, polarisation_count, stored_to_h,
                                two_time_cycle_wall)
from ..prepare.one import one_seed

V1_FP = "77f6d251"                     # ONE v1 (couple_doublet=False): the owner's default since ~16:13 UTC (matter does not
COUPLED_FP = "593753fa"                # read the cosmic clock); the coupled build is an explicit opt-in only (first 8 hex)
RENAMED = {"metric.hxx": "metric.a1", "metric.hyy": "metric.a2", "metric.hzz": "metric.a3"}


def _reduced(Q, P, body_signs=(1, -1, 1), light=None):
    """metric (DeWitt copy) + L0 form C + its lapse + the Einstein L0 block (+ an optional test light)."""
    blocks = [build_l0c(Q=Q, body_signs=body_signs, name="ref", label="audit"), dewitt_metric_block(gr.build_metric(Q=Q)),
              build_l0c_lapse(Q=Q, P=P, field="metric.h00", body_signs=body_signs),
              build_l0_dewitt(Q=Q, P=P, body_signs=body_signs)]
    if light:
        blocks.append(build_test_light(Q=Q, P=P, mode=light, name="lt"))
    return compose(*blocks)


class TestEinstein(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # the bases are EXPLICIT (independent of which one one_system() returns by default): v1 first, coupled opt-in second
        cls.base = one_system(couple_doublet=False)
        cls.T0 = compose(*cls.base.blocks)
        cls.S = einstein_system(cls.base, on=True)
        cls.T = compose(*cls.S.blocks)
        cls.Q, cls.P = cls.S.Q, cls.S.info["P"]
        cls.base_c = one_system(couple_doublet=True)
        cls.T0c = compose(*cls.base_c.blocks)
        cls.Sc = einstein_system(cls.base_c, on=True)
        cls.Tc = compose(*cls.Sc.blocks)

    # ------------------------------------------------------------------ T1 law
    def test_T1a_default_off_is_base(self):
        """on=False returns the GIVEN base unchanged (v1 77f6d251; the explicit coupled base 593753fa); base=None builds on
        whatever one_system() returns (no fingerprint is hard-coded as 'the default')."""
        self.assertIs(einstein_system(self.base), self.base)
        self.assertIs(einstein_system(self.base_c), self.base_c)
        self.assertTrue(self.T0.dynamics_fingerprint.startswith(V1_FP))
        self.assertTrue(self.T0c.dynamics_fingerprint.startswith(COUPLED_FP))
        self.assertEqual(compose(*einstein_system().blocks).dynamics_fingerprint,
                         compose(*one_system().blocks).dynamics_fingerprint)

    def test_T1b_law(self):
        T = self.T
        self.assertEqual(T.rank, 4)
        self.assertEqual(T.Q, self.Q)
        self.assertEqual(self.Q % 2, 1)
        rep = check_reciprocity(T)
        self.assertTrue(rep.ok, rep.violations[:3])
        self.assertEqual(sorted(g for g, _ in rep.negative_sign_gears),
                         ["metric.a3", "metric.h0x", "metric.h0y", "metric.h0z"])
        new = {b.name: b for b in self.S.blocks if b.name in ("einL0", "einbeta")}
        self.assertTrue(all(len(t) == 3 for t in new["einL0"].terms))                 # reciprocal: no designation
        self.assertTrue(all(t[3]["designated_one_way"] == WHY_BETA for t in new["einbeta"].terms))
        self.assertEqual(len(T.designations) - len(self.T0.designations), len(new["einbeta"].terms))

    def test_T1c_free_part_u_identical(self):
        """Replacing ONLY the metric block by its DeWitt copy leaves the dynamics bit-identical (names/signs are metadata),
        on both bases."""
        for base, T0 in ((self.base, self.T0), (self.base_c, self.T0c)):
            blocks = [dewitt_metric_block(b) if b.name == "metric" else b for b in base.blocks]
            self.assertEqual(compose(*blocks).dynamics_fingerprint, T0.dynamics_fingerprint)
        for T in (self.T, self.Tc):
            self.assertEqual(T.rank, 4)
            self.assertTrue(check_reciprocity(T).ok)

    def test_T1d_no_new_linear_term_edge_mode(self):
        """Edge-mode lemma (s18 R5) is not triggered: every NEW monomial has degree 2 with one metric/G factor and one L0
        factor (or two L0 factors in a source): the vacuum linearisation (degree-1 monomials) is unchanged, exactly."""
        def lin(T, ren=None):
            nm = T.names
            out = set()
            for m in T.monomials:
                if m.degree == 1:
                    f = m.factors[0]
                    tg, fg = nm[m.target], nm[f.gear]
                    if ren:
                        tg, fg = ren.get(tg, tg), ren.get(fg, fg)
                    out.add((tg, m.coeff, fg, f.offset, f.field))
            return out
        self.assertEqual(lin(self.T), lin(self.T0, RENAMED))
        self.assertEqual(lin(self.Tc), lin(self.T0c, RENAMED))
        for b in self.S.blocks:
            if b.name in ("einL0", "einbeta"):
                self.assertTrue(all(len(t[2]) == 2 for t in b.terms))

    def test_T1e_vacuum_and_rewind_ONE(self):
        for S, T in ((self.S, self.T), (self.Sc, self.Tc)):
            E = Engine(T, self.Q)
            for L in (3, 4):
                vac = E.vacuum(L, {n: 3 * self.Q - 1 for n in T.names})
                self.assertTrue(E.run(vac, 10).same_as(vac))
            s0, _ = one_seed(S, T, 3)
            s = E.run(s0, 12)
            self.assertTrue(E.rewind(s, 12).same_as(s0))

    # ------------------------------------------------------------------ T2 one cone, exact dispersion
    def test_T2a_stencil_and_walls_census(self):
        """All ten metric gears: on-site 6, six faces Q - 1. h0i, hij: nothing else targets them and nothing reads them
        (the walls); a1, a2, a3: sourced only by einL0; F: unchanged sources."""
        T, Q = self.T, self.Q
        names = T.names
        for g in SIGNS:
            gi = T.gear_index(f"metric.{g}")
            st = {m.factors[0].offset: m.coeff for m in T.monomials if m.target == gi and m.degree == 1
                  and m.factors[0].gear == gi}
            self.assertEqual(st.get((0, 0, 0)), 6)
            self.assertEqual(sorted(v for k, v in st.items() if k != (0, 0, 0)), [Q - 1] * 6)
        for g in ("h0x", "h0y", "h0z", "hxy", "hxz", "hyz"):
            gi = T.gear_index(f"metric.{g}")
            self.assertEqual(sum(1 for m in T.monomials if m.target == gi), 7)
            self.assertEqual(sum(1 for m in T.monomials if m.target != gi and any(f.gear == gi for f in m.factors)), 0)
        for g in ("a1", "a2", "a3"):
            gi = T.gear_index(f"metric.{g}")
            src = [m for m in T.monomials if m.target == gi and m.degree == 2]
            self.assertTrue(src and all(names[f.gear].startswith("ref.") for m in src for f in m.factors))

    def test_T2b_symbol_exact(self):
        """cos w = m(k)/D with m(k) = 6 + 2(Q-1) Sum cos k_d, i.e. 1 - cos w = c^2 Sum (1 - cos k_d), c^2 = (Q-1)/(3Q):
        the integer identity D - m(k) = 2(Q-1) Sum (1 - cos k_d) at the 8 corner-type k (cos k_d in {1, -1})."""
        Q, D = self.Q, 6 * self.Q
        for bits in range(8):
            cs = [1 - 2 * ((bits >> d) & 1) for d in range(3)]
            m = 6 + 2 * (Q - 1) * sum(cs)
            self.assertEqual(D - m, 2 * (Q - 1) * sum(1 - c for c in cs))
        self.assertEqual(Fraction(2 * (Q - 1), D), Fraction(Q - 1, 3 * Q))

    def test_T2c_board_plane_wave_phase(self):
        """A free metric gear on the board: a plane wave turns by the exact w(k) per update (rounding <= 1e-6)."""
        Q = 8193
        L = 8
        T = compose(dewitt_metric_block(gr.build_metric(Q=Q)))
        E = Engine(T, Q)
        k = 2 * math.pi / L
        w = math.acos(1 - (Q - 1) / (3 * Q) * (1 - math.cos(k)))
        A = 2 ** 40
        G, N = T.G, L ** 3
        x = np.array([n // (L * L) for n in range(N)])
        a = np.zeros((G, N), dtype=OBJ)
        b = np.zeros((G, N), dtype=OBJ)
        g = T.gear_index("metric.a1")
        b[g] = [int(round(A * math.cos(k * xi))) for xi in x]
        a[g] = [int(round(A * math.cos(k * xi + w))) for xi in x]
        s = State(L, a, b, np.full((G, N), 3 * Q - 1, dtype=OBJ))
        n_steps = 40
        s = E.run(s, n_steps)
        v = np.array([float(s.b[g][n]) for n in range(N)])
        c0 = np.sum(v * np.cos(k * x))
        s0 = np.sum(v * np.sin(k * x))
        phase = math.atan2(-s0, c0)
        expect = (-w * n_steps + math.pi) % (2 * math.pi) - math.pi
        self.assertLess(abs((phase - expect + math.pi) % (2 * math.pi) - math.pi) / n_steps, 1e-6)

    # ------------------------------------------------------------------ T3a polarisations, DeWitt algebra
    def test_T3a_dewitt_and_polarisations(self):
        r = dewitt_check()
        self.assertEqual((r["dewitt_identity_failures"], r["trace_reversal_failures"], r["signature"]), (0, 0, (6, 4)))
        for row in polarisation_count():
            self.assertEqual((row["constraint_rank"], row["gauge_rank"], row["physical_polarisations"]), (4, 4, 2))
            self.assertTrue(row["gauge_inside_constraint"] and row["riemann_kills_gauge"])

    def test_T3b_static_newtonian_is_y0_only(self):
        """hbar_00 only (dust) <=> a1 = a2 = a3 = 0 and h_00 = h_ii = F/P (gamma = 1 from the trace reversal)."""
        vals = {g: 0 for g in SIGNS}
        vals["h00"] = 12345
        h = stored_to_h(vals)
        self.assertEqual((h["00"], h["xx"], h["yy"], h["zz"]), (12345,) * 4)

    # ------------------------------------------------------------------ T4 exact: dust sources only F; the reader factors
    def test_T4a_uniform_L0_sources_only_F(self):
        """A uniform (k = 0) L0 state has zero link energy, so it sources ONLY F (a1 = a2 = a3 inputs exactly 0)."""
        Q, P = self.Q, self.P
        T = _reduced(Q, P)
        E = Engine(T, Q)
        L = 3
        rng = np.random.default_rng(5)
        v = rng.integers(-2 ** 20, 2 ** 20, size=48)
        G, N = T.G, L ** 3
        a = np.zeros((G, N), dtype=np.int64)
        b = np.zeros((G, N), dtype=np.int64)
        for i in range(48):
            b[T.gear_index(f"ref.R{i:02d}")] = v[i]
        s = State(L, a, b, np.full((G, N), 3 * Q - 1, dtype=np.int64))
        u = E.inputs(s)
        for g in ("a1", "a2", "a3"):
            self.assertEqual(int(np.max(np.abs(u[T.gear_index(f"metric.{g}")]))), 0)
        self.assertNotEqual(int(np.max(np.abs(u[T.gear_index("metric.h00")]))), 0)

    def test_T4b_L0_reader_factors_exact(self):
        """Uniform F, a1, a2, a3: L0's input at k = pi e_d (integer Bloch states) is EXACTLY
        D v - (Q-1)[(1 - F/P) M0 + (1 - (2F + Delta_d)/P) T_d(pi)] v (the Einstein reader: h_00 on M0, h_00 + h_dd on T_d)."""
        Q, P = self.Q, self.P
        T = _reduced(Q, P)
        E = Engine(T, Q)
        L = 4
        D = 6 * Q
        M0 = m0_matrix((1, -1, 1)).astype(object)
        rng = np.random.default_rng(11)
        v0 = np.array([int(x) for x in rng.integers(-1000, 1000, size=48)], dtype=object)
        G, N = T.G, L ** 3
        coords = [(n // 16, (n // 4) % 4, n % 4) for n in range(N)]
        for d in range(3):
            sgn = np.array([(-1) ** c[d] for c in coords], dtype=object)

            def state(F0, A):
                a = np.zeros((G, N), dtype=object)
                b = np.zeros((G, N), dtype=object)
                for i in range(48):
                    b[T.gear_index(f"ref.R{i:02d}")] = v0[i] * sgn
                b[T.gear_index("metric.h00")] = F0
                for g, x in A.items():
                    b[T.gear_index(f"metric.{g}")] = x
                return State(L, a, b, np.full((G, N), 3 * Q - 1, dtype=object))
            ref_idx = [T.gear_index(f"ref.R{i:02d}") for i in range(48)]
            u00 = E.inputs(state(0, {}))[ref_idx, 0]
            Tv = np.array([Fraction(int(x), Q - 1) for x in (D * v0 - u00)], dtype=object) - M0.dot(v0)   # T_d(pi) v0
            self.assertTrue(all(Fraction(x).denominator == 1 for x in Tv))
            F0, A = 3 * P // 64, {"a1": 5 * P // 128, "a2": -7 * P // 256, "a3": 9 * P // 512}
            Dd = sum(m * A[g] for g, m in DELTA[d].items())
            u = E.inputs(state(F0, A))[ref_idx, 0]
            pred = D * v0 - (Q - 1) * (M0.dot(v0) * Fraction(P - F0, P) + Tv * Fraction(P - 2 * F0 - Dd, P))
            self.assertTrue(all(Fraction(int(x)) == y for x, y in zip(u, pred)), f"axis {d}")

    def test_T4c_test_light_factors_exact(self):
        """Test light: link factor 1 - (2F + Delta_d)/P ('full') and 1 - F/P ('h00' control), exactly, uniform metric."""
        Q, P = self.Q, self.P
        D = 6 * Q
        for mode, fac in (("full", lambda F0, Dd: Fraction(P - 2 * F0 - Dd, P)), ("h00", lambda F0, Dd: Fraction(P - F0, P))):
            T = _reduced(Q, P, light=mode)
            E = Engine(T, Q)
            L = 4
            G, N = T.G, L ** 3
            coords = [(n // 16, (n // 4) % 4, n % 4) for n in range(N)]
            for d in range(3):
                A = {"a1": 3 * P // 64, "a2": P // 32, "a3": -P // 128}
                F0 = P // 16
                Dd = sum(m * A[g] for g, m in DELTA[d].items())
                a = np.zeros((G, N), dtype=object)
                b = np.zeros((G, N), dtype=object)
                b[T.gear_index("lt.L")] = [1000 * (-1) ** c[d] for c in coords]
                b[T.gear_index("metric.h00")] = F0
                for g, x in A.items():
                    b[T.gear_index(f"metric.{g}")] = x
                s = State(L, a, b, np.full((G, N), 3 * Q - 1, dtype=object))
                u = int(E.inputs(s)[T.gear_index("lt.L"), 0])
                # k = pi e_d: Lap -> -4 on axis d: u = D v + (Q-1) f (-4) v (x = 0 has v = +1000)
                pred = D * 1000 + (Q - 1) * fac(F0, Dd) * (-4) * 1000
                self.assertEqual(Fraction(u), pred, f"{mode} axis {d}")

    def test_T4e_beta_read_factors_exact(self):
        """einbeta: with uniform F = 0 and G = G0, L0's input at k = pi e_d is EXACTLY
        D v - (Q-1)[(1 + G0/P) M0 + (1 + (17/4) G0/P) T_d(pi)] v, i.e. clock factor 1 - 2U + 2U^2 (beta = 1) once G = F^2/(2P)."""
        from ..layers.gravity_beta_fix import build_beta_detuned
        Q, P = self.Q, self.P
        k = (Q - 1) // (2 * P)
        blocks = [build_l0c(Q=Q, body_signs=(1, -1, 1), name="ref", label="audit"), dewitt_metric_block(gr.build_metric(Q=Q)),
                  build_l0c_lapse(Q=Q, P=P, field="metric.h00", body_signs=(1, -1, 1)),
                  build_beta_detuned(Q=Q, P=P, k=k, field="metric.h00"), build_l0_beta_read(Q=Q, P=P)]
        T = compose(*blocks)
        E = Engine(T, Q)
        L = 4
        D = 6 * Q
        M0 = m0_matrix((1, -1, 1)).astype(object)
        rng = np.random.default_rng(13)
        v0 = np.array([int(x) for x in rng.integers(-1000, 1000, size=48)], dtype=object)
        G, N = T.G, L ** 3
        coords = [(n // 16, (n // 4) % 4, n % 4) for n in range(N)]
        ref_idx = [T.gear_index(f"ref.R{i:02d}") for i in range(48)]
        for d in range(3):
            sgn = np.array([(-1) ** c[d] for c in coords], dtype=object)

            def state(G0):
                a = np.zeros((G, N), dtype=object)
                b = np.zeros((G, N), dtype=object)
                for i in range(48):
                    b[ref_idx[i]] = v0[i] * sgn
                b[T.gear_index("beta.G")] = G0
                return State(L, a, b, np.full((G, N), 3 * Q - 1, dtype=object))
            u00 = E.inputs(state(0))[ref_idx, 0]
            Tv = np.array([Fraction(int(x), Q - 1) for x in (D * v0 - u00)], dtype=object) - M0.dot(v0)
            G0 = P // 64
            u = E.inputs(state(G0))[ref_idx, 0]
            pred = D * v0 - (Q - 1) * (M0.dot(v0) * Fraction(P + G0, P) + Tv * Fraction(4 * P + 17 * G0, 4 * P))
            self.assertTrue(all(Fraction(int(x)) == y for x, y in zip(u, pred)), f"axis {d}")

    def test_T4d_light_beam_sources_pp_wave_structure(self):
        """A RECIPROCAL test light beam along x (k = pi e_x) sources the metric exactly like a null beam in GR:
        hbar_yy and hbar_zz sources = 0, hbar_00 source = hbar_xx source (T_00 = T_xx, traceless), exact integers."""
        from ..observe.einstein import source_of_stored, stored_to_hbar
        Q, P = self.Q, self.P
        blocks = [dewitt_metric_block(gr.build_metric(Q=Q)),
                  build_test_light(Q=Q, P=P, mode="full", name="lt", oneway=False)]
        T = compose(*blocks)
        self.assertTrue(check_reciprocity(T).ok)
        E = Engine(T, Q)
        L = 4
        G, N = T.G, L ** 3
        a = np.zeros((G, N), dtype=object)
        b = np.zeros((G, N), dtype=object)
        b[T.gear_index("lt.L")] = [1000 * (-1) ** (n // 16) for n in range(N)]
        s = State(L, a, b, np.full((G, N), 3 * Q - 1, dtype=object))
        hb = stored_to_hbar(source_of_stored(E, s))
        self.assertEqual(int(np.max(np.abs(hb["yy"]))), 0)
        self.assertEqual(int(np.max(np.abs(hb["zz"]))), 0)
        self.assertTrue(bool(np.all(hb["00"] == hb["xx"])))
        self.assertNotEqual(int(np.max(np.abs(hb["00"]))), 0)

    # ------------------------------------------------------------------ walls
    def test_W_walls(self):
        self.assertTrue(b3_offdiagonal_wall()["wall"])
        self.assertTrue(two_time_cycle_wall()["wall"])

    def test_W_beta_read_is_second_order(self):
        """einbeta: L0 reads beta.G only (designated), coefficient integer; u has degree 2 (G x L0)."""
        blk = build_l0_beta_read(Q=self.Q, P=self.P)
        for t in blk.terms:
            self.assertEqual(len(t[2]), 2)
            self.assertEqual(sum(1 for f in t[2] if f[0] == "beta.G"), 1)
            self.assertTrue(t[0].startswith("ref."))


if __name__ == "__main__":
    unittest.main()

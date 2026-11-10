"""Stage 0.2 test T0.13: generic reversor building blocks (core/reversors.py); pre-registered in NOTES.md.

Run from the repository root:
    python -m unittest universe24.tests.test_stage02 -v
"""
from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from universe24.core import Engine, GearType, State, Tensor, build, reference_block
from universe24.tests.l0_oracle import reference_arrays, to_reference_state
from universe24.core.engine import OBJ
from universe24.core.lattice import DIRECTIONS, ZERO, lattice
from universe24.core.reversors import (GEAR_MAPS, GearwiseMap, GroupLinearMap, inversion_about_box_centre,
                                                       inversion_about_cube_centre, inversion_about_node, is_fixed,
                                                       reversor_check, uniform)
from universe24.tests import randgen
from universe24.tests.test_core import record, ref_random_state
from universe24.tests.test_layers import gradient_terms
from universe24.tests.l0_oracle import time_reverse

MAPS = ("M", "Mp", "J", "JR", "JM", "Jp")


def rstate(seed, G, L, Q, lo=-30, hi=30):
    return randgen.random_state(seed, G, L, 6 * Q, lo, hi)


def official(eng, s, s2, k):
    return [((*xyz, g), kind, q) for _, xyz, g, kind, q, _ in eng.clicks(s, s2, k).rows()]


def inversion_relabelings(ports, weights):
    """All channel permutations sigma with sigma(ports[d][h]) = ports[d^1][sigma(h)] and equal weights (search)."""
    sols = []
    for s0 in range(48):
        sigma, stack, ok = {0: s0}, [0], True
        while stack and ok:
            h = stack.pop()
            for d in range(6):
                if weights[d][h] != weights[d ^ 1][sigma[h]]:
                    ok = False
                    break
                a, b = ports[d][h], ports[d ^ 1][sigma[h]]
                if a in sigma:
                    if sigma[a] != b:
                        ok = False
                        break
                else:
                    sigma[a] = b
                    stack.append(a)
        if ok and len(sigma) == 48 and sorted(sigma.values()) == list(range(48)):
            sols.append([sigma[h] for h in range(48)])
    return sols


def perm_map(tensor, Q, names, sigma, name):
    """Gear relabeling: the new gear names[h] takes the values of the old gear names[sigma(h)]."""
    k = len(names)
    return GroupLinearMap(tensor, Q, names, [[1 if j == sigma[i] else 0 for j in range(k)] for i in range(k)],
                          name=name)


class T13Reversors(unittest.TestCase):
    def test_1_involutions(self):
        out = {}
        tensor = Tensor([GearType("n0"), GearType("n1"), GearType("Lx", link=0), GearType("Ly", link=1),
                         GearType("Lz", link=2)], [])
        for Q in (1, 7, 50):
            for L in (4, 5):
                s = rstate(13 + Q + L, tensor.G, L, Q)
                maps = [uniform(tensor, Q, m) for m in MAPS]
                rng = random.Random(Q * 100 + L)
                maps.append(GearwiseMap(tensor, Q, {n: rng.choice(list(GEAR_MAPS)) for n in tensor.names}))
                maps += [inversion_about_node(tensor, (1, 2, 0)), inversion_about_cube_centre(tensor, (0, 1, 2)),
                         inversion_about_box_centre(tensor, L)]
                maps.append(GroupLinearMap(tensor, Q, ["n0", "n1"], [[0, -1], [-1, 0]], name="swap_neg"))
                for X in maps:
                    ok = (X @ X)(s).same_as(s)
                    out[f"Q{Q}_L{L}_{X.name}"] = ok
                    self.assertTrue(ok, X.name)
                # unimodular integer matrix and its inverse (explicit remainder rules)
                A = GroupLinearMap(tensor, Q, ["n0", "n1"], [[2, 1], [1, 1]], r_rule=[(0, "id"), (1, "id")])
                Ai = GroupLinearMap(tensor, Q, ["n0", "n1"], [[1, -1], [-1, 2]], r_rule=[(0, "id"), (1, "id")])
                self.assertTrue((Ai @ A)(s).same_as(s))
                t = A(s)
                self.assertTrue(np.array_equal(t.a[0], 2 * s.a[0] + s.a[1]) and np.array_equal(t.b[1], s.b[0] + s.b[1]))
                # K^2 = J on the block
                K = GroupLinearMap(tensor, Q, ["n0", "n1"], [[0, -1], [1, 0]], name="K")
                J01 = GearwiseMap(tensor, Q, {"n0": "J", "n1": "J"})
                self.assertTrue((K @ K)(s).same_as(J01(s)))
        out["unimodular_inverse_and_K2=J"] = True
        record("T0.13_1_involutions", {"cases": out})

    def test_2_Mp_equals_universe24_time_reverse(self):
        tensor = build(reference_block(1))
        Mp = uniform(tensor, 1, "Mp")
        n = 0
        for seed in (1, 2, 3):
            rs = ref_random_state(500 + seed, 5, -40, 40)
            mine = Mp(State(5, *reference_arrays(rs, 1)))
            theirs = State(5, *reference_arrays(time_reverse(rs), 1))
            self.assertTrue(mine.same_as(theirs))
            n += 1
        record("T0.13_2_Mp_vs_time_reverse", {"states": n, "equal": True})

    def test_3_reference_reversors_and_kinds(self):
        out = {}
        for Q in (1, 7):
            tensor = build(reference_block(Q))
            eng = Engine(tensor, Q)
            for seed in (1, 2):
                s0 = State(4, *reference_arrays(ref_random_state(600 + seed, 4, -40, 40), Q))
                hist = eng.run(s0, 10, history=True)
                fwd = [official(eng, hist[k - 1], hist[k], k) for k in range(1, 11)]
                for mname in ("M", "Mp", "JR", "JM"):
                    X = uniform(tensor, Q, mname)
                    chk = reversor_check(X, eng, [s0], 10)
                    self.assertTrue(chk["ok"] and chk["identity"] == 1, (Q, mname, chk))
                    mh = eng.run(X(hist[-1]), 10, history=True)
                    back = [official(eng, mh[k - 1], mh[k], k) for k in range(1, 11)]
                    swap = mname in ("JR", "JM")
                    for k in range(10):          # mirrored update k+1 retraces original update 10-k
                        exp = sorted((addr, (0, 2, 1)[kind] if swap else kind, -q if swap else q)
                                     for addr, kind, q in fwd[9 - k])
                        self.assertEqual(sorted(back[k]), exp, (Q, mname, k))
                    out[f"Q{Q}_seed{seed}_{mname}"] = {"reversor": True, "clicks": sum(len(f) for f in fwd),
                                                       "kinds": "C1<->C2, quotient negated" if swap else "kept"}
        record("T0.13_3_reference_reversors", {"cases": out})

    def test_4_reference_inversion(self):
        from universe24.algebra.coupling import Coupling
        out = {}
        for signs in [(1, 1, 1), (1, 1, -1), (1, -1, -1), (-1, -1, -1)]:
            c = Coupling(signs)
            sols = inversion_relabelings(c.ports, c.weights)
            out[f"relabelings_{signs}"] = len(sols)
        self.assertEqual(out["relabelings_(1, 1, 1)"], 8)
        self.assertEqual(out["relabelings_(1, 1, -1)"], 0)
        c = Coupling((1, 1, 1))
        sols = inversion_relabelings(c.ports, c.weights)
        Q = 7
        tensor = build(reference_block(Q))
        eng = Engine(tensor, Q)
        names = tensor.names
        n_ok = 0
        for L in (4, 5):
            s = State(L, *reference_arrays(ref_random_state(700 + L, L, -40, 40), Q))
            for P in (inversion_about_node(tensor, (1, 0, 2)), inversion_about_cube_centre(tensor, (0, 2, 1))):
                for i, sigma in enumerate(sols):
                    X = P @ perm_map(tensor, Q, names, sigma, f"sigma{i}")
                    self.assertTrue(eng.step(X(s)).same_as(X(eng.step(s))), (L, P.name, i))
                    n_ok += 1
                self.assertFalse(eng.step(P(s)).same_as(P(eng.step(s))), "plain inversion must fail")
        out["commuting_checks"] = n_ok
        out["plain_inversion_commutes"] = False
        out["sigma0"] = sols[0]
        record("T0.13_4_reference_inversion", out)

    def test_5_link_rebasing(self):
        names = ["n0", "n1", "U0", "U1", "U2"]
        gears = [GearType("n0"), GearType("n1"), GearType("U0", link=0), GearType("U1", link=1),
                 GearType("U2", link=2)]
        links = {"U0": 0, "U1": 1, "U2": 2}
        rng = random.Random(55)
        pot = []
        for _ in range(14):
            # potential monomials whose PHYSICAL support is one link (x, x+e_k): node gears at {0, e_k}, link gear Uk
            # at 0. (A storage-legal monomial with a link gear of another axis would leave the storage rule after
            # inversion, because inversion re-bases link gears.)
            k = rng.randrange(3)
            e = DIRECTIONS[2 * k]
            P = [(f"U{k}", ZERO) if rng.random() < 0.35 else (rng.choice(["n0", "n1"]), rng.choice([ZERO, e]))
                 for _ in range(rng.randint(2, 3))]
            pot.append((rng.choice([v for v in range(-5, 6) if v]), P))

        def invert(P):            # node gear at o -> -o; link gear of axis k at o -> -o - e_k
            out = []
            for g, o in P:
                e = DIRECTIONS[2 * links[g]] if g in links else (0, 0, 0)
                out.append((g, tuple(-o[i] - e[i] for i in range(3))))
            return out
        sym = pot + [(c, invert(P)) for c, P in pot]
        tensor = Tensor(gears, gradient_terms(sym))
        Q = 10 ** 6
        eng = Engine(tensor, Q)
        res = {}
        for L in (4, 5):
            s = rstate(800 + L, tensor.G, L, Q, -20, 20)
            for P in (inversion_about_node(tensor, (2, 1, 0)), inversion_about_cube_centre(tensor, (1, 1, 0))):
                ok = eng.step(P(s)).same_as(P(eng.step(s)))
                res[f"L{L}_{P.name}"] = ok
                self.assertTrue(ok, (L, P.name))
            # control: treat link gears as node gears (no re-basing)
            plain = Tensor([GearType(n) for n in names], [])
            Pn = inversion_about_node(plain, (2, 1, 0))
            ctrl = eng.step(Pn(s)).same_as(Pn(eng.step(s)))
            res[f"L{L}_control_without_rebasing_commutes"] = ctrl
            self.assertFalse(ctrl)
        res["monomials"] = len(tensor)
        record("T0.13_5_link_rebasing", res)

    def test_6_central_detection(self):
        L, Q = 4, 7
        gears = [GearType("X"), GearType("Y")]
        lam = [(3, 1), (2, -1)]          # complex coefficients alpha + i beta, on-site and +x hop (with reciprocal -x)
        terms = []
        for (al, be), offs in zip(lam, [[ZERO], [DIRECTIONS[0], DIRECTIONS[1]]]):
            for o in offs:
                terms += [("X", al * Q, (("X", o, "b"),)), ("X", -be * Q, (("Y", o, "b"),)),
                          ("Y", be * Q, (("X", o, "b"),)), ("Y", al * Q, (("Y", o, "b"),))]
        cl = Tensor(gears, terms)
        eng = Engine(cl, Q)
        K = GroupLinearMap(cl, Q, ["X", "Y"], [[0, -1], [1, 0]], name="K")
        M = uniform(cl, Q, "M")
        J = uniform(cl, Q, "J")
        states = [rstate(900 + i, 2, L, Q, -15, 15) for i in range(4)]
        km = reversor_check(K @ M, eng, states, 12, central=[("J", J)])
        m = reversor_check(M, eng, states, 12)
        self.assertEqual(km["central"]["J"], 4)
        self.assertEqual(km["failures"], 0)
        self.assertEqual(m["identity"], 4)
        km_strict = reversor_check(K @ M, eng, states, 12)
        self.assertEqual(km_strict["failures"], 4)
        real = Tensor(gears, [("X", 2 * Q, (("X", ZERO, "b"),)), ("Y", 5 * Q, (("Y", ZERO, "b"),)),
                              ("X", Q, (("Y", DIRECTIONS[0], "b"),)), ("Y", Q, (("X", DIRECTIONS[1], "b"),))])
        ctrl = reversor_check(K @ M, Engine(real, Q), states, 12, central=[("J", J)])
        self.assertGreater(ctrl["failures"], 0)
        record("T0.13_6_central", {"KM_complex_linear": km, "M": m, "KM_without_central": km_strict,
                                   "KM_real_linear_control": ctrl})

    def test_7_is_fixed(self):
        Q, L = 7, 4
        tensor = build(reference_block(Q))
        vac = Engine(tensor, Q).vacuum(L, [2 * Q] * 48)
        names = tensor.names
        res = {"P_node": is_fixed(inversion_about_node(tensor, (1, 1, 1)), vac),
               "P_cube": is_fixed(inversion_about_cube_centre(tensor), vac),
               "perm": is_fixed(perm_map(tensor, Q, names, list(range(1, 48)) + [0], "cycle"), vac),
               "M": is_fixed(uniform(tensor, Q, "M"), vac)}
        self.assertEqual(res, {"P_node": True, "P_cube": True, "perm": True, "M": False})
        record("T0.13_7_is_fixed", res)


if __name__ == "__main__":
    unittest.main()

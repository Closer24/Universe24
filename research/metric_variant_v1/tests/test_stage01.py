"""Stage 0.1 tests (pre-registered in NOTES.md): T0.11 int64 extremes (fix of B0-VERIFY X7), T0.12 opt-in strict
physical-support rule (manager ruling on X11).

Run from the repository root:
    python -m unittest research.metric_variant_v1.tests.test_stage01 -v
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from research.metric_variant_v1.core import (Engine, GearType, LocalityError, State, Tensor, build, compose,
                                             reference_block)
from research.metric_variant_v1.core.engine import OBJ
from research.metric_variant_v1.core.lattice import ZERO, lattice
from research.metric_variant_v1.core.tensor import Block
from research.metric_variant_v1.layers import build_reference
from research.metric_variant_v1.tests import randgen
from research.metric_variant_v1.tests.test_core import record

EX, EY = (1, 0, 0), (0, 1, 0)


# ---------------------------------------------------------------- independent pure-Python oracle (b-only tensors)
def _u(tensor, L, A, B, g, n):
    lat = lattice(L)
    x, y, z = lat.coords(n)
    u = 0
    for m in tensor.monomials:
        if m.target != g:
            continue
        term = m.coeff
        for f in m.factors:
            nn = lat.index(x + f.offset[0], y + f.offset[1], z + f.offset[2])
            term *= (A if f.field == "a" else B)[f.gear][nn]
        u += term
    return u


def oracle_step(tensor, Q, L, A, B, R):
    D, G, N = 6 * Q, len(A), len(A[0])
    nA, nB, nR = [[0] * N for _ in range(G)], [[0] * N for _ in range(G)], [[0] * N for _ in range(G)]
    for g in range(G):
        for n in range(N):
            ell, rn = divmod(2 * _u(tensor, L, A, B, g, n) + R[g][n], D)
            nA[g][n], nB[g][n], nR[g][n] = B[g][n], ell - A[g][n], rn
    return nA, nB, nR


def oracle_inverse(tensor, Q, L, A, B, R):
    """b-only tensors: K from the old b = new a."""
    D, G, N = 6 * Q, len(A), len(A[0])
    oA, oB, oR = [[0] * N for _ in range(G)], [[0] * N for _ in range(G)], [[0] * N for _ in range(G)]
    for g in range(G):
        for n in range(N):
            K = 2 * _u(tensor, L, None, A, g, n)
            r = (R[g][n] - K) % D
            oA[g][n], oB[g][n], oR[g][n] = (K + r - R[g][n]) // D - B[g][n], A[g][n], r
    return oA, oB, oR


def oracle_clicks(D, before, after):
    (A, B, R), (A2, B2, R2) = before, after
    rows = []
    for n in range(len(A[0])):
        for g in range(len(A)):
            q = B2[g][n] + A[g][n]
            if q != 0 and (A[g][n], B[g][n], R[g][n]) != (A2[g][n], B2[g][n], R2[g][n]):
                d = (R2[g][n] - R[g][n]) % D
                kind = 0 if d in (0, D // 2) else (1 if d < D // 2 else 2)
                rows.append((n, g, kind, q))
    return rows


def as_lists(s: State):
    return ([[int(v) for v in row] for row in s.a], [[int(v) for v in row] for row in s.b],
            [[int(v) for v in row] for row in s.r])


class T11Int64Extremes(unittest.TestCase):
    def test_T11(self):
        L, Q = 3, 1
        N = lattice(L).N
        tensors = {
            "linear": Tensor(["g"], [("g", 1, (("g", EX, "b"),))]),
            "cubic": Tensor(["g"], [("g", 1, (("g", EX, "b"),)), ("g", -1, (("g", ZERO, "b"), ("g", ZERO, "b"),
                                                                             ("g", EX, "b")))]),
        }
        M = 2 ** 63
        cases = {
            "b=-2^63": ([[3] * N], [[-M] + [1] * (N - 1)], [[2] * N]),
            "a=-2^63": ([[-M] + [0] * (N - 1)], [[5] * N], [[1] * N]),
            "b=2^63-1": ([[0] * N], [[M - 1] + [-2] * (N - 1)], [[4] * N]),
            "mixed_2^63_and_negatives": ([[M, -7] + [0] * (N - 2)], [[-3, M] + [1] * (N - 2)], [[0] * N]),
        }
        forms = {
            "plain_lists": lambda x: x,
            "int64_arrays": lambda x: np.array(x, dtype=np.int64) if all(-M <= v < M for row in x for v in row)
            else None,
            "object_arrays": lambda x: np.array(x, dtype=OBJ),
        }
        out, checked = {}, 0
        for tname, tensor in tensors.items():
            eng = Engine(tensor, Q)
            for cname, (A, B, R) in cases.items():
                exp_f = oracle_step(tensor, Q, L, A, B, R)
                exp_i = oracle_inverse(tensor, Q, L, A, B, R)
                exp_c = oracle_clicks(6 * Q, (A, B, R), exp_f)
                for fname, conv in forms.items():
                    arrs = [conv(x) for x in (A, B, R)]
                    if any(x is None for x in arrs):
                        continue                      # value does not fit int64: that input form does not exist
                    s = State(L, *arrs)
                    f = eng.step(s)
                    i = eng.inverse_step(s)
                    c = [(int(n), int(g), int(k), int(q)) for g, n, k, q in
                         zip(*(getattr(eng.clicks(s, f, 1), k) for k in ("gear", "node", "kind", "quotient")))]
                    ok = (as_lists(f) == tuple(exp_f) and as_lists(i) == tuple(exp_i) and c == exp_c)
                    out[f"{tname}/{cname}/{fname}"] = ok
                    checked += 1
                    self.assertTrue(ok, f"{tname}/{cname}/{fname}")
        record("T0.11", {"checked": checked, "cases": out})


class T12StrictSupport(unittest.TestCase):
    def test_T12(self):
        gears = [GearType("n"), GearType("Lx", "audit", link=0), GearType("Ax", "audit", link=0),
                 GearType("Ux", "audit", link=0)]
        probe = ("Lx", 1, (("n", (-1, 0, 0), "b"),))           # B0-VERIFY X11 probe
        stencil = ("Ax", 1, (("Ax", EY, "b"),))                # link-field stencil across a plaquette
        hop = [("n", 2, (("Ux", ZERO, "b"), ("n", EX, "b"))),  # hopping THROUGH the link (x, x+e_x)
               ("n", 2, (("Ux", (-1, 0, 0), "b"), ("n", (-1, 0, 0), "b"))),
               ("Ux", 2, (("n", ZERO, "b"), ("n", EX, "b")))]
        out = {}
        for name, mons in (("probe", [probe]), ("stencil", [stencil])):
            T = Tensor(gears, mons)
            self.assertEqual(len(T.support_violations()), 1, name)
            with self.assertRaises(LocalityError, msg=name):
                Tensor(gears, mons, strict_support=True)
            with self.assertRaises(LocalityError, msg=name):
                Tensor.from_dict(T.to_dict(), strict_support=True)
            out[name] = "default ACCEPTED + reported; strict REJECTED"
        T = Tensor(gears, hop, strict_support=True)
        self.assertEqual(T.support_violations(), [])
        out["hop_through_link"] = f"ACCEPTED in strict mode ({len(T)} monomials)"
        # node-gear tensors are unaffected
        build(reference_block(1), strict_support=True)
        compose(build_reference(Q=7, name="ref"), strict_support=True)
        for seed in range(10, 16):
            for a_reads in (False, True):
                build(randgen.random_tensor_block(seed, G=6, Q=10 ** 6, a_reads=a_reads), strict_support=True)
        out["reference_and_T03_tensors_strict"] = "ACCEPTED"
        blk = Block(tuple(gears), (probe,), name="lk")
        self.assertEqual(len(compose(blk).support_violations()), 1)
        with self.assertRaises(LocalityError):
            compose(blk, strict_support=True)
        out["compose_flag"] = "passes strict_support through"
        record("T0.12", {"cases": out})


if __name__ == "__main__":
    unittest.main()

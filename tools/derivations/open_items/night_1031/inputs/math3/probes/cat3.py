"""MATH3's cat-map probe (MATH2's cat.py with the shear's factor and the dial read from the structure, not typed): the third click's hidden pair (Big Pic's mode 11 at ed6a1f225, circ.py's Stepper, its triangle
part re-written line for line), in whole numbers; Rule3's carry the one division.

Usage: python -I cat3.py <tree> <click world dir> <D odd, small>

G0 the structure: the click world's edges at one Node-clock (run.joined on the layout's click plan), its triangles
   (three trains pairwise joined), C (each edge's sign on a triangle's boundary, [j, k] - [i, k] + [i, j]) and
   G = C^T C; the shear's factor is G's diagonal, the dial N = G D with D the layout's edge key. Read, not typed.

The round on the centred pair w = (u, v) = (tau - B3, eta - B3) at the dial N = 3 D: eta += 3 tau, tau += 3 eta; then
(W, tau) = carry(y, N, tau); then tau += 3 eta, eta += 3 tau. The shear's 3 is C^T C's diagonal on a lone triangle (the
triangle's edge count), not a new number; the passings y below are a probe's stand-ins (readings, not acts).

K1 the second difference u(t+2) - 38 u(t+1) + u(t) of the u row, read at three points of the round (its start, just
   before the carry, just after it), over every pair of the small torus and y = 5, 6, -4: each point's set of values.
K2 L = I mod 3: every round keeps v mod 3 and moves u mod 3 by y, on every pair of the small torus, y = 5, 6, -4.
K3 the period on the file's dial: the affine round R(w) = M w + t, M = A2 A1 = [[19, 6], [60, 19]], t = A2 (y, 0),
   raised to n = 528,480 and 3n = 1,585,440 by squaring mod N: is R^n the identity, and if not, its translation, for
   y = 1, 2, 3, 6, 9 and 10.
K4 the lag-two value floor(38 a) / (38 a) at a = 1 / 10, in per mille, by the carry.
"""

import sys
from pathlib import Path

TREE, WORLD, DS = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
sys.path.insert(0, str(TREE.joinpath("src")))
import json  # noqa: E402

import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.runner import run as trun  # noqa: E402

paths = [WORLD.joinpath(n + ".json") for n in ("universe", "piece", "setting")]
universe, piece, setting = (json.loads(x.read_text(encoding="utf-8")) for x in paths)
engine = tmain.ENGINE
kinds, tables, square, lifted = engine.made(trun.star(len(piece["shape"])))
loaded, found = trun.load(universe, setting, trun.sites_of(piece["shape"]), kinds, tables, square, lifted)
assert not found, found
layout = engine.layout(universe, piece["shape"], loaded)
trains = layout.click.weight.shape[-1]
partners = trun.joined(layout.click, trains)
edges = sorted({(min(t, u), max(t, u)) for t in range(trains) for u in partners[t]})
tris = [(i, j, k) for (i, j) in edges for k in range(j + 1, trains) if (i, k) in edges and (j, k) in edges]
C = [[(1 if e == (j, k) else 0) - (1 if e == (i, k) else 0) + (1 if e == (i, j) else 0) for (i, j, k) in tris] for e in edges]
G = [[sum(C[e][f] * C[e][g] for e in range(len(edges))) for g in range(len(tris))] for f in range(len(tris))]
DF = int(np.asarray(layout.click.key).reshape(-1)[0])
SH = G[0][0]
print(f"G0 edges {edges}; triangles {tris}; C {C}; G = C^T C = {G}; the shear's factor {SH}; the edge key D = {DF}; the dial N = {SH * DF}")


def mod(x, n):
    _, r = carry(x, n, 0)
    return r


def stepper(D):
    N = SH * D
    B3, _ = carry(N - 1, 2, 0)

    def cen(v):
        return mod(v + B3, N) - B3

    def shear(dst, src, k):
        return B3 + cen(dst - B3 + k * (src - B3))

    def rnd(t, e, y, look):
        """One round; look collects u (= tau - B3) at the round's start, before the carry and after it."""
        look[0].append(t - B3)
        e = shear(e, t, SH)
        t = shear(t, e, SH)
        look[1].append(t - B3)
        w, t = carry(y, N, t)
        look[2].append(t - B3)
        t = shear(t, e, SH)
        e = shear(e, t, SH)
        return t, e, w

    return N, B3, cen, rnd


# the half-rounds' matrices from the read factor, and the trace, exact
A1s = [[1 + SH * SH, SH], [SH, 1]]
A2s = [[1, SH], [SH, 1 + SH * SH]]
Ms = [[sum(A2s[i][k] * A1s[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
TR = Ms[0][0] + Ms[1][1]
print(f"G0 A1 = {A1s}, A2 = {A2s}, M = A2 A1 = {Ms}, trace {TR}, det {Ms[0][0] * Ms[1][1] - Ms[0][1] * Ms[1][0]}")

# K1 and K2 on the small torus
N, B3, cen, rnd = stepper(DS)
found = {y: [set(), set(), set()] for y in (5, 6, -4)}
k2_ok, k2_of = 0, 0
for y in (5, 6, -4):
    for t0 in range(N):
        for e0 in range(N):
            t, e = t0, e0
            look = [[], [], []]
            for _ in range(4):
                t1, e1, _ = rnd(t, e, y, look)
                k2_of += 1
                k2_ok += int(mod(e1 - B3, SH) == mod(e - B3, SH) and mod(t1 - B3, SH) == mod(t - B3 + y, SH))
                t, e = t1, e1
            for p in range(3):
                u = look[p]
                found[y][p].add(cen(u[2] - TR * u[1] + u[0]))
print(f"small torus N = {N}, B3 = {B3}")
for y in (5, 6, -4):
    print(f"K1 y = {y}: the u row's second difference, at the round's start {sorted(found[y][0])}, before the carry "
          f"{sorted(found[y][1])}, after it {sorted(found[y][2])} (2 G^2 y mod N centred: {cen(2 * SH * SH * y)}, -2 G^2 y: {cen(-2 * SH * SH * y)})")
print(f"K2 v mod G kept and u mod G moved by y (G = {SH}): {k2_ok} of {k2_of} rounds")

# K3 on the file's dial
NF = SH * DF


def mat(a, b):
    return [[mod(a[i][0] * b[0][j] + a[i][1] * b[1][j], NF) for j in range(2)] for i in range(2)]


def app(a, w):
    return [mod(a[i][0] * w[0] + a[i][1] * w[1], NF) for i in range(2)]


def compose(f, g):
    """f after g, each (M, t) for w -> M w + t."""
    (mf, tf), (mg, tg) = f, g
    return mat(mf, mg), [mod(x + z, NF) for x, z in zip(app(mf, tg), tf)]


def power(f, n):
    result = ([[1, 0], [0, 1]], [0, 0])
    base = f
    while n:
        n, bit = carry(n, 2, 0)
        if bit:
            result = compose(base, result)
        base = compose(base, base)
    return result


A2 = [[1, SH], [SH, 1 + SH * SH]]
M = mat(A2, [[1 + SH * SH, SH], [SH, 1]])
print(f"K3 the file's dial N = {NF} (D = {DF}); M = A2 A1 = {M}")
for y in (1, 2, 3, 6, 9, 10):
    t = app(A2, [y, 0])
    for n in (528480, 1585440):
        mn, tn = power((M, t), n)
        ident = mn == [[1, 0], [0, 1]]
        print(f"K3 y = {y}: R^{n} has M^n = I {ident}, translation {tn} "
              f"({'the identity' if ident and tn == [0, 0] else 'not the identity'}); D y mod N = {mod(DF * y, NF)}")

# K3b: R^n's translation is linear in y: t_n(y) = y t_n(1) mod N, for y = 2 .. 12
mn1, tn1 = power((M, app(A2, [1, 0])), 528480)
lin = 0
for y in range(2, 13):
    _, tny = power((M, app(A2, [y, 0])), 528480)
    lin += int(tny == [mod(y * x, NF) for x in tn1])
print(f"K3b R^528480's translation at y equals y times its translation at y = 1, mod N: {lin} of 11 (y = 2 .. 12); at y = 1 it is {tn1}")

# K4
q, _ = carry(TR, 10, 0)  # floor(TR a) at a = 1/10, TR the read trace
per, _ = carry(q * 10 * 1000, TR, 0)  # floor(TR a) / (TR a) in per mille
print(f"K4 the trace TR = {TR}; floor(TR a) = {q} at a = 1/10; floor(TR a) / (TR a) = {per} per mille")

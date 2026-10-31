"""The held hand's cells in whole numbers: the square of h (g + u) against the click world's ties and band, the square of
h (M + D L) against the mesh world's tie and vertex, and the vacuum's least under each cell, the hat's among them.

Clock: the held hand h ties the giver g and the taker u (the click world), or the tied hand's dial M and the wave's step
D L across one Mesh (the mesh world, one axis; every axis alike). A cell is h times the sum of what it ties.
Algebra: each term is the tie factor f times its cell's square; the probe expands the squares exactly as polynomials with
whole coefficients and compares them with the terms the worlds lay: f h^2 g^2, f h^2 u^2 and a band on g u; f h^2 M^2
and a vertex on M D L. A cell with no constant vanishes at the dials' 0, so its square weighs nothing there; the hat's
cell |k|^2 - n holds the constant n.
Board: the grain's rules only: the grip den Gamma^2, the rest teeth W = 6 grips (load.teeth), f = W div Gamma
(plans.holding), the held hand's own spring S = the grip; every division the carry's, its remainder checked 0. No world
is run here (Big Pic's miracle/cell.py runs the band's cell on road B). No value is searched.
Clicks: none.

Usage: python3 -I held_cells.py <src of node-all 9d75a4904> <full_rate Gamma> <den> <n>
"""

import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

gamma, den, n = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])


def exact(a, b):
    """a / b by the carry, its remainder checked 0."""
    q, r = carry(a, b, 0)
    assert r == 0
    return q


def dial(size, i):
    """The polynomial of the i-th dial among size dials."""
    return {tuple(1 if j == i else 0 for j in range(size)): 1}


def add(p, q):
    out = dict(p)
    for m, c in q.items():
        out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c}


def times(p, q):
    out = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            m = tuple(a + b for a, b in zip(m1, m2, strict=True))
            out[m] = out.get(m, 0) + c1 * c2
    return {m: c for m, c in out.items() if c}


def scale(p, k):
    return {m: c * k for m, c in p.items() if c * k}


def zero_at_rest(p):
    """The polynomial's value with every dial at 0: its constant coefficient."""
    size = len(next(iter(p)))
    return p.get(tuple(0 for _ in range(size)), 0)


grip = den * gamma * gamma
W = 6 * grip
f = exact(W, gamma)
S = grip
print(f"grain: Gamma {gamma}, den {den}; grip {grip}, W {W}, f = W div Gamma = {f}, S = the grip {S}")

# The click world: dials (h, g, u).
h, g, u = (dial(3, i) for i in range(3))
cell = times(h, add(g, u))
square = scale(times(cell, cell), f)
ties = add(scale(times(times(h, h), times(g, g)), f), scale(times(times(h, h), times(u, u)), f))
band = add(square, scale(ties, -1))
print(
    f"click world: f (h (g + u))^2 minus the two laid ties = {band}  (the band on h^2 g u: 2 f = {2 * f})"
)
print(
    f"  the square equals the ties plus 2 f h^2 g u exactly: {band == scale(times(times(h, h), times(g, u)), 2 * f)}"
)
opposite = {}
for m, c in square.items():  # u = -g: the opposite swing
    folded = (m[0], m[1] + m[2], 0)
    opposite[folded] = opposite.get(folded, 0) + c * (1 - 2 * carry(m[2], 2, 0)[1])
opposite = {m: c for m, c in opposite.items() if c}
print(f"  the square on the opposite swing u = -g: {opposite or 0} (the cell holds g + u alone)")
print(f"  its value with every dial at 0: {zero_at_rest(square)}")

# The mesh world, one axis: dials (h, M, d), d the wave's step D L across the Mesh.
h, M, d = (dial(3, i) for i in range(3))
cell = times(h, add(M, d))
square = scale(times(cell, cell), f)
tie = scale(times(times(h, h), times(M, M)), f)
vertex = scale(times(times(h, h), times(M, d)), 2 * f)
medium = scale(times(times(h, h), times(d, d)), f)
print(
    f"mesh world: f (h (M + D L))^2 = the tie + the vertex 2 f h^2 M D L + the medium f h^2 (D L)^2 exactly:"
    f" {square == add(add(tie, vertex), medium)} (the vertex at h^2 = 1: {2 * f})"
)
print(f"  its value with every dial at 0: {zero_at_rest(square)}")

# The held hand's own spring: S |k|^2 on its four dials (the quaternion hand).
k = [dial(4, i) for i in range(4)]
norm = {}
for a in k:
    norm = add(norm, times(a, a))
print(f"the held spring S |k|^2: its value with every dial at 0: {zero_at_rest(scale(norm, S))}")

# The hat's cell |k|^2 - n: the one cell with a constant.
hat_cell = add(norm, {tuple(0 for _ in range(4)): -n})
print(
    f"the hat's cell |k|^2 - n squared: its value with every dial at 0: {zero_at_rest(times(hat_cell, hat_cell))} = n^2"
)
hat_n = exact(W, 20)  # G3's window at its top: 20 hat n = W
hat = exact(hat_n, n)
print(
    f"G3's window at its top: hat n = W div 20 = {hat_n}, hat = {hat}; 2 hat n = {2 * hat_n} against S = {S}:"
    f" {'S is at least 2 hat n, so the least of S x + hat (x - n)^2 over x = |k|^2 is at x = 0' if S >= 2 * hat_n else 'a rest off 0'}"
)
if S >= 2 * hat_n:
    print(
        f"  the vacuum's least per Node-clock beside S: hat n^2 = {hat * n * n} (W div 20 times n: {hat_n * n})"
    )
else:
    print(
        f"  the vacuum's least per Node-clock beside S, times 4 hat: 4 hat S n - S^2 = {4 * hat * S * n - S * S}"
    )


def value(p, point):
    total = 0
    for m, c in p.items():
        term = c
        for x, e in zip(point, m, strict=True):
            term *= x**e
        total += term
    return total


unit = [1 if i == 0 else 0 for i in range(4)]  # a unit of the 24, |k|^2 = 1
print(
    f"  in place of S, the hat at the unit k = (1, 0, 0, 0): hat (|k|^2 - n)^2 = {hat * value(times(hat_cell, hat_cell), unit)}"
    f" (0 exactly where n is 1, the norm of the 24's units: the least 0 on the rest |k|^2 = n)"
)

"""The held hand's cells in whole numbers: the square of h (g + u) against the click world's ties and band, the square of
h (M + D L) against the mesh world's tie and vertex, the potential at the dials' 0 under each cell, and the hat's cell.

Clock: the held hand h (h^2 = |k|^2, its rows' squares) ties the giver g and the taker u (the click world), or the tied
hand's dial M (the mesh world, one axis; every axis alike), with D L the wave's centred difference across two Meshes.
Algebra: each term is the tie factor f times its cell's square; the squares are expanded exactly as polynomials with
whole coefficients and compared with the terms the worlds lay: f h^2 g^2, f h^2 u^2 and a band on g u; f h^2 M^2 and a
vertex on M D L. A cell with no constant term is 0 at the dials' 0; the hat's cell |k|^2 - n holds the constant n.
The hat beside the held spring S: its least over whole |k|^2 with the constant written (the step rule, no search), its
continuous least, and the form without the constant, which differs by the constant alone and so has the same pushes,
under G3's two bounds and at hat n = S / 2; in place of S, at a unit of the 24. The README's ground-state bound under
the cell's vertex, at h = 20 and h = 21, by two comparisons.
Board: the grain's rules only: the grip den Gamma^2, the rest teeth W = 6 grips (load.teeth), f = W div Gamma
(plans.holding, CHOSEN with its reason there), S = the grip (OPEN in the README's strengths list). Every division is the
carry's, its remainder checked 0, but for one carry that reads a parity and one that takes a ceiling. No world is run
(Big Pic's miracle/cell.py runs the band's cell in a stand-alone model). No value is searched.
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
added = scale(times(times(h, h), times(d, d)), f)
print(
    f"mesh world: f (h (M + D L))^2 = the tie + the vertex 2 f h^2 M D L + an added term f h^2 (D L)^2 exactly:"
    f" {square == add(add(tie, vertex), added)} (the vertex at h^2 = 1: {2 * f})"
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


def whole_least(hat):
    """The least of V(x) = S x + hat (x - n)^2 over whole x = |k|^2 at or above 0, with the constant hat n^2 written.
    V is convex in x: its step V(x + 1) - V(x) = S + hat (2 x + 1 - 2 n) grows with x, so the least is at the first x
    whose step is at or above 0, x = 0 when S + hat (1 - 2 n) is at or above 0, else the ceiling of
    (2 hat n - hat - S) / (2 hat), one carry. No x is searched."""
    if S + hat * (1 - 2 * n) >= 0:
        return 0, hat * n * n
    q, r = carry(2 * hat * n - hat - S, 2 * hat, 0)
    x = q + (1 if r else 0)
    return x, S * x + hat * (x - n) * (x - n)


def continuous_least_times_4hat(hat):
    """4 hat times the least of V over x a fraction at or above 0: 4 hat^2 n^2 at x = 0 where S is at least 2 hat n,
    else 4 hat S n - S^2 at x = n - S / (2 hat)."""
    return 4 * hat * hat * n * n if S >= 2 * hat * n else 4 * hat * S * n - S * S


# The hat beside S, written without its constant: hat |k|^4 + (S - 2 hat n) |k|^2. Its pushes are the same, since the
# two forms differ by the constant hat n^2 alone (checked as polynomials below).
for label, hat_n in (
    ("G3's measured bound for its hand with no S, 20 hat n at most W, at its top", exact(W, 20)),
    ("G3's frozen guide, 20 hat R^2 below 4 W, at its edge", exact(W, 5)),
    ("hat n = S div 2", exact(S, 2)),
):
    hat = exact(hat_n, n)
    full = add(scale(norm, S), scale(times(hat_cell, hat_cell), hat))
    free = add(scale(times(norm, norm), hat), scale(norm, S - 2 * hat * n))
    gap = add(full, scale(free, -1))
    x, v = whole_least(hat)
    print(
        f"{label}: hat n = {hat_n}. With the constant: the whole least is {v} at |k|^2 = {x}; 4 hat times the"
        f" continuous least is {continuous_least_times_4hat(hat)} (4 hat = {4 * hat}). Without it the two forms differ by"
        f" {gap} alone, and the free form's weights are hat = {hat} and S - 2 hat n = {S - 2 * hat * n}:"
        f" {'both at or above 0, so its least is 0 at k = 0' if S - 2 * hat * n >= 0 else 'the second below 0, so it is no sum of squares in |k|^2 and k'}"
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
    f"in place of S, the hat at the unit k = (1, 0, 0, 0): hat (|k|^2 - n)^2 = {hat * value(times(hat_cell, hat_cell), unit)}"
    f" at n = {n} (0 where n is 1; for a general n a whole k of norm n exists by Lagrange's four squares, not checked here)"
)
# The README's ground-state bound under the cell's vertex: (2 f h^2)^2 below grip x 2 hold f / 2 with hold = h^2 asks
# 4 f h^2 below the grip, h^2 below grip / (4 f); its two whole neighbours, by two comparisons and no root.
print(
    f"the README's bound under the cell's vertex holds while 4 f h^2 is below the grip: at h = 20, 4 f h^2 = {4 * f * 400}"
    f" against the grip {grip}: {4 * f * 400 < grip}; at h = 21, {4 * f * 441}: {4 * f * 441 < grip}"
)

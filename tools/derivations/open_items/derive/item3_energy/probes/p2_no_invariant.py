"""P2 (question 4): is any polynomial in (a, b, r) kept exactly by the engine's free tick?  An exact nullspace search.

Unknown: Q(a, b, r) = sum over monomials a^alpha b^beta of degree <= DEG, times any function of the fine teeth r (one
coefficient per value of r).  Each sampled state gives one linear equation Q(tick(state)) - Q(state) = 0, the next state
made by the engine's own step.tick.  The rational nullspace (exact Fractions) is the space of kept polynomials.
Prediction (DRAFT.md, Q4, the theorem): only constants where W >= 2 and s K is invertible mod W; the wind E and its powers
where W = 1; functions of the momentum sum Pi = sum (W (a - b) + r) where the springs are 0 (K's kernel the constants).
"""

import itertools
from fractions import Fraction

import numpy as np
from common import empty_plan, ints, layout_of, state_of, wind
from tensor24.engine import step


def monomials(nvar, deg):
    return [e for e in itertools.product(range(deg + 1), repeat=nvar) if sum(e) <= deg]


def features(a, b, r, w, mons):
    xs = list(a) + list(b)
    rs = list(itertools.product(*[range(int(x)) for x in w]))
    out = []
    for m in mons:
        v = 1
        for x, e in zip(xs, m):
            v *= int(x) ** e
        for rho in rs:
            out.append(v if tuple(int(x) for x in r) == rho else 0)
    return out


def nullspace(rows, ncols):
    """Exact RREF over Q; returns a basis of the nullspace."""
    m = [[Fraction(x) for x in row] for row in rows]
    pivots, at = [], 0
    for col in range(ncols):
        piv = next((i for i in range(at, len(m)) if m[i][col] != 0), None)
        if piv is None:
            continue
        m[at], m[piv] = m[piv], m[at]
        p = m[at][col]
        m[at] = [x / p for x in m[at]]
        for i in range(len(m)):
            if i != at and m[i][col] != 0:
                f = m[i][col]
                m[i] = [x - f * y for x, y in zip(m[i], m[at])]
        pivots.append(col)
        at += 1
        if at == len(m):
            break
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for f in free:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for i, pc in enumerate(pivots):
            v[pc] = -m[i][f]
        basis.append(v)
    return basis


def case(label, shape, w_val, spring, grips, deg, samples, seed):
    rng = np.random.default_rng(seed)
    n = int(np.prod(shape))
    w = np.full((1, n), w_val, dtype=object)
    lay = layout_of(shape, w, np.ones((1, 1), dtype=object), np.full((1, 1), spring, dtype=object),
                    np.ones((1, 1), dtype=object), np.ones((1, 1), dtype=object),
                    np.array([grips], dtype=object), empty_plan())
    mons = monomials(2 * n, deg)
    rows, states = [], []
    for _ in range(samples):
        a, b = ints(rng, -12, 13, (1, n)), ints(rng, -12, 13, (1, n))
        r = ints(rng, 0, w_val, (1, n))
        s = state_of(a, b, r, np.zeros((1, n), dtype=object))
        now, _ = step.tick(lay, s, np.ones((1, n), dtype=object))
        f0 = features(a[0], b[0], r[0], w[0], mons)
        f1 = features(now.a[0], now.b[0], now.r[0], w[0], mons)
        rows.append([x - y for x, y in zip(f1, f0)])
        states.append(s)
    ncols = len(rows[0])
    basis = nullspace(rows, ncols)
    # the named candidates, each tested directly on the same exact transitions of the engine's tick
    kept = {"E": True, "Pi": True, "r": True}
    for s in states:
        now, _ = step.tick(lay, s, np.ones((1, n), dtype=object))
        kept["E"] &= int(wind(lay, now.a, now.b)[0]) == int(wind(lay, s.a, s.b)[0])
        kept["Pi"] &= int((w * (now.a - now.b) + now.r).sum()) == int((w * (s.a - s.b) + s.r).sum())
        kept["r"] &= bool((now.r == s.r).all())
    print(f"{label}: {ncols} unknowns, {samples} exact equations from the engine's tick; kept space dim {len(basis)}; "
          f"kept on every transition: E {kept['E']}, Pi {kept['Pi']}, the fine teeth r {kept['r']}")


def main():
    # one gear, the board folded on itself (1x1x1: every Spoke returns the clock, no pull), a spring D: k = s D
    case("one gear, W = 1, D = 1 (control)", (1, 1, 1), 1, 1, [0, 0, 0], 4, 120, 1)
    case("one gear, W = 2, D = 1", (1, 1, 1), 2, 1, [0, 0, 0], 4, 160, 2)
    case("one gear, W = 3, D = 1", (1, 1, 1), 3, 1, [0, 0, 0], 4, 200, 3)
    case("one gear, W = 3, D = 2", (1, 1, 1), 3, 2, [0, 0, 0], 4, 200, 4)
    case("one gear, W = 2, D = 2 (s K = 2, not invertible mod W)", (1, 1, 1), 2, 2, [0, 0, 0], 4, 160, 5)
    # two gears on a ring of two (2x1x1): grips on its two x-Meshes; y and z fold
    case("two gears, W = 1, D = 0, grips (1, 2) (control)", (2, 1, 1), 1, 0, [1, 2, 0, 0, 0, 0], 2, 120, 6)
    case("two gears, W = 2, D = 0, grips (1, 2)", (2, 1, 1), 2, 0, [1, 2, 0, 0, 0, 0], 2, 200, 7)
    case("two gears, W = 2, D = 1, grips (1, 1)", (2, 1, 1), 2, 1, [1, 1, 0, 0, 0, 0], 2, 200, 8)
    case("two gears, W = 3, D = 1, grips (1, 1)", (2, 1, 1), 3, 1, [1, 1, 0, 0, 0, 0], 2, 300, 9)


if __name__ == "__main__":
    main()

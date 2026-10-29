"""P5 (question 4): the proved bound on the wind's drift, checked exactly, and the free orbit's wind over long runs.

Proved (DRAFT.md, Q4): where the wind E is positive definite (the board's stability: 0 < eig(W^-1/2 s K W^-1/2) < 4), the
free step is the exact rational leapfrog M (which keeps E) plus the shift e = -(r+ - r) / W on the now slot, so
    |sqrt E(n+1) - sqrt E(n)| <= sqrt C(n),   C(n) = sum (r+ - r)^2 / W  <  sum W,
i.e. the root of the wind moves by less than sqrt(sum W) a tick: at most linearly in time.  Checked here exactly: E's
positive definiteness by Sylvester's criterion (exact Bareiss minors), the inequality per tick in rationals with no root
taken ((A + B - C <= 0) or (A + B - C)^2 <= 4 A B).  Also read: the wind's range over the run, and whether the state comes
back to its start exactly (the step is a bijection, so a bounded orbit is periodic).
"""

import sys
from fractions import Fraction

import numpy as np
from common import empty_plan, ints, layout_of, state_of, stiffness, wind
from tensor24.engine import step


def gram(lay, n, w):
    """2E = z^T G z, z = (a, b): G = [[2W, -2W + sK], [-2W + sK, 2W]], K read column by column from the engine's pull."""
    s = int(lay.gearing.stretch[0, 0])
    k = np.zeros((n, n), dtype=object)
    for j in range(n):
        e = np.zeros((1, n), dtype=object)
        e[0, j] = 1
        k[:, j] = stiffness(lay, e)[0]
    wd = np.diag([int(x) for x in w[0]]).astype(object)
    top = np.concatenate((2 * wd, -2 * wd + s * k), axis=1)
    bot = np.concatenate((-2 * wd + s * k, 2 * wd), axis=1)
    return np.concatenate((top, bot), axis=0)


def positive_definite(g):
    """Sylvester: every leading principal minor > 0, by Bareiss's fraction-free elimination (exact integers)."""
    m = [[int(x) for x in row] for row in g]
    size, prev = len(m), 1
    for k in range(size):
        if m[k][k] <= 0:
            return False
        for i in range(k + 1, size):
            for j in range(k + 1, size):
                m[i][j] = (m[i][j] * m[k][k] - m[i][k] * m[k][j]) // prev
        prev = m[k][k]
    return True


def run(seed, ticks):
    rng = np.random.default_rng(seed)
    shape = tuple(int(x) for x in rng.integers(1, 3, size=3))
    n = int(np.prod(shape))
    for _ in range(200):
        w = ints(rng, 2, 7, (1, n))
        lay = layout_of(shape, w, np.ones((1, 1), dtype=object), ints(rng, 1, 3, (1, 1)),
                        np.ones((1, 1), dtype=object), np.ones((1, 1), dtype=object),
                        ints(rng, 0, 2, (1, 3 * n)), empty_plan())
        if positive_definite(gram(lay, n, w)):
            break
    else:
        return None
    s0 = state_of(ints(rng, -30, 31, (1, n)), ints(rng, -30, 31, (1, n)), ints(rng, 0, 1 << 20, (1, n)) % w,
                  np.zeros((1, n), dtype=object))
    s, e0 = s0, int(wind(lay, s0.a, s0.b)[0])
    lo = hi = e0
    bound_ok, period = 0, None
    one = np.ones((1, n), dtype=object)
    for t in range(1, ticks + 1):
        now, _ = step.tick(lay, s, one)
        a_, b_ = int(wind(lay, now.a, now.b)[0]), int(wind(lay, s.a, s.b)[0])
        c = sum(Fraction(int(x) * int(x), int(y)) for x, y in zip((now.r - s.r)[0], w[0]))
        lhs = a_ + b_ - c
        bound_ok += int(lhs <= 0 or lhs * lhs <= 4 * a_ * b_)
        lo, hi = min(lo, a_), max(hi, a_)
        s = now
        if (s.a == s0.a).all() and (s.b == s0.b).all() and (s.r == s0.r).all():
            period = t
            break
    return shape, [int(x) for x in w[0]], e0, lo, hi, bound_ok, t, period


def main():
    worlds, ticks = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (16, 6000)
    total_ok = total = 0
    for seed in range(worlds):
        got = run(seed, ticks)
        if got is None:
            print(f"seed {seed}: no positive-definite layout drawn")
            continue
        shape, w, e0, lo, hi, ok, t, period = got
        total_ok, total = total_ok + ok, total + t
        back = f"back at its start after {period} ticks" if period else f"not back within {t} ticks"
        print(f"seed {seed}: board {shape}, W {w}: E0 {e0}, E over the run within [{lo}, {hi}]"
              f" (per mille of E0: {1000 * lo // e0} to {1000 * hi // e0}); bound held {ok} of {t}; {back}")
    print(f"the per-tick bound |sqrt E+ - sqrt E| <= sqrt(sum (r+ - r)^2 / W): held at {total_ok} of {total} ticks")


if __name__ == "__main__":
    main()

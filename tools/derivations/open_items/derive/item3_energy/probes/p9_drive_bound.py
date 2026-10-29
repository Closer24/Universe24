"""P9 (question 4): the per-tick bound with J and the drive, checked exactly on the engine's tick.

Derived (DRAFT.md, Q4): the step is z+ = M z + (e, 0) with e = (s T_k q - (r+ - r)) / W, and M keeps E; where E is
positive definite (springs and grips alone decide it; J enters as a forcing), the triangle inequality gives
    |sqrt E+ - sqrt E| <= sqrt C,   C = SUM (s T_k q - (r+ - r))^2 / W,
checked with no root taken: (A + B - C <= 0) or (A + B - C)^2 <= 4 A B.  Also its sharper free form (q = 0) at the ticks
with no quantum.
"""

from fractions import Fraction

import numpy as np
from common import act, ints, layout_of, state_of, wind
from p5_drift_bound import gram, positive_definite
from tensor24.engine.state import Plan

TERMS = 6


def main():
    rng = np.random.default_rng(9)
    held = ticks = worlds = 0
    for _ in range(400):
        shape = tuple(int(x) for x in rng.integers(1, 3, size=3))
        n = int(np.prod(shape))
        w = ints(rng, 2, 8, (1, n))
        idx = [rng.integers(0, h, size=TERMS).astype(np.intp) for h in (5, 5, 1)]
        plan = Plan(idx[0], idx[1], ints(rng, -2, 3, TERMS), idx[2])
        one = np.ones((1, 1), dtype=object)
        lay = layout_of(shape, w, one, ints(rng, 1, 3, (1, 1)), ints(rng, 1, 3, (1, 1)), ints(rng, 1, 6, (1, 1)),
                        ints(rng, 0, 2, (1, 3 * n)), plan)
        if not positive_definite(gram(lay, n, w)):
            continue
        worlds += 1
        st = state_of(ints(rng, -20, 21, (1, n)), ints(rng, -20, 21, (1, n)), ints(rng, 0, 1 << 20, (1, n)) % w,
                      ints(rng, 0, 1 << 20, (1, n)) % lay.gearing.drive)
        g = lay.gearing
        for _ in range(8):
            now, _, _, q, _ = act(lay, st)
            big_a, big_b = int(wind(lay, now.a, now.b)[0]), int(wind(lay, st.a, st.b)[0])
            f = g.stretch * g.kick * q - (now.r - st.r)
            c = sum(Fraction(int(x) * int(x), int(y)) for x, y in zip(f[0], w[0]))
            lhs = big_a + big_b - c
            held += int(lhs <= 0 or lhs * lhs <= 4 * big_a * big_b)
            ticks += 1
            if max(abs(int(x)) for x in now.a.flatten()) > 1 << 40:
                break
            st = now
    print(f"{worlds} worlds with E positive definite, J random, T_d 1..5: the bound |sqrt E+ - sqrt E| <= "
          f"sqrt(SUM (s T_k q - (r+ - r))^2 / W) held at {held} of {ticks} round-ticks")


if __name__ == "__main__":
    main()

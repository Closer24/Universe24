"""P7 (question 4): the 7b gearing at rest, W = W+ = 2T with s = 2, against the same act at (T, 1), on the engine's tick.

Derived (DRAFT.md, Q4): with u = 2T (a - b) + r + 2 (F + T_k q) and r = 2 r' + e (e the fine tooth's parity bit),
u = 2 u' + e where u' = T (a - b) + r' + F + T_k q is the (T, 1) act's; so u div 2T = u' div T and u mod 2T = 2 (u' mod T) + e.
The positions run alike, r' runs as the (T, 1) remainder, and the parity e of every fine tooth is kept for ever.
Checked: (i) the trajectories agree bit for bit, with J and the drive; (ii) the wind's identity at (2T, 2); (iii) the kept
polynomials of the free one-gear act at (2T, 2): the parity bit's functions (dim 2), and not the wind.
"""

import numpy as np
from common import act, empty_plan, ints, layout_of, state_of, wind
from p2_no_invariant import features, monomials, nullspace
from tensor24.engine import step
from tensor24.engine.state import Plan

ROWS, TERMS, PLANES = 3, 10, 5


def pair(rng, n, sourced):
    t = ints(rng, 1, 8, (ROWS, n))
    d, tk, td = ints(rng, -2, 4, (ROWS, 1)), ints(rng, 1, 4, (ROWS, 1)), ints(rng, 1, 8, (ROWS, 1))
    grip = ints(rng, -2, 3, (ROWS, 3 * n))
    if sourced:
        idx = [rng.integers(0, h, size=TERMS).astype(np.intp) for h in (PLANES * ROWS, PLANES * ROWS, ROWS)]
        plan = Plan(idx[0], idx[1], ints(rng, -2, 3, TERMS), idx[2])
    else:
        plan = empty_plan()
    one = np.ones((ROWS, 1), dtype=object)
    return t, d, tk, td, grip, plan, one


def main():
    rng = np.random.default_rng(7)
    agree = ticks = ident = parity = 0
    for world in range(300):
        shape = tuple(int(x) for x in rng.integers(1, 4, size=3))
        n = int(np.prod(shape))
        t, d, tk, td, grip, plan, one = pair(rng, n, world % 2 == 1)
        low = layout_of(shape, t, one, d, tk, td, grip, plan)  # (T, 1)
        high = layout_of(shape, 2 * t, 2 * one, d, tk, td, grip, plan)  # (2T, 2)
        a, b = ints(rng, -30, 31, (ROWS, n)), ints(rng, -30, 31, (ROWS, n))
        r1 = ints(rng, 0, 1 << 20, (ROWS, n)) % t
        e = ints(rng, 0, 2, (ROWS, n))
        rd = ints(rng, 0, 1 << 20, (ROWS, n)) % td
        s1, s2 = state_of(a, b, r1, rd), state_of(a, b, 2 * r1 + e, rd)
        for _ in range(6):
            n1, _, _, _, _ = act(low, s1)
            n2, _, _, q2, _ = act(high, s2)
            ticks += 1
            agree += int((n1.a == n2.a).all() and (n2.r == 2 * n1.r + e).all() and (n1.rd == n2.rd).all())
            parity += int((n2.r % 2 == e).all())
            lhs = wind(high, n2.a, n2.b) - wind(high, s2.a, s2.b)
            rhs = ((n2.a - s2.b) * (2 * tk * q2 - (n2.r - s2.r))).sum(axis=1)
            ident += int(all(lhs == rhs))
            s1, s2 = n1, n2
            if max(abs(int(x)) for x in n2.a.flatten()) > 1 << 50:
                break
    print(f"(i) (2T, 2) runs as (T, 1) with r = 2 r' + e, a and r_d alike: {agree} of {ticks} round-ticks (300 worlds, half with J)")
    print(f"    the parity bit e of every fine tooth kept: {parity} of {ticks}")
    print(f"(ii) the wind's identity dE = sum (a+ - b)(s T_k q - (r+ - r)) at (2T, 2): {ident} of {ticks}")
    # (iii) the kept polynomials of one free gear at (2T, 2), T = 2 and 3, D = 1: degree <= 4 in (a, b), any function of r
    for t_ in (2, 3):
        w = np.full((1, 1), 2 * t_, dtype=object)
        lay = layout_of((1, 1, 1), w, np.full((1, 1), 2, dtype=object), np.ones((1, 1), dtype=object),
                        np.ones((1, 1), dtype=object), np.ones((1, 1), dtype=object),
                        np.zeros((1, 3), dtype=object), empty_plan())
        mons = monomials(2, 4)
        rows, kept_e, kept_p = [], True, True
        for _ in range(60 * t_ + 120):
            a, b, r = ints(rng, -12, 13, (1, 1)), ints(rng, -12, 13, (1, 1)), ints(rng, 0, 2 * t_, (1, 1))
            s = state_of(a, b, r, np.zeros((1, 1), dtype=object))
            nw, _ = step.tick(lay, s, np.ones((1, 1), dtype=object))
            f0, f1 = features(a[0], b[0], r[0], w[0], mons), features(nw.a[0], nw.b[0], nw.r[0], w[0], mons)
            rows.append([x - y for x, y in zip(f1, f0)])
            kept_e &= int(wind(lay, nw.a, nw.b)[0]) == int(wind(lay, a, b)[0])
            kept_p &= int(nw.r[0, 0]) % 2 == int(r[0, 0]) % 2
        basis = nullspace(rows, len(rows[0]))
        print(f"(iii) one free gear at (W, s) = ({2 * t_}, 2), D = 1: kept space dim {len(basis)}; "
              f"the wind kept {kept_e}; the parity of r kept {kept_p}")


if __name__ == "__main__":
    main()

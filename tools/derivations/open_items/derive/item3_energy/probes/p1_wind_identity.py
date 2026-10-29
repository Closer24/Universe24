"""P1 (question 4): the wind E = sum W (a - b)^2 + s a . K b over the engine's own tick, exact integers.

Claim (derived in DRAFT.md, Q4): on the synchronous act at W = W+, per gear row,
    E(a+, a) - E(a, b) = sum (a+ - b) (s T_k q - (r+ - r))
bit for bit, for any J and drive. Hence E is kept exactly where every r stays (W = 1) and q = 0, and nowhere else in general.
Also checked: the gear's carry keeps the stride exactly, pi+ = pi + push with pi = W (a - b) + r; the drive keeps J whole,
T_d q = J + r_d - r_d+; and a mutant (the identity without the remainder term) fails.
"""

import sys

import numpy as np
from common import act, empty_plan, ints, layout_of, state_of, wind
from tensor24.engine.state import Plan

ROWS, TERMS, PLANES = 3, 12, 5


def world(rng, shape, teeth_one, sourced):
    n = int(np.prod(shape))
    w = np.ones((ROWS, n), dtype=object) if teeth_one else ints(rng, 1, 10, (ROWS, n))
    s, d, tk = ints(rng, 1, 4, (ROWS, 1)), ints(rng, -2, 4, (ROWS, 1)), ints(rng, 1, 4, (ROWS, 1))
    td = ints(rng, 1, 10, (ROWS, 1))
    grip = ints(rng, -3, 4, (ROWS, 3 * n))
    if sourced:
        idx = [rng.integers(0, h, size=TERMS).astype(np.intp) for h in (PLANES * ROWS, PLANES * ROWS, ROWS)]
        plan = Plan(idx[0], idx[1], ints(rng, -3, 4, TERMS), idx[2])
    else:
        plan = empty_plan()
    lay = layout_of(shape, w, s, d, tk, td, grip, plan)
    a, b = ints(rng, -40, 41, (ROWS, n)), ints(rng, -40, 41, (ROWS, n))
    r = ints(rng, 0, 1 << 20, (ROWS, n)) % w
    rd = ints(rng, 0, 1 << 20, (ROWS, n)) % td
    return lay, state_of(a, b, r, rd)


def run(seed, teeth_one, sourced, ticks=6):
    rng = np.random.default_rng(seed)
    shape = tuple(int(x) for x in rng.integers(1, 4, size=3))
    lay, s = world(rng, shape, teeth_one, sourced)
    g = lay.gearing
    held = kept = stride = drive = mutant = ran = 0
    for _ in range(ticks):
        ran += 1
        now, out, j, q, push = act(lay, s)
        if not all(out.k.flatten() == 1):
            raise SystemExit("not synchronous")
        before, after = wind(lay, s.a, s.b), wind(lay, now.a, now.b)
        work = ((now.a - s.b) * (g.stretch * g.kick * q - (now.r - s.r))).sum(axis=1)
        held += int(all(after - before == work))
        kept += int(all(after == before))
        pi, pi1 = g.w * (s.a - s.b) + s.r, g.w * (now.a - now.b) + now.r
        stride += int((pi1 == pi + push).all())
        drive += int((g.drive * q == j + s.rd - now.rd).all())
        bare = ((now.a - s.b) * (g.stretch * g.kick * q)).sum(axis=1)
        mutant += int(all(after - before == bare))
        if max(abs(int(x)) for x in now.a.flatten()) > 1 << 60:
            break
        s = now
    return held, kept, stride, drive, mutant, ran


def main():
    worlds = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    for teeth_one, sourced, label in (
        (True, False, "W = 1, no J (the force's path, free)"),
        (False, False, "W random 1..9, no J (free gear)"),
        (True, True, "W = 1, J random, T_d random 1..9"),
        (False, True, "W random 1..9, J random, T_d random 1..9"),
    ):
        tot = [0] * 6
        for seed in range(worlds):
            for i, x in enumerate(run(seed, teeth_one, sourced)):
                tot[i] += x
        held, kept, stride, drive, mutant, ticks = tot
        print(f"{label}: {worlds} worlds, {ticks} round-ticks run (a world stops once a gear passes 2**60)")
        print(f"  identity dE = sum (a+ - b)(s T_k q - (r+ - r)) held: {held} of {ticks}")
        print(f"  E kept exactly (dE = 0 on every row): {kept} of {ticks}")
        print(f"  stride pi+ = pi + push exact: {stride} of {ticks}; drive T_d q = J + r_d - r_d+ exact: {drive} of {ticks}")
        print(f"  mutant (no remainder term) held: {mutant} of {ticks}")


if __name__ == "__main__":
    main()

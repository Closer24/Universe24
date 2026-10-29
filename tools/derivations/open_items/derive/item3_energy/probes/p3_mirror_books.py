"""P3 (question 1): the click as the drive's carry, with the take as the mirror terms of one A1 invariant.

Three hand trains X, Y, Z (part 2), coupled by U = Re(lam conj(Z) . (X o Y)), built as universe coupling rows and planned by
the engine's own load (runner/load.py plan) on the engine's own tables (main.made), then run on the engine's own tick.
  kind A1: X o Y the product (table A1 x A1 -> A1);  kind T1: X o Y the cross product (table T1 x T1 -> T1), its mirrors
  cycled (Y, Z -> X) and (Z, X -> Y).
The lay: Z's rows.  The take (the mirrors): X's rows from conj(Y) o Z, Y's rows from conj(X) o Z (the derivatives of U).
Per train t, its sweep S_t = sum Im(conj(a) pi), pi = W (a - b) + r the stride the carry keeps.  Derived (DRAFT.md, Q1):
  (c1) dS_t = tau_t + sum Im(conj(a) push_t),  tau_t = sum Im(conj(a+ - a) r+)  (the gear's torque)       every tick
  (c2) T_d d(S_X + S_Z) = T_d (tau_X + tau_Z) + s T_k sum Im(conj(a) (r_d - r_d+)) over X and Z            with the mirrors
  (c3) at W = 1 and T_d = 1: d(S_X + S_Z) = 0 and d(S_Y + S_Z) = 0, bit for bit (Manley-Rowe, the books in sweep)
  (c4) the mutant, the lay without the take (Z's rows alone): (c3) fails
  (c5) the drive's quanta: the count of ticks where sum q over the take's trains = - sum q over the lay's (the books in q)
"""

import sys

import numpy as np
from common import act, ints, layout_of, state_of
from tensor24.engine.state import Plan
from tensor24.main import made
from tensor24.runner.load import plan as planned
from tensor24.runner.load import trains_of

LABELS, DIMS = ("A1", "A2", "E", "T1", "T2"), (1, 1, 2, 3, 3)


def rows_of(lam, mirrors):
    """U = Re(lam conj(Z) . (X o Y)) as 12-field rows: the lay Z += lam X o Y; the take X += lam conj(Y) o Z and
    Y += lam Z o conj(X) (the operands cycled, so that the cross product's mirrors keep their sign).  A complex product
    u o v lands re: u_re v_re - u_im v_im and im: u_re v_im + u_im v_re; a conjugated operand flips its im part's sign.
    Operand 0 is the value; each train holds one kind (index 0)."""

    def product(f, g, t, cf, cg):
        sf, sg = (-1 if cf else 1), (-1 if cg else 1)
        return [
            [f, 0, 0, 0, g, 0, 0, 0, t, 0, 0, lam],
            [f, 0, 1, 0, g, 0, 1, 0, t, 0, 0, -lam * sf * sg],
            [f, 0, 0, 0, g, 0, 1, 0, t, 0, 1, lam * sg],
            [f, 0, 1, 0, g, 0, 0, 0, t, 0, 1, lam * sf],
        ]

    rows = product(0, 1, 2, False, False)  # the lay: Z += lam X o Y
    if mirrors:
        rows += product(1, 2, 0, True, False)  # the take on X: lam conj(Y) o Z
        rows += product(2, 0, 1, False, True)  # the take on Y: lam Z o conj(X)
    return rows


def sweep(a, pi):
    """Per train (rows re, im alternating per component): sum Im(conj(a) pi) = a_re pi_im - a_im pi_re."""
    return (a[0::2] * pi[1::2] - a[1::2] * pi[0::2]).sum()


def run(kind, seed, unit, mirrors, ticks=8):
    rng = np.random.default_rng(seed)
    shape = tuple(int(x) for x in rng.integers(1, 4, size=3))
    n = int(np.prod(shape))
    kinds, tables = made(shape)
    trains, bad = trains_of([{"name": c, "kinds": [kind], "part": 2} for c in "XYZ"], LABELS, DIMS)
    assert not bad
    lam = int(rng.choice([-2, -1, 1, 2]))
    (first, second, factor, target), refused = planned(rows_of(lam, mirrors), trains, tables, LABELS, 3)
    assert not refused, refused
    plan = Plan(first, second, factor, target)
    per = trains[0].rows()  # rows per train
    rows = 3 * per
    # a hand's two gears alike: W per (train, site), D and grips per train; s, T_k, T_d one for all (the pairing's weights)
    def alike(x):
        return np.repeat(x, per, axis=0)

    w = alike(np.ones((3, n), dtype=object) if unit else ints(rng, 1, 7, (3, n)))
    d = alike(ints(rng, 0, 3, (3, 1)))
    grip = alike(ints(rng, 0, 3, (3, 3 * n)))
    s = np.full((rows, 1), int(rng.integers(1, 3)), dtype=object)
    tk = np.full((rows, 1), int(rng.integers(1, 3)), dtype=object)
    td = np.full((rows, 1), 1 if unit else int(rng.integers(2, 6)), dtype=object)
    lay = layout_of(shape, w, s, d, tk, td, grip, plan)
    st = state_of(ints(rng, -6, 7, (rows, n)), ints(rng, -6, 7, (rows, n)),
                  ints(rng, 0, 1 << 20, (rows, n)) % w, ints(rng, 0, 1 << 20, (rows, n)) % td)
    g = lay.gearing
    tally = dict(ran=0, c1=0, c2=0, c3=0, c5=0, qmoves=0, negq=0)
    for _ in range(ticks):
        now, out, j, q, push = act(lay, st)
        pi0, pi1 = g.w * (st.a - st.b) + st.r, g.w * (now.a - now.b) + now.r
        S0 = [sweep(st.a[t * per:(t + 1) * per], pi0[t * per:(t + 1) * per]) for t in range(3)]
        S1 = [sweep(now.a[t * per:(t + 1) * per], pi1[t * per:(t + 1) * per]) for t in range(3)]
        v1 = now.a - st.a
        tau = [sweep(v1[t * per:(t + 1) * per], now.r[t * per:(t + 1) * per]) for t in range(3)]
        work = [sweep(st.a[t * per:(t + 1) * per], push[t * per:(t + 1) * per]) for t in range(3)]
        dri = [sweep(st.a[t * per:(t + 1) * per], (st.rd - now.rd)[t * per:(t + 1) * per]) for t in range(3)]
        dS = [S1[t] - S0[t] for t in range(3)]
        tally["ran"] += 1
        tally["c1"] += int(all(dS[t] == tau[t] + work[t] for t in range(3)))
        T, sk = int(td[0, 0]), int(s[0, 0] * tk[0, 0])
        tally["c2"] += int(T * (dS[0] + dS[2]) == T * (tau[0] + tau[2]) + sk * (dri[0] + dri[2])
                           and T * (dS[1] + dS[2]) == T * (tau[1] + tau[2]) + sk * (dri[1] + dri[2]))
        tally["c3"] += int(dS[0] + dS[2] == 0 and dS[1] + dS[2] == 0)
        qs = [int(q[t * per:(t + 1) * per].sum()) for t in range(3)]
        moved = any(int(x) != 0 for x in q.flatten())
        tally["qmoves"] += int(moved)
        tally["c5"] += int(moved and qs[0] + qs[1] == -qs[2])
        tally["negq"] += int(any(int(x) < 0 for x in q.flatten()))
        if max(abs(int(x)) for x in now.a.flatten()) > 1 << 50:
            break
        st = now
    return tally


def main():
    worlds = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    for kind in ("A1", "T1"):
        for unit in (True, False):
            for mirrors in (True, False):
                tot = dict(ran=0, c1=0, c2=0, c3=0, c5=0, qmoves=0, negq=0)
                for seed in range(worlds):
                    for k, v in run(kind, seed, unit, mirrors).items():
                        tot[k] += v
                tag = f"kind {kind}, " + ("W = 1, T_d = 1" if unit else "W 1..6, T_d 2..5") + (
                    ", lay + take (mirrors)" if mirrors else ", lay alone (mutant)")
                print(f"{tag}: {tot['ran']} round-ticks over {worlds} worlds")
                print(f"  (c1) dS_t = tau_t + sum Im(conj(a) push_t), every train: {tot['c1']} of {tot['ran']}")
                print(f"  (c2) the pairs X+Z, Y+Z kept up to the two torques: {tot['c2']} of {tot['ran']}")
                print(f"  (c3) the pairs X+Z, Y+Z kept bit for bit: {tot['c3']} of {tot['ran']}")
                print(f"  (c5) ticks with a drive quantum: {tot['qmoves']}; of them sum q(take) = -sum q(lay): {tot['c5']};"
                      f" ticks with some q < 0: {tot['negq']}")


if __name__ == "__main__":
    main()

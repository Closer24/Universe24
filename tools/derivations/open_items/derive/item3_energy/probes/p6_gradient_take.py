"""P6 (question 1): the take of a coupling with a gradient operand is not a coupling row, and reads two Meshes away.

The lay J_Z = lam grad X . grad Y (the centred differences, T1 x T1 -> A1 on three A1 trains of one gear), planned by the
engine's load and computed by the engine's own step.sources.  Its invariant U = sum over sites Z J_Z is linear in X, so
the exact take on X at a site x0 is dU/dX(x0) = U(X + e_x0) - U(X), exact integers.  Read: which sites of Y and Z it
depends on (a change of Y or Z at each site, one at a time).  A coupling row reads only x0 and its six neighbours.
"""

import numpy as np
from common import ints, layout_of, state_of
from tensor24.engine import step
from tensor24.engine.state import Plan
from tensor24.main import made
from tensor24.runner.load import plan as planned
from tensor24.runner.load import trains_of

LABELS, DIMS = ("A1", "A2", "E", "T1", "T2"), (1, 1, 2, 3, 3)


def main():
    shape = (7, 1, 1)  # a ring of seven along x; y and z fold
    n = 7
    _, tables = made(shape)
    trains, _ = trains_of([{"name": c, "kinds": ["A1"], "part": 1} for c in "XYZ"], LABELS, DIMS)
    (f, s, fac, t), bad = planned([[0, 0, 0, 1, 1, 0, 0, 1, 2, 0, 0, 1]], trains, tables, LABELS, 3)
    assert not bad
    one = np.ones((3, 1), dtype=object)
    lay = layout_of(shape, np.ones((3, n), dtype=object), one, 0 * one, one, one,
                    np.zeros((3, 3 * n), dtype=object), Plan(f, s, fac, t))
    rng = np.random.default_rng(0)
    a = ints(rng, -9, 10, (3, n))

    def u(field):
        _, j = step.sources(lay, state_of(field, field, 0 * field, 0 * field))
        return int((field[2] * j[2]).sum())

    def take(field, x0):
        bumped = field.copy()
        bumped[0, x0] += 1
        return u(bumped) - u(field)

    x0 = 3
    base = take(a, x0)
    for row, name in ((1, "Y"), (2, "Z")):
        reach = []
        for x in range(n):
            moved = a.copy()
            moved[row, x] += 1
            if take(moved, x0) != base:
                reach.append((x - x0 + 3) % n - 3)
        print(f"the exact take on X at x0 depends on {name} at the offsets {sorted(reach)} along x")
    print("a coupling row at x0 reads x0 and its six neighbours (offsets -1, 0, +1): the take is no coupling row")


if __name__ == "__main__":
    main()

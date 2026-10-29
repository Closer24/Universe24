"""P4 (question 1): do the engine's own tables give each coupling's mirror terms, and with which sign?

For a coupling row i x k -> m with table C = C[i, k -> m] (shape (m, i, k), C[c, a, b]: out c of m, in a of i, in b of k),
the A1 invariant is U = sum C[c, a, b] z_c x_a y_b.  Its mirror on x (target i, read from k and m) is
dU/dx_a = sum C[c, a, b] y_b z_c: is it the engine's table C[k, m -> i][a, b, c] times a sign s1?  Its mirror on y
(target k, read from m and i) is dU/dy_b = sum C[c, a, b] z_c x_a: is it C[m, i -> k][b, c, a] times a sign s2?
A sign of -1 means the mirror row must carry the strength's opposite, or the operands' order cycled (as P3 does).
"""

import itertools

import numpy as np
from tensor24.main import made

LABELS = ("A1", "A2", "E", "T1", "T2")


def ratio(u, v):
    """+1 or -1 where u = s v exactly, else None (0 where both vanish)."""
    if not u.any() and not v.any():
        return 0
    for s in (1, -1):
        if (u == s * v).all():
            return s
    return None


def main():
    _, c = made((3, 3, 3))
    signs = {}
    for i, k, m in itertools.product(range(5), repeat=3):
        t = c[(i, k, m)]
        if not t.any():
            continue
        on_x = np.einsum("cab->abc", t)  # [a, b, c]
        on_y = np.einsum("cab->bca", t)  # [b, c, a]
        signs[(i, k, m)] = (ratio(c[(k, m, i)], on_x), ratio(c[(m, i, k)], on_y))
    plus = [key for key, s in signs.items() if s == (1, 1)]
    other = {key: s for key, s in signs.items() if s != (1, 1)}
    print(f"non-zero tables: {len(signs)}; both mirrors the engine's own table with sign +1: {len(plus)}")
    for key, s in sorted(other.items()):
        name = " x ".join(LABELS[x] for x in key[:2]) + " -> " + LABELS[key[2]]
        print(f"  {name}: mirror on x {s[0]}, mirror on y {s[1]}  (None: not proportional)")


if __name__ == "__main__":
    main()

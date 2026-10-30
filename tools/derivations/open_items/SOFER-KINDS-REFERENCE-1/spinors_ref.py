"""Sofer's independent reference for the 48 (the binary octahedral group 2O) and its eight kinds, exact.

Elements: unit quaternions with coordinates in Q(sqrt 2), a coordinate x + y sqrt 2 held as a pair of Fractions.
Generators (1 + i)/sqrt 2 and (1 + i + j + k)/2; the closure must hold 48 elements. The five kinds of the 24 come from
the rotation each element induces (kinds_ref); the spinor kinds: E1/2 the trace of the lift (2 Re q), E5/2 = E1/2 A2,
G3/2 = E1/2 T1 - E1/2. Characters are pairs (a, b) meaning a + b sqrt 2, whole numbers."""

import os
import sys
from fractions import Fraction as F
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kinds_ref

Z = (F(0), F(0))


def padd(p, q):
    return (p[0] + q[0], p[1] + q[1])


def pneg(p):
    return (-p[0], -p[1])


def pmul(p, q):  # (a + b s)(c + d s) = (ac + 2bd) + (ad + bc) s, s = sqrt 2
    return (p[0] * q[0] + 2 * p[1] * q[1], p[0] * q[1] + p[1] * q[0])


def qmul(a, b):  # quaternion product, coordinates (w, x, y, z) of pairs
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b

    def m(p, q):
        return pmul(p, q)

    def s(*terms):
        out = Z
        for sign, t in terms:
            out = padd(out, t if sign > 0 else pneg(t))
        return out

    return (
        s((1, m(w1, w2)), (-1, m(x1, x2)), (-1, m(y1, y2)), (-1, m(z1, z2))),
        s((1, m(w1, x2)), (1, m(x1, w2)), (1, m(y1, z2)), (-1, m(z1, y2))),
        s((1, m(w1, y2)), (-1, m(x1, z2)), (1, m(y1, w2)), (1, m(z1, x2))),
        s((1, m(w1, z2)), (1, m(x1, y2)), (-1, m(y1, x2)), (1, m(z1, w2))),
    )


def conj(q):
    return (q[0], pneg(q[1]), pneg(q[2]), pneg(q[3]))


half, root_half = (F(1, 2), F(0)), (F(0), F(1, 2))  # 1/2 and 1/sqrt 2 = sqrt 2 / 2
zero = Z
G1 = (root_half, root_half, zero, zero)
G2 = (half, half, half, half)
ONE = ((F(1), F(0)), zero, zero, zero)


def closure():
    seen, frontier = {ONE}, [ONE]
    while frontier:
        nxt = []
        for a in frontier:
            for g in (G1, G2):
                b = qmul(a, g)
                if b not in seen:
                    seen.add(b)
                    nxt.append(b)
        frontier = nxt
    return sorted(seen)


def rotation_of(q):
    """The integer 3 x 3 matrix of v -> q v q^-1, read off the images of i, j, k (exact; entries must be whole)."""
    cols = []
    for unit in (1, 2, 3):
        v = [zero] * 4
        v[unit] = (F(1), F(0))
        r = qmul(qmul(q, tuple(v)), conj(q))
        for p in r[1:]:
            assert p[1] == 0 and p[0].denominator == 1, p
        assert r[0] == zero
        cols.append([int(p[0]) for p in r[1:]])
    return tuple(tuple(cols[j][i] for j in range(3)) for i in range(3))


def run():
    group = closure()
    assert len(group) == 48, len(group)
    table24 = kinds_ref.characters()[1]
    rows = []
    for q in group:
        rot = rotation_of(q)
        assert rot in table24, rot
        k = table24[rot]
        trace = pmul((F(2), F(0)), q[0])  # 2 Re q as a pair
        chars = {name: (F(k[name]), F(0)) for name in ("A1", "A2", "E", "T1", "T2")}
        chars["E1/2"] = trace
        chars["E5/2"] = pmul(trace, (F(k["A2"]), F(0)))
        chars["G3/2"] = padd(pmul(trace, (F(k["T1"]), F(0))), pneg(trace))
        rows.append((q, k, chars))
    names = ["A1", "A2", "E", "T1", "T2", "E1/2", "E5/2", "G3/2"]
    for i, j in product(names, names):
        s = Z
        for _, _, c in rows:
            s = padd(s, pmul(c[i], c[j]))
        assert s == ((F(48), F(0)) if i == j else Z), (i, j, s)
    dims = {n: rows[[r[0] for r in rows].index(ONE)][2][n] for n in names}
    assert sum(d[0] ** 2 for d in dims.values()) == 48, dims

    # classes: by (the lift's order, the rotation's order, trace of the lift)
    def order(q):
        x, n = q, 1
        while x != ONE:
            x, n = qmul(x, q), n + 1
        return n

    classes = {}
    for q, k, c in rows:
        classes.setdefault((order(q), k["order"], k["fixed"], c["E1/2"]), []).append(c)
    return names, classes


if __name__ == "__main__":
    names, classes = run()
    print("48 elements; 8 kinds orthonormal over the 48 lifts (all 64 sums exact).")
    print(
        "classes (lift order, rotation order, fixed faces, trace of the lift) and size, with each kind's character as (a, b) = a + b sqrt 2:"
    )
    for key, members in sorted(classes.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2], kv[0][3])):
        c = members[0]
        print(
            f"  order {key[0]} over a rotation of order {key[1]}, {len(members):2d} elements:",
            {n: (int(c[n][0]), int(c[n][1])) for n in names},
        )
    print("number of classes:", len(classes))

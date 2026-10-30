"""The spring a held count gives a three-component gear, read from the act's own tables: whole numbers alone.

A gear X of kind T1 meshes with a held count n of kind K through the three-leg table C[K, T1 -> T1] of load.tables
(made once from the Node-clock's star by main.made). With n held, the push on X is linear in X: push_x = sum over y
and z of C[x, y, z] n_y X_z, a 3 x 3 matrix M(n) on X. That matrix is the spring. The probe reads, for each kind K:

- the matrix of each of K's components: zero, symmetric, antisymmetric, diagonal, traceless;
- for an A1 + E count (n0; e1, e2): the spring's three diagonal values, their sum, their spread
  sum (d_i - mean)^2 and the discriminant prod (d_i - d_j)^2, which is 0 exactly where two masses meet;
- the Koide reading: if the three values were the roots of the masses, Koide's 2/3 would be
  sum d^2 / (sum d)^2 = 2/3, which on this form is spread = 3 (n0)^2, that is 2 (e1^2 - e1 e2 + e2^2) = 3 n0^2;
  the probe searches every whole count up to a bound and finds none (the page proves none exists);
- a T2 count along the body diagonal (a real circulant): two masses, a pair alike;
- a T1 count on a hand of two parts, read as the hermitian i M: three masses; with T2 and A1 along the same diagonal,
  the complex circulant;
- an A2 count: no T1 -> T1 spring at all (A2 x T1 is T2), and the T1 - T2 mixing C[A2, T2 -> T1].

Usage: python3 -I m2_spring.py <src of tensor24-review>
"""

import sys
from fractions import Fraction

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24 import main  # noqa: E402
from tensor24.runner.load import star  # noqa: E402

held, tables = main.made(star(3))
labels = tuple(n.upper() for n in held._fields)
at = {lab: i for i, lab in enumerate(labels)}
T1, T2 = at["T1"], at["T2"]


def spring(kind, comp):
    c = np.array(tables[(at[kind], T1, T1)], dtype=object)
    return [[int(c[x][comp][z]) for z in range(3)] for x in range(3)]


def describe(m):
    flat = [m[i][j] for i in range(3) for j in range(3)]
    if not any(flat):
        return "zero"
    sym = all(m[i][j] == m[j][i] for i in range(3) for j in range(3))
    anti = all(m[i][j] == -m[j][i] for i in range(3) for j in range(3))
    diag = all(m[i][j] == 0 for i in range(3) for j in range(3) if i != j)
    tr = m[0][0] + m[1][1] + m[2][2]
    kind = "symmetric" if sym else "antisymmetric" if anti else "neither"
    return f"{kind}, diagonal {diag}, trace {tr}: {m}"


print("the spring M(n) on a T1 gear from each held kind's components, C[K, T1 -> T1]:")
for kind in labels:
    dim = held[at[kind]].shape[-1]
    for comp in range(dim):
        print(f"  {kind}[{comp}]: {describe(spring(kind, comp))}")

a1 = spring("A1", 0)
e = [spring("E", 0), spring("E", 1)]


def values(n0, e1, e2):
    return [a1[i][i] * n0 + e[0][i][i] * e1 + e[1][i][i] * e2 for i in range(3)]


print()
print("an A1 + E count (n0; e1, e2): the spring's diagonal, as forms in the counts")
print("  d_i = a1_ii n0 + E0_ii e1 + E1_ii e2 with a1_ii", [a1[i][i] for i in range(3)],
      "E0_ii", [e[0][i][i] for i in range(3)], "E1_ii", [e[1][i][i] for i in range(3)])
print("  sum of the E parts: E0", sum(e[0][i][i] for i in range(3)), ", E1", sum(e[1][i][i] for i in range(3)))


def spread(e1, e2):
    mu = [e[0][i][i] * e1 + e[1][i][i] * e2 for i in range(3)]
    return sum(m * m for m in mu)


form = all(spread(e1, e2) == 2 * (e1 * e1 - e1 * e2 + e2 * e2) for e1 in range(-9, 10) for e2 in range(-9, 10))
print("  the spread sum mu_i^2 of the E part equals 2 (e1^2 - e1 e2 + e2^2) at every |e1|, |e2| <= 9:", form)
meet = []
three = 0
for e1 in range(-3, 4):
    for e2 in range(-3, 4):
        d = values(0, e1, e2)
        disc = ((d[0] - d[1]) * (d[1] - d[2]) * (d[2] - d[0])) ** 2
        if (e1, e2) != (0, 0):
            if disc == 0:
                meet.append((e1, e2))
            else:
                three += 1
print(f"  whole (e1, e2) in [-3, 3]^2 but 0: {three} give three masses; two meet on the lines through {meet}")

print()
print("Koide's 2/3 on this form, read as roots of the masses: sum d^2 / (sum d)^2 = 2/3 iff spread = 3 (a1 n0)^2")
found = [
    (n0, e1, e2)
    for n0 in range(1, 61)
    for e1 in range(-60, 61)
    for e2 in range(-60, 61)
    if spread(e1, e2) == 3 * (a1[0][0] * n0) ** 2
]
print(f"  whole counts with 1 <= n0 <= 60 and |e1|, |e2| <= 60 that meet it: {found or 'none'}")
best = min(
    ((abs(Fraction(spread(e1, e2), 3 * n0 * n0) - 1), n0, e1, e2)
     for n0 in range(1, 61) for e1 in range(-60, 61) for e2 in range(-60, 61) if (e1, e2) != (0, 0)),
)
gap, n0, e1, e2 = best
d = values(n0, e1, e2)
k = Fraction(sum(x * x for x in d), sum(d) ** 2)
print(f"  the nearest in that range: n0 {n0}, (e1, e2) ({e1}, {e2}), Koide's ratio {k.numerator}/{k.denominator},"
      f" off 2/3 by {(k - Fraction(2, 3)).numerator}/{(k - Fraction(2, 3)).denominator}")


def charpoly(m):
    """Characteristic polynomial of a 3 x 3 whole matrix with complex entries as pairs, from the constant up."""
    def mul(x, y):
        return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])

    def add(*xs):
        return (sum(x[0] for x in xs), sum(x[1] for x in xs))

    neg = (-1, 0)
    tr = add(m[0][0], m[1][1], m[2][2])
    minors = add(*[add(mul(m[i][i], m[j][j]), mul(neg, mul(m[i][j], m[j][i]))) for i, j in ((0, 1), (0, 2), (1, 2))])
    det = add(
        mul(m[0][0], add(mul(m[1][1], m[2][2]), mul(neg, mul(m[1][2], m[2][1])))),
        mul(neg, mul(m[0][1], add(mul(m[1][0], m[2][2]), mul(neg, mul(m[1][2], m[2][0]))))),
        mul(m[0][2], add(mul(m[1][0], m[2][1]), mul(neg, mul(m[1][1], m[2][0])))),
    )
    assert tr[1] == minors[1] == det[1] == 0, "not hermitian"
    return [-det[0], minors[0], -tr[0], 1]


def disc(p):
    """The cubic's discriminant: 0 iff two roots meet."""
    d, c, b, a = p
    return 18 * a * b * c * d - 4 * b ** 3 * d + b * b * c * c - 4 * a * c ** 3 - 27 * a * a * d * d


def combine(parts, imag=()):
    """Sum of (weight, matrix) as real parts, and (weight, matrix) as i times matrix."""
    out = [[(0, 0) for _ in range(3)] for _ in range(3)]
    for w, m in parts:
        for i in range(3):
            for j in range(3):
                out[i][j] = (out[i][j][0] + w * m[i][j], out[i][j][1])
    for w, m in imag:
        for i in range(3):
            for j in range(3):
                out[i][j] = (out[i][j][0], out[i][j][1] + w * m[i][j])
    return out


t2 = [spring("T2", c) for c in range(3)]
t1 = [spring("T1", c) for c in range(3)]
diag_t2 = combine([(1, t2[0]), (1, t2[1]), (1, t2[2])])
p = charpoly(diag_t2)
print()
print("a T2 count along the body diagonal (1, 1, 1), the real circulant: characteristic polynomial", p,
      ", discriminant", disc(p))
p = charpoly(combine([], [(1, t1[0]), (1, t1[1]), (1, t1[2])]))
print("a T1 count along (1, 1, 1) on a hand, i M: characteristic polynomial", p, ", discriminant", disc(p))
p = charpoly(combine([(1, t1[2])]))
print("  the same T1 count on a real gear, M itself (its quadratic form x M x is 0): x M x at x = (1, 2, 3):",
      sum(x * t1[2][i][j] * y for i, x in enumerate((1, 2, 3)) for j, y in enumerate((1, 2, 3))))
p = charpoly(combine([(5, a1), (2, t2[0]), (2, t2[1]), (2, t2[2])], [(1, t1[0]), (1, t1[1]), (1, t1[2])]))
print("A1 5, T2 2 and T1 1 along (1, 1, 1) on a hand, the complex circulant: polynomial", p, ", discriminant", disc(p))
mix = np.array(tables[(at["A2"], T2, T1)], dtype=object)
mm = [[int(mix[x][0][z]) for z in range(3)] for x in range(3)]
mmt = [[sum(mm[i][k] * mm[j][k] for k in range(3)) for j in range(3)] for i in range(3)]
print()
print("an A2 count: C[A2, T1 -> T1] zero:", not np.array(tables[(at["A2"], T1, T1)], dtype=object).any(),
      "; C[A2, T2 -> T1]:", mm, ", M M^T", mmt)
print("  so with a T1 gear (spring a) and a T2 gear (spring a') mixed by b: (lambda - a)(lambda - a') = b^2 (M M^T)_00,"
      " two masses, each three alike")

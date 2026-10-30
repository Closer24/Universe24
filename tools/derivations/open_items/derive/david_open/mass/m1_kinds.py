"""Which breaks of the 24 split a triplet into three masses: whole numbers alone, on the act's own kinds.

The 24 turns and their kinds come from the head's kinds.turns and kinds.kinds on the Node-clock's star. For each
subgroup H of the 24 the probe reads two things, both exact:

- which kinds of held count H leaves standing: the count of H-invariant vectors of each kind, sum of the traces over
  H divided by the order of H;
- how many different masses a held count that keeps H can give a three-component gear (T1): a generic H-invariant
  spring, S_H = sum over H of h S0 h^T for one fixed whole-number S0, and its number of distinct eigenvalues, read as
  the degree of its characteristic polynomial less the degree of that polynomial's gcd with its derivative. On a hand
  of two parts the spring may also hold an antisymmetric part, A_H = sum over H of h A0 h^T, and the count is read on
  the hermitian S_H + i A_H, whose characteristic polynomial has whole coefficients.

The restriction of each kind to the even half A4 (the turns where A2 is +1) is read by characters: m_1 trivial,
m_3 the triplet (T1's character), and the complex pair 1' + 1'' the rest.

Usage: python3 -I m1_kinds.py <src of tensor24-review>
"""

import sys
from fractions import Fraction

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.engine import kinds as K  # noqa: E402
from tensor24.runner.load import star  # noqa: E402

matrix, weight = K.turns(star(3))
held = K.kinds(matrix)
labels = tuple(n.upper() for n in held._fields)
keep = [g for g, w in enumerate(weight) if w == 1]
print("turns weighed 1:", len(keep), "; kinds", labels, "dims", tuple(k.shape[-1] for k in held))

t1 = {g: np.array(held.t1[g], dtype=object) for g in keep}
a2 = {g: int(held.a2[g][0][0]) for g in keep}
one = (1, 1, 1)


def same(m, n):
    return all(m[i][j] == n[i][j] for i in range(3) for j in range(3))


eye = np.eye(3, dtype=object)
cyc = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=object)
groups = {
    "O, the 24": keep,
    "A4, A2 = +1": [g for g in keep if a2[g] == 1],
    "D4, the z axis kept": [g for g in keep if t1[g][2][2] != 0],
    "D3, the line (1,1,1) kept": [
        g for g in keep if tuple(t1[g].dot(np.array(one, dtype=object))) in (one, (-1, -1, -1))
    ],
    "D2, the three half turns": [g for g in keep if all(t1[g][i][j] == 0 for i in range(3) for j in range(3) if i != j)],
    "C4, quarter turns about z": [g for g in keep if t1[g][2][2] == 1],
    "Z3, about (1,1,1)": [g for g in keep if same(t1[g], eye) or same(t1[g], cyc) or same(t1[g], cyc.dot(cyc))],
    "C2, the half turn about z": [g for g in keep if same(t1[g], eye) or same(t1[g], np.diag([-1, -1, 1]))],
    "1, nothing kept": [g for g in keep if same(t1[g], eye)],
}


def poly_mul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def poly_mod(p, q):
    p = [Fraction(x) for x in p]
    while len(p) >= len(q) and any(p):
        f = Fraction(p[-1], q[-1])
        shift = len(p) - len(q)
        for i, c in enumerate(q):
            p[shift + i] -= f * c
        while p and p[-1] == 0:
            p.pop()
    return p


def poly_gcd(p, q):
    p, q = [Fraction(x) for x in p], [Fraction(x) for x in q]
    while q and any(q):
        p, q = q, poly_mod(p, q)
    return p


def distinct(coeffs):
    """Coefficients from the constant up; the number of distinct roots."""
    deriv = [i * c for i, c in enumerate(coeffs)][1:]
    g = poly_gcd(coeffs, deriv)
    return (len(coeffs) - 1) - (len(g) - 1)


def cmul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def cadd(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def charpoly_herm(s, a):
    """lambda^3 - c2 lambda^2 + c1 lambda - c0 for M = s + i a, from the constant up; every c whole and real."""
    m = [[(int(s[i][j]), int(a[i][j])) for j in range(3)] for i in range(3)]
    tr = cadd(m[0][0], m[1][1], m[2][2])
    minors = cadd(*[cadd(cmul(m[i][i], m[j][j]), cmul((-1, 0), cmul(m[i][j], m[j][i])))
                    for i, j in ((0, 1), (0, 2), (1, 2))])
    det = cadd(
        cmul(m[0][0], cadd(cmul(m[1][1], m[2][2]), cmul((-1, 0), cmul(m[1][2], m[2][1])))),
        cmul((-1, 0), cmul(m[0][1], cadd(cmul(m[1][0], m[2][2]), cmul((-1, 0), cmul(m[1][2], m[2][0]))))),
        cmul(m[0][2], cadd(cmul(m[1][0], m[2][1]), cmul((-1, 0), cmul(m[1][1], m[2][0])))),
    )
    assert tr[1] == 0 and minors[1] == 0 and det[1] == 0
    return [-det[0], minors[0], -tr[0], 1]


s0 = np.array([[3, 5, 7], [5, 11, 13], [7, 13, 17]], dtype=object)
a0 = np.array([[0, 2, -3], [-2, 0, 5], [3, -5, 0]], dtype=object)
zero = np.zeros((3, 3), dtype=object)
print()
print("subgroup | order | held kinds it keeps (invariant vectors of A1, A2, E, T1, T2) | masses of a triplet: real gear, hand")
for name, hs in groups.items():
    inv = []
    for lab, k in zip(labels, held):
        total = sum(int(np.trace(np.array(k[g], dtype=object))) for g in hs)
        inv.append(total // len(hs))
    s = sum((t1[g].dot(s0).dot(t1[g].T) for g in hs), zero)
    a = sum((t1[g].dot(a0).dot(t1[g].T) for g in hs), zero)
    real = distinct(charpoly_herm(s, zero))
    hand = distinct(charpoly_herm(s, a))
    print(f"  {name}: {len(hs)} | {dict(zip(labels, inv))} | {real}, {hand}")

print()
a4 = groups["A4, A2 = +1"]
chi3 = {g: int(np.trace(t1[g])) for g in a4}
print("the kinds on the even half A4 (12 turns): m_1, m_3, and the complex pair 1' + 1''")
for lab, k in zip(labels, held):
    dim = k.shape[-1]
    chi = {g: int(np.trace(np.array(k[g], dtype=object))) for g in a4}
    m1 = sum(chi.values()) // 12
    m3 = sum(chi[g] * chi3[g] for g in a4) // 12
    print(f"  {lab}: m_1 {m1}, m_3 {m3}, 1' + 1'' {(dim - m1 - 3 * m3) // 2} pair(s)")

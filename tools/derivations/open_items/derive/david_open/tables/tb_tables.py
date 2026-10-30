"""The 24's 43 tables with no seed chosen, and the Mesh unit as one carry: the Boss's (a) and (b) of #2187 6515625919.

Whole numbers alone (no float, no root, no fraction: a quotient is compared by cross-multiplying). On the head's own 24
and five kinds:
(1) every channel C[i, k -> m] with a table has multiplicity 1: its group sum P has trace 24;
(2) one seed every channel keeps, B to the power of the seed's index (the first index heaviest), through P times its
    transpose: the head's 43 tables bit for bit after the greatest common divisor, at B = 2, 3 and 5;
(3) E's form G = [[2, -1], [-1, 2]] is kept by the 24, and S = P (3 G^-1 on an E output, G on each E input) is whole,
    symmetric and c u u^T on all 43 (u the head's table, c > 0);
(4) the reading by the diagonal (the row of S at its first diagonal entry not 0, over p = the sum of the diagonal's
    squares over its sum) gives the table on the 33 whose entries are 0 and +-1, and is off on the ten holding a 2;
(5) on those ten, c = (s1 s4 - s2 s3) div (5 (s1 s3 - s2^2)), s_k the sum of the diagonal's k-th powers, is exact;
    on the 33 it reads 0 / 0;
(6) E read in the weight basis where a table reads it still leaves ten tables holding a 2;
(7) the Mesh unit: one notch of tension moves the old Link factor (K (Gamma - 1)^2 + Gamma^2 div 2) div Gamma^2 off K
    exactly when 2 K (2 Gamma - 1) > Gamma^2, for every K up to 1,000 at Gamma 1,000; the least such K by one carry,
    Gamma^2 div (2 (2 Gamma - 1)) + 1, is 251, and the least square among them is 16^2 = 256.

Usage: python3 -I tb_tables.py <src of tensor24-review at 8ea447532>
"""

import functools
import itertools
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.engine import kinds as K  # noqa: E402
from tensor24.runner import load as L  # noqa: E402

matrix, weight = K.turns(L.star(3))
held = list(K.kinds(matrix))
inv = list(K.kinds(K.inverse(matrix)))
names = ["A1", "A2", "E", "T1", "T2"]
head = L.tables(held, inv, weight, K.projector)
G = np.array([[2, -1], [-1, 2]], dtype=object)  # the Gram matrix of (e1 - e2, e2 - e3)
G3inv = np.array([[2, 1], [1, 2]], dtype=object)  # 3 G^-1


def eye(d):
    return np.eye(d, dtype=object)


def name(i, k, m):
    return f"{names[i]} x {names[k]} -> {names[m]}"


def channels(inputs):
    """Every channel with a table: (i, k, m, shape, P), P from seed (y, p, q) to table entry (x, a, b)."""
    out = []
    for i, k, m in itertools.product(range(5), repeat=3):
        shape = tuple(held[n].shape[-1] for n in (m, i, k))
        n = int(np.prod(shape))
        P = K.projector(weight, held[m], inputs[i], inputs[k]).reshape(n, n)
        if P.any():
            out.append((i, k, m, shape, P))
    return out


def times(base, m):
    """base multiplied by itself m times (1 at m = 0)."""
    out = 1
    for _ in range(m):
        out *= base
    return out


def gcd(values):
    g = 0
    for v in values:
        a, b = abs(int(v)), g
        while b:
            a, b = b, a % b
        g = a
    return g


def quotient(num, den):
    """num / den as a reduced whole pair (den > 0), printed as a quotient prints."""
    if den < 0:
        num, den = -num, -den
    g = gcd([num, den]) or 1
    return num // g, den // g


def shown(q):
    return str(q[0]) if q[1] == 1 else f"{q[0]}/{q[1]}"


def order(p, q):
    return (p[0] * q[1] > q[0] * p[1]) - (p[0] * q[1] < q[0] * p[1])


chan = channels(inv)
traces = {sum(int(P[j, j]) for j in range(P.shape[0])) for _, _, _, _, P in chan}
print(
    f"(1) channels with a table: {len(chan)}; their group sums' traces: {sorted(traces)} (24 x the multiplicity)"
)

for B in (2, 3, 5):
    same = 0
    for i, k, m, shape, P in chan:
        n = P.shape[0]
        x = np.array([times(B, n - 1 - j) for j in range(n)], dtype=object)
        v = P.dot(P.T).dot(x)
        g = gcd(v)
        same += int(
            g > 0
            and all(int(a) // g == int(b) for a, b in zip(v, head[(i, k, m)].reshape(-1), strict=True))
        )
    print(
        f"(2) the seed B^(index), first index heaviest, B = {B}, through P P^T, over the gcd: {same} of 43 tables bit for bit"
    )

kept = all((held[2][t].T.dot(G).dot(held[2][t]) == G).all() for t in range(len(weight)) if weight[t])
print(f"(3) E's form G = [[2, -1], [-1, 2]] kept by the 24: {kept}")
sym = rank1 = boss = power = zero = 0
off, cs = [], []
for i, k, m, shape, P in chan:
    n = P.shape[0]
    u = [int(a) for a in head[(i, k, m)].reshape(-1)]
    form = np.kron(
        np.kron(G3inv if m == 2 else eye(shape[0]), G if i == 2 else eye(shape[1])),
        G if k == 2 else eye(shape[2]),
    )
    S = P.dot(form)
    sym += int((S == S.T).all())
    j = next(t for t in range(n) if u[t])
    c = quotient(int(S[j, j]), u[j] * u[j])
    rank1 += int(all(int(S[r, s]) * c[1] == c[0] * u[r] * u[s] for r in range(n) for s in range(n)))
    d = [int(S[t, t]) for t in range(n)]
    p = (sum(a * a for a in d), sum(d))  # the quotient p[0] / p[1]
    hit = all(int(S[j, s]) * p[1] == u[j] * u[s] * p[0] for s in range(n))
    boss += int(hit)
    if not hit:
        off.append(name(i, k, m))
    s1, s2, s3, s4 = (sum(times(a, q) for a in d) for q in (1, 2, 3, 4))
    num, den = s1 * s4 - s2 * s3, 5 * (s1 * s3 - s2 * s2)
    if den == 0:
        zero += int(num == 0 and max(abs(a) for a in u) == 1)
    else:
        q, r = divmod(num, den)
        power += int(r == 0 and q * c[1] == c[0])
    cs.append(c)
print(
    f"    S = P (3 G^-1 on an E output, G on each E input): whole and symmetric on {sym} of 43; c u u^T on {rank1};"
    f" c in {[shown(q) for q in sorted(set(cs), key=functools.cmp_to_key(order))]}"
)
print(f"(4) the diagonal reading: the table on {boss} of 43; off on the {len(off)} holding a 2: {off}")
print(
    f"(5) the four-power reading: exact on {power} channels; 0 / 0 on {zero}, every one a table of 0 and +-1"
)

dual = list(inv)
dual[2] = np.einsum(
    "gij->gji", held[2]
)  # E's matrices of g^-1 in the weight basis: (E(g^-1))^-T = E(g)^T
tab = L.tables(held, dual, weight, K.projector)
two = [
    name(i, k, m)
    for (i, k, m), t in tab.items()
    if t.any() and max(abs(int(a)) for a in t.reshape(-1)) > 1
]
print(f"(6) E read in the weight basis where a table reads it: {len(two)} tables still hold a 2: {two}")

gamma = 1000
wall = gamma * gamma
agree = all(
    ((kk * (gamma - 1) ** 2 + wall // 2) // wall < kk) == (2 * kk * (2 * gamma - 1) > wall)
    for kk in range(1, 1001)
)
least = wall // (2 * (2 * gamma - 1)) + 1
g = next(g for g in itertools.count(1) if 2 * g * g * (2 * gamma - 1) > wall)
print(
    f"(7) Gamma {gamma}: one notch moves the old factor off K exactly when 2 K (2 Gamma - 1) > Gamma^2, K = 1..1000: {agree};"
    f" the least K by one carry {least} ({least - 1} x {2 * (2 * gamma - 1)} = {(least - 1) * 2 * (2 * gamma - 1)},"
    f" {least} x {2 * (2 * gamma - 1)} = {least * 2 * (2 * gamma - 1)}); the least square {g}^2 = {g * g}"
)

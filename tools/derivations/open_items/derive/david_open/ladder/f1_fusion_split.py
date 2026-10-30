"""Fusion's split by 7a's own tables: the joint dial of two clocks into kinds, the shares filling the room, the equal parts'
symmetry, why a drawn kind needs rows of its own, and the composite's whole numbers from its parts' (exact fractions).

usage: python -I f1_fusion_split.py <tensor24 src>
1. For every product i x k of the five kinds: n_m = tr(G_p^-1 C^T G_m C) / dim m from 7a's primitive table C[i, k -> m],
   G the kind's kept form (the identity on A1 and A2 and on T1 and T2, whose matrices are signed permutations; [[2, -1], [-1, 2]] on
   E in its basis e1 - e2, e2 - e3); the projectors P_m = G_p^-1 C^T G_m C / n_m idempotent and summing to 1; the fill
   SUM_m |C_m x|^2_m / n_m = |x|^2_p on random whole x of the joint dial, products u x v and others.
2. Equal parts (i = k): each kind's table even or odd under the exchange u <-> v.
3. A drawn kind's part of u x v as a matrix of the two parts' components: its rank (1 is a product the parts' own rows
   could hold, more is not).
4. The composite's pair: the product of the parts' pairs (p + i s) lies on den^2's circle, so its rest beat is the sum of
   theirs; the width it costs at the example universe's den.
"""

import sys
from fractions import Fraction
from itertools import product

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24 import main  # noqa: E402

NAMES = ("A1", "A2", "E", "T1", "T2")
lab = {n: j for j, n in enumerate(NAMES)}
_, tables = main.made((3, 3, 3))
FORM = {"A1": [[1]], "A2": [[1]], "E": [[2, -1], [-1, 2]], "T1": np.eye(3, dtype=int).tolist(), "T2": np.eye(3, dtype=int).tolist()}
F = lambda m: [[Fraction(x) for x in r] for r in m]  # noqa: E731


def mat(a):
    return [[Fraction(int(x)) for x in r] for r in a]


def mm(a, b):
    return [[sum(a[i][t] * b[t][j] for t in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def tr(a):
    return sum(a[i][i] for i in range(len(a)))


def kron(a, b):
    return [[a[i][j] * b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))] for i in range(len(a)) for k in range(len(b))]


def inv(a):
    n = len(a)
    m = [list(r) + [Fraction(int(i == j)) for j in range(n)] for i, r in enumerate(a)]
    for c in range(n):
        p = next(i for i in range(c, n) if m[i][c] != 0)
        m[c], m[p] = m[p], m[c]
        m[c] = [x / m[c][c] for x in m[c]]
        for i in range(n):
            if i != c and m[i][c] != 0:
                f = m[i][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[c], strict=True)]
    return [r[n:] for r in m]


def T(a):
    return [list(r) for r in zip(*a, strict=True)]


rng = np.random.default_rng(6)
print("1. The joint dial split by 7a's tables (n_m from the table and the forms; every check exact):")
all_ok = True
for i, k in product(NAMES, NAMES):
    if lab[i] > lab[k]:
        continue
    di, dk = len(FORM[i]), len(FORM[k])
    gp = kron(F(FORM[i]), F(FORM[k]))
    gpi = inv(gp)
    parts, P = [], {}
    for m in NAMES:
        c = np.asarray(tables[(lab[i], lab[k], lab[m])], dtype=object)
        if not c.any():
            continue
        dm = len(FORM[m])
        C = mat(c.reshape(dm, di * dk))
        M = mm(mm(gpi, T(C)), mm(F(FORM[m]), C))
        n_m = tr(M) / dm
        P[m] = ([[x / n_m for x in r] for r in M], C, n_m)
        parts.append(f"{m} (n {n_m})")
    idem = all(mm(p, p) == p for p, _, _ in P.values())
    total = [[sum(P[m][0][r][s] for m in P) for s in range(di * dk)] for r in range(di * dk)]
    one = total == [[Fraction(int(r == s)) for s in range(di * dk)] for r in range(di * dk)]
    fills = 0
    for trial in range(200):
        if trial % 2:
            u, v = rng.integers(-20, 21, di), rng.integers(-20, 21, dk)
            x = [Fraction(int(a) * int(b)) for a in u for b in v]
        else:
            x = [Fraction(int(a)) for a in rng.integers(-20, 21, di * dk)]
        norm = sum(x[r] * gp[r][s] * x[s] for r in range(di * dk) for s in range(di * dk))
        shares = Fraction(0)
        for m, (_, C, n_m) in P.items():
            y = [sum(C[r][s] * x[s] for s in range(di * dk)) for r in range(len(C))]
            g = F(FORM[m])
            shares += sum(y[r] * g[r][s] * y[s] for r in range(len(y)) for s in range(len(y))) / n_m
        fills += shares == norm
    ok = idem and one and fills == 200
    all_ok &= ok
    print(f"   {i} x {k} = {' + '.join(parts)}: projectors idempotent {idem}, summing to 1 {one}, the fill {fills} of 200")
print(f"   all products: {all_ok}")

print("\n2. Equal parts: each kind's table under the exchange of the two parts (even: open to equal quanta that keep the")
print("   exchange even; odd: open only to an odd pair, closed to one train's quantum met with itself):")
for i in NAMES:
    out = []
    for m in NAMES:
        c = np.asarray(tables[(lab[i], lab[i], lab[m])], dtype=object)
        if not c.any():
            continue
        sw = np.swapaxes(c, 1, 2)
        out.append(f"{m} {'even' if np.array_equal(sw, c) else ('odd' if np.array_equal(sw, -c) else 'mixed')}")
    print(f"   {i} x {i}: {', '.join(out)}")

print("\n3. A drawn kind's part of the joint dial, as a matrix over the two parts' components (T1 x T1, 500 random pairs):")


def rank(rows):
    m = [list(r) for r in rows if any(r)]
    rk = 0
    cols = len(m[0]) if m else 0
    for c in range(cols):
        p = next((i for i in range(rk, len(m)) if m[i][c] != 0), None)
        if p is None:
            continue
        m[rk], m[p] = m[p], m[rk]
        for i in range(len(m)):
            if i != rk and m[i][c] != 0:
                f = m[i][c] / m[rk][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[rk], strict=True)]
        rk += 1
    return rk


i = k = "T1"
gp = kron(F(FORM[i]), F(FORM[k]))
gpi = inv(gp)
ranks = {}
for m in ("A1", "E", "T1", "T2"):
    c = np.asarray(tables[(lab[i], lab[k], lab[m])], dtype=object)
    dm = len(FORM[m])
    C = mat(c.reshape(dm, 9))
    M = mm(mm(gpi, T(C)), mm(F(FORM[m]), C))
    n_m = tr(M) / dm
    Pm = [[x / n_m for x in r] for r in M]
    seen = {}
    for _ in range(500):
        u, v = rng.integers(-20, 21, 3), rng.integers(-20, 21, 3)
        if not (u.any() and v.any()):
            continue
        x = [Fraction(int(a) * int(b)) for a in u for b in v]
        y = [sum(Pm[r][s] * x[s] for s in range(9)) for r in range(9)]
        if not any(y):
            continue
        rk = rank([y[0:3], y[3:6], y[6:9]])
        seen[rk] = seen.get(rk, 0) + 1
    ranks[m] = seen
    print(f"   {m}: the part's rank over the two parts (count of pairs): {dict(sorted(seen.items()))}")
print("   a rank above 1 is no product of two parts' states, so a drawn kind cannot be written back into the parts' rows")

print("\n4. The composite's pair and its width:")
den = 5525  # 5^2 x 13 x 17, a hypotenuse of several whole pairs, to show the identity
pairs = [(p, s) for p in range(1, den) for s in [int(round((den * den - p * p) ** 0.5))] if s > 0 and p * p + s * s == den * den]
on = sum(((p1 * p2 - s1 * s2) ** 2 + (p1 * s2 + s1 * p2) ** 2 == den ** 4) for p1, s1 in pairs for p2, s2 in pairs)
print(f"   den {den}: {len(pairs)} whole pairs on its circle; the products of every two lie on den^2's circle: {on} of {len(pairs) ** 2}")
import math  # noqa: E402

p1, s1 = pairs[3]
p2, s2 = pairs[7]
w = lambda p, s, d: math.atan2(s, p)  # noqa: E731
print(f"   e.g. ({p1}, {s1}) x ({p2}, {s2}) = ({p1 * p2 - s1 * s2}, {p1 * s2 + s1 * p2}) on den^2's circle: its turn per tick "
      f"{w(p1 * p2 - s1 * s2, p1 * s2 + s1 * p2, den * den):.12f} = {w(p1, s1, den):.12f} + {w(p2, s2, den):.12f} (a reading)")
DEN, GAMMA, G = 15162856759112389, 1000, 16
T_part = 6 * DEN * GAMMA**2 * G**2
T_comp = 6 * DEN**2 * GAMMA**2 * G**2
print(f"   the example universe: den {DEN.bit_length()} bits, den^2 {(DEN**2).bit_length()} bits; a train's T = 6 den Gamma^2 G^2 "
      f"{T_part.bit_length()} bits; a composite at rim den^2, T = 6 den^2 Gamma^2 G^2, {T_comp.bit_length()} bits, past the width 128")

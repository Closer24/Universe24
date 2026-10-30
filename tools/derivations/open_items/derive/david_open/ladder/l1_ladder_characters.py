"""The ladder of kinds from the 24's characters, read against 7a's own 125 tables (exact integers and fractions).

usage: python -I l1_ladder_characters.py <tensor24 src>
1. The 24 and their five kinds from 7a's kinds module (no table typed): the classes, the characters, their orthonormality.
2. Every product i x k split into kinds by the characters; every multiplicity 0 or 1; the count of the triples.
3. The ladder from A1 and its gradient: T1, then T1 x T1, then T1 x T2; the symmetric and antisymmetric squares and the
   symmetric cube of T1 (one train's gradient read twice and thrice), by chi(g^2) and chi(g^3).
4. The 7a tables (main.made): nonzero exactly where the multiplicity is 1; the space of intertwiners spanned by all the
   projector's seeds of the dimension of the multiplicity; each nonzero table of full rank dim m; each turning as its kind
   under the 24, C(rho_i u, rho_k v) = rho_m C(u, v), on random whole u and v.
"""

import sys
from fractions import Fraction
from itertools import product

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24 import main  # noqa: E402
from tensor24.engine import kinds as K  # noqa: E402

NAMES = ("A1", "A2", "E", "T1", "T2")


def rank(rows):
    """Exact rank of a list of integer vectors, by fraction Gaussian elimination."""
    m = [[Fraction(int(x)) for x in r] for r in rows if any(int(x) for x in r)]
    if not m:
        return 0
    rk, cols = 0, len(m[0])
    for c in range(cols):
        piv = next((i for i in range(rk, len(m)) if m[i][c] != 0), None)
        if piv is None:
            continue
        m[rk], m[piv] = m[piv], m[rk]
        for i in range(len(m)):
            if i != rk and m[i][c] != 0:
                f = m[i][c] / m[rk][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[rk], strict=True)]
        rk += 1
    return rk


matrix, weight = K.turns(K.axes(3))
held = K.kinds(matrix)
turn = [g for g in range(len(weight)) if weight[g] == 1]
print(f"1. The 24: {len(turn)} of the {len(weight)} matrices whose rows are three Spokes carry the weight 1 (det 1).")
rho = {n: [np.asarray(getattr(held, n.lower())[g], dtype=object) for g in turn] for n in NAMES}
t1 = rho["T1"]


def index_of(m):
    return next(j for j, x in enumerate(t1) if np.array_equal(x, m))


inv = [index_of(x.T) for x in t1]
mul = [[index_of(t1[a].dot(t1[b])) for b in range(24)] for a in range(24)]
classes, seen = [], set()
for g in range(24):
    if g in seen:
        continue
    cl = sorted({mul[mul[x][g]][inv[x]] for x in range(24)})
    seen |= set(cl)
    classes.append(cl)
order = lambda g: next(n for n in range(1, 25) if np.array_equal(np.linalg.matrix_power(t1[g].astype(int), n), np.eye(3, dtype=int)))  # noqa: E731
classes.sort(key=lambda cl: (order(cl[0]), len(cl)))
chi = {n: [int(np.trace(rho[n][g])) for g in range(24)] for n in NAMES}
print("   the classes (order of the turn, size) and the characters, each the trace of the kind's whole matrix:")
print("   " + " ".join(f"{'(' + str(order(cl[0])) + ',' + str(len(cl)) + ')':>8}" for cl in classes))
for n in NAMES:
    print(f"   {n:>2}: " + " ".join(f"{chi[n][cl[0]]:>8}" for cl in classes))
ortho = all(sum(chi[a][g] * chi[b][g] for g in range(24)) == (24 if a == b else 0) for a in NAMES for b in NAMES)
print(f"   orthonormal over the 24 (SUM chi_a chi_b = 24 delta_ab, the characters real): {ortho}")
print(f"   dimensions 1 + 1 + 4 + 9 + 9 = {sum(chi[n][index_of(np.eye(3, dtype=object))] ** 2 for n in NAMES)}")


def mult(m, i, k):
    s = sum(chi[i][g] * chi[k][g] * chi[m][g] for g in range(24))
    assert s % 24 == 0
    return s // 24


print("\n2. Every product split by the characters, n(m; i, k) = SUM chi_i chi_k chi_m / 24:")
triples = 0
allowed = True
for i in NAMES:
    for k in NAMES:
        parts = [m for m in NAMES if mult(m, i, k)]
        allowed &= all(mult(m, i, k) in (0, 1) for m in NAMES)
        triples += len(parts)
        if NAMES.index(i) <= NAMES.index(k):
            print(f"   {i} x {k} = {' + '.join(parts)}")
print(f"   every multiplicity 0 or 1 (the 24 split every product of two kinds without repeat): {allowed}")
print(f"   the triples (i, k -> m) the 24 allow: {triples} of 125")


def chi_power(n, p):
    return [int(np.trace(np.linalg.matrix_power(rho[n][g].astype(int), p))) for g in range(24)]


def split(c):
    out = []
    for m in NAMES:
        s = sum(c[g] * chi[m][g] for g in range(24))
        assert s % 24 == 0
        out += [m] * (s // 24)
    return " + ".join(out)


c1, c2, c3 = chi["T1"], chi_power("T1", 2), chi_power("T1", 3)
sym2 = [(c1[g] ** 2 + c2[g]) // 2 for g in range(24)]
alt2 = [(c1[g] ** 2 - c2[g]) // 2 for g in range(24)]
sym3 = [(c1[g] ** 3 + 3 * c1[g] * c2[g] + 2 * c3[g]) // 6 for g in range(24)]
print("\n3. The ladder from A1 and its gradient:")
print("   step 1: an A1 train's centred differences along the three axes read as T1 (7a's readings)")
print(f"   step 2: T1 x T1 = {split([c1[g] ** 2 for g in range(24)])}; one train's gradient read twice is the")
print(f"           symmetric square, Sym^2 T1 = {split(sym2)}; two different T1 readings add Alt^2 T1 = {split(alt2)}")
print(f"   step 3: T1 x T2 = {split([chi['T1'][g] * chi['T2'][g] for g in range(24)])}; one train's gradient thrice,")
print(f"           Sym^3 T1 = {split(sym3)}")
levels = [{"A1"}, {"A1", "T1"}]
for _ in range(2):
    nxt = set(levels[-1])
    for i in levels[-1]:
        for k in levels[-1]:
            nxt |= {m for m in NAMES if mult(m, i, k)}
    levels.append(nxt)
for s, lv in enumerate(levels):
    print(f"   after step {s}: {sorted(lv, key=NAMES.index)}")
first = {n: next(s for s, lv in enumerate(levels) if n in lv) for n in NAMES}
print(f"   the step at which each kind first stands: {first}")
x, y, z = 3, 5, 7
xyz_ok = True
for g in range(24):
    v = t1[g].dot(np.array([x, y, z], dtype=object))
    xyz_ok &= v[0] * v[1] * v[2] == chi["A2"][g] * x * y * z
print(f"   the triple product of one gradient, dx a dy a dz a, turns as A2 under all 24 (rho_A2 the sign): {xyz_ok}")

print("\n4. 7a's tables (main.made on the board's axes), C[i, k -> m] of shape (dim m, dim i, dim k):")
_, tables = main.made((3, 3, 3))
inverse = K.kinds(K.inverse(matrix))
nonzero = sum(1 for t in tables.values() if np.asarray(t).any())
print(f"   tables {len(tables)}, nonzero {nonzero}")
exactly = True
span_ok = True
full = True
turns_ok = True
rng = np.random.default_rng(24)
lab = {n: j for j, n in enumerate(NAMES)}
for i, k, m in product(NAMES, NAMES, NAMES):
    t = np.asarray(tables[(lab[i], lab[k], lab[m])], dtype=object)
    nz = bool(t.any())
    exactly &= nz == (mult(m, i, k) == 1)
    seeds = K.projector(weight, getattr(held, m.lower()), getattr(inverse, i.lower()), getattr(inverse, k.lower()))
    dm, di, dk = t.shape
    seeds = np.asarray(seeds, dtype=object).reshape(dm * di * dk, -1).T
    span_ok &= rank(seeds.tolist()) == mult(m, i, k)
    if nz:
        full &= rank(t.reshape(dm, di * dk).tolist()) == dm
        for g in range(24):
            for _ in range(3):
                u = np.asarray(rng.integers(-9, 10, di), dtype=object)
                v = np.asarray(rng.integers(-9, 10, dk), dtype=object)
                lhs = np.einsum("xab,a,b->x", t, rho[i][g].dot(u), rho[k][g].dot(v))
                rhs = rho[m][g].dot(np.einsum("xab,a,b->x", t, u, v))
                turns_ok &= bool(np.array_equal(lhs, rhs))
print(f"   nonzero exactly where the characters give m in i x k: {exactly}")
print(f"   the seeds' span (the intertwiners) has the dimension of the multiplicity, 0 or 1, for all 125: {span_ok}")
print(f"   each nonzero table has rank dim m as a map from i x k: {full}")
print(f"   each nonzero table turns as its kind under all 24, C(rho_i u, rho_k v) = rho_m C(u, v), 3 pairs each: {turns_ok}")
for key in (("T1", "T1", "A1"), ("T1", "T1", "T1"), ("T1", "T2", "A2"), ("E", "E", "A2")):
    t = np.asarray(tables[tuple(lab[n] for n in key)], dtype=object)
    entries = [(tuple(int(q) for q in w), int(t[tuple(w)])) for w in np.argwhere(t)]
    print(f"   {key[0]} x {key[1]} -> {key[2]}: {len(entries)} entries, {entries}")

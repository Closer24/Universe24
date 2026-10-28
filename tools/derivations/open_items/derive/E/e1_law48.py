"""Draft E, probe e1: the big law on the 24's double cover, exactly.

  python3 -I e1_law48.py            the claims (must print 0 failures)
  python3 -I e1_law48.py mutants    the mutations (each must fail)

For each of the eight kinds of 2O (the 48: the 24 turns of the cube, each with its two signs) the probe computes,
from the group itself and with exact numbers only:
  - the full turn z on the kind (the phase reversal on the board): chi(z) / dim;
  - the Frobenius-Schur indicator nu = (1/48) SUM_g chi(g g): the symmetry of the kind's one A1 pairing;
  - the count of A1 in the symmetric and in the antisymmetric square;
  - the square of every half turn's two lifts.
The claim: nu = chi(z) / dim on all eight kinds, so the A1 (the clock) of two equal quanta lies in the antisymmetric
square exactly where the full turn is -1. Numbers are Fractions and pairs (a, b) = a + b r2 with r2 r2 = 2; no float.
Mutations: the 12 turns of the tetrahedron (2T), commuting lifts (O x Z2), and the sign flipped.
"""

from __future__ import annotations

import sys
from fractions import Fraction as Fr
from itertools import permutations, product

FAIL = []


def check(name, ok, count=None):
    tag = "ok" if ok else "FAILED"
    if not ok:
        FAIL.append(name)
    print(f"  [{tag}] {name}" + ("" if count is None else f": {count}"))


# ---- Q(r2): a + b r2 ----
def qa(x, y):
    return (x[0] + y[0], x[1] + y[1])


def qm(x, y):
    return (x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def qn(x):
    return (-x[0], -x[1])


Z0, Z1 = (Fr(0), Fr(0)), (Fr(1), Fr(0))
HALF, INV_R2 = (Fr(1, 2), Fr(0)), (Fr(0), Fr(1, 2))  # 1/2 and 1/r2 = r2/2


def qs(k, x):
    return (k * x[0], k * x[1])


# ---- quaternions with Q(r2) coordinates: (w, x, y, z) = w + x i + y j + z k ----
def hm(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q

    def s(*terms):
        out = Z0
        for sign, u, v in terms:
            t = qm(u, v)
            out = qa(out, t if sign > 0 else qn(t))
        return out

    return (
        s((1, a1, a2), (-1, b1, b2), (-1, c1, c2), (-1, d1, d2)),
        s((1, a1, b2), (1, b1, a2), (1, c1, d2), (-1, d1, c2)),
        s((1, a1, c2), (-1, b1, d2), (1, c1, a2), (1, d1, b2)),
        s((1, a1, d2), (1, b1, c2), (-1, c1, b2), (1, d1, a2)),
    )


def hconj(q):
    return (q[0], qn(q[1]), qn(q[2]), qn(q[3]))


def binary_octahedral():
    els = set()
    for k in range(4):
        for sg in (1, -1):
            q = [Z0] * 4
            q[k] = (Fr(sg), Fr(0))
            els.add(tuple(q))
    for sg in product((1, -1), repeat=4):
        els.add(tuple(qs(Fr(s), HALF) for s in sg))
    for a in range(4):
        for b in range(a + 1, 4):
            for sa, sb in product((1, -1), repeat=2):
                q = [Z0] * 4
                q[a], q[b] = qs(Fr(sa), INV_R2), qs(Fr(sb), INV_R2)
                els.add(tuple(q))
    return sorted(els)


def binary_tetrahedral():
    """The 24 Hurwitz units: the double cover of the tetrahedron's 12 turns."""
    return [q for q in binary_octahedral() if all(c[1] == 0 for c in q)]


def rotation(q):
    """The 3 x 3 matrix of v -> q v q*, its entries read as rationals (they are integers for 2O)."""
    cols = []
    for e in range(3):
        v = [Z0] * 4
        v[1 + e] = Z1
        w = hm(hm(q, tuple(v)), hconj(q))
        cols.append([w[1 + a] for a in range(3)])
    m = [[cols[b][a] for b in range(3)] for a in range(3)]
    for row in m:
        for x in row:
            assert x[1] == 0, "a rotation entry outside Q"
    return tuple(tuple(x[0] for x in row) for row in m)


def perm_of(r):
    """The permutation part of a signed permutation matrix: pi with r[pi(b)][b] != 0."""
    return tuple(next(a for a in range(3) if r[a][b] != 0) for b in range(3))


def sign_of(pi):
    s = 1
    for i in range(len(pi)):
        for j in range(i + 1, len(pi)):
            if pi[i] > pi[j]:
                s = -s
    return s


def fixed(pi):
    return sum(1 for i, p in enumerate(pi) if i == p)


def kinds_2o():
    """The eight kinds of 2O as character functions with values in Q(r2), each from its construction."""

    def tr(r):
        return (Fr(r[0][0] + r[1][1] + r[2][2]), Fr(0))

    def a2(r):
        return (Fr(sign_of(perm_of(r))), Fr(0))

    def e(r):
        return (Fr(fixed(perm_of(r)) - 1), Fr(0))

    def half_spin(q):
        return qs(Fr(2), q[0])

    return {
        "A1": (1, lambda q, r: Z1),
        "A2": (1, lambda q, r: a2(r)),
        "E": (2, lambda q, r: e(r)),
        "T1": (3, lambda q, r: tr(r)),
        "T2": (3, lambda q, r: qm(tr(r), a2(r))),
        "E1/2": (2, lambda q, r: half_spin(q)),
        "E5/2": (2, lambda q, r: qm(half_spin(q), a2(r))),
        "G3/2": (4, lambda q, r: qm(half_spin(q), e(r))),
    }


def main_claims():
    G = binary_octahedral()
    print("1. The group of the 48: 48 unit quaternions with coordinates in Q(r2), closed, z = -1 central")
    check("order", len(G) == 48, len(G))
    S = set(G)
    closed = all(hm(p, q) in S for p in G for q in G)
    check("closed under the product (48 x 48 products)", closed, 48 * 48)
    z = ((Fr(-1), Fr(0)), Z0, Z0, Z0)
    check("the full turn z = -1 is in the group and central", z in S and all(hm(z, q) == hm(q, z) for q in G))
    rots = {q: rotation(q) for q in G}
    image = set(rots.values())
    signed = all(
        sorted(abs(x) for row in r for x in row) == [0] * 6 + [1] * 3 and det3(r) == 1 for r in image
    )
    check("the image is the 24 signed permutation matrices of determinant 1 (each met twice)", len(image) == 24 and signed, len(image))
    check("q and -q give the same turn", all(rots[q] == rots[hm(z, q)] for q in G), 48)

    print("2. The eight kinds: irreducible, orthogonal, and complete (1+1+4+9+9+4+4+16 = 48)")
    K = kinds_2o()
    chars = {name: [f(q, rots[q]) for q in G] for name, (dim, f) in K.items()}
    for name, vals in chars.items():
        ip = sum_q(qm(v, v) for v in vals)
        check(f"{name}: (1/48) SUM chi chi = 1", ip == (Fr(48), Fr(0)), f"SUM = {fmt(ip)} over 48")
    names = list(chars)
    ortho = all(
        sum_q(qm(a, b) for a, b in zip(chars[x], chars[y], strict=True)) == Z0
        for i, x in enumerate(names)
        for y in names[i + 1 :]
    )
    check("distinct kinds orthogonal (28 pairs)", ortho, 28)
    check("SUM dim^2 = 48", sum(d * d for d, _f in K.values()) == 48)

    print("3. The big law: the Frobenius-Schur indicator equals the full turn's sign on every kind")
    idx = {q: i for i, q in enumerate(G)}
    for name, (dim, f) in K.items():
        vals = chars[name]
        nu = sum_q(vals[idx[hm(q, q)]] for q in G)
        nu = (nu[0] / 48, nu[1] / 48)
        zsign = vals[idx[z]]
        zsign = (zsign[0] / dim, zsign[1] / dim)
        sym = sum_q(qa(qm(v, v), vals[idx[hm(q, q)]]) for v, q in zip(vals, G, strict=True))
        alt = sum_q(qa(qm(v, v), qn(vals[idx[hm(q, q)]])) for v, q in zip(vals, G, strict=True))
        a1_sym, a1_alt = sym[0] / 96, alt[0] / 96
        check(
            f"{name}: nu = {fmt(nu)}, chi(z)/dim = {fmt(zsign)}, A1 in Sym^2: {a1_sym}, A1 in Alt^2: {a1_alt}",
            nu == zsign and sym[1] == 0 and alt[1] == 0 and (a1_sym, a1_alt) == ((1, 0) if nu == Z1 else (0, 1)),
        )

    print("4. The half turns: every lift squares to the full turn; the face lifts anticommute; their turns commute")
    halves = [q for q in G if is_half_turn(rots[q])]
    check("the half turns' lifts: 9 half turns, 18 lifts", len(halves) == 18, len(halves))
    check("every half turn's lift squared is z (= -1)", all(hm(q, q) == z for q in halves), 18)
    I = ((Fr(1), Fr(0)), Z0, Z0, Z0)
    face = [q for q in halves if rots[q] in diag_half_turns()]
    anti = all(hm(p, q) == hm(z, hm(q, p)) for p in face for q in face if p != q and p != hm(z, q))
    comm = all(matmul3(rots[p], rots[q]) == matmul3(rots[q], rots[p]) for p in face for q in face)
    check("the face half turns' lifts anticommute (i j = -j i ...), 24 ordered pairs", anti and len(face) == 6)
    check("the face half turns commute as turns of the cube", comm)
    check("on the 24's kinds a half turn squared is the identity (the turn matrix squared)", all(matmul3(rots[q], rots[q]) == rots[I] for q in halves))
    return G, rots, chars, idx


def det3(r):
    return (
        r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1])
        - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
        + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0])
    )


def matmul3(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def is_half_turn(r):
    ident = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    return r != ident and matmul3(r, r) == ident


def diag_half_turns():
    return {
        ((1, 0, 0), (0, -1, 0), (0, 0, -1)),
        ((-1, 0, 0), (0, 1, 0), (0, 0, -1)),
        ((-1, 0, 0), (0, -1, 0), (0, 0, 1)),
    }


def sum_q(it):
    out = Z0
    for v in it:
        out = qa(out, v)
    return out


def fmt(x):
    return str(x[0]) if x[1] == 0 else f"{x[0]} + {x[1]} r2"


# ---- Q(w), w = exp(2 pi i / 3): (a, b) = a + b w, w w = -1 - w ----
def wa(x, y):
    return (x[0] + y[0], x[1] + y[1])


def wm(x, y):
    a, b = x
    c, d = y
    return (a * c - b * d, a * d + b * c - b * d)


def wconj(x):
    return (x[0] - x[1], -x[1])


def wpow(k):
    out = (Fr(1), Fr(0))
    for _ in range(k % 3):
        out = wm(out, (Fr(0), Fr(1)))
    return out


def mutant_tetrahedral():
    """2T: the law fails on the complex kinds (nu = 0 while chi(z)/dim = +1 or -1)."""
    G = binary_tetrahedral()
    rots = {q: rotation(q) for q in G}
    ident = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    v4 = {ident} | diag_half_turns()
    a = next(q for q in G if q[0] == HALF and q[1] == HALF and q[2] == HALF and q[3] == HALF)
    ra = rots[a]
    cosets = [v4, {matmul3(ra, v) for v in v4}, {matmul3(matmul3(ra, ra), v) for v in v4}]

    def k_of(q):
        return next(m for m, c in enumerate(cosets) if rots[q] in c)

    def two(q):
        return (2 * q[0][0], Fr(0))

    kinds = {
        "1": (1, lambda q: (Fr(1), Fr(0))),
        "1'": (1, lambda q: wpow(k_of(q))),
        "1''": (1, lambda q: wpow(2 * k_of(q))),
        "3": (3, lambda q: (Fr(sum(rots[q][i][i] for i in range(3))), Fr(0))),
        "2": (2, two),
        "2'": (2, lambda q: wm(two(q), wpow(k_of(q)))),
        "2''": (2, lambda q: wm(two(q), wpow(2 * k_of(q)))),
    }
    z = ((Fr(-1), Fr(0)), Z0, Z0, Z0)
    fails = 0
    for name, (dim, f) in kinds.items():
        ip = (Fr(0), Fr(0))
        nu = (Fr(0), Fr(0))
        for q in G:
            ip = wa(ip, wm(f(q), wconj(f(q))))
            nu = wa(nu, f(hm(q, q)))
        nu = (nu[0] / 24, nu[1] / 24)
        zs = f(z)
        zs = (zs[0] / dim, zs[1] / dim)
        good = nu == zs
        fails += 0 if good else 1
        print(f"    2T kind {name}: irreducible {ip == (Fr(24), Fr(0))}, nu = {nu[0]}{'' if nu[1] == 0 else ' + ' + str(nu[1]) + ' w'}, chi(z)/dim = {zs[0]}: {'holds' if good else 'FAILS'}")
    return fails


def mutant_commuting(chars_o, G, rots):
    """O x Z2: the full turn (I, -1) is central, the lifts commute, and the law fails on every odd kind."""
    by_rot = {}
    for q in G:
        by_rot.setdefault(rots[q], q)
    reps = list(by_rot.items())  # 24 turns, one quaternion each to read the O characters
    idx = {q: i for i, q in enumerate(G)}
    fails = 0
    for name in ("A1", "A2", "E", "T1", "T2"):
        vals = chars_o[name]
        nu_num = Fr(0)
        for r, q in reps:
            r2 = matmul3(r, r)
            q2 = by_rot[r2]
            for s in (1, -1):
                nu_num += vals[idx[q2]][0] * 1  # chi_V(r r) chi_sgn(s s) = chi_V(r r)
        nu = nu_num / 48
        zsign = Fr(-1)  # chi_{V x sgn}((I, -1)) / dim = -1 for every V
        good = nu == zsign
        fails += 0 if good else 1
        print(f"    O x Z2, kind {name} x sgn: nu = {nu}, chi(z)/dim = {zsign}: {'holds' if good else 'FAILS'}")
    return fails


def mutants():
    G = binary_octahedral()
    rots = {q: rotation(q) for q in G}
    K = kinds_2o()
    chars = {name: [f(q, rots[q]) for q in G] for name, (dim, f) in K.items()}
    idx = {q: i for i, q in enumerate(G)}
    print("M1. The 12 turns of the tetrahedron (2T) in place of the 24: the law must fail")
    f1 = mutant_tetrahedral()
    print(f"  kinds where nu != chi(z)/dim: {f1} of 7 (must be above 0)")
    print("M2. Commuting lifts (O x Z2, the full turn central but no half turn's lift of order 4): the law must fail")
    f2 = mutant_commuting(chars, G, rots)
    print(f"  odd kinds where nu != chi(z)/dim: {f2} of 5 (must be above 0)")
    print("M3. The sign flipped (nu compared with -chi(z)/dim): the law must fail")
    z = ((Fr(-1), Fr(0)), Z0, Z0, Z0)
    f3 = 0
    for name, (dim, f) in K.items():
        vals = chars[name]
        nu = sum_q(vals[idx[hm(q, q)]] for q in G)
        zs = vals[idx[z]]
        f3 += 0 if (nu[0] / 48, nu[1] / 48) == (-zs[0] / dim, -zs[1] / dim) else 1
    print(f"  kinds where nu != -chi(z)/dim: {f3} of 8 (must be above 0)")
    bad = [n for n, f in (("M1", f1), ("M2", f2), ("M3", f3)) if f == 0]
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main_claims()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)

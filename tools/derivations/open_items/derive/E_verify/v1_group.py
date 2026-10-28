"""Verifier of draft E, probe v1: the 48 rebuilt by another road, its kinds found from the group, the three signs read.

  python3 -I v1_group.py            the claims (prints its counts; must end with 0 failures)
  python3 -I v1_group.py mutants    the mutations (each must fail)

Independent of the draft's e1: the group is closed from two generators (the lifts of a quarter turn about z and of a
third turn about (1,1,1)) as 2 x 2 matrices over Q(zeta24), not listed as quaternions; the character table is found
from the group alone (the abelianization's linear characters and the products of the defining character, split by
inner products), not from named constructions; the three signs are read on explicit matrices of every kind:
  z      the matrix of the full turn -1,
  nu     (1/|G|) SUM chi(g g),
  B      the symmetry of the solved invariant bilinear form, rho(g)^T B rho(g) = B,
  JJ     the sign of X conj(X) for the solved antiunitary intertwiner, X conj(rho(g)) = rho(g) X.
Then the subgroups: 2T (the tetrahedron's 24 lifts), Q8 (the 8 lifts of the three face half turns), the 16 lifts of
D4, the 12 lifts of D3, and cyclic ones. Exact rationals only; the one real sign is decided by integer bounds.
"""

from __future__ import annotations

import sys
from fractions import Fraction as Fr
from math import isqrt

FAIL = []


def check(name, ok, info=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if info is None else f": {info}"))


# ---------------- Q(zeta24): a = SUM_k a[k] x^k (k < 8), x = zeta24, x^8 = x^4 - 1 ----------------
Z0 = (Fr(0),) * 8
E1 = (Fr(1),) + (Fr(0),) * 7


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def sc(q, a):
    return tuple(q * x for x in a)


def mul(a, b):
    p = [Fr(0)] * 15
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    p[i + j] += x * y
    for k in range(14, 7, -1):
        c = p[k]
        if c:
            p[k] = Fr(0)
            p[k - 4] += c
            p[k - 8] -= c
    return tuple(p[:8])


_XP = {}


def xp(k):
    k %= 24
    if k not in _XP:
        v, x = E1, (Fr(0), Fr(1)) + (Fr(0),) * 6
        for _ in range(k):
            v = mul(v, x)
        _XP[k] = v
    return _XP[k]


def conj(a):
    out = Z0
    for k, c in enumerate(a):
        if c:
            out = add(out, sc(c, xp(-k)))
    return out


def galois(a, k):
    out = Z0
    for j, c in enumerate(a):
        if c:
            out = add(out, sc(c, xp(j * k)))
    return out


def rat(q):
    return (Fr(q),) + (Fr(0),) * 7


I_ = xp(6)
OM = xp(8)  # omega, a cube root of 1
Z8 = xp(3)  # zeta8


def solve_q(A, b):
    """Solve A y = b over Q (A square, invertible)."""
    n = len(A)
    m = [list(A[r]) + [b[r]] for r in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        iv = 1 / m[c][c]
        m[c] = [x * iv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[r][n] for r in range(n)]


def inv(a):
    cols = [mul(a, xp(j)) for j in range(8)]
    A = [[cols[j][r] for j in range(8)] for r in range(8)]
    return tuple(solve_q(A, list(E1)))


# the embedding x -> exp(2 pi i / 24): real and imaginary parts in the basis (1, r2, r3, r6), exact
# cos(k pi / 12) for k = 0..23, as coefficient 4-vectors over (1, r2, r3, r6)
_C = {
    0: (1, 0, 0, 0), 1: (0, Fr(1, 4), 0, Fr(1, 4)), 2: (0, 0, Fr(1, 2), 0), 3: (0, Fr(1, 2), 0, 0),
    4: (Fr(1, 2), 0, 0, 0), 5: (0, Fr(-1, 4), 0, Fr(1, 4)), 6: (0, 0, 0, 0),
}


def cosv(k):
    k %= 24
    if k <= 6:
        return tuple(Fr(c) for c in _C[k])
    if k <= 12:
        return tuple(-x for x in cosv(12 - k))
    return cosv(24 - k)


def sinv(k):
    return cosv(6 - k)


def real_part(a):
    out = [Fr(0)] * 4
    for k, c in enumerate(a):
        for t in range(4):
            out[t] += c * cosv(k)[t]
    return tuple(out)


def imag_part(a):
    out = [Fr(0)] * 4
    for k, c in enumerate(a):
        for t in range(4):
            out[t] += c * sinv(k)[t]
    return tuple(out)


def sign_real(v):
    """The sign of v0 + v1 r2 + v2 r3 + v3 r6, decided by integer bounds on the roots (no float)."""
    for digits in (20, 60, 200):
        S = 10 ** digits
        lo = [S, isqrt(2 * S * S), isqrt(3 * S * S), isqrt(6 * S * S)]
        hi = [S, lo[1] + 1, lo[2] + 1, lo[3] + 1]
        low = high = Fr(0)
        for c, l, h in zip(v, lo, hi):
            low += c * (l if c >= 0 else h)
            high += c * (h if c >= 0 else l)
        if low > 0:
            return 1
        if high < 0:
            return -1
        if v == (0, 0, 0, 0):
            return 0
    return 0


# ---------------- matrices over the field ----------------
def mm(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return tuple(tuple(_dot([A[i][t] for t in range(k)], [B[t][j] for t in range(k)]) for j in range(m)) for i in range(n))


def _dot(u, v):
    out = Z0
    for x, y in zip(u, v):
        if any(x) and any(y):
            out = add(out, mul(x, y))
    return out


def mT(A):
    return tuple(tuple(A[j][i] for j in range(len(A))) for i in range(len(A[0])))


def mconj(A):
    return tuple(tuple(conj(x) for x in row) for row in A)


def mdag(A):
    return mT(mconj(A))


def ident(n):
    return tuple(tuple(E1 if i == j else Z0 for j in range(n)) for i in range(n))


def msc(c, A):
    return tuple(tuple(mul(c, x) for x in row) for row in A)


def tr(A):
    out = Z0
    for i in range(len(A)):
        out = add(out, A[i][i])
    return out


def closure(gens):
    n = len(gens[0])
    e = ident(n)
    els, front = {e}, [e]
    while front:
        new = []
        for g in front:
            for s in gens:
                h = mm(g, s)
                if h not in els:
                    els.add(h)
                    new.append(h)
        front = new
    return sorted(els)


def classes_of(G):
    inv_of = {g: mdag(g) for g in G}
    seen, cls = set(), []
    for g in G:
        if g in seen:
            continue
        c = sorted({mm(mm(h, g), inv_of[h]) for h in G})
        seen |= set(c)
        cls.append(c)
    return cls


# ---------------- the 48 ----------------
QA = ((xp(21), Z0), (Z0, xp(3)))  # diag(zeta8^-1, zeta8): the lift of the quarter turn about z
HALF = Fr(1, 2)
QB = (
    (sc(HALF, sub(E1, I_)), sc(HALF, neg(add(E1, I_)))),
    (sc(HALF, sub(E1, I_)), sc(HALF, add(E1, I_))),
)  # (1 - i (sx + sy + sz)) / 2: the lift of the third turn about (1, 1, 1)
SX = ((Z0, E1), (E1, Z0))
SY = ((Z0, neg(I_)), (I_, Z0))
SZ = ((E1, Z0), (Z0, neg(E1)))
PAULI = (SX, SY, SZ)
MINUS = msc(rat(-1), ident(2))


def rotation(U):
    """R_ab = (1/2) tr(s_a U s_b U^dagger): must be rational."""
    Ud = mdag(U)
    R = []
    for a in range(3):
        row = []
        for b in range(3):
            t = tr(mm(mm(PAULI[a], U), mm(PAULI[b], Ud)))
            t = sc(HALF, t)
            assert all(x == 0 for x in t[1:]), "a rotation entry outside Q"
            row.append(t[0])
        R.append(tuple(row))
    return tuple(R)


def det3(r):
    return (
        r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1])
        - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
        + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0])
    )


# ---------------- characters from the group alone ----------------
class Table:
    def __init__(self, G):
        self.G = G
        self.n = len(G)
        self.cls = classes_of(G)
        self.ci = {}
        for k, c in enumerate(self.cls):
            for g in c:
                self.ci[g] = k
        self.sizes = [len(c) for c in self.cls]
        self.sq = [self.ci[mm(c[0], c[0])] for c in self.cls]
        self.invc = [self.ci[mdag(c[0])] for c in self.cls]
        self.zc = self.ci[MINUS] if MINUS in self.ci else None

    def ip(self, a, b):
        out = Z0
        for k, s in enumerate(self.sizes):
            out = add(out, sc(Fr(s), mul(a[k], conj(b[k]))))
        return sc(Fr(1, self.n), out)

    def nu(self, ch):
        out = Z0
        for k, s in enumerate(self.sizes):
            out = add(out, sc(Fr(s), ch[self.sq[k]]))
        return sc(Fr(1, self.n), out)

    def linear(self):
        """The linear characters, from the abelianization G / [G, G]."""
        G = self.G
        comm = closure(sorted({mm(mm(g, h), mm(mdag(g), mdag(h))) for g in G for h in G}))
        cs = set(comm)
        coset = {}
        reps = []
        for g in G:
            if g in coset:
                continue
            c = frozenset(mm(g, k) for k in cs)
            for h in c:
                coset[h] = len(reps)
            reps.append(g)
        m = len(reps)
        # a generating set of the quotient, greedy
        def gen_closure(gs):
            got = {coset[ident(len(G[0]))]}
            front = list(got)
            while front:
                new = []
                for a in front:
                    for s in gs:
                        b = coset[mm(reps[a], s)]
                        if b not in got:
                            got.add(b)
                            new.append(b)
                front = new
            return got

        gens = []
        while len(gen_closure(gens)) < m:
            for g in reps:
                if coset[g] not in gen_closure(gens):
                    gens.append(g)
                    break
        chars = []
        from itertools import product as prod_

        for ks in prod_(range(24), repeat=len(gens)):
            val = {coset[ident(len(G[0]))]: 0}
            front = [coset[ident(len(G[0]))]]
            ok = True
            while front and ok:
                new = []
                for a in front:
                    for s, k in zip(gens, ks):
                        b = coset[mm(reps[a], s)]
                        v = (val[a] + k) % 24
                        if b in val:
                            if val[b] != v:
                                ok = False
                                break
                        else:
                            val[b] = v
                            new.append(b)
                    if not ok:
                        break
                front = new
            if ok:
                # homomorphism check on all pairs of cosets
                for a in range(m):
                    for b in range(m):
                        if (val[a] + val[b]) % 24 != val[coset[mm(reps[a], reps[b])]]:
                            ok = False
                            break
                    if not ok:
                        break
            if ok:
                ch = tuple(xp(val[coset[c[0]]]) for c in self.cls)
                if ch not in chars:
                    chars.append(ch)
        return chars

    def irreducibles(self, defining):
        """Split products of the defining character with known kinds until SUM dim^2 = |G|."""
        known = list(self.linear())
        pool = [defining]
        tried = 0
        while sum(int(c[self.ci[ident(len(self.G[0]))]][0]) ** 2 for c in known) < self.n and tried < 400:
            tried += 1
            fresh = []
            for a in [defining] + list(known):
                for b in list(known) + [defining]:
                    fresh.append(tuple(mul(x, y) for x, y in zip(a, b)))
            for ch in pool + fresh:
                rem = ch
                for k in known:
                    c = self.ip(rem, k)
                    rem = tuple(sub(x, mul(c, y)) for x, y in zip(rem, k))
                if self.ip(rem, rem) == E1:
                    dim = rem[self.ci[ident(len(self.G[0]))]]
                    if dim[0] > 0 and all(x == 0 for x in dim[1:]) and rem not in known:
                        known.append(rem)
            pool = []
        return known


def describe(t, ch):
    one = t.ci[ident(len(t.G[0]))]
    dim = ch[one][0]
    nu = t.nu(ch)
    z = sc(1 / dim, ch[t.zc]) if t.zc is not None else None
    return dim, nu, z


def fmt(a):
    if all(x == 0 for x in a[1:]):
        return str(a[0])
    return "(" + " + ".join(f"{c} x^{k}" for k, c in enumerate(a) if c) + ")"


# ---------------- explicit matrices of the eight kinds of 2O ----------------
DIAG = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]


def perm_sign(p):
    s = 1
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                s = -s
    return s


def a2_of(R):
    """The sign of the permutation of the four body diagonals (an independent road to A2)."""
    img = []
    for d in DIAG:
        v = tuple(sum(R[i][j] * d[j] for j in range(3)) for i in range(3))
        k = next(k for k, e in enumerate(DIAG) if e == v or e == tuple(-x for x in v))
        img.append(k)
    return perm_sign(img)


def e_of(R):
    """The permutation of the three axes on the sum-zero plane, basis f1 = e0 - e1, f2 = e1 - e2."""
    p = [next(a for a in range(3) if R[a][b] != 0) for b in range(3)]

    def img(v):
        w = [Fr(0)] * 3
        for b in range(3):
            w[p[b]] += v[b]
        return w

    cols = []
    for f in ((1, -1, 0), (0, 1, -1)):
        w = img(f)
        cols.append((w[0], -w[2]))
    return tuple(tuple(rat(cols[c][r]) for c in range(2)) for r in range(2))


def sym3(U):
    """The action on cubics in (e1, e2), monomial basis e1^3, e1^2 e2, e1 e2^2, e2^3."""
    u1 = (U[0][0], U[1][0])  # U e1 = U00 e1 + U10 e2
    u2 = (U[0][1], U[1][1])

    def pmul(p, q):
        out = [Z0] * (len(p) + len(q) - 1)
        for i, x in enumerate(p):
            for j, y in enumerate(q):
                out[i + j] = add(out[i + j], mul(x, y))
        return out

    cols = []
    for a in range(3, -1, -1):
        b = 3 - a
        p = [E1]
        for _ in range(a):
            p = pmul(p, list(u1))
        for _ in range(b):
            p = pmul(p, list(u2))
        cols.append(p)  # coefficients of e1^(3-k) e2^k, k = 0..3
    return tuple(tuple(cols[c][r] for c in range(4)) for r in range(4))


def kinds_explicit(G):
    rots = {g: rotation(g) for g in G}
    out = {}
    out["A1"] = {g: ((E1,),) for g in G}
    out["A2"] = {g: ((rat(a2_of(rots[g])),),) for g in G}
    out["E"] = {g: e_of(rots[g]) for g in G}
    out["T1"] = {g: tuple(tuple(rat(x) for x in row) for row in rots[g]) for g in G}
    out["T2"] = {g: msc(rat(a2_of(rots[g])), out["T1"][g]) for g in G}
    out["E1/2"] = {g: g for g in G}
    out["E5/2"] = {g: msc(rat(a2_of(rots[g])), g) for g in G}
    out["G3/2"] = {g: sym3(g) for g in G}
    return out, rots


def nullspace_field(rows, nunk):
    """Nullspace over Q(zeta24) of a list of equations (each a list of nunk field coefficients)."""
    m = [list(r) for r in rows]
    piv = []
    r = 0
    for c in range(nunk):
        p = next((i for i in range(r, len(m)) if any(m[i][c])), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        iv = inv(m[r][c])
        m[r] = [mul(iv, x) for x in m[r]]
        for i in range(len(m)):
            if i != r and any(m[i][c]):
                f = m[i][c]
                m[i] = [sub(x, mul(f, y)) for x, y in zip(m[i], m[r])]
        piv.append(c)
        r += 1
    free = [c for c in range(nunk) if c not in piv]
    basis = []
    for fc in free:
        v = [Z0] * nunk
        v[fc] = E1
        for i, pc in enumerate(piv):
            v[pc] = neg(m[i][fc])
        basis.append(v)
    return basis


def invariant_forms(rep, gens, n):
    rows = []
    for s in gens:
        M = rep[s]
        for r in range(n):
            for c in range(n):
                eq = [Z0] * (n * n)
                for k in range(n):
                    for l in range(n):
                        eq[k * n + l] = add(eq[k * n + l], mul(M[k][r], M[l][c]))
                eq[r * n + c] = sub(eq[r * n + c], E1)
                rows.append(eq)
    return [tuple(tuple(v[i * n + j] for j in range(n)) for i in range(n)) for v in nullspace_field(rows, n * n)]


def antiunitary_intertwiners(rep, gens, n):
    rows = []
    for s in gens:
        M = rep[s]
        Mc = mconj(M)
        for r in range(n):
            for c in range(n):
                eq = [Z0] * (n * n)
                for k in range(n):
                    eq[r * n + k] = add(eq[r * n + k], Mc[k][c])  # X[r][k] conj(M)[k][c]
                    eq[k * n + c] = sub(eq[k * n + c], M[r][k])  # - M[r][k] X[k][c]
                rows.append(eq)
    return [tuple(tuple(v[i * n + j] for j in range(n)) for i in range(n)) for v in nullspace_field(rows, n * n)]


def jj_sign(X):
    P = mm(X, mconj(X))
    n = len(P)
    scalar = all(P[i][j] == (P[0][0] if i == j else Z0) for i in range(n) for j in range(n))
    if not scalar:
        return None
    c = P[0][0]
    im = imag_part(c)
    if sign_real(im) != 0:
        return None
    return sign_real(real_part(c))


def main():
    print("1. The group, closed from two generators (no listing): order, centre, image in the rotations")
    G = closure([QA, QB])
    check("order 48", len(G) == 48, len(G))
    S = set(G)
    check("closed: 48 x 48 products in the set", all(mm(a, b) in S for a in G for b in G))
    check("-1 in the group and central", MINUS in S and all(mm(MINUS, g) == mm(g, MINUS) for g in G))
    check("every element unitary of determinant 1", all(mm(g, mdag(g)) == ident(2) and sub(mul(g[0][0], g[1][1]), mul(g[0][1], g[1][0])) == E1 for g in G))
    rots = {g: rotation(g) for g in G}
    image = set(rots.values())
    signed = all(sorted(abs(x) for row in r for x in row) == [0] * 6 + [1] * 3 and det3(r) == 1 for r in image)
    check("the image is the 24 signed permutation matrices of determinant 1, each met by g and -g", len(image) == 24 and signed and all(rots[g] == rots[mm(MINUS, g)] for g in G), len(image))
    ent = set()
    for g in G:
        for row in g:
            for x in row:
                ent.add(x)
    in_z8 = all(galois(x, 17) == x for x in ent)  # x -> x^17 fixes zeta8 = x^3 and moves omega = x^8
    integral = all(all(c.denominator == 1 for c in x) for x in ent)
    check("entries lie in Q(zeta8): fixed by the Galois map x -> x^17", in_z8 and galois(OM, 17) != OM and galois(Z8, 17) == Z8)
    print(f"  entries all algebraic integers in this basis: {integral} (the quarter turns' 1/r2 is not in Z[zeta8])")

    print("2. The character table found from the group alone")
    t = Table(G)
    check("8 classes", len(t.cls) == 8, [len(c) for c in t.cls])
    real_cls = sum(1 for k in range(len(t.cls)) if t.invc[k] == k)
    check("every class is real (g ~ g^-1): every kind self-dual (Brauer)", real_cls == 8, f"{real_cls} of 8")
    chi_def = tuple(tr(c[0]) for c in t.cls)
    irr = t.irreducibles(chi_def)
    dims = sorted(int(describe(t, c)[0]) for c in irr)
    check("8 irreducible characters, dimensions 1 1 2 2 2 3 3 4, SUM dim^2 = 48", dims == [1, 1, 2, 2, 2, 3, 3, 4], dims)
    ortho = all(t.ip(a, b) == (E1 if i == j else Z0) for i, a in enumerate(irr) for j, b in enumerate(irr))
    check("orthonormal (64 inner products)", ortho)
    law = []
    for ch in irr:
        dim, nu, z = describe(t, ch)
        symA1 = sc(HALF, add(t.ip(tuple(mul(x, x) for x in ch), tuple(E1 for _ in ch)), nu))
        altA1 = sc(HALF, sub(t.ip(tuple(mul(x, x) for x in ch), tuple(E1 for _ in ch)), nu))
        law.append((dim, nu, z, symA1, altA1))
        print(f"    kind of dim {dim}: nu = {fmt(nu)}, chi(z)/dim = {fmt(z)}, A1 in Sym^2 = {fmt(symA1)}, in Alt^2 = {fmt(altA1)}")
    check("nu = chi(z)/dim on all eight kinds (from the table found here)", all(nu == z for _d, nu, z, _s, _a in law), f"{sum(nu == z for _d, nu, z, _s, _a in law)} of 8")
    check("the A1 of V x V lies in Sym^2 where nu = +1 and in Alt^2 where nu = -1, once", all((s, a) == ((E1, Z0) if nu == E1 else (Z0, E1)) for _d, nu, _z, s, a in law))
    count_minus = sum(1 for _d, nu, _z, _s, _a in law if nu == rat(-1))
    check("three kinds have nu = -1 (dims 2, 2, 4), five have +1", count_minus == 3 and sorted(int(d) for d, nu, *_ in law if nu == rat(-1)) == [2, 2, 4])

    print("3. The three signs on explicit matrices of every kind (A2 by the body diagonals, G3/2 as Sym^3)")
    reps, _r = kinds_explicit(G)
    gens = [QA, QB]
    agree = 0
    for name, rep in reps.items():
        n = len(rep[G[0]])
        hom = all(mm(rep[g], rep[s]) == rep[mm(g, s)] for g in G for s in gens)
        chi = tuple(tr(rep[c[0]]) for c in t.cls)
        irreducible = t.ip(chi, chi) == E1
        zmat = rep[MINUS]
        zs = 1 if zmat == ident(n) else (-1 if zmat == msc(rat(-1), ident(n)) else None)
        nu = t.nu(chi)
        forms = invariant_forms(rep, gens, n)
        bsym = None
        if len(forms) == 1:
            B = forms[0]
            if mT(B) == B:
                bsym = 1
            elif mT(B) == msc(rat(-1), B):
                bsym = -1
        Xs = antiunitary_intertwiners(rep, gens, n)
        js = jj_sign(Xs[0]) if len(Xs) == 1 else None
        ok = hom and irreducible and len(forms) == 1 and len(Xs) == 1 and zs is not None and nu == rat(zs) and bsym == zs and js == zs
        agree += ok
        print(f"    {name:5s} dim {n}: homomorphism {hom}, irreducible {irreducible}, z = {zs:+d}, nu = {fmt(nu)}, invariant forms {len(forms)} (symmetry {bsym}), antiunitary intertwiners {len(Xs)} (JJ sign {js})")
    check("z = nu = symmetry of the invariant form = sign of JJ, on every kind", agree == 8, f"{agree} of 8")
    print("3b. The standard proof by restriction: each kind occurs once in some spin j of SU(2), whose form is Sym^2j(det)")
    t_vals = [tr(c[0]) for c in t.cls]
    chis = [[E1 for _ in t.cls], list(t_vals)]
    for _two_j in range(2, 7):
        chis.append([sub(mul(tv, a), b) for tv, a, b in zip(t_vals, chis[-1], chis[-2])])
    once = 0
    for ch in irr:
        hits = [tj for tj in range(7) if t.ip(tuple(chis[tj]), ch) == E1]
        dim, nu, z = describe(t, ch)
        ok = bool(hits) and all(nu == rat((-1) ** tj) for tj in hits)
        once += ok
        print(f"    kind of dim {int(dim)} (nu {fmt(nu)}): multiplicity one in spin j = {[f'{tj}/2' for tj in hits]}, sign (-1)^2j = {[(-1) ** tj for tj in hits]}")
    check("every kind occurs once in some spin j <= 3 and its nu is (-1)^2j: the law on 2O by restriction", once == 8, f"{once} of 8")
    rep = reps["E1/2"]
    X = antiunitary_intertwiners(rep, gens, 2)[0]
    prop = X[0][0] == Z0 and X[1][1] == Z0 and X[1][0] == neg(X[0][1]) and any(X[0][1])  # X = c [[0, 1], [-1, 0]] = -c (-i sigma_y)
    check("on the twin hands the intertwiner is a multiple of -i sigma_y: T = (-i sigma_y) K up to a scalar", prop, [[fmt(x) for x in r] for r in X])
    return G, t, reps


# ---------------- subgroups ----------------
HZ = mm(QA, QA)  # diag(-i, i) = -i sigma_z, the lift of the half turn about z
HX = msc(neg(I_), SX)
HY = msc(neg(I_), SY)
L110 = ((Z0, xp(21)), (neg(xp(3)), Z0))  # -i (sx - sy)/r2: the lift of the half turn about (1, -1, 0)


def subgroup_report(name, gens, want_order):
    H = closure(gens)
    t = Table(H)
    chi_def = tuple(tr(c[0]) for c in t.cls)
    irr = t.irreducibles(chi_def)
    complete = sum(int(describe(t, c)[0]) ** 2 for c in irr) == len(H) and len(irr) == len(t.cls)
    real_cls = sum(1 for k in range(len(t.cls)) if t.invc[k] == k)
    strict = weak_ok = selfdual = 0
    rows = []
    for ch in irr:
        dim, nu, z = describe(t, ch)
        strict += nu == z
        if nu != Z0:
            selfdual += 1
            weak_ok += nu == z
        rows.append(f"{int(dim)}:{fmt(nu)}/{fmt(z)}")
    E12 = tuple(tr(c[0]) for c in t.cls)
    e12_irr = t.ip(E12, E12) == E1
    print(f"    {name}: order {len(H)} (want {want_order}), {len(t.cls)} classes, {real_cls} real; kinds (dim:nu/z) {' '.join(rows)}")
    print(f"      strict law nu = z on {strict} of {len(irr)} kinds; on the self-dual kinds {weak_ok} of {selfdual}; the twin hands irreducible here: {e12_irr}")
    return dict(order=len(H), complete=complete, strict=strict, n=len(irr), weak=weak_ok, sd=selfdual, real=real_cls, e12=e12_irr, H=H, t=t)


def twin_T_forced(H):
    rep = {g: g for g in H}
    gens = H  # all elements as equations: the commutant of the whole group
    Xs = antiunitary_intertwiners(rep, gens, 2)
    signs = [jj_sign(X) for X in Xs]
    return len(Xs), signs


def subgroups():
    print("4. The law on subgroups of the 48 (is it 'the cube's 24 and not less'?)")
    res = {}
    res["2T"] = subgroup_report("2T, the tetrahedron's 24 lifts", [QB, HZ], 24)
    res["Q8"] = subgroup_report("Q8, the 8 lifts of the three face half turns", [HZ, HX], 8)
    res["Dic4"] = subgroup_report("the 16 lifts of D4 (the z axis as a line)", [QA, HX], 16)
    res["Dic3"] = subgroup_report("the 12 lifts of D3 (the (1,1,1) axis as a line)", [QB, L110], 12)
    res["Z8"] = subgroup_report("Z8, the quarter turns' lifts about z", [QA], 8)
    res["Z6"] = subgroup_report("Z6, the third turns' lifts about (1,1,1)", [QB], 6)
    res["Z4"] = subgroup_report("Z4, the half turn's lifts about z", [HZ], 4)
    r = res["2T"]
    check("2T: the strict law fails on 4 of 7 kinds, as the draft says", r["complete"] and r["n"] == 7 and r["n"] - r["strict"] == 4)
    check("2T: those 4 are exactly its non-self-dual kinds (nu = 0, no A1 in V x V, no commuting antiunitary)", r["sd"] == 3 and r["real"] == 3)
    check("2T: on all 3 self-dual kinds the signs agree (the weak law holds)", r["weak"] == r["sd"] == 3)
    check("Q8: the strict law holds on 5 of 5 kinds: 8 lifts already carry the whole law", res["Q8"]["complete"] and res["Q8"]["strict"] == res["Q8"]["n"] == 5)
    check("the 16 lifts of D4: the strict law holds on 7 of 7", res["Dic4"]["complete"] and res["Dic4"]["strict"] == res["Dic4"]["n"] == 7)
    check("the 12 lifts of D3: strict fails only on its 2 complex kinds; weak holds", res["Dic3"]["complete"] and res["Dic3"]["n"] - res["Dic3"]["strict"] == 2 and res["Dic3"]["weak"] == res["Dic3"]["sd"])
    check("Z6: even the weak law fails (the real kind g -> -1 has z = -1 and nu = +1)", res["Z6"]["complete"] and res["Z6"]["weak"] < res["Z6"]["sd"])
    for key in ("2T", "Q8", "Dic3", "Dic4"):
        n, signs = twin_T_forced(res[key]["H"])
        check(f"{key}: on the twin hands the commuting phase reversal is forced (1 intertwiner) and squares to -1", n == 1 and signs == [-1], (n, signs))
    n, signs = twin_T_forced(res["Z8"]["H"])
    check("Z8 (abelian lifts): the phase reversal is not forced (intertwiners 2-dimensional over the field)", n == 2, (n, signs))
    return res


def mutants():
    bad = []

    def report(name, count, of):
        print(f"  {name}: {count} of {of} (must be above 0)")
        if count == 0:
            bad.append(name)

    G = closure([QA, QB])
    t = Table(G)
    irr = t.irreducibles(tuple(tr(c[0]) for c in t.cls))
    print("M1. The sign flipped: nu compared with -chi(z)/dim")
    report("kinds where nu != -chi(z)/dim", sum(1 for ch in irr if describe(t, ch)[1] != neg(describe(t, ch)[2])), 8)
    print("M2. Commuting lifts (O x Z2 built as the 24 rotation matrices with a sign): the odd kinds' nu = +1 against z = -1")
    rots = sorted({rotation(g) for g in G})
    O = [tuple(tuple(rat(x) for x in row) for row in r) for r in rots]
    OxZ2 = [(R, s) for R in O for s in (1, -1)]
    # the odd kinds V x sgn: chi(g g) = chi_V(R R) (s s = 1), z = (1, -1) acts as -1
    t1 = [tr(R) for R, _s in OxZ2]
    sq = [tr(mm(R, R)) for R, _s in OxZ2]
    nu_t1 = sc(Fr(1, 48), sum_f(sq))
    print(f"    T1 x sgn on O x Z2: nu = {fmt(nu_t1)}, chi(z)/dim = -1")
    report("the odd T1's mismatch (nu = +1 while z = -1)", int(nu_t1 == E1), 1)
    print("F1 (a finding, not a must-fail): the tetrahedron's 24 lifts only (2T). If Pauli needed the cube's 24, a fact it uses")
    print("   must fail on 2T: the twin hands irreducible, nu = -1 = z on them, T forced with T T = -1.")
    t2 = closure([QB, HZ])
    tt = Table(t2)
    e12 = tuple(tr(c[0]) for c in tt.cls)
    n_x, signs = twin_T_forced(t2)
    facts = [tt.ip(e12, e12) == E1, tt.nu(e12) == rat(-1), n_x == 1 and signs == [-1]]
    print(f"    on 2T: twin hands irreducible {facts[0]}, nu = -1 {facts[1]}, T forced with T T = -1 {facts[2]}: {sum(facts)} of 3 facts hold")
    print("F2 (a finding): Q8 alone (the 8 lifts of the face half turns), the plan's 'it needs the whole 24'")
    q8 = closure([HZ, HX])
    tq = Table(q8)
    iq = tq.irreducibles(tuple(tr(c[0]) for c in tq.cls))
    miss = sum(1 for ch in iq if describe(tq, ch)[1] != describe(tq, ch)[2])
    n_x, signs = twin_T_forced(q8)
    print(f"    Q8 kinds where nu != chi(z)/dim: {miss} of {len(iq)}; T forced with T T = -1 on the twin hands: {n_x == 1 and signs == [-1]}")
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    print("findings: F1 and F2 do not fail: the law, and every fact of it that Pauli uses, holds on 2T's twin hands and on Q8")
    return 1 if bad else 0


def sum_f(xs):
    out = Z0
    for x in xs:
        out = add(out, x)
    return out


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main()
    subgroups()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)

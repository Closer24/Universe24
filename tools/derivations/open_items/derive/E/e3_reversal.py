"""Draft E, probe e3: the phase reversal of a train at the turnover, T = i sigma_y K, against the head's K.

  python3 -I e3_reversal.py            the claims (must print 0 failures)
  python3 -I e3_reversal.py mutants    the mutations (each must fail)

T(z1, z2) = (-conj z2, conj z1) on the twin hands (an exchange of the two twins, two conjugations and a sign);
K(z1, z2) = (conj z1, conj z2) is the head's (hands.signs: the twelve gear of every hand negated).
The 48 lifts act on twin pairs as 2 x 2 matrices U(q) = [[a - i d, -c - i b], [c - i b, a + i d]] for
q = a + b i + c j + d k, with entries in Q(r2)(i), held exactly as four Fractions (re, re r2, im, im r2).
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction as Fr
from itertools import product

FAIL = []
RNG = random.Random(28102026)


def check(name, ok, count=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if count is None else f": {count}"))


# ---- numbers of Q(r2)(i): (p, q, s, t) = (p + q r2) + i (s + t r2) ----
def r2m(x, y):
    return (x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def r2a(x, y):
    return (x[0] + y[0], x[1] + y[1])


def r2n(x):
    return (-x[0], -x[1])


def cm(a, b):
    re = r2a(r2m(a[:2], b[:2]), r2n(r2m(a[2:], b[2:])))
    im = r2a(r2m(a[:2], b[2:]), r2m(a[2:], b[:2]))
    return re + im


def ca(a, b):
    return tuple(x + y for x, y in zip(a, b, strict=True))


def cneg(a):
    return tuple(-x for x in a)


def cconj(a):
    return (a[0], a[1], -a[2], -a[3])


C0 = (Fr(0),) * 4


def cg(z):
    """A Gaussian integer as a number of Q(r2)(i)."""
    return (Fr(z[0]), Fr(0), Fr(z[1]), Fr(0))


def binary_octahedral():
    """The 48 unit quaternions, coordinates as Q(r2) pairs."""
    z, one, half, inv = (Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(1, 2), Fr(0)), (Fr(0), Fr(1, 2))
    els = set()
    for k in range(4):
        for s in (1, -1):
            q = [z] * 4
            q[k] = (Fr(s), Fr(0))
            els.add(tuple(q))
    for sg in product((1, -1), repeat=4):
        els.add(tuple((s * half[0], s * half[1]) for s in sg))
    for a in range(4):
        for b in range(a + 1, 4):
            for sa, sb in product((1, -1), repeat=2):
                q = [z] * 4
                q[a], q[b] = (sa * inv[0], sa * inv[1]), (sb * inv[0], sb * inv[1])
                els.add(tuple(q))
    return sorted(els)


def U_of(q):
    a, b, c, d = q
    neg = r2n
    return (
        (a + neg(d), neg(c) + neg(b)),
        (c + neg(b), a + d),
    )


def mat(q):
    """U(q) as a 2 x 2 matrix of Q(r2)(i) numbers."""
    a, b, c, d = q
    return (
        (a + r2n(d), r2n(c) + r2n(b)),
        (c + r2n(b), a + d),
    )


def apply(M, v):
    return tuple(ca(cm(M[r][0], v[0]), cm(M[r][1], v[1])) for r in range(2))


def T(v):
    return (cneg(cconj(v[1])), cconj(v[0]))


def K(v):
    return (cconj(v[0]), cconj(v[1]))


def spin(v):
    c = cm(cconj(v[0]), v[1])
    n1, n2 = cm(cconj(v[0]), v[0]), cm(cconj(v[1]), v[1])
    return (tuple(2 * x for x in c[:2]), tuple(2 * x for x in c[2:]), r2a(n1[:2], r2n(n2[:2])))


def rpair(k=9):
    while True:
        v = ((RNG.randint(-k, k), RNG.randint(-k, k)), (RNG.randint(-k, k), RNG.randint(-k, k)))
        if any(x for z in v for x in z):
            return v


def as_c(v):
    return (cg(v[0]), cg(v[1]))


# ---- Gaussian-integer twin pairs ----
def gm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gc(a):
    return (a[0], -a[1])


def gk(k, a):
    return (k * a[0], k * a[1])


def gT(v):
    return (gk(-1, gc(v[1])), gc(v[0]))


def gK(v):
    return (gc(v[0]), gc(v[1]))


def ginner(u, v):
    p, q = gm(gc(u[0]), v[0]), gm(gc(u[1]), v[1])
    return (p[0] + q[0], p[1] + q[1])


def gdet(u, v):
    p, q = gm(u[0], v[1]), gm(u[1], v[0])
    return (p[0] - q[0], p[1] - q[1])


def gspin(v):
    c = gm(gc(v[0]), v[1])
    return (2 * c[0], 2 * c[1], v[0][0] ** 2 + v[0][1] ** 2 - v[1][0] ** 2 - v[1][1] ** 2)


def rho(v):
    return sum(x * x for z in v for x in z)


def sweep(now, before):
    """Im(conj(now) before) of one hand, the head's hands.sweep."""
    return now[0] * before[1] - now[1] * before[0]


def turns24():
    out = []
    for p in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
        for s in product((1, -1), repeat=3):
            m = [[0] * 3 for _ in range(3)]
            for col, row in enumerate(p):
                m[row][col] = s[col]
            if det3(m) == 1:
                out.append(tuple(tuple(r) for r in m))
    return out


def det3(r):
    return (
        r[0][0] * (r[1][1] * r[2][2] - r[1][2] * r[2][1])
        - r[0][1] * (r[1][0] * r[2][2] - r[1][2] * r[2][0])
        + r[0][2] * (r[1][0] * r[2][1] - r[1][1] * r[2][0])
    )


def mv(m, v):
    return tuple(sum(m[i][k] * v[k] for k in range(3)) for i in range(3))


def main_claims():
    G = binary_octahedral()
    lifts = [mat(q) for q in G]
    probes = [as_c(rpair()) for _ in range(40)]

    print("1. T commutes with all 48 lifts; K with the 8 real ones (16 up to a sign: 8 of the 24 turns)")
    t_ok = sum(all(apply(U, T(v)) == T(apply(U, v)) for v in probes) for U in lifts)
    k_ok = sum(all(apply(U, K(v)) == K(apply(U, v)) for v in probes) for U in lifts)
    k_sign = sum(all(spin(apply(U, K(v))) == spin(K(apply(U, v))) for v in probes) for U in lifts)
    check("T U psi = U T psi", t_ok == 48, f"{t_ok} of 48 lifts x 40 twin pairs")
    check("K U psi = U K psi", k_ok == 8, f"{k_ok} of 48 (the turns about the y axis)")
    check("S(K U psi) = S(U K psi): K keeps the 24 on the reading only for", k_sign == 16, f"{k_sign} of 48 lifts")
    R = turns24()
    flip_y = ((1, 0, 0), (0, -1, 0), (0, 0, 1))
    t24 = sum(all(tuple(-x for x in mv(r, s)) == mv(r, tuple(-x for x in s)) for s in [gspin(rpair()) for _ in range(20)]) for r in R)
    k24 = sum(all(mv(flip_y, mv(r, s)) == mv(r, mv(flip_y, s)) for s in [gspin(rpair()) for _ in range(20)]) for r in R)
    check("on the reading S: T's S -> -S commutes with the 24 turns", t24 == 24, f"{t24} of 24")
    check("on the reading S: K's S -> (Sx, -Sy, Sz) commutes only with the y axis's 8", k24 == 8, f"{k24} of 24")

    print("2. T T = -1 on the twin hands, K K = +1; T keeps rho, reverses S, and conjugates the overlap")
    n = [0] * 5
    for _ in range(20000):
        v, w = rpair(), rpair()
        n[0] += gT(gT(v)) == (gk(-1, v[0]), gk(-1, v[1]))
        n[1] += gK(gK(v)) == v
        n[2] += rho(gT(v)) == rho(v) and gspin(gT(v)) == tuple(-x for x in gspin(v))
        n[3] += ginner(gT(v), gT(w)) == gc(ginner(v, w))
        n[4] += gspin(gK(v)) == (gspin(v)[0], -gspin(v)[1], gspin(v)[2])
    for name, c in zip(("T T psi = -psi", "K K psi = psi", "rho(T psi) = rho, S(T psi) = -S", "<T u, T v> = conj <u, v>", "S(K psi) = (Sx, -Sy, Sz)"), n, strict=True):
        check(name, c == 20000, f"{c} of 20000")

    print("3. Kramers and the pairing: <T phi, phi> = 0, det[phi, chi] = <T phi, chi>; the one hand's K: <K z, z> = z z")
    box = [v for v in product(range(-2, 3), repeat=4)]
    pairs = [((a, b), (c, d)) for a, b, c, d in box if (a, b, c, d) != (0, 0, 0, 0)]
    kr = sum(ginner(gT(p), p) == (0, 0) for p in pairs)
    dt = sum(gdet(p, q) == ginner(gT(p), q) for p in pairs for q in pairs[::7])
    check("<T phi, phi> = 0, exhaustive", kr == len(pairs), f"{kr} of {len(pairs)}")
    check("det[phi, chi] = <T phi, chi>", dt == len(pairs) * len(pairs[::7]), f"{dt} of {len(pairs) * len(pairs[::7])}")
    zs = [(a, b) for a, b in product(range(-4, 5), repeat=2) if (a, b) != (0, 0)]
    one = sum(gm(gc(gc(z)), z) == gm(z, z) and gm(z, z) != (0, 0) for z in zs)
    check("one hand: <K z, z> = z z, never 0 for z != 0", one == len(zs), f"{one} of {len(zs)}")

    print("4. T is the one covariant phase reversal: X conj(U) = U X for the generators gives X = lam (-i sigma_y), so J J < 0")
    sol = commutant()
    shown = [[[f"{x[0]}{x[1]:+}i" for x in row] for row in X] for X in sol]
    want = [(((0, 0), (-1, 0)), ((1, 0), (0, 0))), (((0, 0), (0, -1)), ((0, 1), (0, 0)))]
    check(
        "the solutions X over Q form a space of dimension 2 (lam in Q(i)), spanned by -i sigma_y and its i multiple",
        len(sol) == 2 and sol == want,
        shown,
    )
    neg = all(is_neg_scalar(xconjx(X)) for X in sol + [combo(sol, 3, -5), combo(sol, 7, 2)])
    check("X conj(X) is a negative multiple of 1 for every solution: every 24-covariant phase reversal squares to minus", neg)

    print("5. The ratchet's carry: T^n psi = (-1)^(n div 2) T^(n mod 2) psi, the sign the carry of the pawl's two teeth")
    ok = 0
    for _ in range(500):
        v = rpair()
        w = v
        good = True
        for n in range(17):
            base = v if n % 2 == 0 else gT(v)
            sign = -1 if (n // 2) % 2 else 1
            good &= w == (gk(sign, base[0]), gk(sign, base[1]))
            w = gT(w)
        ok += good
    check("n = 0 .. 16", ok == 500, f"{ok} of 500")

    print("6. The turnover's act on the twin gears: now' = T(before), before' = T(now)")
    n = [0] * 5
    for _ in range(20000):
        un, ub, dn, db = [(RNG.randint(-9, 9), RNG.randint(-9, 9)) for _ in range(4)]
        now, before = (un, dn), (ub, db)
        tn, tb = gT(before), gT(now)
        kn, kb = gK(before), gK(now)
        g = (tn[0][0], tn[0][1], tn[1][0], tn[1][1])
        n[0] += g == (-db[0], db[1], ub[0], -ub[1])
        n[1] += gspin(tn) == tuple(-x for x in gspin(before)) and rho(tn) == rho(before)
        n[2] += sweep(tn[0], tb[0]) == sweep(dn, db) and sweep(tn[1], tb[1]) == sweep(un, ub)
        n[3] += sweep(kn[0], kb[0]) == sweep(un, ub) and sweep(kn[1], kb[1]) == sweep(dn, db)
        back = (gk(-1, gT(tb)[0]), gk(-1, gT(tb)[1])), (gk(-1, gT(tn)[0]), gk(-1, gT(tn)[1]))
        twice = gT(tb), gT(tn)
        n[4] += back == (now, before) and twice == ((gk(-1, un), gk(-1, dn)), (gk(-1, ub), gk(-1, db)))
    labels = (
        "the gears (u3, u12, d3, d12) of the before become (-d3, d12, u3, -u12) of the now after: an exchange and signs",
        "S of the now after = -S of the before, rho kept (time reversed, the spin reversed)",
        "T: the two twins' sweeps exchange (the total kept)",
        "K (head): each twin's sweep kept",
        "the rewind is the turnover with T^-1 = -T; the turnover twice gives -psi (no involution on the twin hands)",
    )
    for name, c in zip(labels, n, strict=True):
        check(name, c == 20000, f"{c} of 20000")


def commutant():
    """Solve X conj(U) = U X over Q for U = U(i), U(j), U((1 + i + j + k)/2) (entries in Q(i)). Unknowns: X's 4 entries as
    (re, im), 8 rationals. Returns a basis of the solution space as 2 x 2 matrices of Gaussian-rational pairs."""
    half = (Fr(1, 2), Fr(0))
    z, one = (Fr(0), Fr(0)), (Fr(1), Fr(0))
    gens = [(z, one, z, z), (z, z, one, z), (half, half, half, half)]
    Ms = []
    for q in gens:
        U = mat(q)
        Ms.append(tuple(tuple((x[0], x[2]) for x in row) for row in U))  # rational entries: drop the r2 parts (all 0)

    def qmul(a, b):
        return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])

    rows = []
    for U in Ms:
        Uc = tuple(tuple((x[0], -x[1]) for x in r) for r in U)
        for r in range(2):
            for c in range(2):
                # (X conj U - U X)[r][c] = SUM_k X[r][k] Uc[k][c] - U[r][k] X[k][c]; X[r][k] = x_(2r+k) = (p, q)
                for part in (0, 1):
                    coeff = [Fr(0)] * 8
                    for k in range(2):
                        # X[r][k] * Uc[k][c]
                        for comp, unit in ((0, (Fr(1), Fr(0))), (1, (Fr(0), Fr(1)))):
                            prod_ = qmul(unit, Uc[k][c])
                            coeff[2 * (2 * r + k) + comp] += prod_[part]
                        # - U[r][k] * X[k][c]
                        for comp, unit in ((0, (Fr(1), Fr(0))), (1, (Fr(0), Fr(1)))):
                            prod_ = qmul(U[r][k], unit)
                            coeff[2 * (2 * k + c) + comp] -= prod_[part]
                    rows.append(coeff)
    basis = nullspace(rows, 8)
    return [tuple(tuple((b[2 * (2 * r + c)], b[2 * (2 * r + c) + 1]) for c in range(2)) for r in range(2)) for b in basis]


def nullspace(rows, n):
    m = [r[:] for r in rows]
    piv = []
    r = 0
    for c in range(n):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        inv = 1 / m[r][c]
        m[r] = [x * inv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r], strict=True)]
        piv.append(c)
        r += 1
    free = [c for c in range(n) if c not in piv]
    out = []
    for fc in free:
        v = [Fr(0)] * n
        v[fc] = Fr(1)
        for i, pc in enumerate(piv):
            v[pc] = -m[i][fc]
        out.append(v)
    return out


def xconjx(X):
    def qmul(a, b):
        return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])

    Xc = tuple(tuple((x[0], -x[1]) for x in r) for r in X)
    return tuple(
        tuple(tuple(a + b for a, b in zip(qmul(X[r][0], Xc[0][c]), qmul(X[r][1], Xc[1][c]), strict=True)) for c in range(2))
        for r in range(2)
    )


def is_neg_scalar(P):
    return P[0][1] == (0, 0) and P[1][0] == (0, 0) and P[0][0] == P[1][1] and P[0][0][1] == 0 and P[0][0][0] < 0


def combo(sol, a, b):
    return tuple(
        tuple((a * sol[0][r][c][0] + b * sol[1][r][c][0], a * sol[0][r][c][1] + b * sol[1][r][c][1]) for c in range(2))
        for r in range(2)
    )


def mutants():
    bad = []

    def report(name, count, of):
        print(f"  {name}: {count} of {of} (must be above 0)")
        if count == 0:
            bad.append(name)

    G = binary_octahedral()
    lifts = [mat(q) for q in G]
    probes = [as_c(rpair()) for _ in range(20)]
    print("M1. K in place of T at the turnover: the 24 must break and Kramers must fail")
    report("lifts with S(K U psi) != S(U K psi)", sum(not all(spin(apply(U, K(v))) == spin(K(apply(U, v))) for v in probes) for U in lifts), 48)
    pairs = [((a, b), (c, d)) for a, b, c, d in product(range(-2, 3), repeat=4) if (a, b, c, d) != (0, 0, 0, 0)]
    report("hands with <K phi, phi> != 0", sum(ginner(gK(p), p) != (0, 0) for p in pairs), len(pairs))
    report("twin pairs where K K psi != -psi (eps read as K squared is +1, not the full turn)", sum(gK(gK(p)) != (gk(-1, p[0]), gk(-1, p[1])) for p in pairs), len(pairs))
    print("M2. T without its sign, (conj z2, conj z1): its square must stop being -1 and the 24 must break")

    def t_nosign(v):
        return (cconj(v[1]), cconj(v[0]))

    report("lifts it fails to commute with", sum(not all(apply(U, t_nosign(v)) == t_nosign(apply(U, v)) for v in probes) for U in lifts), 48)
    report("twin pairs where its square is not -1", sum(1 for p in pairs if (gc(gc(p[0])), gc(gc(p[1]))) != (gk(-1, p[0]), gk(-1, p[1]))), len(pairs))
    print("M3. the exchange without the conjugation (the half turn about y, a turn and no reversal): Kramers must fail")

    def hy(v):
        return (gk(-1, v[1]), v[0])

    report("hands with <H_y phi, phi> != 0", sum(ginner(hy(p), p) != (0, 0) for p in pairs), len(pairs))
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main_claims()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)

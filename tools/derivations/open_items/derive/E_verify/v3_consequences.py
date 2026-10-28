"""Verifier of draft E, probe v3: the consequences re-derived with independent code (Gaussian integers only).

  python3 -I v3_consequences.py            the claims (must end with 0 failures)
  python3 -I v3_consequences.py mutants    the mutations (each must fail)

The joint amplitude of q equal quanta at parts rows[0..q-1] is SUM_pi eps^inv(pi) PROD_j M[rows[j]][pi(j)]: the
determinant (eps = -1) or the permanent (eps = +1) of the q x q matrix of overlaps, computed here by Leibniz's sum.
1. One Node-clock (parts phi, T phi): the amplitudes themselves, A_++ = A_-- = 0 and A_+- = -A_-+ = rho(phi) det[psi1, psi2],
   exhaustive on a box and random.
2. A third (and a fourth) twin quantum at one Node-clock: every assignment 0.
3. q quanta in one part: SUM sgn = 0 for q = 2..7, and the determinant with q equal rows 0 for random overlaps.
4. Bosons: sigma_aa = 4 N(M_a1 M_a2); Hong, Ou and Mandel's zero; the ordering bosons <= distinguishable <= fermions on
   splitters of the unitary form, and where it breaks on general overlaps.
5. The books: SUM over ordered pairs = 2 [(psi1 G psi1)(psi2 G psi2) + eps N(psi1 G psi2)] for K = 2..5 parts; Cauchy-Binet.
6. Sofer's occupant frame: free + blocked = room, the two-quantum total 2 rho^2 free, the deficit 2 rho^2 blocked.
"""

from __future__ import annotations

import random
import sys
from itertools import permutations, product

FAIL = []
RNG = random.Random(1940)


def check(name, ok, info=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if info is None else f": {info}"))


# Gaussian integers as Python pairs; written afresh (not the draft's helpers)
def m(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def p(a, b):
    return (a[0] + b[0], a[1] + b[1])


def s(a, b):
    return (a[0] - b[0], a[1] - b[1])


def cj(a):
    return (a[0], -a[1])


def nn(a):
    return a[0] * a[0] + a[1] * a[1]


def k(c, a):
    return (c * a[0], c * a[1])


O, ONE, II = (0, 0), (1, 0), (0, 1)


def ip(u, v):
    out = O
    for x, y in zip(u, v):
        out = p(out, m(cj(x), y))
    return out


def rev(f):
    return (k(-1, cj(f[1])), cj(f[0]))


def rho(f):
    return sum(nn(x) for x in f)


def dt(u, v):
    return s(m(u[0], v[1]), m(u[1], v[0]))


def rg(r=9):
    return (RNG.randint(-r, r), RNG.randint(-r, r))


def rv(n=2, r=9):
    while True:
        v = tuple(rg(r) for _ in range(n))
        if any(x != O for x in v):
            return v


def sign(perm):
    sg, seen = 1, [False] * len(perm)
    for i in range(len(perm)):
        if not seen[i]:
            j, L = i, 0
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                L += 1
            if L % 2 == 0:
                sg = -sg
    return sg  # by cycles, not by inversions (an independent count)


def leibniz(Mrows, eps):
    q = len(Mrows)
    out = O
    for perm in permutations(range(q)):
        t = ONE
        for j in range(q):
            t = m(t, Mrows[j][perm[j]])
        out = p(out, k(sign(perm) if eps == -1 else 1, t))
    return out


def amp2(M, a, b, eps):
    return leibniz([M[a], M[b]], eps)


def overl(parts, quanta):
    return [[ip(f, q) for q in quanta] for f in parts]


def main():
    print("1. One Node-clock: the amplitudes in the frame (phi, T phi)")
    box = [v for v in product(range(-1, 2), repeat=4) if any(v)]
    pairs = [((a, b), (c, d)) for a, b, c, d in box]
    n = tot = 0
    for f in pairs:
        for q1 in pairs[::3]:
            for q2 in pairs[::5]:
                M = overl([f, rev(f)], [q1, q2])
                tot += 1
                A = {(a, b): amp2(M, a, b, -1) for a in range(2) for b in range(2)}
                n += A[(0, 0)] == O and A[(1, 1)] == O and A[(0, 1)] == k(rho(f), dt(q1, q2)) and A[(1, 0)] == k(-rho(f), dt(q1, q2))
    check("exhaustive on the box {-1, 0, 1}^4 (phi all 80, quanta thinned): A_++ = A_-- = 0, A_+- = -A_-+ = rho(phi) det", n == tot, f"{n} of {tot}")
    n = 0
    for _ in range(20000):
        f, q1, q2 = rv(), rv(), rv()
        M = overl([f, rev(f)], [q1, q2])
        n += amp2(M, 0, 0, -1) == O and amp2(M, 0, 1, -1) == k(rho(f), dt(q1, q2))
    check("random, entries up to 9", n == 20000, f"{n} of 20000")

    print("2. A third and a fourth twin quantum at one Node-clock: every assignment to the two senses has amplitude 0")
    for q in (3, 4):
        n = nb = 0
        trials = 2000 if q == 3 else 400
        for _ in range(trials):
            f = rv()
            M = overl([f, rev(f)], [rv() for _ in range(q)])
            n += all(leibniz([M[r] for r in rows], -1) == O for rows in product(range(2), repeat=q))
            nb += any(leibniz([M[r] for r in rows], 1) != O for rows in product(range(2), repeat=q))
        check(f"q = {q}: all {2 ** q} assignments 0 with eps = -1 (and some not 0 with eps = +1)", n == trials and nb == trials, f"{n} and {nb} of {trials}")

    print("3. q quanta in one part")
    for q in range(2, 8):
        check(f"q = {q}: SUM over the q! orders of sgn (counted by cycles) = 0", sum(sign(pp) for pp in permutations(range(q))) == 0)
    for q in range(2, 6):
        n = 0
        for _ in range(200):
            row = [rg() for _ in range(q)]
            prod_ = ONE
            for x in row:
                prod_ = m(prod_, x)
            fact = 1
            for t in range(2, q + 1):
                fact *= t
            n += leibniz([row] * q, -1) == O and leibniz([row] * q, 1) == k(fact, prod_)
        check(f"q = {q}: the determinant with q equal rows is 0, the permanent q! PROD M", n == 200, f"{n} of 200")
    print("   (this bounds the q-quantum joint amplitude in one part; it does not bound law 5's q = E div w_c on one hand's wind)")

    print("4. The force carriers: bunching, Hong-Ou-Mandel, the ordering")
    n = 0
    for _ in range(20000):
        M = overl([rv(), rv()], [rv(), rv()])
        n += all(nn(amp2(M, a, a, 1)) == 4 * nn(m(M[a][0], M[a][1])) for a in range(2))
    check("sigma_aa = 4 N(M_a1 M_a2) for eps = +1", n == 20000, f"{n} of 20000")
    M = [[ONE, II], [II, ONE]]
    check("the balanced splitter (1, i), (i, 1): sigma_xy = 0 for eps = +1, 4 for eps = -1", nn(amp2(M, 0, 1, 1)) == 0 and nn(amp2(M, 0, 1, -1)) == 4)
    unit_ok = gen_bad = seen = 0
    for _ in range(20000):
        a, c = rg(), rg()
        if nn(a) + nn(c) == 0:
            continue
        seen += 1
        U = [[a, k(-1, cj(c))], [c, cj(a)]]
        cb = 2 * nn(amp2(U, 0, 1, 1))
        cf = 2 * nn(amp2(U, 0, 1, -1))
        cd = 2 * (nn(m(U[0][0], U[1][1])) + nn(m(U[1][0], U[0][1])))
        unit_ok += cb <= cd <= cf and ((cb == 0) == (nn(a) == nn(c)))
        G = [[rg(), rg()], [rg(), rg()]]  # general overlaps, not a splitter
        gb = 2 * nn(amp2(G, 0, 1, 1))
        gf = 2 * nn(amp2(G, 0, 1, -1))
        gd = 2 * (nn(m(G[0][0], G[1][1])) + nn(m(G[1][0], G[0][1])))
        gen_bad += not (gb <= gd <= gf)
    check("splitters [[a, -conj c], [c, conj a]]: bosons <= distinguishable <= fermions, bosons 0 iff N(a) = N(c)", unit_ok == seen, f"{unit_ok} of {seen}")
    print(f"    general 2 x 2 overlaps (not a splitter): the ordering breaks at {gen_bad} of {seen}; the draft's claim holds for splitters only")

    print("5. The books over K parts: SUM_(a, b) sigma = 2 [(psi1 G psi1)(psi2 G psi2) + eps N(psi1 G psi2)]")
    for K in (2, 3, 4, 5):
        n = cb = 0
        for _ in range(2000):
            parts = [rv() for _ in range(K)]
            q1, q2 = rv(), rv()
            M = overl(parts, [q1, q2])
            # G = SUM phi phi^dagger applied as forms: psi_i G psi_j = SUM_a conj(M_ai) M_aj
            g11 = sum(nn(M[a][0]) for a in range(K))
            g22 = sum(nn(M[a][1]) for a in range(K))
            g12 = O
            for a in range(K):
                g12 = p(g12, m(cj(M[a][0]), M[a][1]))
            good = True
            for eps in (1, -1):
                tot = sum(nn(amp2(M, a, b, eps)) for a in range(K) for b in range(K))
                good &= tot == 2 * (g11 * g22 + eps * nn(g12))
            n += good
            minors = sum(nn(amp2(M, a, b, -1)) for a in range(K) for b in range(a + 1, K))
            cb += minors == g11 * g22 - nn(g12)
        check(f"K = {K} parts: the sum rule for both signs, and Cauchy-Binet SUM_(a<b) N(minor) = det(M^dagger M)", n == 2000 and cb == 2000, f"{n}, {cb} of 2000")
    n = 0
    for _ in range(5000):
        f = rv()
        q1, q2 = rv(), rv()
        M = overl([f, rev(f)], [q1, q2])
        lam = rho(f)
        n += all(sum(nn(amp2(M, a, b, e)) for a in range(2) for b in range(2)) == 2 * lam * lam * (rho(q1) * rho(q2) + e * nn(ip(q1, q2))) for e in (1, -1))
    check("a complete frame (phi, T phi), G = rho(phi) I: 2 lam^2 (rho1 rho2 + eps N<psi1, psi2>)", n == 5000, f"{n} of 5000")

    print("6. Sofer's occupant frame is the joint click of occupant and newcomer, read in the occupant's frame")
    box2 = [((a, b), (c, d)) for a, b, c, d in product(range(-2, 3), repeat=4) if (a, b, c, d) != (0, 0, 0, 0)]
    n = tot = 0
    for f in box2:
        for chi in box2[::17]:
            tot += 1
            M = overl([f, rev(f)], [f, chi])
            free, blocked, r = nn(ip(rev(f), chi)), nn(ip(f, chi)), rho(f)
            two = sum(nn(amp2(M, a, b, -1)) for a in range(2) for b in range(2))
            dist = 2 * (r * r) * (r * rho(chi))
            n += free + blocked == r * rho(chi) and two == 2 * r * r * free and dist - two == 2 * r * r * blocked and free == nn(dt(f, chi))
    check("exhaustive phi in the box {-2..2}^4, newcomers thinned", n == tot, f"{n} of {tot}")


def mutants():
    bad = []

    def report(name, count, of):
        print(f"  {name}: {count} of {of} (must be above 0)")
        if count == 0:
            bad.append(name)

    print("M1. eps = +1 on the twin hands: the one-Node-clock zero must fail")
    c = 0
    for _ in range(2000):
        f = rv()
        M = overl([f, rev(f)], [rv(), rv()])
        c += amp2(M, 0, 0, 1) != O
    report("pairs with A_++ != 0", c, 2000)
    print("M2. the frame (phi, K phi) in place of (phi, T phi): the singlet must stop being frame-free")
    c = 0
    for _ in range(2000):
        f = rv()
        q1, q2 = rv(), rv()
        M = overl([f, (cj(f[0]), cj(f[1]))], [q1, q2])
        c += amp2(M, 0, 1, -1) != k(rho(f), dt(q1, q2))
    report("pairs whose A_+- is not rho(phi) det", c, 2000)
    print("M3. a third quantum with eps = +1: some assignment must survive")
    c = 0
    for _ in range(500):
        f = rv()
        M = overl([f, rev(f)], [rv(), rv(), rv()])
        c += any(leibniz([M[r] for r in rows], 1) != O for rows in product(range(2), repeat=3))
    report("triples with a nonzero assignment", c, 500)
    print("M4. the books with the exchange term dropped (distinguishable): the eps = -1 sum rule must fail")
    c = 0
    for _ in range(2000):
        f = rv()
        q1, q2 = rv(), rv()
        M = overl([f, rev(f)], [q1, q2])
        d = sum(nn(m(M[a][0], M[b][1])) + nn(m(M[b][0], M[a][1])) for a in range(2) for b in range(2))
        c += d != 2 * rho(f) ** 2 * (rho(q1) * rho(q2) - nn(ip(q1, q2)))
    report("pairs whose books fail", c, 2000)
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)

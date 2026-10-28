"""Verifier of draft E, probe v4: the board's state and Sofer's bound, with independent code.

  python3 -I v4_board.py            the claims (must end with 0 failures)
  python3 -I v4_board.py mutants    the mutations (each must fail)

1. One twin pair per train and Node-clock holds one spinor: S . S = rho^2 for every pair (exhaustive), so its
   occupation n = psi psi^dagger has rank 1 and is never the filled orbital (S = 0); a third newcomer finds room.
2. One hand per quantum: n = SUM psi_k psi_k^dagger reaches the filled orbital, and then a third has no room.
3. The occupation is a reading, not a state: two boards equal in (rho, S) at every Node-clock step apart. Shown on a
   ring and on a 3 x 3 x 2 torus with this probe's own step, a+ = 2a - a- + g SUM_j (a_j - a) - d a (exact Fractions).
4. That step keeps the two-slot form W(u, v) and moves the one-slot form; one quantum's two-slot occupation D has
   det D = -N(det[now, before]), so D is not positive (no bound on the board from the kept form).
5. Sofer's bound |S| <= rho <= 2u against 0 <= n <= u (|S| <= min(rho, 2u - rho)): exhaustive over integer (rho, S)
   for u = 3, 4, 6, newcomers searched in growing boxes until every occupation outside the corrected bound shows a
   negative free size.
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction as Fr
from itertools import product
from math import isqrt

FAIL = []
RNG = random.Random(1925)


def check(name, ok, info=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if info is None else f": {info}"))


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


O = (0, 0)


def ip(u, v):
    out = O
    for x, y in zip(u, v):
        out = p(out, m(cj(x), y))
    return out


def rev(f):
    return (k(-1, cj(f[1])), cj(f[0]))


def rho(f):
    return sum(nn(x) for x in f)


def spin(f):
    c = m(cj(f[0]), f[1])
    return (2 * c[0], 2 * c[1], nn(f[0]) - nn(f[1]))


def dt(u, v):
    return s(m(u[0], v[1]), m(u[1], v[0]))


def dot3(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def rg(r=9):
    return (RNG.randint(-r, r), RNG.randint(-r, r))


def rv(r=9):
    while True:
        v = (rg(r), rg(r))
        if v != (O, O):
            return v


def box(r):
    return [((a, b), (c, d)) for a, b, c, d in product(range(-r, r + 1), repeat=4) if (a, b, c, d) != (0, 0, 0, 0)]


def occ(quanta):
    R = sum(rho(q) for q in quanta)
    S = tuple(sum(spin(q)[i] for q in quanta) for i in range(3))
    return R, S


# ---- this probe's own step on a torus (exact), each twin component alike ----
def neighbours(x, dims):
    for a in range(len(dims)):
        for e in (1, -1):
            t = list(x)
            t[a] = (t[a] + e) % dims[a]
            yield tuple(t)


def step(board, dims, g, d):
    now, before = board
    new = {}
    for x, v in now.items():
        comps = []
        for c in range(2):
            lap = [Fr(0), Fr(0)]
            for y in neighbours(x, dims):
                lap[0] += now[y][c][0] - v[c][0]
                lap[1] += now[y][c][1] - v[c][1]
            comps.append(tuple(2 * v[c][t] - before[x][c][t] + g * lap[t] - d * v[c][t] for t in range(2)))
        new[x] = tuple(comps)
    return (new, now)


def rboard(dims, r=4):
    sites = list(product(*[range(n) for n in dims]))
    def one():
        return tuple((Fr(RNG.randint(-r, r)), Fr(RNG.randint(-r, r))) for _ in range(2))
    return ({x: one() for x in sites}, {x: one() for x in sites})


def focc(v):
    c = (v[0][0] * v[1][0] + v[0][1] * v[1][1], v[0][0] * v[1][1] - v[0][1] * v[1][0])
    n1 = v[0][0] ** 2 + v[0][1] ** 2
    n2 = v[1][0] ** 2 + v[1][1] ** 2
    return (n1 + n2, 2 * c[0], 2 * c[1], n1 - n2)


UNITS = [(Fr(1), Fr(0)), (Fr(0), Fr(1)), (Fr(-1), Fr(0)), (Fr(0), Fr(-1))]


def fm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def fip(u, v):
    re = im = Fr(0)
    for x, y in zip(u, v):
        t = fm((x[0], -x[1]), y)
        re += t[0]
        im += t[1]
    return (re, im)


def W(u, v):
    re = im = Fr(0)
    for x in u[0]:
        a = fip(u[0][x], v[1][x])
        b = fip(u[1][x], v[0][x])
        re += a[0] - b[0]
        im += a[1] - b[1]
    return (re, im)


def L1(u, v):
    re = im = Fr(0)
    for x in u[0]:
        a = fip(u[0][x], v[0][x])
        re += a[0]
        im += a[1]
    return (re, im)


def aimed(S, R, u):
    """A Gaussian newcomer whose m(chi) points along S to within the gap |S| - (2u - R) > 0: the inverse Hopf map
    z1 = A + N S3, z2 = N (S1 + i S2), A = isqrt(N^2 S . S), refined until the free size is below 0 (integers only)."""
    ss = dot3(S, S)
    for e in range(1, 40):
        N = 2 ** e
        A = isqrt(N * N * ss)
        for chi in (((A + N * S[2], 0), (N * S[0], N * S[1])), ((N * S[0], -N * S[1]), (A - N * S[2], 0))):
            if chi != (O, O) and (2 * u - R) * rho(chi) - dot3(S, spin(chi)) < 0:
                return chi
    return None


def main():
    print("1. One twin pair per Node-clock: one spinor, rank one")
    B3 = box(3)
    pure = sum(dot3(spin(f), spin(f)) == rho(f) ** 2 for f in B3)
    check("S . S = rho^2 for every Gaussian twin pair in {-3..3}^4 (Fierz for one spinor)", pure == len(B3), f"{pure} of {len(B3)}")
    third = tried = 0
    for f in box(2):
        summed = (p(f[0], rev(f)[0]), p(f[1], rev(f)[1]))
        for chi in box(2)[::11]:
            tried += 1
            third += nn(dt(summed, chi)) > 0
    print(f"    the two quanta phi, T phi summed into one pair: a third newcomer finds free > 0 at {third} of {tried}")
    check("so the head's one pair per Node-clock cannot hold the filled orbital", third > 0)

    print("2. One hand per quantum: phi and T phi as two hands")
    n = 0
    for f in box(2):
        R, S = occ([f, rev(f)])
        u = rho(f)
        n += S == (0, 0, 0) and R == 2 * u and all((2 * u - R) * rho(c) - dot3(S, spin(c)) == 0 for c in box(1))
    check("n = rho(phi) I: S = 0, rho = 2u, and a third newcomer's free size is 0 for every newcomer in {-1..1}^4", n == len(box(2)), f"{n} of {len(box(2))}")

    print("3. The occupation is a reading, not a state")
    for dims in ((7,), (3, 3, 2)):
        apart = same_global = 0
        trials = 12
        for _ in range(trials):
            b = rboard(dims)
            ph = {x: UNITS[(sum((i + 1) * c for i, c in enumerate(x))) % 4] for x in b[0]}
            b2 = ({x: tuple(fm(ph[x], c) for c in v) for x, v in b[0].items()}, {x: tuple(fm(ph[x], c) for c in v) for x, v in b[1].items()})
            assert all(focc(b[0][x]) == focc(b2[0][x]) and focc(b[1][x]) == focc(b2[1][x]) for x in b[0])
            n1, n2 = step(b, dims, Fr(1, 4), Fr(1, 8)), step(b2, dims, Fr(1, 4), Fr(1, 8))
            apart += any(focc(n1[0][x]) != focc(n2[0][x]) for x in n1[0])
            gph = UNITS[1]
            b3 = ({x: tuple(fm(gph, c) for c in v) for x, v in b[0].items()}, {x: tuple(fm(gph, c) for c in v) for x, v in b[1].items()})
            n3 = step(b3, dims, Fr(1, 4), Fr(1, 8))
            same_global += all(focc(n1[0][x]) == focc(n3[0][x]) for x in n1[0])
        check(f"torus {dims}: a Node-clock phase keeps every (rho, S) and moves the next tick's", apart == trials, f"{apart} of {trials}")
        check(f"torus {dims}: a global phase moves nothing (the control)", same_global == trials, f"{same_global} of {trials}")

    print("4. The step keeps W(u, v), moves the one-slot form; one quantum's two-slot occupation is not positive")
    dims = (3, 3, 2)
    hs = [rboard(dims) for _ in range(3)]
    W0 = [[W(a, b) for b in hs] for a in hs]
    L0 = [[L1(a, b) for b in hs] for a in hs]
    kept = moved = 0
    for _ in range(16):
        hs = [step(h, dims, Fr(1, 4), Fr(1, 8)) for h in hs]
        kept += [[W(a, b) for b in hs] for a in hs] == W0
        moved += [[L1(a, b) for b in hs] for a in hs] != L0
    check("W kept at every tick (3 x 3 entries, 16 ticks); the one-slot form moved", kept == 16 and moved > 0, f"kept {kept} of 16, moved {moved} of 16")
    n = neg = 0
    for _ in range(20000):
        nw, bf = rv(), rv()
        # D = i (b n^dagger ... ) as a 2 x 2 Hermitian: D_ac = i (conj(b_a) n_c - conj(n_a) b_c)
        D = [[None, None], [None, None]]
        for a in range(2):
            for c in range(2):
                t = s(m(cj(bf[a]), nw[c]), m(cj(nw[a]), bf[c]))
                D[a][c] = m((0, 1), t)
        detD = s(m(D[0][0], D[1][1]), m(D[0][1], D[1][0]))
        n += detD == (-nn(dt(nw, bf)), 0)
        neg += detD[0] < 0
    check("det D = -N(det[now, before]) exactly, so D has a negative eigenvalue wherever now and before are independent", n == 20000 and neg > 0, f"{n} of 20000, strictly indefinite at {neg}")

    n = 0
    for _ in range(20000):
        un, ub = rv(), rv()
        vn, vb = rev(ub), rev(un)  # the occupant's turnover image: the slots exchanged, T on each
        w_uv = s(ip(un, vb), ip(ub, vn))
        w_uu = s(ip(un, ub), ip(ub, un))
        w_vv = s(ip(vn, vb), ip(vb, vn))
        n += w_uv == O and w_vv == w_uu
    check("the occupant's turnover image (T before, T now) has W(u, v) = 0 and W(v, v) = W(u, u)", n == 20000, f"{n} of 20000")

    print("5. Sofer's bound against 0 <= n <= u")
    for u in (3, 4, 6):
        inside_bad = sofer_only = 0
        found = {}
        boxes = [box(2), box(3), box(4)]
        pending = []
        for R in range(0, 2 * u + 1):
            for S in product(range(-2 * u, 2 * u + 1), repeat=3):
                ss = dot3(S, S)
                if ss > R * R:
                    continue
                if ss <= (2 * u - R) ** 2:
                    inside_bad += any((2 * u - R) * rho(c) - dot3(S, spin(c)) < 0 for c in boxes[0])
                else:
                    sofer_only += 1
                    pending.append((R, S))
        for r, bx in zip((2, 3, 4), boxes):
            still = []
            for R, S in pending:
                if any((2 * u - R) * rho(c) - dot3(S, spin(c)) < 0 for c in bx):
                    found[r] = found.get(r, 0) + 1
                else:
                    still.append((R, S))
            pending = still
        cum = 0
        cums = []
        for r in (2, 3, 4):
            cum += found.get(r, 0)
            cums.append(cum)
        check(f"u = {u}: no negative free size inside |S| <= 2u - rho (newcomers in {{-2..2}}^4)", inside_bad == 0, inside_bad)
        print(f"    u = {u}: occupations inside Sofer's bound but outside 0 <= n <= u: {sofer_only}; shown negative with newcomers up to 2, 3, 4: {cums}; left {len(pending)}")
        built = 0
        for R, S in pending:
            chi = aimed(S, R, u)
            built += chi is not None and (2 * u - R) * rho(chi) - dot3(S, spin(chi)) < 0
        print(f"    the {len(pending)} left: a newcomer aimed along S by the inverse Hopf map shows a negative free size at {built} of {len(pending)}")
        check(f"u = {u}: every occupation inside Sofer's bound and outside 0 <= n <= u has a newcomer with a negative free size", len(pending) == built, f"{cums[-1] + built} of {sofer_only}")
    print("   (the theorem: free >= 0 for every newcomer iff the larger eigenvalue (rho + |S|)/2 <= u, by Cauchy-Schwarz and")
    print("    the density of Gaussian directions; with n >= 0 the full bound is |S| <= min(rho, 2u - rho), i.e. 0 <= n <= u)")


def mutants():
    bad = []

    def report(name, count, of):
        print(f"  {name}: {count} of {of} (must be above 0)")
        if count == 0:
            bad.append(name)

    print("M1. Sofer's bound taken as enough: the occupation (2u, (0, 0, 2u)), two quanta in one sense, must show a negative free size")
    u = 6
    report("newcomers in {-1..1}^4 with a negative free size", sum(1 for c in box(1) if (2 * u - 2 * u) * rho(c) - dot3((0, 0, 2 * u), spin(c)) < 0), len(box(1)))
    print("M2. the occupation taken as the state (stepped by a rule of its own): two boards equal in (rho, S) must still step apart")
    dims = (7,)
    c = 0
    for _ in range(6):
        b = rboard(dims)
        ph = {x: UNITS[x[0] % 4] for x in b[0]}
        b2 = ({x: tuple(fm(ph[x], cc) for cc in v) for x, v in b[0].items()}, {x: tuple(fm(ph[x], cc) for cc in v) for x, v in b[1].items()})
        n1, n2 = step(b, dims, Fr(1, 4), Fr(1, 8)), step(b2, dims, Fr(1, 4), Fr(1, 8))
        c += any(focc(n1[0][x]) != focc(n2[0][x]) for x in n1[0])
    report("boards whose next occupations differ (no rule on (rho, S) alone can step them)", c, 6)
    print("M3. the step made unequal on two quanta (one hand's grip changed): W must move")
    a, b = rboard(dims), rboard(dims)
    w0 = W(a, b)
    moved = 0
    for _ in range(5):
        a, b = step(a, dims, Fr(1, 4), Fr(1, 8)), step(b, dims, Fr(1, 3), Fr(1, 8))
        moved += W(a, b) != w0
    report("ticks with W moved", moved, 5)
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)

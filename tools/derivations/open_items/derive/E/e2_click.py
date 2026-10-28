"""Draft E, probe e2: the click of two equal quanta reads their two-quantum amplitude.

  python3 -I e2_click.py            the claims (must print 0 failures)
  python3 -I e2_click.py mutants    the mutations (each must fail)

Integers only: a Gaussian integer is a pair (re, im); a hand of the twin hands is a twin pair (z1, z2); a hand of a
one-hand train is one Gaussian integer. For quanta psi_1, psi_2 of one train and parts phi_a (a detector's senses, an
occupant's frame, or the two ends of a Mesh), M_aj = <phi_a, psi_j> and the joint click of the pair at the parts (a, b)
has the size sigma_ab = N(M_a1 M_b2 + eps M_b1 M_a2), eps the train's full turn (its half turn applied twice).
"""

from __future__ import annotations

import random
import sys
from itertools import permutations, product

FAIL = []
RNG = random.Random(20261028)


def check(name, ok, count=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if count is None else f": {count}"))


# ---- Gaussian integers ----
def gm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def ga(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gs(a, b):
    return (a[0] - b[0], a[1] - b[1])


def gc(a):
    return (a[0], -a[1])


def gn(a):
    return a[0] * a[0] + a[1] * a[1]


def gk(k, a):
    return (k * a[0], k * a[1])


ZERO, ONE, I = (0, 0), (1, 0), (0, 1)


def gsum(it):
    out = ZERO
    for v in it:
        out = ga(out, v)
    return out


# ---- twin pairs ----
def inner(phi, psi):
    return gsum(gm(gc(p), q) for p, q in zip(phi, psi, strict=True))


def det(u, v):
    return gs(gm(u[0], v[1]), gm(u[1], v[0]))


def rev(phi):
    """T, the phase reversal of the twin hands: (z1, z2) -> (-conj z2, conj z1)."""
    return (gk(-1, gc(phi[1])), gc(phi[0]))


def rho(phi):
    return sum(gn(z) for z in phi)


def spin(phi):
    c = gm(gc(phi[0]), phi[1])
    return (2 * c[0], 2 * c[1], gn(phi[0]) - gn(phi[1]))


def dot3(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def rg(k=9):
    return (RNG.randint(-k, k), RNG.randint(-k, k))


def rpair(k=9):
    while True:
        p = (rg(k), rg(k))
        if rho(p):
            return p


BOX = range(-2, 3)


def box_pairs():
    for a, b, c, d in product(BOX, repeat=4):
        p = ((a, b), (c, d))
        if rho(p):
            yield p


# ---- the joint click ----
def overlaps(parts, quanta):
    return [[inner(p, q) for q in quanta] for p in parts]


def amp(M, a, b, eps):
    return ga(gm(M[a][0], M[b][1]), gk(eps, gm(M[b][0], M[a][1])))


def sizes(M, eps):
    K = len(M)
    return {(a, b): gn(amp(M, a, b, eps)) for a in range(K) for b in range(K)}


def herm(parts):
    """G = SUM_a phi_a phi_a^dagger, as a 2 x 2 matrix of Gaussian integers."""
    return [[gsum(gm(p[r], gc(p[c])) for p in parts) for c in range(2)] for r in range(2)]


def form(G, u, v):
    """u^dagger G v."""
    return gsum(gm(gc(u[r]), gm(G[r][c], v[c])) for r in range(2) for c in range(2))


def main_claims():
    print("1. The exchange: a unit eps with N(eps) = 1 and eps eps = 1 (the double swap) is +1 or -1")
    units = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    ok = [u for u in units if gn(u) == 1 and gm(u, u) == ONE]
    check("the units with eps eps = 1", ok == [(1, 0), (-1, 0)], ok)

    print("2. eps_T read as the train's half turn applied twice, every act exact on integers")
    halves = {
        "x": lambda p: (gm((0, -1), p[1]), gm((0, -1), p[0])),
        "y": lambda p: (gk(-1, p[1]), p[0]),
        "z": lambda p: (gm((0, -1), p[0]), gm((0, 1), p[1])),
    }
    for axis, h in halves.items():
        n = 0
        for _ in range(5000):
            p = rpair()
            n += h(h(p)) == (gk(-1, p[0]), gk(-1, p[1]))
        check(f"twin hands: H_{axis}(H_{axis}(psi)) = -psi", n == 5000, f"{n} of 5000")
    hp = [halves[a] for a in "xyz"]
    anti = all(
        hp[i](hp[j](p)) == tuple(gk(-1, z) for z in hp[j](hp[i](p)))
        for i in range(3)
        for j in range(3)
        if i != j
        for p in [rpair() for _ in range(200)]
    )
    check("twin hands: the half turns about two axes anticommute", anti, "6 ordered pairs x 200")
    face = [((1, 0, 0), (0, -1, 0), (0, 0, -1)), ((-1, 0, 0), (0, 1, 0), (0, 0, -1)), ((-1, 0, 0), (0, -1, 0), (0, 0, 1))]
    edge = [((0, 1, 0), (1, 0, 0), (0, 0, -1)), ((0, 0, 1), (0, -1, 0), (1, 0, 0)), ((-1, 0, 0), (0, 0, 1), (0, 1, 0))]
    sq = all(mm(m, m) == ((1, 0, 0), (0, 1, 0), (0, 0, 1)) for m in face + edge)
    check("the 24's T1 gears (the offset's odd gears): every half turn squared is the identity", sq, len(face + edge))
    check("a one-hand train (A1): the 24 act on its own part as 1, so its half turn squared is +1", True)

    print("3. Pauli: sigma_aa = N((1 + eps) M_a1 M_a2): 0 for the twin hands, 4 N(M_a1 M_a2) for eps = +1")
    zero = bunch = 0
    for _ in range(20000):
        parts = [rpair(), rpair()]
        M = overlaps(parts, [rpair(), rpair()])
        zero += all(sizes(M, -1)[(a, a)] == 0 for a in range(2))
        bunch += all(sizes(M, 1)[(a, a)] == 4 * gn(gm(M[a][0], M[a][1])) for a in range(2))
    check("eps = -1: both parts' sigma_aa = 0", zero == 20000, f"{zero} of 20000")
    check("eps = +1: sigma_aa = 4 N(M_a1 M_a2) (bunching)", bunch == 20000, f"{bunch} of 20000")

    print("4. The books over a complete set of parts: SUM_(a,b) sigma_ab = 2 lam^2 (rho1 rho2 + eps N(<psi1, psi2>))")
    for label, maker in (
        ("the occupant's frame (phi, T phi), lam = rho(phi)", lambda: (lambda f: ([f, rev(f)], rho(f)))(rpair())),
        ("the standard senses ((1,0), (0,1)), lam = 1", lambda: ([(ONE, ZERO), (ZERO, ONE)], 1)),
        (
            "a Gaussian frame [[a, -conj b], [b, conj a]], lam = N(a) + N(b)",
            lambda: (lambda a, b: ([(a, b), (gk(-1, gc(b)), gc(a))], gn(a) + gn(b)))(rg(), rg()),
        ),
    ):
        n = 0
        for _ in range(10000):
            parts, lam = maker()
            if lam == 0:
                parts, lam = [(ONE, ZERO), (ZERO, ONE)], 1
            q1, q2 = rpair(), rpair()
            M = overlaps(parts, [q1, q2])
            n += all(
                sum(sizes(M, e).values()) == 2 * lam * lam * (rho(q1) * rho(q2) + e * gn(inner(q1, q2)))
                for e in (1, -1)
            )
        check(label, n == 10000, f"{n} of 10000 (both eps)")
    n = nb = 0
    for _ in range(10000):
        parts = [rpair(), rpair(), rpair()]
        q1, q2 = rpair(), rpair()
        M = overlaps(parts, [q1, q2])
        G = herm(parts)
        a, b, c = form(G, q1, q1)[0], form(G, q2, q2)[0], gn(form(G, q1, q2))
        n += all(sum(sizes(M, e).values()) == 2 * (a * b + e * c) for e in (1, -1))
        minors = sum(gn(gs(gm(M[i][0], M[j][1]), gm(M[j][0], M[i][1]))) for i in range(3) for j in range(i + 1, 3))
        nb += minors == a * b - c
    check("any three parts: SUM sigma = 2 [(psi1 G psi1)(psi2 G psi2) + eps N(psi1 G psi2)], G = SUM phi phi^dagger", n == 10000, f"{n} of 10000")
    check("Cauchy-Binet (eps = -1): SUM_(a<b) N(minor_ab) = det(M^dagger M)", nb == 10000, f"{nb} of 10000")

    print("5. At one Node-clock (the parts its two senses): two twin quanta only in the singlet, of size N(det)")
    n = indep = 0
    for _ in range(10000):
        q1, q2 = rpair(), rpair()
        vals = set()
        good = True
        for _f in range(5):
            f = rpair()
            s = sizes(overlaps([f, rev(f)], [q1, q2]), -1)
            r2 = rho(f) * rho(f)
            good &= s[(0, 0)] == 0 and s[(1, 1)] == 0 and s[(0, 1)] == s[(1, 0)] == r2 * gn(det(q1, q2))
            vals.add((s[(0, 1)], r2))
        n += good
        indep += len({v // r for v, r in vals}) == 1
    check("sigma_++ = sigma_-- = 0, sigma_+- = sigma_-+ = rho(phi)^2 N(det[psi1, psi2])", n == 10000, f"{n} of 10000 pairs x 5 frames")
    check("the singlet's size is the same in every frame (it is the A1)", indep == 10000, f"{indep} of 10000")

    print("6. A third twin quantum at one Node-clock has no state (the 3 x 3 Slater amplitude over two senses is 0)")
    n = nb = 0
    for _ in range(3000):
        f = rpair()
        parts = [f, rev(f)]
        qs = [rpair(), rpair(), rpair()]
        M = overlaps(parts, qs)
        n += all(slater(M, rows, -1) == ZERO for rows in product(range(2), repeat=3))
        nb += any(slater(M, rows, 1) != ZERO for rows in product(range(2), repeat=3))
    check("eps = -1: all 8 assignments of three quanta to two senses have amplitude 0", n == 3000, f"{n} of 3000")
    check("eps = +1 (control): some assignment is not 0", nb == 3000, f"{nb} of 3000")

    print("7. Law 5's q per state: the q-quantum amplitude in one part is PROD M times SUM_pi eps^inv(pi)")
    for q in range(2, 8):
        s_minus = sum((-1) ** inversions(p) for p in permutations(range(q)))
        s_plus = sum(1 for _ in permutations(range(q)))
        check(f"q = {q}: SUM sgn = {s_minus} (must be 0), SUM 1 = {s_plus} (q!)", s_minus == 0 and s_plus == fact(q))

    print("8. Bunching at a Mesh (a one-hand train, the parts the two ends): a balanced splitter gives no coincidence")
    M = [[ONE, I], [I, ONE]]  # psi1 = (1, i), psi2 = (i, 1) read at the ends x, y
    b, f = sizes(M, 1), sizes(M, -1)
    dist = gn(gm(M[0][0], M[1][1])) + gn(gm(M[1][0], M[0][1]))
    check("eps = +1: sigma_xy = 0, sigma_xx = sigma_yy = 4", b[(0, 1)] == 0 and b[(1, 0)] == 0 and b[(0, 0)] == 4 and b[(1, 1)] == 4, b)
    check("probabilities added (distinguishable): the coincidence 2; eps = -1: sigma_xy = 4, sigma_xx = 0", dist == 2 and f[(0, 1)] == 4 and f[(0, 0)] == 0, (dist, f))
    order = zero_iff = seen = 0
    for _ in range(20000):
        a, c = rg(), rg()
        if gn(a) + gn(c) == 0:
            continue
        seen += 1
        M = [[a, gk(-1, gc(c))], [c, gc(a)]]
        tot = (gn(a) + gn(c)) ** 2
        bos = sizes(M, 1)
        fer = sizes(M, -1)
        cb = bos[(0, 1)] + bos[(1, 0)]
        cf = fer[(0, 1)] + fer[(1, 0)]
        cd = 2 * (gn(gm(M[0][0], M[1][1])) + gn(gm(M[1][0], M[0][1])))
        order += cb <= cd <= cf and sum(bos.values()) == 2 * tot == sum(fer.values()) and cf == 2 * tot
        zero_iff += (cb == 0) == (gn(a) == gn(c))
    check("coincidences: bosons <= distinguishable <= fermions = all, the totals 2 (N(a) + N(b))^2", order == seen, f"{order} of {seen} splitters")
    check("the bosons' coincidence is 0 exactly where the splitter is balanced, N(a) = N(b)", zero_iff == seen, f"{zero_iff} of {seen}")

    print("9. Sofer's occupant frame is the same act: the pair's joint click with the occupant phi and the newcomer chi")
    n = 0
    for phi in box_pairs():
        for chi in (((1, 0), (0, 1)), ((0, 1), (2, -1)), ((-1, 1), (1, 1)), phi, rev(phi), ((2, 0), (0, 0))):
            s = sizes(overlaps([phi, rev(phi)], [phi, chi]), -1)
            free, blocked = gn(inner(rev(phi), chi)), gn(inner(phi, chi))
            r = rho(phi)
            dist = 2 * r * r * r * rho(chi)
            n += (
                s[(0, 1)] + s[(1, 0)] == 2 * r * r * free
                and s[(0, 0)] + s[(1, 1)] == 0
                and dist - sum(s.values()) == 2 * r * r * blocked
                and free + blocked == r * rho(chi)
                and free == gn(det(phi, chi))
            )
    total = sum(1 for _ in box_pairs()) * 6
    check("2Q free = 2 rho^2 N(<T phi, chi>), 2Q same = 0, deficit = 2 rho^2 N(<phi, chi>), room rho rho_chi", n == total, f"{n} of {total}")

    print("10. The occupation n = SUM_k psi_k psi_k^dagger = (rho + S . sigma) / 2: Sofer's sizes are the hole projector")
    n = n1 = n2 = 0
    for _ in range(20000):
        k = RNG.randint(1, 3)
        qs = [rpair(4) for _ in range(k)]
        R = sum(rho(q) for q in qs)
        Sv = tuple(sum(spin(q)[i] for q in qs) for i in range(3))
        chi = rpair(5)
        m = spin(chi)
        nchi = sum(gn(inner(q, chi)) for q in qs)  # chi^dagger n chi
        u = RNG.randint(1, 40)
        n += 2 * nchi == R * rho(chi) + dot3(Sv, m) and (2 * u - R) * rho(chi) - dot3(Sv, m) == 2 * (u * rho(chi) - nchi)
    check("chi^dagger n chi = (rho rho_chi + S . m) / 2, so free = (2u - rho) rho_chi - S . m = 2 chi^dagger (u - n) chi", n == 20000, f"{n} of 20000")
    for phi in box_pairs():
        u = rho(phi)
        for chi in box_pairs():
            m = spin(chi)
            one = (2 * u - u) * rho(chi) - dot3(spin(phi), m)
            full = (2 * u - 2 * u) * rho(chi) - dot3(tuple(a + b for a, b in zip(spin(phi), spin(rev(phi)), strict=True)), m)
            n1 += one == 2 * gn(det(phi, chi))
            n2 += full == 0
    tot = sum(1 for _ in box_pairs()) ** 2
    check("one quantum there (rho = u): free = 2 N(det[phi, chi])", n1 == tot, f"{n1} of {tot}")
    check("the filled orbital (phi and T phi, rho = 2u, S = 0): free = 0 for every newcomer", n2 == tot, f"{n2} of {tot}")

    print("11. The bound: free >= 0 for every newcomer iff S . S <= (2u - rho)^2 (the larger eigenvalue at most u)")
    u = 6
    newcomers = list(box_pairs())
    mine_bad = sofer_only = sofer_only_neg = 0
    for R in range(0, 2 * u + 1):
        for Sv in product(range(-2 * u, 2 * u + 1), repeat=3):
            ss = dot3(Sv, Sv)
            if ss > R * R:
                continue  # not an occupation: n would not be positive
            neg = any((2 * u - R) * rho(c) - dot3(Sv, spin(c)) < 0 for c in newcomers)
            if ss <= (2 * u - R) ** 2:
                mine_bad += neg
            else:
                sofer_only += 1
                sofer_only_neg += neg
    check("occupations inside S . S <= (2u - rho)^2 with a negative free size", mine_bad == 0, mine_bad)
    check(
        "occupations inside Sofer's |S| <= rho <= 2u but outside it, with a negative free size in the box",
        sofer_only_neg > 0,
        f"{sofer_only_neg} of {sofer_only} (Sofer's bound is not enough; e.g. (2u, (0, 0, 2u)))",
    )
    bad = 0
    for R in range(0, 13):
        for Sv in product(range(-4, 5), repeat=3):
            if dot3(Sv, Sv) <= R * R:
                bad += any(R * rho(c) + dot3(Sv, spin(c)) < 0 for c in newcomers)
    check("blocked = rho rho_chi + S . m >= 0 for every newcomer wherever S . S <= rho^2", bad == 0, bad)


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def inversions(p):
    return sum(1 for i in range(len(p)) for j in range(i + 1, len(p)) if p[i] > p[j])


def fact(q):
    out = 1
    for k in range(2, q + 1):
        out *= k
    return out


def slater(M, rows, eps):
    """The 3-quantum amplitude with quantum j at part rows[j]: SUM_pi eps^inv(pi) PROD_j M[rows[j]][pi(j)]."""
    out = ZERO
    for p in permutations(range(3)):
        t = ONE
        for j in range(3):
            t = gm(t, M[rows[j]][p[j]])
        out = ga(out, gk(eps ** inversions(p), t))
    return out


def mutants():
    bad = []

    def report(name, count, of):
        print(f"  {name}: {count} of {of} (must be above 0)")
        if count == 0:
            bad.append(name)

    print("M1. eps = +1 on the twin hands: sigma_aa must stop being 0")
    c = sum(1 for _ in range(2000) for M in [overlaps([rpair(), rpair()], [rpair(), rpair()])] if sizes(M, 1)[(0, 0)] > 0)
    report("twin pairs with sigma_aa > 0", c, 2000)
    print("M2. probabilities added (no amplitude sum): sigma_aa = 2 N(M_a1) N(M_a2) must stop being 0")
    c = sum(1 for _ in range(2000) for M in [overlaps([rpair(), rpair()], [rpair(), rpair()])] if 2 * gn(M[0][0]) * gn(M[0][1]) > 0)
    report("pairs with the same part's size above 0", c, 2000)
    print("M3. the exchange term conjugated (the head's K on the second way): Pauli and the books must fail")
    cp = cb = 0
    for _ in range(2000):
        q1, q2 = rpair(), rpair()
        f = rpair()
        M = overlaps([f, rev(f)], [q1, q2])
        s = {(a, b): gn(ga(gm(M[a][0], M[b][1]), gk(-1, gc(gm(M[b][0], M[a][1]))))) for a in range(2) for b in range(2)}
        cp += s[(0, 0)] > 0
        cb += sum(s.values()) != 2 * rho(f) ** 2 * (rho(q1) * rho(q2) - gn(inner(q1, q2)))
    report("pairs with sigma_aa > 0", cp, 2000)
    report("pairs whose books fail", cb, 2000)
    print("M4. the parts left unexchanged (A = M_a1 M_a2 + eps M_b1 M_b2): the books must fail")
    c = 0
    for _ in range(2000):
        q1, q2 = rpair(), rpair()
        f = rpair()
        M = overlaps([f, rev(f)], [q1, q2])
        s = sum(gn(ga(gm(M[a][0], M[a][1]), gk(-1, gm(M[b][0], M[b][1])))) for a in range(2) for b in range(2))
        c += s != 2 * rho(f) ** 2 * (rho(q1) * rho(q2) - gn(inner(q1, q2)))
    report("pairs whose books fail", c, 2000)
    print("M5. K's partner in the occupant's frame (K phi = conj phi in place of T phi): the same state must stay free")
    c = sum(1 for p in box_pairs() if gn(inner((gc(p[0]), gc(p[1])), p)) > 0)
    report("hands with N(<K phi, phi>) > 0", c, sum(1 for _ in box_pairs()))
    print("M6. the capacity u in place of 2u: free sizes must go negative; 3u: a third quantum must be free")
    neg = third = tried = 0
    for phi in box_pairs():
        u = rho(phi)
        for chi in [rpair(3) for _ in range(6)]:
            tried += 1
            neg += (u - u) * rho(chi) - dot3(spin(phi), spin(chi)) < 0
            third += (3 * u - 2 * u) * rho(chi) > 0
    report("negative free sizes with the capacity u", neg, tried)
    report("a third quantum free with the capacity 3u (the filled orbital 2u, S = 0)", third, tried)
    print("N1. not a mutation: the sign on the other term (eps M_a1 M_b2 + M_b1 M_a2) keeps every size, N(eps x + y) = N(x + eps y)")
    same = 0
    for _ in range(2000):
        M = overlaps([rpair(), rpair()], [rpair(), rpair()])
        same += all(
            gn(ga(gk(-1, gm(M[a][0], M[b][1])), gm(M[b][0], M[a][1]))) == sizes(M, -1)[(a, b)]
            for a in range(2)
            for b in range(2)
        )
    print(f"  pairs with every size unchanged: {same} of 2000 (it must be 2000: this change cannot fail, by N(-w) = N(w))")
    if same != 2000:
        bad.append("N1")
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main_claims()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)

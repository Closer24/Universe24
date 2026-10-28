"""Draft E, probe e4: what the board must hold so that a click is Pauli.

  python3 -I e4_board.py            the claims (must print 0 failures)
  python3 -I e4_board.py mutants    the mutations (each must fail)

1. One twin pair per train and Node-clock (the head's board) cannot hold two quanta: their sum is one spinor.
2. One hand per quantum: the occupation n(x) = SUM_k psi_k(x) psi_k(x)^dagger is a reading at x; Bessel's bound.
3. The one formula's linear step keeps the quanta's mutual two-slot form W(u, v) exactly (no carries; Fractions).
4. A child set at one Node-clock meets every quantum's hand there alone; the occupant's turnover image (the slots
   exchanged and T) is exactly orthogonal to the occupant in the two-slot form: the free partner is the phase reversal.
Integers and Fractions only.
"""

from __future__ import annotations

import random
import sys
from fractions import Fraction as Fr
from itertools import product

FAIL = []
RNG = random.Random(2810)


def check(name, ok, count=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if count is None else f": {count}"))


def gm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def ga(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gs(a, b):
    return (a[0] - b[0], a[1] - b[1])


def gc(a):
    return (a[0], -a[1])


def gk(k, a):
    return (k * a[0], k * a[1])


def gn(a):
    return a[0] * a[0] + a[1] * a[1]


ZERO = (0, 0)


def inner(u, v):
    out = ZERO
    for p, q in zip(u, v, strict=True):
        out = ga(out, gm(gc(p), q))
    return out


def det(u, v):
    return gs(gm(u[0], v[1]), gm(u[1], v[0]))


def T(v):
    return (gk(-1, gc(v[1])), gc(v[0]))


def K(v):
    return (gc(v[0]), gc(v[1]))


def rho(v):
    return sum(gn(z) for z in v)


def spin(v):
    c = gm(gc(v[0]), v[1])
    return (2 * c[0], 2 * c[1], gn(v[0]) - gn(v[1]))


def add2(u, v):
    return (ga(u[0], v[0]), ga(u[1], v[1]))


def rg(k=9):
    return (RNG.randint(-k, k), RNG.randint(-k, k))


def rpair(k=9):
    while True:
        p = (rg(k), rg(k))
        if rho(p):
            return p


def box_pairs(r=2):
    for a, b, c, d in product(range(-r, r + 1), repeat=4):
        if (a, b, c, d) != (0, 0, 0, 0):
            yield ((a, b), (c, d))


def occupation(quanta):
    """n = SUM psi psi^dagger read as (rho, S)."""
    R = sum(rho(q) for q in quanta)
    S = tuple(sum(spin(q)[i] for q in quanta) for i in range(3))
    return R, S


def dot3(a, b):
    return sum(x * y for x, y in zip(a, b, strict=True))


def main_claims():
    print("1. One twin pair per train at a Node-clock (the head's board) cannot hold two quanta")
    pairs = list(box_pairs())
    pure = sum(dot3(spin(add2(p, T(p))), spin(add2(p, T(p)))) == rho(add2(p, T(p))) ** 2 for p in pairs)
    check("the filled orbital summed into one spinor, psi = phi + T phi, is a pure spinor: S . S = rho^2 (not S = 0)", pure == len(pairs), f"{pure} of {len(pairs)}")
    third = tried = 0
    for p in pairs:
        psi = add2(p, T(p))
        for c in pairs[::13]:
            tried += 1
            third += gn(det(psi, c)) > 0
    check("so a third newcomer finds a free size N(det[phi + T phi, chi]) > 0 (it must be 0 for the filled orbital)", third > 0, f"{third} of {tried}")
    same = coh = 0
    for _ in range(5000):
        q = rpair()
        parts = [rpair(), rpair()]
        M = [[inner(f, q), inner(f, q)] for f in parts]  # two quanta in one state
        two_q = [gn(ga(gm(M[a][0], M[b][1]), gk(-1, gm(M[b][0], M[a][1])))) for a in range(2) for b in range(2)]
        field = add2(q, q)
        prod_ = [gn(gm(inner(parts[a], field), inner(parts[b], field))) for a in range(2) for b in range(2)]
        same += all(x == 0 for x in two_q)
        coh += any(x > 0 for x in prod_)
    check("two quanta in one state: the two-quantum amplitude is 0 at every pair of parts", same == 5000, f"{same} of 5000")
    check("the summed field's product at the parts is not 0: the board's sum has lost the two ways", coh == 5000, f"{coh} of 5000")
    lost = sum(rho(add2(p, (gk(-1, p[0]), gk(-1, p[1])))) == 0 and 2 * rho(p) > 0 for p in pairs)
    check("the plan's law 7, psi + (-psi) = 0: the wind of two quanta goes to 0 while two are booked (the books fail)", lost == len(pairs), f"{lost} of {len(pairs)}")

    print("2. One hand per quantum: n(x) is a reading of the quanta's hands at x")
    psd = 0
    for _ in range(20000):
        R, S = occupation([rpair(5) for _ in range(RNG.randint(1, 4))])
        psd += dot3(S, S) <= R * R
    check("|S| <= rho for any sum of quanta (n is positive)", psd == 20000, f"{psd} of 20000")
    F4 = [[pow_i(j * k) for k in range(4)] for j in range(4)]
    H2 = [[1, 1], [1, -1]]
    rows = [[gk(H2[a][b], F4[j][k]) for k in range(4) for b in range(2)] for j in range(4) for a in range(2)]
    ortho = all(sum_inner(rows[r], rows[s]) == ((8, 0) if r == s else ZERO) for r in range(8) for s in range(8))
    check("eight orthogonal quanta on four Node-clocks x two senses (F4 x H2, entries 1, -1, i, -i), each of norm 8", ortho)
    u, worst = 8, 0
    good = 0
    for mask in range(1, 256):
        chosen = [rows[r] for r in range(8) if mask >> r & 1]
        ok = True
        for x in range(4):
            R, S = occupation([(q[2 * x], q[2 * x + 1]) for q in chosen])
            ok &= dot3(S, S) <= (2 * u - R) ** 2 and R <= 2 * u
        good += ok
    check("Bessel: every one of the 255 sets of orthogonal quanta keeps n(x) <= u at every Node-clock (S . S <= (2u - rho)^2)", good == 255, f"{good} of 255")
    full = all(occupation([(q[2 * x], q[2 * x + 1]) for q in rows]) == (2 * u, (0, 0, 0)) for x in range(4))
    check("all eight: the filled band, rho = 2u and S = 0 at every Node-clock (two per Node-clock, one per sense)", full)
    local = [[(1, 0) if i == r else ZERO for i in range(8)] for r in range(8)]
    goodl = 0
    for mask in range(1, 256):
        chosen = [local[r] for r in range(8) if mask >> r & 1]
        ok = True
        for x in range(4):
            R, S = occupation([(q[2 * x], q[2 * x + 1]) for q in chosen])
            ok &= dot3(S, S) <= (2 - R) ** 2 and R <= 2
        goodl += ok
    check("the same for quanta held at one Node-clock each (the eight unit hands, u = 1): 255 sets", goodl == 255, f"{goodl} of 255")

    print("3. The one formula's linear step keeps the quanta's mutual two-slot form W(u, v) exactly")
    side, ticks = 4, 24
    g, d = Fr(1, 4), Fr(1, 8)
    hands = [random_field(side) for _ in range(3)]
    W0 = [[wform(hands[a], hands[b]) for b in range(3)] for a in range(3)]
    L0 = [[l2(hands[a], hands[b]) for b in range(3)] for a in range(3)]
    kept = moved = 0
    for t in range(ticks):
        hands = [step(h, side, g, d) for h in hands]
        W = [[wform(hands[a], hands[b]) for b in range(3)] for a in range(3)]
        L = [[l2(hands[a], hands[b]) for b in range(3)] for a in range(3)]
        kept += W == W0
        moved += L != L0
    check(f"W(u, v) = SUM_x <u_now, v_before> - <u_before, v_now> kept at every tick, 3 x 3 entries, {ticks} ticks", kept == ticks, f"{kept} of {ticks}")
    check("the one-slot form SUM_x <u_now, v_now> is not kept (the conserved form is the two-slot one)", moved > 0, f"moved at {moved} of {ticks} ticks")

    print("4. The lay is local, and the free partner is the occupant's turnover image")
    loc = 0
    for _ in range(200):
        h = random_field(side)
        x0 = (RNG.randrange(side), RNG.randrange(side), RNG.randrange(side))
        child_n, child_b = rpair(), rpair()
        child = local_field(side, x0, child_n, child_b)
        w_glob = wform(h, child)
        n0, b0 = h[0][x0], h[1][x0]
        w_loc = ga(inner(n0, child_b), gk(-1, inner(b0, child_n)))
        loc += w_glob == (Fr(w_loc[0]), Fr(w_loc[1]))
    check("a child set at one Node-clock meets a spread hand at that Node-clock alone (the global form = its local term)", loc == 200, f"{loc} of 200")
    part = same_charge = 0
    for _ in range(20000):
        un, ub = rpair(), rpair()
        vn, vb = T(ub), T(un)  # the turnover image: the slots exchanged and T
        w = ga(inner(un, vb), gk(-1, inner(ub, vn)))
        part += w == ZERO
        wuu = ga(inner(un, ub), gk(-1, inner(ub, un)))
        wvv = ga(inner(vn, vb), gk(-1, inner(vb, vn)))
        same_charge += wuu == wvv
    check("W(occupant, its turnover image) = <u_now, T u_now> - <u_before, T u_before> = 0 (Kramers on each slot)", part == 20000, f"{part} of 20000")
    check("the image carries the occupant's own two-slot charge W(v, v) = W(u, u): an equal quantum, the other sense", same_charge == 20000, f"{same_charge} of 20000")

    print("5. The occupation is no state: two boards with the same occupation at every Node-clock step apart")
    apart = 0
    for _ in range(20):
        h = random_field(side)
        phase = {x: [(Fr(1), Fr(0)), (Fr(0), Fr(1)), (Fr(-1), Fr(0)), (Fr(0), Fr(-1))][(x[0] + 2 * x[1]) % 4] for x in h[0]}
        h2 = ({x: tuple(fmul(phase[x], c) for c in v) for x, v in h[0].items()}, {x: tuple(fmul(phase[x], c) for c in v) for x, v in h[1].items()})
        same0 = all(focc(h[0][x]) == focc(h2[0][x]) for x in h[0])
        n1, n2 = step(h, side, g, d), step(h2, side, g, d)
        apart += same0 and any(focc(n1[0][x]) != focc(n2[0][x]) for x in n1[0])
    check("a Node-clock phase i^(x + 2y) keeps every occupation (rho, S) and changes the next tick's", apart == 20, f"{apart} of 20 boards")

    print("6. The two-slot occupation of one quantum is not positive: S . S - W W = 4 N(det[now, before]) >= 0 (draft D's P2)")
    ok = strict = 0
    for _ in range(20000):
        nw, bf = rpair(), rpair()
        c = gs(gm(gc(bf[0]), nw[1]), gm(gc(nw[0]), bf[1]))  # conj(b_u) n_d - conj(n_u) b_d
        Duu = gs(gm(gc(bf[0]), nw[0]), gm(gc(nw[0]), bf[0]))
        Ddd = gs(gm(gc(bf[1]), nw[1]), gm(gc(nw[1]), bf[1]))
        # D_ac = i (conj(b_a) n_c - conj(n_a) b_c): the diagonal is real: i times a pure imaginary
        W = -(Duu[1] + Ddd[1])
        Sx, Sy, Sz = -2 * c[1], -2 * c[0], -(Duu[1] - Ddd[1])
        lhs = Sx * Sx + Sy * Sy + Sz * Sz - W * W
        ok += lhs == 4 * gn(det(nw, bf))
        strict += lhs > 0
    check("S . S - W^2 = 4 N(det[now, before]) for one quantum's two slots", ok == 20000, f"{ok} of 20000")
    check("so its smaller eigenvalue (W - |S|) / 2 is below 0 wherever det[now, before] != 0", strict > 0, f"{strict} of 20000")


def fmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def focc(v):
    """(rho, S) of one twin pair with Fraction coefficients."""
    c = fmul((v[0][0], -v[0][1]), v[1])
    n1 = v[0][0] ** 2 + v[0][1] ** 2
    n2 = v[1][0] ** 2 + v[1][1] ** 2
    return (n1 + n2, 2 * c[0], 2 * c[1], n1 - n2)


def pow_i(k):
    return [(1, 0), (0, 1), (-1, 0), (0, -1)][k % 4]


def sum_inner(u, v):
    out = ZERO
    for p, q in zip(u, v, strict=True):
        out = ga(out, gm(gc(p), q))
    return out


def random_field(side):
    """A twin hand over the torus: (now, before), each a dict site -> twin pair, Fraction coefficients."""
    sites = list(product(range(side), repeat=3))
    now = {s: tuple((Fr(RNG.randint(-5, 5)), Fr(RNG.randint(-5, 5))) for _ in range(2)) for s in sites}
    before = {s: tuple((Fr(RNG.randint(-5, 5)), Fr(RNG.randint(-5, 5))) for _ in range(2)) for s in sites}
    return (now, before)


def local_field(side, x0, n, b):
    sites = list(product(range(side), repeat=3))
    zero = ((Fr(0), Fr(0)), (Fr(0), Fr(0)))
    now = {s: zero for s in sites}
    before = {s: zero for s in sites}
    now[x0] = tuple((Fr(z[0]), Fr(z[1])) for z in n)
    before[x0] = tuple((Fr(z[0]), Fr(z[1])) for z in b)
    return (now, before)


def neighbours(s, side):
    for a in range(3):
        for e in (1, -1):
            t = list(s)
            t[a] = (t[a] + e) % side
            yield tuple(t)


def step(h, side, g, d):
    """The one formula's linear step without carries, alike on both twins: a+ = 2a - a- + g SUM_j (a_j - a) - d a."""
    now, before = h
    new = {}
    for s, v in now.items():
        comps = []
        for c in range(2):
            lap = [Fr(0), Fr(0)]
            for t in neighbours(s, side):
                lap[0] += now[t][c][0] - v[c][0]
                lap[1] += now[t][c][1] - v[c][1]
            comps.append(tuple(2 * v[c][k] - before[s][c][k] + g * lap[k] - d * v[c][k] for k in range(2)))
        new[s] = tuple(comps)
    return (new, now)


def finner(u, v):
    re = im = Fr(0)
    for p, q in zip(u, v, strict=True):
        re += p[0] * q[0] + p[1] * q[1]
        im += p[0] * q[1] - p[1] * q[0]
    return (re, im)


def wform(u, v):
    re = im = Fr(0)
    for s in u[0]:
        a = finner(u[0][s], v[1][s])
        b = finner(u[1][s], v[0][s])
        re += a[0] - b[0]
        im += a[1] - b[1]
    return (re, im)


def l2(u, v):
    re = im = Fr(0)
    for s in u[0]:
        a = finner(u[0][s], v[0][s])
        re += a[0]
        im += a[1]
    return (re, im)


def mutants():
    bad = []

    def report(name, count, of):
        print(f"  {name}: {count} of {of} (must be above 0)")
        if count == 0:
            bad.append(name)

    print("M1. Two equal quanta held at one Node-clock (not orthogonal): Bessel's bound must fail")
    local = [[(1, 0) if i == r else ZERO for i in range(8)] for r in range(8)]
    over = 0
    for r in range(8):
        chosen = [local[r], local[r]]
        for x in range(4):
            R, S = occupation([(q[2 * x], q[2 * x + 1]) for q in chosen])
            over += dot3(S, S) > (2 - R) ** 2
    report("Node-clocks where an equal pair exceeds one quantum in one sense", over, "8 pairs x 4 Node-clocks")
    print("M2. The head's K at the turnover in place of T: the image must stop being orthogonal to the occupant")
    c = 0
    for _ in range(5000):
        un, ub = rpair(), rpair()
        vn, vb = K(ub), K(un)
        c += ga(inner(un, vb), gk(-1, inner(ub, vn))) != ZERO
    report("occupants with W(u, K image) != 0", c, 5000)
    print("M3. The partner without the slot exchange (T on each slot in place): W must stop being 0")
    c = 0
    for _ in range(5000):
        un, ub = rpair(), rpair()
        vn, vb = T(un), T(ub)
        c += ga(inner(un, vb), gk(-1, inner(ub, vn))) != ZERO
    report("occupants with W(u, T in place) != 0", c, 5000)
    print("M4. A step that is not the same on the two quanta (one hand's grip changed): W(u, v) must move")
    side = 4
    a, b = random_field(side), random_field(side)
    w0 = wform(a, b)
    moved = 0
    for _ in range(6):
        a = step(a, side, Fr(1, 4), Fr(1, 8))
        b = step(b, side, Fr(1, 5), Fr(1, 8))
        moved += wform(a, b) != w0
    report("ticks with W moved", moved, 6)
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main_claims()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)

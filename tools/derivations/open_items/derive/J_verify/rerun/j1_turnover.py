"""Draft J, probe j1: route a, the turnover (the phase reversal on the board) and the click of two equal quanta.

  python3 -I j1_turnover.py            the claims (must end with 0 failures)
  python3 -I j1_turnover.py mutants    the mutations (each must fail)

Gaussian integers as (re, im) pairs of ints; no float anywhere.
1. Run back (parts and quanta turned over, the quanta's order reversed, antiunitary): every joint size
   sigma_ab = N(M_a1 M_b2 + eps M_b1 M_a2) is kept, for eps = +1 AND eps = -1. The turnover chooses nothing at parts.
2. The pair's one directionless pairing B(u, v) = <T u, v> (det on twin hands, the product on a hand, the dot on
   vectors) under the turnover: B(T u, T v) = conj B(u, v); with the order reversed, B(T v, T u) = (T T) conj B(u, v).
3. The A1 part Q = B(u, v) + eps B(v, u) of two equal quanta, run back with the order reversed and compensated by eps:
   eps conj Q(T v, T u) = (eps T T) Q. So "the same law run back" holds with Q not 0 iff eps = T T; for eps = -T T
   the pair has no A1 part at all (Q = 0), and the condition is empty: the turnover reduces to the A1 premise.
4. The A1 pair Omega_T = SUM_k e_k x T e_k: the exchange of its two quanta is the double turnover, P Omega = (T T) Omega;
   on the pair's dial the exchange is the full turn of one quantum: B(v, u) = B(u, z v).
5. Superselection: every act linear and alike on each quantum (the step, the hop, the turnover) commutes with the
   exchange, so the board's dynamics keeps both two-quantum sectors and never picks one.
"""

from __future__ import annotations

import random
import sys
from itertools import product

FAIL = []
RNG = random.Random(24_2026_1028)


def check(name, ok, info=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if info is None else f": {info}"))


# --- Gaussian integers -----------------------------------------------------------------------------------------
Z0 = (0, 0)


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


def rg(k=6):
    return (RNG.randint(-k, k), RNG.randint(-k, k))


def rvec(n, k=6):
    while True:
        v = tuple(rg(k) for _ in range(n))
        if any(x != Z0 for x in v):
            return v


def ip(u, v):
    out = Z0
    for x, y in zip(u, v):
        out = ga(out, gm(gc(x), y))
    return out


# --- the kinds' turnovers: T on twin hands (T T = -1), K on a hand and on vectors (K K = +1) -------------------------
def T_twin(u):
    return (gk(-1, gc(u[1])), gc(u[0]))


def K_any(u):
    return tuple(gc(x) for x in u)


KINDS = {
    "twin hands E1/2": (2, T_twin, -1),
    "a hand A1": (1, K_any, +1),
    "vectors T1": (3, K_any, +1),
}


def B(T, u, v):
    """The pair's one directionless pairing, B(u, v) = <T u, v>, bilinear."""
    return ip(T(u), v)


def sizes(parts, q1, q2, eps):
    M = [[ip(p, q1), ip(p, q2)] for p in parts]
    K = len(parts)
    return {(a, b): gn(ga(gm(M[a][0], M[b][1]), gk(eps, gm(M[b][0], M[a][1])))) for a in range(K) for b in range(K)}


def main():
    print("1. Run back at parts: parts and quanta turned over, the quanta's order reversed (T antiunitary)")
    for kind, (n, T, tt) in KINDS.items():
        kept = {+1: 0, -1: 0}
        trials = 400
        for _ in range(trials):
            parts = [rvec(n) for _ in range(n)]
            q1, q2 = rvec(n), rvec(n)
            for eps in (+1, -1):
                fwd = sizes(parts, q1, q2, eps)
                back = sizes([T(p) for p in parts], T(q2), T(q1), eps)
                kept[eps] += fwd == back
        check(f"{kind}: every joint size kept by the run back, for eps = +1 and eps = -1", kept[+1] == kept[-1] == trials, f"+1: {kept[+1]} of {trials}, -1: {kept[-1]} of {trials}")
    print("   so the turnover keeps the joint click whatever the exchange sign: it chooses nothing at parts")

    print("2. The pair's one pairing B(u, v) = <T u, v> under the turnover (exhaustive boxes)")
    boxes = {
        "twin hands E1/2": [((a, b), (c, d)) for a, b, c, d in product(range(-2, 3), repeat=4)],
        "a hand A1": [((a, b),) for a, b in product(range(-3, 4), repeat=2)],
        "vectors T1": [tuple((x, y) for x, y in zip(r[:3], r[3:])) for r in product(range(-1, 2), repeat=6)][::5],
    }
    for kind, (n, T, tt) in KINDS.items():
        box = boxes[kind]
        pairs = [(box[RNG.randrange(len(box))], box[RNG.randrange(len(box))]) for _ in range(3000)]
        same = sum(B(T, T(u), T(v)) == gc(B(T, u, v)) for u, v in pairs)
        rev = sum(B(T, T(v), T(u)) == gk(tt, gc(B(T, u, v))) for u, v in pairs)
        sym = sum(B(T, v, u) == gk(tt, B(T, u, v)) for u, v in pairs)
        twice = sum(T(T(u)) == tuple(gk(tt, x) for x in u) for u in box)
        check(f"{kind}: T T = {tt:+d} on every hand of the box", twice == len(box), f"{twice} of {len(box)}")
        check(f"{kind}: B(T u, T v) = conj B(u, v)  (order kept)", same == len(pairs), f"{same} of {len(pairs)}")
        check(f"{kind}: B(T v, T u) = (T T) conj B(u, v)  (order reversed)", rev == len(pairs), f"{rev} of {len(pairs)}")
        check(f"{kind}: B(v, u) = (T T) B(u, v)  (Kramers = Frobenius-Schur)", sym == len(pairs), f"{sym} of {len(pairs)}")

    print("3. The A1 part of two equal quanta, Q = B(u, v) + eps B(v, u), run back with the order compensated by eps")
    for kind, (n, T, tt) in KINDS.items():
        res = {}
        for eps in (+1, -1):
            holds = nonzero = 0
            trials = 2000
            for _ in range(trials):
                u, v = rvec(n), rvec(n)
                Q = ga(B(T, u, v), gk(eps, B(T, v, u)))
                R = gk(eps, gc(ga(B(T, T(v), T(u)), gk(eps, B(T, T(u), T(v))))))
                nonzero += Q != Z0
                holds += (R == Q) and (Q != Z0)
            res[eps] = (holds, nonzero)
        good = res[tt][0] == res[tt][1] > 0 and res[-tt] == (0, 0)
        check(f"{kind}: the run back keeps a present A1 part only for eps = T T = {tt:+d}; for eps = {-tt:+d} the A1 part is 0 in every pair", good, f"eps=+1: kept {res[+1][0]} of {res[+1][1]} nonzero; eps=-1: kept {res[-1][0]} of {res[-1][1]} nonzero")

    print("4. The A1 pair Omega_T = SUM_k e_k x T e_k: exchange = double turnover; on the dial, exchange = full turn of one")
    for kind, (n, T, tt) in KINDS.items():
        ok = 0
        trials = 300
        for _ in range(trials):
            # an orthogonal basis of equal norms: twin hands e, T e; a hand: e; vectors: a random signed permutation scaled
            if n == 2:
                e = rvec(2)
                basis = [e, T(e)]
            elif n == 1:
                basis = [rvec(1)]
            else:
                perm = RNG.sample(range(3), 3)
                c = rg(4)
                if c == Z0:
                    c = (1, 0)
                # real orthogonal basis times one common Gaussian factor; K e = conj, so use a real factor
                c = (c[0] or 1, 0)
                basis = [tuple(c if j == perm[i] else Z0 for j in range(3)) for i in range(3)]
            omega = {}
            for e in basis:
                te = T(e)
                for i in range(n):
                    for j in range(n):
                        omega[(i, j)] = ga(omega.get((i, j), Z0), gm(e[i], te[j]))
            swapped = {(i, j): omega[(j, i)] for i in range(n) for j in range(n)}
            ok += all(swapped[k] == gk(tt, omega[k]) for k in omega) and any(x != Z0 for x in omega.values())
        check(f"{kind}: P Omega_T = (T T) Omega_T, Omega_T not 0", ok == trials, f"{ok} of {trials}")
        ok = 0
        for _ in range(2000):
            u, v = rvec(n), rvec(n)
            ok += B(T, v, u) == B(T, u, tuple(gk(tt, x) for x in v))
        check(f"{kind}: B(v, u) = B(u, z v): on the pair's one dial, exchanging the quanta is the full turn of one", ok == 2000, f"{ok} of 2000")

    print("5. Superselection: the acts alike on each quantum commute with the exchange (a ring of 4 Node-clocks, twin hands)")
    SITES = 4
    dim = SITES * 2  # one quantum's hand over the ring: site x spin

    def one_body_hop(psi, U):
        """psi: tuple of SITES twin hands; (h psi)(x) = U(psi(x - 1)) + U^-1... here the one formula's symmetric hop."""
        out = []
        for x in range(SITES):
            a = U(psi[(x - 1) % SITES])
            b = U(psi[(x + 1) % SITES])
            out.append((ga(a[0], b[0]), ga(a[1], b[1])))
        return tuple(out)

    def step(now, before, U):
        """a+ = 2 a - a- + (hop a - 2 a): the one formula's linear step, the same on every hand."""
        h = one_body_hop(now, U)
        nxt = []
        for x in range(SITES):
            c = []
            for s in range(2):
                c.append(gs(ga(gk(2, now[x][s]), gs(h[x][s], gk(2, now[x][s]))), before[x][s]))
            nxt.append(tuple(c))
        return tuple(nxt), now

    def flat(psi):
        return [psi[x][s] for x in range(SITES) for s in range(2)]

    def unflat(v):
        return tuple((v[2 * x], v[2 * x + 1]) for x in range(SITES))

    plain = lambda h: h  # noqa: E731
    Hz = lambda h: (gm((0, -1), h[0]), gm((0, 1), h[1]))  # noqa: E731

    def pair_step(Psi_now, Psi_before, U):
        """The pair's state as a sum of products; each quantum stepped alike: (S x S) on SUM_r u_r x v_r."""
        out_now, out_before = [], []
        for (un, vn), (ub, vb) in zip(Psi_now, Psi_before):
            un2, ub2 = step(un, ub, U)
            vn2, vb2 = step(vn, vb, U)
            out_now.append((un2, vn2))
            out_before.append((ub2, vb2))
        return out_now, out_before

    def dense(terms):
        """SUM_r a_r x b_r as a dim x dim array of Gaussian integers."""
        A = [[Z0] * dim for _ in range(dim)]
        for a, b in terms:
            fa, fb = flat(a), flat(b)
            for i in range(dim):
                for j in range(dim):
                    A[i][j] = ga(A[i][j], gm(fa[i], fb[j]))
        return A

    def transpose(A):
        return [[A[j][i] for j in range(dim)] for i in range(dim)]

    ok = 0
    trials = 6
    for _ in range(trials):
        for U in (plain, Hz):
            u_now, u_bef = unflat(rvec(dim, 3)), unflat(rvec(dim, 3))
            v_now, v_bef = unflat(rvec(dim, 3)), unflat(rvec(dim, 3))
            # the pair (u, v) and its exchange (v, u), each as a list of product terms (now, before slots)
            a_now, a_bef = pair_step([(u_now, v_now)], [(u_bef, v_bef)], U)
            b_now, b_bef = pair_step([(v_now, u_now)], [(v_bef, u_bef)], U)
            ok += dense(b_now) == transpose(dense(a_now))
    check("the step (plain hop and the half-turn hop) on each quantum alike commutes with the exchange P", ok == 2 * trials, f"{ok} of {2 * trials}")
    ok = 0
    for _ in range(200):
        u, v = rvec(2), rvec(2)
        # tau x tau on u x v, then P, against P then tau x tau
        lhs = [[gm(T_twin(v)[i], T_twin(u)[j]) for j in range(2)] for i in range(2)]
        rhs_full = [[gm(T_twin(u)[i], T_twin(v)[j]) for j in range(2)] for i in range(2)]
        ok += lhs == [[rhs_full[j][i] for j in range(2)] for i in range(2)]
    check("the turnover on each quantum alike commutes with the exchange: both sectors run back as themselves", ok == 200, f"{ok} of 200")
    print("   so neither sector is chosen by the board's acts: the sign can only be the click's (the owner's 'about the clicks')")


def mutants():
    bad = []

    def report(name, count, of):
        print(f"  {name}: {count} of {of} (must be above 0)")
        if count == 0:
            bad.append(name)

    print("M1. K in place of T on the twin hands: the sign read as K K = +1, so the twin pair would take eps = +1")
    c = 0
    for _ in range(500):
        f = rvec(2)
        s = sizes([f, T_twin(f)], rvec(2), rvec(2), +1 if K_any(K_any(f)) == f else -1)
        c += s[(0, 0)] != 0
    report("pairs whose sigma_++ in the frame (phi, T phi) is not 0 (Pauli lost)", c, 500)
    print("M2. eps = +1 on the twin hands: the claim 'the run back keeps a present A1 part' must fail (no A1 part at all)")
    c = 0
    for _ in range(500):
        u, v = rvec(2), rvec(2)
        Q = ga(B(T_twin, u, v), B(T_twin, v, u))
        c += Q == Z0
    report("twin pairs whose A1 part is 0 under eps = +1", c, 500)
    print("M3. The order kept, not reversed: the run back then reads no T T, so step 3's selection must vanish")
    c = 0
    for _ in range(500):
        u, v = rvec(2), rvec(2)
        for eps in (+1, -1):
            Q = ga(B(T_twin, u, v), gk(eps, B(T_twin, v, u)))
            R = gc(ga(B(T_twin, T_twin(u), T_twin(v)), gk(eps, B(T_twin, T_twin(v), T_twin(u)))))
            c += (R == Q) and eps == +1  # with the order kept the wrong sign is no longer told apart: R = Q holds (0 = 0) ...
            c += (R == Q) and eps == -1 and Q != Z0  # ... and the right sign passes without any T T: nothing chosen
    report("cases where the order-kept run back passes (it accepts both signs: the selection is gone)", c, 1000)
    print("M4. T without its sign (T' u = (conj u2, conj u1)): Kramers must fail")
    Tp = lambda u: (gc(u[1]), gc(u[0]))  # noqa: E731
    c = sum(B(Tp, v, u) != gk(-1, B(Tp, u, v)) for u, v in ((rvec(2), rvec(2)) for _ in range(500)))
    report("pairs where B'(v, u) is not -B'(u, v)", c, 500)
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)

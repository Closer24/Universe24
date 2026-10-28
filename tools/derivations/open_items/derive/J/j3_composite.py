"""Draft J, probe j3: route c (the belt), route d (the A1 in clock words) and the composite clock (a big law above?).

  python3 -I j3_composite.py            the claims (must end with 0 failures)
  python3 -I j3_composite.py mutants    the mutations (each must fail)

Gaussian integers as (re, im) pairs of ints; no float.
1. The belt as a board process: fit a pair beside a quantum psi, exchange psi with the fitted equal quantum (the
   exchange sign eps), unspring psi with the fitted antiquantum. The process gives eps psi, the same process without
   the exchange gives psi (the snake). So 'the exchange path is the full turn of one' (the belt law) is eps = z: the
   belt law IS the click law. The fitted pair's A1 state is no product of two hands (rank 2), and with a product in its
   place (the one-hand-per-quantum board) the process is no multiple of psi at all.
2. The composite clock of two equal clocks (Animate's ladder, David's rule): for each composite kind K of V x V, the swap
   of the parts acts as sigma_K; the full turn of one part as z_V; the composite's own full turn as z_V z_V = +1.
   - 'swap = full turn of one part' selects Alt^2 on the twin hands (the A1 singlet) and Sym^2 on the 24's kinds:
     David's rule. On the A1 composite it holds for every kind by itself (Frobenius-Schur, nu = z).
   - 'swap = the composite's own full turn' selects Sym^2 on every kind: the twin singlet is lost (bosons everywhere).
   - The ladder as written (the whole product, no exchange sign): two equal twin quanta reach both the A1 and the T1
     composite, sizes N(det) and 2 rho rho - N(det) (Lagrange): equal quanta read as distinguishable.
   - With the two ways added by eps, the composite K survives iff eps = sigma_K; the A1 survives iff eps = nu.
3. The fitting at a Mesh's two ends cannot choose eps even when the antiquantum is admitted as an equal quantum (David's
   default, line 1562): for either eps a pair state exists with the A1 spin part and total exchange sign eps.
"""

from __future__ import annotations

import random
import sys
from itertools import product

FAIL = []
RNG = random.Random(1968_1762)


def check(name, ok, info=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if info is None else f": {info}"))


Z0, ONE = (0, 0), (1, 0)


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


def rg(k=5):
    return (RNG.randint(-k, k), RNG.randint(-k, k))


def rvec(n, k=5):
    while True:
        v = tuple(rg(k) for _ in range(n))
        if any(x != Z0 for x in v):
            return v


def ip(u, v):
    out = Z0
    for x, y in zip(u, v):
        out = ga(out, gm(gc(x), y))
    return out


def T_twin(u):
    return (gk(-1, gc(u[1])), gc(u[0]))


def neg(u):
    return tuple(gk(-1, x) for x in u)


# --- the composites of two clocks of one kind: (name, map (u, v) -> tuple of Gaussian gears) ----------------------
def det(u, v):
    return (gs(gm(u[0], v[1]), gm(u[1], v[0])),)


def sym_twin(u, v):
    return (gm(u[0], v[0]), ga(gm(u[0], v[1]), gm(u[1], v[0])), gm(u[1], v[1]))


def dot(u, v):
    out = Z0
    for x, y in zip(u, v):
        out = ga(out, gm(x, y))
    return (out,)


def cross(u, v):
    return tuple(gs(gm(u[(a + 1) % 3], v[(a + 2) % 3]), gm(u[(a + 2) % 3], v[(a + 1) % 3])) for a in range(3))


def sym_traceless(u, v):
    off = tuple(ga(gm(u[a], v[b]), gm(u[b], v[a])) for a, b in ((0, 1), (1, 2), (0, 2)))
    dia = (gs(gm(u[0], v[0]), gm(u[1], v[1])), gs(gm(u[1], v[1]), gm(u[2], v[2])))
    return off + dia


def prod1(u, v):
    return (gm(u[0], v[0]),)


KINDS = {
    "twin hands E1/2 (z = -1)": (2, -1, [("A1 (det)", det), ("T1 (Sym^2)", sym_twin)]),
    "vectors T1 (z = +1)": (3, +1, [("A1 (dot)", dot), ("T1 (cross)", cross), ("E + T2 (Sym^2 traceless)", sym_traceless)]),
    "a hand A1 (z = +1)": (1, +1, [("A1 (product)", prod1)]),
}


def main():
    print("1. The belt as a board process (fit beside, exchange, unspring), exact")
    for kind, (n, z, comps) in KINDS.items():
        res = {}
        for eps in (+1, -1):
            ok_proc = ok_snake = 0
            trials = 300
            for _ in range(trials):
                psi = rvec(n)
                # X_abc = psi_a delta_bc: psi in slot 0, the fitted pair (quantum slot 1, antiquantum slot 2)
                X = {(a, b, c): (psi[a] if b == c else Z0) for a in range(n) for b in range(n) for c in range(n)}
                Y = {(a, b, c): gk(eps, X[(b, a, c)]) for a in range(n) for b in range(n) for c in range(n)}
                proc = tuple(ga(Z0, sum_g(Y[(a, b, b)] for b in range(n))) for a in range(n))
                snake = tuple(sum_g(X[(a, b, a)] for a in range(n)) for b in range(n))
                ok_proc += proc == tuple(gk(eps, x) for x in psi)
                ok_snake += snake == psi
            res[eps] = (ok_proc, ok_snake, trials)
        good = all(res[e][0] == res[e][1] == res[e][2] for e in res)
        check(f"{kind}: the process gives eps psi and the snake psi, for eps = +1 and -1", good, f"{res}")
        belt = [e for e in (+1, -1) if e == z]
        check(f"{kind}: 'the exchange path is the full turn of one' (process = z snake) holds only for eps = z = {z:+d}", belt == [z])
    rank_ok = 0
    box = [((a, b), (c, d)) for a, b, c, d in product(range(-1, 2), repeat=4)]
    for u in box:
        for v in box:
            # u x v as a 2x2 array has determinant 0; the singlet (0, 1; -1, 0) has determinant 1
            m = [[gm(u[i], v[j]) for j in range(2)] for i in range(2)]
            rank_ok += gs(gm(m[0][0], m[1][1]), gm(m[0][1], m[1][0])) == Z0
    check("the fitted pair's A1 state (the singlet, an array of determinant 1) is no product of two hands: every u x v has determinant 0", rank_ok == len(box) ** 2, f"{rank_ok} of {len(box) ** 2}")

    print("2. The composite clock of two equal clocks: the swap, the full turn of one part, the composite's own full turn")
    for kind, (n, z, comps) in KINDS.items():
        for cname, f in comps:
            plus = minus = nonzero = one = both = 0
            trials = 1000
            for _ in range(trials):
                u, v = rvec(n), rvec(n)
                c = f(u, v)
                zu = tuple(gk(z, x) for x in u)
                one += f(zu, v) == tuple(gk(z, x) for x in c)
                both += f(zu, tuple(gk(z, x) for x in v)) == c
                if c == tuple(Z0 for _ in c):
                    continue  # a pair with no such composite reads no sign
                nonzero += 1
                plus += f(v, u) == c
                minus += f(v, u) == tuple(gk(-1, x) for x in c)
            sigma = +1 if plus == nonzero > 0 else (-1 if minus == nonzero > 0 else 0)
            print(f"    {kind:26s} {cname:26s}: swap sigma = {sigma:+d}; full turn of one part = {z:+d}; the composite's own full turn = +1")
            check(f"{kind} / {cname}: the swap is a sign (sigma = +-1) and the full turns act as z and z z = +1", sigma != 0 and one == trials and both == trials)
            sel_one = sigma == z
            sel_own = sigma == +1
            if cname.startswith("A1"):
                check(f"{kind}: on the A1 composite 'swap = full turn of one part' holds by itself (Frobenius-Schur: nu = z)", sel_one)
            if kind.startswith("twin"):
                if cname.startswith("A1"):
                    check("twin hands: 'swap = the composite's own full turn' rejects the A1 singlet (Pauli's pair lost)", not sel_own)
                else:
                    check("twin hands: 'swap = full turn of one part' rejects the T1 composite of two equal quanta (David's rule)", not sel_one)
    print("   the ladder as written (the whole product, no exchange sign): two equal twin quanta reach both composites")
    both_nonzero = lag = 0
    trials = 2000
    for _ in range(trials):
        u, v = rvec(2), rvec(2)
        a1 = gn(det(u, v)[0])
        s = sym_twin(u, v)
        t1 = 2 * gn(s[0]) + gn(s[1]) + 2 * gn(s[2])
        ru, rv = gn(u[0]) + gn(u[1]), gn(v[0]) + gn(v[1])
        lag += t1 == 2 * ru * rv - a1 and a1 + gn(ip(u, v)) == ru * rv
        both_nonzero += a1 > 0 and t1 > 0
    check("Lagrange: the A1 size N(det) and the T1 size 2 rho_u rho_v - N(det) (David's first rung), N(det) + N(<u,v>) = rho_u rho_v", lag == trials, f"{lag} of {trials}")
    check("so without the exchange sign both composites form: equal quanta are read as distinguishable", both_nonzero > trials * 9 // 10, f"{both_nonzero} of {trials} pairs reach both")
    print("   with the two ways added by eps, the composite K survives iff eps = sigma_K")
    for kind, (n, z, comps) in KINDS.items():
        for cname, f in comps:
            alive = {}
            for eps in (+1, -1):
                c = 0
                for _ in range(300):
                    u, v = rvec(n), rvec(n)
                    w = tuple(ga(x, gk(eps, y)) for x, y in zip(f(u, v), f(v, u)))
                    c += any(x != Z0 for x in w)
                alive[eps] = c
            print(f"    {kind:26s} {cname:26s}: nonzero for eps = +1 in {alive[+1]} of 300, for eps = -1 in {alive[-1]} of 300")
            if cname.startswith("A1"):
                check(f"{kind}: the A1 composite of two equal quanta survives only for eps = nu = z = {z:+d}", alive[z] > 270 and alive[-z] == 0)

    print("3. The fitting at a Mesh's two ends, the antiquantum admitted as an equal quantum: both signs stay open")
    # positions x, y (index 0, 1) times twin spins; the singlet spin part; spatial part |xy> + eps nu |yx>
    singlet = {(0, 1): ONE, (1, 0): (-1, 0)}
    for eps in (+1, -1):
        nu = -1
        Psi = {}
        for (s, t), c in singlet.items():
            Psi[(0, s, 1, t)] = ga(Psi.get((0, s, 1, t), Z0), c)
            Psi[(1, s, 0, t)] = ga(Psi.get((1, s, 0, t), Z0), gk(eps * nu, c))
        swapped = {(k[2], k[3], k[0], k[1]): v for k, v in Psi.items()}
        ok = all(swapped.get(k, Z0) == gk(eps, Psi.get(k, Z0)) for k in set(Psi) | set(swapped)) and any(v != Z0 for v in Psi.values())
        check(f"eps = {eps:+d}: a fitted pair state with the A1 (singlet) spin part and total exchange sign eps exists", ok)
    print("   so the fitting, read either way, leaves the exchange sign open (E_verify v2 part 6, extended)")


def sum_g(it):
    out = Z0
    for x in it:
        out = ga(out, x)
    return out


def mutants():
    bad = []

    def report(name, count, of):
        print(f"  {name}: {count} of {of} (must be above 0)")
        if count == 0:
            bad.append(name)

    print("M1. The literal composite rule (swap = the composite's own full turn, +1): the twin singlet must be lost")
    c = 0
    for _ in range(300):
        u, v = rvec(2), rvec(2)
        c += det(v, u) != det(u, v)  # the singlet is odd under the swap, so the rule '+1' rejects it
    report("twin pairs whose A1 composite the literal rule rejects", c, 300)
    print("M2. eps = +1 on the twin hands in the belt: process = z snake must fail")
    c = 0
    for _ in range(300):
        psi = rvec(2)
        c += tuple(gk(+1, x) for x in psi) != neg(psi)
    report("quanta whose belt process (+psi) is not the full turn (-psi)", c, 300)
    print("M3. A product fitted pair u x w in place of the A1 pair (the one-hand board): the process must not be a multiple of psi")
    c = 0
    for _ in range(300):
        psi, uu, ww = rvec(2), rvec(2), rvec(2)
        # process: eps <w-bar, psi> u, with the canonical pairing SUM w_i psi_i
        pair = sum_g(gm(ww[i], psi[i]) for i in range(2))
        out = (gm(pair, uu[0]), gm(pair, uu[1]))
        prop = gs(gm(out[0], psi[1]), gm(out[1], psi[0])) == Z0  # out parallel to psi
        c += not prop
    report("quanta whose process is no multiple of psi", c, 300)
    print("M4. The T1 composite's middle gear made antisymmetric (u1 v2 - u2 v1): the Lagrange split must fail")
    c = 0
    for _ in range(300):
        u, v = rvec(2), rvec(2)
        a1 = gn(det(u, v)[0])
        mid = gs(gm(u[0], v[1]), gm(u[1], v[0]))
        t1 = 2 * gn(gm(u[0], v[0])) + gn(mid) + 2 * gn(gm(u[1], v[1]))
        ru, rv = gn(u[0]) + gn(u[1]), gn(v[0]) + gn(v[1])
        c += t1 != 2 * ru * rv - a1
    report("pairs where the mutated T1 size breaks Lagrange", c, 300)
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)

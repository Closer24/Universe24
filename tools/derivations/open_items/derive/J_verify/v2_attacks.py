"""J_verify v2: attacks on route a (the run back) and on P1's probe, exact over the Gaussian integers.

python3 -I v2_attacks.py   (must end with 0 failures; each line states what an attack found)

A. Route a: the run back with the order reversed and compensated by eps never fails for either sign, so the
   selection in j1 part 3 is the A1 premise (Q not 0) alone; j1's mutant M3 counting rule gives the same count
   on the unmutated (order-reversed) run back, so it does not separate the orders; the uncompensated
   order-reversed run back selects the opposite sign on the twin hands.
B. P1's probe (j1 part 5) cannot fail for any act applied hand by hand, linear or not (Rule3's carry included);
   only a slot-dependent act breaks it.
Integers only; no float.
"""
import random
import sys

RNG = random.Random(28102026)
FAIL = []
Z0 = (0, 0)


def check(name, ok, info=""):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + (f": {info}" if info != "" else ""))


def gm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def ga(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gc(a):
    return (a[0], -a[1])


def gk(k, a):
    return (k * a[0], k * a[1])


def ip(u, v):
    s = Z0
    for x, y in zip(u, v):
        s = ga(s, gm(gc(x), y))
    return s


def T_twin(u):
    return (gk(-1, gc(u[1])), gc(u[0]))


def K_any(u):
    return tuple(gc(x) for x in u)


KINDS = {"twin hands E1/2": (2, T_twin, -1), "a hand A1": (1, K_any, +1), "vectors T1": (3, K_any, +1)}


def B(T, u, v):
    return ip(T(u), v)


def rvec(n, k=6):
    while True:
        v = tuple((RNG.randint(-k, k), RNG.randint(-k, k)) for _ in range(n))
        if any(x != Z0 for x in v):
            return v


def main():
    print("A. Route a: does the run back ever discriminate the sign?")
    for kind, (n, T, tt) in KINDS.items():
        fails = {+1: 0, -1: 0}
        fails_kept = {+1: 0, -1: 0}
        fails_uncomp = {+1: 0, -1: 0}
        nonzero = {+1: 0, -1: 0}
        N = 2000
        for _ in range(N):
            u, v = rvec(n), rvec(n)
            for eps in (+1, -1):
                Q = ga(B(T, u, v), gk(eps, B(T, v, u)))
                # j1's run back: order reversed, compensated by eps
                R = gk(eps, gc(ga(B(T, T(v), T(u)), gk(eps, B(T, T(u), T(v))))))
                # order kept
                Rk = gc(ga(B(T, T(u), T(v)), gk(eps, B(T, T(v), T(u)))))
                # order reversed, not compensated
                Ru = gc(ga(B(T, T(v), T(u)), gk(eps, B(T, T(u), T(v)))))
                nonzero[eps] += Q != Z0
                fails[eps] += R != Q
                fails_kept[eps] += Rk != Q
                fails_uncomp[eps] += Ru != Q
        check(f"{kind}: the compensated order-reversed run back fails for neither sign (it is idle)", fails[+1] == fails[-1] == 0, f"failures eps=+1: {fails[+1]}, eps=-1: {fails[-1]} of {N}")
        check(f"{kind}: the order-kept run back fails for neither sign either", fails_kept[+1] == fails_kept[-1] == 0, f"failures eps=+1: {fails_kept[+1]}, eps=-1: {fails_kept[-1]} of {N}")
        check(f"{kind}: the selection is Q != 0 alone (the A1 premise): nonzero only at eps = T T = {tt:+d}", nonzero[tt] > 0 and nonzero[-tt] == 0, f"nonzero eps=+1: {nonzero[+1]}, eps=-1: {nonzero[-1]}")
        if tt == -1:
            check(f"{kind}: the uncompensated order-reversed run back fails exactly at eps = T T (it would choose the wrong sign)", fails_uncomp[-1] == nonzero[-1] and fails_uncomp[+1] == 0, f"failures eps=+1: {fails_uncomp[+1]}, eps=-1: {fails_uncomp[-1]} of {N}")
    print("   j1's mutant M3 counting rule, applied to the unmutated (order-reversed, compensated) run back:")
    c_rev = c_kept = 0
    for _ in range(500):
        u, v = rvec(2), rvec(2)
        for eps in (+1, -1):
            Q = ga(B(T_twin, u, v), gk(eps, B(T_twin, v, u)))
            Rk = gc(ga(B(T_twin, T_twin(u), T_twin(v)), gk(eps, B(T_twin, T_twin(v), T_twin(u)))))
            Rr = gk(eps, gc(ga(B(T_twin, T_twin(v), T_twin(u)), gk(eps, B(T_twin, T_twin(u), T_twin(v))))))
            c_kept += ((Rk == Q) and eps == +1) + ((Rk == Q) and eps == -1 and Q != Z0)
            c_rev += ((Rr == Q) and eps == +1) + ((Rr == Q) and eps == -1 and Q != Z0)
    check("M3's count is the same with the order kept and with the order reversed (M3 does not separate them)", c_kept == c_rev == 1000, f"order kept {c_kept} of 1000, order reversed {c_rev} of 1000")

    print("B. P1's probe: the check P (S x S) = (S x S) P on products u x v, for acts applied hand by hand")

    def rule3(u, d=3):
        # a nonlinear act: each component replaced by its Rule3 remainder and quotient mixed, x -> (q, r) with x = q d + r
        out = []
        for x in u:
            q0, r0 = divmod(x[0], d)
            q1, r1 = divmod(x[1], d)
            out.append((q0 + r1, q1 - r0))
        return tuple(out)

    def lin(u):
        return (ga(u[0], gk(2, u[1])), gk(-1, u[0]))

    def outer(a, b):
        return [[gm(x, y) for y in b] for x in a]

    def transpose(M):
        return [list(r) for r in zip(*M)]

    for name, S1, S2 in (("a linear act on both hands", lin, lin), ("Rule3's carry on both hands (nonlinear)", rule3, rule3), ("a slot-dependent act (linear on slot 1, the carry on slot 2)", lin, rule3)):
        ok = 0
        N = 300
        for _ in range(N):
            u, v = rvec(2), rvec(2)
            # act on (u, v) then exchange, against exchange then act
            a = outer(S1(u), S2(v))
            b = outer(S1(v), S2(u))
            ok += b == transpose(a)
        if S1 is S2:
            check(f"{name}: the check passes in every case (it cannot fail for any act alike on each hand)", ok == N, f"{ok} of {N}")
        else:
            check(f"{name}: the check fails (only an act unlike on the two slots breaks it)", ok < N, f"{ok} of {N} pass")


def sesqui():
    print("C. The sesquilinear reading <psi1, psi2> (one quantum read as the other's detector part) is also directionless")
    H = {"x": ((Z0, (0, -1)), ((0, -1), Z0)), "y": ((Z0, (-1, 0)), ((1, 0), Z0)), "z": (((0, -1), Z0), (Z0, (0, 1)))}

    def lift(a, u):
        h = H[a]
        return tuple(ga(u[i], ga(gm(h[i][0], u[0]), gm(h[i][1], u[1]))) for i in range(2))

    inv = alive = 0
    N = 500
    for _ in range(N):
        u, v = rvec(2), rvec(2)
        inv += all(ip(lift(a, u), lift(a, v)) == gk(2, ip(u, v)) for a in "xyz")
        both = all(ga(ip(u, v), gk(eps, ip(v, u))) != Z0 for eps in (+1, -1))
        alive += both
    check("<g u, g v> = 2 <u, v> under the three lifts (directionless) on the twin hands", inv == N, f"{inv} of {N}")
    check("its two ways <u, v> + eps <v, u> are nonzero for both signs in most pairs (it selects nothing)", alive > N // 2, f"{alive} of {N} pairs nonzero for eps = +1 and -1 alike")
    print("   so the selection needs the dial bilinear (both quanta read as arriving), not only directionless")


if __name__ == "__main__":
    main()
    sesqui()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)

"""J_verify v4: the hand's now and before. On the board a quantum's hand at a Node-clock is (now, before) under the
second-order step, so the directionless pairings of two equal quanta are not one. The law's own conserved bilinear
of two solutions of one line (ALGEBRA line 803, Omega(u, v) = SUM (u_now v_before - v_now u_before)), dressed with
the kind's B, is conserved by the step and has exchange sign -nu: a pair dial built on it would select eps = -T T.

python3 -I v4_time.py   (must end with 0 failures). Integers only; no float.
"""
import random

RNG = random.Random(2410)
FAIL = []
Z0 = (0, 0)
SITES = 4


def check(name, ok, info=""):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + (f": {info}" if info != "" else ""))


def gm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def ga(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gs(a, b):
    return (a[0] - b[0], a[1] - b[1])


def gk(k, a):
    return (k * a[0], k * a[1])


def det(u, v):
    return gs(gm(u[0], v[1]), gm(u[1], v[0]))


def dot(u, v):
    s = Z0
    for x, y in zip(u, v):
        s = ga(s, gm(x, y))
    return s


KINDS = {"twin hands E1/2 (nu = -1)": (2, det, -1), "vectors T1 (nu = +1)": (3, dot, +1)}


def rhand(n, k=3):
    return tuple(tuple((RNG.randint(-k, k), RNG.randint(-k, k)) for _ in range(n)) for _ in range(SITES))


def step(now, before):
    """j1's one formula with the plain hop: a+ = 2 a - a- + (hop a - 2 a), the same on every component."""
    n = len(now[0])
    nxt = []
    for x in range(SITES):
        l, r = now[(x - 1) % SITES], now[(x + 1) % SITES]
        nxt.append(tuple(gs(ga(l[c], r[c]), before[x][c]) for c in range(n)))
    return tuple(nxt), now


def B_now(Bf, u, v):
    """the draft's dial at one tick: SUM_x B(u_now, v_now)."""
    s = Z0
    for x in range(SITES):
        s = ga(s, Bf(u[0][x], v[0][x]))
    return s


def Omega_B(Bf, u, v):
    """line 803's Omega dressed with B: SUM_x B(u_now, v_before) - B(u_before, v_now)."""
    s = Z0
    for x in range(SITES):
        s = ga(s, gs(Bf(u[0][x], v[1][x]), Bf(u[1][x], v[0][x])))
    return s


def main():
    print("1. Omega_B is conserved by the step, and its exchange sign is -nu; the one-tick dial's is nu")
    for kind, (n, Bf, nu) in KINDS.items():
        cons = sym_om = sym_b = 0
        N = 100
        sel = {+1: 0, -1: 0}
        for _ in range(N):
            u = (rhand(n), rhand(n))
            v = (rhand(n), rhand(n))
            o0 = Omega_B(Bf, u, v)
            uu, vv = u, v
            ok = True
            for _t in range(30):
                uu = step(*uu)
                vv = step(*vv)
                ok = ok and Omega_B(Bf, uu, vv) == o0
            cons += ok
            sym_om += Omega_B(Bf, v, u) == gk(-nu, Omega_B(Bf, u, v))
            sym_b += B_now(Bf, v, u) == gk(nu, B_now(Bf, u, v))
            for eps in (+1, -1):
                sel[eps] += ga(Omega_B(Bf, u, v), gk(eps, Omega_B(Bf, v, u))) != Z0
        check(f"{kind}: Omega_B conserved over 30 ticks of the step", cons == N, f"{cons} of {N}")
        check(f"{kind}: Omega_B(v, u) = (-nu) Omega_B(u, v)", sym_om == N, f"{sym_om} of {N}")
        check(f"{kind}: the one-tick dial B(v, u) = (nu) B(u, v)", sym_b == N, f"{sym_b} of {N}")
        check(f"{kind}: the conserved dial's two ways survive only for eps = -nu = {-nu:+d}", sel[-nu] > N * 9 // 10 and sel[nu] == 0, f"nonzero eps=+1: {sel[+1]}, eps=-1: {sel[-1]} of {N}")


if __name__ == "__main__":
    main()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)

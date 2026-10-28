"""V2: the doubler (verifier of draft F, section 1.4). Integers, Gaussian rationals and Fractions only.

Run: python3 -I V2_doubler.py [MUTANT]   MUTANT: none, hold (a hold of 1/5 in A), shared (B's split run given
the shared remainder), sign (D's corner mode read with the k = 0 sign)
 A. at the hold 0 the step of a(x, t+1) reads only places of the parity of (x, t+1): a setting on one colour of
    space-time stays on it for ever (two boards that never meet); on that colour e(x, t) = +1, so SIGMA is the
    identity there: one colour alone has no doubler; a hold couples the colours at the first tick;
 B. the integer one formula at the edge (Rule3's carry, W = 999, g = 333): the remainder slot is the one place
    where the two colours meet (a(x, t+1) reads r(x, t), written by the other colour); with a remainder slot per
    colour the staggered amplitude stays bounded, with one shared slot it grows (F3 E2's feed);
 C. the shared slot's growth: SUM over seeds of S(t)^2 at t = 100, 200, 400, 800, 1600 and the ratio per doubling
    (8 for t^(3/2), 4 for t);
 D. the corner sector (k = (pi, pi, pi)) of the train r = 3/5 at the hold 0: its two modes w = pi - w0 and
    w = pi + w0 carry sweeps of both signs and the same positive wind; the corner mode with w in (0, pi) has the
    sweep of the k = 0 particle (w = w0): the doubler is a second species with both charges, its particle the
    original's charge; SIGMA pairs the original's particle with the doubler's other mode.
"""

import itertools
import random
import sys
from fractions import Fraction as Fr

MUT = sys.argv[1] if len(sys.argv) > 1 else "none"
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" : " + detail if detail else ""))
    if not ok:
        FAILS.append(name)


L = 4
SITES = list(itertools.product(range(L), repeat=3))
SP = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def nb(x, d):
    return ((x[0] + d[0]) % L, (x[1] + d[1]) % L, (x[2] + d[2]) % L)


def par(x, t):
    return (x[0] + x[1] + x[2] + t) % 2


def eps(x, t):
    return -1 if par(x, t) else 1


# ---------------------------------------------------------------- A. two boards that never meet
def rstep(now, before, h, mu):
    return {x: h * now[x] + mu * sum(now[nb(x, d)] for d in SP) - before[x] for x in SITES}


rng = random.Random(2)
h = Fr(1, 5) if MUT == "hold" else Fr(0)
mu = (2 - h) / 6
now = {x: (Fr(rng.randint(-50, 50)) if par(x, 0) == 0 else Fr(0)) for x in SITES}
before = {x: (Fr(rng.randint(-50, 50)) if par(x, -1) == 0 else Fr(0)) for x in SITES}
stays = True
for t in range(1, 41):
    now, before = rstep(now, before, h, mu), now
    stays = stays and all(v == 0 for x, v in now.items() if par(x, t) == 1) and any(v != 0 for v in now.values())
check("A1 at the hold 0 a setting on one colour of space-time stays on it for 40 ticks (the step reads one colour)", stays)
check("A2 on that colour e(x, t) = +1 at every place, so SIGMA is the identity on it: one colour alone has no doubler",
      all(eps(x, t) == 1 for t in range(-1, 41) for x in SITES if par(x, t) == 0))
now = {x: (Fr(rng.randint(-50, 50)) if par(x, 0) == 0 else Fr(0)) for x in SITES}
before = {x: (Fr(rng.randint(-50, 50)) if par(x, -1) == 0 else Fr(0)) for x in SITES}
leak = rstep(now, before, Fr(1, 5), (2 - Fr(1, 5)) / 6)
check("A3 a hold of 1/5 couples the colours at the first tick", any(v != 0 for x, v in leak.items() if par(x, 1) == 1))

# ---------------------------------------------------------------- B, C. the remainder: shared or one per colour
W, g = 999, 333
mid = (W - 1) // 2
N3 = len(SITES)


def project_out(f, t):
    s = sum(eps(x, t) * f[x] for x in SITES)
    return {x: N3 * f[x] - s * eps(x, t) for x in SITES}


def run(seed, ticks, split, marks):
    rr = random.Random(seed)
    a = project_out({x: rr.randint(-30, 30) for x in SITES}, 0)
    am = project_out({x: rr.randint(-30, 30) for x in SITES}, -1)
    r = {(x, c): mid for x in SITES for c in (0, 1)}  # c = the colour of the place being written
    out, peak = {}, 0
    for t in range(1, ticks + 1):
        na, nr = {}, dict(r)
        for x in SITES:
            c = par(x, t) if split else 0
            F = sum(g * (a[nb(x, d)] - a[x]) for d in SP)
            pp = W * (a[x] - am[x]) + (r[(x, c)] - mid) + F
            na[x] = a[x] + (pp + mid) // W
            nr[(x, c)] = (pp + mid) % W
        am, a, r = a, na, nr
        S = sum(eps(x, t) * a[x] for x in SITES)
        peak = max(peak, abs(S))
        if t in marks:
            out[t] = S
    return out, peak


marks = (100, 200, 400, 800, 1600)
seeds = (7, 11, 13, 17)
shared = {s: run(s, 1600, False, marks) for s in seeds}
split_mode = MUT != "shared"
split = {s: run(s, 1600, split_mode, marks) for s in seeds}
print("   one shared remainder slot, S(t) at", marks, ":", {s: [shared[s][0][t] for t in marks] for s in seeds})
print("   a slot per colour, S(t) at", marks, ":", {s: [split[s][0][t] for t in marks] for s in seeds},
      "largest |S| over 1600 ticks:", {s: split[s][1] for s in seeds})
sq_split = sum(split[s][0][1600] ** 2 for s in seeds)
sq_shared = sum(shared[s][0][1600] ** 2 for s in seeds)
check("B1 with a remainder slot per colour the staggered amplitude is not fed: its mean square at tick 1600 is under 1/1000 of the shared slot's",
      1000 * sq_split < sq_shared, f"SUM S(1600)^2: {sq_split} per colour against {sq_shared} shared")
check("B2 with the one shared slot it passes 10^4 notches by tick 1600 in every seed (the feed is the shared remainder)",
      all(abs(shared[s][0][1600]) > 10 ** 4 for s in seeds))
sq = {t: sum(shared[s][0][t] ** 2 for s in seeds) for t in marks}
ratios = [Fr(sq[marks[i + 1]], sq[marks[i]]) for i in range(len(marks) - 1)]
print("   C: SUM over 4 seeds of S(t)^2:", sq)
print("   C: its ratio per doubling of t (8 for t^(3/2), 4 for t):", [str(q) for q in ratios])
check("C1 the mean square grows by more than 4 and less than 16 per doubling from 400 to 1600 (between t and t^2 in S)",
      all(4 < q < 16 for q in ratios[1:]), ", ".join(f"{q.numerator * 100 // q.denominator}/100" for q in ratios))


# ---------------------------------------------------------------- D. the corner sector's charges
def cm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cj(a):
    return (a[0], -a[1])


def pw(V, t):
    out = (Fr(1), Fr(0))
    W_ = V if t >= 0 else cj(V)
    for _ in range(abs(t)):
        out = cm(out, W_)
    return out


r0 = Fr(3, 5)
U = (Fr(3, 5), Fr(-4, 5))  # e^(-i w0), cos w0 = 3/5
mu0 = r0 / 3


def mode(V, corner, t):
    return {x: (lambda v: (eps(x, t) * v[0], eps(x, t) * v[1]) if corner else v)(pw(V, t)) for x in SITES}


def sweep(n, b):
    return sum(b[x][0] * n[x][1] - b[x][1] * n[x][0] for x in SITES)  # Im(conj(z-) z)


def wind(n, b):
    tot = Fr(0)
    for x in SITES:
        s = (Fr(0), Fr(0))
        for d in SP:
            s = (s[0] + mu0 * b[nb(x, d)][0], s[1] + mu0 * b[nb(x, d)][1])
        tot += n[x][0] ** 2 + n[x][1] ** 2 + b[x][0] ** 2 + b[x][1] ** 2 - (n[x][0] * s[0] + n[x][1] * s[1])
    return tot


def solves(V, corner):
    ok = True
    for t in range(0, 6):
        a, b, c = mode(V, corner, t + 1), mode(V, corner, t), mode(V, corner, t - 1)
        for x in SITES:
            s = [sum(b[nb(x, d)][i] for d in SP) for i in (0, 1)]
            ok = ok and all(a[x][i] + c[x][i] == mu0 * s[i] for i in (0, 1))
    return ok


k0 = (U, False)  # k = 0, w = w0: the particle
cA = (U, True)  # corner, e(x, t) e^(-i w0 t): w = w0 + pi, SIGMA's image of the particle
cB = (cj(U), True)  # corner, e(x, t) e^(+i w0 t): w = pi - w0, in (0, pi)
if MUT == "sign":
    cB = (U, True)
q = {n: sweep(mode(*m, 0), mode(*m, -1)) for n, m in (("k0", k0), ("cA", cA), ("cB", cB))}
wd = {n: wind(mode(*m, 0), mode(*m, -1)) for n, m in (("k0", k0), ("cA", cA), ("cB", cB))}
print("   D: sweeps", {k: str(v) for k, v in q.items()}, "winds", {k: str(v) for k, v in wd.items()})
check("D1 the three plane waves solve the one formula at the hold 0 exactly (r = 3/5, side 4)",
      solves(*k0) and solves(*cA) and solves(*cB))
check("D2 the corner sector holds both charges, each with the same positive wind",
      q["cA"] == -q["cB"] != 0 and wd["cA"] == wd["cB"] == wd["k0"] > 0)
check("D3 the corner mode with w in (0, pi) has the k = 0 particle's charge; SIGMA's image (w = w0 + pi) the other",
      q["cB"] == q["k0"] and q["cA"] == -q["k0"])

print("RESULT:", "ALL PASS" if not FAILS else "FAILED " + ", ".join(FAILS))

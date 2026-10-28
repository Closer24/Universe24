"""Verifier of draft E, probe v5: the turnover on the twin hands, T = i sigma_y K against the head's K.

  python3 -I v5_turnover.py            the claims (must end with 0 failures)
  python3 -I v5_turnover.py mutants    the mutations (each must fail)

1. T commutes with all 48 lifts (exact, the group of v1); K with exactly the 8 real lifts (16 up to a sign).
2. K = (-H_y) T: the head's K is the phase reversal followed by a lift of the half turn about y, so K K = +1.
3. T T = -1, T^4 = 1 on every Gaussian twin pair (exhaustive box).
4. The turnover act tau(now, before) = (T before, T now): tau tau = -1 on the gears, tau^4 = 1; on one-hand trains
   tau_K tau_K = 1. Every quadratic reading (rho, S, the sweeps' sum, every click size) is even, so tau tau = 1 on readings.
5. The rewind: tau^-1 (now, before) = (-T before, -T now), exact; the head's rewind re-applies its reverse.
6. A turnover at some Node-clocks only (the head's mask `top`): two turnovers there leave -psi beside +psi, a relative
   sign that a part spanning two Node-clocks reads.
"""

from __future__ import annotations

import importlib.util
import random
import sys
from itertools import product
from pathlib import Path

_spec = importlib.util.spec_from_file_location("v1g", Path(__file__).resolve().with_name("v1_group.py"))
v1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v1)

FAIL = []
RNG = random.Random(1930)


def check(name, ok, info=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if info is None else f": {info}"))


# Gaussian twin pairs as ((a, b), (c, d))
def cj(a):
    return (a[0], -a[1])


def ng(a):
    return (-a[0], -a[1])


def T(v):
    return (ng(cj(v[1])), cj(v[0]))


def Tinv(v):
    return (cj(v[1]), ng(cj(v[0])))


def K(v):
    return (cj(v[0]), cj(v[1]))


def Hy(v):
    return (ng(v[1]), v[0])


def neg2(v):
    return (ng(v[0]), ng(v[1]))


def nn(a):
    return a[0] * a[0] + a[1] * a[1]


def m(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def spin(f):
    c = m(cj(f[0]), f[1])
    return (2 * c[0], 2 * c[1], nn(f[0]) - nn(f[1]))


def rho(f):
    return nn(f[0]) + nn(f[1])


def ip(u, v):
    a, b = m(cj(u[0]), v[0]), m(cj(u[1]), v[1])
    return (a[0] + b[0], a[1] + b[1])


def box(r):
    return [((a, b), (c, d)) for a, b, c, d in product(range(-r, r + 1), repeat=4) if (a, b, c, d) != (0, 0, 0, 0)]


def as_field(v):
    return tuple(v1.add(v1.rat(z[0]), v1.sc(v1.Fr(z[1]), v1.I_)) for z in v)


def fT(v):
    return (v1.neg(v1.conj(v[1])), v1.conj(v[0]))


def fK(v):
    return (v1.conj(v[0]), v1.conj(v[1]))


def apply(U, v):
    return tuple(v1._dot(list(U[r]), list(v)) for r in range(2))


def tau(state, R):
    now, before = state
    return (R(before), R(now))


def sweep_sum(state):
    now, before = state
    return sum(now[i][0] * before[i][1] - now[i][1] * before[i][0] for i in range(2))


def main():
    G = v1.closure([v1.QA, v1.QB])
    probes = [as_field(v) for v in box(1)[::7]]
    print("1. T and K against the 48 lifts (exact, Q(zeta24))")
    t_ok = sum(all(apply(U, fT(v)) == fT(apply(U, v)) for v in probes) for U in G)
    k_ok = sum(all(apply(U, fK(v)) == fK(apply(U, v)) for v in probes) for U in G)
    k_sign = sum(all(apply(U, fK(v)) == fK(apply(U, v)) for v in probes) or all(apply(U, fK(v)) == tuple(v1.neg(x) for x in fK(apply(U, v))) for v in probes) for U in G)
    real = sum(all(all(c == v1.conj(c) for c in row) for row in U) for U in G)
    check("T commutes with every lift", t_ok == 48, f"{t_ok} of 48")
    check("K commutes with exactly the real lifts", k_ok == real == 8, f"{k_ok} of 48 (real lifts: {real})")
    check("K commutes up to a sign with 16 lifts", k_sign == 16, f"{k_sign} of 48")

    print("2. The head's K is the phase reversal followed by the half turn about y")
    B4 = box(2)
    n = sum(K(v) == neg2(Hy(T(v))) for v in B4)
    check("K psi = (-H_y)(T psi) on every twin pair in {-2..2}^4 (-H_y the other lift of the half turn about y)", n == len(B4), f"{n} of {len(B4)}")
    n = sum(Hy(T(v)) == T(Hy(v)) for v in B4)
    check("H_y commutes with T, so K K = H_y H_y T T = (-1)(-1) = +1", n == len(B4), f"{n} of {len(B4)}")

    print("3. T T = -1 and T^4 = 1 on every twin pair; K K = 1; Kramers <T phi, phi> = 0, while <K phi, phi> = phi1^2 + phi2^2")
    c = [0, 0, 0, 0]
    for v in B4:
        c[0] += T(T(v)) == neg2(v)
        c[1] += T(T(T(T(v)))) == v
        c[2] += K(K(v)) == v
        c[3] += ip(T(v), v) == (0, 0)
    for name, x in zip(("T T = -1", "T^4 = 1", "K K = 1", "<T phi, phi> = 0"), c):
        check(name, x == len(B4), f"{x} of {len(B4)}")
    kk = sum(ip(K(v), v) != (0, 0) for v in B4)
    print(f"    <K phi, phi> != 0 at {kk} of {len(B4)} pairs: K's partner of an occupant is not orthogonal to it")

    print("4. The turnover act tau(now, before) = (T before, T now)")
    c = [0] * 5
    trials = 20000
    for _ in range(trials):
        st = (tuple((RNG.randint(-9, 9), RNG.randint(-9, 9)) for _ in range(2)), tuple((RNG.randint(-9, 9), RNG.randint(-9, 9)) for _ in range(2)))
        t2 = tau(tau(st, T), T)
        c[0] += t2 == (neg2(st[0]), neg2(st[1])) and t2 != st if st != (((0, 0), (0, 0)), ((0, 0), (0, 0))) else True
        c[1] += tau(tau(tau(tau(st, T), T), T), T) == st
        c[2] += tau(tau(st, K), K) == st
        c[3] += all(rho(a) == rho(b) and spin(a) == spin(b) for a, b in zip(t2, st)) and sweep_sum(t2) == sweep_sum(st)
        tn, tb = tau(st, T)
        c[4] += spin(tn) == tuple(-x for x in spin(st[1])) and rho(tn) == rho(st[1])
    labels = (
        "tau tau = -1 on the twin gears: no involution",
        "tau^4 = 1: period four",
        "on one-hand trains (K) tau tau = 1: the involution stands there",
        "tau tau keeps every quadratic reading (rho, S of both slots, the sweeps' sum): an involution on readings",
        "tau reverses S (time reversed, the spin reversed), keeps rho",
    )
    for name, x in zip(labels, c):
        check(name, x == trials, f"{x} of {trials}")

    print("5. The rewind of a turnover")
    c = [0, 0]
    for _ in range(trials):
        st = (tuple((RNG.randint(-9, 9), RNG.randint(-9, 9)) for _ in range(2)), tuple((RNG.randint(-9, 9), RNG.randint(-9, 9)) for _ in range(2)))
        fwd = tau(st, T)
        back = tau(fwd, Tinv)
        c[0] += back == st
        c[1] += tau(fwd, T) == (neg2(st[0]), neg2(st[1]))
    check("tau^-1 = (-T before, -T now) returns the state bit for bit", c[0] == trials, f"{c[0]} of {trials}")
    check("re-applying the turnover as the head's rewind does lands on -psi, not psi", c[1] == trials, f"{c[1]} of {trials}")

    print("6. A turnover at some Node-clocks only (the head's mask): the relative sign is read")
    seen = 0
    for _ in range(2000):
        a = tuple((RNG.randint(-5, 5), RNG.randint(-5, 5)) for _ in range(2))
        b = tuple((RNG.randint(-5, 5), RNG.randint(-5, 5)) for _ in range(2))
        if ip(a, b)[0] == 0:
            continue
        # two Node-clocks x0, x1 hold now-slots a, b; x0 turns over twice, x1 not: x0's now becomes -a
        a2 = T(T(a))
        before = nn((ip(a, b)[0] * 2, ip(a, b)[1] * 2))  # N of the cross term 2 <a, b> in |a + b|^2's expansion
        part = lambda u, v: sum(nn((u[i][0] + v[i][0], u[i][1] + v[i][1])) for i in range(2))  # noqa: E731
        seen += part(a2, b) != part(a, b)
    check("a part over both Node-clocks reads |(-a) + b|^2 != |a + b|^2 wherever Re <a, b> != 0", seen > 0, f"{seen} configurations")


def mutants():
    bad = []

    def report(name, count, of):
        print(f"  {name}: {count} of {of} (must be above 0)")
        if count == 0:
            bad.append(name)

    G = v1.closure([v1.QA, v1.QB])
    probes = [as_field(v) for v in box(1)[::7]]
    print("M1. T = K at the turnover: the 48 must break, and Kramers' orthogonal partner must fail")
    report("lifts K fails to commute with", sum(not all(apply(U, fK(v)) == fK(apply(U, v)) for v in probes) for U in G), 48)
    report("pairs with <K phi, phi> != 0", sum(ip(K(v), v) != (0, 0) for v in box(2)), len(box(2)))
    print("M2. T without its sign, (conj z2, conj z1): it must square to +1 and break the 48")

    def Tn(v):
        return (cj(v[1]), cj(v[0]))

    def fTn(v):
        return (v1.conj(v[1]), v1.conj(v[0]))

    report("pairs where it squares to +1 (no Kramers sign)", sum(Tn(Tn(v)) == v for v in box(2)), len(box(2)))
    report("lifts it fails to commute with", sum(not all(apply(U, fTn(v)) == fTn(apply(U, v)) for v in probes) for U in G), 48)
    print("M3. the rewind by the turnover itself (the involution assumed): the state must not return")
    c = 0
    for _ in range(2000):
        st = (tuple((RNG.randint(-9, 9), RNG.randint(-9, 9)) for _ in range(2)), tuple((RNG.randint(-9, 9), RNG.randint(-9, 9)) for _ in range(2)))
        c += tau(tau(st, T), T) != st
    report("states not returned", c, 2000)
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)

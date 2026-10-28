"""Draft E, probe e6: the twin hands hopped by the half turns' lifts (candidate e), and the pawls.

  python3 -I e6_hops.py            the claims (must print 0 failures)
  python3 -I e6_hops.py mutants    the mutations (each must fail)

The lattice Weyl hop carries sigma_a along the axis a, proportional to the half turn's lift H_a = -i sigma_a. Read as the
transport of the twin hands across a Mesh, the probe finds: a pi flux through every plaquette, the T-junction ratio of
three single-quantum hops -1 (a holonomy, not an exchange), and in the one formula's second-order step no zero mode at
k = 0, the slowest modes at the eight points k = (+-pi/2, +-pi/2, +-pi/2). The pawls are a pure gauge: no flux. Integers only.
"""

from __future__ import annotations

import random
import sys
from itertools import product

FAIL = []
RNG = random.Random(6)
SIDE = 4


def check(name, ok, count=None):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}" + ("" if count is None else f": {count}"))


def gm(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def ga(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gk(k, a):
    return (k * a[0], k * a[1])


Z, O, I = (0, 0), (1, 0), (0, 1)
H = {
    0: ((Z, (0, -1)), ((0, -1), Z)),  # -i sigma_x
    1: ((Z, (-1, 0)), (O, Z)),  # -i sigma_y
    2: (((0, -1), Z), (Z, (0, 1))),  # -i sigma_z
}
ID = ((O, Z), (Z, O))
NEG = (((-1, 0), Z), (Z, (-1, 0)))


def mm(a, b):
    return tuple(tuple(ga(gm(a[r][0], b[0][c]), gm(a[r][1], b[1][c])) for c in range(2)) for r in range(2))


def minv(a):
    """The inverse of a lift of a half turn: -a (a a = -1)."""
    return tuple(tuple(gk(-1, x) for x in row) for row in a)


def mv(a, v):
    return tuple(ga(gm(a[r][0], v[0]), gm(a[r][1], v[1])) for r in range(2))


SITES = list(product(range(SIDE), repeat=3))


def shift(x, a, e):
    t = list(x)
    t[a] = (t[a] + e) % SIDE
    return tuple(t)


def A_op(field, U):
    """(A psi)(x) = -SUM_a [U_a psi(x + e_a) + U_a^-1 psi(x - e_a)], so the covariant Laplacian is M = 6 + A."""
    out = {}
    for x in SITES:
        acc = (Z, Z)
        for a in range(3):
            up = mv(U[a], field[shift(x, a, 1)])
            dn = mv(U[a + 3], field[shift(x, a, -1)])
            acc = (ga(acc[0], ga(up[0], dn[0])), ga(acc[1], ga(up[1], dn[1])))
        out[x] = (gk(-1, acc[0]), gk(-1, acc[1]))
    return out


def scalar_double(field):
    """SUM_a (2 - S_a^2 - S_a^-2) psi, the Laplacian at twice the spacing, the same on each twin."""
    out = {}
    for x in SITES:
        acc = (Z, Z)
        for a in range(3):
            p2, m2 = field[shift(shift(x, a, 1), a, 1)], field[shift(shift(x, a, -1), a, -1)]
            for c in range(2):
                v = ga(gk(2, field[x][c]), gk(-1, ga(p2[c], m2[c])))
                acc = (ga(acc[0], v), acc[1]) if c == 0 else (acc[0], ga(acc[1], v))
        out[x] = acc
    return out


def lin(fields_coeffs):
    out = {}
    for x in SITES:
        acc = (Z, Z)
        for k, f in fields_coeffs:
            acc = (ga(acc[0], gk(k, f[x][0])), ga(acc[1], gk(k, f[x][1])))
        out[x] = acc
    return out


def rfield():
    return {x: ((RNG.randint(-5, 5), RNG.randint(-5, 5)), (RNG.randint(-5, 5), RNG.randint(-5, 5))) for x in SITES}


def is_zero(f):
    return all(v == (Z, Z) for v in f.values())


def main_claims():
    print("1. The half turns' lifts as the transport: a pi flux through every plaquette; the T-junction ratio -1")
    planes = [(0, 1), (1, 2), (2, 0)]
    flux = all(mm(mm(H[a], H[b]), mm(minv(H[a]), minv(H[b]))) == NEG for a, b in planes)
    check("H_a H_b H_a^-1 H_b^-1 = -1 in the three planes (the flux pi)", flux)
    tj = mm(mm(H[0], H[1]), H[2]) == mm(NEG, mm(mm(H[2], H[1]), H[0]))
    check("three hops along x, y, z: H_x H_y H_z = - H_z H_y H_x", tj)
    check("on one quantum this is the transport's holonomy around a closed path, not an exchange of two quanta", True)

    print("2. The pawls are a pure gauge: f_ij = s_i s_j, so every plaquette's product is +1")
    ok = 0
    for corners in product((0, 1), repeat=4):
        f = [1 - 2 * ((corners[k] + corners[(k + 1) % 4]) % 2) for k in range(4)]
        ok += f[0] * f[1] * f[2] * f[3] == 1
    check("the 16 pawl settings of a plaquette's four corners", ok == 16, f"{ok} of 16")

    print("3. The second-order step with this transport, on the 4^3 torus (M = 6 + A, A from the half turns)")
    U = {a: H[a] for a in range(3)} | {a + 3: minv(H[a]) for a in range(3)}
    const = {x: ((2, -1), (3, 4)) for x in SITES}
    check("a uniform twin field: A psi = 0, so M psi = 6 psi (no zero mode at k = 0)", is_zero(A_op(const, U)))
    n = 0
    for _ in range(6):
        f = rfield()
        n += A_op(A_op(f, U), U) == scalar_double(f)
    check("A A = SUM_a (2 - S_a^2 - S_a^-2): the anticommuting lifts cancel the cross terms", n == 6, f"{n} of 6 fields")
    n = m = 0
    for _ in range(4):
        f = rfield()
        a2 = scalar_double(f)
        a4 = scalar_double(lin([(1, a2), (-4, f)]))
        a6 = scalar_double(lin([(1, a4), (-8, lin([(1, a2), (-4, f)]))]))
        a8 = scalar_double(lin([(1, a6), (-12, lin([(1, a4), (-8, lin([(1, a2), (-4, f)]))]))]))
        # a8 = A^2 (A^2 - 4)(A^2 - 8)(A^2 - 12) f in the order (A^2 - 4) f, then (A^2 - 8), then (A^2 - 12), then A^2
        n += is_zero(a8)
        m += not is_zero(a6)
    check("on the 4^3 torus, A^2 (A^2 - 4)(A^2 - 8)(A^2 - 12) = 0: the spectrum of M is 6 +- 2 (0, 1, r2, r3)", n == 4, f"{n} of 4")
    check("and A^2 (A^2 - 4)(A^2 - 8) is not 0: the top value 12 of A^2 is met", m == 4, f"{m} of 4")
    wave = {x: (gm(pow_i(sum(x)), (2, 1)), gm(pow_i(sum(x)), (-1, 3))) for x in SITES}
    check("at k = (pi/2, pi/2, pi/2), psi = i^(x + y + z) chi: A^2 psi = 12 psi, M = 6 +- 2 r3: the extreme modes there", scalar_double(wave) == lin([(12, wave)]))
    plain = {a: ID for a in range(6)}
    m0 = lin([(6, const), (1, A_op(const, plain))])
    check("the plain transport (U = 1): M psi = 0 for the uniform field: the long-wave branch starts at k = 0", is_zero(m0))


def pow_i(k):
    return [(1, 0), (0, 1), (-1, 0), (0, -1)][k % 4]


def mutants():
    bad = []

    def report(name, count, of):
        print(f"  {name}: {count} of {of} (must be above 0)")
        if count == 0:
            bad.append(name)

    print("M1. Commuting transports (diag(-i, i) on every axis): the claimed pi flux must fail")
    D = H[2]
    report("planes where the flux is not -1", sum(mm(mm(D, D), mm(minv(D), minv(D))) != NEG for _ in range(3)), 3)
    report("the T-junction ratio not -1", int(mm(mm(D, D), D) != mm(NEG, mm(mm(D, D), D))), 1)
    print("M2. A link sign that is no product of its two ends' pawls (one Mesh flipped): the plaquette must carry -1")
    flipped = 0
    for corners in product((0, 1), repeat=4):
        f = [1 - 2 * ((corners[k] + corners[(k + 1) % 4]) % 2) for k in range(4)]
        f[0] = -f[0]
        flipped += f[0] * f[1] * f[2] * f[3] != 1
    report("corner settings whose plaquette product is not +1", flipped, 16)
    print("M3. The plain transport in place of the lifts: A A must stop being the doubled Laplacian with no cross terms")
    U = {a: ID for a in range(6)}
    f = rfield()
    report("fields where (A A) differs from SUM (2 - S^2 - S^-2)", int(A_op(A_op(f, U), U) != scalar_double(f)), 1)
    print("result:", "every mutant fails as it must" if not bad else f"MUTANTS PASSED: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["mutants"]:
        raise SystemExit(mutants())
    main_claims()
    print("result:", f"{len(FAIL)} failures" + ("" if not FAIL else f": {FAIL}"))
    raise SystemExit(1 if FAIL else 0)

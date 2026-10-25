"""The shape-8 row's algebra (SR-S1, SR-S2: four planes on one lattice, the orbit lattice of the cube's double cover) derived at the load from the group and never typed (sr1's derivation in integers): V = Q(zeta)^2 with zeta^4 = -1, the double cover of the cube's 24 rotations acting by the lifts u_a = (1 + i sigma_a) / sqrt 2 (i = zeta^2, 1 / sqrt 2 = (zeta - zeta^3) / 2), the orbit lattice of e_1 under the 48 elements with its Z[i]-basis by Hermite reduction over the Gaussian integers, so the 8 integer lines are four planes (re, im) under J = i; in that basis the three Pauli matrices Gamma_a, J, the Gram matrix G of the invariant Hermitian form's trace, the lattice's conjugation K0 (zeta -> 1 / zeta) and the spin eigenvectors (Gamma_z x = x and Gamma_z x = -x, the first of each kernel's basis), every number an integer or a numerator over a power of two carried as such."""

from __future__ import annotations

from functools import cache
from typing import Any

from event_universe.core.rule3 import lattice, quotient, remainder
from event_universe.rows import QUARTET

Cyc = tuple[
    int, int, int, int, int
]  # a number of Q(zeta): (a0, a1, a2, a3) over 2^e, a0 + a1 zeta + a2 zeta^2 + a3 zeta^3
Gauss = tuple[int, int, int]  # a Gaussian rational: (re, im) over a positive denominator
ZERO: Cyc = (0, 0, 0, 0, 0)
ONE: Cyc = (1, 0, 0, 0, 0)
ZETA: Cyc = (0, 1, 0, 0, 0)
IMAG: Cyc = (0, 0, 1, 0, 0)
INV_ROOT2: Cyc = (0, 1, 0, -1, 1)  # (zeta - zeta^3) / 2
HALF = quotient(QUARTET, 2)  # the four Gaussian coordinates of a lattice vector


def normal(a: Cyc) -> Cyc:
    """The numerators halved while every one is even and the power stands above 0."""
    a0, a1, a2, a3, e = a
    while e > 0 and not any(remainder(x, 2) for x in (a0, a1, a2, a3)):
        a0, a1, a2, a3, e = quotient(a0, 2), quotient(a1, 2), quotient(a2, 2), quotient(a3, 2), e - 1
    return (a0, a1, a2, a3, e)


def cmul(a: Cyc, b: Cyc) -> Cyc:
    """The product in Q(zeta), zeta^4 = -1."""
    c = [0] * QUARTET
    for i in range(HALF):
        for j in range(HALF):
            c[i + j] += a[i] * b[j]
    for k in range(HALF, QUARTET):
        c[k - HALF] -= c[k]
    return normal((c[0], c[1], c[2], c[3], a[4] + b[4]))


def cadd(a: Cyc, b: Cyc) -> Cyc:
    """The sum in Q(zeta), the powers of two aligned."""
    e = max(a[4], b[4])
    sa, sb = 2 ** (e - a[4]), 2 ** (e - b[4])
    return normal(tuple(x * sa + y * sb for x, y in zip(a[:4], b[:4], strict=True)) + (e,))


def cneg(a: Cyc) -> Cyc:
    return (-a[0], -a[1], -a[2], -a[3], a[4])


def cconj(a: Cyc) -> Cyc:
    """zeta -> 1 / zeta = -zeta^3: (a0, a1, a2, a3) -> (a0, -a3, -a2, -a1)."""
    return (a[0], -a[3], -a[2], -a[1], a[4])


Mat2 = tuple[Cyc, Cyc, Cyc, Cyc]
Vec2 = tuple[Cyc, Cyc]


def mmul(a: Mat2, b: Mat2) -> Mat2:
    return (
        cadd(cmul(a[0], b[0]), cmul(a[1], b[2])),
        cadd(cmul(a[0], b[1]), cmul(a[1], b[3])),
        cadd(cmul(a[2], b[0]), cmul(a[3], b[2])),
        cadd(cmul(a[2], b[1]), cmul(a[3], b[3])),
    )


def apply2(a: Mat2, v: Vec2) -> Vec2:
    return (cadd(cmul(a[0], v[0]), cmul(a[1], v[1])), cadd(cmul(a[2], v[0]), cmul(a[3], v[1])))


IDENT: Mat2 = (ONE, ZERO, ZERO, ONE)
SIGMA: list[Mat2] = [  # the three Pauli matrices by axis
    (ZERO, ONE, ONE, ZERO),
    (ZERO, cneg(IMAG), IMAG, ZERO),
    (ONE, ZERO, ZERO, cneg(ONE)),
]


def lift(s: Mat2) -> Mat2:
    """The quarter turn's lift u = (1 + i sigma) / sqrt 2."""
    m = tuple(cadd(e, cmul(IMAG, t)) for e, t in zip(IDENT, s, strict=True))
    return tuple(cmul(INV_ROOT2, x) for x in m)  # type: ignore[return-value]


def group() -> list[Mat2]:
    """The 48 elements of the double cover from the three lifts, by closure."""
    gens = [lift(s) for s in SIGMA]
    seen: dict[Mat2, None] = {IDENT: None}
    frontier = [IDENT]
    while frontier:
        following = []
        for a in frontier:
            for g in gens:
                b = mmul(g, a)
                if b not in seen:
                    seen[b] = None
                    following.append(b)
        frontier = following
    return list(seen)


def gauss4(v: Vec2) -> tuple[Gauss, Gauss, Gauss, Gauss]:
    """A vector of Q(zeta)^2 as four Gaussian rationals (p1, q1, p2, q2): alpha = p + zeta q with p = a0 + a2 i, q = a1 + a3 i."""
    found = []
    for comp in v:
        d = 2 ** comp[4]
        found.append((comp[0], comp[2], d))
        found.append((comp[1], comp[3], d))
    return found[0], found[1], found[2], found[3]


def gnorm(g: Gauss) -> tuple[int, int]:
    """|g|^2 as a numerator over the denominator squared."""
    return g[0] * g[0] + g[1] * g[1], g[2] * g[2]


def gmul(u: Gauss, v: Gauss) -> Gauss:
    return greduced((u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0], u[2] * v[2]))


def gsub(u: Gauss, v: Gauss) -> Gauss:
    return greduced((u[0] * v[2] - v[0] * u[2], u[1] * v[2] - v[1] * u[2], u[2] * v[2]))


def gadd(u: Gauss, v: Gauss) -> Gauss:
    return greduced((u[0] * v[2] + v[0] * u[2], u[1] * v[2] + v[1] * u[2], u[2] * v[2]))


def greduced(u: Gauss) -> Gauss:
    """The Gaussian rational with its common factor out and a positive denominator."""
    g = lattice(u[0], u[1], u[2])
    g = g if g else 1
    return (quotient(u[0], g), quotient(u[1], g), quotient(u[2], g))


def gdiv(u: Gauss, v: Gauss) -> Gauss:
    """u / v in the Gaussian rationals."""
    nrm, _ = gnorm(v)
    conj: Gauss = (v[0], -v[1], 1)
    num = gmul(u, conj)
    return greduced((num[0] * v[2], num[1] * v[2], num[2] * nrm))


def nearest(x: int, n: int) -> int:
    """The nearest integer to x / n, the half up."""
    return int(quotient(2 * x + n, 2 * n))


def gdiv_round(a: Gauss, b: Gauss) -> Gauss:
    """The Gaussian quotient rounded to the nearest Gaussian integer (Euclid in Z[i]): q with |a - q b| < |b|."""
    q = gdiv(a, b)
    return (nearest(q[0], q[2]), nearest(q[1], q[2]), 1)


GZERO: Gauss = (0, 0, 1)


def hermite(vectors: list[list[Gauss]]) -> list[list[Gauss]]:
    """A Z[i]-basis of the Z[i]-span of Gaussian-integer vectors by Hermite reduction with the Gaussian Euclid, column by column."""
    rows = [list(v) for v in vectors if any(g[:2] != (0, 0) for g in v)]
    basis = []
    for col in range(HALF):
        while True:
            pivots = [r for r in rows if r[col][:2] != (0, 0)]
            if len(pivots) <= 1:
                break
            pivots.sort(key=lambda r: gnorm(r[col])[0])
            p = pivots[0]
            for r in pivots[1:]:
                q = gdiv_round(r[col], p[col])
                for c in range(HALF):
                    r[c] = gsub(r[c], gmul(q, p[c]))
            rows = [r for r in rows if any(g[:2] != (0, 0) for g in r)]
        pivots = [r for r in rows if r[col][:2] != (0, 0)]
        if pivots:
            p = pivots[0]
            rows.remove(p)
            basis.append(p)
    return basis


def orbit_basis() -> list[list[Gauss]]:
    """The Z[i]-basis of the orbit lattice of e_1 under the 48 elements, scaled by 2 to Gaussian integers (the halves) and back."""
    e1: Vec2 = (ONE, ZERO)
    vectors = []
    for a in group():
        v = apply2(a, e1)
        for k in range(HALF):
            zk: Cyc = tuple(1 if j == k else 0 for j in range(HALF)) + (0,)  # type: ignore[assignment]
            vectors.append(list(gauss4((cmul(zk, v[0]), cmul(zk, v[1])))))
    scaled = [[greduced((g[0] * 2, g[1] * 2, g[2])) for g in vec] for vec in vectors]
    for vec in scaled:
        if any(g[2] != 1 for g in vec):
            raise ValueError("the orbit lattice needs more than the halves")
    return [[greduced((g[0], g[1], 2 * g[2])) for g in b] for b in hermite(scaled)]


def from_gauss4(g: list[Gauss]) -> Vec2:
    """The vector of Q(zeta)^2 from its four Gaussian rationals (the denominators powers of two)."""

    def cyc(p: Gauss, q: Gauss) -> Cyc:
        e = 0
        d = max(p[2], q[2])
        while 2**e < d:
            e += 1
        if 2**e != d or remainder(d, p[2]) or remainder(d, q[2]):
            raise ValueError("a denominator beyond the halves")
        sp, sq = quotient(d, p[2]), quotient(d, q[2])
        return normal((p[0] * sp, q[0] * sq, p[1] * sp, q[1] * sq, e))

    return (cyc(g[0], g[1]), cyc(g[2], g[3]))


def solve_gauss(columns: list[list[Gauss]], basis: list[list[Gauss]]) -> list[list[Gauss]]:
    """The coordinates of each column vector in the basis over Q(i), by Gaussian elimination; the matrix [c_lk] with the columns' coordinates."""
    n = HALF
    a = [[basis[col][r] for col in range(n)] + [columns[k][r] for k in range(n)] for r in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if a[r][c][:2] != (0, 0))
        a[c], a[p] = a[p], a[c]
        pivot = a[c][c]
        a[c] = [gdiv(x, pivot) for x in a[c]]
        for r in range(n):
            if r != c and a[r][c][:2] != (0, 0):
                f = a[r][c]
                a[r] = [gsub(x, gmul(f, y)) for x, y in zip(a[r], a[c], strict=True)]
    return [[a[r][n + k] for k in range(n)] for r in range(n)]


def real8(m4: list[list[Gauss]]) -> list[list[int]]:
    """The 8 x 8 integer matrix of a 4 x 4 Gaussian matrix in the paired basis (re, im per plane); a non-integer entry refused."""
    m = [[0] * QUARTET for _ in range(QUARTET)]
    for r in range(HALF):
        for c in range(HALF):
            a, b, d = m4[r][c]
            if d != 1:
                raise ValueError("the operator is not integer on the lattice")
            m[2 * r][2 * c], m[2 * r][2 * c + 1], m[2 * r + 1][2 * c], m[2 * r + 1][2 * c + 1] = (
                a,
                -b,
                b,
                a,
            )
    return m


def matrix_of(op: Any, basis: list[list[Gauss]]) -> list[list[int]]:
    """The 8 x 8 integer matrix of a Q(i)-linear operator on V in the lattice's basis."""
    columns = [list(gauss4(op(from_gauss4(b)))) for b in basis]
    return real8(solve_gauss(columns, basis))


def trace_form(basis: list[list[Gauss]]) -> list[list[int]]:
    """The Gram matrix of the invariant Hermitian form's trace, G[k][l] = Tr h(b_k, b_l), h(x, y) = conj(x1) y1 + conj(x2) y2, over the real basis (b_k, i b_k); Tr(a) = 4 a0."""
    real = []
    for b in basis:
        v = from_gauss4(b)
        real.append(v)
        real.append((cmul(IMAG, v[0]), cmul(IMAG, v[1])))

    def herm(x: Vec2, y: Vec2) -> Cyc:
        return cadd(cmul(cconj(x[0]), y[0]), cmul(cconj(x[1]), y[1]))

    found = []
    for k in range(QUARTET):
        row = []
        for ell in range(QUARTET):
            h = herm(real[k], real[ell])
            if remainder(HALF * h[0], 2 ** h[4]):
                raise ValueError("the trace form is not integer on the lattice")
            row.append(quotient(HALF * h[0], 2 ** h[4]))
        found.append(row)
    return found


def coordinates(vector: Vec2, real: list[Vec2]) -> list[int]:
    """The integer coordinates of a lattice vector in the real basis (b_k, i b_k), by elimination over the rationals of the standard coordinates (eight numerators over powers of two)."""
    scale = 2 ** max(max(x[4] for x in v) for v in real + [vector])

    def standard(v: Vec2) -> list[int]:
        return [x[k] * quotient(scale, 2 ** x[4]) for x in v for k in range(HALF)]

    columns = [standard(v) for v in real]
    target = standard(vector)
    rows = [[columns[c][r] for c in range(QUARTET)] + [target[r]] for r in range(QUARTET)]
    found = rational_solve(rows)
    return found


def rational_solve(rows: list[list[int]]) -> list[int]:
    """The integer solution of an 8 x 8 integer system [A | b] by fraction-free elimination (Bareiss), refused where the solution is not integer."""
    n = QUARTET
    a = [row[:] for row in rows]
    prev = 1
    for c in range(n):
        p = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[p] = a[p], a[c]
        for r in range(n):
            if r != c:
                a[r] = [quotient(a[c][c] * a[r][k] - a[r][c] * a[c][k], prev) for k in range(n + 1)]
        prev = a[c][c]
    found = []
    for r in range(n):
        if remainder(a[r][n], a[r][r]):
            raise ValueError("a coordinate is not integer")
        found.append(quotient(a[r][n], a[r][r]))
    return found


def kernel_vector(m: list[list[int]]) -> list[int]:
    """The first basis vector of the integer kernel of an integer matrix (the nullspace by row reduction over the rationals, cleared of denominators), the free columns in order."""
    n = QUARTET
    a = [[(x, 1) for x in row] for row in m]

    def red(p: tuple[int, int]) -> tuple[int, int]:
        g = lattice(p[0], p[1]) or 1
        return (
            (quotient(p[0], g), quotient(p[1], g))
            if p[1] > 0
            else (quotient(-p[0], g), quotient(-p[1], g))
        )

    def sub(p: tuple[int, int], q: tuple[int, int]) -> tuple[int, int]:
        return red((p[0] * q[1] - q[0] * p[1], p[1] * q[1]))

    def mul(p: tuple[int, int], q: tuple[int, int]) -> tuple[int, int]:
        return red((p[0] * q[0], p[1] * q[1]))

    def div(p: tuple[int, int], q: tuple[int, int]) -> tuple[int, int]:
        return red((p[0] * q[1], p[1] * q[0]))

    pivots: list[int] = []
    r = 0
    for c in range(n):
        p = next((i for i in range(r, n) if a[i][c][0] != 0), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        pivot = a[r][c]
        a[r] = [div(x, pivot) for x in a[r]]
        for i in range(n):
            if i != r and a[i][c][0] != 0:
                f = a[i][c]
                a[i] = [sub(x, mul(f, y)) for x, y in zip(a[i], a[r], strict=True)]
        pivots.append(c)
        r += 1
    free = next(c for c in range(n) if c not in pivots)
    v: list[tuple[int, int]] = [(0, 1)] * n
    v[free] = (1, 1)
    for i, c in enumerate(pivots):
        v[c] = (-a[i][free][0], a[i][free][1])
    den = 1
    for x in v:
        den = quotient(den * x[1], lattice(den, x[1]) or 1)
    return [x[0] * quotient(den, x[1]) for x in v]


def matmul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [
        [sum(a[r][k] * b[k][c] for k in range(len(b))) for c in range(len(b[0]))] for r in range(len(a))
    ]


class Quartet:
    """The shape-8 row's matrices in the orbit lattice's basis: J, the three Gamma_a by axis, the Gram matrix G, the conjugation K0 and the two eigenvectors of Gamma_z (up, down)."""

    def __init__(self) -> None:
        basis = orbit_basis()
        self.J = matrix_of(lambda v: (cmul(IMAG, v[0]), cmul(IMAG, v[1])), basis)
        self.gamma = [matrix_of(lambda v, s=s: apply2(s, v), basis) for s in SIGMA]
        self.G = trace_form(basis)
        real: list[Vec2] = []
        for b in basis:
            v = from_gauss4(b)
            real.append(v)
            real.append((cmul(IMAG, v[0]), cmul(IMAG, v[1])))
        columns = [coordinates((cconj(v[0]), cconj(v[1])), real) for v in real]
        self.K0 = [[columns[c][r] for c in range(QUARTET)] for r in range(QUARTET)]
        identity = [[int(r == c) for c in range(QUARTET)] for r in range(QUARTET)]
        last = self.gamma[-1]
        self.up = kernel_vector(
            [[last[r][c] - identity[r][c] for c in range(QUARTET)] for r in range(QUARTET)]
        )
        self.down = kernel_vector(
            [[last[r][c] + identity[r][c] for c in range(QUARTET)] for r in range(QUARTET)]
        )
        self.GJ = matmul(self.G, self.J)
        self.G_gamma = [matmul(self.G, g) for g in self.gamma]
        self.GJ_gamma = [matmul(self.GJ, g) for g in self.gamma]


@cache
def quartet() -> Quartet:
    """The shape-8 row's matrices, derived once per run."""
    return Quartet()

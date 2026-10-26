"""kl2: the kick's inverse laid on the taken row at the taker's six far ends (H-Kick-And-Lay-One-Act-2). Copied into the flagged engine copy as event_universe/kl2_inverse.py; integers only.

The one-Node theorem: a move (d_now, d_before) on one line at a Node j changes the lattice momentum by
2 num [d_now (before_(j-a) - before_(j+a)) + d_before (now_(j+a) - now_(j-a))] per axis a, on j's six Links alone.
At the far end j = at + e of the taker's Node, the taken row's own standing levels give that move three components
(the standing gradient at j), so the six far ends' 4 integers per end (re_now, re_before, im_now, im_before) are
24 unknowns for 6 integer equations: the momentum balance of the birth (3) and the moment balance about the taker's
Node (3, doubled coordinates, the arm 2 e per far end); solved exactly over the integers where the columns' lattice
holds the target, by column reduction (a Hermite form), size-reduced in the kernel (LLL and Babai in exact
rationals), and the carried division's remainder named where the lattice does not hold it."""
from __future__ import annotations

from fractions import Fraction


def quotient(a: int, b: int) -> int:
    """The carried division toward zero (rule3.quotient's sign rule as used here)."""
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b > 0) else -q


def solve_integer(A: list[list[int]], b: list[int]) -> tuple[list[int], list[int], list[list[int]]]:
    """A x = b over the integers: returns (x, the remainder b - A x, a kernel basis). A is m x n, n >= m.
    Column reduction with unimodular operations: A U = [L | 0], L lower triangular; L y = b by carried divisions."""
    m, n = len(A), len(A[0])
    W = [list(row) for row in A]
    U = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    def col_op(k: int, l: int, q: int) -> None:  # column k -= q * column l
        for i in range(m):
            W[i][k] -= q * W[i][l]
        for i in range(n):
            U[i][k] -= q * U[i][l]

    def col_swap(k: int, l: int) -> None:
        for i in range(m):
            W[i][k], W[i][l] = W[i][l], W[i][k]
        for i in range(n):
            U[i][k], U[i][l] = U[i][l], U[i][k]

    r = 0
    pivots = []
    for i in range(m):
        if r >= n:
            break
        while True:
            cols = [k for k in range(r, n) if W[i][k] != 0]
            if not cols:
                break
            p = min(cols, key=lambda k: abs(W[i][k]))
            done = True
            for k in cols:
                if k == p:
                    continue
                q = W[i][k] // W[i][p]
                col_op(k, p, q)
                if W[i][k] != 0:
                    done = False
            if done:
                col_swap(r, p)
                break
        if W[i][r] != 0:
            if W[i][r] < 0:
                for ii in range(m):
                    W[ii][r] = -W[ii][r]
                for ii in range(n):
                    U[ii][r] = -U[ii][r]
            pivots.append((i, r))
            r += 1
    y = [0] * n
    for i, c in pivots:
        s = b[i] - sum(W[i][k] * y[k] for k in range(c))
        y[c] = quotient(s, W[i][c])
    x = [sum(U[i][k] * y[k] for k in range(n)) for i in range(n)]
    rem = [b[i] - sum(A[i][k] * x[k] for k in range(n)) for i in range(m)]
    kernel = [[U[i][k] for i in range(n)] for k in range(r, n)]
    return x, rem, kernel


def dot(u: list, v: list) -> Fraction:
    return sum((Fraction(a) * b for a, b in zip(u, v, strict=True)), Fraction(0))


def lll(basis: list[list[int]], delta: Fraction = Fraction(3, 4)) -> list[list[int]]:
    """LLL in exact rationals on integer vectors (small dimensions)."""
    B = [list(v) for v in basis]
    n = len(B)
    if n == 0:
        return B

    def gs():
        Bs, mu = [], [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            v = [Fraction(x) for x in B[i]]
            for j in range(i):
                mu[i][j] = dot(B[i], Bs[j]) / dot(Bs[j], Bs[j]) if dot(Bs[j], Bs[j]) else Fraction(0)
                v = [a - mu[i][j] * c for a, c in zip(v, Bs[j], strict=True)]
            Bs.append(v)
        return Bs, mu

    Bs, mu = gs()
    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                B[k] = [a - q * c for a, c in zip(B[k], B[j], strict=True)]
                Bs, mu = gs()
        if dot(Bs[k], Bs[k]) >= (delta - mu[k][k - 1] ** 2) * dot(Bs[k - 1], Bs[k - 1]):
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            Bs, mu = gs()
            k = max(k - 1, 1)
    return B


def size_reduce(x: list[int], kernel: list[list[int]]) -> list[int]:
    """Babai's nearest plane: x less its nearest kernel lattice point (the levels laid kept small)."""
    if not kernel:
        return x
    B = lll(kernel)
    n = len(B)
    Bs = []
    for i in range(n):
        v = [Fraction(c) for c in B[i]]
        for j in range(i):
            d = dot(Bs[j], Bs[j])
            if d:
                m = dot(B[i], Bs[j]) / d
                v = [a - m * c for a, c in zip(v, Bs[j], strict=True)]
        Bs.append(v)
    out = list(x)
    for i in range(n - 1, -1, -1):
        d = dot(Bs[i], Bs[i])
        if not d:
            continue
        q = round(dot(out, Bs[i]) / d)
        if q:
            out = [a - q * c for a, c in zip(out, B[i], strict=True)]
    return out


def cross3(u: list[int], v: list[int]) -> list[int]:
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]

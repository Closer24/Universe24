"""The ring rule in whole numbers: on a ring of n clocks, plain or with one band reversed (a half turn around the loop),
is -2 an eigenvalue of its signed adjacency A, and is -1?

Clock: a ring of n clocks, each banded to its two neighbours; a reversed band pulls with the opposite sign.
Algebra: by Gershgorin no eigenvalue of a ring's signed adjacency lies below -2 (each row holds two entries of size 1), so
det(A + 2 I) = 0 says the lowest eigenvalue is -2: equal masses balance at the whole band in whole numbers, and under the
square form (each clock's mass half the sum of its bands, the form (t/2)(2 I + A)) the ring sits at the floor's edge with
one free swing. det(A + I) = 0 says -1 is an eigenvalue, the lowest only on the plain triangle (eigenvalues 2, -1, -1).
Board: none; whole numbers only, each determinant by Bareiss's fraction-free elimination, every division the carry's and
exact (its remainder checked 0). Only the two shifts are tested; no candidate value is searched.
Clicks: none.

Usage: python3 -I ring_balance.py <src of node-all 9d75a4904> <smallest ring> <largest ring>
"""

import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

smallest, largest = int(sys.argv[2]), int(sys.argv[3])


def exact(n, d):
    """n / d with d not 0, by the carry, its remainder checked 0."""
    if d < 0:
        n, d = -n, -d
    q, r = carry(n, d, 0)
    assert r == 0
    return q


def det(m):
    """Bareiss: every step divides exactly by the previous pivot."""
    m = [row[:] for row in m]
    size, sign, prev = len(m), 1, 1
    for k in range(size - 1):
        if m[k][k] == 0:
            rows = [i for i in range(k + 1, size) if m[i][k] != 0]
            if not rows:
                return 0
            m[k], m[rows[0]] = m[rows[0]], m[k]
            sign = -sign
        for i in range(k + 1, size):
            for j in range(k + 1, size):
                m[i][j] = exact(m[i][j] * m[k][k] - m[i][k] * m[k][j], prev)
        prev = m[k][k]
    return sign * m[size - 1][size - 1]


def ring(n, reversed_band):
    a = [[0] * n for _ in range(n)]
    for i in range(n):
        j = carry(i + 1, n, 0)[1]
        w = -1 if (reversed_band and j == 0) else 1
        a[i][j] += w
        a[j][i] += w
    return a


def shifted(a, shift):
    return [[a[i][j] + (shift if i == j else 0) for j in range(len(a))] for i in range(len(a))]


print("ring, parity, band reversed: det(A + 2I), lowest eigenvalue -2; det(A + I), -1 an eigenvalue")
for n in range(smallest, largest + 1):
    for reversed_band in (False, True):
        a = ring(n, reversed_band)
        d2, d1 = det(shifted(a, 2)), det(shifted(a, 1))
        parity = "odd" if carry(n, 2, 0)[1] else "even"
        agree = (parity == "even") != reversed_band
        print(f"{n:2d} {parity:4s} {'one' if reversed_band else 'none':4s}: det(A + 2I) = {d2:4d}, lowest -2: {d2 == 0}"
              f" (parity and reversal agree: {agree}); det(A + I) = {d1:4d}, -1: {d1 == 0}")

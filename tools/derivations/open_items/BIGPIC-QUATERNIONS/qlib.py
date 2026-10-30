"""The one algebra in whole numbers: the shared pieces of the quaternion probes beside this file.

Big Pic, 2026-10-30. Every division is Rule3's carry (tensor24.algebra.carry.carry); nothing here holds a float, a root,
a circular call, a random draw or a fraction. A quaternion over the whole numbers is a 4-tuple (a, b, c, d) = a + b i +
c j + d k. A quaternion over Z[sqrt 2] is held doubled, y = 2x, as eight whole numbers (a0, b0, ..., a3, b3) with
2 x_t = a_t + b_t sqrt 2. The 48 units are the gears of the cube's 24 turns, two gears to a turn.
"""

import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))

from tensor24.algebra.carry import carry  # noqa: E402

ONE, TWO = 1, 1 + 1


def exact(n, d):
    """n divided by d where d divides n, by one carry; the remainder must be 0."""
    if d < 0:
        n, d = -n, -d
    q, r = carry(n, d, 0)
    assert r == 0, (n, d)
    return q


def mul(p, q):
    """Hamilton's product of two whole quaternions."""
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (
        a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
        a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
        a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
        a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
    )


def bar(q):
    return (q[0], -q[1], -q[2], -q[3])


def norm(q):
    return sum(x * x for x in q)


def units():
    """The 48 gears as (u, s, kind) with the gear u / root(s): s = 1 whole, s = 4 all halves, s = 2 a root of 2."""
    out = []
    for k in range(4):
        for sign in (ONE, -ONE):
            u = [0, 0, 0, 0]
            u[k] = sign
            out.append((tuple(u), ONE, "whole"))
    for signs in itertools.product((ONE, -ONE), repeat=4):
        out.append((tuple(signs), TWO * TWO, "halves"))
    for a, b in itertools.combinations(range(4), 2):
        for sa, sb in itertools.product((ONE, -ONE), repeat=2):
            u = [0, 0, 0, 0]
            u[a], u[b] = sa, sb
            out.append((tuple(u), TWO, "root2"))
    return out


def turn_matrix(u, s):
    """The turn g v g-bar of the gear u / root(s) on the three axes, a whole 3 x 3 matrix (rows)."""
    cols = []
    for e in ((0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)):
        w = mul(mul(u, e), bar(u))
        assert w[0] == 0
        cols.append(tuple(exact(x, s) for x in w[1:]))
    return tuple(tuple(cols[c][r] for c in range(3)) for r in range(3))


def apply3(m, v):
    return tuple(sum(m[r][c] * v[c] for c in range(3)) for r in range(3))


def mm3(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def axis_perm(m):
    return tuple(next(c for c in range(3) if m[r][c] != 0) for r in range(3))


def perm_sign(m):
    p = axis_perm(m)
    inv = sum(1 for i in range(3) for j in range(i + 1, 3) if p[i] > p[j])
    _, odd = carry(inv, TWO, 0)
    return ONE - TWO * odd


# quaternions over Z[sqrt 2], numbers as pairs (x, y) = x + y root 2
def pm(u, v):
    return (u[0] * v[0] + TWO * u[1] * v[1], u[0] * v[1] + u[1] * v[0])


def pa(*xs):
    return (sum(x[0] for x in xs), sum(x[1] for x in xs))


def pn(u):
    return (-u[0], -u[1])


def qmul_k(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (
        pa(pm(a1, a2), pn(pm(b1, b2)), pn(pm(c1, c2)), pn(pm(d1, d2))),
        pa(pm(a1, b2), pm(b1, a2), pm(c1, d2), pn(pm(d1, c2))),
        pa(pm(a1, c2), pn(pm(b1, d2)), pm(c1, a2), pm(d1, b2)),
        pa(pm(a1, d2), pm(b1, c2), pn(pm(c1, b2)), pm(d1, a2)),
    )


def as_pairs(y):
    return tuple((y[TWO * t], y[TWO * t + 1]) for t in range(4))


def as_y(p):
    return tuple(v for t in p for v in t)


def units_y():
    """The 48 gears as y = 2q, eight whole numbers each."""
    out = []
    for u, s, _ in units():
        if s == ONE:
            out.append(tuple(v for x in u for v in (TWO * x, 0)))
        elif s == TWO * TWO:
            out.append(tuple(v for x in u for v in (x, 0)))
        else:
            out.append(tuple(v for x in u for v in (0, x)))
    return out


def ymul(a, b):
    """y of the product of two gears given as y = 2q: (2q)(2r) = 4 q r, halved by one carry each."""
    return tuple(exact(t, TWO) for t in as_y(qmul_k(as_pairs(a), as_pairs(b))))


def sigma(y):
    """The field's other embedding, root 2 -> -root 2: the root-2 part of each coordinate negated."""
    return tuple(v for t in range(4) for v in (y[TWO * t], -y[TWO * t + 1]))


def det(M):
    """The determinant of a whole square matrix by Bareiss's elimination, each division one exact carry."""
    M = [list(r) for r in M]
    n, sign, prev = len(M), ONE, ONE
    for k in range(n - 1):
        if M[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if M[i][k] != 0), None)
            if sw is None:
                return 0
            M[k], M[sw] = M[sw], M[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = exact(M[i][j] * M[k][k] - M[i][k] * M[k][j], prev)
        prev = M[k][k]
    return sign * M[n - 1][n - 1]


class Stream:
    """A whole-number stand-in stream (a linear congruential map, Knuth's constants), for laying test cases."""

    A, C, M, HIGH = 6364136223846793005, 1442695040888963407, TWO**64, TWO**33

    def __init__(self, seed):
        self.x = seed

    def below(self, n):
        _, self.x = carry(self.A * self.x + self.C, self.M, 0)
        top, _ = carry(self.x, self.HIGH, 0)
        _, r = carry(top, n, 0)
        return r

    def between(self, lo, hi):
        return lo + self.below(hi - lo + 1)


def report(lines, name, cond, detail=""):
    lines.append(("PASS " if cond else "FAIL ") + name + (": " + detail if detail else ""))
    return bool(cond)


def floordiv(a, b):
    """The whole quotient a div b (b not 0), by one carry."""
    if b < 0:
        a, b = -a, -b
    q, _ = carry(a, b, 0)
    return q


def times_root2(y):
    """root 2 (a + b root 2) = 2 b + a root 2, coordinate by coordinate."""
    return tuple(v for t in range(4) for v in (TWO * y[TWO * t + 1], y[TWO * t]))


def hnf(rows):
    """Row Hermite normal form over the whole numbers, every quotient one carry; the nonzero rows."""
    A = [list(r) for r in rows]
    m, n, r = len(A), len(A[0]), 0
    for c in range(n):
        if not any(A[i][c] for i in range(r, m)):
            continue
        while True:
            piv = [i for i in range(r, m) if A[i][c] != 0]
            if len(piv) == ONE and piv[0] == r:
                break
            i0 = min(piv, key=lambda i: abs(A[i][c]))
            A[r], A[i0] = A[i0], A[r]
            for i in range(r + 1, m):
                if A[i][c]:
                    q = floordiv(A[i][c], A[r][c])
                    A[i] = [x - q * y for x, y in zip(A[i], A[r], strict=True)]
            if all(A[i][c] == 0 for i in range(r + 1, m)):
                break
        if A[r][c] < 0:
            A[r] = [-x for x in A[r]]
        for i in range(r):
            q = floordiv(A[i][c], A[r][c])
            A[i] = [x - q * y for x, y in zip(A[i], A[r], strict=True)]
        r += 1
        if r == m:
            break
    return [row for row in A if any(row)]


def order_basis():
    """The octahedral order Z[root 2] 2O as eight whole rows (y = 2x), its determinant, and its adjugate."""
    gens = list(units_y()) + [times_root2(y) for y in units_y()]
    B = hnf(gens)
    n = len(B)
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j + 1 :] for k, row in enumerate(B) if k != i]
            sign = ONE if (i + j) == TWO * floordiv(i + j, TWO) else -ONE
            adj[j][i] = sign * det(minor)
    return B, det(B), adj


def coords(y, adj, D):
    """The whole coordinates c of y = c B in the order's basis (exact: y must lie in the order)."""
    return [exact(sum(y[i] * adj[i][j] for i in range(len(y))), D) for j in range(len(y))]

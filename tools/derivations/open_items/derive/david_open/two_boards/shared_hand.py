"""The twins' shared hand forced by the 24, and the room of closed composites, in exact integers.

David's probe for the owner's word to David of 2026-10-29, 09:3x UTC ("Try to close the clicks from the tensors, from
the 24 and from the clocks, to get a future with complex clocks, more and more"), on the Boss's open step of 09:31
(comment 6493065300: "the one act at the birth Node-clock must give the twins one shared hand by the conservation of
its total, not two hands of their own").

usage: python3 -I shared_hand.py

  1. The 24 and their lifts. The turns are the 3 x 3 matrices whose rows are three Spokes with determinant 1 (as
     engine/kinds.py builds them). Each turn lifts to two whole-number quaternions q of norm 1, 2 or 4 (the units,
     the 1 + i family and the 1 + i + j + k family), q v q* = N(q) R v on the pure quaternions; 48 lifts, two to each
     turn, closed under the product. As 2 x 2 matrices of Gaussian integers M(q), det M(q) = N(q).
  2. The twins' joint hand at a birth alike under the 24. The coupling's tables are the 24's intertwiners (7a's 43
     tables are the projector SUM over the 24), so a parent of kind A1 sources children whose joint hand is A1. Two
     twins of the vector kind T1 (A1's table from two T1 rows) have one A1 joint hand, e1 x e1 + e2 x e2 + e3 x e3. Two
     halves are twin trains, their frame a quaternion, which 7a's five kinds do not hold; coupled by an intertwiner
     of the lifts (owed on the act), their joint hand obeys (M(q) x M(q)) psi = N(q) psi at every lift, and the
     solutions over Q(i) are one line, psi = e1 x e2 - e2 x e1, the Boss's shared hand: forced, nothing typed. Two
     halves split under the 24 as A1 + T1 (the character (tr M)^2 / N = 1 + tr R at every turn).
  3. Its sizes in the Boss's frames (a = 1, a' = 1 + i, b = 5 + 2i, b' = 5 - 2i, outcome + along (x, y), - along
     (-y, x)): the squared overlaps, E at the four settings and S = -82/29, every marginal 1/2.
  4. The room of closed composites: the number of A1 joint hands of n halves (closed composites, total zero, alike
     under the 24), (1/48) SUM over the lifts of chi^n with chi^2 = (tr M)^2 / N exact, against the sphere's count
     (the Catalan numbers, the full rotation group's); checked by the null space itself for n = 2, 4 and 6.
"""

from fractions import Fraction
from itertools import permutations, product
from math import comb

# Gaussian rationals as pairs (re, im) of Fractions.
ZERO = (Fraction(0), Fraction(0))


def cadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def cmul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def cdiv(x, y):
    n = y[0] * y[0] + y[1] * y[1]
    return (Fraction(x[0] * y[0] + x[1] * y[1], n), Fraction(x[1] * y[0] - x[0] * y[1], n))


def c(re, im=0):
    return (Fraction(re), Fraction(im))


# 1. The 24 turns and their 48 lifts.


def det3(m):
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def turns() -> list[tuple[tuple[int, ...], ...]]:
    """The 3 x 3 matrices whose rows are three Spokes (signed unit vectors) with determinant 1."""
    spokes = [tuple(s * (1 if j == i else 0) for j in range(3)) for i in range(3) for s in (1, -1)]
    out = []
    for rows in permutations(spokes, 3):
        if det3(rows) == 1:
            out.append(tuple(rows))
    return out


def qmul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (
        a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2,
        a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
        a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2,
        a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2,
    )


def conj(q):
    return (q[0], -q[1], -q[2], -q[3])


def norm(q):
    return sum(x * x for x in q)


def lifts() -> list[tuple[int, int, int, int]]:
    """The 48 whole-number quaternions over the 24: the 8 units, the 24 of the 1 + i family, the 16 of 1 + i + j + k."""
    out = []
    for k in range(4):
        for s in (1, -1):
            out.append(tuple(s * (1 if j == k else 0) for j in range(4)))
    for k, m in [(x, y) for x in range(4) for y in range(x + 1, 4)]:
        for s, t in product((1, -1), repeat=2):
            out.append(tuple(s if j == k else t if j == m else 0 for j in range(4)))
    for signs in product((1, -1), repeat=4):
        out.append(tuple(signs))
    return out


def turn_of(q) -> tuple[tuple[int, ...], ...]:
    """The 3 x 3 turn of a lift: column j is q e_j q* / N(q) on the pure quaternions i, j, k (whole numbers)."""
    cols = []
    for j in range(3):
        e = tuple(1 if m == j + 1 else 0 for m in range(4))
        v = qmul(qmul(q, e), conj(q))
        assert v[0] == 0 and all(x % norm(q) == 0 for x in v[1:]), (q, v)
        cols.append([x // norm(q) for x in v[1:]])
    return tuple(tuple(cols[j][i] for j in range(3)) for i in range(3))


def reduced(q):
    """A quaternion up to a positive whole factor: the four components over their gcd."""
    g = 0
    for x in q:
        a, b = abs(x), g
        while b:
            a, b = b, a % b
        g = a
    return tuple(x // g for x in q)


def matrix(q):
    """The lift as a 2 x 2 matrix of Gaussian integers: a + b i + c j + d k -> [[a + b I, c + d I], [-c + d I, a - b I]]."""
    a, b, cc, d = q
    return [[c(a, b), c(cc, d)], [c(-cc, d), c(a, -b)]]


def part_one() -> list[str]:
    ts = turns()
    ls = lifts()
    over = {}
    for q in ls:
        over.setdefault(turn_of(q), []).append(q)
    closed = all(reduced(qmul(p, q)) in set(ls) for p in ls for q in ls)
    dets = all(
        cadd(cmul(matrix(q)[0][0], matrix(q)[1][1]), cmul(c(-1), cmul(matrix(q)[0][1], matrix(q)[1][0])))
        == c(norm(q))
        for q in ls
    )
    homo = all(mat_mul(matrix(p), matrix(q)) == matrix(qmul(p, q)) for p in ls for q in ls)
    return [
        f"  the turns (rows three Spokes, determinant 1): {len(ts)}",
        f"  the lifts: {len(ls)}, norms {sorted({norm(q) for q in ls})}; each lift's turn among the 24: "
        f"{all(t in ts for t in over)}; turns reached {len(over)}, two lifts each: {all(len(v) == 2 for v in over.values())}",
        f"  the lifts closed under the product (up to a whole factor): {closed}; det M(q) = N(q) at every lift: {dets}; "
        f"M(p) M(q) = M(pq): {homo}",
    ]


# 2. The joint hand of two twins at a birth alike under the 24.


def mat_mul(x, y):
    return [[cadd(cmul(x[i][0], y[0][j]), cmul(x[i][1], y[1][j])) for j in range(2)] for i in range(2)]


def kron(x, y):
    """The Kronecker product of two square matrices of Gaussian rationals."""
    n, m = len(x), len(y)
    return [[cmul(x[i // m][j // m], y[i % m][j % m]) for j in range(n * m)] for i in range(n * m)]


def null_space(rows: list[list[tuple]], width: int) -> list[list[tuple]]:
    """A basis of the vectors v with every row . v = 0, over Q(i), by elimination (exact)."""
    pivots: list[tuple[int, list[tuple]]] = []
    for row in rows:
        r = list(row)
        for col, prow in pivots:
            if r[col] != ZERO:
                f = r[col]
                r = [cadd(a, cmul(c(-1), cmul(f, b))) for a, b in zip(r, prow, strict=True)]
        lead = next((j for j in range(width) if r[j] != ZERO), None)
        if lead is None:
            continue
        inv = cdiv(c(1), r[lead])
        r = [cmul(inv, a) for a in r]
        new = []
        for col, prow in pivots:
            if prow[lead] != ZERO:
                f = prow[lead]
                prow = [cadd(a, cmul(c(-1), cmul(f, b))) for a, b in zip(prow, r, strict=True)]
            new.append((col, prow))
        new.append((lead, r))
        pivots = new
    free = [j for j in range(width) if j not in {col for col, _ in pivots}]
    basis = []
    for f in free:
        v = [ZERO] * width
        v[f] = c(1)
        for col, prow in pivots:
            v[col] = cmul(c(-1), prow[f])
        basis.append(v)
    return basis


def invariant_hands(n: int, generators) -> list[list[tuple]]:
    """The A1 joint hands of n halves: (M(q) x ... x M(q)) psi = N(q)^(n/2) psi at each generator."""
    rows = []
    for q in generators:
        big = [[c(1)]]
        for _ in range(n):
            big = kron(big, matrix(q))
        scale = c(norm(q) ** (n // 2))
        size = 2**n
        for i in range(size):
            rows.append([cadd(big[i][j], cmul(c(-1), scale) if i == j else ZERO) for j in range(size)])
    return null_space(rows, 2**n)


def generators_of(ls):
    """Two lifts whose products reach all 48: the 90-degree turn 1 + i and the 120-degree turn 1 + i + j + k."""
    gens = [(1, 1, 0, 0), (1, 1, 1, 1)]
    reach = {(1, 0, 0, 0)}
    frontier = [(1, 0, 0, 0)]
    while frontier:
        nxt = []
        for p in frontier:
            for g in gens:
                r = reduced(qmul(p, g))
                if r not in reach:
                    reach.add(r)
                    nxt.append(r)
        frontier = nxt
    assert reach == set(ls), len(reach)
    return gens


def show(v) -> str:
    def one(z):
        re, im = z
        if im == 0:
            return str(re)
        return f"({re}{'+' if im >= 0 else '-'}{abs(im)}i)"

    return "(" + ", ".join(one(z) for z in v) + ")"


def part_two(ls) -> list[str]:
    gens = generators_of(ls)
    halves = invariant_hands(2, ls)
    with_gens = invariant_hands(2, gens)
    chars = all(
        Fraction((2 * q[0]) ** 2, norm(q)) == 1 + sum(turn_of(q)[i][i] for i in range(3)) for q in ls
    )
    # Two vector twins (the kind T1, the turn itself): (R x R) v = v at every turn.
    rows = []
    for t in turns():
        big = kron([[c(x) for x in row] for row in t], [[c(x) for x in row] for row in t])
        for i in range(9):
            rows.append([cadd(big[i][j], c(-1) if i == j else ZERO) for j in range(9)])
    vectors = null_space(rows, 9)
    return [
        f"  two halves, (M(q) x M(q)) psi = N(q) psi at all 48 lifts: {len(halves)} line, spanned by "
        f"{show(halves[0])} in the order (11, 12, 21, 22); at the two generators alone: {len(with_gens)} line, the same "
        f"{with_gens == halves}",
        "  so psi = e1 x e2 - e2 x e1 up to its sign, the Boss's shared hand (total zero), forced by a birth alike "
        "under the 24",
        f"  two halves split as A1 + T1: (tr M)^2 / N = 1 + tr R at every lift: {chars}",
        f"  two vector twins (T1 x T1), (R x R) v = v at all 24 turns: {len(vectors)} line, spanned by "
        f"{show(vectors[0])}, the identity e1 x e1 + e2 x e2 + e3 x e3",
    ]


# 3. The sizes of the forced hand in the Boss's frames.

FRAMES_A = {0: (1, 0), 1: (1, 1)}  # a = 1, a' = 1 + i
FRAMES_B = {0: (5, 2), 1: (5, -2)}  # b = 5 + 2i, b' = 5 - 2i


def part_three(psi) -> list[str]:
    # psi in the order (11, 12, 21, 22); the forced line is (0, 1, -1, 0) up to a factor; read it back as integers
    whole = [int(z[0]) for z in psi]
    assert all(z[1] == 0 and z[0].denominator == 1 for z in psi)
    out, s_total = [], Fraction(0)
    marginals_half = True
    for x, y in product((0, 1), repeat=2):
        a, b = FRAMES_A[x], FRAMES_B[y]
        ua = {1: a, -1: (-a[1], a[0])}
        ub = {1: b, -1: (-b[1], b[0])}
        sizes = {}
        for s, t in product((1, -1), repeat=2):
            overlap = sum(ua[s][i] * ub[t][j] * whole[2 * i + j] for i in range(2) for j in range(2))
            sizes[(s, t)] = overlap * overlap
        total = sum(sizes.values())
        e = Fraction(sum(s * t * v for (s, t), v in sizes.items()), total)
        for side in (0, 1):
            for v in (1, -1):
                p = Fraction(sum(n for k, n in sizes.items() if k[side] == v), total)
                marginals_half &= p == Fraction(1, 2)
        s_total += (-1 if (x, y) == (1, 1) else 1) * e
        out.append(
            f"  settings {x}{y}: sizes {[sizes[k] for k in ((1, 1), (1, -1), (-1, 1), (-1, -1))]}, E = {e}"
        )
    out.append(f"  S = {s_total}; every marginal 1/2: {marginals_half}")
    return out


# 4. The room of closed composites.


def catalan(m: int) -> int:
    return comb(2 * m, m) // (m + 1)


def closed_count(n: int, ls) -> Fraction:
    """(1/48) SUM over the lifts of chi^n, chi = tr M / sqrt N, exact for even n through chi^2 = (2 a)^2 / N."""
    if n % 2:
        return Fraction(0)
    return sum(Fraction((2 * q[0]) ** 2, norm(q)) ** (n // 2) for q in ls) / len(ls)


def part_four(ls) -> list[str]:
    gens = generators_of(ls)
    out = []
    direct = {n: len(invariant_hands(n, gens)) for n in (2, 4, 6)}
    rows = []
    for n in range(2, 17, 2):
        k = closed_count(n, ls)
        assert k.denominator == 1
        rows.append((n, int(k), catalan(n // 2)))
    out.append("  halves n: " + ", ".join(str(n) for n, _, _ in rows))
    out.append("  closed under the 24: " + ", ".join(str(k) for _, k, _ in rows))
    out.append("  closed under the sphere (Catalan): " + ", ".join(str(s) for _, _, s in rows))
    out.append(
        "  each pair of halves more multiplies the 24's count by "
        + ", ".join(f"{rows[i + 1][1] / rows[i][1]:.2f}" for i in range(len(rows) - 1))
    )
    out.append(
        f"  the null space itself at n = 2, 4, 6: {direct[2]}, {direct[4]}, {direct[6]} "
        f"(the count's {rows[0][1]}, {rows[1][1]}, {rows[2][1]})"
    )
    odd = all(closed_count(n, ls) == 0 for n in range(1, 17, 2))
    out.append(f"  an odd number of halves has no closed hand (n = 1 to 15): {odd}")
    return out


def main() -> None:
    ls = lifts()
    lines = [
        "The twins' shared hand forced by the 24, and the room of closed composites (David, 2026-10-29)",
        "",
    ]
    lines.append("1. The 24 and their lifts")
    lines.extend(part_one())
    lines.append("")
    lines.append("2. The twins' joint hand at a birth alike under the 24")
    two = part_two(ls)
    lines.extend(two)
    lines.append("")
    lines.append("3. The forced hand's sizes in the Boss's frames")
    psi = invariant_hands(2, ls)[0]
    lines.extend(part_three(psi))
    lines.append("")
    lines.append("4. The room of closed composites (A1 joint hands of n halves)")
    lines.extend(part_four(ls))
    print("\n".join(lines))


if __name__ == "__main__":
    main()

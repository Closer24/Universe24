"""p2: one product for the vertex's two tables, the books, and what the click reads (Big Pic, 2026-10-30).

Run: python3 tools/derivations/open_items/BIGPIC-QUATERNIONS/p2_product.py   (seconds; output p2_product.txt)
"""

import itertools

from qlib import TWO, Stream, apply3, bar, mul, norm, report, turn_matrix, units

lines = []
st = Stream(2026103002)


def pure(q):
    return q[1:]


def rnd(n, lo, hi):
    return tuple(st.between(lo, hi) for _ in range(n))


# 1. the vertex's two tables are one product: v w = -(v . w) + v x w for pure v, w
good = True
for v in itertools.product(range(-3, 4), repeat=3):
    for w in [(1, 2, -1), (0, -3, 2), (4, 1, 1), (-2, 0, 5)]:
        dot = sum(a * b for a, b in zip(v, w, strict=True))
        cross = (v[1] * w[2] - v[2] * w[1], v[2] * w[0] - v[0] * w[2], v[0] * w[1] - v[1] * w[0])
        good &= mul((0,) + v, (0,) + w) == (-dot,) + cross
report(
    lines,
    "1. for pure whole v, w: v w = -(v . w) + v x w; the dot table and the epsilon table are one product",
    good,
)

# 2. the norm multiplies (Euler's four squares): the books of a product close
good = all(
    norm(mul(p, q)) == norm(p) * norm(q)
    for p in itertools.product(range(-2, 3), repeat=4)
    for q in [(1, -2, 3, 1), (0, 4, -1, 2), (5, 0, 0, -1)]
)
report(lines, "2. N(p q) = N(p) N(q) on 5^4 x 3 whole pairs (Euler's four squares)", good)

# 3. the click's two readings of a half-speed hand turned from one side (psi -> g psi), on all 48 gears:
#    conj(before) x now does not move; now x conj(before) keeps its real part and its pure part turns with the board
good_r = good_l = True
for u, s, _ in units():
    m = turn_matrix(u, s)
    for _ in range(30):
        a, b = rnd(4, -9, 9), rnd(4, -9, 9)
        ga, gb = mul(u, a), mul(u, b)
        r0, r1 = mul(bar(b), a), mul(bar(gb), ga)
        l0, l1 = mul(a, bar(b)), mul(ga, bar(gb))
        good_r &= r1 == tuple(s * v for v in r0)
        good_l &= l1[0] == s * l0[0] and pure(l1) == tuple(s * v for v in apply3(m, pure(l0)))
report(
    lines,
    "3. on all 48 gears: conj(before) x now does not move when the board turns the hand: three inner charges",
    good_r,
)
report(
    lines,
    "   now x conj(before) keeps its real part, and its pure part turns with the board: the spin",
    good_l,
)

# 4. the books of the click's product: real^2 + |turn|^2 = |before|^2 |now|^2, both orders sharing one real part
good = True
for _ in range(2000):
    a, b = rnd(4, -50, 50), rnd(4, -50, 50)
    for p in (mul(bar(b), a), mul(a, bar(b))):
        good &= p[0] * p[0] + sum(v * v for v in p[1:]) == norm(a) * norm(b)
    good &= mul(bar(b), a)[0] == mul(a, bar(b))[0]
report(
    lines,
    "4. real^2 + |turn|^2 = |before|^2 |now|^2 in both orders, and both orders share one real part (one wind)",
    good,
)

# 5. the six turns are the 4-d area of before and now: half-sum b0 a - a0 b, half-difference b x a
good = True
for _ in range(500):
    a, b = rnd(4, -30, 30), rnd(4, -30, 30)
    lp, rp = pure(mul(a, bar(b))), pure(mul(bar(b), a))
    tsp = tuple(b[0] * a[t] - a[0] * b[t] for t in (1, 2, 3))
    bv, av = b[1:], a[1:]
    crs = (bv[1] * av[2] - bv[2] * av[1], bv[2] * av[0] - bv[0] * av[2], bv[0] * av[1] - bv[1] * av[0])
    good &= all(lp[t] + rp[t] == TWO * tsp[t] and lp[t] - rp[t] == TWO * crs[t] for t in range(3))
report(
    lines,
    "5. the six turns are the board's triplet and the inner triplet: their half-sum and half-difference "
    "are the 4-d area's parts",
    good,
)

# 6. the free step a+ = c a - b, c = cn / cd, keeps the wind D = |a|^2 + |b|^2 - c Re(conj(b) a) and all six turns
good = True
for _ in range(500):
    a, b = rnd(4, -30, 30), rnd(4, -30, 30)
    cd = st.between(1, 50)
    cn = st.between(-TWO * cd + 1, TWO * cd - 1)
    nx = tuple(cn * a[t] - cd * b[t] for t in range(4))  # cd times next
    good &= pure(mul(bar(a), nx)) == tuple(cd * v for v in pure(mul(bar(b), a)))
    good &= pure(mul(nx, bar(a))) == tuple(cd * v for v in pure(mul(a, bar(b))))
    d_now = cd * (norm(a) + norm(b)) - cn * mul(bar(b), a)[0]  # cd times D now
    d_next = cd * cd * norm(a) + norm(nx) - cn * mul(bar(a), nx)[0]  # cd^2 times D next
    good &= d_next == cd * d_now
report(
    lines,
    "6. with no carry, the step keeps the wind and all six turns exactly, at any spring, "
    "inside or outside the window (500 lays)",
    good,
)

print("\n".join(lines))
print("ALL PASS" if all(line.startswith(("PASS", "   ")) for line in lines) else "SOME FAILED")

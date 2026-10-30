"""p8: Euclid's division on whole quaternions, and the four-fold tie it needs the halves for (Big Pic, 2026-10-30).

1. Hurwitz's division: a = q b + r with N(r) <= N(b) / 2, the quotient the nearer of the whole and the all-halves
   roundings (one compare: the reason no per-gear carry makes it).
2. The covering radii on the grid of eighths: part by part (Lipschitz) the worst remainder is the full divisor, at the
   four-fold tie (1 + i + j + k)/2; with the halves (Hurwitz) it is half; the half-D4 lattice a quarter.
3. The octahedral order over Z[root 2] (all 48 gears): the absolute norm's worst remainder is 1/2 exactly at its double
   deep holes, and no point met near them exceeds it. Run: python3 .../p8_euclid.py (about a minute; p8_euclid.txt).
"""

import itertools

from qlib import ONE, TWO, Stream, bar, carry, mul, order_basis, report

lines = []
st = Stream(2026103008)


def nearest(n, d):  # the whole number nearest n / d (d > 0), halves up: one carry
    q, _ = carry(TWO * n + d, TWO * d, 0)
    return q


# 1. Hurwitz's division with remainder, on 20,000 pairs of whole-or-all-halves quaternions held as 2x
def rnd_h():
    par = st.below(TWO)
    return tuple(TWO * st.between(-30, 30) + par for _ in range(4))


def dist(q2, P, M):  # |2P - M q2|^2, the distance to a candidate times M^2
    return sum((TWO * p - M * q) ** 2 for p, q in zip(P, q2, strict=True))


worst_n, worst_d, ok = 0, ONE, True
for _ in range(20000):
    a2, b2 = rnd_h(), rnd_h()
    M = sum(v * v for v in b2)  # |2b|^2
    if M == 0:
        continue
    P = mul(a2, bar(b2))  # (2a)(2b)^-bar = 4 a b-bar; a b^-1 = P / M
    ev = tuple(TWO * nearest(p, M) for p in P)  # the nearest whole point, as 2q
    od = tuple(
        TWO * nearest(TWO * p - M, TWO * M) + ONE for p in P
    )  # the nearest all-halves point, as 2q
    q2 = ev if dist(ev, P, M) <= dist(od, P, M) else od  # one compare
    r2 = tuple(x - y for x, y in zip(a2, (carry(v, TWO, 0)[0] for v in mul(q2, b2)), strict=True))
    nr = sum(v * v for v in r2)
    ok &= TWO * nr <= M
    if nr * worst_d > worst_n * M:
        worst_n, worst_d = nr, M
report(
    lines,
    "1. Hurwitz: a = q b + r with N(r) <= N(b) / 2 on 20,000 pairs, q the nearer of two roundings (one compare)",
    ok,
    f"the largest N(r) / N(b) met {worst_n} / {worst_d}",
)


# 2. covering radii on the grid of eighths (x = x8 / 8), as |x - h|^2 times 64
def far(points_ok, x8):
    best = None
    for h2 in itertools.product(range(-2, 4), repeat=4):  # h = h2 / 2
        if points_ok(h2):
            d = sum((x8[t] - 4 * h2[t]) ** 2 for t in range(4))
            best = d if best is None else min(best, d)
    return best


def even(v):
    return carry(v, TWO, 0)[1] == 0


lip = lambda h2: all(even(v) for v in h2)  # noqa: E731
hur = lambda h2: len({even(v) for v in h2}) == ONE  # noqa: E731
d4h = lambda h2: even(sum(h2))  # noqa: E731
grid = list(itertools.product(range(0, 8), repeat=4))
L, H, Dh = (max(far(f, x) for x in grid) for f in (lip, hur, d4h))
report(
    lines,
    f"2. the worst |x - q|^2 on the grid of eighths: part by part {L}/64 (the full divisor), with the halves "
    f"{H}/64 (half), half-D4 {Dh}/64",
    L == 64 and H == 32 and Dh == 16,
)
report(
    lines,
    "   the four-fold tie (1+i+j+k)/2 lies at 1 from its nearest part-by-part points and is itself an "
    "all-halves point, a corner turn's gear",
    far(lip, (4, 4, 4, 4)) == 64 and far(hur, (4, 4, 4, 4)) == 0,
)

# 3. the octahedral order: the absolute norm N(x - q) = (P^2 - 2 R^2) / (16 m^4) for x = y / 2m
B, D, adj = order_basis()


def best_remainder(y, m, span):
    c = [sum(y[i] * adj[i][j] for i in range(8)) for j in range(8)]
    base = [carry(cj, m * D, 0)[0] for cj in c]
    best = None
    for off in itertools.product(range(-span + 1, span + 1) if span > ONE else range(0, TWO), repeat=8):
        cq = [b + o for b, o in zip(base, off, strict=True)]
        q2 = [sum(cq[k] * B[k][t] for k in range(8)) for t in range(8)]
        z = [y[t] - m * q2[t] for t in range(8)]
        P = sum(z[TWO * t] ** 2 + TWO * z[TWO * t + 1] ** 2 for t in range(4))
        R = sum(TWO * z[TWO * t] * z[TWO * t + 1] for t in range(4))
        num = P * P - TWO * R * R
        best = num if best is None else min(best, num)
    return best, 16 * m**4


holes = (
    ("(1+i)/2 + root2 (1/2)", [1, 1, 1, 0, 0, 0, 0, 0], 1),
    ("(1+i)/2 + root2 (1/4)(1+i+j+k)", [2, 1, 2, 1, 0, 1, 0, 1], 2),
    ("(1+j)/2 + root2 (1/2) k", [1, 0, 0, 0, 1, 0, 0, 1], 1),
)
hole_vals = [(name,) + best_remainder(y, m, TWO) for name, y, m in holes]
lines.append("   the double deep holes, least N(x - q) over 4^8 candidates: " + str(hole_vals))
report(
    lines,
    "3. the octahedral order: at its three double deep holes the least absolute norm of x - q is 1/2 exactly",
    all(TWO * n == d for _, n, d in hole_vals),
)
worst = (0, ONE)
for _ in range(3000):
    m = 48
    centre = [[1, 1, 1, 0, 0, 0, 0, 0], [2, 1, 2, 1, 0, 1, 0, 1]][st.below(TWO)]
    scale = m if centre[0] == ONE else carry(m, TWO, 0)[0]
    y = [scale * c + st.between(-6, 6) for c in centre]
    n, d = best_remainder(y, m, ONE)
    if n * worst[1] > worst[0] * d:
        worst = (n, d)
report(
    lines,
    "   3,000 points close around the double deep holes: none exceeds 1/2",
    TWO * worst[0] <= worst[1],
    f"the largest least N(x - q) met {worst[0]} / {worst[1]}",
)
print("\n".join(lines))
print("ALL PASS" if all(line.startswith(("PASS", "   ")) for line in lines) else "SOME FAILED")

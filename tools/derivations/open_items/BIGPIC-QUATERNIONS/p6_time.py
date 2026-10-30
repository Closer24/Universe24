"""p6: the time part, the beat and its mirror (Big Pic, 2026-10-30).

The beat maps (now, before) to (next, now) by M = [[c, -1], [1, 0]], c = 2 - k/W. Run: python3 .../p6_time.py
(about half a minute; output p6_time.txt).
"""

from qlib import ONE, TWO, carry, report

lines = []


def m2(a, b):
    return (
        (a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]),
        (a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]),
    )


I2 = ((1, 0), (0, 1))
S = ((0, 1), (1, 0))
ok_det = ok_tr = ok_mirror = True
for c in range(-9, 10):
    M = ((c, -ONE), (ONE, 0))
    Minv = ((0, ONE), (-ONE, c))
    ok_det &= M[0][0] * M[1][1] - M[0][1] * M[1][0] == ONE
    P, tn = M, [TWO, c]
    for _ in range(TWO, 9):
        P = m2(P, M)
        tn.append(c * tn[-1] - tn[-2])
        ok_tr &= P[0][0] + P[1][1] == tn[-1]
    ok_mirror &= m2(M, Minv) == I2 and m2(m2(S, M), S) == Minv
report(lines, "1. the beat has determinant 1 and trace c for every whole c in -9..9", ok_det)
report(
    lines,
    "   the traces of its powers follow t_(n+1) = c t_n - t_(n-1): 2 cos(n w) with 2 cos w = c",
    ok_tr,
)
report(
    lines,
    "2. the time mirror is the swap S (determinant -1), and S M S = M^-1: the beat run backward",
    ok_mirror,
)


# 3. on the act, with the carry: inside the window 0 < k/W < 4 the hand stays on its ellipse; outside it runs away
def peaks(kappa, W, L, rounds):
    r, _ = carry(W, TWO, 0)
    a, b = L, L
    top = 0
    for _ in range(rounds):
        q, r = carry(W * (a - b) - kappa * a, W, r)
        a, b = a + q, a
        top = max(top, abs(a))
    return top


W, L = 1000, 10**6
inside = []
for k in (1, 100, 1000, 2000, 3000, 3990):
    top = peaks(k, W, L, 4000)
    bound = 4 * L * L * W  # A^2 (4W - k): the exact ellipse's largest a^2, times (4W - k)
    inside.append((k, top * top * (4 * W - k) * 1000 <= bound * 1001))
report(
    lines,
    "3. inside the window (k/W = 0.001 to 3.99) the hand's largest a^2 stays within a thousandth of its "
    "ellipse's 4 L^2 W / (4W - k) over 4,000 rounds",
    all(ok for _, ok in inside),
    str(inside),
)
outside = [(k, peaks(k, W, L, 60) > 10**8) for k in (4010, 4500, 6000)]
report(
    lines,
    "   outside it (k/W = 4.01 to 6) it runs past a hundred times its lay within 60 rounds",
    all(ok for _, ok in outside),
    str(outside),
)

print("\n".join(lines))
print("ALL PASS" if all(line.startswith(("PASS", "   ")) for line in lines) else "SOME FAILED")

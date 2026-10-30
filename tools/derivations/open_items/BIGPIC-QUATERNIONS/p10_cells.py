"""p10: one cell rule for the carry and the draw, the run back's tooth, and a beat with a whole sine (Big Pic, 2026-10-30).

1. The half-open carry, x = 2D q + s with s in [-D, D - 1]: the mirror -1 - x goes to (-q, -1 - s).
2. The draw: a pointer u in [0, W) falls in the half-open cell of one part, the parts' sizes in their own order; the
   mirrored pointer W - 1 - u, read against the parts from the other end, falls in the same part. With equal sizes the
   draw's cell is the carry's quotient.
3. An increment odd under reversal: run back with its tooth kept, it recovers (-q, k); flipped by (iii), it does not.
4. W = a^2 + b^2 and k = 4 b^2: k (4W - k) = (4ab)^2, so cos w = (a^2 - b^2)/(a^2 + b^2) and sin w = 2ab/(a^2 + b^2),
   the beat the Gaussian square (a + bi)^2 over its norm. Run: python3 .../p10_cells.py (seconds; p10_cells.txt).
"""

import itertools

from qlib import ONE, TWO, Stream, carry, report

lines = []
st = Stream(2026103010)


def half_open(x, D):
    q, s = carry(x + D, TWO * D, 0)
    return q, s - D


# 1. the half-open carry's mirror
ok = all(
    half_open(-ONE - x, D) == (-half_open(x, D)[0], -ONE - half_open(x, D)[1])
    and -D <= half_open(x, D)[1] <= D - ONE
    for D in range(1, 9)
    for x in range(-60, 61)
)
report(
    lines,
    "1. the half-open carry: -1 - x goes to (-q, -1 - s), for every D from 1 to 8 and x from -60 to 60",
    ok,
)


# 2. the draw and its run back
def part(u, sizes):
    c = 0
    for k, s in enumerate(sizes, 1):
        if c <= u < c + s:
            return k
        c += s


cases = 0
ok = True
for n in range(1, 5):
    for sizes in itertools.product(range(1, 6), repeat=n):
        W = sum(sizes)
        for u in range(W):
            ok &= n - part(W - ONE - u, sizes[::-1]) + ONE == part(u, sizes)
            cases += 1
report(
    lines,
    f"2. the mirrored pointer W - 1 - u against the parts read from the other end picks the same part: "
    f"{cases} cases",
    ok,
)
report(
    lines,
    "   with equal sizes m the draw's cell is the carry's quotient",
    all(
        part(u, [m] * n) - ONE == carry(u, m, 0)[0]
        for m in range(1, 7)
        for n in range(1, 6)
        for u in range(m * n)
    ),
)

# 3. the tooth of an increment odd under reversal: kept, not flipped
kept = flipped = 0
N = 20000
for _ in range(N):
    D = st.between(1, 50)
    m = TWO * D
    x = st.between(-(10**4), 10**4)
    k = st.between(-D, D - ONE)
    q, k1 = half_open(x + k, D)  # forward: x + k = q m + k1
    kept += half_open(-x + k1, D) == (-q, k)  # back, odd increment -x, tooth kept
    flipped += half_open(-x - ONE - k1, D) == (-q, -ONE - k)
report(
    lines,
    f"3. an odd increment run back with its tooth kept recovers (-q, k): {kept} of {N}; flipped by (iii): "
    f"{flipped} of {N}",
    kept == N and flipped < N,
)

# 4. a beat with a whole sine
ok = True
for a in range(1, 30):
    for b in range(1, 30):
        W, k = a * a + b * b, 4 * b * b
        ok &= (
            k * (4 * W - k) == (4 * a * b) ** 2
            and TWO * W - k == TWO * (a * a - b * b)
            and 0 < k < 4 * W
        )
report(
    lines,
    "4. W = a^2 + b^2, k = 4 b^2: k (4W - k) = (4ab)^2, cos w = (a^2 - b^2)/(a^2 + b^2), inside the window "
    "(a, b from 1 to 29); a = 7, b = 1 is W = 50, k = 4: cos w = 24/25, sin w = 7/25",
    ok and (7 * 7 - 1) * 25 == 24 * 50 and TWO * 7 * 25 == 7 * 50,
)

print("\n".join(lines))
print("ALL PASS" if all(line.startswith(("PASS", "   ")) for line in lines) else "SOME FAILED")

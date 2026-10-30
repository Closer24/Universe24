"""p9: free two-part and four-part hands on the act, with the carry, read by windows (Big Pic, 2026-10-30).

Each part steps by the act: q, r+ = carry(W (a - b) - k a, W, r), a+ = a + q. Read each round from before and now:
the wind W D = W (|a|^2 + |b|^2) - (2W - k) Re(conj(b) a), the board's triplet Pure(a conj(b)) and the inner triplet
Pure(conj(b) a). Their window means (12,000 rounds) over 240,000 rounds, in grains (one count's worth at radius R).
Run: python3 .../p9_act.py (a few minutes; output p9_act.txt).
"""

from qlib import TWO, bar, carry, mul, norm, report

lines = []
W, KAPPA, R = 10**6, 3 * 10**4, 10**7
ROUNDS, WIN = 240000, 12000


def run(parts, a0, v0):
    a = list(a0)
    b = [a0[t] - v0[t] for t in range(parts)]
    half, _ = carry(W, TWO, 0)
    r = [half] * parts
    pad = lambda x: tuple(x) + (0,) * (4 - parts)  # noqa: E731
    sums, cur, n = [], None, 0
    for _ in range(ROUNDS):
        A, Bq = pad(a), pad(b)
        P, Q = mul(A, bar(Bq)), mul(bar(Bq), A)
        row = (W * (norm(A) + norm(Bq)) - (TWO * W - KAPPA) * Q[0],) + P[1:] + Q[1:]
        cur = row if cur is None else tuple(x + y for x, y in zip(cur, row, strict=True))
        n += 1
        if n == WIN:
            sums.append(tuple(carry(x, WIN, 0)[0] for x in cur))
            cur, n = None, 0
        for t in range(parts):
            q, r[t] = carry(W * (a[t] - b[t]) - KAPPA * a[t], W, r[t])
            a[t], b[t] = a[t] + q, a[t]
    return sums


def grains(series, grain):
    first = series[0]
    return [
        carry(x - first, grain, 0)[0] if x >= first else -carry(first - x, grain, 0)[0] for x in series
    ]


cases = (
    ("two-part, a circle", 2, (R, 0), (0, 1700)),
    ("two-part, another", 2, (R, carry(R, 3, 0)[0]), (-500, 1300)),
    (
        "four-part, one lay",
        4,
        (R, carry(R, TWO, 0)[0], carry(-R, 3, 0)[0], carry(R, 5, 0)[0]),
        (0, 1700, -900, 400),
    ),
    ("four-part, another", 4, (carry(R, TWO, 0)[0], -R, carry(R, 4, 0)[0], 0), (800, 0, 1100, -600)),
)
widest = {}
for name, parts, a0, v0 in cases:
    sums = run(parts, a0, v0)
    cols = list(zip(*sums, strict=True))
    keep = [0, 3] if parts == TWO else [0, 1, 2, 3, 4, 5, 6]
    for c in keep:
        label = (
            "wind"
            if c == 0
            else ("board turn " + "ijk"[c - 1] if c <= 3 else "inner turn " + "ijk"[c - 4])
        )
        g = grains(cols[c], W * R if c == 0 else R)
        widest[(name, label)] = max(abs(x) for x in g)
        lines.append(f"   {name}, {label}: window means from the first, in grains: {g}")
two_turn = max(widest[(n, "board turn k")] for n, p, _, _ in cases if p == TWO)
two_wind = max(widest[(n, "wind")] for n, p, _, _ in cases if p == TWO)
four_turn = max(v for (n, lab), v in widest.items() if n.startswith("four") and lab != "wind")
report(
    lines,
    "1. a free two-part hand's turn (its one charge) holds to under one grain in every window over 240,000 rounds",
    two_turn == 0,
    f"widest {two_turn}",
)
report(
    lines,
    "2. its wind's window mean wanders by up to ten grains: within grains, not exactly",
    0 < two_wind <= 10,
    f"widest {two_wind}",
)
report(
    lines,
    "3. a four-part hand's six turns wander back and forth by up to about thirty grains",
    four_turn <= 30,
    f"widest {four_turn}",
)

print("\n".join(lines))
print("ALL PASS" if all(line.startswith(("PASS", "   ")) for line in lines) else "SOME FAILED")

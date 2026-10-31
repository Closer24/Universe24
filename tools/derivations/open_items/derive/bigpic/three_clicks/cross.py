"""R3 on the real act, per edge and between edges, in whole numbers: each edge's lives (the rounds between two clicks
at one Node-clock), their variance over their mean squared in per mille (1000 for lives drawn with no memory, near 0
for a clock striking on its beat); and between two edges, the signed square of the correlation of their per-round
gaps (booked less swept, dial q - x), beside the same for their swept flows, which the board shares and the turn does
not choose.

Usage: python3 -I cross.py <src> <world> <rounds> [modes, e.g. 045] [laid]
"""
import sys

src, world, rounds = sys.argv[1], sys.argv[2], int(sys.argv[3])
modes = [int(m) for m in (sys.argv[4] if len(sys.argv) > 4 else "045")]
laid = len(sys.argv) > 5 and "laid" in sys.argv[5]
sys.path.insert(0, src)
sys.path.insert(0, ".")
import edgeclick as E  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402


def signed_r2(xs, ys):
    n = len(xs)
    sx, sy = sum(xs), sum(ys)
    num = n * sum(x * y for x, y in zip(xs, ys)) - sx * sy
    dx = n * sum(x * x for x in xs) - sx * sx
    dy = n * sum(y * y for y in ys) - sy * sy
    if dx == 0 or dy == 0:
        return None
    q, _ = carry(1000 * num * num, dx * dy, 0)
    return q if num >= 0 else -q


for mode in modes:
    a = E.run(src, world, rounds, mode, laid=laid)
    dial, ne, sites = a["dial"], len(a["pairs"]), a["sites"]
    q = {(t, x, e): c for (t, x, e, c) in a["sides"]}
    gaps = [[dial * q.get((t, x, e), 0) - a["flows"][t][x][e] for x in range(sites) for t in range(rounds)] for e in range(ne)]
    flows = [[a["flows"][t][x][e] for x in range(sites) for t in range(rounds)] for e in range(ne)]
    lives = []
    for e in range(ne):
        ds = []
        for x in range(sites):
            last = None
            for t in range(rounds):
                if q.get((t, x, e), 0):
                    if last is not None:
                        ds.append(t - last)
                    last = t
        n, s1, s2 = len(ds), sum(ds), sum(d * d for d in ds)
        lives.append((n, carry(1000 * (n * s2 - s1 * s1), s1 * s1, 0)[0] if s1 else None, carry(1000 * s1, n, 0)[0] if n else None))
    print(f"{world}{', laid' if laid else ''}, {E.NAMES[mode]}, {rounds} rounds: books open {a['books_open']} of {a['places']}; run back {a['runback']}")
    for e, pr in enumerate(a["pairs"]):
        n, vm, mean = lives[e]
        print(f"   edge {pr}: {n} lives, their mean {mean} per mille of a round, variance over mean squared {vm} per mille")
    for e in range(ne):
        for f in range(e + 1, ne):
            print(f"   edges {a['pairs'][e]} and {a['pairs'][f]}: the gaps' signed squared correlation {signed_r2(gaps[e], gaps[f])} per mille,"
                  f" the flows' {signed_r2(flows[e], flows[f])} per mille")

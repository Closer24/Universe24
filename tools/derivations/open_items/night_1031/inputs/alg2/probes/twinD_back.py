"""ALG1: the D-twin pair's run back by the same round on the mirrored pair (tau kept, the twin flipped on its dial D),
the passings negated and in reverse order, from the end alone; every pair of the dials 3D = 63 and 255. Whole numbers.
Args: <tree> <rounds>"""
import sys
from pathlib import Path

tree, rounds = Path(sys.argv[1]), int(sys.argv[2])
sys.path.insert(0, str(tree.joinpath("src")))
from tensor24.algebra.carry import carry  # noqa: E402

for D in (21, 85):
    D3 = 3 * D
    B3, _ = carry(D3 - 1, 2, 0)
    BD, _ = carry(D - 1, 2, 0)

    def cen3(v):
        return carry(v + B3, D3, 0)[1] - B3

    def cenD(v):
        return carry(v + BD, D, 0)[1] - BD

    def rnd(u, v, y):
        v = cenD(v + 3 * u)
        u = cen3(u + 3 * v)
        w, tt = carry(y, D3, u + B3)
        u = tt - B3
        u = cen3(u + 3 * v)
        v = cenD(v + 3 * u)
        return u, v, w

    ys = [carry(7919 * k, 2 * D + 1, 0)[1] - D + carry(104729 * k, 2 * D + 1, 0)[1] - D for k in range(rounds)]
    bad, wsum_bad = 0, 0
    for t0 in range(-B3, D3 - B3):
        for e0 in range(-BD, D - BD):
            u, v, ws = t0, e0, []
            for y in ys:
                u, v, w = rnd(u, v, y)
                ws.append(w)
            u, v = u, cenD(-v)  # the mirror: tau kept, the twin flipped
            back = []
            for y in reversed(ys):
                u, v, w = rnd(u, v, -y)
                back.append(w)
            u, v = u, cenD(-v)
            bad += int((u, v) != (t0, e0))
            wsum_bad += int(back != [-w for w in reversed(ws)])
    print(f"D {D}: {D3 * D} pairs (tau on 3D, the twin on D), {rounds} rounds: run back misses the start {bad};"
          f" its landings not the forward ones negated and reversed {wsum_bad}")
print("END")

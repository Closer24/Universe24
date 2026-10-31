"""GEN4c probe: two clock facts and one piece of algebra, in whole numbers (Rule3's carry the one division).
Part 1: chi(g) / dim on the two third-turn lifts, w = (-1 + i + j + k) / 2 (order 3) and -w (order 6), as p + q r2.
Part 2: the Koide circle in the triangle of root shares, in exact Z[r2] pairs over a common denominator 6:
        s_2 = (1 + r2) / 3, s' = s'' = (2 - r2) / 6 sums to 1 and has SUM s^2 = 2/3; the median's other meeting is on
        the circle too. No order claim is printed: Z[r2] pairs have no order (ruling 4).
"""
from probe_half2 import CHI, INDEX, M1, MUL, carry, zmul

ONE = INDEX[((2, 0), (0, 0), (0, 0), (0, 0))]


def part1():
    w = INDEX[((-1, 0), (1, 0), (1, 0), (1, 0))]
    print("PART 1: chi(g) / dim on the third-turn lifts w (order 3) and -w (order 6)")
    order = {}
    for g in (w, MUL[M1][w]):
        x, n = g, 1
        while x != ONE:
            x, n = MUL[x][g], n + 1
        order[g] = n
    for name in ("A1", "T1", "E1/2", "E5/2", "G3/2"):
        dim = CHI[name][ONE][0]
        cells = [f"order {order[g]}: ({CHI[name][g][0]} + {CHI[name][g][1]} r2) / {dim}" for g in (w, MUL[M1][w])]
        print(f"  {name}: {cells[0]}; {cells[1]}")


def part2():
    print("PART 2: the Koide circle on the median s' = s'' (pairs p + q r2, all over 6)")
    s2 = (2, 2)  # (1 + r2) / 3 = (2 + 2 r2) / 6
    sp = (2, -1)  # (2 - r2) / 6
    total = (s2[0] + 2 * sp[0], s2[1] + 2 * sp[1])
    print(f"  6 (s_2 + 2 s') = {total[0]} + {total[1]} r2: the shares sum to 1: {total == (6, 0)}")
    sq = zmul(s2, s2)
    sq2 = zmul(sp, sp)
    q36 = (sq[0] + 2 * sq2[0], sq[1] + 2 * sq2[1])
    k, rem = carry(q36[0] * 3, 36, 0)
    print(f"  36 SUM s^2 = {q36[0]} + {q36[1]} r2; 3 x 36 SUM s^2 / 36 = {k} remainder {rem}: SUM s^2 = 2/3: "
          f"{q36 == (24, 0)}")
    centre = (2, 0)  # 1/3 = 2/6
    d2 = zmul((s2[0] - centre[0], s2[1]), (s2[0] - centre[0], s2[1]))
    dp = zmul((sp[0] - centre[0], sp[1]), (sp[0] - centre[0], sp[1]))
    r36 = (d2[0] + 2 * dp[0], d2[1] + 2 * dp[1])
    print(f"  36 |s - centre|^2 = {r36[0]} + {r36[1]} r2: = 36 / 3: {r36 == (12, 0)}")
    s2o = (6 - 2 * 2, -2 * 1)  # the median's other meeting, s' = (2 + r2) / 6: s_2 = (1 - r2) / 3 = (2 - 2 r2) / 6
    o2 = zmul(s2o, s2o)
    op = zmul((2, 1), (2, 1))
    qo = (o2[0] + 2 * op[0], o2[1] + 2 * op[1])
    print(f"  the median's other meeting, s' = (2 + r2) / 6 and s_2 = ({s2o[0]} + {s2o[1]} r2) / 6: sums to 1 "
          f"{(s2o[0] + 2 * 2, s2o[1] + 2 * 1) == (6, 0)}, 36 SUM s^2 = {qo[0]} + {qo[1]} r2 (on the circle: {qo == (24, 0)}); "
          f"its sign is an order claim, DERIVED on paper, not here")


part1()
part2()

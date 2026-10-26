"""The seam term, exact: about two centres c and c' on the torus, 2 L_c - 2 L_c' - 2 (c' - c) x P = SUM over the Links whose minimum-image arm differs by other than 2 (c' - c) of (the arm difference) x p; measured on the folder's light wave world at the first departure interval."""
import json
import sys

from am_reader import moment, positions, row_p
from event_universe.loader.world import load_world
from event_universe.node import Node

sys.set_int_max_str_digits(0)
universe, world = load_world(sys.argv[1])
intervals = int(sys.argv[2])
shape = tuple(int(x) for x in world["shape"])
c, c2 = [4, 4, 4], [6, 4, 4]
node = Node(universe, world)
d1, d2 = positions(shape, c), positions(shape, c2)
for t in range(intervals):
    node.step()
    L1, L2, P = [0, 0, 0], [0, 0, 0], [0, 0, 0]
    seam = [0, 0, 0]
    for row in node.records():
        p = row_p(row, int(row.pair[0]))
        l1, p1, _ = moment(p, d1, shape)
        l2, _, _ = moment(p, d2, shape)
        L1 = [L1[k] + l1[k] for k in range(3)]
        L2 = [L2[k] + l2[k] for k in range(3)]
        P = [P[k] + p1[k] for k in range(3)]
        # the Links whose arm difference is not 2 (c' - c): the term they add, exactly
        for a in range(3):
            for k, v in enumerate(p[a]):
                if v == 0:
                    continue
                arm1 = [d1[0][k], d1[1][k], d1[2][k]]
                arm2 = [d2[0][k], d2[1][k], d2[2][k]]
                arm1[a] += 1
                arm2[a] += 1
                diff = [arm1[j] - arm2[j] - 2 * (c2[j] - c[j]) for j in range(3)]
                if diff != [0, 0, 0]:
                    e = [0, 0, 0]
                    e[a] = v
                    seam[0] += diff[1] * e[2] - diff[2] * e[1]
                    seam[1] += diff[2] * e[0] - diff[0] * e[2]
                    seam[2] += diff[0] * e[1] - diff[1] * e[0]
    dz = [2 * (c2[j] - c[j]) for j in range(3)]
    cross = [dz[1] * P[2] - dz[2] * P[1], dz[2] * P[0] - dz[0] * P[2], dz[0] * P[1] - dz[1] * P[0]]
    left = [L1[k] - L2[k] - cross[k] for k in range(3)]
    print(json.dumps({"i": node.interval, "2L_c - 2L_c' - 2(c'-c)xP": left, "seam term": seam, "equal": left == seam, "P": P}))

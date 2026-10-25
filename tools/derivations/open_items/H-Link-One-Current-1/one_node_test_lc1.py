"""lc1's one-Node test (under 15 s, integers only): the Link's current at the two ends of one Link between two contents.

On the 3-cube at universe_toy the centre's carrier level is set to the volume of the content c (a well of one Node), every
other Node at the vacuum, and for the gap-0 row (a riding row) and the carrier's row the test reads, on the Link from the
centre i to its +X neighbour j:
  (a) the engine's reach from each end, R_ij (at i) and R_ji (at j): equal iff the paces are (the law's p_i^2);
  (b) the riding row's Link current, X_i R_ij against X_j R_ji (the kick's weight X at each end): one number from both
      ends to the rounding of X p_i^2 against Gamma^3, the residue in per mille;
  (c) the carrier's Link current R_ij against R_ji (its wall w carries no X): the two ends' ratio p_i^2 / p_j^2 in per mille.
Then 20 intervals of the hole world (the 3-cube, the sea with the hole) are run and the board's sum of the carrier's Links'
numerator is read at every interval (the lift's source, 0 by identity under a symmetric reach), with the run back 5 of 5.
Usage: LC1_SRC=<src> [LC1_FLAG=...] python one_node_test_lc1.py <contents, e.g. 5,50,500>
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("LC1_SRC", os.path.join(HERE, "..", "..", "..", "src")))

from event_universe.core.ports import across  # noqa: E402
from event_universe.features import volume  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER, PLANE  # noqa: E402


def permille(num, den):
    return (1000 * num) // den if den else 0


def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(os.path.join(HERE, "worlds", "bare_3_60.json"))
    for c in [int(x) for x in argv[1].split(",")]:
        node = Node(universe, world)
        x = node.row(CARRIER).lines[0]
        xc = int(volume.volume_of(node.gamma, np.array([c], dtype=object))[0])
        x.now[1, 1, 1] = xc
        x.before[1, 1, 1] = xc
        content = node.content()
        factors = node.link_factors()
        i, j = (1, 1, 1), (2, 1, 1)  # j the +X neighbour of the centre, Port 0
        out = {"content at the centre": c, "X at the centre": xc, "X at j": int(x.now[j])}
        for name, row in (("gap-0 row (riding)", node.row(PLANE, gap=0)), ("carrier row (wall w)", node.row(CARRIER))):
            rule = node.rule_of(row, content, factors)
            r_ij = int(np.asarray(rule.reaches[0], dtype=object)[i])  # Port 0 (+X) read at i
            r_ji = int(np.asarray(rule.reaches[1], dtype=object)[j])  # Port 1 (-X) read at j, back to i
            out[name] = {
                "R_ij at i": r_ij, "R_ji at j": r_ji, "R_ij / R_ji per mille": permille(r_ij, r_ji),
                "X_i R_ij": xc * r_ij, "X_j R_ji": int(x.now[j]) * r_ji,
                "(X_i R_ij - X_j R_ji) per mille of X_j R_ji": permille(xc * r_ij - int(x.now[j]) * r_ji, int(x.now[j]) * r_ji),
            }
        print(json.dumps(out))
    universe, world = load_world(os.path.join(HERE, "worlds", "hole_3_400.json"))
    node = Node(universe, world)
    sums = []
    hashes = []
    for t in range(20):
        if t >= 15:
            hashes.append(node.state_hash())
        xl = node.row(CARRIER).lines[0]
        xn = np.asarray(xl.now, dtype=object)
        rule = node.rule_of(node.row(CARRIER), node.content(), node.link_factors())
        arrivals = node.arrivals([xn], rule, None)[0]
        sums.append(int(np.sum(arrivals - sum(rule.reaches) * xn)))
        node.step()
    exact = 0
    for k in range(len(hashes)):
        node.step_back()
        exact += node.state_hash() == hashes[len(hashes) - 1 - k]
    print(json.dumps({"flag": os.environ.get("LC1_FLAG", ""), "hole 3-cube, 20 intervals: the carrier's Links' numerator summed over the board": sums, "intervals with the sum 0": sum(1 for s in sums if s == 0), "run back": [len(hashes), exact]}))


if __name__ == "__main__":
    main(sys.argv)

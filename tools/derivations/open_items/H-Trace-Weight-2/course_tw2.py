"""tw2's course of one world under the flagged copy at TW2_TRACE: per interval the carrier's X at the hole's Node
[0, 0, 0] (the first Node), the board's least, mean and greatest X, the count of turned Nodes, and the running counts
(met, births, body_clicks, laid, refused_lay, refused_stop); every `every` intervals, and the last. Usage:
course_tw2.py <world.json> <every>"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src_tw2"))

from event_universe import rows  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import CARRIER  # noqa: E402


def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    every = int(argv[2])
    node = Node(universe, world)
    n = int(world["intervals"])
    print(json.dumps({"trace": rows.TRACE, "world": os.path.basename(argv[1])}))
    for t in range(1, n + 1):
        node.step()
        if t % every == 0 or t == n:
            xs = [int(x) for x in node.row(CARRIER).lines[0].now.reshape(-1)]
            c = node.counts
            print(json.dumps({
                "i": t, "X[0]": xs[0], "X min/mean/max": [min(xs), sum(xs) // len(xs), max(xs)],
                "turned": int(node.turned.sum()) if hasattr(node, "turned") else None,
                "met": c["met"], "births": c["births"], "credits": c["body_clicks"], "laid": c["laid"],
                "refused_lay": c["refused_lay"], "refused_stop": c["refused_stop"],
            }))


if __name__ == "__main__":
    main(sys.argv)

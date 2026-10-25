"""pm2: light's click (the owner's word of 15:0x UTC): the gap-0 row's own credits and standing on a record. The Node run N intervals; at every interval: the Nodes where the gap-0 plane's share at the close's weight reads a whole quantum (node.standing[gap0] above 0), the longest standing run, the gap-0 re line's upward crossings this interval (re.before < 0 <= re.now, the beat's trigger), node.beats[gap0] max, the gap-0 credits so far (the log's credits with line = gap0), the births (two gap-0 quanta meeting at a Link). Usage: PYTHONPATH=<src> python light_click.py <world.json> <intervals>"""
import json
import sys

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import PLANE


def main(argv):
    universe, world = load_world(argv[1])
    n = int(argv[2])
    node = Node(universe, world)
    g = node.records().index(node.row(PLANE, gap=0))
    re = node.row(PLANE, gap=0).lines[0]
    crossings_total = 0
    standing_nodes_max = 0
    run_max = 0
    for t in range(n):
        node.step()
        re = node.row(PLANE, gap=0).lines[0]
        up = sum(1 for b, a in zip(re.before.reshape(-1), re.now.reshape(-1)) if int(b) < 0 <= int(a))
        crossings_total += up
        st = [int(v) for v in node.standing[g].reshape(-1)]
        standing_nodes = sum(1 for v in st if v > 0)
        standing_nodes_max = max(standing_nodes_max, standing_nodes)
        run_max = max(run_max, max(st))
        if node.interval in (1, 4, 10, 20, 50, 100, 120, 200, 300) or node.interval == n:
            print(json.dumps({"i": node.interval, "gap-0 nodes standing at a whole quantum": standing_nodes, "longest standing run so far": run_max, "gap-0 upward crossings this interval / so far": [up, crossings_total], "gap-0 beats max": max(int(v) for v in node.beats[g].reshape(-1)), "gap-0 credits so far": sum(1 for e in node.log if e["event"] == "credit" and e["line"] == g), "births so far": node.counts["births"], "body credits so far": node.counts["body_clicks"], "gap-0 levels min/max": [min(int(v) for v in re.now.reshape(-1)), max(int(v) for v in re.now.reshape(-1))]}))
    print(json.dumps({"end": n, "gap-0 credits": sum(1 for e in node.log if e["event"] == "credit" and e["line"] == g), "gap-0 credit nodes": sorted(set(tuple(e["node"]) for e in node.log if e["event"] == "credit" and e["line"] == g)), "births (two gap-0 quanta at a Link)": node.counts["births"], "standing nodes max": standing_nodes_max, "longest standing run": run_max, "upward crossings in all": crossings_total}))


if __name__ == "__main__":
    main(sys.argv)

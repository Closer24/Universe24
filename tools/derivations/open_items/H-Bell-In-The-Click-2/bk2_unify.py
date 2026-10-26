"""The generic unification the item exposes (the owner's word of 03:3x UTC): the birth's take (close.births) and the credit's take (bodies) are the one exact take of the gap-0 row at one Node (take.take_at), logged and undone alike (unclick), but the laid-back clause of EQ-S1 (the gap-0 current across the six Links summed 0 at the Node at the interval's start) stands on the credit alone. This reader counts, per record, the births whose take's Node has the gap-0 net current 0 at the start (where the one act would lay the birth's take back) beside the credits laid back and standing, and the first clicks of born pairs by the same reading. Integers only; no act touched.

Usage: python bk2_unify.py <world.json> <out.json>"""
import json
import sys
import time

from event_universe.core.ports import PORTS
from event_universe.links import row_current
from event_universe.node import Node
from event_universe.run import load_world


def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    node = Node(universe, world)
    intervals = int(world["intervals"])
    rec0 = node.records().index(node.emitter())
    t0 = time.monotonic_ns()
    births_net0 = births = credits = credits_net0 = laid = 0
    birth_nets = []
    for _ in range(intervals):
        net = sum((row_current(node.records()[rec0].lines, port) for port in range(PORTS)), start=0)
        n0 = len(node.log)
        node.step()
        for e in node.log[n0:]:
            if e["event"] == "birth":
                births += 1
                z = int(net[tuple(e["node"])])
                births_net0 += z == 0
                birth_nets.append(z)
            elif e["event"] == "credit":
                credits += 1
                credits_net0 += int(net[tuple(e["node"])]) == 0
                laid += "laid_back" in e
    out = {
        "world": argv[1], "intervals": intervals, "ms": (time.monotonic_ns() - t0) // 1000000,
        "births": births, "births whose take's Node has the gap-0 net current 0 at the start (laid back under the one act)": births_net0,
        "the births' net currents at the take's Node (least, largest)": [min(birth_nets), max(birth_nets)] if birth_nets else None,
        "credits": credits, "credits at a Node with net 0": credits_net0, "credits laid back (the log)": laid,
        "the credit's clause and the log agree": credits_net0 == laid,
    }
    with open(argv[2], "w", encoding="utf-8") as f:
        json.dump(out, f)
    print(json.dumps(out))


if __name__ == "__main__":
    main(sys.argv)

"""mk2: a world run with every record row's lattice momentum read before and after every close (the engine's own writer,
the flag MK2_RECOIL in the environment or not): the first interval with a click, the rows' P before and after that close,
the interval's own change of P between the closes (what the acts between the clicks move), summed in magnitude.
Usage: python momenta_mk2.py <world.json> <intervals> <out.json>. Integers only."""
import json
import os
import sys

import numpy as np

from event_universe.loader.world import load_world
from event_universe.node import Node

sys.set_int_max_str_digits(0)
AXES = 3


def momenta(node):
    found = []
    for row in node.records():
        per = []
        for a in range(AXES):
            total = 0
            for line in row.lines:
                moved = np.roll(line.now, -1, axis=a) * line.before - line.now * np.roll(line.before, -1, axis=a)
                total += sum(int(x) for x in moved.reshape(-1))
            per.append(2 * row.pair[0] * total)
        found.append(per)
    return found


def main(argv):
    universe, world = load_world(argv[1])
    node = Node(universe, dict(world, intervals=int(argv[2])))
    closes, original = [], node.click
    log_len = [0]

    def click(plane_starts, held, direction=1, frame=None):
        before = momenta(node)
        original(plane_starts, held, direction, frame)
        after = momenta(node)
        clicks = [e for e in node.log[log_len[0]:] if e["event"] in ("birth", "credit")]
        log_len[0] = len(node.log)
        closes.append({"i": node.interval, "before": before, "after": after, "clicks": len(clicks),
                       "dP_take": [sum(e["dP_take"][a] for e in clicks) for a in range(AXES)],
                       "dP_recoil": [sum(e.get("dP_recoil", [0] * AXES)[a] for e in clicks) for a in range(AXES)]})

    node.click = click
    for _ in range(int(argv[2])):
        node.step()
    first = next((c for c in closes if c["clicks"]), None)
    between = [0] * AXES
    for k in range(1, len(closes)):
        for a in range(AXES):
            between[a] += abs(closes[k]["before"][a_row][a] for a_row in [0])[0] if False else abs(sum(r[a] for r in closes[k]["before"]) - sum(r[a] for r in closes[k - 1]["after"]))
    out = {
        "world": argv[1], "flag": os.environ.get("MK2_RECOIL", ""), "closes": len(closes),
        "closes with clicks": sum(1 for c in closes if c["clicks"]),
        "first click interval": first["i"] if first else None,
        "rows P before the first clicking close": first["before"] if first else None,
        "rows P after it": first["after"] if first else None,
        "board P change across it": [sum(r[a] for r in first["after"]) - sum(r[a] for r in first["before"]) for a in range(AXES)] if first else None,
        "its dP_take summed": first["dP_take"] if first else None, "its dP_recoil summed": first["dP_recoil"] if first else None,
        "board P change across every close, abs summed": [sum(abs(sum(r[a] for r in c["after"]) - sum(r[a] for r in c["before"])) for c in closes) for a in range(AXES)],
        "board P change between the closes (the interval's own acts), abs summed": between,
        "board P at the start": [sum(r[a] for r in closes[0]["before"]) for a in range(AXES)] if closes else None,
        "board P at the end": [sum(r[a] for r in closes[-1]["after"]) for a in range(AXES)] if closes else None,
        "rows P at the end": closes[-1]["after"] if closes else None,
    }
    json.dump({"summary": out, "closes": closes}, open(argv[3], "w"))
    print(json.dumps(out))


if __name__ == "__main__":
    main(sys.argv)

"""The check of the reading (H-Helicity-From-The-Twist-1): the twist the close reads at every birth (close.meet's `twists`, links.row_twist on the record's `start` lines) recorded by a wrapper around the close's own call, and compared with the twists' file of twist_run.py (the state after the interval before). Integers only. Usage: python twist_check.py <world.json> <twists.json>"""
import json
import sys

from event_universe import run as engine
from event_universe.loader.world import load_world

close = sys.modules["event_universe.close"]
seen = []
original = close.row_twist


def recording(lines, axis):
    found = original(lines, axis)
    seen.append((axis, [int(x) for x in found.reshape(-1)]))
    return found


close.row_twist = recording


def main(argv):
    sys.set_int_max_str_digits(0)
    universe, world = load_world(argv[1])
    tw = json.load(open(argv[2]))
    node = engine.Node(universe, world)
    per_interval = {}
    for t in range(int(world["intervals"])):
        seen.clear()
        node.step()
        per_interval[node.interval] = list(seen)
    births = [e for e in node.log if e["event"] == "birth"]
    equal = read = 0
    off = []
    for b in births:
        i, rec = int(b["i"]), int(b["taken_row"])
        calls = per_interval[i]
        mine = tw["twists"][str(i - 1)][rec]
        # the close reads row_twist once per record and axis: the calls of this record are the rec-th group of three
        group = calls[3 * rec : 3 * rec + 3]
        for axis, values in group:
            read += 1
            signs = [(x > 0) - (x < 0) for x in values]
            if signs == mine[axis]:
                equal += 1
            else:
                off.append((i, rec, axis, sum(1 for a, c in zip(signs, mine[axis]) if a != c)))
    print(json.dumps({"births": len(births), "twist arrays read at the births (record, axis)": read, "equal to the twists' file at the interval before": equal, "off (i, rec, axis, nodes apart)": off[:20], "calls per interval (first birth's interval)": len(per_interval[int(births[0]["i"])]) if births else 0}))


if __name__ == "__main__":
    main(sys.argv)

"""One turned Node of the chiral 3-cube under A48-S1: the walled row's bit before and after its turn, the count of reversals per line at the next draw there, the remainder and its fold. Usage: frame_bit.py <src> <worktree>"""
import sys

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe import take  # noqa: E402
from event_universe.core.rule3 import mirrored, quotient, remainder  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.take import at_node  # noqa: E402

universe, world = load_world(sys.argv[2] + "/tests/worlds/world_node.json")
lays = [{"lay": "sea", "row": 0}, {"lay": "hole", "at": [0, 0, 0]}]
lays += [{"lay": "at", "row": 0, "centre": c, "quanta": 1} for c in ([1, 0, 0], [0, 2, 1], [2, 1, 0])]
world = dict(world, shape=[3, 3, 3], intervals=12, seed=lays)
node = Node(universe, world)
walled = node.rows_[0]
print("rows_[0] shape", walled.shape, "wall", walled.wall, "is rows_[0] the walled row:", walled.wall is not None)
print("walled rem at seed, unique values:", sorted(set(int(x) for x in walled.lines[0].rem.flat)))
shown = {"n": 0}
orig = take.read_number


def spy(nd, at, rules, unit):
    turned_here = int(nd.turn_counts[at]) if hasattr(nd, "turn_counts") else None
    bit = int(rules[0][0].rem[at])
    if bit == 0 and shown["n"] < 2:
        shown["n"] += 1
        is_im = nd.is_im()
        print("interval", nd.interval, "draw at Node", at, "walled bit", bit, "turns of the Node so far", turned_here)
        for li, (line, r) in enumerate(rules):
            wl = at_node(line.wall, at)
            rem = int(line.rem[at])
            count = (1 - bit) * (1 + is_im[li])
            rho = mirrored(rem, wl, count)
            folded = min(rho, remainder(wl - rho, wl))
            print("  line", li, "im" if is_im[li] else "re", "wall", wl, "rem", rem, "reversals", count, "rho", rho, "folded", folded)
    return orig(nd, at, rules, unit)


take.read_number = spy
import event_universe.close as close  # noqa: E402

close.read_number = spy
bits = {}
for _ in range(12):
    node.step()
    if node.turned is not None and node.turned.any():
        import numpy as np

        for at in zip(*np.nonzero(node.turned)):
            at = tuple(int(x) for x in at)
            bits.setdefault(at, []).append((node.interval, int(walled.lines[0].rem[at])))
print("turned Nodes: (interval, walled bit after the turn) per Node, first 4:", list(bits.items())[:4])
print("counts", {k: node.counts[k] for k in ("turns", "births", "body_clicks")})

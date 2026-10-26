"""vf11 (d): on the plasma_3 world through the top, the shape-4 row's time line's write remainder after each step equals what the kick's carried division left (no second division on that line: zero writes at its write wall, exactly one carried division at that wall per interval in either direction), and one step back returns it bit for bit."""
import sys

import numpy as np

sys.set_int_max_str_digits(0)
import event_universe.interval as iv  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.rows import POTENTIAL  # noqa: E402

seen = {"after_kick": None, "divisions_at_wall": [], "written_ids": set(), "time_line_written": 0, "unequal_at": []}
orig_kicks, orig_cd, orig_write = iv.Interval.kicks, iv.carried_division, Node.write


def kicks(self):
    orig_kicks(self)
    k = self.where[id(self.potential)]
    seen["after_kick"] = self.rows[k][0].wr.copy()


def cd(total, wall, remainder, direction=1):
    if wall == seen["wwall"]:
        seen["divisions_at_wall"].append(direction)
    return orig_cd(total, wall, remainder, direction)


def write(self, line, numerator, direction):
    seen["written_ids"].add(id(line))
    return orig_write(self, line, numerator, direction)


iv.Interval.kicks, iv.carried_division, Node.write = kicks, cd, write
universe, world = load_world(sys.argv[1])
n = int(sys.argv[2])
node = Node(universe, world)
seen["wwall"] = node.row(POTENTIAL).lines[0].wwall
print("the time line's write wall T:", seen["wwall"], "; every write wall of the shape-4 row and the gap-0 line:", sorted({line.wwall for r in node.rows_ for line in r.lines if line.wwall is not None and r.shape != 10}))
held, back_ok, fwd_div, bwd_div, nonzero_q = 0, 0, [], [], 0
for i in range(n):
    wr0 = node.row(POTENTIAL).lines[0].wr.copy()
    seen["divisions_at_wall"] = []
    seen["written_ids"] = set()
    node.step()
    seen["time_line_written"] += id(node.row(POTENTIAL).lines[0]) in seen["written_ids"]
    fwd_div.append(tuple(seen["divisions_at_wall"]))
    wr1 = node.row(POTENTIAL).lines[0].wr
    equal = bool(np.array_equal(wr1, seen["after_kick"]))
    held += equal
    if not equal:
        seen["unequal_at"].append(node.interval)
    nonzero_q += bool((wr1 != wr0).any())
    seen["divisions_at_wall"] = []
    node.step_back()
    bwd_div.append(tuple(seen["divisions_at_wall"]))
    back_ok += bool(np.array_equal(node.row(POTENTIAL).lines[0].wr, wr0))
    node.step()
print(f"intervals {n}: wr after the step equal to the kick's {held} of {n}; wr returned by one step back {back_ok} of {n}")
print(f"intervals where the time line was written by node.write: {seen['time_line_written']} of {n}; wr unequal to the kick's at the intervals {seen['unequal_at']}; divisions at that wall per forward interval: {sorted(set(fwd_div))}; per backward interval: {sorted(set(bwd_div))}")
print(f"intervals where the write remainder moved: {nonzero_q} of {n}; turns {node.turns}")

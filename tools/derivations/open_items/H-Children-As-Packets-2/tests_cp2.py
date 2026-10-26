"""cp2's test (under 15 s): on the hole world's Node at the seed, with CP2_FORM=1, one child packet laid at a wave number along x by close.child_at carries lattice momentum along x alone of the gain's sign, at most the ceiling 9 num (T div 2) per axis (the raised cosine's overlap 9/4 at the half-width 2 times 4 num A B), the packet at the wave 0 onto nothing carries none and its conjugate pair's charge sums to 0 exactly, every lay is undone bit for bit by its own undo, and every act is one Node's (27 Nodes, each with its six Links). Usage: CP2_FORM=1 PYTHONPATH=<copy> python tests_cp2.py"""
import os
import sys
import time

sys.set_int_max_str_digits(0)
assert os.environ.get("CP2_FORM") == "1", "run with CP2_FORM=1"
from event_universe import close  # noqa: E402
from event_universe.core.rule3 import largest_below, quotient  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402

t0 = time.time()
here = os.path.dirname(os.path.abspath(__file__))
u, w = load_world(os.path.join(here, "..", "..", "..", "..", "tests", "worlds", "world_hole.json"))
node = Node(u, w)
s = 1  # a plane with a gap, standing at nothing at the seed
row = node.records()[s]
num = row.pair[0]
where = (2, 2, 2)
state = lambda: [(int(a.now.sum()), int(a.before.sum()), tuple(int(x) for x in a.now.reshape(-1))) for a in row.lines]  # noqa: E731
start = state()
top = largest_below(quotient(node.den * node.den, 2))
acts = []
dp = close.child_at(node, s, where, 1, 1, (top, 0, 0), acts)
assert len(acts) == 27 and all(len(per) == 3 for _n, per in acts), "27 acts, each on one Node's six Links"
assert dp[1] == 0 and dp[2] == 0, ("a wave along x carries along x alone", dp)
ceiling = 9 * num * (node.A * node.B)
assert 0 < abs(dp[0]) <= ceiling, ("the ceiling 9 num (T div 2)", dp[0], ceiling)
close.child_at(node, s, where, 1, -1, (top, 0, 0))
assert state() == start, "the lay undone bit for bit"
levels = close.packet_levels(node, where, 1, None)
conj = close.packet_levels(node, where, -1, None)
w_sum = sum(rn * ib - rb * inow for _n, (rn, rb, inow, ib) in levels) + sum(rn * ib - rb * inow for _n, (rn, rb, inow, ib) in conj)
assert w_sum == 0, ("the conjugate pair's charge sums to 0 at the wave 0", w_sum)
centre = dict((n, lv) for n, lv in levels)[where]
assert centre == (node.A, 0, 0, node.B), ("MS-S1 at the centre", centre)
rest = close.packet_momentum(node, s, where, 1, None)
assert rest == [0, 0, 0], ("a packet at the wave 0 onto nothing carries none", rest)
moving = close.packet_levels(node, where, 1, (top, 0, 0))
w_moving = sum(rn * ib - rb * inow for _n, (rn, rb, inow, ib) in moving)
w_rest = sum(rn * ib - rb * inow for _n, (rn, rb, inow, ib) in levels)
print({"dp_x_at_top": dp[0], "ceiling": ceiling, "permille_of_ceiling": abs(dp[0]) * 1000 // ceiling, "W_rest": w_rest, "W_moving": w_moving, "acts": len(acts), "seconds": int(time.time() - t0)})
print("ok")

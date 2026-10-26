"""vf12: the merger board's births with their W_children (the charge at every birth), under a given src. Usage: python merger_charge.py <worktree-for-tests> (PYTHONPATH names the src)"""
import sys
sys.set_int_max_str_digits(0)
sys.path.insert(0, sys.argv[1])
from event_universe.rows import PLANE
from tests.laws import node_of
node = node_of("world_node.json", shape=[5, 5, 5], seed=[])
a, b, k = node.A, node.B, 3
heavy = max(range(len(node.records())), key=lambda r: node.records()[r].gap or 0)
for at, levels in (((1, 1, 1), (k * a, 0, 0, k * b)), ((2, 1, 1), (k * a, b, 0, -k * b)), ((1, 2, 1), (a, b, 0, 0)), ((2, 1, 2), (b, a, 0, 0))):
    node.lay(heavy, at, levels)
for _ in range(20):
    node.step()
births = [e for e in node.log if e["event"] == "birth"]
print("births", len(births), "T", node.T)
for e in births:
    print("  i", e["i"], "node", e["node"], "taken_row", e["taken_row"], "line_pair", e.get("line_pair"), "W_children", e["W_children"], "sum", sum(int(x) for x in e["W_children"]), "taken_line", e.get("taken_line"), "taken", e["taken"], "booked", e["booked"])

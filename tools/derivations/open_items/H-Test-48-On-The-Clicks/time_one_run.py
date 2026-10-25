"""t48: the time of one run of the chiral 3-cube at N intervals on the engine in PYTHONPATH, and the births by interval."""
import sys, time
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world
from event_universe.node import Node
universe, world = load_world(sys.argv[1])
n = int(sys.argv[2])
t0 = time.perf_counter()
node = Node(universe, world)
for _ in range(n):
    node.step()
t1 = time.perf_counter()
print("intervals", n, "ms", int((t1 - t0) * 1000), "counts", node.counts)
births = [(e["i"], e["node"], e["line_pair"], e["minus"], e["plus"], e["W_children"]) for e in node.log if e["event"] == "birth"]
print("births", births)
print("log keys", sorted(set(k for e in node.log for k in e)))
print("events", sorted(set(e["event"] for e in node.log)))

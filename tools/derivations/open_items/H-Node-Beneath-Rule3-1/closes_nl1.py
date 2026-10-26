"""A bug check (H-Node-Beneath-Rule3-1): node.closes under the run back, forward n and back n on a world; the sum of |closes| and of closes over the board after the run back, 0 expected for a bijection, and the per-birth forward net at the emitter's take."""

import sys
from pathlib import Path

from event_universe.loader.world import load_world
from event_universe.node import Node

universe, world = load_world(Path(sys.argv[1]))
n = int(sys.argv[2])
node = Node(universe, world)
for _ in range(n):
    node.step()
births = node.counts["births"]
credits = sum(1 for e in node.log if e["event"] == "credit")
forward = [int(sum(abs(int(x)) for x in node.closes.reshape(-1))), int(sum(int(x) for x in node.closes.reshape(-1)))]
for _ in range(n):
    node.step_back()
back = [int(sum(abs(int(x)) for x in node.closes.reshape(-1))), int(sum(int(x) for x in node.closes.reshape(-1)))]
print({"births": births, "credits": credits, "closes_after_forward [abs sum, sum]": forward, "closes_after_back [abs sum, sum]": back})

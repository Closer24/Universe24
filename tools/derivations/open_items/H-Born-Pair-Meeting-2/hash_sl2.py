"""sl2: the state hash of a world run N intervals under whichever event_universe is on PYTHONPATH (David's src or the copy), with the counts; the control (a): the copy with the flag absent against David's bit for bit.
Usage: PYTHONPATH=<src> python hash_sl2.py <world.json> <intervals>"""
import json
import sys

from event_universe.loader.world import load_world
from event_universe.node import Node

sys.set_int_max_str_digits(0)
universe, world = load_world(sys.argv[1])
node = Node(universe, world)
for _ in range(int(sys.argv[2])):
    node.step()
print(json.dumps({"world": sys.argv[1], "intervals": node.interval, "hash": node.state_hash(), "counts": node.counts, "log_lines": len(node.log)}))

"""Every world laid through the loader and the Node, its state hash at the lay. Usage: lay_hash.py <src> <world.json>..."""
import sys, json
sys.path.insert(0, sys.argv[1]); sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world
from event_universe.node import Node
for p in sys.argv[2:]:
    try:
        u, w = load_world(p)
        n = Node(u, w)
        print(p.split("/")[-1], n.state_hash(), "records", len(n.records()), "units", n.units)
    except Exception as e:
        print(p.split("/")[-1], "REFUSED", type(e).__name__, str(e)[:120])

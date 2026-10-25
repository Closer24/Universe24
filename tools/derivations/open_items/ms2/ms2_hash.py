"""ms2: the state hash at every interval of a world under whichever event_universe PYTHONPATH names (the flag-off control):
python ms2_hash.py <world.json> <out.txt>; two runs (src, src_ms2) diffed show the copy bit for bit the engine with the key absent."""
import sys
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world
from event_universe.node import Node
universe, world = load_world(sys.argv[1])
node = Node(universe, world)
with open(sys.argv[2], "w") as out:
    out.write(node.state_hash() + "\n")
    for _ in range(int(world["intervals"])):
        node.step()
        out.write(node.state_hash() + "\n")
    n, bits = node.census()
    out.write(f"integers {n} bits {bits} transient {node.max_transient} counts {node.counts}\n")

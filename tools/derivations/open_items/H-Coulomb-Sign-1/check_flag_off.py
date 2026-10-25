"""Control (a): the flag off is the engine's path bit for bit. The kit's world_bodies_120 (7-cube, two neutral bodies, no field) run twice in one
process: the engine's Node with seed.lay_world, then run_cl1's Node with lay_cl1.lay_world bound; the last `back` states' hashes compared.
Prediction: 10 of 10 equal. Usage: python check_flag_off.py <world.json> [back N]"""
import sys
sys.set_int_max_str_digits(0)
from event_universe import run, seed
from event_universe.loader.world import load_world
from event_universe.node import Node
import run_cl1, lay_cl1

universe, world = load_world(sys.argv[1])
back = int(sys.argv[sys.argv.index("back") + 1]) if "back" in sys.argv else 10
engine = Node(universe, world)
_r, _n, h_engine = run.forward(engine, int(world["intervals"]), back, lambda s: None)
seed.lay_world = lay_cl1.lay_world
flagged = run_cl1.Cl1Node(universe, world)
_r, _n, h_flag = run.forward(flagged, int(world["intervals"]), back, lambda s: None)
equal = sum(a == b for a, b in zip(h_engine, h_flag))
print({"world": sys.argv[1], "intervals": int(world["intervals"]), "hashes compared": len(h_engine), "equal": equal, "last": h_engine[-1][:16], "census": flagged.census()})

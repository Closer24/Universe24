"""hp1: the carrier's rule as the letter builds it (node.rule_of on the shape-10 row) at the horizon's contents and the vacuum's: the six reaches, the own weight, the wall, the mass; the quotients R / w and D / w per million. Usage: carrier_rule.py <src> <world.json>"""
import sys
import numpy as np
sys.path.insert(0, sys.argv[1]); sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import CARRIER
from event_universe import readings
u, w = load_world(sys.argv[2]); node = Node(u, w)
car = node.row(CARRIER)
print("carrier pair", car.pair, "wall(own)", car.wall, "w", node.w, "bits", node.w.bit_length(), "G", node.G)
for c in (0, 919, 2446, 3424, 3707, 3792, 3793, 3837, 3885):
    cc = np.full(node.shape, c, dtype=object)
    r = node.rule_of(car, cc, node.link_factors(None, None))
    p0, pi = readings.paces_of(node, cc)
    R = int(r.reaches[0].reshape(-1)[0]) if np.ndim(r.reaches[0]) else int(r.reaches[0])
    print("content", c, "p0", int(np.asarray(p0).reshape(-1)[0]), "pi", int(np.asarray(pi).reshape(-1)[0]), "R", R, "6R/w per million", 6 * R * 1000000 // int(r.wall), "D", int(np.asarray(r.mass).reshape(-1)[0]), "D/w per million", int(np.asarray(r.mass).reshape(-1)[0]) * 1000000 // int(r.wall), "S", int(np.asarray(r.self_coefficient).reshape(-1)[0]))

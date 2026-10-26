import sys, itertools
sys.set_int_max_str_digits(0)
import numpy as np
from event_universe.node import Node
from event_universe.rows import CARRIER
from tests.laws import world_of
m = np.array([[-1,0,0],[0,-1,0],[0,0,1]])  # the rotation by a half turn about z: x -> -x, y -> -y
def image(m, node, cube): return tuple(int(x) % cube for x in m @ np.array(node, dtype=int))
universe, world = world_of("world_hole.json")
def world_image(world, m, cube):
    found = dict(world, shape=[cube] * 3, seed=[dict(lay) for lay in world["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay: lay[key] = list(image(m, tuple(lay[key]), cube))
    return found
base, other = Node(universe, world), Node(universe, world_image(world, m, 5))
signs = [1, 1, 1, 1, -1, -1, 1, 1, -1, -1]  # g_00, g_aa, g_0x, g_0y, g_0z, g_xy (+), g_yz (-), g_zx (-)
for i in range(1, 21):
    base.step(); other.step()
    lb, lo = base.row(CARRIER).lines, other.row(CARRIER).lines
    for k in range(10):
        bad = [at for at in np.ndindex(5,5,5) if int(lo[k].now[image(m, at, 5)]) != signs[k] * int(lb[k].now[at])]
        badr = [at for at in np.ndindex(5,5,5) if int(lo[k].rem[image(m, at, 5)]) != (int(lb[k].rem[at]) if signs[k] == 1 else base.w - int(lb[k].rem[at]))]
        badw = [at for at in np.ndindex(5,5,5) if int(lo[k].wr[image(m, at, 5)]) != (int(lb[k].wr[at]) if signs[k] == 1 else lb[k].wwall - int(lb[k].wr[at]))]
        if bad or badr or badw:
            print("interval", i, "line", k, "levels apart", len(bad), "rem apart", len(badr), "wr apart", len(badw), bad[:3], badr[:3])
    if any(int(lo[0].now[image(m, at, 5)]) != int(lb[0].now[at]) for at in np.ndindex(5,5,5)):
        print("X parted at", i); break
print("births", base.counts["births"], other.counts["births"])

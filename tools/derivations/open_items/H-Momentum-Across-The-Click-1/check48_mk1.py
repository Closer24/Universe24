"""mk1: the kick under one rotation negating two axes (diag(1, -1, -1)) on the hole seed of the 5-cube: the base and the image run interval by interval under the flag; the first interval where the booked kicks differ through the image is named with its lines."""
import json, sys
import numpy as np
from event_universe.node import Node
from event_universe.loader.world import load_world
sys.set_int_max_str_digits(0)
universe, world = load_world(sys.argv[1])
cube = 5
m = np.diag([1, -1, -1])
def image(at): return tuple(int(x) % cube for x in m @ np.array(at, dtype=int))
w2 = dict(world, seed=[dict(lay) for lay in world["seed"]])
for lay in w2["seed"]:
    for key in ("at", "centre"):
        if key in lay: lay[key] = list(image(tuple(lay[key])))
a, b = Node(universe, world), Node(universe, w2)
for t in range(1, 21):
    a.step(); b.step()
    ka = sorted((image(tuple(e["node"])), e["event"], e.get("line", e.get("line_pair")), e["kick"], tuple(e["dP_take"]), tuple(e["dP_recoil"])) for e in a.log if e["i"] == t and "kick" in e)
    kb = sorted((tuple(e["node"]), e["event"], e.get("line", e.get("line_pair")), e["kick"], tuple(e["dP_take"]), tuple(e["dP_recoil"])) for e in b.log if e["i"] == t and "kick" in e)
    # the image's momenta: y and z negated
    ka = [(n, ev, l, q, (d[0], -d[1], -d[2]), (r[0], -r[1], -r[2])) for n, ev, l, q, d, r in ka]
    same_rows = all(int(a.row(2, gap=0).lines[0].now[at]) == int(b.row(2, gap=0).lines[0].now[image(at)]) for at in np.ndindex(cube, cube, cube))
    if ka != kb or not same_rows:
        print("interval", t, "rows alike through the image:", same_rows, "kicks alike:", ka == kb)
        for x, y in zip(ka, kb):
            if x != y: print("  base->image", x); print("  image     ", y)
        if len(ka) != len(kb): print("  counts", len(ka), len(kb))
        break
else:
    print("20 of 20 intervals alike through the image, kicks alike")

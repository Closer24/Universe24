import sys, itertools, json
sys.set_int_max_str_digits(0)
import numpy as np
from event_universe.node import Node
from event_universe.rows import CARRIER, PLANE
from tests.laws import world_of
n = int(sys.argv[1])
IMAGES = [np.array([[s[a] if pi[a] == b else 0 for a in range(3)] for b in range(3)]) for pi in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]
def image(m, node, cube): return tuple(int(x) % cube for x in m @ np.array(node, dtype=int))
def world_image(world, m, cube):
    found = dict(world, shape=[cube] * 3, seed=[dict(lay) for lay in world["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay: lay[key] = list(image(m, tuple(lay[key]), cube))
    return found
universe, world = world_of("world_hole.json")
def run(w):
    node = Node(universe, w)
    for _ in range(n): node.step()
    return node
base = run(world_image(world, np.eye(3, dtype=int), 5))
alike = []
for k, m in enumerate(IMAGES):
    other = run(world_image(world, m, 5))
    same = all(int(base.row(CARRIER).lines[0].now[at]) == int(other.row(CARRIER).lines[0].now[image(m, at, 5)]) for at in np.ndindex(5, 5, 5))
    det = int(round(np.linalg.det(m)))
    alike.append((k, det, same, other.counts["births"]))
print(n, "X alike:", sum(1 for a in alike if a[2]), "rotations alike", sum(1 for a in alike if a[2] and a[1] == 1), "reflections alike", sum(1 for a in alike if a[2] and a[1] == -1), "births", sorted({a[3] for a in alike}), "base births", base.counts["births"])

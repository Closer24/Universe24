"""The candidate world files on the 4-cube (and one on the 8-cube): ga2's cycle lay with the hole laid as a digit of the pattern. Every hole is {"lay": "hole", "at": [x, y, z]}; the class of a Node is p = (p1[4 (x mod 4) + (y mod 4)] + cz z) mod 4."""
import json
import os

P1 = [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2]
WAVE = {"lay": "wave", "row": 0, "quanta": 5, "p1": P1, "cz": 1, "mirror": 0}
U = "universe_ga2.json"


def cls(x, y, z):
    return (P1[4 * (x % 4) + (y % 4)] + z) % 4


def nodes(cube):
    return [(x, y, z) for x in range(cube) for y in range(cube) for z in range(cube)]


def holes(where):
    return [{"lay": "hole", "at": list(at)} for at in where]


def world(name, cube, seed, intervals=450):
    with open(os.path.join(os.path.dirname(__file__), "worlds", name), "w") as f:
        json.dump({"universe": U, "shape": [cube, cube, cube], "intervals": intervals, "seed": seed}, f)


c0 = [at for at in nodes(4) if cls(*at) == 0]
even = [at for at in nodes(4) if all(v % 2 == 0 for v in at)]
assert len(c0) == 16 and len(even) == 8
world("n0_ga2.json", 4, [WAVE])
world("n1_hole_origin.json", 4, [WAVE] + holes([(0, 0, 0)]))
world("n2_hole_class0.json", 4, [WAVE] + holes(c0))
world("n3_hole_every_node.json", 4, [WAVE] + holes(nodes(4)))
world("n4_sea_hole_class0.json", 4, [WAVE, {"lay": "sea", "row": 0}] + holes(c0))
world("n5_mirror1.json", 4, [dict(WAVE, mirror=1)])
world("n6_hole_period2.json", 4, [WAVE] + holes(even))
world("n7_sea_hole_every_node.json", 4, [WAVE, {"lay": "sea", "row": 0}] + holes(nodes(4)))
c0_8 = [at for at in nodes(8) if cls(*at) == 0]
assert len(c0_8) == 128
world("n2_hole_class0_8cube.json", 8, [WAVE] + holes(c0_8), 230)
print("classes on the 4-cube:", {k: sum(1 for at in nodes(4) if cls(*at) == k) for k in range(4)})
print("class 0 Nodes:", c0)
print("even-lattice classes:", [cls(*at) for at in even])

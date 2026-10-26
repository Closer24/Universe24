"""The candidate world files: ga2's cycle lay (CS5-S2's wave form) with holes laid inside the pattern's classes. Usage: make_worlds.py <worlds dir>. Integers only."""
import json
import sys

P1 = [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2]
WAVE = {"lay": "wave", "row": 0, "quanta": 5, "p1": P1, "cz": 1, "mirror": 0}


def phase(x, y, z):
    return (P1[4 * (x % 4) + (y % 4)] + z) % 4


def nodes(n):
    return [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]


def holes(at):
    return [{"lay": "hole", "at": list(a)} for a in at]


def world(n, lays, intervals=450):
    return {"universe": "universe_ga2.json", "shape": [n, n, n], "intervals": intervals, "seed": lays}


out = sys.argv[1]
for n in (4, 8):
    all_nodes = nodes(n)
    cands = {
        "c0_ga2": [WAVE],
        "c1_class0": [WAVE] + holes([a for a in all_nodes if phase(*a) == 0]),
        "c1b_class2": [WAVE] + holes([a for a in all_nodes if phase(*a) == 2]),
        "c2_every": [WAVE] + holes(all_nodes),
        "c3_fixed_column": [WAVE] + holes([a for a in all_nodes if (a[0] % 4, a[1] % 4) in ((0, 0), (2, 2))]),
        "c4_one_hole": [WAVE] + holes([(0, 0, 0)]),
        "c5_hole_first_class0": holes([a for a in all_nodes if phase(*a) == 0]) + [WAVE],
        "c6_period4_lattice": [WAVE] + holes([a for a in all_nodes if a[0] % 4 == 0 and a[1] % 4 == 0 and a[2] % 4 == 0]),
        "c7_classes02": [WAVE] + holes([a for a in all_nodes if phase(*a) in (0, 2)]),
    }
    for name, lays in cands.items():
        with open(f"{out}/{name}_{n}.json", "w") as f:
            json.dump(world(n, lays), f)
        print(name, n, "holes", sum(1 for l in lays if l["lay"] == "hole"))

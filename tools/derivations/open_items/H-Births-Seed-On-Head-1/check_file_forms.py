"""rg1: what the world file can lay on this head, by the loader's own answer: (a) cs3's `wave` cycle form {"lay": "wave", "row": 0, "quanta": 5, "p1": [...], "cz": 1, "mirror": 0}; (b) the fourth form `sea` on the gap-0 plane at a count; (c) the `at` lay of the gap-0 plane at a wave number (the one moving lay the file has for the light), read for its uniformity: the light's share per Node (min, max, distinct values), the phase pattern it lays against the cycle pattern's p1. Integers only. Usage: PYTHONPATH=<src> python check_file_forms.py <worlds dir>"""
import json
import os
import sys

sys.set_int_max_str_digits(0)
import numpy as np

from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.rows import PLANE

here = sys.argv[1]
base = json.load(open(os.path.join(here, "empty4_ga2_450.json")))
P1 = [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2]


def attempt(name, seed):
    path = os.path.join("/dev/shm/tmp", f"rg1_{name}.json")
    json.dump(dict(base, seed=seed, intervals=2), open(path, "w"))
    os.system(f"cp {os.path.join(here, 'universe_ga2.json')} /dev/shm/tmp/")
    try:
        universe, world = load_world(path)
        node = Node(universe, world)
    except Exception as e:  # noqa: BLE001
        print(name, "REFUSED by the loader:", type(e).__name__, str(e)[:160])
        return None
    print(name, "LAID")
    return node


def light_census(node):
    gap0 = node.row(PLANE, gap=0)
    rec = node.records().index(gap0)
    c = node.content()
    rule = node.rule_of(gap0, c, node.link_factors())
    sh = [int(v) for v in node.share(gap0.lines, rule).reshape(-1)]
    re, im = gap0.lines
    quads = []
    for at in np.ndindex(*node.shape):
        a, b = int(re.now[at]), int(im.now[at])
        quads.append((1 if a > 0 else -1 if a < 0 else 0, 1 if b > 0 else -1 if b < 0 else 0))
    print("   light share per Node: min", min(sh), "max", max(sh), "distinct", len(set(sh)), "unit", node.unit_gap0, "| Nodes at or above 5 units:", sum(1 for v in sh if v >= 5 * node.unit_gap0), "of", len(sh), "| sign quadrants (re, im) distinct:", sorted(set(quads)), "| levels at the origin:", [int(l.now[0, 0, 0]) for l in gap0.lines], [int(l.before[0, 0, 0]) for l in gap0.lines])


attempt("wave_cycle", [{"lay": "wave", "row": 0, "quanta": 5, "p1": P1, "cz": 1, "mirror": 0}])
attempt("sea_gap0_quanta", [{"lay": "sea", "row": 0, "quanta": 5}])
attempt("at_cycle_keys", [{"lay": "at", "row": 0, "centre": [0, 0, 0], "quanta": 5, "p1": P1, "cz": 1}])
n = attempt("sea_gap0_drift", [{"lay": "sea", "row": 0}])
if n:
    light_census(n)
for h in (0, 10722142120563800, 15162856759112389):
    n = attempt(f"at_gap0_wave_h{h}_w2", [{"lay": "at", "row": 0, "centre": [1, 1, 1], "quanta": 5, "width": 2, "wave": [h, 0, 0]}])
    if n:
        light_census(n)
n = attempt("at_gap0_wave_top3", [{"lay": "at", "row": 0, "centre": [1, 1, 1], "quanta": 5, "width": 2, "wave": [15162856759112389, 0, 0], "top": 3}])
if n:
    light_census(n)

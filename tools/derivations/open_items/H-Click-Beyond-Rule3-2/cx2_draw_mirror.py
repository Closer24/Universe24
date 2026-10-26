"""H-Click-Beyond-Rule3-2: the draw's number read at a Node and at its mirror under z -> -z on a state symmetric under it (the hole seed): close.meet wrapped at one interval, read_number called at every standing Node and at its mirror with the same rules, the numbers compared; the digits listed where they differ. Usage: python cx2_draw_mirror.py world.json interval"""
import json
import sys

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe import close, run
from event_universe.draw import read_number
from event_universe.loader.world import load_world

universe, world = load_world(sys.argv[1])
target = int(sys.argv[2])
node = run.Node(universe, world)
OUT = {}
original = close.meet


def probe(node, rec, start, sh, rules, frozen):
    if node.interval == target and rec == node.records().index(node.emitter()):
        unit = node.units[rec]
        cube = node.cube
        same = diff = 0
        examples = []
        for at in [(x, y, z) for x in range(cube) for y in range(cube) for z in range(cube)]:
            mirror = (at[0], at[1], (-at[2]) % cube)
            a, b = read_number(node, at, rules, unit), read_number(node, mirror, rules, unit)
            node.drawn.pop((at, rec), None)
            if a == b:
                same += 1
            else:
                diff += 1
                if len(examples) < 3:
                    examples.append([list(at), str(a), str(b)])
        OUT.update({"interval": target, "same": same, "diff": diff, "examples": examples})
    return original(node, rec, start, sh, rules, frozen)


close.meet = probe
for _ in range(target):
    node.step()
print(json.dumps(OUT))

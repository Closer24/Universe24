"""H-Click-Beyond-Rule3-2: are the remainders of the seed's lines covariant under a reflection that keeps the seed (the hole seed under z -> -z)? The Node built through run.py's Node, stepped N intervals, every row's lines' now, before and rem compared with their image under the reflection. Usage: python cx2_rem_symmetry.py world.json N"""
import json
import sys

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe import run
from event_universe.loader.world import load_world

universe, world = load_world(sys.argv[1])
node = run.Node(universe, world)
for _ in range(int(sys.argv[2])):
    node.step()


def mirror(a):
    return np.roll(a[:, :, ::-1], 1, axis=2)


found = {}
for rec, row in enumerate(node.rows()):
    for k, line in enumerate(row):
        for name, a in (("now", line.now), ("before", line.before), ("rem", line.rem)):
            arr = np.asarray(a)
            off = int(np.sum(arr != mirror(arr)))
            found[f"row{rec}_line{k}_{name}_off"] = off
found["interval"] = node.interval
found["rem_values_rec0_line0"] = sorted(set(int(x) for x in np.asarray(node.records()[0].lines[0].rem).reshape(-1)))[:6]
print(json.dumps(found))

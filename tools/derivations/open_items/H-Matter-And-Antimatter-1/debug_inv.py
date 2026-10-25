"""Which arrays break the checker's group at the seed and at the first intervals (ma1's debug reading; integers only)."""
import json, sys
import numpy as np
from pathlib import Path
from event_universe.loader.world import read_world
from event_universe.node import Node
import ma_run

sys.set_int_max_str_digits(0)
where = Path(sys.argv[1])
world = json.loads(where.read_text())
universe = json.loads(where.parent.joinpath(world["universe"]).read_text())
plasma = [l for l in world["seed"] if l.get("lay") == "plasma"]
stripped = dict(world, seed=[l for l in world["seed"] if l.get("lay") != "plasma"])
universe, stripped = read_world(stripped, universe)
node = Node(universe, stripped)
for lay in plasma:
    ma_run.lay_plasma(node, lay)
names = []
for k, r in enumerate(node.rows_):
    for j, line in enumerate(r.lines):
        for nm in ("now", "before", "rem", "wr"):
            if getattr(line, nm) is not None:
                names.append((f"row shape {r.shape} gap {r.gap} line {j} {nm}", getattr(line, nm), j == 1 and r.shape == 2))

def report(tag):
    bad = []
    for name, a, is_im in names:
        s = -1 if is_im else 1
        ok = all(bool(np.all(np.roll(a, 1, axis=ax) == s * a)) for ax in range(3))
        if not ok:
            vals = sorted(set(int(v) for v in a.reshape(-1)))
            bad.append((name, vals[:6], len(vals)))
    print(tag, "broken:", len(bad))
    for b in bad:
        print("   ", b)

report("seed")
for i in range(int(sys.argv[2])):
    node.step()
    names = []
    for k, r in enumerate(node.rows_):
        for j, line in enumerate(r.lines):
            for nm in ("now", "before", "rem", "wr"):
                if getattr(line, nm) is not None:
                    names.append((f"row shape {r.shape} gap {r.gap} line {j} {nm}", getattr(line, nm), j == 1 and r.shape == 2))
    report(f"i={node.interval}")

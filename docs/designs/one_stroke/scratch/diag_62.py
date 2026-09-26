"""Commit 3's diagnosis: on the moving long Lorentz clock, is the anisotropic path taken
(the matter record reads the well's xx part at the moving body), and does the difference to
the old engine vanish when the tensor read is silenced?"""

import json
import sys
from pathlib import Path

import numpy as np

S = Path("/tmp/claude-0/-home-user-Universe24/514152eb-97ce-5ae9-a1a5-7760c4b5aaef/scratchpad")
rel = "toward_nature/lorentz_moving_long.json"


def engine(root):
    sys.path.insert(0, str(root / "src"))
    for name in list(sys.modules):
        if name.startswith("event_universe"):
            del sys.modules[name]
    from event_universe.events.detector_law import DetectorLawSimulation
    from event_universe.events.world import parse_nature_beam_world

    sys.path.pop(0)
    return DetectorLawSimulation, parse_nature_beam_world


def run(root, ticks, silence=False):
    Sim, parse = engine(root)
    lines = []
    sim = Sim(parse(json.loads((root / "examples/events" / rel).read_text())), observer=lines.append)
    if silence:
        sim._axis_contents = lambda family, inverse=False: None
    snaps = []
    for _ in range(ticks):
        sim.step()
        snaps.append({int(k): (v.now.copy(), v.remainder.copy()) for k, v in sim.records.items()})
    return sim, snaps, lines


ticks = 60
sim_new, new, new_lines = run(S / "wt_ec", ticks)
matter = [f.name for f in sim_new.families].index("matter")
gravity = [f.name for f in sim_new.families].index("gravity")
contents = sim_new._axis_contents(matter)
print(
    "GAMEBOARD axis contents for matter:", None if contents is None else [int(c.max()) for c in contents]
)
parts = sim_new.held_parts[gravity]
print("GAMEBOARD gravity parts max:", [int(p.now.max()) for p in parts])
sim_sil, sil, sil_lines = run(S / "wt_ec", ticks, silence=True)
sim_old, old, old_lines = run(S / "wt_old", ticks)


def same(a, b):
    return all(
        sorted(x) == sorted(y)
        and all(np.array_equal(x[k][0], y[k][0]) and np.array_equal(x[k][1], y[k][1]) for k in x)
        for x, y in zip(a, b, strict=True)
    )


print("COMPUTATION new vs old rows:", "same" if same(new, old) else "differ")
print("COMPUTATION silenced vs old rows:", "same" if same(sil, old) else "differ")


def strip(line):
    return {k: v for k, v in line.items() if k != "input"}


print(
    "COMPUTATION silenced vs old lines:",
    "same" if [strip(line) for line in sil_lines] == [strip(line) for line in old_lines] else "differ",
)
print(
    "COMPUTATION new vs old lines:",
    "same" if [strip(line) for line in new_lines] == [strip(line) for line in old_lines] else "differ",
)

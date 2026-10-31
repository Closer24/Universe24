"""The THIRD physicist's probe for VARY4 2.5: node-all's act on a world's three files (VARY3's world_nohold, read only),
R rounds; every 25 rounds each train's largest |count| over its rows and sites (the now slot), and the bits of the
largest; whole numbers only, no division; the prober's loops and comparisons are the probe's.
Args: <node-all src> <world dir> <setting file name> <rounds> <out.json>
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
from tensor24 import main as t24  # noqa: E402
from tensor24.engine import state as state_mod  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402
from tensor24.runner.files import sites_of  # noqa: E402

world, name, rounds, out = Path(sys.argv[2]), sys.argv[3], int(sys.argv[4]), Path(sys.argv[5])
universe = json.loads(world.joinpath("universe.json").read_text(encoding="utf-8"))
shape = json.loads(world.joinpath("piece.json").read_text(encoding="utf-8"))["shape"]
setting = json.loads(world.joinpath(name).read_text(encoding="utf-8"))
held, laid = loading.load(universe, setting, sites_of(shape), *t24.made(loading.star(len(shape))))
lay = t24.layout(universe, shape, held)
s = state_mod.State(*held.state)
first = [int(x) for x in held.trains.first]
size = [int(x) for x in held.trains.size]
rows = {t: list(range(first[t], first[t] + size[t])) for t in range(len(first))}


def largest(a):
    return {t: max(abs(int(v)) for r in rows[t] for v in a[r]) for t in rows}


trace = {"0": largest(s.a)}
lines = 0
for at in range(1, rounds + 1):
    s, clicks = step.act(lay, s)
    lines += int(np.sum(np.asarray(clicks != 0, dtype=bool)))
    if at % 25 == 0:
        trace[str(at)] = largest(s.a)
out.write_text(json.dumps({"world": world.name, "setting": name, "rounds": rounds, "loader departures": laid,
                           "trains": [t["name"] for t in universe["trains"]], "side lines": lines,
                           "largest |count| by train, every 25 rounds": trace,
                           "bits of the largest at the end": {t: v.bit_length() for t, v in trace[str(rounds)].items()}},
                          indent=1), encoding="utf-8")

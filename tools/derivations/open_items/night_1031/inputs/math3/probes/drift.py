"""MATH3's drift probe: one aperiodic lawful orbit, so <T, M> has infinite order (the mathematician's m1).

Usage: python -I drift.py <tree> <bang world dir> <rounds>

A test's lay, named so (never a shipped world): the bang world's layout with its wave row laid as a uniform drift at
every site, a = c + 1, b = c, r = 0 (c the row's lay count at site 0), every other count, tooth and fine tooth as the
lay has them. A uniform row feels no pull (every stretch 0), so the act should carry it to a = c + n + 1 after n rounds,
each round lawful (both slots' teeth at least 1, every tooth within its dial): an orbit that is not periodic.
"""

import json
import sys
from pathlib import Path

TREE, WORLD, N = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
sys.path.insert(0, str(TREE.joinpath("src")))
sys.set_int_max_str_digits(0)

import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import run as trun  # noqa: E402

paths = [WORLD.joinpath(n + ".json") for n in ("universe", "piece", "setting")]
universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
engine = tmain.ENGINE
kinds, tables, square, lifted = engine.made(trun.star(len(piece["shape"])))
loaded, found = trun.load(universe, setting, trun.sites_of(piece["shape"]), kinds, tables, square, lifted)
assert not found, found
layout = engine.layout(universe, piece["shape"], loaded)
s0 = engine.state(*loaded.state)
a = np.array(s0.a, dtype=object)
b = np.array(s0.b, dtype=object)
r = np.array(s0.r, dtype=object)
row = 0
c = int(a[row, 0])
a[row, :] = c + 1
b[row, :] = c
r[row, :] = 0
s = engine.state(a, b, r, s0.rd, s0.k)
ok, lawful = 0, 0
for n in range(1, N + 1):
    found = trun.promised(engine, layout, s, universe["integers"]["width"])
    lawful += int(not found)
    s = step.tick(layout, s)
    ok += int(all(int(v) == c + n + 1 for v in np.asarray(s.a)[row]))
print(f"world {WORLD.name} (a test's lay: row {row} a uniform drift from c = {c}); rounds {N}")
print(f"D1 the row at c + n + 1 at every site after round n: {ok} of {N}; the promise met before every round: {lawful} of {N}")
print(f"D1 the row's count after the last round: {sorted(set(int(v) for v in np.asarray(s.a)[row]))}")

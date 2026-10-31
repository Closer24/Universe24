"""MIRACLE_A, Theorem A's degree-1 case: a row whose forces are the Mesh pull alone keeps its total momentum over the
sites. The engine's own act, unpatched, on a world's files. The written momentum of the edge (b, a) is
M = senses (W(a) + W(b)) (a - b) + s, the tooth read on the dial it was written on (the edge's own). Per round, per
row: the sum of M over the sites, against the lay's. Also read: whether the row's counts move. Usage:
python -I momentum.py <universe> <piece> <setting> [rounds=N]"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import qrat  # noqa: E402,F401  (puts the tree on the path)

import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import load as loadmod  # noqa: E402
from tensor24.runner.files import sites_of, star  # noqa: E402

opts = dict(x.split("=") for x in sys.argv[4:] if "=" in x)
universe, piece, setting = (json.loads(Path(p).read_text(encoding="utf-8")) for p in sys.argv[1:4])
shape = piece["shape"]
kinds, c, square = tmain.made(star(len(shape)))
loaded, found = loadmod.load(universe, setting, sites_of(shape), kinds, c, square)
assert found == [], found
layout = tmain.layout(universe, shape, loaded)
senses = step.halves(layout)
print("strengths:", {k: v for k, v in universe["chosen"].items() if k != "key"}, "; key", universe["chosen"]["key"])


def total(s):
    wa, wb = step.dials(layout, s)
    m = senses * (wa + wb) * (s.a - s.b) + s.r
    return [int(x) for x in m.sum(axis=1)]


s = State(*loaded.state)
t0 = total(s)
rows = len(t0)
moved = [False] * rows
kept = [True] * rows
first_off = [None] * rows
ticks = int(opts.get("rounds", 200))
for at in range(1, ticks + 1):
    before = s.a.copy()
    s = step.tick(layout, s)
    tt = total(s)
    for r in range(rows):
        moved[r] = moved[r] or not np.array_equal(s.a[r], before[r])
        if tt[r] != t0[r] and kept[r]:
            kept[r], first_off[r] = False, at
for r in range(rows):
    print(f"row {r}: counts moved {moved[r]}; total momentum over the {s.a.shape[1]} sites at the lay {t0[r]}, "
          f"kept exactly in every round of {ticks}: {kept[r]}" + ("" if kept[r] else f" (first off at round {first_off[r]})"))
print(f"rows that moved and kept their total momentum: {sum(1 for r in range(rows) if moved[r] and kept[r])} of "
      f"{sum(1 for r in range(rows) if moved[r])} moving rows")

"""SPLIT1's probe of the split take's parts from the structure: on a shipped world (argv: its folder), loaded by node-live's
own loader (runner.load.load, main.made, files.departures), every monomial of the value legs' potential, the one plan the
whole click's passing reads (step.passing), mapped to the trains its legs lie in; an edge is a pair of distinct trains
that one monomial joins, the owner's pair of clocks; per train, the edges it ends: a train on two edges or more at a
place is a split take's giver or taker there. Nothing is typed: the trains, rows, legs and factors are the loader's.
Whole numbers only; no division but Rule3's carry; paths by joinpath."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("nl", "src")))
import numpy as np  # noqa: E402
from tensor24 import main  # noqa: E402
from tensor24.runner import files as F  # noqa: E402
from tensor24.runner import load as L  # noqa: E402

folder = HERE.joinpath("worlds", sys.argv[1])
paths = [folder.joinpath(n) for n in ("universe.json", "piece.json", "setting.json")]
found = F.departures(*paths)
if found:
    raise SystemExit("departures: " + "; ".join(found))
universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
shape = piece["shape"]
kinds_, tables, square = main.made(F.star(len(shape)))
loaded, found = L.load(universe, setting, F.sites_of(shape), kinds_, tables, square)
if found:
    raise SystemExit("load departures: " + "; ".join(found))
tr = loaded.trains
names = [t["name"] for t in universe["trains"]]
rows = int(tr.size.sum())
of_row = np.zeros(rows + 1, dtype=np.intp) - 1  # the unit, the readings' last row, belongs to no train
for t in range(len(tr)):
    of_row[int(tr.first[t]):int(tr.first[t] + tr.size[t])] = t
factor, legs = loaded.potential
legs = np.stack(legs)  # (4, monomials), -1 the unit
print(f"world {sys.argv[1]}: shape {shape}, trains {names}, rows {rows}, monomials {factor.shape[0]}")
edges, own = {}, {}
for m in range(factor.shape[0]):
    f = int(factor[m])
    if f == 0:
        continue
    held = sorted({int(of_row[int(x)]) for x in legs[:, m] if int(x) >= 0})
    if len(held) == 1:
        own[held[0]] = own.get(held[0], 0) + 1
    else:
        key = tuple(held)
        edges[key] = edges.get(key, 0) + 1
for t, c in sorted(own.items()):
    print(f"  own monomials of {names[t]}: {c} (no edge: a monomial within one train passes nothing between clocks)")
for key, c in sorted(edges.items()):
    print(f"  edge {tuple(names[t] for t in key)}: {c} monomials with a factor not 0")
ends = {}
for key in edges:
    for t in key:
        ends[t] = ends.get(t, 0) + 1
for t in range(len(tr)):
    e = ends.get(t, 0)
    word = "a split take's end (two edges or more)" if e >= 2 else ("one edge: whole takes only" if e == 1 else "no edge")
    print(f"  {names[t]}: {e} edges, {word}")
n3 = [key for key in edges if len(key) > 2]
print(f"  monomials joining three trains or more: {len(n3)}")

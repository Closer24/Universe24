"""MATH3's record probe (MATH2's record.py with R4 made an equality and R5 the ledger): what node-all's 1.4 record and
its ledger write, read from them alone.

Usage: python -I record.py <tree> <world dir> <rounds> <out dir>

The world's three files are copied into <out dir> with the setting's ticks set to <rounds> (nothing else changed), the
tree's own runner writes the record there (main.ran), and the record is read back:
 R1 the header's dial and birth, against the layout's edge key and the lay's teeth;
 R2 every listed side [u, q, before, after] at its own Node-clock: x = K q + after - before, against the act's own
    passing at that round, side and site (step.passing), recomputed from the lay;
 R3 every side across a Mesh [u, place, q, before, after]: the same against step.crossing;
 R4 the end line's teeth, own edges and across, against the act's end teeth, entry by entry;
 R5 the ledger beside the record: every Count line's counts against the act's now counts of that train at that site
    and round.
"""

import json
import sys
from pathlib import Path

TREE, WORLD, N, OUT = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), Path(sys.argv[4])
sys.path.insert(0, str(TREE.joinpath("src")))
sys.set_int_max_str_digits(0)

import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.runner import run as trun  # noqa: E402

OUT.mkdir(parents=True, exist_ok=True)
for name in ("universe", "piece", "setting"):
    held = json.loads(WORLD.joinpath(name + ".json").read_text(encoding="utf-8"))
    if name == "setting":
        held["ticks"] = N
    OUT.joinpath(name + ".json").write_text(json.dumps(held), encoding="utf-8")
paths = [OUT.joinpath(n + ".json") for n in ("universe", "piece", "setting")]
record = OUT.joinpath("record.jsonl")
found = tmain.ran(paths, record)
assert not found, found
lines = [json.loads(x) for x in record.read_text(encoding="utf-8").splitlines()]
header, clicks, end = lines[0], [x for x in lines if x.get("kind") == "click"], lines[-1]

universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
shape = piece["shape"]
engine = tmain.ENGINE
kinds, tables, square, lifted = engine.made(trun.star(len(shape)))
loaded, found = trun.load(universe, setting, trun.sites_of(shape), kinds, tables, square, lifted)
assert not found, found
layout = engine.layout(universe, shape, loaded)
s = engine.state(*loaded.state)
click = layout.click
K = int(np.asarray(click.key).reshape(-1)[0])
trains = click.weight.shape[-1]
print("R1 header dial", header.get("dial"), "birth", header.get("birth"), "; layout key", K,
      "; lay teeth", sorted(set(int(v) for v in np.asarray(s.k).reshape(-1)))[:4])

passings = []
for n in range(N):
    t, _ = step.act(layout, s)
    own = step.passing(click, layout.plan, s.b, s.a, t.a)
    far = step.crossing(click, layout.nb, s.b, s.a, t.a)
    passings.append((own, far))
    s = t
ok2 = of2 = ok3 = of3 = 0
for line in clicks:
    own, far = passings[line["round"] - 1]
    site, train = line["site"], line["train"]
    for u, q, before, after in line["sides"]:
        of2 += 1
        ok2 += int(K * q + after - before == int(own[train * trains + u, site]))
    for u, place, q, before, after in line["across"]:
        # the Spoke across which the partner stands: the one whose neighbour is place and whose side carried
        hits = [
            sp for sp in range(layout.nb.shape[0])
            if int(layout.nb[sp, site]) == place
            and K * q + after - before == int(far[(sp * trains + train) * trains + u, site])
        ]
        of3 += 1
        ok3 += int(len(hits) > 0)
print(f"R2 own sides: x = K q + after - before equals the act's passing on {ok2} of {of2} listed sides")
print(f"R3 across sides: equal on {ok3} of {of3}")
print("click lines", len(clicks), "rounds", N)
# R4: the end teeth, entry by entry, against the act's end state s (the state after the last round)
trains_n = trains
own = trains_n * trains_n
inner = np.asarray(s.k)[:own].reshape(trains_n, trains_n, -1)
outer = np.asarray(s.k)[own:].reshape(-1, trains_n, trains_n, np.asarray(s.k).shape[-1])
ok4 = of4 = 0
for t_, u_, row in end.get("teeth", []):
    for site, v in enumerate(row):
        of4 += 1
        ok4 += int(int(inner[t_, u_, site]) == v)
for t_, u_, places, row in end.get("across", []):
    # the across entry carries its Spoke's partner places; find the Spoke whose neighbours they are
    spokes = [sp for sp in range(layout.nb.shape[0]) if [int(x) for x in layout.nb[sp]] == places]
    for site, v in enumerate(row):
        of4 += 1
        ok4 += int(len(spokes) > 0 and int(outer[spokes[0], t_, u_, site]) == v)
print(f"R4 the end line's teeth equal the act's end teeth on {ok4} of {of4} entries (own edges {len(end.get('teeth', []))}, across {len(end.get('across', []))})")
# R5: the ledger
ledger = OUT.joinpath("record.ledger.jsonl")
counts = [json.loads(x) for x in ledger.read_text(encoding="utf-8").splitlines()]
states = []
s2 = engine.state(*loaded.state)
for n in range(N):
    s2, _ = step.act(layout, s2)
    states.append(s2)
ok5 = of5 = 0
for c in counts:
    tr = loaded.trains[c["train"]]
    now = np.asarray(states[c["round"] - 1].a)[tr.first: tr.first + tr.rows(), c["site"]]
    of5 += 1
    ok5 += int([int(v) for v in now] == c["count"])
print(f"R5 the ledger: {len(counts)} Count lines; each equal to the act's now counts of its train, site and round on {ok5} of {of5}")

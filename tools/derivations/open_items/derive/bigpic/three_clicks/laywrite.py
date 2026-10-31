"""The full-picture world's lay written into its own setting.json (VARY1's B1, #2187 6539418183 item 2: the varied lay
lives in the world's files, written by the world's lay, not by the loader or the run): from a base setting, the
giver's first component one count up per the board's first coordinate and the taker, which the base leaves at rest at
0, laid at the bare unit 1 one count up per the second, now and before alike, so every hand starts at rest. The same
lay edgeclick.py's `laid` makes in memory (board_lay), labelled the same: VARY1's stand-in.

Usage: python3 -I laywrite.py <src> <base world dir> <out setting.json>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

base = Path(sys.argv[2])
shape = json.loads((base / "piece.json").read_text())["shape"]
universe = json.loads((base / "universe.json").read_text())
setting = json.loads((base / "setting.json").read_text())
names = [t["name"] for t in universe["trains"]]
giver, taker = names.index("giver"), names.index("taker")
sites = shape[0] * shape[1] * shape[2]
gears = [g for g in setting["gears"] if g[0] != taker]
out = []
for g in gears:
    train, component, site, now, before, tooth = g
    if train == giver and component == 0:
        _, x = carry(site, shape[0], 0)
        now, before = now + x, before + x
    out.append([train, component, site, now, before, tooth])
for n in range(sites):
    rest, _ = carry(n, shape[0], 0)
    _, y = carry(rest, shape[1], 0)
    out.append([taker, 0, n, 1 + y, 1 + y, 0])
text = '{"version": 1, "ticks": ' + str(setting["ticks"]) + ', "gears": [\n' + ",\n".join("  " + json.dumps(g) for g in out) + "\n]}\n"
Path(sys.argv[3]).write_text(text)
print(f"{sys.argv[3]}: {len(out)} gears, the giver one count up per the first coordinate and the taker at 1 up per the second")

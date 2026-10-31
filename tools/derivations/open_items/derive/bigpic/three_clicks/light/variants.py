"""The mesh world's seeds for the light probes (Big Pic, the owner's ask of 07:1x UTC), written from the shipped
examples/tensor24-mesh/setting.json of node-edge 88b4d281c: the plain lay run longer (450 and 560 rounds), the held
hand laid at 2 instead of 1 on Node-clocks 60 to 70 (a patch 40 to 50 Meshes from the wave's bump, 300 rounds), and the
tied train laid at rest at 1, 4, 16, 64, 256 and 500 on the same Node-clocks (120 rounds; 500 at 300). Only the lay
changes; the universe and piece files are the shipped ones.

Usage: python3 -I variants.py <the shipped setting.json> <out folder>
"""
import json
import sys
from pathlib import Path

shipped, out = json.load(open(sys.argv[1])), Path(sys.argv[2])


def write(name, ticks, held=None, tied=None):
    d = json.loads(json.dumps(shipped))
    d["ticks"] = ticks
    for g in d["gears"]:
        if held is not None and g[0] == 1 and 60 <= g[2] <= 70:
            g[3] = held
            g[4] = held
    if tied is not None:
        for s in range(60, 71):
            d["gears"].append([2, 0, s, tied, tied, 0])
    out.joinpath(name).mkdir(parents=True, exist_ok=True)
    json.dump(d, open(out.joinpath(name, "setting.json"), "w"))


write("mesh450", 450)
write("mesh560", 560)
write("heldpatch", 300, held=2)
write("tiedpatch", 300, tied=500)
for c in (1, 4, 16, 64, 256):
    write(f"tied{c}", 120, tied=c)

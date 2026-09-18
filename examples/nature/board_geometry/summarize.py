"""Compact tables from the JSON of lattice_anisotropy.py.

usage: python summarize.py results.json [more.json ...] [--skip lattice:L ...]
"""

import json
import sys

RADII = (4, 6, 8, 12, 16, 24)
SHORT = {
    "axis (1,0,0)": "axis",
    "face diagonal (1,1,0)": "(110)",
    "body diagonal (1,1,1)": "(111)",
    "oblique (2,1,0)": "(210)",
    "oblique (2,1,1)": "(211)",
    "oblique (3,2,1)": "(321)",
}

args = sys.argv[1:]
skips = set()
paths = []
i = 0
while i < len(args):
    if args[i] == "--skip":
        skips.add(args[i + 1])
        i += 2
    else:
        paths.append(args[i])
        i += 1
results = []
for path in paths:
    with open(path, encoding="utf-8") as handle:
        for res in json.load(handle):
            if f"{res['lattice']}:{res['half_width']}" not in skips:
                results.append(res)


def entry(res, R):
    return res["summary"].get(str(R), res["summary"].get(R, {}))


def spread_table(title, selector):
    print(f"\n{title}: spread between the six lines, max/min - 1, in percent")
    print(
        f"{'lattice':>9} {'walk':>10} {'L':>3} {'quantity':>7} "
        + " ".join(f"{'r=' + str(R):>7}" for R in RADII)
    )
    for res in results:
        for key in selector(res["walk"]):
            cells = []
            for R in RADII:
                s = entry(res, R).get(key, {}).get("spread")
                cells.append(f"{100 * s:>6.1f}%" if s is not None else f"{'-':>7}")
            print(
                f"{res['lattice']:>9} {res['walk']:>10} {res['half_width']:>3} {key:>7} "
                + " ".join(cells)
            )


spread_table("(A) the simple walk, the lattice alone", lambda w: ("n", "J") if w == "simple" else ())
spread_table(
    "(B) the persistent table (forward 6/11), the beam removed on link lines",
    lambda w: ("n_rest", "J_rest") if w == "persistent" else (),
)
spread_table(
    "(C) the persistent table, as is (beam included): what a sink measures",
    lambda w: ("n", "J") if w == "persistent" else (),
)


def line_table(title, key, radii, walk):
    print(f"\n{title}")
    for R in radii:
        print(f"\n r = {R}")
        print(f"{'lattice':>9} {'walk':>10} " + " ".join(f"{SHORT[k]:>7}" for k in SHORT))
        for res in results:
            if res["walk"] != walk:
                continue
            over = entry(res, R).get(key, {}).get("over_axis", {})
            cells = []
            for label in SHORT:
                v = over.get(label)
                cells.append(f"{v:>7.3f}" if v is not None else f"{'-':>7}")
            print(f"{res['lattice']:>9} {res['walk']:>10} " + " ".join(cells))


line_table("(D) simple walk: density n x r per line over the axis", "n", (4, 8, 16), "simple")
line_table(
    "(E) persistent, beam removed: n_rest x r per line over the axis", "n_rest", (4, 8, 16), "persistent"
)
line_table(
    "(F) persistent, as is: |J| x r^2 per line over the axis (the A5s ratio)",
    "J",
    (4, 6, 8, 12, 16),
    "persistent",
)

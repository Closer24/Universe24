"""Hand z1, part (d): the two bodies read apart from the nodes log (the heavy lift's quanta per Node every interval, the board's view): the z-profile summed over x and y, the peak z of each half (z in 0..3 about the centre 2, z in 4..6 about 5), each half's share in milli of the family's, the two peaks' torus distance, and the centroid of each half along z in milli Links; integers only.

    python tools/derivations/open_items/H-Minimal-Seed-1/z1_two_lumps.py tools/derivations/open_items/H-Minimal-Seed-1/out/bodies/bodies.nodes.jsonl "point 2 0" 5 5 7
"""
import json, sys
from pathlib import Path

path, family, X, Y, Z = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
marks = {1, 2, 5, 10, 20, 25, 50, 75, 100, 150, 200, 250, 300}
out = []
for line in Path(path).read_text().splitlines():
    row = json.loads(line)
    q = row["quanta"].get(family)
    if q is None:
        continue
    profile = [0] * Z
    for i, v in enumerate(q):
        profile[i % Z] += int(v)
    total = sum(profile)
    halves = ([0, 1, 2, 3], [4, 5, 6])  # the lump about z = 2 and the lump about z = 5 (the torus's 7 Nodes split at 3 | 4 and 6 | 0)
    found = {"t": row["interval"], "total": total, "profile": profile}
    peaks = []
    for name, centre, zs in (("A", 2, halves[0]), ("B", 5, halves[1])):
        part = sum(profile[z] for z in zs)
        peak = max(zs, key=lambda z: profile[z]) if part else None
        moment = sum(profile[z] * (z - centre) for z in zs)
        found[name] = {"share_milli": (1000 * part) // total if total else None, "peak_z": peak, "centroid_milli": (1000 * moment) // part if part else None}
        peaks.append(peak)
    if None not in peaks:
        d = abs(peaks[0] - peaks[1])
        found["peak_gap"] = min(d, Z - d)
        found["separation_milli"] = 3000 + found["B"]["centroid_milli"] - found["A"]["centroid_milli"]
    out.append(found)
for f in out:
    if f["t"] in marks:
        print(json.dumps(f))
seps = [(f["t"], f.get("separation_milli")) for f in out if f.get("separation_milli") is not None]
gaps = [f.get("peak_gap") for f in out if f.get("peak_gap") is not None]
print(json.dumps({"separation_first_last": [seps[0], seps[-1]], "separation_least_largest": [min(s for _t, s in seps), max(s for _t, s in seps)], "peak_gap_least": min(gaps), "peak_gap_largest": max(gaps), "intervals_gap_1": sum(1 for g in gaps if g == 1), "intervals_gap_0": sum(1 for g in gaps if g == 0), "intervals_gap_3": sum(1 for g in gaps if g == 3)}))
Path(path).with_suffix(".two_lumps.json").write_text(json.dumps(out) + "\n")

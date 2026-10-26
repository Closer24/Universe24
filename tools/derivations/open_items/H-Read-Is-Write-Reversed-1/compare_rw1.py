"""rw1's comparison of records bit for bit, the rows' milliseconds (a clock reading, no integer of the law) struck: the flagged run against the cache (seven worlds) and the flag on against the flag off (three worlds); the run back, the counts, the turns, the Node lines and the log named in the table. Usage: compare_rw1.py <out dir> <cache dir>"""
import json
import os
import sys

sys.set_int_max_str_digits(0)
out, cache = sys.argv[1], sys.argv[2]
PAIRS = [
    ("hole60", os.path.join(cache, "world_hole_60.json")),
    ("chiral60", os.path.join(cache, "world_chiral_60.json")),
    ("bodies300", os.path.join(cache, "world_bodies_300.json")),
    ("universe400", os.path.join(cache, "world_universe_400.json")),
    ("pair3_400", os.path.join(cache, "world_pair_3_400.json")),
    ("plasma3_170", os.path.join(cache, "world_plasma_3_170.json")),
    ("ga2_450", os.path.join(cache, "world_ga2_450.json")),
    ("sea3_240_on", os.path.join(out, "sea3_240_off.json")),
    ("universe3_100_on", os.path.join(out, "universe3_100_off.json")),
    ("plasma_170_on", os.path.join(out, "plasma_170_off.json")),
]


def load(path):
    d = json.load(open(path))
    for r in d.get("rows", []):
        r.pop("milliseconds", None)
    return d


rows = []
for name, other in PAIRS:
    mine = os.path.join(out, name + ".json")
    if not (os.path.exists(mine) and os.path.exists(other)):
        rows.append((name, "NOT RUN", None, None, None, None))
        continue
    a, b = load(mine), load(other)
    keys = ["log", "nodes", "counts", "turns", "rows"]
    same = {k: a.get(k) == b.get(k) for k in keys}
    rb = a.get("run_back")
    # the run back of the cached record may be of another count; the flagged run's own run back is the measure
    rows.append((name, "SAME" if all(same.values()) else "APART " + ",".join(k for k, v in same.items() if not v), rb, a["counts"]["births"], a["counts"]["body_clicks"], a["counts"]["turns"], len(a["log"])))
print("| run | against | run back (intervals, exact) | births | credits | turns | log lines |")
print("| --- | --- | --- | --- | --- | --- | --- |")
for r in rows:
    print("| " + " | ".join(str(x) for x in r) + " |")

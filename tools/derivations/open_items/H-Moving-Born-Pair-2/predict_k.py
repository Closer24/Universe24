"""H-Moving-Born-Pair-2: the prediction before the runs. For every birth of a record of the head (the log's dP_take, the born Link's axis from minus to plus, the children's row's num, E = A B (v.G.v): the plane's T div 2, the quartet's 4 (T div 2)), den sin k = min(den, |dP_a| den div (2 num 2 E)) and h = den sin(k / 2) = isqrt(den (den - den cos k) div 2); the count of births with h = 0 (the rest lay returns) against h above 0. Integers only. Usage: python predict_k.py <record.json> [<record.json> ...]"""

import json
import sys
from math import isqrt

AXES = 3


def axis_side(minus, plus, cube):
    for a in range(AXES):
        for side in (1, -1):
            if all(((minus[b] + (side if b == a else 0)) % cube) == plus[b] % cube for b in range(AXES)):
                return a, side
    raise ValueError("not one Link")


for path in sys.argv[1:]:
    r = json.load(open(path))
    den, cube = int(r["den"]), int(r["cube"])
    rows = r["universe"]["rows"]
    T = int(r["universe"]["integers"]["quantum_action"])
    E_plane = T // 2
    births = [e for e in r["log"] if e["event"] == "birth" and "takes" not in e]
    zero, above, edge, first = 0, 0, 0, None
    sines = []
    for e in births:
        s = e["line_pair"]
        row = rows[s]
        num = int(row["pair"][0])
        norm = 4 if row["shape"] == 8 else 1
        E = E_plane * norm
        a, side = axis_side(e["minus"], e["plus"], cube)
        dp = abs(int(e["dP_take"][a]))
        sine = min(den, (dp * den) // ((num + num) * (E + E)))
        cosine = isqrt(den * den - sine * sine)
        h = isqrt((den * (den - cosine)) // 2)
        if h == 0:
            zero += 1
        else:
            above += 1
            if first is None:
                first = e["i"]
        if sine == den:
            edge += 1
        sines.append((e["i"], a, side, dp, sine * 1000 // den, h * 1000 // den))
    print(json.dumps({"record": path.split("/")[-1], "births": len(births), "h zero": zero, "h above zero": above, "at the band's edge": edge, "first interval with h above 0": first, "per birth (i, axis, side, |dP_a|, den sin k per mille, h per mille)": sines}))

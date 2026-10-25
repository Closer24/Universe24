"""pl2: the two rows' Wronskians at the plasma's seed (nothing run): the lay's amplitude per row, W per Node per row, the total, the sign row's write quotient per interval 2 W div T, and whether an integer amplitude of the light row cancels the heavy row's W exactly (letter (b), the neutral lay to the integer). Integers only."""
import json, os, sys
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe import gram
from event_universe.core.paces import sine_den
from event_universe.core.rule3 import quotient, signed_quotient
world_path = sys.argv[1]
universe, world = load_world(world_path)
node = Node(universe, world)
T, den = node.T, node.den
out = {"world": world_path, "T": T}
rows = []
for rec, row in enumerate(node.records()):
    w = gram.charge(row.shape, row.lines)
    vals = sorted(set(int(x) for x in w.reshape(-1)))
    re, im = row.lines
    rows.append({"rec": rec, "pair num": str(row.pair[0]), "gap": str(row.gap), "sine": str(sine_den(row.pair[0], den)),
        "unit": str(node.units[rec]), "re_now": int(re.now.reshape(-1)[0]), "re_before": int(re.before.reshape(-1)[0]),
        "im_now": int(im.now.reshape(-1)[0]), "im_before": int(im.before.reshape(-1)[0]), "W per Node (distinct)": vals})
out["rows"] = rows
total = sum(r["W per Node (distinct)"][0] for r in rows)
out["W total per Node"] = total
out["2 W total div T, remainder"] = [quotient(2 * total, T), 2 * total - T * quotient(2 * total, T)]
out["lays"] = [e for e in node.log if e["event"] == "lay"]
# letter (b): the light row's amplitude A at which A * (A s div den) equals the heavy row's |W| exactly
heavy = [r for r in rows if int(r["gap"]) > 0 and r["W per Node (distinct)"][0] > 0]
light = [r for r in rows if int(r["gap"]) > 0 and r["W per Node (distinct)"][0] < 0]
if heavy and light:
    target = heavy[0]["W per Node (distinct)"][0]
    s = int(light[0]["sine"])
    def w_of(a):
        return a * int(signed_quotient(a * s, den))
    lo, hi = 1, 1
    while w_of(hi) < target:
        hi *= 2
    while hi - lo > 1:
        mid = quotient(lo + hi, 2)
        if w_of(mid) < target:
            lo = mid
        else:
            hi = mid
    out["letter (b)"] = {"heavy W": target, "light sine": str(s), "light amplitude laid": light[0]["re_now"],
        "W(light) at laid amplitude": w_of(light[0]["re_now"]),
        "nearest amplitudes": [(a, w_of(a), w_of(a) - target) for a in (lo - 1, lo, hi, hi + 1)],
        "exact integer amplitude exists": any(w_of(a) == target for a in (lo - 1, lo, hi, hi + 1))}
print(json.dumps(out, indent=1))

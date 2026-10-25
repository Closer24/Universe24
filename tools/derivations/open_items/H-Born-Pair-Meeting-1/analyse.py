"""sl1's reading of a record under the generic close: every birth with its children's W, taken against booked; every probe of the born pair's Link by its offset from the birth (whole at both ends, F_re, F_im, the twist, the gap-0 standing at the ends, the fall against the walls of two light quanta); every gapped meeting's refusal sorted into the born pairs' own Links against other Links; the clicks' conservations (the charge at every birth, taken >= booked, the senses' sum). Integers only.
Usage: python analyse.py <out.json>"""

import json
import sys

sys.set_int_max_str_digits(0)
rec = json.load(open(sys.argv[1]))
log = rec["log"]
units = [int(u) for u in rec["units"]]
planes = rec["planes"]
den = int(rec["den"])
nrec = len(units)
gap0 = next(k for k, p in enumerate(planes) if int(p) == den)
print("den", den, "units", units, "gap-0 record", gap0, "intervals", rec["intervals"])
print("counts:", {k: v for k, v in rec["counts"].items() if not k.startswith("sl1_") or "rec" in k})
print("final:", rec["final"], "run back:", rec["run_back"])

births = [e for e in log if e["event"] == "birth"]
print("\nBIRTHS", len(births))
opposite = sum(1 for e in births if e["W_children"][0] * e["W_children"][1] < 0)
senses = sum(s for e in births for s in e["senses"])
w_sum = sum(w for e in births for w in e["W_children"])
at_or_above = sum(1 for e in births if e["taken"] >= e["booked"])
taken_total = sum(e["taken"] for e in births)
booked_total = sum(e["booked"] for e in births)
print("children at opposite W: %d of %d; senses' sum %d; W_children summed %d; taken >= booked at %d of %d; taken per booked (hundredths) %d" % (
    opposite, len(births), senses, w_sum, at_or_above, len(births), (100 * taken_total) // booked_total if booked_total else 0))
for e in births:
    print("  birth i %d at %s row %d minus %s plus %s W %s taken %d booked %d levels %d taken_row %s" % (
        e["i"], e["node"], e["line_pair"], e["minus"], e["plus"], e["W_children"], e["taken"], e["booked"], e["levels"], e.get("taken_row", gap0)))

links = {}
for e in births:
    links[(tuple(e["minus"]), tuple(e["plus"]))] = e
    links[(tuple(e["plus"]), tuple(e["minus"]))] = e

print("\nPROBES of the born pairs' Links by the offset from the birth (count; whole at both ends; F_re = 0; F_im = 0; twist = 0; gap-0 standing > 0 at both ends; the fall at the into end against the walls)")
probes = [e for e in log if e["event"] == "sl1_probe"]
by_offset = {}
for p in probes:
    by_offset.setdefault(p["i"] - p["birth_i"], []).append(p)
for off in sorted(by_offset):
    ps = by_offset[off]
    whole = sum(p["whole_both_ends"] for p in ps)
    fre0 = sum(1 for p in ps if p["F_re"] == 0)
    fim0 = sum(1 for p in ps if p["F_im"] == 0)
    tw0 = sum(1 for p in ps if p["twist"] == 0)
    g0 = sum(1 for p in ps if p["gap0_standing"][0] > 0 and p["gap0_standing"][1] > 0)
    can_pay = sum(1 for p in ps if any(f[0] is not None for f in p["falls"]))
    full_max = max(max(f[1] for f in p["falls"]) for p in ps)
    print("  offset %2d: %2d probes; whole both ends %2d; F_re=0 %2d; F_im=0 %2d; twist=0 %2d; gap-0 standing at both ends %2d; an end able to pay two light quanta %d (largest full fall %d against walls %d)" % (
        off, len(ps), whole, fre0, fim0, tw0, g0, can_pay, full_max, ps[0]["walls_two_light"]))
print("the first probes in full (offset 1):")
for p in by_offset.get(1, [])[:16]:
    print("  ", json.dumps({k: p[k] for k in ("birth_i", "node", "link", "line_pair", "standing", "F_re", "F_im", "twist", "gap0_standing", "falls", "F_gap0")}))
print("offset 2, the standing in the unit and the currents:")
for p in by_offset.get(2, [])[:16]:
    print("  ", json.dumps({k: p[k] for k in ("birth_i", "standing", "F_re", "F_im", "twist")}))

print("\nthe gapped meetings' refusals: at a born pair's own Link against another Link, by cause and record")
table = {}
for e in log:
    if e["event"] != "refused" or e.get("taken_row", gap0) == gap0:
        continue
    r = e["taken_row"]
    if "link" in e:
        own = (tuple(e["node"]), tuple(e["link"])) in links
        b = links.get((tuple(e["node"]), tuple(e["link"])))
        where = "own Link (born at %d, read at %d)" % (b["i"], e["i"]) if own else "other Link"
        where = "own Link" if own else "other Link"
    else:
        where = "take's Node"
    key = (r, e["cause"], where)
    table[key] = table.get(key, 0) + 1
for key in sorted(table):
    print("  record %d cause %-12s %-12s %d" % (key[0], key[1], key[2], table[key]))
stops = [e for e in log if e["event"] == "refused" and e["cause"] == "stop" and e.get("taken_row", gap0) != gap0]
for e in stops:
    print("  STOP of a gapped take:", json.dumps(e))
lays = [e for e in log if e["event"] == "refused" and e["cause"] == "lay" and e.get("taken_row", gap0) != gap0]
if lays:
    print("  the first gapped lay refusals:", json.dumps(lays[:4]))
taken_gapped = [e for e in births if e.get("taken_row", gap0) != gap0]
print("  gapped meetings TAKEN (the merger):", len(taken_gapped))

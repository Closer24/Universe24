"""The exact take read in the clicks (hand ex2): over every birth and credit line of a record, the identity
taken + rem_before == booked + rem_after (EX-S1), counted exact of all; the former reading taken per booked over the births
in hundredths; the new reading (taken - (rem_after - rem_before)) per booked, exact 100 where the identity holds; the
takes paid from the carry alone (levels 0); the largest remainder held, in share units, in bits and in hundredths of the
gap-0 unit; the Nodes taken more than once; the counts.  Usage: python read_exact.py record.json"""
import json, sys
from collections import Counter

sys.set_int_max_str_digits(0)
rec = json.load(open(sys.argv[1], encoding="utf-8"))
# the units of the record's rows (the default's credit lines carry no booked): unit_of(sine_den(num, den), T), 3 den T at the gap 0
from event_universe.core.paces import sine_den
from event_universe.core.rule3 import unit_of
den, T = int(rec["den"]), int(rec["T"])
units = [unit_of(sine_den(int(p), den) if int(p) != den else den, T) for p in rec["planes"]]
lines = [e for e in rec["log"] if e["event"] in ("birth", "credit")]
births = [e for e in lines if e["event"] == "birth"]
credits = [e for e in lines if e["event"] == "credit"]
# one take per Node per interval: the birth lines of one take repeat the take's numbers, so count takes once
takes = {}
for e in lines:
    key = (e["i"], tuple(e["node"]), e["event"])
    takes.setdefault(key, e)
takes = list(takes.values())
exact = 0
zero_level = 0
max_rem = 0
by_node = Counter()
for e in takes:
    by_node[tuple(e["node"])] += 1
    if "take_rem" in e:
        before, after, booked = e["take_rem"]
        if e["taken"] + before == booked + after:
            exact += 1
        max_rem = max(max_rem, after)
        if e["levels"] == 0:
            zero_level += 1
taken_b = sum(e["taken"] for e in births)
booked_b = sum(e["booked"] for e in births)
taken_t = sum(e["taken"] for e in takes)
booked_t = sum((e["take_rem"][2] if "take_rem" in e else e.get("booked", units[e["line"]])) for e in takes)
d_rem = sum((e["take_rem"][1] - e["take_rem"][0]) for e in takes if "take_rem" in e)
hund = lambda a, b: (100 * a) // b if b else None
counts = rec["counts"]
out = {
    "births": len(births),
    "credits": len(credits),
    "takes (one per Node per interval)": len(takes),
    "identity taken + rem_before == booked + rem_after: exact of all": [exact, len(takes)],
    "former reading: taken per booked over the births (hundredths)": hund(taken_b, booked_b),
    "former reading over every take (hundredths)": hund(taken_t, booked_t),
    "new reading: (taken - dE) per booked over every take (hundredths)": hund(taken_t - d_rem, booked_t) if "take_rem" in (takes[0] if takes else {}) else None,
    "takes paid from the carry alone (levels 0)": zero_level,
    "Nodes taken more than once": sum(1 for n, k in by_node.items() if k > 1),
    "takes at a Node taken before": sum(k - 1 for k in by_node.values()),
    "largest remainder held (share units)": str(max_rem),
    "largest remainder held (bits)": max_rem.bit_length(),
    "sum of the remainders' changes (share units)": str(d_rem),
    "counts": counts,
    "run_back": rec["run_back"],
    "integers / max bits (last reader row)": [rec["rows"][-1]["integers"], rec["rows"][-1]["max bits"]],
}
if "take_rem_held" in counts:
    out["identity in the counts: taken_all - booked_all == take_rem_held"] = (
        int(counts["taken_all"]) - int(counts["booked_all"]) == int(counts["take_rem_held"])
    )
    out["remainder held in hundredths of the first take's booked"] = hund(int(counts["take_rem_held"]), takes[0]["take_rem"][2]) if takes else None
for k, v in out.items():
    print(json.dumps({k: v}))

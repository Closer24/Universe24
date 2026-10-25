"""cs7: the third slimming where shrink2's is still above the bound: the credits' frames dropped (the credit's numbers kept: i, node, line, sense, beat, taken, levels, taker, taken_line, arrivals, laid_back, dP_take), the landing census kept, the diag kept whole. Usage: python shrink3.py <record.json> ..."""
import json, os, sys
sys.set_int_max_str_digits(0)
for p in sys.argv[1:]:
    rec = json.load(open(p))
    for e in rec["log"]:
        if e["event"] == "credit":
            e.pop("frame", None)
    json.dump(rec, open(p, "w"))
    print(p, "slimmed to", os.path.getsize(p))

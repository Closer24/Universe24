"""cs5: the records slimmed under 1,500,000 bytes (the rule): the per-interval Node rows and the run's rows dropped (the diag, the log, the counts, the run back and the integers kept, which every reader of this round uses); a record still above the bound after the slimming is removed after its reading and named.
Usage: python shrink.py out"""
import json
import os
import sys

sys.set_int_max_str_digits(0)
out = sys.argv[1]
bound = 1500000
for name in sorted(os.listdir(out)):
    p = os.path.join(out, name)
    if not name.endswith(".json") or os.path.getsize(p) <= bound:
        continue
    rec = json.load(open(p))
    for k in ("rows", "nodes"):
        rec.pop(k, None)
    json.dump(rec, open(p, "w"))
    size = os.path.getsize(p)
    print(name, "slimmed to", size, "REMOVED (above the bound after the slimming)" if size > bound else "")
    if size > bound:
        os.remove(p)

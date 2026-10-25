"""cs4: a record kept slim under 1.5 MB: the Node lines reduced to i, X, turned; the log kept without the refused lines (counted per cause and interval into refused_counts) where the record is above the limit; the diag, the lay line, the landing census, the births and the credits kept whole. Usage: python shrink2.py <out.json> ..."""
import json
import os
import sys

sys.set_int_max_str_digits(0)
for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    d["nodes"] = [{"i": n["i"], "X": n["X"], "turned": n["turned"]} for n in d["nodes"]]
    counts = {}
    kept = []
    for e in d["log"]:
        if e["event"] == "refused":
            key = f"{e['i']}:{e['cause']}" + ("_crowd" if "children_at_one_node" in e else "_standing" if "standing" in e else "")
            counts[key] = counts.get(key, 0) + 1
        else:
            kept.append(e)
    d["log"] = kept
    d["refused_counts"] = counts
    d["slim"] = "the Node lines reduced to i, X, turned; the refused lines counted per interval and cause (shrink2.py)"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f)
    print(path, os.path.getsize(path))

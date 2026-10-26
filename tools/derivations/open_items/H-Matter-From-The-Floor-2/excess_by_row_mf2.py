"""mf2: the excess (+ child at the take's Node less at the other end) per taken row and per bang, and the rest births (room 0 on the emitter's births)."""
import json
import sys

rec = json.load(open(sys.argv[1]))
starts = [int(x) for x in sys.argv[2].split(",")] + [10 ** 9]
out = {}
for e in rec["log"]:
    if e["event"] != "birth":
        continue
    k = max(j for j in range(len(starts) - 1) if e["i"] >= starts[j]) + 1
    r = out.setdefault("bang %d row %d" % (k, e["taken_row"]), {"births": 0, "plus_at_take": 0, "minus_at_take": 0, "room0": 0})
    r["births"] += 1
    r["plus_at_take"] += tuple(e["plus"]) == tuple(e["node"])
    r["minus_at_take"] += tuple(e["minus"]) == tuple(e["node"])
    r["room0"] += e["room"] == 0
print(json.dumps(out))

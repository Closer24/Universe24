"""bg1: read a probe record (bg1_probe.py's jsonl): the frozen count per interval, the board's content sum at every 100, the hovering set's content, the gradient meetings and the births from the first freeze with their Nodes and distances, the counts' change from the first freeze, the children's course. Integers only. Usage: bg1_read.py <out.jsonl>"""
import json
import sys
from collections import Counter

lines = [json.loads(l) for l in open(sys.argv[1])]
body = [l for l in lines if "i" in l]
tail = lines[-1] if lines[-1].get("tail") else None
first_freeze = next((l["i"] for l in body if l["frozen"]), None)
print("intervals read", len(body), "first freeze", first_freeze, "ever frozen", body[-1]["ever"])
fro = Counter(len(l["frozen"]) for l in body)
print("frozen per interval histogram", dict(sorted(fro.items())), "max", max(fro))
print("board content sum at every 100:", [(l["i"], l["board_content_sum"]) for l in body if l["i"] % 100 == 0])
after = [l for l in body if first_freeze is not None and l["i"] >= first_freeze]
delta = Counter()
for l in after:
    for k, v in l["counts_delta"].items():
        delta[k] += v
print("counts change from the first freeze:", dict(delta))
clicks = [c for l in body for c in l["clicks"]]
print("clicks by kind:", dict(Counter(c["event"] for c in clicks)))
g = [c for c in clicks if c["event"] == "gradient"]
print("gradient meetings by distance from the frozen set:", dict(Counter(c["distance_from_frozen"] for c in g)), "by row:", dict(Counter(c["row"] for c in g)), "twist 0:", sum(1 for c in g if c["twist"] == 0), "paces (sorted pairs) top:", Counter(tuple(sorted(c["paces"])) for c in g).most_common(6))
g_after = [c for c in g if first_freeze is not None and c["i"] >= first_freeze]
print("gradient meetings from the first freeze:", len(g_after), "intervals with one:", len(set(c["i"] for c in g_after)))
b = [c for c in clicks if c["event"] == "birth"]
print("births:", len(b), "from the first freeze:", sum(1 for c in b if first_freeze is not None and c["i"] >= first_freeze))
for x in b:
    print("  birth", {k: x.get(k) for k in ("i", "node", "minus", "plus", "line_pair", "taken_row", "W_children", "taken", "booked", "levels", "distance_from_frozen", "content", "content_minus_plus")})
cr = [c for c in clicks if c["event"] == "credit"]
print("credits:", len(cr), "last at", cr[-1]["i"] if cr else None, "from the first freeze:", sum(1 for c in cr if first_freeze is not None and c["i"] >= first_freeze))
if after:
    w0 = after[0]["content_watch"]
    print("hovering set at the first freeze:", len(w0), "content", sorted(w0.values())[:3], "...", sorted(w0.values())[-3:])
    wl = after[-1]["content_watch"]
    print("hovering set at the end:", len(wl), "content min/max", min(wl.values()), max(wl.values()))
print("bits: transient", max(l["max transient"] for l in body), "state", max(l["state bits"] for l in body))
if tail:
    print("run back", tail["run back"], "counts", tail["counts"])
    for k, v in list(tail.get("course", {}).items())[:6]:
        print("course", k, v[:8], "...", v[-3:])

"""hr1: the horizon's neighbourhood read on a record (run.record's JSON with nodes and log, or hr1_stream.py's JSONL): the Nodes that ever froze and their first freeze; per interval from the first freeze the frozen set, the content at every Node that ever froze, the sum of content over the neighbourhood (the ever-frozen Nodes and their six neighbours) against the rest of the board; the credits per interval with their Node, their distance in Links (on the torus) from the nearest Node that ever froze at that interval or before, their levels and taken; the credits' rate per interval in the neighbourhood against the rest, before and after the first freeze; the gap-0 current on the six Links of the ever-frozen Nodes (out of the Node positive) where the record carries it. Integers only. Usage: hr1_read.py <record> <out.json> [label]"""
import json
import sys

sys.set_int_max_str_digits(0)
path = sys.argv[1]
label = sys.argv[3] if len(sys.argv) > 3 else path
if path.endswith(".jsonl"):
    lines = [json.loads(l) for l in open(path)]
    head = lines[0]
    nodes = [l for l in lines if "i" in l]
    tail = next((l for l in lines if l.get("tail")), None)
    cube = int(head["shape"][0])
    log = [dict(c, i=l["i"]) for l in nodes for c in l["clicks"]]
    counts = tail["counts"] if tail else None
    run_back = tail["run back"] if tail else None
else:
    R = json.load(open(path))
    cube = int(R["cube"])
    nodes = R["nodes"]
    log = R["log"]
    counts = R["counts"]
    run_back = R.get("run_back")
N = cube ** 3
at = lambda i: (i // (cube * cube), (i // cube) % cube, i % cube)
idx = lambda p: (p[0] % cube) * cube * cube + (p[1] % cube) * cube + (p[2] % cube)
def dist(a, b):
    return sum(min(abs(x - y), cube - abs(x - y)) for x, y in zip(at(a), at(b)))
def neighbours(n):
    x, y, z = at(n)
    return [idx((x + 1, y, z)), idx((x - 1, y, z)), idx((x, y + 1, z)), idx((x, y - 1, z)), idx((x, y, z + 1)), idx((x, y, z - 1))]
first = {}
for ln in nodes:
    for n in ln["frozen"]:
        first.setdefault(n, ln["i"])
ever = sorted(first)
first_i = min(first.values()) if first else None
hood = set(ever) | {m for n in ever for m in neighbours(n)}
credits = [e for e in log if e["event"] == "credit"]
births = [e for e in log if e["event"] == "birth"]
last_i = nodes[-1]["i"]
per = []
for ln in nodes:
    i = ln["i"]
    if first_i is None or i < first_i - 2:
        continue
    frozen_so_far = [n for n in ever if first[n] <= i]
    c = ln["content"]
    hood_i = set(frozen_so_far) | {m for n in frozen_so_far for m in neighbours(n)}
    cr = [e for e in credits if e["i"] == i]
    row = {
        "i": i, "frozen": ln["frozen"], "turned at frozen": [n for n in ln["frozen"] if n in ln["turned"]],
        "content at ever-frozen": {str(n): int(c[n]) for n in ever if first[n] <= i},
        "hood nodes": len(hood_i), "hood content sum": sum(int(c[n]) for n in hood_i), "rest content sum": sum(int(c[n]) for n in range(N) if n not in hood_i),
        "board content sum": sum(int(x) for x in c), "board content max": max(int(x) for x in c),
        "credits": [{"node": idx(e["node"]), "d": min((dist(idx(e["node"]), n) for n in frozen_so_far), default=None), "levels": int(e["levels"]), "taken bits": int(e["taken"]).bit_length(), "content": int(e["content"])} for e in cr],
    }
    if "current" in ln:
        cur = ln["current"]
        outflow = 0
        for n in frozen_so_far:
            x, y, z = at(n)
            for axis in range(3):
                outflow += int(cur[axis][n])  # from the Node along +axis
                outflow -= int(cur[axis][idx(tuple(v - (1 if k == axis else 0) for k, v in enumerate((x, y, z))))])  # into the Node from the -axis neighbour
        row["gap-0 current out of the frozen Nodes (sum of six Links)"] = outflow
    per.append(row)
def rate(lo, hi, where):
    sel = [e for e in credits if lo <= e["i"] <= hi and where(idx(e["node"]))]
    return {"credits": len(sel), "intervals": hi - lo + 1, "levels sum": sum(int(e["levels"]) for e in sel)}
summary = {
    "record": label, "cube": cube, "intervals": last_i, "counts": counts, "run back": run_back,
    "ever-frozen Nodes": {str(n): {"at": list(at(n)), "first freeze": first[n], "frozen lines": sum(1 for ln in nodes if n in ln["frozen"])} for n in ever},
    "first freeze": first_i, "hood size at the end": len(hood),
    "credits total": len(credits), "births total": len(births),
    "credits at an ever-frozen Node, ever": sum(1 for e in credits if idx(e["node"]) in ever),
    "credits at an ever-frozen Node after its first freeze": sum(1 for e in credits if idx(e["node"]) in ever and e["i"] > first[idx(e["node"])]),
    "credits at a frozen Node at its frozen interval": sum(1 for e in credits for ln in nodes if ln["i"] == e["i"] and idx(e["node"]) in ln["frozen"]),
    "credits by distance from the nearest ever-frozen Node (all intervals, final set)": {str(d): sum(1 for e in credits if min(dist(idx(e["node"]), n) for n in ever) == d) for d in range(0, 3 * (cube // 2) + 1)} if ever else None,
    "credits by distance after the first freeze (the set at the interval)": {},
    "rate in the hood before/after the first freeze (final hood)": None if first_i is None else {
        "before": rate(1, first_i - 1, lambda n: n in hood), "after": rate(first_i, last_i, lambda n: n in hood),
        "rest before": rate(1, first_i - 1, lambda n: n not in hood), "rest after": rate(first_i, last_i, lambda n: n not in hood)},
    "levels of credits min/max": [min((int(e["levels"]) for e in credits), default=None), max((int(e["levels"]) for e in credits), default=None)],
    "taken bits of credits min/max": [min((int(e["taken"]).bit_length() for e in credits), default=None), max((int(e["taken"]).bit_length() for e in credits), default=None)],
    "credits with levels > 1": sum(1 for e in credits if int(e["levels"]) > 1),
    "board content sum first/last": [sum(int(x) for x in nodes[0]["content"]), sum(int(x) for x in nodes[-1]["content"])],
    "per interval": per,
}
by_d = {}
for row in per:
    if row["i"] >= (first_i or 0):
        for cr in row["credits"]:
            by_d[str(cr["d"])] = by_d.get(str(cr["d"]), 0) + 1
summary["credits by distance after the first freeze (the set at the interval)"] = by_d
json.dump(summary, open(sys.argv[2], "w"), default=str, indent=1)
print(json.dumps({k: v for k, v in summary.items() if k != "per interval"}, default=str))

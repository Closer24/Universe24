"""hr2: the same reading on a record file (the Boss's head chiral 2,400, $S/bh/chiral_2400.json): per interval the frozen set, the content at every Node that ever froze, the sum of content over the horizon's neighbourhood (ever frozen and six neighbours) against the rest, the credits of the interval with their Node and distance in Links from the nearest Node that ever froze; written as JSON lines. Usage: read_head.py <record.json> <out.jsonl> <summary.json>"""
import json
import sys

sys.set_int_max_str_digits(0)
R = json.load(open(sys.argv[1]))
cube = int(R["cube"])


def at(i):
    return (i // (cube * cube), (i // cube) % cube, i % cube)


def index(p):
    return p[0] * cube * cube + p[1] * cube + p[2]


def dist(a, b):
    return sum(min((x - y) % cube, (y - x) % cube) for x, y in zip(a, b))


def neighbours(i):
    p = at(i)
    out = set()
    for ax in range(3):
        for d in (-1, 1):
            q = list(p)
            q[ax] = (q[ax] + d) % cube
            out.add(index(tuple(q)))
    return out


by_i = {}
for e in R["log"]:
    if e.get("event") in ("birth", "credit"):
        by_i.setdefault(int(e["i"]), []).append(e)
ever, ever_set, hood, first = [], set(), set(), {}
out = open(sys.argv[2], "w")
tot = {"credits": 0, "credits_after_first_freeze": 0, "credits_in_hood_after": 0, "credits_at_ever_after": 0, "credits_dist": {}}
for line in R["nodes"]:
    i = int(line["i"])
    c = [int(x) for x in line["content"]]
    frozen = [int(k) for k in line["frozen"]]
    for k in frozen:
        if k not in ever_set:
            ever_set.add(k); ever.append(k); first[k] = i; hood.add(k); hood |= neighbours(k)
    clicks = []
    for e in by_i.get(i, []):
        p = tuple(int(v) for v in e["node"])
        d = min((dist(p, at(k)) for k in ever), default=None)
        clicks.append({"event": e["event"], "node": list(p), "index": index(p), "dist": d, "levels": int(e.get("levels", 0)), "beat": int(e.get("beat", 0)) if e["event"] == "credit" else None, "proper": int(e.get("proper", 0)), "content": int(e.get("content", 0)), "sense": e.get("sense")})
        if e["event"] == "credit":
            tot["credits"] += 1
            if ever:
                tot["credits_after_first_freeze"] += 1
                tot["credits_dist"][str(d)] = tot["credits_dist"].get(str(d), 0) + 1
                if index(p) in hood: tot["credits_in_hood_after"] += 1
                if index(p) in ever_set: tot["credits_at_ever_after"] += 1
    rec = {"i": i, "frozen": frozen, "turned_ever": [k for k in ever if k in set(int(t) for t in line["turned"])], "content_ever": {str(k): c[k] for k in ever}, "X_ever": {str(k): int(line["X"][k]) for k in ever}, "hood_size": len(hood), "hood_content_sum": sum(c[k] for k in hood), "rest_content_sum": sum(c[k] for k in range(len(c)) if k not in hood), "board_content_sum": sum(c), "max_content": max(c), "clicks": clicks, "credits": sum(1 for e in clicks if e["event"] == "credit"), "births": sum(1 for e in clicks if e["event"] == "birth")}
    out.write(json.dumps(rec) + "\n")
out.close()
summary = {"record": sys.argv[1], "intervals": len(R["nodes"]), "ever frozen": [{"index": k, "node": list(at(k)), "first freeze": first[k]} for k in ever], "hood": sorted(hood), "hood size": len(hood), "counts": R["counts"], "run_back": R.get("run_back"), "max bits": max(int(r["max bits"]) for r in R["rows"]), "max transient bits": max(int(r["max transient bits"]) for r in R["rows"]), **tot}
json.dump(summary, open(sys.argv[3], "w"), indent=1)
print(json.dumps(summary)[:3000])

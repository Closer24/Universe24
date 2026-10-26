"""fr2: the chiral 2,400 record under the flag read against the head's (the Boss's $S/bh/chiral_2400.json): the frozen count per interval on both, the head's frozen Nodes (which, at which interval they first freeze on the head), on the flagged record each one's first freeze, its release (the first interval after a freeze at which it is not frozen), its turned intervals, its content after, the clicks (births, credits) at it after its first freeze; the max bits (the rows' 'max bits' and 'max transient bits'); the counts; the run back. Usage: read_chiral.py <flagged.json> <head.json> <out.json>"""
import json
import sys

sys.set_int_max_str_digits(0)
F = json.load(open(sys.argv[1]))
Hd = json.load(open(sys.argv[2]))
cube = int(Hd["cube"])


def at(i):
    return (i // (cube * cube), (i // cube) % cube, i % cube)


def frozen_by_interval(rec):
    return {line["i"]: list(line["frozen"]) for line in rec["nodes"]}


fh, ff = frozen_by_interval(Hd), frozen_by_interval(F)
head_frozen_nodes = {}
for i in sorted(fh):
    for n in fh[i]:
        head_frozen_nodes.setdefault(n, i)
flag_frozen_nodes = {}
for i in sorted(ff):
    for n in ff[i]:
        flag_frozen_nodes.setdefault(n, i)
per_node = []
for n, i0 in sorted(head_frozen_nodes.items(), key=lambda kv: kv[1]):
    fi = sorted(i for i in ff if n in ff[i])
    first = fi[0] if fi else None
    release = next((i for i in sorted(ff) if first is not None and i > first and n not in ff[i]), None)
    turned = [i for i in sorted(ff) if n in F["nodes"][i - 1].get("turned", [])] if first is not None else []
    clicks_after = [e for e in F["log"] if e.get("event") in ("birth", "credit") and tuple(e.get("node", ())) == at(n) and first is not None and e["i"] > first]
    content_after = [int(F["nodes"][i - 1]["content"][n]) for i in range(first, min(first + 6, 2401))] if first is not None else []
    per_node.append({"node": at(n), "index": n, "head first freeze": i0, "head frozen lines": len([i for i in fh if n in fh[i]]), "flag first freeze": first, "flag frozen lines": len(fi), "flag release": release, "flag frozen intervals": fi[:12], "flag turned intervals (around)": [i for i in turned if first is not None and abs(i - first) <= 8][:12], "content after (from the freeze)": content_after, "clicks after first freeze": len(clicks_after), "first click after": clicks_after[:2]})
head_counts = {i: len(fh[i]) for i in sorted(fh) if fh[i]}
flag_counts = {i: len(ff[i]) for i in sorted(ff) if ff[i]}
bits = lambda rec, key: max(int(r.get(key, 0)) for r in rec["rows"])
out = {
    "head frozen Nodes": len(head_frozen_nodes), "flag frozen Nodes": len(flag_frozen_nodes),
    "head frozen count per interval (nonzero)": head_counts, "flag frozen count per interval (nonzero)": flag_counts,
    "flag frozen lines total": sum(flag_counts.values()), "head frozen lines total": sum(head_counts.values()),
    "flag max frozen at once": max(flag_counts.values(), default=0), "head max frozen at once": max(head_counts.values(), default=0),
    "flag Nodes frozen more than one interval in a row": sorted({n for i in ff for n in ff[i] if (i + 1) in ff and n in ff[i + 1]}),
    "max bits head/flag": [bits(Hd, "max bits"), bits(F, "max bits")], "max transient bits head/flag": [bits(Hd, "max transient bits"), bits(F, "max transient bits")],
    "counts head": Hd["counts"], "counts flag": F["counts"], "run back flag": F.get("run_back"), "turns head/flag": [Hd["counts"]["turns"], F["counts"]["turns"]],
    "first apart interval (X)": next((line["i"] for line, hl in zip(F["nodes"], Hd["nodes"]) if line["X"] != hl["X"]), None),
    "per head frozen Node": per_node,
}
json.dump(out, open(sys.argv[3], "w"), default=str, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "per head frozen Node"}, default=str)[:4000])
for p in per_node:
    print(p["node"], "head", p["head first freeze"], p["head frozen lines"], "| flag first", p["flag first freeze"], "lines", p["flag frozen lines"], "release", p["flag release"], "turned", p["flag turned intervals (around)"], "content", p["content after (from the freeze)"], "clicks after", p["clicks after first freeze"])

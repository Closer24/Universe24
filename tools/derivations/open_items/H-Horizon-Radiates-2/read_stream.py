"""hr2: the reading of a streamed record (hr2_stream.py's or read_head.py's JSON lines): per Node that ever froze its first freeze, its frozen lines, its releases (a frozen line followed by an unfrozen one), its content's course after the first freeze (min, max, last, the mean of the velocity of X in X-levels per interval while unfrozen), the hovering bound (the longest run of intervals between two freezes and the longest unfrozen stretch); the horizon's neighbourhood against the rest (the content sums at the first freeze, at the end and the change); the credits per interval before and after the first freeze, by their distance in Links from the nearest Node that ever froze (0 at it, 1 its neighbour, 2 and more outside), their levels (the energy in quanta) and beats; the max transient and state bits. Integers only (every rate as numerator / denominator). Usage: read_stream.py <stream.jsonl> [<out.json>]"""
import json
import sys

sys.set_int_max_str_digits(0)
lines = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
n = len(lines)
ever = []
for l in lines:
    for k in l["frozen"]:
        if k not in ever:
            ever.append(k)
first_i = {k: next(l["i"] for l in lines if k in l["frozen"]) for k in ever}
per_node = {}
for k in ever:
    f0 = first_i[k]
    frozen_at = [l["i"] for l in lines if k in l["frozen"]]
    fs = set(frozen_at)
    releases = sum(1 for i in frozen_at if (i + 1) <= lines[-1]["i"] and (i + 1) not in fs)
    two_in_row = sum(1 for i in frozen_at if (i + 1) in fs)
    after = [l for l in lines if l["i"] >= f0]
    contents = [l["content_ever"][str(k)] for l in after]
    xs = [l["X_ever"][str(k)] for l in after]
    vel = [xs[j + 1] - xs[j] for j in range(len(xs) - 1)]
    turned = [l["i"] for l in after if k in l["turned_ever"]]
    # the longest unfrozen stretch between two freezes and the longest since the last freeze
    gaps = [b - a - 1 for a, b in zip(frozen_at, frozen_at[1:])]
    credits_at = [c for l in after for c in l["clicks"] if c["event"] == "credit" and c["index"] == k]
    per_node[str(k)] = {
        "first freeze": f0, "frozen lines": len(frozen_at), "releases": releases, "frozen two in a row": two_in_row,
        "turned lines after": len(turned), "content at first freeze": contents[0], "content min after": min(contents), "content max after": max(contents), "content last": contents[-1],
        "intervals after": len(after), "longest unfrozen gap between freezes": max(gaps, default=0), "intervals since last freeze at the end": lines[-1]["i"] - frozen_at[-1],
        "X at first freeze": xs[0], "X last": xs[-1], "X min after": min(xs), "velocity abs max": max((abs(v) for v in vel), default=0), "velocity sum (X last - X first)": xs[-1] - xs[0],
        "credits at it after": len(credits_at), "credit levels at it after": sum(c["levels"] for c in credits_at),
        "content course (every 50th)": contents[::50][:40], "frozen intervals (first 20)": frozen_at[:20],
    }
f_first = min(first_i.values()) if ever else None
before = [l for l in lines if f_first is None or l["i"] < f_first]
after = [l for l in lines if f_first is not None and l["i"] >= f_first]
def credits_of(ls):
    return [c for l in ls for c in l["clicks"] if c["event"] == "credit"]
cb, ca = credits_of(before), credits_of(after)
by_d = {}
for c in ca:
    d = "0" if c["dist"] == 0 else "1" if c["dist"] == 1 else "2+" if c["dist"] is not None else "none"
    e = by_d.setdefault(d, {"credits": 0, "levels": 0, "beat sum": 0, "beats": {}})
    e["credits"] += 1; e["levels"] += c["levels"]; e["beat sum"] += (c["beat"] or 0); e["beats"][str(c["beat"])] = e["beats"].get(str(c["beat"]), 0) + 1
hood_nodes = set()
out = {
    "stream": sys.argv[1], "intervals": n, "last i": lines[-1]["i"], "ever frozen": ever, "first freeze": f_first,
    "hood size at end": lines[-1]["hood_size"], "board Nodes": len(lines[-1]["content_ever"]) and None,
    "frozen count per interval max": max(len(l["frozen"]) for l in lines), "frozen lines total": sum(len(l["frozen"]) for l in lines),
    "releases total": sum(v["releases"] for v in per_node.values()), "frozen two in a row total": sum(v["frozen two in a row"] for v in per_node.values()),
    "hood content sum at first freeze / end": [after[0]["hood_content_sum"], after[-1]["hood_content_sum"]] if after else None,
    "rest content sum at first freeze / end": [after[0]["rest_content_sum"], after[-1]["rest_content_sum"]] if after else None,
    "board content sum at first freeze / end": [after[0]["board_content_sum"], after[-1]["board_content_sum"]] if after else None,
    "max content at first freeze / end": [after[0]["max_content"], after[-1]["max_content"]] if after else None,
    "credits before first freeze": [len(cb), len(before)], "credits after first freeze": [len(ca), len(after)],
    "credit levels before / after": [sum(c["levels"] for c in cb), sum(c["levels"] for c in ca)],
    "credits after by distance from the nearest Node that ever froze": by_d,
    "credits per 100 intervals after (by distance)": {d: (e["credits"] * 100) // max(1, len(after)) for d, e in by_d.items()},
    "credits at ever-frozen Nodes after, per Node": {k: v["credits at it after"] for k, v in per_node.items()},
    "max transient bits": max((l.get("max_transient_bits", 0) for l in lines), default=None), "max state bits": max((l.get("state_bits", 0) for l in lines), default=None),
    "per node": per_node,
}
if "centre" in lines[-1]:
    cs = [l["centre"] for l in lines]
    out["centre"] = {"frozen lines": sum(1 for c in cs if c["frozen"]), "turned lines": sum(1 for c in cs if c["turned"]), "content min/max/last": [min(c["content"] for c in cs), max(c["content"] for c in cs), cs[-1]["content"]], "content course (first 40)": [c["content"] for c in cs[:40]], "content every 100th": [c["content"] for c in cs[::100]], "neighbours content at end": lines[-1]["centre_neighbours_content"], "neighbours content at 1": lines[0]["centre_neighbours_content"], "proper at end": cs[-1]["proper"], "credits at centre": sum(1 for l in lines for c in l["clicks"] if c["event"] == "credit" and c["dist"] == 0), "credits at neighbours": sum(1 for l in lines for c in l["clicks"] if c["event"] == "credit" and c["dist"] == 1), "credits farther": sum(1 for l in lines for c in l["clicks"] if c["event"] == "credit" and (c["dist"] or 0) >= 2)}
    # the hovering cycle: the frozen intervals of the centre and the gaps
    fz = [l["i"] for l in lines if l["centre"]["frozen"]]
    out["centre"]["frozen intervals (first 30)"] = fz[:30]
    out["centre"]["gaps between freezes (first 30)"] = [b - a for a, b in zip(fz, fz[1:])][:30]
    out["centre"]["gaps between freezes max"] = max([b - a for a, b in zip(fz, fz[1:])], default=0)
if len(sys.argv) > 2:
    json.dump(out, open(sys.argv[2], "w"), indent=1, default=str)
print(json.dumps({k: v for k, v in out.items() if k != "per node"}, default=str))
for k, v in per_node.items():
    print(k, json.dumps({kk: vv for kk, vv in v.items() if "course" not in kk and "first 20" not in kk}))

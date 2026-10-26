"""cm1: the close's one moment, read off two records' own logs (no import of the engine).

Usage: cm1_read.py frame <record.json>          the frame's second moment against its now slot
       cm1_read.py part <a.json> <b.json>       two records compared: counts, refusals, the first parting
       cm1_read.py ends <a.json> <b.json>       the merger births' per-end bookings under two namings
"""

import json
import sys
from collections import Counter


def load(path):
    with open(path) as handle:
        return json.load(handle)


def credits_of(rec):
    return [e for e in rec["log"] if e.get("event") == "credit"]


def births_of(rec):
    return [e for e in rec["log"] if e.get("event") == "birth"]


def frame(path):
    rec = load(path)
    same, off, planes = 0, [], 0
    for c in credits_of(rec):
        f = c["frame"]
        if "re_stepped" not in f:
            continue
        planes += 1
        if (f["re_stepped"], f["im_stepped"]) == (f["re_now"], f["im_now"]):
            same += 1
        else:
            off.append([c["i"], c["node"], f["re_stepped"], f["re_now"], f["im_stepped"], f["im_now"]])
    print(json.dumps({"record": path, "credits": len(credits_of(rec)), "plane frames": planes,
                      "stepped equals now": same, "off": off[:5], "off count": len(off)}))


def counts_of(rec):
    got = dict(rec["counts"])
    got["turns_rows"] = len(rec.get("turns", []))
    got["run_back"] = rec.get("run_back")
    return got


def part(a, b):
    ra, rb = load(a), load(b)
    first = None
    for ea, eb in zip(ra["log"], rb["log"]):
        if ea != eb:
            first = [ea.get("i"), ea.get("event"), eb.get("event"),
                     sorted(k for k in set(ea) | set(eb) if ea.get(k) != eb.get(k))]
            break
    if first is None and len(ra["log"]) != len(rb["log"]):
        longer = ra["log"] if len(ra["log"]) > len(rb["log"]) else rb["log"]
        first = [longer[min(len(ra["log"]), len(rb["log"]))].get("i"), "log length", None, []]
    ca_, cb_ = credits_of(ra), credits_of(rb)
    senses = sum(1 for x, y in zip(ca_, cb_) if x.get("sense") != y.get("sense"))
    frames = sum(
        1
        for x, y in zip(ca_, cb_)
        if "re_stepped" in x["frame"]
        and (x["frame"]["re_stepped"], x["frame"]["im_stepped"])
        != (y["frame"]["re_stepped"], y["frame"]["im_stepped"])
    )
    ca, cb = counts_of(ra), counts_of(rb)
    print(json.dumps({
        "a": a, "b": b,
        "nodes equal": ra["nodes"] == rb["nodes"],
        "log lengths": [len(ra["log"]), len(rb["log"])],
        "first parting": first,
        "credits": [len(credits_of(ra)), len(credits_of(rb))],
        "births": [len(births_of(ra)), len(births_of(rb))],
        "senses apart": senses,
        "frame stepped apart": frames,
        "counts a": ca, "counts b": cb,
        "refused a": {k: v for k, v in ca.items() if k.startswith("refused")},
        "refused b": {k: v for k, v in cb.items() if k.startswith("refused")},
    }))


def ends(a, b):
    out = []
    for path in (a, b):
        rec = load(path)
        for e in births_of(rec):
            if "takes" not in e:
                continue
            out.append({
                "record": path, "i": e["i"], "node": e["node"],
                "minus": e["minus"], "plus": e["plus"],
                "per end node": [t["node"] for t in e["takes"]],
                "per end dP": [t["dP_take"] for t in e["takes"]],
                "per end taken": [t["taken"] for t in e["takes"]],
                "per end booked": [t["booked"] for t in e["takes"]],
                "sum dP": [sum(x) for x in zip(*(t["dP_take"] for t in e["takes"]))],
                "taken": e["taken"], "booked": e["booked"],
            })
    for row in out:
        print(json.dumps(row))
    by_node = {}
    for row in out:
        key = (row["i"], tuple(row["node"]))
        by_node.setdefault(key, []).append(row)
    verdicts = Counter()
    for key, rows in sorted(by_node.items()):
        if len(rows) != 2:
            verdicts["alone"] += 1
            continue
        one, two = rows
        per = {tuple(n): d for n, d in zip(one["per end node"], one["per end dP"])}
        other = {tuple(n): d for n, d in zip(two["per end node"], two["per end dP"])}
        verdicts["per end equal" if per == other else "per end apart"] += 1
        verdicts["sum equal" if one["sum dP"] == two["sum dP"] else "sum apart"] += 1
    print(json.dumps({"mergers compared": len(by_node), "verdicts": dict(verdicts)}))


if __name__ == "__main__":
    {"frame": frame, "part": part, "ends": ends}[sys.argv[1]](*sys.argv[2:])

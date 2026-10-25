"""sl2: the born pair's Link read from a record of the flagged copy (the generic close logs every meeting of a row with a gap with its numbers): for every birth at interval i on the Link (minus, plus) of the row s, what the generic close did at that Link at i + 1 (the meeting's flow, twist, shares, W at the ends; the cause: not met / orientation / twist / sense / draw / lay / stop / merger) and at every later interval; the counts by cause; the mergers' Links against the births'; the charge at every birth and merger (W_children summing to 0); the run back; the bits.
Usage: python pair_links.py <record.json> [<out.json>]"""
import json
import sys

sys.set_int_max_str_digits(0)


def key(a, b):
    a, b = tuple(a), tuple(b)
    return (a, b) if a < b else (b, a)


def main(path, out_path=None):
    rec = json.load(open(path))
    log = rec["log"]
    births = [e for e in log if e["event"] == "birth" and not e.get("merger")]
    mergers = [e for e in log if e["event"] == "birth" and e.get("merger")]
    meetings = {}
    for e in log:
        if e["event"] == "meeting":
            meetings.setdefault((e["i"], e["row"], key(e["node"], e["link"])), e)
    refusals = {}
    for e in log:
        if e["event"] == "refused" and "link" in e and "row" in e:
            refusals[(e["i"], e["row"], key(e["node"], e["link"]))] = e["cause"]
    lays = {}
    stops = {}
    u0 = 3 * int(rec["T"]) * int(rec["den"])
    for e in log:
        if e["event"] == "refused" and e["cause"] == "lay" and "row" in e:
            lays.setdefault((e["i"], e["row"]), []).append(tuple(e["node"]))
        if e["event"] == "refused" and e["cause"] == "stop" and e.get("walls") == 2 * u0:
            stops.setdefault(e["i"], []).append(tuple(e["node"]))
    for (i, r, kk) in meetings:
        if (i, r, kk) in refusals:
            continue
        if any(n in kk for n in lays.get((i, r), [])):
            refusals[(i, r, kk)] = "lay"
        elif any(n in kk for n in stops.get(i, [])):
            refusals[(i, r, kk)] = "stop"
    merged_at = {}
    for e in mergers:
        merged_at[(e["i"], e["taken_row"], key(e["minus"], e["plus"]))] = e
    next_causes = {}
    later_causes = {}
    rows_next = []
    for b in births:
        k = key(b["minus"], b["plus"])
        s = b["line_pair"]
        i1 = b["i"] + 1
        m = meetings.get((i1, s, k))
        cause = "not met" if m is None else refusals.get((i1, s, k), "merger" if (i1, s, k) in merged_at else "taken?")
        next_causes[cause] = next_causes.get(cause, 0) + 1
        rows_next.append({"i": b["i"], "row": s, "link": [list(k[0]), list(k[1])], "W_children": b["W_children"], "next": cause, "meeting": None if m is None else {kk: m[kk] for kk in ("flow", "twist", "shares", "unit", "W_ends", "light_shares")}})
        for (i, r, kk), m2 in meetings.items():
            if r == s and kk == k and i > i1:
                c2 = refusals.get((i, r, kk), "merger" if (i, r, kk) in merged_at else "taken?")
                later_causes[c2] = later_causes.get(c2, 0) + 1
    causes_all = {}
    for (i, r, kk) in meetings:
        c = refusals.get((i, r, kk), "merger" if (i, r, kk) in merged_at else "taken?")
        causes_all[c] = causes_all.get(c, 0) + 1
    flows_zero = sum(1 for m in meetings.values() if m["flow"] == 0)
    twist_zero = sum(1 for m in meetings.values() if m["twist"] == 0)
    charge_births = sum(1 for b in births if sum(b["W_children"]) == 0)
    charge_mergers = sum(1 for e in mergers if sum(e["W_children"]) == 0)
    merger_links_born = sum(1 for e in mergers if any(key(b["minus"], b["plus"]) == key(e["minus"], e["plus"]) and b["line_pair"] == e["taken_row"] and b["i"] < e["i"] for b in births))
    found = {
        "record": path,
        "counts": rec["counts"],
        "run_back": rec["run_back"],
        "max bits": max(r["max bits"] for r in rec["rows"]),
        "max transient bits": max(r["max transient bits"] for r in rec["rows"]),
        "integers": rec["rows"][-1]["integers"],
        "births": len(births),
        "mergers": len(mergers),
        "mergers on a Link a birth laid earlier (the same row)": merger_links_born,
        "charge 0 at births / of": [charge_births, len(births)],
        "charge 0 at mergers / of": [charge_mergers, len(mergers)],
        "gapped meetings": len(meetings),
        "gapped meetings with flow 0": flows_zero,
        "gapped meetings with twist 0": twist_zero,
        "gapped meetings by cause": causes_all,
        "born pair's Link at i+1 by cause": next_causes,
        "born pair's Link at i+2 and later by cause": later_causes,
        "per birth": rows_next,
    }
    text = json.dumps(found, indent=1, default=str)
    if out_path:
        open(out_path, "w").write(text)
    found.pop("per birth")
    print(json.dumps(found, indent=1, default=str))
    for r in rows_next[:12]:
        print(json.dumps(r, default=str))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

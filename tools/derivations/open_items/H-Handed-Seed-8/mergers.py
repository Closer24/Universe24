"""cs5: the mergers and the per-bang gates read from the log alone: the births grouped by (the taken record, the children's record) per interval (a birth whose taken record is a row with a gap and whose children's record is the plane at the gap 0 is SL-S2's merger: two gapped quanta meeting give light); the refusals of the gapped records' meetings by cause (orientation, twist, stop, lay); the credits per record per bang window; the children's senses at one Node (the pair) counted.
Usage: python mergers.py <out.json> [cut1 cut2 ...] (the bangs cut at the named intervals)"""
import json
import sys

sys.set_int_max_str_digits(0)
rec = json.load(open(sys.argv[1]))
cuts = [int(x) for x in sys.argv[2:]]
log = rec["log"]
light = log[0]["line_pair"]
n = int(rec["intervals"])
edges = [0] + cuts + [n]
print(sys.argv[1], "the light's index", light, "records", len(rec["planes"]))
births = [e for e in log if e["event"] == "birth"]
by = {}
for e in births:
    k = (e.get("taken_row", light), e["line_pair"])
    by[k] = by.get(k, 0) + 1
print("births by (taken record -> children's record):", {f"{a}->{b}": v for (a, b), v in sorted(by.items())})
print("mergers (a gapped record taken, the light born):", sum(v for (a, b), v in by.items() if a != light and b == light))
for lo, hi in zip(edges, edges[1:]):
    inside = [e for e in log if lo < e["i"] <= hi]
    b = [e for e in inside if e["event"] == "birth"]
    c = [e for e in inside if e["event"] == "credit"]
    credits = {}
    for e in c:
        credits[e["line"]] = credits.get(e["line"], 0) + 1
    senses = {}
    for e in c:
        senses[(e["line"], e["sense"])] = senses.get((e["line"], e["sense"]), 0) + 1
    gapped = {}
    for e in inside:
        if e["event"] == "refused" and e.get("row", light) != light:
            k = (e["row"], e["cause"] + ("_crowd" if "children_at_one_node" in e else "_standing" if "standing" in e else "_control" if "control" in e else ""))
            gapped[k] = gapped.get(k, 0) + 1
    landing = [e for e in inside if e["event"] == "landing"]
    taken_rows = {}
    for e in landing:
        for k, v in e.get("taken_rows", {}).items():
            taken_rows[k] = taken_rows.get(k, 0) + v
    print(f"bang [{lo}, {hi}]: births {len(b)} at {sorted({e['i'] for e in b})[:6]} by children's record {json.dumps({str(k): v for k, v in sorted({e['line_pair']: 0 for e in b}.items())})}".replace("0}", "..}") if False else f"bang [{lo}, {hi}]: births {len(b)} at {sorted({e['i'] for e in b})[:6]}; credits {json.dumps({str(k): v for k, v in sorted(credits.items())})} by sense {json.dumps({f'{k[0]}:{k[1]}': v for k, v in sorted(senses.items())})}; the draws reaching the lay by taken record {json.dumps(taken_rows)}; the gapped records' meetings refused {json.dumps({f'{k[0]}:{k[1]}': v for k, v in sorted(gapped.items())})}")
    cred_i = sorted({e["i"] for e in c})
    print("   credit intervals (first 12):", cred_i[:12], "count", len(c), "Nodes credited", len({tuple(e["node"]) for e in c}))

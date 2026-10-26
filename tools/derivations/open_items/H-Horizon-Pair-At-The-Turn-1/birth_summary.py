"""hp1: the close's condition at the released Nodes, summed over birth_read.py's lines: at every interval where a Node stands released (turned at its frozen interval, unfrozen now), per record: does the Node stand (share >= unit), do its six neighbours stand, is any Link's current not 0, is any twist not 0; the counts and the first intervals. Usage: birth_summary.py <lines.jsonl> <from> <to>"""
import json, sys
lo, hi = int(sys.argv[2]), int(sys.argv[3])
tot = {"released_node_intervals": 0, "frozen_node_intervals": 0}
per_rec = {}
examples = []
cube = None
for l in open(sys.argv[1]):
    r = json.loads(l)
    if "nodes" not in r or not (lo <= r["i"] <= hi): continue
    by = {tuple(e["node"]): e for e in r["nodes"]}
    if cube is None: cube = max(max(k) for k in by) + 1
    for at, e in by.items():
        if not e["watched"]: continue
        tot["frozen_node_intervals" if e["frozen"] else "released_node_intervals"] += 1
        if not e["released"]: continue
        nbs = []
        for a in range(3):
            for s in (1, -1):
                m = list(at); m[a] = (m[a] + s) % max(cube, 5 if len(by) > 27 else 3); nbs.append(by.get(tuple(m)))
        for k in e["records"]:
            d = per_rec.setdefault(k["rec"], {"unit": k["unit"], "node_standing": 0, "node_share_max": 0, "neighbour_standing_links": 0, "both_standing_links": 0, "current_nonzero_at_node": 0, "twist_nonzero_at_node": 0, "neighbours_seen": 0, "charge_nonzero": 0})
            d["node_standing"] += k["standing"]; d["node_share_max"] = max(d["node_share_max"], k["share"])
            d["current_nonzero_at_node"] += any(x != 0 for x in k["current"]); d["twist_nonzero_at_node"] += any(x != 0 for x in k["twist"])
            d["charge_nonzero"] += (k["charge"] not in (None, 0))
            for nbx in nbs:
                if nbx is None: continue
                d["neighbours_seen"] += 1
                kn = nbx["records"][k["rec"]]
                d["neighbour_standing_links"] += kn["standing"]; d["both_standing_links"] += kn["standing"] and k["standing"]
        if len(examples) < 6:
            examples.append({"i": r["i"], "node": list(at), "content": e["content"], "X": e["X"], "records": [(k["rec"], k["share"] // k["unit"], k["standing"], [x != 0 for x in k["current"]], [x != 0 for x in k["twist"]]) for k in e["records"]], "neighbours_standing_rec_emitter": [None if n is None else n["records"][-1]["standing"] for n in nbs], "neighbours_content": [None if n is None else n["content"] for n in nbs]})
print(json.dumps({"range": [lo, hi], "totals": tot, "per_record_at_released_nodes": per_rec, "first_examples": examples}, indent=0))

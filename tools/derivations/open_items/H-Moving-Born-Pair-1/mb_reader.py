"""This hand's reader of a record (the log alone; integers only): the births by the children's shape; per birth the laid levels (the flag's `laid_levels`, else the rest lay by the amplitude), each child's W and the pair's sum, the lay's momentum dP_lay (0 predicted for every pair by the algebra), the recoil along the born Link and the velocity reading 1000 P div (2 E); the pair's survival past the next close (a merger whose two takes stand at the pair's ends on the same row: taken back at the delay d; surviving where none); the credits of the born row at the pair's ends and their neighbours after the birth (the track); against a second record (the head's), the first interval whose Node lines or log part.
Usage: python mb_reader.py <record.json> <out.json> [head <record.json>]"""
import json, sys

rec = json.load(open(sys.argv[1]))
_den = int(rec["den"]) if "den" in rec else int(rec["universe"]["integers"]["den"])
_all = rec["universe"]["rows"]
rows = [r for r in _all if int(r["shape"]) in (2, 8) and int(r["pair"][0]) != _den] + [r for r in _all if int(r["shape"]) == 2 and int(r["pair"][0]) == _den]  # the records in the acts' order (rows.order_key): the gapped planes and the quartets in the file's order, then the emitter
log = rec["log"]
births = [e for e in log if e["event"] == "birth" and "takes" not in e]
mergers = [e for e in log if e["event"] == "birth" and "takes" in e]
credits = [e for e in log if e["event"] == "credit"]
out = {"record": sys.argv[1], "counts": rec["counts"], "run_back": rec["run_back"], "births": len(births), "mergers": len(mergers), "credits": len(credits), "by_shape": {}, "pairs": []}
for b in births:
    s = b["line_pair"]
    shape = int(rows[s]["shape"])
    out["by_shape"][str(shape)] = out["by_shape"].get(str(shape), 0) + 1
    minus, plus = tuple(b["minus"]), tuple(b["plus"])
    axis = [a for a in range(3) if minus[a] != plus[a]][0]
    p = abs(int(b["dP_take"][axis]))
    e = int(b["booked"]) // 2
    taken_back = None
    for m in mergers:
        if m["i"] <= b["i"] or m["taken_row"] != s:
            continue
        ends = {tuple(t["node"]) for t in m["takes"]}
        if ends == {minus, plus}:
            taken_back = m["i"] - b["i"]
            break
    track = [c for c in credits if c["i"] > b["i"] and c.get("line_pair", c.get("row")) == s]
    out["pairs"].append({
        "i": b["i"], "row": s, "shape": shape, "axis": axis, "minus": list(minus), "plus": list(plus),
        "laid_levels": b.get("laid_levels"), "amplitude": b["amplitude"], "W_children": b["W_children"],
        "W_sum": sum(int(w) for w in b["W_children"]), "dP_lay": b["dP_lay"], "dP_take": b["dP_take"],
        "P_along": p, "E_child": e, "v_milli": (1000 * p) // (e + e) if e else None,
        "taken_back_delay": taken_back, "credits_of_row_after": len(track),
    })
pairs = out["pairs"]
for shape in sorted({p["shape"] for p in pairs}):
    ps = [p for p in pairs if p["shape"] == shape]
    out["survived_next_close shape " + str(shape)] = [sum(1 for p in ps if p["taken_back_delay"] is None), len(ps)]
    out["taken_back_at_delay_1 shape " + str(shape)] = [sum(1 for p in ps if p["taken_back_delay"] == 1), len(ps)]
    out["dP_lay_zero shape " + str(shape)] = [sum(1 for p in ps if all(int(x) == 0 for x in p["dP_lay"])), len(ps)]
    out["W_sum_zero shape " + str(shape)] = [sum(1 for p in ps if p["W_sum"] == 0), len(ps)]
    out["W_unit shape " + str(shape)] = sorted({abs(int(w)) for p in ps for w in p["W_children"]})
    out["laid_levels_distinct shape " + str(shape)] = sorted({json.dumps(p["laid_levels"]) for p in ps})[:6]
if "head" in sys.argv:
    head = json.load(open(sys.argv[sys.argv.index("head") + 1]))
    first = None
    for k, (a, b) in enumerate(zip(rec["nodes"], head["nodes"])):
        if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
            first = k
            break
    hb = [e for e in head["log"] if e["event"] == "birth"]
    out["head"] = {"record": sys.argv[sys.argv.index("head") + 1], "counts": head["counts"], "first_parting_node_line": first,
                   "births_head": len(hb), "births_flag": len(births) + len(mergers),
                   "first_parting_birth": next((i for i, (x, y) in enumerate(zip(log, head["log"])) if json.dumps(x, sort_keys=True) != json.dumps(y, sort_keys=True)), None)}
json.dump(out, open(sys.argv[2], "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "pairs"}))

"""a48b: the readings in the clicks of a record (run.py's out.json): the births, the charge (the senses' sum over the births' children and over the credits), every pair at opposite W, taken at or above booked on every birth and credit, the run back, the counts, the integers and bits. Usage: python a48b_clicks_read.py <out.json> [<out.json> ...]"""
import json
import sys

sys.set_int_max_str_digits(0)

for path in sys.argv[1:]:
    d = json.load(open(path))
    log = d["log"]
    births = [e for e in log if e["event"] == "birth"]
    credits = [e for e in log if e["event"] == "credit"]
    opposite = sum(1 for e in births if (e["W_children"][0] < 0 < e["W_children"][1]) or (e["W_children"][1] < 0 < e["W_children"][0]))
    charge_births = sum((1 if w > 0 else -1 if w < 0 else 0) for e in births for w in e["W_children"])
    charge_credits = sum(e["sense"] for e in credits)
    covered = sum(1 for e in births + credits if int(e["taken"]) >= int(e["booked"] if "booked" in e else 0))
    planes = {}
    for e in births:
        planes[e["line_pair"]] = planes.get(e["line_pair"], 0) + 1
    last = d["rows"][-1]
    print(json.dumps({
        "record": path.split("/")[-1], "intervals": d["intervals"], "births": len(births), "credits": len(credits),
        "charge over births (senses summed)": charge_births, "pairs at opposite W": [opposite, len(births)],
        "charge over credits": charge_credits, "taken >= booked (births)": [sum(1 for e in births if int(e["taken"]) >= int(e["booked"])), len(births)],
        "children per plane": planes, "turns": d["counts"]["turns"], "refused_stop": d["counts"]["refused_stop"],
        "run back": d["run_back"], "integers": last["integers"], "max bits": last["max bits"], "max transient bits": last["max transient bits"],
    }))

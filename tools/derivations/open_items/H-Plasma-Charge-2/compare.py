"""pl2: two records of event_universe.run compared: the counts, the turns, the run back, the Node lines (X per interval) equal or the first interval apart, the log's births and credits (count, and bit for bit as JSON), the bits. Usage: compare.py <a.json> <b.json>"""
import json, sys
sys.set_int_max_str_digits(0)
a, b = (json.load(open(p)) for p in sys.argv[1:3])
def events(r, kind):
    return [e for e in r["log"] if e["event"] == kind]
first_x = next((l["i"] for l, m in zip(a["nodes"], b["nodes"]) if l["X"] != m["X"]), None)
strip = lambda e: {k: v for k, v in e.items() if k not in ("arrivals", "laid_back")}
out = {
    "a": sys.argv[1], "b": sys.argv[2],
    "counts a": a["counts"], "counts b": b["counts"], "counts equal": a["counts"] == b["counts"],
    "turns equal": a["turns"] == b["turns"], "turns a": a["turns"][:6], "turns b": b["turns"][:6],
    "X lines equal at every interval": first_x is None, "first interval X apart": first_x,
    "births a/b": [len(events(a, "birth")), len(events(b, "birth"))], "credits a/b": [len(events(a, "credit")), len(events(b, "credit"))],
    "credits laid back a/b": [sum(1 for e in events(a, "credit") if "laid_back" in e), sum(1 for e in events(b, "credit") if "laid_back" in e)],
    "log bit for bit (the readers' fields arrivals and laid_back aside)": [strip(e) for e in a["log"]] == [strip(e) for e in b["log"]],
    "run back a/b": [a["run_back"], b["run_back"]],
    "max bits a/b": [max(int(r["max bits"]) for r in a["rows"]), max(int(r["max bits"]) for r in b["rows"])],
    "mean X at the last interval a/b": [sum(a["nodes"][-1]["X"]) // len(a["nodes"][-1]["X"]), sum(b["nodes"][-1]["X"]) // len(b["nodes"][-1]["X"])],
}
print(json.dumps(out, indent=1))

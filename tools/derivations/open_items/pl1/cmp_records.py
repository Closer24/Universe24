"""Two engine records compared: the Node lines, the log, the counts and the run back equal or not; where not, the counts side by side and the first interval whose Node line differs. Usage: cmp_records.py <a.json> <b.json>"""
import json
import sys

sys.set_int_max_str_digits(0)
a = json.load(open(sys.argv[1], encoding="utf-8"))
b = json.load(open(sys.argv[2], encoding="utf-8"))
same_nodes = a["nodes"] == b["nodes"]
first = next((k for k, (x, y) in enumerate(zip(a["nodes"], b["nodes"])) if x != y), None)
print(json.dumps({
    "a": sys.argv[1], "b": sys.argv[2],
    "node lines equal": same_nodes, "first interval differing": None if first is None else a["nodes"][first]["i"],
    "log equal": a["log"] == b["log"], "counts equal": a["counts"] == b["counts"],
    "counts a": a["counts"], "counts b": b["counts"],
    "run back a": a["run_back"], "run back b": b["run_back"],
    "max bits a / b": [max(int(r["max bits"]) for r in a["rows"]), max(int(r["max bits"]) for r in b["rows"])],
    "integers a / b": [a["rows"][-1]["integers"], b["rows"][-1]["integers"]],
    "sign level max at the end a / b": [a["rows"][-1]["sign level max"], b["rows"][-1]["sign level max"]],
    "W total at the end a / b": [a["rows"][-1]["W total"], b["rows"][-1]["W total"]],
    "volume mean at the end a / b": [a["rows"][-1]["volume mean"], b["rows"][-1]["volume mean"]],
}, indent=1))

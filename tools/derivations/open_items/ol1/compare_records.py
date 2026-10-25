"""ol1: two engine records compared: the counts, the run back, the Node lines interval by interval (the first interval apart), the log's length and the first entry apart (the keys laid_back / arrivals aside). Usage: compare_records.py <a.json> <b.json>"""
import json, sys
sys.set_int_max_str_digits(0)
a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
first_node = next((i for i, (x, y) in enumerate(zip(a["nodes"], b["nodes"])) if x != y), None)
first_log = next((i for i, (x, y) in enumerate(zip(a["log"], b["log"])) if x != y), None)
def births(r): return sum(1 for e in r["log"] if e["event"] == "birth")
def credits(r): return sum(1 for e in r["log"] if e["event"] == "credit")
def laid(r): return sum(1 for e in r["log"] if e["event"] == "credit" and "laid_back" in e)
print(json.dumps({"a": sys.argv[1], "b": sys.argv[2],
  "a counts": {"births": births(a), "credits": credits(a), "laid back": laid(a), "turns": a["counts"]["turns"], "refused_stop": a["counts"]["refused_stop"], "run back": a["run_back"]},
  "b counts": {"births": births(b), "credits": credits(b), "laid back": laid(b), "turns": b["counts"]["turns"], "refused_stop": b["counts"]["refused_stop"], "run back": b["run_back"]},
  "node lines equal": first_node is None and len(a["nodes"]) == len(b["nodes"]), "first interval apart (node lines, 1-based)": None if first_node is None else first_node + 1,
  "log equal": first_log is None and len(a["log"]) == len(b["log"]), "log lengths": [len(a["log"]), len(b["log"])], "first log entry apart": first_log,
  "bits": [max(r["bits"] for r in a["rows"]) if a["rows"] and "bits" in a["rows"][0] else None, max(r["bits"] for r in b["rows"]) if b["rows"] and "bits" in b["rows"][0] else None]}))

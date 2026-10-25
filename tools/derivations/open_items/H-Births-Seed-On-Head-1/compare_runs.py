"""rg1: two records of event_universe.run compared: the counts (births, body_clicks, laid_back, turns, the refusals), the Node rows at the end (the `nodes` field) and the run back; the log's events counted by kind. Usage: python compare_runs.py a.json b.json"""
import json
import sys

sys.set_int_max_str_digits(0)
a, b = (json.load(open(p)) for p in sys.argv[1:3])
ka = sorted(a)
counts_a = {k: str(v) for k, v in a.get("counts", {}).items()}
counts_b = {k: str(v) for k, v in b.get("counts", {}).items()}
apart = {k: (counts_a.get(k), counts_b.get(k)) for k in set(counts_a) | set(counts_b) if counts_a.get(k) != counts_b.get(k)}
same_nodes = a.get("nodes") == b.get("nodes")
same_rows = a.get("rows") == b.get("rows")
def kinds(r):
    found = {}
    for e in r.get("log", []):
        found[e.get("event")] = found.get(e.get("event"), 0) + 1
    return found
print(sys.argv[1].split("/")[-1], "against", sys.argv[2].split("/")[-1], "| keys", ka[:12], "| nodes equal", same_nodes, "| rows equal", same_rows, "| counts apart", apart if apart else "none (equal)", "| births / credits / laid back", counts_a.get("births"), counts_a.get("body_clicks"), counts_a.get("laid_back"), "against", counts_b.get("births"), counts_b.get("body_clicks"), counts_b.get("laid_back"), "| run back", a.get("run_back"), b.get("run_back"), "| log kinds", kinds(a), kinds(b))

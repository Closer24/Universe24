"""The credits of a writer's record: the count, the levels taken, the laid back, the credits at Nodes where the light's current is 0 on every Link cannot be read here (the record carries the current per axis from the Node: read it), the refusals by cause, the run back, the bits."""
import json, sys
sys.set_int_max_str_digits(0)
rec = json.load(open(sys.argv[1]))
log = rec["log"]
credits = [e for e in log if e["event"] == "credit"]
births = [e for e in log if e["event"] == "birth"]
refused = {}
for e in log:
    if e["event"] == "refused":
        refused[e["cause"]] = refused.get(e["cause"], 0) + 1
print(json.dumps({
    "credits": len(credits), "births": len(births),
    "levels taken": sum(int(c["levels"]) for c in credits),
    "laid back": sum(int(c.get("laid_back", 0)) for c in credits),
    "credits by line": {str(k): sum(1 for c in credits if c["line"] == k) for k in sorted(set(c["line"] for c in credits))},
    "credits at turned Nodes": sum(1 for c in credits if c.get("turned")),
    "senses summed over the credits": sum(int(c["sense"]) for c in credits),
    "children W": sorted(set(w for b in births for w in b["W_children"])),
    "taken >= booked at every birth": all(int(b["taken"]) >= int(b["booked"]) for b in births),
    "refused": refused, "counts": rec["counts"], "run back": rec["run_back"],
    "max bits": max(r["max bits"] for r in rec["rows"]), "integers": rec["rows"][-1]["integers"],
    "first credit interval": min((c["i"] for c in credits), default=None),
}))

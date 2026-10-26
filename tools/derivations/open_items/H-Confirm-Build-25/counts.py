"""A record's marks: the run back, the counts dict, the births, the credits, the refusals by cause, and the merger events of the log (the event names counted), integers only."""
import json, sys, collections
for p in sys.argv[1:]:
    d = json.load(open(p), parse_float=lambda s: (_ for _ in ()).throw(ValueError("float " + s)))
    log = d.get("log", [])
    kinds = collections.Counter(e.get("event", "?") for e in log if isinstance(e, dict))
    rb = d.get("run_back")
    print(p.split("/")[-1], "run_back", json.dumps(rb)[:120])
    print("   counts", json.dumps(d.get("counts", {}))[:300])
    print("   log events", len(log), dict(sorted(kinds.items(), key=lambda kv: -kv[1])))

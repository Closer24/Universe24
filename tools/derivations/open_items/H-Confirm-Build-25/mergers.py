"""The mergers of a record: a birth whose log entry carries `takes` (the two takers of a merger, the exact lay at -1), counted against the births; a record given as a path or as sha:path of this tree."""
import json, subprocess, sys
def load(a):
    if ":" in a and not a.startswith("/"):
        sha, path = a.split(":", 1)
        return json.loads(subprocess.run(["git", "show", sha + ":" + path], capture_output=True, text=True).stdout)
    return json.load(open(a))
for a in sys.argv[1:]:
    d = load(a)
    births = [e for e in d["log"] if e.get("event") == "birth"]
    mergers = [e for e in births if e.get("takes")]
    print(a, "births", len(births), "mergers", len(mergers), "merger intervals", [e.get("i") for e in mergers][:20])

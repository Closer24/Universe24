"""Two records compared from their own files: the counts, the first parting interval of the log, the
merger takes' per-end bookings and their sum, the credits' senses. Imports nothing of the engine."""
import json
import sys


def load(path):
    with open(path) as handle:
        return json.load(handle)


def mergers(log):
    found = []
    for e in log:
        if e.get("event") == "birth" and "takes" in e:
            found.append({
                "i": e["i"], "ends": [t["node"] for t in e["takes"]],
                "dP_take": [t["dP_take"] for t in e["takes"]],
                "sum": [sum(t["dP_take"][a] for t in e["takes"]) for a in range(3)],
                "taken": [t["taken"] for t in e["takes"]],
                "dP_lay_ends": e.get("dP_lay_ends"),
            })
    return found


def first_apart(a, b):
    for k, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return {"log line": k, "interval": [x.get("i"), y.get("i")],
                    "event": [x.get("event"), y.get("event")]}
    return {"log lines": [len(a), len(b)], "equal to the shorter": True} if len(a) != len(b) else None


left, right = load(sys.argv[1]), load(sys.argv[2])
print(json.dumps({
    "left": sys.argv[1].split("/")[-1], "right": sys.argv[2].split("/")[-1],
    "counts left": left["counts"], "counts right": right["counts"],
    "run back": [left.get("run_back"), right.get("run_back")],
    "nodes equal": left.get("nodes") == right.get("nodes"),
    "log lengths": [len(left["log"]), len(right["log"])],
    "first apart": first_apart(left["log"], right["log"]),
    "mergers left": mergers(left["log"]), "mergers right": mergers(right["log"]),
}, indent=1))

"""cs6: the second bang read on a letter record: the first bang's close (births, crowd), the first bottom of the mean, the first interval not uniform, the births per interval after the first bang, and the draws per class at every landing with a birth after the first bang (which class drew which record). Usage: python sv_read.py <record.json> ..."""
import json, sys
sys.set_int_max_str_digits(0)
for p in sys.argv[1:]:
    r = json.load(open(p))
    diag = [d for d in r["diag"] if d["i"] >= 1]
    means = [d["X_mean"] for d in diag]
    n = len(diag)
    log = r["log"]
    light = log[0]["line_pair"] if log and log[0]["event"] == "lay_pattern" else None
    births = {}
    for e in log:
        if e["event"] == "birth":
            births[e["i"]] = births.get(e["i"], 0) + 1
    first = min(births) if births else None
    landing = {e["i"]: e for e in log if e["event"] == "landing"}
    bottoms = [(diag[k]["i"], means[k], diag[k]["X_min"], diag[k]["X_max"]) for k in range(1, n - 1) if means[k] <= means[k - 1] and means[k] < means[k + 1]]
    tops = [(diag[k]["i"], means[k], diag[k + 1]["turned"]) for k in range(1, n - 1) if means[k] >= means[k - 1] and means[k] > means[k + 1]]
    split = next((d["i"] for d in diag if d["X_min"] != d["X_max"]), None)
    later = [(i, c) for i, c in sorted(births.items()) if first is not None and i > first + 5]
    draws = []
    for i, c in later[:3]:
        e = landing.get(i)
        if e:
            draws.append((i, c, e["nodes_crowded"], {k: sorted(v) for k, v in sorted(e["draws_per_class"].items())}))
    print(p.split("/")[-1], "light", light, "| first bang:", first, births.get(first), "crowd", landing[first]["nodes_crowded"] if first in landing else None, "| tops", tops[:3], "| bottoms", bottoms[:2], "| split at", split, "| later births", later[:6], "| draws at the later births", json.dumps(draws)[:400])

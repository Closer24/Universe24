"""cs7: two engine records compared on the state (every Node row at every interval, the run's rows, the counts) and on the log (the credits' count and the count laid back, the births); the clicks where the net reading fired listed by interval. Usage: python compare_three.py a.json b.json"""
import json, sys
sys.set_int_max_str_digits(0)
a, b = (json.load(open(p)) for p in sys.argv[1:3])
def strip(log):
    return [{k: v for k, v in e.items() if k not in ("taken_line", "arrivals", "laid_back")} for e in log]
ca = [e for e in a["log"] if e["event"] == "credit"]
cb = [e for e in b["log"] if e["event"] == "credit"]
print(sys.argv[1].split("/")[-1], "against", sys.argv[2].split("/")[-1], "| nodes equal", a["nodes"] == b["nodes"], "rows equal", a["rows"] == b["rows"], "counts equal", {k: a["counts"][k] for k in a["counts"]} == {k: b["counts"][k] for k in a["counts"]}, "log equal (the added keys apart)", strip(a["log"]) == strip(b["log"]), "| births", a["counts"]["births"], b["counts"]["births"], "credits", len(ca), len(cb), "laid back", sum(1 for e in cb if "laid_back" in e), "| laid back at", sorted({e["i"] for e in cb if "laid_back" in e})[:12], "| run back", a["run_back"], b["run_back"])

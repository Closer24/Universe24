"""One line set per record: the fields of read_record that the comparison needs; gates 1 / 46 / 8 / 7 / 40 verdicts where asked."""
import json
import subprocess
import sys

KEYS = ("counts", "run_back", "max bits", "integers", "alike (spread 0) of intervals", "tops (every Node turning at once)", "bottoms (interval, mean X, at Gamma at every Node)", "credits", "credits laid back", "credit intervals (first 12: interval, count, levels->count)", "credit intervals in all", "stop refusals (intervals, count)", "arrival refusals (intervals, count)", "credits per cycle (lo, hi, credits, levels summed)", "X at the bottoms and the intervals around (i, mean)", "retrace")
for path in sys.argv[1:]:
    with_gates = "--gates" in sys.argv
    if path == "--gates":
        continue
    out = subprocess.run([sys.executable, "read_record.py", path] + (["--gates"] if with_gates else []), capture_output=True, text=True)
    if out.returncode:
        print(path, "FAILED", out.stderr[-800:])
        continue
    d = json.loads(out.stdout)
    print("=====", path)
    for k in KEYS:
        print(k, "=", json.dumps(d[k]))
    if with_gates:
        for k, v in d["gates"].items():
            print("gate", k, "=", v.get("verdict"), "|", json.dumps({kk: vv for kk, vv in v.items() if kk != "verdict"})[:400])

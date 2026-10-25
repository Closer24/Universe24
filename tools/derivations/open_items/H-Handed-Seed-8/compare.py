"""cs6: two records compared on the state: every diag line (the log's key taken_line apart), every count, every Node row. Usage: python compare.py a.json b.json"""
import json, sys
sys.set_int_max_str_digits(0)
a, b = (json.load(open(p)) for p in sys.argv[1:3])
same_diag = a["diag"] == b["diag"]
same_nodes = a["nodes"] == b["nodes"]
same_counts = a["counts"] == b["counts"]
def strip(log):
    return [{k: v for k, v in e.items() if k != "taken_line"} for e in log]
same_log = strip(a["log"]) == strip(b["log"])
print("diag equal", same_diag, "nodes equal", same_nodes, "counts equal", same_counts, "log equal (taken_line apart)", same_log, "run back", a["run_back"], b["run_back"])

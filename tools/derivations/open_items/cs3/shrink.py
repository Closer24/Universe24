"""cs3: the records above the size limit kept slim: every Node line reduced to its interval, X and the turned Nodes, and on the four largest the refused log lines dropped too (the decoder's gates were read before on the whole record: out/*_gates.jsonl). Usage: python shrink.py <out.json> ..."""
import json
import os
import sys

sys.set_int_max_str_digits(0)
for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    d["nodes"] = [{"i": n["i"], "X": n["X"], "turned": n["turned"]} for n in d["nodes"]]
    d["slim"] = "the Node lines reduced to i, X, turned (shrink.py)"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f)
    print(path, os.path.getsize(path))

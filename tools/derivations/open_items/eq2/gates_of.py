"""The gates' verdicts of several records side by side (the engine's table), for the rows named. Usage: gates_of.py <record.json>... """
import json
import sys

from event_universe import gates as table

sys.set_int_max_str_digits(0)
ROWS = ("1 ", "4 ", "7 ", "8 ", "9 ", "10 ", "11 ", "16 ", "18 ", "22 ", "40 ", "45 ", "46 ", "47 ")
for path in sys.argv[1:]:
    run = json.load(open(path, encoding="utf-8"))
    g = table.gates(run)
    print("=====", path, "counts", {k: run["counts"][k] for k in ("births", "body_clicks", "refused_stop", "turns", "laid")}, "laid_back", run["counts"].get("laid_back"), "run back", run["run_back"])
    for k, v in g.items():
        if k.startswith(ROWS) and isinstance(v, dict) and "verdict" in v:
            print("  ", k, "=", v["verdict"][:160])

"""Run one world to N intervals with a run back on a named src; write the record. Usage: run_record.py <src> <world.json> <intervals> <back> <out.json>"""
import json
import sys

sys.path.insert(0, sys.argv[1])
sys.set_int_max_str_digits(0)
from event_universe.run import record  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402

u, w = load_world(sys.argv[2])
w = dict(w, intervals=int(sys.argv[3]))
found = record(u, w, int(sys.argv[4]), lambda line: None)
with open(sys.argv[5], "w", encoding="utf-8") as out:
    json.dump(found, out)

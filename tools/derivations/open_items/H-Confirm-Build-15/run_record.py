"""The writer's record of a world at a given count of intervals and run back: world file, intervals, back, out file."""
import json, sys
from event_universe.loader.world import load_world
from event_universe import run
sys.set_int_max_str_digits(0)
universe, world = load_world(sys.argv[1])
world = dict(world, intervals=int(sys.argv[2]))
found = run.record(universe, world, int(sys.argv[3]), lambda line: print(line, flush=True))
with open(sys.argv[4], "w", encoding="utf-8") as out:
    json.dump(found, out)

"""pm1's runner over the flagged copy: the engine's writer (run.record) with the world file's key `pm1_weight` popped and set as
readings.WEIGHT (absent: "default", David's path bit for bit). Usage: python pm1_run.py <world.json> <out.json> [back N]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'src_pm1'))
from event_universe import readings, run
from event_universe.loader.world import read_world

sys.set_int_max_str_digits(0)
where = sys.argv[1]
world = json.loads(open(where).read())
readings.WEIGHT = world.pop('pm1_weight', 'default')
universe = json.loads(open(os.path.join(os.path.dirname(where), world['universe'])).read())
read_world(world, universe)
back = int(sys.argv[sys.argv.index('back') + 1]) if 'back' in sys.argv else 0
print(json.dumps({'pm1_weight': readings.WEIGHT}), flush=True)
found = run.record(universe, world, back, lambda line: print(line, flush=True))
found['pm1_weight'] = readings.WEIGHT
with open(sys.argv[2], 'w') as out:
    json.dump(found, out)

"""The lean toy's former loop: one interval forward and one back on the quartet world (the call self.swap(held, None, -1, top) against Node.swap's signature)."""
import json, sys, traceback
sys.path.insert(0, sys.argv[1] + "/tools/derivations/toys/lean")
import toy as TOY
universe = json.load(open(sys.argv[1] + "/tests/worlds/universe_quartet.json"))
world = json.load(open(sys.argv[1] + "/tests/worlds/world_quartet.json"))
t = TOY.Toy(universe, dict(world, control={}))
t.step()
try:
    t.step(-1)
    print("the toy back holds interval", t.interval)
except Exception as e:
    traceback.print_exc()
    print("the toy back fails:", type(e).__name__, e)

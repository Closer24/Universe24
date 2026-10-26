"""The lean toy's run back on the quartet world (the 5-cube's middle universe) under no key and under each digit key: N intervals forward with the state hashed, N back, the hashes compared; and the toy's hooks read: close.read_number after the run."""
import json, sys, traceback
W = sys.argv[1]; N = int(sys.argv[2])
sys.path.insert(0, W + "/tools/derivations/toys/lean")
import toy as TOY
from event_universe import close, draw
universe = json.load(open(W + "/tests/worlds/universe_quartet.json"))
world = json.load(open(W + "/tests/worlds/world_quartet.json"))
for control in ({}, {"digits": "folded"}, {"digits": "former"}):
    t = TOY.Toy(universe, dict(world, control=control))
    hashes = []
    try:
        for _ in range(N):
            hashes.append(t.state_hash()); t.step()
        exact = 0
        for h in reversed(hashes):
            t.step(-1); exact += t.state_hash() == h
        print("control", control, "run back exact", exact, "of", N, "births", t.counts["births"], "clicks", t.counts["body_clicks"], "close.read_number after the run:", close.read_number.__name__, "draw's:", draw.read_number.__name__)
    except Exception as e:
        traceback.print_exc(); print("control", control, "FAILS", type(e).__name__, e)

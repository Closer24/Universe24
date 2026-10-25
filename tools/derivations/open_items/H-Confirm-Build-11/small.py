"""vf11 (item 5): the two test boards whose counts moved, run per interval at one src: the chiral seed on the 3-cube at 30 (SL-S1's board) and the horizon's fed Node (test_the_node.fed_horizon's board, the same lay by hand); the state hash and the births' intervals per interval, for the two shas to be compared."""
import hashlib
import json
import sys

sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402

WORLDS = sys.argv[1]
out = {}


def course(node, n):
    hashes, charge_nonzero = [], []
    for _ in range(n):
        node.step()
        hashes.append(hashlib.sha256(node.state_bytes()).hexdigest()[:16])
        gapped_levels = sum(int(abs(int(x))) for r in node.gapped for line in r.lines for x in line.now.reshape(-1))
        charge_nonzero.append(gapped_levels != 0)
    births = sorted(int(e["i"]) for e in node.log if e["event"] == "birth")
    return {"hashes": hashes, "births": births, "counts": {k: int(v) for k, v in node.counts.items()},
            "first_gapped_levels_at": next((i + 1 for i, c in enumerate(charge_nonzero) if c), None)}


universe, world = load_world(f"{WORLDS}/world_chiral.json")
lays = [lay for lay in world["seed"] if lay.get("lay") != "at" or all(x < 3 for x in lay["centre"])]
out["chiral_3cube_30"] = course(Node(universe, dict(world, shape=[3, 3, 3], intervals=30, seed=lays)), 30)
exec(open(sys.argv[3]).read())  # the fed_horizon lay, copied from the test by hand into fed.py
universe, world = load_world(f"{WORLDS}/world_node.json")
node = fed_horizon(Node(universe, world), (1, 1, 1))  # noqa: F821
out["horizon_fed_20"] = course(node, 20)
json.dump(out, open(sys.argv[2], "w"))
print({k: (v["births"], v["first_gapped_levels_at"], v["counts"]["births"], v["counts"]["body_clicks"]) for k, v in out.items()})

"""a483's test (under 15 s): (1) the 48 on the clicks, the x reflection of the chiral 3-cube to 60 against the base: the state carried through the image parts in two scalar levels at the interval 5 (the walled row's level at one Node, -1 against +1 with the remainder 0 at the wall 2, and the emitter's re line at one Node) before the first parting draw (6) and before the clicks part (the image births 2 by 12 against the base's 3, apart from 11); (2) the cycle seed from the file at the first close (tests/worlds/world_ga2.json, 2 intervals): the births at 2 and the Nodes they stand at, read from the src named by A483_SRC (the head's src by default: 0 births, 64 reads refused as the origin). Run: PYTHONPATH=<src> python tests_a483.py from the worktree root, or pytest -q tests_a483.py."""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.environ.get("A483_SRC", os.path.join(ROOT, "src")))
sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402

FLAG = os.environ.get("A483_READ", "")


def chiral_3cube(n):
    universe, world = load_world(os.path.join(HERE, "worlds", "world_chiral_3_30.json"))
    return universe, dict(world, intervals=n)


def reflected(world):
    found = dict(world, seed=[dict(lay) for lay in world["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = [(-lay[key][0]) % 3, lay[key][1], lay[key][2]]
    return found


def test_the_reflected_state_parts_at_5_before_the_clicks_part_at_11():
    universe, world = chiral_3cube(12)
    base, img = Node(universe, world), Node(universe, reflected(world))
    walled, emitter_re = base.all_lines()[0], base.records().index(base.emitter())
    first_level, first_birth_apart = None, None
    for t in range(12):
        base.step()
        img.step()
        bad = 0
        for x in np.ndindex(3, 3, 3):
            gx = ((-x[0]) % 3, x[1], x[2])
            bad += int(walled.now[x]) != int(img.all_lines()[0].now[gx])
        if bad and first_level is None:
            first_level = base.interval
        if base.counts["births"] != img.counts["births"] and first_birth_apart is None:
            first_birth_apart = base.interval
    if not FLAG:
        assert first_level == 5, first_level
        assert first_birth_apart == 11, first_birth_apart
        assert (base.counts["births"], img.counts["births"]) == (3, 2)
    print(json.dumps({"flag": FLAG, "first_parting_level_interval": first_level, "first_birth_apart": first_birth_apart, "births": [base.counts["births"], img.counts["births"]]}))


def test_the_cycle_seed_at_the_first_close():
    universe, world = load_world(os.path.join(ROOT, "tests", "worlds", "world_ga2.json"))
    node = Node(universe, dict(world, intervals=2))
    for _ in range(2):
        node.step()
    births = [e for e in node.log if e["event"] == "birth" and e["i"] == 2]
    nodes = {tuple(e["node"]) for e in births}
    found = {"flag": FLAG, "births_at_2": len(births), "nodes_at_2": len(nodes), "refused_origin": int(node.counts["refused_origin"]), "children": sorted({e["line_pair"] for e in births})}
    if not FLAG:
        assert found["births_at_2"] == 0 and found["refused_origin"] == 64, found
    else:
        assert found["births_at_2"] in (0, 32), found
    print(json.dumps(found))


if __name__ == "__main__":
    t0 = time.time()
    test_the_reflected_state_parts_at_5_before_the_clicks_part_at_11()
    test_the_cycle_seed_at_the_first_close()
    print(json.dumps({"seconds": round(time.time() - t0, 1)}))

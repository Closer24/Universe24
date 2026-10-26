"""a484's one test (under 15 s): the 48 on the clicks of the chiral 3-cube to 60 under one rotation (EQUAL) and one reflection (CONJUGATE: the children's Nodes exchanged, the credits' senses negated), and the cycle seed ga2 (tests/worlds/world_ga2.json) birthing at 64 of 64 Nodes at the interval 2. The law as the owner states it; the integers printed where it is unmet. Run: PYTHONPATH=<src> python -m pytest tests_a484.py -q (A484_READ=1 for the flagged copy)."""
import os
import sys

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
import event_universe  # noqa: E402

print("event_universe read from", event_universe.__file__)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..", "..")
N = 60
ROTATION = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
REFLECTION = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])


def chiral_world():
    universe, world = load_world(os.path.join(ROOT, "tests", "worlds", "world_node.json"))
    lays = [{"lay": "sea", "row": 0}, {"lay": "hole", "at": [0, 0, 0]}]
    lays += [{"lay": "at", "row": 0, "centre": c, "quanta": 1} for c in ([1, 0, 0], [0, 2, 1], [2, 1, 0])]
    return universe, dict(world, shape=[3, 3, 3], intervals=N, seed=lays)


def image(m, node, cube):
    return tuple(int(x) % cube for x in m @ np.array(node, dtype=int))


def world_image(w, m, cube):
    found = dict(w, seed=[dict(lay) for lay in w["seed"]])
    for lay in found["seed"]:
        for key in ("at", "centre"):
            if key in lay:
                lay[key] = list(image(m, lay[key], cube))
    return found


def run(universe, w, n):
    node = Node(universe, w)
    for _ in range(n):
        node.step()
    return node.log


def clicks(log, m, cube, conj):
    births = sorted((e["i"], image(m, e["node"], cube), e["line_pair"]) + ((image(m, e["plus"], cube), image(m, e["minus"], cube)) if conj else (image(m, e["minus"], cube), image(m, e["plus"], cube))) for e in log if e["event"] == "birth")
    credits = sorted((e["i"], image(m, e["node"], cube), e["line"], -e["sense"] if conj else e["sense"], e["beat"]) for e in log if e["event"] == "credit")
    return births, credits


def first_apart(a, b):
    apart = sorted(set(a[0]) ^ set(b[0]) | set(a[1]) ^ set(b[1]), key=lambda x: x[0])
    return apart[0][0] if apart else None


def test_48_on_the_clicks_to_60():
    universe, world = chiral_world()
    base = run(universe, world, N)
    eye = np.eye(3, dtype=int)
    rot = clicks(run(universe, world_image(world, ROTATION, 3), N), eye, 3, False)
    refl = clicks(run(universe, world_image(world, REFLECTION, 3), N), eye, 3, False)
    want_rot = clicks(base, ROTATION, 3, False)
    want_refl = clicks(base, REFLECTION, 3, True)
    i_rot, i_refl = first_apart(rot, want_rot), first_apart(refl, want_refl)
    assert i_rot is None, f"the rotation parts at the interval {i_rot}"
    assert i_refl is None, f"the reflection's conjugate parts at the interval {i_refl}"


def test_cycle_seed_births_at_2():
    universe, world = load_world(os.path.join(ROOT, "tests", "worlds", "world_ga2.json"))
    log = run(universe, dict(world, intervals=3), 3)
    at_2 = {tuple(e["node"]) for e in log if e["event"] == "birth" and e["i"] == 2}
    refused = sorted({e["cause"] for e in log if e["event"] == "refused" and e["i"] == 2})
    assert len(at_2) == 64, f"births at 64 of 64 Nodes wanted at the interval 2; {len(at_2)} found, the refusals by name {refused}"

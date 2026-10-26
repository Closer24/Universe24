"""H-Birth-On-Six-Links-2: three tests on the flagged copy (SL2_FORM=1; PYTHONPATH the copy's src): the integer solver on the six-by-twelve system returns an exact small solution or the remainder; the six-Link lay closes the click's momentum and its moment about the taker's Node exactly wherever it reports closed, on the hole to 12; the run back undoes the six lays exactly (the state hash)."""
import os
import random
import sys

sys.set_int_max_str_digits(0)
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("SL2_SRC", "/dev/shm/tmp/sl2/src_sl2")
sys.path.insert(0, SRC)
os.environ["SL2_FORM"] = "1"
WORLD = os.path.join(HERE, "..", "..", "..", "..", "tests", "worlds", "world_hole.json")


def test_solver_exact_and_small():
    from event_universe.six import solve
    rng = random.Random(7)
    for _ in range(6):
        a = [[rng.randrange(-10**6, 10**6) for _ in range(12)] for _ in range(6)]
        x0 = [rng.randrange(-50, 50) for _ in range(12)]
        t = [sum(a[r][c] * x0[c] for c in range(12)) for r in range(6)]
        x, rem = solve(a, t)
        assert x is not None and rem == [0] * 6
        assert [sum(a[r][c] * x[c] for c in range(12)) for r in range(6)] == t
        assert max(abs(v) for v in x) < 10**4
    x, rem = solve([[2, 4, 6, 8, 10, 12, 2, 4, 6, 8, 10, 12]] + [[0] * 12] * 5, [3, 0, 0, 0, 0, 0])
    assert x is None and rem[0] != 0


_CACHE = {}


def _run(n):
    if n in _CACHE:
        return _CACHE[n]
    from event_universe.loader.world import load_world
    from event_universe.node import Node
    u, w = load_world(WORLD)
    node = Node(u, dict(w, intervals=n))
    hashes = []
    for _ in range(n):
        node.step()
        hashes.append(node.state_hash())
    _CACHE[n] = (node, hashes)
    return node, hashes


def test_six_lay_closes_momentum_and_moment():
    node, _ = _run(12)
    six = [e for e in node.log if e["event"] == "six"]
    assert six
    closed = [e for e in six if e.get("closed")]
    assert closed
    for e in closed:
        assert e["P_laid"] == [-(a + b) for a, b in zip(e["dP_take"], e["dP_children"], strict=True)]
        assert e["torque_laid"] == [-v for v in e["torque_children"]]
        assert max(abs(v) for l_ in e["lays"] for v in l_) < 10**6
    for e in six:
        if not e.get("closed"):
            assert e["lays"] == [] and any(e["remainder"])


def test_run_back_exact():
    node, hashes = _run(12)
    for k in range(3):
        node.run(-1)
        assert node.state_hash() == hashes[len(hashes) - 2 - k]

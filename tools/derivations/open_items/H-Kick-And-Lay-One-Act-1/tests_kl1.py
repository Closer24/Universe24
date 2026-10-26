"""H-Kick-And-Lay-One-Act-1: the kick's inverse at the six far ends is booked exactly (a now-move at a far end changes MV-S1's density by momentum_of's booking, its moment about the far end 0, so the six-equation system's columns are exact and independent of the order of the moves), the carried division's remainder is the identity rhs - M x, and on a smooth row (every gradient alike) the six columns span one direction for P (the theorem met again). Run: KL1_SRC=<flagged copy> python -m pytest tests_kl1.py -q (under 15 s; the copy /dev/shm/tmp/kl1/src_kl1 by default)."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("KL1_SRC", "/dev/shm/tmp/kl1/src_kl1"))
sys.path.insert(0, HERE)
sys.set_int_max_str_digits(0)

from event_universe.close import solve_carried  # noqa: E402
from event_universe.core.ports import AXES, PORTS, across  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.take import lay, momentum_of, neighbour  # noqa: E402


def density(rec):
    num = rec.pair[0]
    return [2 * num * sum(across(l.now, 2 * a) * l.before - l.now * across(l.before, 2 * a) for l in rec.lines) for a in range(AXES)]


def test_the_kicks_inverse_is_booked_exactly_and_the_division_leaves_its_remainder():
    universe, world = load_world(os.path.join(HERE, "worlds", "world_chiral_3_30.json"))
    node = Node(universe, world)
    rec = node.records().index(node.emitter())
    row = node.records()[rec]
    rng = np.random.default_rng(7)
    for line in row.lines:
        line.now[...] = rng.integers(500, 1500, size=node.shape)
        line.before[...] = rng.integers(500, 1500, size=node.shape)
    z = row.lines[0]
    at = (1, 1, 1)
    fars = [neighbour(node, at, p) for p in range(PORTS)]
    cols = [momentum_of(node, z.now, z.before, far, d_now=1, num=row.pair[0]) for far in fars]
    deltas = [int(x) for x in rng.integers(-30, 30, size=PORTS)]
    p0 = [int(np.sum(x)) for x in density(row)]
    for far, d in zip(fars, deltas, strict=True):
        lay(node, rec, far, d, line=0)
    p1 = [int(np.sum(x)) for x in density(row)]
    assert [b - a for a, b in zip(p0, p1, strict=True)] == [sum(d * cols[p][a] for p, d in enumerate(deltas)) for a in range(AXES)]
    m = [[cols[p][i] for p in range(PORTS)] for i in range(AXES)] + [[0] * PORTS for _ in range(AXES)]
    rhs = [int(x) * 10**12 + int(y) for x, y in zip(rng.integers(-10**8, 10**8, size=AXES), rng.integers(-10**8, 10**8, size=AXES), strict=True)] + [0, 0, 0]
    x, rem, rank, _broken = solve_carried(m, rhs)
    assert rem == [r - sum(mv * xv for mv, xv in zip(mrow, x, strict=True)) for mrow, r in zip(m, rhs, strict=True)]
    assert rank == AXES
    for line in row.lines:
        line.before[...] = 0
        line.now[...] = 0
    for i in range(3):
        z.before[i, :, :] = 100 * i
    cols = [momentum_of(node, z.now, z.before, far, d_now=1, num=row.pair[0]) for far in fars]
    m = [[cols[p][i] for p in range(PORTS)] for i in range(AXES)]
    _x, _rem, rank, _broken = solve_carried(m, [1, 1, 1])
    assert rank == 1

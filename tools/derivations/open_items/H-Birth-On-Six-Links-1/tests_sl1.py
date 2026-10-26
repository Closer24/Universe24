"""H-Birth-On-Six-Links-1: the one-Node theorem (a move at one Node changes the lattice momentum on its six Links alone, each along its own axis, so its moment about the Node is 0), the recoil lay's formula onto nothing, and the reader's counts on the flagged hole 60. Run: SL1_SRC=<flagged copy> python -m pytest tests_sl1.py -q (under 15 s; the copy /dev/shm/tmp/sl1/src_sl1 by default)."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("SL1_SRC", "/dev/shm/tmp/sl1/src_sl1"))
sys.path.insert(0, HERE)
sys.set_int_max_str_digits(0)

from event_universe.core.ports import AXES, across, port_of  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.take import lay, momentum_of, neighbour  # noqa: E402

from sl1_moment import cross  # noqa: E402


def density(rec):
    num = rec.pair[0]
    found = []
    for a in range(AXES):
        s = 0
        for line in rec.lines:
            s = s + across(line.now, 2 * a) * line.before - line.now * across(line.before, 2 * a)
        found.append(2 * num * s)
    return found


def moment_about(rec, c2, shape):
    """The moment of MV-S1's density about a doubled centre, each Link's momentum at its midpoint 2 r_i + e_a."""
    p = density(rec)
    idx = np.indices(shape)
    L = [0, 0, 0]
    for a in range(AXES):
        arm = [2 * idx[b].astype(object) + (1 if b == a else 0) - c2[b] for b in range(AXES)]
        pa = [p[a] if b == a else 0 for b in range(AXES)]
        for cc in range(AXES):
            x, y = (cc + 1) % 3, (cc + 2) % 3
            L[cc] += int(np.sum(arm[x] * pa[y] - arm[y] * pa[x]))
    return L, [int(np.sum(x)) for x in p]


def fresh():
    universe, world = load_world(os.path.join(HERE, "worlds", "world_chiral_3_30.json"))
    node = Node(universe, world)
    s = [k for k, r in enumerate(node.records()) if r is not node.emitter()][0]
    return node, s


def test_a_move_at_one_node_has_no_moment_about_its_node_whatever_stands():
    """Any lay of four integers at one Node onto any standing levels changes P on the Node's six Links alone, each along its axis: the moment of the change about the Node is 0 and the change is momentum_of's booking."""
    node, s = fresh()
    row = node.records()[s]
    rng = np.random.default_rng(11)
    for _ in range(10):
        for line in row.lines:
            line.now[...] = rng.integers(-300, 300, size=node.shape)
            line.before[...] = rng.integers(-300, 300, size=node.shape)
        i = tuple(int(x) for x in rng.integers(3, size=3))
        c2 = [2 * x for x in i]
        L0, P0 = moment_about(row, c2, node.shape)
        li = [int(x) for x in rng.integers(-200, 200, size=4)]
        re, im = row.lines
        booked = [a + b for a, b in zip(momentum_of(node, re.now, re.before, i, li[0], li[1], row.pair[0]), momentum_of(node, im.now, im.before, i, li[2], li[3], row.pair[0]), strict=True)]
        lay(node, s, i, li)
        L1, P1 = moment_about(row, c2, node.shape)
        assert [a - b for a, b in zip(P1, P0, strict=True)] == booked
        assert [a - b for a, b in zip(L1, L0, strict=True)] == [0, 0, 0]


def test_recoil_lay_onto_nothing_carries_momentum_along_its_link_alone():
    """The child (A, 0, 0, sB) at the taker's Node, a lay re_before beta at the far end beyond the Port the recoil points to: P = -sigma 2 num A beta along that axis, 0 across, the far end's W 0, the moment about the taker's Node 0."""
    node, s = fresh()
    row = node.records()[s]
    re, im = row.lines
    num, A, B = row.pair[0], node.A, node.B
    for sigma in (1, -1):
        for b in range(AXES):
            for line in row.lines:
                line.now[...] = 0
                line.before[...] = 0
            at = (1, 1, 1)
            lay(node, s, at, (A, 0, 0, B))
            far = neighbour(node, at, port_of(b, 0 if sigma > 0 else 1))
            beta = 37
            booked = momentum_of(node, re.now, re.before, far, d_before=beta, num=num)
            lay(node, s, far, (0, beta, 0, 0))
            L, P = moment_about(row, [2 * x for x in at], node.shape)
            assert P == booked
            assert P[b] == -sigma * 2 * num * A * beta and all(P[k] == 0 for k in range(3) if k != b)
            assert L == [0, 0, 0]
            assert int(re.now[far] * im.before[far] - im.now[far] * re.before[far]) == 0


def test_reader_on_the_flagged_hole_60():
    path = os.path.join(HERE, "out", "J_hole60_f1.json")
    if not os.path.exists(path):
        return
    found = json.load(open(path))
    n = found["counts"]
    assert n["births"] == 15 and n["recoil lays"] == 24 and n["births: W_children summing 0"] == 15
    assert n["births: P balance 0 (every move summed)"] == 0 and n["births: J balance 0 about the centre"] == 0
    assert n["births: J balance 0 about the taker's Node"] == 9
    assert cross([1, 0, 0], [0, 5, 0]) == [0, 0, 5]

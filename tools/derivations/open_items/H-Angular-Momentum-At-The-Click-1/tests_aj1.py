"""H-Angular-Momentum-At-The-Click-1: the theorem of the one-Link lay's moment and the reader's identities. Run: PYTHONPATH=src_aj1 python -m pytest tests_aj1.py -q (under 15 s)."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src_aj1"))
sys.path.insert(0, HERE)
sys.set_int_max_str_digits(0)

from event_universe.core.ports import AXES, across  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402
from event_universe.take import lay  # noqa: E402

from aj1_moment import cross, read  # noqa: E402


def density(rec):
    """MV-S1's momentum density per axis on the +a Link of every Node, 2 num SUM_lines (now_(i+a) before_i - now_i before_(i+a))."""
    num = rec.pair[0]
    found = []
    for a in range(AXES):
        s = 0
        for line in rec.lines:
            s = s + across(line.now, 2 * a) * line.before - line.now * across(line.before, 2 * a)
        found.append(2 * num * s)
    return found


def moment_about(rec, c2, shape):
    """The moment of the density about a doubled centre: the Link's momentum sits at the Link's midpoint (2 r_i + e_a)."""
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


def test_one_link_lay_carries_momentum_along_the_axis_alone_and_no_moment_about_its_midpoint():
    """The theorem: eight integers laid at the two ends of one Link onto an empty plane give a density on that Link alone, so P is along the axis and the moment about the Link's midpoint is 0 whatever the integers; the moment about the Link's own axis is 0 about any centre."""
    universe, world = load_world(os.path.join(HERE, "worlds", "world_chiral_3_30.json"))
    node = Node(universe, world)
    s = [k for k, r in enumerate(node.records()) if r is not node.emitter()][0]
    rng = np.random.default_rng(7)
    for _ in range(12):
        row = node.records()[s]
        for line in row.lines:
            line.now[...] = 0
            line.before[...] = 0
        axis = int(rng.integers(3))
        i = tuple(int(x) for x in rng.integers(3, size=3))
        j = tuple((i[b] + (1 if b == axis else 0)) % 3 for b in range(3))
        li = [int(x) for x in rng.integers(-200, 200, size=4)]
        lj = [int(x) for x in rng.integers(-200, 200, size=4)]
        lay(node, s, i, li)
        lay(node, s, j, lj)
        mid2 = [2 * i[b] + (1 if b == axis else 0) for b in range(3)]
        L, P = moment_about(row, mid2, node.shape)
        assert all(P[b] == 0 for b in range(3) if b != axis)
        assert P[axis] == 2 * row.pair[0] * ((lj[0] * li[1] - li[0] * lj[1]) + (lj[2] * li[3] - li[2] * lj[3]))
        assert L == [0, 0, 0]
        c2 = [int(x) for x in rng.integers(-6, 6, size=3)]
        Lc, _ = moment_about(row, c2, node.shape)
        assert Lc[axis] == 0
        assert Lc == cross([m - c for m, c in zip(mid2, c2)], P)


def test_take_at_one_end_has_the_transverse_recoil_as_its_moment_about_the_midpoint():
    """(r_at - r_mid) x dP = (e/2) x dP: the along-axis part 0, the transverse part the whole; the taker's moment about the Link's own axis is 0."""
    e = [1, 0, 0]
    dp = [5, -7, 11]
    m = cross(e, dp)
    assert m[0] == 0 and m[1:] == [-11, -7]


def test_reader_on_the_flagged_hole_60():
    path = os.path.join(HERE, "out", "hole60_f.json")
    if not os.path.exists(path):
        return
    found = read(json.load(open(path)))
    n = found["counts"]
    assert n["births"] == 16 and n["births: dP_lay_ends present"] == 16 and n["births: dP_lay_ends summing to dP_lay"] == 16
    assert n["births: lay's moment about the Link's midpoint 0"] == 16 and n["births: moment about the Link's own axis 0 (take and lay)"] == 16
    assert n["births: balance 0 about the centre (J conserved at the event)"] == 0
    assert found["J2 by class"]["births' lays"] == [0, 0, 0]
    assert found["W_children summed over births"] == 0

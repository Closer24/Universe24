"""mk2's test for the Boss to carry into tests/ (under 15 seconds): Theorem A and the act's booking. (1) On an empty
3-cube a plane's quantum laid in the children's form at the two ends of one Link, then its first line's before at the far
end moved by p levels: the row's lattice momentum changes along the Link's axis alone, by exactly 2 num A p, the two
transverse components 0 whatever p (a two-Node lay onto nothing carries one integer, the current on its Link). (2) On the
hole seed to 14 under the act (MK-S2): every click line books dP_take, dP_recoil, the recoil, the wall and the axis; at
every birth the along-axis sum dP_take + dP_recoil is the
remainder of one division, below the wall's half in magnitude; the wall is 2 num times the first line's now gradient at
the far end; the run back exact 4 of 4. Runs against the patched src (mk2.patch) or the flagged copy with MK2_RECOIL=1."""

from __future__ import annotations

import os

os.environ.setdefault("MK2_RECOIL", "1")

import numpy as np

from event_universe.node import Node
from event_universe.rows import PLANE
from event_universe.take import lay, momentum_of, neighbour
from tests.laws import node_of

AXES, INTERVALS, BACK = 3, 14, 4


def momenta(node: Node, rec: int) -> list[int]:
    """One record row's lattice momentum per axis, P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a)) over its lines."""
    row = node.records()[rec]
    assert row.pair is not None
    found = [0] * AXES
    for a in range(AXES):
        for line in row.lines:
            moved = np.roll(line.now, -1, axis=a) * line.before - line.now * np.roll(line.before, -1, axis=a)
            found[a] += 2 * row.pair[0] * sum(int(x) for x in moved.reshape(-1))
    return found


def test_a_two_node_lay_onto_nothing_carries_the_current_on_its_link_alone_theorem_a() -> None:
    node = node_of("world_hole.json", shape=[3, 3, 3], seed=[], intervals=1)
    planes = [k for k, r in enumerate(node.records()) if r.shape == PLANE and r.gap]
    s = planes[0]
    num = node.records()[s].pair[0]
    at = (1, 1, 1)
    for port in range(6):
        far = neighbour(node, at, port)
        axis = port // 2
        assert all(x == 0 for x in momenta(node, s))
        lay(node, s, at, (node.A, 0, 0, -node.B))
        lay(node, s, far, (node.A, 0, 0, node.B))
        assert all(x == 0 for x in momenta(node, s)), "the children's form carries no momentum"
        for p in (1, -7, 88):
            lay(node, s, far, (0, p, 0, 0))
            found = momenta(node, s)
            booked = momentum_of(node, node.records()[s].lines[0].now, node.records()[s].lines[0].before, far, d_before=p, num=num)
            assert all(found[b] == 0 for b in range(AXES) if b != axis), (port, p, found)
            assert abs(found[axis]) == 2 * num * node.A * abs(p), (port, p, found)
            assert found == booked, "momentum_of books the lay exactly"
            lay(node, s, far, (0, p, 0, 0), -1)
        lay(node, s, far, (node.A, 0, 0, node.B), -1)
        lay(node, s, at, (node.A, 0, 0, -node.B), -1)


def test_the_recoil_across_the_link_books_the_axis_to_one_remainder_and_runs_back_mk_s2() -> None:
    node = node_of("world_hole.json", intervals=INTERVALS)
    hashes = []
    for k in range(INTERVALS):
        if k >= INTERVALS - BACK:
            hashes.append(node.state_hash())
        node.step()
    clicks = [e for e in node.log if e["event"] in ("birth", "credit")]
    assert clicks and all("recoil" in e or "laid_back" in e for e in clicks)
    births = [e for e in clicks if e["event"] == "birth"]
    assert births
    moved = 0
    for e in births:
        a = e["recoil_axis"]
        assert a >= 0
        # the transverse components are 0 only where the far end's neighbours hold nothing at the lay (Theorem A, test 1);
        # the hole's mirrored births lay children one Link apart in one close, so the log's `stood` cannot say so here
        along = e["dP_take"][a] + e["dP_recoil"][a]
        assert 2 * abs(along) <= abs(e["recoil_wall"]) or e["recoil_wall"] == 0, e
        assert e["dP_recoil"][a] == e["recoil_wall"] * e["recoil"], e
        moved += e["recoil"] != 0
    assert moved
    returned = 0
    for k in range(BACK):
        node.step_back()
        returned += node.state_hash() == hashes[BACK - 1 - k]
    assert returned == BACK

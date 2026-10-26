"""mk1's test for the Boss to carry into tests/ (under 15 seconds; the room: the hole seed of the 5-cube to 24 with the
board's lattice momentum read at every close, about 10 seconds): MK-S1's booking is exact and its act reversible, and
what the one-Node kick cannot do is pinned by name. On the hole seed to 24: every click line carries dP_take, dP_recoil
and the kick; at every close the board's lattice momentum changes by exactly what the lines book (dP_take + dP_recoil +
dP_lay summed, the reader's identity of gate 23); the kick is 0 wherever the kicked line's before gradient is 0 (a flat
line holds no momentum at the Node); dP_recoil is 2 num q Gb exactly on every line; the per-click identity dP_take +
dP_recoil = 0 holds on no click whose kick moved (the one-Node theorem: one integer against three axes); the run back
exact 10 of 10 through the clicks. On the one-Node form: a body line fed with a before gradient at the 3-cube's centre,
the act's q the nearest quotient and its inverse the same lay at -q. Runs against the patched src (mk1.patch) or the
flagged copy with MK1_RECOIL=1."""

from __future__ import annotations

import os

os.environ.setdefault("MK1_RECOIL", "1")

import numpy as np

from event_universe.core.rule3 import division_forward, half
from event_universe.node import Node
from event_universe.take import momentum_of, neighbour, recoil
from tests.laws import node_of

AXES, INTERVALS, BACK = 3, 24, 10


def momenta(node: Node) -> list[int]:
    """The board's lattice momentum per axis summed over the record rows, P_a = 2 num SUM_i (now_(i+a) before_i - now_i before_(i+a))."""
    found = [0] * AXES
    for row in node.records():
        assert row.pair is not None
        for a in range(AXES):
            for line in row.lines:
                moved = np.roll(line.now, -1, axis=a) * line.before - line.now * np.roll(line.before, -1, axis=a)
                found[a] += 2 * row.pair[0] * sum(int(x) for x in moved.reshape(-1))
    return found


def test_the_recoil_books_exactly_what_the_close_moves_and_runs_back_mk_s1() -> None:
    node = node_of("world_hole.json", intervals=INTERVALS)
    original, closes = node.click, []

    def click(plane_starts, held, direction=1, frame=None):  # type: ignore[no-untyped-def]
        before = momenta(node) if direction == 1 else None
        original(plane_starts, held, direction, frame)
        if direction == 1:
            closes.append((node.interval, before, momenta(node)))

    node.click = click  # type: ignore[method-assign]
    hashes = []
    for k in range(INTERVALS):
        if k >= INTERVALS - BACK:
            hashes.append(node.state_hash())
        node.step()
    clicks = [e for e in node.log if e["event"] in ("birth", "credit")]
    returned = 0
    for k in range(BACK):
        node.step_back()
        returned += node.state_hash() == hashes[BACK - 1 - k]
    assert returned == BACK
    assert clicks and all("kick" in e and "dP_recoil" in e for e in clicks if "laid_back" not in e)
    for i, before, after in closes:
        lines = [e for e in clicks if e["i"] == i]
        booked = [
            sum(e["dP_take"][a] + e.get("dP_recoil", [0] * AXES)[a] + e.get("dP_lay", [0] * AXES)[a] for e in lines)
            for a in range(AXES)
        ]
        assert [after[a] - before[a] for a in range(AXES)] == booked, i
    moved = [e for e in clicks if e.get("kick")]
    assert moved and all(e["kick_wall"] > 0 for e in moved)
    assert all(e["kick"] == 0 for e in clicks if e.get("kick_wall") == 0)
    assert not any(all(e["dP_take"][a] + e["dP_recoil"][a] == 0 for a in range(AXES)) for e in moved)
    assert max(abs(e["kick"]) for e in moved).bit_length() < 128


def test_the_one_node_kick_is_the_nearest_quotient_along_the_lines_gradient_and_inverts_mk_s1() -> None:
    node = node_of("world_hole.json", shape=[3, 3, 3], intervals=1, seed=[{"lay": "sea", "row": 0}])
    rec = node.records().index(node.gapped[0])
    row = node.records()[rec]
    assert row.pair is not None
    line, num, at = row.lines[0], row.pair[0], (1, 1, 1)
    feed = {neighbour(node, at, 0): 7, neighbour(node, at, 1): -2, neighbour(node, at, 2): 3, neighbour(node, at, 4): 5}
    for where, level in feed.items():
        line.before[where] = level
    gradient = [int(line.before[neighbour(node, at, 2 * a + 1)]) - int(line.before[neighbour(node, at, 2 * a)]) for a in range(AXES)]
    assert gradient == [-9, -3, -5]
    dp_take = [-4 * num * 10**6, 2 * num * 10**6, -6 * num * 10**6]
    was = int(line.now[at])
    q, dp, wall = recoil(node, rec, at, dp_take)
    assert wall == 2 * num * sum(g * g for g in gradient)
    assert q == division_forward(-sum(d * g for d, g in zip(dp_take, gradient, strict=True)), wall, half(wall))[0]
    assert dp == [2 * num * q * g for g in gradient] == momentum_of(node, line.now, line.before, at, d_now=q, num=num)
    assert int(line.now[at]) == was + q and q != 0
    node.lay(rec, at, (-q, 0, 0, 0))
    assert int(line.now[at]) == was
    for where in feed:
        line.before[where] = 0
    assert recoil(node, rec, at, dp_take) == (0, [0, 0, 0], 0)

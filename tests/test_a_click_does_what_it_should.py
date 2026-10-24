"""A click does what it is supposed to, to the Nodes and to the Node (the owner's word of 2026-10-24, 16:4x UTC; ALGEBRA.md, The board reads itself, the hole's clause and the click's read): one close at one Node, every Node's every line snapshotted before the close and after it. The Node: the seed record's lines at the clicking Node changed by exactly the take, the before kept and the now moved by the take's levels, the frame's light fallen by the children's walls summed within the last level's step, nothing made; the children laid there at the two senses, their Wronskians summing to 0. The Nodes: every other Node's seed lines unchanged by the close, the six neighbours read and never written. The log: the birth line's take keys the take's, the credit's support the Node, its windows the Node's first close, its point the three levels' at the interval's start. The draw: the number read from the Node and its six neighbours alone, divided by the unit once, the remainder below the rest where a whether is asked. The run back through that close exact. The chain of three Nodes at den 1,021 and the 3-cube hole seed's first close, on the law's own course (the holder of the volume gapped by the clock's one level: the hole's six neighbours turn at 2 and birth together at 4 on the 3-cube, one close, six Nodes alike, each the Node of its own take)."""

from __future__ import annotations

import json

import numpy as np
import pytest

from event_universe import digits, meeting_board, records, share, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import board_state, same_state
from tests.laws_universe import small_universe


def world_of(folder, shape, intervals):  # type: ignore[no-untyped-def]
    small_universe(folder)
    path = folder / "w.json"
    path.write_text(
        json.dumps({"universe": "u.json", "shape": shape, "intervals": intervals}), encoding="utf-8"
    )
    return path


def seed_lines(board):  # type: ignore[no-untyped-def]
    index = board.world.seed
    span = records.record_slice(board.families[index], 0)
    return [
        (np.array(line.now, dtype=object), np.array(line.before, dtype=object))
        for line in board.states[index].lines[span]
    ]


@pytest.mark.parametrize("shape", [[1, 1, 3], [3, 3, 3]])
def test_one_close_at_one_node_writes_the_take_there_and_nothing_elsewhere(tmp_path, monkeypatch, shape):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_world(world_of(tmp_path, shape, 12)), output=lines.append)
    unit = board.credit.units[board.world.seed]
    takes, reads, draws, light = [], [], [], {}
    real_take, real_read, real_drawn, real_closed = (
        meeting_board.take_of,
        meeting_board.read_of,
        meeting_board.drawn_from,
        meeting_board.closed,
    )
    monkeypatch.setattr(
        meeting_board, "take_of", lambda *a: (takes.append((a[3], real_take(*a))), takes[-1][1])[1]
    )
    monkeypatch.setattr(
        meeting_board, "read_of", lambda b, r, label: (reads.append(r), real_read(b, r, label))[1]
    )
    monkeypatch.setattr(
        meeting_board,
        "drawn_from",
        lambda *a: (draws.append((a[0], a[1], real_drawn(*a))), draws[-1][2])[1],
    )

    def closing(b, begun):  # type: ignore[no-untyped-def]
        before = seed_lines(b)
        real_closed(b, begun)
        light[b.interval] = (before, seed_lines(b))

    monkeypatch.setattr(meeting_board, "closed", closing)
    states = [board_state(board)]
    while not any(row.get("event") == "birth" for row in lines) and board.interval < 12:
        board.step()
        states.append(board_state(board))
    first = min(row["interval"] for row in lines if row.get("event") == "birth")
    births = [row for row in lines if row.get("event") == "birth" and row["interval"] == first]
    holed = {tuple(row["nodes"][0]) for row in births}
    assert len(holed) == len(births) and all(
        len(row["nodes"]) == 1 for row in births
    )  # one close, one Node per birth (six alike under the gapped holder on the 3-cube)
    before, after = light[first]
    for row in births:  # the Node: each born Node changed by its own take alone, the before kept
        at = tuple(row["nodes"][0])
        take = next(found for node, found in takes if node == at and found.taken == row["taken"])
        assert (row["taken"], row["walls"], row["excess"], row["step"]) == tuple(take[1:])  # the log
        assert 0 <= row["excess"] < row["step"] and row["taken"] == row["walls"] + row["excess"]
        for (now_0, before_0), (now_1, before_1) in zip(before, after, strict=True):
            toward = 0 if now_0[at] == before_0[at] else (1 if before_0[at] > now_0[at] else -1)
            assert before_1[at] == before_0[at] and now_1[at] == now_0[at] + toward * min(
                take.levels, abs(now_0[at] - before_0[at])
            )
        children = [k for k in board.order if board.families[k].name in row["children"]]
        senses = [
            int(np.asarray(records.wronskian(board.lines_of(k, r), True), dtype=object)[at])
            for k in children
            for r in range(2)
        ]
        assert sorted(row["senses"]) == [-1, 1] and sum(senses) == 0
        credit = next(
            c
            for c in lines
            if c.get("event") == "credit" and c["interval"] == first and c["support"] == list(at)
        )
        assert credit["windows"] == 1 and credit["identity"] == [board.world.seed, 0]
    elsewhere = np.ones(board.shape, dtype=bool)
    for at in holed:
        elsewhere[at] = False
    for (now_0, before_0), (now_1, before_1) in zip(
        before, after, strict=True
    ):  # the Nodes: every other Node unchanged
        assert np.array_equal(now_1[elsewhere], now_0[elsewhere]) and np.array_equal(
            before_1[elsewhere], before_0[elsewhere]
        )
    for frame in reads:  # the draw: the Node and its six neighbours, nothing else
        assert all(
            list(nodes) == digits.frame_of(nodes[0], board.shape, board.world.periodic)
            for _k, nodes in frame
        )
    for number, weights, (port, left) in draws:
        assert (
            sum(weights) == unit
            and (port == 0) == (number % unit < weights[0])
            and left == number // unit
        )
    back = 0
    for k in range(first):
        board.step_inverse()
        back += same_state(board_state(board), states[first - 1 - k])
    assert back == first


def test_a_bound_bodys_click_writes_the_take_at_its_node_and_nothing_elsewhere(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The owner's standing test for the bound body's click (the owner's sentence of 2026-10-24, 16:45 UTC): the lone pair on the 3-cube, its two records clicking together at their Node at the first window met; every seed line snapshotted before that close and after it: the Node's now moved by the two takes' levels summed and its before kept, every other Node unchanged bit for bit; the credits at the Node with the records' identities and the light taken by at least the two units; nothing born; the run back through that close exact."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    real_child = meeting_board.child_of

    def once(board, index, value, whole):  # type: ignore[no-untyped-def]
        born = any(board.states[k].lines for k in board.order if share.charged(board.families[k]))
        return () if born else real_child(board, index, value, whole)

    monkeypatch.setattr(meeting_board, "child_of", once)
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_world(world_of(tmp_path, [3, 3, 3], 30)), output=lines.append)
    seed, takes, light = board.world.seed, [], {}
    real_take, real_closed = meeting_board.take_of, meeting_board.closed
    monkeypatch.setattr(
        meeting_board,
        "take_of",
        lambda *a: (takes.append((board.interval, a[3], real_take(*a))), takes[-1][2])[1],
    )

    def closing(b, begun):  # type: ignore[no-untyped-def]
        before = seed_lines(b)
        real_closed(b, begun)
        light[b.interval] = (before, seed_lines(b))

    monkeypatch.setattr(meeting_board, "closed", closing)
    states = [board_state(board)]
    while (
        not any(row["event"] == "credit" and row["identity"][0] != seed for row in lines)
        and board.interval < 30
    ):
        board.step()
        states.append(board_state(board))
    bodies = [row for row in lines if row["event"] == "credit" and row["identity"][0] != seed]
    interval, at = bodies[0]["interval"], tuple(bodies[0]["support"])
    assert len(bodies) == 2 and all(
        row["interval"] == interval and tuple(row["support"]) == at for row in bodies
    )
    assert sorted(row["identity"][1] for row in bodies) == [0, 1] and not any(
        row["event"] == "birth" and row["interval"] == interval for row in lines
    )
    levels = sum(found.levels for t, node, found in takes if t == interval and node == at)
    assert levels > 0 and all(found.taken >= found.walls for t, node, found in takes if t == interval)
    before, after = light[interval]
    for (now_0, before_0), (now_1, before_1) in zip(before, after, strict=True):
        toward = 0 if now_0[at] == before_0[at] else (1 if before_0[at] > now_0[at] else -1)
        assert before_1[at] == before_0[at] and now_1[at] == now_0[at] + toward * min(
            levels, abs(now_0[at] - before_0[at])
        )
        elsewhere = np.ones(board.shape, dtype=bool)
        elsewhere[at] = False
        assert np.array_equal(now_1[elsewhere], now_0[elsewhere]) and np.array_equal(
            before_1[elsewhere], before_0[elsewhere]
        )
    back = 0
    for k in range(interval):
        board.step_inverse()
        back += same_state(board_state(board), states[interval - 1 - k])
    assert back == interval

"""A click does what it is supposed to, to the Nodes and to the Node (the owner's word of 2026-10-24, 16:4x UTC; ALGEBRA.md, The board reads itself, the hole's clause and the click's read): one close at one Node, every Node's every line snapshotted before the close and after it. The Node: the seed record's lines at the clicking Node changed by exactly the take, the before kept and the now moved by the take's levels, the frame's light fallen by the children's walls summed within the last level's step, nothing made; the children laid there at the two senses, their Wronskians summing to 0. The Nodes: every other Node's seed lines unchanged by the close, the six neighbours read and never written. The log: the birth line's take keys the take's, the credit's support the Node, its windows the Node's first close, its point the three levels' at the interval's start. The draw: the number read from the Node and its six neighbours alone, divided by the unit once, the remainder below the rest where a whether is asked. The run back through that close exact. The chain of three Nodes at den 1,021 (its first click by the drawn whether) and the 3-cube hole seed's first close."""

from __future__ import annotations

import json

import numpy as np
import pytest

from event_universe import digits, meeting_board, records, world_files
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
    birth = next(row for row in lines if row.get("event") == "birth")
    at, interval = tuple(birth["nodes"][0]), birth["interval"]
    assert len(birth["nodes"]) == 1 and len([row for row in lines if row.get("event") == "birth"]) == 1
    before, after = light[interval]
    take = next(found for node, found in takes if node == at and found.taken == birth["taken"])
    for (now_0, before_0), (now_1, before_1) in zip(
        before, after, strict=True
    ):  # the Node: the take alone
        toward = 0 if now_0[at] == before_0[at] else (1 if before_0[at] > now_0[at] else -1)
        assert before_1[at] == before_0[at] and now_1[at] == now_0[at] + toward * min(
            take.levels, abs(now_0[at] - before_0[at])
        )
        elsewhere = np.ones(board.shape, dtype=bool)
        elsewhere[at] = False
        assert np.array_equal(now_1[elsewhere], now_0[elsewhere]) and np.array_equal(
            before_1[elsewhere], before_0[elsewhere]
        )  # the Nodes
    assert (birth["taken"], birth["walls"], birth["excess"], birth["step"]) == tuple(take[1:])  # the log
    assert 0 <= birth["excess"] < birth["step"] and birth["taken"] == birth["walls"] + birth["excess"]
    children = [k for k in board.order if board.families[k].name in birth["children"]]
    senses = [
        int(np.asarray(records.wronskian(board.lines_of(k, r), True), dtype=object)[at])
        for k in children
        for r in range(2)
    ]
    assert sorted(birth["senses"]) == [-1, 1] and sum(senses) == 0 and senses[0] * senses[1] < 0
    credit = next(row for row in lines if row.get("event") == "credit" and row["interval"] == interval)
    assert credit["support"] == list(at) and credit["windows"] == 1
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
    if shape == [1, 1, 3]:
        assert draws and draws[-1][2][0] == 0  # the chain's first click by the drawn whether, met
    back = 0
    for k in range(interval):
        board.step_inverse()
        back += same_state(board_state(board), states[interval - 1 - k])
    assert back == interval

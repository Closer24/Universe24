"""The readings made once per interval and given again to every act that reads them (the architect's second round of 2026-10-24): the records' read (features/read READS; node.read_lines, node.read, node.rulers) and the board's share (share.board_share under Lattice.share_of), each with and without its memo the same integers at every Node and the same output lines over 20 intervals of the shipped Universe24 (its first clicks among them), and the memo read again more often than made."""

from pathlib import Path
from typing import Any

import pytest

from event_universe import node, share, world_files
from event_universe.features import read
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import board_state, same_state
from tests.laws_universe import ERAS, WORLD, small_world

INTERVALS, FIRST_TURN = 20, 34  # the small universe's first turned Node is at the interval 34


class Unkept(dict[Any, Any]):
    """A memo that keeps nothing: every reading made again."""

    def __setitem__(self, key: Any, value: Any) -> None:
        pass


def stepped(intervals: int) -> tuple[list[Any], list[dict[str, object]]]:
    """The board stepped with the readings the eras tool makes after every interval (every family's share and quanta over the board) kept among the lines."""
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(WORLD), output=lines.append)
    states = []
    for _ in range(intervals):
        board.step()
        states.append(board_state(board))
        for index in board.order:  # the share, the eras line's quanta and the nodes line's quanta
            share, quanta, again = (
                board.share_of(index)[0],
                board.quanta(index)[0],
                board.quanta(index)[0],
            )
            assert (quanta == again).all()
            lines.append({"event": "read", "share": share.tolist(), "quanta": quanta.tolist()})
    return states, lines


@pytest.mark.parametrize("holder", [node, share])
def test_the_reading_made_once_per_interval_is_the_reading_at_every_act(
    monkeypatch: pytest.MonkeyPatch, holder: Any
) -> None:
    monkeypatch.setattr(holder, "READS", Unkept())  # the names as the module holds them
    made, made_lines = stepped(INTERVALS)
    monkeypatch.undo()
    hits = {"again": 0, "made": 0}
    again = read.read_again

    def counted(key: Any, taken: Any) -> Any:
        found = again(key, taken)
        hits["again" if found is not None else "made"] += 1
        return found

    monkeypatch.setattr(holder, "read_again", counted)
    kept, kept_lines = stepped(INTERVALS)
    assert all(same_state(a, b) for a, b in zip(kept, made, strict=True))
    assert kept_lines == made_lines and any(line["event"] == "credit" for line in kept_lines)
    assert hits["again"] > hits["made"] > 0
    board = Lattice(load_world(WORLD), output=lambda line: None)
    for _ in range(INTERVALS):
        board.step()
        board.quanta(board.order[0])
        if board.interval == INTERVALS // 4:
            entries = len(read.READS)
    assert (
        len(read.READS) == entries
    )  # the memo bounded: one entry per key, the states compared by identity


def test_the_nodes_line_is_the_reading_node_by_node(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(small_world(tmp_path)), output=lambda line: None)
    for _ in range(FIRST_TURN - 1):
        board.step()
    time_line = board.states[board.held[0]].lines[0]
    before = tuple([int(x) for x in level.reshape(-1)] for level in (time_line.now, time_line.before))
    board.step()
    gamma, nodes = board.world.node_clock, len(before[0])
    found = ERAS.node_lines(board, before, [1] * nodes)
    now = [int(x) for x in board.states[board.held[0]].lines[0].now.reshape(-1)]
    before_now = [int(x) for x in board.states[board.held[0]].lines[0].before.reshape(-1)]
    turned = [
        i
        for i in range(nodes)
        if before_now[i] == before[0][i] and now[i] == before[1][i] and before[1][i] <= before[0][i]
        if now[i] != before_now[i]
    ]
    assert found["X"] == now and found["turned"] == turned and turned
    assert found["length"] == [round(float((x / gamma) ** (1 / 4)), 6) if x > 0 else 0 for x in now]
    assert found["direction"] == [-1 if i in turned else 1 for i in range(nodes)]
    assert all(type(q) is int for name in found["quanta"] for q in found["quanta"][name])
    assert found["quanta"]["matter"] == [int(q) for q in board.quanta(2)[0].reshape(-1)]

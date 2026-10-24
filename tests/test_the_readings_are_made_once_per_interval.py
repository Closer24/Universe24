"""The readings made once per interval and given again to every act that reads them (the architect's second round of 2026-10-24): the records' read (features/read READS; node.read_lines, node.read, node.rulers) and the board's share (share.board_share under Lattice.share_of), each with and without its memo the same integers at every Node and the same output lines over 20 intervals of the shipped Universe24 (its first clicks among them), and the memo read again more often than made."""

from pathlib import Path
from typing import Any

import pytest

from event_universe import node, share, world_files
from event_universe.features import read
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import board_state, same_state
from tests.laws_universe import ERAS, bare_torus

INTERVALS, FIRST_TURN = (
    32,
    154,
)  # the bare 3-cube torus: the births at 29, the first turned Node at 154 (20 and 34 on the small universe, laid with bodies, to 2026-10-24)


class Unkept(dict[Any, Any]):
    """A memo that keeps nothing: every reading made again."""

    def __setitem__(self, key: Any, value: Any) -> None:
        pass


def stepped(path: Path, intervals: int) -> tuple[list[Any], list[dict[str, object]], list[int]]:
    """The board stepped with the readings the eras tool makes after every interval (every family's share and quanta over the board) kept among the lines."""
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(path), output=lines.append)
    states, sizes = [], []
    for _ in range(intervals):
        board.step()
        states.append(board_state(board))
        sizes.append(len(read.READS))  # the memo's entries after the interval
        for index in board.order:  # the share, the eras line's quanta and the nodes line's quanta
            share, quanta = board.share_of(index)[0], board.quanta(index)[0]
            lines.append({"event": "read", "share": share.tolist(), "quanta": quanta.tolist()})
    return states, lines, sizes


def test_the_reading_made_once_per_interval_is_the_reading_at_every_act(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The one run with both memos kept against the run with neither (the readings made again at every act), then each holder's memo counted on its own run: the same states and lines, the credit lines of the births at 29 among them, the memo bounded (one entry per key)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = bare_torus(tmp_path)
    for holder in (node, share):
        monkeypatch.setattr(holder, "READS", Unkept())  # the names as the module holds them
    made, made_lines, _sizes = stepped(path, INTERVALS)
    monkeypatch.undo()
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    again = read.read_again
    for holder in (node, share):
        hits = {"again": 0, "made": 0}

        def counted(key: Any, taken: Any, hits: dict[str, int] = hits) -> Any:
            found = again(key, taken)
            hits["again" if found is not None else "made"] += 1
            return found

        monkeypatch.setattr(holder, "read_again", counted)
        kept, kept_lines, sizes = stepped(path, INTERVALS)
        monkeypatch.setattr(holder, "read_again", again)
        assert all(same_state(a, b) for a, b in zip(kept, made, strict=True))
        assert kept_lines == made_lines and any(line["event"] == "credit" for line in kept_lines)
        assert hits["again"] > hits["made"] > 0, holder.__name__
        assert (
            sizes[INTERVALS // 4] == sizes[-1] > 0
        )  # the memo bounded: one entry per key, the states compared by identity


def test_the_nodes_line_is_the_reading_node_by_node(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(bare_torus(tmp_path, intervals=FIRST_TURN)), output=lambda line: None)
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
    assert found["quanta"]["light"] == [
        int(q) for q in board.quanta(2)[0].reshape(-1)
    ]  # the third row, light since matter left (2026-10-24)

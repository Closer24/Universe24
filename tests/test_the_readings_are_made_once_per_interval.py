"""The readings made once per interval and given again to every act that reads them (the architect's second round of 2026-10-24): the records' read (features/read READS, node.read_lines, node.read, node.rulers), with and without the memo the same integers at every Node and the same output lines over 20 intervals of the shipped Universe24 (its first clicks among them), and the memo read again more often than made."""

from typing import Any

import pytest

from event_universe import node
from event_universe.features import read
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import board_state, same_state
from tests.laws_universe import WORLD

INTERVALS = 20


class Unkept(dict[Any, Any]):
    """A memo that keeps nothing: every reading made again."""

    def __setitem__(self, key: Any, value: Any) -> None:
        pass


def stepped(intervals: int) -> tuple[list[Any], list[dict[str, object]]]:
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(WORLD), output=lines.append)
    states = []
    for _ in range(intervals):
        board.step()
        states.append(board_state(board))
    return states, lines


def test_the_records_read_once_per_interval_are_the_read_at_every_act(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(node, "READS", Unkept())  # the names as node.py holds them
    made, made_lines = stepped(INTERVALS)
    monkeypatch.undo()
    hits = {"again": 0, "made": 0}
    again = read.read_again

    def counted(key: Any, taken: Any) -> Any:
        found = again(key, taken)
        hits["again" if found is not None else "made"] += 1
        return found

    monkeypatch.setattr(node, "read_again", counted)
    kept, kept_lines = stepped(INTERVALS)
    assert all(same_state(a, b) for a, b in zip(kept, made, strict=True))
    assert kept_lines == made_lines and any(line["event"] == "credit" for line in kept_lines)
    assert hits["again"] > hits["made"] > 0

"""The readings made once per interval and given again to every act that reads them (the architect's second round of 2026-10-24): the records' read (features/read READS; node.read_lines, node.read, node.rulers) and the board's share (share.board_share under Lattice.share_of), each with and without its memo the same integers at every Node and the same output lines over 20 intervals of the shipped Universe24 (its first clicks among them), and the memo read again more often than made."""

from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe import digits, node, plane, registry, share, world_files
from event_universe.features import read
from event_universe.lattice import Lattice
from event_universe.loader.derived import amplitude_bound, turns
from event_universe.loader.universe import MASSLESS
from event_universe.world_files import load_world
from tests.laws import board_state, same_state
from tests.laws_universe import ERAS, GAMMA, bare_torus

# the bare 3-cube torus of the tests' small universe: the births by the draw from the hole seed's first intervals, and no turned Node ever under the massless volume holder (2026-10-24, the owner's closure: one bang, the expansion for ever; the first turned Node at 205 to 328 under the gapped holder's cycle, kept by name), the Nodes' line read over TURN_BOUND intervals
INTERVALS, TURN_BOUND = 32, 20


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
    """The one run with both memos kept against the run with neither (the readings made again at every act), then each holder's memo counted on its own run: the same states and lines, the credit lines of the births among them (the hole seed's, one per close at the origin under the hole the Node's own level before, the drift stopped, 2026-10-24), the memo bounded (one entry per key: its entries stand over the second half of the run, the digits' keys added at the first draw by the digits) and each key made at most once per interval, the hits above 0 (the selector's course at den 1,021 reads at one Node per close, so the former "hits above makes" read the course and not the memo, 2026-10-24)."""
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
        assert hits["made"] <= sizes[-1] * INTERVALS and hits["again"] > 0 < hits["made"], (
            holder.__name__
        )  # each key made at most once per interval and given again (the memo's own bound; "again above made" read the course, several reading Nodes per close under the former pick, and under the selector the toy's close reads at one Node per close, 565 hits against 569 makes for the records' read, 2026-10-24)
        # the memo bounded: one entry per key, the states compared by identity; it gains the digits' keys at the
        # first draw by the digits (the records' rules read at the Node's frame) and stands from there
        assert sizes[INTERVALS // 2] == sizes[-1] > 0


def test_the_nodes_line_is_the_reading_node_by_node(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(bare_torus(tmp_path, intervals=TURN_BOUND)), output=lambda line: None)
    turned: list[int] = []
    while (
        not turned and board.interval < TURN_BOUND
    ):  # to the first turned Node, wherever the course puts it
        time_line = board.states[board.held[0]].lines[0]
        before = tuple(
            [int(x) for x in level.reshape(-1)] for level in (time_line.now, time_line.before)
        )
        board.step()
        now = [int(x) for x in board.states[board.held[0]].lines[0].now.reshape(-1)]
        before_now = [int(x) for x in board.states[board.held[0]].lines[0].before.reshape(-1)]
        turned = [
            i
            for i in range(len(now))
            if before_now[i] == before[0][i] and now[i] == before[1][i] and before[1][i] <= before[0][i]
            if now[i] != before_now[i]
        ]
    gamma, nodes = board.world.node_clock, len(now)
    found = ERAS.node_lines(board, before, [1] * nodes)
    assert (
        found["X"] == now and found["turned"] == turned == []
    )  # no Node turns under the massless holder
    assert found["length"] == [round(float((x / gamma) ** (1 / 4)), 6) if x > 0 else 0 for x in now]
    assert found["direction"] == [-1 if i in turned else 1 for i in range(nodes)]
    assert all(type(q) is int for name in found["quanta"] for q in found["quanta"][name])
    assert found["quanta"][MASSLESS] == [
        int(q) for q in board.quanta(2)[0].reshape(-1)
    ]  # the third row, the massless point after the two holders (2026-10-24)


def test_the_rule_and_the_pairs_of_the_digits_read_are_made_once_per_close(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """digits.ruled and flux.pairs_of asked at every Node's frame of the bare 3-cube at one interval: the digits with the memo cleared before every frame against the memo warm, the same integers; node.rule_of called once per record over every frame."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(bare_torus(tmp_path)), output=lambda line: None)
    for _ in range(4):
        board.step()
    frames = [digits.frame_of(at, board.shape, board.world.periodic) for at in np.ndindex(*board.shape)]

    def read_digits(frame: list[Any]) -> list[list[Any]]:
        return [list(digits.digits_of(board, index, frame)) for index in board.order]

    cold = []
    for frame in frames:
        read.READS.clear()
        cold.append(read_digits(frame))
    read.READS.clear()
    calls, rule_of = list[int](), node.rule_of
    monkeypatch.setattr(node, "rule_of", lambda *a, **k: (calls.append(1), rule_of(*a, **k))[1])
    assert [read_digits(frame) for frame in frames] == cold
    assert len(calls) == sum(
        len(registry.quanta_records(board.families, board.states, i)) for i in board.order
    )


def test_the_turned_room_is_computed_once_per_pair_at_load(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """plane.turned_room under functools.cache: the same integer cold and warm for every turned family of the one universe, every warm call a hit, and the amplitude bound the world's."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = load_world(bare_torus(tmp_path))
    pairs = {f.pair for i, f in enumerate(world.families) if turns(world.families, i)}
    plane.turned_room.cache_clear()
    cold = {pair: plane.turned_room(pair, GAMMA, world.link_unit) for pair in pairs}
    assert plane.turned_room.cache_info().misses == len(pairs) > 0
    assert {pair: plane.turned_room(pair, GAMMA, world.link_unit) for pair in pairs} == cold
    assert plane.turned_room.cache_info().hits == len(pairs)
    action, bits = world.quantum_action, world.width.bit_length()  # World.width the largest integer
    assert amplitude_bound(world.families, GAMMA, action, bits, world.link_unit) == world.amplitude_bound

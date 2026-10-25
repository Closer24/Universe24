"""The draw's digits read in the Node's own frame (digits.frame_of: the Node first, then its six Ports in the Port order; the owner's rule of 2026-10-24: the click reads the Node and its six neighbours only, nothing of the board's labels): a lawful seed rolled one Link along x on the torus gives the rolled board bit for bit, every line, write remainder and phase line, through the first drawn whether and after, with the same births at the rolled Nodes."""

import json
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe import digits, records, seed
from event_universe.emission import emitted_lines
from event_universe.lattice import Lattice
from event_universe.lay import laid
from event_universe.world_files import load_world

UNIVERSE, SIDE, INTERVALS, DRAWN = "examples/events/universe24/universe_universe24.json", 3, 8, 3


def sea_plus_one(at: tuple[int, int, int]) -> Any:
    """The seed hand's S1: the law's uniform sea of light and one more quantum of it at the Node `at` (a test's seed, laid through the lay act as the law's own is)."""

    def laid_seed(board: Lattice, index: int) -> None:
        family, drift = board.families[index], seed.drift_of(board.world.quantum_action)
        first, zeros = records.record_slice(family, 0).start, records.zeros(board.shape, board.kind)
        mask = board.mask((at,))
        for level, nodes in (
            (records.full(board.shape, drift, board.kind), None),
            (np.where(mask, drift, 0), mask),
        ):
            for line in emitted_lines(family):
                laid(board, index, first + line, (level, zeros), None, None, nodes)

    return laid_seed


def arrays_of(board: Lattice) -> list[np.ndarray]:
    found: list[Any] = []
    for state in board.states:
        found += [a for line in state.lines for a in (line.now, line.before, line.remainder)]
        found += list(state.write_remainders)
        found += [
            a for row in state.phases for line in row for a in (line.now, line.before, line.remainder)
        ]
    return [np.asarray(a, dtype=object) for a in found]


def test_the_frame_is_the_node_and_its_six_ports_in_the_port_order() -> None:
    assert digits.frame_of((0, 0, 0), (3, 3, 3), (True, True, True)) == [
        (0, 0, 0),
        (1, 0, 0),
        (2, 0, 0),
        (0, 1, 0),
        (0, 2, 0),
        (0, 0, 1),
        (0, 0, 2),
    ]
    assert digits.frame_of((1, 1, 1), (3, 3, 3), (True, True, True)) == [
        (1, 1, 1),
        (2, 1, 1),
        (0, 1, 1),
        (1, 2, 1),
        (1, 0, 1),
        (1, 1, 2),
        (1, 1, 0),
    ]
    assert digits.frame_of((0, 1, 1), (3, 3, 3), (False, True, True)) == [
        (0, 1, 1),
        (1, 1, 1),
        (0, 2, 1),
        (0, 0, 1),
        (0, 1, 2),
        (0, 1, 0),
    ]


def test_a_seed_rolled_one_link_gives_the_rolled_board_bit_for_bit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    world = tmp_path / "w.json"
    world.write_text(
        json.dumps({"universe": UNIVERSE, "shape": [SIDE] * 3, "intervals": INTERVALS}), encoding="utf-8"
    )
    runs = []
    for at in ((0, 0, 0), (1, 0, 0)):
        monkeypatch.setattr(seed, "uniform_seed", sea_plus_one(at))
        lines: list[dict[str, Any]] = []
        board = Lattice(load_world(world), output=lines.append)
        kept = []
        for _ in range(INTERVALS):
            board.step()
            kept.append(arrays_of(board))
        runs.append((kept, lines))
    (origin, origin_lines), (rolled, rolled_lines) = runs
    for tick, (a, b) in enumerate(zip(origin, rolled, strict=True), start=1):
        assert all(np.array_equal(np.roll(x, 1, axis=0), y) for x, y in zip(a, b, strict=True)), tick
    births = [
        sorted(
            (
                ((line["nodes"][0][0] + shift) % SIDE, *line["nodes"][0][1:]),
                line["interval"],
                line["children"][0],
            )
            for line in lines
            if line["event"] == "birth"
        )
        for lines, shift in ((origin_lines, 1), (rolled_lines, 0))
    ]
    assert births[0] == births[1] and any(interval == DRAWN for _at, interval, _child in births[0])

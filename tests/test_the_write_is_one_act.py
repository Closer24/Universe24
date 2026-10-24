"""The write is one act (ALGEBRA.md #the-primitives, a family's write is one act; the row "the held write": the held family's parts at every Node, each by one division, one write remainder per part at the Node; features/held_write.held_write, node.held_write_at): (numerator + r) div wall at every Node by Rule3's carried division with the remainder kept at the Node in [0, wall), forward then back exact, at one wall or a wall per Node and on numerators of both signs, a wall below 1 refused by name; asserted on arrays alone and on the bare 3-cube torus of the one universe file's own records, the act and not the whole step."""

from pathlib import Path

import numpy as np
import pytest

from event_universe import node, records, world_files
from event_universe.features.held_write import held_write
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import refused
from tests.laws_universe import CUBE, bare_torus

SHAPE = (CUBE,) * 3


def test_the_held_write_is_one_carried_division_forward_and_back() -> None:
    """On random levels, numerators of both signs within 10^9 and remainders in [0, wall) at one wall and at a wall per Node: the level gains (numerator + r) div wall, the remainder after is (numerator + r) mod wall, in [0, wall), and the act at -1 from the state after returns the level and the remainder before, bit for bit; a wall below 1 at any Node is refused by name."""
    draw = np.random.default_rng(24)
    for wall in (7, 36_000, draw.integers(1, 10**6, SHAPE).astype(object)):
        level = draw.integers(-(10**6), 10**6, SHAPE).astype(object)
        numerator = draw.integers(-(10**9), 10**9, SHAPE).astype(object)
        remainder = np.asarray(draw.integers(0, 10**9, SHAPE).astype(object) % wall, dtype=object)
        after, kept = held_write(level, numerator, wall, remainder)
        total = numerator + remainder
        assert np.array_equal(np.asarray(after, dtype=object), level + total // wall)
        assert np.array_equal(np.asarray(kept, dtype=object), total % wall)
        assert ((np.asarray(kept, dtype=object) >= 0) & (np.asarray(kept, dtype=object) < wall)).all()
        back, origin = held_write(after, numerator, wall, kept, -1)
        assert np.array_equal(np.asarray(back, dtype=object), level)
        assert np.array_equal(np.asarray(origin, dtype=object), remainder)
    refused("wall E_s T is from 1", held_write, 0, 1, 0, 0)
    refused(
        "wall E_s T is from 1", held_write, level, numerator, np.array([[[1]], [[0]]], dtype=object), 0
    )


def test_the_one_write_per_line_on_the_bare_torus_is_the_act_by_hand(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The held row of the volume on the bare 3-cube torus as loaded: its lines and its write remainders at the division's origin, half the wall each line's write divides at (`records.divided_walls` on `Lattice.fixed_walls`, the carried factor's wall at the rest's paces: the volume's time line at Gamma times its fixed wall, the volume's divisor Gamma E_s T, every other line at its fixed wall; to 2026-10-24 the time line's remainder was born at half the fixed wall, 1 / (2 Gamma) of its own wall, the builder's finding of #2187), written once by `node.held_write_at` on random numerators at those walls: every line gains (numerator + r) div wall at every Node with the remainder kept, the lines' kind kept, and the act back returns the loaded state bit for bit."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(bare_torus(tmp_path, CUBE)))
    held = board.held[0]
    fixed = board.fixed_walls[held]
    divided = records.divided_walls(board.families[held], fixed, board.world.node_clock)
    assert np.array_equal(
        np.asarray(divided[0], dtype=object), board.world.node_clock * np.asarray(fixed[0], dtype=object)
    ) and all(d is f for d, f in zip(divided[1:], fixed[1:], strict=True))
    walls = [np.asarray(wall, dtype=object) for wall in divided]
    state = board.states[held]
    assert len(walls) == len(state.lines) == len(state.write_remainders)
    assert all(
        np.array_equal(np.asarray(r, dtype=object), np.broadcast_to(w // 2, SHAPE))
        for r, w in zip(state.write_remainders, walls, strict=True)
    )
    draw = np.random.default_rng(5)
    numerators = [
        draw.integers(-3, 3, SHAPE).astype(object) * w + draw.integers(0, 10**9, SHAPE).astype(object)
        for w in walls
    ]
    lines, kept = node.held_write_at(state.lines, numerators, walls, state.write_remainders)
    for line, after, numerator, wall, before, remainder in zip(
        state.lines, lines, numerators, walls, state.write_remainders, kept, strict=True
    ):
        total = numerator + np.asarray(before, dtype=object)
        assert np.array_equal(
            np.asarray(after.now, dtype=object), np.asarray(line.now, dtype=object) + total // wall
        )
        assert (
            np.array_equal(np.asarray(remainder, dtype=object), total % wall)
            and after.now.dtype == line.now.dtype
        )
        assert (
            after.before is line.before and after.remainder is line.remainder
        )  # the write touches the level now alone
    back, origin = node.held_write_at(lines, numerators, walls, kept, -1)
    assert all(np.array_equal(a.now, b.now) for a, b in zip(back, state.lines, strict=True))
    assert all(np.array_equal(a, b) for a, b in zip(origin, state.write_remainders, strict=True))

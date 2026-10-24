"""The asynchronous local run (the owner's word of 2026-10-24: run whatever Nodes you want, independent of the others, only the same number of ticks at the end): the folded Universe24's torus cut in two tiles along x, each a lattice of its own over its slab and one-Link halos, each advancing a tick from its own state and its halos at the tick before (the one constraint on every Link, the two ends' ticks a tick apart at most), the halos exchanged after; the tiles' interiors equal the one board's every line, write remainder and phase line at every tick, bit for bit, over the 28 intervals before the first meeting, and at the meeting the one act that reads the whole lattice is named (the births' count by the board's sum; the click's books are the board's own, 0.6 (iii) of the architect's design)."""

import json
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe import records, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws_universe import UNIVERSE, bare_torus

INTERVALS, SIDE = 32, 3  # through the births at 29 (28 before them on the 5-cube to 2026-10-24)
TILES = (
    {"x": [0, 1]},
    {"x": [2]},
)  # the two slabs' interiors along x; the halos one layer each side


def layers_of(interior: list[int]) -> list[int]:
    """A tile's layers along x on the torus: the halo before, the interior, the halo after."""
    return [(interior[0] - 1) % SIDE, *interior, (interior[-1] + 1) % SIDE]


def tile_world(folder: Path, layers: int) -> Path:
    """The tile's world: the one universe over the tile's layers along x and the board's other two sides."""
    (folder / "u.json").write_text(UNIVERSE.read_text(encoding="utf-8"), encoding="utf-8")
    world = {"universe": "u.json", "shape": [layers, SIDE, SIDE], "intervals": INTERVALS}
    path = folder / f"tile_{layers}.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    return path


def taken(array: Any, layers: list[int]) -> np.ndarray:
    """The torus's layers along x gathered into a tile's array, a copy."""
    return np.asarray(array)[layers]


def imposed(tile: Lattice, whole: list[Any], layers: list[int]) -> None:
    """The tile's whole state (lines, write remainders, phase lines) set from the board's arrays over its layers, every record a new one."""
    for state, (lines, remainders, phases) in zip(tile.states, whole, strict=True):
        state.lines = [records.Record(*(taken(a, layers) for a in line)) for line in lines]
        state.write_remainders = [taken(r, layers) for r in remainders]
        state.phases = [
            [records.Record(*(taken(a, layers) for a in line)) for line in row] for row in phases
        ]


def arrays_of(board: Lattice) -> list[Any]:
    """Every family's lines, write remainders and phase lines as arrays."""
    return [
        (
            [(line.now, line.before, line.remainder) for line in state.lines],
            list(state.write_remainders),
            [[(line.now, line.before, line.remainder) for line in row] for row in state.phases],
        )
        for state in board.states
    ]


def merged(tiles: list[Lattice], interiors: list[list[int]], shape: tuple[int, ...]) -> list[Any]:
    """The board's arrays from the tiles' interiors (each tile's layers 1 onward up to its last halo), the halos left out."""
    found = []
    for index in range(len(tiles[0].states)):
        parts = [arrays_of(tile)[index] for tile in tiles]

        def put(part: int, *path: int, parts: list[Any] = parts) -> np.ndarray:
            pieces = []
            for tile_part, interior in zip(parts, interiors, strict=True):
                a = tile_part[part]
                for step in path:
                    a = a[step]
                pieces.append((interior, np.asarray(a)[1 : 1 + len(interior)]))
            whole = np.zeros(shape, dtype=pieces[0][1].dtype)
            for interior, piece in pieces:
                whole[interior] = piece
            return whole

        lines = [tuple(put(0, k, j) for j in range(3)) for k in range(len(parts[0][0]))]
        remainders = [put(1, k) for k in range(len(parts[0][1]))]
        phases = [
            [tuple(put(2, r, k, j) for j in range(3)) for k in range(len(parts[0][2][r]))]
            for r in range(len(parts[0][2]))
        ]
        found.append((lines, remainders, phases))
    return found


def differences(whole: list[Any], board: Lattice) -> list[tuple[Any, ...]]:
    """Every array of the tiles' merged state that differs from the board's, named by family, line and part."""
    found: list[tuple[Any, ...]] = []
    for family, ((lines, remainders, phases), state) in zip(
        board.families, zip(whole, board.states, strict=True), strict=True
    ):
        kept_lines = [(line.now, line.before, line.remainder) for line in state.lines]
        kept_phases = [[(line.now, line.before, line.remainder) for line in row] for row in state.phases]
        for k, (line, kept) in enumerate(zip(lines, kept_lines, strict=True)):
            found += [
                (family.name, "line", k, part)
                for part in range(3)
                if not np.array_equal(line[part], kept[part])
            ]
        found += [
            (family.name, "write remainder", k)
            for k, (a, b) in enumerate(zip(remainders, state.write_remainders, strict=True))
            if not np.array_equal(a, b)
        ]
        for r, (row, kept_row) in enumerate(zip(phases, kept_phases, strict=True)):
            for k, (line, kept) in enumerate(zip(row, kept_row, strict=True)):
                found += [
                    (family.name, "phase row", r, "line", k, part)
                    for part in range(3)
                    if not np.array_equal(line[part], kept[part])
                ]
    return found


def test_two_tiles_with_skewed_clocks_hold_the_boards_integers_through_the_births(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Equal bit for bit over 32 intervals in either order of the tiles' ticks, through the first meeting at 29: every birth pays by the hole at its own Node and no act reads beyond one Link (the owner's word, everything local, 2026-10-24), so the tiles' interiors are the board's every line, write remainder and phase line; the births read from the board's lines, a proton pair at every one of the 27 Nodes at the senses -1 and 1. To 2026-10-24 the test ran the 5-cube to 28 and named the births' count summed over the board as the one non-local act; that act left with the fold's local births."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(bare_torus(tmp_path, SIDE, INTERVALS)), output=lines.append)
    interiors = [tile["x"] for tile in TILES]
    layers = [layers_of(interior) for interior in interiors]
    tiles = [
        Lattice(load_world(tile_world(tmp_path, len(rows))), output=lambda line: None) for rows in layers
    ]
    whole = arrays_of(board)
    for tile, rows in zip(tiles, layers, strict=True):
        imposed(tile, whole, rows)
    skew = 0
    for interval in range(1, INTERVALS + 1):
        board.step()
        first, second = (
            tiles if interval % 2 else tiles[::-1]
        )  # either order: each from its halos at the tick before
        first.step()
        skew = max(skew, first.interval - second.interval)
        second.step()
        whole = merged(
            tiles, interiors, board.shape
        )  # the halos exchanged: each tile re-imposed from the two interiors
        for tile, rows in zip(tiles, layers, strict=True):
            imposed(tile, whole, rows)
        assert differences(whole, board) == [], interval
    born = [line for line in lines if line["event"] == "birth"]
    assert len(born) == SIDE**3 and all(line["interval"] == 29 for line in born)  # every Node alike
    assert all(line["children"] == ["proton"] * 2 and line["senses"] == [-1, 1] for line in born)
    assert skew == 1 and board.interval == tiles[0].interval == tiles[1].interval == INTERVALS

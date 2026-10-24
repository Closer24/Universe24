"""The asynchronous local run (the owner's word of 2026-10-24: run whatever Nodes you want, independent of the others, only the same number of ticks at the end): the folded Universe24's torus cut in two tiles along x, each a lattice of its own over its slab and one-Link halos, each advancing a tick from its own state and its halos at the tick before (the one constraint on every Link, the two ends' ticks a tick apart at most), the halos exchanged after; the tiles' interiors equal the one board's every line, write remainder and phase line at every tick, bit for bit, over the 28 intervals before the first meeting, and at the meeting the one act that reads the whole lattice is named (the births' count by the board's sum; the click's books are the board's own, 0.6 (iii) of the architect's design)."""

import json
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe import records, seed, world_files
from event_universe.emission import emitted_lines
from event_universe.lattice import Lattice
from event_universe.lay import laid
from event_universe.loader.circle import vector_of
from event_universe.slabs import arrays_of, imposed, layers_of, rebuilt, tile_layers
from event_universe.world_files import load_world
from tests.laws_universe import bare_torus, small_universe

# the births at 30 since the close reads the interval's start (the branch digit-order; 29 when it read the state after the step); through the births at 29 and one past (28 before them on the 5-cube to 2026-10-24; 32 shortened under the suite's bound)
INTERVALS, SIDE, BIRTH = 26, 3, 24
# the two slabs' interiors along x; the halos one layer each side
TILES = (range(0, 2), range(2, 3))


def tile_world(folder: Path, layers: int) -> Path:
    """The tile's world: the one universe over the tile's layers along x and the board's other two sides."""
    small_universe(folder)
    world = {"universe": "u.json", "shape": [layers, SIDE, SIDE], "intervals": INTERVALS}
    path = folder / f"tile_{layers}.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    return path


def tiles_of(folder: Path, whole: list[Any]) -> tuple[list[Lattice], list[list[int]]]:
    """The two tiles, each a lattice over its layers (the halo before, the interior, the halo after) with every array over the Nodes imposed from the board's arrays `whole` over those layers, and the layers."""
    layers = [tile_layers(interior, SIDE) for interior in TILES]
    tiles = [
        Lattice(load_world(tile_world(folder, len(rows))), output=lambda line: None) for rows in layers
    ]
    for tile, rows in zip(tiles, layers, strict=True):
        rebuilt(tile, layers_of(whole, 0, rows))
    return tiles, layers


def exchanged(tiles: list[Lattice], layers: list[list[int]], whole: list[Any]) -> list[Any]:
    """The halos exchanged: the board's arrays from the tiles' interiors (each tile's layers 1 onward up to its last halo, the halos left out), every tile re-imposed from the two interiors; the board's arrays returned."""
    for tile, interior in zip(tiles, TILES, strict=True):
        own = layers_of(arrays_of(tile), 0, list(range(1, len(interior) + 1)))
        whole = imposed(whole, 0, list(interior), own)
    for tile, rows in zip(tiles, layers, strict=True):
        rebuilt(tile, layers_of(whole, 0, rows))
    return whole


def differences(whole: list[Any], board: Lattice) -> list[int]:
    """Every array of the tiles' merged state that differs from the board's, by its index in `slabs.arrays_of`'s order (every line's three arrays, the write remainders, the phase lines, the time count, the closes)."""
    return [
        k
        for k, (a, b) in enumerate(zip(whole, arrays_of(board), strict=True))
        if not np.array_equal(a, b)
    ]


def test_two_tiles_with_skewed_clocks_hold_the_boards_integers_through_the_births(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Equal bit for bit over 30 intervals in either order of the tiles' ticks, through the first meeting at 29: every birth pays by the hole at its own Node and no act reads beyond one Link (the owner's word, everything local, 2026-10-24), so the tiles' interiors are the board's every line, write remainder and phase line; the births read from the board's lines, a proton pair at every one of the 27 Nodes at the senses -1 and 1. To 2026-10-24 the test ran the 5-cube to 28 and named the births' count summed over the board as the one non-local act; that act left with the fold's local births."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(bare_torus(tmp_path, SIDE, INTERVALS)), output=lines.append)
    tiles, layers = tiles_of(tmp_path, arrays_of(board))
    skew = 0
    for interval in range(1, INTERVALS + 1):
        board.step()
        # either order: each from its halos at the tick before
        first, second = tiles if interval % 2 else tiles[::-1]
        first.step()
        skew = max(skew, first.interval - second.interval)
        second.step()
        assert differences(exchanged(tiles, layers, arrays_of(board)), board) == [], interval
    born = [line for line in lines if line["event"] == "birth"]
    # the hole seed's first birth by the draw at the hole's side (2026-10-24; every Node alike at 24 under the uniform sea to that day)
    assert born and born[0]["interval"] <= BIRTH
    # the points the fit picks, named by their vectors
    assert all(vector_of(c) is not None for line in born for c in line["children"])
    # one record per child, the senses summing to 0 (2026-10-24)
    assert all(sum(line["senses"]) == 0 for line in born)
    assert skew == 1 and board.interval == tiles[0].interval == tiles[1].interval == INTERVALS


def sea_plus_one_or_hole(hole: bool) -> Any:
    """The seed hand's S1 (the sea plus one quantum at the origin) or S2 (the sea with the origin empty), a test's seed laid as the law's own is."""

    def laid_seed(board: Lattice, index: int) -> None:
        family, drift = board.families[index], seed.drift_of(board.world.quantum_action)
        first, zeros = records.record_slice(family, 0).start, records.zeros(board.shape, board.kind)
        sea = records.full(board.shape, drift, board.kind)
        if hole:
            sea[0, 0, 0] = 0
        for line in emitted_lines(family):
            laid(board, index, first + line, (sea, zeros), None, None)
        if not hole:
            mask = board.mask(((0, 0, 0),))
            for line in emitted_lines(family):
                laid(board, index, first + line, (np.where(mask, drift, 0), zeros), None, None, mask)

    return laid_seed


@pytest.mark.parametrize("hole", [False, True])
def test_two_tiles_hold_a_structured_seed_through_its_drawn_whethers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, hole: bool
) -> None:
    """S1 and S2 through the one-Link tiles with skewed clocks over 20 intervals, through the drawn whethers and the births at the lit Nodes: equal bit for bit (the close reads the interval's start and every face before any write; the seed hand's finding of 2026-10-24 parted them at the first drawn whether)."""
    monkeypatch.setattr(seed, "uniform_seed", sea_plus_one_or_hole(hole))
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    lines: list[dict[str, Any]] = []
    board = Lattice(load_world(tile_world(tmp_path, SIDE)), output=lines.append)
    tiles, layers = tiles_of(tmp_path, arrays_of(board))
    for interval in range(1, 21):
        board.step()
        first, second = tiles if interval % 2 else tiles[::-1]
        first.step()
        second.step()
        assert differences(exchanged(tiles, layers, arrays_of(board)), board) == [], interval
    assert any(line["event"] == "birth" for line in lines)

"""The charge written is the Wronskian over T div 2 for every reader (ALGEBRA.md, The constants, the law's sentence of 2026-10-24 on the owner's word of that morning, the charge universal like nature; the former clause of the same day, each reader's Wronskian times 3 T den over its own count unit, kept by name as the defect: the electron's factor 1,822 times the proton's on the one universe file, one born electron written as 1,822 proton charges, the sign holder's row running away; the old "one ratio per holder, E_h T num / (Gamma den)" of 2026-10-23 kept by name too): the holder of the sign carries one alpha = E_h T / Gamma with any pairs under it (`loader/derived.alpha_of`), and each reader's Wronskian enters the holder's one write at the factor 1 over the one wall 2 E_s T Gamma (`loader/derived.held_write_of`, `loader/charge.charge_factors`), so that a quantum of every plane family, W = T div 2 at the birth's quarter-turn lay, writes the same charge, proven on the engine's own write of one quantum of each of the small den's two points (the former file's rows by hand, the register's bound, the holder's course bound and the lightest point struck 2026-10-24 with the tests' audit: duplicates, or the loader's bookkeeping and no sentence of the Node)."""

from __future__ import annotations

import json

import numpy as np

from event_universe import records, registry, world_files
from event_universe.emission import laid_by_count
from event_universe.features.click import amplitude
from event_universe.lattice import Lattice
from event_universe.take import Item
from event_universe.world_files import load_world
from tests.laws_universe import SMALL, small_universe

T = 36_000
SIGN_ROW = "sign"  # the loader's own name for the holder of the sign (loader/universe.SIGN)


def bare_board(tmp_path, monkeypatch, output=None):  # type: ignore[no-untyped-def]
    """The tests' small universe on the bare 3-cube torus, the law's uniform seed of light and nothing else (tests.laws_universe.SMALL, den 1,021 with its two points)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    small_universe(tmp_path)
    world = {"universe": "u.json", "shape": [3, 3, 3], "intervals": 40}
    (tmp_path / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    return Lattice(load_world(tmp_path / "bare.json"), output=output)


def points_of(board: Lattice) -> list[str]:
    """The plane rows of the board's universe by name, the heavier point first (the larger s)."""
    planes = [f for f in board.families if f.plane]
    return [f.name for f in sorted(planes, key=lambda f: f.pair[0])]


def holder_rows(board: Lattice) -> list[int]:
    """The largest level of each row of the holder of the sign's time line (the free row 0, then one per charged family)."""
    charge = [f.name for f in board.families].index(SIGN_ROW)
    width, rows = (
        board.families[charge].width,
        registry.records_of(board.families[charge], board.states[charge].lines),
    )
    lines = board.states[charge].lines
    return [int(np.abs(np.asarray(lines[row * width].now, dtype=object)).max()) for row in range(rows)]


def test_equal_wronskians_of_two_families_write_equal_charge(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The charge written is the Wronskian over T div 2 for every reader (ALGEBRA.md, The constants, 2026-10-24): one quantum of the proton and one of the electron, each laid at a Node in the birth's own form (the count's lay at the massless pair, one sense, W = -A^2 = -17,956), write the same level into the holder of the sign in one interval, 18 each on this file (the former factor wrote the electron's 1,822 times the proton's, 16,427 against 9 per interval)."""
    written = {}
    small = SMALL["integers"]["den"]
    for name in points_of(bare_board(tmp_path, monkeypatch)):
        board = bare_board(tmp_path, monkeypatch)
        names = [f.name for f in board.families]
        index, den = names.index(name), board.families[names.index(name)].pair[1]
        laid_by_count(board, Item(index, 1, ((1, 1, 1),), (den, den), sense=-1))
        wronskian = int(
            np.asarray(records.wronskian(board.lines_of(index, 0), True), dtype=object)[1, 1, 1]
        )
        board.step()
        written[name] = (wronskian, max(holder_rows(board)))
    heavier, lighter = points_of(board)
    assert written[heavier][0] == written[lighter][0] == -(amplitude(1, T, (small, small), 1) ** 2)
    assert written[heavier][1] == written[lighter][1] > 0

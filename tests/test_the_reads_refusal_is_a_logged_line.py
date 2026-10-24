"""A refusal by name is a logged line, never a crash of the universe (ALGEBRA.md, The click's read of the board; The board reads itself; 2026-10-24, the gravity-top hand's finding under the gapped holder on the lean board: an empty gapped Node stands at the exact vacuum paces until light drifts in, and the read's coarse refusal rose out of the board's own close): on the small universe's 3-cube with the holder of the volume at the gapped pair (den - den div Gamma, den) through `loader/universe.volume_pair`, the hole seed runs 20 intervals with the refusal logged at the origin by its name and the light standing, no exception, and births elsewhere."""

from __future__ import annotations

import numpy as np

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.loader import universe
from event_universe.world_files import load_world
from tests.laws_universe import SMALL, bare_torus


def test_a_refused_read_at_the_board_is_a_logged_line_and_the_run_goes_on(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    gamma = SMALL["integers"]["node_clock"]
    monkeypatch.setattr(universe, "volume_pair", lambda den: (den - den // gamma, den))
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_world(bare_torus(tmp_path, 3, 20)), output=lines.append)
    volume = next(k for k, family in enumerate(board.families) if family.name == universe.VOLUME)
    assert (
        board.families[volume].pair[0] != board.families[volume].pair[1]
    )  # the gapped holder through the hook
    for _ in range(20):
        board.step()
        assert int(np.asarray(board.share_of(board.world.seed)[0], dtype=object).sum()) > 0
    refused = [
        row
        for row in lines
        if row.get("event") == "refused" and row["cause"] in ("vacuum", "origin", "unit")
    ]
    assert refused and all(row["node"] == [0, 0, 0] for row in refused if row["cause"] == "vacuum")
    assert any(row.get("event") == "birth" and row["nodes"][0] != [0, 0, 0] for row in lines)

"""THE CLICK IS THE COUNT'S LINE (the model owner's word of 2026-09-29 on #1495, decision (c); ALGEBRA.md #the-counts-line): the count is the family's, a body's quanta of another family are that family's count at its Nodes (laid there by the carried division, none lost), a detector reports the net inflow of a count across its Nodes; the signed read has no floor, so the light band that reads the held rows' ringing below zero is refused by name."""

from __future__ import annotations

import pytest

import event_universe.world_files as world_files
from event_universe.game_board import GameBoard
from event_universe.loader.world import spread
from event_universe.world_files import load_world
from tests.laws import ROOT, chain_body_world, load_file

TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")


def test_held_quanta_are_the_other_familys_count_at_the_bodys_nodes_and_the_light_band_is_refused(
    tmp_path, monkeypatch
):
    """The taker holds 64 quanta of the charge, laid over its Nodes in proportion to its counts with the remainder carried (their sum 64 exactly), so the charge's count at its Nodes is 64 after the lay, and every net rise of a count across its Nodes is a `gather` line naming it; with the charge on the light band [6000, 6000] (its edge P = Gamma) the binding row's tail ringing below zero beside the bodies takes the charge's pace above the edge, and the run ends by the guard's name within 400 intervals (the finding: no floor, as the owner's decision (c) has it)."""
    assert spread(64, (1, 3, 5, 7)) == (4, 12, 20, 28) and sum(spread(10, (3, 3, 3))) == 10
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL, taker_at=200, holds={"charge": 64})
    lines: list[dict[str, object]] = []
    board = GameBoard(load_world(world), lines.append)
    board.step()
    assert board.contents()[1]["charge"] == 64 and board.contents()[0]["charge"] == 0
    with pytest.raises(RuntimeError, match=r"above the stability edge 6000 of its pair \[6000, 6000\]"):
        for _ in range(399):
            board.step()
    gathers = [line for line in lines if line["event"] == "gather"]
    assert gathers and all(line["detector"] == "taker" and line["taker"] == 1 for line in gathers)

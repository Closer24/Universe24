"""A BOUND BODY (ALGEBRA.md #the-generator, #what-a-body-is, #the-counts-line): the pixel tool lays a body, the GameBoard admits its declared count within 2 isqrt(c) + 1 of the count its family's form lays at its Nodes and refuses one beyond it by name, and the body stands with its quanta in its Nodes, which follow its count."""

from __future__ import annotations

import json

import numpy as np
import pytest

import event_universe.world_files as world_files
from event_universe import node
from event_universe.game_board import GameBoard
from event_universe.world_files import input_digest, load_world
from tests.laws import BODY_24 as QUANTA
from tests.laws import ROOT, body_at_24, chain_body_world, load_file

TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")


def test_the_laid_body_is_admitted_and_a_count_far_from_its_form_is_refused_by_name(
    tmp_path, monkeypatch
):
    """The count is laid from the family's form at the wall 3 den T within the law's tolerance of the declared count, every Node of the body carrying a quantum; a declared count off the form by more than 2 isqrt(c) + 1 ends the run at the lay by name."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = body_at_24(tmp_path, TOOL)
    document = json.loads(world.read_text(encoding="utf-8"))
    board = GameBoard(load_world(world))
    declared = board.bodies[0].nodes.copy()
    board.step()
    count = board.states[3].count
    assert count is not None
    laid = int(count[declared].sum())
    assert abs(laid - QUANTA) <= 2 * int(QUANTA**0.5) + 1 and int(count[declared].min()) >= 1
    for line in document["measured"][0]["nodes"]:
        line["count"] = (
            1  # far below the form (a larger count would first trip the pace guard at Gamma = 24)
        )
    world.write_text(json.dumps(document), encoding="utf-8")
    mode_path = world.with_suffix(".mode.json")
    mode = json.loads(mode_path.read_text(encoding="utf-8"))
    mode["world_digest"] = input_digest(document)
    mode_path.write_text(json.dumps(mode), encoding="utf-8")
    with pytest.raises(ValueError, match="a declared count is within 2 isqrt"):
        GameBoard(load_world(world)).step()


def test_a_chain_body_at_gamma_6000_keeps_its_quanta_over_a_hundred_intervals(tmp_path, monkeypatch):
    """A BOUND BODY STANDS: on the universe of Gamma 6000 (no holder of the sign, so the body gives nothing) a body of six hundred quanta laid by the pixel tool keeps at least nineteen of every twenty laid quanta on its Nodes and their Links over a hundred intervals, its family's total conserved to the bit, no hole in its Nodes, which are where its count stands."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL)
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    universe["families"] = [row for row in universe["families"] if row["name"] != "charge"]
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    board = GameBoard(load_world(world))
    body, matter = board.bodies[0], board.states[2]
    inset = body.nodes.copy()
    near = inset | np.roll(inset, 1, axis=0) | np.roll(inset, -1, axis=0)
    board.step()
    assert matter.count is not None and matter.count_remainder is not None
    wall, laid = node.count_wall(board.families[2], 32768), int(matter.count.sum())
    total = int((wall * matter.count.astype(object) + matter.count_remainder).sum())
    assert abs(laid - 600) <= 2 * 24 + 1
    for _ in range(99):
        board.step()
        assert int(matter.count[inset].min()) >= 0 and 20 * int(matter.count[near].sum()) >= 19 * laid
        assert int((wall * matter.count.astype(object) + matter.count_remainder).sum()) == total
        assert not (body.nodes & (matter.count == 0)).any() and body.corner()[1:] == [0, 0]

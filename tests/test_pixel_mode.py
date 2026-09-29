"""THE GENERATOR IS RULE3 (ALGEBRA.md #the-generator): the pixel tool lays a body as the fixed point of its binding row, refusing a cloud, a collapse, a universe without T and two bodies sharing a region by name."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import event_universe.world_files as world_files
from event_universe.game_board import GameBoard
from event_universe.world_files import input_digest, load_world
from tests.laws import BODY_24 as QUANTA
from tests.laws import body_at_24, load_file

TOOL = load_file("pixel_mode", Path(__file__).resolve().parents[1] / "tools" / "pixel_mode.py")


def test_a_body_is_laid_over_its_nodes_as_the_fixed_point_of_its_row_and_loads_lawful(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = body_at_24(tmp_path, TOOL)
    document = json.loads(world.read_text(encoding="utf-8"))
    mode = json.loads((tmp_path / "body.mode.json").read_text(encoding="utf-8"))
    nodes = document["measured"][0]["nodes"]  # the one declared Node became the body's Nodes
    laid = sum(entry["count"] for entry in nodes)
    assert len(nodes) > 1 and all(entry["count"] >= 1 for entry in nodes)
    assert (abs(laid - QUANTA) - (abs(laid - QUANTA) & 1)) ** 2 <= 4 * QUANTA  # within the rounding
    entry, (a, den) = mode["bodies"][0], mode["bodies"][0]["clock"]
    assert TOOL.agree(entry["carried"], QUANTA) and entry["count"] == QUANTA and entry["seed"] >= 1
    assert (
        2 * 16 * den < a * 24 and a < 2 * den
    )  # bound: above the matter band's top 2 x 16 / 24, below 2
    profile, peak = entry["profile"], entry["amplitude"]
    assert (
        max(map(abs, profile)) == abs(profile[(6 * 13 + 6) * 13 + 6]) == peak > 0
    )  # the peak at the centre
    assert entry["period"][1] == 2 and entry["period"][0] >= 4 and "twist" not in entry
    assert entry["moving"]["now"] == profile and len(entry["moving"]["before"]) == len(profile) == 13**3
    assert entry["pair"] == [16, 24] and entry["family"] == "matter" and "wavelength" not in entry
    assert mode["world_digest"] == input_digest(document)
    matter = GameBoard(load_world(world)).states[3].levels  # LAWFUL, the family's two levels
    assert matter is not None and matter.now[6, 6, 6] == peak
    assert matter.before.ravel().tolist() == entry["moving"]["before"]


def test_a_cloud_a_collapse_a_universe_without_t_and_two_bodies_in_one_region_are_refused_by_name(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    with pytest.raises(ValueError, match="is a cloud: its standing reading rotates"):
        body_at_24(tmp_path, TOOL, quanta=12)  # below the window of mass
    with pytest.raises(ValueError, match="collapses: its wells reach the pace 0"):
        body_at_24(tmp_path, TOOL, quanta=48)  # above it: the Link's pace reaches 0
    document = json.loads(body_at_24(tmp_path, TOOL, mode=False).read_text(encoding="utf-8"))
    document["measured"].append(
        {**document["measured"][0], "nodes": [{"node": [8, 6, 6], "count": QUANTA}]}
    )
    with pytest.raises(
        ValueError, match="measured\\[1\\] and measured\\[0\\] share a Node in their regions"
    ):
        TOOL.pixel_mode(document)
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    del universe["integers"]["quantum_action"]
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    with pytest.raises(ValueError, match="declares no quantum_action T"):
        TOOL.pixel_mode(document)

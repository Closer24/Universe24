"""The generator is Rule3 (ALGEBRA.md #the-generator): the generator lays a body as the fixed point of the row it reads, its declared count the weighted share its record lays, a body rotating in a sense beside its record, refusing a cloud, a body that fits no positive pace, a universe without T and two bodies sharing a region by name."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import event_universe.world_files as world_files
from event_universe.game_board import GameBoard
from event_universe.world_files import input_digest, load_world
from tests.laws import CHAIN, QUANTA, chain_body_world, load_file

TOOL = load_file("pixel_mode", Path(__file__).resolve().parents[1] / "tools" / "pixel_mode.py")


def test_a_body_is_laid_over_its_nodes_as_the_fixed_point_of_its_row_and_loads_lawful(
    tmp_path, monkeypatch
):
    """One Node declaring 50 quanta on the chain becomes a body of several Nodes, each carrying a quantum, their counts within the rounding of 50; its standing reading rotates above the matter band's top and below 2, its peak at the centre, its period read whole; the mode file stands for the world by its digest and the GameBoard loads its levels as written; a body laid with a sense carries its second level pair beside them, a neutral one none."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL)
    document = json.loads(world.read_text(encoding="utf-8"))
    mode = json.loads(world.with_suffix(".mode.json").read_text(encoding="utf-8"))
    nodes = document["measured"][0]["nodes"]  # the one declared Node became the body's Nodes
    laid = sum(entry["count"] for entry in nodes)
    assert len(nodes) > 1 and all(entry["count"] >= 1 for entry in nodes)
    assert (abs(laid - QUANTA) - (abs(laid - QUANTA) & 1)) ** 2 <= 4 * QUANTA  # within the rounding
    entry, (a, den) = mode["bodies"][0], mode["bodies"][0]["clock"]
    assert TOOL.agree(entry["carried"], QUANTA) and entry["count"] == QUANTA and entry["seed"] >= 1
    assert 2 * 4000 * den < a * 6000 and a < 2 * den  # above the band's top 2 x 4000 / 6000, below 2
    profile, peak = entry["profile"], entry["amplitude"]
    assert max(map(abs, profile)) == abs(profile[CHAIN // 2]) == peak > 0  # the peak at the centre
    assert entry["period"][1] == 2 and entry["period"][0] >= 4 and "im_now" not in entry["moving"]
    assert entry["moving"]["now"] == profile and len(entry["moving"]["before"]) == len(profile) == CHAIN
    assert entry["pair"] == [4000, 6000] and entry["family"] == "matter"
    assert mode["world_digest"] == input_digest(document)
    matter = GameBoard(load_world(world)).states[3].levels  # lawful, the family's two levels
    assert matter is not None and matter.now[CHAIN // 2, 0, 0] == peak
    assert matter.before.ravel().tolist() == entry["moving"]["before"]
    turned = chain_body_world(tmp_path, TOOL, senses=(-1,))
    rotating = json.loads(turned.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"][0]
    assert any(rotating["moving"]["im_now"]) and len(rotating["moving"]["im_before"]) == CHAIN


def test_a_cloud_a_collapse_a_universe_without_t_and_two_bodies_in_one_region_are_refused_by_name(
    tmp_path, monkeypatch
):
    """Three quanta are a cloud, below the window of mass; four hundred fit no cube with a positive pace on the chain, above it; two bodies of fifty two Links apart collapse, their wells reaching the pace 0; two small bodies whose regions share a Node, a universe without T and a sense other than +1 or -1 are refused by name."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    with pytest.raises(ValueError, match="is a cloud: its standing reading rotates"):
        chain_body_world(tmp_path, TOOL, quanta=3)
    with pytest.raises(ValueError, match="fits no cube on this board with a positive pace"):
        chain_body_world(tmp_path, TOOL, quanta=400)
    document = json.loads(chain_body_world(tmp_path, TOOL, mode=False).read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="a sense is \\+1 or -1"):
        TOOL.pixel_mode(json.loads(json.dumps(document)), [2])
    near = {"family": "matter", "nodes": [{"node": [CHAIN // 2 + 2, 0, 0], "count": QUANTA}]}
    with pytest.raises(ValueError, match="collapses: its wells reach the pace 0"):
        TOOL.pixel_mode({**document, "measured": [*document["measured"], near]})
    small = [{"family": "matter", "nodes": [{"node": [x, 0, 0], "count": 8}]} for x in (20, 23)]
    with pytest.raises(
        ValueError, match="measured\\[1\\] and measured\\[0\\] share a Node in their regions"
    ):
        TOOL.pixel_mode({**document, "measured": small})
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    del universe["integers"]["quantum_action"]
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    with pytest.raises(ValueError, match="declares no quantum_action T"):
        TOOL.pixel_mode(document)

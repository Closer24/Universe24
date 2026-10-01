"""The generator is Rule3 (ALGEBRA.md #the-generator): the generator lays a body as the fixed point of the row it reads, its declared count the weighted share its record lays, a body rotating in a sense beside its record, refusing a cloud, a body that fits no positive pace, a universe without T and two bodies sharing a region by name; it lays a message as the wave under its envelope by the rotation act, and an inner face of the board (the face rule inside it) reflects the wave but for its gap, the gate MATCH."""

from __future__ import annotations

import json
import math

import numpy as np
import pytest

import event_universe.world_files as world_files
from event_universe.game_board import GameBoard
from event_universe.world_files import input_digest, load_world
from tests.laws import CHAIN, PACKET, QUANTA, ROOT, SLIT, chain_body_world, load_file, slit_world

TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")


def dense(levels: dict[str, list[int]]) -> np.ndarray:
    """A level of the mode file's sparse form as the slit board's array."""
    return np.bincount(levels["at"], levels["values"], 24 * 9).astype(np.int64).reshape(24, 9, 1)


BACK = load_file("back_in_time", ROOT / "tools" / "back_in_time.py")


def test_a_message_is_the_wave_under_its_envelope_and_an_inner_face_reflects_it_but_for_its_gap(
    tmp_path, monkeypatch
):
    """The message lay: now_i = b e_i cos(k x_i) and before_i = b e_i cos(k x_i + omega) at k = pi / 4 along x, b = 1,328, the raised cosine of half-width 4 about x = 5, within one unit of the real numbers at the packet's Nodes (the rotation act and the fixed point of the division act, no table); the loader admits the folded board and refuses by name a detector Node, a body Node and a laid level beyond the inner face, faces that leave no Node, a detector's declared remainders at or above W_c, on a family carrying no count, on a detector that reads a body or not one per Node, and a message's `whole` Node (no family's line lays a count whole today); a packet toward -x at the phase pi / 2 with the transverse wave number pi / 8 along y (`wave` [-1, 4], `phase` [1, 4], `transverse` {y: [1, 8]}) is laid as its mirror at that slant within one unit, its band's omega with cos k_y, and a transverse wave number on the along axis is refused by name; the screen's declared remainders stand at its Nodes after the first act (the half wall elsewhere) and its click lines are the whole quanta entering its column through its two boundary Ports along x, none through a Port between two of its Nodes; in the run the Nodes beyond the board stay 0 in every family and no quantum crosses their Links (SUM (W_c c + r) kept to the bit), the wave passes the gap (the light's levels beyond the wall, more in the gap's row than at the board's edge) and reflects elsewhere (more of its form before the wall than on the same board without the wall); the back-in-time gate says MATCH over the run."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    screen = {"name": "screen", "positions": [[20, y, 0] for y in range(9)]}
    screen["remainder"] = {"charge": [7] * 8 + [9]}
    path = slit_world(tmp_path, TOOL, detectors=[screen])
    mode_file = path.with_suffix(".mode.json")
    mode = json.loads(mode_file.read_text(encoding="utf-8"))["messages"][0]
    now, before = (dense(mode["moving"][word]) for word in ("now", "before"))
    k, omega = math.pi / 4, math.acos((math.cos(math.pi / 4) + 2) / 3)
    for x in range(24):
        away = abs(x - 5)
        e = (1 + math.cos(math.pi * away / 4)) / 2 if away <= 4 else 0
        assert abs(now[x, 4, 0] - 1328 * e * math.cos(k * x)) <= 1
        assert abs(before[x, 4, 0] - 1328 * e * math.cos(k * x + omega)) <= 1
    assert (now[:, 4:5, :] == now).all() and mode["count"] > 0 and not now[12].any()
    inner, at = "beyond the board's inner face", {"node": [12, 0, 0], "count": 50}
    with pytest.raises(ValueError, match=f"{inner}: nothing stands there"):
        load_world(slit_world(tmp_path, TOOL, "r", detectors=[{"name": "d", "positions": [[12, 0, 0]]}]))
    with pytest.raises(ValueError, match="faces leave no Node"):
        load_world(slit_world(tmp_path, TOOL, "r", faces=[{"axis": "z", "at": 0, "gaps": []}]))
    with pytest.raises(ValueError, match=r"whole names the Node \[5, 4, 0\]: no line of the family"):
        load_world(slit_world(tmp_path, TOOL, "r", messages=[{**PACKET, "whole": [5, 4, 0]}]))
    with pytest.raises(ValueError, match="unknown key 'remainder'"):  # no count stands at a Node
        entry = {**screen, "name": "d", "remainder": {"charge": 1}}
        load_world(slit_world(tmp_path, TOOL, "r", detectors=[entry]))
    aslant = {**PACKET, "wave": [-1, 4], "phase": [1, 4], "transverse": {"y": [1, 8]}}
    turned = slit_world(tmp_path, TOOL, "turned", messages=[aslant])
    before = json.loads(turned.with_suffix(".mode.json").read_text())["messages"][0]["moving"]["before"]
    mirrored = dense(before)
    tilted = math.acos((math.cos(math.pi / 4) + math.cos(math.pi / 8) + 1) / 3)  # the band with k_y
    for x in range(
        24
    ):  # toward -x at the phase pi / 2, k_y = pi / 8: b e cos(-k x + k_y y + pi / 2 + omega), k_y y = pi / 2 at y = 4
        away = abs(x - 5)
        e = (1 + math.cos(math.pi * away / 4)) / 2 if away <= 4 else 0
        assert abs(mirrored[x, 4, 0] - 1328 * e * math.cos(-k * x + math.pi + tilted)) <= 1
    with pytest.raises(ValueError, match="transverse holds the unknown key 'x'"):
        load_world(slit_world(tmp_path, TOOL, "bad", messages=[{**PACKET, "transverse": {"x": [1, 8]}}]))
    with pytest.raises(ValueError, match=f"{inner}: nothing stands there"):
        TOOL.pixel_mode({**SLIT, "measured": [{"family": "matter", "nodes": [at]}]})
    tampered = json.loads(mode_file.read_text(encoding="utf-8"))
    tampered["messages"][0]["moving"]["now"]["at"].append(12 * 9)
    tampered["messages"][0]["moving"]["now"]["values"].append(5)
    mode_file.write_text(json.dumps(tampered), encoding="utf-8")
    with pytest.raises(ValueError, match=rf"is 5 at the Node \[12, 0, 0\], {inner}"):
        load_world(path)
    mode_file.write_text(json.dumps({**tampered, "messages": [mode]}), encoding="utf-8")
    lines: list[dict[str, object]] = []
    walled = GameBoard(load_world(path), lines.append)
    open_board = GameBoard(load_world(slit_world(tmp_path, TOOL, "open", faces=[])))
    charge, beyond = [family.name for family in walled.families].index("charge"), walled.wrap.beyond
    assert beyond is not None and beyond.sum() == 8 and not beyond[12, 4, 0]
    walled.step()
    clicked = [line for line in lines if line["event"] == "click"]
    assert not clicked and not walled.quanta(charge)[beyond].any()  # nothing stands beyond the face
    for _ in range(23):
        walled.step()
        open_board.step()
        risen = [line for line in lines if line["tick"] == walled.tick and line["detector"] == "screen"]
        assert all(
            line["event"] == "click" and "node" not in line and "ports" not in line for line in risen
        )  # the region's report alone, no Node named
        for state in walled.states:
            records = [r for r in (*state.parts, state.levels, state.second) if r is not None]
            assert not any(getattr(r, key)[beyond].any() for r in records for key in ("now", "before"))
        assert walled.books()["charge"]["quanta"] > 0
    level = np.abs(walled.states[charge].levels.now[:, :, 0])
    passed, free = level[13:].sum(axis=0), np.abs(open_board.states[charge].levels.now[:12]).sum()
    print(f"GAMEBOARD the slit: the light beyond the wall per row {passed.tolist()},")
    print(f"  before it {int(level[:12].sum())} against {int(free)} with no wall")
    assert passed[4] > passed[0] > 0 and level[:12].sum() > free and open_board.wrap.beyond is None
    assert BACK.verdict(GameBoard(load_world(path)), 24)["verdict"] == "MATCH"


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
    board = GameBoard(load_world(world))  # lawful, the family's two levels
    matter = board.states[[family.name for family in board.families].index("matter")].levels
    assert matter is not None and matter.now[CHAIN // 2, 0, 0] == peak
    assert matter.before.ravel().tolist() == entry["moving"]["before"]
    turned = chain_body_world(tmp_path, TOOL, senses=(-1,))
    rotating = json.loads(turned.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"][0]
    assert any(rotating["moving"]["im_now"]) and len(rotating["moving"]["im_before"]) == CHAIN


def test_a_cloud_a_collapse_a_universe_without_t_and_two_bodies_in_one_region_are_refused_by_name(
    tmp_path, monkeypatch
):
    """Three quanta are a cloud, below the window of mass (ten too, under the binding holder's range of 20 Links); three hundred fit no cube with a positive pace on the chain, above it; two bodies of a hundred two Links apart collapse, their wells reaching the pace 0; two bodies of twenty whose regions share a Node, a universe without T and a sense other than +1 or -1 are refused by name."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    with pytest.raises(ValueError, match="is a cloud: its standing reading rotates"):
        chain_body_world(tmp_path, TOOL, quanta=3)
    with pytest.raises(ValueError, match="fits no cube on this board with a positive pace"):
        chain_body_world(tmp_path, TOOL, quanta=6 * QUANTA)
    document = json.loads(chain_body_world(tmp_path, TOOL, mode=False).read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="a sense is \\+1 or -1"):
        TOOL.pixel_mode(json.loads(json.dumps(document)), [2])
    at = (CHAIN // 2, CHAIN // 2 + 2)
    heavy = [{"family": "matter", "nodes": [{"node": [x, 0, 0], "count": 2 * QUANTA}]} for x in at]
    with pytest.raises(ValueError, match="collapses: its wells reach the pace 0"):
        TOOL.pixel_mode({**document, "measured": heavy})
    small = [{"family": "matter", "nodes": [{"node": [x, 0, 0], "count": 20}]} for x in (20, 23)]
    with pytest.raises(ValueError, match=r"measured\[1\] and measured\[0\] share a Node"):
        TOOL.pixel_mode({**document, "measured": small})
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    del universe["integers"]["quantum_action"]
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    with pytest.raises(ValueError, match="declares no quantum_action T"):
        TOOL.pixel_mode(document)

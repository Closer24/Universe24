"""The generator is Rule3 (ALGEBRA.md #the-generator): the generator lays a body as the fixed point of the row it reads, its declared count the weighted share its record lays, a body rotating in a sense beside its record, refusing a cloud, a body that fits no positive pace, a universe without T and two bodies sharing a region by name; it lays a message as the wave under its envelope by the rotation act, and an inner face of the board (the face rule inside it) reflects the wave but for its gap, the gate MATCH."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pytest

import event_universe.world_files as world_files
from event_universe.game_board import GameBoard
from event_universe.world_files import input_digest, load_world
from tests.laws import CHAIN, QUANTA, ROOT, chain_body_world, load_file, universe_beside

TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
BACK = load_file("back_in_time", ROOT / "tools" / "back_in_time.py")
SLIT = dict(shape=[24, 9, 1], boundary=dict(x="open", y="open", z="periodic"), face_depth=1, ticks=24)
SLIT.update(universe="u.json", engine="e.json", measured=[], detectors=[])
SLIT["faces"] = [{"axis": "x", "at": 12, "gaps": [{"y": [4, 4], "z": [0, 0]}]}]
PACKET = {"family": "charge", "along": "x", "wave": [1, 4], "amplitude": 1328}
PACKET.update(top={"x": [5, 5], "y": [0, 8], "z": [0, 0]}, edge={"x": 4, "y": 0, "z": 0})


def slit_world(folder: Path, name: str, **changes: object) -> Path:
    """The slit world, a wall across x with one gap at y = 4 on a board of 24 x 9 x 1 (z folded), the packet of light laid by the generator, in the tests' universe without its row with a gap; `changes` replace the world's keys."""
    universe_beside(folder, drop=("polarisation",))
    path = folder / f"{name}.json"
    path.write_text(json.dumps({**SLIT, "messages": [PACKET], **changes}), encoding="utf-8")
    TOOL.main(["--input", str(path)])
    return path


def test_a_message_is_the_wave_under_its_envelope_and_an_inner_face_reflects_it_but_for_its_gap(
    tmp_path, monkeypatch
):
    """The message lay: now_i = b e_i cos(k x_i) and before_i = b e_i cos(k x_i + omega) at k = pi / 4 along x, b = 1,328, the raised cosine of half-width 4 about x = 5, within one unit of the real numbers at the packet's Nodes (the rotation act and the fixed point of the division act, no table); the loader admits the folded board and refuses by name a detector Node, a body Node and a laid level beyond the inner face and faces that leave no Node; in the run the Nodes beyond the board stay 0 in every family and no quantum crosses their Links (SUM (W_c c + r) kept to the bit), the wave passes the gap (the light's levels beyond the wall, more in the gap's row than at the board's edge) and reflects elsewhere (more of its form before the wall than on the same board without the wall); the back-in-time gate says MATCH over the run."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = slit_world(tmp_path, "slit")
    mode = json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))["messages"][0]
    now, before = (np.array(mode["moving"][word]).reshape(24, 9, 1) for word in ("now", "before"))
    k, omega = math.pi / 4, math.acos((math.cos(math.pi / 4) + 2) / 3)
    for x in range(24):
        away = abs(x - 5)
        e = (1 + math.cos(math.pi * away / 4)) / 2 if away <= 4 else 0
        assert abs(now[x, 4, 0] - 1328 * e * math.cos(k * x)) <= 1
        assert abs(before[x, 4, 0] - 1328 * e * math.cos(k * x + omega)) <= 1
    assert (now[:, 4:5, :] == now).all() and mode["count"] > 0 and not now[12].any()
    refused = [
        (
            "beyond the board's inner face: nothing stands there",
            dict(detectors=[{"name": "d", "positions": [[12, 0, 0]]}]),
        ),
        ("faces leave no Node", dict(faces=[{"axis": "z", "at": 0, "gaps": []}])),
    ]
    for reason, changes in refused:
        with pytest.raises(ValueError, match=reason):
            load_world(slit_world(tmp_path, "refused", **changes))
    with pytest.raises(ValueError, match="beyond the board's inner face: nothing stands there"):
        TOOL.pixel_mode(
            {**SLIT, "measured": [{"family": "matter", "nodes": [{"node": [12, 0, 0], "count": 50}]}]}
        )
    tampered = json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))
    tampered["messages"][0]["moving"]["now"][12 * 9] = 5
    path.with_suffix(".mode.json").write_text(json.dumps(tampered), encoding="utf-8")
    with pytest.raises(
        ValueError, match=r"is 5 at the Node \[12, 0, 0\], beyond the board's inner face"
    ):
        load_world(path)
    path.with_suffix(".mode.json").write_text(
        json.dumps({**tampered, "messages": [mode]}), encoding="utf-8"
    )
    boards = [
        GameBoard(load_world(slit_world(tmp_path, name, **changes)))
        for name, changes in (("slit", {}), ("open", dict(faces=[])))
    ]
    walled, open_board = boards
    names = [family.name for family in walled.families]
    charge = names.index("charge")
    beyond = walled.wrap.beyond
    assert (
        beyond is not None
        and beyond.sum() == 8
        and not beyond[12, 4, 0]
        and open_board.wrap.beyond is None
    )
    walled.step()
    for _ in range(23):
        walled.step()
        open_board.step()
        for state in walled.states:
            records = [r for r in (*state.parts, state.levels, state.second) if r is not None]
            assert not any(getattr(r, key)[beyond].any() for r in records for key in ("now", "before"))
            assert not any(a[beyond].any() for a in (state.count, state.sense) if a is not None)
        assert walled.books()["charge"]["balanced"]
    level = np.abs(walled.states[charge].levels.now[:, :, 0])
    passed = level[13:].sum(axis=0)
    print(
        f"GAMEBOARD the slit: the light beyond the wall per row {passed.tolist()}, before it {int(level[:12].sum())} against {int(np.abs(open_board.states[charge].levels.now[:12]).sum())} with no wall"
    )
    assert (
        passed[4] > passed[0] > 0
        and level[:12].sum() > np.abs(open_board.states[charge].levels.now[:12]).sum()
    )
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
    heavy = [
        {"family": "matter", "nodes": [{"node": [x, 0, 0], "count": 2 * QUANTA}]}
        for x in (CHAIN // 2, CHAIN // 2 + 2)
    ]
    with pytest.raises(ValueError, match="collapses: its wells reach the pace 0"):
        TOOL.pixel_mode({**document, "measured": heavy})
    small = [{"family": "matter", "nodes": [{"node": [x, 0, 0], "count": 20}]} for x in (20, 23)]
    with pytest.raises(
        ValueError, match="measured\\[1\\] and measured\\[0\\] share a Node in their regions"
    ):
        TOOL.pixel_mode({**document, "measured": small})
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    del universe["integers"]["quantum_action"]
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    with pytest.raises(ValueError, match="declares no quantum_action T"):
        TOOL.pixel_mode(document)

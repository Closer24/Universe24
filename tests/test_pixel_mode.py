"""The generator is Rule3 (ALGEBRA.md #the-generator): the generator lays a body as the fixed point of the row it reads, its declared count the weighted share its record lays, a body rotating in a sense beside its record, refusing a cloud, a body that fits no positive pace, a universe without T and two bodies sharing a region by name; it lays a message as the wave under its envelope by the rotation act, and an inner face of the board (the face rule inside it) reflects the wave but for its gap, the gate MATCH."""

import json
import math

import numpy as np

import event_universe.world_files as world_files
from event_universe.core import paces
from event_universe.game_board import GameBoard
from event_universe.world_files import input_digest, load_world
from tests.laws import (
    BACK,
    CHAIN,
    PACKET,
    QUANTA,
    SLIT,
    TOOL,
    chain_body_world,
    refused,
    slit_world,
)


def dense(levels: dict[str, list[int]]) -> np.ndarray:
    """A level of the mode file's sparse form as the slit board's array."""
    return np.bincount(levels["at"], levels["values"], 24 * 9).astype(np.int64).reshape(24, 9, 1)


def test_a_message_is_the_wave_under_its_envelope_and_the_inner_face_reflects_it(tmp_path, monkeypatch):
    """The message lay: now_i = b e_i cos(k x_i) and before_i = b e_i cos(k x_i + omega) at k = pi / 4 along x, b = 1,328, the raised cosine of half-width 4 about x = 5, within one unit of the real numbers at the packet's Nodes (the rotation act and the fixed point of the division act, no table); the loader admits the folded board and refuses by name a detector Node, a body Node and a laid level beyond the inner face, faces that leave no Node, a detector's `remainder` key (no count stands at a Node: the count is the record's share) and a message's `whole` Node (no line lays a count whole: the count is read); a packet toward -x at the phase pi / 2 with the transverse wave number pi / 8 along y (`wave` [-1, 4], `phase` [1, 4], `transverse` {y: [1, 8]}) is laid as its mirror at that slant within one unit, its band's omega with cos k_y, and a transverse wave number on the along axis is refused by name; the screen's click lines are its report, the net inflow into its column through its front boundary Ports, never 0 and never a Node, beside the field's readings; in the run the Nodes beyond the board stay 0 in every family and the charge's share in quanta over the board stays above 0, the wave passes the gap (the light's levels beyond the wall, more in the gap's row than at the board's edge) and reflects elsewhere (more of its form before the wall than on the same board without the wall); the back-in-time gate says MATCH over the run. One Node declaring the tests' count of quanta on the chain becomes a body of several Nodes, each carrying a quantum, their counts within the rounding of the declaration; its standing reading rotates above the matter band's top and below 2, its peak at the centre, its period read whole; the mode file stands for the world by its digest and the GameBoard loads its levels as written; a body laid with a sense carries its second level pair beside them, a neutral one none (the holder of the sign rests inside the lay-and-rest iteration: with the sense +1 the body's own charge deepens its well, with the sense -1 on this chain the content at the centre is below 0, no well, and the generator refuses it by name); the rotating body is laid at 10 quanta, which reach the branch the body of 50 reached, the lay with a sense through the same iteration (a body of eleven quanta over seven Nodes standing above the band's top, its second pair written), at a third of the 50's rounds. Two quanta on a chain of 48 bind as two Nodes carrying a quantum each, the top mode of the read on the board as declared (in one dimension every well binds on a board that holds its mode: on the tests' chain of 24 the two quanta are refused as a cloud, the top mode of the board as declared rotating at [230, 173] = 1.3295, under the band's top 1.3333, the board's length entering the lightest body's binding; the cloud is otherwise a three-dimensional body's refusal, examples/events/matter_alone/cloud.json); twice the tests' count lay as one body on the chain, its well far below the Link's zero (no finite count collapses under the composed paces, the write per proper volume, ALGEBRA.md #the-paces, The paces compose; the horizon on Nodes left with the quadratic forms: the smallest multiple taking that branch, laid in 22 rounds against the 28 of six times the count, whose well on this chain stood at 1390 against the Link's zero 28206); two bodies of twice the count two Links apart at the centre and two bodies of 20 quanta three Links apart (the Nodes 16 and 19, four Links from the centre and apart from the end detectors) are refused by name (no mode stands in the region left to the first body by the second's, or their regions share a Node), a universe without T and a sense other than +1 or -1 are refused by name. The lay at the integer fixed point (the world's `lay` of the kind `fixed_point`, loader/lay.py): the body of 10 quanta re-laid in the content it returns until the record's two levels and the content repeat within the declared stop of 1 unit at every Node, the mode file's trajectory ending within it after more than one pass, the loader reading the lay; the budget's gate refuses by name a tolerance whose least T is above the universe's. The aslant message toward -x at the phase pi / 2 with k_y = pi / 8 is b e cos(-k x + k_y y + pi / 2 + omega), k_y y = pi / 2 at y = 4; the screen's lines are the region's report and the field's reading alone, no Node named."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    screen = {"name": "screen", "positions": [[20, y, 0] for y in range(9)]}
    path = slit_world(tmp_path, TOOL, detectors=[screen])
    mode = json.loads((mode_file := path.with_suffix(".mode.json")).read_text())["messages"][0]
    now, before = (dense(mode["moving"][word]) for word in ("now", "before"))
    k, omega = math.pi / 4, math.acos((math.cos(math.pi / 4) + 2) / 3)
    away = [abs(x - 5) for x in range(24)]
    envelope = [(1 + math.cos(math.pi * d / 4)) / 2 if d <= 4 else 0 for d in away]
    for x, e in enumerate(envelope):
        assert abs(now[x, 4, 0] - 1328 * e * math.cos(k * x)) <= 1
        assert abs(before[x, 4, 0] - 1328 * e * math.cos(k * x + omega)) <= 1
    assert (now[:, 4:5, :] == now).all() and mode["count"] > 0 and not now[12].any()
    inner, at = "beyond the board's inner face", {"node": [12, 0, 0], "count": 50}
    for change, reason in (
        (
            {"detectors": [{"name": "d", "positions": [[12, 0, 0]]}]},
            f"{inner}: nothing stands there",
        ),
        ({"messages": [{**PACKET, "wave": [0, 4]}]}, "wave's p is 0"),
        ({"faces": [{"axis": "z", "at": 0, "gaps": []}]}, "faces leave no Node"),
        ({"messages": [{**PACKET, "whole": [5, 4, 0]}]}, r"whole names the Node \[5, 4, 0\]"),
        ({"detectors": [{**screen, "remainder": {"charge": 1}}]}, "unknown key 'remainder'"),  # no count
        ({"messages": [{**PACKET, "transverse": {"x": [1, 8]}}]}, "transverse holds the unknown key"),
    ):
        refused(reason, lambda c=change: load_world(slit_world(tmp_path, TOOL, "r", **c)))
    aslant = {**PACKET, "wave": [-1, 4], "phase": [1, 4], "transverse": {"y": [1, 8]}}
    turned = slit_world(tmp_path, TOOL, "turned", messages=[aslant])
    before = json.loads(turned.with_suffix(".mode.json").read_text())["messages"][0]["moving"]["before"]
    mirrored = dense(before)
    tilted = math.acos((math.cos(math.pi / 4) + math.cos(math.pi / 8) + 1) / 3)  # the band with k_y
    for x, e in enumerate(envelope):
        assert abs(mirrored[x, 4, 0] - 1328 * e * math.cos(-k * x + math.pi + tilted)) <= 1
    body = {"family": "matter", "nodes": [at]}
    refused(f"{inner}: nothing stands there", TOOL.pixel_mode, {**SLIT, "measured": [body]})
    tampered = json.loads(mode_file.read_text(encoding="utf-8"))
    tampered["messages"][0]["moving"]["now"]["at"].append(12 * 9)
    tampered["messages"][0]["moving"]["now"]["values"].append(5)
    mode_file.write_text(json.dumps(tampered), encoding="utf-8")
    refused(f"is 5 at the Node \\[12, 0, 0\\], {inner}", lambda: load_world(path))
    mode_file.write_text(json.dumps({**tampered, "messages": [mode]}), encoding="utf-8")
    walled = GameBoard(load_world(path), (lines := []).append)
    open_board = GameBoard(load_world(slit_world(tmp_path, TOOL, "open", faces=[])))
    charge, beyond = [family.name for family in walled.families].index("charge"), walled.wrap.beyond
    assert beyond is not None and beyond.sum() == 8 and not beyond[12, 4, 0]
    walled.step()
    assert not [x for x in lines if x["event"] == "click"] and not walled.quanta(charge)[0][beyond].any()
    for _ in range(23):
        walled.step(), open_board.step()
        risen = [x for x in lines if x["tick"] == walled.tick and x["detector"] == "screen"]
        assert all(x["event"] in ("click", "field") and not {"node", "ports"} & x.keys() for x in risen)
        assert all(x["inflow"] != 0 for x in risen if x["event"] == "click")
        assert not np.any([a[beyond] for s in walled.states for r in s.lines for a in (r.now, r.before)])
        assert walled.books()["charge"]["quanta"] > 0
    level = np.abs(walled.states[charge].lines[0].now[:, :, 0])
    passed, free = level[13:].sum(axis=0), np.abs(open_board.states[charge].lines[0].now[:12]).sum()
    assert passed[4] > passed[0] > 0 and level[:12].sum() > free and open_board.wrap.beyond is None
    assert BACK.verdict(GameBoard(load_world(path)), 24)["verdict"] == "MATCH"
    world = chain_body_world(tmp_path, TOOL)
    document, mode = (json.loads(p.read_text()) for p in (world, world.with_suffix(".mode.json")))
    nodes = document["measured"][0]["nodes"]  # the one declared Node became the body's Nodes
    laid = sum(entry["count"] for entry in nodes)
    assert len(nodes) > 1 and all(entry["count"] >= 1 for entry in nodes)
    assert (abs(laid - QUANTA) - (abs(laid - QUANTA) & 1)) ** 2 <= 4 * QUANTA  # within the rounding
    entry, (a, den) = mode["bodies"][0], mode["bodies"][0]["clock"]
    assert TOOL.agree(entry["carried"], QUANTA) and entry["count"] == QUANTA and entry["seed"] >= 1
    assert 2 * 4000 * den < a * 6000 and a < 2 * den  # above the band's top 2 x 4000 / 6000, below 2
    profile, peak, moving = entry["profile"], entry["amplitude"], entry["moving"]
    assert max(map(abs, profile)) == abs(profile[CHAIN // 2]) == peak > 0  # the peak at the centre
    assert entry["period"][1] == 2 and entry["period"][0] >= 4 and "im_now" not in moving
    assert moving["now"] == profile and len(moving["before"]) == len(profile) == CHAIN
    assert (entry["pair"], entry["family"]) == ([4000, 6000], "matter")
    assert mode["world_digest"] == input_digest(document)
    board = GameBoard(load_world(world))  # lawful, the family's two levels
    matter = board.states[[family.name for family in board.families].index("matter")].lines[0]
    assert matter is not None and matter.now[CHAIN // 2, 0, 0] == peak
    assert matter.before.ravel().tolist() == entry["moving"]["before"]
    turned = chain_body_world(tmp_path, TOOL, 10, senses=(1,))  # the rotating lay: the body of 10 quanta
    rotating = json.loads(turned.with_suffix(".mode.json").read_text(encoding="utf-8"))["bodies"][0]
    assert any(rotating["moving"]["im_now"]) and len(rotating["moving"]["im_before"]) == CHAIN
    two = json.loads(chain_body_world(tmp_path, TOOL, 2, chain=48).read_text())["measured"][0]["nodes"]
    big = GameBoard(load_world(chain_body_world(tmp_path, TOOL, quanta=2 * QUANTA)))
    holders = [s for f, s in zip(big.families, big.states, strict=True) if f.held and not f.wronskian]
    deep = int(sum(s.lines[0].now for s in holders).max())
    assert 0 < deep < paces.frozen_content(big.world.node_clock) and [e["count"] for e in two] == [1, 1]
    document = json.loads(chain_body_world(tmp_path, TOOL, mode=False).read_text(encoding="utf-8"))
    refused("a sense is \\+1 or -1", lambda: TOOL.pixel_mode(json.loads(json.dumps(document)), [2]))
    for at, count in (((CHAIN // 2, CHAIN // 2 + 2), 2 * QUANTA), ((CHAIN - 8, CHAIN - 5), 20)):
        near = [{"family": "matter", "nodes": [{"node": [x, 0, 0], "count": count}]} for x in at]
        refused("share a Node|does not stand", TOOL.pixel_mode, {**document, "measured": near})
    fixed = json.loads((lay_path := chain_body_world(tmp_path, TOOL, 10, mode=False)).read_text())
    fixed["lay"] = {"kind": "fixed_point", "stop": 1, "passes": 30, "tolerance": [1, 4]}
    lay_path.write_text(json.dumps(fixed), encoding="utf-8"), TOOL.main(["--input", str(lay_path)])
    laid_mode = json.loads((mode_path := lay_path.with_suffix(".mode.json")).read_text(encoding="utf-8"))
    passes, laid = laid_mode["bodies"][0]["lay"]["trajectory"], json.loads(lay_path.read_text())
    assert len(passes) > 1 and max(passes[-1][1:3]) <= 1 and load_world(lay_path).lay.stop == 1
    lay_path.write_text(json.dumps(dict(fixed, lay=dict(fixed["lay"], seed="compact", profile=[76, 4]))))
    TOOL.main(["--input", str(lay_path)])  # the compact seed's lay by name (loader/lay.py)
    seeded = json.loads(mode_path.read_text(encoding="utf-8"))["bodies"][0]
    assert seeded["lay"]["seed"] == "compact" and load_world(lay_path).lay.profile == (76, 4)
    first = TOOL.compact_seed(100, (12, 0, 0), (24, 1, 1), TOOL.Wrap(False, True, True), (76, 4))
    assert first[11:14, 0, 0].tolist() == [4, 92, 4] and first.sum() == 100  # folded Ports: the centre
    for words, lay in (("seed is one", {"seed": "wide"}), ("profile .* seed", {"seed": "compact"})):
        refused(words, TOOL.lay_of, {"kind": "repeat", **lay}, "lay")
    laid["lay"]["tolerance"] = [1, 1000]  # a tolerance the universe's T cannot meet: the budget's gate
    lay_path.write_text(json.dumps(laid), encoding="utf-8")
    mode_path.write_text(json.dumps({**laid_mode, "world_digest": input_digest(laid)}))
    refused("below the least T", lambda: load_world(lay_path))
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    del universe["integers"]["quantum_action"]
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    refused("declares no quantum_action T", lambda: TOOL.pixel_mode(document))

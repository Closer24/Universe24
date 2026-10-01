"""A bound body (ALGEBRA.md #the-generator, #what-a-body-is, #the-count-is-the-records-share): the generator lays a body, the GameBoard admits its declared count within the rounding of its family's share in quanta at its Nodes and refuses one beyond it by name, the count is the record's share and stays its family's within Rule3's rounding, the body's Nodes derived from where its share stands; two bodies of opposite senses source the sign holder with opposite signs and read it with opposite q."""

from __future__ import annotations

import json

import numpy as np
import pytest

import event_universe.world_files as world_files
from event_universe import node
from event_universe.game_board import GameBoard
from event_universe.loader.derived import CONTENT, count_wall
from event_universe.world_files import input_digest, load_world
from tests.laws import CHAIN, QUANTA, ROOT, chain_body_world, load_file

TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")


def test_the_laid_body_is_admitted_its_count_kept_and_a_count_far_from_its_share_refused(
    tmp_path, monkeypatch
):
    """The count is the record's share in quanta over the wall 3 den T, read at the start within the law's tolerance of the declared count, every Node of the body carrying a quantum; over a hundred intervals the share's total moves only by Rule3's own rounding (the books' drift, under a quantum per Node of the chain) and no quantum changes family, the quanta at the declared Nodes stay above 0 and the body's Nodes derived for a report are where its share stands; a declared count off the share beyond the rounding refuses the world by name."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL)
    board = GameBoard(load_world(world))
    index = [family.name for family in board.families].index("matter")
    declared = board.mask(board.world.bodies[0].nodes)
    quanta = board.quanta(index)
    laid, wall = int(quanta[declared].sum()), count_wall(board.families[index], 32768)
    assert abs(laid - QUANTA) <= 2 * int(QUANTA**0.5) + 1 and int(quanta[declared].min()) >= 1
    kept, drifts = [], []
    for _ in range(100):
        board.step()
        quanta, standing = board.quanta(index), board.body_nodes(0)
        kept.append(int(quanta[standing].sum()))
        assert (quanta[standing] != 0).all() and (standing & declared).any()
        books = board.books()["matter"]
        drifts.append(books["drift"])
        assert abs(books["quanta"] - laid) <= CHAIN  # Rule3's rounding, under a quantum per Node
    print(f"GAMEBOARD the laid body of {laid}: quanta at its Nodes {min(kept)} to {max(kept)} in 100,")
    print(f"  the share's drift {min(drifts)} to {max(drifts)} units against the wall {wall}")
    assert abs(max(drifts, key=abs)) < CHAIN * wall and board.books()["matter"]["pace"] > 0
    document = json.loads(world.read_text(encoding="utf-8"))
    for line in document["measured"][0]["nodes"]:
        line["count"] = 1  # far below the share
    world.write_text(json.dumps(document), encoding="utf-8")
    mode_path = world.with_suffix(".mode.json")
    mode = json.loads(mode_path.read_text(encoding="utf-8"))
    mode["world_digest"] = input_digest(document)
    mode_path.write_text(json.dumps(mode), encoding="utf-8")
    with pytest.raises(ValueError, match="a declared count is within the rounding of the share"):
        GameBoard(load_world(world))


def test_two_bodies_of_opposite_senses_source_the_sign_holder_oppositely_and_read_it_with_opposite_q(
    tmp_path, monkeypatch
):
    """The sign is the rotation sense: on the chain two bodies laid rotating in the senses +1 and -1 carry the Wronskian and the sense of those signs at their Nodes (0 where the booked sense rounds to none), so each reads the sign holder with its own q, +1 and -1; after one interval the sign holder's record (its time part, the light's own record) stands at or above 0 at the first's Nodes and at or below 0 at the second's, not 0 in all (the Wronskian's quanta its source), and a level of one sign read by both enters their contents with opposite signs (the hill and the hollow)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = GameBoard(load_world(chain_body_world(tmp_path, TOOL, at=(14, 34), senses=(1, -1))))
    names = [family.name for family in board.families]
    matter, charge = board.states[names.index("matter")], board.states[names.index("charge")]
    board.step()
    first, second = board.body_nodes(0), board.body_nodes(1)
    q = node.sense_sign(matter, board.shape)
    assert (q[first] >= 0).all() and (q[first] == 1).any() and (q[second] <= 0).all()
    assert (q[second] == -1).any()
    assert (np.sign(node.wronskian(matter.levels, matter.second))[first] == 1).all()
    level = charge.parts[0].now
    assert charge.levels is charge.parts[0]  # light is the sign holder's own record
    assert int(level[first].min()) >= 0 < int(level[first].sum())
    assert int(level[second].max()) <= 0 > int(level[second].sum())
    hill = np.full(board.shape, 100, dtype=np.int64)
    node.with_parts(charge, [node.Record(hill, charge.parts[0].before, charge.parts[0].remainder)])
    reader = names.index("matter")
    content, _axis = node.signed_read(reader, board.families, board.states, 6000, "now", board.shape)
    holders = [s for f, s in zip(board.families, board.states, strict=True) if f.held == CONTENT]
    plain = sum(state.parts[0].now for state in holders)  # every holder of the content, as it stands
    assert ((content - plain) == -100 * q)[first | second].all()  # the hill at q = +1, the hollow at -1

"""A bound body (ALGEBRA.md #the-generator, #what-a-body-is, #the-counts-line): the generator lays a body, the GameBoard admits its declared count within the rounding of the count its family's weighted share lays at its Nodes and refuses one beyond it by name, the count moves by the line alone and stays its family, the body's Nodes derived from where its count stands; two bodies of opposite senses source the sign holder with opposite signs and read it with opposite q."""

from __future__ import annotations

import json

import numpy as np
import pytest

import event_universe.world_files as world_files
from event_universe import node
from event_universe.game_board import GameBoard
from event_universe.loader.world import spread
from event_universe.world_files import input_digest, load_world
from tests.laws import CHAIN, QUANTA, ROOT, chain_body_world, load_file

TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")


def test_the_laid_body_is_admitted_its_count_kept_and_a_count_far_from_its_form_refused(
    tmp_path, monkeypatch
):
    """The count is laid from the family's weighted share at the wall 3 den T within the law's tolerance of the declared count, every Node of the body carrying a quantum; over a hundred intervals SUM (W_c c + r) stays to the bit (no quantum changes family), the count at the declared Nodes stays above 0 and the body's Nodes derived for a report are where its count stands; a declared count off the lay beyond the rounding ends the run at the lay by name; held quanta are laid over a body's Nodes in proportion to its counts, none lost."""
    assert spread(64, (1, 3, 5, 7)) == (4, 12, 20, 28) and sum(spread(10, (3, 3, 3))) == 10
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL)
    board = GameBoard(load_world(world))
    matter = board.states[3]
    declared = board.mask(board.world.bodies[0].nodes)
    board.step()
    assert matter.count is not None and matter.count_remainder is not None
    laid, wall = int(matter.count[declared].sum()), node.count_wall(board.families[3], 32768)
    assert abs(laid - QUANTA) <= 2 * int(QUANTA**0.5) + 1 and int(matter.count[declared].min()) >= 1
    total = int((wall * matter.count.astype(object) + matter.count_remainder).sum())
    kept = []
    for _ in range(99):
        board.step()
        standing = board.body_nodes(0)
        kept.append(int(matter.count[standing].sum()))
        assert (matter.count[standing] != 0).all() and (standing & declared).any()
        assert int((wall * matter.count.astype(object) + matter.count_remainder).sum()) == total
        assert abs(int(matter.count.sum()) - laid) <= CHAIN  # the remainders' walk, a Node at most each
    print(
        f"GAMEBOARD the laid body of {laid}: its count at its Nodes {min(kept)} to {max(kept)} over 100 intervals"
    )
    assert board.books()["matter"]["balanced"] and board.books()["matter"]["pace"] > 0
    document = json.loads(world.read_text(encoding="utf-8"))
    for line in document["measured"][0]["nodes"]:
        line["count"] = 1  # far below the form
    world.write_text(json.dumps(document), encoding="utf-8")
    mode_path = world.with_suffix(".mode.json")
    mode = json.loads(mode_path.read_text(encoding="utf-8"))
    mode["world_digest"] = input_digest(document)
    mode_path.write_text(json.dumps(mode), encoding="utf-8")
    with pytest.raises(ValueError, match="a declared count is within the rounding of SUM D_i div T"):
        GameBoard(load_world(world)).step()


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
    assert (
        (q[first] >= 0).all()
        and (q[first] == 1).any()
        and (q[second] <= 0).all()
        and (q[second] == -1).any()
    )
    assert (np.sign(node.wronskian(matter.levels, matter.second))[first] == 1).all()
    level = charge.parts[0].now
    assert charge.levels is charge.parts[0]  # light is the sign holder's own record
    assert int(level[first].min()) >= 0 < int(level[first].sum()) and int(
        level[second].max()
    ) <= 0 > int(level[second].sum())
    node.with_parts(
        charge,
        [
            node.Record(
                np.full(board.shape, 100, dtype=np.int64),
                charge.parts[0].before,
                charge.parts[0].remainder,
            )
        ],
    )
    content, _axis = node.signed_read(
        names.index("matter"), board.families, board.states, 6000, "now", board.shape
    )
    plain = sum(board.states[names.index(name)].parts[0].now for name in ("gravity", "polarisation"))
    assert ((content - plain) == -100 * q)[first | second].all()  # the hill at q = +1, the hollow at -1

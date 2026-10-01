"""A bound body (ALGEBRA.md #the-generator, #what-a-body-is, #the-count-is-the-records-share): the generator lays a body, the GameBoard admits its declared count within the rounding of its family's share in quanta at its Nodes and refuses one beyond it by name, the count is the record's share and stays its family's within Rule3's rounding, the body's Nodes derived from where its share stands; two bodies of a plane of opposite senses source the sign holder with opposite signs and both read it plainly, a body of real parts not at all."""

from __future__ import annotations

import json

import numpy as np

import event_universe.world_files as world_files
from event_universe import node
from event_universe.game_board import GameBoard
from event_universe.loader.derived import count_wall
from event_universe.world_files import input_digest, load_world
from tests.laws import CHAIN, CHARGED, QUANTA, TOOL, chain_body_world, refused


def test_the_laid_body_is_admitted_its_count_kept_and_a_far_count_refused(tmp_path, monkeypatch):
    """The count is the record's share in quanta over the wall 3 den T, read at the start within the law's tolerance of the declared count, every Node of the body carrying a quantum; over a hundred intervals the share's total moves only by Rule3's own rounding (the books' drift, under a quantum per Node of the chain) and no quantum changes family, the quanta at the declared Nodes stay above 0 and the body's Nodes derived for a report are where its share stands; a declared count off the share beyond the rounding refuses the world by name."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL)
    board = GameBoard(load_world(world))
    index = [family.name for family in board.families].index("matter")
    declared, quanta = board.mask(board.world.bodies[0].nodes), board.quanta(index)[0]
    laid, wall = int(quanta[declared].sum()), count_wall(board.families[index], 32768)
    assert abs(laid - QUANTA) <= 2 * int(QUANTA**0.5) + 1 and int(quanta[declared].min()) >= 1
    kept, drifts = [], []
    for _ in range(100):
        board.step()
        quanta, standing = board.quanta(index)[0], board.body_nodes(0)
        kept.append(int(quanta[standing].sum()))
        assert (quanta[standing] != 0).all() and (standing & declared).any()
        books = board.books()["matter"]
        drifts.append(books["drift"])
        assert abs(books["quanta"] - laid) <= CHAIN  # Rule3's rounding, under a quantum per Node
    print(f"GAMEBOARD the laid body of {laid}: quanta at its Nodes {min(kept)} to {max(kept)} in 100,")
    print(f"  the share's drift {min(drifts)} to {max(drifts)} units against the wall {wall}")
    assert abs(max(drifts, key=abs)) < CHAIN * wall and board.books()["matter"]["pace"] > 0
    document = json.loads(world.read_text(encoding="utf-8"))
    document["measured"][0]["nodes"] = [{**n, "count": 1} for n in document["measured"][0]["nodes"]]
    world.write_text(json.dumps(document), encoding="utf-8")
    mode_path = world.with_suffix(".mode.json")
    mode = json.loads(mode_path.read_text(encoding="utf-8"))
    mode["world_digest"] = input_digest(document)
    mode_path.write_text(json.dumps(mode), encoding="utf-8")
    refused("a declared count is within the rounding of the share", lambda: GameBoard(load_world(world)))


def test_opposite_senses_source_the_sign_holder_oppositely_and_a_plane_reads_it(tmp_path, monkeypatch):
    """The dimension's table (ALGEBRA.md #a-familys-declaration): on the chain two bodies of the charged family (matter's pair as a plane) laid rotating in the senses +1 and -1 carry the Wronskian of those signs at their Nodes, so after one interval the sign holder's record (its time part, the light's own record) stands at or above 0 at the first's Nodes and at or below 0 at the second's, not 0 in all (the Wronskian's quanta its source); the charged family reads the holder plainly, a level of 100 entering its content as 100 at every Node of both bodies, while matter, real parts of the same pair, reads nothing of it and light does not read its own row."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = GameBoard(load_world(chain_body_world(tmp_path, TOOL, at=(14, 34), senses=(1, -1))))
    names = [family.name for family in board.families]
    charged, charge = names.index(CHARGED["name"]), names.index("charge")
    plane, light = board.states[charged], board.states[charge]
    board.step()
    first, second = board.body_nodes(0), board.body_nodes(1)
    turn = np.sign(node.wronskian(plane.lines, True))
    assert (turn[first] == 1).all() and (turn[second] == -1).all()
    level = light.lines[0].now
    assert len(light.lines) == 1 and int(level[first].min()) >= 0 < int(level[first].sum())  # one line
    assert int(level[second].max()) <= 0 > int(level[second].sum())
    hill = np.full(board.shape, 100, dtype=np.int64)
    light.lines[0] = node.Record(hill, light.lines[0].before, light.lines[0].remainder)
    held = [s for f, s in zip(board.families, board.states, strict=True) if f.held and not f.wronskian]
    plain = sum(state.lines[0].now for state in held)  # every holder of the content, as it stands
    content, _axis = node.read(charged, board.families, board.states, 1)
    assert ((content - plain) == 100)[first | second].all()  # the plane reads the holder plainly
    for reader in (names.index("matter"), charge):  # dimension one, and the holder's own record
        assert charge not in [read.family for read in board.families[reader].reads]
        assert np.array_equal(node.read(reader, board.families, board.states, 1)[0], plain)

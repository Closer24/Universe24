"""The Node of the emission's lay and of the conversion's write (ALGEBRA.md, The NodeDetector is one declaration kind for every experiment: the emission's whole quantum laid at the Node drawn by its own record's share over its Nodes, the share at a Node a lattice reading and no measurement; the mathematician's words on A2 of the law-engine audit, #1793): drawn by the record's share at the body's Nodes as the board holds it at the close, the file's lay weights entering no draw."""

import json

from event_universe import act, lists, meeting, node_detector, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, TOOL, packet_world
from tests.laws_read import redeclared


def forced_write(monkeypatch):  # type: ignore[no-untyped-def]
    """The click act forced to its first alternative and the rows' Node draw spied: `act.picked` answers the index 0, `lists.drawn_node` notes the weights it is handed and draws as built; returns the notes."""
    noted: list[list[int]] = []
    real = lists.drawn_node

    def spy(board, books, weights):  # type: ignore[no-untyped-def]
        noted.append(list(weights))
        return real(board, books, weights)

    monkeypatch.setattr(act, "picked", lambda board, books, weights: 0)
    monkeypatch.setattr(lists, "drawn_node", spy)
    return noted


def test_the_emission_lays_its_node_by_the_records_share_and_not_by_the_weights(tmp_path, monkeypatch):
    """The Zeno reader on two Nodes with the lay weights 1 and 2 and its atom at the pair [2, 3], real hopping across its inner Link (the shipped pair [1, 1299] hops by 1 in 1,299, the two Nodes' shares then standing at the lay's proportion for the whole window): at the lay the record's share at its Nodes stands near the weights' proportion, A_i^2 = A^2 w_i / SUM w with the inner Link's term and the amplitudes' rounding (0.306 against 1 / 3), and over ten intervals of Rule3's own step inside the window the record beats between its Nodes, so that the board's share departs from the weights' proportion by more than a fifth; `share_weights` reads the board's shares floored at 0 and not the weights, and the Node drawn through `drawn_node` is one of the body's by its read of the board; `lists.emission` on the packet world's giver and `lists.conversion` on the neutron's record, each stepped one interval (the read has digits off the origin) and forced to its write, hand `drawn_node` the shares the board holds and never the file's weights."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe = json.loads((EVENTS / "zeno" / "zeno_atom.json").read_text(encoding="utf-8"))
    universe["families"][0]["pair"] = [2, 3]  # the atom hops across its inner Link: the record beats
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    world = redeclared(json.loads((EVENTS / "zeno" / "zeno_4.json").read_text(encoding="utf-8")))
    world["bodies"][0]["nodes"][1]["weight"] = 2  # the lay weights 1 and 2 over the two Nodes
    world.update(universe="u.json")
    (path := tmp_path / "zeno.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(path)])
    board = Lattice(load_world(path))
    books = board.credit.bodies[0]
    assert books.weights == (1, 2) and len(books.nodes) == 2
    laid = node_detector.share_weights(board, books)
    for _ in range(10):  # inside the window of 12: the window's close lays the parts again
        board.step()
    shares = node_detector.share_weights(board, books)
    share, weight = shares[0] / sum(shares), books.weights[0] / sum(books.weights)
    assert abs(laid[0] / sum(laid) - weight) < 0.05  # the lay near the weights' proportion
    assert shares != list(books.weights) and abs(share - weight) > 0.2  # the board's own shares
    at = node_detector.drawn_node(board, books, node_detector.share_weights(board, books))
    assert at in books.nodes and books.left is not None  # the Node by the body's read of the board
    print(
        f"shares {shares} ({share:.4f}), weights {list(books.weights)} ({weight:.4f}), the Node drawn {at}"
    )
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", ROOT)  # the shipped worlds' universes
    giver = Lattice(load_world(packet_world(tmp_path, TOOL)))  # a body in its upper part with a rate
    giver.step()  # one interval: the record's remainders leave the origin, the read has its digits
    emitter, given = giver.credit.bodies[0], forced_write(monkeypatch)
    standing = node_detector.share_weights(giver, emitter)  # read before the write, as the row reads it
    assert not meeting.emission_drawn(giver, emitter, 2) and emitter.deferred and given == []
    fell = lists.largest_share_node(giver, emitter)  # the deferred emission's Node: the largest share
    assert fell == emitter.nodes[max(range(len(standing)), key=standing.__getitem__)]
    assert standing != list(emitter.weights) and meeting.emission_fell(giver, emitter)

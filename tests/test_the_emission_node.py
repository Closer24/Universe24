"""The Node of the emission's lay and of the conversion's write (ALGEBRA.md, The NodeDetector is one declaration kind for every experiment: the emission's whole quantum laid at the Node drawn by its own record's share over its Nodes, the share at a Node a lattice reading and no measurement; the mathematician's words on A2 of the law-engine audit, #1793): drawn by the record's share at the body's Nodes as the board holds it at the close, the file's lay weights entering no draw."""

import json
import math

from event_universe import conversion, meeting, node_detector, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, TOOL, load_file, packet_world

TRIALS = 1200


def forced_write(monkeypatch, module):  # type: ignore[no-untyped-def]
    """The module's click act forced to its first list and its Node draw spied: `picked` answers the index 0 with the state kept, `drawn_node` notes the weights it is handed and draws as built; returns the notes."""
    noted: list[list[int]] = []
    real = module.drawn_node

    def spy(board, books, weights):  # type: ignore[no-untyped-def]
        noted.append(list(weights))
        return real(board, books, weights)

    monkeypatch.setattr(module, "picked", lambda board, state, generator, weights, outcomes: (0, state))
    monkeypatch.setattr(module, "drawn_node", spy)
    return noted


def test_the_emission_and_the_conversion_draw_their_node_by_the_records_share_and_not_by_the_weights(
    tmp_path, monkeypatch
):
    """The Zeno reader on two Nodes with the lay weights 1 and 2 and its atom at the pair [2, 3], real hopping across its inner Link (the shipped pair [1, 1299] hops by 1 in 1,299, the two Nodes' shares then standing at the lay's proportion for the whole window): at the lay the record's share at its Nodes stands near the weights' proportion, A_i^2 = A^2 w_i / SUM w with the inner Link's term and the amplitudes' rounding (0.306 against 1 / 3), and over ten intervals of Rule3's own step inside the window the record beats between its Nodes, so that the board's share departs from the weights' proportion by more than a fifth; `share_weights` reads the board's shares floored at 0 and not the weights, and 1,200 draws of the Node through `drawn_node` with the generator at the trials tool's hashed states fall within three standard errors of the share's proportion and farther than three from the weights' 1 / 3; `meeting.emitted` on the packet world's giver and `conversion.converted` on the neutron's record, each forced to its write, hand `drawn_node` the shares the board holds and never the file's weights."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe = json.loads((EVENTS / "zeno" / "zeno_atom.json").read_text(encoding="utf-8"))
    universe["families"][0]["pair"] = [2, 3]  # the atom hops across its inner Link: the record beats
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    (tmp_path / "e.json").write_bytes((EVENTS / "engine_start.json").read_bytes())
    world = json.loads((EVENTS / "zeno" / "zeno_4.json").read_text(encoding="utf-8"))
    world["bodies"][0]["nodes"][1]["weight"] = 2  # the lay weights 1 and 2 over the two Nodes
    world.update(universe="u.json", engine="e.json")
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
    hashed_state = load_file("meeting_trials", ROOT / "tools" / "meeting_trials.py").hashed_state
    drawn = [0, 0]
    for seed in range(TRIALS):
        books.state = hashed_state(seed, board.world.width)
        at = node_detector.drawn_node(board, books, node_detector.share_weights(board, books))
        drawn[books.nodes.index(at)] += 1
    frequency, error = drawn[0] / TRIALS, math.sqrt(share * (1 - share) / TRIALS)
    print(
        f"shares {shares} ({share:.4f}), weights {list(books.weights)} ({weight:.4f}), the first Node"
        f" drawn {drawn[0]} of {TRIALS} ({frequency:.4f}, error {error:.4f})"
    )
    assert abs(frequency - share) < 3 * error < abs(frequency - weight)
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", ROOT)  # the shipped worlds' universes
    giver = Lattice(load_world(packet_world(tmp_path, TOOL)))  # a body in its upper part with a rate
    emitter, given = giver.credit.bodies[0], forced_write(monkeypatch, meeting)
    standing = node_detector.share_weights(
        giver, emitter
    )  # read before the write, as `emitted` reads it
    assert (
        meeting.emitted(giver, emitter, 2) and given == [standing] and given[0] != list(emitter.weights)
    )
    neutron = Lattice(load_world(EVENTS / "neutron_conversion" / "neutron_conversion.json"))
    whole, converted = neutron.credit.bodies[0], forced_write(monkeypatch, conversion)
    standing = node_detector.share_weights(neutron, whole)
    assert conversion.converted(neutron, whole) and converted == [standing]
    assert converted[0] != list(whole.weights)


def test_the_neutron_readers_rows_stand_at_the_conversions_drawn_node(tmp_path):
    """The folder's reader at the drawn Node (the experimenter's tool note, #1827 comment 5984864554; examples/events/neutron_conversion/read_world.py): the shipped neutron conversion world at the rate 1 and the window 1 converts at the first interval at one of the body's two Nodes, A2's draw by the record's share; at the first seed whose draw picks the second Node the reader's rows stand there and the output names the Node as the conversion line's: the Wronskians -15,987, 16,384 and 0 (row 1), one quantum per record out (row 3) and the rotations' sum pi (row 5); with no conversion the body's first Node, named so."""
    reader = load_file("neutron_read_world", EVENTS / "neutron_conversion" / "read_world.py")
    world = json.loads((EVENTS / "neutron_conversion" / "neutron_conversion.json").read_text("utf-8"))
    body, path = world["bodies"][0], tmp_path / "w.json"
    body["conversion"]["rate"], body["node_detector"]["window"], world["intervals"] = 1, 1, 3
    path.write_text(json.dumps(world), encoding="utf-8")
    runs, second = (reader.first_trial(path, s, 3) for s in range(1, 64)), body["nodes"][1]["node"]
    found = next(r for r in runs if r["conversion"]["line"]["node"]["at"] == second)
    assert found["node"]["at"] == second and "conversion line" in found["node"]["source"]
    out = [found["conversion"]["families"][n] for n in ("proton", "electron", "antineutrino")]
    assert [f["wronskian"] for f in out] == [-15987, 16384, 0]  # row 1 at the drawn Node
    assert [round(f["quanta_at_the_node"]) for f in out] == [1, 1, 1]  # row 3
    assert round(found["rotations_sum"]["out_at_the_conversion"], 4) == 3.1416  # row 5
    none = reader.first_trial(path, 1, 0)  # no conversion: the body's first Node, named so
    assert none["node"]["at"] == body["nodes"][0]["node"] and "first Node" in none["node"]["source"]

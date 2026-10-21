"""The conserving click (2026-10-21; the reader's design of the conserving click, (a) to (d); ALGEBRA.md, The click writes on the lattice (3), (4), (5) and (6); The lattice momentum): a bound record declared an instrument body by the host tool's output in the mode file, the key `instrument` typed by tools/frame_of.py beside the levels tools/standing_lay.py laid, so that the engine's instrument-body click runs on it with no new act and no body-wide re-lay. The shipped giver world examples/events/conserve/giver_c5.json: the 5-cube at k_r 3 with light's own family `photon`, the electron laid standing in its upper level (the triplet at [3288, 6000]) and declared through the tool: its two levels the parts with the count in the upper, its transition from the lower [4580, 6000] to the upper by the photon at the weight 3 and the resonance [5751, 6000] (den cos(Omega_upper - Omega_lower) by the two pairs), its rate from the upper to the lower at the lifetime 30 giving to the photon, its standing region the 21 Nodes of the largest shares holding half the record's share joined into one region, its window derived at load as the lifetime. The pinned numbers are the world's own: the first emission at the interval 23, the first interval at which the body's read of its own remainders falls in the emission's cell at the hazard 1 / 30 per interval (the click's read of the board, read and not drawn). The emission's hazard of (5) (the reader's design, (d)): the beat's current of the body's own record through its own front Ports booked each interval as the credit books a drive (`NodeBooks.beat`), the window's outflow over W_c G^2 of the light entering the hazard beside the declared constant at the close (`lists.hazard_weights`); MEASURED on the box of 15 (examples/events/conserve/box_c15.json, the electron in 1s + 2p at k_r 3, the region of 11 Nodes, the lifetime 33; examples/events/conserve/read_beat.py over 99 intervals): the beat's current through the electron's own front swings by at most 0.0058 of a light quantum W_c per interval with the beat's period of 33, its sum over the 24 intervals before the constant fired at 25 -0.036 W_c (the running sum's extreme -0.059 W_c), so the beat term of (5) is at most 0.06 of a draw per window against the constant's one draw per lifetime, and with the constant 0 the law's (5) fires on the box within its 600 intervals in about one window of eighteen: the emission's hazard for a bound body of Rule3, named with its number, OPEN; the first window as booked carried -0.26 W_c, the write's own aftermath after the constant fired at 25, no beat."""

import json
from pathlib import Path

import numpy as np

from event_universe import act, lists, meeting, reports, world_files
from event_universe.lattice import Lattice
from event_universe.lists import hazard_weights
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, family, load_file, refused
from tests.laws_read import load_shipped

FOLDER = EVENTS / "conserve"
FRAME = load_file("frame_of_conserve", ROOT / "tools" / "frame_of.py")  # the host's frame tool
LOWER, UPPER = "level [4580, 6000] x1", "level [3288, 6000] x3"  # the two levels of the transition
RESONANCE, LIFETIME, REGION, FIRST = (
    (5751, 6000),
    30,
    21,
    23,
)  # the declaration and the world's own click
WALL = 482990683139  # the electron's quantum W_c sin omega_0 at T = 36,000,000 and [4000, 6000]
PIECE, FAN, RECOIL = (
    11055256,
    8012902,
    4906083,
)  # the taker world's click: the piece's p_z, the photon's P_z, the body's P_z after


def test_a_bound_record_declared_through_the_mode_file_clicks_on_the_instrument_bodys_path():
    """The loader reads the tool's declaration as a declared layer (the emission's hazard with the beat's term beside the constant, `hazard_weights`: the constant alone where no beat stands, a quarter of a light quantum out over the window a quarter of the row's total more, the weight capped at the total; the body's own record's current through its own front booked each interval into `NodeBooks.beat`, its outflow read at the close alone): the parts by the two levels' names with the count in the upper, the transition and its resonance, the rate at its lifetime, the region of 21 Nodes holding the declared Node with the record's shares as weights, the window 30 derived (no key); the record laid from the mode file into the upper part alone, the lower part's lines at 0, and no Link cut (the step untouched); the books on the region, the body standing in the upper part with its labels at the count's wall. The run to the first emission: the click at 23 (the giver paying by (5) at its own Nodes: the upper part down to 0 over the region, the lower up to one quantum re-laid there, the photon's record up by one, a source in time over the lifetime at the drawn Node), its line the body's with the parts by name and the photon emitted, the photon's count 1 in the books and the body's emitter entry; every lay line of the click at a Node of the region or the photon's one Node and none on the holder's rows (the holder's rows untouched by the click); the upper part's tail outside the region standing (the remainder of a region holding half the share, named); the null window of a bound record lays nothing: an empty list, no lay line, the labels' coherence ended in the books."""
    lines: list[dict] = []  # type: ignore[type-arg]
    world = load_shipped(FOLDER / "giver_c5.json")
    row = world.bodies[1]
    assert row.detector is not None and row.detector.draw is not None
    assert row.detector.names == (LOWER, UPPER) and row.detector.counts == (0, 1)
    (transition,) = row.detector.transitions
    (rate,) = row.detector.rates
    assert (transition.leaves, transition.enters, transition.weight) == (0, 1, 3)
    assert transition.resonance == RESONANCE and rate.resonance == RESONANCE
    assert (rate.leaves, rate.enters, rate.lifetime, rate.width) == (1, 0, LIFETIME, None)
    assert row.detector.draw.window == LIFETIME  # derived at load from the body's own rate, no key
    assert len(row.region) == REGION and row.nodes[0] in row.region and len(row.shares) == REGION
    assert min(row.shares) >= 1 and row.shares[row.region.index(row.nodes[0])] == max(row.shares)
    board = Lattice(world, lines.append)
    electron, photon, charge = (family(board, name) for name in ("electron", "photon", "charge"))
    assert meeting.cut(board, electron) is None  # the bound record's Links stand open
    unit, wall = WALL * WALL, 3 * 6000 * board.world.quantum_action * 16 * 16  # the row's unit; W_c G^2
    assert hazard_weights(1, LIFETIME, 6000, 6000, unit) == [unit, (LIFETIME - 1) * unit]  # the constant
    assert hazard_weights(1, LIFETIME, 6000, 6000, unit, wall // 4, wall) == [
        unit + (LIFETIME * unit) // 4,
        (LIFETIME - 1) * unit - (LIFETIME * unit) // 4,
    ]  # the beat's term: a quarter of a light quantum out over the window, a quarter of the row's total
    assert hazard_weights(1, LIFETIME, 6000, 6000, unit, 2 * wall, wall) == [
        LIFETIME * unit,
        0,
    ]  # capped
    laid = board.lines_of(electron, 0)
    assert not laid[0].now.any() and not laid[1].now.any()  # the lower part empty
    assert laid[2].now.any() and laid[3].now.any()  # the upper part the standing lay's
    (books,) = board.credit.bodies
    assert books.bound and books.nodes == row.region and books.weights == row.shares
    assert (books.part, books.counts, books.labels) == (1, [0, 1], [0, WALL])
    assert board.credit.counts[electron] == 1 and board.credit.counts[photon] == 0
    region = board.mask(row.region)
    for _ in range(FIRST):
        board.step()
    clicks = [c for c in lines if c["event"] == reports.CREDIT]
    assert [(c["interval"], c["label"]) for c in clicks] == [(FIRST, reports.MEASUREMENT)]
    (click,) = clicks
    assert (click["node_detector"], click["before"], click["realised"]) == ("body 1", UPPER, LOWER)
    assert (click["emitted"], click["absorbed"], click["count"], click["window"]) == (
        "photon",
        None,
        1,
        [1, FIRST],
    )
    assert (books.part, books.counts, books.labels) == (0, [1, 0], [WALL, 0])
    assert (
        books.beat != 0 and books.outflow == 0
    )  # the beat booked each interval, the outflow the close's
    assert board.credit.counts[photon] == 1 and board.credit.counts[electron] == 1
    (source,) = board.credit.sources
    assert (source.family, source.span, source.emitter, source.begun) == (photon, LIFETIME, 1, FIRST)
    assert [(e.body, e.outstanding) for e in board.credit.emitters[photon]] == [(1, 1)]
    lays = [row for row in lines if row["event"] == reports.LAY]
    assert {row["interval"] for row in lays} == {FIRST} and len(lays) > REGION
    assert {row["family"] for row in lays} == {"electron", "photon"}  # none on the holder's rows
    assert all(region[tuple(row["node"]["at"])] for row in lays if row["family"] == "electron")
    assert len({tuple(row["node"]["at"]) for row in lays if row["family"] == "photon"}) == 1
    after = board.lines_of(electron, 0)
    assert after[0].now[region].any() and not after[2].now[region].any()  # the exchange over the region
    assert after[2].now[~region].any() or after[3].now[~region].any()  # the tail outside it standing
    assert not board.states[charge].lines[0].now.any()  # light its own family: the free row exactly 0
    alternatives = lists.null_window(board, books)
    assert len(alternatives) == 1 and alternatives[0].items() == [] and alternatives[0].line is not None
    before = len(lines)
    act.click(board, books, alternatives)
    meeting.coherence_ended(board, books)
    assert len(lines) == before and books.labels == [WALL, 0] and books.carried == [0, 0]


def test_the_frame_tool_types_the_declaration_and_the_loader_refuses_a_defective_one_by_name(
    tmp_path, monkeypatch
):
    """The tool run on a copy of the shipped giver world writes the shipped declaration again, word for word (the mode file's digest the world's); the loader refuses by name a region in pieces, a region without the body's declared Node, the count in both parts, a transition naming the body's own family as its drive, and an unknown key of the declaration."""
    for name in ("giver_c5.json", "giver_c5.mode.json"):
        (tmp_path / name).write_text((FOLDER / name).read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "u.json").write_text(
        (FOLDER / "universe_conserve.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    path, mode_path = tmp_path / "giver_c5.json", tmp_path / "giver_c5.mode.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["universe"] = "u.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    shipped = json.loads(mode_path.read_text(encoding="utf-8"))
    shipped["world_digest"] = world_files.input_digest(document)
    mode_path.write_text(json.dumps(shipped), encoding="utf-8")
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    FRAME.main(["--input", str(path), "--light", "photon", "--lifetime", str(LIFETIME)])
    written = json.loads(mode_path.read_text(encoding="utf-8"))
    assert written["bodies"][1]["instrument"] == shipped["bodies"][1]["instrument"]
    assert "instrument" not in written["bodies"][0]  # the frozen proton: no transition, no declaration

    def tampered(change) -> Path:  # type: ignore[no-untyped-def]
        mode = json.loads(json.dumps(shipped))
        change(mode["bodies"][1]["instrument"])
        mode_path.write_text(json.dumps(mode), encoding="utf-8")
        return path

    def in_pieces(instrument: dict) -> None:  # type: ignore[type-arg]
        instrument["nodes"] = [instrument["nodes"][0], {"node": [0, 0, 0], "weight": 1}]

    def without_the_node(instrument: dict) -> None:  # type: ignore[type-arg]
        instrument["nodes"] = [n for n in instrument["nodes"] if n["node"] != [3, 2, 2]]

    def both_parts(instrument: dict) -> None:  # type: ignore[type-arg]
        instrument["parts"][0]["count"] = 1

    def own_drive(instrument: dict) -> None:  # type: ignore[type-arg]
        instrument["transitions"][0]["drive"] = "electron"

    def unknown(instrument: dict) -> None:  # type: ignore[type-arg]
        instrument["frame"] = {}

    for change, reason in (
        (in_pieces, "one connected region of distinct Nodes"),
        (without_the_node, "holds none of the body's declared Nodes"),
        (both_parts, "stands in one part at the start"),
        (own_drive, "a family of quanta other than the body's own"),
        (unknown, "unknown key 'frame'"),
    ):
        refused(reason, lambda c=change: load_world(tampered(c)))
    assert np.array_equal(np.zeros(1), np.zeros(1))  # the tool's doubles stand in the tool alone

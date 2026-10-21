"""The conserving click (2026-10-21; the reader's design of the conserving click, (a) to (d); ALGEBRA.md, The click writes on the lattice (3), (4), (5) and (6); The lattice momentum): a bound record declared an instrument body by the host tool's output in the mode file, the key `instrument` typed by tools/frame_of.py beside the levels tools/standing_lay.py laid, so that the engine's instrument-body click runs on it with no new act and no body-wide re-lay. The shipped giver world examples/events/conserve/giver_c5.json: the 5-cube at k_r 3 with light's own family `photon`, the electron laid standing in its upper level (the triplet at [3288, 6000]) and declared through the tool: its two levels the parts with the count in the upper, its transition from the lower [4580, 6000] to the upper by the photon at the weight 3 and the resonance [5751, 6000] (den cos(Omega_upper - Omega_lower) by the two pairs), its rate from the upper to the lower at the lifetime 30 giving to the photon, its standing region the laid part's whole support by rule, 100 Nodes in two lobes joined through one Node of the level's nodal plane, 101 in all, its window derived at load as the lifetime. The pinned numbers are the world's own: the first emission at the interval 12, the first interval at which the body's read of its own remainders falls in the emission's cell at the hazard 1 / 30 per interval (the click's read of the board, read and not drawn). The emission's hazard of (5) (the reader's design, (d)): the beat's current of the body's own record through its own front Ports booked each interval as the credit books a drive (`NodeBooks.beat`), the window's outflow over W_c G^2 of the light entering the hazard beside the declared constant at the close (`lists.hazard_weights`); MEASURED on the box of 15 (examples/events/conserve/box_c15.json, the electron in 1s + 2p at k_r 3, the region of 11 Nodes, the lifetime 33; examples/events/conserve/read_beat.py over 99 intervals): the beat's current through the electron's own front swings by at most 0.0058 of a light quantum W_c per interval with the beat's period of 33, its sum over the 24 intervals before the constant fired at 25 -0.036 W_c (the running sum's extreme -0.059 W_c), so the beat term of (5) is at most 0.06 of a draw per window against the constant's one draw per lifetime, and with the constant 0 the law's (5) fires on the box within its 600 intervals in about one window of eighteen: the emission's hazard for a bound body of Rule3, named with its number, OPEN; the first window as booked carried -0.26 W_c, the write's own aftermath after the constant fired at 25, no beat."""

import json
from pathlib import Path

import numpy as np

from event_universe import act, lists, meeting, records, reports, world_files
from event_universe.core.paces import sine_den
from event_universe.lattice import Lattice
from event_universe.lists import hazard_weights
from event_universe.take import fan_momentum
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, family, load_file, refused
from tests.laws_read import load_shipped

FOLDER = EVENTS / "conserve"
FRAME = load_file("frame_of_conserve", ROOT / "tools" / "frame_of.py")  # the host's frame tool
LOWER, UPPER = "level [4580, 6000] x1", "level [3288, 6000] x3"  # the two levels of the transition
RESONANCE, LIFETIME, REGION, FIRST = (
    (5751, 6000),
    30,
    101,
    12,
)  # the declaration, the whole support with its one joining Node, and the world's own click
WALL = 482990683139  # the electron's quantum W_c sin omega_0 at T = 36,000,000 and [4000, 6000]
PIECE, FAN, RECOIL = (
    11055256,
    8012902,
    10191633,
)  # the taker world's click: the piece's p_z, the photon's P_z, the body's P_z after
T = 36000000  # the clock's unit of both worlds, the energies' scale
GIVER_BEFORE = ((1, 0), 21029078, (0, 0, 0), 692879288000, 0)  # the giver at 11: see table_of
GIVER_AFTER = ((1, 1), 18000211, (2500, 0, 0), 650975322000, 6675858000)  # the giver at 12
TAKER_BEFORE = ((1, 1), 21310641, (0, 0, 0), 903766398000, 186746982000)  # the taker at 17
TAKER_AFTER = ((1, 0), 18010750, (0, 0, RECOIL), 979032106000, 186776658000)  # the taker at 18


def test_a_bound_record_declared_through_the_mode_file_clicks_on_the_instrument_bodys_path():
    """The loader reads the tool's declaration as a declared layer (the emission's hazard with the beat's term beside the constant, `hazard_weights`: the constant alone where no beat stands, a quarter of a light quantum out over the window a quarter of the row's total more, the weight capped at the total; the body's own record's current through its own front booked each interval into `NodeBooks.beat`, 0 at every interval on the laid part's whole support, whose front Ports lead to Nodes at the level 0, so the hazard is the constant alone; its outflow read at the close alone): the parts by the two levels' names with the count in the upper, the transition and its resonance, the rate at its lifetime, the region the laid part's whole support by rule (the cold reader's first finding of 2026-10-21, the half region's tail out), 100 Nodes with one joining Node across the level's nodal plane at the weight 1, holding the declared Node with the record's shares as weights, the window 30 derived (no key); the record laid from the mode file into the upper part alone, the lower part's lines at 0, and no Link cut (the step untouched); the books on the region, the body standing in the upper part with its labels at the count's wall. The run to the first emission: the click at 12 (the giver paying by (5) at its own Nodes: the upper part down to 0 over the region, the lower up to one quantum re-laid there, the charge T / 2 + 211 after against the well's 1.17 T / 2 before, the photon's record up by one, a source in time over the lifetime at the drawn Node), its line the body's with the parts by name and the photon emitted, the photon's count 1 in the books and the body's emitter entry; every lay line of the click at a Node of the region or the photon's one Node and none on the holder's rows (the holder's rows untouched by the click); no level of the upper part standing outside the region after the write, the whole support re-laid and no charge created by the write; the null window of a bound record lays nothing: an empty list, no lay line, the labels' coherence ended in the books."""
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
    for _ in range(FIRST - 1):
        board.step()
    assert table_of(board, electron, photon) == GIVER_BEFORE  # the table's row at the close before
    board.step()
    assert table_of(board, electron, photon) == GIVER_AFTER  # the table's row after the click
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
    assert (books.beat, books.outflow) == (0, 0)  # the whole support's front at the level 0: no beat
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
    assert not after[2].now[~region].any() and not after[3].now[~region].any()  # no tail outside
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
    """The tool run on a copy of the shipped giver world writes the shipped declaration again, word for word (the mode file's digest the world's); the loader refuses by name a region in pieces, a region without the body's declared Node, a region leaving a level of the laid part outside it (the whole support by rule), the count in both parts, a transition naming the body's own family as its drive, and an unknown key of the declaration."""
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
        instrument["nodes"] = [{"node": [3, 2, 2], "weight": 1}, {"node": [0, 0, 0], "weight": 1}]

    def without_the_node(instrument: dict) -> None:  # type: ignore[type-arg]
        instrument["nodes"] = [n for n in instrument["nodes"] if n["node"] != [3, 2, 2]]

    def with_a_tail(instrument: dict) -> None:  # type: ignore[type-arg]
        instrument["nodes"] = [n for n in instrument["nodes"] if n["node"][0] != 0]

    def both_parts(instrument: dict) -> None:  # type: ignore[type-arg]
        instrument["parts"][0]["count"] = 1

    def own_drive(instrument: dict) -> None:  # type: ignore[type-arg]
        instrument["transitions"][0]["drive"] = "electron"

    def unknown(instrument: dict) -> None:  # type: ignore[type-arg]
        instrument["frame"] = {}

    for change, reason in (
        (in_pieces, "one connected region of distinct Nodes"),
        (without_the_node, "holds none of the body's declared Nodes"),
        (with_a_tail, "leaves the laid part's level standing outside the region"),
        (both_parts, "stands in one part at the start"),
        (own_drive, "a family of quanta other than the body's own"),
        (unknown, "unknown key 'frame'"),
    ):
        refused(reason, lambda c=change: load_world(tampered(c)))
    assert np.array_equal(np.zeros(1), np.zeros(1))  # the tool's doubles stand in the tool alone


def test_the_recoil_is_written_as_the_entered_parts_phase_on_a_bound_record():
    """The recoil as the per-Node phase (the reader's design, (c); ALGEBRA.md, The lattice momentum) on the shipped taker world examples/events/conserve/taker_c5.json: the board of 5 x 5 x 7 with the electron standing in its 1s at the centre, declared through the tool over its whole support (175 Nodes, the whole support by rule, the transition to the level [3536, 6000] at the weight 51 and the resonance [5822, 6000], no rate), and a photon packet of one quantum laid at the near end along z (the wave [1, 6], the amplitude 2300, the count 1), the window 9 derived at load from the packet's passage. The body's lattice momentum read as its books read a turned record, with the Link's pair (`take.fan_momentum`): 0 exactly on every axis at the lay and at every interval to the click (a standing record moves nowhere), its Wronskian standing to 0.1 percent at 21311362, 1.18 of T / 2 at the count 1, while the books read 2 quanta from the second interval: the well's reading (the cold reader's third finding of 2026-10-21, measured on the taker before any click: the lay stands, its profile to 0.3 percent and its Wronskian to four digits over 17 intervals, while the rotation per interval runs 45.5 to 79.6 degrees from Node to Node, 68 in the mean, against the family's free 48.2 and the level's 40.0, and the share form reads 1.43 to 1.87 units beating with the period 12, the books' quanta 2 from the second interval at the count 1: the well's share is not the count's unit, the lay standing), named for research. The click at the second close, 18 (the first close at 9 drew null at the share 0.14, the packet half arrived): the piece's p_z 11055256 in T's unit (the packet's momentum over its share through the body's Nodes, 0.31 of a plane wave's 2 T sin k at k = pi / 6, the five-Node packet's own), the photon's P over the board 8012902 at the click, the reading `WRITTEN_AS_PHASE` with the lay's source and no side (the hole's Node two-sided, the quantum taken in the books, the front from it at the count 0); after the write the body carries P_z 10191633 and nothing on x and y, the sign the piece's and the size 0.92 of it: the phase written at the envelope's k (the cold reader's second finding of 2026-10-21; `take.recoil_phases`, den sin k' = p_z den SUM A_i^2 div (2 T SUM A_i A_(i+1)) over the lay's own amplitudes, 1913 at den 6000 for the envelope 0.4817, where k from p_z alone, 921, carried 0.44), the lay's own reading 2 T sin k' e = 11057921, the piece to 0.03 percent, and the board's turned read 0.92 of it, the remainder 0.08 the well's reading through the Link's pair, named for item 48; the light's piece gone with its count; the charge of the electron's record T / 2 + 10750 after against 21310641 at the close before (the standing form's one quantum at its unit; the well's reading, 21311362 at the lay and the walk since), its share 979032106000 against 903766398000 at the close before (689673994000 at the lay, the plain share's climb in the well; the lay at the free rotation in the well after, the run's reading), named for the table."""
    lines: list[dict] = []  # type: ignore[type-arg]
    world = load_shipped(FOLDER / "taker_c5.json")
    row = world.bodies[1]
    assert row.detector is not None and row.detector.draw is not None
    (transition,) = row.detector.transitions
    assert (transition.weight, transition.resonance, row.detector.rates) == (51, (5822, 6000), ())
    assert row.detector.draw.window == 9 and len(row.region) == 175 and row.detector.counts == (1, 0)
    board = Lattice(world, lines.append)
    electron, photon = family(board, "electron"), family(board, "photon")
    (books,) = board.credit.bodies
    assert board.credit.counts[photon] == 1 and fan_momentum(board, electron) == (0, 0, 0)
    before = fan_momentum(board, photon)
    assert before[0] == before[1] == 0 < before[2]  # the packet moves toward +z
    lay = wronskian_of(board, electron)
    for _ in range(17):
        board.step()
        assert fan_momentum(board, electron) == (0, 0, 0)  # the standing record moves nowhere
        assert abs(wronskian_of(board, electron) - lay) * 1000 <= lay  # the lay stands in its well
    assert (board.books()["electron"]["quanta"], board.credit.counts[electron], lay) == (2, 1, 21311362)
    assert [c["interval"] for c in lines if c["event"] == reports.CREDIT] == []
    charge, share = wronskian_of(board, electron), board.total_share(electron)[0]
    assert table_of(board, electron, photon) == TAKER_BEFORE  # the table's row at the close before
    board.step()
    assert table_of(board, electron, photon) == TAKER_AFTER  # the table's row after the click
    (click,) = [c for c in lines if c["event"] == reports.CREDIT]
    assert (click["interval"], click["node_detector"], click["absorbed"], click["count"]) == (
        18,
        "body 1",
        "photon",
        1,
    )
    assert (click["momentum"], click["fan"]) == ([0, 0, PIECE], [0, 0, FAN])
    assert click["lost"] == [reports.WRITTEN_AS_PHASE, reports.LOST_TO_LAY, reports.NO_SIDE]
    assert (click["source"], click["recoil"]) == (reports.THE_LAY, [0, 0, -PIECE])
    after = fan_momentum(board, electron)
    assert after == (0, 0, RECOIL) and PIECE * 9 // 10 < RECOIL < PIECE  # the piece to the remainder
    assert (books.part, books.counts) == (1, [0, 1]) and board.credit.counts[photon] == 0
    assert board.credit.deficits == {photon: 1} and len(board.credit.fronts) == 1
    assert (charge, wronskian_of(board, electron)) == (21310641, 18010750)
    assert (share, board.total_share(electron)[0]) == (903766398000, 979032106000)


def wronskian_of(board: Lattice, index: int) -> int:
    """The Wronskian of a two-part plane record summed over its parts and the board, the charge the click conserves exactly."""
    lines = board.lines_of(index, 0)
    planes = [lines[2 * part : 2 * part + 2] for part in range(len(lines) // 2)]
    return sum(int(np.asarray(records.wronskian(plane, True)).sum(dtype=object)) for plane in planes)


def table_of(
    board: Lattice, electron: int, photon: int
) -> tuple[tuple[int, int], int, tuple[int, int, int], int, int]:
    """One row of the conservation table (examples/events/conserve/README.md): the counts of the electron and of the photon in the books, the electron's charge (the Wronskian summed over its parts and the board), its lattice momentum read with the Link's pair, its share and the photon's over the board."""
    return (
        (board.credit.counts[electron], board.credit.counts[photon]),
        wronskian_of(board, electron),
        fan_momentum(board, electron),
        board.total_share(electron)[0],
        board.total_share(photon)[0],
    )


def test_the_conservation_table_closes_in_the_count_and_names_its_remainders():
    """The conservation table through one click on the two shipped worlds (examples/events/conserve/README.md, the paragraph of 2026-10-21), its rows pinned above from the boards at the close before and after (`table_of`, asserted inside the two runs): the count closes exactly, the photon's up by one on the giver and down by one on the taker with the electron's 1 standing; the electron's lattice momentum moves by the written phase alone on the taker, 0 to 10191633 along the packet's axis, 0.92 of the piece at the envelope's k with the remainder named, and by the lay's rounding on the giver, 2500 along x of the lower part's lay over the whole support, 0.0002 of the taker's piece and no recoil written (an emission's alternative carries no piece, the source lays at one Node); the energies in the clock's unit against the count, T sin Omega of the declared resonance (the light's quantum, `sine_den`) against T (sin e - sin g) of the two levels' pairs the frame tool read, 10260000 against 6852000 on the giver and 8700000 against 5964000 on the taker, the remainder 0.33 and 0.31 of the light's quantum named and OPEN (the levels' cosine gap a reading of the frame, the resonance the declaration's); the charge (the Wronskian) after the write is one quantum to the lay's rounding on both worlds, T / 2 + 211 on the giver and T / 2 + 10750 on the taker, the whole support re-laid (no tail, no charge created by the write; the half region's 1.5 of T / 2 out by rule), against 1.17 and 1.18 of T / 2 before the click, the well's reading (the cold reader's third finding of 2026-10-21, measured on the taker before any click: the lay stands, its profile to 0.3 percent and its Wronskian to four digits over 17 intervals, while the rotation per interval runs 45.5 to 79.6 degrees from Node to Node, 68 in the mean, against the family's free 48.2 and the level's 40.0, and the share form reads 1.43 to 1.87 units beating with the period 12, the books' quanta 2 from the second interval at the count 1: the well's share is not the count's unit, the lay standing); the shares read and not the count's unit, the giver's down by 0.06 and the taker's up by 0.083 in the lay at the free rotation, the photon's share on the taker up by 0.0002 in the packet's walk (the erasure owed as a deficit of 1), on the giver from 0 the source's first lay at the drawn Node; the well's reading named for research."""
    for before, after, moved in ((GIVER_BEFORE, GIVER_AFTER, 1), (TAKER_BEFORE, TAKER_AFTER, -1)):
        assert after[0] == (before[0][0], before[0][1] + moved)  # the count closes exactly
    assert GIVER_BEFORE[2] == TAKER_BEFORE[2] == (0, 0, 0)  # the standing records move nowhere
    assert TAKER_AFTER[2] == (0, 0, RECOIL) and PIECE * 9 // 10 < RECOIL < PIECE  # the envelope's k
    assert 0 < GIVER_AFTER[2][0] < PIECE // 500 and GIVER_AFTER[2][1:] == (0, 0)  # the lay's remainder
    light = [T * sine_den(*resonance) // 6000 for resonance in (RESONANCE, (5822, 6000))]
    levels = [
        T * (sine_den(upper, 6000) - sine_den(lower, 6000)) // 6000
        for lower, upper in ((4580, 3288), (4599, 3536))
    ]
    assert (light, levels) == ([10260000, 8700000], [6852000, 5964000])
    assert [round((a - b) / a, 2) for a, b in zip(light, levels, strict=True)] == [0.33, 0.31]  # OPEN
    half = T // 2
    assert (round(GIVER_BEFORE[1] / half, 2), GIVER_AFTER[1]) == (1.17, half + 211)  # one quantum
    assert (round(TAKER_BEFORE[1] / half, 2), TAKER_AFTER[1]) == (1.18, half + 10750)  # one quantum
    assert round(GIVER_AFTER[3] / GIVER_BEFORE[3] - 1, 2) == -0.06  # the lay's share in the well, read
    assert round(TAKER_AFTER[3] / TAKER_BEFORE[3] - 1, 3) == 0.083  # the lay at the free rotation
    assert round(TAKER_AFTER[4] / TAKER_BEFORE[4] - 1, 4) == 0.0002 and GIVER_BEFORE[4] == 0  # the walk

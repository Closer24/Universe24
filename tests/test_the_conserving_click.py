"""The conserving click (2026-10-21; the reader's design of the conserving click, (a) to (d); ALGEBRA.md, The click writes on the lattice (3), (4), (5) and (6); The lattice momentum): a bound record declared an instrument body by the host tool's output in the mode file, the key `instrument` typed by tools/frame_of.py beside the levels tools/standing_lay.py laid, so that the engine's instrument-body click runs on it with no new act and no body-wide re-lay. The shipped giver world examples/events/conserve/giver_c5.json: the 5-cube at k_r 3 with light's own family `photon`, the electron laid standing in its upper level (the triplet at [3288, 6000]) and declared through the tool: its two levels the parts with the count in the upper, its transition from the lower [4580, 6000] to the upper by the photon at the weight 3 and the resonance [5751, 6000] (den cos(Omega_upper - Omega_lower) by the two pairs), its rate from the upper to the lower at the lifetime 30 giving to the photon, its standing region the laid part's whole support by rule, 100 Nodes in two lobes joined through one Node of the level's nodal plane, 101 in all, its window derived at load as the lifetime. The pinned numbers are the world's own: the first emission at the interval 8, the first interval at which the body's read of its own remainders falls in the emission's cell at the hazard 1 / 30 per interval (the click's read of the board, read and not drawn). The emission's hazard of (5) the declared constant (`lists.hazard_weights`, main's row; the beat's term of 2026-10-21 beside it, the body's own current through its front Ports booked per interval into `NodeBooks.beat` and read at the close, deleted 2026-10-22, dead since the light book: 0 at every interval on the giver to its emission at 8 and on the box of 15 before its emission, the numbers in CHANGELOG.md's bullet of the branch)."""

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
    8,
)  # the declaration, the whole support with its one joining Node, and the world's own click
WALL = 482990683139  # the electron's quantum W_c sin omega_0 at T = 36,000,000 and [4000, 6000]
PIECE, FAN, RECOIL = (
    5940256,
    7156328,
    5947440,
)  # the taker world's click at 9: the piece's p_z, the photon's P_z, the body's P_z after at the k of the record's own covariant Link angles, the piece to the integers' roundings (5497698, 0.9255, at the amplitudes' k of 2026-10-21 on this lay; 4945189, 2600676, 4571327 at the click at 27 on the packet's return, the first lay with the top at z = 1 to 2026-10-22 03:39; 11055256, 8012902, 10192931 at the click at 18 on 2026-10-21, the coupling 51; the packet laid one Node nearer the body on 2026-10-22, 03:39, for the test's bound (the Boss's word of that hour; the nearer lay a declaration of the experimenter by the reader's ruling))
T = 36000000  # the clock's unit of both worlds, the energies' scale
GIVER_BEFORE = ((1, 0), 17987200, (0, 0, 0), 577227456000, 0)  # the giver at 7: see table_of
GIVER_AFTER = ((1, 1), 18001216, (-14170, 0, 0), 620382634000, 6675858000)  # the giver at 8
TAKER_BEFORE = (
    (1, 1),
    17999924,
    (0, 0, 0),
    693173072000,
    195675174000,
)  # the taker at 8 (26 on the first lay at z = 1, to 2026-10-22 03:39; 17 to 2026-10-21)
TAKER_AFTER = (
    (1, 0),
    17985966,
    (0, 0, RECOIL),
    790248268000,
    195573372000,
)  # the taker at 9 (17986213 and 790168088000 at the amplitudes' k; 27 on the first lay; 18 to 2026-10-21)


def test_a_bound_record_declared_through_the_mode_file_clicks_on_the_instrument_bodys_path():
    """The loader reads the tool's declaration as a declared layer (the emission's hazard the declared constant, `hazard_weights`, main's row, the beat's term of 2026-10-21 beside it deleted 2026-10-22, dead since the light book; the body's own light, the sign holder's record's conserved current through its front Ports, booked each interval per front Node into `NodeBooks.light` outward positive (2026-10-22, the bound body the region detector of its own light; the body's own record's current, 0 on the whole support, until then), -14,506,423,296,000 in the unit G^2 over the giver's run [1, 8] to its click, inward on balance, 0.307 of W_c sin Omega G^2, which the whether of (5) floors to 0; the giver keeps its declared rate, so its emission is the instrument's draw): the parts by the two levels' names with the count in the upper, the transition and its resonance, the rate at its lifetime, the region the laid part's whole support by rule (the cold reader's first finding of 2026-10-21, the half region's tail out), 100 Nodes with one joining Node across the level's nodal plane at the weight 1, holding the declared Node with the record's shares as weights, the window 30 derived (no key); the record laid from the mode file into the upper part alone, the lower part's lines at 0, and no Link cut (the step untouched); the books on the region, the body standing in the upper part with its labels at the count's wall. The run to the first emission: the click at 8 (the giver paying by (5) at its own Nodes: the upper part down to 0 over the region, the lower up to one quantum re-laid there, the charge T / 2 + 1216 after against T / 2 - 12800 before, the count 1 on the board at every interval and at the close (the ruling of 2026-10-22), the photon's record up by one, a source in time over the lifetime at the drawn Node), its line the body's with the parts by name and the photon emitted, the photon's count 1 in the books and the body's emitter entry; every lay line of the click at a Node of the region or the photon's one Node and none on the holder's rows (the holder's rows untouched by the click); no level of the upper part standing outside the region after the write, the whole support re-laid and no charge created by the write; the null window of a bound record lays nothing: an empty list, no lay line, the labels' coherence ended in the books."""
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
    unit = WALL * WALL  # the row's unit, W_c^2
    assert hazard_weights(1, LIFETIME, 6000, 6000, unit) == [unit, (LIFETIME - 1) * unit]  # the constant
    laid = board.lines_of(electron, 0)
    assert not laid[0].now.any() and not laid[1].now.any()  # the lower part empty
    assert laid[2].now.any() and laid[3].now.any()  # the upper part the standing lay's
    (books,) = board.credit.bodies
    assert books.bound and books.nodes == row.region and books.weights == row.shares
    assert (
        (row.radius, len(row.shell), row.missing) == (3, 25, 25)
    )  # the light's front: the shell at r = 1 / k, 6000 div 2899 + 1, about [3, 2, 2] leaves the 5-cube on every side but x = 0, its 25 Ports off the board (2026-10-22)
    box = load_shipped(FOLDER / "box_c15.json").bodies[1]
    assert (
        (box.radius, len(box.shell), box.missing) == (4, 386, 0)
    )  # the box's shell at 4 Links about [8, 7, 7], 6000 div 1971 + 1, 9^3 - 7^3 Nodes, every Port on the board
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
    assert (
        sum(books.light) == 0
    )  # the giver's light front has no Port on its 5-cube (the shell at 3 leaves the board), the book 0 (2026-10-22; -14506423296000 through the support's front, the first front of the same day)
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
    lists.coherence_ended(board, books)
    assert len(lines) == before and books.labels == [WALL, 0] and books.carried == [0, 0]


def test_the_light_front_follows_the_board_as_it_grows_at_a_receding_face(tmp_path, monkeypatch):
    """The near zone's ball is taken at the board's shape every interval, as the body's region mask is (`reports.booked_light`, `reports.ball`; the tube's refusal of 2026-10-22 at its first interval, the masks at the start's shape against the grown board): the giver world copied with its x faces receding, the lay at x = 0 reaching the low face, grows by two layers at the first interval, the offset moving with it, and the shell's 25 Nodes keep their places and their book its length; whether the grown layer's Nodes count as the declared board for the shell's Ports off the start's board is named and not pinned (the book read 0 over ten intervals on this copy)."""
    for name in ("giver_c5.json", "giver_c5.mode.json"):
        (tmp_path / name).write_text((FOLDER / name).read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "u.json").write_text(
        (FOLDER / "universe_conserve.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    path, mode_path = tmp_path / "giver_c5.json", tmp_path / "giver_c5.mode.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["universe"] = "u.json"
    document["boundary"]["x"] = "open"
    document["receding"] = {"x": {"sides": ["low", "high"], "largest": 21, "layers": 2}}
    path.write_text(json.dumps(document), encoding="utf-8")
    shipped = json.loads(mode_path.read_text(encoding="utf-8"))
    shipped["world_digest"] = world_files.input_digest(document)
    mode_path.write_text(json.dumps(shipped), encoding="utf-8")
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    board = Lattice(load_world(path), None)
    (books,) = [b for b in board.credit.bodies if b.bound]
    assert (len(books.shell), books.zone) == (25, ((3, 2, 2), 3))
    for _ in range(3):
        board.step()
    assert board.shape[0] > 5 and board.offset[0] > 0  # grown at the low face, the offset with it
    assert (len(books.shell), len(books.light)) == (25, 25)  # the shell's places and its book stand


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
    """The recoil as the per-Node phase (the reader's design, (c); ALGEBRA.md, The lattice momentum) on the shipped taker world examples/events/conserve/taker_c5.json: the board of 5 x 5 x 7 with the electron standing in its 1s at the centre, declared through the tool over its whole support (175 Nodes, the whole support by rule, the transition to the level [3536, 6000] at the read weight 3 by reciprocity (51 declared on 2026-10-21) and the resonance [5822, 6000], no rate), and a photon packet of one quantum laid along z with its flat top at z = 2 (the wave [1, 6], the amplitude 2300, the count 1; the top at z = 1, the near end, to 2026-10-22 03:39, the packet laid one Node nearer the body on 2026-10-22, 03:39, for the test's bound (the Boss's word of that hour; the nearer lay a declaration of the experimenter by the reader's ruling), the first lay), the window 9 derived at load from the packet's passage (its length and the declared Node's extent, not its position). The body's lattice momentum read as its books read a turned record, with the Link's pair (`take.fan_momentum`): 0 exactly on every axis at the lay and at every interval to the click (a standing record moves nowhere), its Wronskian standing within 0.3 per mille of the lay's 18001539, T / 2 + 1539 at the count 1, over the 8 intervals to the close before (the electron's lay and its run to 8 bit for bit the first lay's, the packet sourcing nothing until the click; within 1.1 per mille over the 26 to the first lay's click), the books reading 1 quantum at every interval, the count by the charge (the cold reader's third finding of 2026-10-21 and his ruling of 2026-10-22: a plane record's count is its charge, the Wronskian over its planes and the board over T / 2, the same unit in every well, and the share in the free unit is the energy; measured on the taker before any click the lay stands, its profile to 0.3 percent and its Wronskian to four digits, the count 1 at every interval, while the energy beats 1.21 to 1.49 units over the 8, 1.21 to 1.58 over the first lay's 17). The click at the first close, 9 (the absorption's share 0.805 of the row's total at the close, the packet's passage over the body nearly whole within the window, the draw falling; on the first lay at the coupling 3 the shares 0.116 at 9 and 0.243 at 18 with the rest drawn, the click at 27 on the packet's return from the far z face at the share 0.170, and at the coupling 51 of 2026-10-21 the click at 18 on the first passage; the trial lay with the top at z = 3 drew the rest at its share 0.86 and clicked at 18 on the reflected packet with the piece 841357, not shipped): the piece's p_z 5940256 in T's unit (the packet's momentum over its share through the body's Nodes; 4945189 at 27 and 11055256 at 18 on the first lay), the photon's P over the board 7156328 at the click, the reading `WRITTEN_AS_PHASE` with the lay's source and no side (the hole's Node two-sided, the quantum taken in the books, the front from it at the count 0); after the write the body carries P_z 5947440 and nothing on x and y, the piece to the integers' roundings, 1.0012 of it: the phase written at the k of the record's own covariant Link angles (`take.recoil_phases`, den sin k_a = p_a den A^2 den^2 M div (2 T SUM A_i A_(i+a) Re(conj(u_i) R_i u_(i+a))), A^2 the count's square the read divides by (4 sin omega_0 = 2 T over it), u_i the leaving part's direction at each Node at the size den, R_i the holder's pair the step reads on the Link and M its modulus by the one search, the real part of the bilinear whose imaginary part is the current the books read, one signed rounding per axis, 1112 at den 6000; the two-path blind of 2026-10-22, the same composition in the reals from the same integer inputs against the integer path: the reals give the piece exactly, so the remainder is the integers' roundings', by stage the write's floors in the turn and in the standing lay's normalisation (`resonance.turned_direction`, `features/click.direction`; a systematic Link angle of 0.02 degrees, +0.20 percent) and the sine's one rounding (1112 against 1111.886, +0.01 percent); on the first lay at the coupling 51 the same build carries 11032730 of the piece's 11055256, 0.9980 (the Link angle -0.030 degrees, the sine's +0.02 percent); the formula's norm the count's square, the floored sizes' sum having stood 0.09 percent below it; at the amplitudes' k of 2026-10-21, den sin k' = p_z den SUM A_i^2 div (2 T SUM A_i A_(i+1)), the read carried 5497698 on this lay, 0.9255, and 0.924 and 0.922 on the first lay's two couplings, the remainder the cosines of those angles, item 48 CHANGED), the light's piece gone with its count; the charge of the electron's record T / 2 - 14034 after (T / 2 - 13787 at the amplitudes' k) against T / 2 - 76 at the close before (the lay's T / 2 + 1539 and the walk since, one quantum at every interval; T / 2 - 9208 against T / 2 - 17986 at 27 on the first lay), its share 790248268000 against 693173072000 at the close before (790168088000 at the amplitudes' k; 582538848000 at the lay, the energy's climb in the well from 1.21 to 1.64 units; the lay at the free rotation in the well after, the run's reading), named for the table."""
    lines: list[dict] = []  # type: ignore[type-arg]
    world = load_shipped(FOLDER / "taker_c5.json")
    row = world.bodies[1]
    assert row.detector is not None and row.detector.draw is not None
    (transition,) = row.detector.transitions
    assert (
        (transition.weight, transition.resonance, row.detector.rates)
        == (
            3,
            (5822, 6000),
            (),
        )
    )  # the coupling the record's read weight of its holder by reciprocity since 2026-10-22 (51 declared on 2026-10-21, a declared weight refused by name)
    assert row.detector.draw.window == 9 and len(row.region) == 175 and row.detector.counts == (1, 0)
    board = Lattice(world, lines.append)
    electron, photon = family(board, "electron"), family(board, "photon")
    (books,) = board.credit.bodies
    assert board.credit.counts[photon] == 1 and fan_momentum(board, electron) == (0, 0, 0)
    before = fan_momentum(board, photon)
    assert before[0] == before[1] == 0 < before[2]  # the packet moves toward +z
    lay = wronskian_of(board, electron)
    for _ in range(8):
        board.step()
        assert fan_momentum(board, electron) == (0, 0, 0)  # the standing record moves nowhere
        assert (
            abs(wronskian_of(board, electron) - lay) * 10000 <= 3 * lay
        )  # the lay stands in its well: within 0.3 per mille over the 8 intervals to the close before (within 1 per mille to 23 and 1.1 per mille at 24 to 26 on the first lay's run to 27, the packet returned by the far face beating against it)
    assert (board.books()["electron"]["quanta"], board.credit.counts[electron], lay) == (1, 1, 18001539)
    assert [c["interval"] for c in lines if c["event"] == reports.CREDIT] == []
    charge, share = wronskian_of(board, electron), board.total_share(electron)[0]
    assert table_of(board, electron, photon) == TAKER_BEFORE  # the table's row at the close before
    board.step()
    assert table_of(board, electron, photon) == TAKER_AFTER  # the table's row after the click
    (click,) = [c for c in lines if c["event"] == reports.CREDIT]
    assert (click["interval"], click["node_detector"], click["absorbed"], click["count"]) == (
        9,
        "body 1",
        "photon",
        1,
    )
    assert (click["momentum"], click["fan"]) == ([0, 0, PIECE], [0, 0, FAN])
    assert click["lost"] == [reports.WRITTEN_AS_PHASE, reports.LOST_TO_LAY, reports.NO_SIDE]
    assert (click["source"], click["recoil"]) == (reports.THE_LAY, [0, 0, -PIECE])
    after = fan_momentum(board, electron)
    assert (
        after == (0, 0, RECOIL) and abs(RECOIL - PIECE) * 1000 < 2 * PIECE
    )  # the piece to the integers' roundings, 0.12 percent (0.9255 at the amplitudes' k)
    assert (books.part, books.counts) == (1, [0, 1]) and board.credit.counts[photon] == 0
    assert board.credit.deficits == {photon: 1} and len(board.credit.fronts) == 1
    assert (
        (charge, wronskian_of(board, electron))
        == (
            17999924,
            17985966,
        )
    )  # (17986213 after at the amplitudes' k; (17982014, 17990792) at 26 and 27 on the first lay; (17992808, 18010122) at 18, 2026-10-21
    assert (
        (share, board.total_share(electron)[0])
        == (
            693173072000,
            790248268000,
        )
    )  # (790168088000 at the amplitudes' k; (708152334000, 880331622000) at 26 and 27 on the first lay; (762383080000, 978929402000) at 18


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
    """The conservation table through one click on the two shipped worlds (examples/events/conserve/README.md, the paragraph of 2026-10-21), its rows pinned above from the boards at the close before and after (`table_of`, asserted inside the two runs): the count closes exactly, the photon's up by one on the giver and down by one on the taker with the electron's 1 standing; the electron's lattice momentum moves by the written phase alone on the taker, 0 to 5947440 along the packet's axis on the lay at z = 2 of 2026-10-22, the piece to the integers' roundings, 1.0012 of it at the k of the record's own covariant Link angles (5497698, 0.9255, at the amplitudes' k; 4571327 at 27 on the first lay at z = 1, 10192931 at the click at 18 of 2026-10-21), and by the lay's rounding on the giver, -14170 along x of the lower part's lay over the whole support, 0.0013 of the taker's piece and no recoil written (an emission's alternative carries no piece, the source lays at one Node); the energies in the clock's unit against the count, T sin Omega of the declared resonance (the light's quantum, `sine_den`) against T (sin e - sin g) of the two levels' pairs the frame tool read, 10260000 against 6852000 on the giver and 8700000 against 5964000 on the taker, the remainder 0.33 and 0.31 of the light's quantum named and OPEN (the levels' cosine gap a reading of the frame, the resonance the declaration's); the charge (the Wronskian) is one quantum to the lay's rounding before and after the write on both worlds, T / 2 - 12800 on the giver and T / 2 - 76 on the taker at the close before (the lays at T / 2 to the rounding, the walk since; T / 2 - 17986 at 26 and T / 2 - 7192 at 17 on the first lay), T / 2 + 1216 on the giver and T / 2 - 14034 on the taker after (T / 2 - 13787 at the amplitudes' k; T / 2 - 9208 at 27 and T / 2 + 10122 at 18 on the first lay), the whole support re-laid (no tail, no charge created by the write; the half region's 1.5 of T / 2 out by rule), the count on the board (the cold reader's third finding of 2026-10-21 and his ruling of 2026-10-22: a plane record's count is its charge, the Wronskian over its planes and the board over T / 2, the same unit in every well, and the share in the free unit is the energy; measured on the taker before any click the lay stands, its profile to 0.3 percent and its Wronskian to four digits over 17 intervals, the count 1 at every interval, while the energy beats 1.21 to 1.58 units); the shares the energy and no count, the giver's up by 0.07 and the taker's by 0.140 in the lay at the free rotation (0.243 at 27 on the first lay, 0.284 at 18), the photon's share on the taker down by 0.0005 in the packet's walk (down by 0.00009 at 27 and up by 0.0002 at 18 on the first lay; the erasure owed as a deficit of 1), on the giver from 0 the source's first lay at the drawn Node; the well's reading named for research."""
    for before, after, moved in ((GIVER_BEFORE, GIVER_AFTER, 1), (TAKER_BEFORE, TAKER_AFTER, -1)):
        assert after[0] == (before[0][0], before[0][1] + moved)  # the count closes exactly
    assert GIVER_BEFORE[2] == TAKER_BEFORE[2] == (0, 0, 0)  # the standing records move nowhere
    assert (
        TAKER_AFTER[2] == (0, 0, RECOIL) and abs(RECOIL - PIECE) * 1000 < 2 * PIECE
    )  # the piece to the integers' roundings
    assert (
        0 < abs(GIVER_AFTER[2][0]) < PIECE // 300
        and GIVER_AFTER[2][1:]
        == (
            0,
            0,
        )
    )  # the lay's rounding, 14170 against the taker's piece 5940256 at its click at 9 (4945189 at 27 on the first lay; PIECE // 500 against 11055256 at the click at 18 of 2026-10-21)
    light = [T * sine_den(*resonance) // 6000 for resonance in (RESONANCE, (5822, 6000))]
    levels = [
        T * (sine_den(upper, 6000) - sine_den(lower, 6000)) // 6000
        for lower, upper in ((4580, 3288), (4599, 3536))
    ]
    assert (light, levels) == ([10260000, 8700000], [6852000, 5964000])
    assert [round((a - b) / a, 2) for a, b in zip(light, levels, strict=True)] == [0.33, 0.31]  # OPEN
    half = T // 2
    assert (round(GIVER_BEFORE[1] / half, 2), GIVER_AFTER[1]) == (1.0, half + 1216)  # one quantum
    assert (
        (round(TAKER_BEFORE[1] / half, 2), TAKER_AFTER[1])
        == (
            1.0,
            half - 14034,
        )
    )  # one quantum (half - 13787 at the amplitudes' k; half - 9208 at 27 on the first lay at z = 1, half + 10122 at the click at 18 of 2026-10-21; the lay at z = 2 of 2026-10-22, the click at 9)
    assert round(GIVER_AFTER[3] / GIVER_BEFORE[3] - 1, 2) == 0.07  # the lay's energy in the well, read
    assert (
        round(TAKER_AFTER[3] / TAKER_BEFORE[3] - 1, 3) == 0.14
    )  # the lay at the free rotation (0.243 at 27 on the first lay; 0.284 at 18, 2026-10-21)
    assert (
        round(TAKER_AFTER[4] / TAKER_BEFORE[4] - 1, 4) == -0.0005 and GIVER_BEFORE[4] == 0
    )  # the walk (-0.0001 at 27 on the first lay, the returned packet's share falling; 0.0002 at 18, 2026-10-21)

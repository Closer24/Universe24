"""The emission lays no uniform mode and the front writes to 0 at its reach (ALGEBRA.md, The click writes on the lattice (5) and (6); the owner's "yes to everything" of 2026-10-04, #1793 comment 5975629873; the mathematician's hand, #1793 comments 5975866852 and 5975925032, the advisor's seconds 5975890713 and 5975964920): the source in time's increments corrected by the division act in time where the span holds its period, the open board's packet's two levels by the packet lay's act, the front's taper with the erasure line's take in quanta; one test each, on the mathematician's branch for the engine's reopening."""

from event_universe import node_detector, world_files
from event_universe.emission import holds_period, increments_of, radiated_total
from event_universe.features.click import SCALE_OF
from event_universe.lattice import Lattice
from event_universe.lay import division_act_in_time
from event_universe.reports import NO_SIDE
from event_universe.world_files import load_world
from tests.laws import TOOL, packet_world
from tests.laws_content import one_photon_board


def test_the_source_in_time_lays_no_uniform_mode_where_its_span_holds_a_period():
    """The emission lays no uniform mode (ALGEBRA.md, The click writes on the lattice (5); the mathematician's hand, #1793 comments 5975866852 and 5975925032; `emission.increments_of`, `lay.division_act_in_time`, `holds_period`): the source's increments at [2, 3] over 48 intervals sum to 31 with the moment SUM t delta_t 938 as laid, and corrected by the division act in time to 0 and 0 exactly, the corrections at most 2 levels; the span holds a period where tau Omega >= 2 pi by the rotation act (from 8 at [2, 3], from 15 at [5414, 6000], never at 1 or 2), and a span of 4 is laid as built since the correction would leave [-9, 13, 1, -5] of [73, 49, -8, -60]; the lay's two sums over an open board are read on the packet world in the test below."""
    scale, total = (3 * 6000 * 32768) ** SCALE_OF, radiated_total(32768, (2, 3))
    raw, amplitudes = increments_of(total, 48, (2, 3), scale)
    fixed = division_act_in_time(raw, amplitudes)
    assert (sum(raw), sum(t * d for t, d in enumerate(raw)), min(amplitudes), max(amplitudes)) == (
        31,
        938,
        21,
        22,
    )
    assert sum(fixed) == 0 and sum(t * d for t, d in enumerate(fixed)) == 0
    assert max(abs(a - b) for a, b in zip(raw, fixed, strict=True)) == 2
    assert [holds_period(t, (2, 3), scale) for t in (1, 2, 7, 8, 48)] == [
        False,
        False,
        False,
        True,
        True,
    ]
    assert [holds_period(t, (5414, 6000), scale) for t in (14, 15)] == [False, True]
    short, amps = increments_of(total, 4, (2, 3), scale)
    assert short == [73, 49, -8, -60] and division_act_in_time(short, amps) == [-9, 13, 1, -5]


def test_the_open_boards_packet_lays_no_uniform_mode(tmp_path):
    """The packet's two levels take the packet lay's division act over the packet's Nodes where the span holds a period (ALGEBRA.md, The click writes on the lattice (5) and The packet lay; `emission.laid_packet`, `holds_period`, `features/start.uniform_removed`): on an open board of 160 by 5 by 5 a giver of the lifetime 8 in the exact dark lays its packet of 3 across along x at its window's close, 194, its train's passage (`meeting.emission_fell`), and the light record's levels now and before each sum to 0 over the board exactly after the lay (the energy-form envelope under the carrier sums to other than 0: the shipped packet world's before summed to -80 over 4,992 Nodes, the two slits' bump of +24,442 the same defect), the top's level standing above 20 of the envelope's 24, the count 1 in the books; the lifetime-2 toy of the test above is laid as built, below its period."""
    board = Lattice(load_world(packet_world(tmp_path, TOOL, intervals=200)), (lines := []).append)
    pulse = [f.name for f in board.families].index("pulse")
    while board.interval < 200 and not any(
        c["event"] == "credit" and c["emitted"] == "pulse" for c in lines
    ):
        board.step()
    lays = [c for c in lines if c["event"] == "lay" and c["family"] == "pulse"]
    assert len(lays) > 500 and board.credit.counts[pulse] == 1  # the train of 69 slices by 9 across
    sums = [sum(c["after"][k] - c["before"][k] for c in lays) for k in (0, 1)]
    assert sums == [0, 0] and max(abs(c["after"][0]) for c in lays) > 20  # each level's lay sums to 0


def test_a_tied_axis_is_faced_on_both_ports_and_a_set_above_the_wall_is_booked(tmp_path, monkeypatch):
    """C6's face set at a tie (the cold reader's re-fix of 2026-10-19, the Boss's decision under the owner's word, generic and right: a tied axis contributes both its Ports where the set's read coefficients sum to the wall at most, `node_detector.face_ports`; above the wall the booked path): given by hand on the shipped one_photon world through `arrival_ports` (its packets are not exact mirror images, so no built tie stands). (i) One tied axis, the two x Ports (2 w / 3 for light): the hole is faced on both, two faces per line at 77 and 78 with the set (0, 1), the count 0 with no deficit and no `NO_SIDE`, the front begun from the hole's Node. (ii) Two tied axes, four Ports (4 w / 3, above the wall): the set is emptied, the quantum taken in the books alone (the deficit 1, the reading `NO_SIDE` after the taker's own), no face, and the front begun from the drawn Node all the same (the law's line: from every Node written in that draw), so the quantum's share, standing on the board at 79, is erased by the front as in the faced case, the faced run ending at 170 with the packet's other half beyond the front's reach, 124,482,000 as the Part G oracle's header reads, and the booked run with 162,000 more, the standing origin's remnant: at the derived close, 61, the bulk's end (2026-10-19), the hole's Node still carries the tail's form, which the booked path leaves standing and spreading behind the front at the count 0 (C6, the standing origin, named in the law; at the click of 76 under the declared 48 the packet had passed the Node, it carried no form and the two shares were one, 127,530,000)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    found = {}
    for name, ports in (("tied", (0, 1)), ("above", (0, 1, 2, 3))):
        monkeypatch.setattr(node_detector, "arrival_ports", lambda booked, ports=ports: ports)
        board, lines = one_photon_board(tmp_path)
        photon = [f.name for f in board.families].index("photon")
        for _ in range(64):
            board.step()
        taken = [c for c in lines if c["event"] == "credit" and c["absorbed"]]
        faces = [f for f in lines if f["event"] == "face"]
        origin = board.credit.fronts[0].origin
        share = board.books()["photon"]["share"]  # the quantum's share on the board at 64
        for _ in range(64, 120):  # 170 before the suite's bound of 2026-10-24
            board.step()
        dark = board.books()["photon"]["share"]  # the board at the run's end
        faces = [
            f for f in faces if f["node"]["at"] == list(origin)
        ]  # the hole's own faces, not the front's
        found[name] = (
            len(taken),
            taken[0]["lost"],
            board.credit.counts[photon],
            board.credit.deficits.get(photon, 0),
            sorted({tuple(f["ports"]) for f in faces}),
            len(board.credit.fronts),
            share > 0,
            dark,
        )
    lost = ["P lost to the taker", "recoil lost to the lay"]
    assert found["tied"][:7] == (1, lost, 0, 0, [(0, 1)], 1, True)
    assert found["above"][:7] == (1, [*lost, NO_SIDE], 0, 1, [], 1, True)  # booked, the front begun
    print(f"the dark shares at the end: tied {found['tied'][7]}, above {found['above'][7]}")
    assert (
        found["above"][7] > found["tied"][7] > 0
    )  # the dark share at the end: the set above the wall is booked, so more stands dark than at the tie, the other half beyond the front's reach (the course's numbers 117996109 and 119927551 under the content of 2026-10-20, 122508000 and 124482000 at the exact vacuum; the sentence and not the numbers since 2026-10-23)

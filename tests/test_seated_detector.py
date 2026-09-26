"""THE SEATED DETECTOR (ALGEBRA.md 9.46 (8) (c); the model owner's word of 2026-09-25 in
Nature24's session, "start", on the cube rule of record 1899 lifted for seats under
`body_record`; BUILD.md section 26 item 40): under the world key `body_record` a detector may be
ONE Node, its seat, whose six Links are its Ports (four on a layer, two on a chain), a set of
more than one Node keeping the cube rule; the click is the seat's, the flux into it through its
Ports from outside, Born's rule at the taking end the increment ladder on the plain flux as for
a cube; a seated detector's inflow per interval is its Ports' share of a
cube's, so its clicks come later and, where records can leave, fewer (9.46 (8) (c): the
counts rescaled, the pattern not). On the detector-law layer (80 by 9, closed at both x faces,
the emitter's train across the whole width, three places at x = 70 on the rows 1, 4 and 7):
(i) three seats against the three cubes over the same run of 60 giving clicks: every record
clicks at one of the places on both forms (nothing leaves the closed layer), the seats' clicks
come later (the mean wait from the giving to the taking click longer), and the three places
share alike within the draw on both forms (the train uniform across the width); (ii) at every seat's click the detector is the one the increment ladder chooses on the
plain flux (Born's rule, 9.25 (2) and (3), item 36) and the taker's content rises by one;
(iii) the loader: one Node without `body_record` refused naming record 1899, two Nodes under
it refused naming the seat, a seated block of extents [1, 1, 1] bound as its own detector
admitted under the key and refused without it. Every number a COMPUTATION; GAMEBOARD; no pin."""

from __future__ import annotations

import json

import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.test_body_record import with_body_record
from tests.test_detector_law import Seen, chosen_by_the_rule, layer_world, spy_on

PLACES = ((1, "s0"), (4, "s1"), (7, "s2"))
STOCK = 60


def seated_layer(stock: int = STOCK, seats: bool = True) -> dict:
    """The layer world with the emitter's stock `stock` and its three places as seats (one
    receiver body of light at (71, row) read as the set) or as the cubes of the layer test."""
    document = layer_world(receiver=[name for _, name in PLACES])
    # the stock as the given family's content held at the body (ALGEBRA.md 9.51 (8); item 47)
    document["measured"][0]["stocks"] = {"light": stock}
    document["ticks"] = stock * 250 + 300  # every giving a window and a rung (commit 7)
    if seats:
        document["measured"] = [document["measured"][0]]
        document["detectors"] = []
        for row, name in PLACES:
            document["measured"].append(
                {
                    "position": [71, row, 0],
                    "family": "light",
                    "amount": 1,
                    "stocks": {},
                    "momentum": [0, 0, 0],
                }
            )
            document["detectors"].append({"name": name, "positions": [[71, row, 0]]})
    document["stamp"] = input_stamp(document)
    return with_body_record(document, True)


def run(document: dict) -> tuple[DetectorLawSimulation, list[dict], Seen]:
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    seen: Seen = {}
    spy_on(simulation, seen)
    for _ in range(document["ticks"]):
        simulation.step()
    assert simulation.books()["balanced"]
    return simulation, lines, seen


def counts_of(lines: list[dict]) -> tuple[dict[str, int], float]:
    """The clicks per place (the face for the rest) and the mean wait from a record's giving
    click to its taking click."""
    gathers = [line for line in lines if line["event"] == "gather"]
    counts = {name: 0 for _, name in PLACES}
    counts["face"] = 0
    waits = []
    for line in gathers:
        chosen = line["chosen"][0][0] if line["chosen"] else None
        if chosen in counts:
            counts[chosen] += 1
        else:
            counts["face"] += 1
        waits.append(line["tick"] - line["giving"])
    return counts, sum(waits) / len(waits)


def test_three_seats_click_later_than_three_cubes_and_share_alike():
    """(i) On the closed layer (mirrors at both x faces, y periodic) every one of the 60 records
    clicks at one of the three places on both forms (nothing leaves); the seats' clicks come
    later than the cubes' (the mean wait from the giving click to the taking click longer: the
    flux into a seat per interval is its four Ports' against the cube's twelve, so the running
    total reaches the record's threshold later); the three places share the records alike on
    both forms (the train is uniform across the periodic width: each place within 9 of 20);
    the Ports: four per seat, twelve per cube."""
    seated, seat_lines, _ = run(seated_layer(seats=True))
    cubed, cube_lines, _ = run(seated_layer(seats=False))
    seat_counts, seat_wait = counts_of(seat_lines)
    cube_counts, cube_wait = counts_of(cube_lines)
    assert sum(seat_counts.values()) == STOCK == sum(cube_counts.values())
    assert seat_counts["face"] == 0 == cube_counts["face"], (seat_counts, cube_counts)
    assert seat_wait > cube_wait, (seat_wait, cube_wait)
    for counts in (seat_counts, cube_counts):
        for _, name in PLACES:
            assert abs(counts[name] - STOCK // 3) <= 9, counts
    _, _, port_detector = seated._inflow_ports(0)
    for _, name in PLACES:
        detector = seated.detector_names.index(name)
        assert int((port_detector == detector).sum()) == 4, name
    _, _, port_detector = cubed._inflow_ports(0)
    for _, name in PLACES:
        detector = cubed.detector_names.index(name)
        assert int((port_detector == detector).sum()) == 12, name


def test_borns_rule_at_a_seat_is_the_increment_ladder_on_the_plain_flux():
    """(ii) At every seat's click the detector chosen is the increment ladder's on the plain
    flux against the norm's rational, and the seat's content rises by one per click."""
    seated, lines, seen = run(seated_layer(stock=20, seats=True))
    gathers = [line for line in lines if line["event"] == "gather" and line["chosen"]]
    assert gathers
    for line in gathers:
        total, increments, ladder, u, norm, wheel, pace = seen[line["record"]]
        assert line["chosen"][0][0] == chosen_by_the_rule(
            seated, total, increments, ladder, u, norm, wheel, pace
        )
    for index, (_row, name) in enumerate(PLACES):
        number = index + 1  # the seat's measured event
        taken = sum(1 for line in gathers if line["chosen"][0][0] == name)
        assert sum(seated.held[number]) == 1 + taken, name


def test_the_loader_admits_a_seat_under_body_record_alone():
    """(iii) One Node without `body_record` is refused naming record 1899; two Nodes under it
    are refused naming the seat; a block of extents [1, 1, 1] bound as its own detector is
    admitted under the key and refused without it."""
    document = seated_layer(stock=2, seats=True)
    parse_nature_beam_world(document)
    # SINCE COMMIT 7 a detector of one Node is admitted on every world (ALGEBRA.md 9.92,
    # record 2109: several bodies on one Node each are several detectors), the lattice body's too
    lattice = json.loads(json.dumps(document))
    lattice["body_record"] = False
    lattice["stamp"] = input_stamp(lattice)
    parse_nature_beam_world(lattice)
    pair = json.loads(json.dumps(document))
    pair["measured"].append(
        {
            "position": [72, 1, 0],
            "family": "light",
            "amount": 1,
            "stocks": {},
            "momentum": [0, 0, 0],
        }
    )
    pair["detectors"][0]["positions"] = [[71, 1, 0], [72, 1, 0]]
    pair["stamp"] = input_stamp(pair)
    with pytest.raises(ValueError, match="one Node .a body's. or a cube of three or more"):
        parse_nature_beam_world(pair)

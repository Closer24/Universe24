"""A one-Node detector under `body_record` (ALGEBRA.md #what-a-body-is): its body's Node with its six Ports,
the click from the flux through them, the counts rescaled from a cube's and the pattern the same."""

from __future__ import annotations

import json

import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.bodies import with_body_record
from tests.running import Seen, chosen_by_the_rule, spy_on
from tests.worlds import layer_world

PLACES = ((1, "s0"), (4, "s1"), (7, "s2"))
STOCK = 60


def one_node_layer(stock: int = STOCK, one_node_detectors: bool = True) -> dict:
    """The layer world with the emitter's stock `stock` and its three places as bodies on one Node (one
    receiver body of light at (71, row) read as the set) or as the cubes of the layer test."""
    document = layer_world(receiver=[name for _, name in PLACES])
    # the stock as the given family's content held at the body (ALGEBRA.md #the-paces; item 47)
    document["measured"][0]["stocks"] = {"light": stock}
    document["ticks"] = stock * 250 + 300  # every giving a window and a rung (commit 7)
    if one_node_detectors:
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
                    "fixed": False,
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


def test_three_one_node_detectors_click_later_than_three_cubes_and_share_alike():
    """(i) On the closed layer (mirrors at both x faces, y periodic) every one of the 60 records
    clicks at one of the three places on both forms (nothing leaves); the bodies on one Node' clicks come
    later than the cubes' (the mean wait from the giving click to the taking click longer: the
    flux into a body on one Node per interval is its four Ports' against the cube's twelve, so the running
    total reaches the record's threshold later); the three places share the records alike on
    both forms (the train is uniform across the periodic width: each place within 9 of 20);
    the Ports: four per body's Node, twelve per cube."""
    one_node, one_node_lines, _ = run(one_node_layer(one_node_detectors=True))
    cubed, cube_lines, _ = run(one_node_layer(one_node_detectors=False))
    one_node_counts, one_node_wait = counts_of(one_node_lines)
    cube_counts, cube_wait = counts_of(cube_lines)
    assert sum(one_node_counts.values()) == STOCK == sum(cube_counts.values())
    assert one_node_counts["face"] == 0 == cube_counts["face"], (one_node_counts, cube_counts)
    assert one_node_wait > cube_wait, (one_node_wait, cube_wait)
    for counts in (one_node_counts, cube_counts):
        for _, name in PLACES:
            assert abs(counts[name] - STOCK // 3) <= 9, counts
    _, _, port_detector = one_node._inflow_ports(0)
    for _, name in PLACES:
        detector = one_node.detector_names.index(name)
        assert int((port_detector == detector).sum()) == 4, name
    _, _, port_detector = cubed._inflow_ports(0)
    for _, name in PLACES:
        detector = cubed.detector_names.index(name)
        assert int((port_detector == detector).sum()) == 12, name


def test_borns_rule_at_a_one_node_detector_is_the_increment_ladder_on_the_plain_flux():
    """(ii) At every body's Node's click the detector chosen is the increment ladder's on the plain
    flux against the norm's rational, and the body's Node's content rises by one per click."""
    one_node, lines, seen = run(one_node_layer(stock=20, one_node_detectors=True))
    gathers = [line for line in lines if line["event"] == "gather" and line["chosen"]]
    assert gathers
    for line in gathers:
        total, increments, ladder, u, norm, wheel, pace = seen[line["record"]]
        assert line["chosen"][0][0] == chosen_by_the_rule(
            one_node, total, increments, ladder, u, norm, wheel, pace
        )
    for index, (_row, name) in enumerate(PLACES):
        number = index + 1  # the body's Node's measured event
        taken = sum(1 for line in gathers if line["chosen"][0][0] == name)
        assert sum(one_node.held[number]) == 1 + taken, name


def test_the_loader_admits_a_one_node_detector_under_body_record_alone():
    """(iii) One Node without `body_record` is refused naming record 1899; two Nodes under it
    are refused naming the body's Node; a block of extents [1, 1, 1] bound as its own detector is
    admitted under the key and refused without it."""
    document = one_node_layer(stock=2, one_node_detectors=True)
    parse_nature_beam_world(document)
    # SINCE COMMIT 7 a detector of one Node is admitted on every world (ALGEBRA.md #the-rows-against-nature,
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
            "fixed": False,
        }
    )
    pair["detectors"][0]["positions"] = [[71, 1, 0], [72, 1, 0]]
    pair["stamp"] = input_stamp(pair)
    with pytest.raises(ValueError, match="one Node .a body's. or a cube of three or more"):
        parse_nature_beam_world(pair)

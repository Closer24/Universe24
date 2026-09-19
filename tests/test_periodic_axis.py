"""A periodic axis as a declared run parameter of the world (the model owner,
2026-09-19, the declared exception to the open board): on an axis the world
declares periodic the departures that would leave through one face are
created at the first Node of the opposite face, nothing escapes on that axis
and the momentum they carry stays on the board; the other faces stay open,
"closed" and every other word are refused, and the record carries the
boundary as declared. The expected integers of docs/TEST_EXPECTATIONS.md
("A periodic axis"), written down first. Bars of K 16, N 64, `release`
[0, 1], `suspension` 0, one paid family `light` (quantum 1), one measured
event of it held in place off the units' path, every unit number 1:

(a) a bar of 5 x 1 x 1 with {"z": "periodic"}: a unit in transit at
    (2, 0, 0) on +Z at phase 5 (its momentum (0, 0, 1)) leaves its Node on
    +Z, and the walk creates it at the same Node as its arrival in the +Z
    slot, phase 5 and momentum (0, 0, 1) unchanged, nothing escaped (the
    stub of one interval: with an extent of 1 the Node's two Ports on that
    axis are its own); after each of six intervals the only departure is at
    (2, 0, 0) on +Z, amount 1, phase 5, momentum (0, 0, 1), escaped 0, the
    books balanced and the momentum in flight (0, 0, 1). The edge case: the
    same world with "boundary": "open" escapes the unit at the first walk
    that carries it (after interval 2: escaped 1, the momentum escaped
    (0, 0, 1), nothing in flight, the books balanced);
(b) a bar of 1 x 1 x 4 with {"z": "periodic"}: three units, at z = 3 on +Z
    (phase 5), at z = 0 on -Z (phase 6) and at z = 2 on +X (phase 7); after
    interval 1 each has left its Node by its momentum; after interval 2 the
    first is at z = 0 on +Z with (0, 0, 1) and phase 5, the second at z = 3
    on -Z with (0, 0, -1) and phase 6, and the third escaped through the
    open x face: escaped 1 with momentum (1, 0, 0), 2 in flight, the momentum
    in flight (0, 0, 0), the books balanced;
(c) the refusals and the record: "closed", {"z": "closed"},
    {"w": "periodic"}, {"z": 1} and the bare word "periodic" are refused by
    the parser naming the closed board and by the preflight (valid false,
    code validation); {"z": "periodic"} parses with periodic
    (False, False, True) and boundary {"z": "periodic"}, the preflight's
    summary reads {"x": "open", "y": "open", "z": "periodic"}; a world
    without the key is "open", (False, False, False); a 3-interval run of
    the bar of (a) through execute_event_run writes run.json with boundary
    {"z": "periodic"}, 3 completed ticks, conserved, nothing escaped, and
    state.json with the same boundary.
"""

from __future__ import annotations

import json

import pytest

from event_universe.configuration_validation import validate_configuration
from event_universe.events import EventSimulation, parse_event_world
from event_universe.events.run import execute_event_run

PLUS_X, MINUS_X, PLUS_Y, MINUS_Y, PLUS_Z, MINUS_Z = range(6)


def bar(
    shape: list[int],
    boundary: object,
    in_transit: list[dict[str, object]],
    measured_at: list[int],
    ticks: int = 6,
) -> dict[str, object]:
    return {
        "law": "events",
        "model_id": "periodic-axis-test",
        "shape": shape,
        "boundary": boundary,
        "ticks": ticks,
        "K": 16,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "light", "kind": "paid"}],
        "measured": [{"position": measured_at, "family": "light", "amount": 1, "fixed": True}],
        "in_transit": in_transit,
    }


def unit(position: list[int], heading: list[int], phase: int) -> dict[str, object]:
    return {
        "position": position,
        "family": "light",
        "number": 1,
        "heading": heading,
        "amount": 1,
        "phase": phase,
    }


def departures(simulation: EventSimulation) -> list[tuple[int, int, int, int, int]]:
    transit = simulation.transits[0]
    return sorted(
        (int(x), int(y), int(z), int(port), int(transit.fly_amt[x, y, z, n, port]))
        for x, y, z, n, port in zip(*transit.fly_amt.nonzero(), strict=True)
    )


STUB = bar([5, 1, 1], {"z": "periodic"}, [unit([2, 0, 0], [0, 0, 1], 5)], [0, 0, 0])


def test_a_unit_on_a_periodic_axis_of_extent_one_returns_to_its_node_and_never_escapes():
    """(a)."""
    # The walk alone: after the first interval the unit is a departure on
    # +Z; the next walk creates it at the same Node in the +Z slot.
    probe = EventSimulation(parse_event_world(STUB))
    probe.step()
    transit = probe.transits[0]
    arrived = transit.walk()
    assert transit.arr_amt[2, 0, 0, 0].tolist() == [0, 0, 0, 0, 1, 0]
    assert int(transit.arr_ph[2, 0, 0, 0, PLUS_Z]) == 5
    assert transit.arr_mom[2, 0, 0, 0, PLUS_Z].tolist() == [0, 0, 1]
    assert bool(arrived[2, 0, 0, 0]) and int(transit.fly_amt.sum()) == 0 and transit.escaped == 0
    # Six intervals: it leaves by its momentum and comes back, never escaping.
    simulation = EventSimulation(parse_event_world(STUB))
    transit = simulation.transits[0]
    for tick in range(1, 7):
        simulation.step()
        books = simulation.books()
        assert books["balanced"], tick
        assert departures(simulation) == [(2, 0, 0, PLUS_Z, 1)], tick
        assert int(transit.fly_ph[2, 0, 0, 0, PLUS_Z]) == 5
        assert transit.fly_mom[2, 0, 0, 0, PLUS_Z].tolist() == [0, 0, 1]
        assert transit.escaped == 0 and transit.escaped_momentum.tolist() == [0, 0, 0]
        assert books["momentum"] == {"measured": [0, 0, 0], "transit": [0, 0, 1], "escaped": [0, 0, 0]}
    # The edge case: the open board escapes it at the first walk that carries it.
    simulation = EventSimulation(parse_event_world({**STUB, "boundary": "open"}))
    transit = simulation.transits[0]
    simulation.step()
    assert departures(simulation) == [(2, 0, 0, PLUS_Z, 1)] and transit.escaped == 0
    simulation.step()
    assert departures(simulation) == [] and transit.escaped == 1
    assert transit.escaped_momentum.tolist() == [0, 0, 1]
    books = simulation.books()
    assert books["balanced"] and books["momentum"]["escaped"] == [0, 0, 1]
    assert books["families"]["light"]["transit"]["current"] == 0


def test_the_wrap_joins_the_two_faces_of_the_axis_while_the_other_faces_stay_open():
    """(b)."""
    world = bar(
        [1, 1, 4],
        {"z": "periodic"},
        [
            unit([0, 0, 3], [0, 0, 1], 5),
            unit([0, 0, 0], [0, 0, -1], 6),
            unit([0, 0, 2], [1, 0, 0], 7),
        ],
        [0, 0, 1],
        ticks=2,
    )
    simulation = EventSimulation(parse_event_world(world))
    transit = simulation.transits[0]
    simulation.step()
    assert departures(simulation) == [(0, 0, 0, MINUS_Z, 1), (0, 0, 2, PLUS_X, 1), (0, 0, 3, PLUS_Z, 1)]
    assert transit.escaped == 0
    simulation.step()
    assert departures(simulation) == [(0, 0, 0, PLUS_Z, 1), (0, 0, 3, MINUS_Z, 1)]
    assert int(transit.fly_ph[0, 0, 0, 0, PLUS_Z]) == 5 and int(transit.fly_ph[0, 0, 3, 0, MINUS_Z]) == 6
    assert transit.fly_mom[0, 0, 0, 0, PLUS_Z].tolist() == [0, 0, 1]
    assert transit.fly_mom[0, 0, 3, 0, MINUS_Z].tolist() == [0, 0, -1]
    assert transit.escaped == 1 and transit.escaped_momentum.tolist() == [1, 0, 0]
    books = simulation.books()
    assert books["balanced"]
    assert books["momentum"] == {"measured": [0, 0, 0], "transit": [0, 0, 0], "escaped": [1, 0, 0]}
    line = books["families"]["light"]["transit"]
    assert line["initial"] == 3 and line["current"] == 2 and line["escaped"] == 1


def test_the_refusals_and_the_record_carry_the_boundary_as_declared(tmp_path):
    """(c)."""
    for refused in ("closed", {"z": "closed"}, {"w": "periodic"}, {"z": 1}, "periodic"):
        with pytest.raises(ValueError, match="closed board is refused"):
            parse_event_world({**STUB, "boundary": refused})
        report = validate_configuration(json.dumps({**STUB, "boundary": refused}))
        assert not report.valid and report.issues[0].code == "validation"
        assert "closed board is refused" in report.issues[0].message
    parsed = parse_event_world(STUB)
    assert parsed.periodic == (False, False, True) and parsed.boundary == {"z": "periodic"}
    report = validate_configuration(json.dumps(STUB))
    assert report.valid and report.summary["boundary"] == {"x": "open", "y": "open", "z": "periodic"}
    default = parse_event_world({key: value for key, value in STUB.items() if key != "boundary"})
    assert default.boundary == "open" and default.periodic == (False, False, False)
    output = tmp_path / "run"
    output.mkdir()
    source = json.dumps(STUB).encode("utf-8")
    record = json.loads(execute_event_run(parsed, source, output, "test", 3).read_text(encoding="utf-8"))
    assert record["boundary"] == {"z": "periodic"} and record["status"] == "completed"
    assert record["completed_ticks"] == 3 and record["conserved_at_every_completed_tick"] is True
    assert record["escaped"] == [{"family": "light", "amount": 0, "momentum": [0, 0, 0]}]
    state = json.loads((output / "state.json").read_text(encoding="utf-8"))
    assert state["boundary"] == {"z": "periodic"} and state["tick"] == 3

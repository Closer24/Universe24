"""The integer bounds of a measured event's quantities and of a free family's
emission (the architect's review of 2026-09-19, findings F2, F4 and F9;
ARCHITECTURE.md, the local integer operation contract: "check intermediates
before cancellation, scaling or assignment"; Python's integers do not
overflow, the model's 64-bit register does).

(a) A measured event's momentum, the push taken and its terms, its content
    and what waits to be created again are checked against
    `transit.MOMENTUM_BOUND` (2^62 - 1, the bound of a declared and of a
    carried momentum) before they are assigned (`engine.bounded`), and a
    value beyond it refuses the run with `OverflowError` naming the
    measured event, its Node and the quantity. A bar of 2 x 1 x 1, K 1024,
    N 64, `suspension` 0, every measured event `fixed`, the free family `m`:
    at `release` [1, 1] two measured events of content 64 one Link apart
    release 64 per Port at interval 1, and at interval 2 each reads the
    other's 64 with the flow toward itself and is pushed by
    -M c = -64 x 64 = 4096 toward the other; the event at x = 1 declared
    with the momentum -(2^62 - 1) + 4096 on x lands exactly on the bound,
    -(2^62 - 1), accepted, its push taken (-4096, 0, 0); declared one unit
    nearer the bound, -(2^62 - 1) + 4095, it is refused at interval 2
    naming "momentum", the measured event 2 and [1, 0, 0]. The push itself:
    at `release` [0, 1] a reader of `m` without a phase circle and 64 units
    of another number arriving on +X at its Node; with content 2^56 - 1
    (the largest content whose push -64 x M fits the bound) the push is
    -(2^62 - 64) and accepted; with content 2^56 the push, -2^62, is
    refused at interval 1 naming "push".
(b) The emission bound at parsing (F4): for a free measured event,
    amount x n // d at the world's `release` is what it releases per Port per
    self-creation, and 3 x that must not exceed the mixing's cell bound
    2^30 - 1 (a neighbour's slot holds up to about 2.3 x the release per
    Port; until now the parser accepted any amount up to 2^62 - 1 and the
    run failed at the first crowded mixing, interval 4 to 14). At [1, 128]:
    2^36 releases 2^29 per Port, 3 x 2^29 = 1610612736 > 1073741823,
    refused by the parser and by the preflight naming the Node, the release
    and the bound; 2^33 releases 2^26, 3 x 2^26 = 201326592, accepted; the
    edge at [1, 128]: 357913941 x 128 + 127 releases 357913941 per Port,
    3 x that = 1073741823 = the bound, accepted; one unit more releases
    357913942, refused. A lamp of a paid family of 2^36 at the same release
    is not a free release and is accepted (the two-slit lamp).
(c) The refusals of the mixing (F9) name the quantity and the bound, not the
    retired engine ("disturbance"): the amount in a cell above 2^30 - 1, the
    momentum carried by a departure above the bound, the amount placed on a
    departure above 2^30 - 1, and the coherent sum's component at or above
    2^31 (six arrivals of 2^34 at phase 0: an amplitude of 2^22 x 256 =
    2^30 per Port, the leaving component 3 x 2^30).
"""

from __future__ import annotations

import json

import numpy as np
import pytest

from event_universe.configuration_validation import validate_configuration
from event_universe.core.lattice import MAX_VALUE
from event_universe.events import EventSimulation, parse_event_world
from event_universe.events.mixing import coherent_weights, mix_arrivals, place_departures
from event_universe.events.transit import MOMENTUM_BOUND, Transit
from event_universe.events.world import EMISSION_CELL_BOUND, EMISSION_MARGIN

PLUS_X = 0
BOUND = (1 << 62) - 1


def bar(
    measured: list[dict[str, object]],
    *,
    release: list[int],
    phased: bool = True,
    clock: int = 1024,
    in_transit: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "law": "events",
        "model_id": "integer-bounds-test",
        "shape": [2, 1, 1],
        "boundary": "open",
        "ticks": 2,
        "K": clock,
        "N": 64,
        "release": release,
        "suspension": 0,
        "families": [{"name": "m", "kind": "free", "charge": 0, "phase": phased}],
        "measured": measured,
        "in_transit": in_transit or [],
    }


def fixed(x: int, amount: int, **keys: object) -> dict[str, object]:
    return {"position": [x, 0, 0], "family": "m", "amount": amount, "fixed": True, **keys}


def run(world: dict[str, object], ticks: int) -> EventSimulation:
    simulation = EventSimulation(parse_event_world(world))
    for _ in range(ticks):
        simulation.step()
    return simulation


def test_a_push_past_the_bound_refuses_the_run_naming_the_node_and_the_quantity():
    """(a): the momentum after a push, at the bound and one past it."""
    assert MOMENTUM_BOUND == BOUND
    pair = [fixed(0, 64), fixed(1, 64, momentum=[-(BOUND - 4096), 0, 0])]
    simulation = run(bar(pair, release=[1, 1]), 2)
    reader = simulation.measured[2]
    assert reader.momentum == [-BOUND, 0, 0]
    assert reader.pushed == [-4096, 0, 0]
    assert simulation.measured[1].pushed == [4096, 0, 0]
    assert simulation.books()["balanced"]
    nearer = [fixed(0, 64), fixed(1, 64, momentum=[-(BOUND - 4095), 0, 0])]
    simulation = EventSimulation(parse_event_world(bar(nearer, release=[1, 1])))
    simulation.step()
    with pytest.raises(OverflowError, match=r"the momentum of measured event 2 at \[1, 0, 0\]"):
        simulation.step()


def test_the_push_itself_is_checked_before_the_momentum():
    """(a): -M c with M = 2^56 - 1 fits, M = 2^56 does not."""
    largest = (1 << 56) - 1
    assert 64 * largest <= BOUND < 64 * (largest + 1)
    arrival = [{"position": [1, 0, 0], "family": "m", "number": 1, "heading": [1, 0, 0], "amount": 64}]
    world = bar([fixed(0, 1), fixed(1, largest)], release=[0, 1], phased=False, in_transit=arrival)
    simulation = run(world, 1)
    assert simulation.measured[2].momentum == [-64 * largest, 0, 0]
    assert simulation.measured[2].measured[0]["read"] == 64
    world = bar([fixed(0, 1), fixed(1, largest + 1)], release=[0, 1], phased=False, in_transit=arrival)
    simulation = EventSimulation(parse_event_world(world))
    with pytest.raises(OverflowError, match=r"the push of measured event 2 at \[1, 0, 0\]"):
        simulation.step()


def emitter(amount: int, *, release: list[int], paid: bool = False) -> dict[str, object]:
    """One measured event at the centre of an open 3^3 board, K 2^40 (no
    phase step reaches half the circle at these contents)."""
    family = {"name": "light", "kind": "paid"} if paid else {"name": "m", "kind": "free"}
    entry: dict[str, object] = {"position": [1, 1, 1], "family": family["name"], "amount": amount}
    if paid:
        entry["lamp"] = {"rate": [1, 1]}
    return {
        "law": "events",
        "model_id": "emission-bound-test",
        "shape": [3, 3, 3],
        "ticks": 1,
        "K": 1 << 40,
        "N": 64,
        "release": release,
        "families": [family],
        "measured": [entry],
    }


def test_the_parser_refuses_a_free_emission_the_mixing_could_not_hold():
    """(b): 2^36 at [1, 128] refused, 2^33 accepted, the edge exact."""
    assert EMISSION_CELL_BOUND == MAX_VALUE == (1 << 30) - 1 and EMISSION_MARGIN == 3
    assert (1 << 36) // 128 * 3 == 1610612736 > MAX_VALUE
    assert (1 << 33) // 128 * 3 == 201326592 <= MAX_VALUE
    refusal = (
        r"measured\[0\].amount 68719476736 at \[1, 1, 1\] releases 536870912 units per Port per "
        r"self-creation at release \[1, 128\]; 3 x that, 1610612736, exceeds the mixing's cell "
        r"bound 1073741823"
    )
    with pytest.raises(ValueError, match=refusal):
        parse_event_world(emitter(1 << 36, release=[1, 128]))
    report = validate_configuration(json.dumps(emitter(1 << 36, release=[1, 128])))
    assert not report.valid and "mixing's cell bound 1073741823" in report.issues[0].message
    assert parse_event_world(emitter(1 << 33, release=[1, 128])).measured[0].amount == 1 << 33
    per_port = MAX_VALUE // 3
    assert per_port * 3 == MAX_VALUE
    edge = per_port * 128 + 127
    assert parse_event_world(emitter(edge, release=[1, 128])).measured[0].amount == edge
    with pytest.raises(ValueError, match=rf"releases {per_port + 1} units per Port"):
        parse_event_world(emitter(edge + 1, release=[1, 128]))
    with pytest.raises(ValueError, match=r"releases 536870912 units per Port .* at release \[1, 1\]"):
        parse_event_world(emitter(1 << 29, release=[1, 1]))
    assert parse_event_world(emitter(1 << 36, release=[0, 1])).measured[0].amount == 1 << 36
    lamp = parse_event_world({**emitter(1 << 36, release=[1, 128], paid=True), "K": 1 << 34})
    assert lamp.measured[0].amount == 1 << 36 and lamp.measured[0].lamp is not None


def one_node() -> Transit:
    return Transit(0, (1, 1, 1), (1,), 8, 1 << 20)


def test_the_refusals_of_the_mixing_name_the_quantity_and_not_the_retired_engine():
    """(c): four refusals of the mixing, each naming what exceeded."""
    transit = one_node()
    transit.arr_amt[0, 0, 0, 0, PLUS_X] = MAX_VALUE + 1
    with pytest.raises(
        ValueError, match="the amount in a cell exceeds the integer bound of the mixing"
    ) as cell:
        transit.cycle()
    transit = one_node()
    transit.arr_amt[0, 0, 0, 0, PLUS_X] = 9
    transit.arr_mom[0, 0, 0, 0, PLUS_X] = (100, 0, 0)
    with pytest.raises(
        ValueError,
        match=r"the momentum carried by a departure exceeds the integer bound of the mixing \(10\)",
    ) as carried:
        mix_arrivals(transit, 10)
    whole = np.zeros((1, 1, 1, 1, 6), dtype=np.int64)
    phase = np.zeros((1, 1, 1, 1, 6), dtype=np.int64)
    momenta = np.zeros((1, 1, 1, 1, 6, 3), dtype=np.int64)
    whole[0, 0, 0, 0, PLUS_X] = MAX_VALUE + 1
    with pytest.raises(
        ValueError, match="the amount placed on a departure exceeds the integer bound"
    ) as placed:
        place_departures(one_node(), whole, phase, momenta)
    whole[0, 0, 0, 0, PLUS_X] = 1
    momenta[0, 0, 0, 0, PLUS_X] = (11, 0, 0)
    with pytest.raises(ValueError, match="the momentum carried by a departure exceeds") as departure:
        place_departures(one_node(), whole, phase, momenta, 10)
    amounts = np.full((1, 1, 1, 1, 6), 1 << 34, dtype=np.int64)
    with pytest.raises(
        OverflowError, match="the coherent sum's component at a Node exceeds"
    ) as component:
        coherent_weights(one_node(), amounts, np.zeros_like(amounts))
    for refusal in (cell, carried, placed, departure, component):
        assert "disturbance" not in str(refusal.value)
        assert "bound" in str(refusal.value)

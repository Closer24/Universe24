"""A detector's sensitivity under the law of events (Highlights 5.4, the
model owner, 2026-09-19: "There are detectors by sensitivity"; "every
detector must state what its sensitivity is"): a detector's sensitivity is
its Nodes and its threshold, the smallest bundle of one number it measures
in one interval, and the threshold gates every response of its Nodes, a
receiver's and a re-emitter's alike, whatever the table says; a release
reads no threshold. K 2^20 so that no phase moves, no suspension, no
release of the free family. The expected integers of
docs/TEST_EXPECTATIONS.md ("A detector's sensitivity"), written down first:

(a) a receiver: a detector Node (a measured event of the free family,
    content 4, measuring light) with threshold 3; 2 units of light of
    another number arriving on +X pass: no click, no push, the content 4,
    the 2 units leaving whole on +X and at the neighbour after the next
    interval; 3 units are measured: 3 clicks, the content 4 + 3, the push
    (3, 0, 0) into the momentum, nothing left in transit;
(b) a re-emitter: the same Node re-releasing light with threshold 3; 2
    units pass as in (a); 3 units are taken (re-released 3, no click, the
    push (3, 0, 0) taken, the 3 waiting to be created again when the
    record is written) and created again at the self-creation of the same
    interval on +X with the detector's number 1 and phase 9 (the arrivals'
    phase 20) and momentum (3, 0, 0), the recoil leaving the momentum at
    zero; after the next interval the 3 leave the neighbour as number 1;
(c) an emitter inside a detector: a lamp of light (content 24, rate [1, 1])
    declared in a detector with threshold 5 releases one unit per heading
    per interval as before, its content 18 then 12 and nothing measured;
    and a detector Node reading the free family (content 4) with threshold
    4: 3 units of another number pass with no push and mix on, 4 units
    push by -M c = (-16, 0, 0) and mix on.
"""

from __future__ import annotations

from event_universe.events import EventSimulation, parse_event_world

PLUS_X = 0
M, LIGHT = 0, 1
FAMILIES = [{"name": "m", "kind": "free"}, {"name": "light", "kind": "paid"}]
NODE = [4, 1, 1]
NO_RESPONSE = {"home": 0, "read": 0, "measure": 0, "rerelease": 0}
# The source of the light in transit (its number, releasing nothing).
SOURCE = {"position": [0, 1, 1], "family": "light", "amount": 4, "fixed": True}


def world(
    measured: list[dict[str, object]],
    in_transit: list[dict[str, object]],
    threshold: int,
) -> dict[str, object]:
    return {
        "law": "events",
        "model_id": "detector-sensitivity-test",
        "shape": [9, 3, 3],
        "boundary": "open",
        "ticks": 2,
        "K": 1 << 20,
        "N": 64,
        "release": [0, 1],
        "suspension": 0,
        "families": FAMILIES,
        "measured": measured,
        "in_transit": in_transit,
        "detectors": [{"name": "d", "positions": [NODE], "threshold": threshold}],
    }


def arrival(amount: int, family: str = "light", number: int = 2, phase: int = 0) -> dict[str, object]:
    """A bundle of one number arriving at the detector's Node on +X in interval 1."""
    return {
        "position": NODE,
        "family": family,
        "number": number,
        "heading": [1, 0, 0],
        "amount": amount,
        "phase": phase,
    }


def test_a_receiver_measures_only_a_bundle_at_its_threshold_and_a_smaller_one_passes():
    """(a)."""
    receiver = {
        "position": NODE,
        "family": "m",
        "amount": 4,
        "fixed": True,
        "table": {"light": "measure"},
    }
    simulation = EventSimulation(parse_event_world(world([receiver, SOURCE], [arrival(2)], 3)))
    entry, light = simulation.measured[1], simulation.transits[LIGHT]
    assert entry.detector == 0 and entry.threshold == 3
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.events == [0, 0] and entry.held == [4, 0] and entry.momentum == [0, 0, 0]
    assert entry.measured[LIGHT] == NO_RESPONSE
    assert int(light.fly_amt[4, 1, 1, light.rank[2], PLUS_X]) == 2 and int(light.fly_amt.sum()) == 2
    simulation.step()
    assert simulation.books()["balanced"]
    assert int(light.fly_amt[5, 1, 1, light.rank[2], PLUS_X]) == 2 and int(light.fly_amt.sum()) == 2
    assert entry.events == [0, 0] and entry.measured[LIGHT] == NO_RESPONSE

    simulation = EventSimulation(parse_event_world(world([receiver, SOURCE], [arrival(3)], 3)))
    entry, light = simulation.measured[1], simulation.transits[LIGHT]
    simulation.step()
    assert simulation.books()["balanced"]
    assert entry.events == [0, 3] and entry.held == [4, 3] and entry.momentum == [3, 0, 0]
    assert entry.pushed == [3, 0, 0] and entry.measured[LIGHT] == {**NO_RESPONSE, "measure": 3}
    assert int(light.arr_amt.sum()) == 0 and int(light.fly_amt.sum()) == 0
    assert simulation.detectors()[0]["families"]["light"] == {"measured": 3, "clicks": 3}


def test_a_re_emitter_takes_only_a_bundle_at_its_threshold_and_creates_it_again_as_its_own():
    """(b)."""
    emitter = {
        "position": NODE,
        "family": "m",
        "amount": 4,
        "phase": 9,
        "fixed": True,
        "table": {"light": "rerelease"},
    }
    seen: list[tuple[dict[str, object], list[int]]] = []

    def observer(record: dict[str, object]) -> None:
        # The record of a re-release is written before the self-creation
        # that creates the amount again: the home at that moment.
        if record["event"] == "rerelease":
            seen.append((record, list(simulation.measured[1].home)))

    simulation = EventSimulation(
        parse_event_world(world([emitter, SOURCE], [arrival(2, phase=20)], 3)), observer
    )
    entry, light = simulation.measured[1], simulation.transits[LIGHT]
    assert light.rank == {1: 0, 2: 1}
    simulation.step()
    assert simulation.books()["balanced"] and seen == []
    assert entry.measured[LIGHT] == NO_RESPONSE and entry.home == [0, 0] and entry.momentum == [0, 0, 0]
    assert int(light.fly_amt[4, 1, 1, light.rank[2], PLUS_X]) == 2 and int(light.fly_amt.sum()) == 2

    simulation = EventSimulation(
        parse_event_world(world([emitter, SOURCE], [arrival(3, phase=20)], 3)), observer
    )
    entry, light = simulation.measured[1], simulation.transits[LIGHT]
    simulation.step()
    assert simulation.books()["balanced"]
    assert len(seen) == 1
    record, home = seen[0]
    assert home == [0, 3]
    assert record["tick"] == 1 and record["measured"] == 1 and record["detector"] == "d"
    assert record["number"] == 2 and record["amount"] == 3 and record["push"] == [3, 0, 0]
    assert entry.measured[LIGHT] == {**NO_RESPONSE, "rerelease": 3} and entry.events == [0, 0]
    assert entry.held == [4, 0] and entry.home == [0, 0]
    assert entry.pushed == [3, 0, 0] and entry.momentum == [0, 0, 0]
    assert simulation.transit_absorbed[LIGHT] == 3 and simulation.transit_released[LIGHT] == 3
    own = (4, 1, 1, light.rank[1], PLUS_X)
    assert int(light.fly_amt[own]) == 3 and int(light.fly_ph[own]) == 9
    assert light.fly_mom[own].tolist() == [3, 0, 0] and int(light.fly_amt.sum()) == 3
    simulation.step()
    assert simulation.books()["balanced"]
    assert int(light.arr_amt.sum()) == 0 and int(light.fly_amt.sum()) == 3
    assert int(light.fly_amt[5, 1, 1, light.rank[1]].sum()) == 3
    assert int(light.fly_amt[..., light.rank[2], :].sum()) == 0


def test_a_release_reads_no_threshold_and_a_reading_is_gated_like_a_measurement():
    """(c)."""
    lamp = {"position": NODE, "family": "light", "amount": 24, "fixed": True, "lamp": {"rate": [1, 1]}}
    simulation = EventSimulation(parse_event_world(world([lamp], [], 5)))
    entry, light = simulation.measured[1], simulation.transits[LIGHT]
    assert entry.detector == 0 and entry.threshold == 5
    for tick in (1, 2):
        simulation.step()
        assert simulation.books()["balanced"], tick
        assert light.fly_amt[4, 1, 1, light.rank[1]].tolist() == [1, 1, 1, 1, 1, 1], tick
        assert entry.held == [0, 24 - 6 * tick] and simulation.held_spent[LIGHT] == 6 * tick, tick
        assert simulation.transit_released[LIGHT] == 6 * tick and entry.momentum == [0, 0, 0], tick
    assert simulation.detectors()[0]["families"]["light"] == {"measured": 0, "clicks": 0}

    source = {"position": [0, 1, 1], "family": "m", "amount": 16, "fixed": True}
    reader = {"position": NODE, "family": "m", "amount": 4, "fixed": True, "table": {"m": "read"}}
    for amount, push, read in ((3, [0, 0, 0], 0), (4, [-16, 0, 0], 4)):
        simulation = EventSimulation(
            parse_event_world(world([source, reader], [arrival(amount, family="m", number=1)], 4))
        )
        entry, m = simulation.measured[2], simulation.transits[M]
        simulation.step()
        assert simulation.books()["balanced"], amount
        assert entry.momentum == push and entry.pushed == push, amount
        assert entry.measured[M] == {**NO_RESPONSE, "read": read}, amount
        assert entry.held == [4, 0] and entry.events == [0, 0], amount
        assert int(m.arr_amt.sum()) == 0 and int(m.fly_amt[4, 1, 1, m.rank[1]].sum()) == amount, amount
        assert int(m.fly_amt[..., m.rank[2], :].sum()) == 0, amount
        assert simulation.detectors()[0]["families"]["m"] == {"measured": 0, "clicks": 0}, amount

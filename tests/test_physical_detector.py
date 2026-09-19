"""Isolated runtime rules for reversible-detector-v1, design 418c5ac.

A carrier seeded at x=2 meets that Node in tick 1, x=3 in tick 2, and
output x=4 in tick 3. The output count is 0, 0, 1: coverage is not a
nonlocal trigger. These fixtures are generic rules, not example-world pins.
"""

from copy import deepcopy

import pytest

from event_universe.events import EventSimulation, parse_event_world


def world(*, nodes=3, amount=1, phase=16, threshold=1, capacity=31, output_phase=0, start=None):
    positions = [[x, 1, 1] for x in range(2, 2 + nodes)]
    measured = [
        {
            "position": position,
            "family": "carrier",
            "amount": 4,
            "phase": output_phase if position == positions[-1] else 0,
            "fixed": True,
            "table": {"carrier": "transduce"},
            "port_map": list(range(6)),
        }
        for position in positions
    ]
    return {
        "law": "events",
        "dynamics": "reversible-detector-v1",
        "model_id": "physical-detector-rule-test",
        "shape": [max(nodes + 5, 9), 3, 3],
        "boundary": "open",
        "ticks": nodes,
        "K": 1 << 20,
        "N": 32,
        "release": [0, 1],
        "suspension": 0,
        "max_active_owners": 1,
        "families": [{"name": "carrier", "kind": "paid", "quantum": 3}],
        "measured": measured,
        "in_transit": [
            {
                "position": positions[0] if start is None else start,
                "family": "carrier",
                "number": 1,
                "heading": [1, 0, 0],
                "amount": amount,
                "phase": phase,
            }
        ],
        "detectors": [
            {
                "name": "apparatus",
                "positions": positions,
                "groups": [
                    {
                        "name": "shared",
                        "positions": positions,
                        "output": positions[-1],
                        "threshold": threshold,
                        "capacity": capacity,
                        "reference_phase": 0,
                    }
                ],
            }
        ],
    }


def physical_state(simulation):
    """Actual Events and transit, without observer records or audit counters."""
    material = tuple(
        (
            entry.number,
            entry.position,
            tuple(entry.held),
            entry.phase,
            tuple(entry.momentum),
            entry.age,
            entry.owed,
            tuple(entry.home),
        )
        for entry in simulation.measured.values()
    )
    transit = tuple(
        tuple(
            getattr(entry, name).tobytes()
            for name in ("arr_amt", "arr_ph", "arr_mom", "fly_amt", "fly_ph", "fly_mom", "suspended")
        )
        for entry in simulation.transits
    )
    return simulation.tick, material, transit


def group(simulation):
    return simulation.detector_readouts()[0]["groups"][0]


def test_output_changes_only_after_each_required_local_link_transfer():
    simulation = EventSimulation(parse_event_world(world()))
    assert group(simulation) == {"name": "shared", "value": 0, "triggered": False}
    for tick, value in ((1, 0), (2, 0), (3, 1)):
        simulation.step()
        assert simulation.tick == tick
        assert group(simulation) == {"name": "shared", "value": value, "triggered": bool(value)}
        carrier = simulation.transits[0]
        slot = (tick + 1, 1, 1, carrier.rank[1], 0)
        assert int(carrier.fly_amt[slot]) == 1 and int(carrier.fly_amt.sum()) == 1
        assert int(carrier.fly_ph[slot]) == 16
        assert carrier.fly_mom[slot].tolist() == [3, 0, 0]
        assert int(carrier.arr_amt.sum()) == 0
        assert [entry.held for entry in simulation.measured.values()] == [[4], [4], [4]]


@pytest.mark.parametrize(
    "nodes,threshold,amount,triggered",
    [(1, 1, 1, True), (3, 1, 1, True), (3, 2, 1, False), (3, 2, 2, True)],
)
def test_coverage_and_threshold_are_independent_of_local_amount(nodes, threshold, amount, triggered):
    simulation = EventSimulation(
        parse_event_world(world(nodes=nodes, threshold=threshold, amount=amount))
    )
    for _ in range(nodes):
        simulation.step()
    assert group(simulation) == {"name": "shared", "value": amount, "triggered": triggered}
    assert int(simulation.transits[0].fly_amt.sum()) == amount


def test_input_node_changes_arrival_time_but_preserves_the_common_category():
    results = []
    for start_x, elapsed in ((2, 3), (3, 2), (4, 1)):
        simulation = EventSimulation(parse_event_world(world(start=[start_x, 1, 1])))
        for _ in range(elapsed):
            simulation.step()
        results.append(group(simulation))
    assert results == [{"name": "shared", "value": 1, "triggered": True}] * 3


def test_phase_and_previous_apparatus_information_remain_on_the_board():
    complete_states = []
    for phase, old_pointer, expected in ((0, 5, 6), (16, 5, 6), (16, 6, 7)):
        simulation = EventSimulation(
            parse_event_world(world(nodes=1, phase=phase, output_phase=old_pointer))
        )
        simulation.step()
        assert group(simulation)["value"] == expected
        transit = simulation.transits[0]
        assert int(transit.fly_ph[2, 1, 1, transit.rank[1], 0]) == phase
        complete_states.append(physical_state(simulation))
    assert len(set(complete_states)) == 3


def test_runtime_transfers_exact_recoil_and_retains_incoming_identity():
    document = world(nodes=1, amount=2, phase=16, output_phase=5)
    document["measured"][0]["port_map"] = [2, 1, 0, 3, 4, 5]
    document["measured"][0]["momentum"] = [7, -4, 2]
    simulation = EventSimulation(parse_event_world(document))
    simulation.step()
    entry = simulation.measured[1]
    assert entry.phase == 7 and entry.momentum == [13, -10, 2]
    transit = simulation.transits[0]
    slot = (2, 1, 1, transit.rank[1], 2)
    assert int(transit.fly_amt[slot]) == 2 and int(transit.fly_ph[slot]) == 16
    assert transit.fly_mom[slot].tolist() == [0, 6, 0]
    assert tuple(a + b for a, b in zip(entry.momentum, (0, 6, 0), strict=True)) == (13, -4, 2)


def test_two_distinct_owner_channels_are_counted_without_merging_their_phases():
    document = world(nodes=2, threshold=2, phase=0)
    document["max_active_owners"] = 2
    second = deepcopy(document["in_transit"][0])
    second.update(number=2, phase=16)
    document["in_transit"].append(second)
    simulation = EventSimulation(parse_event_world(document))
    simulation.step()
    simulation.step()
    assert group(simulation) == {"name": "shared", "value": 2, "triggered": True}
    transit = simulation.transits[0]
    for number, phase in ((1, 0), (2, 16)):
        slot = (3, 1, 1, transit.rank[number], 0)
        assert int(transit.fly_amt[slot]) == 1 and int(transit.fly_ph[slot]) == phase


def test_readout_and_mutating_diagnostics_do_not_change_replay():
    records = []

    def corrupt_lists(value):
        if isinstance(value, dict):
            for child in value.values():
                corrupt_lists(child)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                if type(child) is int:
                    value[index] = 999
                else:
                    corrupt_lists(child)

    def observer(record):
        records.append(deepcopy(record))
        corrupt_lists(record)

    document = world()
    silent = EventSimulation(parse_event_world(document))
    observed = EventSimulation(parse_event_world(document), observer)
    replay = EventSimulation(parse_event_world(document))
    for _ in range(3):
        before = physical_state(observed)
        readout = observed.detector_readouts()
        readout[0]["groups"][0]["value"] = 999
        assert physical_state(observed) == before
        for simulation in (silent, observed, replay):
            simulation.step()
        assert physical_state(silent) == physical_state(observed) == physical_state(replay)
    assert any(record.get("kind") == "transduction" for record in records)


def test_full_capacity_refuses_contact_without_partial_state_tick_or_callback_change():
    records = []
    simulation = EventSimulation(parse_event_world(world(output_phase=3, capacity=3)), records.append)
    simulation.step()
    simulation.step()
    before = deepcopy(simulation.snapshot())
    before_physical = physical_state(simulation)
    before_records = deepcopy(records)
    with pytest.raises(ValueError):
        simulation.step()
    assert simulation.snapshot() == before
    assert physical_state(simulation) == before_physical
    assert records == before_records


@pytest.mark.parametrize("has_arrival", [False, True])
def test_full_pointer_accepts_empty_or_explicit_pass_contact(has_arrival):
    document = world(nodes=1, output_phase=3, capacity=3)
    document["measured"][0]["table"]["carrier"] = "pass"
    document["measured"][0].pop("port_map")
    if not has_arrival:
        document["in_transit"] = []
    simulation = EventSimulation(parse_event_world(document))
    simulation.step()
    assert group(simulation)["value"] == 3
    assert simulation.measured[1].age == 1


def test_open_edge_refusal_keeps_the_complete_last_supported_state():
    simulation = EventSimulation(parse_event_world(world(nodes=1, start=[8, 1, 1])))
    simulation.step()
    before = deepcopy(simulation.snapshot())
    with pytest.raises(ValueError):
        simulation.step()
    assert simulation.snapshot() == before


def test_noncanonical_runtime_carrier_is_refused_before_any_partial_step():
    simulation = EventSimulation(parse_event_world(world()))
    transit = simulation.transits[0]
    transit.arr_mom[2, 1, 1, transit.rank[1], 0, 0] = 4
    before = deepcopy(simulation.snapshot())
    with pytest.raises(ValueError):
        simulation.step()
    assert simulation.snapshot() == before

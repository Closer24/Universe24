"""Frozen local timing, inventory and rejection checks for Node output holds."""

from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE
from event_universe.fields.output_clock import output_delays
from event_universe.initialization import parse_initial_state

from .test_energy_audit import document


def clock_document(mass=1, reserve=None, gain=1):
    raw = document(
        headings=[[1, 0, 0]],
        rays_per_tick=1,
        energy=mass if reserve is None else reserve,
        amount={"field": "mass"},
        recoil=False,
    )
    raw["model_id"] = "mass-clock-ray-v1"
    raw["fields"].append(
        {
            "name": "mass",
            "components": 1,
            "units": "candidate mass",
            "signed": False,
            "conserved": True,
            "extensive": True,
        }
    )
    raw["disturbance_types"][0]["fields"].append("mass")
    raw["disturbance_types"][0]["defaults"]["mass"] = mass
    raw["computation_field"] = "energy"
    raw["output_clock"] = {"gain": gain}
    raw["emissions"][0].update(whole_pulse=True, interval=8, first_tick=0)
    raw.pop("conservation", None)
    return raw


@pytest.mark.parametrize(
    ("mass", "gain", "first", "second"),
    [(1, 1, 2, 4), (2, 1, 3, 6), (3, 1, 4, 8), (2, 0, 1, 2), (1, 2, 3, 6)],
)
def test_clock_field_arrivals_have_independent_declared_times(mass, gain, first, second):
    events = []
    world = Simulation(parse_initial_state(clock_document(mass, gain=gain)), observer=events.append)
    initial = world.totals()
    for _ in range(second):
        world.step()
        assert world.totals() == initial
    arrivals = [e["tick"] for e in events if e["event"] == "spatial_received"]
    assert arrivals[:2] == [first, second]
    assert all(e["arrival_tick"] == e["tick"] + 1 for e in events if e["event"] == "spatial_sent")
    assert world._resolver is None


def test_insufficient_full_pulse_reserve_is_retained():
    world = Simulation(parse_initial_state(clock_document(3, reserve=2)))
    before = world.totals()
    for _ in range(10):
        world.step()
    assert world.totals() == before
    assert all(
        not any(node.held_outputs) and not any(node.rays) for node in world._spatial.nodes.values()
    )


def test_occupied_face_rejects_emission_without_partial_source_debit():
    raw = clock_document(2, reserve=4)
    raw["emissions"][0]["interval"] = 1
    world = Simulation(parse_initial_state(raw))
    world.step()
    before = world.inventory_view()
    with pytest.raises(ValueError, match="capacity collision"):
        world.step()
    assert world.inventory_view() == before
    assert world.faulted


def test_transient_sample_does_not_recount_held_stock():
    world = Simulation(parse_initial_state(clock_document(3)))
    world.step()
    node = next(iter(world._spatial.nodes.values()))
    assert node.output_clock.sample == 3 and any(node.held_outputs)
    world.step()
    assert node.output_clock.sample == 0
    assert node.output_clock.ready[0] == 3
    assert any(node.held_outputs)


def test_timed_pulses_continue_while_source_is_stationary():
    events = []
    world = Simulation(parse_initial_state(clock_document(1, reserve=3)), observer=events.append)
    for _ in range(20):
        world.step()
    origin = world.initial.seeds[0].position
    departures = [e["tick"] for e in events if e["event"] == "spatial_sent" and e["position"] == origin]
    assert departures == [1, 9, 17]
    assert next(r for r in world.nodes[origin].records if r is not None).values[0] == (1,)


def test_held_inventory_uses_active_owners_without_scanning_spatial_history():
    world = Simulation(parse_initial_state(clock_document(3)))
    initial = world.totals()
    world.step()
    assert any(any(node.held_outputs) for node in world._spatial.nodes.values())

    class NoHistoryScan(dict):
        def __iter__(self):
            pytest.fail("spatial history was enumerated")

        def values(self):
            pytest.fail("spatial history values were enumerated")

        def items(self):
            pytest.fail("spatial history items were enumerated")

    world._spatial.nodes = NoHistoryScan(world._spatial.nodes)
    for _ in range(9):
        assert world.totals() == initial
        assert world.spatial_accounting()["energy"]["balanced"]
        world.step()


@pytest.mark.parametrize("mutation", ["moving", "self", "link", "unfunded", "shared"])
def test_unsupported_clock_compositions_reject_before_simulation(mutation):
    raw = deepcopy(clock_document())
    if mutation == "moving":
        raw["disturbance_types"][0]["transport"] = {"mode": "move", "weights": [1, 0, 0, 0, 0, 0]}
    elif mutation == "self":
        raw["spatial_fields"][0]["self_exclusion"] = True
    elif mutation == "link":
        raw["link_ticks"] = 2
    elif mutation == "unfunded":
        raw["emissions"][0]["source"] = True
    else:
        raw["spatial_computation_delay"] = True
    with pytest.raises(ValueError):
        parse_initial_state(raw)


def test_clock_operation_preserves_integer_boundaries():
    assert output_delays(3, 2) == (6,) * 6
    assert output_delays(MAX_VALUE, 0) == (0,) * 6
    with pytest.raises(ValueError, match="bound"):
        output_delays(MAX_VALUE, 2)
    with pytest.raises(ValueError):
        output_delays(True, 1)


def pending_source_document():
    raw = clock_document(1, reserve=3)
    partner = deepcopy(raw["disturbance_types"][0])
    partner["name"] = "partner"
    partner["defaults"]["energy"] = 0
    raw["disturbance_types"].append(partner)
    raw["seeds"].append({"type": "partner", "position": raw["seeds"][0]["position"]})
    raw["interactions"] = [
        {
            "name": "retained_pair",
            "left_type": "emitter",
            "right_type": "partner",
            "k": 20,
            "assignments": [
                {"side": "left", "field": "mass", "expression": {"field": "mass", "side": "left"}}
            ],
            "invariants": [{"name": "mass", "expression": {"field": "mass", "side": "left"}}],
        }
    ]
    return raw


def test_material_pending_completion_does_not_restore_independent_source_reserve():
    events = []
    world = Simulation(parse_initial_state(pending_source_document()), observer=events.append)
    origin = world.initial.seeds[0].position
    for tick in range(25):
        world.step()
        if tick == 1:
            assert world.nodes[origin].pending.ready_tick == 20
    source = next(
        record for record in world.nodes[origin].records if record is not None and record.type_index == 0
    )
    assert source.values[0] == (1,)
    prepared = [
        event["tick"]
        for event in events
        if event["event"] == "output_prepared"
        and event["clock"] == "spatial"
        and event["position"] == origin
    ]
    assert prepared == [0, 8, 16]


def test_pending_material_rule_cannot_write_independent_source_reserve():
    raw = pending_source_document()
    raw["interactions"][0]["assignments"] = [{"side": "left", "field": "energy", "expression": 3}]
    with pytest.raises(ValueError, match="source reserve"):
        parse_initial_state(raw)


def probe_pair_document():
    raw = clock_document()
    probe = deepcopy(raw["disturbance_types"][0])
    probe["name"] = "probe"
    probe["defaults"]["energy"] = 0
    probe["transport"] = {"mode": "move", "weights": [0, 0, 1, 0, 0, 0]}
    partner = deepcopy(probe)
    partner["name"] = "partner"
    partner["transport"] = {"mode": "hold"}
    raw["disturbance_types"].extend([probe, partner])
    receiver = list(raw["seeds"][0]["position"])
    receiver[0] += 1
    raw["seeds"].extend(
        [{"type": "probe", "position": receiver}, {"type": "partner", "position": receiver}]
    )
    raw["interactions"] = [
        {
            "name": "prepared_probe",
            "left_type": "probe",
            "right_type": "partner",
            "k": 2,
            "assignments": [
                {"side": "left", "field": "mass", "expression": {"field": "mass", "side": "left"}}
            ],
            "invariants": [{"name": "mass", "expression": {"field": "mass", "side": "left"}}],
        }
    ]
    return raw, tuple(receiver)


def test_material_completion_samples_field_that_arrived_at_its_ready_tick():
    raw, receiver = probe_pair_document()
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    for _ in range(4):
        world.step()
    prepared = [
        event
        for event in events
        if event["event"] == "output_prepared"
        and event["clock"] == "carrier"
        and event["position"] == receiver
    ]
    assert prepared[0]["tick"] == 2
    assert prepared[0]["sample"] == 1
    assert prepared[0]["release_tick"] == 3
    sent = [event for event in events if event["event"] == "sent" and event["position"] == receiver]
    assert sent[0]["tick"] == 3 and sent[0]["arrival_tick"] == 4


def test_zero_wait_carrier_reserves_all_events_before_commit():
    from dataclasses import replace

    from event_universe.core.event_space import CausalEventSpace
    from event_universe.core.node_services import NodeEvents

    raw, receiver = probe_pair_document()
    raw["interactions"] = []
    world = Simulation(parse_initial_state(raw))
    node = world._nodes[receiver]
    space = CausalEventSpace(capacity=3)
    services = replace(world._services, events=NodeEvents(space, None))
    node._begin(0, services, None, None)
    before = replace(node)
    with pytest.raises(OverflowError, match="capacity"):
        node._commit(0, services, None, None)
    assert node == before


def test_new_clock_state_audit_traverses_held_payloads():
    from event_universe.core.disturbance_state import Expression
    from event_universe.core.output_holds import OutputHold
    from event_universe.diagnostics.node_contract import node_state_violations

    world = Simulation(parse_initial_state(clock_document()))
    world.step()
    node = next(iter(world._spatial.nodes.values()))
    assert not node_state_violations(node)
    corrupt = OutputHold(0, 1, Expression("literal", literal=(1,)))
    assert node_state_violations(corrupt) == ("state.packet: forbidden NodeState object Expression",)


def test_profile_rejects_an_unfunded_physical_field_readout():
    raw = clock_document()
    raw["conservation"] = {
        "name": "unsupported field energy",
        "energy_units": "unit",
        "momentum_units": "unit",
        "carriers": [
            {
                "requires": ["energy", "momentum"],
                "energy": {"field": "energy"},
                "momentum": {"field": "momentum"},
            }
        ],
        "spatial": {"energy": {"field": "energy", "side": "right"}, "momentum": [0, 0, 0]},
    }
    with pytest.raises(ValueError, match="physical field E/P"):
        parse_initial_state(raw)

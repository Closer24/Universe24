"""Independent geometry, causal transit and bounded generic carrier contracts."""

from dataclasses import asdict, replace
from itertools import product

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_engine import DisturbanceEngine
from event_universe.core.disturbance_state import (
    CARDINAL_OFFSETS,
    MAX_VALUE,
    CostMeter,
    Expression,
    OperationCosts,
    PortTopology,
    pack,
)
from event_universe.core.event_space import CausalEventSpace
from event_universe.core.spatial_state import (
    SpatialCouplingDefinition,
    SpatialFieldDefinition,
    zero_spatial_state,
)
from event_universe.core.topology import (
    inverse_port,
    neighbor_address,
    site_allowed,
    site_count,
    validate_position,
    validate_topology,
    validate_topology_configuration,
)
from event_universe.fields.disturbances import DisturbanceLaw, evaluate
from event_universe.fields.ratios import evaluate_ratio
from event_universe.fields.record_operations import RecordOperations
from event_universe.fields.routing import balanced_port, direction_weights
from event_universe.fields.spatial_coupling import SpatialCouplingLaw, sample_fluxes, sample_values
from event_universe.initialization import parse_initial_state
from tests.test_disturbance_engine import document, field, kind, resident_values

CORNERS = tuple(product((-1, 1), repeat=3))
BCC = PortTopology(CORNERS, 2, ((0, 0, 0), (1, 1, 1)), "configured-ports-v1")
FCC = PortTopology(
    tuple(v for v in product((-1, 0, 1), repeat=3) if sum(abs(x) for x in v) == 2),
    2,
    ((0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)),
    "configured-ports-v1",
)


def meter():
    return CostMeter(OperationCosts((1,) * 9))


def world_for(
    topology=BCC, *, mode="split", weights=None, position=(4, 4, 4), travel=2, boundary="periodic"
):
    raw = document(
        [kind("parcel", mode=mode, values={"inventory": 16})],
        [(position, "parcel")],
        travel=travel,
        capacity=8,
    )
    initial = parse_initial_state(raw)
    record = replace(
        initial.seeds[0].record,
        route_count_codes=(1,) * topology.degree,
        route_weight_codes=(1,) * topology.degree,
    )
    definition = initial.disturbances[0]
    definition = replace(
        definition,
        transport=replace(definition.transport, weights=weights or (1,) * topology.degree),
    )
    initial = replace(
        initial,
        topology=topology,
        shape=(8, 8, 8),
        boundary=boundary,
        disturbances=(definition,),
        seeds=(replace(initial.seeds[0], record=record),),
    )
    events = []
    law = DisturbanceLaw(
        initial.fields,
        initial.disturbances,
        (),
        initial.operation_costs,
        port_offsets=topology.offsets,
    )
    world = DisturbanceEngine(
        initial,
        law,
        events.append,
        record_policy=RecordOperations(initial.fields, initial.disturbances),
    )
    return world, events


@pytest.mark.parametrize("degree", [2, 4, 6, 8, 12, 18, 26])
def test_supported_bounded_port_sets_have_distinct_reciprocal_neighbors(degree):
    if degree <= 6:
        offsets = CARDINAL_OFFSETS[:degree]
    else:
        offsets = tuple(
            v
            for v in product((-1, 0, 1), repeat=3)
            if (
                sum(abs(x) for x in v) == 3
                if degree == 8
                else sum(abs(x) for x in v) == 2
                if degree == 12
                else 1 <= sum(abs(x) for x in v) <= 2
                if degree == 18
                else any(v)
            )
        )
    topology = PortTopology(offsets=offsets, model_id="configured-ports-v1")
    validate_topology(topology, (8, 8, 8), "periodic")
    neighbors = [
        neighbor_address((4, 4, 4), port, (8, 8, 8), "periodic", topology) for port in range(degree)
    ]
    assert len(set(neighbors)) == degree == topology.degree
    for port, neighbor in enumerate(neighbors):
        assert neighbor_address(
            neighbor, inverse_port(port, topology), (8, 8, 8), "periodic", topology
        ) == (4, 4, 4)


def test_eight_real_packets_arrive_at_corners_after_one_link_interval():
    world, events = world_for()
    world.step()
    snapshot = world.snapshot()
    assert len(snapshot["transfers"]) == 8
    assert {tuple(p["target"]) for p in snapshot["transfers"]} == set(product((3, 5), repeat=3))
    assert all(p["arrival_tick"] == 2 for p in snapshot["transfers"])
    assert all(not resident_values(world, p) for p in product((3, 5), repeat=3))
    assert world.totals() == {"inventory": (16,)}
    world.step()
    assert all(resident_values(world, p) == [{"inventory": (2,)}] for p in product((3, 5), repeat=3))
    arrivals = [e for e in events if e["event"] == "received"]
    assert len(arrivals) == 8 and all(e["tick"] == 2 for e in arrivals)
    assert {tuple(e["position"]) for e in arrivals} == set(product((3, 5), repeat=3))
    assert world.totals() == {"inventory": (16,)}


def test_bcc_uses_one_connected_parity_pair_and_even_periodic_closure():
    validate_topology(BCC, (8, 8, 8), "periodic")
    assert site_allowed((2, 4, 6), BCC)
    assert site_allowed((1, 3, 5), BCC)
    assert not site_allowed((1, 2, 3), BCC)
    assert neighbor_address((0, 0, 0), 0, (8, 8, 8), "periodic", BCC) == (7, 7, 7)
    with pytest.raises(ValueError, match="divisible"):
        validate_topology(BCC, (7, 8, 8), "periodic")
    with pytest.raises(ValueError, match="not a site"):
        validate_position((1, 2, 3), (8, 8, 8), BCC)
    # A finite BFS is a test oracle; production validation never scans the grid.
    reached, pending = {(0, 0, 0)}, [(0, 0, 0)]
    while pending:
        origin = pending.pop()
        for port in range(8):
            target = neighbor_address(origin, port, (4, 4, 4), "periodic", BCC)
            if target not in reached:
                reached.add(target)
                pending.append(target)
    assert len(reached) == 16


def test_port_permutation_controls_inverse_receipt_without_cardinal_index_arithmetic():
    permuted = replace(BCC, offsets=tuple(CORNERS[p] for p in (0, 3, 6, 4, 7, 1, 5, 2)))
    assert inverse_port(0, permuted) == 4
    world, events = world_for(permuted, mode="move", weights=(1, 0, 0, 0, 0, 0, 0, 0))
    world.step()
    world.step()
    arrivals = [e for e in events if e["event"] == "received"]
    assert len(arrivals) == 1
    assert arrivals[0]["position"] == (3, 3, 3)
    assert arrivals[0]["port"] == 4


def test_open_diagonal_escape_owns_inventory_until_full_link_completion():
    world, _ = world_for(
        mode="move", weights=(1, 0, 0, 0, 0, 0, 0, 0), position=(0, 0, 0), boundary="open"
    )
    world.step()
    assert world.totals() == {"inventory": (16,)}
    assert world.escaped_totals() == {"inventory": (0,)}
    assert world.snapshot()["transfers"][0]["target"] is None
    world.step()
    assert world.totals() == {"inventory": (0,)}
    assert world.escaped_totals() == {"inventory": (16,)}


@pytest.mark.parametrize(
    ("topology", "shape", "message"),
    [
        (replace(BCC, offsets=CORNERS + (CORNERS[0],)), (8, 8, 8), "unique"),
        (replace(BCC, offsets=CORNERS[:-1]), (8, 8, 8), "reciprocal"),
        (replace(BCC, offsets=((0, 0, 0),) + CORNERS), (8, 8, 8), "nonzero"),
        (replace(BCC, offsets=((2, 0, 0), (-2, 0, 0))), (8, 8, 8), "components"),
        (replace(BCC, site_residues=((0, 0, 0),)), (8, 8, 8), "not closed"),
        (replace(BCC, site_modulus=3), (8, 8, 8), "fixed bound"),
        (replace(BCC, site_residues=((0, 0, 0), (2, 2, 2))), (8, 8, 8), "below"),
        (replace(BCC, model_id="cardinal-six-v1"), (8, 8, 8), "unchanged"),
        (replace(BCC, model_id="unknown"), (8, 8, 8), "unknown"),
        (BCC, (2, 2, 2), "alias"),
        (PortTopology(model_id="configured-ports-v1"), (1, 8, 8), "self-links"),
    ],
)
def test_invalid_geometry_is_rejected_before_world_state(topology, shape, message):
    with pytest.raises(ValueError, match=message):
        validate_topology(topology, shape, "periodic")


def test_legacy_tiny_domain_and_cardinal_direction_remain_unchanged():
    validate_topology(PortTopology(), (1, 1, 1), "periodic")
    assert all(neighbor_address((0, 0, 0), p, (1, 1, 1), "periodic") == (0, 0, 0) for p in range(6))
    tariff = meter()
    assert direction_weights((2, -1, 0), CARDINAL_OFFSETS, "cardinal", tariff) == (2, 0, 0, 1, 0, 0)
    assert tariff.total == 0
    balanced_port((1, 0, 1, 0, 0, 0), (0,) * 6, (0,) * 6, tariff)
    assert tariff.total == 512


def test_positive_dot_is_an_explicit_affinity_and_preserves_its_bounded_counters():
    tariff = meter()
    scores = direction_weights((1, 1, 1), CORNERS, "positive-dot", tariff)
    assert scores == (0, 0, 0, 1, 0, 1, 1, 3)
    assert tariff.total == 8
    counts, previous, selected = (0,) * 8, (0,) * 8, []
    for _ in range(6):
        port, counts, previous = balanced_port(scores, counts, previous, tariff)
        selected.append(port)
    assert [selected.count(p) for p in range(8)] == list(scores)
    assert tariff.total == 8 + 6 * 683
    with pytest.raises(ValueError, match="default six"):
        direction_weights((1, 1, 1), CORNERS, "cardinal", meter())
    with pytest.raises(ValueError, match="bound"):
        direction_weights((MAX_VALUE, MAX_VALUE, MAX_VALUE), CORNERS, "positive-dot", meter())


def test_packet_bookkeeping_matches_all_26_configured_ports():
    offsets = tuple(v for v in product((-1, 0, 1), repeat=3) if any(v))
    topology = PortTopology(offsets=offsets, model_id="configured-ports-v1")
    world, _ = world_for(topology, weights=(1,) * 26)
    world.step()
    packets = [p for links in world.links.values() for p in links if p is not None]
    assert len(packets) == 16
    assert sum(p.record.values[0][0] != 1 for p in packets) == 16
    assert all(
        len(p.record.route_count_codes) == len(p.record.route_weight_codes) == 26 for p in packets
    )
    assert world.totals() == {"inventory": (16,)}


@pytest.mark.parametrize("degree", [2, 8, 26])
@pytest.mark.parametrize("operation", ["received", "outgoing"])
def test_rational_port_expressions_share_the_generic_supplied_channel_contract(degree, operation):
    channels = tuple((pack((port - 9,)),) for port in range(degree))
    arguments = {"ports" if operation == "received" else "outgoing": channels}
    reference = Expression(operation, field=0, port=degree - 1)
    projection = Expression("rational_whole", arguments=(reference,))
    assert evaluate(projection, (), (), meter(), **arguments) == (degree - 10,)
    assert evaluate(reference, (), (), meter(), **arguments) == (degree - 10,)
    for invalid in (-1, degree, True):
        bad = replace(reference, port=invalid)
        with pytest.raises(ValueError, match="channels"):
            evaluate(bad, (), (), meter(), **arguments)
        with pytest.raises(ValueError, match="channels"):
            evaluate_ratio(bad, (), (), meter(), **arguments)


@pytest.mark.parametrize(
    "boundary", ["outward", "specialized_coupling", "native_program", "direction_policy", "invalid_site"]
)
def test_typed_initial_state_cannot_bypass_topology_capabilities(boundary):
    world, _ = world_for()
    initial = world.initial
    expected = ""
    if boundary == "outward":
        initial = replace(initial, spatial_fields=(SpatialFieldDefinition(0, pack((0,))),))
        expected = "requires local spatial"
    elif boundary == "specialized_coupling":
        coupling = SpatialCouplingDefinition(
            "coupling", 0, 0, "exchange", Expression("literal", literal=(0,))
        )
        initial = replace(initial, spatial_couplings=(coupling,))
        expected = "generic spatial_interactions"
    elif boundary == "native_program":
        initial = replace(initial, event_program='{"model":"causal-events-v1","capacity":100}')
        expected = "native event_program"
    elif boundary == "direction_policy":
        definition = initial.disturbances[0]
        definition = replace(
            definition,
            transport=replace(
                definition.transport, mode="move", direction=Expression("literal", literal=(1, 1, 1))
            ),
        )
        initial = replace(initial, disturbances=(definition,))
        expected = "positive-dot"
    else:
        initial = replace(initial, seeds=(replace(initial.seeds[0], position=(1, 2, 3)),))
        expected = "not a site"
    with pytest.raises(ValueError, match=expected):
        validate_topology_configuration(initial)
    with pytest.raises(ValueError, match=expected):
        DisturbanceEngine(
            initial,
            lambda records, residuals, received: None,
            record_policy=RecordOperations(initial.fields, initial.disturbances),
        )


def test_direct_engine_cannot_attach_a_six_port_causal_backend_to_eight_ports():
    world, _ = world_for()
    initial = world.initial
    with pytest.raises(ValueError, match="causal event_space"):
        DisturbanceEngine(
            initial,
            lambda records, residuals, received: None,
            record_policy=RecordOperations(initial.fields, initial.disturbances),
            event_space=CausalEventSpace(shape=initial.shape),
        )


@pytest.mark.parametrize(
    ("topology", "shape", "boundary", "expected_sites"),
    [
        (BCC, (4, 4, 4), "periodic", 16),
        (FCC, (4, 4, 4), "periodic", 32),
        (BCC, (5, 7, 3), "open", 30),
        (FCC, (5, 7, 3), "open", 53),
        (PortTopology(), (5, 7, 3), "periodic", 105),
        (PortTopology(), (1, 1, 1), "periodic", 1),
    ],
)
def test_immutable_baselines_are_counted_once_per_permitted_site(
    topology, shape, boundary, expected_sites
):
    raw = document(
        [kind("unused", values={"stock": 0, "vector": [0, 0, 0]})],
        [],
        fields=[field("stock"), field("vector", 3)],
    )
    raw["shape"], raw["boundary"] = list(shape), boundary
    if topology.model_id != "cardinal-six-v1":
        raw["topology"] = asdict(topology)
        raw["topology"]["offsets"] = [list(v) for v in topology.offsets]
        raw["topology"]["site_residues"] = [list(v) for v in topology.site_residues]
    raw["spatial_fields"] = [
        {"field": "stock", "transport": "local", "baseline": 2},
        {"field": "vector", "transport": "local", "baseline": [1, -2, 3]},
    ]
    world = Simulation(parse_initial_state(raw))
    assert site_count(shape, topology) == expected_sites
    # Enumeration is an independent small-world test oracle only.
    assert sum(site_allowed(v, topology) for v in product(*(range(n) for n in shape))) == expected_sites
    expected = {
        "stock": (2 * expected_sites,),
        "vector": (expected_sites, -2 * expected_sites, 3 * expected_sites),
    }
    for tick in range(3):
        if tick:
            world.step()
        assert world.totals() == expected
        assert world.snapshot()["spatial_fields"] == []
        for name, ledger in world.spatial_accounting().items():
            assert ledger["initial"] == ledger["current"] == expected[name]
            assert ledger["balanced"]


@pytest.mark.parametrize("degree", [6, 8, 12, 26])
@pytest.mark.parametrize("under_budget", [False, True])
def test_scalar_flux_sampling_reservation_matches_meter_and_local_delay(degree, under_budget):
    topology = (
        PortTopology()
        if degree == 6
        else BCC
        if degree == 8
        else FCC
        if degree == 12
        else PortTopology(
            offsets=tuple(v for v in product((-1, 0, 1), repeat=3) if any(v)),
            model_id="configured-ports-v1",
        )
    )
    # Nonuniform prices make omitted directional reads/updates distinguishable.
    raw = document([kind("parcel", values={"inventory": 1})], [((4, 4, 4), "parcel")], travel=3)
    raw["shape"] = [8, 8, 8]
    raw["operation_costs"].update(read=2, update=3, evaluate=5, route=7, commit=11)
    if degree != 6:
        raw["topology"] = asdict(topology)
        raw["topology"]["offsets"] = [list(v) for v in topology.offsets]
        raw["topology"]["site_residues"] = [list(v) for v in topology.site_residues]
    raw["spatial_fields"] = [{"field": "inventory", "transport": "local", "baseline": 0}]
    raw["spatial_interactions"] = [
        {
            "name": "inactive local response",
            "type": "parcel",
            "when": 0,
            "assignments": [
                {"side": "left", "field": "inventory", "expression": {"field": "inventory"}}
            ],
            "invariants": [{"name": "unchanged", "expression": {"field": "inventory"}}],
        }
    ]
    flux_updates = 3 if degree == 6 else 6 * degree
    # Observable:9 reads/8 updates; flux:D reads/F updates; received:D reads;
    # carrier:1 read/1 route/1 commit; adding the scalar reaction:2 reads/1 update;
    # the inactive response evaluates one literal.
    expected_cost = 2 * (12 + 2 * degree) + 3 * (9 + flux_updates) + 5 + 7 + 11
    raw["normal_budget"] = expected_cost - int(under_budget)
    initial = parse_initial_state(raw)
    states = (zero_spatial_state(1, degree),)
    actual_meter = CostMeter(initial.operation_costs)
    sample = sample_values(
        states, initial.spatial_fields, initial.fields, actual_meter, port_count=degree
    )
    flux = sample_fluxes(
        states, initial.spatial_fields, initial.fields, actual_meter, port_offsets=topology.offsets
    )
    reserved = SpatialCouplingLaw(
        initial.fields,
        (),
        initial.operation_costs,
        initial.spatial_fields,
        port_offsets=topology.offsets,
    )((), sample, flux)
    assert actual_meter.total == reserved.cost == 2 * (9 + degree) + 3 * (8 + flux_updates)
    events = []
    world = Simulation(initial, observer=events.append)
    world.step()
    started = [event for event in events if event["event"] == "cycle_started"]
    assert len(started) == 1
    assert started[0]["cost"] == expected_cost
    assert started[0]["ready_tick"] == 3 * int(under_budget)
    assert started[0]["next_tick"] == 3 * (1 + int(under_budget))
    assert world.totals() == {"inventory": (1,)}

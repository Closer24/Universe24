"""Independent causal, source and inventory contracts for configured spatial fields."""

import json
from itertools import product
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE, OPERATIONS
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

ORIGIN = (15, 15, 15)
PORTS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
ROOT = Path(__file__).resolve().parents[1]


def field(name, components=1, *, conserved=True, extensive=True):
    return {
        "name": name,
        "components": components,
        "units": "configured unit",
        "signed": True,
        "conserved": conserved,
        "extensive": extensive,
    }


def document(*, moving=False, source=False, baseline=0, components=1, travel=1, budget=100000):
    return {
        "schema_version": 1,
        "model_id": "configured-outward-integration-v1",
        "shape": [31, 31, 31],
        "slots_per_node": 4,
        "link_ticks": travel,
        "normal_budget": budget,
        "ticks": 5,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            field("strength"),
            field("heading", 3, conserved=False, extensive=False),
            field("radiation", components),
        ],
        "disturbance_types": [
            {
                "name": "carrier",
                "fields": ["strength", "heading"],
                "defaults": {"strength": 72, "heading": [1, 0, 0]},
                "transport": (
                    {"mode": "move", "direction_field": "heading"} if moving else {"mode": "hold"}
                ),
            }
        ],
        "seeds": [{"position": list(ORIGIN), "type": "carrier"}] if source else [],
        "spatial_fields": [
            {
                "field": "radiation",
                "baseline": baseline,
                "transport": "outward",
                "axis_weights": [1, 1, 1],
                "octant_weights": [1] * 8,
            }
        ],
        "emissions": (
            [
                {
                    "type": "carrier",
                    "field": "radiation",
                    "amount": {"field": "strength"},
                    "denominator": 1,
                    "source": True,
                }
            ]
            if source
            else []
        ),
        "spatial_seeds": [],
    }


def offset(position, displacement):
    return tuple(a + b for a, b in zip(position, displacement, strict=True))


def value(world, position):
    return world.spatial_values(position)["radiation"]["value"]


def residents(world, position):
    node = world.nodes.get(position)
    return [] if node is None else [world.record_values(r) for r in node.records if r is not None]


def test_isolated_pulse_keeps_exact_inventory_on_an_outward_causal_shell():
    raw = document()
    raw["spatial_seeds"] = [{"position": list(ORIGIN), "field": "radiation", "populations": [27] * 8}]
    world = Simulation(parse_initial_state(raw))
    assert value(world, ORIGIN) == (216,)
    for distance in (1, 2, 3):
        world.step()
        observed = {
            displacement: value(world, offset(ORIGIN, displacement))[0]
            for displacement in product(range(-3, 4), repeat=3)
            if value(world, offset(ORIGIN, displacement)) != (0,)
        }
        assert observed
        assert all(sum(abs(component) for component in d) == distance for d in observed)
        assert sum(observed.values()) == 216
        assert world.totals() == {"strength": (0,), "radiation": (216,)}
        assert world.source_totals() == {"strength": (0,), "radiation": (0,)}
        assert value(world, ORIGIN) == (0,)
        if distance == 1:
            assert observed == {port: 36 for port in PORTS}
        elif distance == 2:
            # Six axial nodes and twelve diagonal nodes, each with twelve units.
            assert len(observed) == 18 and set(observed.values()) == {12}
        else:
            assert observed[(3, 0, 0)] == 4
            assert observed[(2, 1, 0)] == observed[(1, 1, 1)] == 6


def test_signed_vector_payload_preserves_travel_direction_on_the_receiving_face():
    raw = document(baseline=[0, 0, 0], components=3)
    raw["spatial_seeds"] = [
        {
            "position": list(ORIGIN),
            "field": "radiation",
            "populations": [[27, -54, 81]] * 8,
        }
    ]
    world = Simulation(parse_initial_state(raw))
    world.step()
    for port, displacement in enumerate(PORTS):
        field_state = world.spatial_values(offset(ORIGIN, displacement))["radiation"]
        assert field_state["value"] == (36, -72, 108)
        expected = [(0, 0, 0)] * 6
        expected[port] = (36, -72, 108)
        assert field_state["directions"] == tuple(expected)
    assert world.totals() == {"strength": (0,), "radiation": (216, -432, 648)}


@pytest.mark.parametrize("moving", [False, True])
@pytest.mark.parametrize("travel", [1, 2])
def test_continuous_source_keeps_carried_strength_and_adds_only_declared_emission(moving, travel):
    world = Simulation(parse_initial_state(document(moving=moving, source=True, travel=travel)))
    assert value(world, ORIGIN) == (0,)
    for interval in range(1, 6):
        for _ in range(travel):
            world.step()
            assert world.totals() == {"strength": (72,), "radiation": (72 * interval,)}
        position = offset(ORIGIN, (interval if moving else 0, 0, 0))
        assert residents(world, position) == [{"strength": (72,), "heading": (1, 0, 0)}]
        assert world.source_totals() == {"strength": (0,), "radiation": (72 * interval,)}
        if not moving:
            assert value(world, ORIGIN) == (0,)


def test_same_speed_source_and_own_field_can_coarrive_without_silent_exclusion():
    world = Simulation(parse_initial_state(document(moving=True, source=True)))
    world.step()
    position = offset(ORIGIN, (1, 0, 0))
    assert residents(world, position) == [{"strength": (72,), "heading": (1, 0, 0)}]
    # Four forward octants deliver three units each at the same time as the carrier.
    # Arrival order alone therefore cannot prove that the local self-field is zero.
    assert value(world, position) == (12,)
    assert world.spatial_values(position)["radiation"]["directions"][0] == (12,)


def test_field_front_keeps_fixed_transit_while_the_source_waits_for_computation():
    raw = document(moving=True, source=True, budget=1)
    raw["operation_costs"]["read"] = 1000
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    for tick in range(1, 4):
        world.step()
        assert residents(world, ORIGIN) == [{"strength": (72,), "heading": (1, 0, 0)}]
        assert world.nodes[ORIGIN].pending is not None
        assert world.totals() == {"strength": (72,), "radiation": (72 * tick,)}
    assert value(world, offset(ORIGIN, (3, 0, 0)))[0] > 0
    origin_cost = next(
        event["cost"]
        for event in events
        if event["event"] == "spatial_cycle" and event["position"] == ORIGIN
    )
    generic_cost = next(event["cost"] for event in events if event["event"] == "cycle_started")
    assert origin_cost > 0 and generic_cost > origin_cost
    sent = [event for event in events if event["event"] == "spatial_sent"]
    assert sent and all(event["arrival_tick"] - event["tick"] == 1 for event in sent)


@pytest.mark.parametrize("baseline", [0, 7])
def test_uniform_baseline_is_implicit_and_neither_emits_nor_decays(baseline):
    raw = document(baseline=baseline)
    raw["shape"] = [5, 7, 9]
    world = Simulation(parse_initial_state(raw))
    before = world.snapshot()
    for _ in range(4):
        world.step()
        state = world.spatial_values((4, 6, 8))["radiation"]
        assert state == {
            "baseline": (baseline,),
            "value": (baseline,),
            "directions": ((0,),) * 6,
            "populations": ((0,),) * 8,
        }
        assert world.totals() == {"strength": (0,), "radiation": (315 * baseline,)}
        assert world.source_totals() == {"strength": (0,), "radiation": (0,)}
    assert world.snapshot()["spatial_fields"] == before["spatial_fields"]
    assert world.snapshot()["spatial_transfers"] == []
    assert not world.nodes


def test_pulse_inventory_is_owned_once_during_multitick_transit():
    raw = document(travel=2)
    raw["spatial_seeds"] = [{"position": list(ORIGIN), "field": "radiation", "populations": [27] * 8}]
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert value(world, ORIGIN) == value(world, offset(ORIGIN, (1, 0, 0))) == (0,)
    assert world.snapshot()["spatial_transfers"]
    assert world.totals()["radiation"] == (216,)
    world.step()
    assert value(world, offset(ORIGIN, (1, 0, 0))) == (36,)
    assert not world.snapshot()["spatial_transfers"]
    for _ in range(4):
        world.step()
        assert world.totals()["radiation"] == (216,)
        assert world.source_totals()["radiation"] == (0,)
    assert value(world, offset(ORIGIN, (3, 0, 0))) == (4,)


@pytest.mark.parametrize("amount", [1, -1])
@pytest.mark.parametrize("moving", [False, True])
def test_fractional_emission_keeps_signed_remainders_without_changing_source_strength(amount, moving):
    raw = document(source=True, moving=moving)
    raw["emissions"][0].update(amount=amount, denominator=3)
    world = Simulation(parse_initial_state(raw))
    for tick in range(1, 7):
        world.step()
        expected = amount * (tick // 3)
        assert world.totals() == {"strength": (72,), "radiation": (expected,)}
        assert world.source_totals()["radiation"] == (expected,)
        position = offset(ORIGIN, (tick if moving else 0, 0, 0))
        assert residents(world, position)[0]["strength"] == (72,)


def test_moving_source_example_records_headless_source_and_spatial_evidence(tmp_path):
    initialization = ROOT / "examples" / "moving_source.json"
    output = run_initialization(initialization, tmp_path)
    metadata = json.loads(output.read_text(encoding="utf-8"))
    state = json.loads((tmp_path / "state.json").read_text(encoding="utf-8"))
    assert metadata["status"] == "completed"
    assert metadata["completed_ticks"] == metadata["tick"] == 5
    assert metadata["display"] == "none"
    assert metadata["initial_totals"] == {"strength": [72], "radiation": [0]}
    assert metadata["source_totals"] == {"strength": [0], "radiation": [360]}
    assert metadata["final_totals"] == {"strength": [72], "radiation": [360]}
    assert metadata["conserved_at_every_completed_tick"]
    assert state["spatial_fields"]
    assert "spatial_transfers" in state
    occupied = [node for node in state["nodes"] if node["disturbances"]]
    assert [node["position"] for node in occupied] == [[20, 15, 15]]
    assert {path.name for path in tmp_path.iterdir()} == {
        "initialization.json",
        "events.jsonl",
        "state.json",
        "run.json",
    }
    assert (tmp_path / "initialization.json").read_bytes() == initialization.read_bytes()
    assert (tmp_path / "events.jsonl").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "case",
    [
        "self_filter",
        "diffusion",
        "nonextensive",
        "axis_count",
        "octant_count",
        "zero_axis_weights",
        "negative_octant_weight",
        "duplicate_spatial_field",
        "duplicate_spatial_seed",
        "duplicate_emission",
        "unknown_emitting_type",
        "implicit_source",
        "unsigned_negative_seed",
        "unsigned_negative_baseline",
    ],
)
def test_invalid_spatial_definitions_fail_before_a_run(case):
    raw = document(source=True)
    definition = raw["spatial_fields"][0]
    if case in ("self_filter", "diffusion"):
        definition[case] = True
    elif case == "nonextensive":
        raw["fields"][-1].update(conserved=False, extensive=False)
    elif case == "axis_count":
        definition["axis_weights"] = [1, 1]
    elif case == "octant_count":
        definition["octant_weights"] = [1] * 6
    elif case == "zero_axis_weights":
        definition["axis_weights"] = [0, 0, 0]
    elif case == "negative_octant_weight":
        definition["octant_weights"][0] = -1
    elif case == "duplicate_spatial_field":
        raw["spatial_fields"].append(dict(definition))
    elif case == "duplicate_spatial_seed":
        seed = {"position": list(ORIGIN), "field": "radiation", "populations": [1] * 8}
        raw["spatial_seeds"] = [seed, dict(seed)]
    elif case == "duplicate_emission":
        raw["emissions"].append(dict(raw["emissions"][0]))
    elif case == "unknown_emitting_type":
        raw["emissions"][0]["type"] = "missing"
    elif case == "implicit_source":
        raw["emissions"][0]["source"] = False
    elif case == "unsigned_negative_seed":
        raw["fields"][-1]["signed"] = False
        raw["spatial_seeds"] = [
            {"position": list(ORIGIN), "field": "radiation", "populations": [-1] * 8}
        ]
    else:
        raw["fields"][-1]["signed"] = False
        definition["baseline"] = -1
    with pytest.raises(ValueError):
        parse_initial_state(raw)


def test_simultaneous_spatial_delivery_overflow_retains_both_packets_without_partial_arrival():
    raw = document()
    raw["spatial_fields"][0]["axis_weights"] = [1, 0, 0]
    raw["spatial_seeds"] = [
        {
            "position": list(offset(ORIGIN, (-1, 0, 0))),
            "field": "radiation",
            "populations": [MAX_VALUE, 0, 0, 0, 0, 0, 0, 0],
        },
        {
            "position": list(offset(ORIGIN, (1, 0, 0))),
            "field": "radiation",
            "populations": [0, 0, 0, 0, MAX_VALUE, 0, 0, 0],
        },
    ]
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    initial_total = world.totals()
    with pytest.raises((ValueError, OverflowError)):
        world.step()
    assert world.faulted
    assert world.tick == 1
    assert value(world, ORIGIN) == (0,)
    assert world.totals() == initial_total == {"strength": (0,), "radiation": (2 * MAX_VALUE,)}
    transfers = world.snapshot()["spatial_transfers"]
    assert len(transfers) == 2
    assert all(packet["target"] == ORIGIN for packet in transfers)
    assert not any(event["event"] == "spatial_received" for event in events)
    with pytest.raises(RuntimeError, match="cannot continue"):
        world.step()


def test_renaming_fields_and_source_type_does_not_change_spatial_physics_or_timing():
    original = document(moving=True, source=True)
    encoded = json.dumps(original)
    mapping = {
        "radiation": "quantity",
        "strength": "amplitude",
        "heading": "direction",
        "carrier": "thing",
    }
    for before, after in mapping.items():
        encoded = encoded.replace(f'"{before}"', f'"{after}"')
    worlds = [
        Simulation(parse_initial_state(original)),
        Simulation(parse_initial_state(json.loads(encoded))),
    ]
    for _ in range(4):
        for world in worlds:
            world.step()
        assert worlds[0].nodes == worlds[1].nodes
        assert worlds[0].links == worlds[1].links
        first = json.dumps(worlds[0].snapshot(), sort_keys=True)
        for before, after in mapping.items():
            first = first.replace(f'"{before}"', f'"{after}"')
        assert json.loads(first) == json.loads(json.dumps(worlds[1].snapshot()))
        assert list(worlds[0].totals().values()) == list(worlds[1].totals().values())
        assert list(worlds[0].source_totals().values()) == list(worlds[1].source_totals().values())


def test_departed_pulse_leaves_no_permanent_computation_load_at_a_visited_node():
    traces = []
    for pulse in (False, True):
        raw = document(source=True)
        raw["emissions"] = []
        if pulse:
            # An indivisible unit also leaves a nonzero allocation phase behind.
            raw["spatial_seeds"] = [
                {"position": list(ORIGIN), "field": "radiation", "populations": [1, 0, 0, 0, 0, 0, 0, 0]}
            ]
        events = []
        world = Simulation(parse_initial_state(raw), observer=events.append)
        for _ in range(3):
            world.step()
        traces.append(
            {
                event["tick"]: event["cost"]
                for event in events
                if event["event"] == "cycle_started" and event["position"] == ORIGIN
            }
        )
    assert traces[1][0] > traces[0][0]
    assert traces[1][1] == traces[0][1]
    assert traces[1][2] == traces[0][2]


def test_delivered_direction_samples_clear_when_the_pulse_leaves():
    raw = document()
    raw["spatial_fields"][0]["axis_weights"] = [1, 0, 0]
    raw["spatial_seeds"] = [
        {"position": list(ORIGIN), "field": "radiation", "populations": [3, 0, 0, 0, 0, 0, 0, 0]}
    ]
    world = Simulation(parse_initial_state(raw))
    neighbor = offset(ORIGIN, (1, 0, 0))
    world.step()
    assert world.spatial_values(neighbor)["radiation"]["directions"] == ((3,), *((0,),) * 5)
    world.step()
    assert value(world, neighbor) == (0,)
    assert world.spatial_values(neighbor)["radiation"]["directions"] == ((0,),) * 6
    assert value(world, offset(ORIGIN, (2, 0, 0))) == (3,)


def test_spatial_receiving_operation_price_contributes_to_the_next_local_cycle():
    costs = []
    for receive_price in (1, 9):
        raw = document()
        raw["operation_costs"]["receive"] = receive_price
        raw["spatial_fields"][0]["axis_weights"] = [1, 0, 0]
        raw["spatial_seeds"] = [
            {"position": list(ORIGIN), "field": "radiation", "populations": [3, 0, 0, 0, 0, 0, 0, 0]}
        ]
        events = []
        world = Simulation(parse_initial_state(raw), observer=events.append)
        world.step()
        world.step()
        assert value(world, offset(ORIGIN, (2, 0, 0))) == (3,)
        costs.append(
            next(
                event["cost"]
                for event in events
                if event["event"] == "spatial_cycle"
                and event["position"] == offset(ORIGIN, (1, 0, 0))
                and event["tick"] == 1
            )
        )
    # Exactly one incoming packet is charged once; propagation still takes one tick.
    assert costs[1] - costs[0] == 8

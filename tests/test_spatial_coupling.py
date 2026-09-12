"""Independent rotation, reaction, sampling and timing contracts for spatial coupling."""

import json
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE, OPERATIONS, unpack
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

ORIGIN = (15, 15, 15)
ROOT = Path(__file__).resolve().parents[1]


def document(*, vector=(5, 0, 0), control=(0, 0, 1), moving=False, denominator=1, polarity=1):
    return {
        "schema_version": 1,
        "model_id": "configured-spatial-coupling-contract-v1",
        "shape": [31, 31, 31],
        "slots_per_cell": 4,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": 3,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "inventory", "components": 3, "units": "unit", "signed": True, "conserved": True},
            {
                "name": "control",
                "components": 3,
                "units": "turn numerator",
                "signed": True,
                "conserved": False,
            },
            {
                "name": "polarity",
                "components": 1,
                "units": "multiplier",
                "signed": True,
                "conserved": False,
                "extensive": False,
            },
        ],
        "disturbance_types": [
            {
                "name": "carrier",
                "fields": ["inventory", "polarity"],
                "defaults": {"inventory": list(vector), "polarity": polarity},
                "transport": (
                    {"mode": "move", "direction_field": "inventory"} if moving else {"mode": "hold"}
                ),
            }
        ],
        "spatial_fields": [
            {
                "field": "inventory",
                "baseline": [0, 0, 0],
                "transport": "outward",
                "axis_weights": [1, 0, 0],
            },
            {
                "field": "control",
                "baseline": list(control),
                "transport": "outward",
                "axis_weights": [1, 0, 0],
            },
        ],
        "spatial_couplings": [
            {
                "name": "configured_turn",
                "type": "carrier",
                "field": "inventory",
                "mode": "rotation",
                "rotation": {
                    "op": "mul",
                    "args": [{"field": "polarity"}, {"field": "control", "side": "right"}],
                },
                "denominator": denominator,
                "axis_order": [0, 1, 2],
            }
        ],
        "seeds": [{"position": list(ORIGIN), "type": "carrier"}],
    }


def resident(world, position=ORIGIN):
    return next(
        world.record_values(record)
        for record in world.cells[position].records
        if record is not None and world.initial.disturbances[record.type_index].name == "carrier"
    )


def field_value(world, position=ORIGIN, name="inventory"):
    return world.spatial_values(position)[name]["value"]


def field_inventory(world):
    snapshot = world.snapshot()
    payloads = [
        payload
        for cell in snapshot["spatial_fields"]
        for payload in cell["fields"]["inventory"]["populations"]
    ]
    payloads.extend(
        payload for packet in snapshot["spatial_transfers"] for payload in packet["fields"]["inventory"]
    )
    return tuple(sum(payload[component] for payload in payloads) for component in range(3))


@pytest.mark.parametrize(
    ("initial", "axis", "expected"),
    [
        ((0, 5, 0), (1, 0, 0), (0, 0, 5)),
        ((0, 5, 0), (-1, 0, 0), (0, 0, -5)),
        ((0, 0, 5), (0, 1, 0), (5, 0, 0)),
        ((0, 0, 5), (0, -1, 0), (-5, 0, 0)),
        ((5, 0, 0), (0, 0, 1), (0, 5, 0)),
        ((5, 0, 0), (0, 0, -1), (0, -5, 0)),
        ((-5, 0, 0), (0, 0, 1), (0, -5, 0)),
    ],
)
def test_exact_signed_quarter_turn_and_opposite_field_reaction(initial, axis, expected):
    world = Simulation(parse_initial_state(document(vector=initial, control=axis)))
    world.step()
    assert resident(world)["inventory"] == expected
    assert sum(component * component for component in expected) == 25
    assert field_inventory(world) == tuple(a - b for a, b in zip(initial, expected, strict=True))
    assert world.totals() == {"inventory": initial}
    assert world.source_totals() == {"inventory": (0, 0, 0)}


@pytest.mark.parametrize(
    ("vector", "control"),
    [((5, 0, 0), (0, 0, 0)), ((0, 0, 5), (0, 0, 1)), ((0, 0, 0), (1, -1, 1))],
)
def test_zero_driver_parallel_vector_and_zero_vector_have_no_rotation_reaction(vector, control):
    world = Simulation(parse_initial_state(document(vector=vector, control=control)))
    world.step()
    assert resident(world)["inventory"] == vector
    assert field_value(world) == (0, 0, 0)
    assert world.totals()["inventory"] == vector


@pytest.mark.parametrize(("polarity", "expected"), [(1, (0, 5, 0)), (-1, (0, -5, 0)), (0, (5, 0, 0))])
def test_declared_polarity_expression_controls_the_turn_sign(polarity, expected):
    world = Simulation(parse_initial_state(document(polarity=polarity)))
    world.step()
    assert resident(world)["inventory"] == expected
    assert world.totals()["inventory"] == (5, 0, 0)


@pytest.mark.parametrize(("order", "expected"), [([0, 1, 2], (0, 0, -5)), ([2, 1, 0], (0, 0, 5))])
def test_multiple_rotation_axes_follow_the_declared_noncommuting_order(order, expected):
    raw = document(control=(1, 1, 1))
    raw["spatial_couplings"][0]["axis_order"] = order
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert resident(world)["inventory"] == expected
    assert world.totals()["inventory"] == (5, 0, 0)


@pytest.mark.parametrize("moving", [False, True])
@pytest.mark.parametrize("polarity", [1, -1])
def test_fractional_rotation_waits_for_a_whole_turn_and_carries_its_remainder(moving, polarity):
    world = Simulation(parse_initial_state(document(moving=moving, denominator=2, polarity=polarity)))
    world.step()
    first = (16, 15, 15) if moving else ORIGIN
    assert resident(world, first)["inventory"] == (5, 0, 0)
    assert field_value(world, first) == (0, 0, 0)
    assert world.totals()["inventory"] == (5, 0, 0)
    world.step()
    second = (16, 15 + polarity, 15) if moving else ORIGIN
    assert resident(world, second)["inventory"] == (0, polarity * 5, 0)
    assert field_inventory(world) == (5, -polarity * 5, 0)
    assert world.totals()["inventory"] == (5, 0, 0)


def test_repeated_exact_turns_do_not_drift_in_length_or_total_vector():
    world = Simulation(parse_initial_state(document()))
    cycle = [(0, 5, 0), (-5, 0, 0), (0, -5, 0), (5, 0, 0)]
    for tick in range(16):
        world.step()
        vector = resident(world)["inventory"]
        assert vector == cycle[tick % 4]
        assert sum(component * component for component in vector) == 25
        assert world.totals()["inventory"] == (5, 0, 0)
        assert world.source_totals()["inventory"] == (0, 0, 0)


def test_rotation_changes_routing_in_the_same_committed_local_cycle():
    world = Simulation(parse_initial_state(document(moving=True)))
    world.step()
    assert resident(world, (15, 16, 15))["inventory"] == (0, 5, 0)
    assert not any(record is not None for record in world.cells[ORIGIN].records)
    assert field_inventory(world) == (5, -5, 0)
    assert world.totals()["inventory"] == (5, 0, 0)


def test_coupling_samples_the_received_field_before_new_local_emission():
    raw = document(moving=True, control=(0, 0, 0), denominator=4)
    raw["spatial_fields"][1]["axis_weights"] = [1, 1, 1]
    raw["emissions"] = [{"type": "carrier", "field": "control", "amount": [0, 0, 24], "source": True}]
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert resident(world, (16, 15, 15))["inventory"] == (5, 0, 0)
    assert field_value(world, (16, 15, 15), "control") == (0, 0, 4)
    assert field_value(world) == (0, 0, 0)


def test_delayed_rotation_keeps_its_original_sample_and_commits_reaction_atomically():
    raw = document()
    raw["shape"] = [1001, 31, 31]
    raw["normal_budget"] = 100
    raw["spatial_fields"][1]["octant_weights"] = [1, 0, 0, 0, 0, 0, 0, 0]
    raw["disturbance_types"].append(
        {
            "name": "beacon",
            "fields": ["polarity"],
            "defaults": {"polarity": 1},
            "transport": {"mode": "hold"},
        }
    )
    raw["seeds"].append({"position": [14, 15, 15], "type": "beacon"})
    raw["emissions"] = [{"type": "beacon", "field": "control", "amount": [0, 0, 1], "source": True}]
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    world.step()
    ready = world.cells[ORIGIN].pending.ready_tick
    assert ready > 2
    assert field_value(world, ORIGIN, "control") == (0, 0, 2)
    while world.tick < ready:
        assert resident(world)["inventory"] == (5, 0, 0)
        assert field_value(world) == (0, 0, 0)
        assert world.totals()["inventory"] == (5, 0, 0)
        world.step()
    # Later arrivals keep the live control at two; the frozen proposal used one.
    assert field_value(world, ORIGIN, "control") == (0, 0, 2)
    assert resident(world)["inventory"] == (0, 5, 0)
    assert field_value(world) == (5, -5, 0)
    assert world.totals()["inventory"] == (5, 0, 0)
    incoming = [
        event for event in events if event["event"] == "spatial_received" and event["position"] == ORIGIN
    ]
    assert {event["tick"] for event in incoming} == set(range(1, ready + 1))


def test_reaction_overflow_cannot_commit_only_the_carrier_rotation():
    raw = document()
    raw["normal_budget"] = 100
    raw["spatial_fields"][0]["baseline"] = [MAX_VALUE, 0, 0]
    world = Simulation(parse_initial_state(raw))
    before = world.totals()
    world.step()
    ready = world.cells[ORIGIN].pending.ready_tick
    with pytest.raises((ValueError, OverflowError)):
        while world.tick < ready:
            world.step()
    assert world.faulted
    assert resident(world)["inventory"] == (5, 0, 0)
    assert field_value(world) == (MAX_VALUE, 0, 0)
    assert world.totals() == before


def test_valid_opposite_vectors_do_not_hide_an_unrepresentable_reaction_delta():
    world = Simulation(parse_initial_state(document(vector=(MAX_VALUE, 0, 0), control=(0, 0, 2))))
    with pytest.raises((ValueError, OverflowError)):
        world.step()
    # Both +MAX and -MAX are valid values, but their difference exceeds one payload.
    assert world.faulted
    assert resident(world)["inventory"] == (MAX_VALUE, 0, 0)
    assert field_inventory(world) == (0, 0, 0)
    assert world.totals()["inventory"] == (MAX_VALUE, 0, 0)


def test_generic_exchange_moves_equal_opposite_components_between_carrier_and_space():
    raw = document()
    raw["spatial_couplings"] = [
        {
            "name": "transfer",
            "type": "carrier",
            "field": "inventory",
            "mode": "exchange",
            "amount": [2, -3, 0],
        }
    ]
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert resident(world)["inventory"] == (3, 3, 0)
    assert field_inventory(world) == (2, -3, 0)
    assert world.totals()["inventory"] == (5, 0, 0)


def test_absent_spatial_coupling_keeps_existing_straight_motion():
    raw = document(moving=True)
    raw.pop("spatial_couplings")
    world = Simulation(parse_initial_state(raw))
    for tick in range(1, 5):
        world.step()
        assert resident(world, (15 + tick, 15, 15))["inventory"] == (5, 0, 0)
        assert world.totals()["inventory"] == (5, 0, 0)
        assert field_value(world) == (0, 0, 0)


def test_field_and_rule_names_have_no_special_coupling_semantics():
    original = document(moving=True)
    encoded = json.dumps(original)
    replacements = {
        "inventory": "a",
        "control": "b",
        "polarity": "c",
        "carrier": "thing",
        "configured_turn": "custom",
    }
    for before, after in replacements.items():
        encoded = encoded.replace(f'"{before}"', f'"{after}"')
    worlds = [
        Simulation(parse_initial_state(original)),
        Simulation(parse_initial_state(json.loads(encoded))),
    ]
    for _ in range(3):
        for world in worlds:
            world.step()
        snapshot = json.dumps(worlds[0].snapshot())
        for before, after in replacements.items():
            snapshot = snapshot.replace(f'"{before}"', f'"{after}"')
        assert json.loads(snapshot) == json.loads(json.dumps(worlds[1].snapshot()))


def flux_document(*, moving=False, denominator=1):
    raw = document(moving=moving, control=(0, 0, 0), denominator=denominator)
    raw["fields"].append(
        {
            "name": "radiation",
            "components": 1,
            "units": "signal unit",
            "signed": False,
            "conserved": True,
        }
    )
    raw["spatial_fields"].append({"field": "radiation", "baseline": 0, "transport": "outward"})
    raw["spatial_couplings"][0]["rotation"] = {"flux": "radiation"}
    return raw


@pytest.mark.parametrize("denominator", [2, 5])
def test_isolated_cardinal_source_parallel_flux_does_not_turn_or_accumulate_fraction(denominator):
    raw = flux_document(moving=True, denominator=denominator)
    raw["emissions"] = [{"type": "carrier", "field": "radiation", "amount": 72, "source": True}]
    world = Simulation(parse_initial_state(raw))
    for tick in range(1, 6):
        world.step()
        position = (15 + tick, 15, 15)
        assert resident(world, position)["inventory"] == (5, 0, 0)
        assert field_inventory(world) == (0, 0, 0)
        assert world.spatial_values(position)["radiation"]["directions"][0][0] > 0
        assert world.totals() == {"inventory": (5, 0, 0), "radiation": (72 * tick,)}
        record = next(record for record in world.cells[position].records if record is not None)
        assert all(not any(unpack(payload)) for payload in record.spatial_remainders)


@pytest.mark.parametrize(("source_y", "octant", "expected"), [(14, 0, (0, 0, -5)), (16, 2, (0, 0, 5))])
def test_external_transverse_scalar_flux_turns_the_carrier_and_preserves_vector_inventory(
    source_y, octant, expected
):
    raw = flux_document()
    raw["spatial_fields"][-1]["axis_weights"] = [0, 1, 0]
    populations = [0] * 8
    populations[octant] = 1
    raw["spatial_seeds"] = [
        {"position": [15, source_y, 15], "field": "radiation", "populations": populations}
    ]
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert resident(world)["inventory"] == (5, 0, 0)
    assert world.spatial_values(ORIGIN)["radiation"]["value"] == (1,)
    world.step()
    assert resident(world)["inventory"] == expected
    assert field_inventory(world) == (5, 0, -expected[2])
    assert world.totals() == {"inventory": (5, 0, 0), "radiation": (1,)}


@pytest.mark.parametrize("travel", [1, 2])
@pytest.mark.parametrize("delayed", [False, True])
def test_reaction_first_neighbor_arrival_is_one_link_interval_after_commit(travel, delayed):
    raw = document(vector=(8, 0, 0))
    raw["link_ticks"] = travel
    if delayed:
        raw["normal_budget"] = 100
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    world.step()
    first_start = next(event for event in events if event["event"] == "cycle_started")
    committed_at = first_start["ready_tick"]
    if delayed:
        assert committed_at >= travel
        while world.tick < committed_at:
            assert resident(world)["inventory"] == (8, 0, 0)
            assert field_inventory(world) == (0, 0, 0)
            world.step()
        assert resident(world)["inventory"] == (0, 8, 0)
        assert field_value(world) == (8, -8, 0)
    arrival = committed_at + travel
    while world.tick < arrival:
        assert field_value(world, (14, 15, 15)) == (0, 0, 0)
        assert field_value(world, (16, 15, 15)) == (0, 0, 0)
        assert world.totals()["inventory"] == (8, 0, 0)
        world.step()
    assert field_value(world, (14, 15, 15)) == (4, -4, 0)
    assert field_value(world, (16, 15, 15)) == (4, -4, 0)
    assert world.totals()["inventory"] == (8, 0, 0)


@pytest.mark.parametrize(
    "case",
    [
        "unknown_mode",
        "missing_expression",
        "scalar_rotation",
        "wrong_axis_count",
        "duplicate_axis",
        "out_of_range_axis",
        "zero_denominator",
        "negative_denominator",
        "unsigned_target",
        "nonspatial_target",
        "unowned_target",
        "nonspatial_right_reference",
        "unknown_type",
        "split_carrier",
        "undeclared_self_filter",
        "vector_flux_reference",
    ],
)
def test_invalid_spatial_coupling_is_rejected_before_simulation(case):
    raw = document()
    rule = raw["spatial_couplings"][0]
    if case == "unknown_mode":
        rule["mode"] = "arbitrary_rotation"
    elif case == "missing_expression":
        rule.pop("rotation")
    elif case == "scalar_rotation":
        rule["rotation"] = 1
    elif case == "wrong_axis_count":
        rule["axis_order"] = [0, 1]
    elif case == "duplicate_axis":
        rule["axis_order"] = [0, 0, 1]
    elif case == "out_of_range_axis":
        rule["axis_order"] = [0, 1, 3]
    elif case == "zero_denominator":
        rule["denominator"] = 0
    elif case == "negative_denominator":
        rule["denominator"] = -1
    elif case == "unsigned_target":
        raw["fields"][0]["signed"] = False
    elif case == "nonspatial_target":
        raw["spatial_fields"].pop(0)
    elif case == "unowned_target":
        rule["field"] = "control"
    elif case == "nonspatial_right_reference":
        rule["rotation"] = {"op": "mul", "args": [[0, 0, 1], {"field": "polarity", "side": "right"}]}
    elif case == "unknown_type":
        rule["type"] = "missing"
    elif case == "split_carrier":
        raw["disturbance_types"][0]["fields"] = ["inventory"]
        raw["disturbance_types"][0]["defaults"].pop("polarity")
        raw["disturbance_types"][0]["transport"] = {"mode": "split", "weights": [1, 0, 0, 0, 0, 0]}
        rule["rotation"] = [0, 0, 1]
    elif case == "vector_flux_reference":
        rule["rotation"] = {"flux": "control"}
    else:
        rule["self_filter"] = True
    with pytest.raises(ValueError):
        parse_initial_state(raw)


def test_spatial_turning_example_is_headless_and_preserves_vector_inventory(tmp_path):
    output = run_initialization(ROOT / "examples" / "spatial_turning.json", tmp_path)
    metadata = json.loads(output.read_text(encoding="utf-8"))
    state = json.loads((tmp_path / "state.json").read_text(encoding="utf-8"))
    assert metadata["status"] == "completed"
    assert metadata["display"] == "none"
    assert metadata["completed_ticks"] == 3
    assert metadata["initial_totals"] == metadata["final_totals"] == {"inventory": [5, 0, 0]}
    assert metadata["source_totals"] == {"inventory": [0, 0, 0]}
    assert metadata["conserved_at_every_completed_tick"]
    occupied = [cell for cell in state["cells"] if cell["disturbances"]]
    assert [cell["position"] for cell in occupied] == [[14, 15, 15]]
    assert occupied[0]["disturbances"][0]["values"]["inventory"] == [0, -5, 0]
    assert {path.name for path in tmp_path.iterdir()} == {
        "initialization.json",
        "events.jsonl",
        "state.json",
        "run.json",
    }

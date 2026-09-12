"""Independent active-input rejection, local exchanges, finite stock and field clocks."""

import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE, Expression, UpdateRule
from event_universe.initialization import parse_initial_json, parse_initial_state
from event_universe.runner import run_initialization


def document(*, delay=False, boundary="periodic", travel=1, vector=False):
    size = 3 if vector else 1
    value = [0, 3, 0] if vector else 8
    return {
        "schema_version": 3,
        "model_id": "elementary-test-v1",
        "shape": [7, 7, 7],
        "slots_per_cell": 2,
        "link_ticks": travel,
        "normal_budget": 100000,
        "ticks": 12,
        "boundary": boundary,
        "operation_costs": {
            key: 1
            for key in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": [
            {"name": "inventory", "components": size, "units": "unit", "signed": True, "conserved": True}
        ],
        "disturbance_types": [
            {
                "name": "carrier",
                "fields": ["inventory"],
                "transport": {"mode": "hold"},
                "defaults": {"inventory": [3, 0, 0] if vector else 5},
            }
        ],
        "seeds": [],
        "spatial_fields": [
            {
                "field": "inventory",
                "routing_weights": [1, 0, 0, 0, 0, 0],
                "computation_delay": delay,
                "decay": {"retain_numerator": 1, "retain_denominator": 2},
            }
        ],
        "spatial_seeds": [
            {
                "position": [2, 2, 2],
                "field": "inventory",
                "populations": [value] + ([[0, 0, 0]] * 7 if vector else [0] * 7),
            }
        ],
    }


def records(world):
    return [
        world.record_values(r)["inventory"]
        for cell in world.cells.values()
        for r in cell.records
        if r is not None
    ]


def balance(world, initial):
    assert tuple(
        a + b + c
        for a, b, c in zip(
            world.totals()["inventory"],
            world.dissipation_totals()["inventory"],
            world.escaped_totals()["inventory"],
            strict=True,
        )
    ) == tuple(a + b for a, b in zip(initial, world.source_totals()["inventory"], strict=True))
    assert world.spatial_accounting()["inventory"]["balanced"]


@pytest.mark.parametrize("travel", [1, 2])
@pytest.mark.parametrize("delay", [False, True])
def test_field_clock_waits_locally_before_a_fixed_full_link(delay, travel):
    raw = document(delay=delay, travel=travel)
    raw["normal_budget"] = 8
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    initial = world.totals()["inventory"]
    world.step()
    cycle = next(e for e in events if e["event"] == "spatial_cycle")
    departure = ((cycle["cost"] + 7) // 8 - 1) * travel if delay else 0
    assert departure > 0 if delay else departure == 0
    for _ in range(departure + travel - world.tick):
        balance(world, initial)
        assert not any(e["event"] == "spatial_received" for e in events)
        world.step()
    sent = next(e for e in events if e["event"] == "spatial_sent")
    received = next(e for e in events if e["event"] == "spatial_received")
    assert sent["tick"] == departure
    assert received["tick"] == sent["tick"] + travel
    assert world.totals()["inventory"] == (4,)
    assert world.dissipation_totals()["inventory"] == (4,)
    balance(world, initial)


def test_two_fields_choose_their_clocks_independently_in_one_cell():
    raw = document(delay=True)
    raw["normal_budget"] = 8
    other = deepcopy(raw["fields"][0])
    other["name"] = "other"
    raw["fields"].append(other)
    other_field = deepcopy(raw["spatial_fields"][0])
    other_field.update(field="other", computation_delay=False)
    raw["spatial_fields"].append(other_field)
    other_seed = deepcopy(raw["spatial_seeds"][0])
    other_seed["field"] = "other"
    raw["spatial_seeds"].append(other_seed)
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert world.spatial_values((3, 2, 2))["other"]["value"] == (4,)
    assert world.spatial_values((3, 2, 2))["inventory"]["value"] == (0,)
    assert world.totals() == {"inventory": (8,), "other": (4,)}
    assert world.snapshot()["spatial_waiting"]


def test_vector_encounter_turns_carrier_and_keeps_joint_sum_and_norm():
    raw = document(vector=True)
    raw["seeds"] = [{"position": [2, 2, 2], "type": "carrier"}]
    raw["exchanges"] = [
        {"name": "contact", "type": "carrier", "field": "inventory", "budget": [3, 3, 0]}
    ]
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert records(world) == [(0, 3, 0)]
    field = world.spatial_values((2, 2, 2))["inventory"]["value"]
    assert field == (3, 0, 0)
    assert world.totals()["inventory"] == (3, 3, 0)
    assert sum(v * v for v in records(world)[0] + field) == 18
    record = next(r for cell in world.cells.values() for r in cell.records if r is not None)
    assert record.interaction_remaining == ((1, 1, 1),)
    for _ in range(8):
        world.step()
    assert records(world) == [(0, 3, 0)]
    assert world.spatial_accounting()["inventory"]["current"] == (0, 0, 0)
    balance(world, (3, 3, 0))


def test_no_field_and_insufficient_allowance_do_not_create_a_response():
    raw = document(vector=True)
    raw["seeds"] = [{"position": [2, 2, 2], "type": "carrier"}]
    raw["exchanges"] = [
        {"name": "contact", "type": "carrier", "field": "inventory", "budget": [1, 1, 1]}
    ]
    for seeds in ([], raw["spatial_seeds"]):
        raw["spatial_seeds"] = seeds
        world = Simulation(parse_initial_state(raw))
        world.step()
        assert records(world) == [(3, 0, 0)]


@pytest.mark.parametrize("port", range(6))
@pytest.mark.parametrize("boundary", ["periodic", "open"])
def test_all_seams_preserve_or_record_signed_stock(port, boundary):
    raw = document(boundary=boundary, travel=2)
    raw["spatial_fields"][0]["routing_weights"] = [int(i == port) for i in range(6)]
    position = [3, 3, 3]
    position[port // 2] = 6 if port % 2 == 0 else 0
    raw["spatial_seeds"][0].update(position=position, populations=[-8] + [0] * 7)
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert world.totals()["inventory"] == (-8,)
    world.step()
    if boundary == "open":
        assert world.escaped_totals()["inventory"] == (-8,)
        assert world.totals()["inventory"] == (0,)
    else:
        position[port // 2] = 0 if port % 2 == 0 else 6
        assert world.spatial_values(tuple(position))["inventory"]["value"] == (-4,)
    balance(world, (-8,))


@pytest.mark.parametrize(
    "key",
    [
        "field_rules",
        "spatial_interactions",
        "spatial_couplings",
        "interactions",
        "couplings",
        "event_program",
        "reference",
    ],
)
def test_json_cannot_enable_supplied_laws_or_choose_the_reference_path(key):
    raw = document()
    raw[key] = []
    with pytest.raises(ValueError, match="unknown keys"):
        parse_initial_state(raw)


@pytest.mark.parametrize("where", ["update", "emission", "rate", "exchange"])
def test_renamed_force_expression_cannot_enter_through_another_write_path(where):
    raw = document()
    formula = {"op": "mul", "args": [{"field": "inventory"}, {"field": "inventory"}]}
    if where == "update":
        raw["disturbance_types"][0]["updates"] = [{"field": "inventory", "expression": formula}]
    elif where == "rate":
        raw["disturbance_types"][0]["transport"]["rate"] = formula
    elif where == "emission":
        raw["emissions"] = [
            {"type": "carrier", "field": "inventory", "amount": formula, "source": True, "budget": 20}
        ]
    else:
        raw["exchanges"] = [
            {
                "name": "anything",
                "type": "carrier",
                "field": "inventory",
                "budget": 20,
                "expression": formula,
            }
        ]
    with pytest.raises(ValueError):
        parse_initial_state(raw)


def test_typed_state_cannot_inject_an_expression_after_loading():
    initial = parse_initial_state(document())
    kind = replace(
        initial.disturbances[0], updates=(UpdateRule(0, Expression("literal", literal=(99,)), True),)
    )
    with pytest.raises(ValueError, match="update"):
        Simulation(replace(initial, disturbances=(kind,)))


def test_ordinary_runner_rejects_old_lorentz_json_before_creating_outputs(tmp_path):
    path = Path(__file__).resolve().parents[1] / "examples/local_lorentz_field.json"
    with pytest.raises(ValueError):
        run_initialization(path, tmp_path / "rejected")
    assert not (tmp_path / "rejected").exists()


def test_duplicate_keys_cannot_replace_the_input_contract():
    with pytest.raises(ValueError, match="duplicate"):
        parse_initial_json('{"schema_version":3,"schema_version":1}')


@pytest.mark.parametrize("axes", [(0, 1), (1, 2), (2, 0)])
@pytest.mark.parametrize("sign", [-1, 1])
def test_moving_encounters_turn_actual_paths_in_signed_coordinate_planes(axes, sign):
    raw = document(vector=True)
    first, second = axes
    p = [0, 0, 0]
    p[first] = 3 * sign
    q = [0, 0, 0]
    q[second] = 3 * sign
    raw["disturbance_types"][0].update(
        defaults={"inventory": p}, transport={"mode": "move", "direction_field": "inventory"}
    )
    raw["spatial_seeds"][0]["populations"][0] = q
    raw["seeds"] = [{"position": [2, 2, 2], "type": "carrier"}]
    raw["exchanges"] = [
        {"name": "encounter", "type": "carrier", "field": "inventory", "budget": [3, 3, 3]}
    ]
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    world.step()
    target = [2, 2, 2]
    target[second] += sign
    assert next(position for position, cell in world.cells.items() if any(cell.records)) == tuple(target)
    assert records(world) == [tuple(q)]
    assert world.spatial_values((2, 2, 2))["inventory"]["value"] == tuple(p)
    assert any(e["event"] == "spatial_coupled" and e["reaction"] for e in events)


def test_finite_emission_continues_to_zero_dynamic_field():
    raw = document()
    raw["spatial_seeds"] = []
    raw["seeds"] = [{"position": [2, 2, 2], "type": "carrier"}]
    raw["emissions"] = [
        {"type": "carrier", "field": "inventory", "amount": 4, "source": True, "budget": 9}
    ]
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    for _ in range(16):
        world.step()
        balance(world, (5,))
    assert world.source_totals()["inventory"] == (9,)
    assert world.dissipation_totals()["inventory"] == (9,)
    assert world.spatial_accounting()["inventory"]["current"] == (0,)
    assert not world.snapshot()["spatial_waiting"]
    assert not world.snapshot()["spatial_transfers"]


@pytest.mark.parametrize("name", ["__proto__", "op", "cross", "force"])
def test_labels_do_not_select_laws_or_change_active_states(name):
    raw = document(vector=True, delay=True)
    raw["normal_budget"] = 25
    original = Simulation(parse_initial_state(raw))
    text = json.dumps(raw).replace('"inventory"', json.dumps(name)).replace('"carrier"', '"constructor"')
    renamed = Simulation(parse_initial_json(text))
    for _ in range(8):
        original.step()
        renamed.step()
        normalized = json.loads(
            json.dumps(renamed.snapshot())
            .replace(json.dumps(name), '"inventory"')
            .replace('"constructor"', '"carrier"')
        )
        assert json.loads(json.dumps(original.snapshot())) == normalized
    assert (
        original.snapshot()["spatial_waiting"]
        or original.snapshot()["spatial_transfers"]
        or original.dissipation_totals()["inventory"] != (0, 0, 0)
    )


def test_waiting_stock_keeps_bounded_formula_free_state_and_incoming_owners():
    from event_universe.diagnostics.cell_contract import cell_state_violations

    raw = document(delay=True)
    raw["normal_budget"] = 8
    raw["spatial_seeds"].append(
        {"position": [1, 2, 2], "field": "inventory", "populations": [4] + [0] * 7}
    )
    world = Simulation(parse_initial_state(raw))
    for _ in range(80):
        world.step()
        balance(world, (12,))
        assert not cell_state_violations(tuple(world._spatial.cells.values()))
    assert world.spatial_accounting()["inventory"]["current"] == (0,)


@pytest.mark.parametrize(
    "field_key,value",
    [
        ("computation_delay", 1),
        ("computation_delay", "true"),
        ("decay", {"retain_numerator": 1, "retain_denominator": 1}),
        ("routing_weights", [0] * 6),
    ],
)
def test_field_policy_rejects_ambiguous_or_infinite_settings(field_key, value):
    raw = document()
    raw["spatial_fields"][0][field_key] = value
    with pytest.raises(ValueError):
        parse_initial_state(raw)


def test_workspace_cannot_validate_or_start_a_supplied_force_json(tmp_path):
    from event_universe.ui import Workspace, validate_source

    root = Path(__file__).resolve().parents[1]
    source = (root / "examples/local_lorentz_field.json").read_text(encoding="utf-8")
    workspace = Workspace(root / "examples", tmp_path / "outputs")
    for action in (lambda: validate_source(source), lambda: workspace.start(source, False, 1)):
        with pytest.raises(ValueError):
            action()
    assert not workspace.jobs
    assert not workspace.output.exists()


def test_three_local_carriers_exchange_selected_components_without_loss():
    raw = document(vector=True)
    raw["slots_per_cell"] = 3
    raw["spatial_seeds"][0]["populations"][0] = [2, 9, -1]
    raw["seeds"] = [
        {"position": [2, 2, 2], "type": "carrier", "values": {"inventory": values}}
        for values in ([5, 1, 0], [7, 2, 3], [-3, 4, 6])
    ]
    raw["exchanges"] = [
        {
            "name": "contact",
            "type": "carrier",
            "field": "inventory",
            "components": [0],
            "budget": [10, 0, 0],
        }
    ]
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert records(world) == [(2, 1, 0), (5, 2, 3), (7, 4, 6)]
    field = world.spatial_values((2, 2, 2))["inventory"]["value"]
    assert field == (-3, 9, -1)
    assert world.totals()["inventory"] == (11, 16, 8)
    assert sum(v * v for row in [*records(world), field] for v in row) == 235


def test_intervening_arrival_rejects_stale_delayed_exchange_atomically():
    raw = document()
    raw["normal_budget"] = 10
    raw["spatial_seeds"][0]["populations"][0] = 2
    raw["spatial_seeds"].append(
        {"position": [1, 2, 2], "field": "inventory", "populations": [2] + [0] * 7}
    )
    raw["seeds"] = [{"position": [2, 2, 2], "type": "carrier"}]
    raw["exchanges"] = [{"name": "contact", "type": "carrier", "field": "inventory", "budget": 10}]
    world = Simulation(parse_initial_state(raw))
    world.step()
    pending = world.cells[(2, 2, 2)].pending
    assert pending is not None and pending.ready_tick > 1
    assert world.spatial_values((2, 2, 2))["inventory"]["value"] == (3,)
    while world.tick < pending.ready_tick - 1:
        world.step()
    with pytest.raises(ValueError, match="invariant"):
        world.step()
    assert world.faulted
    assert records(world) == [(5,)]
    assert world.spatial_values((2, 2, 2))["inventory"]["value"] == (3,)
    assert world.spatial_accounting()["inventory"]["reactions"] == (0,)
    assert next(r for r in world.cells[(2, 2, 2)].records if r is not None).interaction_remaining == ()
    balance(world, (9,))


def test_carried_leaf_emission_spends_a_finite_allowance_including_the_last_unit():
    raw = document()
    raw["spatial_seeds"] = []
    raw["seeds"] = [{"position": [2, 2, 2], "type": "carrier"}]
    raw["emissions"] = [
        {
            "type": "carrier",
            "field": "inventory",
            "amount": {"field": "inventory"},
            "source": True,
            "denominator": 2,
            "budget": 6,
        }
    ]
    world = Simulation(parse_initial_state(raw))
    sources = []
    for _ in range(8):
        world.step()
        sources.append(world.source_totals()["inventory"][0])
        balance(world, (5,))
    assert sources[:4] == [2, 5, 6, 6]
    assert world.dissipation_totals()["inventory"] == (6,)
    assert records(world) == [(5,)]


def test_inline_observer_preserves_elementary_dynamics_and_records_local_arrivals(tmp_path):
    raw = document()
    source = tmp_path / "input.json"
    source.write_text(json.dumps(raw), encoding="utf-8")
    run_initialization(source, tmp_path / "plain", ticks=3)
    raw["observer"] = {"position": [3, 2, 2], "max_receipts": 10}
    source.write_text(json.dumps(raw), encoding="utf-8")
    run_initialization(source, tmp_path / "observed", ticks=3)
    assert (tmp_path / "plain/state.json").read_bytes() == (
        tmp_path / "observed/state.json"
    ).read_bytes()
    observation = json.loads((tmp_path / "observed/observations.json").read_text())
    assert observation["receipts"]
    metadata = json.loads((tmp_path / "observed/run.json").read_text())
    assert metadata["execution_contract"] == "elementary-local-v1"
    assert metadata["emission_cadence"] == "per-field-activation"
    assert metadata["display"] == "none"
    assert not list((tmp_path / "observed").glob("*.html"))


@pytest.mark.parametrize("observer", [{"position": [7, 0, 0]}, {"position": [0, 0, 0], "updates": []}])
def test_observer_cannot_bypass_elementary_validation(observer):
    raw = document()
    raw["observer"] = observer
    with pytest.raises(ValueError, match="observer"):
        parse_initial_state(raw)


def test_extreme_exchange_declines_unaffordable_working_width_request():
    raw = document()
    raw["disturbance_types"][0]["defaults"]["inventory"] = -MAX_VALUE
    raw["spatial_seeds"][0]["populations"][0] = MAX_VALUE
    raw["seeds"] = [{"position": [2, 2, 2], "type": "carrier"}]
    raw["exchanges"] = [
        {"name": "contact", "type": "carrier", "field": "inventory", "budget": MAX_VALUE}
    ]
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert records(world) == [(-MAX_VALUE,)]
    assert world.spatial_accounting()["inventory"]["reactions"] == (0,)
    balance(world, (0,))


@pytest.mark.parametrize(
    "populations",
    [
        (MAX_VALUE, MAX_VALUE, -MAX_VALUE),
        (MAX_VALUE, -MAX_VALUE, MAX_VALUE),
        (-MAX_VALUE, MAX_VALUE, MAX_VALUE),
    ],
)
def test_signed_population_cancellation_is_independent_of_storage_order(populations):
    raw = document()
    raw["spatial_seeds"][0]["populations"] = [*populations, *([0] * 5)]
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert world.totals()["inventory"] == (MAX_VALUE // 2,)
    assert world.dissipation_totals()["inventory"] == (MAX_VALUE - MAX_VALUE // 2,)
    balance(world, (MAX_VALUE,))


@pytest.mark.parametrize(
    "case",
    [
        "too_many_emissions",
        "duplicate_emission",
        "transport_mode",
        "routing",
        "shape",
        "tariffs",
        "duplicate_spatial",
        "duplicate_seed",
        "seed_bookkeeping",
        "fields",
        "components",
        "denominator",
    ],
)
def test_typed_state_obeys_the_same_closed_capacity_and_owner_boundary(case):
    raw = document()
    raw["seeds"] = [{"position": [2, 2, 2], "type": "carrier"}]
    raw["emissions"] = [
        {"type": "carrier", "field": "inventory", "amount": 1, "source": True, "budget": 10}
    ]
    initial = parse_initial_state(raw)
    kind = initial.disturbances[0]
    if case in ("too_many_emissions", "duplicate_emission"):
        initial = replace(
            initial, emissions=initial.emissions * (33 if case == "too_many_emissions" else 2)
        )
    elif case in ("transport_mode", "routing"):
        mode = replace(
            kind.transport,
            **({"mode": "unknown"} if case == "transport_mode" else {"routing": "unknown"}),
        )
        initial = replace(initial, disturbances=(replace(kind, transport=mode),))
    elif case == "shape":
        initial = replace(initial, shape=(7, 7, True))
    elif case == "tariffs":
        initial = replace(initial, operation_costs=replace(initial.operation_costs, prices=(1,)))
    elif case == "duplicate_spatial":
        initial = replace(initial, spatial_fields=initial.spatial_fields * 2)
    elif case == "duplicate_seed":
        initial = replace(initial, spatial_seeds=initial.spatial_seeds * 2)
    elif case == "seed_bookkeeping":
        seed = initial.seeds[0]
        initial = replace(
            initial,
            seeds=(replace(seed, record=replace(seed.record, interaction_remaining=((1,),) * 33)),),
        )
    elif case == "fields":
        initial = replace(initial, fields=initial.fields * 17)
    elif case == "components":
        initial = replace(initial, fields=(replace(initial.fields[0], components=2),))
    else:
        initial = replace(initial, emissions=(replace(initial.emissions[0], denominator=0),))
    with pytest.raises(ValueError):
        Simulation(initial)


def test_typed_spatial_policy_cannot_enable_reference_emission_parameters():
    initial = parse_initial_state(document())
    changed = replace(initial.spatial_fields[0], octant_weights=(1,) * 9)
    with pytest.raises(ValueError, match="reference propagation"):
        Simulation(replace(initial, spatial_fields=(changed,)))


def test_configuration_skill_template_remains_an_active_periodic_world():
    root = Path(__file__).resolve().parents[1]
    source = root / "skills/simulation-configuration/assets/two-streams.json"
    world = Simulation(parse_initial_json(source.read_bytes()))
    for _ in range(18):
        world.step()
        assert world.totals()["inventory"] == (2,)
    assert {p for p, cell in world.cells.items() if any(cell.records)} == {(2, 4, 4), (6, 4, 4)}

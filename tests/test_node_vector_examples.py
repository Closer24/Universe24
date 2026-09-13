"""Independent register-projection checks for generic Node examples."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe.configuration_validation import validate_configuration
from event_universe.core.node_conservation import LocalInventory
from event_universe.core.spatial_state import zero_spatial_state
from event_universe.fields.disturbances import DisturbanceLaw
from event_universe.fields.node_conservation import LocalBalanceGuard
from event_universe.fields.spatial_interactions import JointSpatialCouplingLaw
from event_universe.initialization import parse_initial_state

EXAMPLES = Path(__file__).resolve().parents[1] / "examples/node-vector"


def load(name):
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


def proposed(raw):
    initial = parse_initial_state(raw)
    records = tuple(seed.record for seed in initial.seeds)
    states = [
        zero_spatial_state(initial.fields[field.field].components) for field in initial.spatial_fields
    ]
    for seed in initial.spatial_seeds:
        states[seed.spatial_field] = replace(states[seed.spatial_field], populations=seed.populations)
    guard = LocalBalanceGuard(
        initial.fields, initial.spatial_fields, initial.operation_costs, initial.conservation_contract
    )
    before = LocalInventory(records=records, spatial=tuple(state.populations for state in states))
    if initial.interactions:
        law = DisturbanceLaw(
            initial.fields, initial.disturbances, (), initial.operation_costs, initial.interactions
        )
        result = law(records, (), 0)
        after = LocalInventory(records=tuple(record for _, record in result.replacements))
    else:
        law = JointSpatialCouplingLaw(
            initial.fields,
            (),
            initial.operation_costs,
            initial.spatial_fields,
            initial.spatial_interactions,
        )
        states = tuple(states)
        result = law(records, law.sample(states), law.sample_fluxes(states), law.sample_ports(states))
        deposited, _ = law.deposit(states, (), result.reaction)
        after = LocalInventory(
            records=result.records, spatial=tuple(state.populations for state in deposited)
        )
    guard.check(before, after, "example proposal")
    return initial, before, after, result, guard.measure(before), guard.measure(after)


@pytest.mark.parametrize("name", ["six-records.json", "two-fields.json", "joint-reaction.json"])
def test_node_examples_pass_public_preflight(name):
    report = validate_configuration((EXAMPLES / name).read_bytes(), kind="initialization")
    assert report.valid, report.to_dict()


def test_six_record_permutation_preserves_independent_nonzero_projections_and_costs_three_ticks():
    initial, before, after, result, original, final = proposed(load("six-records.json"))
    # Register projections are declared assumptions: E, P, Q and J in that order.
    assert original == final == ((21,), (3, 0, 0), (0,), (0, 15, 0))
    assert result.interaction_ticks == 3
    assert tuple(record.values for record in after.records) == (
        tuple(record.values for record in before.records[1:]) + (before.records[0].values,)
    )
    assert after.records != before.records
    assert initial.conservation_contract.quantities[0].name == "declared_energy"


def test_two_field_exchange_preserves_joint_projections_and_costs_two_ticks():
    _, before, after, result, original, final = proposed(load("two-fields.json"))
    assert original == final == ((7,), (0, 0, 0), (0,), (0, 0, 0))
    assert result.interaction_ticks == 2
    assert after.records[0].values[0] == before.spatial[1][0]
    assert after.spatial[1][0] == before.records[0].values[0]
    assert after.records != before.records and after.spatial != before.spatial


def test_two_carriers_and_two_fields_share_one_snapshot_and_derived_readouts():
    _, before, after, result, original, final = proposed(load("joint-reaction.json"))
    assert original == final == ((34,), (4, 6, 2))
    assert result.interaction_ticks == 3
    assert len(result.guards) == 1
    assert result.guards[0].slots == (0, 1)
    assert after.records[0].values[0] == before.spatial[0][0]
    assert after.records[1].values[0] == before.records[0].values[0]
    assert after.spatial[0][0] == before.spatial[1][0]
    assert after.spatial[1][0] == before.records[1].values[0]


def rename(value, labels):
    """Rename known declared labels without rewriting schema or operation names."""
    if isinstance(value, str):
        return labels.get(value, value)
    if isinstance(value, list):
        return [rename(item, labels) for item in value]
    if isinstance(value, dict):
        return {labels.get(key, key): rename(item, labels) for key, item in value.items()}
    return value


@pytest.mark.parametrize(
    "name, labels",
    [
        ("six-records.json", {"registers": "__proto__", "parcel": "constructor"}),
        ("two-fields.json", {"first": "field", "second": "participants", "parcel": "__proto__"}),
        (
            "joint-reaction.json",
            {"state": "__proto__", "first": "participants", "second": "constructor", "parcel": "side"},
        ),
    ],
)
def test_active_proposals_do_not_depend_on_physical_or_schema_like_labels(name, labels):
    raw = load(name)
    original = proposed(raw)
    renamed = proposed(rename(raw, labels))
    assert original[1] != original[2]
    assert original[1:] == renamed[1:]
    assert [field.name for field in renamed[0].fields] == [
        labels[field.name] for field in original[0].fields
    ]

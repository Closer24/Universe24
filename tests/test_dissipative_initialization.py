"""Versioned finite decay and allowance inputs are checked before allocation."""

from typing import Any

import pytest

from event_universe.core.disturbance_state import MAX_VALUE, OPERATIONS, unpack
from event_universe.core.spatial_state import DecayDefinition, SpatialCell
from event_universe.reference_api import parse_reference_state as parse_initial_state


def document(*, version: int = 2) -> dict[str, Any]:
    raw: dict[str, Any] = {
        "schema_version": version,
        "model_id": "arbitrary-configured-identity",
        "shape": [9, 9, 9],
        "slots_per_cell": 2,
        "link_ticks": 1,
        "normal_budget": 10000,
        "ticks": 4,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "signal", "components": 1, "units": "unit", "signed": True, "conserved": True},
            {"name": "inventory", "components": 3, "units": "unit", "signed": True, "conserved": True},
        ],
        "disturbance_types": [
            {
                "name": "carrier",
                "fields": ["signal", "inventory"],
                "defaults": {"signal": 5, "inventory": [3, 0, 0]},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [
            {"field": "signal", "baseline": 7, "transport": "outward"},
            {"field": "inventory", "baseline": [7, -5, 3], "transport": "outward"},
        ],
        "emissions": [
            {"type": "carrier", "field": "signal", "amount": -1, "source": True},
            {
                "type": "carrier",
                "field": "inventory",
                "amount": [1, -1, 0],
                "source": True,
            },
        ],
        "spatial_couplings": [
            {
                "name": "scalar_exchange",
                "type": "carrier",
                "field": "signal",
                "mode": "exchange",
                "amount": -1,
            },
            {
                "name": "vector_turn",
                "type": "carrier",
                "field": "inventory",
                "mode": "rotation",
                "rotation": [0, 0, 1],
            },
        ],
        "seeds": [{"position": [4, 4, 4], "type": "carrier"}],
    }
    if version == 2:
        for entry in raw["spatial_fields"]:
            entry["decay"] = {"retain_numerator": 2, "retain_denominator": 3}
        for group in ("emissions", "spatial_couplings"):
            raw[group][0]["budget"] = 6
            raw[group][1]["budget"] = [9, 8, 0]
    return raw


def test_v2_parses_finite_laws_without_interpreting_model_identity() -> None:
    initial = parse_initial_state(document())
    assert initial.schema_version == 2
    assert initial.model_id == "arbitrary-configured-identity"
    assert tuple(field.decay for field in initial.spatial_fields) == (DecayDefinition(2, 3),) * 2
    assert tuple(unpack(field.baseline) for field in initial.spatial_fields) == ((7,), (7, -5, 3))
    for rules in (initial.emissions, initial.spatial_couplings):
        assert tuple(unpack(rule.budget) for rule in rules if rule.budget is not None) == (
            (6,),
            (9, 8, 0),
        )
    record = initial.seeds[0].record
    assert record.emission_remaining == record.spatial_remaining == ()
    assert SpatialCell(()).received_decay_cost == 0


def test_v1_retains_unbounded_source_and_conservative_field_defaults() -> None:
    initial = parse_initial_state(document(version=1))
    assert initial.schema_version == 1
    assert all(field.decay is None for field in initial.spatial_fields)
    assert all(rule.budget is None for rule in initial.emissions)
    assert all(rule.budget is None for rule in initial.spatial_couplings)
    assert initial.seeds[0].record.emission_remaining == ()
    assert initial.seeds[0].record.spatial_remaining == ()


def test_v2_without_any_spatial_laws_is_valid() -> None:
    raw = document()
    for key in ("spatial_fields", "emissions", "spatial_couplings"):
        del raw[key]
    initial = parse_initial_state(raw)
    assert initial.schema_version == 2
    assert initial.spatial_fields == initial.emissions == initial.spatial_couplings == ()


@pytest.mark.parametrize(
    ("group", "key"),
    [("spatial_fields", "decay"), ("emissions", "budget"), ("spatial_couplings", "budget")],
)
@pytest.mark.parametrize("index", [0, 1])
def test_v2_requires_each_entry_to_declare_its_finite_law(group: str, key: str, index: int) -> None:
    raw = document()
    del raw[group][index][key]
    with pytest.raises(ValueError, match=f"missing keys: {key}"):
        parse_initial_state(raw)


@pytest.mark.parametrize(
    ("group", "key", "value"),
    [
        ("spatial_fields", "decay", {"retain_numerator": 0, "retain_denominator": 1}),
        ("emissions", "budget", 0),
        ("spatial_couplings", "budget", 0),
    ],
)
def test_v1_rejects_v2_only_keys(group: str, key: str, value: object) -> None:
    raw = document(version=1)
    raw[group][0][key] = value
    with pytest.raises(ValueError, match="unknown keys"):
        parse_initial_state(raw)


@pytest.mark.parametrize(("numerator", "denominator"), [(0, 1), (MAX_VALUE - 1, MAX_VALUE)])
def test_decay_accepts_complete_loss_and_largest_bounded_ratio(numerator: int, denominator: int) -> None:
    raw = document()
    raw["spatial_fields"][0]["decay"] = {
        "retain_numerator": numerator,
        "retain_denominator": denominator,
    }
    assert parse_initial_state(raw).spatial_fields[0].decay == DecayDefinition(numerator, denominator)


@pytest.mark.parametrize(
    "decay",
    [
        None,
        {},
        {"retain_numerator": 0},
        {"retain_denominator": 1},
        {"retain_numerator": -1, "retain_denominator": 2},
        {"retain_numerator": 0, "retain_denominator": 0},
        {"retain_numerator": 1, "retain_denominator": 1},
        {"retain_numerator": 3, "retain_denominator": 2},
        {"retain_numerator": MAX_VALUE + 1, "retain_denominator": MAX_VALUE},
        {"retain_numerator": 0, "retain_denominator": MAX_VALUE + 1},
        {"retain_numerator": False, "retain_denominator": 1},
        {"retain_numerator": 0, "retain_denominator": True},
        {"retain_numerator": 0.5, "retain_denominator": 1},
        {"retain_numerator": 0, "retain_denominator": 1, "background": True},
    ],
)
def test_decay_rejects_missing_noninteger_unbounded_or_nondissipative_ratios(decay: object) -> None:
    raw = document()
    raw["spatial_fields"][0]["decay"] = decay
    with pytest.raises(ValueError, match="decay"):
        parse_initial_state(raw)


@pytest.mark.parametrize("group", ["emissions", "spatial_couplings"])
@pytest.mark.parametrize("amount", [0, MAX_VALUE])
def test_allowance_accepts_zero_and_component_bound(group: str, amount: int) -> None:
    raw = document()
    raw[group][0]["budget"] = amount
    raw[group][1]["budget"] = [amount, 0, amount]
    initial = parse_initial_state(raw)
    rules = initial.emissions if group == "emissions" else initial.spatial_couplings
    assert rules[0].budget is not None and unpack(rules[0].budget) == (amount,)
    assert rules[1].budget is not None and unpack(rules[1].budget) == (amount, 0, amount)


@pytest.mark.parametrize("group", ["emissions", "spatial_couplings"])
@pytest.mark.parametrize("budget", [-1, MAX_VALUE + 1, True, 0.5, None, [1], [1, 2, 3]])
def test_scalar_allowance_rejects_negative_unbounded_or_wrong_shape(group: str, budget: object) -> None:
    raw = document()
    raw[group][0]["budget"] = budget
    with pytest.raises(ValueError, match="budget"):
        parse_initial_state(raw)


@pytest.mark.parametrize("group", ["emissions", "spatial_couplings"])
@pytest.mark.parametrize(
    "budget",
    [0, [], [1, 2], [1, 2, 3, 4], [1, -1, 1], [1, MAX_VALUE + 1, 1], [1, True, 1], [1, 0.5, 1], None],
)
def test_vector_allowance_requires_three_bounded_nonnegative_integers(
    group: str, budget: object
) -> None:
    raw = document()
    raw[group][1]["budget"] = budget
    with pytest.raises(ValueError, match="budget"):
        parse_initial_state(raw)

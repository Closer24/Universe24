"""Exact calibration and independent dimensional counterexamples at preparation."""

import json
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE, Expression
from event_universe.initialization import parse_initial_state
from event_universe.units import convert_value, encode_field_value, parse_unit_system, validate_units

from .test_disturbance_engine import document, field, kind, resident_values
from .test_local_field_rules import operation as op
from .test_native_event_runtime import configuration as native_configuration

DIMENSIONS = {
    "mass": [0, 1, 0, 0, 0, 0, 0],
    "duration": [0, 0, 1, 0, 0, 0, 0],
    "p": [1, 1, -1, 0, 0, 0, 0],
    "energy": [2, 1, -2, 0, 0, 0, 0],
    "force": [1, 1, -2, 0, 0, 0, 0],
    "count": [0] * 7,
}


def registry(dimensions=DIMENSIONS):
    return {
        "model_id": "si-rational-v1",
        "base_scales": [[1, 1] for _ in range(7)],
        "units": [
            {"name": name, "dimensions": list(dim), "si_scale": [1, 1]}
            for name, dim in dimensions.items()
        ],
    }


def ref(name, side="left"):
    return {"field": name, "side": side}


def example():
    values = {"mass": 2, "duration": 2, "p": [6, 8, 0], "energy": 25, "force": [2, 0, 0], "count": 1}
    fields = []
    for name, value in values.items():
        item = field(name, 3 if isinstance(value, list) else 1, conserved=False)
        item["units"] = name
        fields.append(item)
    raw = document([kind("body", values=values)], [((2, 2, 2), "body")], fields=fields)
    raw["unit_system"] = registry()
    raw["spatial_fields"] = [
        {"field": name, "baseline": [0, 0, 0] if isinstance(value, list) else 0, "transport": "local"}
        for name, value in values.items()
    ]
    return raw


@pytest.mark.parametrize("calibrated", [False, True])
def test_force_impulse_and_energy_have_nonzero_independent_results_and_unchanged_trace(calibrated):
    raw = example()
    if calibrated:
        raw["unit_system"]["base_scales"][:3] = [[1, 1000] for _ in range(3)]
        for unit in raw["unit_system"]["units"]:
            unit["si_scale"] = [1, 1] if unit["name"] in ("force", "count") else [1, 1000]
    raw["disturbance_types"][0]["updates"] = [
        {"field": "p", "expression": op("add", ref("p"), op("mul", ref("force"), ref("duration")))},
        {
            "field": "energy",
            "expression": op("exact_div", op("dot", ref("p"), ref("p")), op("mul", 2, ref("mass"))),
        },
    ]
    legacy = deepcopy(raw)
    legacy.pop("unit_system")
    events = [[], []]
    worlds = [
        Simulation(parse_initial_state(v), observer=e.append)
        for v, e in zip((raw, legacy), events, strict=True)
    ]
    for px, energy in ((10, 41), (14, 65), (18, 97)):
        for world in worlds:
            world.step()
            value = resident_values(world, (2, 2, 2))[0]
            assert value["p"] == (px, 8, 0)
            assert value["energy"] == (energy,)
            if calibrated:
                # Independent SI diagnostic for millimetre, gram, millisecond base units.
                p_si = [Fraction(component, 1000) for component in value["p"]]
                mass_si = Fraction(value["mass"][0], 1000)
                assert sum(component**2 for component in p_si) / (2 * mass_si) == Fraction(energy, 1000)
        assert worlds[0].snapshot() == worlds[1].snapshot()
    assert events[0] == events[1]


@pytest.mark.parametrize(
    "context",
    [
        "update",
        "pair",
        "coupling",
        "field",
        "joint",
        "emission",
        "spatial",
        "rotation",
        "check",
        "condition",
        "rate",
        "invariant",
    ],
)
def test_each_law_context_rejects_dimensionally_wrong_formula(context):
    raw = example()
    assignment = {"field": "mass", "expression": ref("duration")}
    guard = {"name": "mass", "expression": ref("mass")}
    if context == "update":
        raw["disturbance_types"][0]["updates"] = [assignment]
    elif context in ("pair", "invariant"):
        raw["interactions"] = [
            {
                "name": "pair",
                "left_type": "body",
                "right_type": "body",
                "assignments": [{**assignment, "side": "left"}],
                "invariants": [guard],
            }
        ]
        if context == "invariant":
            raw["interactions"][0]["assignments"][0]["expression"] = ref("mass")
            guard["expression"] = op("add", ref("mass"), ref("duration"))
    elif context == "coupling":
        raw["couplings"] = [
            {
                "name": "pair",
                "left_type": "body",
                "right_type": "body",
                "field": "mass",
                "amount": ref("duration"),
            }
        ]
    elif context in ("field", "condition"):
        assignment["expression"] = ref("duration", "right") if context == "field" else 0
        guard["expression"] = ref("mass", "right")
        rule = {"name": "local", "assignments": [{**assignment, "port": 5}], "invariants": [guard]}
        if context == "condition":
            rule["when"] = ref("mass", "right")
        raw["field_rules"] = [rule]
    elif context == "joint":
        raw["spatial_interactions"] = [
            {
                "name": "joint",
                "type": "body",
                "assignments": [{**assignment, "side": "left"}],
                "invariants": [guard],
            }
        ]
    elif context == "emission":
        raw["emissions"] = [{"type": "body", "field": "mass", "amount": ref("duration"), "source": True}]
    elif context == "spatial":
        raw["spatial_couplings"] = [
            {
                "name": "response",
                "type": "body",
                "field": "mass",
                "mode": "exchange",
                "amount": ref("duration"),
            }
        ]
    elif context == "rotation":
        raw["spatial_couplings"] = [
            {"name": "turn", "type": "body", "field": "p", "mode": "rotation", "rotation": ref("force")}
        ]
    elif context == "check":
        raw["disturbance_types"][0]["checks"] = [{"name": "wrong", "expression": ref("mass")}]
    elif context == "rate":
        raw["disturbance_types"][0]["transport"] = {
            "mode": "move",
            "direction_field": "p",
            "rate": ref("mass"),
        }
    with pytest.raises(ValueError, match="dimension"):
        parse_initial_state(raw)


def test_zero_and_dimensionless_coefficients_preserve_typed_vector_operations():
    raw = example()
    raw["disturbance_types"][0]["updates"] = [
        {"field": "p", "expression": op("cross", [0, 0, 1], ref("p"))},
        {"field": "force", "expression": op("exact_div", ref("p"), ref("duration"))},
        {"field": "energy", "expression": 0},
    ]
    world = Simulation(parse_initial_state(raw))
    world.step()
    values = resident_values(world, (2, 2, 2))[0]
    assert values["p"] == (-8, 6, 0)
    assert values["force"] == (-4, 3, 0)
    assert values["energy"] == (0,)
    raw["disturbance_types"][0]["updates"][-1]["expression"] = 1
    with pytest.raises(ValueError, match="dimension"):
        parse_initial_state(raw)


def test_exact_authoring_conversions_and_coherent_different_labels():
    dims = {"metre": [1, 0, 0, 0, 0, 0, 0], "millimetre": [1, 0, 0, 0, 0, 0, 0]}
    raw = registry(dims)
    raw["base_scales"][0] = [1, 1000]
    raw["units"][1]["si_scale"] = [1, 1000]
    system = parse_unit_system(raw)
    assert convert_value(Fraction(3, 2), "metre", "millimetre", system) == 1500
    assert convert_value(7, "millimetre", "metre", system) == Fraction(7, 1000)
    data = document(
        [kind("ruler", values={"a": 0, "b": 0})],
        [((2, 2, 2), "ruler")],
        fields=[{**field("a"), "units": "metre", "scale": 1000}, {**field("b"), "units": "millimetre"}],
    )
    data["unit_system"] = raw
    initial = parse_initial_state(data)
    assert encode_field_value(Fraction(3, 2), "metre", initial.fields[0], system) == 1500
    assert encode_field_value(-7, "millimetre", initial.fields[1], system) == -7
    with pytest.raises(ValueError, match="exact integer"):
        encode_field_value(Fraction(1, 2000), "metre", initial.fields[0], system)
    with pytest.raises(ValueError, match="bound"):
        encode_field_value(MAX_VALUE + 1, "millimetre", initial.fields[0], system)
    data["fields"][0]["scale"] = 1
    with pytest.raises(ValueError, match="coherent quantum"):
        parse_initial_state(data)


@pytest.mark.parametrize("bad", [True, 0, -1, 1.5, 1 << 256])
def test_calibration_rejects_inexact_or_out_of_bound_metadata(bad):
    raw = registry()
    raw["base_scales"][0][0] = bad
    with pytest.raises(ValueError, match="positive integers"):
        parse_unit_system(raw)


def test_duplicate_unknown_dimension_and_typed_metadata_are_rejected():
    raw = example()
    raw["unit_system"]["units"].append(deepcopy(raw["unit_system"]["units"][0]))
    with pytest.raises(ValueError, match="duplicate"):
        parse_initial_state(raw)
    raw = example()
    raw["fields"][0]["units"] = "unregistered"
    with pytest.raises(ValueError, match="unknown unit"):
        parse_initial_state(raw)
    raw = example()
    raw["unit_system"]["units"][0]["dimensions"][0] = 17
    with pytest.raises(ValueError, match="exponents"):
        parse_initial_state(raw)
    initial = parse_initial_state(example())
    altered = replace(
        initial.unit_system, base_scales=((True, 1),) + initial.unit_system.base_scales[1:]
    )
    with pytest.raises(ValueError, match="positive integers"):
        Simulation(replace(initial, unit_system=altered))


def test_strict_typed_api_rejects_unknown_formula_instead_of_assuming_units():
    initial = parse_initial_state(example())
    from event_universe.core.disturbance_state import UpdateRule

    bad = replace(
        initial.disturbances[0],
        updates=(UpdateRule(0, Expression("sqrt", (Expression("field", field=0),))),),
    )
    with pytest.raises(ValueError, match="does not support"):
        validate_units(replace(initial, disturbances=(bad,)))


def test_native_event_coefficients_and_control_bindings_remain_dimensionless():
    raw = native_configuration()
    raw["unit_system"] = registry({item["units"]: [0] * 7 for item in raw["fields"]})
    world = Simulation(parse_initial_state(raw))
    world.step()
    decision = next(item for item in raw["fields"] if item["name"] == "decision")
    original = decision["units"]
    decision["units"] = "wrong_dimensional_code"
    raw["unit_system"]["units"].append(
        {"name": decision["units"], "dimensions": DIMENSIONS["mass"], "si_scale": [1, 1]}
    )
    # Reject the binding independently of subsequent mechanical comparisons.
    with pytest.raises(ValueError, match="outcome fields must be dimensionless"):
        parse_initial_state(raw)
    assert original != decision["units"]


def test_published_unit_schema_accepts_valid_structure_and_rejects_bad_dimensions():
    jsonschema = pytest.importorskip("jsonschema")
    path = Path(__file__).resolve().parents[1] / "src/event_universe/schemas/unit-system.schema.json"
    schema = json.loads(path.read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(registry(), schema)
    raw = registry()
    raw["units"][0]["dimensions"] = [1, 2]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(raw, schema)


def test_rational_projections_keep_quantity_units_and_separate_denominator_codes():
    raw = example()
    fraction = op("ratio", op("dot", ref("p"), ref("p")), op("mul", 2, ref("mass")))
    updates = [
        {"field": "energy", "expression": op("rational_whole", fraction)},
        {"field": "count", "expression": op("rational_denominator", fraction)},
    ]
    raw["disturbance_types"][0]["updates"] = updates
    world = Simulation(parse_initial_state(raw))
    world.step()
    values = resident_values(world, (2, 2, 2))[0]
    assert values["energy"] == (25,)
    assert values["count"] == (1,)
    updates[0]["expression"] = op("rational_denominator", fraction)
    with pytest.raises(ValueError, match="dimension"):
        parse_initial_state(raw)


def test_movement_ratio_matches_dimensions_without_assuming_physical_velocity():
    raw = example()
    movement = {
        "mode": "move",
        "direction_field": "p",
        "rate": ref("duration"),
        "rate_divisor": op("mul", 3, ref("duration")),
    }
    raw["disturbance_types"][0]["transport"] = movement
    world = Simulation(parse_initial_state(raw))
    for _ in range(3):
        world.step()
    snapshot = world.snapshot()
    records = [record for cell in snapshot["cells"] for record in cell["disturbances"]]
    records += snapshot["transfers"]
    assert [record["values"]["p"] for record in records] == [(6, 8, 0)]
    movement["rate_divisor"] = ref("mass")
    with pytest.raises(ValueError, match="dimension"):
        parse_initial_state(raw)
    movement["rate_divisor"] = 0
    with pytest.raises(ValueError, match="identically zero"):
        parse_initial_state(raw)


def test_authoring_rejects_cross_dimension_and_inexact_values():
    system = parse_unit_system(registry())
    with pytest.raises(ValueError, match="different dimensions"):
        convert_value(1, "mass", "duration", system)
    for value in (True, 1.25):
        with pytest.raises(ValueError, match="exact integers"):
            convert_value(value, "mass", "mass", system)
    assert convert_value(Fraction(91093837139, 10**41), "mass", "mass", system) == Fraction(
        91093837139, 10**41
    )

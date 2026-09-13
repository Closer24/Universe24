"""External central-value encoding does not select physical laws or lose vectors."""

import copy
import json
from fractions import Fraction
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE
from event_universe.entities import compile_entities
from event_universe.entity_catalog import resolve_property
from event_universe.initialization import parse_initial_state
from event_universe.reference_units import encode_components, main, parse_reference_units

EXAMPLES = Path(__file__).resolve().parents[1] / "examples/known-entities"


@pytest.fixture
def registry():
    return json.loads((EXAMPLES / "physical-units.json").read_text())


def field(unit, scale=1, components=1, signed=True):
    return {"units": unit, "scale": scale, "components": components, "signed": signed}


def test_defining_constants_and_dimensions_have_independent_si_expectations(registry):
    units = parse_reference_units(registry)
    assert units["speed_of_light"].si_scale == 299792458
    assert units["planck_h"].si_scale == Fraction(662607015, 10**42)
    assert units["elementary_charge"].si_scale == Fraction(1602176634, 10**28)
    assert units["MeV/c2"].dimensions == (0, 1, 0, 0, 0, 0, 0)
    assert units["MeV/c"].dimensions == (1, 1, -1, 0, 0, 0, 0)
    assert units["T"].dimensions == (0, 1, -2, -1, 0, 0, 0)
    assert units["J_per_T"].dimensions == (2, 0, 0, 1, 0, 0, 0)
    assert encode_components(registry, "1", "planck_h", field("planck_h"))["value"] == 1
    with pytest.raises(ValueError, match="dimensions"):
        encode_components(registry, "1", "planck_h", field("s"))


def test_all_three_components_use_one_scale_without_rotating_them(registry):
    result = encode_components(registry, ["1.25", "-2.5", "0"], "MeV/c", field("keV/c", components=3))
    assert result["value"] == [1250, -2500, 0]
    assert result["errors_source_units"] == ["0", "0", "0"]
    charge = encode_components(registry, "-1", "elementary_charge", field("charge_third"))
    assert charge["value"] == -3
    assert (
        encode_components(registry, "-1", "elementary_charge", field("elementary charge", 3))["value"]
        == -3
    )


def test_exact_mode_rejects_rounding_and_explicit_budget_bounds_actual_error(registry):
    catalog = json.loads((EXAMPLES / "catalog.json").read_text())
    mass = resolve_property(catalog, "electron", "mass")
    with pytest.raises(ValueError, match="exact integer"):
        encode_components(registry, mass["value_decimal"], mass["unit"], field("keV/c2"))
    result = encode_components(
        registry, mass["value_decimal"], mass["unit"], field("keV/c2"), max_error="0.000002"
    )
    assert result["value"] == 511
    assert Fraction(result["errors_source_units"][0]) == Fraction(104931, 10**11)
    with pytest.raises(ValueError, match="exceeds max_error"):
        encode_components(
            registry, mass["value_decimal"], mass["unit"], field("keV/c2"), max_error="0.000001"
        )


@pytest.mark.parametrize("value,expected", [("1.5", 2), ("-1.5", -2), ("0.5", 1), ("-0.5", -1)])
def test_ties_have_symmetric_explicit_rounding(registry, value, expected):
    assert encode_components(registry, value, "one", field("one"), max_error="0.5")["value"] == expected


@pytest.mark.parametrize("value", [float("nan"), 1.5, True, "NaN", "Infinity", "1/3", "1" * 129])
def test_external_values_reject_implicit_or_unbounded_numeric_inputs(registry, value):
    with pytest.raises(ValueError):
        encode_components(registry, value, "one", field("one"))


@pytest.mark.parametrize(
    "bad", [field("one", 0), field("one", True), field("one", MAX_VALUE + 1), field("one", components=6)]
)
def test_runtime_shape_and_scale_bounds_apply_before_encoding(registry, bad):
    with pytest.raises(ValueError):
        encode_components(registry, "1", "one", bad)


def test_overflow_sign_and_shape_fail_without_partial_output(registry):
    assert encode_components(registry, str(MAX_VALUE), "one", field("one"))["value"] == MAX_VALUE
    with pytest.raises(ValueError, match="payload"):
        encode_components(registry, ["1", str(MAX_VALUE + 1), "0"], "one", field("one", components=3))
    with pytest.raises(ValueError, match="unsigned"):
        encode_components(registry, "-0.01", "one", field("one", signed=False), max_error="1")
    with pytest.raises(ValueError, match="shape"):
        encode_components(registry, ["1", "2"], "one", field("one", components=3))


@pytest.mark.parametrize(
    "mutation",
    ["cycle", "unknown", "bad_dimension", "negative_ratio", "uncited", "measured_without_error"],
)
def test_registry_rejects_invalid_unused_entries(registry, mutation):
    if mutation in ("cycle", "unknown"):
        registry["definitions"]["unused"] = {
            "factors": {"unused" if mutation == "cycle" else "missing": 1},
            "ratio": [1, 1],
        }
    elif mutation == "bad_dimension":
        registry["definitions"]["m"]["dimensions"][0] = True
    elif mutation == "negative_ratio":
        registry["definitions"]["m"]["si_ratio"] = [-1, 1]
    elif mutation == "uncited":
        registry["definitions"]["planck_h"]["sources"] = ["missing"]
    else:
        registry["definitions"]["newton_G"].pop("uncertainty_decimal")
    with pytest.raises(ValueError):
        parse_reference_units(registry)


def test_measured_unit_uncertainty_is_not_hidden_in_encoding_precision(registry):
    result = encode_components(
        registry, "1", "bohr_magneton", field("J_per_T", scale=MAX_VALUE), max_error="1"
    )
    assert result["value"] == 0
    assert result["measured_scale_dependencies"] == ["bohr_magneton"]
    assert result["experimental_uncertainty_propagated"] is False


def test_catalog_cli_uses_signed_reference_and_keeps_scalar_shape(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        [
            "reference_units",
            "--registry",
            str(EXAMPLES / "physical-units.json"),
            "--catalog",
            str(EXAMPLES / "catalog.json"),
            "--entity",
            "positron",
            "--property",
            "magnetic_moment",
            "--field-unit",
            "bohr_magneton",
            "--scale",
            "1000000",
            "--max-error",
            "0.000001",
        ],
    )
    main()
    assert json.loads(capsys.readouterr().out)["value"] == 1001160


def test_charge_encoding_reuses_catalog_intrinsic_integer(registry):
    catalog = json.loads((EXAMPLES / "catalog.json").read_text())
    charge = resolve_property(catalog, "electron", "electric_charge")
    assert charge["metadata_key"] == "electric_charge_thirds"
    assert (
        encode_components(
            registry, charge["value_decimal"], charge["unit"], field("elementary charge", 3)
        )["value"]
        == -3
    )


def test_encoded_reference_inventory_and_vectors_survive_periodic_link_transfers(registry):
    catalog = json.loads((EXAMPLES / "catalog.json").read_text())
    profiles = json.loads((EXAMPLES / "representation-probes.json").read_text())
    profiles = copy.deepcopy(profiles)
    selected = ["electron", "proton", "neutron"]
    expected_mass = {"electron": 511, "proton": 938272, "neutron": 939565}
    for row in profiles["profiles"]:
        if row["entity_id"] not in selected:
            continue
        profile = row["executable_profile"]
        definition = {"name": "reference_mass", **field("keV/c2", signed=False), "conserved": True}
        prop = resolve_property(catalog, row["entity_id"], "mass")
        value = encode_components(
            registry, prop["value_decimal"], prop["unit"], definition, max_error="0.0005"
        )["value"]
        assert value == expected_mass[row["entity_id"]]
        profile["fields"].append(definition)
        profile["disturbance"]["fields"].append("reference_mass")
        profile["disturbance"]["defaults"]["reference_mass"] = value
        profile["seed_values"]["reference_mass"] = value
        # The existing half-rate motion is a transport probe, not mass-dependent physics.
        profile["seed_values"]["momentum"] = encode_components(
            registry, ["1", "-2", "3"], "one", field("one", components=3)
        )["value"]
    raw = compile_entities(catalog, selected, profiles=profiles, shape=(9, 9, 9), link_ticks=2, ticks=40)
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    for _ in range(40):
        world.step()
        assert world.totals()["reference_mass"] == (1878348,)
        assert world.totals()["charge"] == (0,)
        assert world.totals()["momentum"] == (3, -6, 9)
    sent = [event for event in events if event["event"] == "sent"]
    assert sent and all(event["arrival_tick"] - event["tick"] == 2 for event in sent)

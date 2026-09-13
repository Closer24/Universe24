"""Independent validation of named readouts before constructing any physical world."""

import json
from copy import deepcopy

import pytest

from event_universe.configuration_validation import validate_configuration
from event_universe.core.disturbance_engine import DisturbanceEngine
from event_universe.core.disturbance_state import MAX_VALUE
from event_universe.disturbance_api import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

from .test_disturbance_engine import document, field, kind
from .test_local_field_rules import document as spatial_document
from .test_local_field_rules import local, operation, seed
from .test_node_rule_contract import node_profile


def configuration(*, spatial=False):
    if spatial:
        return node_profile(spatial_document([field("quantity", conserved=False)]))
    return node_profile(
        document(
            [kind("parcel", values={"quantity": 2})],
            [((0, 0, 0), "parcel")],
            fields=[field("quantity", conserved=False)],
        )
    )


@pytest.mark.parametrize(
    "failure, message",
    [
        ("empty quantities", "conservation quantities"),
        ("missing quantities", "missing keys"),
        ("duplicate quantity", "duplicate conserved readout name"),
        ("empty coverage", "cover every disturbance layout"),
        ("missing carriers", "missing keys"),
        ("overlapping coverage", "exactly once"),
        ("duplicate requirement", "duplicate readout property"),
        ("empty requirement", "readout requires"),
        ("unknown requirement", "unknown name"),
        ("unowned property", "not owned"),
        ("wrong shape", "expected 3"),
        ("cost dependency", "cost reporters"),
        ("incoming projection", "unknown name"),
    ],
)
def test_readouts_reject_incomplete_ambiguous_or_noninventory_definitions(failure, message):
    raw = configuration()
    contract = raw["conservation_contract"]
    quantity = contract["quantities"][0]
    carrier = quantity["carriers"][0]
    if failure == "empty quantities":
        contract["quantities"] = []
    elif failure == "missing quantities":
        contract.pop("quantities")
    elif failure == "duplicate quantity":
        contract["quantities"].append(deepcopy(quantity))
    elif failure == "empty coverage":
        quantity["carriers"] = []
    elif failure == "missing carriers":
        quantity.pop("carriers")
    elif failure == "overlapping coverage":
        quantity["carriers"].append(deepcopy(carrier))
    elif failure == "duplicate requirement":
        carrier["requires"] *= 2
    elif failure == "empty requirement":
        carrier["requires"] = []
    elif failure == "unknown requirement":
        carrier["requires"] = ["undefined"]
    elif failure == "unowned property":
        raw["fields"].append({**field("other", conserved=False), "aggregation": "sum"})
        carrier["value"] = {"field": "other"}
    elif failure == "wrong shape":
        quantity["components"] = 3
    elif failure == "cost dependency":
        raw["disturbance_types"][0]["cost_field"] = "quantity"
    else:
        carrier["value"] = {"received": "quantity", "port": 0}
    with pytest.raises(ValueError, match=message):
        parse_initial_state(raw)


@pytest.mark.parametrize("components", [0, -1, True, 1.5, 33])
def test_readout_components_require_bounded_positive_integers(components):
    raw = configuration()
    raw["conservation_contract"]["quantities"][0]["components"] = components
    with pytest.raises(ValueError):
        parse_initial_state(raw)


@pytest.mark.parametrize(
    "failure, message",
    [
        ("missing spatial", "cover the configured spatial fields"),
        ("nonzero baseline", "zero spatial baselines"),
        ("nonzero empty", "empty spatial inventory"),
        ("unexpected spatial", "cover the configured spatial fields"),
    ],
)
def test_spatial_readouts_cover_actual_stock_and_preserve_empty_inventory(failure, message):
    raw = configuration(spatial=failure != "unexpected spatial")
    quantity = raw["conservation_contract"]["quantities"][0]
    if failure == "missing spatial":
        quantity.pop("spatial")
    elif failure == "nonzero baseline":
        raw["spatial_fields"][0]["baseline"] = 1
    elif failure == "nonzero empty":
        quantity["spatial"] = 1
    else:
        quantity["spatial"] = 0
    with pytest.raises(ValueError, match=message):
        parse_initial_state(raw)


def test_canonical_preflight_prepares_readouts_without_constructing_a_world(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("preflight attempted to construct or run a physical world")

    monkeypatch.setattr(Simulation, "__init__", forbidden)
    monkeypatch.setattr(DisturbanceEngine, "__init__", forbidden)
    monkeypatch.setattr(DisturbanceEngine, "step", forbidden)
    raw = configuration(spatial=True)
    original = deepcopy(raw)
    report = validate_configuration(json.dumps(raw), kind="initialization")
    assert report.valid, report.to_dict()
    assert raw == original
    assert parse_initial_state(raw).conservation_contract.quantities[0].name == "declared stock"
    raw["conservation_contract"]["quantities"][0]["spatial"] = 1
    failed = validate_configuration(json.dumps(raw), kind="initialization")
    assert not failed.valid
    assert "empty spatial inventory" in failed.issues[0].message


@pytest.mark.parametrize("name", ["energy", "momentum", "constructor", "__proto__"])
def test_readout_names_do_not_select_a_formula_or_change_the_declared_expression(name):
    raw = configuration()
    raw["conservation_contract"]["quantities"][0]["name"] = name
    parsed = parse_initial_state(raw).conservation_contract.quantities[0]
    assert parsed.name == name
    assert parsed.components == 1
    assert parsed.carriers[0].expression.op == "field"
    assert parsed.carriers[0].expression.field == 0


def large_initial_readouts(count, *, spatial=False):
    raw = node_profile(
        document(
            [kind("parcel", values={"quantity": MAX_VALUE})],
            [((0, 0, 0), "parcel")] * count,
            fields=[field("quantity", conserved=False)],
        )
    )
    quantity = raw["conservation_contract"]["quantities"][0]
    quantity["carriers"][0]["value"] = operation("mul", {"field": "quantity"}, {"field": "quantity"})
    if spatial:
        raw["spatial_fields"] = [{"field": "quantity", "baseline": 0, "transport": "local"}]
        raw["spatial_seeds"] = [seed("quantity", MAX_VALUE, (0, 0, 0))]
        quantity["spatial"] = operation("mul", local("quantity"), local("quantity"))
    return raw


@pytest.mark.parametrize("spatial", [False, True])
def test_initial_joint_owner_readouts_enforce_local_accumulation_bounds(spatial):
    # Eight squared maximum payloads fit in a working integer; nine do not.
    raw = large_initial_readouts(8 - int(spatial), spatial=spatial)
    original = deepcopy(raw)
    assert parse_initial_state(raw).conservation_contract is not None
    assert raw == original
    raw["seeds"].append(deepcopy(raw["seeds"][0]))
    with pytest.raises(ValueError, match=r"initial conservation.*\(0, 0, 0\).*64-bit"):
        parse_initial_state(raw)


@pytest.mark.parametrize("spatial", [False, True])
def test_initial_owner_readouts_check_expression_intermediates(spatial):
    raw = large_initial_readouts(0 if spatial else 1, spatial=spatial)
    quantity = raw["conservation_contract"]["quantities"][0]
    if spatial:
        quantity["spatial"] = operation("mul", quantity["spatial"], local("quantity"))
    else:
        carrier = quantity["carriers"][0]
        carrier["value"] = operation("mul", carrier["value"], {"field": "quantity"})
    with pytest.raises(ValueError, match="initial conservation.*64-bit"):
        parse_initial_state(raw)


def test_initial_readout_bounds_apply_per_node_and_not_to_host_totals():
    raw = large_initial_readouts(9)
    for index, item in enumerate(raw["seeds"]):
        item["position"] = [index, 0, 0]
    assert parse_initial_state(raw).conservation_contract is not None


def test_initial_readout_failure_is_pure_preflight_and_creates_no_run_artifacts(monkeypatch, tmp_path):
    def forbidden(*args, **kwargs):
        raise AssertionError("preflight attempted to construct a physical world")

    monkeypatch.setattr(Simulation, "__init__", forbidden)
    monkeypatch.setattr(DisturbanceEngine, "__init__", forbidden)
    source = json.dumps(large_initial_readouts(9))
    report = validate_configuration(source, kind="initialization")
    assert not report.valid
    assert "initial conservation" in report.issues[0].message
    path, output = tmp_path / "initial.json", tmp_path / "output"
    path.write_text(source, encoding="utf-8")
    with pytest.raises(ValueError, match="initial conservation.*64-bit"):
        run_initialization(path, output, ticks=1)
    assert not output.exists()

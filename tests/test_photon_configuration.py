"""Independent checks of field-owned photon preparation, not photon dynamics."""

import copy
import hashlib
import json
import runpy
import subprocess
import sys
from pathlib import Path

import pytest

from event_universe.configuration_validation import prepare_initialization
from event_universe.core.integer import MAX_WORK_INT
from event_universe.entities import compile_entities
from event_universe.integration.event_program import parse_event_program

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/photon"
MODULE = runpy.run_path(str(EXAMPLE / "prepare.py"))
PREPARE = MODULE["prepare"]
WRITE = MODULE["write_preparation"]
CATALOG_PATH = ROOT / "examples/known-entities/catalog.json"
PROFILES_PATH = ROOT / "examples/known-entities/representation-probes.json"
CATALOG = json.loads(CATALOG_PATH.read_text())
PROFILES = json.loads(PROFILES_PATH.read_text())
DEFINITION = json.loads((EXAMPLE / "definition.json").read_text())


def prepared(change=None):
    definition = copy.deepcopy(DEFINITION)
    if change:
        change(definition)
    return PREPARE(definition, CATALOG, PROFILES)


def test_one_photon_uses_only_the_two_parent_field_registers():
    raw, report = prepared()
    program = parse_event_program(prepare_initialization(raw).initial)
    assert program.network.register_names == (
        "electromagnetic_field:transverse-1",
        "electromagnetic_field:transverse-2",
    )
    assert program.network.local_dimensions == (3, 3)
    assert program.network.levels == (1, 0)
    assert raw["seeds"] == []
    assert "spatial_fields" not in raw
    assert raw["event_program"]["layers"] == []
    assert raw["event_program"]["bindings"] == []
    assert report["entity_id"] == "photon" and report["field_id"] == "electromagnetic_field"
    assert report["quantum_count"] == 1
    assert report["energy"]["per_quantum"] == {"numerator": 1, "denominator": 8}
    assert report["energy"]["total_above_vacuum"] == {"numerator": 1, "denominator": 8}


def test_frequency_doubles_energy_not_transport_or_quantum_amplitudes():
    a, report_a = prepared()
    b, report_b = prepared(lambda d: d["frequency"].update(numerator=2))
    assert a == b  # Preparation descriptor is not a fabricated phase or motion law.
    assert report_a["energy"]["per_quantum"] == {"numerator": 1, "denominator": 8}
    assert report_b["energy"]["per_quantum"] == {"numerator": 1, "denominator": 4}
    assert report_b["frequency"]["status"] == "declared_preparation"
    assert report_b["energy"]["reference_frame"] == report_b["frequency"]["reference_frame"]


@pytest.mark.parametrize(
    "levels,total", [((0, 0), (0, 1)), ((0, 1), (1, 8)), ((1, 1), (1, 4)), ((2, 2), (1, 2))]
)
def test_polarization_and_occupation_keep_frequency_and_count_energy_once(levels, total):
    raw, report = prepared(
        lambda d: d.update(occupations=dict(zip(("transverse-1", "transverse-2"), levels, strict=True)))
    )
    assert raw["event_program"]["initial_levels"] == list(levels)
    assert report["energy"]["per_quantum"] == {"numerator": 1, "denominator": 8}
    assert report["energy"]["total_above_vacuum"] == dict(
        zip(("numerator", "denominator"), total, strict=True)
    )
    assert report["quantum_count"] == sum(levels)


@pytest.mark.parametrize("field", ["numerator", "denominator"])
@pytest.mark.parametrize("value", [0, -1, True, 1.5, "1", None])
def test_frequency_requires_positive_bounded_integer_ratio(field, value):
    with pytest.raises(ValueError):
        prepared(lambda d: d["frequency"].update({field: value}))


@pytest.mark.parametrize("field", ["reference_frame", "time_unit"])
@pytest.mark.parametrize("value", ["", " ", " bad ", 1])
def test_frequency_context_is_explicit(field, value):
    with pytest.raises(ValueError):
        prepared(lambda d: d["frequency"].update({field: value}))


@pytest.mark.parametrize("level", [-1, True, 1.5, 3])
def test_occupation_rejects_invalid_or_unrepresented_levels(level):
    with pytest.raises(ValueError):
        prepared(lambda d: d["occupations"].update({"transverse-1": level}))


@pytest.mark.parametrize(
    "changes",
    [
        {"field_id": "strong_field"},
        {"entity_id": "electron"},
        {"field_id": "missing"},
        {"energy": 123},
        {"definition_version": True},
        {"representation": "classical_particle"},
        {"occupations": {"transverse-1": 1}},
        {"shape": [9, 9]},
        {"link_ticks": 0},
        {"ticks": -1},
    ],
)
def test_inconsistent_association_and_unsupported_configuration_fail(changes):
    with pytest.raises(ValueError):
        prepared(lambda d: d.update(changes))


def test_missing_profile_fails_instead_of_creating_an_implicit_field():
    profiles = copy.deepcopy(PROFILES)
    profiles["profiles"] = [
        row for row in profiles["profiles"] if row["entity_id"] != "electromagnetic_field"
    ]
    with pytest.raises(ValueError, match="no profile"):
        PREPARE(DEFINITION, CATALOG, profiles)


def test_arbitrary_quantum_basis_is_not_interpreted_as_photon_number():
    profiles = copy.deepcopy(PROFILES)
    field = next(row for row in profiles["profiles"] if row["entity_id"] == "electromagnetic_field")
    field["quantum_profile"]["registers"][0]["basis"] = ["left", "middle", "right"]
    with pytest.raises(ValueError, match="number-occupation"):
        PREPARE(DEFINITION, CATALOG, profiles)


def test_exact_ratios_and_checked_integer_limits():
    _, report = prepared(lambda d: d["frequency"].update(numerator=6, denominator=10))
    assert report["energy"]["per_quantum"] == {"numerator": 3, "denominator": 5}
    _, report = prepared(lambda d: d["frequency"].update(numerator=MAX_WORK_INT, denominator=1))
    assert report["energy"]["per_quantum"] == {"numerator": MAX_WORK_INT, "denominator": 1}
    with pytest.raises(OverflowError):
        prepared(lambda d: d["frequency"].update(numerator=MAX_WORK_INT + 1))

    def overflow_total(d):
        d["frequency"].update(numerator=MAX_WORK_INT, denominator=1)
        d["occupations"]["transverse-1"] = 2

    with pytest.raises(OverflowError):
        prepared(overflow_total)


def test_inputs_and_existing_classical_photon_proxy_are_unchanged():
    before = copy.deepcopy((DEFINITION, CATALOG, PROFILES))
    baseline = compile_entities(CATALOG, ["photon"], profiles=PROFILES)
    prepared()
    assert (DEFINITION, CATALOG, PROFILES) == before
    assert compile_entities(CATALOG, ["photon"], profiles=PROFILES) == baseline
    assert baseline["disturbance_types"][0]["transport"]["rate_denominator"] == 2


def test_outputs_bind_definition_and_runtime_bytes_without_overwrite(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    report = WRITE(EXAMPLE / "definition.json", CATALOG_PATH, PROFILES_PATH, a)
    WRITE(EXAMPLE / "definition.json", CATALOG_PATH, PROFILES_PATH, b)
    assert (
        report["initialization_sha256"]
        == hashlib.sha256((a / "initialization.json").read_bytes()).hexdigest()
    )
    assert (
        report["source_sha256"]["definition"]
        == hashlib.sha256((a / "definition.json").read_bytes()).hexdigest()
    )
    for path in a.iterdir():
        assert path.read_bytes() == (b / path.name).read_bytes()
    with pytest.raises(FileExistsError):
        WRITE(EXAMPLE / "definition.json", CATALOG_PATH, PROFILES_PATH, a)
    assert not list(a.glob("*.html"))


def test_invalid_definition_never_creates_output(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"definition_version":1,"definition_version":2}')
    with pytest.raises(ValueError):
        WRITE(bad, CATALOG_PATH, PROFILES_PATH, tmp_path / "output")
    assert not (tmp_path / "output").exists()


def test_preparation_cli_produces_ordinary_validated_input(tmp_path):
    output = tmp_path / "prepared"
    result = subprocess.run(
        [
            sys.executable,
            str(EXAMPLE / "prepare.py"),
            "--catalog",
            str(CATALOG_PATH),
            "--profiles",
            str(PROFILES_PATH),
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    report = json.loads(result.stdout)
    assert report["quantum_count"] == 1
    raw = json.loads((output / "initialization.json").read_text())
    assert parse_event_program(prepare_initialization(raw).initial).network.levels == (1, 0)

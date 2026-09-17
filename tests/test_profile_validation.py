"""Whole-library profile validation uses existing representation owners."""

import copy
import json
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.entities import compile_entities, validate_profiles

HERE = Path(__file__).resolve().parents[1] / "examples/known-entities"


@pytest.fixture
def documents():
    return (
        json.loads((HERE / "catalog.json").read_text()),
        json.loads((HERE / "representation-probes.json").read_text()),
    )


def test_all_profiles_validate_independently_without_world_capacity_failure(documents):
    catalog, profiles = documents
    assert validate_profiles(catalog, profiles) == {"profiles": 46, "classical": 46}


def test_invalid_unselected_profile_is_caught_with_context(documents):
    catalog, profiles = documents
    positron = next(row for row in profiles["profiles"] if row["entity_id"] == "positron")
    positron["executable_profile"]["seed_values"]["inventory"] = 1.5
    # Selection-scoped compilation need not inspect unrelated profile contents.
    compile_entities(catalog, ["electron"], profiles=profiles)
    with pytest.raises(ValueError, match="positron classical profile"):
        validate_profiles(catalog, profiles)


def test_subset_with_one_profile_is_valid(documents):
    catalog, profiles = documents
    electron = next(row for row in profiles["profiles"] if row["entity_id"] == "electron")
    profiles["profiles"] = [
        {"entity_id": "electron", "executable_profile": electron["executable_profile"]}
    ]
    assert validate_profiles(catalog, profiles) == {"profiles": 1, "classical": 1}


def test_empty_library_does_not_require_unsupported_catalog_families(documents):
    catalog, profiles = documents
    profiles["profiles"] = []
    assert validate_profiles(catalog, profiles) == {"profiles": 0, "classical": 0}


def test_validation_preserves_inputs_and_never_constructs_simulation_or_reads_files(
    documents, monkeypatch
):
    catalog, profiles = documents
    before = copy.deepcopy(documents)

    def forbidden(*args, **kwargs):
        raise AssertionError("Profile validation must not construct, step, read, or write")

    monkeypatch.setattr(Simulation, "__init__", forbidden)
    monkeypatch.setattr(Simulation, "step", forbidden)
    for method in ("read_text", "read_bytes", "write_text", "write_bytes", "open"):
        monkeypatch.setattr(Path, method, forbidden)
    assert validate_profiles(catalog, profiles)["profiles"] == 46
    assert documents == before


@pytest.mark.parametrize(
    "mutation, message",
    [
        ("missing_id", "unique nonempty"),
        ("orphan_id", "orphan"),
        ("duplicate_id", "unique nonempty"),
        ("missing_representation", "incomplete profile binding"),
        ("missing_document", "requires explicit profiles"),
        ("invalid_version", "profile_version"),
    ],
)
def test_invalid_profile_binding_or_document_is_rejected(documents, mutation, message):
    catalog, profiles = documents
    if mutation == "missing_id":
        del profiles["profiles"][0]["entity_id"]
    elif mutation == "orphan_id":
        profiles["profiles"][0]["entity_id"] = "absent entity"
    elif mutation == "duplicate_id":
        profiles["profiles"].append(copy.deepcopy(profiles["profiles"][0]))
    elif mutation == "missing_representation":
        profiles["profiles"][0] = {"entity_id": "electron"}
    elif mutation == "missing_document":
        profiles = None
    else:
        profiles["profile_version"] = True
    with pytest.raises(ValueError, match=message):
        validate_profiles(catalog, profiles)


def test_malformed_profile_object_has_entity_and_representation_context(documents):
    catalog, profiles = documents
    row = next(row for row in profiles["profiles"] if row["entity_id"] == "electron")
    row["executable_profile"] = None
    with pytest.raises(ValueError, match="electron classical profile"):
        validate_profiles(catalog, profiles)


def test_public_library_validator_requires_physical_catalog_v2(documents):
    catalog, profiles = documents
    catalog["catalog_version"] = 1
    with pytest.raises(ValueError, match="catalog_version 2"):
        validate_profiles(catalog, profiles)


def test_failed_validation_also_preserves_inputs(documents):
    catalog, profiles = documents
    profiles["profiles"][-1]["executable_profile"]["claim_level"] = "unsupported"
    before = copy.deepcopy(documents)
    with pytest.raises(ValueError):
        validate_profiles(catalog, profiles)
    assert documents == before

"""Catalog coverage, native compilation and adversarial profile validation."""

import copy
import json
from pathlib import Path

import pytest

from event_universe.entities import compile_entities
from event_universe.integration.event_program import parse_event_program
from event_universe.reference_api import ReferenceSimulation as Simulation
from event_universe.reference_api import parse_reference_state as parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "examples/known-entities/catalog.json").read_text())
ENTRIES = CATALOG["field_entities"] + CATALOG["particle_entities"]


@pytest.mark.parametrize("identity", [e["id"] for e in ENTRIES])
def test_every_existing_entity_has_a_finite_quantum_definition(identity):
    raw = compile_entities(CATALOG, [identity], representation="quantum")
    initial = parse_initial_state(raw)
    program = parse_event_program(initial)
    assert program.network is not None
    assert program.network.register_names
    # One representative tick suffices: these profiles only declare preparation.
    world = Simulation(initial)
    world.step()
    assert world.computation_report()["resolver"]["random_draws"] == 0
    assert world.computation_report()["resolver"]["oracle_calls"] == 0
    assert raw["seeds"] == []


def test_particle_and_field_quantum_profiles_compose_without_classical_copies():
    raw = compile_entities(
        CATALOG, ["electron", "positron", "electromagnetic_field"], representation="quantum"
    )
    p = parse_event_program(parse_initial_state(raw))
    assert p.network.local_dimensions == (2, 2, 2, 2, 3, 3)
    assert p.network.levels == (1, 0, 1, 0, 1, 0)
    assert len(set(p.network.register_names)) == 6
    assert len(set(p.network.addresses)) == 1
    assert "spatial_fields" not in raw


def test_quantum_labels_do_not_select_hidden_species_laws():
    catalog = copy.deepcopy(CATALOG)
    e = catalog["particle_entities"][0]
    previous = e["id"]
    e["id"] = "arbitrary renamed mode"
    a = compile_entities(CATALOG, [previous], representation="quantum")
    b = compile_entities(catalog, [e["id"]], representation="quantum")
    a["event_program"]["register_names"] = b["event_program"]["register_names"]
    assert a == b


@pytest.mark.parametrize("mutation", ["basis", "level", "profile", "duplicate", "incomplete"])
def test_invalid_quantum_profile_rejected(mutation):
    catalog = copy.deepcopy(CATALOG)
    e = catalog["particle_entities"][0]
    p = e["quantum_profile"]
    if mutation == "basis":
        p["registers"][0]["basis"] = ["a", "a"]
    if mutation == "level":
        p["registers"][0]["initial_level"] = 2
    if mutation == "profile":
        p["claim_level"] = "verified physical field"
    if mutation == "duplicate":
        p["registers"][1]["name"] = p["registers"][0]["name"]
    if mutation == "incomplete":
        del p["missing_dynamics"]
    with pytest.raises(ValueError):
        compile_entities(catalog, [e["id"]], representation="quantum")


def test_excessive_composition_does_not_expand_local_capacity():
    with pytest.raises((ValueError, OverflowError)):
        compile_entities(CATALOG, [e["id"] for e in ENTRIES], representation="quantum")


def test_classical_profiles_are_unchanged_by_quantum_selection():
    a = compile_entities(CATALOG, ["electron"])
    b = compile_entities(CATALOG, ["electron"], representation="classical")
    assert a == b
    assert "event_program" not in a
    with pytest.raises(ValueError):
        compile_entities(CATALOG, ["electron"], representation="unknown")

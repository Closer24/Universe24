"""Catalog coverage, native compilation and adversarial profile validation."""

import copy
import json
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.entities import compile_entities
from event_universe.initialization import parse_initial_state
from event_universe.integration.event_program import parse_event_program

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "examples/known-entities/catalog.json").read_text())
PROFILES = json.loads((ROOT / "examples/known-entities/representation-probes.json").read_text())
ENTRIES = PROFILES["profiles"]


@pytest.mark.parametrize("identity", [e["entity_id"] for e in ENTRIES])
def test_every_existing_entity_has_a_finite_quantum_definition(identity):
    raw = compile_entities(CATALOG, [identity], profiles=PROFILES, representation="quantum")
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
        CATALOG,
        ["electron", "positron", "electromagnetic_field"],
        profiles=PROFILES,
        representation="quantum",
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
    e["label"] = "arbitrary renamed mode"
    a = compile_entities(CATALOG, [previous], profiles=PROFILES, representation="quantum")
    b = compile_entities(catalog, [e["id"]], profiles=PROFILES, representation="quantum")
    a["event_program"]["register_names"] = b["event_program"]["register_names"]
    assert a == b


@pytest.mark.parametrize("mutation", ["basis", "level", "profile", "duplicate", "incomplete"])
def test_invalid_quantum_profile_rejected(mutation):
    catalog = copy.deepcopy(CATALOG)
    e = catalog["particle_entities"][0]
    profiles = copy.deepcopy(PROFILES)
    p = next(row for row in profiles["profiles"] if row["entity_id"] == e["id"])["quantum_profile"]
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
        compile_entities(catalog, [e["id"]], profiles=profiles, representation="quantum")


def test_excessive_composition_does_not_expand_local_capacity():
    with pytest.raises((ValueError, OverflowError)):
        compile_entities(
            CATALOG, [e["entity_id"] for e in ENTRIES], profiles=PROFILES, representation="quantum"
        )


def test_classical_profiles_are_unchanged_by_quantum_selection():
    a = compile_entities(CATALOG, ["electron"], profiles=PROFILES)
    b = compile_entities(CATALOG, ["electron"], profiles=PROFILES, representation="classical")
    assert a == b
    assert "event_program" not in a
    with pytest.raises(ValueError):
        compile_entities(CATALOG, ["electron"], profiles=PROFILES, representation="unknown")

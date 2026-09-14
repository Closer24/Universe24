"""Catalog data reaches the unchanged causal contact mechanism with one inventory owner."""

import importlib.util
import json
from functools import cache
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import unpack
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "catalog_contact_prepare", ROOT / "examples/catalog-contact/prepare.py"
)
AUTHOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUTHOR)
SETTINGS = AUTHOR.load(AUTHOR.EXPERIMENT)
REPRESENTATIVES = (
    "electron",
    "positron",
    "up_quark",
    "antiup_quark",
    "down_quark",
    "antidown_quark",
    "photon",
    "electron_neutrino",
    "top_quark",
    "neutron",
    "higgs_boson",
)


@cache
def prepared(identity):
    raw, provenance = AUTHOR.prepare([identity])
    # Share immutable authoring output, never mutable worlds or configurations.
    return json.dumps(raw), json.dumps(provenance)


@pytest.mark.parametrize("identity", SETTINGS["particle_ids"])
def test_every_catalog_binding_reaches_both_conversion_templates(identity):
    encoded, provenance = prepared(identity)
    raw, binding = json.loads(encoded), json.loads(provenance)["bindings"][identity]
    values = binding["values"]
    assert values["charge"] == binding["catalog_reference"]["electric_charge_thirds"]
    assert values["spin_twice"] == binding["catalog_reference"]["twice_spin"]
    assert values["mass_assigned"] == int(binding["mass_encoding"] is not None)
    initial = parse_initial_state(raw)
    source = initial.seeds[0].record
    decoded = {
        field.name: unpack(value)[0] for field, value in zip(initial.fields, source.values, strict=True)
    }
    assert {name: decoded[name] for name in values} == values
    kind = next(row for row in raw["disturbance_types"] if row["name"] == binding["source_type"])
    assert kind["defaults"] == values
    domain = raw["event_program"]["domains"][0]
    assert domain["source"]["type"] == binding["source_type"]
    assert domain["capture"]["output"]["values"] == values
    assert any(row["type"] == binding["source_type"] for row in raw["emissions"])


def test_dynamic_representatives_cover_every_encoded_property_regime_and_largest_mass():
    values = {
        key: json.loads(prepared(key)[1])["bindings"][key]["values"] for key in SETTINGS["particle_ids"]
    }

    def regimes(row):
        return {
            ("charge", row["charge"]),
            ("spin", row["spin_twice"]),
            ("mass", bool(row["mass"]), row["mass_assigned"]),
        }

    assert set(REPRESENTATIVES) <= values.keys()
    assert set.union(*(regimes(values[key]) for key in REPRESENTATIVES)) == set.union(
        *(regimes(row) for row in values.values())
    )
    assert max(values[key]["mass"] for key in REPRESENTATIVES) == max(
        row["mass"] for row in values.values()
    )


@pytest.mark.parametrize("identity", REPRESENTATIVES)
def test_property_regime_preserves_inventory_through_contact_and_capture(identity):
    encoded, report = prepared(identity)
    raw, provenance = json.loads(encoded), json.loads(report)
    values = provenance["bindings"][identity]["values"]
    world = Simulation(parse_initial_state(raw))
    for _ in range(raw["ticks"]):
        world.step()
        assert world.totals()["charge"] == (values["charge"],)
        assert world.totals()["mass"] == (values["mass"],)
        assert all(row["balanced"] for row in world.spatial_accounting().values())
    transfers = world._resolver.report()["contact_transfers"]
    assert [row["direction"] for row in transfers] == ["to_quantum", "to_localized"]
    assert transfers[1]["address"] == (3, 1, 1)
    outputs = [
        record
        for node in world.nodes.values()
        for record in node.records
        if record is not None and record.type_index == 0
    ]
    assert len(outputs) == 1
    assert world.record_values(outputs[0]) == {key: (value,) for key, value in values.items()}
    emitted = world.source_totals()["electric_signal"][0]
    assert (emitted > 0) - (emitted < 0) == (values["charge"] > 0) - (values["charge"] < 0)


def test_demo_uses_actual_charge_thirds_and_bounded_mass_encoding():
    raw, report = AUTHOR.prepare()
    values = {key: binding["values"] for key, binding in report["bindings"].items()}
    assert [values[key]["charge"] for key in SETTINGS["default_entities"]] == [-3, 2, -1]
    assert values["electron"]["mass"] == 511
    assert values["up_quark"]["mass"] == 2160
    world = Simulation(parse_initial_state(raw))
    for _ in range(raw["ticks"]):
        world.step()
        assert world.totals()["charge"] == (-2,)
        assert world.totals()["mass"] == (sum(row["mass"] for row in values.values()),)
        assert all(row["balanced"] for row in world.spatial_accounting().values())
    transfers = world._resolver.report()["contact_transfers"]
    assert sum(row["direction"] == "to_localized" for row in transfers) == 3


def test_unknown_flavor_mass_is_distinct_from_theoretical_zero_mass():
    _, report = AUTHOR.prepare(["electron_neutrino", "photon"])
    neutrino, photon = (report["bindings"][key] for key in ("electron_neutrino", "photon"))
    assert neutrino["values"]["mass"] == photon["values"]["mass"] == 0
    assert neutrino["values"]["mass_assigned"] == 0
    assert neutrino["mass_encoding"] is None
    assert neutrino["mass_reference"]["status"] == "not_applicable"
    assert photon["values"]["mass_assigned"] == 1
    assert photon["mass_reference"]["status"] == "theoretical"


def test_conjugates_reuse_mass_and_reverse_source_sign_without_species_laws():
    raw, report = AUTHOR.prepare(["up_quark", "antiup_quark", "up_quark"])
    positive, negative = (report["bindings"][key]["values"] for key in ("up_quark", "antiup_quark"))
    assert positive["charge"] == -negative["charge"] == 2
    assert positive["mass"] == negative["mass"]
    assert len(raw["disturbance_types"]) == 4
    assert len(raw["event_program"]["domains"]) == 3


def test_capacity_and_unknown_identity_fail_before_running():
    raw, _ = AUTHOR.prepare(SETTINGS["particle_ids"][:10])
    assert len(raw["event_program"]["addresses"]) == 30
    assert len(raw["disturbance_types"]) == 12
    for selection in ([], ["electron"] * 11, ["graviton"], ["invented_particle"]):
        with pytest.raises(ValueError):
            AUTHOR.prepare(selection)


def test_manifest_covers_established_particle_records_only():
    catalog = AUTHOR.load(ROOT / SETTINGS["catalog"])
    expected = {
        row["id"] for row in catalog["particle_entities"] if row["physical_status"] == "established"
    }
    assert set(SETTINGS["particle_ids"]) == expected

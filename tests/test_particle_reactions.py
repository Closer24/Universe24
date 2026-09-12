"""Known particle identity is data; reaction balances remain generic local contracts."""

import copy
import json
from pathlib import Path

import pytest

from event_universe.disturbance_api import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.particle_reactions import compile_particle_reaction, reaction_manifest

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "examples/known-entities/catalog.json"
REACTION = ROOT / "examples/known-entities/electron-positron-to-two-photons.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def owned(world):
    records = [record for cell in world.cells.values() for record in cell.records if record is not None]
    records += [packet.record for packets in world.links.values() for packet in packets if packet is not None]
    return sorted((record.type_index, world.record_values(record)) for record in records)


def test_known_particle_facts_and_reaction_totals_are_validated_from_catalog_data():
    manifest = reaction_manifest(read(CATALOG), read(REACTION))
    assert [item["entity"] for item in manifest["inputs"]] == ["electron", "positron"]
    assert [item["statistics_class"] for item in manifest["inputs"]] == ["fermion", "fermion"]
    assert [item["electric_charge_thirds"] for item in manifest["inputs"]] == [-3, 3]
    assert [item["entity"] for item in manifest["outputs"]] == ["photon", "photon"]
    assert [item["statistics_class"] for item in manifest["outputs"]] == ["boson", "boson"]
    assert all(item["antiparticle_id"] == "photon" for item in manifest["outputs"])
    assert all(item["rest_mass_relation"] == "massless" for item in manifest["outputs"])
    assert manifest["conservation"] == {
        "electric_charge_thirds": {"before": 0, "after": 0},
        "configured_energy": {"before": 10, "after": 10},
        "configured_momentum": {"before": [0, 0, 0], "after": [0, 0, 0]},
    }
    assert manifest["runtime_enforcement"] == ["charge", "energy", "momentum"]


def test_compiled_reaction_replaces_local_inputs_and_runtime_balances_stay_exact():
    initial, _ = compile_particle_reaction(read(CATALOG), read(REACTION))
    parsed = parse_initial_state(initial)
    world = Simulation(parsed)
    assert world.totals() == {"charge": (0,), "energy": (10,), "momentum": (0, 0, 0)}
    world.step()
    assert [index for index, _ in owned(world)] == [2, 3]
    for _ in range(2):
        world.step()
        assert world.totals() == {"charge": (0,), "energy": (10,), "momentum": (0, 0, 0)}
        assert world.source_totals() == {
            "charge": (0,),
            "energy": (0,),
            "momentum": (0, 0, 0),
        }
    values = [value for _, value in owned(world)]
    assert sorted(value["charge"] for value in values) == [(0,), (0,)]
    assert sorted(value["energy"] for value in values) == [(5,), (5,)]
    assert sorted(value["momentum"] for value in values) == [(-5, 0, 0), (5, 0, 0)]


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda raw: raw["outputs"].__setitem__(1, {"entity": "electron", "energy": 5, "momentum": [-5, 0, 0]}), "charge"),
        (lambda raw: raw["outputs"][0].__setitem__("energy", 4), "energy"),
        (lambda raw: raw["outputs"][0].__setitem__("momentum", [4, 0, 0]), "momentum"),
    ],
)
def test_authoring_rejects_nonconserving_reaction_before_runtime(mutation, message):
    raw = read(REACTION)
    mutation(raw)
    with pytest.raises(ValueError, match=message):
        compile_particle_reaction(read(CATALOG), raw)


def test_runtime_still_rejects_a_tampered_compiled_conversion():
    initial, _ = compile_particle_reaction(read(CATALOG), read(REACTION))
    energy_assignment = next(
        item
        for item in initial["interactions"][0]["assignments"]
        if item["side"] == "left" and item["field"] == "energy"
    )
    energy_assignment["expression"] = 4
    world = Simulation(parse_initial_state(initial))
    before = world.snapshot()
    with pytest.raises(ValueError, match="conservation|invariant"):
        world.step()
    assert world.snapshot() == before
    assert all(cell.pending is None for cell in world.cells.values())


def test_species_names_do_not_select_reaction_physics():
    catalog = read(CATALOG)
    reaction = read(REACTION)
    baseline, _ = compile_particle_reaction(catalog, reaction)
    renamed = copy.deepcopy(catalog)
    mapping = {"electron": "left arbitrary", "positron": "right arbitrary", "photon": "output arbitrary"}
    selected = {
        row["id"]: row
        for row in renamed["particle_entities"]
        if row["id"] in mapping
    }
    for old, new in mapping.items():
        selected[old]["id"] = new
    selected["electron"]["antiparticle_id"] = mapping["positron"]
    selected["positron"]["antiparticle_id"] = mapping["electron"]
    selected["photon"]["antiparticle_id"] = mapping["photon"]
    changed_reaction = copy.deepcopy(reaction)
    for side in ("inputs", "outputs"):
        for leg in changed_reaction[side]:
            leg["entity"] = mapping[leg["entity"]]
    compiled, manifest = compile_particle_reaction(renamed, changed_reaction)
    assert compiled == baseline
    assert [item["entity"] for item in manifest["inputs"]] == [mapping["electron"], mapping["positron"]]


def test_new_established_particle_can_be_added_as_catalog_data_without_engine_code():
    catalog = read(CATALOG)
    photon = next(row for row in catalog["particle_entities"] if row["id"] == "photon")
    added = copy.deepcopy(photon)
    added["id"] = "neutral_test_boson"
    added["label"] = "Neutral test boson"
    added["antiparticle_id"] = added["id"]
    catalog["particle_entities"].append(added)
    reaction = read(REACTION)
    for leg in reaction["outputs"]:
        leg["entity"] = added["id"]
    initial, manifest = compile_particle_reaction(catalog, reaction)
    parse_initial_state(initial)
    assert [item["entity"] for item in manifest["outputs"]] == [added["id"], added["id"]]
    assert all(item["statistics_class"] == "boson" for item in manifest["outputs"])


def test_malformed_particle_identity_and_product_count_fail_explicitly():
    catalog = read(CATALOG)
    positron = next(row for row in catalog["particle_entities"] if row["id"] == "positron")
    positron["twice_spin"] = 2
    with pytest.raises(ValueError, match="antiparticle charge or spin"):
        reaction_manifest(catalog, read(REACTION))
    reaction = read(REACTION)
    reaction["outputs"].append(copy.deepcopy(reaction["outputs"][0]))
    with pytest.raises(ValueError, match="exactly 2"):
        reaction_manifest(read(CATALOG), reaction)

"""Explicit catalog profiles share property rules and independently balanced inventories."""

import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.configuration_validation import validate_configuration
from event_universe.entities import compile_entities, main, validate_profiles
from event_universe.entity_catalog import validate_catalog
from event_universe.initialization import parse_initial_state

EXAMPLES = Path(__file__).resolve().parents[1] / "examples/known-entities"
ENTITIES = ("electron", "positron", "electron_neutrino")


def documents():
    return tuple(
        json.loads((EXAMPLES / name).read_text(encoding="utf-8"))
        for name in ("catalog.json", "property-coupling-probes.json")
    )


def compiled(entities=ENTITIES, *, profiles=None):
    catalog, default_profiles = documents()
    return compile_entities(
        catalog, entities, profiles=default_profiles if profiles is None else profiles
    )


def records(world):
    return {
        record["values"]["coupling"][0]: record["values"]
        for cell in world.snapshot()["cells"]
        for record in cell["disturbances"]
    }


def inventories(snapshot):
    energy = 0
    momentum = [0, 0, 0]
    for cell in snapshot["cells"]:
        for record in cell["disturbances"]:
            values = record["values"]
            energy += values["energy"][0]
            for axis, value in enumerate(values["momentum"]):
                momentum[axis] += value
    for node in snapshot["spatial_fields"]:
        for reservoir in ("r", "s"):
            energy += node["fields"][f"reservoir_{reservoir}_energy"]["value"][0]
            for axis, value in enumerate(node["fields"][f"reservoir_{reservoir}_momentum"]["value"]):
                momentum[axis] += value
    for packet in snapshot["spatial_transfers"]:
        for reservoir in ("r", "s"):
            energy += sum(row[0] for row in packet["fields"][f"reservoir_{reservoir}_energy"])
            for row in packet["fields"][f"reservoir_{reservoir}_momentum"]:
                for axis, value in enumerate(row):
                    momentum[axis] += value
    return energy, tuple(momentum)


def test_shared_profiles_and_fresh_compiled_input_pass_their_real_preflight_owners():
    catalog, profiles = documents()
    assert validate_profiles(catalog, profiles) == {"profiles": 3, "classical": 3, "quantum": 0}
    report = validate_configuration(json.dumps(profiles), catalog_source=json.dumps(catalog))
    assert report.valid, report.to_dict()
    raw = compiled()
    assert raw["model_id"] == "catalog-property-reservoir-transfer-v1"
    assert len(raw["spatial_interactions"]) == 2
    assert all(
        rule["requires"] == ["energy", "momentum", "coupling"] and "type" not in rule
        for rule in raw["spatial_interactions"]
    )
    assert validate_configuration(json.dumps(raw)).valid


def test_both_reservoirs_change_the_same_carried_inventory_and_neutral_control_stays_unchanged():
    raw = compiled()
    world = Simulation(parse_initial_state(raw))
    position = tuple(raw["seeds"][0]["position"])
    assert inventories(world.snapshot()) == (14, (0, 0, 0))
    before_neutral = deepcopy(records(world)[0])
    for tick in range(1, 5):
        world.step()
        assert inventories(world.snapshot()) == (14, (0, 0, 0))
        report = world.conservation_report()
        assert report["status"] == "passed"
        assert report["current"] == {"energy": 14, "momentum": (0, 0, 0)}
        assert all(row["balanced"] for row in world.spatial_accounting().values())
        carried = records(world)
        transfers = 2 * min(tick, 2)
        for selector in (-1, 1):
            assert carried[selector]["energy"] == (2 + transfers,)
            assert carried[selector]["momentum"] == (selector * transfers, 0, 0)
        assert carried[0] == before_neutral
        for reservoir in ("r", "s"):
            values = world.spatial_values(position)
            assert values[f"reservoir_{reservoir}_energy"]["value"] == (max(0, 4 - 2 * tick),)
            assert values[f"reservoir_{reservoir}_momentum"]["value"] == (0, 0, 0)


def test_different_catalog_identities_with_equal_properties_receive_equal_transfers():
    _, profiles = documents()
    profiles["profiles"][0]["executable_profile"]["seed_values"]["coupling"] = 1
    raw = compiled(ENTITIES[:2], profiles=profiles)
    world = Simulation(parse_initial_state(raw))
    world.step()
    values = [record["values"] for cell in world.snapshot()["cells"] for record in cell["disturbances"]]
    assert len(values) == 2 and values[0] == values[1]
    assert values[0]["energy"] == (4,)
    assert values[0]["momentum"] == (2, 0, 0)
    assert inventories(world.snapshot()) == (12, (0, 0, 0))
    position = tuple(raw["seeds"][0]["position"])
    for reservoir in ("r", "s"):
        assert world.spatial_values(position)[f"reservoir_{reservoir}_momentum"]["value"] == (-2, 0, 0)


def test_labels_cannot_change_property_response_and_compilation_does_not_alias_profiles():
    catalog, profiles = documents()
    before = deepcopy((catalog, profiles))
    original = compile_entities(catalog, ENTITIES, profiles=profiles)
    assert (catalog, profiles) == before
    original["conservation"]["spatial"]["energy"]["args"][0]["field"] = "modified_output"
    original["spatial_seeds"][0]["populations"][0] = 999
    assert (catalog, profiles) == before
    for index, row in enumerate(profiles["profiles"]):
        row["executable_profile"]["disturbance"]["name"] = f"arbitrary_carrier_{index}"
    for row in catalog["particle_entities"]:
        row["label"] = "Arbitrary descriptive label"
    changed = compile_entities(catalog, ENTITIES, profiles=profiles)
    world = Simulation(parse_initial_state(changed))
    world.step()
    assert records(world)[-1]["momentum"] == (-2, 0, 0)
    assert records(world)[1]["momentum"] == (2, 0, 0)
    assert records(world)[0]["momentum"] == (0, 0, 0)
    assert inventories(world.snapshot()) == (14, (0, 0, 0))


@pytest.mark.parametrize(
    "change",
    [
        "missing",
        "unknown",
        "null",
        "claim",
        "assumptions",
        "seeds",
        "field_conflict",
        "quantum",
        "empty",
    ],
)
def test_shared_context_rejects_incomplete_or_ambiguous_authoring(change):
    catalog, profiles = documents()
    shared = profiles["shared_classical"]
    representation = "classical"
    if change == "missing":
        del shared["conservation"]
    elif change == "unknown":
        shared["unexpected"] = True
    elif change == "null":
        profiles["shared_classical"] = None
    elif change == "claim":
        shared["claim_level"] = "established_physics"
    elif change == "assumptions":
        shared["assumptions"] = []
    elif change == "seeds":
        del shared["spatial_seed_values"]["reservoir_r_energy"]
    elif change == "field_conflict":
        shared["fields"][0]["name"] = "energy"
        shared["fields"][0]["signed"] = True
    elif change == "quantum":
        representation = "quantum"
    else:
        profiles["profiles"] = []
        with pytest.raises(ValueError, match="at least one classical profile"):
            validate_profiles(catalog, profiles)
        return
    with pytest.raises(ValueError):
        compile_entities(catalog, ENTITIES, profiles=profiles, representation=representation)


@pytest.mark.parametrize("target", ["energy", "momentum"])
def test_shared_audit_rejects_a_later_carrier_update_without_repairing_it(target):
    raw = compiled()
    expression = 0 if target == "energy" else {"op": "add", "args": [{"field": "momentum"}, [0, 0, 1]]}
    raw["disturbance_types"][0]["updates"] = [{"field": target, "expression": expression}]
    assert validate_configuration(json.dumps(raw)).valid
    world = Simulation(parse_initial_state(raw))
    with pytest.raises(ValueError, match="conservation"):
        world.step()
    assert world.faulted
    assert world.conservation_report()["status"] == "failed"
    # The checker reports the committed violation; it supplies no physical correction.
    if target == "energy":
        assert records(world)[-1]["energy"] == (0,)
        assert inventories(world.snapshot()) == (10, (0, 0, 0))
    else:
        assert records(world)[-1]["momentum"] == (-2, 0, 1)
        assert inventories(world.snapshot()) == (14, (0, 0, 1))


def test_cli_compiles_explicit_property_profiles_and_preserves_existing_output(tmp_path, monkeypatch):
    output = tmp_path / "property-probe.json"
    arguments = [
        "entities",
        "--catalog",
        str(EXAMPLES / "catalog.json"),
        "--profiles",
        str(EXAMPLES / "property-coupling-probes.json"),
        "--output-init",
        str(output),
    ]
    for identity in ENTITIES:
        arguments.extend(["--entity", identity])
    monkeypatch.setattr(sys, "argv", arguments)
    main()
    written = output.read_bytes()
    assert json.loads(written) == compiled()
    assert validate_configuration(written).valid
    with pytest.raises(FileExistsError):
        main()
    assert output.read_bytes() == written


def test_shared_compilation_never_reads_an_implicit_configuration(monkeypatch):
    catalog, profiles = documents()

    def forbidden_read(*args, **kwargs):
        raise AssertionError("The supplied profile document must be self-contained")

    monkeypatch.setattr(Path, "read_text", forbidden_read)
    monkeypatch.setattr(Path, "read_bytes", forbidden_read)
    raw = compile_entities(catalog, ENTITIES, profiles=profiles)
    assert raw["conservation"] == profiles["shared_classical"]["conservation"]


@pytest.mark.parametrize("runtime_key", ["shared_classical", "spatial_interactions", "conservation"])
def test_physical_catalog_rejects_runtime_contracts_even_if_the_payload_is_empty(runtime_key):
    catalog, _ = documents()
    catalog["scope"][runtime_key] = {}
    with pytest.raises(ValueError, match="executable rules or formulas"):
        validate_catalog(catalog)


def test_out_of_range_selector_faults_without_spending_either_reservoir():
    _, profiles = documents()
    profiles["profiles"][0]["executable_profile"]["seed_values"]["coupling"] = 2
    world = Simulation(parse_initial_state(compiled(profiles=profiles)))
    before = records(world)
    with pytest.raises(ValueError, match="signed_unit_selector"):
        world.step()
    assert world.faulted
    assert records(world) == before
    assert inventories(world.snapshot()) == (14, (0, 0, 0))
    for reservoir in ("r", "s"):
        assert (
            sum(
                node["fields"][f"reservoir_{reservoir}_energy"]["value"][0]
                for node in world.snapshot()["spatial_fields"]
            )
            == 4
        )

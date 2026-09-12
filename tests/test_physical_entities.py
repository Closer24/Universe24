"""Independent acceptance for restricted entity configurations, not inferred physics."""

import json
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
PAIR = ROOT / "examples/known-entities/discrete-pair.json"
CHANNEL = ROOT / "examples/known-entities/field-channel.json"
CATALOG = ROOT / "examples/known-entities/catalog.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def bodies(world):
    snapshot = world.snapshot()
    return {
        record["type"]: (cell["position"], record["values"])
        for cell in snapshot["cells"]
        for record in cell["disturbances"]
    }


def rotate_components(expression, axis):
    if isinstance(expression, dict):
        if expression.get("op") == "component":
            expression["index"] = axis
        for child in expression.values():
            rotate_components(child, axis)
    elif isinstance(expression, list):
        for child in expression:
            rotate_components(child, axis)


def test_catalog_references_and_conjugate_attributes_match_the_examples():
    catalog = read(CATALOG)
    rows = catalog["field_entities"] + catalog["particle_entities"]
    entities = {row["id"]: row for row in rows}
    assert len(entities) == len(rows)
    for row in rows:
        assert row["sources"] and set(row["sources"]) <= catalog["sources"].keys()
        assert row["emergence_status"] == "not_established"
        assert row["missing_capabilities"]
    for source in catalog["sources"].values():
        assert source["title"] and source["url"].startswith("https://")
    particles = {row["id"]: row for row in catalog["particle_entities"]}
    for row in particles.values():
        partner = particles[row["antiparticle_id"]]
        assert partner["antiparticle_id"] == row["id"]
        assert partner["twice_spin"] == row["twice_spin"]
        assert partner["electric_charge_thirds"] == -row["electric_charge_thirds"]
        assert partner["rest_mass_relation"] == row["rest_mass_relation"]
        if row["conjugacy_status"] == "distinct_antiparticle":
            assert row["id"] != partner["id"]
            assert row["rest_mass_relation"] == "equal_positive_pair"
        if row["conjugacy_status"] == "dirac_majorana_unresolved":
            assert row["electric_charge_thirds"] == 0
            assert row["rest_mass_relation"] == "flavor_state_not_definite_mass"
    assert particles["neutron"]["antiparticle_id"] == "antineutron"
    assert particles["photon"]["antiparticle_id"] == "photon"
    examples = {row["path"]: row for row in catalog["examples"]}
    assert len(examples) == len(catalog["examples"])
    for path, example in examples.items():
        assert (ROOT / path).is_file()
        assert set(example["entity_ids"]) <= entities.keys()
    pair_entry = examples[PAIR.relative_to(ROOT).as_posix()]
    assert "annihilation" in pair_entry["not_claimed"]
    assert "maxwell_dynamics" in examples[CHANNEL.relative_to(ROOT).as_posix()]["not_claimed"]
    for kind in read(PAIR)["disturbance_types"]:
        entity = particles[pair_entry["type_entities"][kind["name"]]]
        assert kind["defaults"]["charge"] == entity["electric_charge_thirds"]
        assert kind["defaults"]["mass"] > 0


def test_new_candidates_change_state_only_by_copying_or_clearing_values():
    for path in (PAIR, CHANNEL):
        raw = read(path)
        parse_initial_state(raw)
        for rule in raw.get("interactions", []) + raw.get("field_rules", []):
            for assignment in rule["assignments"]:
                value = assignment["expression"]
                assert value in (0, [0, 0, 0]) or (
                    isinstance(value, dict)
                    and set(value) == {"field", "side"}
                    and value["field"] == assignment["field"]
                )
        for kind in raw["disturbance_types"]:
            assert not kind.get("updates")
            assert type(kind["transport"].get("rate", 1)) is int


@pytest.mark.parametrize(("size", "axis"), [(9, 0), (15, 1)])
def test_equal_mass_permutation_has_same_local_outcome_after_size_and_axis_change(size, axis):
    raw = read(PAIR)
    raw["shape"] = [size] * 3
    center = size // 2
    for index, (seed, kind) in enumerate(zip(raw["seeds"], raw["disturbance_types"], strict=True)):
        seed["position"] = [center] * 3
        seed["position"][axis] += -1 if index == 0 else 1
        kind["defaults"]["momentum"] = [0, 0, 0]
        kind["defaults"]["momentum"][axis] = 1 if index == 0 else -1
    rotate_components(raw["interactions"][0]["when"], axis)
    world = Simulation(parse_initial_state(raw))
    names = [kind["name"] for kind in raw["disturbance_types"]]
    for tick in range(1, 17):
        world.step()
        assert world.totals() == {"mass": (2,), "charge": (0,), "momentum": (0, 0, 0)}
        assert all(not any(value) for value in world.source_totals().values())
        current = bodies(world)
        assert len(current) == 2
        for index, name in enumerate(names):
            position, values = current[name]
            assert values["mass"] == (1,)
            assert values["charge"] == ((-3,) if index == 0 else (3,))
            expected = [0, 0, 0]
            expected[axis] = (1 if index == 0 else -1) * (1 if tick <= 4 else -1)
            assert values["momentum"] == tuple(expected)
            assert all(position[i] == center for i in range(3) if i != axis)
        # For these equal unit masses, this is twice the raw kinetic diagnostic.
        assert sum(v * v for _, values in current.values() for v in values["momentum"]) == 2
        if tick == 4:
            assert all(position == (center, center, center) for position, _ in current.values())
    assert current[names[0]][0][axis] == center - 3
    assert current[names[1]][0][axis] == center + 3


@pytest.mark.parametrize("case", ["outgoing", "rest", "unequal"])
def test_pair_guard_does_not_swap_outgoing_resting_or_unequal_mass_records(case):
    raw = read(PAIR)
    for seed in raw["seeds"]:
        seed["position"] = [4, 4, 4]
    if case == "outgoing":
        raw["disturbance_types"][0]["defaults"]["momentum"] = [-1, 0, 0]
        raw["disturbance_types"][1]["defaults"]["momentum"] = [1, 0, 0]
    elif case == "rest":
        for kind in raw["disturbance_types"]:
            kind["defaults"]["momentum"] = [0, 0, 0]
    else:
        raw["disturbance_types"][1]["defaults"]["mass"] = 2
    world = Simulation(parse_initial_state(raw))
    before = bodies(world)
    world.step()
    assert bodies(world) == before


def test_transverse_probe_moves_once_per_link_without_duplicate_field_ownership():
    raw = read(CHANNEL)
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    amplitudes = {"E": (0, 3, 0), "B": (0, 0, 3)}
    for tick in range(7):
        snapshot = world.snapshot()
        owned = []
        for node in snapshot["spatial_fields"]:
            for name, state in node["fields"].items():
                if any(state["value"]):
                    owned.append((name, state["value"]))
                    assert node["position"] == (2 + tick // 2, 4, 4)
        for packet in snapshot["spatial_transfers"]:
            assert tick % 2 == 1
            assert packet["port"] == 0
            assert packet["origin"] == (2 + tick // 2, 4, 4)
            assert packet["target"] == (3 + tick // 2, 4, 4)
            assert packet["arrival_tick"] == tick + 1
            for name, populations in packet["fields"].items():
                for vector in populations:
                    if any(vector):
                        owned.append((name, vector))
        assert sorted(owned) == sorted(amplitudes.items())
        # Only this isolated, copied pulse has this squared-amplitude diagnostic.
        assert sum(component * component for _, vector in owned for component in vector) == 18
        if tick % 2:
            assert len(snapshot["spatial_transfers"]) == 1
            assert not any(
                any(state["value"])
                for node in snapshot["spatial_fields"]
                for state in node["fields"].values()
            )
        else:
            assert not snapshot["spatial_transfers"]
        for name, balance in world.spatial_accounting().items():
            assert balance["current"] == amplitudes[name]
            assert balance["balanced"]
            assert all(
                balance[key] == (0, 0, 0) for key in ("sources", "reactions", "dissipated", "escaped")
            )
        if tick < 6:
            world.step()
    sent = [event for event in events if event["event"] == "spatial_sent"]
    assert len(sent) == 3
    assert all(event["arrival_tick"] - event["tick"] == 2 for event in sent)

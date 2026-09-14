"""Independent local outcome, generation and inventory acceptance."""

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path

import pytest

from event_universe.configuration_validation import validate_configuration
from event_universe.core.source_envelope_state import EnvelopeAmplitude
from event_universe.diagnostics.node_contract import node_state_violations
from event_universe.quantum import LocalInstrument
from event_universe.runner import run_initialization

from .test_localized_quantum_contact import configuration, step, world_for
from .test_quantum_event_network import matrix, probability

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/quantum/repeated_contacts.json"


def recurrent_configuration():
    raw = configuration()
    raw["boundary"] = "periodic"
    raw["model_id"] = "recurrent-local-outcome-probe-v1"
    raw["ticks"] = 18
    program = raw["event_program"]
    program["model"] = "recurrent-contact-fields-v1"
    program["max_generations"] = 6
    program["tickets"] = [9, 9, 0]
    domain = program["domains"][0]
    source = domain["source"]
    source["outcomes"] = [{"effect": "new_wave", "matrix": source.pop("preparation")}]
    capture = domain["capture"]
    capture.pop("instrument")
    capture["register_indices"] = [0, 1, 2]
    capture["outcomes"] = [
        {"effect": "null", "matrix": [[5, 0], [0, 0]]},
        {"effect": "localized", "matrix": [[0, 3], [0, 0]]},
        {"effect": "new_wave", "matrix": [[0, 0], [0, 4]]},
    ]
    raw["seeds"].append({"position": [2, 1, 1], "type": "contact_probe"})
    raw["spatial_fields"][0]["decay"]["residue"] = "dissipate"
    return raw


def test_repeated_local_results_create_distinct_origins_and_preserve_inventory():
    raw = recurrent_configuration()
    world, resolver = world_for(raw)
    with world:
        step(world, raw["ticks"])
        transfers = resolver.report()["contact_transfers"]
        assert [e["direction"] for e in transfers] == [
            "to_quantum",
            "new_wave",
            "new_wave",
            "to_localized",
        ]
        origins = [e["origin"] for e in transfers[:3]]
        assert len(set(origins)) == 3
        assert all(world.event_space.resolution(origin) is not None for origin in origins)
        assert len({e["address"] for e in transfers[1:]}) >= 2
        assert resolver.draws == 3
        assert resolver.report()["quantum_inventory"]["charge"] == (0,)
        assert all(not node_state_violations(node) for node in world._nodes.values())
        assert all(item["balanced"] for item in world.spatial_accounting().values())


def test_source_can_remain_local_without_refilling_its_emission_allowance():
    raw = recurrent_configuration()
    source = raw["event_program"]["domains"][0]["source"]
    source["outcomes"] = [{"effect": "localized", "matrix": [[1, 0], [0, 1]]}]
    raw["event_program"]["tickets"] = []
    world, resolver = world_for(raw)
    with world:
        step(world, 10)
        assert not resolver.space.waves.names
        assert resolver.draws == 0
        assert world.source_totals()["electric_signal"] == (-12,)


@pytest.mark.parametrize("effect", ["new_wave", "localized", "continue"])
def test_invalid_outcome_support_is_rejected_by_preflight(effect):
    raw = recurrent_configuration()
    raw["event_program"]["domains"][0]["capture"]["outcomes"] = [
        {"effect": "null", "matrix": [[1, 0], [0, 0]]},
        {"effect": effect, "matrix": [[0, 1], [0, 1]]},
    ]
    assert not validate_configuration(raw).valid


def test_generation_exhaustion_preserves_inventory_before_a_random_draw():
    raw = recurrent_configuration()
    raw["event_program"]["max_generations"] = 1
    world, resolver = world_for(deepcopy(raw))
    with world:
        step(world, 1)
        prior_draws = resolver.draws
        with pytest.raises(OverflowError, match="generation capacity"):
            for _ in range(5):
                world.step()
        assert resolver.draws == prior_draws
        assert world.totals()["charge"] == (-1,)
        assert world.totals()["mass"] == (1,)


def test_complete_capture_instrument_has_independent_exhaustive_ticket_weights():
    counts = Counter()
    for ticket in range(169):
        raw = recurrent_configuration()
        raw["event_program"]["tickets"] = [ticket]
        raw["event_program"]["domains"][0]["capture"]["outcomes"] = [
            {"effect": "null", "matrix": [[13, 0], [0, 0]]},
            {"effect": "localized", "matrix": [[0, 3], [0, 0]]},
            {"effect": "new_wave", "matrix": [[0, 0], [0, 4]]},
            {"effect": "continue", "matrix": [[0, 0], [0, 12]]},
        ]
        world, resolver = world_for(raw)
        with world:
            step(world, 1)
            original = resolver.space.waves.names["charge_mode"]
            step(world, 1)
            transfer = resolver.report()["contact_transfers"][-1]
            counts[transfer["effect"]] += 1
            assert resolver.draws == 1
            current = resolver.space.waves.names["charge_mode"]
            if transfer["effect"] == "continue":
                assert current == original and resolver.space.wave_relevant(original)
                assert resolver._source_banks[0][(2, 1, 1)].amplitude == EnvelopeAmplitude(1)
            elif transfer["effect"] == "new_wave":
                assert current != original and not resolver.space.wave_relevant(original)
                assert resolver._source_banks[1][(2, 1, 1)].amplitude == EnvelopeAmplitude(1)
            else:
                assert not resolver.space.wave_relevant(original)
    assert counts == {"localized": 9, "new_wave": 16, "continue": 144}


def test_source_lottery_uses_complete_instrument_without_an_extra_random_switch():
    counts = Counter()
    for ticket in range(25):
        raw = recurrent_configuration()
        raw["event_program"]["tickets"] = [ticket]
        raw["event_program"]["domains"][0]["source"]["outcomes"] = [
            {"effect": "localized", "matrix": [[3, 0], [0, 3]]},
            {"effect": "new_wave", "matrix": [[0, 4], [4, 0]]},
        ]
        world, resolver = world_for(raw)
        with world:
            step(world, 1)
            counts[resolver.report()["contact_transfers"][0]["effect"]] += 1
            assert resolver.draws == 1
    assert counts == {"localized": 9, "new_wave": 16}


def test_semantic_owner_rejects_terminal_null_even_when_local_mode_is_vacuum():
    world, resolver = world_for(recurrent_configuration())
    with world:
        step(world, 1)
        space = resolver.space
        origin = space.waves.names["charge_mode"]
        heads = space.heads
        count = len(world.event_space.events)
        with pytest.raises(ValueError, match="retain or retire"):
            space.prepare(
                world.event_space.next_id,
                0,
                LocalInstrument((matrix([[1, 0], [0, 0]]), matrix([[0, 1], [0, 0]]))),
                origins=(origin,),
                terminal_origins=(origin,),
                terminal_outcomes=(0,),
                null_outcome=0,
                contact_effects=("null", "localized"),
            )
        assert space.heads == heads and len(world.event_space.events) == count
        assert space.wave_relevant(origin) and probability(space.query(1)) == 1


def test_new_wave_origin_is_part_of_quantum_commit_and_repeated_read_cannot_resurrect():
    world, resolver = world_for(recurrent_configuration())
    with world:
        step(world, 2)
        space = resolver.space
        record = next(
            r for r in reversed(space.records) if r.decision.contact_effects[r.outcome] == "new_wave"
        )
        origin = space.waves.names["charge_mode"]
        assert world.event_space.event(origin).parents == (record.event_id,)
        count = len(world.event_space.events)
        assert space.activate_contact_result("charge_mode", record) == origin
        assert len(world.event_space.events) == count
        assert space.commit(record.decision) is record


def test_primary_runner_records_repeated_origins_without_loading_display(tmp_path):
    result = run_initialization(EXAMPLE, tmp_path / "output")
    report = json.loads((tmp_path / "output/run.json").read_text())
    assert report["display"] == "none"
    transfers = report["computation"]["resolver"]["contact_transfers"]
    assert [(t["tick"], t["generation"]) for t in transfers] == [
        (0, 1),
        (3, 2),
        (6, 2),
        (9, 3),
        (12, 3),
        (15, 3),
        (18, 3),
        (21, 4),
        (24, 4),
    ]
    assert [t["address"] for t in transfers if t["direction"] == "new_wave"] == [
        [2, 1, 1],
        [3, 1, 1],
        [2, 1, 1],
    ]
    assert report["accounting_balanced_at_every_completed_tick"]
    assert not list(tmp_path.rglob("*.html"))
    assert result is not None


def test_renamed_fields_and_vector_inventory_survive_every_recurrent_outcome():
    raw = json.loads(EXAMPLE.read_text())
    raw["fields"].append(
        {"name": "vector_stock", "components": 3, "units": "test", "signed": True, "conserved": True}
    )
    for kind in raw["disturbance_types"][:2]:
        kind["fields"].append("vector_stock")
        kind["defaults"]["vector_stock"] = [2, -3, 5]
    alternate = deepcopy(raw["disturbance_types"][1])
    alternate["name"] = "alternate_output"
    raw["disturbance_types"].append(alternate)
    emission = deepcopy(raw["emissions"][1])
    emission["type"] = "alternate_output"
    raw["emissions"].append(emission)
    raw["event_program"]["domains"][0]["capture"]["outcomes"][1]["output"] = {"type": "alternate_output"}
    replacements = {
        "charge": "inventory_a",
        "mass": "inventory_b",
        "electric_signal": "ordinary_c",
        "incoming_charge": "input_a",
        "localized_charge": "output_a",
        "charge_mode": "domain_a",
    }

    def renamed(value):
        if isinstance(value, dict):
            return {replacements.get(k, k): renamed(v) for k, v in value.items()}
        if isinstance(value, list):
            return [renamed(v) for v in value]
        return replacements.get(value, value) if isinstance(value, str) else value

    left, left_resolver = world_for(raw)
    right, right_resolver = world_for(renamed(raw))
    with left, right:
        for _ in range(raw["ticks"]):
            left.step()
            right.step()
            assert {replacements.get(k, k): v for k, v in left.totals().items()} == right.totals()
            assert right.totals()["vector_stock"] == (2, -3, 5)
        assert (
            renamed(left_resolver.report()["contact_transfers"])
            == right_resolver.report()["contact_transfers"]
        )
        assert right.source_totals()["ordinary_c"] == (-36,)
        assert right.totals()["ordinary_c"] == (0,)
        assert all(a["balanced"] for a in right.spatial_accounting().values())


def test_alternate_output_cannot_change_conserved_inventory_before_runtime():
    raw = recurrent_configuration()
    raw["event_program"]["domains"][0]["capture"]["outcomes"][1]["output"] = {
        "type": "localized_charge",
        "values": {"charge": -2},
    }
    assert not validate_configuration(raw).valid

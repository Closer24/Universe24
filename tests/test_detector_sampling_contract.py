"""Actual Detector ownership is required by the canonical sampling contract."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.configuration_validation import validate_configuration
from event_universe.core.event_space import CausalEventSpace
from event_universe.fields.spatial_plan import SpatialLaw
from event_universe.initialization import parse_initial_state
from event_universe.integration.event_program import parse_event_program
from event_universe.integration.event_runtime import NativeEventResolver
from event_universe.runner import run_initialization

from .test_kerengonen import lottery_document, two_lamps

ROOT = Path(__file__).resolve().parents[1]


def ordinary_lottery():
    raw = lottery_document(8, 1, 1, seed=7)
    raw.pop("sampling_profile", None)
    return raw


def test_canonical_ordinary_lottery_fails_before_a_draw(monkeypatch):
    def forbidden(*args):
        pytest.fail("a rejected ordinary profile consumed a ticket")

    monkeypatch.setattr("event_universe.fields.spatial_plan.next_ticket", forbidden)
    with pytest.raises(ValueError, match="actual external Detector"):
        parse_initial_state(ordinary_lottery())
    report = validate_configuration(json.dumps(ordinary_lottery()))
    assert not report.valid
    assert "actual external Detector" in report.issues[0].message


@pytest.mark.parametrize("name", ["native_quantum", "wave_origins", "localized_charge"])
def test_ordinary_quantum_instruments_cannot_authorize_themselves(name):
    raw = json.loads((ROOT / "examples/quantum" / f"{name}.json").read_text())
    raw.pop("sampling_profile", None)
    with pytest.raises(ValueError, match="actual external Detector"):
        parse_initial_state(raw)


def test_local_semantic_owner_rejects_unbound_lottery_directly():
    initial = parse_initial_state(two_lamps(8, 1, absorber=1))
    fields = (replace(initial.spatial_fields[0], capture="lottery"),)
    with pytest.raises(ValueError, match="actual external Detector"):
        replace(initial, spatial_fields=fields)
    with pytest.raises(ValueError, match="actual external Detector"):
        SpatialLaw(initial.fields, fields, initial.emissions, initial.operation_costs)


def test_diagnostic_observer_or_entity_name_does_not_grant_draw_authority():
    raw = ordinary_lottery()
    raw["model_id"] = "actual external Detector"
    raw["disturbance_types"][2]["name"] = "Detector"
    for rule in raw["spatial_couplings"]:
        rule["type"] = "Detector"
    for seed in raw["seeds"]:
        if seed["type"] == "body":
            seed["type"] = "Detector"
    raw["observer"] = {"position": [8, 7, 7], "max_receipts": 10}
    with pytest.raises(ValueError, match="actual external Detector"):
        parse_initial_state(raw)


def test_deterministic_quantum_preparation_needs_no_sampling_exception(tmp_path):
    raw = json.loads((ROOT / "examples/quantum/native_quantum.json").read_text())
    raw.pop("sampling_profile", None)
    raw["event_program"]["bindings"] = []
    initial = parse_initial_state(raw)
    assert initial.sampling_profile == "detector-only-v1"
    source = tmp_path / "input.json"
    source.write_text(json.dumps(raw))
    run_initialization(source, tmp_path / "run", visualize=True)
    meta = json.loads((tmp_path / "run/run.json").read_text())
    assert meta["computation"]["resolver"]["random_draws"] == 0
    assert meta["sampling_profile"] == "detector-only-v1"
    assert (tmp_path / "run/run.html").exists()


@pytest.mark.parametrize("profile", ["Detector", "detector-only", "", True, None, 1])
def test_unknown_profile_cannot_disable_the_gate(profile):
    raw = ordinary_lottery()
    raw["sampling_profile"] = profile
    with pytest.raises(ValueError, match="sampling_profile"):
        parse_initial_state(raw)


def test_bond_registry_is_not_an_external_detector():
    raw = two_lamps(8, 1, absorber=1)
    raw["spatial_fields"][0]["bond"] = {"seed": 7}
    with pytest.raises(ValueError, match="actual external Detector"):
        parse_initial_state(raw)


def test_direct_native_resolver_rejects_unbound_program_before_sampling():
    raw = json.loads((ROOT / "examples/quantum/native_quantum.json").read_text())
    raw["sampling_profile"] = "historical-autonomous-v1"
    historical = parse_initial_state(raw)
    program = parse_event_program(historical)
    canonical = replace(historical, sampling_profile="detector-only-v1")
    events = CausalEventSpace(program.capacity, shape=canonical.shape)
    with pytest.raises(ValueError, match="actual external Detector"):
        NativeEventResolver(canonical, program, events)
    with pytest.raises(ValueError, match="actual external Detector"):
        Simulation(canonical)
    assert events.next_id == 0


def test_historical_lottery_retains_counterexample_and_marks_its_profile(tmp_path, monkeypatch):
    from event_universe.fields import spatial_plan

    calls = []
    original = spatial_plan.next_ticket

    def counted(state, salt):
        calls.append((state, salt))
        return original(state, salt)

    monkeypatch.setattr(spatial_plan, "next_ticket", counted)
    raw = ordinary_lottery()
    raw["sampling_profile"] = "historical-autonomous-v1"
    report = validate_configuration(json.dumps(raw))
    assert report.valid and report.summary["sampling_profile"] == "historical-autonomous-v1"
    source = tmp_path / "input.json"
    source.write_text(json.dumps(raw))
    run_initialization(source, tmp_path / "run", visualize=True)
    meta = json.loads((tmp_path / "run/run.json").read_text())
    state = json.loads((tmp_path / "run/state.json").read_text())
    absorber = next(
        record for node in state["nodes"] for record in node["disturbances"] if record["type"] == "body"
    )
    # Historical evidence: seed 7 consumed 18 tickets and absorbed five quanta.
    assert len(calls) == 18 and absorber["values"]["quanta"] == [5]
    assert meta["sampling_profile"] == "historical-autonomous-v1"
    assert meta["status"] == "completed" and meta["completed_ticks"] == 12
    assert meta["accounting_balanced_at_every_completed_tick"]
    assert (tmp_path / "run/run.html").exists()


def test_direct_bond_owner_cannot_bypass_an_unbonded_definition():
    from event_universe.fields.bonds import BondRegistry

    initial = parse_initial_state(two_lamps(8, 1, absorber=1))
    with pytest.raises(ValueError, match="actual external Detector"):
        SpatialLaw(
            initial.fields,
            initial.spatial_fields,
            initial.emissions,
            initial.operation_costs,
            bonds=BondRegistry(7, 8),
        )
    with pytest.raises(ValueError, match="actual external Detector"):
        SpatialLaw(
            initial.fields,
            initial.spatial_fields,
            initial.emissions,
            initial.operation_costs,
            absorptions=(replace(initial.spatial_couplings[0], bond_setting=0),),
        )


@pytest.mark.parametrize("tickets", [None, (0,)])
def test_direct_native_ticket_sampling_requires_bound_detector_even_without_bindings(tickets):
    raw = json.loads((ROOT / "examples/quantum/native_quantum.json").read_text())
    raw.pop("sampling_profile", None)
    raw["event_program"]["bindings"] = []
    initial = parse_initial_state(raw)
    program = replace(parse_event_program(initial), tickets=tickets)
    events = CausalEventSpace(program.capacity, shape=initial.shape)
    resolver = NativeEventResolver(initial, program, events)
    before = events.next_id, resolver.rng.getstate()
    with pytest.raises(ValueError, match="actual external Detector"):
        resolver._sample(2)
    assert resolver.draws == 0
    assert (events.next_id, resolver.rng.getstate()) == before

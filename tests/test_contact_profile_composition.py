"""Distinct contact extensions retain their opt-in configuration boundaries."""

import json
from copy import deepcopy
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.integration.contact_program import FieldPhase
from event_universe.integration.event_program import parse_event_program
from examples.quantum.position_moment_response import configuration as moment_configuration

EXAMPLES = Path(__file__).resolve().parents[1] / "examples/quantum"


def _input(name):
    return json.loads((EXAMPLES / name).read_text())


def recurrent_configuration():
    return _input("repeated_contacts.json")


def _contacts(raw):
    program = parse_event_program(parse_initial_state(raw))
    assert program.contacts is not None
    return program.contacts


def test_one_shot_options_do_not_shift_the_generation_or_recurrent_parameters():
    raw = _input("causal_charge.json")
    raw["event_program"]["null_notices"] = True
    notices = _contacts(raw)
    assert notices.causal_sources and notices.null_notices
    assert notices.max_generations == 1 and not notices.recurrent
    raw["event_program"]["null_notices"] = False
    raw["event_program"]["domains"][0]["phases"][0] = [
        {
            "register_indices": [0],
            "field_phase": {"field": "electric_signal", "divisor": 1, "vacuum": 5, "unit": [3, 4]},
        }
    ]
    phase = _contacts(raw)
    assert phase.causal_sources and not phase.null_notices
    assert phase.max_generations == 1 and not phase.recurrent
    assert isinstance(phase.domains[0].phases[0][0][0], FieldPhase)


@pytest.mark.parametrize("explicit_default", [False, True])
def test_legacy_recurrent_generations_still_run_with_null_notices_disabled(explicit_default):
    raw = recurrent_configuration()
    if explicit_default:
        raw["event_program"]["null_notices"] = False
    contacts = _contacts(raw)
    assert contacts.causal_sources and contacts.recurrent and not contacts.null_notices
    assert contacts.max_generations == 6
    with Simulation(parse_initial_state(raw)) as world:
        for _ in range(raw["ticks"]):
            world.step()
            assert world.totals()["charge"] == (-1,)
        report = world.computation_report()["resolver"]
        assert [event["direction"] for event in report["contact_transfers"]] == [
            "to_quantum",
            "new_wave",
            "continued",
            "new_wave",
            "continued",
            "continued",
            "continued",
            "new_wave",
            "to_localized",
        ]
        assert report["null_notices"] is False


def test_recurrent_null_notices_are_rejected_before_a_world_is_constructed():
    raw = recurrent_configuration()
    raw["event_program"]["null_notices"] = True
    before = deepcopy(raw)
    with pytest.raises(ValueError, match="null notices are not supported with recurrent"):
        parse_initial_state(raw)
    assert raw == before


@pytest.mark.parametrize("maximum", [0, 4])
def test_recurrent_field_phases_require_a_separate_composition_contract(maximum):
    raw = recurrent_configuration()
    raw["event_program"]["domains"][0]["phases"][0] = [
        {
            "register_indices": [1],
            "field_phase": {
                "field": "electric_signal",
                "divisor": 1,
                "vacuum": 5,
                "unit": [3, 4],
                "max_exponent": maximum,
            },
        }
    ]
    with pytest.raises(ValueError, match="field phases are not supported with recurrent"):
        parse_initial_state(raw)


@pytest.mark.parametrize(("capture", "spread"), [("endpoint", 1), ("middle", 2)])
def test_localized_moment_inputs_keep_their_independent_capture_behavior(capture, spread):
    raw = moment_configuration(capture=capture, reservoir=False)
    contacts = _contacts(raw)
    assert not contacts.causal_sources and not contacts.recurrent and not contacts.null_notices
    assert contacts.max_generations == 1
    with Simulation(parse_initial_state(raw)) as world:
        for _ in range(4):
            world.step()
        localized = [
            world.record_values(record)
            for node in world.nodes.values()
            for record in node.records
            if record is not None
            and world.initial.disturbances[record.type_index].name == "localized_charge"
        ]
        assert len(localized) == 1
        assert localized[0]["coarse_momentum"] == (0, 0, 0)
        assert localized[0]["momentum_spread"] == (spread,)
        assert localized[0]["momentum_known"] == (0,)

"""Only a Node whose Detector bit is set may draw: every ordinary sampler is rejected."""

import json
from dataclasses import replace

import pytest

from event_universe.configuration_validation import validate_configuration
from event_universe.core.sampling_contract import (
    DETECTOR_ONLY,
    validate_sampling_profile,
    validate_spatial_sampling,
)
from event_universe.fields.spatial_plan import SpatialLaw
from event_universe.initialization import parse_initial_state

from .test_kerengonen import two_lamps


def ordinary_lottery():
    """The two-lamp world with the deleted lottery capture on its field."""
    raw = two_lamps(8, 1, absorber=1, ticks=12)
    raw["spatial_fields"][0]["kerengonen"].update({"capture": "lottery"})
    return raw


def test_the_only_sampling_profile_is_detector_only():
    validate_sampling_profile(DETECTOR_ONLY)
    assert parse_initial_state(two_lamps(8, 1, absorber=1)).sampling_profile == DETECTOR_ONLY
    with pytest.raises(ValueError, match="deleted on 2026-09-17"):
        validate_sampling_profile("historical-autonomous-v1")


@pytest.mark.parametrize(
    "profile", ["historical-autonomous-v1", "Detector", "detector-only", "", True, None, 1]
)
def test_no_profile_value_reopens_an_ordinary_draw(profile):
    raw = two_lamps(8, 1, absorber=1)
    raw["sampling_profile"] = profile
    with pytest.raises(ValueError, match="sampling_profile"):
        parse_initial_state(raw)
    report = validate_configuration(json.dumps(raw))
    assert not report.valid


def test_the_lottery_capture_is_rejected_before_any_draw(monkeypatch):
    def forbidden(*args):
        pytest.fail("a rejected lottery consumed a ticket")

    monkeypatch.setattr("event_universe.core.spatial_state.next_ticket", forbidden)
    with pytest.raises(ValueError, match="lottery capture was deleted"):
        parse_initial_state(ordinary_lottery())
    report = validate_configuration(json.dumps(ordinary_lottery()))
    assert not report.valid
    assert "lottery capture was deleted" in report.issues[0].message
    raw = ordinary_lottery()
    raw["spatial_fields"][0]["kerengonen"]["capture_seed"] = 7
    with pytest.raises(ValueError, match="unknown keys: capture_seed"):
        parse_initial_state(raw)
    raw = two_lamps(8, 1, absorber=1)
    raw["spatial_couplings"][0]["capture_salt"] = 3
    with pytest.raises(ValueError, match="unknown keys: capture_salt"):
        parse_initial_state(raw)


def test_direct_typed_construction_rejects_the_same_lottery():
    initial = parse_initial_state(two_lamps(8, 1, absorber=1))
    fields = (replace(initial.spatial_fields[0], capture="lottery"),)
    with pytest.raises(ValueError, match="lottery capture was deleted"):
        validate_spatial_sampling(DETECTOR_ONLY, fields)
    with pytest.raises(ValueError, match="lottery capture was deleted"):
        replace(initial, spatial_fields=fields)
    with pytest.raises(ValueError, match="lottery capture was deleted"):
        SpatialLaw(initial.fields, fields, initial.emissions, initial.operation_costs)
    with pytest.raises(ValueError, match="deleted on 2026-09-17"):
        SpatialLaw(
            initial.fields,
            initial.spatial_fields,
            initial.emissions,
            initial.operation_costs,
            sampling_profile="historical-autonomous-v1",
        )


def test_a_record_named_detector_or_an_observer_does_not_grant_draw_authority():
    raw = ordinary_lottery()
    raw["model_id"] = "actual external Detector"
    raw["disturbance_types"][2]["name"] = "Detector"
    for rule in raw["spatial_couplings"]:
        rule["type"] = "Detector"
    for seed in raw["seeds"]:
        if seed["type"] == "body":
            seed["type"] = "Detector"
    raw["observer"] = {"position": [8, 7, 7], "max_receipts": 10}
    with pytest.raises(ValueError, match="lottery capture was deleted"):
        parse_initial_state(raw)


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("spatial_fields", "bond", {"seed": 7}),
        ("spatial_fields", "claim", {"ticks": 3, "slots": 4}),
        ("emissions", "bond_field", "origin"),
        ("emissions", "train_field", "quanta"),
        ("spatial_couplings", "bond_setting", "quanta"),
        ("spatial_couplings", "claim", True),
    ],
)
def test_the_bond_registry_and_claim_gather_keys_are_unknown(section, key, value):
    raw = two_lamps(8, 1, absorber=1)
    raw[section][0][key] = value
    with pytest.raises(ValueError, match=f"unknown keys: {key}"):
        parse_initial_state(raw)
    report = validate_configuration(json.dumps(raw))
    assert not report.valid


def test_the_two_deterministic_captures_remain_and_draw_nothing(monkeypatch):
    def forbidden(*args):
        pytest.fail("a deterministic capture consumed a ticket")

    monkeypatch.setattr("event_universe.core.spatial_state.next_ticket", forbidden)
    for capture in ("share", "threshold"):
        raw = two_lamps(8, 1, absorber=1, ticks=4)
        raw["spatial_fields"][0]["kerengonen"]["capture"] = capture
        initial = parse_initial_state(raw)
        assert initial.spatial_fields[0].capture == capture
        assert initial.sampling_profile == DETECTOR_ONLY
        report = validate_configuration(json.dumps(raw))
        assert report.valid and report.summary["sampling_profile"] == DETECTOR_ONLY

"""Historical research inputs retain explicit sampling scope after integration."""

import importlib.util
import json
from pathlib import Path

import pytest

from event_universe.configuration_validation import validate_configuration
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]


def load_builder(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "panel,builder", [("4-bonded-pair", "bonded_pair"), ("8-lottery-detector", "lottery_detector")]
)
def test_autonomous_gallery_builder_and_saved_input_have_explicit_historical_scope(panel, builder):
    worlds = load_builder("examples/research/ray-gallery/worlds.py", "sampling_gallery")
    generated = getattr(worlds, builder)()
    saved = json.loads((ROOT / "examples/research/ray-gallery/configs" / f"{panel}.json").read_text())
    assert generated == saved
    report = validate_configuration(json.dumps(saved))
    assert report.valid and report.summary["sampling_profile"] == "historical-autonomous-v1"
    saved.pop("sampling_profile")
    with pytest.raises(ValueError, match="actual external Detector"):
        parse_initial_state(saved)


def test_bonded_research_builder_and_new_metadata_preserve_historical_identity():
    common = load_builder("examples/research/bell-postulate-22/common.py", "sampling_bell_research")
    raw = common.bonded_world(0, 0, 8, 3)
    report = validate_configuration(json.dumps(raw))
    assert report.valid and report.summary["sampling_profile"] == "historical-autonomous-v1"
    assert common.stamp()["sampling_profile"] == "historical-autonomous-v1"
    raw.pop("sampling_profile")
    with pytest.raises(ValueError, match="actual external Detector"):
        parse_initial_state(raw)


def test_deterministic_gallery_control_keeps_the_canonical_profile():
    worlds = load_builder("examples/research/ray-gallery/worlds.py", "sampling_gallery_control")
    control = json.loads(
        (ROOT / "examples/research/ray-gallery/configs/2-straight-rays.json").read_text()
    )
    assert "sampling_profile" not in worlds._base("control", 1)
    assert parse_initial_state(control).sampling_profile == "detector-only-v1"

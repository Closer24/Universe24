"""Recorded multi-contact acceptance without changing the physical profile."""

import importlib.util
import json
from collections import Counter
from pathlib import Path

from event_universe.configuration_validation import validate_configuration

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "examples/quantum/many_contacts.json"
SPEC = importlib.util.spec_from_file_location("many_contacts_experiment", INPUT.with_suffix(".py"))
EXPERIMENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPERIMENT)


def test_many_contacts_uses_thirty_modes_with_two_link_detector_separation():
    source = INPUT.read_bytes()
    assert validate_configuration(source).valid
    raw = json.loads(source)
    assert raw["boundary"] == "periodic"
    assert len(raw["event_program"]["addresses"]) == 30
    assert len(raw["event_program"]["domains"]) == 6
    for domain in EXPERIMENT.geometry(raw):
        for target in domain["targets"].values():
            assert sum(abs(a - b) for a, b in zip(target, domain["source"], strict=True)) == 2


def test_headless_repetition_preserves_inventory_and_records_one_capture_per_particle(tmp_path):
    output = tmp_path / "experiment"
    result = EXPERIMENT.run_experiment(INPUT, output, trials=1)
    assert result["trial_count"] == 1 and result["total_captures"] == 6
    assert result["counts"] == {"A": 3, "B": 2, "C": 1}
    trial = result["trials"][0]
    assert Counter(c["tick"] for c in trial["captures"]) == {3: 3, 5: 2, 7: 1}
    assert trial["charge"] == (-6,) and trial["mass"] == (24,)
    assert trial["final_totals"]["electric_signal"] == (0,)
    assert trial["source_totals"]["electric_signal"] == trial["dissipation_totals"]["electric_signal"]
    assert trial["ticks"] == 24 and trial["all_envelopes_retired"]
    assert trial["accounting_balanced"]
    primary = json.loads((output / "representative/run.json").read_text())
    assert primary["display"] == "none"
    assert not list(output.rglob("*.html"))
    assert not list(output.rglob("frames.json"))

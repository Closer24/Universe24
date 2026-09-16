"""Frozen source, causal reception and independent output-clock timing fixtures."""

import json
import runpy
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/mass_computation"
# Example CLI siblings are private authoring modules, not production imports.
# Restore import names afterward so another example can have its own configuration.
PRIVATE_NAMES = ("configuration", "observe")
PREVIOUS_MODULES = {name: sys.modules.pop(name, None) for name in PRIVATE_NAMES}
with patch.object(sys, "path", [str(EXAMPLE), *sys.path]):
    PROBE = runpy.run_path(str(EXAMPLE / "run_experiments.py"))
for module_name, previous_module in PREVIOUS_MODULES.items():
    if previous_module is None:
        sys.modules.pop(module_name, None)
    else:
        sys.modules[module_name] = previous_module


@pytest.mark.parametrize("name", tuple(PROBE["expectations"]()["cases"]))
def test_frozen_candidate_fixture_matches_independent_event_expectations(name, tmp_path):
    raw = PROBE["document"](name)
    initialization = tmp_path / f"{name}.json"
    initialization.write_text(json.dumps(raw) + "\n", encoding="utf-8")
    case = PROBE["run_case"](initialization, tmp_path / "run")
    result = PROBE["assess"](case, name)
    assert result["passed"], result
    assert (tmp_path / "run/run.html").is_file()


def test_six_face_check_rejects_serialized_outputs_and_double_counted_stock(tmp_path):
    """A negative observation control cannot pass the acceptance report silently."""
    initialization = tmp_path / "P6.json"
    initialization.write_text(json.dumps(PROBE["document"]("P6")) + "\n", encoding="utf-8")
    case = PROBE["run_case"](initialization, tmp_path / "run")
    assert PROBE["assess"](case, "P6")["passed"]
    event = next(
        event
        for event in case["events"]
        if event["event"] == "sent" and event["position"] == [2, 3, 3] and event["port"] == 4
    )
    event["tick"] += 2
    case["metadata"]["accounting_balanced_at_every_completed_tick"] = False
    result = PROBE["assess"](case, "P6")
    assert not result["passed"]
    assert not result["checks"]["independent_face_departures"]
    assert not result["checks"]["declared_token_accounting"]
    # This corrupts an in-memory observation only. Saved physical evidence stays intact.
    assert PROBE["read_recording"](tmp_path / "run/run.html")["metadata"]["status"] == "completed"

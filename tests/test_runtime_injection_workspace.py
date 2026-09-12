"""The local workspace edits scheduled generic disturbances without a second engine."""

import json
from pathlib import Path

from event_universe.ui import validate_source

ROOT = Path(__file__).resolve().parents[1]


def configured_source() -> str:
    raw = json.loads((ROOT / "examples/basic.json").read_text(encoding="utf-8"))
    raw["runtime_injections"] = [
        {
            "tick": 4,
            "position": [6, 7, 8],
            "type": "carrier",
            "values": {"mass": 9, "charge": -2, "velocity": [1, 0, -1]},
        }
    ]
    return json.dumps(raw)


def test_workspace_validation_reports_scheduled_injections() -> None:
    summary = validate_source(configured_source())
    assert summary["runtime_injections"] == 1
    assert summary["seeds"] == 3


def test_workspace_assets_offer_generic_drag_and_touch_timed_placement() -> None:
    page = (ROOT / "src/event_universe/ui_assets/index.html").read_text(encoding="utf-8")
    script = (ROOT / "src/event_universe/ui_assets/app.js").read_text(encoding="utf-8")
    styles = (ROOT / "src/event_universe/ui_assets/style.css").read_text(encoding="utf-8")

    assert 'data-tab="timeline"' in page
    assert "Timed placement" in page
    assert "runtime_injections" in script
    assert "draggable = true" in script
    assert 'addEventListener("dragstart"' in script
    assert 'addEventListener("drop"' in script
    assert 'addEventListener("click"' in script
    assert "placement-canvas" in styles
    assert "carrier" not in script

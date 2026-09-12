"""Self-contained playback of recorded generic state; never invent trajectories."""

import json
from importlib.resources import files
from pathlib import Path


def render_disturbances(
    frames: list[dict[str, object]], output: Path, metadata: dict[str, object]
) -> Path:
    if not frames:
        raise ValueError("playback requires at least one recorded frame")
    document = files("event_universe").joinpath("ui_assets", "playback.html").read_text("utf-8")
    data = json.dumps({"frames": frames, "metadata": metadata}).replace("<", "\\u003c")
    output.write_text(document.replace("__RECORDING__", data), encoding="utf-8")
    return output

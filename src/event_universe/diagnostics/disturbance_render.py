"""Self-contained playback of recorded generic state; never invent trajectories."""

from collections.abc import Sequence
from importlib.resources import files
from pathlib import Path

from event_universe.archive import write_json


def render_disturbances(
    frames: Sequence[dict[str, object]],
    output: Path,
    metadata: dict[str, object],
    *,
    observation: dict[str, object] | None = None,
) -> Path:
    if not frames:
        raise ValueError("playback requires at least one recorded frame")
    document = files("event_universe").joinpath("ui_assets", "playback.html").read_text("utf-8")
    recording: dict[str, object] = {"frames": frames, "metadata": metadata}
    if observation is not None:
        recording["observation"] = observation
    before, marker, after = document.partition("__RECORDING__")
    if not marker:
        raise ValueError("playback template has no recording placeholder")
    with output.open("w", encoding="utf-8") as stream:
        stream.write(before)
        write_json(stream, recording, escape_html=True)
        stream.write(after)
    return output

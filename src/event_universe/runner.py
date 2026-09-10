"""One application entry point: initial conditions -> simulation -> metadata + HTML."""

import argparse
import hashlib
import json
from dataclasses import asdict, replace
from pathlib import Path

from event_universe import __version__
from event_universe.diagnostics.frames import Frame, Slice, VolumeFrame, capture_frame, capture_volume
from event_universe.diagnostics.measurements import report, total_momentum
from event_universe.diagnostics.recorder import JsonlRecorder
from event_universe.diagnostics.render import render_run, render_volume
from event_universe.models.current_field import MODEL_ID
from event_universe.models.linked_field import MODEL_ID as LINKED_MODEL_ID
from event_universe.scenarios import Scenario, get_scenario


def source_fingerprint() -> str:
    """Content identity remains available in source archives and installed wheels."""
    root = Path(__file__).parent
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*.py")):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def run_scenario(
    scenario: Scenario, output: Path, *, frame_stride: int = 1, volume: bool = False
) -> Path:
    """Every application run writes event JSONL, metadata JSON and standalone HTML."""
    if type(frame_stride) is not int or frame_stride < 1:
        raise ValueError("frame_stride must be a positive integer")
    if type(scenario.ticks) is not int or scenario.ticks < 0:
        raise ValueError("ticks must be a non-negative integer")
    output.mkdir(parents=True, exist_ok=True)
    frames: list[Frame] = []
    volume_frames: list[VolumeFrame] = []
    failure: Exception | None = None
    with (output / "events.jsonl").open("w", encoding="utf-8") as stream:
        world = scenario.create(JsonlRecorder(stream))
        frames.append(capture_frame(world, scenario.view))
        if volume:
            volume_frames.append(capture_volume(world))
        initial_momentum = total_momentum(world)
        conserved = True
        try:
            for _ in range(scenario.ticks):
                world.step()
                conserved = conserved and total_momentum(world) == initial_momentum
                if world.tick % frame_stride == 0:
                    frames.append(capture_frame(world, scenario.view))
                    if volume:
                        volume_frames.append(capture_volume(world))
        except Exception as error:
            failure = error
        if frames[-1].tick != world.tick or failure is not None:
            frames.append(capture_frame(world, scenario.view))
            if volume:
                volume_frames.append(capture_volume(world))
    metadata: dict[str, object] = {
        "package_version": __version__,
        "source_sha256": source_fingerprint(),
        "model": MODEL_ID if scenario.links is None else LINKED_MODEL_ID,
        "scenario": asdict(scenario),
        "frame_stride": frame_stride,
        "display": "volume-3d" if volume else "plane-slice",
        "initial_total_momentum": initial_momentum,
        "momentum_equal_at_every_completed_tick": conserved,
        "status": "failed" if failure else "completed",
        "error": str(failure) if failure else None,
        "report": report(world) if failure is None else {"tick": world.tick, "faulted": world.faulted},
    }
    (output / "run.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    title = f"Event Universe — {scenario.name}"
    if volume:
        artifact = render_volume(volume_frames, output / "run.html", title=title, metadata=metadata)
    else:
        artifact = render_run(frames, scenario.view, output / "run.html", title=title, metadata=metadata)
    if failure is not None:
        raise failure
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the integer 3D simulator and save HTML diagnostics."
    )
    parser.add_argument(
        "--scenario", choices=("contact", "turning", "stationary", "links"), default="contact"
    )
    parser.add_argument("--ticks", type=int)
    parser.add_argument("--output", type=Path, default=Path("artifacts/run"))
    parser.add_argument("--frame-stride", type=int, default=1)
    parser.add_argument(
        "--view-3d", action="store_true", help="Show the full XYZ field and particle paths"
    )
    parser.add_argument("--plane", choices=("XY", "XZ", "YZ"))
    parser.add_argument("--slice", type=int, dest="coordinate")
    args = parser.parse_args()
    scenario = get_scenario(args.scenario)
    if args.ticks is not None:
        scenario = replace(scenario, ticks=args.ticks)
    if args.plane is not None or args.coordinate is not None:
        scenario = replace(
            scenario,
            view=Slice(
                args.plane or scenario.view.plane,
                scenario.view.coordinate if args.coordinate is None else args.coordinate,
            ),
        )
    print(
        run_scenario(
            scenario, args.output, frame_stride=args.frame_stride, volume=args.view_3d
        ).resolve()
    )

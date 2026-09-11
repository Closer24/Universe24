"""Explicit historical scenario runner; the default runner uses initialization files."""

import argparse
import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import TYPE_CHECKING

from event_universe import __version__
from event_universe.diagnostics.invariants import require_inertial_momentum
from event_universe.diagnostics.measurements import report, total_momentum
from event_universe.diagnostics.recorder import JsonlRecorder
from event_universe.models.collisions import LINKED_MODEL_ID as COLLISION_LINKED_MODEL_ID
from event_universe.models.collisions import MODEL_ID as COLLISION_MODEL_ID
from event_universe.models.current_field import MODEL_ID
from event_universe.models.linked_field import MODEL_ID as LINKED_MODEL_ID
from event_universe.runner import source_fingerprint
from event_universe.scenarios import Scenario, get_scenario

if TYPE_CHECKING:
    from event_universe.diagnostics.frames import Frame, VolumeFrame


def run_scenario(
    scenario: Scenario,
    output: Path,
    *,
    frame_stride: int = 1,
    volume: bool = True,
    visualize: bool = False,
) -> Path:
    """Write events and metadata; capture frames and return HTML only when requested."""
    if type(frame_stride) is not int or frame_stride < 1:
        raise ValueError("frame_stride must be a positive integer")
    if type(scenario.ticks) is not int or scenario.ticks < 0:
        raise ValueError("ticks must be a non-negative integer")
    if visualize:
        from event_universe.diagnostics.frames import capture_frame, capture_volume

    output.mkdir(parents=True, exist_ok=True)
    frames: list[Frame] = []
    volume_frames: list[VolumeFrame] = []
    failure: Exception | None = None
    with (output / "events.jsonl").open("w", encoding="utf-8") as stream:
        world = scenario.create(JsonlRecorder(stream))
        if visualize:
            if volume:
                volume_frames.append(capture_volume(world))
            else:
                frames.append(capture_frame(world, scenario.view))
        # The runner owns the run: no external seeds or later particle additions.
        # Field-bearing initial states are not evidence of isolation.
        isolated = (
            next(iter(world.particles.items()))
            if len(world.particles) == 1 and not any(any(cell) for cell in world.cells.values())
            else None
        )
        isolated_status = "not_applicable" if isolated is None else "passed"
        initial_momentum = total_momentum(world)
        conserved = True
        try:
            for _ in range(scenario.ticks):
                world.step()
                conserved = conserved and total_momentum(world) == initial_momentum
                if isolated is not None:
                    pid, initial_particle = isolated
                    isolated_status = "failed"
                    require_inertial_momentum(
                        initial_particle.momentum,
                        world.particles[pid].momentum,
                        pid=pid,
                        tick=world.tick,
                    )
                    isolated_status = "passed"
                if visualize and world.tick % frame_stride == 0:
                    if volume:
                        volume_frames.append(capture_volume(world))
                    else:
                        frames.append(capture_frame(world, scenario.view))
        except Exception as error:
            failure = error
        if visualize:
            last_tick = volume_frames[-1].tick if volume else frames[-1].tick
            if last_tick != world.tick or failure is not None:
                if volume:
                    volume_frames.append(capture_volume(world))
                else:
                    frames.append(capture_frame(world, scenario.view))
    metadata: dict[str, object] = {
        "package_version": __version__,
        "source_sha256": source_fingerprint(),
        "model": (
            (COLLISION_MODEL_ID if scenario.links is None else COLLISION_LINKED_MODEL_ID)
            if scenario.collisions or any(m != 1 for m in scenario.masses)
            else (MODEL_ID if scenario.links is None else LINKED_MODEL_ID)
        ),
        "scenario": asdict(scenario),
        "frame_stride": frame_stride,
        "display": ("volume-3d" if volume else "plane-slice") if visualize else "none",
        "initial_total_momentum": initial_momentum,
        "momentum_equal_at_every_completed_tick": conserved,
        "status": "failed" if failure else "completed",
        "isolated_momentum_check": isolated_status,
        "error": str(failure) if failure else None,
        "report": report(world) if failure is None else {"tick": world.tick, "faulted": world.faulted},
    }
    artifact = output / "run.json"
    artifact.write_text(json.dumps(metadata, indent=2, default=str) + "\n", encoding="utf-8")
    if visualize:
        from event_universe.diagnostics.render import render_run, render_volume

        title = f"Event Universe — {scenario.name}"
        if failure is not None:
            title = f"FAILED RUN — {title} — {failure}"
        if volume:
            artifact = render_volume(volume_frames, output / "run.html", title=title, metadata=metadata)
        else:
            artifact = render_run(
                frames, scenario.view, output / "run.html", title=title, metadata=metadata
            )
    if failure is not None:
        raise failure
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the integer 3D simulator; request visualization explicitly."
    )
    parser.add_argument(
        "--scenario",
        choices=(
            "contact",
            "turning",
            "stationary",
            "links",
            "collision",
            "collision-masses",
            "collision-links",
        ),
        default="contact",
    )
    parser.add_argument("--ticks", type=int)
    parser.add_argument("--output", type=Path, default=Path("artifacts/run"))
    parser.add_argument("--frame-stride", type=int, default=1)
    parser.add_argument("--visualize", action="store_true", help="Save HTML/GIF diagnostics")
    views = parser.add_mutually_exclusive_group()
    views.add_argument("--view-3d", dest="view_3d", action="store_true", help="Render full XYZ view")
    views.add_argument("--view-2d", dest="view_3d", action="store_false", help="Show a plane slice")
    parser.set_defaults(view_3d=None)
    parser.add_argument("--plane", choices=("XY", "XZ", "YZ"))
    parser.add_argument("--slice", type=int, dest="coordinate")
    args = parser.parse_args()
    scenario = get_scenario(args.scenario)
    if args.ticks is not None:
        scenario = replace(scenario, ticks=args.ticks)
    if args.plane is not None or args.coordinate is not None:
        scenario = replace(
            scenario,
            view=replace(
                scenario.view,
                plane=args.plane or scenario.view.plane,
                coordinate=scenario.view.coordinate if args.coordinate is None else args.coordinate,
            ),
        )
    print(
        run_scenario(
            scenario,
            args.output,
            frame_stride=args.frame_stride,
            volume=(
                args.view_3d
                if args.view_3d is not None
                else args.plane is None and args.coordinate is None
            ),
            visualize=(
                args.visualize
                or args.view_3d is not None
                or args.plane is not None
                or args.coordinate is not None
            ),
        ).resolve()
    )


if __name__ == "__main__":
    main()

"""Explicit historical scenario runner; the default runner uses initialization files."""

import argparse
import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import TYPE_CHECKING

from event_universe import __version__
from event_universe.diagnostics.invariants import require_inertial_momentum
from event_universe.diagnostics.measurements import ExactVector, report, total_momentum
from event_universe.diagnostics.recorder import JsonlRecorder
from event_universe.models.collisions import LINKED_MODEL_ID as COLLISION_LINKED_MODEL_ID
from event_universe.models.collisions import MODEL_ID as COLLISION_MODEL_ID
from event_universe.models.current_field import MODEL_ID
from event_universe.models.linked_field import MODEL_ID as LINKED_MODEL_ID
from event_universe.runner import source_fingerprint
from event_universe.scenarios import Scenario, get_scenario

if TYPE_CHECKING:
    from event_universe.diagnostics.frames import Frame, VolumeFrame
    from event_universe.diagnostics.live import LiveDisplay


def run_scenario(
    scenario: Scenario,
    output: Path,
    *,
    frame_stride: int = 1,
    volume: bool = True,
    visualize: bool = False,
    live: bool = False,
) -> Path:
    """Write events/metadata, with optional saved visualization and concurrent preview."""
    if type(frame_stride) is not int or frame_stride < 1:
        raise ValueError("frame_stride must be a positive integer")
    if type(scenario.ticks) is not int or scenario.ticks < 0:
        raise ValueError("ticks must be a non-negative integer")
    output.mkdir(parents=True, exist_ok=True)
    display = None
    if live:
        from event_universe.diagnostics.live import LiveDisplay

        display = LiveDisplay(
            output,
            title=f"Event Universe — {scenario.name}",
            total_ticks=scenario.ticks,
            view=scenario.view,
            volume=volume,
        )
    try:
        if display is not None:
            display.start()
        return _run_scenario(
            scenario,
            output,
            frame_stride=frame_stride,
            volume=volume,
            visualize=visualize or live,
            display=display,
        )
    except BaseException as error:
        if display is not None:
            display.fail(error)
        raise
    finally:
        if display is not None:
            display.close()


def _run_scenario(
    scenario: Scenario,
    output: Path,
    *,
    frame_stride: int,
    volume: bool,
    visualize: bool,
    display: LiveDisplay | None,
) -> Path:
    if visualize:
        from event_universe.diagnostics.frames import capture_frame, capture_volume

    frames: list[Frame] = []
    volume_frames: list[VolumeFrame] = []
    failure: Exception | None = None
    with (output / "events.jsonl").open("w", encoding="utf-8") as stream:
        world = scenario.create(JsonlRecorder(stream))
        if visualize:
            scenario.view.validate_shape((world.config.nx, world.config.ny, world.config.nz))

        def capture(momentum: ExactVector | None = None) -> None:
            frame: Frame | VolumeFrame
            if volume:
                frame = capture_volume(world, momentum=momentum)
                volume_frames.append(frame)
            else:
                frame = capture_frame(world, scenario.view, momentum=momentum)
                frames.append(frame)
            if display is not None:
                display.submit(frame)

        initial_momentum = total_momentum(world)
        current_momentum = initial_momentum
        if visualize:
            capture(current_momentum)
        # The runner owns the run: no external seeds or later particle additions.
        # Field-bearing initial states are not evidence of isolation.
        isolated = (
            next(iter(world.particles.items()))
            if len(world.particles) == 1 and not any(any(cell) for cell in world.cells.values())
            else None
        )
        isolated_status = "not_applicable" if isolated is None else "passed"
        conserved = True
        try:
            for _ in range(scenario.ticks):
                world.step()
                current_momentum = total_momentum(world)
                conserved = conserved and current_momentum == initial_momentum
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
                    capture(current_momentum)
        except Exception as error:
            failure = error
        if visualize:
            last_tick = volume_frames[-1].tick if volume else frames[-1].tick
            if last_tick != world.tick or failure is not None:
                # Failed steps can commit local changes without incrementing time.
                capture(None if failure is not None else current_momentum)
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
        try:
            if display is not None:
                display.stop_preview()
            if volume:
                if display is None:
                    artifact = render_volume(
                        volume_frames, output / "run.html", title=title, metadata=metadata
                    )
                else:
                    artifact = render_volume(
                        volume_frames,
                        output / "run.html",
                        title=title,
                        metadata=metadata,
                        on_frame=display.rendered,
                    )
            elif display is None:
                artifact = render_run(
                    frames, scenario.view, output / "run.html", title=title, metadata=metadata
                )
            else:
                artifact = render_run(
                    frames,
                    scenario.view,
                    output / "run.html",
                    title=title,
                    metadata=metadata,
                    on_frame=display.rendered,
                )
            if display is not None:
                if failure is not None:
                    display.fail(failure)
                display.finish(artifact)
        except Exception as error:
            if failure is not None:
                failure.add_note(f"Final diagnostic rendering also failed: {error}")
                raise failure from error
            raise
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
    preview = parser.add_mutually_exclusive_group()
    preview.add_argument("--live", action="store_true", help="Render a concurrent live preview")
    preview.add_argument(
        "--no-live", action="store_false", dest="live", help="Disable the optional live preview"
    )
    parser.set_defaults(live=False)
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
    if args.live:
        print((args.output / "live.html").resolve(), flush=True)
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
                or args.live
                or args.view_3d is not None
                or args.plane is not None
                or args.coordinate is not None
            ),
            live=args.live,
        ).resolve()
    )


if __name__ == "__main__":
    main()

"""Initialization file -> generic disturbances -> headless artifacts by default."""

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import TYPE_CHECKING, cast

from event_universe import __version__
from event_universe.core.disturbance_state import InitialState
from event_universe.core.local_execution import validate_execution_options
from event_universe.disturbance_api import Simulation
from event_universe.initialization import parse_initial_state, parse_json_document
from event_universe.observer_configuration import ObserverDefinition
from event_universe.retention import ArtifactLease, cleanup_expired, validate_output_path

if TYPE_CHECKING:
    from collections.abc import Callable
    from concurrent.futures import Executor

    from event_universe.core.event_resolution import Planner
    from event_universe.diagnostics.local_observer import LocalObserver


def source_fingerprint() -> str:
    root = Path(__file__).parent
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*.py")):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def run_initialization(
    initialization: Path,
    output: Path,
    *,
    ticks: int | None = None,
    visualize: bool = False,
    frame_stride: int = 1,
    observer: Path | None = None,
    workers: int = 1,
    parallel_threshold: int = 64,
    chunk_size: int = 32,
    executor_factory: Callable[[Planner], Executor] | None = None,
    execution_backend: str = "interpreters",
) -> Path:
    """Preserve input, events, final state, and conservation evidence."""
    validate_execution_options(workers, parallel_threshold, chunk_size)
    source = initialization.read_bytes()
    document = parse_json_document(source)
    initial = parse_initial_state(document)
    document = cast(dict[str, object], document)
    observer_definition = (
        ObserverDefinition.parse(document["observer"], initial.shape) if "observer" in document else None
    )
    if observer is not None:
        if observer_definition is not None:
            raise ValueError("define observer in initialization or --observer, not both")
        observer_definition = ObserverDefinition.load(observer, initial.shape)
    fingerprint = source_fingerprint()
    count = initial.ticks if ticks is None else ticks
    if type(count) is not int or count < 0 or type(frame_stride) is not int or frame_stride < 1:
        raise ValueError("ticks must be nonnegative and frame_stride positive")
    validate_output_path(output)
    if initialization.resolve().is_relative_to(output.resolve()):
        raise ValueError("the original initialization must be outside the output directory")
    if observer is not None and observer.resolve().is_relative_to(output.resolve()):
        raise ValueError("the original observer configuration must be outside the output directory")
    cleanup_expired(output.parent)
    if output.exists() and any(output.iterdir()):
        raise ValueError("use an empty output directory to preserve earlier run artifacts")
    output.mkdir(parents=True, exist_ok=True)
    with ArtifactLease(output.parent, [output.resolve()]):
        return _execute_run(
            initial,
            source,
            output,
            fingerprint,
            count,
            visualize,
            frame_stride,
            observer_definition,
            workers,
            parallel_threshold,
            chunk_size,
            executor_factory,
            execution_backend,
        )


def _execute_run(
    initial: InitialState,
    source: bytes,
    output: Path,
    fingerprint: str,
    count: int,
    visualize: bool,
    frame_stride: int,
    observer_definition: ObserverDefinition | None,
    workers: int,
    parallel_threshold: int,
    chunk_size: int,
    executor_factory: Callable[[Planner], Executor] | None,
    execution_backend: str,
) -> Path:
    (output / "initialization.json").write_bytes(source)
    frames: list[dict[str, object]] = []
    probe: LocalObserver | None = None
    if observer_definition is not None:
        from event_universe.diagnostics.local_observer import LocalObserver

        probe = LocalObserver(observer_definition)
        (output / "observer.json").write_text(
            json.dumps(
                {
                    "position": observer_definition.position,
                    "max_receipts": observer_definition.max_receipts,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    failure: Exception | None = None
    conservation = True
    accounting = True
    completed = 0
    started = time.perf_counter()
    with (output / "events.jsonl").open("w", encoding="utf-8") as stream:

        def record(event: dict[str, object]) -> None:
            stream.write(json.dumps(event) + "\n")
            if probe is not None:
                probe.receive(event)

        world = Simulation(
            initial,
            observer=record,
            workers=workers,
            parallel_threshold=parallel_threshold,
            chunk_size=chunk_size,
            executor_factory=executor_factory,
            execution_backend=execution_backend,
        )
        initial_totals = world.totals()
        if visualize:
            frames.append(world.snapshot())
        if probe is not None:
            probe.capture(world.tick)
        sampled_tick = world.tick
        try:
            for _ in range(count):
                world.step()
                totals, spatial_accounting = world.inventory_and_spatial_accounting()
                sources = world.source_totals()
                losses = world.dissipation_totals()
                escaped = world.escaped_totals()
                equal = all(
                    totals[name] == tuple(a + b for a, b in zip(values, sources[name], strict=True))
                    for name, values in initial_totals.items()
                )
                conservation = conservation and equal
                balanced = all(
                    tuple(
                        value + loss + out
                        for value, loss, out in zip(
                            totals[name],
                            losses[name],
                            escaped[name],
                            strict=True,
                        )
                    )
                    == tuple(a + b for a, b in zip(values, sources[name], strict=True))
                    for name, values in initial_totals.items()
                ) and all(item["balanced"] for item in spatial_accounting.values())
                accounting = accounting and balanced
                if not balanced:
                    raise ValueError(
                        "declared quantity conservation, dissipation or escape accounting failed"
                    )
                completed += 1
                if visualize and world.tick % frame_stride == 0:
                    frames.append(world.snapshot())
                if world.tick % frame_stride == 0:
                    sampled_tick = world.tick
                    if probe is not None:
                        probe.capture(world.tick)
        except Exception as error:
            failure = error
        finally:
            world.close()
        final = world.snapshot()
        if visualize and (frames[-1]["tick"] != world.tick or failure is not None):
            frames.append(final)
        if probe is not None and (sampled_tick != world.tick or failure is not None):
            probe.capture(world.tick)
    metadata: dict[str, object] = {
        "package_version": __version__,
        "source_sha256": fingerprint,
        "initialization_sha256": hashlib.sha256(source).hexdigest(),
        "model": initial.model_id,
        "schema_version": initial.schema_version,
        "boundary": initial.boundary,
        "elapsed_seconds": time.perf_counter() - started,
        "status": "failed" if failure else "completed",
        "error": str(failure) if failure else None,
        "requested_ticks": count,
        "completed_ticks": completed,
        "tick": world.tick,
        "display": "disturbances" if visualize else "none",
        "initial_totals": initial_totals,
        "final_totals": world.totals(),
        "source_totals": world.source_totals(),
        "conserved_at_every_completed_tick": conservation,
        "dissipation_totals": world.dissipation_totals(),
        "escaped_totals": world.escaped_totals(),
        "accounting_balanced_at_every_completed_tick": accounting,
        "fields": [field.name for field in initial.fields],
        "disturbance_types": [kind.name for kind in initial.disturbances],
        "shape": initial.shape,
        "link_ticks": initial.link_ticks,
        "computation": world.computation_report(),
        "execution": world.execution_report(),
    }
    if world.event_space is not None:
        from dataclasses import asdict

        with (output / "causal-events.jsonl").open("w", encoding="utf-8") as causal_stream:
            for entry in world.event_space.events:
                causal_stream.write(json.dumps(asdict(entry)) + "\n")
    if initial.spatial_fields:
        metadata.update(
            spatial_fields=[initial.fields[item.field].name for item in initial.spatial_fields],
            spatial_transport=(
                "configured-six-ports"
                if any(field.transport == "local" for field in initial.spatial_fields)
                else "outward-octants"
            ),
            emission_interval_ticks=initial.link_ticks,
            self_field_filter="unsupported",
            spatial_policy=(
                "finite-dissipative-v1"
                if initial.schema_version == 2
                else "configured-local-fields-v1"
                if any(field.transport == "local" for field in initial.spatial_fields)
                else "conservative-outward-v1"
            ),
            spatial_accounting=world.spatial_accounting(),
            spatial_background="immutable; excluded from decay",
        )
    if initial.spatial_couplings:
        metadata.update(
            spatial_couplings=[rule.name for rule in initial.spatial_couplings],
            spatial_response="local-exchange-or-quarter-turn",
            spatial_sampling="resident-before-emission",
        )
    (output / "state.json").write_text(json.dumps(final, indent=2) + "\n", encoding="utf-8")
    observation = None if probe is None else probe.recording()
    if observation is not None:
        metadata["observer"] = {
            "model": observation["model"],
            "position": observation["position"],
            "clock_kind": observation["clock_kind"],
            "receipt_count": len(probe.receipts) if probe is not None else 0,
        }
        (output / "observations.json").write_text(
            json.dumps(observation, indent=2) + "\n", encoding="utf-8"
        )
    path = output / "run.json"
    path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    if visualize:
        from event_universe.diagnostics.disturbance_render import render_disturbances

        path = render_disturbances(frames, output / "run.html", metadata, observation=observation)
    if failure is not None:
        raise failure
    return path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run generic disturbances from an initialization JSON file."
    )
    parser.add_argument(
        "--init", required=True, type=Path, help="Field, disturbance, law and initial-state file"
    )
    parser.add_argument("--output", type=Path, default=Path("artifacts/run"))
    parser.add_argument("--ticks", type=int, help="Override only the requested run duration")
    parser.add_argument("--visualize", action="store_true", help="Create an interactive HTML view")
    parser.add_argument("--frame-stride", type=int, default=1)
    parser.add_argument("--observer", type=Path, help="Local reception probe placement JSON")
    parser.add_argument("--workers", type=int, default=1, help="CPU workers within this simulation")
    parser.add_argument(
        "--parallel-threshold",
        type=int,
        default=64,
        help="Minimum eligible cells before dispatching parallel local proposals",
    )
    parser.add_argument("--chunk-size", type=int, default=32, help="Local proposals per worker job")
    args = parser.parse_args()
    try:
        artifact = run_initialization(
            args.init,
            args.output,
            ticks=args.ticks,
            visualize=args.visualize,
            frame_stride=args.frame_stride,
            observer=args.observer,
            workers=args.workers,
            parallel_threshold=args.parallel_threshold,
            chunk_size=args.chunk_size,
        )
    except (ValueError, OSError) as error:
        parser.exit(1, f"Run failed: {error}\n")
    print(artifact.resolve())

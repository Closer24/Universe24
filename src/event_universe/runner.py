"""Initialization file -> generic disturbances -> headless artifacts by default."""

import argparse
import hashlib
import json
import time
from pathlib import Path

from event_universe import __version__
from event_universe.core.disturbance_state import InitialState
from event_universe.disturbance_api import Simulation
from event_universe.initialization import parse_initial_json
from event_universe.retention import ArtifactLease, cleanup_expired, validate_output_path


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
) -> Path:
    """Preserve input, events, final state, and conservation evidence."""
    source = initialization.read_bytes()
    initial = parse_initial_json(source)
    fingerprint = source_fingerprint()
    count = initial.ticks if ticks is None else ticks
    if type(count) is not int or count < 0 or type(frame_stride) is not int or frame_stride < 1:
        raise ValueError("ticks must be nonnegative and frame_stride positive")
    validate_output_path(output)
    if initialization.resolve().is_relative_to(output.resolve()):
        raise ValueError("the original initialization must be outside the output directory")
    cleanup_expired(output.parent)
    if output.exists() and any(output.iterdir()):
        raise ValueError("use an empty output directory to preserve earlier run artifacts")
    output.mkdir(parents=True, exist_ok=True)
    with ArtifactLease(output.parent, [output.resolve()]):
        return _execute_run(initial, source, output, fingerprint, count, visualize, frame_stride)


def _execute_run(
    initial: InitialState,
    source: bytes,
    output: Path,
    fingerprint: str,
    count: int,
    visualize: bool,
    frame_stride: int,
) -> Path:
    (output / "initialization.json").write_bytes(source)
    frames: list[dict[str, object]] = []
    failure: Exception | None = None
    conservation = True
    accounting = True
    completed = 0
    started = time.perf_counter()
    with (output / "events.jsonl").open("w", encoding="utf-8") as stream:

        def record(event: dict[str, object]) -> None:
            stream.write(json.dumps(event) + "\n")

        world = Simulation(initial, observer=record)
        initial_totals = world.totals()
        if visualize:
            frames.append(world.snapshot())
        try:
            for _ in range(count):
                world.step()
                totals, sources = world.totals(), world.source_totals()
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
                ) and all(item["balanced"] for item in world.spatial_accounting().values())
                accounting = accounting and balanced
                if not balanced:
                    raise ValueError(
                        "declared quantity conservation, dissipation or escape accounting failed"
                    )
                completed += 1
                if visualize and world.tick % frame_stride == 0:
                    frames.append(world.snapshot())
        except Exception as error:
            failure = error
        final = world.snapshot()
        if visualize and (frames[-1]["tick"] != world.tick or failure is not None):
            frames.append(final)
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
    path = output / "run.json"
    path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    if visualize:
        from event_universe.diagnostics.disturbance_render import render_disturbances

        path = render_disturbances(frames, output / "run.html", metadata)
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
    args = parser.parse_args()
    try:
        artifact = run_initialization(
            args.init,
            args.output,
            ticks=args.ticks,
            visualize=args.visualize,
            frame_stride=args.frame_stride,
        )
    except (ValueError, OSError) as error:
        parser.exit(1, f"Run failed: {error}\n")
    print(artifact.resolve())

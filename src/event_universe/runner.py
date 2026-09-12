"""Initialization file -> generic disturbances -> headless artifacts by default."""

import argparse
import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, cast

from event_universe import __version__
from event_universe.core.disturbance_engine import EventSink
from event_universe.core.disturbance_state import InitialState
from event_universe.core.topology import validate_position
from event_universe.disturbance_api import Simulation
from event_universe.initialization import parse_initial_json, parse_json_document
from event_universe.observer_configuration import ObserverDefinition
from event_universe.retention import ArtifactLease, cleanup_expired, validate_output_path

if TYPE_CHECKING:
    from event_universe.diagnostics.local_observer import LocalObserver
    from event_universe.experiment import ExperimentPackage


@dataclass
class _Restart:
    """Attach the new diagnostic stream only after checkpoint validation succeeds."""

    sink: EventSink | None = None

    def record(self, event: dict[str, object]) -> None:
        if self.sink is not None:
            self.sink(event)


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
    checkpoint: Path | None = None,
) -> Path:
    """Preserve input, events, final state, and conservation evidence."""
    source = initialization.read_bytes()
    initial = parse_initial_json(source)
    return _run_input(
        initial,
        source,
        output,
        inputs=(initialization,),
        ticks=ticks,
        visualize=visualize,
        frame_stride=frame_stride,
        observer=observer,
        checkpoint=checkpoint,
    )


def run_experiment(
    experiment: Path,
    output: Path,
    *,
    ticks: int | None = None,
    visualize: bool | None = None,
    frame_stride: int | None = None,
    observer: Path | None = None,
    checkpoint: Path | None = None,
) -> Path:
    """Run a validated package and preserve every exact input beside its merged JSON."""
    from event_universe.experiment import load_experiment

    package = load_experiment(experiment)
    controls = package.run_controls
    return _run_input(
        package.initial,
        package.runtime_json,
        output,
        inputs=tuple(experiment.resolve().parent / item.path for item in package.sources),
        ticks=ticks,
        visualize=cast(bool, controls["visualize"]) if visualize is None else visualize,
        frame_stride=cast(int, controls["frame_stride"]) if frame_stride is None else frame_stride,
        observer=observer,
        checkpoint=checkpoint,
        package=package,
    )


def run_checkpoint(
    resume: Path,
    output: Path,
    *,
    ticks: int | None = None,
    visualize: bool = False,
    frame_stride: int = 1,
    observer: Path | None = None,
    checkpoint: Path | None = None,
) -> Path:
    """Continue exact saved state; ticks means additional steps, without replay."""
    from event_universe.checkpoint import load_checkpoint

    relay = _Restart()
    world = load_checkpoint(resume, observer=relay.record)
    source = world.initial.source_json
    if source is None:
        raise ValueError("checkpoint has no canonical initialization source")
    count = max(0, world.initial.ticks - world.tick) if ticks is None else ticks
    return _run_input(
        world.initial,
        source.encode("utf-8"),
        output,
        inputs=(resume,),
        ticks=count,
        visualize=visualize,
        frame_stride=frame_stride,
        observer=observer,
        checkpoint=checkpoint,
        restart=(world, relay),
        resumed_sha256=hashlib.sha256(resume.read_bytes()).hexdigest(),
    )


def _run_input(
    initial: InitialState,
    source: bytes,
    output: Path,
    *,
    inputs: tuple[Path, ...],
    ticks: int | None,
    visualize: bool,
    frame_stride: int,
    observer: Path | None,
    checkpoint: Path | None,
    package: ExperimentPackage | None = None,
    restart: tuple[Simulation, _Restart] | None = None,
    resumed_sha256: str | None = None,
) -> Path:
    document = cast(dict[str, object], parse_json_document(source))
    observer_definition = (
        ObserverDefinition.parse(document["observer"], initial.shape) if "observer" in document else None
    )
    if observer_definition is not None:
        validate_position(observer_definition.position, initial.shape, initial.topology)
    if observer is not None:
        if observer_definition is not None:
            raise ValueError("define observer in initialization or --observer, not both")
        observer_definition = ObserverDefinition.load(observer, initial.shape)
        validate_position(observer_definition.position, initial.shape, initial.topology)
    fingerprint = source_fingerprint()
    count = initial.ticks if ticks is None else ticks
    if type(count) is not int or count < 0 or type(frame_stride) is not int or frame_stride < 1:
        raise ValueError("ticks must be nonnegative and frame_stride positive")
    validate_output_path(output)
    if any(item.resolve().is_relative_to(output.resolve()) for item in inputs):
        raise ValueError("original input files must be outside the output directory")
    if observer is not None and observer.resolve().is_relative_to(output.resolve()):
        raise ValueError("the original observer configuration must be outside the output directory")
    if checkpoint is not None:
        protected = (*inputs, *((observer,) if observer is not None else ()))
        if checkpoint.resolve() in {item.resolve() for item in protected}:
            raise ValueError("checkpoint destination must not overwrite an input file")
        if (
            checkpoint.resolve().is_relative_to(output.resolve())
            and checkpoint.resolve() != (output / "checkpoint.json").resolve()
        ):
            raise ValueError("a checkpoint inside run output must be named checkpoint.json")
    cleanup_expired(output.parent)
    if output.exists() and any(output.iterdir()):
        raise ValueError("use an empty output directory to preserve earlier run artifacts")
    output.mkdir(parents=True, exist_ok=True)
    with ArtifactLease(output.parent, [output.resolve()]) as lease:
        return _execute_run(
            initial,
            source,
            output,
            fingerprint,
            count,
            visualize,
            frame_stride,
            observer_definition,
            checkpoint=checkpoint,
            lease=lease,
            package=package,
            restart=restart,
            resumed_sha256=resumed_sha256,
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
    *,
    checkpoint: Path | None,
    lease: ArtifactLease,
    package: ExperimentPackage | None,
    restart: tuple[Simulation, _Restart] | None,
    resumed_sha256: str | None,
) -> Path:
    (output / "initialization.json").write_bytes(source)
    if package is not None:
        for item in package.sources:
            destination = output / "experiment" / item.path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(item.content)
        (output / "experiment-provenance.json").write_bytes(package.provenance_json)
    frames: list[dict[str, object]] = []
    probe: LocalObserver | None = None
    if observer_definition is not None:
        from event_universe.diagnostics.local_observer import LocalObserver

        probe = LocalObserver(observer_definition, port_count=initial.topology.degree)
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

        if restart is None:
            world = Simulation(initial, observer=record)
            initial_totals = world.totals()
        else:
            world, relay = restart
            relay.sink = record
            # Compare against the original inventory, not the resumed inventory:
            # sources/losses/escapes in the checkpoint are cumulative from tick zero.
            initial_totals = Simulation(initial).totals()
        start_tick = world.tick
        if visualize:
            frames.append(world.snapshot())
        if probe is not None:
            probe.capture(world.tick)
        sampled_tick = world.tick
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
                if world.tick % frame_stride == 0:
                    sampled_tick = world.tick
                    if probe is not None:
                        probe.capture(world.tick)
        except Exception as error:
            failure = error
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
        "effective_run_controls": {
            "ticks": count,
            "visualize": visualize,
            "frame_stride": frame_stride,
        },
        "tick": world.tick,
        "start_tick": start_tick,
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
    if resumed_sha256 is not None:
        metadata["resumed_checkpoint_sha256"] = resumed_sha256
    if package is not None:
        metadata["experiment"] = package.provenance
    if checkpoint is not None and failure is None:
        from event_universe.checkpoint import save_checkpoint

        try:
            save_checkpoint(
                world,
                checkpoint,
                lease=lease if checkpoint.resolve().is_relative_to(output.resolve()) else None,
            )
            metadata["checkpoint_sha256"] = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
            metadata["checkpoint_tick"] = world.tick
        except (OSError, ValueError) as error:
            failure = error
            metadata.update(status="failed", error=str(error))
    if initial.topology.model_id == "configured-ports-v1":
        metadata["topology"] = {
            "model_id": initial.topology.model_id,
            "offsets": initial.topology.offsets,
            "site_modulus": initial.topology.site_modulus,
            "site_residues": initial.topology.site_residues,
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
                "configured-ports"
                if initial.topology.model_id == "configured-ports-v1"
                else "configured-six-ports"
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
    from event_universe.schemas import SCHEMA_NAMES, schema_document

    parser = argparse.ArgumentParser(
        description="Validate, run or resume a generic disturbance experiment."
    )
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--init", type=Path, help="Canonical runtime initialization JSON")
    inputs.add_argument("--experiment", type=Path, help="Reusable experiment package manifest")
    inputs.add_argument("--resume", type=Path, help="Full checkpoint; ticks are additional steps")
    inputs.add_argument(
        "--schema",
        nargs="?",
        const="runtime",
        choices=SCHEMA_NAMES,
        help="Print a packaged JSON Schema to standard output",
    )
    parser.add_argument("--validate", action="store_true", help="Validate input without advancing time")
    parser.add_argument("--output", type=Path, default=Path("artifacts/run"))
    parser.add_argument("--ticks", type=int, help="Override only the requested run duration")
    parser.add_argument(
        "--visualize",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Create an interactive HTML view (package default otherwise)",
    )
    parser.add_argument("--frame-stride", type=int)
    parser.add_argument("--observer", type=Path, help="Local reception probe placement JSON")
    parser.add_argument(
        "--checkpoint", type=Path, help="Save complete state at the final successful tick"
    )
    args = parser.parse_args()
    try:
        if args.schema is not None:
            print(json.dumps(schema_document(args.schema), indent=2))
            return
        if args.validate:
            if args.checkpoint is not None:
                raise ValueError("--validate does not write a checkpoint")
            if args.experiment is not None:
                from event_universe.experiment import load_experiment

                initial = load_experiment(args.experiment).initial
            elif args.resume is not None:
                from event_universe.checkpoint import load_checkpoint

                initial = load_checkpoint(args.resume).initial
            else:
                initial = parse_initial_json(args.init.read_bytes())
            if args.ticks is not None and args.ticks < 0:
                raise ValueError("ticks must be nonnegative")
            if args.frame_stride is not None and args.frame_stride < 1:
                raise ValueError("frame_stride must be positive")
            if args.observer is not None:
                from event_universe.diagnostics.local_observer import ObserverDefinition

                probe = ObserverDefinition.load(args.observer, initial.shape)
                validate_position(probe.position, initial.shape, initial.topology)
            print("Valid")
            return
        if args.experiment is not None:
            artifact = run_experiment(
                args.experiment,
                args.output,
                ticks=args.ticks,
                visualize=args.visualize,
                frame_stride=args.frame_stride,
                observer=args.observer,
                checkpoint=args.checkpoint,
            )
        else:
            run = run_checkpoint if args.resume is not None else run_initialization
            artifact = run(
                args.resume if args.resume is not None else args.init,
                args.output,
                ticks=args.ticks,
                visualize=args.visualize or False,
                frame_stride=1 if args.frame_stride is None else args.frame_stride,
                observer=args.observer,
                checkpoint=args.checkpoint,
            )
    except (ValueError, OSError) as error:
        parser.exit(1, f"Run failed: {error}\n")
    print(artifact.resolve())

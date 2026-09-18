"""Initialization file -> generic disturbances -> headless artifacts by default."""

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import TYPE_CHECKING

from event_universe import __version__
from event_universe.configuration_validation import (
    prepare_initialization,
    validate_observer_selection,
)
from event_universe.core.disturbance_state import InitialState
from event_universe.core.ray_event_audit import RAY_EVENT_AUDIT, audit_failure
from event_universe.core.spatial_state import (
    BIT_LAW,
    CLOCK_READINGS,
    DENSE_FIELD,
    DETECTOR_ABSORB,
    DETECTOR_MARK,
    DETECTOR_RETURN,
    EXTERNAL_BODY,
    FIELD_REMAINDER,
    INVERSE_SPLIT,
    LANES,
    LOOP_BINDING,
    NODE_IS_PORTS,
    NODE_MIXING,
    RAY_EVENT_STATE,
    RAY_LAYERS,
    RAY_MEETING,
    RAY_MOMENTUM_TURN,
    RAY_POLARIZATION_PROPERTY,
    RELEASED_FIELD,
    RETURN_FIELD,
    SHADOW_WAIT,
    WAIT_READS,
    WAVE_RAY_FAMILY,
    external_body_names,
    mixing_field_names,
    polarization_declared,
    ray_layer_names,
    shadow_family_names,
)
from event_universe.disturbance_api import Simulation
from event_universe.json_documents import parse_json_document
from event_universe.observer_configuration import ObserverDefinition
from event_universe.retention import ArtifactLease, cleanup_expired, validate_output_path
from event_universe.snapshot_writer import write_snapshot

if TYPE_CHECKING:
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
    node_workers: int = 1,
    dense_field: bool | None = None,
    standing_field: bool | int | None = None,
) -> Path:
    """Preserve input, events, final state, and conservation evidence.

    `dense_field` overrides the world's own `dense_field` key (dense-field-v1)
    when given, `standing_field` the world's own `standing_field` key
    (standing-field-v1: `True` looks for the layer's fixed point within the run's
    ticks, an integer within that many intervals); the saved `initialization.json`
    is the input as read, and the run record names the modes when they are on.
    """
    source = initialization.read_bytes()
    document = parse_json_document(source)
    if dense_field is not None and isinstance(document, dict):
        document = {**document, "dense_field": dense_field}
    if standing_field is not None and isinstance(document, dict):
        document = {**document, "standing_field": standing_field}
    validate_observer_selection(document, external=observer is not None)
    prepared = (
        prepare_initialization(document)
        if observer is None
        else prepare_initialization(
            document, observer_document=parse_json_document(observer.read_bytes())
        )
    )
    initial, observer_definition = prepared.initial, prepared.observer
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
            node_workers,
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
    node_workers: int,
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
    accounting = True
    completed = 0
    # The world ledger per completed tick (ray-event-audit-v1); the conservation
    # flag is true when every line of every completed tick balances.
    audit: list[dict[str, object]] = []
    # Whether the world declares a push (ray-momentum-turn-v2 under bit-law-v1):
    # a momentum table on a coupling or on a body; a push writes no event.
    turned = any(rule.momentum_table for rule in initial.ray_interactions) or any(
        any(body.signs) for body in initial.external_bodies
    )
    # The content of the things per completed tick (bit-law-v1, point 11), and
    # whether the things' own identity held at every completed tick (point 7),
    # and the momentum of every thing per completed tick (point 15).
    real_content: list[int] = []
    shadow_content: list[int] = []
    momentum: list[dict[str, list[int]]] = []
    # The computation per completed tick (clock-readings-v1, point 11): the sum
    # over the things of the phase steps they made that interval, content / K
    # each with the remainders carried; constant between absorptions.
    computation: list[int] = []
    steps_before = 0
    real_conserved = True
    started = time.perf_counter()
    with (output / "events.jsonl").open("w", encoding="utf-8") as stream:

        def record(event: dict[str, object]) -> None:
            stream.write(json.dumps(event) + "\n")
            if probe is not None:
                probe.receive(event)

        with Simulation(initial, observer=record, node_workers=node_workers) as world:
            initial_totals = world.totals()
            # The external bodies' positions per tick (external-body-v1), tick 0 first.
            trajectories: list[list[list[int]]] = [[] for _ in initial.external_bodies]
            for item in world.external_bodies():
                index = item["index"]
                assert isinstance(index, int)
                trajectories[index].append([world.tick, *item["position"]])  # type: ignore[misc]
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
                    absorbed = world.external_body_totals()
                    taken = world.detector_mark_totals()
                    returned = world.returned_totals()
                    spent = world.spent_totals()
                    ledger = world.audit()
                    audit.append(ledger)
                    real_conserved = real_conserved and bool(ledger.get("real_conserved", True))
                    real_content.append(world.real_content())
                    shadow_content.append(world.shadow_content())
                    momentum.append(
                        {str(thing): value for thing, value in world.thing_momentum().items()}
                    )
                    steps_after = world.phase_steps()
                    computation.append(steps_after - steps_before)
                    steps_before = steps_after
                    # The conservation line: initial + sources = current + dissipated
                    # + escaped + absorbed_by_bodies + absorbed_by_marks +
                    # returned + spent at every completed tick (bit-law-v1,
                    # clock-readings-v1), the sources holding the re-releases, the
                    # marks' line what their clicks absorbed and spent what the
                    # things' steps took off their momentum.
                    balanced = all(
                        tuple(
                            value + loss + out + sunk + clicked + home + stepped
                            for value, loss, out, sunk, clicked, home, stepped in zip(
                                totals[name],
                                losses[name],
                                escaped[name],
                                absorbed[name],
                                taken[name],
                                returned[name],
                                spent[name],
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
                    for item in world.external_bodies():
                        index = item["index"]
                        assert isinstance(index, int)
                        trajectories[index].append([world.tick, *item["position"]])  # type: ignore[misc]
                    if visualize and world.tick % frame_stride == 0:
                        frames.append(world.snapshot())
                    if world.tick % frame_stride == 0:
                        sampled_tick = world.tick
                        if probe is not None:
                            probe.capture(world.tick)
            except Exception as error:
                failure = error
            final_bodies = {item["index"]: item for item in world.external_bodies()}
            if visualize and (frames[-1]["tick"] != world.tick or failure is not None):
                frames.append(world.snapshot())
            if probe is not None and (sampled_tick != world.tick or failure is not None):
                probe.capture(world.tick)
            # The final snapshot, Node by Node from the engine and the dense
            # region's arrays (`snapshot_writer`): the same text as
            # `json.dumps(world.snapshot(), indent=2)` without every Node held at
            # once, the peak memory of a filled board's snapshot the arrays plus
            # one Node (the performance review of 2026-09-18, A5s Run 2's r = 20).
            with (output / "state.json").open("w", encoding="utf-8") as state_stream:
                write_snapshot(world, state_stream)
                state_stream.write("\n")
    metadata: dict[str, object] = {
        "package_version": __version__,
        "source_sha256": fingerprint,
        "initialization_sha256": hashlib.sha256(source).hexdigest(),
        "model": initial.model_id,
        "schema_version": initial.schema_version,
        "ray_state": RAY_EVENT_STATE,
        "detector_mark": DETECTOR_MARK,
        "detector_return": DETECTOR_RETURN,
        "detector_absorb": DETECTOR_ABSORB,
        "inverse_split": INVERSE_SPLIT,
        # The law of the bit (bit-law-v1, the model owner's decision of 2026-09-18):
        # the engine's only behaviour, so it is recorded in every record, with the
        # families whose things have shadows, the things' own identity, the
        # content of the things per completed tick and the shadows per thing.
        "bit_law": BIT_LAW,
        "shadow_families": shadow_family_names(initial),
        # The field given with the board (`initial_field`): the fill, the exact
        # integer transient of the split table (whole quanta per Node and Port,
        # the shares below one quantum parked at the Node), or the size of the
        # declared profile; booked as initial content.
        "initial_field": {
            initial.fields[initial.spatial_fields[index].field].name: (
                {"fill": entry.fill} if entry.fill else {"rays": len(entry.rays)}
            )
            for index, entry in sorted(initial.initial_field.items())
        },
        "real_conserved": real_conserved,
        "real_content": real_content,
        "shadow_content": shadow_content,
        "momentum": momentum,
        # A Node is its six Ports (node-is-ports-v1, Highlights 5.4 point 22): the
        # parked shadows, the resident thing of a mark and the source
        # that spends its content are the engine's only behaviour.
        "node_is_ports": NODE_IS_PORTS,
        # A Port is two lanes (lanes-v1, Highlights 5.4 point 25): one real ray
        # and one shadow per owner on every lane, the lane a condition on the step.
        "lanes": LANES,
        # The clock is the content (clock-readings-v1, feature 16b): K, the
        # computation per completed tick (point 11) and the momentum spent on
        # the things' steps (the settled rule (i)).
        "clock_readings": CLOCK_READINGS,
        "K": initial.clock,
        "N": initial.phase_steps,
        "wait_per_quantum": list(initial.wait_per_quantum),
        "computation_per_tick": computation,
        "spent_totals": world.spent_totals(),
        "shadows": [
            {"thing": owner, "rays": count[0], "amount": count[1]}
            for owner, count in world.shadow_counts().items()
        ],
        "wave_ray": WAVE_RAY_FAMILY,
        "ray_layers": RAY_LAYERS,
        "ray_layer_families": [
            list(layer)
            for layer in ray_layer_names(
                initial.fields, initial.spatial_fields, initial.ray_interactions
            )
        ],
        "ray_meeting": RAY_MEETING,
        "released_field": RELEASED_FIELD,
        "loop_binding": LOOP_BINDING,
        "external_body": EXTERNAL_BODY,
        "external_bodies": [
            declared | {"positions": trajectories[index], "final": final_bodies.get(index)}
            for index, declared in enumerate(external_body_names(initial))
        ],
        "external_body_totals": world.external_body_totals(),
        "external_body_momentum": world.external_body_momentum(),
        # The Detector marks after the run (node-is-ports-v1): each with the thing
        # resident at it, what it absorbed per bit and family with its momentum,
        # and the marks' lines.
        "detector_marks": world.detector_marks(),
        "detector_mark_totals": world.detector_mark_totals(),
        "detector_mark_momentum": world.detector_mark_momentum(),
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
        "local_conservation": world.conservation_report(),
        "source_totals": world.source_totals(),
        "conserved_at_every_completed_tick": audit_failure(audit) is None,
        "ray_event_audit": RAY_EVENT_AUDIT,
        "audit": audit,
        "dissipation_totals": world.dissipation_totals(),
        "localized_totals": world.localized_totals(),
        "escaped_totals": world.escaped_totals(),
        "returned_totals": world.returned_totals(),
        "accounting_balanced_at_every_completed_tick": accounting,
        "fields": [field.name for field in initial.fields],
        "disturbance_types": [kind.name for kind in initial.disturbances],
        "shape": initial.shape,
        "link_ticks": initial.link_ticks,
        "computation": world.computation_report(),
        "execution": world.execution_report(),
    }
    if turned:
        # A thing turns by momentum (ray-momentum-turn-v3): recorded when the world
        # declares a push, so the record of every other world is byte for byte the same.
        metadata["ray_momentum_turn"] = RAY_MOMENTUM_TURN
    if polarization_declared(initial):
        # Polarization (ray-polarization-v1): recorded only when the world declares
        # the property anywhere, so the record of every other world is unchanged.
        metadata["ray_polarization"] = RAY_POLARIZATION_PROPERTY
    if initial.dense_field:
        # The dense mode (dense-field-v1): recorded only when on, so the record of
        # every other world is byte for byte the same; a dense region writes no
        # per-Node events, its record being its totals per tick.
        metadata["dense_field"] = DENSE_FIELD
    standing = world.standing_field_report()
    if standing is not None:
        # The standing set (standing-field-v1): recorded only when the world
        # declares the mode: whether the layer was kept fixed to the end, the
        # interval at which it repeated, the residual of the last comparison,
        # the intervals it was kept fixed and the fallback, if a thing stepped.
        metadata["standing_field_max_iterations"] = initial.standing_field
        metadata.update(standing)
    mixing = mixing_field_names(initial.fields, initial.spatial_fields)
    if mixing:
        # The Node mixes the six (node-mixing-v1): recorded with the phase width N
        # of every family whose shadows spread, the mixing's one input, only when
        # a world has such a family, so the record of every other world is byte
        # for byte the same.
        metadata["node_mixing"] = NODE_MIXING
        # The return is a field (return-field-v1, feature 16d).
        metadata["return_field"] = RETURN_FIELD
        metadata["field_remainder"] = FIELD_REMAINDER
        metadata["mixing_fields"] = mixing
    if initial.shadow_wait is not None:
        # The shadow's wait (shadow-wait-v1), a declared option: recorded only
        # when a world declares it, so every other record is byte for byte the same.
        metadata["shadow_wait"] = SHADOW_WAIT
        metadata["shadow_wait_option"] = {
            "per_quantum": list(initial.shadow_wait),
            "reads": initial.shadow_wait_reads,
        }
    if initial.wait_reads == "amplitude":
        # The wait reads the amplitude (wait-reads-v1), a declared coupling
        # option: recorded only when declared, so every other record, the
        # default "amount" declared or not, is byte for byte the same.
        metadata["wait_reads"] = WAIT_READS
        metadata["wait_reads_option"] = initial.wait_reads
    if initial.spatial_fields:
        metadata.update(
            spatial_fields=[initial.fields[item.field].name for item in initial.spatial_fields],
            spatial_transport=(
                "straight-rays"
                if any(field.rays for field in initial.spatial_fields)
                else "configured-six-ports"
                if any(field.transport == "local" for field in initial.spatial_fields)
                else "outward-octants"
            ),
            emission_interval_ticks=initial.link_ticks,
            self_field_filter="unsupported",
            spatial_metric=(
                "euclidean-ray-pace-v1"
                if any(field.euclidean for field in initial.spatial_fields)
                else "links"
            ),
            spatial_policy=(
                (
                    "finite-localizing-v1"
                    if all(
                        field.decay is not None and field.decay.localizes
                        for field in initial.spatial_fields
                    )
                    else "finite-dissipative-v1"
                )
                if initial.schema_version == 2
                else "kerengonen-ray-field-v1"
                if any(field.kerengonen for field in initial.spatial_fields)
                else "isotropic-ray-field-v1"
                if any(field.rays for field in initial.spatial_fields)
                else "configured-local-fields-v1"
                if any(field.transport == "local" for field in initial.spatial_fields)
                else "conservative-outward-v1"
            ),
            spatial_accounting=world.spatial_accounting(),
            spatial_background="immutable; excluded from decay",
            spatial_decay_residue=[
                None if field.decay is None else field.decay.residue for field in initial.spatial_fields
            ],
        )
        if initial.spatial_computation_delay:
            metadata.update(
                spatial_computation_delay=True,
                local_clock="shared-field-carrier-cycle-v1",
                emission_interval_ticks=None,
                emission_schedule="once per completed local computation cycle",
            )
    if initial.spatial_couplings:
        metadata.update(
            spatial_couplings=[rule.name for rule in initial.spatial_couplings],
            spatial_response="local-exchange-or-quarter-turn",
            spatial_sampling="resident-before-emission",
        )
    if initial.field_phase_first:
        metadata.update(
            field_phase_first=True,
            spatial_sampling="after-field-phase-delivery",
            field_order="causal-front-first-v1",
            self_field_filter="field-phase-first-v1",
        )
    if initial.arrival_port_blind:
        metadata.update(
            arrival_port_blind=True,
            spatial_sampling="entry-port-blind-on-arrival",
            self_field_filter="arrival-port-blind-v1",
        )
    if initial.computation_field is not None:
        metadata.update(
            computation_field=initial.fields[initial.computation_field].name,
            local_delay=(
                "computation-field-load-v1"
                if initial.delay_direction is None
                else f"directional-departure-delay-{initial.delay_direction}-v1"
            ),
            least_delay_routing=initial.least_delay_routing,
        )
    if initial.spatial_fields:
        metadata.update(
            allocation_phase=initial.allocation_phase,
            spatial_allocation=(
                "node-phase-legacy"
                if initial.allocation_phase == "node"
                else f"carried-{initial.allocation_phase}-phase-v1"
            ),
        )
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
    parser.add_argument(
        "--node-workers",
        type=int,
        default=1,
        help="Isolated Python interpreters used for per-Node planning (1-64)",
    )
    parser.add_argument(
        "--dense-field",
        action="store_true",
        help="Cycle the board's pure-field Nodes as one vectorized step (dense-field-v1)",
    )
    parser.add_argument(
        "--standing-field",
        nargs="?",
        const=-1,
        type=int,
        metavar="N",
        help=(
            "Step the dense layer to its fixed point and keep it fixed (standing-field-v1); "
            "N the most intervals to look, the run's ticks by default"
        ),
    )
    args = parser.parse_args()
    standing: bool | int | None = None
    if args.standing_field is not None:
        standing = True if args.standing_field < 0 else args.standing_field
    try:
        artifact = run_initialization(
            args.init,
            args.output,
            ticks=args.ticks,
            visualize=args.visualize,
            frame_stride=args.frame_stride,
            observer=args.observer,
            node_workers=args.node_workers,
            dense_field=True if args.dense_field else None,
            standing_field=standing,
        )
    except (ValueError, OSError) as error:
        parser.exit(1, f"Run failed: {error}\n")
    print(artifact.resolve())

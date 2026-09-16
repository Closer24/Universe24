"""Record the configured candidate through Simulation and the canonical HTML view.

This harness does not add, correct or interpolate physical state. The detailed
sidecar is an external read-only audit; it does not stand in for a Detector.
"""

import argparse
import hashlib
import json
import time
from pathlib import Path

from evidence import capture

from event_universe import Simulation
from event_universe.configuration_validation import prepare_initialization
from event_universe.diagnostics.disturbance_render import render_disturbances
from event_universe.retention import ArtifactLease, cleanup_expired, validate_output_path
from event_universe.runner import source_fingerprint


def run_document(document, output):
    """Execute one validated initialization, retaining failures and all actual ticks."""
    initial = prepare_initialization(document).initial
    validate_output_path(output)
    cleanup_expired(output.parent)
    if output.exists() and any(output.iterdir()):
        raise ValueError("Use a fresh output directory to preserve previous evidence")
    output.mkdir(parents=True, exist_ok=True)
    source = (json.dumps(document, indent=2) + "\n").encode()
    fingerprint = source_fingerprint()
    started = time.perf_counter()
    events, frames = [], []
    error = None
    with ArtifactLease(output.parent, [output.resolve()]):
        (output / "initialization.json").write_bytes(source)
        with Simulation(initial, observer=events.append) as world:
            frames.append(capture(world))
            try:
                for _ in range(initial.ticks):
                    world.step()
                    frames.append(capture(world))
                    if not all(item["balanced"] for item in world.spatial_accounting().values()):
                        raise ValueError("Spatial inventory accounting failed")
                    latest = frames[-1]
                    for name, initial_values in frames[0]["totals"].items():
                        actual = tuple(
                            value + escaped + loss
                            for value, escaped, loss in zip(
                                latest["totals"][name],
                                latest["escaped_totals"][name],
                                latest["dissipation_totals"][name],
                                strict=True,
                            )
                        )
                        expected = tuple(
                            value + source_value
                            for value, source_value in zip(
                                initial_values, latest["source_totals"][name], strict=True
                            )
                        )
                        if actual != expected:
                            raise ValueError(f"Complete-owner accounting failed for {name}")
            except Exception as failure:
                error = failure
                frames.append(capture(world))
            metadata = {
                "model": initial.model_id,
                "source_sha256": fingerprint,
                "initialization_sha256": hashlib.sha256(source).hexdigest(),
                "status": "completed" if error is None else "failed",
                "error": None if error is None else str(error),
                "completed_ticks": world.tick,
                "requested_ticks": initial.ticks,
                "shape": initial.shape,
                "boundary": initial.boundary,
                "link_ticks": initial.link_ticks,
                "fields": [field.name for field in initial.fields],
                "disturbance_types": [kind.name for kind in initial.disturbances],
                "initial_totals": frames[0]["totals"],
                "final_totals": world.totals(),
                "escaped_totals": world.escaped_totals(),
                "source_totals": world.source_totals(),
                "dissipation_totals": world.dissipation_totals(),
                "spatial_accounting": world.spatial_accounting(),
                "local_conservation": world.conservation_report(),
                "computation": world.computation_report(),
                "execution": world.execution_report(),
                "elapsed_seconds": time.perf_counter() - started,
                "evidence_scope": "Finite residence and release; stable nucleus and atom not established",
                "display": "disturbances",
            }
        if source_fingerprint() != fingerprint:
            raise ValueError("The simulated source changed during execution")
        (output / "run.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        (output / "events.jsonl").write_text(
            "".join(json.dumps(event) + "\n" for event in events), encoding="utf-8"
        )
        (output / "ray-recording.json").write_text(
            json.dumps({**metadata, "frames": frames}, indent=2) + "\n", encoding="utf-8"
        )
        (output / "state.json").write_text(
            json.dumps(frames[-1]["snapshot"], indent=2) + "\n", encoding="utf-8"
        )
        render_disturbances([frame["snapshot"] for frame in frames], output / "run.html", metadata)
    if error is not None:
        raise error
    return output / "run.html"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("initialization", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(run_document(json.loads(args.initialization.read_text(encoding="utf-8")), args.output))


if __name__ == "__main__":
    main()

"""Reproduce the finite candidate and preserve ordinary headless run evidence."""

import argparse
import gc
import hashlib
import json
import platform
import time
import tracemalloc
from collections import Counter
from dataclasses import asdict
from pathlib import Path

from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import run_initialization, source_fingerprint

from . import closure, coupling, routing


def parallel_waves(side):
    return tuple(closure.Wave((x, y, 0), 1, (1, 0, 0)) for x in range(side) for y in range(side))


def measure_macro(side):
    """Trace Python allocation for compression; physical model costs stay separate."""
    raw = closure.stream_configuration(side, parallel_waves(side))
    gc.collect()
    tracemalloc.start()
    start = time.perf_counter_ns()
    macro = closure.compress_free(raw)
    elapsed = time.perf_counter_ns() - start
    gc.collect()
    retained, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "nodes": side * side,
        "initial_owners": side * side,
        "retained_bins": len(macro.bins),
        "retained_traced_bytes": retained,
        "peak_traced_bytes": peak,
        "compression_host_ns": elapsed,
        "scope": "Python allocations during parsing/compression; source input predates tracing; no RSS claim",
    }


def experiment_fingerprint():
    digest = hashlib.sha256()
    for file in sorted(Path(__file__).parent.glob("*.py")):
        digest.update(file.name.encode())
        digest.update(b"\0")
        digest.update(file.read_bytes())
    return digest.hexdigest()


def run(output):
    validate_output_path(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError("use an empty experiment output directory")
    output.mkdir(parents=True, exist_ok=True)
    with ArtifactLease(output.parent, [output.resolve()]):
        return _run(output)


def _run(output):
    source_before = source_fingerprint()
    experiments_before = experiment_fingerprint()
    inputs = {
        "momentum-route": routing.build_configuration(),
        "rest": routing.build_configuration((0, 0, 0)),
        "local-transfer": coupling.build_configuration(),
        "neutral-control": coupling.build_configuration(0),
        "opposite-coupling": coupling.build_configuration(-1),
        **{
            f"parallel-{side * side}": closure.stream_configuration(side, parallel_waves(side))
            for side in closure.BLOCK_SIDES
        },
    }
    input_directory = output / "inputs"
    input_directory.mkdir()
    runs = []
    for name, raw in inputs.items():
        initialization = input_directory / (name + ".json")
        initialization.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")
        # Share one retention registry with the report, using sibling runs.
        destination = output.parent / (output.name + "-" + name)
        run_initialization(initialization, destination)
        metadata = json.loads((destination / "run.json").read_text(encoding="utf-8"))
        if metadata["status"] != "completed" or metadata["completed_ticks"] != raw["ticks"]:
            raise AssertionError(f"candidate run failed: {name}: {metadata['error']}")
        if metadata["display"] != "none":
            raise AssertionError("ordinary candidate run unexpectedly rendered")
        if not metadata["accounting_balanced_at_every_completed_tick"]:
            raise AssertionError(f"candidate inventory accounting failed: {name}")
        if "conservation" in raw and metadata["local_conservation"]["status"] != "passed":
            raise AssertionError(f"candidate local energy/momentum audit failed: {name}")
        runs.append({"name": name, "directory": destination.name, "metadata": metadata})
    trace = routing.run_configuration(inputs["momentum-route"])
    encounter = closure.interaction_counterexample()
    encounter["initial_summary"] = asdict(encounter["initial_summary"])
    report = {
        "python": platform.python_version(),
        "source_sha256": source_before,
        "experiment_sha256": experiments_before,
        "runs": runs,
        "routing": {
            "sent_ports": [event.port for event in trace.events if event.event == "sent"],
            "counts": dict(Counter(event.port for event in trace.events if event.event == "sent")),
            "model_operations_cost": trace.model_operations_cost,
            "local_cycles_started": trace.local_cycles_started,
        },
        "field_transfer": coupling.run_configuration(inputs["local-transfer"]),
        "parallel_blocks": [
            closure.compare_free(side, parallel_waves(side), link_ticks=travel)
            for side in closure.BLOCK_SIDES
            for travel in (1, 2)
        ],
        "interaction_counterexample": encounter,
        "closure_search": closure.closure_search(),
        "invariant_mass_readout": {
            "units": "candidate c=1; no elementary mass derivation",
            "single": closure.invariant_mass_squared(3, (3, 0, 0)),
            "opposite_pair": closure.invariant_mass_squared(6, (0, 0, 0)),
        },
        "macro_memory": [measure_macro(side) for side in closure.BLOCK_SIDES],
        "limits": [
            "Additive energy and momentum are declared owned quantities, not a derived dispersion relation.",
            "The closed macro predicts one admitted isolated free block; it is not an interacting coarse backend.",
            "Direction/phase is minimal only among the three tested observable families and finite launch domain.",
            "Node storage and production source are unchanged; host traces and visited-world storage still grow.",
        ],
    }
    if source_fingerprint() != source_before or experiment_fingerprint() != experiments_before:
        raise RuntimeError("source changed during the experiment; rerun after edits finish")
    destination = output / "report.json"
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(destination), "runs": len(runs), "source_sha256": source_before}))
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("artifacts/disturbance-coarse-graining"))
    run(parser.parse_args().output)


if __name__ == "__main__":
    main()

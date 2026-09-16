"""Compare dense and sparse execution of one private 24-Register graph."""

import argparse
import hashlib
import json
import platform
import tracemalloc
from dataclasses import asdict
from pathlib import Path
from statistics import median
from time import perf_counter

from prepare import prepare

import event_universe
from event_universe.core.private_worklist import PrivateSimulation
from event_universe.diagnostics.disturbance_render import render_disturbances
from event_universe.diagnostics.private_render import frame
from event_universe.runner import source_fingerprint


def measure(document: dict, strategy: str, output: Path, *, memory: bool = False) -> dict:
    output.mkdir(parents=True, exist_ok=False)
    if memory:
        tracemalloc.start()
    started = perf_counter()
    wiring, seeds, ticks = prepare(document)
    world = PrivateSimulation(wiring, seeds, strategy=strategy)
    initialization_seconds = perf_counter() - started
    stepping_seconds = 0.0
    hashes, frames = [], []
    failure = None
    for tick in range(ticks + 1):
        hashes.append(hashlib.sha256(repr(world.canonical_state()).encode()).hexdigest())
        frames.append(frame(world))
        if tick < ticks:
            started = perf_counter()
            try:
                world.step()
            except Exception as error:
                failure = error
                frames.append(frame(world))
                break
            finally:
                stepping_seconds += perf_counter() - started
    traced_peak = tracemalloc.get_traced_memory()[1] if memory else None
    if memory:
        tracemalloc.stop()
    metadata = {
        "model": document["profile"],
        "shape": document["shape"],
        "boundary": "periodic",
        "link_ticks": 1,
        "status": "completed" if failure is None else "failed",
        "error": None if failure is None else str(failure),
        "strategy": strategy,
        "ticks": ticks,
        "python": platform.python_version(),
        "source_sha256": source_fingerprint(),
        "initialization_seconds": initialization_seconds,
        "stepping_seconds": stepping_seconds,
        "work": world.work_report(),
        "traced_python_peak_bytes": traced_peak,
        "memory_scope": "Separate instrumented pair; includes initialization, stepping and passive audit/frame capture; excludes HTML. Python allocations only.",
        "scope": "Private identity transport on an explicitly supplied test graph; no whole-Node mixer or species law.",
    }
    started = perf_counter()
    render_disturbances(frames, output / "run.html", metadata)
    metadata["render_seconds"] = perf_counter() - started
    (output / "events.jsonl").write_text(
        "".join(json.dumps(asdict(event)) + "\n" for event in world.events)
    )
    (output / "state_hashes.json").write_text(json.dumps(hashes) + "\n")
    (output / "run.json").write_text(json.dumps(metadata, indent=2) + "\n")
    if failure is not None:
        raise failure
    return {"metadata": metadata, "hashes": hashes}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    if not 1 <= args.repeats <= 7:
        parser.error("repeats must be between one and seven")
    if (
        Path(event_universe.__file__).resolve()
        != args.source.resolve() / "src/event_universe/__init__.py"
    ):
        parser.error("the imported engine must match --source; set PYTHONPATH explicitly")
    raw = args.input.read_bytes()
    document = json.loads(raw)
    before = source_fingerprint()
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "input.json").write_bytes(raw)
    samples = {"dense": [], "sparse": []}
    memory_samples = {}
    for repeat in range(args.repeats + 1):
        memory = repeat == args.repeats
        order = ("dense", "sparse") if repeat % 2 == 0 else ("sparse", "dense")
        pair = {
            strategy: measure(
                document,
                strategy,
                args.output / f"{'memory' if memory else repeat}-{strategy}",
                memory=memory,
            )
            for strategy in order
        }
        if pair["dense"]["hashes"] != pair["sparse"]["hashes"]:
            raise ValueError("private state, ownership, deadlines or events differ at a recorded tick")
        for strategy in order:
            if memory:
                memory_samples[strategy] = pair[strategy]["metadata"]
            else:
                samples[strategy].append(pair[strategy]["metadata"])
    if source_fingerprint() != before:
        raise ValueError("source changed during the comparison")
    report = {
        "profile": document["profile"],
        "per_tick_parity": True,
        "source_sha256": before,
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "samples": samples,
        "memory_samples": memory_samples,
        "median_step_seconds": {
            strategy: median(sample["stepping_seconds"] for sample in values)
            for strategy, values in samples.items()
        },
        "limits": "One host and one finite identity-transport graph. Timing excludes initialization and passive recording/export; separate tracemalloc runs are excluded from time medians. No interference, mass, coupling, detector or universal routing claim.",
    }
    (args.output / "comparison.json").write_text(json.dumps(report, indent=2) + "\n")
    print(
        json.dumps(
            {key: value for key, value in report.items() if key not in ("samples", "memory_samples")}
        )
    )


if __name__ == "__main__":
    main()

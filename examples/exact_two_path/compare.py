"""Compare one input on the ordinary Node and interim Port scheduling paths.

This is reusable execution verification, not execution of the proposed 24
internal Registers. Every explicit run produces the canonical recorded HTML.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
from statistics import median
from time import perf_counter

import event_universe
from event_universe import Simulation
from event_universe.core.disturbance_state import InitialState
from event_universe.diagnostics.disturbance_render import render_disturbances
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint


def measure(initial: InitialState, strategy: str, output: Path) -> dict:
    """Measure stepping separately from initialization and passive recording."""
    output.mkdir(parents=True, exist_ok=False)
    events, frames, hashes = [], [], []
    started = perf_counter()
    world = Simulation(initial, observer=events.append, execution_strategy=strategy)
    initialization_seconds = perf_counter() - started
    stepping_seconds = 0.0
    failure = None
    with world:
        for tick in range(initial.ticks + 1):
            frame = world.snapshot()
            frames.append(frame)
            audit = (
                frame,
                tuple(world.nodes.items()),
                tuple(world.links.items()),
                world.inventory_view(),
                world.computation_report(),
                tuple(events),
            )
            hashes.append(hashlib.sha256(repr(audit).encode()).hexdigest())
            if tick < initial.ticks:
                started = perf_counter()
                try:
                    world.step()
                except Exception as error:
                    failure = error
                    frames.append(world.snapshot())
                    break
                finally:
                    stepping_seconds += perf_counter() - started
        execution = world.execution_report()
    metadata = {
        "model": initial.model_id,
        "shape": initial.shape,
        "boundary": initial.boundary,
        "link_ticks": initial.link_ticks,
        "status": "completed" if failure is None else "failed",
        "error": None if failure is None else str(failure),
        "strategy": strategy,
        "scope": "interim six-Port scheduling; not 24 internal Register execution",
        "source_sha256": source_fingerprint(),
        "python": platform.python_version(),
        "ticks": initial.ticks,
        "fields": [field.name for field in initial.fields],
        "disturbance_types": [kind.name for kind in initial.disturbances],
        "initialization_seconds": initialization_seconds,
        "stepping_seconds": stepping_seconds,
        "execution": execution,
    }
    started = perf_counter()
    render_disturbances(frames, output / "run.html", metadata)
    metadata["render_seconds"] = perf_counter() - started
    (output / "events.jsonl").write_text("".join(json.dumps(event) + "\n" for event in events))
    (output / "state_hashes.json").write_text(json.dumps(hashes) + "\n")
    (output / "run.json").write_text(json.dumps(metadata, indent=2) + "\n")
    if failure is not None:
        raise failure
    return {"metadata": metadata, "hashes": hashes}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--initialization", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    if not 1 <= args.repeats <= 7:
        parser.error("repeats must be between 1 and 7")
    if (
        Path(event_universe.__file__).resolve()
        != args.source.resolve() / "src/event_universe/__init__.py"
    ):
        parser.error("the imported simulator does not match --source; set PYTHONPATH explicitly")
    raw = args.initialization.read_bytes()
    initial = parse_initial_state(json.loads(raw))
    before = source_fingerprint()
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "input.json").write_bytes(raw)
    samples = {"node": [], "port": []}
    for repeat in range(args.repeats):
        strategies = ("node", "port") if repeat % 2 == 0 else ("port", "node")
        pair = {
            strategy: measure(initial, strategy, args.output / f"{repeat}-{strategy}")
            for strategy in strategies
        }
        if pair["node"]["hashes"] != pair["port"]["hashes"]:
            raise ValueError("canonical state or ordered events differ; timing cannot select a winner")
        for strategy in strategies:
            samples[strategy].append(pair[strategy]["metadata"])
    if source_fingerprint() != before:
        raise ValueError("simulator source changed during comparison")
    report = {
        "scope": "interim six-Port scheduling only; 24 internal Register mapping remains open",
        "per_tick_parity": True,
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "source_sha256": before,
        "samples": samples,
        "median_step_seconds": {
            strategy: median(sample["stepping_seconds"] for sample in values)
            for strategy, values in samples.items()
        },
        "limits": "One host. Step timers include identical event callbacks, exclude recording and HTML. "
        "Queue entry counts are structural storage evidence, not a host peak-memory measurement. "
        "No result chooses or validates the unimplemented 24-Register strategy.",
    }
    (args.output / "comparison.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "samples"}))


if __name__ == "__main__":
    main()

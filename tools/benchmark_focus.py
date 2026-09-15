"""Reproduce exact-state Focus benchmarks against an explicitly selected checkout.

Run with PYTHONPATH set to that checkout's src. Step timers exclude per-tick
state verification and playback export; event serialization remains included.
Each invocation is a fresh world and writes its input, trace, hashes and HTML.
"""

import argparse
import hashlib
import json
import platform
from copy import deepcopy
from pathlib import Path
from time import perf_counter, process_time

import event_universe
from event_universe import Simulation
from event_universe.diagnostics.disturbance_render import render_disturbances
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint


def configuration(case, source):
    if case == "fields":
        raw = json.loads((source / "examples/node-vector/two-fields.json").read_text())
        raw["shape"] = [8, 8, 8]
        positions = [(x, y, 2) for x in range(2, 6) for y in range(2, 6)]
        for key in ("seeds", "spatial_seeds"):
            raw[key] = [dict(seed, position=list(p)) for p in positions for seed in raw.get(key, [])]
        raw["ticks"] = 48
        return raw
    if case == "finite":
        raw = json.loads((source / "examples/finite_fields.json").read_text())
        raw["ticks"] = 16
        return raw
    raw = json.loads((source / "examples/basic.json").read_text())
    raw["disturbance_types"] = [deepcopy(raw["disturbance_types"][0])]
    raw["disturbance_types"][0]["transport"] = {"mode": "move", "weights": [1, 0, 0, 0, 0, 0]}
    raw["slots_per_node"] = 1
    if case == "trail":
        raw["shape"], raw["ticks"] = [512, 4, 4], 240
        positions = [(1, 1, 1)]
    else:
        raw["shape"], raw["ticks"] = [12, 40, 4], 120
        positions = [(1, y, 1) for y in range(1, 33)]
    raw["seeds"] = [{"position": list(p), "type": "carrier"} for p in positions]
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=("trail", "repeated", "fields", "finite"), required=True)
    parser.add_argument("--focus", choices=("default", "true", "false"), default="default")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    if Path(event_universe.__file__).resolve() != source / "src/event_universe/__init__.py":
        raise RuntimeError("imported simulator differs from the selected source")
    args.output.mkdir(parents=True, exist_ok=False)
    raw = configuration(args.case, source)
    if args.focus != "default":
        raw["focus"] = args.focus == "true"
    initial = parse_initial_state(raw)
    (args.output / "input.json").write_text(json.dumps(raw, indent=2) + "\n")
    before = source_fingerprint()
    traces, states = hashlib.sha256(), hashlib.sha256()
    frames, samples, cpu_samples = [], [], []
    with (args.output / "events.jsonl").open("w") as events:

        def observe(event):
            line = json.dumps(event, sort_keys=True) + "\n"
            traces.update(line.encode())
            events.write(line)

        with Simulation(initial, observer=observe) as world:
            frames.append(world.snapshot())
            for _ in range(raw["ticks"]):
                start, cpu_start = perf_counter(), process_time()
                world.step()
                cpu_samples.append(process_time() - cpu_start)
                samples.append(perf_counter() - start)
                snapshot = world.snapshot()
                states.update(json.dumps(snapshot, sort_keys=True).encode())
                states.update(repr(world.inventory_view()).encode())
                states.update(json.dumps(world.computation_report(), sort_keys=True).encode())
                frames.append(snapshot)
            report = {
                "case": args.case,
                "python": platform.python_version(),
                "source": str(source),
                "source_sha256": before,
                "focus": initial.focus,
                "ticks": world.tick,
                "step_seconds": sum(samples),
                "step_cpu_seconds": sum(cpu_samples),
                "state_sha256": states.hexdigest(),
                "events_sha256": traces.hexdigest(),
                "computation": world.computation_report(),
                "execution": world.execution_report(),
                "totals": world.totals(),
                "spatial_accounting": world.spatial_accounting(),
                "status": "completed",
            }
    if source_fingerprint() != before:
        raise RuntimeError("simulator source changed during measurement")
    (args.output / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    render_disturbances(frames, args.output / "run.html", report)
    print(json.dumps(report))


if __name__ == "__main__":
    main()

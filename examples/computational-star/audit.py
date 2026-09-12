"""Measure actual vector-field processing delays without changing momentum or routing."""

import argparse
import hashlib
import json
import platform
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path

from event_universe import Simulation
from event_universe.experiment import load_experiment
from event_universe.initialization import parse_initial_state
from event_universe.retention import ArtifactLease
from event_universe.runner import source_fingerprint

HERE = Path(__file__).resolve().parent
PROBES = ("inner", "middle", "outer")


def configurations():
    raw = json.loads(load_experiment(HERE / "experiment.json").runtime_json)
    cases = {"active": raw}
    for name in ("no_field", "small_mass", "reverse_vector", "high_budget"):
        cases[name] = deepcopy(raw)
    cases["no_field"]["emissions"] = []
    for seed in cases["small_mass"]["seeds"]:
        if seed["type"] == "star_constituent":
            seed["values"]["mass"] = 4
    cases["reverse_vector"]["disturbance_types"][0]["defaults"]["load_axis"] = [-1, -1, -1]
    cases["high_budget"]["normal_budget"] = 100000
    return cases


def records(snapshot):
    result = {
        r["type"]: {"position": c["position"], "values": r["values"], "in_transit": False}
        for c in snapshot["cells"]
        for r in c["disturbances"]
        if r["type"] in PROBES
    }
    result.update(
        {
            r["type"]: {"position": r["origin"], "values": r["values"], "in_transit": True}
            for r in snapshot["transfers"]
            if r["type"] in PROBES
        }
    )
    return result


def run_case(task):
    name, raw, destination = task
    output = Path(destination) / name
    output.mkdir()
    (output / "initial.json").write_text(json.dumps(raw, indent=2))
    departures = {name: [] for name in PROBES}
    delays = {name: [] for name in PROBES}
    lanes = {seed["position"][1]: seed["type"] for seed in raw["seeds"] if seed["type"] in PROBES}
    digest = hashlib.sha256()
    event_counts = {}

    def observer(event):
        kind = event["event"]
        event_counts[kind] = event_counts.get(kind, 0) + 1
        digest.update(json.dumps(event, sort_keys=True).encode())
        if kind == "sent" and event["disturbance"] in PROBES:
            departures[event["disturbance"]].append(
                {
                    "tick": event["tick"],
                    "port": event["port"],
                    "position": event["position"],
                    "arrival_tick": event["arrival_tick"],
                    "values": event["values"],
                }
            )
        if kind == "cycle_started" and event["position"][1] in lanes:
            delays[lanes[event["position"][1]]].append(
                {
                    "tick": event["tick"],
                    "cost": event["cost"],
                    "extra": event["ready_tick"] - event["tick"],
                    "position": event["position"],
                }
            )

    world = Simulation(parse_initial_state(raw), observer=observer)
    initial = world.totals()
    errors = {field: 0 for field in initial}
    frames = []
    fault = None
    with (output / "frames.jsonl").open("w") as recording:
        for _ in range(raw["ticks"] + 1):
            snapshot = world.snapshot()
            owned = records(snapshot)
            for probe in owned.values():
                if tuple(probe["values"]["momentum"]) != (1, 0, 0) or tuple(probe["values"]["mass"]) != (
                    4,
                ):
                    raise AssertionError("A delay-only probe changed momentum or mass")
            totals = world.totals()
            escaped, lost, supplied = (
                world.escaped_totals(),
                world.dissipation_totals(),
                world.source_totals(),
            )
            for field in initial:
                for i, value in enumerate(totals[field]):
                    errors[field] = max(
                        errors[field],
                        abs(
                            value
                            + escaped[field][i]
                            + lost[field][i]
                            - supplied[field][i]
                            - initial[field][i]
                        ),
                    )
            field_slice = []
            if world.tick % 2 == 0:
                for node in snapshot["spatial_fields"]:
                    if node["position"][2] == 32:
                        value = node["fields"]["computational_load"]["value"]
                        if any(value):
                            field_slice.append([*node["position"], *value])
            source_work = [
                r["values"]["work"][0]
                for c in snapshot["cells"]
                for r in c["disturbances"]
                if r["type"] == "star_constituent"
            ]
            frame = {
                "tick": world.tick,
                "probes": owned,
                "field_slice": field_slice,
                "source_work_max": max(source_work, default=0),
            }
            frames.append(frame)
            recording.write(json.dumps(frame) + "\n")
            if world.tick >= raw["ticks"] or fault:
                break
            try:
                world.step()
            except (ValueError, OverflowError, RuntimeError) as exc:
                fault = type(exc).__name__ + ": " + str(exc)
    result = {
        "case": name,
        "ticks": world.tick,
        "fault": fault,
        "max_inventory_error": errors,
        "momentum_unchanged": True,
        "departures": departures,
        "cycles": delays,
        "trace_sha256": digest.hexdigest(),
        "event_counts": event_counts,
        "final_probes": frames[-1]["probes"],
        "star_mass": sum(s["values"]["mass"] for s in raw["seeds"] if s["type"] == "star_constituent"),
        "source_injection": world.source_totals(),
        "dissipation": world.dissipation_totals(),
    }
    (output / "result.json").write_text(json.dumps(result, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    with ArtifactLease(args.output.parent, [args.output]):
        metadata = {
            "model_id": "measured-vector-work-delay-only-v1",
            "source_fingerprint": source_fingerprint(),
            "python": platform.python_version(),
            "base_commit": "7074e2c4490486f8524d687557af70579521da0a",
        }
        (args.output / "metadata.json").write_text(json.dumps(metadata, indent=2))
        results = []
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            jobs = [
                pool.submit(run_case, (name, raw, str(args.output)))
                for name, raw in configurations().items()
            ]
            for job in as_completed(jobs):
                result = job.result()
                results.append(result)
                (args.output / "results.json").write_text(json.dumps(results, indent=2))
                print(
                    result["case"],
                    result["ticks"],
                    result["fault"],
                    {k: len(v) for k, v in result["departures"].items()},
                    flush=True,
                )
        control = next(r for r in results if r["case"] == "no_field")
        comparisons = []
        for result in results:
            for probe in PROBES:
                observed = result["departures"][probe]
                reference = control["departures"][probe][: len(observed)]
                same_ports = [r["port"] for r in observed] == [r["port"] for r in reference]
                assert same_ports, "Delay-only port sequence changed"
                comparisons.append(
                    {
                        "case": result["case"],
                        "probe": probe,
                        "hops": len(observed),
                        "same_port_prefix": same_ports,
                        "scheduled_extra_wait_sum": sum(c["extra"] for c in result["cycles"][probe]),
                        "delayed_cycles": sum(c["extra"] > 0 for c in result["cycles"][probe]),
                        "max_local_cost": max((c["cost"] for c in result["cycles"][probe]), default=0),
                    }
                )
        (args.output / "comparisons.json").write_text(json.dumps(comparisons, indent=2))


if __name__ == "__main__":
    main()

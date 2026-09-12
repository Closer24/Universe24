"""Configure and measure local mass-flux experiments; diagnostics never drive physics."""

import argparse
import hashlib
import json
import math
import platform
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy
from pathlib import Path

from event_universe import Simulation
from event_universe.experiment import load_experiment
from event_universe.initialization import parse_initial_state
from event_universe.retention import ArtifactLease
from event_universe.runner import source_fingerprint

HERE = Path(__file__).resolve().parent


def configurations():
    package = load_experiment(HERE / "experiment.json")
    template = json.loads(package.runtime_json)
    matrix = json.loads((HERE / "matrix.json").read_text())
    result = []
    for family in matrix["families"]:
        for variant in matrix["variants"]:
            raw = deepcopy(template)
            probe = raw["seeds"][-1]
            probe["position"] = [5 + x for x in family["position"]]
            n, d = variant.get("speed", [1, 1])
            probe["values"]["momentum"] = [x * n // d for x in family["momentum"]]
            probe["values"]["mass"] = variant.get("probe_mass", 64)
            if family.get("live"):
                for seed in raw["seeds"][:-1]:
                    seed["type"] = "live_source"
            if variant.get("no_field"):
                raw["emissions"] = []
            if "denominator" in variant:
                for coupling in raw["spatial_couplings"]:
                    coupling["denominator"] = variant["denominator"]
            if variant.get("rotate"):
                for seed in raw["seeds"]:
                    seed["position"] = [seed["position"][2], seed["position"][0], seed["position"][1]]
                    if "momentum" in seed["values"]:
                        p = seed["values"]["momentum"]
                        seed["values"]["momentum"] = [p[2], p[0], p[1]]
            if variant.get("reverse"):
                raw["seeds"].reverse()
            raw["ticks"] = matrix["long_ticks"] if variant["name"] == "base" else matrix["screen_ticks"]
            parse_initial_state(raw)
            result.append((family["name"] + "-" + variant["name"], raw))
    return result


def carriers(frame):
    result = [
        {"position": cell["position"], **row} for cell in frame["cells"] for row in cell["disturbances"]
    ]
    # A link packet owns the carrier at its origin until arrival. No interpolated
    # position enters the simulator or the contact/orbit acceptance measurement.
    result.extend({"position": row["origin"], **row} for row in frame["transfers"])
    return result


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def classify(trajectory, escaped, fault):
    points = [f["probe"] for f in trajectory if f["probe"] is not None]
    radii = [math.dist(p["position"], [5, 5, 5]) for p in points]
    # Project onto the initial orbital plane; a radial launch has no such plane.
    initial = points[0]
    radius = [x - 5 for x in initial["position"]]
    normal = cross(radius, initial["values"]["momentum"])
    norm = math.sqrt(sum(x * x for x in normal))
    angle = 0.0
    if norm:
        normal = [x / norm for x in normal]
        for a, b in zip(points, points[1:], strict=False):
            u = [x - 5 for x in a["position"]]
            v = [x - 5 for x in b["position"]]
            u_normal = sum(x * y for x, y in zip(u, normal, strict=True))
            v_normal = sum(x * y for x, y in zip(v, normal, strict=True))
            u = [x - u_normal * n for x, n in zip(u, normal, strict=True)]
            v = [x - v_normal * n for x, n in zip(v, normal, strict=True)]
            angle += math.atan2(
                sum(x * y for x, y in zip(cross(u, v), normal, strict=True)),
                sum(x * y for x, y in zip(u, v, strict=True)),
            )
    contact = any(f["contact"] for f in trajectory)
    turns = abs(angle) / (2 * math.pi)
    live = any(r["type"] == "live_source" for r in trajectory[0].get("sources", []))
    status = (
        "runtime_fault"
        if fault
        else "escaped"
        if escaped
        else "cluster_contact"
        if contact
        else "finite_time_circling_candidate"
        if not live and turns >= 2 and min(radii) > 1.8
        else "no_two_revolutions_observed"
    )
    return {
        "classification": status,
        "turns": turns,
        "minimum_radius": min(radii),
        "maximum_radius": max(radii),
        "cluster_contact": contact,
    }


def run_case(task):
    name, raw, output = task
    directory = Path(output) / name
    directory.mkdir()
    (directory / "initial.json").write_text(json.dumps(raw, indent=2))
    events = {}
    trace = hashlib.sha256()
    maximum_cost = 0
    delayed_cycles = 0

    def observe(event):
        nonlocal maximum_cost, delayed_cycles
        kind = event["event"]
        events[kind] = events.get(kind, 0) + 1
        trace.update(json.dumps(event, sort_keys=True).encode())
        if kind == "cycle_started":
            maximum_cost = max(maximum_cost, event["cost"])
            delayed_cycles += event["ready_tick"] > event["tick"]

    world = Simulation(parse_initial_state(raw), observer=observe)
    initial = world.totals()
    trajectory = []
    fault = None
    max_error = {name: 0 for name in initial}
    started = time.perf_counter()
    overspeed = 0
    for _ in range(raw["ticks"] + 1):
        frame = world.snapshot()
        rows = carriers(frame)
        probes = [r for r in rows if r["type"] == "probe"]
        probe = probes[0] if probes else None
        sources = [r for r in rows if r["type"] != "probe"]
        # Distinguish same origin while in transit from co-residence.
        contact = any(
            any(r["type"] == "probe" for r in c["disturbances"])
            and any(r["type"] != "probe" for r in c["disturbances"])
            for c in frame["cells"]
        )
        totals, escaped = world.totals(), world.escaped_totals()
        injected, dissipated = world.source_totals(), world.dissipation_totals()
        for field, values in totals.items():
            for i, value in enumerate(values):
                error = (
                    value
                    + escaped[field][i]
                    + dissipated[field][i]
                    - initial[field][i]
                    - injected[field][i]
                )
                max_error[field] = max(max_error[field], abs(error))
        kinetic = sum(
            sum(p * p for p in r["values"]["momentum"]) / (2 * r["values"]["mass"][0]) for r in rows
        )
        overspeed += sum(
            sum(abs(p) for p in r["values"]["momentum"]) > r["values"]["mass"][0] for r in rows
        )
        signal_samples = []
        # Fixed actual lattice slice, retaining the delivered vector and stock.
        if world.tick % 4 == 0:
            z = raw["shape"][2] // 2
            for x in range(raw["shape"][0]):
                for y in range(raw["shape"][1]):
                    field = world.spatial_values((x, y, z))["signal"]
                    directions = field["directions"]
                    flux = [directions[2 * i][0] - directions[2 * i + 1][0] for i in range(3)]
                    signal_samples.append([x, y, z, field["value"][0], *flux])
        trajectory.append(
            {
                "tick": world.tick,
                "probe": probe,
                "sources": sources,
                "contact": contact,
                "kinetic_proxy": kinetic,
                "signal_slice": signal_samples,
            }
        )
        if world.tick >= raw["ticks"] or probe is None or fault:
            break
        try:
            world.step()
        except (ValueError, OverflowError, RuntimeError) as exc:
            fault = type(exc).__name__ + ": " + str(exc)
    result = {
        "case": name,
        "requested_ticks": raw["ticks"],
        "completed_ticks": world.tick,
        "seconds": time.perf_counter() - started,
        "fault": fault,
        "max_inventory_error": max_error,
        "maximum_cost": maximum_cost,
        "delayed_cycles": delayed_cycles,
        "overspeed_record_ticks": overspeed,
        "events": events,
        "trace_sha256": trace.hexdigest(),
        "initial_sha256": hashlib.sha256(json.dumps(raw, sort_keys=True).encode()).hexdigest(),
        **classify(trajectory, trajectory[-1]["probe"] is None, fault),
    }
    (directory / "trajectory.json").write_text(json.dumps(trajectory))
    (directory / "result.json").write_text(json.dumps(result, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--case", help="Exact case name for a bounded rerun")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    with ArtifactLease(args.output.parent, [args.output]):
        cases = [
            (name, raw, str(args.output))
            for name, raw in configurations()
            if args.case is None or name == args.case
        ]
        if not cases:
            raise ValueError("No selected cases")
        metadata = {
            "model_id": "local-mass-flux-attraction-v1",
            "source_fingerprint": source_fingerprint(),
            "python": platform.python_version(),
            "planned_cases": [name for name, _, _ in cases],
            "limitations": [
                "Externally supplied scalar signal",
                "No gravitational energy law",
                "Held cluster is supported",
                "Open boundaries",
                "Cold field startup",
            ],
        }
        (args.output / "metadata.json").write_text(json.dumps(metadata, indent=2))
        results = []
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            jobs = [pool.submit(run_case, task) for task in cases]
            for job in as_completed(jobs):
                result = job.result()
                results.append(result)
                (args.output / "results.json").write_text(
                    json.dumps(sorted(results, key=lambda r: r["case"]), indent=2)
                )
                print(
                    result["case"],
                    result["classification"],
                    result["completed_ticks"],
                    result["max_inventory_error"],
                    flush=True,
                )


if __name__ == "__main__":
    main()

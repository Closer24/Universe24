"""Measure covering-space paths and ownership of actual timing-only encounters."""

import argparse
import hashlib
import json
import math
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from configuration import configurations

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.retention import ArtifactLease
from event_universe.runner import source_fingerprint

PROBES = ("light_neutral", "heavy_neutral", "light_charged")
OFFSETS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def run_case(task):
    name, raw, destination = task
    started = time.perf_counter()
    folder = Path(destination) / name
    folder.mkdir()
    (folder / "initial.json").write_text(json.dumps(raw, indent=2))
    departures = {p: [] for p in PROBES}
    counts = {}
    digest = hashlib.sha256()
    carrier_waits = []
    field_waits = []
    transit_errors = []

    def observer(event):
        kind = event["event"]
        counts[kind] = counts.get(kind, 0) + 1
        digest.update(json.dumps(event, sort_keys=True).encode())
        if (
            kind in ("sent", "spatial_sent")
            and event["arrival_tick"] - event["tick"] != raw["link_ticks"]
        ):
            transit_errors.append(event)
        if kind == "sent" and event["disturbance"] in PROBES:
            departures[event["disturbance"]].append(event)
        if kind == "departure_waiting" and event["disturbance"] in PROBES:
            carrier_waits.append({k: event[k] for k in ("tick", "dispatch_tick", "port", "disturbance")})
        if kind == "spatial_departure_waiting":
            field_waits.append(event["dispatch_tick"] - event["tick"])

    world = Simulation(parse_initial_state(raw), observer=observer)
    initial = world.totals()
    expected = {
        kind["name"]: kind["defaults"] for kind in raw["disturbance_types"] if kind["name"] in PROBES
    }
    errors = {key: 0 for key in initial}
    momentum_errors = 0
    frames = []
    fault = None
    for tick in range(raw["ticks"] + 1):
        if tick:
            try:
                world.step()
            except (ValueError, RuntimeError, OverflowError) as exc:
                fault = f"{type(exc).__name__}: {exc}"
        totals = world.totals()
        escaped, lost, supplied = (
            world.escaped_totals(),
            world.dissipation_totals(),
            world.source_totals(),
        )
        for field, values in totals.items():
            errors[field] = max(
                errors[field],
                *(
                    abs(v + escaped[field][i] + lost[field][i] - supplied[field][i] - initial[field][i])
                    for i, v in enumerate(values)
                ),
            )
        snapshot = world.snapshot()
        records = {
            r["type"]: {"position": c["position"], "values": r["values"], "phase": "resident"}
            for c in snapshot["cells"]
            for r in c["disturbances"]
            if r["type"] in PROBES
        }
        records.update(
            {
                r["type"]: {
                    "position": r["origin"],
                    "values": r["values"],
                    "phase": r.get("phase", "transit"),
                }
                for r in snapshot["transfers"]
                if r["type"] in PROBES
            }
        )
        for probe, row in records.items():
            momentum_errors += tuple(row["values"]["momentum"]) != tuple(expected[probe]["momentum"])
        if world.tick % 4 == 0 or fault:
            field = []
            for cell in snapshot["spatial_fields"]:
                if cell["position"][2] == 64:
                    value = cell["fields"]["computational_load"]["value"]
                    if any(value):
                        field.append([*cell["position"], *value, 0])
            for packet in snapshot["spatial_transfers"]:
                if packet["origin"][2] == 64:
                    value = [
                        sum(pop[i] for pop in packet["fields"]["computational_load"]) for i in range(3)
                    ]
                    if any(value):
                        field.append(
                            [*packet["origin"], *value, 1 if packet.get("phase") == "waiting" else 2]
                        )
            frames.append({"tick": world.tick, "probes": records, "field": field})
        if fault:
            break
    measured = {}
    for probe, events in departures.items():
        start = next(s["position"] for s in raw["seeds"] if s["type"] == probe)
        positions = [start]
        for event in events:
            positions.append(
                [a + b for a, b in zip(event["position"], OFFSETS[event["port"]], strict=True)]
            )
        angles = [math.atan2(p[1] - 64, p[0] - 64) for p in positions]
        sweep = sum(
            math.atan2(math.sin(b - a), math.cos(b - a))
            for a, b in zip(angles, angles[1:], strict=False)
        )
        radii = [math.dist(p, [64, 64, 64]) for p in positions]
        momentum = expected[probe]["momentum"]
        increasing = all(
            sum(a * b for a, b in zip(momentum, OFFSETS[e["port"]], strict=True)) > 0 for e in events
        )
        measured[probe] = {
            "hops": len(events),
            "ports": [e["port"] for e in events],
            "positions": positions,
            "min_radius": min(radii),
            "final_radius": radii[-1],
            "angle_sweep_degrees": math.degrees(sweep),
            "projection_strictly_increasing": increasing,
            "closed_orbit": len(events) > 0
            and positions[-1] == positions[0]
            and abs(sweep) >= 2 * math.pi - 0.1,
        }
    result = {
        "case": name,
        "ticks": world.tick,
        "fault": fault,
        "max_inventory_error": errors,
        "momentum_errors": momentum_errors,
        "transit_errors": len(transit_errors),
        "probes": measured,
        "carrier_waits": carrier_waits,
        "field_wait_count": len(field_waits),
        "field_wait_max": max(field_waits, default=0),
        "event_counts": counts,
        "trace_sha256": digest.hexdigest(),
        "source_totals": supplied,
        "host_seconds": time.perf_counter() - started,
    }
    (folder / "frames.jsonl").write_text("".join(json.dumps(f) + "\n" for f in frames))
    (folder / "result.json").write_text(json.dumps(result, indent=2))
    print(name, world.tick, fault, {p: m["hops"] for p, m in measured.items()}, flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--near", action="store_true")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    with ArtifactLease(args.output.parent, [args.output]):
        cases = configurations()
        if args.near:
            cases = {
                name: cases[name]
                for name in ("active", "small_star", "reverse_vector", "mirrored_approach")
            }
            for case in cases.values():
                for seed in case["seeds"][27:]:
                    seed["position"][1] = 66
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            results = [
                f.result()
                for f in as_completed(
                    pool.submit(run_case, (n, c, str(args.output))) for n, c in cases.items()
                )
            ]
        (args.output / "summary.json").write_text(
            json.dumps({"source_fingerprint": source_fingerprint(), "results": results}, indent=2)
        )


if __name__ == "__main__":
    main()

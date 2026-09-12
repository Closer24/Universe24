"""Measure actual receptions, not a path whose direction was fixed by the launcher."""

import argparse
import json
from pathlib import Path

from configuration import WAVE, configuration, settings

from event_universe.runner import run_initialization


def receipt_has_wave(values: dict) -> bool:
    return any(any(values.get(name, ())) for name in WAVE.NAMES)


def summarize(output: Path, options: dict) -> dict:
    meta = json.loads((output / "run.json").read_text())
    observation = json.loads((output / "observations.json").read_text())
    arrivals = []
    wave_positions = set()
    for line in (output / "events.jsonl").read_text().splitlines():
        event = json.loads(line)
        if event["event"] == "spatial_received":
            if any(receipt_has_wave(values) for values in event["received_fields"]):
                wave_positions.add(tuple(event["position"]))
                if event["position"] == options["observer_position"]:
                    arrivals.append(event["tick"])
    local_receipts = [
        receipt for receipt in observation["receipts"] if receipt_has_wave(receipt["values"])
    ]
    beam_lines = {tuple(p[1:]) for p in options["wave_seed_positions"]}
    initial = json.loads((output / "initialization.json").read_text())
    final = json.loads((output / "state.json").read_text())
    norm_initial = sum(
        sum(v * v for v in population)
        for seed in initial["spatial_seeds"]
        if seed["field"] in WAVE.NAMES
        for population in seed["populations"]
    )
    norm_final = sum(
        sum(v * v for v in node["fields"][name]["value"])
        for node in final["spatial_fields"]
        for name in WAVE.NAMES
    )
    for packet in final["spatial_transfers"]:
        for name in WAVE.NAMES:
            norm_final += sum(sum(p[c] for p in packet["fields"][name]) ** 2 for c in range(3))
    for line in (output / "events.jsonl").read_text().splitlines():
        event = json.loads(line)
        if event["event"] == "spatial_escaped":
            norm_final += sum(
                sum(v * v for v in vector)
                for name, vector in event["escaped"].items()
                if name in WAVE.NAMES
            )
    controls = [
        node["fields"][options["delay_control"]["field"]["name"]]["value"]
        for node in final["spatial_fields"]
    ]

    return {
        "completed_ticks": meta["completed_ticks"],
        "accounting_balanced": meta["accounting_balanced_at_every_completed_tick"],
        "audit_detector_first_wave_tick": min(arrivals, default=None),
        "detector_status": "received" if arrivals else "not_observed_within_window",
        "observer_first_wave_clock": local_receipts[0]["clock"] if local_receipts else None,
        "observer_clock_kind": observation["clock_kind"],
        "transverse_receipts_present": any(p[1:] not in beam_lines for p in wave_positions),
        "wave_receiving_nodes": len(wave_positions),
        "wave_squared_amplitude_initial": norm_initial,
        "wave_squared_amplitude_final_plus_escaped": norm_final,
        "wave_squared_amplitude_balance_matches": norm_initial == norm_final,
        "nonuniform_control_nodes_at_end": sum(len(set(value)) > 1 for value in controls),
        "directional_delay": meta["directional_delay"],
        "source_sha256": meta["source_sha256"],
        "initialization_sha256": meta["initialization_sha256"],
    }


def delay_difference(candidate: dict, control: dict) -> int | None:
    first, reference = (
        candidate["audit_detector_first_wave_tick"],
        control["audit_detector_first_wave_tick"],
    )
    return None if first is None or reference is None else first - reference


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--visualize", action="store_true")
    args = parser.parse_args()
    options = settings(args.settings) if args.settings else settings()
    inputs = args.output / "inputs"
    args.output.mkdir(parents=True, exist_ok=False)
    inputs.mkdir()
    observer = inputs / "observer.json"
    observer.write_text(json.dumps({"position": options["observer_position"], "max_receipts": 100000}))
    uniform = {"weights": 1, "spatial_mode": "cost"}
    selected = options["directional_delay"]
    cases = (
        ("legacy_fixed_control", 0, {"weights": 1, "spatial_mode": "fixed"}, True),
        ("uniform_zero_strength", 0, uniform, True),
        ("uniform_source", options["source_strength"], uniform, True),
        ("directional_zero_strength", 0, selected, True),
        ("directional_source", options["source_strength"], selected, True),
        ("locked_direction_control", 0, selected, False),
    )
    results = {}
    for name, mass, delay, mixing in cases:
        source = inputs / f"{name}.json"
        source.write_text(
            json.dumps(configuration(options, mass=mass, delay=delay, mixing=mixing), indent=2) + "\n"
        )
        output = args.output / name
        run_initialization(source, output, observer=observer, visualize=args.visualize)
        results[name] = summarize(output, options)
    report = {
        "cases": results,
        "uniform_mass_arrival_difference": delay_difference(
            results["uniform_source"], results["uniform_zero_strength"]
        ),
        "directional_mass_arrival_difference": delay_difference(
            results["directional_source"], results["directional_zero_strength"]
        ),
        "curvature_status": "not_established",
        "interpretation": "Transverse mixing alone is not gravitational bending. Null arrival differences are censored, not zero. Audit ticks and local transaction counts are different measurements; no physical ruler or proper-time law is derived.",
    }
    (args.output / "measurements.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

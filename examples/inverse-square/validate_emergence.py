"""Read-only radial-law experiment on the existing local transport candidates."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

import event_universe
from event_universe import Simulation
from event_universe.configuration_validation import prepare_initialization
from event_universe.runner import source_fingerprint

SPEC = importlib.util.spec_from_file_location(
    "radial_configuration", Path(__file__).with_name("run_experiments.py")
)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)
RADIUS = 9
STRENGTH = 8 * 3**RADIUS


def offsets(radius):
    """Enumerate one complete Manhattan shell without duplicate zero coordinates."""
    for x in range(-radius, radius + 1):
        for y in range(-radius + abs(x), radius - abs(x) + 1):
            z = radius - abs(x) - abs(y)
            for signed_z in sorted({z, -z}):
                yield (x, y, signed_z)


def prediction(position, strength):
    """Independent path counting, valid only before wrap and exact integer splitting."""
    absolute = [abs(v) for v in position]
    radius = sum(absolute)
    paths = math.factorial(radius) // math.prod(math.factorial(v) for v in absolute)
    octants = 2 ** absolute.count(0)
    return Fraction(strength * octants * paths, 8 * 3**radius)


def configuration(size=25, strength=STRENGTH, center=None, headings=0, weighted=False):
    PROBE.configure(size, 11, strength)
    raw = PROBE.conservative_document(False)
    raw["spatial_couplings"] = []
    raw["boundary"] = "open"
    raw["seeds"][0]["position"] = center or [size // 2] * 3
    if weighted:
        raw["spatial_fields"][0]["axis_weights"] = [4, 1, 1]
    if headings:
        raw["spatial_fields"][0] = {
            "field": "radiation",
            "baseline": 0,
            "transport": "ray",
            "headings": PROBE.golden_headings(headings, 96),
            "rays_per_tick": 32,
            "ray_slots": 512,
        }
        warm = max(11, headings // 32)
        raw["ticks"] = warm + headings // 32
    return raw


def run_case(name, raw, output, exact=False, capture=False):
    directory = output / name
    directory.mkdir()
    encoded = json.dumps(raw, indent=2) + "\n"
    (directory / "initialization.json").write_text(encoded, encoding="utf-8")
    prepared = prepare_initialization(raw)
    world = Simulation(prepared.initial)
    center = raw["seeds"][0]["position"]
    strength = raw["disturbance_types"][0]["defaults"]["strength"]
    ray = raw["spatial_fields"][0]["transport"] == "ray"
    warm = raw["ticks"] - len(raw["spatial_fields"][0]["headings"]) // 32 if ray else 10
    points = [p for radius in range(1, RADIUS + 1) for p in offsets(radius)]
    accumulated = dict.fromkeys(points, 0)
    trace, frames, samples = [], [], 0
    started = time.perf_counter()
    for tick in range(1, raw["ticks"] + 1):
        world.step()
        values = {
            p: world.spatial_values(tuple(a + b for a, b in zip(center, p, strict=True)))["radiation"][
                "value"
            ][0]
            for p in points
        }
        totals = world.totals()["radiation"][0]
        sources = world.source_totals()["radiation"][0]
        escaped = world.escaped_totals()["radiation"][0]
        residual = totals + escaped - sources
        premature = sum(v for p, v in values.items() if sum(map(abs, p)) > tick)
        trace.append(
            {
                "tick": tick,
                "inventory": totals,
                "injected": sources,
                "escaped": escaped,
                "residual": residual,
                "premature_stock": premature,
            }
        )
        (directory / "trace.json").write_text(json.dumps(trace, indent=2), encoding="utf-8")
        assert residual == 0, (name, tick, "inventory", residual)
        assert premature == 0, (name, tick, "causal_front", premature)
        if tick > warm:
            samples += 1
            for p, value in values.items():
                accumulated[p] += value
        if capture:
            frames.append({"tick": tick, "points": [[*p, v] for p, v in values.items() if v]})
    means = {p: Fraction(v, samples) for p, v in accumulated.items()}
    shells = []
    for radius in range(1, RADIUS + 1):
        shell = list(offsets(radius))
        total = sum(means[p] for p in shell)
        assert len(shell) == 4 * radius * radius + 2
        assert total == strength, (name, radius, total, strength)
        shells.append(
            {
                "radius": radius,
                "node_count": len(shell),
                "stock": float(total),
                "mean": float(total / len(shell)),
                "mean_times_radius_squared_over_source": float(
                    total * radius**2 / len(shell) / strength
                ),
            }
        )
    mismatches = None
    if exact:
        mismatches = sum(means[p] != prediction(p, strength) for p in points)
        assert mismatches == 0, (name, "multinomial", mismatches)
    pair = [(5, 0, 0), (3, 4, 0)]
    readings = [float(means[p]) for p in pair]
    result = {
        "name": name,
        "ticks": raw["ticks"],
        "samples": samples,
        "elapsed_seconds": time.perf_counter() - started,
        "configuration_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
        "shells": shells,
        "exact_point_mismatches": mismatches,
        "same_euclidean_radius": {
            "positions": pair,
            "radius": 5,
            "values": readings,
            "second_over_first": readings[1] / readings[0] if readings[0] else None,
        },
        "max_balance_residual": max(abs(row["residual"]) for row in trace),
        "max_premature_stock": max(row["premature_stock"] for row in trace),
    }
    (directory / "trace.json").write_text(json.dumps(trace, indent=2), encoding="utf-8")
    (directory / "measurements.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    if capture:
        (directory / "frames.json").write_text(json.dumps(frames), encoding="utf-8")
    print(json.dumps(result), flush=True)
    return result, means


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    before = source_fingerprint()
    cases = [
        ("octant_base", configuration(), True),
        ("larger_world", configuration(size=31), True),
        ("translated_source", configuration(size=31, center=[11, 14, 17]), True),
        ("double_source", configuration(strength=2 * STRENGTH), True),
        ("indivisible_units", configuration(strength=8), False),
        ("biased_axes", configuration(weighted=True), False),
        ("rays_512", configuration(headings=512), False),
        ("rays_2048", configuration(headings=2048), False),
    ]
    rows, baseline = [], None
    for name, raw, exact in cases:
        row, measured = run_case(name, raw, args.output, exact, name in ("octant_base", "rays_2048"))
        if baseline is None:
            baseline = measured
        if name in ("larger_world", "translated_source"):
            assert measured == baseline
        if name == "double_source":
            assert measured == {p: 2 * v for p, v in baseline.items()}
        rows.append(row)
    assert before == source_fingerprint()
    report = {
        "source_sha256": before,
        "package_path": event_universe.__file__,
        "python": sys.version,
        "measurement_scope": "read-only world/event audit",
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "cases": rows,
    }
    (args.output / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

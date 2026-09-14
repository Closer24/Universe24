"""Isotropy probe: how evenly do the two field candidates spread around a source?

Nature's point sources radiate the same intensity in every direction at the
same distance. This probe measures, on recorded runs of the canonical runner,
how far each configured spreading rule is from that: the octant-splitting
outward field, whose pointwise stock follows an exact path count, and the
straight-ray field, whose evenness depends on how many headings it fires.

Every number is a read-only world audit at host Euclidean distance; no engine
law is added or changed. Analytic references are computed independently of
the update code: the multinomial path count for the outward rule, and the
isotropic inverse-square expectation for both.
"""

import argparse
import json
import math
import shutil
import statistics
from math import factorial
from pathlib import Path
from typing import Any

from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import run_initialization

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUTWARD_TEMPLATE = ROOT / "examples/moving_source.json"
RAY_TEMPLATE = ROOT / "examples/isotropic_rays.json"
OUTWARD_SOURCE = 8 * 3**9
OUTWARD_SHELL = 9
RAY_SCALE = 24
RAYS_PER_TICK = 64
RAY_UNITS = 16
RAY_RADIUS = 8.0
RAY_WARMUP = 12
HEADING_COUNTS = (256, 1024, 4096, 16384)
OUTWARD_POINTS = (
    (9, 0, 0),
    (8, 1, 0),
    (7, 2, 0),
    (6, 3, 0),
    (5, 4, 0),
    (7, 1, 1),
    (5, 2, 2),
    (4, 4, 1),
    (3, 3, 3),
)


def golden_headings(count: int, scale: int) -> list[list[int]]:
    ratio = (1 + 5**0.5) / 2
    result = []
    for i in range(count):
        z = 1 - 2 * (i + 0.5) / count
        radius = math.sqrt(1 - z * z)
        angle = 2 * math.pi * i / ratio
        heading = [
            round(scale * radius * math.cos(angle)),
            round(scale * radius * math.sin(angle)),
            round(scale * z),
        ]
        result.append(heading if any(heading) else [scale, 0, 0])
    return result


def path_count(x: int, y: int, z: int, source: int = OUTWARD_SOURCE) -> float:
    """Exact stock of the outward rule at one offset: octant share times multinomial hop orderings."""
    a, b, c = abs(x), abs(y), abs(z)
    radius = a + b + c
    zeros = (a == 0) + (b == 0) + (c == 0)
    return (
        source
        * 2**zeros
        / 8
        * factorial(radius)
        / (factorial(a) * factorial(b) * factorial(c))
        / 3**radius
    )


def outward_configuration() -> dict[str, Any]:
    raw = json.loads(OUTWARD_TEMPLATE.read_text(encoding="utf-8"))
    for kind in raw["disturbance_types"]:
        kind["transport"] = {"mode": "hold"}
        kind["defaults"]["strength"] = OUTWARD_SOURCE
    for emission in raw["emissions"]:
        emission.pop("budget", None)
    raw["ticks"] = OUTWARD_SHELL
    return raw


def ray_configuration(headings: int) -> dict[str, Any]:
    raw = json.loads(RAY_TEMPLATE.read_text(encoding="utf-8"))
    for kind in raw["disturbance_types"]:
        kind["transport"] = {"mode": "hold"}
        kind["defaults"]["strength"] = RAY_UNITS * RAYS_PER_TICK
    field = raw["spatial_fields"][0]
    field["headings"] = golden_headings(headings, RAY_SCALE)
    field["rays_per_tick"] = RAYS_PER_TICK
    field["ray_slots"] = 4096
    raw["ticks"] = RAY_WARMUP + headings // RAYS_PER_TICK
    return raw


def _run(
    raw: dict[str, Any], output: Path, name: str
) -> tuple[Path, list[dict[str, Any]], dict[str, Any]]:
    case_dir = output / name
    if case_dir.exists():
        shutil.rmtree(case_dir)
    output.mkdir(parents=True, exist_ok=True)
    initialization = output / (name + ".json")
    initialization.write_text(json.dumps(raw) + "\n", encoding="utf-8")
    run_initialization(initialization, case_dir, visualize=True)
    report = json.loads((case_dir / "run.json").read_text(encoding="utf-8"))
    assert report["status"] == "completed", report["error"]
    document = (case_dir / "run.html").read_text(encoding="utf-8")
    start = document.find('{"frames"')
    recording, _ = json.JSONDecoder().raw_decode(document[start:])
    return case_dir, recording["frames"], report


def _values(frame: dict[str, Any], field: str) -> dict[tuple[int, int, int], int]:
    return {
        tuple(node["position"]): int(node["fields"][field]["value"][0])
        for node in frame.get("spatial_fields", [])
    }


def outward_probe(output: Path) -> dict[str, Any]:
    """Pointwise stock on the Manhattan shell R = 9 against the path count and against isotropy."""
    raw = outward_configuration()
    center = tuple(raw["seeds"][0]["position"])
    case_dir, frames, report = _run(raw, output, "outward_shell")
    values = _values(frames[OUTWARD_SHELL], "radiation")
    shell = [
        (x, y, z)
        for x in range(-OUTWARD_SHELL, OUTWARD_SHELL + 1)
        for y in range(-OUTWARD_SHELL, OUTWARD_SHELL + 1)
        for z in range(-OUTWARD_SHELL, OUTWARD_SHELL + 1)
        if abs(x) + abs(y) + abs(z) == OUTWARD_SHELL
    ]
    measured = [values.get((center[0] + x, center[1] + y, center[2] + z), 0) for x, y, z in shell]
    mean = sum(measured) / len(shell)
    diagonal = values.get((center[0] + 3, center[1] + 3, center[2] + 3), 0)
    diagonal_r = math.sqrt(27)
    rows = []
    for point in OUTWARD_POINTS:
        x, y, z = point
        r = math.sqrt(x * x + y * y + z * z)
        stock = values.get((center[0] + x, center[1] + y, center[2] + z), 0)
        isotropic = diagonal * (diagonal_r / r) ** 2
        rows.append(
            {
                "offset": list(point),
                "euclidean_r": round(r, 3),
                "measured": stock,
                "path_count": round(path_count(x, y, z), 3),
                "isotropic_expectation": round(isotropic, 1),
                "measured_over_isotropic": round(stock / isotropic, 4),
            }
        )
    assert all(row["measured"] == round(row["path_count"]) for row in rows), rows
    axis5 = values.get((center[0] + 5, center[1], center[2]), 0)
    return {
        "case": case_dir.name,
        "source_per_tick": OUTWARD_SOURCE,
        "shell": OUTWARD_SHELL,
        "shell_nodes": len(shell),
        "shell_mean_measured": round(mean, 3),
        "shell_mean_predicted": round(OUTWARD_SOURCE / (4 * OUTWARD_SHELL**2 + 2), 3),
        "shell_min": min(measured),
        "shell_max": max(measured),
        "points": rows,
        "same_euclidean_distance_5": {
            "axis_5_0_0": axis5,
            "body_diagonal_3_3_3": diagonal,
            "diagonal_over_axis": round(diagonal / max(axis5, 1), 3),
        },
        "elapsed_seconds": report["elapsed_seconds"],
    }


def ray_probe(output: Path, headings: int) -> dict[str, Any]:
    """Field summed over one full heading sweep on the Euclidean shell r = 8, node by node."""
    raw = ray_configuration(headings)
    center = tuple(raw["seeds"][0]["position"])
    case_dir, frames, report = _run(raw, output, f"rays_{headings}")
    sweep = headings // RAYS_PER_TICK
    shell = [
        (x, y, z)
        for x in range(-10, 11)
        for y in range(-10, 11)
        for z in range(-10, 11)
        if abs(math.sqrt(x * x + y * y + z * z) - RAY_RADIUS) < 0.5
    ]
    totals = dict.fromkeys(shell, 0)
    for frame in frames[RAY_WARMUP + 1 : RAY_WARMUP + 1 + sweep]:
        values = _values(frame, "radiation")
        for x, y, z in shell:
            totals[(x, y, z)] += values.get((center[0] + x, center[1] + y, center[2] + z), 0)
    counts = [totals[p] / RAY_UNITS for p in shell]
    mean = statistics.fmean(counts)
    spread = statistics.pstdev(counts) / mean if mean else float("inf")
    axis = [totals[p] / RAY_UNITS for p in shell if sum(1 for c in p if c == 0) == 2]
    diagonal = [
        totals[p] / RAY_UNITS for p in shell if min(abs(c) for c in p) >= 0.6 * max(abs(c) for c in p)
    ]
    expected_rays = headings * len(shell) / (4 * math.pi * RAY_RADIUS**2) / len(shell)
    return {
        "case": case_dir.name,
        "headings": headings,
        "sweep_ticks": sweep,
        "shell_radius": RAY_RADIUS,
        "shell_nodes": len(shell),
        "rays_per_node_per_sweep_mean": round(mean, 3),
        "rays_per_node_expected_from_solid_angle": round(expected_rays, 3),
        "relative_spread": round(spread, 4),
        "poisson_spread_for_that_mean": round(1 / math.sqrt(mean), 4) if mean else None,
        "nodes_never_reached": sum(1 for c in counts if c == 0),
        "axis_mean": round(statistics.fmean(axis), 3) if axis else None,
        "body_diagonal_mean": round(statistics.fmean(diagonal), 3) if diagonal else None,
        "elapsed_seconds": report["elapsed_seconds"],
    }


def run_experiment(output: Path, heading_counts=HEADING_COUNTS) -> dict[str, Any]:
    outward = outward_probe(output)
    rays = [ray_probe(output, count) for count in heading_counts]
    return {
        "status": "pass",
        "outward": outward,
        "rays": rays,
        "reading": [
            "Outward rule: pointwise stock equals the multinomial path count exactly; at equal Euclidean distance the body diagonal carries several times the axis, and the axis falls off exponentially with radius.",
            "Ray rule: the mean per Node follows the solid angle, and the spread between Nodes is the counting spread of a few integer rays per Node; it shrinks with the square root of the headings per Node.",
            "Neither rule is isotropic pointwise at finite resolution; only the ray rule approaches isotropy, at a cost in headings that grows with the square of the radius and the inverse square of the wanted precision.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--headings", type=int, nargs="*", default=list(HEADING_COUNTS))
    args = parser.parse_args()
    out = args.output.resolve()
    validate_output_path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("use a new or empty output directory")
    out.mkdir(parents=True, exist_ok=True)
    summary = out / "summary.json"
    summary.touch()
    with ArtifactLease(out, [summary]):
        result = run_experiment(out, tuple(args.headings))
        summary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "outward_diagonal_over_axis": result["outward"]["same_euclidean_distance_5"][
                    "diagonal_over_axis"
                ],
                "rays": [
                    (
                        r["headings"],
                        r["relative_spread"],
                        r["rays_per_node_per_sweep_mean"],
                        r["elapsed_seconds"],
                    )
                    for r in result["rays"]
                ],
            }
        )
    )


if __name__ == "__main__":
    main()

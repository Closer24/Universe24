"""THE ONE-CLICK HEALTH LOOK'S READING (the owner's word of 2026-09-28, 07:06 Israel time): the world of `lay_out_one_click.py` run headless through the engine's own functions, every interval's declared readings kept up to the run's end or its refusal (the refusal's line is part of the report), and the five things read from them: (1) the record is written at the giving on the giver's Nodes and moves (the light's support and centroid per rows line, GAMEBOARD); (2) its wavelength along the beam by the sign changes of the level between the giver and the window, and its group velocity by the centroid's motion (GAMEBOARD); (3) its largest level against the amplitude bound on every rows line (GAMEBOARD); (4) the levels before and behind the window and the mirror (GAMEBOARD); (5) the strip's click and its interval since the giving against the distance over the group velocity read in (2) (DETECTOR, the one measurement). No closed form of the law is computed here: the expected wavelength and velocity are Cheshbon's numbers in the report's `expected` field where the expectation file beside the world carries them. Run from the repository root: PYTHONPATH=src python examples/events/experiments/de_broglie/one_click.py <world.json>; the report is written beside the world as `<name>.health.json`."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from event_universe.core.readings import Readings
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import load_world


def run(world_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], str | None]:
    """The run with the event lines observed and the readings taken every interval; the refusal's text where the run is refused, else None."""
    world = load_world(world_path)
    lines: list[dict[str, Any]] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    readings = Readings(world.readings)
    readings.read(simulation)
    refusal = None
    for _ in range(world.ticks):
        try:
            simulation.step()
        except (RuntimeError, ValueError) as stop:
            refusal = f"at interval {simulation.tick + 1}: {stop}"
            break
        readings.read(simulation)
    readings.clicks(simulation.layer.gathers)
    output = {
        "verdict": "LAWFUL" if refusal is None else "REFUSED IN THE RUN",
        "ticks_run": simulation.tick,
        "readings": readings.output(),
        "amplitude_bound": int(world.amplitude_bound) if hasattr(world, "amplitude_bound") else None,
        "clicks": [
            {
                "detector": g["chosen"],
                "interval": g["tick"],
                "giving": g["giving"],
            }
            for g in simulation.layer.gathers
        ],
    }
    return output, lines, refusal


def rows_of(output: dict[str, Any], name: str) -> list[dict[str, Any]]:
    """The lines of the named reading."""
    for reading in output["readings"]:
        if reading["name"] == name:
            return list(reading["lines"])
    return []


def centroid_and_extent(row: list[int], shape: list[int]) -> tuple[float | None, int, int]:
    """The centroid along x of |level| over the board, the largest |level|, and the count of Nodes with a level (GAMEBOARD)."""
    weights = [abs(v) for v in row]
    total = sum(weights)
    if total == 0:
        return None, 0, 0
    xs = [i // (shape[1] * shape[2]) for i in range(len(row))]
    return (
        sum(x * w for x, w in zip(xs, weights, strict=True)) / total,
        max(weights),
        sum(1 for w in weights if w),
    )


def wavelength_along(row: list[int], shape: list[int], y: int, x0: int, x1: int) -> float | None:
    """Twice the mean spacing of the sign changes of the level along the beam's row between x0 and x1 (GAMEBOARD): the wavelength in Links, None with fewer than two sign changes."""
    line = [row[(x * shape[1] + y) * shape[2]] for x in range(x0, x1 + 1)]
    crossings = [x0 + i for i in range(1, len(line)) if line[i - 1] * line[i] < 0]
    if len(crossings) < 2:
        return None
    return 2 * (crossings[-1] - crossings[0]) / (len(crossings) - 1)


def report(world_path: Path) -> dict[str, Any]:
    """The five readings of the health look, written beside the world."""
    document = json.loads(world_path.read_text(encoding="utf-8"))
    output, lines, refusal = run(world_path)
    shape = document["shape"]
    beam_y = (
        document["detectors"][0]["positions"][0][1] + len(document["detectors"][0]["positions"]) // 2 - 1
    )
    giver = document["measured"][0]["nodes"]
    giver_far = max(n["node"][0] for n in giver)
    window_x = min(n["node"][0] for n in document["measured"][2]["nodes"])
    givings = [
        {
            "opened": line.get("window"),
            "closed": line["tick"],
            "outward": line.get("outward"),
            "norm_over_den": (line["norm"] // line["pace"]) if line.get("pace") else None,
        }
        for line in lines
        if line["event"] == "giving"
    ]
    rows = rows_of(output, "light_rows")
    path = []
    for line in rows:
        centre, largest, nodes = centroid_and_extent(line["rows"], shape)
        path.append(
            {
                "interval": line["interval"],
                "centroid_x": None if centre is None else round(centre, 2),
                "largest_level": largest,
                "nodes": nodes,
                "wavelength_links": wavelength_along(
                    line["rows"], shape, beam_y, giver_far + 1, window_x - 1
                ),
            }
        )
    moving = [p for p in path if p["centroid_x"] is not None]
    velocity = None
    if len(moving) >= 2:
        first, last = moving[0], moving[-1]
        if last["interval"] > first["interval"]:
            velocity = round(
                (last["centroid_x"] - first["centroid_x"]) / (last["interval"] - first["interval"]), 4
            )
    levels = {
        r["name"]: [(line["interval"], line["level"]) for line in r["lines"]]
        for r in output["readings"]
        if r["kind"] == "level"
    }
    clicks = [c for c in output["clicks"] if c["detector"] == "window_strip"]
    distance = window_x - giver_far
    return {
        "world": world_path.name,
        "kind": "ONE-CLICK HEALTH LOOK (a first look, GAMEBOARD but the strip's click)",
        "verdict": output["verdict"],
        "refusal": refusal,
        "ticks_run": output["ticks_run"],
        "1_written_and_moving": {"label": "GAMEBOARD", "givings_at": givings, "path": path},
        "2_wavelength_and_velocity": {
            "label": "GAMEBOARD",
            "wavelengths_links": [p["wavelength_links"] for p in path if p["wavelength_links"]],
            "centroid_velocity_links_per_interval": velocity,
        },
        "3_largest_level_against_A": {
            "label": "GAMEBOARD",
            "amplitude_bound": output["amplitude_bound"],
            "largest_level_per_line": [(p["interval"], p["largest_level"]) for p in path],
        },
        "4_window_and_mirror": {"label": "GAMEBOARD", "levels_along_the_beam": levels},
        "5_the_click": {
            "label": "DETECTOR",
            "clicks": clicks,
            "distance_giver_to_window_links": distance,
            "expected_interval_after_the_giving": None
            if not velocity
            else round(distance / velocity, 1),
        },
    }


def main() -> None:
    for argument in sys.argv[1:]:
        world_path = Path(argument).resolve()
        found = report(world_path)
        world_path.with_suffix(".health.json").write_text(
            json.dumps(found, indent=1) + "\n", encoding="utf-8"
        )
        shown = dict(found)
        shown["1_written_and_moving"] = {
            **found["1_written_and_moving"],
            "path": found["1_written_and_moving"]["path"][:12],
        }
        shown["4_window_and_mirror"] = {
            "label": "GAMEBOARD",
            "levels_along_the_beam": {
                k: v[:8] for k, v in found["4_window_and_mirror"]["levels_along_the_beam"].items()
            },
        }
        print(json.dumps(shown, indent=1))


if __name__ == "__main__":
    main()

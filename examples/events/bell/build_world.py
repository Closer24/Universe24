"""Bell's gate world (ALGEBRA.md row (h); the advisor's corrected instrument of 2026-09-30, #1563 comment 5918198102) from the design file beside this script: the near-field board of 48 rows, per side two lobes of the light family before a wall with two gaps of two wavelengths and a bar between them, the pair's angle laid as the relative phase of the two lobes (the mirror on the two sides) at the half-offset (k + 1/2) / K of the turn for the design's angle k, the screens at L beyond the walls in regions of rows backed by receding faces, tiled on each side's setting grid; the ports three regions of four rows about the central maximum and the two first minima, displaced by the setting; its mode file by the message lay (tools/pixel_mode.py, with --modes); and the blind expectation file, written before any run: the single-side pattern and its minima by the Huygens sum over the gaps' Nodes, and E, S and the efficiencies by the calibrated rule applied to that sum over the K run phases. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/bell/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from math import atan2, cos, degrees, pi, sin, sqrt
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SIDES = (("left", -1), ("right", 1))
SIDE_SETTINGS = {"left": "b", "right": "a"}


def regions(design: dict[str, Any], side: str) -> list[list[int]]:
    """A screen's regions of rows: from the side's first boundary (`tiling`) by `rows_per_region`, the rows before the first boundary and after the last folded into the edge regions so that no region is narrower than the size rule allows."""
    rows, height = int(design["rows_per_region"]), int(design["height"])
    first = int(design["tiling"][side])
    edges = list(range(first, height + 1, rows))
    if edges[0] > 0:
        edges[0] = 0
    if height - edges[-1] < rows:
        edges[-1] = height
    if edges[-1] != height:
        edges.append(height)
    return [list(range(start, stop)) for start, stop in zip(edges[:-1], edges[1:], strict=True)]


def world(design: dict[str, Any], angle: int) -> dict[str, object]:
    """The world file of the angle k: the board, the two symmetric walls with their gaps, per side the two lobes (the upper one at the phase (k + 1/2) / K of the turn on the right side and its mirror on the left), the screens' regions and the receding faces."""
    source, slab, height = int(design["source"]), int(design["slab"]), int(design["height"])
    p, q = (int(v) for v in design["wave"])
    turns = int(design["angles"])
    gaps = [{"y": list(gap), "z": [0, 0]} for gap in design["gaps"]]
    messages: list[dict[str, object]] = []
    for _side, sign in SIDES:
        top = source + sign * int(design["offset"])
        for index, lobe in enumerate(design["lobes"]):
            message: dict[str, object] = {
                "family": design["family"],
                "along": "x",
                "wave": [sign * p, q],
                "amplitude": int(design["amplitude"]),
                "top": {"x": [top, top], "y": [int(v) for v in lobe], "z": [0, 0]},
                "edge": {"x": int(design["edge_along"]), "y": int(design["edge_across"]), "z": 0},
            }
            if index:
                offset = 2 * angle + 1  # the half-offset (k + 1/2) / K as (2 k + 1) / (2 K)
                message["phase"] = [offset if sign > 0 else 2 * turns - offset, 2 * turns]
            messages.append(message)
    detectors = []
    for side, sign in SIDES:
        near = source + sign * int(design["screen"])
        columns = sorted(range(near, near + sign * slab, sign))
        for number, rows in enumerate(regions(design, side)):
            positions = [[x, y, 0] for y in rows for x in columns]
            detectors.append({"name": f"{side}_{number}", "positions": positions})
    return {
        "shape": [int(design["length"]), height, 1],
        "boundary": {"x": "open", "y": "open", "z": "periodic"},
        "face_depth": 1,
        "faces": [
            {"axis": "x", "at": source + sign * int(design["wall"]), "gaps": gaps}
            for _side, sign in SIDES
        ],
        "ticks": int(design["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [],
        "messages": messages,
        "detectors": detectors,
        "receding": design["receding"],
    }


def port_regions(design: dict[str, Any], side: str, shift: int) -> dict[str, list[str]]:
    """The names of the regions that make the two ports of a side at a setting: the + port the rows about the centre and the - port the rows about the two first minima, each displaced by the setting's shift in rows; a port's rows must be whole regions of the side's tiling, refused by name otherwise."""
    tiles = {tuple(rows): f"{side}_{number}" for number, rows in enumerate(regions(design, side))}
    ports = design["ports"]
    wanted = {"plus": [ports["plus"]], "minus": [list(pair) for pair in ports["minus"]]}
    found: dict[str, list[str]] = {}
    for port, spans in wanted.items():
        names = []
        for first, last in spans:
            rows = tuple(range(int(first) + shift, int(last) + shift + 1))
            if rows not in tiles:
                raise ValueError(
                    f"the {port} port of {side} at the shift {shift} is not a region: rows {rows}"
                )
            names.append(tiles[rows])
        found[port] = names
    return found


def huygens(design: dict[str, Any], phase: float, sign: int) -> list[float]:
    """The single-side pattern at the screen by the Huygens sum in two dimensions: every Node of each gap a source at the wall, the upper gap's sources at the relative phase (the pair's angle on the right, its mirror on the left), the field at each screen row the sum of e^(i k r) / sqrt r, the intensity its square; no number of the engine, the design's alone."""
    p, q = (int(v) for v in design["wave"])
    k = pi * p / q
    distance = float(int(design["screen"]) - int(design["wall"]))
    pattern = []
    for row in range(int(design["height"])):
        real = imaginary = 0.0
        for index, (first, last) in enumerate(design["gaps"]):
            turn = sign * phase if index else 0.0
            for source in range(int(first), int(last) + 1):
                r = sqrt(distance * distance + (row - source) ** 2)
                real += cos(k * r + turn) / sqrt(r)
                imaginary += sin(k * r + turn) / sqrt(r)
        pattern.append(real * real + imaginary * imaginary)
    return pattern


def minima_of(pattern: list[float]) -> list[int]:
    """The rows of the pattern's local minima."""
    return [
        row
        for row in range(1, len(pattern) - 1)
        if pattern[row] < pattern[row - 1] and pattern[row] < pattern[row + 1]
    ]


def phase_of(difference: list[float], turns: int, sign: int) -> float:
    """A setting's phase in radians from the calibrated difference over the run phases (k + 1/2) / turns of the turn (the mirror on the left), fitted to A cos(u - delta) by its first harmonic, as the reader calibrates it (the advisor, #1563 comment 5918622391)."""
    angles = [sign * 2 * pi * (k + 0.5) / turns for k in range(turns)]
    along = sum(d * cos(u) for d, u in zip(difference, angles, strict=True))
    across = sum(d * sin(u) for d, u in zip(difference, angles, strict=True))
    return atan2(across, along)


def side_reading(
    design: dict[str, Any], side: str, shift: int
) -> tuple[list[float], list[float], list[int], float]:
    """The calibrated rule on the Huygens sum for one side at one setting over the K run phases: the light in the ports, the contrast (the calibrated difference over its half swing), the outcome (its sign) and the setting's calibrated phase."""
    sign = dict(SIDES)[side]
    turns = int(design["angles"])
    plus_rows = list(
        range(int(design["ports"]["plus"][0]) + shift, int(design["ports"]["plus"][1]) + shift + 1)
    )
    minus_rows = [
        row
        for first, last in design["ports"]["minus"]
        for row in range(int(first) + shift, int(last) + shift + 1)
    ]
    plus, minus = [], []
    for angle in range(turns):
        pattern = huygens(design, 2 * pi * (2 * angle + 1) / (2 * turns), sign)
        plus.append(sum(pattern[row] for row in plus_rows))
        minus.append(sum(pattern[row] for row in minus_rows))
    mean_plus, mean_minus = sum(plus) / turns, sum(minus) / turns
    difference = [a / mean_plus - b / mean_minus for a, b in zip(plus, minus, strict=True)]
    half_swing = (max(difference) - min(difference)) / 2
    light = [a + b for a, b in zip(plus, minus, strict=True)]
    contrast = [abs(d) / half_swing if half_swing else 0.0 for d in difference]
    outcome = [1 if d > 0 else -1 if d < 0 else 0 for d in difference]
    return light, contrast, outcome, phase_of(difference, turns, sign)


def blind_row(design: dict[str, Any]) -> dict[str, Any]:
    """The blind numbers from the Huygens sum: the u = 0 pattern with its minima; by the reader's own rule E at the four settings, S and the efficiency per side and setting; and the settings' calibrated phases with E = cos(delta_A + delta_B) at them and S from those cosines (the advisor, 5918622391: the row of the paper, nature's law in the polariser's angles with the instrument's angles the calibrated ones)."""
    pattern = huygens(design, 0.0, 1)
    top = max(pattern)
    settings = {side: [int(v) for v in design["settings"][SIDE_SETTINGS[side]]] for side, _s in SIDES}
    by = {design["sign"]: "sign", design["contrast"]: "contrast"}
    sides = {
        side: {shift: side_reading(design, side, shift) for shift in settings[side]} for side in settings
    }
    correlation: dict[str, float] = {}
    efficiency: dict[str, dict[str, float]] = {side: {} for side in settings}
    cosines: dict[str, float] = {}
    for shift_a in settings["right"]:
        light_a, contrast_a, outcome_a, phase_a = sides["right"][shift_a]
        for shift_b in settings["left"]:
            light_b, contrast_b, outcome_b, phase_b = sides["left"][shift_b]
            cosines[f"{shift_a} {shift_b}"] = cos(phase_a + phase_b)
            clicks_a = [
                n * (c if by["right"] == "contrast" else 1.0)
                for n, c in zip(light_a, contrast_a, strict=True)
            ]
            clicks_b = [
                n * (c if by["left"] == "contrast" else 1.0)
                for n, c in zip(light_b, contrast_b, strict=True)
            ]
            weights = [min(x, y) for x, y in zip(clicks_a, clicks_b, strict=True)]
            product = sum(oa * ob * w for oa, ob, w in zip(outcome_a, outcome_b, weights, strict=True))
            correlation[f"{shift_a} {shift_b}"] = product / sum(weights)
    for side, shifts in sides.items():
        for shift, (light, contrast, _outcome, _phase) in shifts.items():
            credited = sum(
                n * (c if by[side] == "contrast" else 1.0) for n, c in zip(light, contrast, strict=True)
            )
            efficiency[side][str(shift)] = credited / sum(light)
    (a, a_prime), (b, b_prime) = settings["right"], settings["left"]
    s_value = (
        correlation[f"{a} {b}"]
        - correlation[f"{a} {b_prime}"]
        + correlation[f"{a_prime} {b}"]
        + correlation[f"{a_prime} {b_prime}"]
    )
    s_cosines = (
        cosines[f"{a} {b}"]
        - cosines[f"{a} {b_prime}"]
        + cosines[f"{a_prime} {b}"]
        + cosines[f"{a_prime} {b_prime}"]
    )
    return {
        "pattern": [round(value / top, 3) for value in pattern],
        "minima": minima_of(pattern),
        "correlation": {key: round(value, 3) for key, value in correlation.items()},
        "S": round(s_value, 3),
        "efficiency": {
            side: {k: round(v, 3) for k, v in values.items()} for side, values in efficiency.items()
        },
        "phases": {
            side: {str(shift): round(degrees(values[3]), 1) for shift, values in shifts.items()}
            for side, shifts in sides.items()
        },
        "cosines": {key: round(value, 3) for key, value in cosines.items()},
        "S_cosines": round(s_cosines, 3),
        "bound": 2.0,
    }


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file: the sides' regions with their rows, per side and setting the regions of the two ports, which side credits by the sign (A) and which by the contrast (B), the settings in rows and in degrees of fringe phase, and the blind row from the Huygens sum."""
    spacing = int(design["spacing"])
    settings = {side: [int(v) for v in design["settings"][SIDE_SETTINGS[side]]] for side, _s in SIDES}
    return {
        "comment": design["blind_comment"],
        "verdict": "DETECTOR",
        "family": design["family"],
        "across": "y",
        "sides": {
            side: {f"{side}_{number}": rows for number, rows in enumerate(regions(design, side))}
            for side, _sign in SIDES
        },
        "ports": {
            side: {str(shift): port_regions(design, side, shift) for shift in shifts}
            for side, shifts in settings.items()
        },
        "sign": design["sign"],
        "contrast": design["contrast"],
        "quanta": None,
        "spacing": spacing,
        "settings": settings,
        "degrees": {
            side: [shift * 360 // spacing for shift in shifts] for side, shifts in settings.items()
        },
        "blind": blind_row(design),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the world written")
    parser.add_argument(
        "--modes", action="store_true", help="write the mode file too (tools/pixel_mode.py)"
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    angle = int(design["angle"])
    path = args.folder / f"bell_{angle}.json"
    document = world(design, angle)
    path.write_text(json.dumps(document) + "\n", encoding="utf-8")
    if args.modes:
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)],
            check=True,
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
        )
    print(json.dumps({"world": str(path), "angle": angle, "detectors": len(document["detectors"])}))
    blind = args.folder / "expectation.json"
    blind.write_text(json.dumps(expectation(design), indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(blind)}))


if __name__ == "__main__":
    main()

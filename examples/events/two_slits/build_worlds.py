"""The two slits' three worlds (ALGEBRA.md row (g); the advisor's design at the owner's word of 2026-09-30, #1515 comment 5912573191) from the design file beside this script: the bright world as run, the dilute world and the which-way world, each with the screen declared as regions of four rows backed by a receding face, the which-way world with one gap closed and an opaque detector before it; their mode files by the message lay (tools/pixel_mode.py); and the blind expectation file of each, per region, written before any run. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/two_slits/build_worlds.py [--design <design>.json] [--folder <folder>]
"""

from __future__ import annotations

import argparse
import cmath
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def screen_regions(design: dict[str, Any]) -> list[dict[str, object]]:
    """The screen's detectors: the column `screen` in regions of `rows_per_region` rows, named screen_0 upward."""
    rows, column = int(design["rows_per_region"]), int(design["screen"])
    return [
        {
            "name": f"screen_{index}",
            "positions": [[column, row, 0] for row in range(first, first + rows)],
        }
        for index, first in enumerate(range(0, int(design["height"]), rows))
    ]


def world(design: dict[str, Any], amplitude: int, which_way: bool) -> dict[str, object]:
    """One world file: the board, the wall (both gaps, or one closed for the which-way world), the packet, the screen's regions, in the worlds with both gaps open the bare region `gap` behind the watched gap (what arrives there, the which-way detector's credit read where nothing reflects it back), the receding face, the ticks."""
    gaps = [{"y": list(gap), "z": [0, 0]} for gap in design["gaps"]]
    detectors = screen_regions(design)
    closed = int(design["which_way"]["closed"])
    if which_way:
        gaps = [gap for index, gap in enumerate(gaps) if index != closed]
    else:
        region = design["which_way"][
            "detector"
        ]  # a bare region behind the watched gap: what arrives there
        detectors.append(
            {
                "name": "gap",
                "positions": [
                    [x, y, 0]
                    for x in range(int(region["columns"][0]), int(region["columns"][1]) + 1)
                    for y in range(int(region["rows"][0]), int(region["rows"][1]) + 1)
                ],
            }
        )
    packet = design["packet"]
    return {
        "shape": [int(design["length"]), int(design["height"]), 1],
        "boundary": {"x": "open", "y": "open", "z": "periodic"},
        "face_depth": 1,
        "faces": [{"axis": "x", "at": int(design["wall"]), "gaps": gaps}],
        "ticks": int(design["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [],
        "messages": [
            {
                "family": design["family"],
                "along": "x",
                "wave": list(design["wave"]),
                "amplitude": amplitude,
                "top": {
                    "x": [packet["column"], packet["column"]],
                    "y": list(packet["across"]),
                    "z": [0, 0],
                },
                "edge": {"x": int(packet["edge_along"]), "y": int(packet["edge_across"]), "z": 0},
            }
        ],
        "detectors": detectors,
        "receding": design["receding"],
    }


def per_region(row: list[float], rows: int) -> list[float]:
    """A per-Node row summed per region of `rows` Nodes."""
    return [sum(row[first : first + rows]) for first in range(0, len(row), rows)]


def envelope(design: dict[str, Any], gap: list[int]) -> list[float]:
    """The open gap's envelope on the screen, per Node of the screen's column: the Huygens sum from the gap's Nodes at the design's wavelength with the obliquity factor L / r, the Boss's computation of the blind row for the which-way world (no fringes, one gap)."""
    wave = design["wave"]
    k = math.pi * wave[0] / wave[1]
    distance = int(design["screen"]) - int(design["wall"])
    found = []
    for y in range(int(design["height"])):
        total = 0j
        for source in range(gap[0], gap[1] + 1):
            r = math.hypot(distance, y - source)
            total += cmath.exp(1j * k * r) / math.sqrt(r) * (distance / r)
        found.append(abs(total) ** 2)
    return found


def rounded(row: list[float]) -> list[float]:
    """A blind row to one decimal."""
    return [round(value, 1) for value in row]


def expectations(design: dict[str, Any]) -> dict[str, dict[str, object]]:
    """The three blind expectation files, per region (DETECTOR, written before the run, as tools/click_counts.py reads them): the bright world's the advisor's per-Node row summed per region; the dilute world's the same shares over its own passing count (the laid count's ratio); the which-way world's the open gap's envelope summed per region, its total the open gap's half of the two gaps' passing count and no fringes, and the gap detector's blind credit about half the passing count."""
    rows = int(design["rows_per_region"])
    names = [detector["name"] for detector in screen_regions(design)]
    blind = per_region([float(v) for v in design["blind_per_node"]], rows)
    through = float(design["blind_through"])
    first, last = design["pattern"]
    maxima = [
        index
        for index in range(first, last + 1)
        if 0 < index < len(blind) - 1
        and blind[index] > blind[index - 1]
        and blind[index] >= blind[index + 1]
    ]
    minima = [
        index
        for index in range(first, last + 1)
        if 0 < index < len(blind) - 1
        and blind[index] < blind[index - 1]
        and blind[index] <= blind[index + 1]
    ]
    base = {
        "verdict": "DETECTOR",
        "detector": names,
        "family": design["family"],
        "window": list(design["window"]),
        "across": "y",
        "pattern": [first, last],
        "spacing": design["spacing"],
        "seed": design["seed"],
    }
    dilute_ratio = int(design["laid"]["dilute"]) / int(design["laid"]["bright"])
    closed = int(design["which_way"]["closed"])
    open_gap = [gap for index, gap in enumerate(design["gaps"]) if index != closed][0]
    shape = per_region(envelope(design, list(open_gap)), rows)
    one_gap = through / 2
    which = [value * one_gap / sum(shape) for value in shape]
    return {
        "expectation": {
            **base,
            "comment": "The bright world's blind row per region of four rows (the advisor's per-Node row, #1515 comment 5903745976, summed by four; ALGEBRA.md row (g)): the clicks per region N times the region's share, the fringes at the spacing 16 with the visibility 1, the total N the passing count, the draw's scatter sqrt(N p (1 - p)) per region; the credit by the shares of the seen inflows with the seed, the instrument's.",
            "counts": rounded(blind),
            "through": through,
            "maxima": maxima,
            "minima": minima,
            "quanta": through,
            "laid": int(design["laid"]["bright"]),
            "aside": ["gap"],
        },
        "expectation_dilute": {
            **base,
            "comment": "The dilute world's blind row per region: the bright row's shares over the dilute packet's own passing count (the laid counts' ratio), the pattern rising click by click as Born by the credit's draw, the instrument's declaration; no rise of the count's line at the screen is expected on the board itself, the credit reading the seen inflows.",
            "counts": rounded([value * dilute_ratio for value in blind]),
            "through": round(through * dilute_ratio, 1),
            "maxima": maxima,
            "minima": minima,
            "quanta": round(through * dilute_ratio, 1),
            "laid": int(design["laid"]["dilute"]),
        },
        "expectation_which_way": {
            **base,
            "comment": "The which-way world's blind row per region: the open gap's envelope alone (the Boss's Huygens sum from the gap's Nodes at lambda = 8 with the obliquity factor), no fringes, its total the open gap's half of the two gaps' passing count; the gap detector before the closed gap credited about that half beside it; the as-run identical row reversed (the advisor's design, #1515 comment 5912573191).",
            "counts": rounded(which),
            "through": round(one_gap, 1),
            "maxima": [],
            "minima": [],
            "quanta": round(one_gap, 1),
            "laid": int(design["laid"]["bright"]),
            "gap": {
                "detector": "gap",
                "credit": round(one_gap, 1),
                "read_in": "two_slits (the bare region behind the open gap, `aside`)",
            },
        },
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    worlds = {
        "two_slits": world(design, int(design["amplitude"]["bright"]), False),
        "two_slits_dilute": world(design, int(design["amplitude"]["dilute"]), False),
        "two_slits_which_way": world(design, int(design["amplitude"]["bright"]), True),
    }
    for name, document in worlds.items():
        path = args.folder / f"{name}.json"
        path.write_text(json.dumps(document) + "\n", encoding="utf-8")
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)],
            check=True,
            cwd=ROOT,
        )
        print(json.dumps({"world": str(path), "detectors": len(document["detectors"])}))
    for name, document in expectations(design).items():
        (args.folder / f"{name}.json").write_text(
            json.dumps(document, indent=1) + "\n", encoding="utf-8"
        )
        print(
            json.dumps(
                {"expectation": name, "counts": document["counts"], "through": document["through"]}
            )
        )


if __name__ == "__main__":
    main()

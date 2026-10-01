"""The two slits' world (ALGEBRA.md row (g); the advisor's design at the owner's word of 2026-09-30, #1515 comment 5912573191) from the design file beside this script: the bright world as run, the screen declared as regions of four rows backed by a receding face and a bare region behind one gap read beside the screen; its mode file by the message lay (tools/pixel_mode.py); and its blind expectation file, per region, written before any run. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/two_slits/build_world.py [--design <design>.json] [--folder <folder>]
"""

from __future__ import annotations

import argparse
import json
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


def world(design: dict[str, Any]) -> dict[str, object]:
    """The world file: the board, the wall with its two gaps, the packet, the screen's regions, the bare region `aside` behind one gap (what arrives there, read beside the screen and taking no share), the receding face, the ticks."""
    gaps = [{"y": list(gap), "z": [0, 0]} for gap in design["gaps"]]
    detectors = screen_regions(design)
    region = design["aside"]
    detectors.append(
        {
            "name": str(region["name"]),
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
                "amplitude": int(design["amplitude"]),
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


def rounded(row: list[float]) -> list[float]:
    """A blind row to one decimal."""
    return [round(value, 1) for value in row]


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file, per region (DETECTOR, written before the run, as tools/click_counts.py reads it): the advisor's per-Node row summed per region, its total the passing count, its maxima and minima within the pattern's range, the laid count and the bare region read beside the screen."""
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
    return {
        "verdict": "DETECTOR",
        "detector": names,
        "family": design["family"],
        "window": list(design["window"]),
        "across": "y",
        "pattern": [first, last],
        "spacing": design["spacing"],
        "seed": design["seed"],
        "comment": "The bright world's blind row per region of four rows (the advisor's per-Node row, #1515 comment 5903745976, summed by four; ALGEBRA.md row (g)): the clicks per region N times the region's share, the fringes at the spacing 16 with the visibility 1, the total N the passing count, the draw's scatter sqrt(N p (1 - p)) per region; the credit by the shares of the seen inflows with the seed, the instrument's.",
        "counts": rounded(blind),
        "through": through,
        "maxima": maxima,
        "minima": minima,
        "quanta": through,
        "laid": int(design["laid"]),
        "aside": [str(design["aside"]["name"])],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the world written")
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    document = world(design)
    path = args.folder / "two_slits.json"
    path.write_text(json.dumps(document) + "\n", encoding="utf-8")
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)],
        check=True,
        cwd=ROOT,
    )
    print(json.dumps({"world": str(path), "detectors": len(document["detectors"])}))
    blind = expectation(design)
    (args.folder / "expectation.json").write_text(json.dumps(blind, indent=1) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"expectation": "expectation", "counts": blind["counts"], "through": blind["through"]}
        )
    )


if __name__ == "__main__":
    main()

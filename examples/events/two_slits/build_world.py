"""The two slits' world (ALGEBRA.md row (g); the advisor's design at the owner's word of 2026-09-30, #1515 comment 5912573191, with the fixes of the owner's word of 2026-10-01, 04:50) from the design file beside this script: the bright world as run, the screen declared as regions of four rows backed by a receding face, the source's face receding too, and a bare region behind one gap read beside the screen; its mode file by the message lay (tools/pixel_mode.py); and its blind expectation file, per region, written before any run: the blind row with its central maximum and the first minima about it, the blind visibility, the arrival wager and the wings from the design, `laid` the generator's count of the lay from the mode file. Every number is the design's or the generator's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/two_slits/build_world.py [--design <design>.json] [--folder <folder>]
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from click_counts import extrema  # noqa: E402  # the one extrema rule, the reader's and the builder's


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
        "instrument": design["instrument"],
    }


def per_region(row: list[float], rows: int) -> list[float]:
    """A per-Node row summed per region of `rows` Nodes."""
    return [sum(row[first : first + rows]) for first in range(0, len(row), rows)]


def rounded(row: list[float]) -> list[float]:
    """A blind row to one decimal."""
    return [round(value, 1) for value in row]


def first_minima(blind: list[float], maxima: list[int], minima: list[int]) -> tuple[int, list[int]]:
    """The blind central maximum, the maximum nearest the pattern's centre, and the two first minima about it, the minima nearest it on either side (the regions 4 and 8 of the bright row; the edge ripple's minima are no interference minima)."""
    central = min(maxima, key=lambda at: abs(2 * at - (len(blind) - 1)))
    return central, [max(at for at in minima if at < central), min(at for at in minima if at > central)]


def expectation(design: dict[str, Any], laid: int) -> dict[str, object]:
    """The blind expectation file, per region (DETECTOR, written before the run, as tools/click_counts.py reads it): the advisor's per-Node row summed per region, its total N's blind, its maxima within the pattern's range, the central maximum with the first minima about it and the blind visibility there, the arrival wager and the wings from the design, `laid` the generator's count of the lay and the bare region read beside the screen."""
    rows = int(design["rows_per_region"])
    names = [detector["name"] for detector in screen_regions(design)]
    blind = per_region([float(v) for v in design["blind_per_node"]], rows)
    through = float(design["blind_through"])
    first, last = design["pattern"]
    maxima, minima = extrema(blind, first, last)
    central, first_two = first_minima(blind, maxima, minima)
    most, low = blind[central], sum(blind[at] for at in first_two)
    return {
        "verdict": "DETECTOR",
        "detector": names,
        "family": design["family"],
        "window": list(design["window"]),
        "across": "y",
        "pattern": [first, last],
        "spacing": design["spacing"],
        "seed": design["seed"],
        "comment": "The bright world's blind row per region of four rows (the advisor's per-Node row, #1515 comment 5903745976, the Huygens sum summed by four; ALGEBRA.md row (g)): the rounded shares per region N times the region's share, the expectation, and the clicks one draw of N by the shares with the seed, the instrument's, with the draw's scatter sqrt(N p (1 - p)) per region; the near field, the first minima at the rows 15.3 and 32.7 (the regions 4 and 8 of the twelve, the visibility read there against the central maximum, the region 6) and the outer maxima at the edges; `quanta` is N's blind, the Huygens total 273, the twelve counts summing to 275 by their rounding; `laid` the generator's count of the lay; the arrival of the clicks in the engine's labels and the wings the lattice's own numbers; a region's seen inflow floored at 0 before the shares; written before the run and never touched after. Status: the row computed from the Huygens sum (1.7 percent under the law's own real line with the source side absorbing over the whole passage, 277.8), the arrival and the wings computed from the law's line over the same passage; fence: clicks.",
        "counts": rounded(blind),
        "through": through,
        "maxima": maxima,
        "minima": first_two,
        "central": central,
        "visibility": [round(most * len(first_two) - low, 1), round(most * len(first_two) + low, 1)],
        "quanta": through,
        "counts_sum": round(sum(blind), 1),
        "laid": laid,
        "arrival": design["arrival"],
        "wings": design["wings"],
        "aside": [str(design["aside"]["name"])],
        "photons": {
            "label": "GAMEBOARD",
            "per_count": round(
                1
                / math.sqrt(
                    1 - ((math.cos(math.pi * design["wave"][0] / design["wave"][1]) + 2) / 3) ** 2
                ),
                4,
            ),
            "at_the_blind_N": round(
                through
                / math.sqrt(
                    1 - ((math.cos(math.pi * design["wave"][0] / design["wave"][1]) + 2) / 3) ** 2
                ),
                1,
            ),
            "status": "the photon count at the light's own omega beside N, a GameBoard reading and no fence: the screen's regions declare the band's top [0, den], so N counts the energy in units of T, and one quantum of the laid light at k = pi / 4 (cos omega = (cos(pi / 4) + 2) / 3, sin omega = 0.4310) carries T sin omega; N over sin omega is the laid light's own quanta, 645 at N = 278 (the mathematician's 214, #1572 comment 5965082449, with the advisor's second, #1563 comment 5965316267; the shipped regions keep the band's top so that no gate number moves)",
        },
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
    mode = json.loads((args.folder / "two_slits.mode.json").read_text(encoding="utf-8"))
    laid = sum(int(message["count"]) for message in mode["messages"])  # the generator's count
    blind = expectation(design, laid)
    (args.folder / "expectation.json").write_text(json.dumps(blind, indent=1) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"expectation": "expectation", "counts": blind["counts"], "through": blind["through"]}
        )
    )


if __name__ == "__main__":
    main()

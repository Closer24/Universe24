"""Bell's worlds under the new laws (ALGEBRA.md row (h); the advisor's design at the owner's word of 2026-09-30, #1515 comments 5912573191 and 5911802610) from the design file beside this script: one world per angle, the pair's angle laid as the relative phase of the two lobes through the two gaps (the mirror on the two sides), the screens in regions of rows backed by receding faces; their mode files by the message lay (tools/pixel_mode.py); and the blind expectation file, written before any run. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/bell/build_world.py [--design <design>.json] [--folder <folder>]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SIDES = (("left", -1), ("right", 1))


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
    """The world file of one angle k: the board, the two symmetric walls with their gaps, per side the two lobes (the upper one at the phase +k / K of the turn on the right side and -k / K on the left), the screens' regions, both far faces receding, the ticks."""
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
            if index and angle:
                message["phase"] = [angle if sign > 0 else turns - angle, turns]
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


def links(degrees: list[int], spacing: int) -> list[int]:
    """Settings in degrees of fringe phase as positions on the screen in Links at the fringe spacing, refused where not whole."""
    found = [Fraction(int(angle) * spacing, 360) for angle in degrees]
    if any(link.denominator != 1 for link in found):
        raise ValueError(f"the settings {degrees} are not whole Links at the spacing {spacing}")
    return [int(link) for link in found]


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file, as tools/bell_clicks.py reads it: the sides' regions with their rows, the runs (one per angle), the comb's centre, spacing and settings in Links, the curve's sums in Links, and the design's blind rows."""
    comb = design["comb"]
    spacing = int(comb["spacing"])
    return {
        "comment": "Bell's blind expectation (the advisor's design at the owner's word of 2026-09-30, #1515 comments 5912573191 and 5911802610; ALGEBRA.md row (h)), written before the run from design.json: DETECTOR. Per run and side the shares per region from what each region saw (the `seen` lines, the amplitudes at its boundary, over W_c the quanta) and its entries; the comb on a half-row about the setting's position (+1 on the rows y_a - 4 to y_a + 3 of each fringe, -1 on the other eight); the marginal at a setting the comb's mean per region weighted by the region's share; E(a, b) the product of the two sides' marginals (the sides independent given the record); S = E(a, b) - E(a, b') + E(a', b) + E(a', b'); E as a curve in a + b at the curve's positions; averaged over the runs. Blind: the first world (k = 0) E = 0.405 cos a cos b, S = 0.57, checking the reader alone; over the eight angles ours E = 0.203 cos(a + b), S = 0.57, the coincidence fringe's visibility 0.50; nature E = 0.405 cos(a + b), S = 1.15, visibility 1.00; the joint credit that would reach nature's row is the one non-local declaration, the owner's word. The GameBoard check: the single-side fringes at the spacing 16 in each run, shifted by q_k d.",
        "verdict": "DETECTOR",
        "family": design["family"],
        "across": "y",
        "sides": {
            side: {f"{side}_{number}": rows for number, rows in enumerate(regions(design, side))}
            for side, _sign in SIDES
        },
        "runs": [f"bell_{angle}" for angle in range(int(design["angles"]))],
        "quanta": None,
        "fringe_centre": int(comb["centre"]),
        "spacing": spacing,
        "settings": {side: links(values, spacing) for side, values in comb["settings"].items()},
        "degrees": comb["settings"],
        "curve": {"degrees": list(comb["curve"]), "links": links(comb["curve"], spacing)},
        "blind": design["blind"],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    parser.add_argument(
        "--modes", action="store_true", help="write the mode files too (tools/pixel_mode.py)"
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    for angle in range(int(design["angles"])):
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
    print(json.dumps({"expectation": str(blind), "runs": int(design["angles"])}))


if __name__ == "__main__":
    main()

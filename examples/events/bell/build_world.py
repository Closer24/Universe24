"""Bell's worlds under the new laws (ALGEBRA.md row (h); the advisor's design at the owner's word of 2026-09-30, #1515 comments 5912573191 and 5911802610) from the design file beside this script: one world per angle, the pair's angle laid as the relative phase of the two lobes through the two gaps (the mirror on the two sides) at the half-offsets, (k + 1/2) / K of the turn (the advisor, #1515 comment 5912958018: at the whole offsets a run falls on a port's zero), the screens in regions of rows backed by receding faces, tiled inside the comb's half-fringes; their mode files by the message lay (tools/pixel_mode.py); and the blind expectation file, written before any run. Every number is the design's and stands in the files, none in this script or the engine.

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


def world(design: dict[str, Any], angle: int | None) -> dict[str, object]:
    """The world file of one angle k: the board, the two symmetric walls with their gaps, per side the two lobes (the upper one at the phase (k + 1/2) / K of the turn on the right side and its mirror, 1 - (k + 1/2) / K, on the left; both lobes in phase, u = 0, where the angle is None: the visibility world), the screens' regions, the far faces and the sides receding, the ticks."""
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
            if index and angle is not None:
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


def links(degrees: list[int], spacing: int) -> list[int]:
    """Settings in degrees of fringe phase as positions on the screen in Links at the fringe spacing, refused where not whole."""
    found = [Fraction(int(angle) * spacing, 360) for angle in degrees]
    if any(link.denominator != 1 for link in found):
        raise ValueError(f"the settings {degrees} are not whole Links at the spacing {spacing}")
    return [int(link) for link in found]


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file, as tools/bell_clicks.py reads it: the sides' regions with their rows, which side credits by the sign (A) and which by the contrast (B), the runs (one per angle), the comb's centre, spacing and settings in Links, the curve's positions in Links, and the design's blind rows."""
    comb = design["comb"]
    spacing = int(comb["spacing"])
    return {
        "comment": "Bell's blind expectation (the owner's decision of 2026-09-30, 14:15, Bell by the detector's contrast, #1515 comment 5912822802, on the advisor's design 5912573191 with his corrections 5912958018; ALGEBRA.md row (h)), written before the run from design.json: DETECTOR. Per run and side the shares per region from what each region saw (the `seen` lines, the net inflow through its front boundary, over W_c the quanta) and its entries; the two ports of a setting the unions of the regions in the comb's two half-rows about the setting's position (+ on the rows y_a - 3 to y_a + 4 of each fringe), the contrast their difference over their sum; the side `sign` (A, the left) credits every quantum to the larger port, the side `contrast` (B, the right) credits the larger port for the fraction of its quanta equal to the contrast and counts nothing for the rest; E(a, b) among the coincidences over the runs, S = E(a, b) - E(a, b') + E(a', b) + E(a', b'), E as a curve in a + b at the curve's positions of a against b's first setting, B's efficiency per setting; beside it the reading by the shares (E the product of the marginals) for comparison. Blind: by the contrast E = cos(a + b) in the fringe phase (the polariser's cos 2(a - b)), S = 2.83 exactly at eight run angles at the half-offsets, B's efficiency 0.64 at every setting, the uncounted pairs 36 percent (the detection loophole as a number); by the shares E = 0.203 cos(a + b), S = 0.57; nature 0.405 cos(a + b), S = 1.15 (2.83 with two-port analysers), and above the loophole's bound in the loophole-free experiments, where the law and nature part. The GameBoard check: the single-side fringes at the spacing 16 in each run, shifted by (k + 1/2) / 8 of it; B's clicks per run the same at every setting in the sum over the runs.",
        "verdict": "DETECTOR",
        "family": design["family"],
        "across": "y",
        "sides": {
            side: {f"{side}_{number}": rows for number, rows in enumerate(regions(design, side))}
            for side, _sign in SIDES
        },
        "sign": design["comb"]["sign"],
        "contrast": design["comb"]["contrast"],
        "runs": [f"bell_{angle}" for angle in range(int(design["angles"]))],
        "visibility_world": "bell_v",
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
    worlds: list[tuple[str, int | None]] = [("bell_v", None)]
    worlds += [(f"bell_{angle}", angle) for angle in range(int(design["angles"]))]
    for name, angle in worlds:
        path = args.folder / f"{name}.json"
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

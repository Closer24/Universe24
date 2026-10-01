"""Bell's gate world (ALGEBRA.md row (h); the advisor's corrected instrument of 2026-09-30, #1563 comment 5918198102) from the design file beside this script: the near-field board of 48 rows, per side two lobes of the light family before a wall with two gaps of two wavelengths and a bar between them, the pair's angle laid as the relative phase of the two lobes (the mirror on the two sides) at the half-offset (k + 1/2) / K of the turn for the design's angle k, the screens at L beyond the walls in regions of rows backed by receding faces, tiled on each side's grid; its mode file by the message lay (tools/pixel_mode.py, with --modes). Every number is the design's and stands in the files, none in this script or the engine; the world's blind expectation is the meeting round's (HIGHLIGHTS.md, One experiment and one gate).

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/bell/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
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


if __name__ == "__main__":
    main()

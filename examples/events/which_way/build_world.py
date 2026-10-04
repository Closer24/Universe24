"""The which-way world (examples/events/which_way; the owner's word of 2026-10-03, 01:52 UTC; the advisor's matrix T2): the two slits with a declared region at one gap backed by a face, three worlds from one design (`which_way`, `one_gap`, `two_gaps`), each with its mode file by the generator, and the blind `expectation.json` written from the design before any lay, byte for byte the same on every run of this script.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/which_way/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
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


def regions(design: dict[str, Any], channel: bool) -> list[dict[str, object]]:
    """The screen's node_readers, the column `screen` in regions of `rows_per_region` rows named screen_0 upward, the channel's rows left to the channel where it stands, and the channel itself, every Node from the wall to the screen's column between its walls."""
    rows, column, height = int(design["rows_per_region"]), int(design["screen"]), int(design["height"])
    low, high = (int(r) for r in design["channel"]["rows"])
    found: list[dict[str, object]] = []
    for index, first in enumerate(range(0, height, rows)):
        if channel and low <= first <= high:
            continue
        positions = [[column, row, 0] for row in range(first, first + rows)]
        found.append(
            {
                "name": f"screen_{index}",
                "positions": positions,
            }
        )
    if channel:
        first, last = (int(c) for c in design["channel"]["columns"])
        positions = [[x, y, 0] for x in range(first, last + 1) for y in range(low, high + 1)]
        found.append(
            {
                "name": str(design["channel"]["name"]),
                "positions": positions,
            }
        )
    return found


def world(design: dict[str, Any], name: str) -> dict[str, object]:
    """One world of the design: the board, the wall with the gaps the world opens, the channel's two walls across y where the world has the channel (inner faces at the channel's `walls` rows over the channel's `wall_columns`, from the wall's far side to the column before the screen), the packet, the node_readers, the receding face and the draw."""
    kind = design["worlds"][name]
    gaps = [{"y": list(design["gaps"][k]), "z": [0, 0]} for k in kind["gaps"]]
    faces: list[dict[str, object]] = [{"axis": "x", "at": int(design["wall"]), "gaps": gaps}]
    if kind["channel"]:
        first, last = (int(c) for c in design["channel"]["wall_columns"])
        open_x = [
            {"x": [0, first - 1], "z": [0, 0]},
            {"x": [last + 1, int(design["length"]) - 1], "z": [0, 0]},
        ]
        faces += [{"axis": "y", "at": int(at), "gaps": open_x} for at in design["channel"]["walls"]]
    packet = design["packet"]
    packet = {
        "family": design["family"],
        "along": "x",
        "wave": list(design["wave"]),
        "phase": [0, 1],
        "amplitude": int(design["amplitude"]),
        "top": {"x": [packet["column"], packet["column"]], "y": list(packet["across"]), "z": [0, 0]},
        "edge": {"x": int(packet["edge_along"]), "y": int(packet["edge_across"]), "z": 0},
    }
    return {
        "shape": [int(design["length"]), int(design["height"]), 1],
        "boundary": {"x": "open", "y": "open", "z": "periodic"},
        "face_depth": 1,
        "faces": faces,
        "intervals": int(design["intervals"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "bodies": [],
        "packets": [packet],
        "node_readers": regions(design, bool(kind["channel"])),
        "receding": design["receding"],
        "draw": design["draw"],
    }


def huygens(
    design: dict[str, Any], gaps: list[int], mirror: int | None, shadow: int | None
) -> list[float]:
    """The crude per-Node row at the screen: the point-source sum e^(ikr) / sqrt(r) over the open gaps' Nodes at the wall, each with its image in the mirror row at the opposite sign where a mirror stands (the channel's upper wall, a face reading 0), the rows at and below `shadow` 0 (behind the channel's walls), the board's edges ignored."""
    k = math.pi * design["wave"][0] / design["wave"][1]
    wall, screen = int(design["wall"]), int(design["screen"])
    row = []
    for y in range(int(design["height"])):
        total = 0j
        for gap in gaps:
            for source in range(int(design["gaps"][gap][0]), int(design["gaps"][gap][1]) + 1):
                r = math.hypot(screen - wall, y - source)
                total += cmath.exp(1j * k * r) / math.sqrt(r)
                if mirror is not None:
                    r = math.hypot(screen - wall, y - (2 * mirror - source))
                    total -= cmath.exp(1j * k * r) / math.sqrt(r)
        row.append(0.0 if shadow is not None and y <= shadow else abs(total) ** 2)
    return row


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind, per world: the Huygens row per screen region (scaled so that the two gaps' total is `blind_through`), the shadowed regions at 0, the channel's quanta and the screen's, the decisive comparison in words; written before any lay."""
    rows, height = int(design["rows_per_region"]), int(design["height"])
    low, high = (int(r) for r in design["channel"]["rows"])
    upper = int(design["channel"]["walls"][1])
    two = huygens(design, [0, 1], None, None)
    scale = float(design["blind_through"]) / sum(two)
    per_region = lambda row: [round(sum(row[f : f + rows]) * scale, 1) for f in range(0, height, rows)]  # noqa: E731
    one = huygens(design, [1], upper, upper)
    half = float(design["blind_through"]) / 2
    shadowed = [index for index, first in enumerate(range(0, height, rows)) if first + rows - 1 < low]
    return {
        "verdict": "NODEREADER",
        "family": design["family"],
        "window": [1, int(design["intervals"])],
        "across": "y",
        "seed": design["draw"]["seed"],
        "comment": design["comment"],
        "rows": {"two_gaps": per_region(two), "one_gap": per_region(one), "which_way": per_region(one)},
        "channel_region": [
            index for index, first in enumerate(range(0, height, rows)) if low <= first <= high
        ],
        "shadowed_regions": shadowed,
        "quanta": {
            "two_gaps": design["blind_through"],
            "which_way": {"channel": half, "screen": half},
            "one_gap": {"screen": half},
        },
        "comparison": "the which-way world's screen row equals the one-gap world's within the draw's scatter, region by region; both differ from the two-gaps world's row at the two slits' minima and maxima",
        "two_slits_extrema": design["two_slits_extrema"],
        "scatter": design["scatter"],
        "status": "the Huygens rows crude, for the shape and no fence (the design's comment); the quanta and the comparison the law's own, the count the record's share and the draw by the shares; fence: clicks",
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json")
    parser.add_argument("--folder", type=Path, default=HERE)
    parser.add_argument("--modes", action="store_true", help="lay the packet by the generator")
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    blind = json.dumps(expectation(design), indent=1, ensure_ascii=False) + "\n"
    (args.folder / "expectation.json").write_text(blind, encoding="utf-8")
    for name in design["worlds"]:
        path = args.folder / f"{name}.json"
        path.write_text(json.dumps(world(design, name)) + "\n", encoding="utf-8")
        if args.modes:
            command = [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)]
            subprocess.run(command, check=True, cwd=ROOT)
        print(json.dumps({"world": str(path), "laid": bool(args.modes)}))


if __name__ == "__main__":
    main()

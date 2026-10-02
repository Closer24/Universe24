"""World (iii) of the families round, matter and the binding holder (HIGHLIGHTS.md, Every family run on the engine and seen to work; the advisor's blinds, #1563 comment 5928483084), from the design file beside this script: two compact pixels of the matter family on an open box on the rule's own universe, twelve Links apart along x, each declared with one Node carrying its quanta and laid by the generator (tools/pixel_mode.py, with --modes, two bodies in two passes), a refusal by name printed and the world left declared; two declared regions, a box of Nodes about each body, whose field lines report each body's count; and the blind expectation file, the holder's range and Yukawa's line, the beat and the parting from the law's lines, written before any run and never touched after. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/matter_and_binding/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
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


def region(box: dict[str, list[int]]) -> list[list[int]]:
    """The Nodes of a box of the design, [first, last] per axis, in x-major order."""
    return [
        [x, y, z]
        for x in range(int(box["x"][0]), int(box["x"][1]) + 1)
        for y in range(int(box["y"][0]), int(box["y"][1]) + 1)
        for z in range(int(box["z"][0]), int(box["z"][1]) + 1)
    ]


def world(design: dict[str, Any], name: str) -> dict[str, object]:
    """One world: the open box, one body of the design's family per centre, each declared with one Node carrying its quanta, the declared regions about the bodies, the universe the design names."""
    row = design["worlds"][name]
    return {
        "shape": [int(v) for v in row["shape"]],
        "boundary": {"x": "open", "y": "open", "z": "open"},
        "face_depth": 1,
        "ticks": int(row["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [
            {
                "family": design["family"],
                "nodes": [{"node": [int(v) for v in centre], "count": int(row["quanta"])}],
            }
            for centre in row["centres"]
        ],
        "detectors": [
            {"name": str(label), "positions": region(box)} for label, box in row["regions"].items()
        ],
    }


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file, as tools/body_rest.py prints it beside the readings: the window, the family, the row read, the worlds, the regions whose field lines are read, the reading named, and the blind with its status and fence."""
    regions = sorted({label for row in design["worlds"].values() for label in row["regions"]})
    return {
        "verdict": "GAMEBOARD",
        "label": "GAMEBOARD",
        "comment": design["comment"],
        "family": design["family"],
        "row": design["row"],
        "window": [int(v) for v in design["window"]],
        "worlds": {name: name for name in design["worlds"]},
        "field": {"detectors": regions, "family": design["family"]},
        "reading": design["reading"],
        "blind": design["blind"],
    }


def laid(path: Path) -> None:
    """The generator's lay of a world's bodies, its mode file written beside the world; a refusal by name is printed and the world stays declared without a mode file."""
    command = [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)]
    found = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if found.returncode:
        print(json.dumps({"world": str(path), "refused": found.stderr.strip().splitlines()[-1]}))
    else:
        print(found.stdout, end="")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    parser.add_argument(
        "--modes",
        action="store_true",
        help="lay the bodies and write the mode files too (tools/pixel_mode.py)",
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    for name in design["worlds"]:
        path = args.folder / f"{name}.json"
        path.write_text(json.dumps(world(design, name)) + "\n", encoding="utf-8")
        print(json.dumps({"world": str(path)}))
        if args.modes:
            laid(path)
    written = expectation(design)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(args.folder / "expectation.json")}))


if __name__ == "__main__":
    main()

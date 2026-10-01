"""World (iv) of the families round, charge (HIGHLIGHTS.md, Every family run on the engine and seen to work; the advisor's blinds, #1563 comment 5928483084), from the design file beside this script: bodies of the charged family, matter's pair as a plane, on an open box, on the rule's own rows with the charged family added (the universe file beside the design, the holder of the sign at the law's level weight 1 and the plain read), one body alone and two bodies in like and in unlike senses, each laid rotating by the generator (tools/pixel_mode.py, with --modes, in the sense the design names), a refusal by name printed and the world left declared; and the blind expectation file, the Wronskian, the sign's write, its well by the lattice constants and the like-or-unlike reading under the plain read, written from the law's lines before any run and never touched after. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/charge/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
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


def world(design: dict[str, Any], name: str) -> dict[str, object]:
    """One world: the open box, one body of the charged family per centre, each declared with one Node carrying its quanta, no declared detector, the universe the design names."""
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
        "detectors": [],
    }


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file, as tools/body_rest.py prints it beside the readings: the window, the family and the holder, the level weight, the worlds with their senses, the reading named, and the blind with its status and fence."""
    return {
        "verdict": "GAMEBOARD",
        "label": "GAMEBOARD",
        "comment": design["comment"],
        "family": design["family"],
        "holder": design["holder"],
        "level_weight": int(design["level_weight"]),
        "window": [int(v) for v in design["window"]],
        "worlds": {name: [int(v) for v in row["senses"]] for name, row in design["worlds"].items()},
        "reading": design["reading"],
        "blind": design["blind"],
    }


def laid(path: Path, senses: list[str]) -> None:
    """The generator's lay of a world's bodies in the senses named, its mode file written beside the world; a refusal by name is printed and the world stays declared without a mode file."""
    command = [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)]
    if senses:
        command += ["--sense", *senses]
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
        senses = [str(int(v)) for v in design["worlds"][name]["senses"]]
        print(json.dumps({"world": str(path), "senses": senses}))
        if args.modes:
            laid(path, senses)
    written = expectation(design)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(args.folder / "expectation.json")}))


if __name__ == "__main__":
    main()

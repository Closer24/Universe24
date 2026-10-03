"""The frozen proton's builder, the proton's row of three planes at the pair [0, 6000] (the two hands of 2026-10-03, the advisor's (b), #1572 comment 5963954612, and the mathematician's 204, 5964082980; ALGEBRA.md #a-familys-declaration, Every family has a dimension): from `design.json` beside it this script writes the world `frozen_proton.json`, one body of the proton family of count 1 at the centre of an open cube with a region node_reader of two Nodes beside it, and the blind `expectation.json` from the design alone, before any run and never from one; with `--modes` it lays the body by the generator's one-Node declaration (tools/pixel_mode.py --pixel 0 --sense -1, `pixel_record`, every plane alike). Every number is the design's and the engine reads none of it.

PYTHONPATH=src python examples/events/frozen_proton/build_world.py --modes [--folder <folder>]
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


def world_of(design: dict[str, Any]) -> dict[str, Any]:
    """The one world: the open cube, the body of count 1 at the centre and the region beside it."""
    centre = [int(v) for v in design["centre"]]
    return {
        "shape": [int(v) for v in design["shape"]],
        "boundary": {"x": "open", "y": "open", "z": "open"},
        "face_depth": 1,
        "ticks": int(design["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "bodies": [
            {"family": design["family"], "nodes": [{"node": centre, "count": int(design["count"])}]}
        ],
        "node_readers": [
            {
                "name": "around",
                "positions": [[int(v) for v in node] for node in design["around"]],
            }
        ],
    }


def expectation(design: dict[str, Any]) -> dict[str, Any]:
    """The blind expectation file, from the design alone: the family, its pair and shape, the count, the sense, the amplitude per plane as the design derives it, and the hands' rows verbatim."""
    return {
        "verdict": "GAMEBOARD",
        "comment": design["comment"],
        "family": design["family"],
        "pair": list(design["pair"]),
        "shape": ["plane", "plane", "plane"],
        "count": int(design["count"]),
        "sense": int(design["sense"]),
        "amplitude_per_plane": design["amplitude_per_plane"],
        "window": [1, int(design["ticks"])],
        "worlds": design["worlds"],
        "blind": design["blind"],
    }


def laid(path: Path, sense: int) -> None:
    """The generator's lay of the world's body by the one-Node declaration, its mode file beside the world; a refusal by name is printed and the world stays declared without a mode file."""
    command = [
        sys.executable,
        str(ROOT / "tools" / "pixel_mode.py"),
        "--input",
        str(path),
        "--pixel",
        "0",
    ]
    found = subprocess.run([*command, "--sense", str(sense)], cwd=ROOT, capture_output=True, text=True)
    if found.returncode:
        print(json.dumps({"world": str(path), "refused": found.stderr.strip().splitlines()[-1]}))
    else:
        print(found.stdout, end="")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the world written")
    parser.add_argument(
        "--modes", action="store_true", help="lay the body (tools/pixel_mode.py --pixel 0)"
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    for name in design["worlds"]:
        path = args.folder / f"{name}.json"
        path.write_text(json.dumps(world_of(design)) + "\n", encoding="utf-8")
        print(json.dumps({"world": str(path)}))
        if args.modes:
            laid(path, int(design["sense"]))
    written = expectation(design)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(args.folder / "expectation.json")}))


if __name__ == "__main__":
    main()

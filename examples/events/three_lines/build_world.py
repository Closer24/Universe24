"""The fifth feasibility world's builder, a record of three real lines under the click (the Boss's list, #1572 comment 5963599079 (A) 5, with the two hands' amendments of 2026-10-03; ALGEBRA.md #a-familys-declaration, Every family has a dimension; #the-click-is-the-meeting): from `design.json` beside it this script writes two worlds, `triple_weighted.json` and `triple_permuted.json`, one message of the dimension-3 family at the declared weights over its three lines (the world file's key `weights`) moving along a chain toward a region detector of two Nodes backed by a receding face, under the declared instrument, and the blind `expectation.json` from the design alone, before any run and never from one; with `--modes` it lays the messages by the generator (tools/pixel_mode.py). Every number is the design's and the engine reads none of it.

PYTHONPATH=src python examples/events/three_lines/build_world.py --modes [--folder <folder>]
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


def world_of(design: dict[str, Any], weights: list[int]) -> dict[str, Any]:
    """One world: the chain, the message at the weights given, the counter and the instrument."""
    length, source = int(design["length"]), int(design["source"])
    message = {
        "family": design["family"],
        "along": "x",
        "wave": list(design["wave"]),
        "amplitude": int(design["amplitude"]),
        "top": {"x": [source, source], "y": [0, 0], "z": [0, 0]},
        "edge": {"x": int(design["edge"]), "y": 0, "z": 0},
        "weights": list(weights),
    }
    counter = {"name": "counter", "positions": [[int(x), 0, 0] for x in design["counter_nodes"]]}
    return {
        "shape": [length, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "ticks": int(design["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [],
        "messages": [message],
        "detectors": [counter],
        "receding": {
            "x": {
                "sides": ["low", "high"],
                "largest": int(design["largest"]),
                "layers": int(design["layers"]),
            }
        },
        "instrument": {
            **design["generator"],
            "window": int(design["window"]),
            "seed": int(design["seed"]),
        },
    }


def fractions(weights: list[int]) -> list[list[int]]:
    """The blind's fractions as exact [numerator, denominator] pairs, each weight's square over the sum of the squares."""
    total = sum(w * w for w in weights)
    return [[w * w, total] for w in weights]


def expectation(design: dict[str, Any]) -> dict[str, Any]:
    """The blind expectation file, from the design alone: the worlds with their weights and the blind's fractions, the window, the counter and the advisor's rows verbatim."""
    worlds = {
        name: {"weights": list(design[key]), "fractions": fractions(list(design[key]))}
        for name, key in design["worlds"].items()
    }
    return {
        "verdict": "DETECTOR",
        "comment": design["comment"],
        "family": design["family"],
        "window": [1, int(design["window"])],
        "counter": "counter",
        "clicks": 1,
        "worlds": worlds,
        "blind": design["blind"],
    }


def laid(path: Path) -> None:
    """The generator's lay of a world's message, its mode file beside the world; a refusal by name is printed and the world stays declared without a mode file."""
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
    parser.add_argument("--modes", action="store_true", help="lay the messages (tools/pixel_mode.py)")
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    for name, key in design["worlds"].items():
        path = args.folder / f"{name}.json"
        path.write_text(json.dumps(world_of(design, list(design[key]))) + "\n", encoding="utf-8")
        print(json.dumps({"world": str(path)}))
        if args.modes:
            laid(path)
    written = expectation(design)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(args.folder / "expectation.json")}))


if __name__ == "__main__":
    main()

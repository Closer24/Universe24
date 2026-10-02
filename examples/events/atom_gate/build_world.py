"""The atom's gate world of the body round, part 2 (the mathematician's 163 with the advisor's second hand; ALGEBRA.md, The atom is a bound body of the holder of the sign), from the design file beside this script: the 1s world and the 2s world, each one electron body of the design's quanta about the nucleus's Node and the nucleus one quantum at that Node (a declaration, design.json), on the open 31-cube in the universe atom.json, declaring the lay `fixed_point` with its tolerance; and the blind expectation file, 163's four rows with the law's numbers, written from the design alone before any run and never touched after, byte for byte the builder's (the committed-worlds gate of tests/test_the_bound_body.py). No lay: the electron's standing record under the sign holder's angle is not the generator's act in this round, so the worlds stand declared without their mode files and the loader refuses them at load (design.json, blind_and_reading.md). Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/atom_gate/build_world.py [--design <design>.json] [--folder <folder>]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent


def world(design: dict[str, Any], name: str) -> dict[str, object]:
    """One world: the open box, the electron body declared with one Node carrying its quanta at the centre and the nucleus's one quantum at the same Node's neighbour along x (two bodies share no Node; the generator's lay, when built, moves the electron's quanta about the nucleus), no declared detector, the universe the design names, the lay of the design."""
    row = design["worlds"][name]
    centre = [int(v) for v in row["centre"]]
    beside = [centre[0] + 1, centre[1], centre[2]]
    return {
        "shape": [int(v) for v in row["shape"]],
        "boundary": {"x": "open", "y": "open", "z": "open"},
        "face_depth": 1,
        "ticks": int(row["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [
            {
                "family": design["nucleus"]["family"],
                "nodes": [{"node": centre, "count": int(design["nucleus"]["quanta"])}],
            },
            {
                "family": design["electron"]["family"],
                "nodes": [{"node": beside, "count": int(design["electron"]["quanta"])}],
            },
        ],
        "detectors": [],
        "lay": dict(design["lay"]),
    }


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file, as tools/body_standing.py prints it beside the readings: the window, the families, the worlds, the law's numbers, the reading named, the blind of 163 with its status and fence per row, and what the short run does not test."""
    return {
        "verdict": "GAMEBOARD",
        "label": "GAMEBOARD",
        "comment": design["comment"],
        "family": design["electron"]["family"],
        "nucleus": design["nucleus"],
        "window": [int(v) for v in design["window"]],
        "worlds": {name: name for name in design["worlds"]},
        "numbers": design["numbers"],
        "reading": design["reading"],
        "blind": design["blind"],
        "not_tested_by_the_short_run": design["not_tested_by_the_short_run"],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    for name in design["worlds"]:
        path = args.folder / f"{name}.json"
        path.write_text(json.dumps(world(design, name)) + "\n", encoding="utf-8")
        print(json.dumps({"world": str(path), "laid": False}))
    written = expectation(design)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(args.folder / "expectation.json")}))


if __name__ == "__main__":
    main()

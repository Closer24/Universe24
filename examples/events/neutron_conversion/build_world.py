"""The neutron conversion's builder (the two hands of 2026-10-03, the advisor's (c), #1572 comment 5963954612, and the mathematician's 204, 5964082980; ALGEBRA.md, A family's declaration, item 5, The conversion's table and rate): from `design.json` beside it this script writes the world `neutron_conversion.json`, one body of the neutron family of count 1 at the centre of an open cube, declared with its conversion's table (the records out, a plane family with the sense of its lay as the design declares it) and rate and its own instrument, with a region node_reader of two Nodes beside it, and the blind `expectation.json` from the design alone, before any run and never from one; with `--modes` it calls the generator for the mode file beside the world (the body, converted whole, takes no mode entry: its lay is the engine's own at its Node). Every number is the design's and the engine reads none of it.

PYTHONPATH=src python examples/events/neutron_conversion/build_world.py --modes [--folder <folder>]
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
    """The one world: the open cube, the neutron of count 1 at the centre with its table, its rate and its draw, and the region beside it."""
    centre, table = [int(v) for v in design["centre"]], design["table"]
    outs = [  # the records out: a plane family with the sense the design declares, a real line its name alone
        {"family": str(row["family"]), "sense": int(row["sense"])}
        if "sense" in row
        else str(row["family"])
        for row in table["to"]
    ]
    body = {
        "family": design["neutron"]["family"],
        "nodes": [
            {"node": centre, "weight": 1},
            {"node": [centre[0] + 1, *centre[1:]], "weight": 1},
        ],
        "count": int(design["neutron"]["count"]),  # the record's count, declared once over its region
    }
    body["conversion"] = {"rate": int(table["rate"]), "to": outs}
    body["node_reader"] = {k: int(v) for k, v in design["generator"].items()}
    return {
        "shape": [int(v) for v in design["shape"]],
        "boundary": {"x": "open", "y": "open", "z": "open"},
        "face_depth": 1,
        "ticks": int(design["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "bodies": [body],
        "node_readers": [
            {
                "name": "around",
                "positions": [[int(v) for v in node] for node in design["around"]],
            }
        ],
    }


def expectation(design: dict[str, Any]) -> dict[str, Any]:
    """The blind expectation file, from the design alone: the neutron's row, the table, the excess, the trials, the rate's expectation and the hands' rows verbatim."""
    return {
        "verdict": "GAMEBOARD",
        "comment": design["comment"],
        "neutron": design["neutron"],
        "table": design["table"],
        "excess": design["excess"],
        "trials": design["trials"],
        "rate_expectation": design["rate_expectation"],
        "window": [1, int(design["ticks"])],
        "worlds": design["worlds"],
        "blind": design["blind"],
    }


def laid(path: Path) -> None:
    """The generator's mode file beside the world (no body of it laid by the generator, the record converted whole taking no mode entry); a refusal by name is printed and the world stays declared without a mode file."""
    command = [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)]
    found = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if found.returncode:
        print(json.dumps({"world": str(path), "refused": found.stderr.strip().splitlines()[-1]}))
    else:
        print(found.stdout, end="")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the world written")
    parser.add_argument(
        "--modes", action="store_true", help="the generator's mode file beside the world"
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    for name in design["worlds"]:
        path = args.folder / f"{name}.json"
        path.write_text(json.dumps(world_of(design)) + "\n", encoding="utf-8")
        print(json.dumps({"world": str(path)}))
        if args.modes:
            laid(path)
    written = expectation(design)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(args.folder / "expectation.json")}))


if __name__ == "__main__":
    main()

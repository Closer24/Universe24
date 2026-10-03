"""World (v) of the families round, light and charge (HIGHLIGHTS.md, Every family run on the engine and seen to work; the advisor's blinds, #1563 comment 5928483084), from the design file beside this script: a packet of light along a tube onto a screen of regions backed by a receding face, one world on the universe of world (iv), no body (the two body worlds of the first design were removed on 2026-10-03 at the owner's word, what does not load is deleted), the message laid by the generator (tools/pixel_mode.py, with --modes); and the blind expectation file in the format tools/click_counts.py reads, the uniform row of the free world and the arrival from the band's group velocity, written from the law's lines before any run and never touched after. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/light_and_charge/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
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


def screen_regions(design: dict[str, Any]) -> list[dict[str, object]]:
    """The screen's regions at the screen's column: `rows` rows along y each, over the whole ring across z, ordered along y, named screen_0 upward (each at least half the wavelength across the beam on both axes, the loader's size rule)."""
    across, rows, column = int(design["across"]), int(design["rows"]), int(design["screen"])
    return [
        {
            "name": f"screen_{number}",
            "positions": [
                [column, y, z] for y in range(number * rows, (number + 1) * rows) for z in range(across)
            ],
        }
        for number in range(across // rows)
    ]


def world(design: dict[str, Any], name: str) -> dict[str, object]:
    """One world: the tube (x open with both faces receding, y and z periodic), no body, the message of light along +x over the whole cross-section, the screen's regions, the universe the design names."""
    across = int(design["across"])
    bodies: list[dict[str, object]] = []  # the free world: no body (the body worlds removed, 2026-10-03)
    return {
        "shape": [int(design["length"]), across, across],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "ticks": int(design["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "bodies": bodies,
        "messages": [
            {
                "family": design["light"],
                "along": "x",
                "wave": [int(v) for v in design["wave"]],
                "phase": [0, 1],
                "amplitude": int(design["amplitude"]),
                "top": {
                    "x": [int(design["top"]), int(design["top"])],
                    "y": [0, across - 1],
                    "z": [0, across - 1],
                },
                "edge": {"x": int(design["edge"]), "y": 0, "z": 0},
            }
        ],
        "node_readers": screen_regions(design),
        "receding": {
            "x": {
                "sides": ["low", "high"],
                "largest": int(design["receding"]["largest"]),
                "layers": int(design["receding"]["layers"]),
            }
        },
    }


def expectation(design: dict[str, Any], laid: int | None) -> dict[str, object]:
    """The blind expectation file (NODEREADER, as tools/click_counts.py reads it): the screen's regions ordered along y, the family of light, the window, the pattern's range, the seed of the draw, the uniform blind row of the free world (every region one share, the lay's count over the regions where the lay stands), the arrival wager and `laid` the generator's count of the lay."""
    names = [str(node_reader["name"]) for node_reader in screen_regions(design)]
    regions = len(names)
    share = round(laid / regions, 1) if laid is not None else 1.0
    return {
        "verdict": "NODEREADER",
        "node_reader": names,
        "family": design["light"],
        "window": [int(v) for v in design["window"]],
        "across": "y",
        "pattern": [int(v) for v in design["pattern"]],
        "seed": int(design["seed"]),
        "comment": design["comment"],
        "counts": [share] * regions,
        "counts_comment": design["counts_comment"],
        "through": laid,
        "quanta": laid,
        "laid": laid,
        "arrival": design["arrival"],
        "worlds": {name: row["body"] for name, row in design["worlds"].items()},
    }


def laid_count(path: Path) -> int | None:
    """The generator's count of the message lay from the mode file beside the world, None where no mode file stands."""
    mode = path.with_suffix(".mode.json")
    if not mode.is_file():
        return None
    document = json.loads(mode.read_text(encoding="utf-8"))
    return sum(int(message["count"]) for message in document["messages"])


def laid(path: Path, senses: list[str]) -> None:
    """The generator's lay of a world's message and body, its mode file written beside the world; a refusal by name is printed and the world stays declared without a mode file."""
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
        help="lay the message and the bodies and write the mode files too (tools/pixel_mode.py)",
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    for name in design["worlds"]:
        path = args.folder / f"{name}.json"
        path.write_text(json.dumps(world(design, name)) + "\n", encoding="utf-8")
        senses = [str(int(v)) for v in design["worlds"][name].get("senses", [])]
        print(json.dumps({"world": str(path), "senses": senses}))
        if args.modes:
            laid(path, senses)
    free = args.folder / f"{next(n for n, r in design['worlds'].items() if r['body'] is None)}.json"
    written = expectation(design, laid_count(free))
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(args.folder / "expectation.json"), "laid": written["laid"]}))


if __name__ == "__main__":
    main()

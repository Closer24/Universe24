"""The atom's gate worlds (the mathematician's 163 with the advisor's second hand; ALGEBRA.md, The atom is a bound body of the holder of the sign), from the design file beside this script: the part-2 worlds hydrogen_1s and hydrogen_2s on atom.json (the electron body of 30,000 quanta, declared and not laid), and the round's worlds at the law's count 1, hydrogen_1s_large and hydrogen_2s_large on atom_large.json (the advisor's line, Gamma 730,838 at the width 128) and hydrogen_1s_toy on atom_toy.json (ALGEBRA.md's toy atom, Gamma 6,000 at the width 63), each one electron quantum beside the nucleus's one quantum at the centre of the open 31-cube, declaring the lay `fixed_point` with its tolerance; with --modes the worlds the design marks `laid` are laid by tools/pixel_mode.py side by side (the nucleus as the one-Node record, `--pixel`, the senses the design's), a refusal by name printed and the world left declared; and the blind expectation file, 163's rows and the round's restated rows with the law's numbers and the derived atom's run's rows (218 and 219), written from the design alone before any run and never touched after, byte for byte the builder's (the committed-worlds gate of tests/test_the_bound_body.py), the one number taken from a file the lay's own readings in the mode file where it stands. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/atom_gate/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
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
    """One world: the open box, the nucleus's one quantum at the centre and the electron body declared with one Node carrying its quanta at the centre's neighbour along x (two bodies share no Node; the generator's lay moves a many-quanta electron's quanta about the nucleus, and the count-1 electron's declaration stays, admitted by the gate within its rounding), the region detector of two Nodes beside the body where the derived atom's run names the world (`blind_derived_run`, the owner's decision of 2026-10-03, 09:38 Israel) and no detector otherwise, the universe the world's row names (the design's where it names none), the lay of the row (the design's where it names none)."""
    row = design["worlds"][name]
    centre = [int(v) for v in row["centre"]]
    beside = [centre[0] + 1, centre[1], centre[2]]
    derived = design.get(
        "blind_derived_run", {}
    )  # the derived atom's run: its region detector beside the body
    detectors = [dict(derived["detector"])] if derived.get("world") == name else []
    return {
        "shape": [int(v) for v in row["shape"]],
        "boundary": {"x": "open", "y": "open", "z": "open"},
        "face_depth": 1,
        "ticks": int(row["ticks"]),
        "universe": row.get("universe", design["universe"]),
        "engine": design["engine"],
        "measured": [
            {
                "family": design["nucleus"]["family"],
                "nodes": [{"node": centre, "count": int(design["nucleus"]["quanta"])}],
            },
            {
                "family": design["electron"]["family"],
                "nodes": [
                    {
                        "node": beside,
                        "count": int(row.get("electron_quanta", design["electron"]["quanta"])),
                    }
                ],
            },
        ],
        "detectors": detectors,
        "lay": dict(row.get("lay", design["lay"])),
    }


def from_the_lay(mode: Path) -> dict[str, object] | None:
    """The lay's own readings from the mode file where it stands (no run): per body its family, count, carried share, amplitude, clock pair, period and the lay's trajectory; None where the world has no mode file."""
    if not mode.exists():
        return None
    bodies = json.loads(mode.read_text(encoding="utf-8"))["bodies"]
    keys = ("family", "count", "carried", "amplitude", "clock", "period", "lay")
    return {"bodies": [{key: body.get(key) for key in keys} for body in bodies]}


def expectation(design: dict[str, Any], folder: Path) -> dict[str, object]:
    """The blind expectation file, as the folder's reader prints it beside the readings: the window, the families, the worlds, the law's numbers of the three universes, the reading named, the blind of 163 with its status and fence per row, the round's restated blind for the large-Gamma worlds and the toy, the caveat, what the short run does not test, and per laid world the lay's own readings from its mode file."""
    return {
        "verdict": "GAMEBOARD",
        "label": "GAMEBOARD",
        "comment": design["comment"],
        "comment_large": design["comment_large"],
        "family": design["electron"]["family"],
        "nucleus": design["nucleus"],
        "senses": design["senses"],
        "window": [int(v) for v in design["window"]],
        "worlds": {name: name for name in design["worlds"]},
        "numbers": design["numbers"],
        "numbers_large": design["numbers_large"],
        "numbers_toy": design["numbers_toy"],
        "reading": design["reading"],
        "blind": design["blind"],
        "blind_large": design["blind_large"],
        "blind_derived_run": design["blind_derived_run"],
        "not_tested_by_the_short_run": design["not_tested_by_the_short_run"],
        "from_the_lay": {
            name: from_the_lay(folder / f"{name}.mode.json")
            for name, row in design["worlds"].items()
            if row.get("laid")
        },
    }


def laid(design: dict[str, Any], paths: list[Path]) -> None:
    """The generator's lay of the worlds' bodies side by side, each mode file written beside its world: the nucleus (measured[0]) as the one-Node record (`--pixel`) and both bodies in the design's senses; a refusal by name is printed and the world stays declared without a mode file."""
    senses = [str(design["senses"][body]) for body in ("nucleus", "electron")]
    pixel = [str(number) for number in design["pixel"]]
    runs = [
        subprocess.Popen(
            [
                sys.executable,
                str(ROOT / "tools" / "pixel_mode.py"),
                "--input",
                str(path),
                "--sense",
                *senses,
                "--pixel",
                *pixel,
            ],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for path in paths
    ]
    for path, run in zip(paths, runs, strict=True):
        out, err = run.communicate()
        if run.returncode:
            print(json.dumps({"world": str(path), "refused": err.strip().splitlines()[-1]}))
        else:
            print(out, end="")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    parser.add_argument(
        "--modes",
        action="store_true",
        help="lay the worlds the design marks laid and write their mode files (tools/pixel_mode.py), side by side",
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    to_lay = []
    for name, row in design["worlds"].items():
        path = args.folder / f"{name}.json"
        rewrite = not row.get("laid") or args.modes or not path.exists()
        if rewrite:  # a laid world stays as the generator left it (its digest binds the mode file)
            path.write_text(json.dumps(world(design, name)) + "\n", encoding="utf-8")
        print(json.dumps({"world": str(path), "written": rewrite, "laid": bool(row.get("laid"))}))
        if row.get("laid") and args.modes:
            to_lay.append(path)
    if to_lay:
        laid(design, to_lay)
    written = expectation(design, args.folder)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(args.folder / "expectation.json")}))


if __name__ == "__main__":
    main()

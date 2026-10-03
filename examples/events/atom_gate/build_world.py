"""The atom's gate worlds (the mathematician's 163 with the advisor's second hand; ALGEBRA.md, The atom is a bound body of the holder of the sign), from the design file beside this script: the part-2 worlds hydrogen_1s and hydrogen_2s on atom.json (the electron body of 30,000 quanta, declared and not laid), and the round's worlds at the law's count 1, hydrogen_1s_large and hydrogen_2s_large on atom_large.json (the advisor's line, Gamma 730,838 at the width 128) and hydrogen_1s_toy on atom_toy.json (ALGEBRA.md's toy atom, Gamma 6,000 at the width 63), each one electron quantum beside the nucleus's one quantum at the centre of the open 31-cube, declaring the lay `fixed_point` with its tolerance; and round D's worlds (`round_d`, 2026-10-03: the atom world along the energy line at nature's alpha, atom_d.json, the nucleus the frozen row [0, 6000] of three planes laid by the one-Node declaration, the electron the turned top mode, the 2s by one deflation, the faces closed), hydrogen_1s_d and hydrogen_2s_d. With --modes the worlds the design marks `laid` are laid by tools/pixel_mode.py side by side (the nucleus as the one-Node record, `--pixel`, the senses the design's, the deflations the world's), a refusal by name printed and the world left declared; with --lays K --into <folder> the gate's lays of round D are written there, the 1s world's electron turned by k / K of a turn, k = 0 to K - 1, by the engine's three shears before any run (the mathematician's 236 and 242: the mean over lays, not seeds), the nucleus and the world's document alike, nothing of it committed; and the blind expectation file, 163's rows and the round's restated rows with the law's numbers, the derived atom's run's rows (218 and 219) and round D's rows, written from the design alone before any run and never touched after, byte for byte the builder's, the one number taken from a file the lay's own readings in the mode file where it stands. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/atom_gate/build_world.py [--design <design>.json] [--folder <folder>] [--modes] [--lays K --into <folder>]
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.features.rotation import turned
from event_universe.world_files import input_digest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
AXES = ("x", "y", "z")


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


def world_d(design: dict[str, Any], name: str) -> dict[str, object]:
    """One world of round D (`round_d`): the cube with its faces as the round declares them (closed, read as 0 as the open faces are, with no face layer reporting every interval), the nucleus's one quantum at the centre (the frozen row, laid by the one-Node declaration) and the electron's one quantum declared at the centre's neighbour along x (the law's count 1 over the mode's Nodes, the declaration admitted within the gate's rounding), no detector (line 1's detector on the body's Nodes is its own branch's), the round's universe and lay."""
    round_d = design["round_d"]
    row = round_d["worlds"][name]
    centre = [int(v) for v in row["centre"]]
    beside = [centre[0] + 1, centre[1], centre[2]]
    return {
        "shape": [int(v) for v in row["shape"]],
        "boundary": {axis: str(round_d["boundary"]) for axis in AXES},
        "ticks": int(row["ticks"]),
        "universe": str(row.get("universe", round_d["universe"])),
        "engine": round_d["engine"],
        "measured": [
            {
                "family": round_d["nucleus"]["family"],
                "nodes": [{"node": centre, "count": int(round_d["nucleus"]["quanta"])}],
            },
            {
                "family": round_d["electron"]["family"],
                "nodes": [{"node": beside, "count": int(round_d["electron"]["quanta"])}],
            },
        ],
        "detectors": [],
        "lay": dict(round_d["lay"]),
    }


def from_the_lay(mode: Path) -> dict[str, object] | None:
    """The lay's own readings from the mode file where it stands (no run): per body its family, count, carried share, amplitude, clock pair, period and the lay's trajectory; None where the world has no mode file."""
    if not mode.exists():
        return None
    bodies = json.loads(mode.read_text(encoding="utf-8"))["bodies"]
    keys = ("family", "count", "carried", "amplitude", "clock", "period", "lay")
    return {"bodies": [{key: body.get(key) for key in keys} for body in bodies]}


def expectation(design: dict[str, Any], folder: Path) -> dict[str, object]:
    """The blind expectation file, as the folder's reader prints it beside the readings: the window, the families, the worlds, the law's numbers of the three universes, the reading named, the blind of 163 with its status and fence per row, the round's restated blind for the large-Gamma worlds and the toy, the caveat, what the short run does not test, round D's numbers, G check and blind, and per laid world the lay's own readings from its mode file."""
    laid_worlds = {name: row for name, row in design["worlds"].items() if row.get("laid")}
    laid_worlds.update(
        {name: row for name, row in design["round_d"]["worlds"].items() if row.get("laid")}
    )
    return {
        "verdict": "GAMEBOARD",
        "label": "GAMEBOARD",
        "comment": design["comment"],
        "comment_large": design["comment_large"],
        "family": design["electron"]["family"],
        "nucleus": design["nucleus"],
        "senses": design["senses"],
        "window": [int(v) for v in design["window"]],
        "worlds": {name: name for name in [*design["worlds"], *design["round_d"]["worlds"]]},
        "numbers": design["numbers"],
        "numbers_large": design["numbers_large"],
        "numbers_toy": design["numbers_toy"],
        "reading": design["reading"],
        "blind": design["blind"],
        "blind_large": design["blind_large"],
        "blind_derived_run": design["blind_derived_run"],
        "round_d": {
            key: design["round_d"][key]
            for key in (
                "comment",
                "universe",
                "nucleus",
                "electron",
                "senses",
                "numbers_d",
                "g_check",
                "blind_d",
            )
        },
        "not_tested_by_the_short_run": design["not_tested_by_the_short_run"],
        "from_the_lay": {name: from_the_lay(folder / f"{name}.mode.json") for name in laid_worlds},
    }


def laid(paths: list[tuple[Path, list[str]]], senses: list[int], pixel: list[int]) -> None:
    """The generator's lay of the worlds' bodies side by side, each mode file written beside its world: the nucleus (measured[0]) as the one-Node record (`--pixel`), both bodies in the senses given and each world's own further arguments (the deflations of round D's 2s); a refusal by name is printed and the world stays declared without a mode file."""
    runs = [
        subprocess.Popen(
            [
                sys.executable,
                str(ROOT / "tools" / "pixel_mode.py"),
                "--input",
                str(path),
                "--sense",
                *(str(sense) for sense in senses),
                "--pixel",
                *(str(number) for number in pixel),
                *extra,
            ],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for path, extra in paths
    ]
    for (path, _extra), run in zip(paths, runs, strict=True):
        out, err = run.communicate()
        if run.returncode:
            print(json.dumps({"world": str(path), "refused": err.strip().splitlines()[-1]}))
        else:
            print(out, end="")


def half_angle(turn: int, count: int, wall: int) -> tuple[int, int]:
    """The k-th of `count` phases of a turn as the engine's turn takes it: the angle 2 pi k / count brought into (-pi, pi], the half-turn taken by the sign (-1) where the angle is beyond a quarter turn either way so that the tangent half-angle stays at most 1, the loader's guard, and the numerator n = round(wall tan(angle / 2)) over the wall (the engine's time turn's wall, 2 Gamma); returns (sign, numerator)."""
    angle = 2 * math.pi * turn / count
    if angle > math.pi:
        angle -= 2 * math.pi
    sign = 1
    if abs(angle) > math.pi / 2:
        sign, angle = -1, angle - math.copysign(math.pi, angle)
    return sign, round(wall * math.tan(angle / 2))


def lays(design: dict[str, Any], folder: Path, into: Path, count: int) -> None:
    """The gate's lays of round D (the mathematician's 236 and 242 with the advisor's second: the mean over lays, not seeds, the electron's phase at the lay advanced by one `count`-th of a turn per lay by the three shears before the run): from the 1s world and its mode file in `folder`, `count` worlds `<name>_lay_<k>.json` in `into` with their mode files, the world's document the same (one digest), the electron's two level pairs (now and before, re and im) turned by the angle 2 pi k / count by the engine's own turn (`features/rotation.turned`, exact and inverted bit for bit), the half-turn by the sign where the angle is beyond a quarter turn, the nucleus's levels as laid; the lay 0 is the generator's own; a run folder, never committed."""
    round_d = design["round_d"]
    name = next(n for n, row in round_d["worlds"].items() if not int(row.get("deflations", 0)))
    document = json.loads((folder / f"{name}.json").read_text(encoding="utf-8"))
    mode = json.loads((folder / f"{name}.mode.json").read_text(encoding="utf-8"))
    universe = json.loads((ROOT / round_d["universe"]).read_text(encoding="utf-8"))
    wall = 2 * int(universe["integers"]["node_clock"])
    electron = next(body for body in mode["bodies"] if body["family"] == round_d["electron"]["family"])
    moving = electron["moving"]
    levels = {key: np.asarray(moving[key], dtype=np.int64) for key in moving}
    into.mkdir(parents=True, exist_ok=True)
    digest = input_digest(document)
    assert digest == mode["world_digest"], "the mode file stands beside another world"
    for turn in range(count):
        sign, numerator = half_angle(turn, count, wall)
        copy = json.loads(json.dumps(mode))
        laid_electron = next(
            body for body in copy["bodies"] if body["family"] == round_d["electron"]["family"]
        )
        for re_key, im_key in (("now", "im_now"), ("before", "im_before")):
            re, im = turned(sign * levels[re_key], sign * levels[im_key], numerator, wall)
            laid_electron["moving"][re_key] = np.asarray(re).tolist()
            laid_electron["moving"][im_key] = np.asarray(im).tolist()
        laid_electron["profile"] = laid_electron["moving"]["now"]
        path = into / f"{name}_lay_{turn}.json"
        path.write_text(json.dumps(document) + "\n", encoding="utf-8")
        path.with_suffix(".mode.json").write_text(
            json.dumps(copy, separators=(",", ":")) + "\n", encoding="utf-8"
        )
        print(
            json.dumps(
                {"lay": turn, "sign": sign, "numerator": numerator, "wall": wall, "world": str(path)}
            )
        )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    parser.add_argument(
        "--modes",
        action="store_true",
        help="lay the worlds the design marks laid and write their mode files (tools/pixel_mode.py), side by side",
    )
    parser.add_argument(
        "--lays",
        type=int,
        default=0,
        help="round D's gate: write that many lays of the 1s world, the phase advanced",
    )
    parser.add_argument(
        "--into", type=Path, default=None, help="the run folder the lays are written into"
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    if args.lays:
        if args.into is None:
            parser.error("--lays needs --into <folder>, a run folder never committed")
        lays(design, args.folder, args.into, int(args.lays))
        return
    args.folder.mkdir(parents=True, exist_ok=True)
    to_lay: list[tuple[Path, list[str]]] = []
    for name, row in design["worlds"].items():
        path = args.folder / f"{name}.json"
        rewrite = not row.get("laid") or args.modes or not path.exists()
        if rewrite:  # a laid world stays as the generator left it (its digest binds the mode file)
            path.write_text(json.dumps(world(design, name)) + "\n", encoding="utf-8")
        print(json.dumps({"world": str(path), "written": rewrite, "laid": bool(row.get("laid"))}))
        if row.get("laid") and args.modes:
            to_lay.append((path, []))
    if to_lay:
        senses = [int(design["senses"][body]) for body in ("nucleus", "electron")]
        laid(to_lay, senses, [int(number) for number in design["pixel"]])
    round_d = design["round_d"]
    to_lay = []
    for name, row in round_d["worlds"].items():
        path = args.folder / f"{name}.json"
        rewrite = not row.get("laid") or args.modes or not path.exists()
        if rewrite:
            path.write_text(json.dumps(world_d(design, name)) + "\n", encoding="utf-8")
        print(json.dumps({"world": str(path), "written": rewrite, "laid": bool(row.get("laid"))}))
        if row.get("laid") and args.modes:
            deflations = [0, int(row.get("deflations", 0))]  # the nucleus, then the electron
            to_lay.append((path, ["--deflate", *(str(number) for number in deflations)]))
    if to_lay:
        senses = [int(round_d["senses"][body]) for body in ("nucleus", "electron")]
        laid(to_lay, senses, [int(number) for number in round_d["pixel"]])
    written = expectation(design, args.folder)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(args.folder / "expectation.json")}))


if __name__ == "__main__":
    main()

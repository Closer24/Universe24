"""The standing world of the body round (HIGHLIGHTS.md, the owner's words of 2026-10-02, 17:40 to 17:55; the mathematician's 167 and the advisor's second hand), from the design file beside this script: the same neutral body of the matter family at the centre of the open 25-cube, laid by the generator at the integer fixed point under its own paces (the world's `lay`) at T = 2^15 on the rule's own universe and at T = 2^19 on the universe file beside this design, each world declaring the tolerance from which the loader derives the least T; with --modes the two lays by tools/pixel_mode.py side by side, a refusal by name printed and the world left declared; and the blind expectation file, 167's three reads with their formulas and numbers written before any run and never touched after, the body's own expectations computed from the lay's profile in the mode file where it stands (the amplitude and the profile's sums, before any run). Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/standing_body/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def world(design: dict[str, Any], name: str) -> dict[str, object]:
    """One world: the open box, one body of the design's family declared with one Node carrying its quanta at the centre, no declared detector, the universe the world's row names, the lay of the design with the world's stop and tolerance."""
    row = design["worlds"][name]
    return {
        "shape": [int(v) for v in row["shape"]],
        "boundary": {"x": "open", "y": "open", "z": "open"},
        "face_depth": 1,
        "ticks": int(row["ticks"]),
        "universe": row["universe"],
        "engine": design["engine"],
        "measured": [
            {
                "family": design["family"],
                "nodes": [{"node": [int(v) for v in row["centre"]], "count": int(row["quanta"])}],
            }
        ],
        "detectors": [],
        "lay": {
            **design["lay"],
            "stop": int(row["stop"]),
            "tolerance": [int(v) for v in row["tolerance"]],
        },
    }


def from_the_lay(design: dict[str, Any], name: str, mode: Path) -> dict[str, object] | None:
    """The blind's numbers for the body as laid, from the mode file's profile alone (no run): the amplitude A, the quanta at the centre, N_eff = SUM f^2 and SUM f^2 / SUM f^4 over the profile f = level / A, rho_x the profile's rms radius along x, and from them 167's expectations at the window's length n and at n / 4: rho_s = (2 sigma sqrt(n) / A) sqrt(SUM f^2 / SUM f^4) and the centroid's rms shift 2 sigma sqrt(n) rho_x / (A sqrt(N_eff)); None where the world has no mode file yet."""
    if not mode.exists():
        return None
    body = json.loads(mode.read_text(encoding="utf-8"))["bodies"][0]
    declared = json.loads(mode.with_suffix("").with_suffix(".json").read_text(encoding="utf-8"))
    counts = [int(node["count"]) for node in declared["measured"][0]["nodes"]]
    shape, centre = design["worlds"][name]["shape"], design["worlds"][name]["centre"]
    amplitude = int(body["amplitude"])
    f2 = f4 = x2 = 0.0
    for flat, level in enumerate(body["profile"]):
        if level:
            f = level / amplitude
            x = flat // (shape[1] * shape[2]) - centre[0]
            f2, f4, x2 = f2 + f * f, f4 + f**4, x2 + x * x * f * f
    sigma, n = float(design["sigma"]["levels_per_interval"]), int(design["window"][1])
    shape_factor, rho_x = math.sqrt(f2 / f4), math.sqrt(x2 / f2)
    return {
        "amplitude": amplitude,
        "quanta_at_centre": max(counts),
        "quanta": sum(counts),
        "nodes": len(counts),
        "n_eff": f2,
        "shape_factor_sqrt_f2_over_f4": shape_factor,
        "rho_x_links": rho_x,
        "rho_s_expected": {
            str(n): 2 * sigma * math.sqrt(n) / amplitude * shape_factor,
            str(n // 4): 2 * sigma * math.sqrt(n // 4) / amplitude * shape_factor,
        },
        "centroid_rms_links": 2 * sigma * math.sqrt(n) * rho_x / (amplitude * math.sqrt(f2)),
        "lay": body.get("lay"),
    }


def expectation(design: dict[str, Any], folder: Path) -> dict[str, object]:
    """The blind expectation file, as tools/body_standing.py prints it beside the readings: the window, the family, the worlds, the reading named, the blind of 167 with its status and fence per read, and per world the body's own numbers from its lay (`from_the_lay`)."""
    return {
        "verdict": "GAMEBOARD",
        "label": "GAMEBOARD",
        "comment": design["comment"],
        "family": design["family"],
        "window": [int(v) for v in design["window"]],
        "worlds": {name: name for name in design["worlds"]},
        "sigma": design["sigma"],
        "reading": design["reading"],
        "blind": design["blind"],
        "from_the_lay": {
            name: from_the_lay(design, name, folder / f"{name}.mode.json") for name in design["worlds"]
        },
    }


def laid(paths: list[Path]) -> None:
    """The generator's lay of the worlds' bodies side by side, each mode file written beside its world; a refusal by name is printed and the world stays declared without a mode file."""
    runs = [
        subprocess.Popen(
            [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)],
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
        help="lay the bodies and write the mode files too (tools/pixel_mode.py), the worlds side by side",
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    paths = []
    for name in design["worlds"]:
        path = args.folder / f"{name}.json"
        path.write_text(json.dumps(world(design, name)) + "\n", encoding="utf-8")
        print(json.dumps({"world": str(path)}))
        paths.append(path)
    if args.modes:
        laid(paths)
    written = expectation(design, args.folder)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(args.folder / "expectation.json")}))


if __name__ == "__main__":
    main()

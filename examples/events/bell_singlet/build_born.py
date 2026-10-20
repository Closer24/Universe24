"""The singlet folder's born pair, the pair born of one emission act read by the click that runs back (ALGEBRA.md, The meeting's reading, with The lay across parts and The births' book, 2026-10-20, the owner's word; ENGINE.md section 3, act 6, and section 10, item 12): four chain worlds from the design file `design_born.json` over the folder's `design.json` (the born design's keys over the folder's, the settings, the patterns, the sides, the sign and the seed the folder's), the singlet's chain with no packet laid, one atom body standing excited at the source whose one emission lays the spin record on both parts alike as a source in time at the transition's resonance, the two regions at the ends with the singlet's axes and identity patterns, the receding faces, the cone's reach, the default, on the draw (`reach: board` until the remainders' fix of 2026-10-20) (a body stands on the board, so the whole board runs back and forward) and the window repeating (the left side's close in the first window, the right side's in the second); the universe file `born.json`, the folder's universe with the giver's family added, written here too; the mode files by tools/pixel_mode.py (with --modes; a body the engine lays takes no mode entry); and the blind `expectation_born.json`, the folder's blind by build_world.py's own arithmetic (the exact fractions at equal parts in the sign's form, which depend neither on the emission's interval nor on the portion of the beam a window reads) with the born pair's own key `born`, written before any run and never touched after. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/bell_singlet/build_born.py [--design <design>.json] [--born <design_born>.json] [--folder <folder>] [--modes]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIX = "born"  # the worlds' names, born_<a>_<b>


def builder() -> Any:
    """The folder's build_world.py loaded by path: the order of the settings, the combination and the blind's arithmetic are its and no other declaration."""
    spec = importlib.util.spec_from_file_location("bell_singlet_build_world", HERE / "build_world.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def designed(folder: dict[str, Any], born: dict[str, Any]) -> dict[str, Any]:
    """The born design over the folder's: every key of `design_born.json` stands, and the folder's `design.json` gives the rest (the settings, the patterns, the sides, the sign, the seed, the screen, the receding faces, the engine)."""
    return {**folder, **born}


def universe(design: dict[str, Any]) -> dict[str, object]:
    """The born universe: the folder's universe file with the giver's family row added, the chain's families untouched so that the beams travel as the singlet's do."""
    base = json.loads((ROOT / str(design["universe_base"])).read_text(encoding="utf-8"))
    return {"integers": base["integers"], "families": [*base["families"], dict(design["giver"])]}


def body(design: dict[str, Any]) -> dict[str, object]:
    """The giver: one body of the giver's family at the source, standing in its upper part, the transition between its parts driven by the pair family at the declared resonance (the frequency the light is born at), the rate out of the upper part at the lifetime giving to the pair family (no `width`: the source in time on the chain, its window derived at load), and its own generator with the seed the design names."""
    row, generator = design["body"], design["draw"]
    return {
        "family": row["family"],
        "nodes": [{"node": [int(row["source"]), 0, 0], "weight": 1}],
        "parts": [dict(part) for part in row["parts"]],
        "transitions": [
            {
                "from": row["parts"][0]["name"],
                "to": row["parts"][1]["name"],
                "drive": design["family"],
                "weight": int(row["weight"]),
                "resonance": [int(v) for v in row["resonance"]],
            }
        ],
        "rates": [
            {
                "from": row["parts"][1]["name"],
                "to": row["parts"][0]["name"],
                "lifetime": int(row["lifetime"]),
                "gives_to": design["family"],
            }
        ],
        "node_detector": {
            "multiplier": int(generator["multiplier"]),
            "increment": int(generator["increment"]),
            "seed": int(row["seed"]),
        },
    }


def world(design: dict[str, Any], a: str, b: str) -> dict[str, object]:
    """One world: the chain, no packet, the giver at the source, the two regions at the ends with their settings as their axes and their patterns, the receding faces, the intervals and the draw with `meeting: back` and the design's reach."""
    depth, length = int(design["screen"]), int(design["length"])
    node_detectors = [
        {
            "name": design["sides"]["a"],
            "positions": [[x, 0, 0] for x in range(depth)],
            "axis": [int(v) for v in design["settings"][a]],
            "pattern": design["patterns"]["a"],
        },
        {
            "name": design["sides"]["b"],
            "positions": [[x, 0, 0] for x in range(length - depth, length)],
            "axis": [int(v) for v in design["settings"][b]],
            "pattern": design["patterns"]["b"],
        },
    ]
    return {
        "shape": [length, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "intervals": int(design["intervals"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "bodies": [body(design)],
        "packets": [],
        "node_detectors": node_detectors,
        "receding": design["receding"],
        "draw": dict(design["draw"]),
    }


def blind(design: dict[str, Any], build: Any) -> dict[str, Any]:
    """The born pair's blind: the folder's blind by build_world.py's arithmetic on the merged design (the same exact fractions, the window the whole run, the runs the born worlds; the probe's arms left to the folder's blind) and the key `born`: the giver, its emission and seed, the two windows and the order of the closes, the two credit lines with their intervals, the correlation and S, and what is exact."""
    found = build.expectation(design)
    found.pop("arms")
    for fence in (
        "by_the_local_sums",
        "by_the_sign",
    ):  # the product forms over two sides closing in different windows: not read for the born pair (2026-10-20)
        found["blind"][fence] = {
            "correlation": {key: None for key in found["blind"][fence]["correlation"]},
            "S": None,
            "status": (
                "not read for the born pair: the product form over two sides is defined where both sides read the same "
                "intervals, and here the right side reads in the window after the left's close; the blind carried the "
                "singlet's fence values until the run of 2026-10-20 showed the two forms undefined for sides closing in "
                "different windows; E, S and the marginals untouched, predicted before the run and matched"
            ),
            "fence": found["blind"][fence]["fence"],
        }
    found["runs"] = {" ".join(pair): f"{PREFIX}_" + "_".join(pair) for pair in build.ORDER}
    row, closes, sides = design["body"], design["closes"], design["sides"]
    first, second = sides["a"], sides["b"]
    found[PREFIX] = {
        "worlds": dict(found["runs"]),
        "giver": {
            "family": row["family"],
            "node": [int(row["source"]), 0, 0],
            "standing_in": row["parts"][1]["name"],
            "rate": {
                "from": row["parts"][1]["name"],
                "to": row["parts"][0]["name"],
                "lifetime": int(row["lifetime"]),
                "gives_to": design["family"],
            },
            "resonance": [int(v) for v in row["resonance"]],
            "seed": int(row["seed"]),
            "seed_found": row["seed_found"],
        },
        "emission": (
            "the body's own draw at the hazard 1 / lifetime per dark interval with its own generator; at the "
            "design's seed the draw picks it at the interval 17, the record's birth (the births' book), and the "
            "source is laid over the lifetime on both parts alike (the lay across parts)"
        ),
        "reach": design["draw"].get("reach", "cone"),
        "windows": {
            first: [1, int(closes[first])],
            second: [int(closes[first]) + 1, int(closes[second])],
        },
        "order": [first, second],
        "arrivals_expected": dict(design["arrivals_expected"]),
        "credit_lines": [
            {
                "node_detector": first,
                "order": 1,
                "count": 1,
                "interval": int(closes[first]),
            },
            {
                "node_detector": second,
                "order": 2,
                "count": 1,
                "interval": int(closes[second]),
            },
        ],
        "correlation": dict(found["blind"]["correlation"]),
        "S": list(found["blind"]["S"]),
        "status": (
            "theorem under the law's paragraphs The meeting's reading and The meeting's identity: the "
            "left side draws at its own place on its own region's read with the Gram of the right side, its realised "
            "port's integer coefficients are written into the record at its birth inside the run back, the board runs "
            "forward with the realised term and carries it on to the right region, which draws coherently "
            "on the rewritten record where it stands; the two draws give the joint distribution J / SUM J, "
            "the gate's, E and S the folder's exactly, since the left side's coefficients take one nonzero "
            "magnitude on the surviving parts at both its settings ((1, 0) and (1, 1)), and the fractions depend "
            "neither on the emission's interval nor on the portion of the beam a window reads; the look of each world "
            "holds the passes of the run, the run back to the birth with its intervals decreasing, the write there, "
            "and the run forward"
        ),
        "fence": "clicks",
    }
    found["comment"] = (
        f"The folder's blind for the born pair's four worlds ({PREFIX}_<a>_<b>, the click that runs back, the one "
        "meeting): every fraction the folder's expectation.json's, written before any run, with the "
        f"born pair's own key `{PREFIX}`. " + str(design["comment"])
    )
    return found


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--design", type=Path, default=HERE / "design.json", help="the folder's design file"
    )
    parser.add_argument(
        "--born", type=Path, default=HERE / "design_born.json", help="the born pair's design file"
    )
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    parser.add_argument(
        "--modes", action="store_true", help="write the mode files too (tools/pixel_mode.py)"
    )
    args = parser.parse_args(argv)
    design = designed(
        json.loads(args.design.read_text(encoding="utf-8")),
        json.loads(args.born.read_text(encoding="utf-8")),
    )
    build = builder()
    args.folder.mkdir(parents=True, exist_ok=True)
    universe_path = ROOT / str(design["universe"])
    universe_path.write_text(json.dumps(universe(design)) + "\n", encoding="utf-8")
    print(json.dumps({"universe": str(universe_path), "giver": design["giver"]["name"]}))
    for a, b in build.ORDER:
        path = args.folder / f"{PREFIX}_{a}_{b}.json"
        path.write_text(json.dumps(world(design, a, b)) + "\n", encoding="utf-8")
        if args.modes:
            subprocess.run(
                [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)],
                check=True,
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
            )
        print(
            json.dumps(
                {"world": str(path), "settings": [a, b], "reach": design["draw"].get("reach", "cone")}
            )
        )
    written = blind(design, build)
    beside = args.folder / f"expectation_{PREFIX}.json"
    beside.write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "expectation": str(beside),
                "key": PREFIX,
                "S": written[PREFIX]["S"],
                "runs": written["runs"],
            }
        )
    )


if __name__ == "__main__":
    main()

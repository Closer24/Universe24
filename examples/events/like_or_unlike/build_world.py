"""The like-or-unlike look's worlds (ALGEBRA.md #the-rows-against-nature (f); #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record) from the design file beside this script: its three uncharged worlds, the look's control, on the universe whose plane family reads no holder of the sign (the pair of two bodies, and each body alone), each body laid whole by the generator (tools/pixel_mode.py, with --modes, in the sense the design names); and the blind expectation file, written from the law's lines before any run and never touched after: the uncharged pair's separation closes under the binding holder and gravity and a single body drifts by its own spreading alone (a GameBoard reading and no finding: the clicks that would tell it are the bodies' round's). The six charged worlds of the look were removed on 2026-10-03 at the owner's word, what does not load is deleted. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/like_or_unlike/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
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
    """One world: the chain, the bodies of the plane family declared one Node each at the design's Nodes or the world's own (a single body's), the generator laying them rotating in the senses the world names, no declared node_reader, the universe the world names."""
    bodies = [
        {
            "family": design["families"]["plane"],
            "nodes": [{"node": [int(x), 0, 0], "count": int(design["quanta"])}],
        }
        for x in design["worlds"][name].get("at", design["at"])
    ]
    return {
        "shape": [int(design["length"]), 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "ticks": int(design["ticks"]),
        "universe": design["universes"][design["worlds"][name]["universe"]],
        "engine": design["engine"],
        "bodies": bodies,
        "node_readers": [],
    }


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file, as tools/body_drift.py reads it: the window, the families, the worlds by their role, the reading named, and the blind with its status and fence; the uncharged pair and the uncharged single bodies, the look's control."""
    return {
        "verdict": "GAMEBOARD",
        "label": "GAMEBOARD",
        "comment": design["comment"],
        "family": design["families"]["plane"],
        "holder": design["families"]["holder"],
        "window": [int(v) for v in design["window"]],
        "worlds": {name: name for name in design["worlds"]},
        "background": {
            "pair": "uncharged_pair",
            "uncharged_alone": ["uncharged_alone_first", "uncharged_alone_second"],
        },
        "reading": "per world the centroid of each body's share over its half of the chain (the share in the current's units at the paces of the read, exact fractions; a single body's over the whole chain), the separation (the second less the first) at the window's ends and its change",
        "blind": {
            "pair": "the uncharged pair's separation closes: the mutual pull of the binding holder and of gravity, G, with no charge read or sourced (the plane family's reads the two holders of the content alone)",
            "alone": "a single uncharged body drifts by its own spreading alone, no image force (its family reads no holder of the sign) and no partner; the pair's change less the singles' drift is G",
            "status": "computed from the law's lines (the rows' reads and the holders' rests); the charged worlds that read like against unlike were removed on 2026-10-03 at the owner's word",
            "fence": "GameBoard: the drift of a share's centroid is a reading of the record, no click; the clicks that tell like from unlike are the bodies' round's (ALGEBRA.md (f))",
        },
    }


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
        if args.modes:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "pixel_mode.py"),
                    "--input",
                    str(path),
                    "--sense",
                    *senses,
                ],
                check=True,
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
            )
        print(json.dumps({"world": str(path), "senses": senses}))
    written = expectation(design)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(args.folder / "expectation.json")}))


if __name__ == "__main__":
    main()

"""The like-or-unlike look's worlds (ALGEBRA.md #the-rows-against-nature (f); #the-hypotheses-under-their-own-names, The sign holder rotates the two-part record) from the design file beside this script: five chain worlds of two bodies, seven on universes declaring the rotation (like senses, unlike senses, each body alone, and the same pair and the same single bodies on the universe whose holder has the level weight 10^6, its coupling nil: the neutral background of the pairs is the uncharged pair's change plus the image force of the faces on a charged body, the charged singles against the uncharged ones) and two on the universe declaring the plain read (the control), each body laid whole by the generator (tools/pixel_mode.py, with --modes, in the sense the design names); and the blind expectation file, written from the law's lines before any run and never touched after: like senses move apart and unlike senses move together, each against the background of the uncharged pair with the image force of the single bodies by the same size to the lattice's precision, with the ray's derivation of the sign and the first order's size beside it (a GameBoard reading and no finding: the clicks that would tell it are the bodies' round's). Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/like_or_unlike/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
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
    """The blind expectation file, as tools/body_drift.py reads it: the window, the families, the worlds by their role, the reading named, and the blind with its derivation, status and fence; the ray's first-order numbers from the design's quanta, level weight and intervals and the plane family's pair in its universe file."""
    universe = json.loads((ROOT / design["universes"]["turning"]).read_text(encoding="utf-8"))
    num, den = next(
        row["pair"] for row in universe["families"] if row["name"] == design["families"]["plane"]
    )
    quanta, weight, ticks = (
        int(design["quanta"]),
        int(design["level_weight"]["turning"]),
        int(design["ticks"]),
    )
    sigma = quanta / (2 * math.sin(math.acos(num / den))) / weight  # the source's levels per interval
    scale = sigma / 0.34  # the ray's estimate was read at 0.34 levels per interval
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
            "charged_alone": ["alone_first", "alone_second"],
            "uncharged_alone": ["uncharged_alone_first", "uncharged_alone_second"],
        },
        "reading": "per world the centroid of each body's share over its half of the chain (the share in the current's units at the paces of the read, exact fractions; a single body's over the whole chain), the separation (the second less the first) at the window's ends and its change; the background the uncharged pair's change plus the image force of the faces read on the single bodies, the charged singles' separation change (the second's drift less the first's) less the uncharged singles'; like and unlike read against it: a = like's change less the background, b = unlike's change less the background",
        "blind": {
            "like": "a > 0: like senses move apart",
            "unlike": "b < 0: unlike senses move together",
            "image": "both charged pairs end further apart than the uncharged pair by the image force, each charged body drawn to its nearer face by its own tent (a grounded wall, the face reading 0), the same force on a charged single body against an uncharged one, a reading beside the blind; the forces adding is what the blind's three lines test",
            "size": "the same size to the lattice's precision: |a + b| at most a third of (a - b) / 2, the second order of the angle (the like world's deeper level and the unlike world's cancelled one shift the two bodies' rotations differently, and the holder's own angle at a body, a twentieth of its binding margin omega_0 - omega_b at the level weight 100) and the lays' rounding; a larger asymmetry is a finding by name, never smoothed",
            "plain": "the control, the act pace: the holder's level is a hollow whatever the reader's sense (ALGEBRA.md (f)), so like_plain's bodies are drawn to each other's positive level and its separation closes faster than neutral's, while unlike_plain's first body is pushed from the second's negative level and the second drawn to the first's positive one, both drifting the same way, its separation near neutral's to the first order",
            "first_order": f"GameBoard, the ray's estimate from the law's lines: the holder's rest on an open chain of N Nodes is a tent with the slope 3 sigma (x_s + 1) / (N + 1) beyond its source at x_s, sigma the source's levels per interval (the body's W div T over the level weight, about {quanta} quanta x 1 / (2 sin omega_0) / {weight} = {sigma:.2f} levels per interval, the tent building up over the run inside the bodies' wells); the second body's ray reads the angle's gradient as dk per interval = (dL / dx) / Gamma and moves at v = (num / (3 den)) k / sin omega_0, so its centroid drifts by about a half of (num / (3 den sin omega_0)) (dL / dx) / Gamma x T^2 Links over T intervals: with the slope about {0.25 * scale:.2f} of a level per Link, about {scale:.1f} Links each way over {ticks} intervals, the separation changing by about {2 * scale:.1f} Links against the neutral world's, a bound body answering a gradient as a free packet does to within a tenth; the background holds the mutual pull of the binding holder and gravity (the uncharged pair's) and the image force of the faces (the single bodies'), each body's own spreading in both",
            "derivation": "the sign, by the ray (WKB) of the law's line and the engine's convention of the turn: the step e^(i theta) z_next + e^(-i theta) z_before = M z_now with theta = L / Gamma turns the plane against the sense of the record of positive Wronskian (z_before = z_now e^(i omega), clockwise), so that record's rotation rate is omega + theta where L > 0 and the record of negative W's is omega - theta; a ray at the wave number k has the rotation rate phi(k, x) = omega(k) + theta(x) for the positive record and dk / dt = -d phi / dx = -(dL / dx) / Gamma, so it accelerates down the level: a body of positive W sources L > 0 about itself (the write (w W + r) div (E_s T), the start's rest of the sources' sign), the other positive body is pushed away and a negative one (whose rate is omega - theta) is pulled in: like apart, unlike together, the same size, (f)'s words. The law's line as written, e^(-i theta) z_next + e^(i theta) z_before, with the same W convention (ALGEBRA.md, +A^2 sin omega for e^(-i omega t)) gives the positive record omega - theta and like senses together; the engine builds the sign (f) names and ENGINE.md states the convention",
            "status": "computed from the law's lines (the ray's first order), the sign the engine's declared convention of the turn",
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

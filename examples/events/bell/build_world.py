"""Bell's first world's builder (the advisor, #1515 comment 5910272948, C; ALGEBRA.md row (h)): from a design file (`design.json` beside it, every number of the world), a flat board with the source at its centre column, one packet of the light family per side carrying N wholes at mirror quantiles, narrow across the beam as the two gaps' aperture, moving apart at one angle (theta = 0), the two-gap walls and the screens symmetric about the source, one detector per screen with no declared remainders, both far faces receding; and the blind expectation file (the comb's settings as positions in Links, the curve's sums, the mirrors' pairing, the blind rows). The pair's mirror lay is the engine round's; --mirror writes its declaration, a key the loader refuses until that round names it. Every number of the world is the design's and stands in the world files, none in the engine.

Run from the checkout with PYTHONPATH set to its src:

    PYTHONPATH=src python examples/events/bell/build_world.py [--design <design>.json] [--folder <folder>] [--name <name>] [--mirror]

then lay the packets with the generator, `PYTHONPATH=src python tools/pixel_mode.py --input <world>.json`.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent


def world(design: dict[str, Any], mirror: bool = False) -> dict[str, object]:
    """The world file from the design: the board, the two symmetric walls with their gaps, the two packets (the left one at the source less the offset moving toward -x, the right one at the source plus the offset moving toward +x, each a flat top of one Node along x and of the two gaps' aperture across y with the raised-cosine edges, at the design's amplitude), the two screens as detectors over every row, both far faces receding as the design's `receding` key declares (the world's key, passed as written), the ticks; with `mirror`, each message names the other as its mirror."""
    packet, source, slab = design["packet"], int(design["source"]), int(design["slab"])
    height, across = int(design["height"]), [int(v) for v in packet["across"]]
    p, q = (int(v) for v in design["wave"])
    gaps = [{"y": list(gap), "z": [0, 0]} for gap in design["gaps"]]
    messages: list[dict[str, object]] = []
    for sign in (-1, 1):
        top = source + sign * int(packet["offset"])
        messages.append(
            {
                "family": design["family"],
                "along": "x",
                "wave": [sign * p, q],
                "amplitude": int(packet["amplitude"]),
                "top": {"x": [top, top], "y": across, "z": [0, 0]},
                "edge": {"x": int(packet["edge_along"]), "y": int(packet["edge_across"]), "z": 0},
            }
        )
    if mirror:
        messages[0]["mirror"], messages[1]["mirror"] = 1, 0
    detectors = []
    for side, sign in (("left", -1), ("right", 1)):
        near = source + sign * int(design["screen"])
        columns = sorted(range(near, near + sign * slab, sign))
        positions = [[x, y, 0] for y in range(height) for x in columns]
        detectors.append({"name": side, "positions": positions})
    return {
        "shape": [int(design["length"]), height, 1],
        "boundary": {"x": "open", "y": "open", "z": "periodic"},
        "face_depth": 1,
        "faces": [
            {"axis": "x", "at": source + sign * int(design["wall"]), "gaps": gaps} for sign in (-1, 1)
        ],
        "ticks": int(design["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [],
        "messages": messages,
        "detectors": detectors,
        "receding": design["receding"],
    }


def links(degrees: list[int], spacing: int) -> list[int]:
    """Settings in degrees of fringe phase as positions on the screen in Links at the fringe spacing, refused where not whole."""
    found = [Fraction(int(angle) * spacing, 360) for angle in degrees]
    if any(link.denominator != 1 for link in found):
        raise ValueError(f"the settings {degrees} are not whole Links at the spacing {spacing}")
    return [int(link) for link in found]


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file, as tools/bell_clicks.py reads it: the sides' detectors, the mirrors (the left packet's whole n pairs with the right packet's whole n), the wholes per side, the comb's centre, spacing, settings in Links, the curve's sums in Links and the bins, and the design's blind rows."""
    comb, packet = design["comb"], design["packet"]
    spacing = int(comb["spacing"])
    return {
        "comment": "Bell's first world's blind expectation (the advisor, #1515 comment 5910272948, C; ALGEBRA.md row (h)), written before the run from design.json: DETECTOR. A landing is a click line on a screen naming its whole; a pair is the left packet's whole n with the right packet's whole n (`mirrors`); the comb about a position: +1 where cos(Phi(y) - a) > 0 and -1 under, Phi(y) = 2 pi (y - fringe_centre) / spacing; E(a, b) the mean product over the pairs landing on both screens, S = E(a, b) - E(a, b') + E(a', b) + E(a', b'), E as a curve in a + b over every position, the coincidence map over Phi_A + Phi_B, each screen's single-side pattern. Blind under the whole line with the mirror lay: the triangle E = 1 - 2 |a + b| / pi, S = 2.00 exactly, a sharp ridge on Phi_A + Phi_B = 0; under the line as it stands E = 0.203 cos(a + b), S = 0.57, no ridge; nature with the same comb E = 0.405 cos(a + b), S = 1.15, a cosine ridge of visibility 1 (2.83 with two-port analysers). The GameBoard check: per pair two landings at mirror rows, the single-side fringes at the spacing 16.",
        "verdict": "DETECTOR",
        "family": design["family"],
        "across": "y",
        "along": "x",
        "sides": {"left": "left", "right": "right"},
        "mirrors": [[0, 1]],
        "wholes": int(packet["wholes"]),
        "fringe_centre": int(comb["centre"]),
        "spacing": spacing,
        "settings": {side: links(values, spacing) for side, values in comb["settings"].items()},
        "degrees": comb["settings"],
        "curve": {"degrees": list(comb["curve"]), "links": links(comb["curve"], spacing)},
        "bins": int(comb["bins"]),
        "blind": design["blind"],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the world written")
    parser.add_argument("--name", default="bell", help="the world's name")
    parser.add_argument(
        "--mirror",
        action="store_true",
        help="declare the two packets mirrors (the key `mirror` on each message, the other's index); the loader refuses it until the whole line's round names it",
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    path = args.folder / f"{args.name}.json"
    document = world(design, args.mirror)
    path.write_text(json.dumps(document) + "\n", encoding="utf-8")
    blind = args.folder / "expectation.json"
    blind.write_text(json.dumps(expectation(design), indent=1) + "\n", encoding="utf-8")
    summary = {"world": str(path), "expectation": str(blind), "shape": document["shape"]}
    print(json.dumps({**summary, "wholes": design["packet"]["wholes"], "ticks": document["ticks"]}))


if __name__ == "__main__":
    main()

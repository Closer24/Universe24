"""The GHZ gate's worlds (ALGEBRA.md #the-click-is-the-meeting, The GHZ gate; HIGHLIGHTS.md, One experiment and one gate) from the design file beside this script: four square worlds, one per combination of settings, the GHZ family's four parts laid equal as one event at the centre, three beams to the three declared regions at the board's ends, each region's `basis` the side's setting (p, q) and its `pattern` the side's, one integer pair per part; their mode files by the message lay (tools/pixel_mode.py, with --modes); and the blind expectation file, derived from the settings and the patterns in exact fractions before any run and never touched after, by the reader's own algebra on equal parts (tools/bell_gate.py, `blind_of`): the eight shares cos^2(a + b + c) / 4 at an even number of - ports and sin^2(a + b + c) / 4 at an odd, E_3 = cos 2(a + b + c), every marginal 1 / 2, every pairwise E 0, Mermin's M = E(x, y, y) + E(y, x, y) + E(y, y, x) - E(x, x, x) = -4 at x = (1, 0) and y = (1, 1) (local realism at most 2), and the three local credits as the fence, M = -1 each, with its status and its fence label. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/ghz/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
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
sys.path.insert(0, str(ROOT / "tools"))

import bell_gate  # noqa: E402  # the reader's algebra: the blind is what it gives on equal parts

ORDER = (
    ("x", "y", "y"),
    ("y", "x", "y"),
    ("y", "y", "x"),
    ("x", "x", "x"),
)  # Mermin, minus on the fourth
COMBINATION = {
    "name": "M",
    "signs": [1, 1, 1, -1],
}  # M = E(x, y, y) + E(y, x, y) + E(y, y, x) - E(x, x, x)
AXES = ("x", "y", "z")


def world(design: dict[str, Any], settings: tuple[str, ...]) -> dict[str, object]:
    """One world: the square board (z folded), the record laid as one event at the centre toward the three sides, each beam's flat top across it with its raised-cosine edges, the three regions at the board's ends with their settings as their bases and their declared patterns, the receding faces, the ticks."""
    length, source, depth = int(design["length"]), int(design["source"]), int(design["screen"])
    p, q = (int(v) for v in design["wave"])
    first, last = (int(v) for v in design["top_across"])
    messages, detectors = [], []
    for label, setting in zip(design["sides"], settings, strict=True):
        along, toward = str(design["beams"][label][0]), int(design["beams"][label][1])
        across = next(name for name in AXES[:2] if name != along)
        messages.append(
            {
                "family": design["family"],
                "along": along,
                "wave": [toward * p, q],
                "amplitude": int(design["amplitude"]),
                "top": {along: [source, source], across: [first, last], "z": [0, 0]},
                "edge": {along: int(design["edge_along"]), across: int(design["edge_across"]), "z": 0},
            }
        )
        deep = range(depth) if toward < 0 else range(length - depth, length)
        detectors.append(
            {
                "name": design["sides"][label],
                "positions": [
                    [u if along == "x" else v, v if along == "x" else u, 0]
                    for u in deep
                    for v in range(first, last + 1)
                ],
                "basis": [int(v) for v in design["settings"][setting]],
                "pattern": design["patterns"][label],
            }
        )
    return {
        "shape": [length, length, 1],
        "boundary": {"x": "open", "y": "open", "z": "periodic"},
        "face_depth": 1,
        "ticks": int(design["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [],
        "messages": messages,
        "detectors": detectors,
        "receding": design["receding"],
        "instrument": design["instrument"],
    }


def ports(design: dict[str, Any], settings: tuple[str, ...]) -> list[dict[str, tuple[int, ...]]]:
    """The sides' ports for one combination of settings, each side's from its setting and its pattern."""
    return [
        bell_gate.ports_of(
            tuple(int(v) for v in design["settings"][setting]),
            tuple((int(a), int(b)) for a, b in design["patterns"][label]),
        )
        for label, setting in zip(design["sides"], settings, strict=True)
    ]


def blind(design: dict[str, Any]) -> dict[str, Any]:
    """The blind numbers from the settings and the patterns alone, exact, by the reader's algebra on equal parts: per combination of settings the eight shares, E_3, the three marginals and the three pairwise E, M by the meeting, the three local credits with their M, and the status and fence of each."""
    found = bell_gate.blind_of(
        {" ".join(settings): ports(design, settings) for settings in ORDER},
        list(design["sides"]),
        COMBINATION["name"],
        COMBINATION["signs"],
    )
    found.update(
        efficiency="1, closed by construction: every triple is credited by the draw",
        status="theorem under the owner's declaration of the credit, by two hands (the mathematician, #1572 comment 5927559738; the advisor, 5927745013): with the patterns A (p, p, q, q), B (p, q, p, q), C (p, -q, -q, -p) and (p, q) = (cos a, sin a), the credit SUM_k e_k(A) e_k(B) e_k(C) is cos(a + b + c) at an even number of - ports and sin(a + b + c) at an odd up to the sign, so the eight shares are cos^2(a + b + c) / 4 and sin^2(a + b + c) / 4 (the normalisation 4 at every setting), E_3 = cos 2(a + b + c), every marginal 1 / 2 and every pairwise E 0, M = -4 at x = 0 and y = pi / 4; the parts laid equal stepping equal by the determinism of Rule3; a gate of the engine and never a result (HIGHLIGHTS.md, One experiment and one gate)",
        fence="clicks",
    )
    found["by_the_parts_shares"].update(
        status="theorem: each part's share credited alone is a mixture over the parts of product forms, local realism, |M| at most 2; M = -1 at the gate's settings",
        fence="clicks",
    )
    found["by_the_local_sums"].update(
        status="theorem: the product of the three sides' own squared sums is a product form, |M| at most 2; M = -1 at the gate's settings, where a reader rewritten as a local sum lands",
        fence="clicks",
    )
    found["by_the_sign"].update(
        status="theorem: the larger port on each side, 0 at a tie, a product form, |M| at most 2; M = -1 at the gate's settings",
        fence="clicks",
    )
    return found


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file, as tools/bell_gate.py reads it: the family, the window, the sides' regions, the settings and the patterns, the four worlds in Mermin's order with the combination's name and signs, the credit's rule named, the seed and the blind."""
    return {
        "verdict": "DETECTOR",
        "comment": design["comment"],
        "family": design["family"],
        "window": [int(v) for v in design["window"]],
        "sides": design["sides"],
        "settings": design["settings"],
        "patterns": design["patterns"],
        "order": [" ".join(settings) for settings in ORDER],
        "runs": {" ".join(settings): "ghz_" + "_".join(settings) for settings in ORDER},
        "combination": COMBINATION,
        "rule": "the joint share accumulated over the window on both members of the level pair over the three sides: J(p_A, p_B, p_C) = SUM over the window of (SUM_k c_k now_k^A now_k^B now_k^C)^2 + (SUM_k c_k before_k^A before_k^B before_k^C)^2 with c_k = e_k(p_A) e_k(p_B) e_k(p_C), e_k(+) = alpha_k p + beta_k q by the side's declared pattern at its basis (p, q) and e_k(-) = alpha_k (-q) + beta_k p; E_3 = the eight shares signed by the product of the ports' signs over their sum, a marginal the side's + shares over the sum, a pairwise E the shares signed by two sides' signs over the sum; the window the whole passage, one triple per world drawn by the shares with the seed; J is a sum of squares and never negative, so no floor is needed (the mathematician, #1572 comment 5927559738; the advisor, 5927745013)",
        "seed": int(design["seed"]),
        "blind": blind(design),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    parser.add_argument(
        "--modes", action="store_true", help="write the mode files too (tools/pixel_mode.py)"
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    for settings in ORDER:
        path = args.folder / ("ghz_" + "_".join(settings) + ".json")
        path.write_text(json.dumps(world(design, settings)) + "\n", encoding="utf-8")
        if args.modes:
            subprocess.run(
                [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)],
                check=True,
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
            )
        print(json.dumps({"world": str(path), "settings": list(settings)}))
    written = expectation(design)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"expectation": str(args.folder / "expectation.json"), "blind": written["blind"]["M"]}
        )
    )


if __name__ == "__main__":
    main()

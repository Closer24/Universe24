"""Bell's gate worlds (ALGEBRA.md #the-click-is-the-meeting, the pair's form; HIGHLIGHTS.md, One experiment and one gate: Bell is the engine's gate and no experiment) from the design file beside this script: four chain worlds, one per pair of settings, the pair family's two parts laid equal as one event at the centre, two beams to the two declared regions at the chain's ends, each region's `basis` the side's setting (p, q) and its `pattern` the pair's, [[1, 0], [0, 1]]; their mode files by the packet lay (tools/pixel_mode.py, with --modes); and the blind expectation file, derived from the settings in exact fractions before any run and never touched after, by the reader's own algebra on equal parts (tools/bell_gate.py, `blind_of`): E = ((p p' + q q')^2 - (p q' - q p')^2) / ((p^2 + q^2) (p'^2 + q'^2)) at equal parts, Lagrange's identity, S = 478 / 169 at (1, 0), (1, 1), (12, 5), (5, 12), the marginal 1 / 2, and the two local credits as the fence (by the parts' shares 238 / 169 and by the sign 2) with the local sums (240 / 169) beside them, each with its status and its fence label. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/bell/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
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
    ("a", "b"),
    ("a", "b_prime"),
    ("a_prime", "b"),
    ("a_prime", "b_prime"),
)  # CHSH, minus on the second
COMBINATION = {"name": "S", "signs": [1, -1, 1, 1]}  # S = E(a, b) - E(a, b') + E(a', b) + E(a', b')


def world(design: dict[str, Any], a: str, b: str) -> dict[str, object]:
    """One world: the chain, the pair laid as one event at the centre toward both sides, the two regions at the ends with their settings as their bases and the pair's pattern, the receding faces, the intervals."""
    source, depth, length = int(design["source"]), int(design["screen"]), int(design["length"])
    p, q = (int(v) for v in design["wave"])
    packets = [
        {
            "family": design["family"],
            "along": "x",
            "wave": [sign * p, q],
            "phase": [0, 1],
            "amplitude": int(design["amplitude"]),
            "top": {"x": [source, source], "y": [0, 0], "z": [0, 0]},
            "edge": {"x": int(design["edge_along"]), "y": 0, "z": 0},
        }
        for sign in (-1, 1)
    ]
    node_detectors = [
        {
            "name": design["sides"]["a"],
            "positions": [[x, 0, 0] for x in range(depth)],
            "basis": [int(v) for v in design["settings"][a]],
            "pattern": design["patterns"]["a"],
        },
        {
            "name": design["sides"]["b"],
            "positions": [[x, 0, 0] for x in range(length - depth, length)],
            "basis": [int(v) for v in design["settings"][b]],
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
        "bodies": [],
        "packets": packets,
        "node_detectors": node_detectors,
        "receding": design["receding"],
        "draw": design["draw"],
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
    """The blind numbers from the settings alone, exact, by the reader's algebra on equal parts: E per pair of settings and S by the meeting, the marginals, the three local credits with their S, S as one line of rho, and the status and fence of each."""
    found = bell_gate.blind_of(
        {" ".join(pair): ports(design, pair) for pair in ORDER},
        list(design["sides"]),
        COMBINATION["name"],
        COMBINATION["signs"],
    )
    s_meeting, s_shares = (
        bell_gate.fraction(found["S"]),
        bell_gate.fraction(found["by_the_parts_shares"]["S"]),
    )
    assert s_meeting is not None and s_shares is not None
    found.update(
        efficiency="1, closed by construction: every pair is credited by the draw",
        status="theorem under the owner's declaration of the credit (the one form of the click, the meeting): E = ((p p' + q q')^2 - (p q' - q p')^2) / ((p^2 + q^2) (p'^2 + q'^2)) at equal parts, Lagrange's identity, the parts laid equal stepping equal by the determinism of Rule3; a gate of the engine and never a result (HIGHLIGHTS.md, One experiment and one gate)",
        fence="clicks",
    )
    found["by_the_parts_shares"].update(
        status="theorem: each part's share credited alone is a product form, E = cos 2a cos 2b, rho = 0, S at most 2; the lower fence",
        fence="clicks",
    )
    found["by_the_local_sums"].update(
        status="theorem: the square of each side's own sum is a product form, E = sin 2a sin 2b, S at most 2; a reader rewritten as a local sum lands here",
        fence="clicks",
    )
    found["by_the_sign"].update(
        status="theorem: the larger port on each side, every outcome the same, E = 1 where neither side ties and 0 where one does, S = 2 exactly; the upper fence of a local credit",
        fence="clicks",
    )
    found["of_rho"] = {
        "S": f"({s_shares.numerator} + {(s_meeting - s_shares).numerator} rho) / {s_meeting.denominator}",
        "status": "derived (the mathematician, #1572 comment 5925175652): E = cos 2a cos 2b + rho sin 2a sin 2b, rho = 2 r / (1 + r^2) the parts' mismatch, 1 at the equal lay; r and rho are the reader's labelled diagnostics and no number of this blind",
        "fence": "lattice for r and rho, clicks for S",
    }
    return found


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file, as tools/bell_gate.py reads it: the family, the window, the sides' regions, the settings and the patterns, the four worlds in CHSH order with the combination's name and signs, the credit's rule named, the seed and the blind."""
    return {
        "verdict": "NODEDETECTOR",
        "comment": design["comment"],
        "family": design["family"],
        "window": [int(v) for v in design["window"]],
        "sides": design["sides"],
        "settings": design["settings"],
        "patterns": design["patterns"],
        "order": [" ".join(pair) for pair in ORDER],
        "runs": {" ".join(pair): "bell_" + "_".join(pair) for pair in ORDER},
        "combination": COMBINATION,
        "rule": "the joint share accumulated over the window on both members of the level pair: J(p_A, p_B) = SUM over the window of (SUM_k c_k now_k^A now_k^B)^2 + (SUM_k c_k before_k^A before_k^B)^2 with c_k = e_k(p_A) e_k(p_B), e(+) = (p, q) the declared basis under the pair's pattern [[1, 0], [0, 1]] and e(-) = (-q, p); E = (J_++ + J_-- - J_+- - J_-+) over the four summed; the window the whole passage, the credit's interval the draw's by the shares over it, one pair per world drawn with the seed; J is a sum of squares and never negative, so no floor is needed (the advisor, #1563 comment 5924731760; the mathematician, #1572 comment 5925374010)",
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
    for a, b in ORDER:
        path = args.folder / f"bell_{a}_{b}.json"
        document = world(design, a, b)
        path.write_text(json.dumps(document) + "\n", encoding="utf-8")
        if args.modes:
            subprocess.run(
                [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)],
                check=True,
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
            )
        print(json.dumps({"world": str(path), "settings": [a, b]}))
    written = expectation(design)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"expectation": str(args.folder / "expectation.json"), "blind": written["blind"]["S"]}
        )
    )


if __name__ == "__main__":
    main()

"""Bell's gate worlds (ALGEBRA.md #the-click-is-the-meeting, the pair's form; HIGHLIGHTS.md, One experiment and one gate: Bell is the engine's gate and no experiment) from the design file beside this script: four chain worlds, one per pair of settings, the pair family's two parts laid equal as one event at the centre, two beams to the two declared regions at the chain's ends, each region's `basis` the side's setting (p, q); their mode files by the message lay (tools/pixel_mode.py, with --modes); and the blind expectation file, derived from the settings in exact fractions before any run and never touched after: E = ((p p' + q q')^2 - (p q' - q p')^2) / ((p^2 + q^2) (p'^2 + q'^2)) at equal parts, Lagrange's identity, S = 478 / 169 at (1, 0), (1, 1), (12, 5), (5, 12), the marginal 1 / 2, and the two local credits as the fence (by the parts' shares 238 / 169 and by the sign 2) with the local sums (240 / 169) beside them, each with its status and its fence label. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/bell/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PORTS = ("plus", "minus")
ORDER = (
    ("a", "b"),
    ("a", "b_prime"),
    ("a_prime", "b"),
    ("a_prime", "b_prime"),
)  # CHSH, minus on the second
Joint = dict[tuple[str, str], Fraction]


def world(design: dict[str, Any], a: str, b: str) -> dict[str, object]:
    """One world: the chain, the pair laid as one event at the centre toward both sides, the two regions at the ends with their settings as their bases, the receding faces, the ticks."""
    source, depth, length = int(design["source"]), int(design["screen"]), int(design["length"])
    p, q = (int(v) for v in design["wave"])
    messages = [
        {
            "family": design["family"],
            "along": "x",
            "wave": [sign * p, q],
            "amplitude": int(design["amplitude"]),
            "top": {"x": [source, source], "y": [0, 0], "z": [0, 0]},
            "edge": {"x": int(design["edge_along"]), "y": 0, "z": 0},
        }
        for sign in (-1, 1)
    ]
    detectors = [
        {
            "name": design["sides"]["a"],
            "positions": [[x, 0, 0] for x in range(depth)],
            "basis": [int(v) for v in design["settings"][a]],
        },
        {
            "name": design["sides"]["b"],
            "positions": [[x, 0, 0] for x in range(length - depth, length)],
            "basis": [int(v) for v in design["settings"][b]],
        },
    ]
    return {
        "shape": [length, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "ticks": int(design["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [],
        "messages": messages,
        "detectors": detectors,
        "receding": design["receding"],
    }


def ports_of(basis: list[int]) -> dict[str, tuple[int, int]]:
    """A side's two ports from its basis (p, q): e(+) = (p, q) and e(-) = (-q, p)."""
    p, q = basis
    return {PORTS[0]: (p, q), PORTS[1]: (-q, p)}


def correlation(shares: Joint) -> Fraction:
    """E from four shares: (++ and --) less (+- and -+), over their sum."""
    total = sum(shares.values(), Fraction(0))
    return sum((1 if x == y else -1) * value for (x, y), value in shares.items()) / total


def meeting(e_a: dict[str, tuple[int, int]], e_b: dict[str, tuple[int, int]]) -> Joint:
    """The joint shares at equal parts: the cross-side sum over the parts, e(p_A) . e(p_B), squared (the common factor of the parts' levels cancels in E, Lagrange's identity closing the four to (p^2 + q^2) (p'^2 + q'^2))."""
    return {
        (x, y): Fraction(sum(u * v for u, v in zip(e_a[x], e_b[y], strict=True)) ** 2)
        for x in PORTS
        for y in PORTS
    }


def parts_shares(e_a: dict[str, tuple[int, int]], e_b: dict[str, tuple[int, int]]) -> Joint:
    """The local credit by the parts' shares at equal parts: the squares summed over the parts, never the amplitudes (rho = 0, E = cos 2a cos 2b)."""
    return {
        (x, y): Fraction(sum((u * v) ** 2 for u, v in zip(e_a[x], e_b[y], strict=True)))
        for x in PORTS
        for y in PORTS
    }


def local_sums(e_a: dict[str, tuple[int, int]], e_b: dict[str, tuple[int, int]]) -> Joint:
    """The local credit by the local sums at equal parts: the product of each side's own sum squared (E = sin 2a sin 2b)."""
    return {(x, y): Fraction(sum(e_a[x]) ** 2 * sum(e_b[y]) ** 2) for x in PORTS for y in PORTS}


def by_the_sign(e: dict[str, tuple[int, int]]) -> int:
    """A side's outcome by the sign at equal parts: the port whose own sum squared is the larger, 0 at a tie."""
    plus, minus = sum(e[PORTS[0]]) ** 2, sum(e[PORTS[1]]) ** 2
    return (plus > minus) - (plus < minus)


def pair(value: Fraction) -> list[int]:
    """A fraction as [numerator, denominator] for the file."""
    return [value.numerator, value.denominator]


def chsh(values: dict[str, Fraction]) -> Fraction:
    """S = E(a, b) - E(a, b') + E(a', b) + E(a', b') from the four E's keyed by the order's names."""
    keys = [f"{a} {b}" for a, b in ORDER]
    return values[keys[0]] - values[keys[1]] + values[keys[2]] + values[keys[3]]


def blind(design: dict[str, Any]) -> dict[str, Any]:
    """The blind numbers from the settings alone, exact: E per pair of settings and S by the meeting, the marginal, the three local credits with their S, S as one line of rho, and the status and fence of each."""
    settings = {name: ports_of([int(v) for v in basis]) for name, basis in design["settings"].items()}
    meet, shares, sums, signs = {}, {}, {}, {}
    marginal = {}
    for a, b in ORDER:
        key, e_a, e_b = f"{a} {b}", settings[a], settings[b]
        joint = meeting(e_a, e_b)
        meet[key] = correlation(joint)
        total = sum(joint.values(), Fraction(0))
        marginal[key] = (joint[(PORTS[0], PORTS[0])] + joint[(PORTS[0], PORTS[1])]) / total
        shares[key] = correlation(parts_shares(e_a, e_b))
        sums[key] = correlation(local_sums(e_a, e_b))
        signs[key] = Fraction(by_the_sign(e_a) * by_the_sign(e_b))
    s_meeting, s_shares = chsh(meet), chsh(shares)
    return {
        "correlation": {key: pair(value) for key, value in meet.items()},
        "S": pair(s_meeting),
        "marginal": {key: pair(value) for key, value in marginal.items()},
        "efficiency": "1, closed by construction: every pair is credited by the draw",
        "status": "theorem under the owner's declaration of the credit (the one form of the click, the meeting): E = ((p p' + q q')^2 - (p q' - q p')^2) / ((p^2 + q^2) (p'^2 + q'^2)) at equal parts, Lagrange's identity, the parts laid equal stepping equal by the determinism of Rule3; a gate of the engine and never a result (HIGHLIGHTS.md, One experiment and one gate)",
        "fence": "clicks",
        "by_the_parts_shares": {
            "correlation": {key: pair(value) for key, value in shares.items()},
            "S": pair(s_shares),
            "status": "theorem: each part's share credited alone is a product form, E = cos 2a cos 2b, rho = 0, S at most 2; the lower fence",
            "fence": "clicks",
        },
        "by_the_local_sums": {
            "correlation": {key: pair(value) for key, value in sums.items()},
            "S": pair(chsh(sums)),
            "status": "theorem: the square of each side's own sum is a product form, E = sin 2a sin 2b, S at most 2; a reader rewritten as a local sum lands here",
            "fence": "clicks",
        },
        "by_the_sign": {
            "correlation": {key: pair(value) for key, value in signs.items()},
            "S": pair(chsh(signs)),
            "status": "theorem: the larger port on each side, every outcome the same, E = 1 where neither side ties and 0 where one does, S = 2 exactly; the upper fence of a local credit",
            "fence": "clicks",
        },
        "of_rho": {
            "S": f"({s_shares.numerator} + {(s_meeting - s_shares).numerator} rho) / {s_meeting.denominator}",
            "status": "derived (the mathematician, #1572 comment 5925175652): E = cos 2a cos 2b + rho sin 2a sin 2b, rho = 2 r / (1 + r^2) the parts' mismatch, 1 at the equal lay; r and rho are the reader's labelled diagnostics and no number of this blind",
            "fence": "GameBoard for r and rho, clicks for S",
        },
    }


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file, as tools/bell_gate.py reads it: the family, the window, the sides' regions, the settings, the four worlds in CHSH order, the credit's rule named, the seed and the blind."""
    return {
        "verdict": "DETECTOR",
        "comment": design["comment"],
        "family": design["family"],
        "window": [int(v) for v in design["window"]],
        "sides": design["sides"],
        "settings": design["settings"],
        "order": [f"{a} {b}" for a, b in ORDER],
        "runs": {f"{a} {b}": f"bell_{a}_{b}" for a, b in ORDER},
        "rule": "the joint share accumulated over the window on both members of the level pair: J(p_A, p_B) = SUM over the window of (SUM_k c_k now_k^A now_k^B)^2 + (SUM_k c_k before_k^A before_k^B)^2 with c_k = e_k(p_A) e_k(p_B), e(+) = (p, q) the declared basis and e(-) = (-q, p); E = (J_++ + J_-- - J_+- - J_-+) over the four summed; the window the whole passage, the credit's interval the draw's by the shares over it, one pair per world drawn with the seed; J is a sum of squares and never negative, so no floor is needed (the advisor, #1563 comment 5924731760; the mathematician, #1572 comment 5925374010)",
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

"""The two-level body's builder (examples/events/body_node_detector; line 1 of the generic emitter/detector, the mathematician's 235 with the advisor's seconds, two hands): one world from the design, the toy two-level body as two standing rotations on the massless family's periodic chain with the one-Node detector on the Node 12 declaring the levels it reads, its mode file by the generator under --modes, and the blind `expectation.json` written from the design alone before any lay, byte for byte the same on every run of this script.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/body_node_detector/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def message(design: dict[str, Any], level: dict[str, Any]) -> dict[str, object]:
    """One level as a message over the whole chain with no envelope: the wave at its wave number and amplitude, the record's rotation in time at that Node the band's."""
    last = int(design["shape"][0]) - 1
    return {
        "family": design["family"],
        "along": "x",
        "wave": list(level["wave"]),
        "amplitude": int(level["amplitude"]),
        "top": {"x": [0, last], "y": [0, 0], "z": [0, 0]},
        "edge": {"x": 0, "y": 0, "z": 0},
    }


def world(design: dict[str, Any], window: int) -> dict[str, object]:
    """The world of the design at the window given: the chain, the two levels as messages, the one-Node detector with its levels and the instrument's draw."""
    levels = [
        {"name": level["name"], "pair": list(level["pair"]), "weight": list(level["weight"])}
        for level in design["levels"]
    ]
    return {
        "shape": list(design["shape"]),
        "boundary": dict(design["boundary"]),
        "ticks": window * int(design["windows"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [],
        "messages": [message(design, level) for level in design["levels"]],
        "detectors": [{"name": "reader", "positions": [list(design["node"])], "levels": levels}],
        "instrument": {**design["generator"], "window": window, "seed": int(design["seed"])},
    }


def share_of(level: dict[str, Any]) -> Fraction:
    """A level's share up to the common factors, a^2 sin^2(omega_n) / weight_n in exact fractions."""
    num, den = level["pair"]
    weight = Fraction(int(level["weight"][0]), int(level["weight"][1]))
    return Fraction(int(level["amplitude"]) ** 2) * Fraction(den * den - num * num, den * den) / weight


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind, from the design alone: each level's probability p_n as an exact fraction, the expected clicks per level over the windows with the binomial's deviation, the window refused and the reference check; written before any lay."""
    shares = {level["name"]: share_of(level) for level in design["levels"]}
    total, windows = sum(shares.values()), int(design["windows"])
    probabilities = {name: share / total for name, share in shares.items()}
    return {
        "verdict": "DETECTOR",
        "comment": design["comment"],
        "family": design["family"],
        "detector": "reader",
        "window": int(design["window"]),
        "windows": windows,
        "seed": int(design["seed"]),
        "probability": {name: [p.numerator, p.denominator] for name, p in probabilities.items()},
        "clicks": {
            name: {
                "expected": round(float(p) * windows, 1),
                "deviation": round(float(p * (1 - p) * windows) ** 0.5, 1),
                "reading": "the credit lines of the detector `reader` whose realised level is this name, over the run",
            }
            for name, p in probabilities.items()
        },
        "refused_window": {
            "window": int(design["refused_window"]),
            "message": "the window does not resolve the beat",
            "status": "the Gram condition, W at least 2 pi / (omega_e - omega_g) = 16.1 intervals at [2, 3] against [1, 3] (the advisor's 5966657866, the mathematician's 235)",
        },
        "clock": "the detector's proper time equals the board's tick at every close (the massless family reads no holder, p_0 = Gamma) and the window index counts the closes",
        "reference": {
            "reading": "the exact solve on the first window's level sequence at the Node, p_e as the shares' ratio",
            "blind": round(float(probabilities["e"]), 4),
            "within": 0.001,
            "status": "235's read 0.838 at W = 32 for his 21-Node well; the solve exact in exact arithmetic for W at or above 4, the rounding's amplification the Gram matrix's condition",
            "fence": "GameBoard",
        },
        "status": "two hands (the mathematician's 235, #1572 comment 5966769056; the advisor's 5966657866 and 5966780505); fence: clicks for the levels realised, a GameBoard reading for the reference",
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json")
    parser.add_argument("--folder", type=Path, default=HERE)
    parser.add_argument("--modes", action="store_true", help="write the mode file by the generator")
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    blind = json.dumps(expectation(design), indent=1, ensure_ascii=False) + "\n"
    (args.folder / "expectation.json").write_text(blind, encoding="utf-8")
    path = args.folder / f"{design['world']}.json"
    path.write_text(json.dumps(world(design, int(design["window"]))) + "\n", encoding="utf-8")
    if args.modes:
        command = [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)]
        source = os.pathsep.join(p for p in (str(ROOT / "src"), os.environ.get("PYTHONPATH", "")) if p)
        subprocess.run(command, check=True, cwd=ROOT, env={**os.environ, "PYTHONPATH": source})
    print(json.dumps({"world": str(path), "laid": bool(args.modes)}))


if __name__ == "__main__":
    main()

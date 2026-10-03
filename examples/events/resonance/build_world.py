"""The resonance world's builder (examples/events/resonance; test (vi), T4; the mathematician's 213 (B) and 220 with the advisor's seconds, two hands): two worlds from one design, the giver at the resonance [2, 3] and a taker at the same resonance (`resonant.json`) or detuned at [1, 3] (`detuned.json`), each with its mode file by the generator under --modes, and the blind `expectation.json` written from the design before any lay, byte for byte the same on every run of this script.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/resonance/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
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


def record(design: dict[str, Any], which: str, resonance: list[int]) -> dict[str, object]:
    """One atom declared an instrument at its Node: the giver standing in e with its giving, or the taker standing in g; the transition g to e by the light at the resonance given."""
    row, light = design[which], design["light"]
    upper = which == "giver"
    parts = [
        {"part": 0, "name": "g", "count": int(not upper)},
        {"part": 1, "name": "e", "count": int(upper)},
    ]
    transitions = [
        {"from": "g", "to": "e", "drive": light, "weight": int(row["weight"]), "resonance": resonance}
    ]
    rates = (
        [{"from": "e", "to": "g", "lifetime": int(row["lifetime"]), "gives_to": light}] if upper else []
    )
    draw = {**design["generator"], "window": int(row["window"]), "seed": int(row["seed"])}
    return {
        "family": row["family"],
        "nodes": [
            {"node": list(row["node"]), "weight": 1},
            {"node": [int(row["node"][0]) + 1, *row["node"][1:]], "weight": 1},
        ],
        "parts": parts,
        "transitions": transitions,
        "rates": rates,
        "instrument": draw,
    }


def world(design: dict[str, Any], name: str) -> dict[str, object]:
    """One world of the design: the chain, no message (the light born by the giving alone), the giver and the taker at the world's resonance, no region detector."""
    taker = record(design, "taker", list(design["worlds"][name]["resonance"]))
    return {
        "shape": list(design["shape"]),
        "boundary": dict(design["boundary"]),
        "ticks": int(design["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [record(design, "giver", list(design["giver"]["resonance"])), taker],
        "messages": [],
        "detectors": [],
    }


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind, from the design alone: the source's total and amplitudes, the far Node's cosine with its gate, the light's count at the span's end, the resonant taker's share and the detuned one's ratio, and the dark grain's chances (`dark_grain`); written before any lay and re-derived before any run under the dark grain."""
    num, den = design["giver"]["resonance"]
    return {
        "verdict": "DETECTOR",
        "comment": design["comment"],
        "family": design["light"],
        "giving": {
            "clock": "the lifetime's hazard 1 / tau per interval: in the dark one draw per interval at the now, the window's draw while a window stands (the giver is in the dark until it gives)",
            "span": int(design["giver"]["lifetime"]),
            "lay_lines": "the lifetime from the giving's interval, cut by the run's end",
            **design["source"],
            **design["dark_grain"],
        },
        "cos_omega": {
            "value": num / den,
            "pair": [num, den],
            "node": list(design["reading_node"]),
            "node_from_the_lay": "the design's reading Node is eight Nodes along x from the giver's first Node; the reader stands over the Nodes 0 and 1 and its giving is laid at the Node drawn by the record's share, so the reading Node is the one eight Nodes along x from the laid Node, 8 or 9",
            "window": list(design["reading_window"]),
            "estimator": "SUM_t n_t (n_(t+1) + n_(t-1)) / (2 SUM_t n_t^2)",
            "gate": "|cos Omega_read - num / den| <= 2 / A_far with A_far = max |n_t| over the window at the reading Node (the mathematician's 220, the advisor's second)",
        },
        "count_at_the_spans_end": {
            "value": 1,
            "reading": "the light's record's share in whole quanta over the board at the interval 96, (SUM share + W_c div 2) div W_c",
            "status": "the count's line, refused by name otherwise (the advisor's second)",
        },
        "resonant": {
            "share": 1.0,
            "reading": "the fraction of the seeds with a taking at the taker (the record's click lines, DETECTOR), gate sqrt(N p (1 - p)) over the seeds",
            "status": "the mathematician's 220: the resonant record's share 1 at delta = 0",
        },
        "detuned": {
            "ratio_to_resonant": design["detuning"]["sinc_squared_at_tau"]["48"],
            "reading": "the detuned taker's fraction over the resonant's",
            "status": "S.43 (the paper's supplement, line 328): P(tau) = [g^2 / (g^2 + delta^2 / 4)] sin^2(sqrt(g^2 + delta^2 / 4) tau), the ratio sinc^2(delta tau / 2) in the weak-turn limit, 1e-4 at tau = 48: fewer than one taking in a thousand of the resonant record's",
            **design["detuning"],
        },
        "seeds": len(design["seeds"]),
        "status": "the two hands' numbers (the mathematician's 220, #1572 comment 5965303134; the advisor's second, #1563 comment 5965316267); fence: clicks for the takings, a GameBoard reading for the cosine and the count",
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json")
    parser.add_argument("--folder", type=Path, default=HERE)
    parser.add_argument("--modes", action="store_true", help="write the mode files by the generator")
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    blind = json.dumps(expectation(design), indent=1, ensure_ascii=False) + "\n"
    (args.folder / "expectation.json").write_text(blind, encoding="utf-8")
    for name in design["worlds"]:
        path = args.folder / f"{name}.json"
        path.write_text(json.dumps(world(design, name)) + "\n", encoding="utf-8")
        if args.modes:
            command = [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)]
            subprocess.run(command, check=True, cwd=ROOT)
        print(json.dumps({"world": str(path), "laid": bool(args.modes)}))


if __name__ == "__main__":
    main()

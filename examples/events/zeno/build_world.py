"""The quantum Zeno world's builder (the paper's S.59; ALGEBRA.md, The click writes on the lattice (j), the record's re-lay read n times is the quantum Zeno effect; the owner's words of 2026-10-02, 12:38, and 2026-10-03): from `design.json` it writes one world per probe count n, `zeno_<n>.json`, a record of two parts (g at the count 1, e at 0) declared a NodeDetector at one Node of a periodic box under a drive's plane wave whose turn over the run is a pi pulse (the Rabi angle pi / 2 in the labels), the record's own window the run over n, so that it reads its own parts n times (the null window's write at each), and the blind `expectation.json`, Itano's column: P(e at T_pi) = (1 - cos^n(pi / n)) / 2. With `--modes` it lays the drives by the generator. Every number is the design's; the engine reads none of it.

PYTHONPATH=src python examples/events/zeno/build_world.py --modes [--folder <folder>]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))


def world_of(design: dict, n: int) -> dict:
    """One Zeno world: the record's window the run over n."""
    shape, at = design["shape"], design["record"]["node"]
    record = {
        "family": design["record"]["family"],
        "nodes": [{"node": at, "weight": 1}, {"node": [at[0] + 1, at[1], at[2]], "weight": 1}],
        "parts": [
            {"part": 0, "name": "g", "role": "ground", "count": 1},
            {"part": 1, "name": "e", "role": "excited", "count": 0},
        ],
        "transitions": [
            {
                "from": "g",
                "to": "e",
                "drive": design["drive"]["family"],
                "weight": design["record"]["weight"],
                "resonance": design["resonance"],
            },
            {
                "from": "e",
                "to": "g",
                "drive": design["drive"]["family"],
                "weight": design["record"]["weight"],
                "resonance": design["resonance"],
            },
        ],
        "rates": [],
        "node_detector": {
            **design["generator"],
            "window": design["intervals"] // n,
            "seed": design["record"]["seed"],
        },
    }
    drive = design["drive"]
    packet = {
        "family": drive["family"],
        "along": "x",
        "wave": drive["wave"],
        "phase": [0, 1],
        "amplitude": drive["amplitude"],
        "top": {"x": [0, shape[0] - 1], "y": [0, shape[1] - 1], "z": [0, shape[2] - 1]},
        "edge": {"x": 0, "y": 0, "z": 0},
    }
    return {
        "shape": shape,
        "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
        "intervals": design["intervals"],
        "universe": design["universe"],
        "engine": design["engine"],
        "bodies": [record],
        "packets": [packet],
        "node_detectors": [],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json")
    parser.add_argument("--folder", type=Path, default=HERE)
    parser.add_argument("--modes", action="store_true", help="lay the drives by the generator")
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    blind = {}
    for n in design["probes"]:
        path = args.folder / f"zeno_{n}.json"
        path.write_text(json.dumps(world_of(design, n)) + "\n", encoding="utf-8")
        if args.modes:
            import pixel_mode

            pixel_mode.main(["--input", str(path)])
        value = (1 - math.cos(math.pi / n) ** n) / 2
        blind[f"zeno_{n}"] = {
            "n": n,
            "window": design["intervals"] // n,
            "reading": "the fraction of the trials whose record stands in e at the run's end (tools/meeting_trials.py, the books' part as the last write left it, a click)",
            "blind": f"P(e at T_pi) = (1 - cos^n(pi / n)) / 2 = {value:.4f}",
            "value": round(value, 4),
            "status": "Itano, Heinzen, Bollinger and Wineland 1990's formula, the paper's S.59 column A, under the null window's write (the owner's 'yes, both of them'); column B, the click writing and the null window leaving the record, 1, 0.625, 0.154, 0.005, 0.000 at n = 1, 2, 4, 8, 16, and column C, no write, 1 at every n, beside it",
            "fence": "clicks",
        }
    expectation = {
        "verdict": "NODEDETECTOR",
        "comment": "The quantum Zeno world (S.59; the mathematician's 146 and 148, the advisor's second hand, the owner's word of 2026-10-02, 12:38, 'Yes, both of them'): one record of two parts declared a NodeDetector at one Node, a drive whose accumulated turn over the run is a pi pulse in the labels, the record reading its own parts n times over the run; written before any run and never edited after.",
        "trials": len(design["seeds"]),
        "intervals": design["intervals"],
        "blind": blind,
        "pi_pulse": design["pi_pulse"],
    }
    (args.folder / "expectation.json").write_text(
        json.dumps(expectation, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()

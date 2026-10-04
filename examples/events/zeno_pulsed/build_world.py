"""The pulsed quantum Zeno gate's builder (the paper's S.59; ALGEBRA.md, The pulsed gate, the window of a body bounded by the lays' schedule; the two hands of 2026-10-03, #1572 comments 5967698811, 5967783614 and 5967913000): from `design.json` it writes one world per probe count n, `zeno_pulsed_<n>.json`, the shipped Zeno body (two parts, g at the count 1 and e at 0) declared a NodeReader at one Node of a periodic box under the continuous drive's plane wave whose turn over the run is a pi pulse at the Node clock 96,000, with a probe, a record of a neutral family of one real line laid whole by the count at the body's Node at the intervals T_pi k / n, k = 1 to n (Itano's protocol), the body's transition of g into itself at the probe's family (taken by g, no turn) and its generator alone under `node_reader`, no declared window: the window is bounded by the probe's lays; and the blind `expectation.json`, Itano's column P(e at T_pi) = (1 - cos^n(pi / n)) / 2 with its standard error at the design's seeds, the passed probes and the fluorescence clicks per run. With `--modes` it lays the drive by the generator (the probe takes no mode entry). Every number is the design's; the engine reads none of it.

PYTHONPATH=src python examples/events/zeno_pulsed/build_world.py --modes [--folder <folder>]
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
    """One pulsed Zeno world: the probe laid at the body's Node at the intervals T_pi k / n, k = 1 to n."""
    shape, at, probe = design["shape"], design["record"]["node"], design["probe"]
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
            {"from": "g", "to": "g", "drive": probe["family"]},
        ],
        "rates": [],
        "node_reader": {**design["generator"], "seed": design["record"]["seed"]},
    }
    drive = design["drive"]
    packets = [
        {
            "family": drive["family"],
            "along": "x",
            "wave": drive["wave"],
            "phase": [0, 1],
            "amplitude": drive["amplitude"],
            "top": {"x": [0, shape[0] - 1], "y": [0, shape[1] - 1], "z": [0, shape[2] - 1]},
            "edge": {"x": 0, "y": 0, "z": 0},
        }
    ]
    packets += [
        {"family": probe["family"], "whole": at, "count": probe["count"], "interval": interval}
        for interval in intervals_of(design, n)
    ]
    return {
        "shape": shape,
        "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
        "intervals": design["intervals"],
        "universe": design["universe"],
        "engine": design["engine"],
        "bodies": [record],
        "packets": packets,
        "node_readers": [],
    }


def intervals_of(design: dict, n: int) -> list[int]:
    """The probe's intervals, T_pi k / n for k = 1 to n, the last at T_pi."""
    return [design["intervals"] * k // n for k in range(1, n + 1)]


def blind_of(n: int, trials: int) -> dict:
    """Itano's row at the probe count n over the trials: P(e at T_pi), its standard error, the passed probes at T_pi (the trials ending in e), the fluorescence clicks per run (the probes finding g, SUM over j of (1 + cos^j(pi / n)) / 2) and the windows per run, n."""
    value = (1 - math.cos(math.pi / n) ** n) / 2
    error = math.sqrt(value * (1 - value) / trials)
    fluorescence = sum((1 + math.cos(math.pi / n) ** j) / 2 for j in range(1, n + 1))
    return {
        "n": n,
        "intervals": None,
        "reading": "the fraction of the trials whose body stands in e at the run's end (tools/meeting_trials.py, the books' part as the last write left it, a click)",
        "blind": f"P(e at T_pi) = (1 - cos^n(pi / n)) / 2 = {value:.4f}",
        "value": round(value, 4),
        "standard_error": round(error, 3),
        "passed": round(trials * value, 1),
        "fluorescence_clicks_per_run": round(fluorescence, 2),
        "windows_per_run": n,
        "status": "Itano, Heinzen, Bollinger and Wineland 1990's formula, the paper's S.59 column A, under the window bounded by the probe's lays and the body's write at every close (the two hands of 2026-10-03, #1572 comments 5967783614 and 5967913000); accepted within two standard errors after the partial hole lands on main, the rows n >= 2 carrying the hole's bias by name before it",
        "fence": "clicks",
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json")
    parser.add_argument("--folder", type=Path, default=HERE)
    parser.add_argument("--modes", action="store_true", help="lay the drive by the generator")
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    blind = {}
    for n in design["probes"]:
        path = args.folder / f"zeno_pulsed_{n}.json"
        path.write_text(json.dumps(world_of(design, n)) + "\n", encoding="utf-8")
        if args.modes:
            import pixel_mode

            pixel_mode.main(["--input", str(path)])
        blind[f"zeno_pulsed_{n}"] = {**blind_of(n, len(design["seeds"])), "intervals": intervals_of(design, n)}
    expectation = {
        "verdict": "NODEREADER",
        "comment": "The pulsed quantum Zeno gate with the probe laid (S.59; the two hands of 2026-10-03, #1572 comments 5967698811, 5967783614 and 5967913000): the shipped Zeno body at the Node clock 96,000 under the continuous drive, the pi pulse 768 intervals, a probe laid whole by the count at its Node n times over the pi time, the body's window bounded by the probe's lays and its write at every close; written before any run and never edited after.",
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

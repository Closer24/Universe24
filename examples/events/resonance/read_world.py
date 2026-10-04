"""The resonance world's reader under the dark grain (examples/events/resonance; the mathematician's 223 (a), #1572 comment 5965727937, and 224 (2)(a), 5966081562, with the advisor's 5965918924 (a) and his second 5966129376, two hands): both worlds of the design run once per seed as tools/meeting_trials.py runs them, every record's generator at its own state from the seed, and read per seed: the giving's interval from the record's click lines, the lay lines on the light's first line, the far Node's cosine over the plateau [t + 28, t + 42] where it lies in the run (a lattice reading), the light's count at the span's end where the whole span lies in the run and no taking emptied the record (a lattice reading), and the takings (clicks); the counts over the seeds beside the blind.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/resonance/read_world.py [--design design.json] [--expectation expectation.json] [--folder .] [--seeds N]

`--seeds N` reads the seeds 1 to N in place of the design's list (the design's own 100 are the first 100 of them); the re-read of the detuned taker at 480 seeds (the mathematician's 240, item 5, #1572 comment 5967367372) runs with `--seeds 480`.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.lattice import Lattice
from event_universe.loader.derived import count_wall
from event_universe.world_files import load_world

HERE = Path(__file__).resolve().parent
AFTER, PLATEAU = (
    28,
    15,
)  # the plateau of a giving at t: [t + 28, t + 42], after the front, before the stop


def one_seed(path: Path, seed: int, design: dict[str, Any]) -> dict[str, Any]:
    """One run from the lay, every record's generator at its own state from the seed: the giving's interval, the lay lines, the cosine on the plateau, the count at the span's end and the takings."""
    lines: list[dict[str, Any]] = []
    board = Lattice(load_world(path), lines.append)
    for books in board.credit.bodies:
        books.state = seed * len(board.credit.bodies) + books.number
    light = [f.name for f in board.families].index(design["light"])
    far, levels = tuple(np.add(design["reading_node"], board.offset)), {}
    beyond = (far[0] + 1, *far[1:])  # the reading Node eight Nodes from either Node of the reader
    intervals, lifetime = int(design["ticks"]), int(design["giver"]["lifetime"])
    for _ in range(intervals):
        board.step()
        levels[board.tick] = tuple(int(board.states[light].lines[0].now[n]) for n in (far, beyond))
    clicks = [c for c in lines if c["event"] == "credit" and (c["taken"] or c["given"])]
    given = [c["tick"] for c in clicks if c["given"] == design["light"]]
    taken = [f"{c['node_reader']} {c['realised']} by {c['taken']}" for c in clicks if c["taken"]]
    found: dict[str, Any] = {"given": given[0] if given else None, "takings": taken}
    found["lay_lines"] = len(
        [c for c in lines if c["event"] == "lay" and c["family"] == design["light"]]
    )
    if not given:
        return found
    t = given[0]
    lays = [c for c in lines if c["event"] == "lay" and c["family"] == design["light"]]
    read_at = lays[0]["node"]["at"][0] - int(design["giver"]["node"][0])  # the lay's Node, 0 or 1
    series = {k: pair[read_at] for k, pair in levels.items()}
    if t + AFTER + PLATEAU <= intervals:
        window = range(t + AFTER, t + AFTER + PLATEAU)
        numerator = sum(series[k] * (series[k + 1] + series[k - 1]) for k in window)
        amplitude = max(abs(series[k]) for k in window)
        cosine = numerator / (2 * sum(series[k] ** 2 for k in window))
        found["cosine"] = {"read": round(cosine, 4), "far": amplitude, "gate": round(2 / amplitude, 4)}
        found["cosine"]["pass"] = (
            abs(cosine - design["giver"]["resonance"][0] / design["giver"]["resonance"][1])
            <= 2 / amplitude
        )
    if t + lifetime - 1 <= intervals and not taken:
        wall = count_wall(board.families[light], board.world.quantum_action)
        total = board.total_share(light)[0]
        found["count_at_the_spans_end"] = (int(total) + wall // 2) // wall if total is not None else None
    return found


def world_reading(path: Path, design: dict[str, Any]) -> dict[str, Any]:
    """One world over the design's seeds: the counts of the givings within the lifetime and the run, the intervals' summary, the cosine's passes, the counts at the span's end and the takings."""
    seeds = [one_seed(path, int(seed), design) for seed in design["seeds"]]
    given = [s["given"] for s in seeds if s["given"] is not None]
    cosines = [s["cosine"] for s in seeds if "cosine" in s]
    counts = [s["count_at_the_spans_end"] for s in seeds if "count_at_the_spans_end" in s]
    lifetime, trials = int(design["giver"]["lifetime"]), len(seeds)
    takings: dict[str, int] = {}
    for s in seeds:
        for word in s["takings"]:
            takings[word] = takings.get(word, 0) + 1
    return {
        "world": path.name,
        "trials": trials,
        "given_within_the_lifetime": [sum(t <= lifetime for t in given), trials],
        "given_within_the_run": [len(given), trials],
        "giving_intervals": {
            "mean": round(sum(given) / len(given), 1) if given else None,
            "least": min(given) if given else None,
            "largest": max(given) if given else None,
            "distinct": len(set(given)),
        },
        "lay_lines": {
            "whole_span": sum(s["lay_lines"] == lifetime for s in seeds),
            "any": sum(s["lay_lines"] > 0 for s in seeds),
        },
        "cosine_on_the_plateau": {
            "read": sum(1 for c in cosines),
            "pass": sum(1 for c in cosines if c["pass"]),
            "reads": sorted({c["read"] for c in cosines}),
        },
        "count_at_the_spans_end": {"read": len(counts), "ones": sum(1 for c in counts if c == 1)},
        "takings": dict(sorted(takings.items())),
        "label": "NODEREADER for the givings and the takings; LATTICE for the cosine and the count",
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json")
    parser.add_argument("--expectation", type=Path, default=HERE / "expectation.json")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder holding the world files")
    parser.add_argument(
        "--seeds", type=int, default=None, help="read the seeds 1 to N in place of the design's list"
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    if args.seeds is not None:
        design["seeds"] = list(range(1, args.seeds + 1))
    blind = json.loads(args.expectation.read_text(encoding="utf-8"))
    found = {
        "worlds": [world_reading(args.folder / f"{name}.json", design) for name in design["worlds"]],
        "blind": {"giving": blind["giving"], "cos_omega": blind["cos_omega"]},
    }
    print(json.dumps(found, indent=1))


if __name__ == "__main__":
    main()

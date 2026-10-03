"""The trials of a world of records declared instruments (examples/events/zeno, examples/events/anticoincidence; ALGEBRA.md, The click writes on the GameBoard (j); the paper's S.57 and S.59): one world file run as many times as the design names seeds, each run from the same lay with every instrument's generator at a state of its own from the trial's seed (the seed times the records' number plus the record's number) (the design's list of seeds, `seeds`, the host's declaration standing where one world file holds one seed; the counter's generator untouched), over the design's intervals, and at the end the part each record stands in (its books, the instrument's own), its windows closed (its books' count, the pulsed gate's n) and its `credit` lines labelled NODEREADER naming `taken` or `given`, the clicks (the null window's GAMEBOARD-labelled lines left out); the readings over the trials: per record the fraction of trials ending in each part and the windows closed per trial, the clicks per kind, the trials the run refused inside (the guard's refusal with its interval, by seed, read and not hidden), and over the records the fractions of trials with a taking at one record alone, at both and at neither, the anticoincidence parameter P(both) / (P(A) P(B)) where defined. Every number a click (the clicks, the parts the writes left) and no array is read; the tool holds no number of the law and compares nothing, the blind printed beside the readings where an expectation file is given.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/meeting_trials.py --world <world>.json --design <design>.json [--expectation <expectation>.json]
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from event_universe.game_board import GameBoard
from event_universe.world_files import load_world


def one_trial(
    path: Path, seed: int, intervals: int
) -> tuple[list[str], list[int], list[dict[str, object]], str | None]:
    """One run from the lay with every record's generator at `seed`: the parts the records stand in at the end, by their declared names, their windows closed, the click lines, and the guard's refusal where the run was refused inside (its message, naming the interval; None otherwise)."""
    lines: list[dict[str, object]] = []
    board = GameBoard(load_world(path), lines.append)
    for books in board.credit.bodies:  # every record its own state, distinct per record and per trial
        books.state = seed * len(board.credit.bodies) + books.number
    refused = None
    try:
        for _ in range(intervals):
            board.step()
            if board.ended is not None:
                break
    except (
        RuntimeError
    ) as refusal:  # the guard: a level above the bound, the run refused at its interval
        refused = str(refusal)
    parts = [books.declared.names[books.part] for books in board.credit.bodies]
    windows = [books.windows for books in board.credit.bodies]
    clicks = [
        line
        for line in lines
        if line["event"] == "credit"
        and line["label"] == "NODEREADER"
        and (line["taken"] or line["given"])
    ]
    return parts, windows, clicks, refused


def reading(path: Path, design: Path, expectation: Path | None) -> dict[str, object]:
    """The trials' readings against the design's seeds and intervals (its keys `seeds` and `intervals`, or the world's `ticks`), the blind beside them where given."""
    declared = json.loads(design.read_text(encoding="utf-8"))
    world = json.loads(path.read_text(encoding="utf-8"))
    seeds = [int(seed) for seed in declared["seeds"]]
    intervals = int(declared.get("intervals", world["ticks"]))
    ends: list[Counter[str]] = []
    closed: list[Counter[int]] = []
    kinds: Counter[str] = Counter()
    took: Counter[tuple[int, ...]] = Counter()
    refusals: dict[int, str] = {}
    for seed in seeds:
        parts, windows, clicks, refused = one_trial(path, seed, intervals)
        if refused is not None:
            refusals[seed] = refused
            continue
        for number, (part, count) in enumerate(zip(parts, windows, strict=True)):
            while len(ends) <= number:
                ends.append(Counter())
                closed.append(Counter())
            ends[number][part] += 1
            closed[number][count] += 1
        kinds.update(f"{j['node_reader']} {j['realised']} by {j['taken'] or j['given']}" for j in clicks)
        took[tuple(sorted({int(str(j["node_reader"]).split()[-1]) for j in clicks if j["taken"]}))] += 1
    trials = len(seeds) - len(refusals)
    fractions = {
        f"body {n}": {part: [c, trials] for part, c in sorted(found.items())}
        for n, found in enumerate(ends)
    }
    windows_closed = {
        f"body {n}": {str(count): c for count, c in sorted(found.items())}
        for n, found in enumerate(closed)
    }
    coincidence: dict[str, object] = {}
    if len(ends) == 2:
        only_a, only_b, both = took[(0,)], took[(1,)], took[(0, 1)]
        a, b = only_a + both, only_b + both
        alpha = Fraction(both * trials, a * b) if a and b else None
        coincidence = {
            "A_only": [only_a, trials],
            "B_only": [only_b, trials],
            "both": [both, trials],
            "neither": [took[()], trials],
            "alpha": [alpha.numerator, alpha.denominator] if alpha is not None else None,
        }
    found: dict[str, object] = {
        "world": path.name,
        "trials": trials,
        "intervals": intervals,
        "ends_in_part": fractions,
        "windows_closed": windows_closed,
        "refused": {str(seed): message for seed, message in sorted(refusals.items())},
        "clicks": dict(sorted(kinds.items())),
        "coincidence": coincidence,
        "label": "NODEREADER",
    }
    if expectation is not None:
        found["blind"] = json.loads(expectation.read_text(encoding="utf-8")).get("blind")
    return found


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--world", type=Path, required=True, help="the world file, its mode file beside it"
    )
    parser.add_argument("--design", type=Path, required=True, help="the design file naming the seeds")
    parser.add_argument("--expectation", type=Path, help="the blind expectation file, printed beside")
    args = parser.parse_args(argv)
    print(json.dumps(reading(args.world, args.design, args.expectation), indent=1))


if __name__ == "__main__":
    main()

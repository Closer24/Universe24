"""A, the read's algebra over many worlds' digits (README.md, section A, item 3): the ensemble's worlds
(a_one_quantum.py --ensemble, laid under the same scratch root) run again with an observer performing the
click's read of the board (digits.read_of, the engine's own function: the digits' lattice F, the copy rule,
the mixed radix) at the screen's Nodes at every interval of the passage, so that each interval's digits
give one number; at the close the regions' window inflows are the law's weights; every number's residue
modulo the screen's total is placed on the screen's cumulative weights (features/click.drawn_from's
placement), the histogram against the shares the test of Born as the credit's; at the close the credit's
own read over the thirteen regions' Nodes placed on the credit's weights, the credited region reproduced
(`close_reproduced`, as a_one_quantum.py's read again reproduces it).

    PYTHONPATH=src python papers/one_rule/variants/scripts/a_reads.py --worlds 40 --from 50
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
from collections import Counter
from collections.abc import Callable
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "src"))

from event_universe import digits, world_files  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.node_detector import node_detector_nodes  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402

OUT = HERE.parent / "out"
INTERVALS = 130


def placed(residue: int, weights: list[int]) -> int:
    """The pick on the cumulative weights, the first index whose cumulative weight exceeds the residue."""
    reached = 0
    for index, weight in enumerate(weights):
        reached += weight
        if residue < reached:
            return index
    return len(weights) - 1


def chi_square(counts: list[int], shares: list[float]) -> float:
    total = sum(counts)
    return sum((c - total * s) ** 2 / (total * s) for c, s in zip(counts, shares, strict=True) if s > 0)


def reader_of(
    board: Lattice,
    index: int,
    screen: list[str],
    first: int,
    numbers: dict[int, int],
    refusals: dict[int, str],
) -> Callable[[int, int, int], None]:
    """The observer: the click's read of the board at the screen's Nodes as the board holds them at this
    interval (the board grows with its receding faces), one number per interval from `first` on."""

    def observer(interval: int, direction: int, _pass_number: int) -> None:
        if interval < first or direction < 0:
            return
        try:
            at = np.zeros(board.shape, dtype=bool)
            for d in board.node_detectors:
                if d.declared and d.name in screen and d.nodes is not None:
                    at |= d.nodes
            number, _moduli = digits.read_of(board, [(index, at)], f"the screen at {interval}")
            numbers[interval] = number
            if interval == INTERVALS:  # the close: the credit's own read over every region's Nodes
                every = node_detector_nodes(board)
                numbers[-1], _moduli = digits.read_of(
                    board, [(index, every)], "the regions at the close"
                )
        except (ValueError, RuntimeError) as refusal:
            refusals[interval] = str(refusal)[:80]

    return observer


def window_weights(lines: list[dict], names: list[str], close: int, window: int) -> dict[str, int]:  # type: ignore[type-arg]
    first = close - window + 1
    found = {}
    for name in names:
        total = sum(
            int(line["inflow"])
            for line in lines
            if line["event"] == "click"
            and line["node_detector"] == name
            and first <= line["interval"] <= close
        )
        found[name] = max(total, 0)
    return found


def one_world(path: Path, first: int, window: int) -> dict:  # type: ignore[type-arg]
    """One world run with the observer: its credits, its regions' window weights, and per interval read the
    number's bit length and its residues modulo the screen's total and modulo the thirteen regions' total."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_world(path), lines.append)
    index = [f.name for f in board.families].index("charge")
    names = [d.name for d in board.node_detectors if d.declared]
    screen = [n for n in names if n.startswith("screen")]
    numbers: dict[int, int] = {}
    refusals: dict[int, str] = {}
    board.observers.append(reader_of(board, index, screen, first, numbers, refusals))
    for _ in range(INTERVALS):
        board.step()
    credits = [c for c in lines if c["event"] == "credit"]
    close = credits[0]["interval"] if credits else board.interval
    weights = window_weights(lines, names, close, window)
    screen_total = sum(weights[n] for n in screen)
    all_total = sum(weights.values())
    at_close = numbers.pop(-1, None)  # the credit's read over the thirteen regions' Nodes at the close
    return {
        "credits": [(c["interval"], c["node_detector"], c["bias_bound"]) for c in credits],
        "weights": weights,
        "bits": {t: n.bit_length() for t, n in numbers.items()},
        "residues_screen": {t: n % screen_total for t, n in numbers.items()} if screen_total else {},
        "close_bits": None if at_close is None else at_close.bit_length(),
        "close_residue_all": None if at_close is None or not all_total else at_close % all_total,
        "refusals": refusals,
    }


def statistics(results: list[dict]) -> dict:  # type: ignore[type-arg]
    """Every interval's residue placed on the screen's cumulative weights of its own world, the counts
    against the mean shares, the residues' uniformity, and the close's read over the thirteen regions'
    Nodes placed on the credit's weights against the credited region (the credit's own read, reproduced)."""
    counts: Counter[str] = Counter()
    fractions: list[float] = []
    screen: list[str] = []
    mean = None
    worlds = reproduced = closes = 0
    for r in results:
        names = list(r["weights"])
        screen = [n for n in names if n.startswith("screen")]
        w = [r["weights"][n] for n in screen]
        total = sum(w)
        if total <= 0:
            continue
        worlds += 1
        shares = [v / total for v in w]
        mean = shares if mean is None else [a + b for a, b in zip(mean, shares, strict=True)]
        for residue in r["residues_screen"].values():
            counts[screen[placed(int(residue), w)]] += 1
            fractions.append(int(residue) / total)
        if r["credits"]:
            closes += 1
            all_w = [r["weights"][n] for n in names]
            residue = r["close_residue_all"]
            if residue is not None:
                reproduced += names[placed(int(residue), all_w)] == r["credits"][0][1]
    assert mean is not None and worlds > 0
    mean_shares = [s / worlds for s in mean]
    found = [counts[n] for n in screen]
    n = len(fractions)
    xs = sorted(fractions)
    ks = max(max(abs((i + 1) / n - x), abs(i / n - x)) for i, x in enumerate(xs)) if n else None
    return {
        "worlds": worlds,
        "reads_placed": n,
        "screen_regions": screen,
        "mean_shares": [round(s, 5) for s in mean_shares],
        "counts": found,
        "expected": [round(n * s, 1) for s in mean_shares],
        "chi_square_11": round(chi_square(found, mean_shares), 2),
        "ks_distance": None if ks is None else round(ks, 4),
        "ks_bound_1pc": None if not n else round(1.628 / math.sqrt(n), 4),
        "close_reproduced": reproduced,
        "closes": closes,
        "screen_clicks": sum(
            1 for r in results if r["credits"] and str(r["credits"][0][1]).startswith("screen")
        ),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--scratch", type=Path, default=Path(tempfile.gettempdir()) / "two_slits_variants"
    )
    parser.add_argument("--worlds", type=int, default=40)
    parser.add_argument("--from", dest="first", type=int, default=50, help="the first interval read")
    parser.add_argument("--window", type=int, default=INTERVALS)
    args = parser.parse_args(argv)
    world_files.REPOSITORY_ROOT = args.scratch
    folder = args.scratch / "examples" / "events" / "one_quantum"
    results = []
    for k in range(args.worlds):
        path = folder / f"ensemble_{k}.json"
        if not path.exists():
            continue
        found = one_world(path, args.first, args.window)
        found["k"] = k
        results.append(found)
        print(
            json.dumps(
                {
                    "k": k,
                    "reads": len(found["bits"]),
                    "refused": len(found["refusals"]),
                    "credits": found["credits"],
                }
            )
        )
    found = statistics(results)
    print(json.dumps(found, indent=1))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "a_reads.json").write_text(
        json.dumps({"statistics": found, "worlds": results}, indent=1), encoding="utf-8"
    )


if __name__ == "__main__":
    main()

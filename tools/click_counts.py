"""The entries and the credit per detector over a window of intervals, read from a run's output file against an expectation file (DETECTOR, the one measurement; ALGEBRA.md #the-click-ends-nothing, the detector a declared instrument): the click lines of the expectation's detector (or detectors, a list) and one family within the window are counted per detector, each one reporter placed at the least coordinate of its Nodes on the axis the expectation names (`across`), so a region across the beam stands at its first row (a click reports its region and never a Node, the owner's word of 2026-09-30); the entries are printed beside the blind counts with the total through the reporters, the local maxima and minima within the pattern's range, the visibility at the blind central maximum against the blind minima, (most - least) over (most + least), as integers, and the summed absolute deviation of the entries from the blind row's shares over the total, sum |n_g B - T b_g| over T B (T the entries' total, B the blind row's), as a fraction. The credit, the instrument's declaration (the advisor's design at the owner's word, #1515 comment 5912573191, with his corrections 5912958018): what each detector saw, the net inflow through its front boundary summed over the window (the `seen` lines, the density that entered it from the declared board), gives its share of the screen's total; N, the quanta the screen absorbed, is the total inflow over the family's count wall W_c, and the laid count less N (`elsewhere`, the expectation's `laid`) is the part that left the board elsewhere, the wall's return through the source's face; the clicks credited are N times the shares, apportioned by the largest remainders (the draw's expectation), and one draw of N clicks by the shares with the expectation's `seed` (the instrument draws; no draw is in the law), the exclusivity by the draw's construction; a bare region named in the expectation's `aside` is read beside the screen (what it saw over W_c and its entries) and takes no share. The window, the detectors, the family, the axis, the pattern's range and the seed are the expectation file's; the tool holds no number.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/click_counts.py --world <world>.json --output <world>.output.json --expectation <expectation>.json
"""

from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction
from pathlib import Path

from event_universe.loader.derived import count_wall
from event_universe.loader.keys import AXES
from event_universe.loader.world import DetectorRow
from event_universe.world_files import load_world

Reporter = tuple[int, str]  # its coordinate on the axis (the least of its Nodes'), its detector


def rises(
    lines: list[dict[str, object]], detectors: list[str], family: str, window: tuple[int, int]
) -> dict[str, int]:
    """The clicks per detector of the named detectors and one family within the window [first, last] of intervals (a click reports its region, never a Node)."""
    found: dict[str, int] = {}
    for line in lines:
        if line.get("event") != "click" or line.get("detector") not in detectors:
            continue
        if line.get("family") != family or not window[0] <= int(str(line["tick"])) <= window[1]:
            continue
        found[str(line["detector"])] = found.get(str(line["detector"]), 0) + 1
    return found


def seen(
    lines: list[dict[str, object]], detectors: list[str], family: str, window: tuple[int, int]
) -> dict[str, int]:
    """What each named detector saw of one family within the window: its `seen` lines' net front inflows summed (0 where it saw nothing)."""
    found = {name: 0 for name in detectors}
    for line in lines:
        if line.get("event") != "seen" or line.get("family") != family:
            continue
        if line.get("detector") in found and window[0] <= int(str(line["tick"])) <= window[1]:
            found[str(line["detector"])] += int(str(line["inflow"]))
    return found


def apportioned(quanta: int, shares: list[int]) -> list[int]:
    """N clicks apportioned by the shares to whole numbers, the largest remainders first (the draw's expectation; 0 everywhere where nothing was seen)."""
    total = sum(shares)
    if not total or quanta <= 0:
        return [0] * len(shares)
    floors = [quanta * share // total for share in shares]
    rests = sorted(range(len(shares)), key=lambda i: (-(quanta * shares[i] % total), i))
    for index in rests[: quanta - sum(floors)]:
        floors[index] += 1
    return floors


def drawn(quanta: int, shares: list[int], seed: int) -> list[int]:
    """One draw of N clicks by the shares, the instrument's, with the declared seed: each quantum credited to one detector and never two."""
    found = [0] * len(shares)
    if sum(shares) and quanta > 0:
        for index in random.Random(seed).choices(range(len(shares)), weights=shares, k=quanta):
            found[index] += 1
    return found


def deviation(found: list[int], blind: list[object]) -> list[int]:
    """The summed absolute deviation of the entries from the blind row's shares over the total, sum |n_g B - T b_g| over T B with T the entries' total and B the blind row's, as [numerator, denominator]; [0, 1] where nothing entered."""
    shares = [Fraction(str(value)) for value in blind]
    total, whole = sum(found), sum(shares)
    if not total or not whole:
        return [0, 1]
    value = sum(abs(n * whole - total * b) for n, b in zip(found, shares, strict=True)) / (total * whole)
    return [value.numerator, value.denominator]


def reporters(rows: list[DetectorRow], axis: int) -> list[Reporter]:
    """The reporters across `axis`, one per detector, ordered by their coordinate on it, the least of the detector's Nodes' (a region across the beam at its first row)."""
    return sorted((min(node[axis] for node in row.positions), row.name) for row in rows)


def extrema(row: list[int], first: int, last: int) -> tuple[list[int], list[int]]:
    """The local maxima and minima of a row within [first, last]: a position whose count is above both neighbours' (a maximum) or below both (a minimum), the ends compared with their one neighbour."""
    maxima, minima = [], []
    for at in range(first, last + 1):
        near = [row[at - 1]] if at > first else []
        near += [row[at + 1]] if at < last else []
        if all(row[at] > value for value in near):
            maxima.append(at)
        if all(row[at] < value for value in near):
            minima.append(at)
    return maxima, minima


def reading(world: Path, output: Path, expectation: Path) -> dict[str, object]:
    """The reading: the entries per detector of the expectation's detector (or detectors) and family over its window, ordered along its axis, with the blind counts, the totals, the extrema, the visibility and the deviation from the blind row's shares."""
    expected = json.loads(expectation.read_text(encoding="utf-8"))
    document = json.loads(output.read_text(encoding="utf-8"))
    lines = document["lines"]
    loaded = load_world(world)
    axis = AXES.index(expected["across"])
    named = expected.get("detector")
    if named is None:  # every detector but the open faces' layer, over the whole run
        rows = [d for d in loaded.detectors if d.body is None]
        names = [d.name for d in rows]
    else:
        names = [str(name) for name in named] if isinstance(named, list) else [str(named)]
        rows = [d for d in loaded.detectors if d.name in names]
    if len(rows) != len(names):
        raise ValueError(
            f"the expectation names the detectors {names}; the world declares {[d.name for d in loaded.detectors]}"
        )
    spanned = expected.get("window", [0, document.get("ticks", 0)])
    window = (int(spanned[0]), int(spanned[1]))
    counted = rises(lines, names, str(expected["family"]), window)
    placed = reporters(rows, axis)
    found = [counted.get(name, 0) for _at, name in placed]
    family = next(f for f in loaded.families if f.name == expected["family"])
    wall = count_wall(family, loaded.quantum_action)
    saw = seen(lines, names, str(expected["family"]), window)
    shares = [saw[name] for _at, name in placed]
    quanta = sum(shares) // wall
    seed = expected.get("seed")
    aside = [str(name) for name in expected.get("aside", [])]  # bare regions read beside the screen
    aside_seen = seen(lines, aside, str(expected["family"]), window)
    aside_entries = rises(lines, aside, str(expected["family"]), window)
    first, last = int(expected["pattern"][0]), int(expected["pattern"][1])
    maxima, minima = extrema(found, first, last)
    watched = [int(at) for at in expected.get("maxima", [])]
    least = [int(at) for at in expected.get("minima", [])]
    visibility = None  # none where the blind row names no minima (one region, no fringe to read)
    if watched and least:
        most, low = found[watched[len(watched) // 2]], sum(found[at] for at in least)
        visibility = [most * len(least) - low, most * len(least) + low]
    return {
        "verdict": "DETECTOR",
        "detector": named if named is not None else names,
        "family": expected["family"],
        "window": list(window),
        "across": expected["across"],
        "at": [at for at, _name in placed],
        "rises": found,
        "blind": expected["counts"],
        "through": sum(found),
        "blind_through": expected["through"],
        "maxima": maxima,
        "minima": minima,
        "blind_maxima": watched,
        "blind_minima": least,
        "visibility": visibility,
        "blind_visibility": expected.get("visibility"),
        "deviation": deviation(found, list(expected["counts"])),
        "seen": shares,
        "quanta": quanta,
        "blind_quanta": expected.get("quanta"),
        "laid": expected.get("laid"),
        "elsewhere": int(expected["laid"]) - quanta if "laid" in expected else None,
        "credited": apportioned(quanta, shares),
        "drawn": drawn(quanta, shares, int(seed)) if seed is not None else None,
        "seed": seed,
        "credited_deviation": deviation(apportioned(quanta, shares), list(expected["counts"])),
        "aside": {
            name: {
                "seen": aside_seen[name],
                "quanta": aside_seen[name] // wall,
                "entries": aside_entries.get(name, 0),
            }
            for name in aside
        },
        "clicks_in_all": sum(1 for line in lines if line.get("event") == "click"),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--world", type=Path, required=True, help="the world file the run ran")
    parser.add_argument("--output", type=Path, required=True, help="the run's output file")
    parser.add_argument("--expectation", type=Path, required=True, help="the blind expectation file")
    args = parser.parse_args(argv)
    print(json.dumps(reading(args.world, args.output, args.expectation)))


if __name__ == "__main__":
    main()

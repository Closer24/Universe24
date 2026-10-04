"""The credit per node_reader over a window of intervals, read from a run's output file against an expectation file (NODEREADER, the one measurement; ALGEBRA.md #the-count-is-the-records-share, the node_reader a declared NodeReader and the click its report; #the-click-is-the-meeting, the share's sign and the credit's floor): the `click` lines of the expectation's node_reader (or node_readers, a list) and one family within the window are summed per node_reader, each one reporter placed at the least coordinate of its Nodes on the axis the expectation names (`across`), so a region across the beam stands at its first row (a click reports its region and never a Node, the owner's word of 2026-09-30). What each node_reader saw, the net inflow through its front boundary summed over the window (the density that entered it from the declared board), floored at 0, the NodeReader's declaration (the owner's word of 2026-10-01, 09:00, on the mathematician's #1572 comment 5925377771: a region's credit is max(s_R, 0) where a window is cut or a record returns through the front, the window the whole passage where it can be), gives its share of the screen's total; N, the quanta the screen absorbed, is the total inflow over the family's count wall W_c to the nearest whole, (total + W_c div 2) div W_c, the share's own rounding, and the expectation's declared total less N (`elsewhere`, the expectation's `laid`) is the part that left the board elsewhere; the rounded shares are N times the shares apportioned by the largest remainders (a tie of remainders broken by the lower index), the expectation and no sample, and the clicks are the quanta the draw credited inside the run, per region the `credit` lines' counts within the window (the click written on the lattice with the world's declared seed and generator, `src/event_universe/credit.py`; one quantum to one node_reader by the draw's construction; None for a world declaring no draw), the tool drawing nothing (the advisor's design at the owner's word, #1515 comment 5912573191, with his corrections 5912958018; the rows named by the owner's word of 2026-10-01, 04:50). Both rows are read beside the blind counts with their local maxima and minima within the pattern's range (`extrema`, the one rule of the builder and the reader), the visibility at the blind central maximum (the expectation's `central`) against the blind first minima, (most - least) over (most + least), as integers, and the summed absolute deviation from the blind row's shares over the total, sum |n_g B - T b_g| over T B (T the row's total, B the blind row's), as a fraction; a bare region named in the expectation's `aside` is read beside the screen (what it saw and that over W_c) and takes no share. The arrival (the wager, the lattice's own number): the screen's inflow summed over its regions per interval within the window, its peak interval (the first at the largest), its centroid over every interval of the window, the negative ones included, as an exact fraction and its half-maximum span, in the engine's interval labels (the click at interval t reports the state after t - 1 steps), beside the expectation's blind arrival; the wings the expectation names are read from both rows. The window, the node_readers, the family, the axis, the pattern's range and the seed are the expectation file's; the tool holds no number.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/click_counts.py --world <world>.json --output <world>.output.json --expectation <expectation>.json
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path

import numpy as np

from event_universe.loader.derived import count_wall
from event_universe.loader.keys import AXES
from event_universe.loader.world import NodeReaderRow, World
from event_universe.world_files import load_world

Reporter = tuple[int, str]  # its coordinate on the axis (the least of its Nodes'), its node_reader


def inflows(
    lines: list[dict[str, object]], node_readers: list[str], family: str, window: tuple[int, int]
) -> dict[str, int]:
    """What each named node_reader saw of one family within the window [first, last] of intervals: its `click` lines' net front inflows summed, in the current's units (0 where it saw nothing; a click reports its region, never a Node)."""
    found = {name: 0 for name in node_readers}
    for line in lines:
        if line.get("event") != "click" or line.get("family") != family:
            continue
        if line.get("node_reader") in found and window[0] <= int(str(line["interval"])) <= window[1]:
            found[str(line["node_reader"])] += int(str(line["inflow"]))
    return found


def per_interval(
    lines: list[dict[str, object]], node_readers: list[str], family: str, window: tuple[int, int]
) -> dict[int, int]:
    """The screen's inflow per interval within the window, the named node_readers' `click` lines summed at each interval, in the current's units."""
    found: dict[int, int] = {}
    for line in lines:
        if line.get("event") != "click" or line.get("family") != family:
            continue
        interval = int(str(line["interval"]))
        if line.get("node_reader") in node_readers and window[0] <= interval <= window[1]:
            found[interval] = found.get(interval, 0) + int(str(line["inflow"]))
    return found


def arrival(profile: dict[int, int]) -> dict[str, object]:
    """The arrival of the screen's inflow over every interval of the window, the negative ones included (the law names the peak and the centroid over the window and excludes nothing): the peak interval (the first at the largest inflow), the centroid as [numerator, denominator] (the intervals weighted by their inflow, an exact fraction) and the half-maximum span, the first and the last interval at or above half the peak; None where nothing arrived (no inflow above 0, or the window's sum not above 0)."""
    if not profile or max(profile.values()) <= 0 or sum(profile.values()) <= 0:
        return {"peak": None, "centroid": None, "span": None}
    largest = max(profile.values())
    peak = min(interval for interval, value in profile.items() if value == largest)
    centroid = Fraction(
        sum(interval * value for interval, value in profile.items()), sum(profile.values())
    )
    high = [interval for interval, value in profile.items() if 2 * value >= largest]
    return {
        "peak": peak,
        "centroid": [centroid.numerator, centroid.denominator],
        "span": [min(high), max(high)],
    }


def nearest(total: int, wall: int) -> int:
    """A total in quanta to the nearest whole, (total + W_c div 2) div W_c, the share's own rounding (ALGEBRA.md #the-count-is-the-records-share)."""
    return (total + wall // 2) // wall


def apportioned(quanta: int, shares: list[int]) -> list[int]:
    """N apportioned by the shares to whole numbers, the largest remainders first (a tie of remainders broken by the lower index, the NodeReader's declaration): the rounded shares, the expectation and no sample (0 everywhere where nothing was seen)."""
    total = sum(shares)
    if not total or quanta <= 0:
        return [0] * len(shares)
    floors = [quanta * share // total for share in shares]
    rests = sorted(range(len(shares)), key=lambda i: (-(quanta * shares[i] % total), i))
    for index in rests[: quanta - sum(floors)]:
        floors[index] += 1
    return floors


def credited(
    lines: list[dict[str, object]], node_readers: list[str], family: str, window: tuple[int, int]
) -> dict[str, int] | None:
    """The quanta the draw credited to each named node_reader inside the run, its `credit` lines' counts of one family within the window summed, the clicks; None where the output holds no credit line of the family (a world declaring no draw)."""
    found = {name: 0 for name in node_readers}
    seen = False
    for line in lines:
        if line.get("event") != "credit" or line.get("family") != family:
            continue
        seen = True
        if line.get("node_reader") in found and window[0] <= int(str(line["interval"])) <= window[1]:
            found[str(line["node_reader"])] += int(str(line["count"]))
    return found if seen else None


def deviation(found: list[int], blind: list[object]) -> list[int]:
    """The summed absolute deviation of a row from the blind row's shares over the total, sum |n_g B - T b_g| over T B with T the row's total and B the blind row's, as [numerator, denominator]; [0, 1] where the row is empty."""
    shares = [Fraction(str(value)) for value in blind]
    total, whole = sum(found), sum(shares)
    if not total or not whole:
        return [0, 1]
    value = sum(abs(n * whole - total * b) for n, b in zip(found, shares, strict=True)) / (total * whole)
    return [value.numerator, value.denominator]


def reporters(rows: list[NodeReaderRow], axis: int) -> list[Reporter]:
    """The reporters across `axis`, one per node_reader, ordered by their coordinate on it, the least of the node_reader's Nodes' (a region across the beam at its first row)."""
    return sorted((min(node[axis] for node in row.positions), row.name) for row in rows)


def extrema(row: Sequence[float], first: int, last: int) -> tuple[list[int], list[int]]:
    """The local maxima and minima of a row within [first, last], the one rule of the builder and the reader (examples/events/two_slits/build_world.py imports it for the blind row): a position above its left neighbour and at or above its right (a maximum), or below its left and at or below its right (a minimum); the row's own ends, with one neighbour, are neither."""
    inside = [at for at in range(first, last + 1) if 0 < at < len(row) - 1]
    maxima = [at for at in inside if row[at] > row[at - 1] and row[at] >= row[at + 1]]
    minima = [at for at in inside if row[at] < row[at - 1] and row[at] <= row[at + 1]]
    return maxima, minima


def read_row(row: list[int], expected: dict[str, object]) -> dict[str, object]:
    """One row's readings against the expectation: the row, its local maxima and minima within the pattern's range, the visibility at the blind central maximum (the expectation's `central`; the middle of the blind maxima where it names none) against the blind minima as [most x the minima's count - least, the same sum] and the deviation from the blind row's shares; the visibility None where the blind names no minima; the wings the expectation names, the row's counts there."""
    first, last = int(expected["pattern"][0]), int(expected["pattern"][1])  # type: ignore[index]
    maxima, minima = extrema(row, first, last)
    watched = [int(at) for at in expected.get("maxima", [])]  # type: ignore[union-attr]
    least = [int(at) for at in expected.get("minima", [])]  # type: ignore[union-attr]
    central = expected.get("central", watched[len(watched) // 2] if watched else None)
    visibility = None
    if central is not None and least:
        most, low = row[int(str(central))], sum(row[at] for at in least)
        visibility = [most * len(least) - low, most * len(least) + low]
    wings = expected.get("wings", {})
    regions = [int(at) for at in wings.get("regions", [])] if isinstance(wings, dict) else []
    return {
        "row": row,
        "maxima": maxima,
        "minima": minima,
        "visibility": visibility,
        "deviation": deviation(row, list(expected["counts"])),  # type: ignore[arg-type]
        "wings": [row[at] for at in regions],
    }


def photons(loaded: World, family: str, quanta: int, blind: object) -> dict[str, object]:
    """The photon count at the light's own frequency beside N, a lattice reading labelled so (the mathematician's 214, #1572 comment 5965082449, with the advisor's second, #1563 comment 5965316267): the screen's regions declare the band's top, so N counts the energy in units of T, while one quantum of the laid light at its own omega carries the energy T sin omega, cos omega = (cos(pi p / q) + 2) / 3 along the axis for the wave [p, q] of the family's first packet; the count N over sin omega is the number of the laid light's own quanta, 645 at N = 278 and k = pi / 4; the blind's value, where the expectation holds one, beside it."""
    waves = [m.wave for m in loaded.packets if loaded.families[m.family].name == family]
    if not waves:
        return {"label": "LATTICE", "value": None}
    p, q = waves[0]
    cosine = (float(np.cos(np.pi * p / q)) + 2) / 3  # light's dispersion along the axis
    sine = (1 - cosine * cosine) ** (1 / 2)
    return {
        "label": "LATTICE",
        "sin_omega": round(sine, 3),
        "value": round(quanta / sine, 1),
        "blind": blind,
    }


def reading(world: Path, output: Path, expectation: Path) -> dict[str, object]:
    """The reading: what each node_reader of the expectation's node_reader (or node_readers) and family saw over its window, ordered along its axis, floored at 0, N over the wall to the nearest whole, the rounded shares (the expectation) and the clicks (the quanta the draw credited in the run, from the credit lines), each row with its extrema, visibility and deviation, the arrival of the screen's inflow in the engine's labels, with the blind numbers beside."""
    expected = json.loads(expectation.read_text(encoding="utf-8"))
    document = json.loads(output.read_text(encoding="utf-8"))
    lines = document["lines"]
    loaded = load_world(world)
    axis = AXES.index(expected["across"])
    named = expected.get("node_reader")
    if named is None:  # every node_reader but the open faces' layer, over the whole run
        rows = [d for d in loaded.node_readers if d.declared]
        names = [d.name for d in rows]
    else:
        names = [str(name) for name in named] if isinstance(named, list) else [str(named)]
        rows = [d for d in loaded.node_readers if d.name in names]
    if len(rows) != len(names):
        raise ValueError(
            f"the expectation names the node_readers {names}; the world declares {[d.name for d in loaded.node_readers]}"
        )
    spanned = expected.get("window", [0, document.get("intervals", 0)])
    window = (int(spanned[0]), int(spanned[1]))
    placed = reporters(rows, axis)
    family = next(f for f in loaded.families if f.name == expected["family"])
    wall = count_wall(family, loaded.quantum_action)
    saw = inflows(lines, names, str(expected["family"]), window)
    seen = [saw[name] for _at, name in placed]
    shares = [max(value, 0) for value in seen]  # the credit's floor, the NodeReader's declaration
    quanta = nearest(sum(shares), wall)
    aside = [str(name) for name in expected.get("aside", [])]  # bare regions read beside the screen
    aside_seen = inflows(lines, aside, str(expected["family"]), window)
    rounded = apportioned(quanta, shares)
    credits = credited(lines, names, str(expected["family"]), window)
    clicks = [credits[name] for _at, name in placed] if credits is not None else None
    blind_row = [Fraction(str(value)) for value in expected["counts"]]
    return {
        "verdict": "NODEREADER",
        "node_reader": named if named is not None else names,
        "family": expected["family"],
        "window": list(window),
        "across": expected["across"],
        "at": [at for at, _name in placed],
        "seen": seen,
        "floored": [value for value in shares if value] != [value for value in seen if value],
        "quanta": quanta,
        "blind_quanta": expected.get("quanta"),
        "laid": expected.get("laid"),
        "elsewhere": int(expected["laid"]) - quanta if "laid" in expected else None,
        "rounded_shares": read_row(rounded, expected),
        "clicks": read_row(clicks, expected) if clicks is not None else None,
        "seed": expected.get("seed"),
        "blind": {
            "counts": expected["counts"],
            "maxima": [int(at) for at in expected.get("maxima", [])],
            "minima": [int(at) for at in expected.get("minima", [])],
            "visibility": expected.get("visibility"),
            "wings": expected.get("wings"),
            "sum": [sum(blind_row).numerator, sum(blind_row).denominator],
        },
        "photons": photons(loaded, str(expected["family"]), quanta, expected.get("photons")),
        "arrival": arrival(per_interval(lines, names, str(expected["family"]), window)),
        "blind_arrival": expected.get("arrival"),
        "aside": {
            name: {"seen": aside_seen[name], "quanta": nearest(max(aside_seen[name], 0), wall)}
            for name in aside
        },
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

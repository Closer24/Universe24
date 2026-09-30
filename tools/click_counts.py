"""The rises per detector Node over a window of intervals, read from a run's output file against an expectation file (DETECTOR, the one measurement): the click lines of one detector and one family within the window are counted per Node, the Nodes ordered by their coordinate on the axis the expectation names (`across`), and printed beside the blind counts with the total through the detector, the local maxima and minima of the rises within the pattern's range, and the visibility at the blind central maximum against the blind minima, (most - least) over (most + least), as integers. The window, the detector, the family, the axis and the pattern's range are the expectation file's; the tool holds no number.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/click_counts.py --world <world>.json --output <world>.output.json --expectation <expectation>.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from event_universe.loader.keys import AXES
from event_universe.world_files import load_world


def rises(
    lines: list[dict[str, object]], detector: str, family: str, window: tuple[int, int]
) -> dict[tuple[int, ...], int]:
    """The clicks per Node of one detector and one family within the window [first, last] of intervals."""
    found: dict[tuple[int, ...], int] = {}
    for line in lines:
        if line.get("event") != "click" or line.get("detector") != detector:
            continue
        if line.get("family") != family or not window[0] <= int(str(line["tick"])) <= window[1]:
            continue
        node = tuple(int(i) for i in list(line["node"]))  # type: ignore[call-overload]
        found[node] = found.get(node, 0) + 1
    return found


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
    """The reading: the rises per Node of the expectation's detector and family over its window, ordered along its axis, with the blind counts, the totals, the extrema and the visibility."""
    expected = json.loads(expectation.read_text(encoding="utf-8"))
    lines = json.loads(output.read_text(encoding="utf-8"))["lines"]
    loaded = load_world(world)
    row = next(d for d in loaded.detectors if d.name == expected["detector"])
    axis = AXES.index(expected["across"])
    window = (int(expected["window"][0]), int(expected["window"][1]))
    counted = rises(lines, str(expected["detector"]), str(expected["family"]), window)
    nodes = sorted(row.positions, key=lambda node: node[axis])
    risen = [counted.get(node, 0) for node in nodes]
    first, last = int(expected["pattern"][0]), int(expected["pattern"][1])
    maxima, minima = extrema(risen, first, last)
    watched = [int(at) for at in expected["maxima"]]
    least = [int(at) for at in expected["minima"]]
    most = risen[watched[len(watched) // 2]]
    low = sum(risen[at] for at in least)
    visibility = (most * len(least) - low, most * len(least) + low)
    return {
        "verdict": "DETECTOR",
        "detector": expected["detector"],
        "family": expected["family"],
        "window": list(window),
        "across": expected["across"],
        "rises": risen,
        "blind": expected["counts"],
        "through": sum(risen),
        "blind_through": expected["through"],
        "maxima": maxima,
        "minima": minima,
        "blind_maxima": expected["maxima"],
        "blind_minima": expected["minima"],
        "visibility": list(visibility),
        "blind_visibility": expected["visibility"],
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

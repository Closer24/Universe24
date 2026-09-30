"""The rises per reporter over a window of intervals, read from a run's output file against an expectation file (DETECTOR, the one measurement): the click lines of the expectation's detector (or detectors, a list) and one family within the window are counted per reporter, ordered by its coordinate on the axis the expectation names (`across`): a detector whose Nodes share one coordinate on that axis is one reporter placed at it (a group across the beam), and a detector whose Nodes spread along it reports per Node; the rises are printed beside the blind counts with the total through the reporters, the local maxima and minima of the rises within the pattern's range, and the visibility at the blind central maximum against the blind minima, (most - least) over (most + least), as integers. An expectation without `detector` (the train's, tools/train_clicks.py's) reads every detector whose Nodes share one coordinate on the axis, over the whole run where it names no window. The window, the detectors, the family, the axis and the pattern's range are the expectation file's; the tool holds no number.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/click_counts.py --world <world>.json --output <world>.output.json --expectation <expectation>.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from event_universe.loader.keys import AXES
from event_universe.loader.world import DetectorRow
from event_universe.world_files import load_world

Node = tuple[int, ...]
Reporter = tuple[
    int, str, Node | None
]  # its coordinate on the axis, its detector, its Node (None: the group)


def rises(
    lines: list[dict[str, object]], detectors: list[str], family: str, window: tuple[int, int]
) -> dict[tuple[str, Node], int]:
    """The clicks per detector and Node of the named detectors and one family within the window [first, last] of intervals."""
    found: dict[tuple[str, Node], int] = {}
    for line in lines:
        if line.get("event") != "click" or line.get("detector") not in detectors:
            continue
        if line.get("family") != family or not window[0] <= int(str(line["tick"])) <= window[1]:
            continue
        key = str(line["detector"]), tuple(int(i) for i in list(line["node"]))  # type: ignore[call-overload]
        found[key] = found.get(key, 0) + 1
    return found


def reporters(rows: list[DetectorRow], axis: int) -> list[Reporter]:
    """The reporters across `axis`, ordered by their coordinate on it: a detector whose Nodes share one coordinate on the axis is one reporter placed at it, and one whose Nodes spread along it reports per Node."""
    found: list[Reporter] = []
    for row in rows:
        shared = {node[axis] for node in row.positions}
        if len(shared) == 1:
            found.append((shared.pop(), row.name, None))
        else:
            found.extend((node[axis], row.name, node) for node in row.positions)
    return sorted(found, key=lambda reporter: reporter[:2])


def risen(counted: dict[tuple[str, Node], int], reporter: Reporter) -> int:
    """A reporter's rises: its Node's, or every Node's of its detector for a group."""
    _at, name, node = reporter
    return sum(
        count for (detector, at), count in counted.items() if detector == name and node in (None, at)
    )


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
    """The reading: the rises per reporter of the expectation's detector (or detectors) and family over its window, ordered along its axis, with the blind counts, the totals, the extrema and the visibility."""
    expected = json.loads(expectation.read_text(encoding="utf-8"))
    document = json.loads(output.read_text(encoding="utf-8"))
    lines = document["lines"]
    loaded = load_world(world)
    axis = AXES.index(expected["across"])
    named = expected.get("detector")
    if named is None:  # the train's expectation: every group placed on the axis, over the whole run
        rows = [d for d in loaded.detectors if len({node[axis] for node in d.positions}) == 1]
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
    found = [risen(counted, reporter) for reporter in placed]
    first, last = int(expected["pattern"][0]), int(expected["pattern"][1])
    maxima, minima = extrema(found, first, last)
    watched = [int(at) for at in expected["maxima"]]
    least = [int(at) for at in expected["minima"]]
    most = found[watched[len(watched) // 2]]
    low = sum(found[at] for at in least)
    visibility = (most * len(least) - low, most * len(least) + low)
    return {
        "verdict": "DETECTOR",
        "detector": named if named is not None else names,
        "family": expected["family"],
        "window": list(window),
        "across": expected["across"],
        "at": [at for at, _name, _node in placed],
        "rises": found,
        "blind": expected["counts"],
        "through": sum(found),
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

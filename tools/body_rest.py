"""The bodies' rest, a lattice reading labelled so and no measurement (docs/ENGINE.md #6-how-to-run-a-world; ALGEBRA.md #the-stable-body, #a-familys-declaration; the families round's worlds under examples/events/): a world of one or two bodies on any board is loaded as tools/run_inputs.py loads it and stepped by the engine's own step over the window; at the window's ends every body is read from its record and from the rows it sources. Per body: its centre (the declared Node of its largest count); the three levels of its record about one interval at the centre, [before, now, next], whose ratio (next + before) / now is 2 cos omega_b, the rest rotation of the standing record, an exact fraction (ALGEBRA.md #the-bound-body-is-one-node); the content its record reads at the centre, the held rows' levels at the law's weights (`Lattice.read`), and the one-Node line at the composed clock read at that content, 2 cos omega = 2 - 2 ((den - num) / den) (1 - 1 / Gamma)^(2 c), the Node's own rest rotation and not the bound omega_b the tail fixes (ALGEBRA.md, The paces compose; The bound body is one Node), as a decimal; its Wronskian at the centre where the body is a plane (its sense, the source of the holder of the sign); its share in quanta at the centre Node and summed over its region (the half of the board nearer its centre along the axis joining two bodies' centres, the whole board for a single body); the centroid of its share over its region and the share-weighted second moment about the centroid (the rms radius squared), exact fractions at the file's coordinates; its well over its region, the form D = now^2 - next x before summed over the region and divided by T, in quanta (the source of the rows holding the content); its record's level along each axis from the centre outward (the tail) with the ratios of successive levels (e^(-kappa) per Link where the tail is evanescent); and every held row's time level along the same axes (a holder of the content's rest about a body, 3 G(r) s on an open box; the holder of the sign's about a plane, light as the sum of its rows, `Lattice.record`). For two bodies the separation of the centroids along the joining axis at the window's ends and its change; the books at the end and, beside their drift, the two terms of the drift's identity summed over every interval the reader stepped (ALGEBRA.md #the-count-is-the-records-share, The share's change is the currents: at the paces a step read, the share's change is the weighted currents less Rule3's remainder term, exactly in rationals; #the-conserved-form: the form changes by the work term where the paces move): the work term of L510, the share of the step's pair at the paces after the step less the same pair at the paces the step read (`work_term`), and Rule3's remainder term, the rounding of the level (`remainder_term`), so that the books' drift is their sum plus the currents through the faces, to the per-Node division's rounding; in the current's units and in quanta, a lattice reading and no fence. With a run's output file the `field` lines of the regions the expectation names (or of every region) are read over the window, each region's least and largest reading with their intervals and the count of its local maxima (a swinging count's beat). With an expectation file its blind is printed beside the readings. The tool compares nothing, holds no number of the law and writes nothing to the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python tools/body_rest.py [--intervals N] [--reach R] [--expectation <expectation>.json] [--output <world>.output.json ...] <world>.json ...
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from event_universe import node, share
from event_universe.lattice import Lattice
from event_universe.loader.derived import count_wall, quanta_records
from event_universe.loader.keys import AXES
from event_universe.world_files import load_world

LABEL = "LATTICE"
Node = tuple[int, ...]


def pair(value: Fraction | None) -> list[int] | None:
    """A fraction as [numerator, denominator] for the output, None where there is none."""
    return None if value is None else [value.numerator, value.denominator]


def copied(record: node.Record) -> node.Record:
    """A record's two levels copied, its remainder shared: the interval's start kept while the board steps."""
    return node.Record(record.now.copy(), record.before.copy(), record.remainder)


def centre_of(board: Lattice, number: int) -> Node:
    """A body's centre: the declared Node of its largest count (the first at a tie), at the file's coordinates."""
    row = board.world.bodies[number]
    at = max(range(len(row.nodes)), key=lambda i: (row.counts[i], -i))
    return row.nodes[at]


def joining_axis(centres: list[Node]) -> int:
    """The axis joining two bodies' centres, the one along which they stand furthest apart (the first at a tie)."""
    gaps = [abs(centres[1][axis] - centres[0][axis]) for axis in range(len(AXES))]
    return gaps.index(max(gaps))


def regions(board: Lattice, centres: list[Node]) -> list[np.ndarray]:
    """Each body's region as a mask over the board: the whole board for one body; for two, the half nearer its centre along the joining axis, split midway between the centres (the first body's half ends before the split)."""
    if len(centres) == 1:
        return [np.ones(board.shape, dtype=bool)]
    axis = joining_axis(centres)
    first, second = sorted(c[axis] for c in centres)
    split = (first + second + 1) // 2 + board.offset[axis]
    along = np.arange(board.shape[axis]).reshape([-1 if a == axis else 1 for a in range(len(AXES))])
    low = np.broadcast_to(along < split, board.shape)
    return [low, ~low] if centres[0][axis] <= centres[1][axis] else [~low, low]


def moments(density: np.ndarray, region: np.ndarray, offset: Node) -> dict[str, object]:
    """The centroid of a density over a region and its second moment about the centroid, exact fractions at the file's coordinates (`offset` the layers grown before the origin); None where the density sums to 0."""
    weights = np.where(region, density, 0)
    total = int(weights.sum(dtype=object))
    if total == 0:
        return {"total": 0, "centroid": None, "second_moment": None}
    grids = np.indices(density.shape)
    centroid = [
        Fraction(int((weights * grids[axis]).sum(dtype=object)), total) - offset[axis]
        for axis in range(len(AXES))
    ]
    second = Fraction(0)
    for axis in range(len(AXES)):
        coordinate = grids[axis].astype(object) - offset[axis]
        second += Fraction(int((weights * coordinate * coordinate).sum(dtype=object)), total)
        second -= centroid[axis] * centroid[axis]
    return {"total": total, "centroid": [pair(c) for c in centroid], "second_moment": pair(second)}


def along(array: np.ndarray, centre: Node, axis: int, reach: int, offset: Node) -> list[int]:
    """An array's values at the Nodes from the centre outward along the + side of one axis, r = 0 through `reach`, at the file's coordinates, stopping at the board's edge."""
    found = []
    for r in range(reach + 1):
        at = [c + o for c, o in zip(centre, offset, strict=True)]
        at[axis] += r
        if not 0 <= at[axis] < array.shape[axis]:
            break
        found.append(int(array[at[0], at[1], at[2]]))
    return found


def ratios(levels: list[int]) -> list[list[int] | None]:
    """The ratio of each level to the one before it along a ray, [level(r + 1), level(r)], None where the level before is 0."""
    return [None if a == 0 else [b, a] for a, b in zip(levels, levels[1:], strict=False)]


def body_reading(
    board: Lattice,
    number: int,
    region: np.ndarray,
    begun: list[node.Record],
    share: np.ndarray,
    quanta: np.ndarray,
    reach: int,
    content: Any,
) -> dict[str, object]:
    """One body's reading about one interval: the board has stepped once since `begun`, `share`, `quanta` and `content` (the record's read at the interval's start, `Lattice.read`) were read, so its records' `now` is the next level; everything else is of the interval's start, the one-Node line at the composed clock read at the content at the centre among it (ALGEBRA.md, The paces compose; The bound body is one Node)."""
    row = board.world.bodies[number]
    family, state = board.families[row.family], board.states[row.family]
    centre = centre_of(board, number)
    at = tuple(c + o for c, o in zip(centre, board.offset, strict=True))
    before, now, after = (int(a[at]) for a in (begun[0].before, begun[0].now, state.lines[0].now))
    num, den, gamma = *family.pair, board.world.node_clock
    read_content = int(content[at]) if np.ndim(content) else int(content)
    one_node = 2 - 2 * Fraction(den - num, den) * Fraction(gamma - 1, gamma) ** (2 * read_content)
    form = node.form(begun, state.lines[: family.record])
    well_sum = int(np.where(region, form, 0).sum(dtype=object))
    wronskian = node.wronskian(begun, family.plane)
    held = {
        board.families[index].name: {
            AXES[axis]: along(board.record(index)[0].now, centre, axis, reach, board.offset)
            for axis in range(len(AXES))
        }
        for index in board.held
    }
    tails = {
        AXES[axis]: along(begun[0].now, centre, axis, reach, board.offset) for axis in range(len(AXES))
    }
    return {
        "family": family.name,
        "centre": list(centre),
        "levels_at_centre": [before, now, after],
        "two_cos_omega": None if now == 0 else pair(Fraction(after + before, now)),
        "content_at_centre": read_content,
        "one_node_line_at_centre": float(one_node),
        "wronskian_at_centre": None if not family.plane else int(np.asarray(wronskian)[at]),
        "quanta_at_centre": int(quanta[at]),
        "quanta_in_region": int(np.where(region, quanta, 0).sum(dtype=object)),
        "share": moments(share, region, board.offset),
        "well_in_quanta": well_sum // board.world.quantum_action,
        "tail": {axis: {"levels": levels, "ratios": ratios(levels)} for axis, levels in tails.items()},
        "held": held,
    }


def grown(
    array: np.ndarray, shape: tuple[int, ...], offset: Node, board: Lattice, fill: int = 0
) -> np.ndarray:
    """An array kept before a step brought to the board's shape after it: where a receding face grew the lattice during the step (`growth.resize`), the layers grown before the origin (the offset's change) are prepended and the rest appended, filled with `fill` (0 for a level or a content, the vacuum's G^2 for a Link's factor), so that the interval's start and its end are read at the same Nodes."""
    pads = []
    for axis in range(len(AXES)):
        low = board.offset[axis] - offset[axis]
        pads.append((low, board.shape[axis] - shape[axis] - low))
    return np.pad(array, pads, constant_values=fill) if any(pad != (0, 0) for pad in pads) else array


def paces_read(board: Lattice, index: int) -> list[tuple[Any, node.Factors]]:
    """A family of quanta's reads at the interval's start, one per record (`Lattice.read`): the content at every Node and its six Links' factors, the paces the step from this interval reads, kept so that the step's pair can be read again at them after the step."""
    return [board.read(index, 1, record) for record in quanta_records(board.families, index)]


def work_term(
    board: Lattice,
    index: int,
    reads: list[tuple[Any, node.Factors]],
    shape: tuple[int, ...],
    offset: Node,
) -> int:
    """The work term of L510 over the one step the board has taken since `reads` were kept, summed over the lattice in the current's units, a lattice reading (ALGEBRA.md #the-conserved-form: the form is exact where the paces stand and changes by the work term where they move; #the-count-is-the-records-share, The share's change is the currents: at the paces the step read, the share's change is the weighted currents less Rule3's remainder term exactly): the family's share of the step's pair at the paces after the step (`Lattice.share_of`) less the same pair at the paces the step read (`share.family_share` with the kept content and factors, grown with the board where a face grew during the step, the vacuum's content 0 and factor G^2 on the grown layers), so that the books' drift is this term's sum over the run plus the currents through the faces, to the rounding."""
    family, gamma, unit = board.families[index], board.world.node_clock, board.unit
    after = int(board.share_of(index)[0].sum(dtype=object))
    at_read = 0
    for record, (content, factors) in zip(quanta_records(board.families, index), reads, strict=True):
        kept = grown(content, shape, offset, board) if np.ndim(content) else content
        links = tuple(
            grown(factor, shape, offset, board, unit * unit) if np.ndim(factor) else factor
            for factor in factors
        )
        lines = board.lines_of(index, record)
        found = share.family_share(family, lines, board.wrap, gamma, kept, links, unit)
        at_read += int(found.sum(dtype=object))
    return after - at_read


def remainder_term(
    board: Lattice,
    index: int,
    reads: list[tuple[Any, node.Factors]],
    kept: list[list[node.Record]],
    shape: tuple[int, ...],
    offset: Node,
) -> int:
    """Rule3's remainder term over the one step the board has taken since `kept` and `reads` were kept, summed over the lattice in the current's units, a lattice reading (ALGEBRA.md #the-count-is-the-records-share, The share's change is the currents, the identity's second term: (next_i - before_i) (r_i - r'_i) over 2 p_i^2 G^2 at the paces the step read, r and r' the record's remainder before and after the step, Rule3's own rounding of the level, by the division act at every Node (`share.over_pace`); the kept arrays grown with the board where a face grew during the step, the level 0 and the family's origin remainder on the grown layers), so that the books' drift is this term plus the work term plus the currents through the faces, to the per-Node division's rounding."""
    gamma, unit, origin = board.world.node_clock, board.unit, board.origins[index]
    found = 0
    for record, (content, _factors), begun in zip(
        quanta_records(board.families, index), reads, kept, strict=True
    ):
        for old, new in zip(begun, board.lines_of(index, record), strict=True):
            before = grown(old.before, shape, offset, board)
            carried = grown(
                np.broadcast_to(np.asarray(old.remainder), shape), shape, offset, board, origin
            )
            left = np.broadcast_to(np.asarray(new.remainder), new.now.shape)
            at = (new.now != 0) | (before != 0)
            moved = new.now[at].astype(object) - before[at].astype(object)
            numerator = moved * (carried[at].astype(object) - left[at].astype(object))
            paced = grown(content, shape, offset, board)[at] if np.ndim(content) else content
            found += int(share.over_pace(numerator, gamma, paced, unit).sum(dtype=object))
    return found


def stepped(board: Lattice, terms: dict[int, dict[str, int]]) -> None:
    """The board stepped once, the step's two terms of the drift's identity added to every family of quanta's running sums (`work_term`, `remainder_term`): the reads, the records and the board's shape kept before the step, so that the step's pair is read at the paces the step read, over the board as grown."""
    shape, offset = tuple(board.shape), tuple(board.offset)
    reads = {index: paces_read(board, index) for index in board.order}
    kept = {
        index: [
            [
                node.Record(line.now.copy(), line.before.copy(), np.array(line.remainder, copy=True))
                for line in board.lines_of(index, record)
            ]
            for record in quanta_records(board.families, index)
        ]
        for index in board.order
    }
    board.step()
    for index in board.order:
        terms[index]["work_term"] += work_term(board, index, reads[index], shape, offset)
        terms[index]["remainder_term"] += remainder_term(
            board, index, reads[index], kept[index], shape, offset
        )


def in_quanta(value: int, wall: int) -> dict[str, int]:
    """A sum in the current's units with the same in quanta over the family's wall by the books' own rounding (`share.quanta_of`)."""
    return {
        "share": value,
        "quanta": int(share.quanta_of(np.array([value], dtype=object), wall, object)[0]),
    }


def work_books(board: Lattice, terms: dict[int, dict[str, int]]) -> dict[str, dict[str, Any]]:
    """The work term of L510 summed over every interval the reader stepped, per family of quanta, printed beside the books' drift with Rule3's remainder term, the other term of the drift's identity (`remainder_term`): each in the current's units (`share`) and in quanta (`in_quanta`), labelled a lattice reading and no fence; the books' drift is the two plus the currents through the faces, to the per-Node division's rounding."""
    found: dict[str, dict[str, Any]] = {}
    for index in board.order:
        wall = count_wall(board.families[index], board.world.quantum_action)
        work, remainder = terms[index]["work_term"], terms[index]["remainder_term"]
        found[board.families[index].name] = {
            "label": LABEL,
            **in_quanta(work, wall),
            "remainder_term": in_quanta(remainder, wall),
        }
    return found


def read_about_one_interval(
    board: Lattice, centres: list[Node], reach: int, terms: dict[int, dict[str, int]]
) -> list[dict[str, object]]:
    """Every body's reading about the interval the board is at: the records, shares, quanta and the records' reads (the content) of the start are kept, the board steps once (`stepped`, the step's two terms of the drift's identity added to `terms`; grown at a receding face where the front reaches it, the kept arrays grown with it, `grown`), the regions are read at the board's shape after the step, and each body is read (`body_reading`)."""
    shape, offset = tuple(board.shape), tuple(board.offset)
    kept = {}
    for number, row in enumerate(board.world.bodies):
        begun = [
            copied(line) for line in board.states[row.family].lines[: board.families[row.family].record]
        ]
        kept[number] = (
            begun,
            board.share_of(row.family)[0].copy(),
            board.quanta(row.family)[0].copy(),
            board.read(row.family, 1, 0)[0],
        )
    stepped(board, terms)
    masks = regions(board, centres)
    found = []
    for number in range(len(board.world.bodies)):
        begun, share, quanta, content = kept[number]
        begun = [
            node.Record(
                grown(line.now, shape, offset, board),
                grown(line.before, shape, offset, board),
                line.remainder,
            )
            for line in begun
        ]
        share, quanta = grown(share, shape, offset, board), grown(quanta, shape, offset, board)
        content = grown(content, shape, offset, board) if np.ndim(content) else content
        found.append(body_reading(board, number, masks[number], begun, share, quanta, reach, content))
    return found


def separation(readings: list[dict[str, object]], centres: list[Node]) -> Fraction | None:
    """Two bodies' separation along the joining axis, the second centroid less the first, None where a region read no share."""
    axis = joining_axis(centres)
    found = []
    for reading in readings:
        share = reading["share"]
        assert isinstance(share, dict)
        centroid = share["centroid"]
        if centroid is None:
            return None
        value = centroid[axis]
        found.append(Fraction(int(value[0]), int(value[1])))
    return found[1] - found[0]


def rest(path: Path, intervals: int | None, reach: int) -> dict[str, Any]:
    """One world's reading: the bodies at the start and after `intervals` intervals (the world's intervals without it), each read about one interval, so the board steps once more than the window; the separation for two bodies; the books at the end with the two terms of their drift's identity summed over every step, the work term of L510 and Rule3's remainder term (`work_books`); labelled LATTICE."""
    board = Lattice(load_world(path))
    if len(board.world.bodies) not in (1, 2):
        raise ValueError(
            f"{path.name} declares {len(board.world.bodies)} bodies: the rest reads one or two"
        )
    steps = board.world.intervals if intervals is None else intervals
    centres = [centre_of(board, number) for number in range(len(board.world.bodies))]
    terms = {index: {"work_term": 0, "remainder_term": 0} for index in board.order}
    start = read_about_one_interval(board, centres, reach, terms)
    while board.interval < steps and board.ended is None:
        stepped(board, terms)
    end = read_about_one_interval(board, centres, reach, terms) if board.ended is None else None
    found: dict[str, Any] = {
        "label": LABEL,
        "input": path.name,
        "intervals": board.interval,
        "ended": board.ended,
        "amplitude_bound": board.world.amplitude_bound,
        "largest_integer": board.world.width,
        "arrays": board.kind.__name__,
        "joining_axis": AXES[joining_axis(centres)] if len(centres) == 2 else None,
        "start": start,
        "end": end,
        "books": board.books(),
        "work_term": work_books(board, terms),
    }
    if len(centres) == 2:
        apart = [separation(readings, centres) if readings else None for readings in (start, end)]
        change = None if apart[0] is None or apart[1] is None else apart[1] - apart[0]
        found["separation"] = {"start": pair(apart[0]), "end": pair(apart[1]), "change": pair(change)}
    return found


def field_series(
    lines: list[dict[str, object]], window: tuple[int, int]
) -> dict[tuple[str, str], dict[int, int]]:
    """The `field` lines of a run's output within the window, per (node_detector, family): the reading at each interval it was written (it is written where it differs from the last interval's)."""
    found: dict[tuple[str, str], dict[int, int]] = {}
    for line in lines:
        if line.get("event") != "density" or line.get("reading") is None:
            continue
        interval = int(str(line["interval"]))
        if window[0] <= interval <= window[1]:
            key = (str(line["node_detector"]), str(line["family"]))
            found.setdefault(key, {})[interval] = int(str(line["reading"]))
    return found


def swing(series: dict[int, int], window: tuple[int, int]) -> dict[str, object]:
    """A region's reading over the window: carried forward where it was not rewritten, its least and largest with the first interval of each, and the count of its local maxima (above the reading before, at or above the one after)."""
    filled, last = [], None
    for interval in range(window[0], window[1] + 1):
        last = series.get(interval, last)
        if last is not None:
            filled.append((interval, last))
    if not filled:
        return {"least": None, "largest": None, "maxima": 0}
    values = [value for _interval, value in filled]
    maxima = sum(
        1 for i in range(1, len(values) - 1) if values[i] > values[i - 1] and values[i] >= values[i + 1]
    )
    least, largest = min(values), max(values)
    return {
        "least": {"interval": next(t for t, v in filled if v == least), "reading": least},
        "largest": {"interval": next(t for t, v in filled if v == largest), "reading": largest},
        "maxima": maxima,
    }


def densities_read(output: Path, expected: dict[str, Any] | None) -> dict[str, Any]:
    """A run's `field` lines read over the window the expectation names (the whole run without one), for the regions and family it names under `field` (every region and family without them)."""
    document = json.loads(output.read_text(encoding="utf-8"))
    lines = [line for line in document.get("lines", []) if isinstance(line, dict)]
    named = (expected or {}).get("density", {})
    window = tuple(
        int(v) for v in (expected or {}).get("window", [0, int(document.get("intervals", 0))])
    )
    series = field_series(lines, (window[0], window[1]))
    wanted = [
        key
        for key in series
        if (not named.get("node_detectors") or key[0] in named["node_detectors"])
        and (not named.get("family") or key[1] == named["family"])
    ]
    return {
        "label": LABEL,
        "output": output.name,
        "verdict": document.get("verdict"),
        "window": list(window),
        "regions": [
            {
                "node_detector": node_detector,
                "family": family,
                **swing(series[(node_detector, family)], (window[0], window[1])),
            }
            for node_detector, family in sorted(wanted)
        ],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "worlds", type=Path, nargs="*", help="the world files, each with its mode file beside it"
    )
    parser.add_argument(
        "--intervals", type=int, default=None, help="the intervals read (the world's intervals)"
    )
    parser.add_argument(
        "--reach", type=int, default=6, help="the Links read along each axis from a centre"
    )
    parser.add_argument("--expectation", type=Path, default=None, help="the blind expectation file")
    parser.add_argument(
        "--output",
        type=Path,
        action="append",
        default=[],
        help="a run's output file, its field lines read (the flag once per file)",
    )
    args = parser.parse_args(argv)
    expected = (
        json.loads(args.expectation.read_text(encoding="utf-8"))
        if args.expectation is not None
        else None
    )
    found: dict[str, Any] = {"label": LABEL}
    if args.worlds:
        found["worlds"] = {path.stem: rest(path, args.intervals, args.reach) for path in args.worlds}
    if args.output:
        found["densities"] = {path.stem: densities_read(path, expected) for path in args.output}
    if expected is not None:
        found["blind"] = {key: expected.get(key) for key in ("reading", "blind", "fence", "status")}
    print(json.dumps(found, indent=1))


if __name__ == "__main__":
    main()

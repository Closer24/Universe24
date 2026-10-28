"""The swing rows of the great clock, read from the clock lines: gate 1, the recurring swing (the great clock tops with every clock turning at once, falls back to the setting's own first state and rises again), row 1b the tops and row 1c the exact returns (the Boss's 6416499848: the return is to the setting's first state, every clock's stretch and load as the first clock line holds them, and not to a constant of the calibre; the bottoms at the full rate, the resolution, named beside), with the rows' reading of the returns kept by name; moved whole out of great_clock.py at the Reader's mend of the return."""

from __future__ import annotations

from typing import Any

from event_universe.reckoner import FOUR_LISTED, LISTED, Chart, unread_words

FITTINGS = -1  # the fittings, the last part of a mark (the tick, the mean stretch, the fittings)


def marks(chart: Chart) -> tuple[list[tuple[int, int, int]], list[tuple[int, int]]]:
    """The rows' marks (tick, the mean stretch, the fittings so far) and the steps of the mean stretch between marks (the tick, the difference)."""
    rows = [(r["i"], int(r["volume mean"]), int(r["births"])) for r in chart.rows]
    return rows, [(b[0], b[1] - a[1]) for a, b in zip(rows, rows[1:], strict=False)]


def returns_of(chart: Chart) -> list[tuple[int, int, int]]:
    """The marks at which the mean stretch is back at or below the first mark's with a fitting after the first mark (the rows' reading, kept beside the clock lines')."""
    rows, _steps = marks(chart)
    return (
        [(i, v, b) for i, v, b in rows[1:] if v <= rows[0][1] and b > rows[0][FITTINGS]] if rows else []
    )


def stretches(chart: Chart) -> list[tuple[int, list[int], int]]:
    """The clock lines' stretches: per tick (the tick, every clock's stretch, the count of clocks turned over)."""
    return [(int(line["i"]), [int(x) for x in line["X"]], len(line["turned"])) for line in chart.clocks]


def bottoms_of(chart: Chart) -> list[tuple[int, int, bool]]:
    """The bottoms of the mean stretch in the clock lines (a local least, at or below the mark before and below the one after): the tick, the mean, and whether every clock stands at the full rate exactly, the resolution (named beside the exact returns, no longer the return's predicate: the Boss's 6416499848)."""
    lines = stretches(chart)
    means = [sum(xs) // len(xs) for _i, xs, _t in lines]
    return [
        (lines[k][0], means[k], all(x == chart.full_rate for x in lines[k][1]))
        for k in range(1, len(means) - 1)
        if means[k] <= means[k - 1] and means[k] < means[k + 1]
    ]


def tops_of(chart: Chart) -> list[int]:
    """The ticks at which every clock turned over at once, the great clock's tops, from the clock lines."""
    lines = stretches(chart)
    count = len(lines[0][1]) if lines else 0
    return [i for i, _xs, turned_over in lines if turned_over == count and count]


def state_of(line: dict[str, Any]) -> tuple[list[int], list[int]]:
    """A clock line's state, every clock's stretch and load as the line holds them."""
    return [int(x) for x in line["X"]], [int(c) for c in line["content"]]


def at_resolution(chart: Chart, line: dict[str, Any]) -> bool:
    """Whether a clock line stands at the resolution, every clock's stretch at the full rate: the great clock's stretches before the setting, whatever load stands on it."""
    return all(x == chart.full_rate for x in state_of(line)[0])


def exact_of(chart: Chart) -> list[int]:
    """The ticks of the exact returns (the Boss's 6416499848): the great clock back at the setting's own first pair of states, the great clock's stretches before the setting (every clock's stretch at the resolution, whatever load stands on it) or the set state itself (every clock's stretch and load as the first clock line holds them), and not at a mark of the rows; a run of such lines with no top of the whole great clock at or between them is one return (the great clock passes down through the setting's state to the resolution and up through it again), read at its last line at the resolution, else at its last line."""
    lines = chart.clocks
    if not lines:
        return []
    first, tops = state_of(lines[0]), tops_of(chart)
    groups: list[list[int]] = []
    for line in lines[1:]:
        i = int(line["i"])
        if state_of(line) != first and not at_resolution(chart, line):
            continue
        if groups and not any(groups[-1][-1] < t <= i for t in tops):
            groups[-1].append(i)
        else:
            groups.append([i])
    return [
        next((i for i in reversed(group) if at_resolution(chart, lines[i - 1])), group[-1])
        for group in groups
    ]


def recurring_swing(chart: Chart) -> dict[str, Any]:
    """Gate 1 (MA-S1's predicate, the Boss's 6400767119): the recurring swing from the clock lines: the great clock tops with every clock turning at once, falls to a bottom at the setting's first stretches at every clock exactly (the exact return, the Boss's 6416499848) and rises again; the swings numbered from the setting's, the fittings and the bob chimes counted between the returns."""
    lines, whole, bottoms = stretches(chart), tops_of(chart), bottoms_of(chart)
    exact = exact_of(chart)
    swings = [1] + exact
    between = [
        [
            sum(1 for b in chart.fittings if lo <= int(b["i"]) < hi),
            sum(1 for c in chart.chimes if lo <= int(c["i"]) < hi),
        ]
        for lo, hi in zip(swings, swings[1:] + [chart.ticks + 1], strict=False)
    ]
    verdict = (
        unread_words(
            "no Node line in the record",
            "the exact return to the seed's first state with the whole board turning at the top",
        )
        if not lines
        else f"SHOWN: {len(exact)} exact returns to the seed's first state, the whole board turning at once at {len(whole)} tops, {len(swings)} bangs"
        if exact and whole
        else f"NOT SHOWN: no return to the seed's first state, the bottom at {bottoms[0][1]} against the seed's mean volume {sum(lines[0][1]) // len(lines[0][1])} (Gamma {chart.full_rate})"
        + (", the whole board turning at once at the top" if whole else ", no whole-board turn")
        if bottoms
        else "NOT SHOWN: no bottom of the mean volume"
        + (", the whole board turning at once" if whole else "")
    )
    return {
        "1 recurring bangs": {
            "tops with every Node turning at once (interval)": whole[:LISTED],
            "exact returns to the seed's first state (interval)": exact[:LISTED],
            "bottoms (interval, mean X, at Gamma at every Node, the resolution)": bottoms[:LISTED],
            "bangs numbered (the interval each begins)": swings[:LISTED],
            "births and body credits between the bangs": between[:LISTED],
            "rows' reading: marks back at or below the first mark's with a birth after it": returns_of(
                chart
            )[:FOUR_LISTED],
            "verdict": verdict,
        }
    }


def tops(chart: Chart) -> dict[str, Any]:
    """Row 1b (the owner's word of 2026-10-26, 00:5x UTC: the top in the gate too): the great clock tops, every clock turning at once at one tick, read from the clock lines as gate 1 reads them; SHOWN from the first such top."""
    lines, whole = stretches(chart), tops_of(chart)
    return {
        "1b the board tops, every Node turning at once": {
            "tops (interval)": whole[:LISTED],
            "verdict": unread_words("no Node line in the record", "every Node turned at one interval")
            if not lines
            else f"SHOWN: the whole board turns at once at {len(whole)} tops, the first at {whole[0]}"
            if whole
            else "NOT SHOWN: no interval with every Node turned",
        }
    }


def returns(chart: Chart) -> dict[str, Any]:
    """Row 1c (the same word: the return in the gate too): the great clock returns to the setting, a bottom of the mean stretch with every clock's stretch at the setting's own first state exactly (the Boss's 6416499848), read from the clock lines as gate 1 reads them; SHOWN from the first such return."""
    exact = exact_of(chart)
    return {
        "1c the board returns to the seed": {
            "exact returns (interval)": exact[:LISTED],
            "verdict": unread_words(
                "no Node line in the record",
                "the board back at the seed's first pair of states, the resolution or the laid state",
            )
            if not chart.clocks
            else f"SHOWN: {len(exact)} exact returns to the seed's first state, the first at {exact[0]}"
            if exact
            else "NOT SHOWN: no return to the seed's first state",
        }
    }

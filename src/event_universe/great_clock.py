"""The great clock's gates, read from the chart's rows and clock lines alone (the reader's view), one function per row of UNIVERSE24's table: 1 the recurring swing (MA-S1: the exact return to the full rate at every clock with the whole great clock turning at once, the swings numbered), 3 shortening then lengthening, 5 the acceleration with LC-S1's lift line, 6 the contraction (the mean stretch's course), 4 the era of matter in the clocks' dials, 14 the horizon, 34 the horizon with the stopped clock, 37 Maxwell's one mesh per tick from the clock lines' leads, 45 the bobs' well and 46 the swings recurring with the same gates; the gates of the strikes are strikes.py and gates.py."""

from __future__ import annotations

from typing import Any

from event_universe.core import rates
from event_universe.core.rule3 import carries, largest_below
from event_universe.core.spokes import AXES
from event_universe.reckoner import (
    HALF,
    LISTED,
    MAX,
    QUARTERS,
    SHORT_LIST,
    THIRDS,
    Chart,
    unread_words,
)
from event_universe.swings import (  # noqa: F401  (the swing rows' readers, names kept for the hands' scripts)
    bottoms_of,
    exact_of,
    marks,
    recurring_swing,
    stretches,
    tops_of,
)

LOAD_PULL = (
    2  # the load pull's weight, 2 sqrt(X / Gamma) per clock (BG-S1's form), against the meshes' lift
)


def contraction(chart: Chart) -> dict[str, Any]:
    """Gate 6: the contraction, a fall of the mean stretch at some mark."""
    rows, steps = marks(chart)
    falls = [i for i, d in steps if d < 0]
    lines = stretches(chart)
    at = None
    if falls and len(lines) >= falls[0]:
        before, after = lines[falls[0] - 1 - 1][1], lines[falls[0] - 1][1]
        at = chart.clock(min(range(len(after)), key=lambda n: after[n] - before[n]))
    return {
        "6 contraction (the board, the reader's view)": {
            "at": at,
            "volume mean course (interval, mean)": [
                (i, v) for i, v, _b in rows[:: max(1, len(rows) // LISTED)]
            ],
            "intervals with the mean volume falling": falls[:SHORT_LIST],
            "turns (Node swaps) total": sum(len(line["turned"]) for line in chart.clocks),
            "verdict": "SHOWN at the board: the mean volume falls"
            if falls
            else "NOT SHOWN: the mean volume rises throughout",
        }
    }


def shortening(chart: Chart) -> dict[str, Any]:
    """Gate 3: shortening then lengthening, a falling run of the mean stretch between rising runs."""
    _rows, steps = marks(chart)
    falls = [i for i, d in steps if d < 0]
    after = [i for (i, d), (_j, e) in zip(steps, steps[1:], strict=False) if d < 0 and e > 0]
    return {
        "3 shortening then lengthening": {
            "falls followed by a rise (the fall's interval)": after[:SHORT_LIST],
            "verdict": "SHOWN at the board: a falling run between rising runs"
            if after
            else ("SHOWN in part: the course ends in a fall" if falls else "NOT SHOWN: no fall"),
        }
    }


def lift_of(chart: Chart) -> tuple[list[int], list[int]]:
    """LC-S1's lift per tick from the clock lines (lc1's carries form): L = SUM_i carries(Gamma SUM_j (X_j - X_i), 3 X_i) over the clocks and their six neighbours, and the load pull SUM_i 2 largest_below(X_i div Gamma); each clock line's read once per chart."""
    memo = chart.memo.setdefault("lift", {})
    lifts, pulls = [], []
    for line in chart.clocks:
        if id(line) not in memo:
            xs = [int(x) for x in line["X"]]
            lift = pull = 0
            for at, x in enumerate(xs):
                lift += int(
                    carries(chart.full_rate * sum(xs[n] - x for n in neighbours(chart, at)), AXES * x)
                )
                pull += LOAD_PULL * largest_below(int(carries(x, chart.full_rate)))
            memo[id(line)] = (lift, pull)
        lifts.append(memo[id(line)][0])
        pulls.append(memo[id(line)][1])
    return lifts, pulls


def acceleration(chart: Chart) -> dict[str, Any]:
    """Gate 5: the acceleration, the rises of the mean stretch growing from mark to mark within the last rising run; beside it LC-S1's lift line (the Boss's 6400767119): the meshes' lift L against the load pull over the run's last third, the lift SHOWN where L exceeds the pull."""
    _rows, steps = marks(chart)
    last_run = []
    for _i, d in reversed(steps):
        if d <= 0:
            break
        last_run.append(d)
    last_run.reverse()
    quickening = sum(1 for a, b in zip(last_run, last_run[1:], strict=False) if b > a)
    lifts, pulls = lift_of(chart)
    third = max(1, len(lifts) // THIRDS)
    lift, pull = sum(lifts[-third:]), sum(pulls[-third:])
    return {
        "5 acceleration (the lengthening quickens)": {
            "the last rising run's steps (per mark)": last_run[-SHORT_LIST:],
            "steps larger than the one before": [quickening, max(len(last_run) - 1, 0)],
            "the Links' lift L and the mass pull at the last interval (LC-S1)": [lifts[-1], pulls[-1]]
            if lifts
            else None,
            "L and the pull summed over the last third": [lift, pull],
            "verdict": (
                "SHOWN at the board: the rises grow from mark to mark"
                if len(last_run) > 1 and quickening * HALF > len(last_run) - 1
                else "NOT SHOWN: the rises do not grow"
                if len(last_run) > 1
                else "NOT READ: no rising run of two marks"
            )
            + (
                "; the lift SHOWN: L exceeds the mass pull over the last third"
                if lifts and lift > pull
                else "; the lift NOT SHOWN: L within the mass pull"
                if lifts
                else ""
            ),
        }
    }


def era(chart: Chart) -> dict[str, Any]:
    """Gate 4: the era of matter in the clocks' own dials: at every clock with a fitting and a bob's chime, the chimes go on past the last fitting in that clock's dial."""
    last_fitting: dict[tuple[int, ...], int] = {}
    last_chime: dict[tuple[int, ...], int] = {}
    for b in chart.fittings:
        last_fitting[tuple(b["node"])] = max(last_fitting.get(tuple(b["node"]), 0), b["proper"])
    for c in chart.chimes:
        last_chime[tuple(c["node"])] = max(last_chime.get(tuple(c["node"]), 0), c["proper"])
    both = [n for n in last_fitting if n in last_chime]
    past = [n for n in both if last_chime[n] > last_fitting[n]]
    verdict = (
        "SHOWN"
        if both and len(past) == len(both)
        else (f"SHOWN in part: {len(past)} of {len(both)}" if past else "NOT SHOWN")
    )
    return {
        "4 an era of matter": {
            "Nodes with a birth and a body credit": len(both),
            "of them with credits past the last birth in the Node's own clock": len(past),
            "births": len(chart.fittings),
            "body credits": len(chart.chimes),
            "at": list(past[0]) if past else None,
            "verdict": verdict,
        }
    }


def standstill(chart: Chart) -> dict[str, Any]:
    """Gate 14: the stopped load against the clock lines' max load (the Boss's 6416277638: the reader's rows stand one at every twelfth tick, so a standstill shorter than a twelfth of the run was blind to the rows' maximum while the stop is in the clock lines; the rows' maximum named beside); a chime at a clock while it stands in the stopped set of the clock lines would deny the horizon (the former read, a chime at or above the stopped load, named beside)."""
    stopped = rates.stopped_load(chart.full_rate)
    stopped_at = {(int(line["i"]), int(at)) for line in chart.clocks for at in line["frozen"]}
    at_stopped = [c for c in chart.chimes if (int(c["i"]), chart.index(c["node"])) in stopped_at]
    at_mark = sum(1 for c in chart.chimes if c["content"] >= stopped)
    rows_max = max((int(r["content min/mean/max"][MAX]) for r in chart.rows), default=0)
    load_max = max((int(x) for line in chart.clocks for x in line["content"]), default=rows_max)
    verdict = (
        "SHOWN as silence (no credit at a frozen Node)"
        if load_max >= stopped and not at_stopped
        else ("NOT REACHED" if load_max < stopped else "NOT SHOWN")
    )
    stopped_first = chart.first_stopped()
    first = chart.clock(min(stopped_first, key=stopped_first.__getitem__)) if stopped_first else None
    return {
        "14 the horizon": {
            "frozen content": stopped,
            "max content in the Node lines": load_max,
            "max content in the rows (one row at every twelfth interval)": rows_max,
            "Nodes frozen": len(stopped_first),
            "credits at a Node while it stands in the frozen set": len(at_stopped),
            "credits at or above the frozen content (the former read)": at_mark,
            "at": first,
            "verdict": verdict,
        }
    }


def stopped_clock(chart: Chart) -> dict[str, Any]:
    """Row 34: the horizon and the stopped clock from the clock lines: a stopped clock (the mesh rate 0) silent while it is stopped (no chime at it on any tick it stands in the stopped set) and its load standing at the load of its stop on every line of that stop, until its release (BH-S1's predicate, the Boss's 6407393577: the clock stops at the horizon; re-cut for a released standstill on the Boss's 6417313230: the former read every chime and every load from the first stop on, which no released clock can hold)."""
    first = chart.first_stopped()
    stopped: list[tuple[int, int]] = []
    held: dict[int, int] = {}
    standing = later = 0
    for line in chart.clocks:
        i, ats = int(line["i"]), {int(at) for at in line["frozen"]}
        for at in list(held):
            if at not in ats:
                del held[at]
        for at in sorted(ats):
            load = int(line["content"][at])
            if at in held:
                standing += load == held[at]
                later += 1
            else:
                held[at] = load
            stopped.append((i, at))
    stopped_at = set(stopped)
    chimed = {
        chart.index(c["node"])
        for c in chart.chimes
        if (int(c["i"]), chart.index(c["node"])) in stopped_at
    }
    silent = sum(1 for _i, at in stopped if at not in chimed)
    earliest = min(first.items(), key=lambda p: p[1])[0] if first else None
    return {
        "34 the horizon and the stopped clock": {
            "Nodes frozen": len(first),
            "frozen Node lines (interval, Node)": len(stopped),
            "of them silent (no credit at the Node while it is frozen)": silent,
            "lines standing at the content of their freeze / lines after a freeze's first": [
                standing,
                later,
            ],
            "at": chart.clock(earliest) if earliest is not None else None,
            "verdict": "SHOWN: every frozen Node silent with its content standing while frozen, the clock stopped at the horizon"
            if stopped and silent == len(stopped) and standing == later
            else "NOT SHOWN: a frozen Node credited while frozen or its content moving while frozen"
            if stopped
            else "NOT REACHED: no frozen Node in the record (as gate 14)",
        }
    }


def same_gates(chart: Chart) -> dict[str, Any]:
    """Row 46 (the Boss's 6400767119): the repeating swing with chimes: after the first exact return of gate 1 (every clock at the full rate), the later cycle fits hands and chimes bobs as the first did."""
    exact = exact_of(chart)
    if not exact:
        return {
            "46 the bangs recurring with the same gates": {
                "verdict": unread_words(
                    "no exact return of the board (gate 1)",
                    "a later bang shows the gates the first showed, its credits counted",
                )
            }
        }
    since = exact[0]
    fittings = sum(1 for b in chart.fittings if int(b["i"]) > since)
    chimes = sum(1 for c in chart.chimes if int(c["i"]) > since)
    return {
        "46 the bangs recurring with the same gates": {
            "the first exact return's interval": since,
            "births and body credits after it": [fittings, chimes],
            "verdict": "SHOWN: body credits in the later cycle"
            + (" with births" if fittings else ", no birth (a birth needs the twist)")
            if chimes
            else "NOT SHOWN: the later cycle credits no body",
        }
    }


def neighbours(chart: Chart, at: int) -> list[int]:
    """The six clocks one mesh from a clock's index on the torus."""
    x, y, z = chart.clock(at)
    cube = chart.cube
    return [
        chart.index(((x + dx) % cube, (y + dy) % cube, (z + dz) % cube))
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
    ]


def maxwell(chart: Chart) -> dict[str, Any]:
    """Row 37: Maxwell's one mesh per tick from the clock lines' unsprung leads: a clock whose lead turns on at a tick stood within one mesh of a clock with a lead the tick before; the violations counted."""
    lit = []
    for line in chart.clocks:
        on = {i for axis in line["current"] for i, c in enumerate(axis) if c}
        lit.append(on | {n for i in on for n in neighbours(chart, i)})
    violations = grown = 0
    for before, after in zip(lit, lit[1:], strict=False):
        new = after - before
        grown += bool(new)
        violations += sum(1 for n in new if not (set(neighbours(chart, n)) & before))
    return {
        "37 Maxwell's one Link per interval": {
            "Node lines": len(chart.clocks),
            "intervals the current's reach grew": grown,
            "Nodes lit beyond one Link of the interval before": violations,
            "verdict": unread_words("no Node line with a current", "the signal of one Link per interval")
            if not any(lit)
            else "SHOWN: the current's reach grows by one Link per interval"
            if violations == 0 and grown
            else "NOT SHOWN: a Node lit beyond one Link of the interval before"
            if violations
            else "NOT READ: the current's reach never grew",
        }
    }


def well(chart: Chart) -> dict[str, Any]:
    """Row 45: the bobs' well, binding and collapse: a bob (a gear at one clock) chimed from the first half of the run into its last quarter stands in its own well, every standing bob listed with its first and last chime (the page draws its ring from them, the Boss's audit of 2026-10-27, 12:2x UTC); a stopped clock ends a collapse."""
    spans = {bob: [int(c["i"]) for c in cs] for bob, cs in chart.bobs_of().items()}
    n = chart.ticks
    bobs = sorted(
        [*clock, gear, min(xs), max(xs)]
        for (clock, gear), xs in spans.items()
        if min(xs) * HALF <= n and max(xs) * QUARTERS >= (QUARTERS - 1) * n
    )
    standing = len(bobs)
    stopped = sum(len(line["frozen"]) for line in chart.clocks)
    return {
        "45 the bodies' well, binding and collapse": {
            "bodies (Node, line) credited": len(spans),
            "of them standing from the first half into the last quarter": standing,
            "the standing bodies (Node, line, first credit, last credit), every one": bobs,
            "frozen Node lines (a collapse's end)": stopped,
            "verdict": unread_words(
                "no credit",
                "a body of enough quanta stands in its own well, a collapse ends in a frozen clock",
            )
            if not spans
            else "SHOWN: a body stands in its own well through the run"
            if standing
            else "NOT SHOWN: no body stands at one Node through the run",
        }
    }

"""The board's gates, read from the record's rows and Node lines alone (the reader's view), one function per row of UNIVERSE24's table: 1 the recurring bang (MA-S1: the exact return to Gamma at every Node with the whole board turning at once, the bangs numbered), 3 shortening then lengthening, 5 the acceleration with LC-S1's lift line, 6 the contraction (the mean volume's course), 4 the era of matter in the Nodes' clocks, 14 the horizon, 34 the horizon with the stopped clock, 37 Maxwell's one Link per interval from the Node lines' currents, 45 the bodies' well and 46 the bangs recurring with the same gates; the gates of the clicks are clicks.py and gates.py."""

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
from event_universe.swings import (  # noqa: F401  (the bang rows' readers, the names kept for the hands' scripts)
    bottoms_of,
    exact_of,
    marks,
    recurring_swing,
    stretches,
    tops_of,
)

LOAD_PULL = (
    2  # the mass pull's weight, 2 sqrt(X / Gamma) per Node (BG-S1's form), against the Links' lift
)


def contraction(record: Chart) -> dict[str, Any]:
    """Gate 6: the contraction, a fall of the mean volume at some mark."""
    rows, steps = marks(record)
    falls = [i for i, d in steps if d < 0]
    lines = stretches(record)
    at = None
    if falls and len(lines) >= falls[0]:
        before, after = lines[falls[0] - 1 - 1][1], lines[falls[0] - 1][1]
        at = record.clock(min(range(len(after)), key=lambda n: after[n] - before[n]))
    return {
        "6 contraction (the board, the reader's view)": {
            "at": at,
            "volume mean course (interval, mean)": [
                (i, v) for i, v, _b in rows[:: max(1, len(rows) // LISTED)]
            ],
            "intervals with the mean volume falling": falls[:SHORT_LIST],
            "turns (Node swaps) total": sum(len(line["turned"]) for line in record.clocks),
            "verdict": "SHOWN at the board: the mean volume falls"
            if falls
            else "NOT SHOWN: the mean volume rises throughout",
        }
    }


def shortening(record: Chart) -> dict[str, Any]:
    """Gate 3: shortening then lengthening, a falling run of the mean volume between rising runs."""
    _rows, steps = marks(record)
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


def lift_of(record: Chart) -> tuple[list[int], list[int]]:
    """LC-S1's lift per interval from the Node lines (lc1's quotient form): L = SUM_i quotient(Gamma SUM_j (X_j - X_i), 3 X_i) over the Nodes and their six neighbours, and the mass pull SUM_i 2 largest_below(X_i div Gamma); each Node line's read once per record."""
    memo = record.memo.setdefault("lift", {})
    lifts, pulls = [], []
    for line in record.clocks:
        if id(line) not in memo:
            xs = [int(x) for x in line["X"]]
            lift = pull = 0
            for at, x in enumerate(xs):
                lift += int(
                    carries(record.full_rate * sum(xs[n] - x for n in neighbours(record, at)), AXES * x)
                )
                pull += LOAD_PULL * largest_below(int(carries(x, record.full_rate)))
            memo[id(line)] = (lift, pull)
        lifts.append(memo[id(line)][0])
        pulls.append(memo[id(line)][1])
    return lifts, pulls


def acceleration(record: Chart) -> dict[str, Any]:
    """Gate 5: the acceleration, the rises of the mean volume growing from mark to mark within the last rising run; beside it LC-S1's lift line (the Boss's 6400767119): the Links' lift L against the mass pull over the run's last third, the lift SHOWN where L exceeds the pull."""
    _rows, steps = marks(record)
    last_run = []
    for _i, d in reversed(steps):
        if d <= 0:
            break
        last_run.append(d)
    last_run.reverse()
    quickening = sum(1 for a, b in zip(last_run, last_run[1:], strict=False) if b > a)
    lifts, pulls = lift_of(record)
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


def era(record: Chart) -> dict[str, Any]:
    """Gate 4: the era of matter in the Nodes' own clocks: at every Node with a birth and a body's credit, the credits go on past the last birth in that Node's proper count."""
    last_birth: dict[tuple[int, ...], int] = {}
    last_credit: dict[tuple[int, ...], int] = {}
    for b in record.fittings:
        last_birth[tuple(b["node"])] = max(last_birth.get(tuple(b["node"]), 0), b["proper"])
    for c in record.chimes:
        last_credit[tuple(c["node"])] = max(last_credit.get(tuple(c["node"]), 0), c["proper"])
    both = [n for n in last_birth if n in last_credit]
    past = [n for n in both if last_credit[n] > last_birth[n]]
    verdict = (
        "SHOWN"
        if both and len(past) == len(both)
        else (f"SHOWN in part: {len(past)} of {len(both)}" if past else "NOT SHOWN")
    )
    return {
        "4 an era of matter": {
            "Nodes with a birth and a body credit": len(both),
            "of them with credits past the last birth in the Node's own clock": len(past),
            "births": len(record.fittings),
            "body credits": len(record.chimes),
            "at": list(past[0]) if past else None,
            "verdict": verdict,
        }
    }


def standstill(record: Chart) -> dict[str, Any]:
    """Gate 14: the frozen content against the Node lines' max content (the Boss's 6416277638: the reader's rows stand one at every twelfth interval, so a horizon shorter than a twelfth of the run was blind to the rows' maximum while the freeze is in the Node lines; the rows' maximum named beside); a credit at a Node while it stands in the frozen set of the Node lines would deny the horizon (the former read, a credit at or above the frozen content, named beside)."""
    frozen = rates.stopped_load(record.full_rate)
    frozen_at = {(int(line["i"]), int(at)) for line in record.clocks for at in line["frozen"]}
    at_frozen = [c for c in record.chimes if (int(c["i"]), record.index(c["node"])) in frozen_at]
    at_mark = sum(1 for c in record.chimes if c["content"] >= frozen)
    rows_max = max((int(r["content min/mean/max"][MAX]) for r in record.rows), default=0)
    cmax = max((int(x) for line in record.clocks for x in line["content"]), default=rows_max)
    verdict = (
        "SHOWN as silence (no credit at a frozen Node)"
        if cmax >= frozen and not at_frozen
        else ("NOT REACHED" if cmax < frozen else "NOT SHOWN")
    )
    frozen_first = record.first_stopped()
    first = record.clock(min(frozen_first, key=frozen_first.__getitem__)) if frozen_first else None
    return {
        "14 the horizon": {
            "frozen content": frozen,
            "max content in the Node lines": cmax,
            "max content in the rows (one row at every twelfth interval)": rows_max,
            "Nodes frozen": len(frozen_first),
            "credits at a Node while it stands in the frozen set": len(at_frozen),
            "credits at or above the frozen content (the former read)": at_mark,
            "at": first,
            "verdict": verdict,
        }
    }


def stopped_clock(record: Chart) -> dict[str, Any]:
    """Row 34: the horizon and the stopped clock from the Node lines: a frozen Node (the Link pace 0) silent while it is frozen (no credit at it on any interval it stands in the frozen set) and its content standing at the content of its freeze on every line of that freeze, until its release (BH-S1's predicate, the Boss's 6407393577: the clock stops at the horizon; re-cut for a released horizon on the Boss's 6417313230: the former read every credit and every content from the first freeze on, which no released Node can hold)."""
    first = record.first_stopped()
    frozen: list[tuple[int, int]] = []
    held: dict[int, int] = {}
    standing = later = 0
    for line in record.clocks:
        i, ats = int(line["i"]), {int(at) for at in line["frozen"]}
        for at in list(held):
            if at not in ats:
                del held[at]
        for at in sorted(ats):
            content = int(line["content"][at])
            if at in held:
                standing += content == held[at]
                later += 1
            else:
                held[at] = content
            frozen.append((i, at))
    frozen_at = set(frozen)
    credited = {
        record.index(c["node"])
        for c in record.chimes
        if (int(c["i"]), record.index(c["node"])) in frozen_at
    }
    silent = sum(1 for _i, at in frozen if at not in credited)
    earliest = min(first.items(), key=lambda p: p[1])[0] if first else None
    return {
        "34 the horizon and the stopped clock": {
            "Nodes frozen": len(first),
            "frozen Node lines (interval, Node)": len(frozen),
            "of them silent (no credit at the Node while it is frozen)": silent,
            "lines standing at the content of their freeze / lines after a freeze's first": [
                standing,
                later,
            ],
            "at": record.clock(earliest) if earliest is not None else None,
            "verdict": "SHOWN: every frozen Node silent with its content standing while frozen, the clock stopped at the horizon"
            if frozen and silent == len(frozen) and standing == later
            else "NOT SHOWN: a frozen Node credited while frozen or its content moving while frozen"
            if frozen
            else "NOT REACHED: no frozen Node in the record (as gate 14)",
        }
    }


def same_gates(record: Chart) -> dict[str, Any]:
    """Row 46 (the Boss's 6400767119): the repeating bang with credits: after the first exact return of gate 1 (every Node at Gamma), the later cycle births and credits bodies as the first did."""
    exact = exact_of(record)
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
    births = sum(1 for b in record.fittings if int(b["i"]) > since)
    credits = sum(1 for c in record.chimes if int(c["i"]) > since)
    return {
        "46 the bangs recurring with the same gates": {
            "the first exact return's interval": since,
            "births and body credits after it": [births, credits],
            "verdict": "SHOWN: body credits in the later cycle"
            + (" with births" if births else ", no birth (a birth needs the twist)")
            if credits
            else "NOT SHOWN: the later cycle credits no body",
        }
    }


def neighbours(record: Chart, at: int) -> list[int]:
    """The six Nodes one Link from a Node's index on the torus."""
    x, y, z = record.clock(at)
    cube = record.cube
    return [
        record.index(((x + dx) % cube, (y + dy) % cube, (z + dz) % cube))
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
    ]


def maxwell(record: Chart) -> dict[str, Any]:
    """Row 37: Maxwell's one Link per interval from the Node lines' gap-0 currents: a Node whose current turns on at an interval stood within one Link of a Node with a current the interval before; the violations counted."""
    lit = []
    for line in record.clocks:
        on = {i for axis in line["current"] for i, c in enumerate(axis) if c}
        lit.append(on | {n for i in on for n in neighbours(record, i)})
    violations = grown = 0
    for before, after in zip(lit, lit[1:], strict=False):
        new = after - before
        grown += bool(new)
        violations += sum(1 for n in new if not (set(neighbours(record, n)) & before))
    return {
        "37 Maxwell's one Link per interval": {
            "Node lines": len(record.clocks),
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


def well(record: Chart) -> dict[str, Any]:
    """Row 45: the bodies' well, binding and collapse: a body (a line at one Node) credited from the first half of the run into its last quarter stands in its own well, every standing body listed with its first and last credit (the page draws its ring from them, the Boss's audit of 2026-10-27, 12:2x UTC); a frozen Node ends a collapse."""
    spans = {body: [int(c["i"]) for c in cs] for body, cs in record.bobs_of().items()}
    n = record.ticks
    bodies = sorted(
        [*node, line, min(xs), max(xs)]
        for (node, line), xs in spans.items()
        if min(xs) * HALF <= n and max(xs) * QUARTERS >= (QUARTERS - 1) * n
    )
    standing = len(bodies)
    frozen = sum(len(line["frozen"]) for line in record.clocks)
    return {
        "45 the bodies' well, binding and collapse": {
            "bodies (Node, line) credited": len(spans),
            "of them standing from the first half into the last quarter": standing,
            "the standing bodies (Node, line, first credit, last credit), every one": bodies,
            "frozen Node lines (a collapse's end)": frozen,
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

"""The board's gates, read from the record's rows and Node lines alone (the reader's view), one function per row of UNIVERSE24's table: 1 the recurring bang (MA-S1: the exact return to Gamma at every Node with the whole board turning at once, the bangs numbered), 3 shortening then lengthening, 5 the acceleration with LC-S1's lift line, 6 the contraction (the mean volume's course), 4 the era of matter in the Nodes' clocks, 14 the horizon, 34 the horizon with the stopped clock, 37 Maxwell's one Link per interval from the Node lines' currents, 45 the bodies' well and 46 the bangs recurring with the same gates; the gates of the clicks are clicks.py and gates.py."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from event_universe.core import paces
from event_universe.core.rule3 import largest_below, quotient
from event_universe.decoder import Record


def marks(record: Record) -> tuple[list[tuple[int, int, int]], list[tuple[int, int]]]:
    """The rows' marks (interval, the mean volume, the births so far) and the steps of the mean volume between marks (the interval, the difference)."""
    rows = [(r["i"], int(r["volume mean"]), int(r["births"])) for r in record.rows]
    return rows, [(b[0], b[1] - a[1]) for a, b in zip(rows, rows[1:], strict=False)]


def contraction(record: Record) -> dict[str, Any]:
    """Gate 6: the contraction, a fall of the mean volume at some mark."""
    rows, steps = marks(record)
    falls = [i for i, d in steps if d < 0]
    lines = volumes(record)
    at = None
    if falls and len(lines) >= falls[0]:
        before, after = lines[falls[0] - 2][1], lines[falls[0] - 1][1]
        cube = int(record.run["cube"])
        k = min(range(len(after)), key=lambda n: after[n] - before[n])
        at = [k // (cube * cube), (k // cube) % cube, k % cube]
    return {
        "6 contraction (the board, the reader's view)": {
            "at": at,
            "volume mean course (interval, mean)": [
                (i, v) for i, v, _b in rows[:: max(1, len(rows) // 8)]
            ],
            "intervals with the mean volume falling": falls[:6],
            "turns (Node swaps) total": sum(len(line["turned"]) for line in record.nodes),
            "verdict": "SHOWN at the board: the mean volume falls"
            if falls
            else "NOT SHOWN: the mean volume rises throughout",
        }
    }


def shortening(record: Record) -> dict[str, Any]:
    """Gate 3: shortening then lengthening, a falling run of the mean volume between rising runs."""
    _rows, steps = marks(record)
    falls = [i for i, d in steps if d < 0]
    after = [i for (i, d), (_j, e) in zip(steps, steps[1:], strict=False) if d < 0 and e > 0]
    return {
        "3 shortening then lengthening": {
            "falls followed by a rise (the fall's interval)": after[:6],
            "verdict": "SHOWN at the board: a falling run between rising runs"
            if after
            else ("SHOWN in part: the course ends in a fall" if falls else "NOT SHOWN: no fall"),
        }
    }


def returns_of(record: Record) -> list[tuple[int, int, int]]:
    """The marks at which the mean volume is back at or below the first mark's with a birth after the first mark (the rows' reading, kept beside the Node lines')."""
    rows, _steps = marks(record)
    return [(i, v, b) for i, v, b in rows[1:] if v <= rows[0][1] and b > rows[0][2]] if rows else []


def volumes(record: Record) -> list[tuple[int, list[int], int]]:
    """The Node lines' volumes: per interval (the interval, every Node's X, the count of Nodes turned)."""
    return [(int(line["i"]), [int(x) for x in line["X"]], len(line["turned"])) for line in record.nodes]


def bottoms_of(record: Record) -> list[tuple[int, int, bool]]:
    """The bottoms of the mean volume in the Node lines (a local least, at or below the mark before and below the one after): the interval, the mean, and whether every Node stands at Gamma exactly."""
    lines = volumes(record)
    means = [sum(xs) // len(xs) for _i, xs, _t in lines]
    return [
        (lines[k][0], means[k], all(x == record.gamma for x in lines[k][1]))
        for k in range(1, len(means) - 1)
        if means[k] <= means[k - 1] and means[k] < means[k + 1]
    ]


def recurring_bang(record: Record) -> dict[str, Any]:
    """Gate 1 (MA-S1's predicate, the Boss's 6400767119): the recurring bang from the Node lines: the board tops with every Node turning at once, falls to a bottom at Gamma at every Node exactly (the exact return) and rises again; the bangs numbered from the seed's, the births and the body credits counted between the returns."""
    lines = volumes(record)
    count = len(lines[0][1]) if lines else 0
    whole = [i for i, _xs, turned in lines if turned == count and count]
    bottoms = bottoms_of(record)
    exact = [i for i, _m, at_gamma in bottoms if at_gamma]
    bangs = [1] + [i + 1 for i in exact]
    between = [
        [
            sum(1 for b in record.births if lo <= int(b["i"]) < hi),
            sum(1 for c in record.credits if lo <= int(c["i"]) < hi),
        ]
        for lo, hi in zip(bangs, bangs[1:] + [record.intervals + 1], strict=False)
    ]
    verdict = (
        "NOT READ: no Node line in the record; the predicate: the exact return to Gamma at every Node with the whole board turning at the top"
        if not lines
        else f"SHOWN: {len(exact)} exact returns to Gamma at every Node, the whole board turning at once at {len(whole)} tops, {len(bangs)} bangs"
        if exact and whole
        else f"NOT SHOWN: the bottom at {bottoms[0][1]} against Gamma {record.gamma}"
        + (", the whole board turning at once at the top" if whole else ", no whole-board turn")
        if bottoms
        else "NOT SHOWN: no bottom of the mean volume"
        + (", the whole board turning at once" if whole else "")
    )
    return {
        "1 recurring bangs": {
            "tops with every Node turning at once (interval)": whole[:8],
            "bottoms (interval, mean X, at Gamma at every Node)": bottoms[:8],
            "bangs numbered (the interval each begins)": bangs[:8],
            "births and body credits between the bangs": between[:8],
            "rows' reading: marks back at or below the first mark's with a birth after it": returns_of(
                record
            )[:4],
            "verdict": verdict,
        }
    }


def lift_of(record: Record) -> tuple[list[int], list[int]]:
    """LC-S1's lift per interval from the Node lines (lc1's quotient form): L = SUM_i quotient(Gamma SUM_j (X_j - X_i), 3 X_i) over the Nodes and their six neighbours, and the mass pull SUM_i 2 largest_below(X_i div Gamma); each Node line's read once per record."""
    cube = int(record.run["cube"])
    memo = record.memo.setdefault("lift", {})
    lifts, pulls = [], []
    for line in record.nodes:
        if id(line) not in memo:
            xs = [int(x) for x in line["X"]]
            lift = pull = 0
            for at, x in enumerate(xs):
                lift += int(quotient(record.gamma * sum(xs[n] - x for n in neighbours(at, cube)), 3 * x))
                pull += 2 * largest_below(int(quotient(x, record.gamma)))
            memo[id(line)] = (lift, pull)
        lifts.append(memo[id(line)][0])
        pulls.append(memo[id(line)][1])
    return lifts, pulls


def acceleration(record: Record) -> dict[str, Any]:
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
    third = max(1, len(lifts) // 3)
    lift, pull = sum(lifts[-third:]), sum(pulls[-third:])
    return {
        "5 acceleration (the lengthening quickens)": {
            "the last rising run's steps (per mark)": last_run[-6:],
            "steps larger than the one before": [quickening, max(len(last_run) - 1, 0)],
            "the Links' lift L and the mass pull at the last interval (LC-S1)": [lifts[-1], pulls[-1]]
            if lifts
            else None,
            "L and the pull summed over the last third": [lift, pull],
            "verdict": (
                "SHOWN at the board: the rises grow from mark to mark"
                if len(last_run) > 1 and quickening * 2 > len(last_run) - 1
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


def era(record: Record) -> dict[str, Any]:
    """Gate 4: the era of matter in the Nodes' own clocks: at every Node with a birth and a body's credit, the credits go on past the last birth in that Node's proper count."""
    last_birth: dict[tuple[int, ...], int] = {}
    last_credit: dict[tuple[int, ...], int] = {}
    for b in record.births:
        last_birth[tuple(b["node"])] = max(last_birth.get(tuple(b["node"]), 0), b["proper"])
    for c in record.credits:
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
            "births": len(record.births),
            "body credits": len(record.credits),
            "at": list(past[0]) if past else None,
            "verdict": verdict,
        }
    }


def horizon(record: Record) -> dict[str, Any]:
    """Gate 14: the frozen content against the rows' max content; a credit at a frozen Node would deny the horizon."""
    frozen = paces.frozen_content(record.gamma)
    at_frozen = [c for c in record.credits if c["content"] >= frozen]
    cmax = max((int(r["content min/mean/max"][2]) for r in record.rows), default=0)
    verdict = (
        "SHOWN as silence (no credit at a frozen Node)"
        if cmax >= frozen and not at_frozen
        else ("NOT REACHED" if cmax < frozen else "NOT SHOWN")
    )
    return {
        "14 the horizon": {
            "frozen content": frozen,
            "max content in the rows": cmax,
            "credits at frozen Nodes": len(at_frozen),
            "verdict": verdict,
        }
    }


def stopped_clock(record: Record) -> dict[str, Any]:
    """Row 34: the horizon and the stopped clock from the Node lines: a frozen Node (the Link pace 0) silent (no credit at it) and its content standing from the interval it froze."""
    frozen = [(line["i"], at) for line in record.nodes for at in line["frozen"]]
    credited = {tuple(c["node"]) for c in record.credits}
    cube = int(record.run["cube"])
    silent = sum(
        1 for _i, at in frozen if (at // (cube * cube), (at // cube) % cube, at % cube) not in credited
    )
    standing = 0
    for (i, at), (j, bt) in zip(frozen, frozen[1:], strict=False):
        if at == bt and j == i + 1:
            standing += record.nodes[j - 1]["content"][at] == record.nodes[i - 1]["content"][at]
    return {
        "34 the horizon and the stopped clock": {
            "frozen Node lines (interval, Node)": len(frozen),
            "of them silent": silent,
            "frozen Node lines with the content standing from the one before": standing,
            "verdict": "SHOWN: a frozen Node silent with its content standing"
            if frozen and silent == len(frozen) and standing
            else "NOT SHOWN: a frozen Node credited or its content moving"
            if frozen
            else "NOT REACHED: no frozen Node in the record (as gate 14)",
        }
    }


def same_gates(record: Record) -> dict[str, Any]:
    """Row 46 (the Boss's 6400767119): the repeating bang with credits: after the first exact return of gate 1 (every Node at Gamma), the later cycle births and credits bodies as the first did."""
    exact = [i for i, _m, at_gamma in bottoms_of(record) if at_gamma]
    if not exact:
        return {
            "46 the bangs recurring with the same gates": {
                "verdict": "NOT READ: no exact return of the board (gate 1); the predicate: a later bang shows the gates the first showed, its credits counted"
            }
        }
    since = exact[0]
    births = sum(1 for b in record.births if int(b["i"]) > since)
    credits = sum(1 for c in record.credits if int(c["i"]) > since)
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


def neighbours(at: int, cube: int) -> list[int]:
    """The six Nodes one Link from a Node's index on the torus."""
    x, y, z = at // (cube * cube), (at // cube) % cube, at % cube
    found = []
    for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
        found.append(((x + dx) % cube) * cube * cube + ((y + dy) % cube) * cube + (z + dz) % cube)
    return found


def maxwell(record: Record) -> dict[str, Any]:
    """Row 37: Maxwell's one Link per interval from the Node lines' gap-0 currents: a Node whose current turns on at an interval stood within one Link of a Node with a current the interval before; the violations counted."""
    cube = int(record.run["cube"])
    lit = []
    for line in record.nodes:
        on = {i for axis in line["current"] for i, c in enumerate(axis) if c}
        lit.append(on | {n for i in on for n in neighbours(i, cube)})
    violations = grown = 0
    for before, after in zip(lit, lit[1:], strict=False):
        new = after - before
        grown += bool(new)
        violations += sum(1 for n in new if not (set(neighbours(n, cube)) & before))
    return {
        "37 Maxwell's one Link per interval": {
            "Node lines": len(record.nodes),
            "intervals the current's reach grew": grown,
            "Nodes lit beyond one Link of the interval before": violations,
            "verdict": "NOT READ: no Node line with a current; the predicate: the signal of one Link per interval"
            if not any(lit)
            else "SHOWN: the current's reach grows by one Link per interval"
            if violations == 0 and grown
            else "NOT SHOWN: a Node lit beyond one Link of the interval before"
            if violations
            else "NOT READ: the current's reach never grew",
        }
    }


def well(record: Record) -> dict[str, Any]:
    """Row 45: the bodies' well, binding and collapse: a body (a line at one Node) credited from the first half of the run into its last quarter stands in its own well; a frozen Node ends a collapse."""
    spans: dict[tuple[tuple[int, ...], int], list[int]] = defaultdict(list)
    for c in record.credits:
        spans[(tuple(c["node"]), c["line"])].append(int(c["i"]))
    n = record.intervals
    standing = sum(1 for xs in spans.values() if min(xs) * 2 <= n and max(xs) * 4 >= 3 * n)
    frozen = sum(len(line["frozen"]) for line in record.nodes)
    return {
        "45 the bodies' well, binding and collapse": {
            "bodies (Node, line) credited": len(spans),
            "of them standing from the first half into the last quarter": standing,
            "frozen Node lines (a collapse's end)": frozen,
            "verdict": "NOT READ: no credit; the predicate: a body of enough quanta stands in its own well, a collapse ends in a frozen clock"
            if not spans
            else "SHOWN: a body stands in its own well through the run"
            if standing
            else "NOT SHOWN: no body stands at one Node through the run",
        }
    }

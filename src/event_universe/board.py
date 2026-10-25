"""The board's gates, read from the record's rows alone (the reader's view): 1 the recurring bang, 3 shortening then lengthening, 5 the acceleration, 6 the contraction (`course`, each its own line and verdict), 4 the era of matter in the Nodes' clocks (`era`) and 14 the horizon (`horizon`); the gates of the clicks are gates.py."""

from __future__ import annotations

from typing import Any

from event_universe.core import paces
from event_universe.decoder import Record


def course(record: Record) -> dict[str, Any]:
    """Gates 1, 3, 5 and 6, each its own line and verdict (the Boss's 6399612901), the board's course from the rows (the reader's view): 6 the contraction, a fall of the mean volume at some mark; 3 shortening then lengthening, a falling run between rising runs; 1 the recurring bang, the mean volume back at or below its first mark's with a birth after the return; 5 the acceleration, the rises growing from mark to mark within the last rising run."""
    rows = [(r["i"], int(r["volume mean"]), int(r["births"])) for r in record.rows]
    steps = [(b[0], b[1] - a[1]) for a, b in zip(rows, rows[1:], strict=False)]
    falls = [i for i, d in steps if d < 0]
    rises_after_fall = [i for (i, d), (_j, e) in zip(steps, steps[1:], strict=False) if d < 0 and e > 0]
    returns = [(i, v, b) for i, v, b in rows[1:] if v <= rows[0][1] and b > rows[0][2]]
    last_run = []
    for _i, d in reversed(steps):
        if d <= 0:
            break
        last_run.append(d)
    last_run.reverse()
    quickening = sum(1 for a, b in zip(last_run, last_run[1:], strict=False) if b > a)
    out = {
        "6 contraction (the board, the reader's view)": {
            "volume mean course (interval, mean)": [
                (i, v) for i, v, _b in rows[:: max(1, len(rows) // 8)]
            ],
            "intervals with the mean volume falling": falls[:6],
            "turns (Node swaps) total": int(record.run["counts"]["turns"]),
            "verdict": "SHOWN at the board: the mean volume falls"
            if falls
            else "NOT SHOWN: the mean volume rises throughout",
        },
        "3 shortening then lengthening": {
            "falls followed by a rise (the fall's interval)": rises_after_fall[:6],
            "verdict": "SHOWN at the board: a falling run between rising runs"
            if rises_after_fall
            else ("SHOWN in part: the course ends in a fall" if falls else "NOT SHOWN: no fall"),
        },
        "1 recurring bangs": {
            "marks with the mean volume back at or below the first mark's and a birth after it": returns[
                :4
            ],
            "verdict": "SHOWN: the mean volume returns and births follow"
            if returns
            else "NOT SHOWN: no return of the mean volume to the first mark's with births after it",
        },
        "5 acceleration (the lengthening quickens)": {
            "the last rising run's steps (per mark)": last_run[-6:],
            "steps larger than the one before": [quickening, max(len(last_run) - 1, 0)],
            "verdict": "SHOWN at the board: the rises grow from mark to mark"
            if len(last_run) > 1 and quickening * 2 > len(last_run) - 1
            else "NOT SHOWN: the rises do not grow"
            if len(last_run) > 1
            else "NOT READ: no rising run of two marks",
        },
    }
    return out


def era(record: Record) -> dict[str, Any]:
    """Gate 4: the era of matter in the Nodes' own clocks: at every Node with a birth and a body's credit, the credits go on past the last birth in that Node's proper count."""
    last_birth: dict[tuple[int, ...], int] = {}
    last_credit: dict[tuple[int, ...], int] = {}
    for b in record.births:
        last_birth[tuple(b["node"])] = max(last_birth.get(tuple(b["node"]), 0), b["proper"])
    for c in record.credits:
        last_credit[tuple(c["node"])] = max(last_credit.get(tuple(c["node"]), 0), c["proper"])
    both = [n for n in last_birth if n in last_credit]
    past = sum(1 for n in both if last_credit[n] > last_birth[n])
    verdict = (
        "SHOWN"
        if both and past == len(both)
        else (f"SHOWN in part: {past} of {len(both)}" if past else "NOT SHOWN")
    )
    return {
        "4 an era of matter": {
            "Nodes with a birth and a body credit": len(both),
            "of them with credits past the last birth in the Node's own clock": past,
            "births": len(record.births),
            "body credits": len(record.credits),
            "verdict": verdict,
        }
    }


def horizon(record: Record) -> dict[str, Any]:
    """Gate 14: the frozen content against the rows' max content; a credit at a frozen Node would deny the horizon."""
    frozen = paces.frozen_content(record.gamma)
    at_frozen = [c for c in record.credits if c["content"] >= frozen]
    cmax = max(int(r["content min/mean/max"][2]) for r in record.rows)
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

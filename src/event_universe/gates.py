"""Every gate of UNIVERSE24 read from the record alone, a verdict with its numbers (the decoder's reads in decoder.py): the course of the board, the era of matter, the horizon's silence, the bodies' tracks, the arrow of time on the run back, the conservations in the clicks, the three constants, the entropy of the clicks. Usage: `python -m event_universe.gates <record.json>`."""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from typing import Any

from event_universe.core import paces
from event_universe.decoder import (
    FEW,
    HUNDRED,
    SPANS,
    THOUSAND,
    WIDTH,
    Rational,
    Record,
    charge_and_take,
    cmp_rat,
    quot,
    species,
)


def halves(pairs: list[tuple[int, Any]]) -> tuple[list[Any], list[Any]]:
    """The values split at the middle key, shallow and deep."""
    med = sorted(p[0] for p in pairs)[len(pairs) // 2]
    return [p[1] for p in pairs if p[0] <= med], [p[1] for p in pairs if p[0] > med]


def dilation(decoded: list[tuple[dict[str, Any], str, Rational]]) -> dict[str, Any]:
    """Gate 10: a body's proper count against the intervals it stood, deep against shallow (the reader's view)."""
    if len(decoded) <= FEW:
        return {}
    lo, hi = halves([(c["content"], (c["proper"], c["i"])) for c, _n, _x in decoded])
    rate_lo = (sum(p for p, _i in lo), sum(i for _p, i in lo))
    rate_hi = (sum(p for p, _i in hi), sum(i for _p, i in hi))
    shown = (
        "SHOWN in the reader's view"
        if cmp_rat(rate_hi, rate_lo) < 0
        else "NOT SHOWN in the reader's view"
    )
    return {
        "10 gravitational time dilation": {
            "reader's view: proper per thousand intervals, shallow / deep": [
                quot(*rate_lo, THOUSAND),
                quot(*rate_hi, THOUSAND),
            ],
            "verdict": shown
            + "; NOT READ in the one-place view: two bodies' clocks compare only through the gap-0 plane between them (gate 7)",
        }
    }


def lengthening(record: Record) -> dict[str, Any]:
    """Gate 2: the spacing of a body's credits longer where the content is deeper (the reader's view)."""
    by_node: dict[tuple[int, ...], list[dict[str, Any]]] = defaultdict(list)
    for c in record.credits:
        by_node[tuple(c["node"])].append(c)
    spans = []
    for cs in by_node.values():
        cs.sort(key=lambda c: int(c["i"]))
        spans += [
            ((a["content"] + b["content"]) // 2, b["i"] - a["i"])
            for a, b in zip(cs, cs[1:], strict=False)
            if b["i"] > a["i"]
        ]
    if len(spans) <= SPANS:
        return {}
    lo, hi = halves(spans)
    shallow, deep = quot(sum(lo), len(lo), HUNDRED), quot(sum(hi), len(hi), HUNDRED)
    shown = (
        "SHOWN in the reader's view"
        if deep is not None and shallow is not None and deep > shallow
        else "NOT SHOWN in the reader's view"
    )
    return {
        "2 the Links lengthening in the clicks": {
            "reader's view: spans": len(spans),
            "spacing in hundredths of a board interval, shallow / deep": [shallow, deep],
            "verdict": shown
            + "; NOT READ in the one-place view (the gap-0 plane between two bodies, gate 7)",
        }
    }


def course(record: Record) -> dict[str, Any]:
    """Gates 1, 3, 5, 6: the board's course from the rows (the reader's view): the mean volume's rises and falls, the turns."""
    rows = [(r["i"], int(r["volume mean"]), r["births"]) for r in record.rows]
    falls = [b[0] for a, b in zip(rows, rows[1:], strict=False) if b[1] - a[1] < 0]
    return {
        "1 recurring bangs / 3 shortening then lengthening / 6 contraction (board, the reader's view)": {
            "volume mean course (interval, mean)": [
                (i, v) for i, v, _b in rows[:: max(1, len(rows) // 8)]
            ],
            "intervals with the mean volume falling": falls[:6],
            "turns (Node swaps) total": int(record.run["counts"]["turns"]),
            "verdict": "contraction SHOWN at the board"
            if falls
            else "NOT SHOWN: the mean volume rises throughout; the turns are local",
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


def tracks(record: Record, decoded: list[tuple[dict[str, Any], str, Rational]]) -> dict[str, Any]:
    """Gates 9 and 13: a body's track (its record's credits by line); a move is a credit of the same line at a new Node after the first; two bodies' tracks approaching to adjacent Nodes a collision."""
    found: dict[tuple[tuple[int, ...], str], int] = Counter()
    for c, n, _x in decoded:
        found[(tuple(c["node"]), n)] += 1
    by_line: dict[int, list[tuple[int, tuple[int, ...]]]] = defaultdict(list)
    for c in record.credits:
        by_line[c["line"]].append((c["proper"], tuple(c["node"])))
    moves = 0
    for cs in by_line.values():
        cs.sort()
        seen = {cs[0][1]}
        for _p, at in cs[1:]:
            if at not in seen:
                moves += 1
                seen.add(at)
    if moves == 0:
        verdict = "NOT SHOWN: no line is credited at a second Node (the bodies stand)"
    else:
        verdict = f"read: {moves} lines credited at a new Node; the predicate (the tail falls, adjacent peaks collide) is the owner's sentence W-S4/W-S5"
    return {
        "9 collisions / 13 free fall": {
            "tracks (node, species)": len(found),
            "longest track credits": max(found.values(), default=0),
            "lines credited at a new Node after their first": moves,
            "verdict": verdict,
        }
    }


def light_and_arrow(record: Record) -> dict[str, Any]:
    """Gates 7, 11, 12 and 18: the gap-0 plane's credits (none in the engine's record: a detector is the toy's reading, kept by name in tools/derivations/toys/lean) and the run back on the record, exact bit for bit or not."""
    light = sum(1 for entry in record.log if entry["event"] == "detector")
    takes = [entry for entry in record.log if entry["event"] in ("birth", "credit")]
    absorbed = sum(int(entry["levels"]) for entry in takes)
    rb = record.run.get("run_back")
    if not rb:
        verdict = "NOT READ: the record carries no run back (the writer with back N)"
    elif rb["exact"] == rb["intervals"]:
        verdict = f"SHOWN: the run back exact bit for bit, {rb['exact']} of {rb['intervals']} intervals"
    else:
        verdict = f"NOT SHOWN: {rb['exact']} of {rb['intervals']}"
    return {
        "7 light with its redshift / 11 / 12": {
            "gap-0 credits in the record": light,
            "absorbed: the takes of the gap-0 line at births and credits (PC-S2)": len(takes),
            "levels taken in all": absorbed,
            "verdict": "read: the gap-0 line's quanta absorbed at the takes, its credit the taker's line (PC-S2); the redshift needs light with a period"
            if takes
            else "NOT READ: no take in the record",
        },
        "18 the arrow of time": {"run back on the record": rb, "verdict": verdict},
    }


def momentum(record: Record) -> Any:
    """The momentum the close wrote (the credit lines' dP_a): the takes' and the lays' sums per axis and the births where the recoil passed to the laid pair."""
    takes = [c["dP_take"] for c in record.credits + record.births if c.get("dP_take")]
    lays = [b["dP_lay"] for b in record.births if b.get("dP_lay")]
    if not takes:
        return "NOT READ: no click booked its momentum"
    passed = sum(
        1
        for b in record.births
        if b.get("dP_lay") and all(b["dP_take"][a] + b["dP_lay"][a] == 0 for a in range(3))
    )
    return {
        "clicks booking dP": len(takes),
        "takes dP_a summed": [sum(t[a] for t in takes) for a in range(3)],
        "lays dP_a summed": [sum(lay[a] for lay in lays) for a in range(3)],
        "recoil passed to the laid pair (take + lay = 0 per birth)": passed,
        "of births": len(lays),
    }


def constants(record: Record) -> dict[str, Any]:
    """The three constants: the count of integers per Node constant, every integer of the state and every transient within the width."""
    rows = record.rows
    counts_seen = sorted({r["integers"] for r in rows})
    state_bits, transient_bits = (
        max(r["max bits"] for r in rows),
        max(r["max transient bits"] for r in rows),
    )
    lacks = ("the count changes; " if len(counts_seen) != 1 else "") + (
        "the state past the width; " if state_bits > WIDTH else ""
    )
    lacks += "a transient past the width" if transient_bits > WIDTH else ""
    return {
        "the three constants": {
            "integers per Node": counts_seen,
            "max state bits": state_bits,
            "max transient bits": transient_bits,
            "first interval past the width": next(
                (r["i"] for r in rows if r["max transient bits"] > WIDTH or r["max bits"] > WIDTH), None
            ),
            "verdict": "SHOWN: the count constant, every integer and transient within the width"
            if not lacks
            else "NOT SHOWN: " + lacks,
        }
    }


def conservations(record: Record, sense_sum: int, taken: int, booked: int) -> dict[str, Any]:
    """The conservations in the clicks (the owner's word: what the lattice conserves is shown conserved in the clicks): the charge, the count, the energy as the beat unchanged from one click to the next, the momentum."""
    cons: dict[str, Any] = {
        "charge: the senses summed over the births": sense_sum,
        "count: taken against booked over the births (hundredths)": quot(taken, booked, HUNDRED),
    }
    beats: dict[tuple[tuple[int, ...], int], list[tuple[int, int]]] = defaultdict(list)
    for c in record.credits:
        beats[(tuple(c["node"]), c["line"])].append((c["proper"], c["beat"]))
    pairs = [
        (b1, b2)
        for cs in beats.values()
        for (_p1, b1), (_p2, b2) in zip(sorted(cs), sorted(cs)[1:], strict=False)
        if b1 > 0 and b2 > 0
    ]
    cons["energy: the beat (intervals per period) of a body unchanged from one click to the next"] = {
        "click pairs": len(pairs),
        "unchanged": sum(1 for a, b in pairs if a == b),
        "changed by one": sum(1 for a, b in pairs if abs(a - b) == 1),
        "changed by more": sum(1 for a, b in pairs if abs(a - b) > 1),
    }
    cons["momentum: the close wrote (the credit lines' dP_a)"] = momentum(record)
    return {"the conservations in the clicks": cons} | constants(record)


def entropy(record: Record) -> dict[str, Any]:
    """The entropy of the clicks as the law's integer: each birth's draw has its room (the count of numbers the one-Link read could give); H(t) = SUM over the births to t of bit_length(room - 1), read from the record alone, never falling."""
    total = last = 0
    found = []
    for b in sorted(record.births, key=lambda b: int(b["i"])):
        total += (int(b["room"]) - 1).bit_length()
        if b["i"] != last:
            found.append((b["i"], total))
            last = b["i"]
    verdict = (
        f"SHOWN: H never falls (a sum of bit lengths), {total} bits over {len(record.births)} births"
        if record.births
        else "NOT READ: no birth"
    )
    return {
        "the entropy of the clicks": {
            "births with a room": len(record.births),
            "H at the end (bits)": total,
            "course (interval, H) at every eighth": found[:: max(1, len(found) // 8)],
            "verdict": verdict,
        }
    }


def gates(run: dict[str, Any]) -> dict[str, Any]:
    """Every gate's verdict with its numbers from the record alone, and the event lines of the gates' first SHOWN (`first_shown`)."""
    record = Record(run)
    out, decoded = species(record)
    found, sense_sum, taken, booked = charge_and_take(record)
    out |= found
    out |= dilation(decoded) | lengthening(record) | course(record) | era(record) | horizon(record)
    out |= tracks(record, decoded) | light_and_arrow(record)
    out |= conservations(record, sense_sum, taken, booked) | entropy(record)
    out["the decoder"] = {
        "floats used": 0,
        "readings": "quotients at a named scale, counts, bit lengths; rationals compared by cross multiplication",
    }
    from event_universe import events  # the events read the gates, after them

    out["events"] = events.first_shown(record, decoded)
    return out


def main(argv: list[str]) -> None:
    """The gates of a record file, one line each."""
    with open(argv[1], encoding="utf-8") as record:
        for k, v in gates(json.load(record)).items():
            print(json.dumps({k: v}))


if __name__ == "__main__":
    main(sys.argv)

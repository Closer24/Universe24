"""The reading's event lines (the owner's word of 2026-10-25: the record tells what it sees as it sees it): one line per gate at the interval it first shows, with its Node where it has one, in the gate's own words of three to six, for the page's labels and the bar's ticks; every line read from the record alone."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any

from event_universe.decoder import Rational, Record
from event_universe.gates import dilation, lengthening


def event(gate: str, label: str, i: int | None, node: Any, numbers: str) -> dict[str, Any]:
    """One event line of the reading: the gate, its label in the gate's own words (three to six), the interval and the Node of its first SHOWN where it has one, its numbers in one line."""
    return {
        "gate": gate,
        "label": label,
        "i": i,
        "node": None if node is None else list(node),
        "numbers": numbers,
    }


def unravel(record: Record, index: int) -> list[int]:
    """A Node's three coordinates from its index in the board's order."""
    cube = int(record.run["cube"])
    return [index // (cube * cube), (index // cube) % cube, index % cube]


def first_click(record: Record) -> list[dict[str, Any]]:
    """The first birth (a pair born), the first body credit (a body clicks) and the first credit of a line at a new Node (a body at a new Node)."""
    found = []
    births = sorted(record.births, key=lambda b: int(b["i"]))
    credits = sorted(record.credits, key=lambda c: int(c["i"]))
    if births:
        b = births[0]
        numbers = f"plane {b['line_pair']}, the children at {b['minus']} and {b['plus']}, taken {b['taken']} of {b['booked']} booked"
        found.append(event("17 charge conservation", "a pair born", b["i"], b["node"], numbers))
    if credits:
        c = credits[0]
        numbers = f"plane {c['line']}, the beat {c['beat']}, the proper count {c['proper']}"
        found.append(
            event("8 families forming (whole view)", "a body clicks", c["i"], c["node"], numbers)
        )
    seen: dict[int, set[tuple[int, ...]]] = defaultdict(set)
    for c in credits:
        if seen[c["line"]] and tuple(c["node"]) not in seen[c["line"]]:
            found.append(
                event(
                    "9 collisions",
                    "a body at a new Node",
                    c["i"],
                    c["node"],
                    f"plane {c['line']} credited at a new Node",
                )
            )
            break
        seen[c["line"]].add(tuple(c["node"]))
    return found


def first_horizon(record: Record) -> list[dict[str, Any]]:
    """The horizon's first held Link or frozen Node from the record's Node lines."""
    lines = record.run.get("nodes", [])
    held = next((line for line in lines if line["held"] or line["frozen"]), None)
    if held is None:
        return []
    at = held["held"][0][0] if held["held"] else held["frozen"][0]
    numbers = f"{len(held['held'])} Links held at the wall, {len(held['frozen'])} Nodes frozen"
    return [event("14 the horizon", "the horizon", held["i"], unravel(record, at), numbers)]


def first_course(record: Record) -> list[dict[str, Any]]:
    """The first interval the mean volume falls (the board contracts) and the era's first credit past the last birth at its Node (the era of matter)."""
    found = []
    rows = [(r["i"], int(r["volume mean"])) for r in record.rows]
    fall = next((b[0] for a, b in zip(rows, rows[1:], strict=False) if b[1] < a[1]), None)
    if fall is not None:
        gate = "6 contraction (the board, the reader's view)"
        found.append(event(gate, "the board contracts", fall, None, "the mean volume falls"))
    last_birth = {tuple(b["node"]): b["proper"] for b in record.births}
    credits = sorted(record.credits, key=lambda c: int(c["i"]))
    era = next(
        (
            c
            for c in credits
            if tuple(c["node"]) in last_birth and c["proper"] > last_birth[tuple(c["node"])]
        ),
        None,
    )
    if era is not None:
        found.append(
            event(
                "4 an era of matter",
                "the era of matter",
                era["i"],
                era["node"],
                "a body credited past the last birth at its Node",
            )
        )
    return found


def first_reader(
    record: Record, decoded: list[tuple[dict[str, Any], str, Rational]]
) -> list[dict[str, Any]]:
    """The dilation's and the lengthening's first SHOWN over the credits to that interval (the reader's view), and the arrow at the end."""
    found = []
    readers: list[tuple[str, str, Callable[[int], dict[str, Any]]]] = [
        ("10 gravitational time dilation", "the clocks run slow", lambda k: dilation(decoded[:k])),
        (
            "2 the Links lengthening in the clicks",
            "the Links lengthen",
            lambda k: lengthening(record.through(k)),
        ),
    ]
    for gate, label, reader in readers:
        for k in range(1, len(decoded) + 1):
            out = reader(k)
            if out and next(iter(out.values()))["verdict"].startswith("SHOWN"):
                found.append(event(gate, label, decoded[k - 1][0]["i"], None, "in the reader's view"))
                break
    rb = record.run.get("run_back")
    if rb and rb["exact"] == rb["intervals"]:
        found.append(
            event(
                "18 the arrow of time",
                "the run back exact",
                int(record.run["intervals"]),
                None,
                f"{rb['exact']} of {rb['intervals']} intervals",
            )
        )
    return found


def first_shown(
    record: Record, decoded: list[tuple[dict[str, Any], str, Rational]]
) -> list[dict[str, Any]]:
    """Every event line in the order of its interval: the first click, the horizon, the course, the reader's view and the arrow."""
    found = (
        first_click(record)
        + first_horizon(record)
        + first_course(record)
        + first_reader(record, decoded)
    )
    return sorted(found, key=lambda e: (e["i"] is None, e["i"] or 0))

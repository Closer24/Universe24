"""Row 15, the conservation at the click, read twice: the books at every whole click, and the ledger beside them."""

# The first reading, K3 (Animate's part C): a whole click's books stand at the click itself, or at each of its two ends
# where it takes at both (the record's guard). Each part takes: its taken holds a holding, each taken holding loses
# and each laid one gains, its windings and kept together, and over the part's holdings the windings and the kept
# together gain nothing (law 8: every integer is held, moved or booked); the click's own train is among those it takes
# from, and where it holds its q, q whole windings left (law 5). A take paid from its remainder alone moves no whole
# winding, so a holding is read by its windings and kept together. A whole click that lacks a field its books are read
# from (its ends, a part's taken and laid, a holding's train, windings and kept) is not read, and named (Sofer's G1).
# The second reading is the plan's (TENSOR24.md section 19, item 8; TENSOR24_PLAN.md section 5, item 8): the wind over
# every train of the header after the clicks against after the step, at every round with a click, whole or split; a
# round is read where its step lines and its clicks lines hold the header's trains and no other, each with its whole
# wind. A click moves wind between trains and keeps its remainder in the train it took from (Holding's kept), so the
# change over every train is what the clicks booked, 0 where the books close: part C's "the change equals the booked"
# is each reading held against 0, and a split click, which books no holding, moves no wind out of the trains. The row:
# not read with no whole click, with the ledger absent or not read, or with a header that names no train, the cause
# named; not shown where a part read fails, the books at a whole click read or the wind at a round read, beside the
# rest named; else not read where a whole click lacks a field or a round with a click is not read; else shown.

from typing import Any

from tensor24.decoder.records import Record, whole

Line = dict[str, Any]
BOOKS = ("taken", "laid")
HELD = ("train", "windings", "kept")
CLICKS = ("whole", "split")


def gained(holdings: list[Line]) -> int:
    """What holdings gained over a click, the windings and the kept together: after less before."""
    return sum(h["windings"][1] - h["windings"][0] + h["kept"][1] - h["kept"][0] for h in holdings)


def parts(click: Line) -> list[Line]:
    """Where a click's books stand: at its ends where it takes at both, else at the click itself."""
    ends: list[Line] = click["ends"]
    return ends if ends else [click]


def left(click: Line) -> int:
    """The whole windings that left the trains a click took from, over its parts."""
    return sum(h["windings"][0] - h["windings"][1] for p in parts(click) for h in p["taken"])


def closes(click: Line) -> bool:
    """Whether a whole click's books close: each part takes and closes, from the click's train, q windings leaving."""
    each = all(
        p["taken"]
        and all(gained([h]) < 0 for h in p["taken"])
        and all(gained([h]) > 0 for h in p["laid"])
        and gained(p["taken"]) + gained(p["laid"]) == 0
        for p in parts(click)
    )
    trains = {h["train"] for p in parts(click) for h in p["taken"]}
    own = not whole(click.get("train")) or click["train"] in trains
    counted = not whole(click.get("q")) or click["q"] == left(click)
    return each and own and counted


def legible(click: Line) -> bool:
    """Whether a whole click holds every field its books are read from: its ends, each part's books, each holding's."""
    sides = [click, *click.get("ends", [])]
    held = [h for p in sides for key in BOOKS for h in p.get(key, [])]
    return (
        "ends" in click
        and all(key in p for p in sides for key in BOOKS)
        and all(key in h for h in held for key in HELD)
    )


def first_reading(record: Record) -> dict[str, int]:
    """The books at every whole click: the whole clicks, those whose books are read, and those that close."""
    clicks = record.of("whole")
    read = [c for c in clicks if legible(c)]
    return {"whole clicks": len(clicks), "read": len(read), "closed": sum(closes(c) for c in read)}


def second_reading(record: Record, ledger: list[Line]) -> dict[str, int]:
    """The wind over every train of the header after the clicks against after the step, at every round with a click."""
    trains = {t["index"] for t in record.header.get("trains", []) if whole(t.get("index"))}
    winds: dict[tuple[int, str], dict[int, Any]] = {}
    for line in ledger:
        winds.setdefault((line["round"], line["at"]), {})[line["train"]] = line.get("wind")
    clicked = sorted({e["round"] for e in record.events if e["kind"] in CLICKS})
    pairs = [(winds.get((r, "step"), {}), winds.get((r, "clicks"), {})) for r in clicked]
    read = [
        (step, clicks)
        for step, clicks in pairs
        if trains
        and set(step) == set(clicks) == trains
        and all(whole(w) for w in [*step.values(), *clicks.values()])
    ]
    agree = sum(sum(step.values()) == sum(clicks.values()) for step, clicks in read)
    return {
        "trains": len(trains),
        "rounds with a click": len(clicked),
        "read": len(read),
        "agree": agree,
    }


def unread(first: dict[str, int]) -> bool:
    """Nothing to read: a record with no whole click."""
    return not first["whole clicks"]


def verdict(kind: str, *causes: str, **readings: dict[str, int]) -> dict[str, Any]:
    """A verdict of the row, its causes joined in order, with the readings it stands on."""
    return {"kind": kind, "cause": "; ".join(cause for cause in causes if cause), **readings}


def row_15(
    record: Record, ledger: list[Line] | None, why: str = "the ledger is absent"
) -> dict[str, Any]:
    """The row's verdict from its two readings, with its cause; why names the cause of a ledger that is None."""
    first = first_reading(record)
    if unread(first):
        return verdict("NOT READ", "no whole click", first=first)
    lacking = [c for c in record.of("whole") if not legible(c)]
    lacks = (
        f"the whole click at round {lacking[0]['round']}, site {lacking[0]['site']} lacks a field its books are read from"
        if lacking
        else ""
    )
    opened = first["read"] - first["closed"]
    books = (
        f"the books open at {opened} of {first['read']} whole clicks read"
        if opened
        else "the books close at every whole click read"
        if lacking
        else "the books close at every whole click"
    )
    if ledger is None:
        return verdict("NOT READ", why, books, lacks, first=first)
    second = second_reading(record, ledger)
    rounds, read, agree = second["rounds with a click"], second["read"], second["agree"]
    if not second["trains"]:
        return verdict("NOT READ", "the header names no train", books, lacks, first=first, second=second)
    lines = f"the ledger's lines are read at {read} of {rounds} rounds with a click"
    if not read:
        return verdict("NOT READ", books, lacks, lines, first=first, second=second)
    wind = f"the wind over every train agrees after the clicks and after the step at {agree} of {read} rounds read, of {rounds} with a click"
    if opened or agree < read:
        return verdict("NOT SHOWN", books, lacks, wind, first=first, second=second)
    if lacking or read < rounds:
        partly = lines if read < rounds else ""
        return verdict("NOT READ", lacks, "" if lacking else books, partly, first=first, second=second)
    return verdict("SHOWN", books, wind, first=first, second=second)

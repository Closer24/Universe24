"""Row 15, the conservation at the click, read twice: the books at every whole click, and the ledger beside them."""

# The first reading, K3 (Animate's part C): a whole click's books stand at the click itself, or at each of its two
# ends where it takes at both (the record's guard), and are read per train. A part's taken and its laid each hold one
# holding per train, a train's holdings on one side read as one where each starts where the last ended, and no train
# stands on both sides of a part. Each part takes: each taken train loses and each laid one gains, its windings at
# its winding and its kept together, and over the part they together gain nothing (law 8: every integer is held, moved
# or booked). A holding's windings count its train's whole windings, each its train's winding in notches as the
# header's train card gives it, and its kept counts notches, so the books read each train's windings at its own
# winding (David's 6488889537, item 2, A6: the giver's kept is the drive's remainder, -r_d). The click's own train is
# among those it takes from, and where it holds its q, q whole windings left (law 5), over both its ends where it
# takes at both. A take paid from its remainder alone moves no whole winding, so a holding is read by its windings and
# kept together. A whole click whose books cannot be read is not read, and named: one that lacks a field they are read
# from (its own train, its ends, a part's taken and laid, a holding's train, windings and kept; Sofer's G1), that books
# a train the header gives no winding, or that books a train twice in a part: twice on one side, unchained, or on both
# sides. The second reading is the plan's (TENSOR24.md section 19, item 8; TENSOR24_PLAN.md
# section 5, item 8): the wind over every train of the header after the clicks against after the step, at every round
# with a click, whole or split; a round is read where its step lines and its clicks lines hold the header's trains
# and no other, each with its whole wind, and the header's trains are read where every train card holds its index. A
# click moves wind between trains and keeps its remainder in the train it took from (Holding's kept), so the change
# over every train is what the clicks booked, 0 where the books close: part C's "the change equals the booked" is
# each reading held against 0, and a split click, which books no holding, moves no wind out of the trains. The row:
# not read with no whole click; not shown where a part read fails, the books at a whole click read or the wind at a
# round read, with every gap named beside it, since law 8 breaks on the first reading alone; else not read where a
# whole click's books are not read, the ledger is absent or not read at a round with a click, or the header names no
# train or a train card holds no index, the cause named; else shown.

from typing import Any

from tensor24.decoder.records import Record, whole

Line = dict[str, Any]
BOOKS = ("taken", "laid")
HELD = ("train", "windings", "kept")
CLICKS = ("whole", "split")
LACKS = "lacks a field its books are read from"
UNWOUND = "books a train the header gives no winding"
TWICE = "books one train twice in a part"
Windings = dict[int, int]  # each train's winding by its index, as the header's train cards give it


def windings_of(record: Record) -> Windings:
    """Each train's winding by its index, from the header's train cards that hold both."""
    cards = record.header.get("trains", [])
    return {t["index"]: t["winding"] for t in cards if whole(t.get("index")) and whole(t.get("winding"))}


def gained(holdings: list[Line], winding: Windings) -> int:
    """What holdings gained over a click, each one's windings at its train's winding and its kept: after less before."""
    return sum(
        (h["windings"][1] - h["windings"][0]) * winding[h["train"]] + h["kept"][1] - h["kept"][0]
        for h in holdings
    )


def parts(click: Line) -> list[Line]:
    """Where a click's books stand: at its ends where it takes at both, else at the click itself."""
    ends: list[Line] = click["ends"]
    return ends if ends else [click]


def left(click: Line) -> int:
    """The whole windings that left the trains a click took from, over its parts."""
    return sum(h["windings"][0] - h["windings"][1] for p in parts(click) for h in p["taken"])


def chained(holdings: list[Line]) -> list[Line] | None:
    """A side's holdings one per train: a train's holdings in turn, each starting where the last ended, read as one."""
    runs: dict[int, Line] = {}
    for h in holdings:
        last = runs.get(h["train"])
        if last is None:
            runs[h["train"]] = h
        elif h["windings"][0] == last["windings"][1] and h["kept"][0] == last["kept"][1]:
            runs[h["train"]] = {
                "train": h["train"],
                "windings": [last["windings"][0], h["windings"][1]],
                "kept": [last["kept"][0], h["kept"][1]],
            }
        else:
            return None
    return list(runs.values())


def per_train(part: Line) -> tuple[list[Line], list[Line]] | None:
    """A part's taken and laid one holding per train, no train on both sides; None where the part books a train twice."""
    taken, laid = chained(part["taken"]), chained(part["laid"])
    if taken is None or laid is None or {h["train"] for h in taken} & {h["train"] for h in laid}:
        return None
    return taken, laid


def part_closes(part: Line, winding: Windings) -> bool:
    """A part takes and closes: each taken train loses, each laid one gains, and the part together gains nothing."""
    held = per_train(part)
    if held is None:
        return False
    taken, laid = held
    return (
        bool(taken)
        and all(gained([h], winding) < 0 for h in taken)
        and all(gained([h], winding) > 0 for h in laid)
        and gained(taken, winding) + gained(laid, winding) == 0
    )


def closes(click: Line, winding: Windings) -> bool:
    """Whether a whole click's books close: each part takes and closes, from the click's train, q windings leaving."""
    each = all(part_closes(p, winding) for p in parts(click))
    trains = {h["train"] for p in parts(click) for h in p["taken"]}
    own = click.get("train") in trains
    counted = not whole(click.get("q")) or click["q"] == left(click)
    return each and own and counted


def unread_books(click: Line, winding: Windings) -> str:
    """Why a whole click's books are not read: a field lacking, a train with no winding, or a train booked twice; or nothing."""
    held_by = [click, *click.get("ends", [])]
    held = [h for p in held_by for key in BOOKS for h in p.get(key, [])]
    if not (
        "ends" in click
        and "train" in click
        and all(key in p for p in held_by for key in BOOKS)
        and all(key in h for h in held for key in HELD)
    ):
        return LACKS
    if not all(h["train"] in winding for h in held):
        return UNWOUND
    return TWICE if any(per_train(p) is None for p in parts(click)) else ""


def first_reading(record: Record) -> dict[str, int]:
    """The books at every whole click: the whole clicks, those whose books are read, and those that close."""
    winding = windings_of(record)
    clicks = record.of("whole")
    read = [c for c in clicks if not unread_books(c, winding)]
    return {
        "whole clicks": len(clicks),
        "read": len(read),
        "closed": sum(closes(c, winding) for c in read),
    }


def second_reading(record: Record, ledger: list[Line]) -> dict[str, int]:
    """The wind over every train of the header after the clicks against after the step, at every round with a click."""
    cards = record.header.get("trains", [])
    indexed = all(whole(t.get("index")) for t in cards)
    trains = {t["index"] for t in cards} if indexed else set()
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


def wall(record: Record, second: dict[str, int] | None, why: str) -> str:
    """Why the second reading is read at no round: the ledger absent or not read, a train card with no index, no train."""
    cards = [
        n for n, t in enumerate(record.header.get("trains", []), start=1) if not whole(t.get("index"))
    ]
    if second is None:
        return why
    if cards:
        return f"the header's train card {cards[0]} holds no index"
    return "" if second["trains"] else "the header names no train"


def row_15(
    record: Record, ledger: list[Line] | None, why: str = "the ledger is absent"
) -> dict[str, Any]:
    """The row's verdict from its two readings, with its cause; why names the cause of a ledger that is None."""
    first = first_reading(record)
    if unread(first):
        return verdict("NOT READ", "no whole click", first=first)
    winding = windings_of(record)
    lacking = [(c, cause) for c in record.of("whole") if (cause := unread_books(c, winding))]
    lacks = (
        f"the whole click at round {lacking[0][0]['round']}, site {lacking[0][0]['site']} {lacking[0][1]}"
        if lacking
        else ""
    )
    opened = first["read"] - first["closed"]
    books = (
        f"the books open at {opened} of {first['read']} whole clicks read"
        if opened
        else "the books close at every whole click read"
        if lacking and first["read"]
        else ""
        if lacking
        else "the books close at every whole click"
    )
    second = None if ledger is None else second_reading(record, ledger)
    readings = {"first": first} if second is None else {"first": first, "second": second}
    barred = wall(record, second, why)
    rounds, read, agree = (
        (0, 0, 0) if second is None else (second["rounds with a click"], second["read"], second["agree"])
    )
    lines = (
        f"the ledger's lines are read at {read} of {rounds} rounds with a click"
        if not barred and read < rounds
        else ""
    )
    wind = (
        f"the wind over every train agrees after the clicks and after the step at {agree} of {read} rounds read, of {rounds} with a click"
        if read
        else ""
    )
    if opened or agree < read:
        return verdict("NOT SHOWN", books, lacks, wind or barred or lines, **readings)
    if barred:
        return verdict("NOT READ", barred, books, lacks, **readings)
    if not read:
        return verdict("NOT READ", books, lacks, lines, **readings)
    if lacking or lines:
        return verdict("NOT READ", lacks, "" if lacking else books, lines, **readings)
    return verdict("SHOWN", books, wind, **readings)

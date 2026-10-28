"""Row 15, the conservation at the click, read twice: the books at every whole click, and the ledger beside them."""

# The first reading, K3 (Animate's part C): over a whole click's holdings, taken and laid, the windings and the kept
# together gain nothing (law 8: every integer is held, moved or booked), at the click itself, or at each of its two
# ends where it takes at both, its books standing in its ends alone there (the record's guard). A whole click that
# lacks a field its books are read from (its ends, a part's taken and laid, a holding's windings and kept) leaves the
# reading not read, the click named (Sofer's G1). The second reading, the plan's (section 8, the books): the wind over
# every train after the clicks against the wind over every train after the step, at every round with a click, whole
# or split, the ledger's control totals beside the clicks' journal; a click moves wind between trains and keeps its
# remainder in the train it took from, so the total stands, and a split click or a turnover between the two lines is
# read alike. A round is read where its step and its clicks lines hold the same trains, each with its whole wind. The
# row: not read with no whole click, "no whole click", or with the ledger absent or not read, the cause named; shown
# where every whole click's books close and the wind agrees at every round with a click; not shown where either
# fails at a part read; not read where the ledger's lines are read at no round with a click, or at some alone.

from typing import Any

from tensor24.decoder.records import Record, whole

Line = dict[str, Any]
BOOKS = ("taken", "laid")
HELD = ("windings", "kept")
CLICKS = ("whole", "split")


def gained(holdings: list[Line]) -> int:
    """What holdings gained over a click, the windings and the kept together: after less before."""
    return sum(h["windings"][1] - h["windings"][0] + h["kept"][1] - h["kept"][0] for h in holdings)


def parts(click: Line) -> list[Line]:
    """Where a click's books stand: at its ends where it takes at both, else at the click itself."""
    ends: list[Line] = click["ends"]
    return ends if ends else [click]


def closes(click: Line) -> bool:
    """Whether a whole click's books close at every part that holds them."""
    return all(gained(p["taken"]) + gained(p["laid"]) == 0 for p in parts(click))


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
    """The wind over every train after the clicks against after the step, at every round with a click."""
    winds: dict[tuple[int, str], dict[int, Any]] = {}
    for line in ledger:
        winds.setdefault((line["round"], line["at"]), {})[line["train"]] = line.get("wind")
    clicked = sorted({e["round"] for e in record.events if e["kind"] in CLICKS})
    pairs = [(winds.get((r, "step"), {}), winds.get((r, "clicks"), {})) for r in clicked]
    read = [
        (step, clicks)
        for step, clicks in pairs
        if step
        and set(step) == set(clicks)
        and all(whole(w) for w in [*step.values(), *clicks.values()])
    ]
    agree = sum(sum(step.values()) == sum(clicks.values()) for step, clicks in read)
    return {"rounds with a click": len(clicked), "read": len(read), "agree": agree}


def unread(first: dict[str, int]) -> bool:
    """Nothing to read: a record with no whole click."""
    return not first["whole clicks"]


def row_15(
    record: Record, ledger: list[Line] | None, why: str = "the ledger is absent"
) -> dict[str, Any]:
    """The row's verdict from its two readings, with its cause; why names the cause of a ledger that is None."""
    first = first_reading(record)
    if unread(first):
        return {"kind": "NOT READ", "cause": "no whole click", "first": first}
    if first["read"] < first["whole clicks"]:
        lacking = [c for c in record.of("whole") if not legible(c)][0]
        cause = f"the whole click at round {lacking['round']}, site {lacking['site']} lacks a field its books are read from"
        return {"kind": "NOT READ", "cause": cause, "first": first}
    every = first["closed"] == first["whole clicks"]
    books = (
        "the books close at every whole click"
        if every
        else f"the books open at {first['whole clicks'] - first['closed']} of {first['whole clicks']} whole clicks"
    )
    if ledger is None:
        return {"kind": "NOT READ", "cause": f"{why}; {books}", "first": first}
    second = second_reading(record, ledger)
    rounds, read, agree = second["rounds with a click"], second["read"], second["agree"]
    held = every and agree == read
    if not read or (held and read < rounds):
        cause = f"{books}; the ledger's lines are read at {read} of {rounds} rounds with a click"
        return {"kind": "NOT READ", "cause": cause, "first": first, "second": second}
    wind = f"the wind over every train agrees after the clicks and after the step at {agree} of {read} rounds read, of {rounds} with a click"
    return {
        "kind": "SHOWN" if held else "NOT SHOWN",
        "cause": f"{books}; {wind}",
        "first": first,
        "second": second,
    }

"""Row 15, the conservation at the click, read twice: the books at every whole click, and the ledger beside them."""

# The first reading, K3 (Animate's part C): over a whole click's holdings, taken and laid, the windings and the kept
# together gain nothing (law 8: every integer is held, moved or booked), at the click itself, or at each of its ends
# where it takes at both, its books standing in its ends alone there. The second reading, the ledger: per round and
# train, the windings held after the clicks less those after the step, against the windings the round's whole clicks
# moved into that train. A record with no whole click reads the row not read, "no whole click"; a ledger absent, or
# with no round holding both its step and its clicks lines, reads the second not read, and the row with it.

from typing import Any

from tensor24.decoder.records import Record, whole

Line = dict[str, Any]


def gained(holdings: list[Line]) -> int:
    """What holdings gained over a click, the windings and the kept together: after less before."""
    return sum(h["windings"][1] - h["windings"][0] + h["kept"][1] - h["kept"][0] for h in holdings)


def parts(click: Line) -> list[Line]:
    """Where a click's books stand: at its ends where it takes at both, else at the click itself."""
    ends: list[Line] = click.get("ends", [])
    return ends if ends else [click]


def closes(click: Line) -> bool:
    """Whether a whole click's books close at every part that holds them."""
    return all(gained(p.get("taken", [])) + gained(p.get("laid", [])) == 0 for p in parts(click))


def moved(click: Line) -> dict[int, int]:
    """The windings a click moved into each train, laid less taken; the kept stays at the clock."""
    into: dict[int, int] = {}
    for p in parts(click):
        for h in [*p.get("taken", []), *p.get("laid", [])]:
            into[h["train"]] = into.get(h["train"], 0) + h["windings"][1] - h["windings"][0]
    return into


def first_reading(record: Record) -> dict[str, int]:
    """The books at every whole click."""
    clicks = record.of("whole")
    return {"whole clicks": len(clicks), "closed": sum(closes(c) for c in clicks)}


def second_reading(record: Record, ledger: list[Line]) -> dict[str, int]:
    """The ledger's clicks less its step, per round and train, against the round's clicks."""
    held = {(line["round"], line["at"], line["train"]): line.get("windings") for line in ledger}
    rounds = sorted(
        {r for r, at, _ in held if at == "step"} & {r for r, at, _ in held if at == "clicks"}
    )
    trains = sorted({t for _, _, t in held})
    into: dict[tuple[int, int], int] = {}
    for c in record.of("whole"):
        for train, windings in moved(c).items():
            into[(c["round"], train)] = into.get((c["round"], train), 0) + windings
    pairs = [(r, t) for r in rounds for t in trains]
    agree = 0
    for r, t in pairs:
        after, before = held.get((r, "clicks", t)), held.get((r, "step", t))
        if whole(after) and whole(before):
            agree += after - before == into.get((r, t), 0)
    return {"rounds with both lines": len(rounds), "pairs read": len(pairs), "agree": agree}


def unread(first: dict[str, int]) -> bool:
    """Nothing to read: a record with no whole click."""
    return not first["whole clicks"]


def row_15(record: Record, ledger: list[Line] | None) -> dict[str, Any]:
    """The row's verdict from its two readings, with its cause."""
    first = first_reading(record)
    if unread(first):
        return {"kind": "NOT READ", "cause": "no whole click", "first": first}
    every = first["closed"] == first["whole clicks"]
    books = (
        "the books close at every whole click"
        if every
        else f"the books open at {first['whole clicks'] - first['closed']} of {first['whole clicks']} whole clicks"
    )
    if ledger is None:
        return {"kind": "NOT READ", "cause": f"the ledger is absent; {books}", "first": first}
    second = second_reading(record, ledger)
    if not second["rounds with both lines"]:
        cause = f"no round of the ledger holds both its step and its clicks lines; {books}"
        return {"kind": "NOT READ", "cause": cause, "first": first, "second": second}
    agree = second["agree"] == second["pairs read"]
    kind = "SHOWN" if every and agree else "NOT SHOWN"
    cause = (
        f"{books}; the ledger agrees at {second['agree']} of {second['pairs read']} rounds and trains"
    )
    return {"kind": kind, "cause": cause, "first": first, "second": second}

"""Clock: the clocks' rate gears wind up and run down together; a bang lies between two bottoms of their load, and each later bang builds clocks of more parts.
Algebra: the load per round; its bottoms, no higher than the round before and lower than the round after; each train's depth, one deeper than its deepest part; compared bang by bang.
Board: the load, read from the ledger at the time gear the header names; the clicks of each bang and the trains they lay; the clocks the ledger holds at each bang's end.
Clicks: row 46, each later bang shows more: more kinds of click and deeper clocks laid; shown, not shown or not read, with its cause.
"""

# What is to be seen (the owner's words: 2026-10-28, 14:44 UTC, "every bang adds more; the clock becomes more and more
# complex"; 2026-10-29, 06:3x UTC, to Animate, "ever more complex clocks"). The bangs: no line marks a top once the
# trigger at the top goes (the owner's word of 2026-10-29, 06:1x UTC, through David), so the bangs are read from the
# load, the time gear's count summed over the board, which stands on the ledger's step line of the train the header
# names its time gear (the header's field time_gear; the time gear's windings, its winding being one notch). A bottom
# is a round whose load is no higher than the round before's and lower than the round after's. A bang runs from the
# first round, or from a bottom, to the round before the next bottom, and is whole where that next bottom closes it.
# A clock's depth: a train whose header card names no parts (the card's field parts, the trains it binds) is 0, and a
# train with parts is one deeper than its deepest part; a card without its index or its parts (a row of whole numbers),
# a part no card names, or parts that bind themselves leave a train's depth unread. Reading 1, the clicks: per bang whole, its click kinds
# (each whole or split click's kind and train) and the deepest clock its whole clicks lay (the trains of their laid
# holdings, at the click or at its ends, and of their children). Reading 2, the ledger: per bang whole, the deepest
# clock holding a winding at the bang's last round, after its clicks where the ledger holds them there, else after its
# step. A later bang shows more where its click kinds and its deepest clock laid are each at least the last bang's and
# one of them more. The row: not read where the ledger is absent, the header names no time gear, a round from the
# first to the last of the ledger's holds no load, fewer than two bangs are whole, or a clock read is of no depth, the
# cause named; not shown where a later bang shows no more than the last, or the deepest clock held falls at a bang's
# end, the first named; else shown. A finite board repeats in the end (draft K, K2), so the row names the bang where
# the rise stops.

from typing import Any

from tensor24.decoder.records import Record, whole

Line = dict[str, Any]
CLICKS = ("whole", "split")
BOOKED = ("laid",)  # where a whole click and each of its ends lay their holdings
Bang = tuple[int, int]  # a bang's first and last rounds


def depths(cards: list[Line]) -> dict[int, int]:
    """Each train's depth by its index, where its parts are read: 0 with no parts, else one deeper than its deepest part."""
    parts = {
        t["index"]: t["parts"]
        for t in cards
        if whole(t.get("index"))
        and isinstance(t.get("parts"), list)
        and all(whole(p) for p in t["parts"])
    }
    found: dict[int, int] = {}
    for _ in parts:
        for train, of in parts.items():
            if train not in found and all(p in found for p in of):
                found[train] = 1 + max(found[p] for p in of) if of else 0
    return found


def bottoms(load: list[int]) -> list[int]:
    """The places of the load's bottoms: no higher than the place before and lower than the place after."""
    return [n for n in range(1, len(load) - 1) if load[n] <= load[n - 1] and load[n] < load[n + 1]]


def bangs(rounds: list[int], load: list[int]) -> list[Bang]:
    """The bangs whole: from the first round, or a bottom, to the round before the next bottom."""
    starts = [0, *bottoms(load)]
    return [(rounds[a], rounds[b] - 1) for a, b in zip(starts, starts[1:], strict=False)]


def laid(click: Line) -> list[Any]:
    """The trains a whole click lays: its laid holdings', at the click and at its ends, and its children's."""
    parts = [click, *click.get("ends", [])]
    holdings = [h for p in parts for key in BOOKED for h in p.get(key, [])]
    return [h.get("train") for h in [*holdings, *click.get("children", [])]]


def read_clicks(record: Record, bang: Bang) -> tuple[int, list[Any]]:
    """Reading 1 on one bang: its count of click kinds, and the trains its whole clicks lay."""
    first, last = bang
    clicks = [e for e in record.events if e["kind"] in CLICKS and first <= e["round"] <= last]
    kinds = {(e["kind"], e.get("train")) for e in clicks}
    return len(kinds), [t for e in clicks if e["kind"] == "whole" for t in laid(e)]


def read_held(ledger: list[Line], last: int) -> list[Any]:
    """Reading 2 on one bang: the trains holding a winding at its last round, after its clicks, else after its step."""
    lines = [line for line in ledger if line["round"] == last]
    at = "clicks" if any(line["at"] == "clicks" for line in lines) else "step"
    return [
        line["train"]
        for line in lines
        if line["at"] == at and whole(line.get("windings")) and line["windings"] > 0
    ]


def verdict(kind: str, cause: str, **readings: Any) -> dict[str, Any]:
    """A verdict of the row, with its cause and the readings it stands on."""
    return {"kind": kind, "cause": cause, **readings}


def frame(record: Record, ledger: list[Line]) -> tuple[list[Bang], str]:
    """The bangs whole read from the load, or why none are: no time gear, a round with no load, fewer than two."""
    gear = record.header.get("time_gear")
    if not whole(gear):
        return [], "the header names no time gear"
    load: dict[int, int] = {}
    for line in ledger:
        windings = line.get("windings")
        if line["at"] == "step" and line["train"] == gear and whole(windings):
            load[line["round"]] = windings
    rounds = list(range(1, max(line["round"] for line in ledger) + 1)) if ledger else []
    unloaded = [r for r in rounds if r not in load]
    if unloaded or not rounds:
        return [], f"the ledger holds no load at round {unloaded[0] if unloaded else 1}"
    found = bangs(rounds, [load[r] for r in rounds])
    if not found[1:]:
        return found, f"the bangs whole number {len(found)}, where the row compares two or more"
    return found, ""


def row_46(
    record: Record, ledger: list[Line] | None, why: str = "the ledger is absent"
) -> dict[str, Any]:
    """The row's verdict from its two readings, with its cause; why names the cause of a ledger that is None."""
    if ledger is None:
        return verdict("NOT READ", why)
    found, gap = frame(record, ledger)
    if gap:
        return verdict("NOT READ", gap)
    depth = depths(record.header.get("trains", []))
    clicked = [read_clicks(record, bang) for bang in found]
    held = [read_held(ledger, last) for _, last in found]
    trains = [t for _, lays in clicked for t in lays] + [t for trains in held for t in trains]
    deep = [t for t in trains if t not in depth]
    if deep:
        return verdict(
            "NOT READ",
            f"the train {deep[0]} is a clock of no depth: its card or a part's names no parts",
        )
    kinds = [k for k, _ in clicked]
    laid_deepest = [max((depth[t] for t in lays), default=0) for _, lays in clicked]
    held_deepest = [max((depth[t] for t in trains), default=0) for trains in held]
    readings = {"bangs": found, "kinds": kinds, "laid": laid_deepest, "held": held_deepest}
    for n in range(1, len(found)):
        more = kinds[n] >= kinds[n - 1] and laid_deepest[n] >= laid_deepest[n - 1]
        if not (more and (kinds[n] > kinds[n - 1] or laid_deepest[n] > laid_deepest[n - 1])):
            cause = (
                f"bang {n + 1} shows no more than bang {n}: {kinds[n]} click kinds against {kinds[n - 1]}, "
                f"its deepest clock laid {laid_deepest[n]} against {laid_deepest[n - 1]}"
            )
            return verdict("NOT SHOWN", cause, **readings)
        if held_deepest[n] < held_deepest[n - 1]:
            cause = f"the deepest clock held falls from {held_deepest[n - 1]} to {held_deepest[n]} at bang {n + 1}'s end"
            return verdict("NOT SHOWN", cause, **readings)
    cause = (
        f"each of the {len(found)} bangs whole shows more than the last: the click kinds {kinds}, "
        f"the deepest clock laid {laid_deepest} and held {held_deepest}"
    )
    return verdict("SHOWN", cause, **readings)

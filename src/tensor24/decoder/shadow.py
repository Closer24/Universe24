"""Clock: the board's physics read in its shadow, the click world (the owner's law of 23:4x UTC): the record's header, its click lines and its end are read, nothing of the board's state, so no claim stands on a board reading alone.
Algebra: whole counts and sums: at every round and Node-clock with a click line, the sum of q over the trains; the cone one Mesh a round, the Meshes the shorter way round each side by Rule3's carry (measure.meshes); no float, no root and no search.
Board: schema 1.3's header (its sides, its train cards, and its setting file verbatim, read for the sites its gears lay with a count or a tooth not 0), its click lines {round, site, train, q, tooth} and its end; no gear's count, slot, plan or act.
Clicks: four readings, each a tool the decoder holds ported to 1.3, each read SHOWN, or NOT SHOWN with its first counterexample named, or NOT READ with its cause named, or NO CLICK where the record holds no click line, not in the click world: the books at each click (row 15's first reading on clicks.py's counts), a duration as a clock's own count (D6) and the twins (D7), not read on 1.3, which names no clock, and the cone check by click (D8 on measure.past).
"""

import json
from typing import Any

from tensor24.decoder import clicks, measure
from tensor24.decoder.records import Line, Record, whole

ABSENT = "NO CLICK"
NO_LINE = "the record holds no click line: not in the click world"
NO_CLOCK = (
    "schema 1.3 names no clock: its click line holds no lay and no face (1.2's clock, K4, left with the whole"
    " click), and the ledger's Count lines name no train a clock; a proper time read from the 00 slot's depth would"
    " need a root, refused"
)
BOOKS = "the books at each click"
DURATION = "a duration as a clock's own count (D6)"
TWINS = "the twins (D7)"
CONE = "the cone check by click (D8)"
Verdict = dict[str, Any]


def books(record: Record) -> Verdict:
    """The books at each click, row 15's first reading on 1.3's click lines: at every round and Node-clock with a line the sum of q over the trains, 0 where they close; beside it, per train (every card, one with no line at 0) and per Node-clock, the lines, given, taken and net."""
    held = clicks.counted(record)
    lacking = [line for line in held.lines if not whole(line.get("q"))]
    if lacking:
        at = lacking[0]
        cause = f"the click line at round {at['round']}, site {at['site']} holds no q, which its books are read from"
        return measure.verdict("NOT READ", cause)
    cards = [t["index"] for t in record.header.get("trains", []) if whole(t.get("index"))]
    trains = {t: held.trains.get(t, clicks.Tally(0, 0, 0, 0)) for t in cards}
    sums = sorted(clicks.summed(held.lines).items())
    open_ = [(place, total) for place, total in sums if total != 0]
    readings = {"trains": trains, "sites": held.sites, "places": len(sums)}
    if open_:
        (round_, site), total = open_[0]
        cause = f"the sum of q over the trains is {total} at round {round_}, site {site}: not 0 at {len(open_)} of {len(sums)} places"
        return measure.verdict("NOT SHOWN", cause, **readings)
    cause = f"the sum of q over the trains is 0 at {len(sums)} of {len(sums)} places"
    return measure.verdict("SHOWN", cause, **readings)


def duration(record: Record) -> Verdict:
    """A duration only as a clock's own count (D6, measure.faces and elapsed on 1.2's whole clicks): not read on 1.3, which names no clock."""
    return measure.verdict("NOT READ", NO_CLOCK)


def twins(record: Record) -> Verdict:
    """The twins (D7, measure.twins on 1.2's clocks): not read on 1.3, by D6's cause, no clock on the record."""
    return measure.verdict("NOT READ", f"by D6's cause, no clock on the record: {NO_CLOCK}")


def laid(record: Record) -> tuple[set[int], str]:
    """The sites the header's setting file lays, a gear there with a count or a tooth not 0; or why it is not read."""
    for text in [f.get("text") for f in record.header.get("files", []) if isinstance(f, dict)]:
        try:
            held = json.loads(text) if isinstance(text, str) else None
        except ValueError, RecursionError:
            held = None
        if not (isinstance(held, dict) and "ticks" in held):
            continue
        gears: Any = held.get("gears", [])
        sites: set[int] = set()
        for n, gear in enumerate(gears if isinstance(gears, list) else [gears], start=1):
            match gear:
                case [_, _, int() as site, *teeth] if whole(site) and teeth and all(map(whole, teeth)):
                    sites |= {site} if any(teeth) else set()
                case _:
                    return set(), f"the setting's gear {n} names no site and counts"
        return sites, ""
    return set(), "the header holds no setting file"


def cone(record: Record) -> Verdict:
    """The cone check by click (D8, measure.cone_check on 1.2's takes), on 1.3's click lines and measure.past: every line's event (t, x) inside the lay's cone, past((0, y), (t, x)) for a site y the setting lays; the lay's cone alone, since measure.meshes obeys the triangle inequality (a line inside an earlier click's cone, that click inside the lay's, is inside the lay's, and the first line outside the lay's cone is outside every earlier click's) and the clicks as built report a passing and push nothing back into the gears, so the lay is the one cause on the board and its cone the whole causal past."""
    sides = record.header.get("sides")
    if not (isinstance(sides, list) and sides and all(whole(s) and s >= 1 for s in sides)):
        return measure.verdict("NOT READ", "the header's sides make no board")
    lay, unread = laid(record)
    if unread:
        return measure.verdict("NOT READ", unread)
    lines: list[Line] = clicks.listed(record)
    events = [(line["round"], line["site"]) for line in lines]
    outside = [e for e in events if not any(measure.past(sides, (0, y), e) for y in lay)]
    if outside:
        (round_, site), far = outside[0], len(outside)
        cause = f"the click line at round {round_}, site {site} stands outside the lay's cone: {far} of {len(lines)} lines outside"
        return measure.verdict("NOT SHOWN", cause, lines=len(lines), laid=len(lay))
    cause = f"every click line stands inside the lay's cone, one Mesh a round from the {len(lay)} sites laid: {len(lines)} of {len(lines)} lines"
    return measure.verdict("SHOWN", cause, lines=len(lines), laid=len(lay))


def shadow(record: Record) -> dict[str, Verdict]:
    """The four readings in the click world, each its verdict; on a record that holds no click line, NO CLICK on all four, not in the click world, before any other cause."""
    readings = {BOOKS: books, DURATION: duration, TWINS: twins, CONE: cone}
    if not clicks.listed(record):
        return {name: measure.verdict(ABSENT, NO_LINE) for name in readings}
    return {name: read(record) for name, read in readings.items()}

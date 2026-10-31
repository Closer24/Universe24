"""Clock: the board's physics read in its shadow, the click world (the owner's law of 23:4x UTC), as the clocks' meetings (the owner's word of 00:3x UTC): each event one quantum passing from one clock to another at one place, with no time axis but the events' order and each clock's count, and space read only by light's echo; the record's header and its click lines are read, nothing of the board's state, so no claim stands on a board reading alone.
Algebra: whole counts and sums: at every place, a round and a Node-clock with click lines, the sum of q over the trains, each side across a Mesh booked at both its places, and each line's q, a meeting one give of q -1 and one take of q +1 on one edge, a side and its mirror, the lines of q 0 that carried on no side dropped; per clock, a site and a train, its meetings counted and its given, taken and net; the cone one Mesh a round, the Meshes the shorter way round each side by Rule3's carry (measure.meshes), the lay's reach the most of them from a site to its nearest laid site; no float, no root and no search.
Board: the record's header (its sides, its train cards, and its setting file, the last of its files in the run's order, read for its gears, each a site on the board with its counts and its tooth, the sites laid those with a count or a tooth not 0) and its click lines, each a round, a site, a train and its q, with its edge sides in its site and across a Mesh; nothing of the board's state, no slot, plan or act.
Clicks: four readings, each read SHOWN, or NOT SHOWN with its first counterexample named, or NOT READ with its cause named, or NO CLICK, the owner's phrase, where the record holds no click line, before any other cause: the books at each click (row 15's first reading on clicks.py's counts, in row 15's order) and the cone check by click (D8 on measure.past), not read where no line could stand outside the lay's cone; and the click board's two, the meetings and each clock's line of meetings, the order counted with no duration. Owed and not built, so no verdict is typed for them: a duration as a clock's own count (D6) and the twins (D7), the act holding no clock's own count, and space by light's echo (reading 7), no rule yet telling light's click lines from the others.
"""

import json
from typing import Any

from tensor24.decoder import clicks, measure, records
from tensor24.decoder.records import Line, Record, whole
from tensor24.decoder.sides import formed
from tensor24.record import schema

ABSENT = "NO CLICK"
NO_LINE = "the record holds no click line: not in the click world"
ORDER = "the order counted, no duration"
BOOKS = "the books at each click"
CONE = "the cone check by click (D8)"
MEETINGS = "the meetings"
LINES = "each clock's line of meetings"
Verdict = dict[str, Any]
Clock = tuple[int, int]  # a site and a train: one clock of the record, its own line of events


def lacking(lines: list[Line], fields: tuple[str, ...], whose: str) -> tuple[set[clicks.Place], str]:
    """The places holding a click line that lacks a field its reading is read from, and the first such line named; or no place and nothing."""
    gaps = [(line, field) for line in lines for field in fields if not whole(line.get(field))]
    places = {(line["round"], line["site"]) for line, _ in gaps}
    if not gaps:
        return places, ""
    line, field = gaps[0]
    return (
        places,
        f"the click line at round {line['round']}, site {line['site']} holds no {field}, which {whose} read from",
    )


def placed(lines: list[Line], gaps: set[clicks.Place]) -> dict[clicks.Place, list[Line]]:
    """The click lines grouped by their place, a round and a Node-clock, in the schema's order, a place with a gap left out."""
    found: dict[clicks.Place, list[Line]] = {}
    for line in lines:
        found.setdefault((line["round"], line["site"]), []).append(line)
    return {place: held for place, held in found.items() if place not in gaps}


def carried(line: Line) -> list[Any]:
    """The edge sides a click line's clock carried on: the other train of each side in its site whose q is not 0, then each side across a Mesh by its place and train; none on a line of no side."""
    sides = [u for u, q, *_ in line.get("sides", []) if q]
    return sides + [(at, u) for u, at, *_ in line.get("across", [])]


def silent(line: Line) -> bool:
    """A click line of q 0 whose clock carried on no side: a clock listed as joined to a side that carried, no click of its own."""
    return line.get("q") == 0 and not carried(line)


def pair(held: list[Line]) -> list[Line]:
    """The click lines at one place whose clocks carried, the silent ones dropped, in the schema's order."""
    return [line for line in held if not silent(line)]


def edged(line: Line, other: Line) -> bool:
    """A line carried on one edge alone, its side to the other's train in its site."""
    return carried(line) == [other["train"]]


def met(held: list[Line]) -> bool:
    """Whether the click lines at one place are a meeting: one give and one take of one quantum, q -1 and q +1, two clocks, as the record's guard holds each train once at a place, the silent lines dropped, an edge side and its mirror: the giver's one side that carried the taker's and the taker's the giver's, and no other side carried there."""
    lines = pair(held)
    if sorted(line["q"] for line in lines) != [-1, 1]:
        return False
    give, take = sorted(lines, key=lambda line: line["q"])
    return edged(give, take) and edged(take, give)


def spread(counts: list[int]) -> str:
    """Whole counts said as one where they agree, else as their least to their most."""
    low, high = min(counts), max(counts)
    return f"{low}" if low == high else f"{low} to {high}"


def across(lines: list[Line]) -> tuple[dict[clicks.Place, int], int]:
    """Each side across a Mesh (schema 1.4) booked at its far place, as its own line books it at its own place: at its round and the Node-clock it names, its own q, which its partner's q, booked there through the partner's line, closes, so each edge across a Mesh closes at both its places; and the sides so booked counted, a side off its form booking nothing (the sides' guard refuses it)."""
    found: dict[clicks.Place, int] = {}
    held = [(e, side) for e in lines if isinstance(e.get("across"), list) for side in e["across"]]
    sides = [
        (e["round"], at, q)
        for e, side in held
        if formed(side, schema.ACROSS)
        for _, at, q, _, _ in [side]
    ]
    for round_, at, q in sides:
        found[(round_, at)] = found.get((round_, at), 0) + q
    return found, len(sides)


def books(record: Record) -> Verdict:
    """The books at each click, row 15's first reading on the click lines in row 15's order: at every place whose lines all hold q the sum of q over the trains, each side across a Mesh booked at both its places (its own line's q at its own, its own q at the far place it names, where its partner's closes it; the Boss's word of 06:0x UTC), so a place closes where each of its edges, in its site and across a Mesh, closes, NOT SHOWN at the first not 0 with the first line lacking q named beside it, else NOT READ naming that line, else SHOWN; beside it, per train (every card, one with no line at 0) and per Node-clock, the lines, given, taken and net."""
    if not clicks.listed(record):
        return measure.verdict(ABSENT, NO_LINE)
    held = clicks.counted(record)
    gaps, lacks = lacking(held.lines, ("q",), "its books are")
    cards = [t["index"] for t in record.header.get("trains", []) if whole(t.get("index"))]
    trains = {t: held.trains.get(t, clicks.Tally(0, 0, 0, 0)) for t in cards}
    booked, crossed = clicks.summed(held.lines), across(held.lines)
    for place, q in crossed[0].items():
        booked[place] = booked.get(place, 0) + q
    sums = [(place, total) for place, total in sorted(booked.items()) if place not in gaps]
    open_ = [(place, total) for place, total in sums if total != 0]
    readings = {"trains": trains, "sites": held.sites, "places": len(sums)}
    each = (
        f", each of the {crossed[1]} sides across a Mesh booked at both its places" if crossed[1] else ""
    )
    if open_:
        (round_, site), total = open_[0]
        cause = f"the sum of q over the trains is {total} at round {round_}, site {site}{each}: not 0 at {len(open_)} of {len(sums)} places"
        return measure.verdict("NOT SHOWN", f"{cause}; {lacks}" if lacks else cause, **readings)
    if lacks:
        return measure.verdict("NOT READ", lacks, **readings)
    cause = f"the sum of q over the trains is 0 at {len(sums)} of {len(sums)} places{each}"
    return measure.verdict("SHOWN", cause, **readings)


def meetings(record: Record) -> Verdict:
    """The meetings, the click board's events: at every place, a round and a Node-clock, one give and one take of one quantum from one clock, a site and a train, to the other, the round its order alone; NOT SHOWN at the first place that is not, among the places whose lines all hold their q and train, the first line lacking one named beside it, else NOT READ naming that line, else SHOWN, the meetings counted by the giving train and the taking train."""
    lines = clicks.listed(record)
    if not lines:
        return measure.verdict(ABSENT, NO_LINE)
    gaps, lacks = lacking(lines, ("q", "train"), "its meeting is")
    places = placed(lines, gaps)
    odd = [(place, held) for place, held in places.items() if not met(held)]
    ways: dict[tuple[int, int], int] = {}
    for held in [held for held in places.values() if met(held)]:
        give, take = sorted(pair(held), key=lambda line: line["q"])
        ways[(give["train"], take["train"])] = ways.get((give["train"], take["train"]), 0) + 1
    readings = {"places": len(places), "ways": ways}
    if odd:
        (round_, site), held = odd[0]
        q, trains = [line["q"] for line in held], [line["train"] for line in held]
        cause = f"the click lines at round {round_}, site {site} hold q {q} of the trains {trains}: not one give and one take of one quantum at {len(odd)} of {len(places)} places"
        return measure.verdict("NOT SHOWN", f"{cause}; {lacks}" if lacks else cause, **readings)
    if lacks:
        return measure.verdict("NOT READ", lacks, **readings)
    given = ", ".join(
        f"{n} from train {giver} to train {taker}" for (giver, taker), n in sorted(ways.items())
    )
    cause = f"one give and one take of one quantum at {len(places)} of {len(places)} places: {given}"
    return measure.verdict("SHOWN", cause, **readings)


def clock_lines(record: Record) -> Verdict:
    """Each clock's line of meetings: per clock, a site and a train, its click lines in round order, the silent ones dropped, the round its order alone, its meetings counted with no duration (its lines that stand in a meeting) and its books beside them (clicks.tallied); NOT SHOWN naming the first clock with a line in no meeting, among the places whose lines all hold their q and train, the first line lacking one named beside it, else NOT READ naming that line, else SHOWN."""
    lines = clicks.listed(record)
    if not lines:
        return measure.verdict(ABSENT, NO_LINE)
    gaps, lacks = lacking(lines, ("q", "train"), "its meeting is")
    places = placed(lines, gaps)
    meeting = {place for place, held in places.items() if met(held)}
    own: dict[Clock, list[Line]] = {}
    for line in sorted(
        [line for line in lines if whole(line.get("train")) and not silent(line)],
        key=lambda line: line["round"],
    ):
        own.setdefault((line["site"], line["train"]), []).append(line)
    owned = sorted(own.items())
    clocks = {
        at: (len([e for e in held if (e["round"], e["site"]) in meeting]), clicks.tallied(held))
        for at, held in owned
    }
    apart = places.keys() - meeting  # the places read and no meeting, once
    astray = [(at, e) for at, held in owned for e in held if (e["round"], e["site"]) in apart]
    if astray:
        (site, train), line = astray[0]
        cause = f"the clock at site {site}, train {train} clicks at round {line['round']} in no meeting: {len({at for at, _ in astray})} of {len(clocks)} clocks click outside one"
        return measure.verdict("NOT SHOWN", f"{cause}; {lacks}" if lacks else cause, clocks=clocks)
    if lacks:
        return measure.verdict("NOT READ", lacks, clocks=clocks)
    labels = {t.get("index"): t.get("label") for t in record.header.get("trains", [])}
    nets: dict[int, list[int]] = {}
    for (_, train), (_, tally) in clocks.items():
        nets.setdefault(train, []).append(tally.net)
    each = ", ".join(
        f"the {len(n)} of train {t} ({labels.get(t)}) net {spread(n)} each"
        for t, n in sorted(nets.items())
    )
    cause = f"every click line stands in a meeting: {len(clocks)} clocks of {spread([k for k, _ in clocks.values()])} meetings each, {ORDER}; {each}"
    return measure.verdict("SHOWN", cause, clocks=clocks)


def laid(record: Record, sides: list[int], size: int) -> tuple[set[int], str]:
    """The sites the setting file lays, read by its place, the last of the header's files in the run's order (universe, piece, setting), a gear there with a count or a tooth not 0 (the runner's six whole numbers: train, component, site, the counts a and b, the tooth r), each gear's site on the board; or why it is not read."""
    files = [f for f in record.header.get("files", []) if isinstance(f, dict)]
    if not files:
        return set(), "the header holds no files"
    text = files[-1].get("text")
    try:
        held = json.loads(text) if isinstance(text, str) else None
    except ValueError, RecursionError:
        held = None
    if not isinstance(held, dict):
        return set(), "the setting file is no JSON object"
    gears = held.get("gears")
    if not (isinstance(gears, list) and gears):
        return set(), "the setting file holds no gears"
    sites: set[int] = set()
    for n, gear in enumerate(gears, start=1):
        match gear:
            case [_, _, int() as site, int() as a, int() as b, int() as r] if all(
                map(whole, (site, a, b, r))
            ):
                if not 0 <= site < size:
                    return (
                        set(),
                        f"the setting's gear {n} names site {site}, off the board of sides {sides}",
                    )
                sites |= {site} if a or b or r else set()
            case _:
                return set(), f"the setting's gear {n} names no site and counts"
    return sites, ""


def cone(record: Record) -> Verdict:
    """The cone check by click (D8), on the click lines and measure.past: every line's event (t, x) inside the lay's cone, past((0, y), (t, x)) for a site y the setting lays, read on the lines that could stand outside it, a line at no laid site and before the lay's reach in rounds (the most Meshes from a site to its nearest laid site), NOT READ where none could; the lay's cone alone, since measure.meshes obeys the triangle inequality (a line inside an earlier click's cone, that click inside the lay's, is inside the lay's, and the first line outside the lay's cone is outside every earlier click's) and the clicks as built report a passing and push nothing back into the gears, so the lay is the one cause on the board and its cone the whole causal past."""
    lines = clicks.listed(record)
    if not lines:
        return measure.verdict(ABSENT, NO_LINE)
    sides = record.header.get("sides")
    if not (isinstance(sides, list) and sides and all(whole(s) and s >= 1 for s in sides)):
        return measure.verdict("NOT READ", "the header's sides make no board")
    _, size = records.board(record.header)
    lay, unread = laid(record, sides, size)
    if unread:
        return measure.verdict("NOT READ", unread)
    reach = max(min(measure.meshes(sides, y, x) for y in lay) for x in range(size)) if lay else 0
    events = [(line["round"], line["site"]) for line in lines]
    could = [(t, x) for t, x in events if x not in lay and (t < reach or not lay)]
    readings = {"lines": len(lines), "laid": len(lay), "could": len(could)}
    if not could and len(lay) == size:
        cause = f"the lay's cone covers the board's {size} sites from round 0, before the first click line at round {events[0][0]}: no line could stand outside it"
        return measure.verdict("NOT READ", cause, **readings)
    if not could:
        cause = f"every click line stands at a laid site ({len(lay)} of the board's {size}) or at or past round {reach}, the lay's reach, the most Meshes from a site to its nearest laid site: no line could stand outside the lay's cone"
        return measure.verdict("NOT READ", cause, **readings)
    outside = [e for e in could if not any(measure.past(sides, (0, y), e) for y in lay)]
    if outside:
        (round_, site), far = outside[0], len(outside)
        cause = f"the click line at round {round_}, site {site} stands outside the lay's cone: {far} of the {len(could)} lines that could stand outside it, of {len(lines)} lines"
        return measure.verdict("NOT SHOWN", cause, **readings)
    cause = f"every click line stands inside the lay's cone, one Mesh a round from the {len(lay)} sites laid: {len(could)} of the {len(could)} lines that could stand outside it, of {len(lines)} lines"
    return measure.verdict("SHOWN", cause, **readings)


def shadow(record: Record) -> dict[str, Verdict]:
    """The click world's two readings on the record, the books and the cone, each its verdict, NO CLICK in each on a record that holds no click line."""
    return {BOOKS: books(record), CONE: cone(record)}


def click_board(record: Record) -> dict[str, Verdict]:
    """The click board read as the clocks' meetings (the owner's word of 00:3x UTC): the meetings and each clock's line of meetings, each its verdict, NO CLICK in each on a record that holds no click line."""
    return {MEETINGS: meetings(record), LINES: clock_lines(record)}

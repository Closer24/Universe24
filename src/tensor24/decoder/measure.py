"""Clock: a duration is a clock's own count between two of its clicks; two clocks that part and meet again count apart by their paths; a click's past is what could reach it, one Mesh a round.
Algebra: differences of a clock's teeth; the Meshes between two sites, the shorter way round each side, summed; shares compared by cross products.
Board: the clicks with their clocks, faces and lays, the settings with their frames, and the board's sides; the rounds give order alone.
Clicks: D6 proper time, D7 no duration from rounds, D8 no signal outside the cone, and the twins: shown, not shown or not read, with its cause.
"""

# The rules (the owner's text to the Boss, space and time the shadows of one four-dimensional spacetime, and his word
# "This is also important for the decoder, no?"; the Boss's D6 to D8, entered at 6499774896; ANIMATE-SCHEMA-1.2,
# part 6). The round is order alone: which event stands before which, and the cone, one Mesh a round, the Meshes
# between two sites being the shorter way round each of the board's sides, summed (the board wraps by Rule3 at each
# side, its sites numbered z the fastest). No reading here takes rounds as a duration (D7): a duration is a clock's
# own count, and a reading that asks one between two events of no common clock is refused by name.
#
# A clock is named on each of its whole clicks by "clock", the round and site of the lay that made it, and its face
# reads its own count there in "tooth", the teeth from that lay, before and after the click (K4). Proper time (D6):
# between two of a clock's clicks, its own count, the later click's tooth after less the earlier's; a duration asked
# between two events of no common clock is refused by name (D7). Its second reading, by signals, is light's, owed.
#
# The twin reading: two clocks that meet twice, a click of each at one round and site and again at a later meeting;
# each one's own count between the meetings, and its path, the sites of its clicks between (a clock with no click
# between has no path on the record). It fails where the counts are equal and the paths differ: the board's tick
# showing in the clicks. Whether a difference is the lapse's and the motion's alone reads the metric along each path,
# which the record does not hold.
#
# The cone check by click (D8): a click is a take (a whole click naming its lay, G5, its outcome the line written) or
# a refusal (a Books line naming its lay, by the slot rule (b)); a setting is a split click naming its lay among its
# members, with the frames it draws among ("axes") and the one drawn. The lays laid at one site are trials alike;
# each click and setting stands at its place, its round after its lay's round and its site. For every click's place
# and every setting's place outside its past cone, each trial's outcome there (a click's, or none) is binned by the
# frame its setting drew there. The record signals where one outcome's share differs between two frames, the pair
# named: shares are compared exactly, by cross products (the records built in memory hold exact laws; a spread for a
# record of the act's draws is the Boss's to rule). The setting of a click's own part stands in its past cone, so no
# click is binned by its own frame.

import json
from typing import Any

from tensor24.algebra.carry import carry
from tensor24.decoder.records import Record, whole

Line = dict[str, Any]
Event = tuple[int, int]  # a round and a site
Place = tuple[int, int]  # a round after the lay's round, and a site
NONE = ("none",)  # a trial's outcome at a place where its lay clicked not
REFUSED = ("refused",)
NO_READING = "compares board ticks, no reading"


def verdict(kind: str, cause: str, **readings: Any) -> dict[str, Any]:
    """A verdict of a rule, with its cause and the readings it stands on."""
    return {"kind": kind, "cause": cause, **readings}


def meshes(sides: list[int], a: int, b: int) -> int:
    """The Meshes between two sites: on each side the shorter way round, summed (z the fastest, x the slowest)."""
    # a site's place on a side is its carry's remainder by the side; the way up, their difference's remainder
    total = 0
    for side in reversed(sides):
        a, here = carry(a, side, 0)
        b, there = carry(b, side, 0)
        _, up = carry(there - here, side, 0)
        total += up if up <= side - up else side - up
    return total


def past(sides: list[int], early: Event, late: Event) -> bool:
    """Whether the early event stands in the late one's past cone: the rounds between at least the Meshes between."""
    return late[0] - early[0] >= meshes(sides, early[1], late[1])


def pair(value: Any) -> Event | None:
    """A row of two whole numbers, or None."""
    match value:
        case [int() as one, int() as other] if whole(one) and whole(other):
            return one, other
    return None


def outcome(line: Line) -> tuple[Any, ...] | None:
    """A click's outcome: the line a take wrote, in its axis form, or refused; None where a take holds no line."""
    if line["kind"] == "books":
        return REFUSED
    written = line.get("written")
    if not isinstance(written, dict):
        return None
    rho, spin = written.get("rho"), written.get("spin")
    if whole(rho) and isinstance(spin, list) and all(whole(s) for s in spin):
        return ("taken", rho, *spin)
    return None


def settings(record: Record) -> tuple[dict[Event, dict[Place, tuple[Any, ...]]], str]:
    """Each lay's settings, the frame drawn at each place, from the split clicks with axes; or the first misread."""
    found: dict[Event, dict[Place, tuple[Any, ...]]] = {}
    for line in record.of("split"):
        axes, members, drawn = line.get("axes"), line.get("members"), line.get("drawn")
        if axes is None:
            continue
        if not (isinstance(axes, list) and whole(drawn) and 0 <= drawn < len(axes)):
            return (
                {},
                f"the setting at round {line['round']}, site {line['site']} draws no frame of its axes",
            )
        if not (isinstance(members, list) and members and all(isinstance(m, list) for m in members)):
            return {}, f"the setting at round {line['round']}, site {line['site']} names no lay"
        for member in members:
            match member:
                case [int() as round_, int() as site, _] if whole(round_) and whole(site):
                    lay = (round_, site)
                case _:
                    return {}, f"the setting at round {line['round']}, site {line['site']} names no lay"
            place = (line["round"] - lay[0], line["site"])
            found.setdefault(lay, {})[place] = (json.dumps(axes[drawn], sort_keys=True),)
    return found, ""


def clicks(record: Record) -> tuple[dict[Event, dict[Place, tuple[Any, ...]]], str]:
    """Each lay's clicks, the outcome at each place: its takes and its refusals; or the first misread."""
    found: dict[Event, dict[Place, tuple[Any, ...]]] = {}
    for line in record.of("whole") + record.of("books"):
        if "birth" not in line:
            continue
        lay, made = pair(line["birth"]), outcome(line)
        if lay is None or made is None:
            return (
                {},
                f"the click at round {line['round']}, site {line['site']} names no lay or writes no line",
            )
        found.setdefault(lay, {})[(line["round"] - lay[0], line["site"])] = made
    return found, ""


def tallies(
    sides: list[int],
    set_by: dict[Event, dict[Place, tuple[Any, ...]]],
    clicked: dict[Event, dict[Place, Any]],
) -> dict[tuple[int, Place, Place], dict[tuple[Any, ...], dict[tuple[Any, ...], int]]]:
    """Per lays' site, click's place and setting's place outside its past cone: per frame, each outcome's count."""
    counts: dict[tuple[int, Place, Place], dict[tuple[Any, ...], dict[tuple[Any, ...], int]]] = {}
    sites = {lay[1] for lay in set_by}
    for site in sites:
        lays = [lay for lay in set_by if lay[1] == site]
        heres = {place for lay in lays for place in clicked.get(lay, {})}
        theres = {place for lay in lays for place in set_by[lay]}
        for here in heres:
            for there in theres:
                if past(sides, there, here):
                    continue
                table = counts.setdefault((site, here, there), {})
                for lay in lays:
                    if there in set_by[lay]:
                        frame = table.setdefault(set_by[lay][there], {})
                        made = clicked.get(lay, {}).get(here, NONE)
                        frame[made] = frame.get(made, 0) + 1
    return counts


def signal(table: dict[tuple[Any, ...], dict[tuple[Any, ...], int]]) -> tuple[Any, ...] | None:
    """The first outcome whose share differs between two frames, with the two frames and their counts; or None."""
    frames = sorted(table)
    made = sorted({m for counts in table.values() for m in counts})
    for one, other in zip(frames, frames[1:], strict=False):
        n1, n2 = sum(table[one].values()), sum(table[other].values())
        for m in made:
            k1, k2 = table[one].get(m, 0), table[other].get(m, 0)
            if k1 * n2 != k2 * n1:
                return m, one, k1, n1, other, k2, n2
    return None


def cone_check(record: Record) -> dict[str, Any]:
    """The cone check by click: SHOWN, or NOT SHOWN with the first pair that differs, or NOT READ with its cause."""
    sides = record.header.get("sides")
    if not (isinstance(sides, list) and sides and all(whole(s) and s >= 1 for s in sides)):
        return verdict("NOT READ", "the header's sides make no board")
    set_by, unset = settings(record)
    clicked, unclicked = clicks(record)
    if unset or unclicked:
        return verdict("NOT READ", unset or unclicked)
    if not clicked:
        return verdict("NOT READ", "no click names its lay (G5)")
    if not set_by:
        return verdict("NOT READ", "no setting names its lay")
    counts = tallies(sides, set_by, clicked)
    compared = {key: table for key, table in counts.items() if len(table) > 1}
    if not compared:
        return verdict("NOT READ", "no setting outside a click's past cone drew two frames")
    for (site, here, there), table in sorted(compared.items(), key=repr):
        found = signal(table)
        if found is not None:
            m, one, k1, n1, other, k2, n2 = found
            cause = (
                f"the lays at site {site}: the outcome {m} at round +{here[0]}, site {here[1]} reads {k1} of {n1} "
                f"at the frame {one[0]} and {k2} of {n2} at the frame {other[0]} of the setting at round "
                f"+{there[0]}, site {there[1]}, outside its past cone"
            )
            return verdict("NOT SHOWN", cause, pairs=len(compared))
    cause = (
        "every click's law is the same at every frame drawn outside its past cone "
        f"(the places of a click and a setting compared: {len(compared)}; the lays: {len(set_by)})"
    )
    return verdict("SHOWN", cause, pairs=len(compared))


def faces(record: Record) -> tuple[dict[Event, list[Line]], str]:
    """Each clock's whole clicks in order, by the lay that made it; or the first click whose clock or face is unread."""
    found: dict[Event, list[Line]] = {}
    for line in record.of("whole"):
        if "clock" not in line:
            continue
        lay, tooth = pair(line["clock"]), pair(line.get("tooth"))
        if lay is None or tooth is None or not whole(line.get("count")):
            return (
                {},
                f"the clock's click at round {line['round']}, site {line['site']} reads no clock, face or count",
            )
        found.setdefault(lay, []).append(line)
    return found, ""


def counted(early: Line, late: Line) -> int:
    """A clock's own count between two of its clicks: the later's tooth after less the earlier's."""
    return int(late["tooth"][1]) - int(early["tooth"][1])


def elapsed(clocked: dict[Event, list[Line]], clock: Event, early: Event, late: Event) -> int | str:
    """A duration: one clock's own count between two of its clicks, or the refusal by name for other events (D7)."""
    at = {(c["round"], c["site"]): c for c in clocked.get(clock, [])}
    if early not in at or late not in at:
        return NO_READING
    return counted(at[early], at[late])


def twins(record: Record) -> dict[str, Any]:
    """The twin reading: NOT SHOWN where two clocks count alike by two paths, SHOWN where all count apart, NOT READ."""
    clocked, unread = faces(record)
    if unread:
        return verdict("NOT READ", unread)
    names = sorted(clocked)
    met = 0
    for n, one in enumerate(names):
        for other in names[n + 1 :]:
            at_one = [(c["round"], c["site"]) for c in clocked[one]]
            meetings = sorted(set(at_one) & {(c["round"], c["site"]) for c in clocked[other]})
            for first, last in zip(meetings, meetings[1:], strict=False):
                paths = [
                    sorted({c["site"] for c in clocked[clock] if first[0] < c["round"] < last[0]})
                    for clock in (one, other)
                ]
                if not (paths[0] and paths[1]) or paths[0] == paths[1]:
                    continue
                met += 1
                own = [elapsed(clocked, clock, first, last) for clock in (one, other)]
                if own[0] == own[1]:
                    cause = (
                        f"the clocks laid at {list(one)} and {list(other)} count {own[0]} each between their meetings "
                        f"at rounds {first[0]} and {last[0]}, their paths {paths[0]} and {paths[1]}: the board's tick"
                    )
                    return verdict("NOT SHOWN", cause, pairs=met)
    if not met:
        return verdict("NOT READ", "no two clocks meet twice by two paths")
    return verdict(
        "SHOWN",
        f"every two clocks that meet twice by two paths count apart (compared: {met})",
        pairs=met,
    )

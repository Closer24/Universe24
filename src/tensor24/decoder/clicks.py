"""Clock: the click lines listed and counted, nothing read into them: the basic part, on which the click world's readings (shadow.py) stand.
Algebra: whole counts and sums: per train and per Node-clock its lines, what it gave (its q below 0, negated), what it took (its q above 0) and the net, their difference; at each round and Node-clock with a line the sum of q over the trains, and the places where that sum is not 0 counted.
Board: the click lines as the record holds them, in the schema's order (round, site, train), each with its q, the sum of its clock's carries over its edge sides in its site and across a Mesh, a clock joined to a side that carried listed at q 0.
Clicks: the list and the counts alone, no verdict: every reading of the click world is shadow.py's.
"""

from typing import Any, NamedTuple

from tensor24.decoder.records import Record, whole

Line = dict[str, Any]
Place = tuple[int, int]  # a round and a Node-clock


class Tally(NamedTuple):
    """The counts of some click lines: how many, what they gave (the q below 0, negated), what they took (the q above 0) and the net, the sum of q."""

    lines: int
    given: int
    taken: int
    net: int


class Counted(NamedTuple):
    """The basic part of a record's click lines: the lines listed, the counts per train and per Node-clock, the places (a round and a Node-clock) with a line, and those among them where the sum of q over the trains is not 0."""

    lines: list[Line]
    trains: dict[int, Tally]
    sites: dict[int, Tally]
    places: int
    nonzero: int


def listed(record: Record) -> list[Line]:
    """The record's click lines, in the schema's order (round, site, train)."""
    return record.of("click")


def tallied(lines: list[Line]) -> Tally:
    """The counts over some click lines; a line whose q is no whole number counts as a line and nothing else."""
    held = [line["q"] for line in lines if whole(line.get("q"))]
    given = sum(-q for q in held if q < 0)
    taken = sum(q for q in held if q > 0)
    return Tally(len(lines), given, taken, taken - given)


def by(lines: list[Line], key: str) -> dict[int, Tally]:
    """The counts per value of one field of a click line, its train or its site, in the values' order; a line with no whole value there stands under none."""
    held: dict[int, list[Line]] = {}
    for line in [line for line in lines if whole(line.get(key))]:  # one pass, the lines in their order
        held.setdefault(line[key], []).append(line)
    return {at: tallied(held[at]) for at in sorted(held)}


def summed(lines: list[Line]) -> dict[Place, int]:
    """At each round and Node-clock with a click line, the sum of q over the trains."""
    found: dict[Place, int] = {}
    for line in lines:
        if whole(line.get("q")):
            place = (line["round"], line["site"])
            found[place] = found.get(place, 0) + line["q"]
    return found


def counted(record: Record) -> Counted:
    """The basic part on one record: its click lines listed and counted, no verdict."""
    lines = listed(record)
    sums = summed(lines)
    nonzero = [place for place, total in sums.items() if total != 0]
    return Counted(lines, by(lines, "train"), by(lines, "site"), len(sums), len(nonzero))

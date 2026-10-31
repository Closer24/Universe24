"""The measurement's rules on the record: a verdict with its cause and its readings, and the cone, one Mesh a round, the Meshes between two sites the shorter way round each of the board's sides."""

# The rules (the owner's text to the Boss, space and time the shadows of one four-dimensional spacetime, and his word
# "This is also important for the decoder, no?"; the Boss's D6 to D8, entered at 6499774896; ANIMATE-SCHEMA-1.2,
# part 6). The round is order alone: which event stands before which, and the cone, one Mesh a round, the Meshes
# between two sites being the shorter way round each of the board's sides, summed (the board wraps by Rule3 at each
# side, its sites numbered z the fastest). No reading here takes rounds as a duration (D7): a duration is a clock's
# own count. The click world reads D6 to D8 on the click lines (decoder/shadow.py), its verdicts and its cone from here.

from typing import Any

from tensor24.algebra.carry import carry

Event = tuple[int, int]  # a round and a site


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

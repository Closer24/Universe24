"""The messages of a world (ALGEBRA.md #the-generator, the message lay): laid records of families of quanta, packets and no bodies, each declared by its family, the axis it travels along, its wave number as a fraction of pi per Link, its amplitude and its envelope (per axis a flat top and the half-width of the raised cosine beyond it), its levels the generator's in the mode file beside the world."""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.loader.derived import FamilyRule
from event_universe.loader.keys import AXES, Node, integer, keyed, span_of
from event_universe.loader.mode import entry_of, levels_of, mode_entries

MESSAGE_KEYS = ("family", "along", "wave", "amplitude", "top", "edge")


@dataclass(frozen=True)
class MessageRow:
    """A laid record as declared, a packet of a family of quanta and no body: its family, the axis it travels along, its wave number as a fraction of pi per Link [p, q], its amplitude (the level at the envelope's top), per axis the Nodes [first, last] of its flat top and the half-width of the raised cosine beyond them, and its two level pairs from the mode file over the whole GameBoard in x-major order (the second pair 0, a real packet)."""

    family: int
    along: int
    wave: tuple[int, int]
    amplitude: int
    top: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]
    edge: tuple[int, int, int]
    now: tuple[int, ...]
    before: tuple[int, ...]
    im_now: tuple[int, ...]
    im_before: tuple[int, ...]


def messages_of(
    value: object,
    mode: object,
    digest: str,
    families: tuple[FamilyRule, ...],
    shape: Node,
    bound: int,
    beyond: tuple[Node, ...],
) -> tuple[MessageRow, ...]:
    """The messages: each its family (a family of quanta), the axis it travels along, its wave number [p, q] (k = pi p / q per Link, p from 0 through q), its amplitude from 1 within the amplitude bound A, per axis its flat top [first, last] and the half-width of the raised cosine beyond it (0: none), and its levels from the mode file; a message with no mode entry is refused by name."""
    names = {family.name: index for index, family in enumerate(families)}
    if not isinstance(value, list):
        raise ValueError("messages must be a list of laid records")
    entries = mode_entries(mode, digest, "messages") if value else []
    found = []
    for number, entry in enumerate(value):
        label = f"messages[{number}]"
        message = keyed(entry, label, MESSAGE_KEYS, MESSAGE_KEYS)
        family = names.get(message["family"])
        if family is None or not families[family].quanta:
            raise ValueError(f"{label}.family must name a family of quanta, got {message['family']!r}")
        if message["along"] not in AXES:
            raise ValueError(f"{label}.along is one of {list(AXES)}, got {message['along']!r}")
        wave = message["wave"]
        if not isinstance(wave, list) or len(wave) != 2:
            raise ValueError(f"{label}.wave must be [p, q], the wave number pi p / q per Link")
        halves = integer(wave[1], f"{label}.wave's q", 1)
        turns = integer(wave[0], f"{label}.wave's p", 0, halves)
        top = keyed(message["top"], f"{label}.top", AXES, AXES)
        edge = keyed(message["edge"], f"{label}.edge", AXES, AXES)
        spans = tuple(
            span_of(top[name], f"{label}.top.{name}", shape[axis]) for axis, name in enumerate(AXES)
        )
        widths = tuple(integer(edge[name], f"{label}.edge.{name}", 0) for name in AXES)
        levels = levels_of(
            entry_of(entries, number, label),
            f"the mode file's messages[{number}]",
            families[family],
            shape,
            bound,
            beyond,
        )
        found.append(
            MessageRow(
                family,
                AXES.index(message["along"]),
                (turns, halves),
                integer(message["amplitude"], f"{label}.amplitude", 1, bound),
                (spans[0], spans[1], spans[2]),
                (widths[0], widths[1], widths[2]),
                *levels,
            )
        )
    return tuple(found)

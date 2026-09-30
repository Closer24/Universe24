"""The messages of a world (ALGEBRA.md #the-generator, the message lay): laid records of families of quanta, packets and no bodies, each declared by its family, the axis it travels along, its wave number as a fraction of pi per Link, its amplitude and its envelope (per axis a flat top and the half-width of the raised cosine beyond it), its levels the generator's in the mode file beside the world."""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.loader.derived import FamilyRule
from event_universe.loader.keys import AXES, Node, integer, keyed, node_of, span_of
from event_universe.loader.mode import Levels, entry_of, levels_of, mode_entries

MESSAGE_KEYS = ("family", "along", "wave", "amplitude", "top", "edge", "phase", "whole")
MESSAGE_REQUIRED = ("family", "along", "wave", "amplitude", "top", "edge")


@dataclass(frozen=True)
class MessageRow:
    """A laid record as declared, a packet of a family of quanta and no body: its family, the axis it travels along, its wave number as a fraction of pi per Link [p, q] (p below 0: the packet travels toward the axis's lower side), its amplitude (the level at the envelope's top), per axis the Nodes [first, last] of its flat top and the half-width of the raised cosine beyond them, its phase as a fraction of the turn [r, s] ((0, 1) without the key), and its two level pairs from the mode file, each the nonzero Nodes' flat x-major indexes with their levels (the second pair 0, a real packet)."""

    family: int
    along: int
    wave: tuple[int, int]
    amplitude: int
    top: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]
    edge: tuple[int, int, int]
    phase: tuple[int, int]
    now: Levels
    before: Levels
    im_now: Levels
    im_before: Levels


def messages_of(
    value: object,
    mode: object,
    digest: str,
    families: tuple[FamilyRule, ...],
    shape: Node,
    bound: int,
    beyond: tuple[Node, ...],
) -> tuple[MessageRow, ...]:
    """The messages: each its family (a family of quanta), the axis it travels along, its wave number [p, q] (k = pi p / q per Link, p from -q through q, its sign the direction along the axis), its amplitude from 1 within the amplitude bound A, per axis its flat top [first, last] and the half-width of the raised cosine beyond it (0: none), optionally its phase [r, s] (the wave cos(k x + 2 pi r / s), r from 0 below s; the wave cos(k x) without the key), and its levels from the mode file; a message with no mode entry is refused by name; `whole`, a Node at which the message's count would be laid whole with its levels spread as they are, is refused by name, since no family's line lays a count whole today (the lay is the share's; the key waits for the light family's line)."""
    names = {family.name: index for index, family in enumerate(families)}
    if not isinstance(value, list):
        raise ValueError("messages must be a list of laid records")
    entries = mode_entries(mode, digest, "messages") if value else []
    found = []
    for number, entry in enumerate(value):
        label = f"messages[{number}]"
        message = keyed(entry, label, MESSAGE_KEYS, MESSAGE_REQUIRED)
        family = names.get(message["family"])
        if family is None or not families[family].quanta:
            raise ValueError(f"{label}.family must name a family of quanta, got {message['family']!r}")
        if "whole" in message:
            at = node_of(message["whole"], f"{label}.whole", shape, beyond)
            raise ValueError(
                f"{label}.whole names the Node {list(at)}: no line of the family {message['family']!r} lays "
                "its count whole at one Node today (the lay is the share's); the key waits for that line"
            )
        if message["along"] not in AXES:
            raise ValueError(f"{label}.along is one of {list(AXES)}, got {message['along']!r}")
        wave = message["wave"]
        if not isinstance(wave, list) or len(wave) != 2:
            raise ValueError(f"{label}.wave must be [p, q], the wave number pi p / q per Link")
        halves = integer(wave[1], f"{label}.wave's q", 1)
        turns = integer(wave[0], f"{label}.wave's p", -halves, halves)
        phase = message.get("phase", [0, 1])
        if not isinstance(phase, list) or len(phase) != 2:
            raise ValueError(f"{label}.phase must be [r, s], the phase 2 pi r / s")
        whole_turn = integer(phase[1], f"{label}.phase's s", 1)
        turned = integer(phase[0], f"{label}.phase's r", 0, whole_turn - 1)
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
                (turned, whole_turn),
                *levels,
            )
        )
    return tuple(found)

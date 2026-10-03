"""The messages of a world (ALGEBRA.md #the-generator, the message lay): laid records of families of quanta, packets and no bodies, each declared by its family, the axis it travels along, its wave number as a fraction of pi per Link, its amplitude and its envelope (per axis a flat top and the half-width of the raised cosine beyond it), its levels the generator's in the mode file beside the world; or a message laid whole at one Node by the count at a declared tick of the run (`WholeMessage`, `wholes_of`; ALGEBRA.md, The pulsed gate: the probe laid at a body's Node by the count at a declared tick; the two hands of 2026-10-03, #1572 comments 5967698811 and 5967783614), the world's protocol in time, no mode entry and no wave."""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.loader.derived import FamilyRule
from event_universe.loader.keys import AXES, Node, integer, keyed, node_of, span_of, weights_of
from event_universe.loader.mode import Levels, entry_of, levels_of, mode_entries

MESSAGE_KEYS: tuple[str, ...] = (
    "family",
    "along",
    "wave",
    "amplitude",
    "top",
    "edge",
    "phase",
    "transverse",
)
MESSAGE_KEYS += ("whole", "weights", "count", "tick")
MESSAGE_REQUIRED = ("family", "along", "wave", "amplitude", "top", "edge")
WHOLE_KEYS = (
    "family",
    "whole",
    "count",
    "tick",
)  # a message laid whole at one Node by the count at a tick of the run: its four keys, all required


@dataclass(frozen=True)
class MessageRow:
    """A laid record as declared, a packet of a family of quanta and no body (or a kick on a holder of the content, laid on the row's rest): its family, the axis it travels along, its wave number as a fraction of pi per Link [p, q] (p below 0: the packet travels toward the axis's lower side), its amplitude (the level at the envelope's top), per axis the Nodes [first, last] of its flat top and the half-width of the raised cosine beyond them, its phase as a fraction of the turn [r, s] ((0, 1) without the key), its wave number per axis across the beam as a fraction of pi per Link ((0, 1) where none; `transverse`), its two level pairs from the mode file, each the nonzero Nodes' flat x-major indexes with their levels (the second pair 0, a real packet), and the weight of the laid pair on each line of its record (`weights`, 1 on every line without the key; `keys.weights_of`)."""

    family: int
    along: int
    wave: tuple[int, int]
    amplitude: int
    top: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]
    edge: tuple[int, int, int]
    phase: tuple[int, int]
    transverse: tuple[tuple[int, int], tuple[int, int], tuple[int, int]]
    now: Levels
    before: Levels
    im_now: Levels
    im_before: Levels
    weights: tuple[int, ...] = ()


@dataclass(frozen=True)
class WholeMessage:
    """A message laid whole at one Node by the count at a declared tick of the run (the probe of the pulsed gate; the two hands of 2026-10-03, #1572 comments 5967698811 and 5967783614): its family (a family of quanta), the Node at the file's coordinates, the whole quanta laid (from 1) and the interval at whose end the engine lays them (from 1, within the run), by the one-Node lay by the count at the family's massless pair, A^2 = count T div 2 on its first line (`giving.laid_by_count`, the conversion's lay of a given quantum; `meeting.laid_whole`); the experimenter's lay in time, a declaration of the world's protocol and nothing of the engine's."""

    family: int
    at: Node
    count: int
    tick: int


def wholes_of(
    value: object, families: tuple[FamilyRule, ...], shape: Node, beyond: tuple[Node, ...], ticks: int
) -> tuple[WholeMessage, ...]:
    """The messages laid whole at a tick among the world's `messages`, the entries with the key `tick`: each its `family` (a family of quanta), `whole` (the Node, none beyond the board), `count` (from 1) and `tick` (from 1 to the run's `ticks`, the interval at whose end the lay is made), every other key refused by name (a packet laid at a tick is not built: a message with the generator's keys is laid at the start)."""
    if not isinstance(value, list):
        raise ValueError("messages must be a list of laid records")
    names = {family.name: index for index, family in enumerate(families)}
    found = []
    for number, entry in enumerate(value):
        if not (isinstance(entry, dict) and "tick" in entry):
            continue
        label = f"messages[{number}]"
        message = keyed(entry, label, WHOLE_KEYS, WHOLE_KEYS)
        family = names.get(message["family"])
        if family is None or not families[family].quanta:
            raise ValueError(
                f"{label}.family must name a family of quanta for a lay by the count, got {message['family']!r}"
            )
        at = node_of(message["whole"], f"{label}.whole", shape, beyond)
        count = integer(message["count"], f"{label}.count", 1)
        tick = integer(message["tick"], f"{label}.tick", 1, ticks)
        found.append(WholeMessage(family, at, count, tick))
    return tuple(found)


def messages_of(
    value: object,
    mode: object,
    digest: str,
    families: tuple[FamilyRule, ...],
    shape: Node,
    bound: int,
    beyond: tuple[Node, ...],
) -> tuple[MessageRow, ...]:
    """The messages: each its family (a family of quanta, or a holder of the content: a kick laid on the row's rest, the row's own travelling events with no count, the advisor's lay, #1563 comment 5916154126), the axis it travels along, its wave number [p, q] (k = pi p / q per Link, p from -q through q and not 0, refused by name at 0, its sign the direction along the axis), its amplitude from 1 within the amplitude bound A, per axis its flat top [first, last] and the half-width of the raised cosine beyond it (0: none), optionally its phase [r, s] (the wave cos(k x + 2 pi r / s), r from 0 below s; the wave cos(k x) without the key), optionally `transverse` {an axis across the beam: [r, s]}, a wave number pi r / s per Link on that axis (r from -s through s; the wave cos(k x + k_y y + ...), a packet leaving at an angle), optionally `weights`, the laid pair's weight per line of its record (`keys.weights_of`, a record of real lines': a record of three real lines laid at (a, b, c) over its lines), and its levels from the mode file; a message with no mode entry is refused by name; an entry with the key `tick` is a message laid whole at one Node by the count at that tick (`wholes_of`, `WholeMessage`) and takes no mode entry, so the mode file's entries number the start's messages alone; `whole` or `count` without `tick` is refused by name (a lay whole at the start is not built: the start lays the generator's levels)."""
    names = {family.name: index for index, family in enumerate(families)}
    if not isinstance(value, list):
        raise ValueError("messages must be a list of laid records")
    started = [entry for entry in value if not (isinstance(entry, dict) and "tick" in entry)]
    for number, entry in enumerate(value):
        if isinstance(entry, dict) and "tick" not in entry and ("whole" in entry or "count" in entry):
            raise ValueError(
                f"messages[{number}] holds `whole` or `count` without `tick`: a message is laid whole at one Node "
                "by the count at a declared tick of the run, and at the start the generator's levels are laid"
            )
    entries = mode_entries(mode, digest, "messages") if started else []
    found, placed = [], 0  # the mode file's entries number the start's messages alone
    for number, entry in enumerate(value):
        label = f"messages[{number}]"
        if isinstance(entry, dict) and "tick" in entry:  # laid whole at a tick of the run: `wholes_of`
            continue
        message = keyed(entry, label, MESSAGE_KEYS, MESSAGE_REQUIRED)
        family = names.get(message["family"])
        if family is None:
            raise ValueError(
                f"{label}.family must name a family of the universe, got {message['family']!r}"
            )
        if message["along"] not in AXES:
            raise ValueError(f"{label}.along is one of {list(AXES)}, got {message['along']!r}")
        wave = message["wave"]
        if not isinstance(wave, list) or len(wave) != 2:
            raise ValueError(f"{label}.wave must be [p, q], the wave number pi p / q per Link")
        halves = integer(wave[1], f"{label}.wave's q", 1)
        turns = integer(wave[0], f"{label}.wave's p", -halves, halves)
        if turns == 0:
            raise ValueError(
                f"{label}.wave's p is 0: a message has a wave number pi p / q per Link, p not 0, its sign "
                "the direction along the axis (a node_reader's region is read against it)"
            )
        phase = message.get("phase", [0, 1])
        if not isinstance(phase, list) or len(phase) != 2:
            raise ValueError(f"{label}.phase must be [r, s], the phase 2 pi r / s")
        whole_turn = integer(phase[1], f"{label}.phase's s", 1)
        turned = integer(phase[0], f"{label}.phase's r", 0, whole_turn - 1)
        crossing = tuple(name for name in AXES if name != message["along"])
        sideways = keyed(message.get("transverse", {}), f"{label}.transverse", crossing, ())
        across = []
        for name in AXES:
            given = sideways.get(name, [0, 1])
            if not isinstance(given, list) or len(given) != 2:
                raise ValueError(
                    f"{label}.transverse.{name} must be [r, s], the wave number pi r / s per Link"
                )
            bottom = integer(given[1], f"{label}.transverse.{name}'s s", 1)
            across.append((integer(given[0], f"{label}.transverse.{name}'s r", -bottom, bottom), bottom))
        top = keyed(message["top"], f"{label}.top", AXES, AXES)
        edge = keyed(message["edge"], f"{label}.edge", AXES, AXES)
        spans = tuple(
            span_of(top[name], f"{label}.top.{name}", shape[axis]) for axis, name in enumerate(AXES)
        )
        widths = tuple(integer(edge[name], f"{label}.edge.{name}", 0) for name in AXES)
        levels = levels_of(
            entry_of(entries, placed, label),
            f"the mode file's messages[{placed}]",
            families[family],
            shape,
            bound,
            beyond,
        )
        placed += 1
        found.append(
            MessageRow(
                family,
                AXES.index(message["along"]),
                (turns, halves),
                integer(message["amplitude"], f"{label}.amplitude", 1, bound),
                (spans[0], spans[1], spans[2]),
                (widths[0], widths[1], widths[2]),
                (turned, whole_turn),
                (across[0], across[1], across[2]),
                *levels,
                weights_of(
                    message.get("weights"),
                    f"{label}.weights",
                    families[family].laid,
                    families[family].plane,
                ),
            )
        )
    return tuple(found)

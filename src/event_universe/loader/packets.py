"""The packets of a world (ALGEBRA.md #the-generator, the packet lay): laid records of families of quanta, packets and no bodies, each declared by its family, the axis it travels along, its wave number as a fraction of pi per Link, its amplitude and its envelope (per axis a flat top and the half-width of the raised cosine beyond it), its levels the generator's in the mode file beside the world; or a packet laid whole at one Node by the count at a declared interval of the run (`WholePacket`, `wholes_of`; ALGEBRA.md, The pulsed gate: the probe laid at a body's Node by the count at a declared interval; the two hands), the world's protocol in time, no mode entry and no wave."""

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
MESSAGE_KEYS += ("whole", "weights", "count", "interval")
MESSAGE_REQUIRED = ("family", "along", "wave", "amplitude", "top", "edge", "phase")
WHOLE_KEYS = (
    "family",
    "whole",
    "count",
    "interval",
)  # a packet laid whole at one Node by the count at an interval of the run: its four keys, all required


@dataclass(frozen=True)
class PacketRow:
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
    second_now: Levels
    second_before: Levels
    weights: tuple[int, ...] = ()


@dataclass(frozen=True)
class WholePacket:
    """A packet laid whole at one Node by the count at a declared interval of the run (the probe of the pulsed gate; the two hands): its family (a family of quanta), the Node at the file's coordinates, the whole quanta laid (from 1) and the interval at whose end the engine lays them (from 1, within the run), by the one-Node lay by the count at the family's massless pair, A^2 = count T div 2 on its first line (`emission.laid_by_count`, the conversion's lay of a emitted quantum; `meeting.laid_whole`); the experimenter's lay in time, a declaration of the world's protocol and nothing of the engine's."""

    family: int
    at: Node
    count: int
    interval: int


def wholes_of(
    value: object,
    families: tuple[FamilyRule, ...],
    shape: Node,
    beyond: tuple[Node, ...],
    intervals: int,
) -> tuple[WholePacket, ...]:
    """The packets laid whole at an interval among the world's `packets`, the entries with the key `interval`: each its `family` (a family of quanta), `whole` (the Node, none beyond the board), `count` (from 1) and `interval` (from 1 to the run's `intervals`, the interval at whose end the lay is made), every other key refused by name (a packet laid at an interval is not built: a packet with the generator's keys is laid at the start)."""
    if not isinstance(value, list):
        raise ValueError("packets must be a list of laid records")
    names = {family.name: index for index, family in enumerate(families)}
    found = []
    for number, entry in enumerate(value):
        if not (isinstance(entry, dict) and "interval" in entry):
            continue
        label = f"packets[{number}]"
        packet = keyed(entry, label, WHOLE_KEYS, WHOLE_KEYS)
        family = names.get(packet["family"])
        if family is None or not families[family].quanta:
            raise ValueError(
                f"{label}.family must name a family of quanta for a lay by the count, got {packet['family']!r}"
            )
        at = node_of(packet["whole"], f"{label}.whole", shape, beyond)
        count = integer(packet["count"], f"{label}.count", 1)
        interval = integer(packet["interval"], f"{label}.interval", 1, intervals)
        found.append(WholePacket(family, at, count, interval))
    return tuple(found)


def packets_of(
    value: object,
    mode: object,
    digest: str,
    families: tuple[FamilyRule, ...],
    shape: Node,
    bound: int,
    beyond: tuple[Node, ...],
) -> tuple[PacketRow, ...]:
    """The packets: each its family (a family of quanta, or a holder of the content: a kick laid on the row's rest, the row's own travelling events with no count, the advisor's lay), the axis it travels along, its wave number [p, q] (k = pi p / q per Link, p from -q through q and not 0, refused by name at 0, its sign the direction along the axis), its amplitude from 1 within the amplitude bound A, per axis its flat top [first, last] and the half-width of the raised cosine beyond it (0: none), optionally its phase [r, s] (the wave cos(k x + 2 pi r / s), r from 0 below s; the wave cos(k x) without the key), optionally `transverse` {an axis across the beam: [r, s]}, a wave number pi r / s per Link on that axis (r from -s through s; the wave cos(k x + k_y y + ...), a packet leaving at an angle), optionally `weights`, the laid pair's weight per line of its record (`keys.weights_of`, a record of real lines': a record of three real lines laid at (a, b, c) over its lines), and its levels from the mode file; a packet with no mode entry is refused by name; an entry with the key `interval` is a packet laid whole at one Node by the count at that interval (`wholes_of`, `WholePacket`) and takes no mode entry, so the mode file's entries number the start's packets alone; `whole` or `count` without `interval` is refused by name (a lay whole at the start is not built: the start lays the generator's levels)."""
    names = {family.name: index for index, family in enumerate(families)}
    if not isinstance(value, list):
        raise ValueError("packets must be a list of laid records")
    started = [entry for entry in value if not (isinstance(entry, dict) and "interval" in entry)]
    for number, entry in enumerate(value):
        if (
            isinstance(entry, dict)
            and "interval" not in entry
            and ("whole" in entry or "count" in entry)
        ):
            raise ValueError(
                f"packets[{number}] holds `whole` or `count` without `interval`: a packet is laid whole at one Node "
                "by the count at a declared interval of the run, and at the start the generator's levels are laid"
            )
    entries = mode_entries(mode, digest, "packets") if started else []
    found, placed = [], 0  # the mode file's entries number the start's packets alone
    for number, entry in enumerate(value):
        label = f"packets[{number}]"
        if (
            isinstance(entry, dict) and "interval" in entry
        ):  # laid whole at an interval of the run: `wholes_of`
            continue
        packet = keyed(entry, label, MESSAGE_KEYS, MESSAGE_REQUIRED)
        family = names.get(packet["family"])
        if family is None:
            raise ValueError(
                f"{label}.family must name a family of the universe, got {packet['family']!r}"
            )
        if packet["along"] not in AXES:
            raise ValueError(f"{label}.along is one of {list(AXES)}, got {packet['along']!r}")
        wave = packet["wave"]
        if not isinstance(wave, list) or len(wave) != 2:
            raise ValueError(f"{label}.wave must be [p, q], the wave number pi p / q per Link")
        halves = integer(wave[1], f"{label}.wave's q", 1)
        turns = integer(wave[0], f"{label}.wave's p", -halves, halves)
        if turns == 0:
            raise ValueError(
                f"{label}.wave's p is 0: a packet has a wave number pi p / q per Link, p not 0, its sign "
                "the direction along the axis (a node_reader's region is read against it)"
            )
        phase = packet["phase"]  # required: the file states its phase, [0, 1] for none
        if not isinstance(phase, list) or len(phase) != 2:
            raise ValueError(f"{label}.phase must be [r, s], the phase 2 pi r / s")
        whole_turn = integer(phase[1], f"{label}.phase's s", 1)
        turned = integer(phase[0], f"{label}.phase's r", 0, whole_turn - 1)
        crossing = tuple(name for name in AXES if name != packet["along"])
        sideways = keyed(packet.get("transverse", {}), f"{label}.transverse", crossing, ())
        across = []
        for name in AXES:
            given = sideways.get(name, [0, 1])
            if not isinstance(given, list) or len(given) != 2:
                raise ValueError(
                    f"{label}.transverse.{name} must be [r, s], the wave number pi r / s per Link"
                )
            bottom = integer(given[1], f"{label}.transverse.{name}'s s", 1)
            across.append((integer(given[0], f"{label}.transverse.{name}'s r", -bottom, bottom), bottom))
        top = keyed(packet["top"], f"{label}.top", AXES, AXES)
        edge = keyed(packet["edge"], f"{label}.edge", AXES, AXES)
        spans = tuple(
            span_of(top[name], f"{label}.top.{name}", shape[axis]) for axis, name in enumerate(AXES)
        )
        widths = tuple(integer(edge[name], f"{label}.edge.{name}", 0) for name in AXES)
        levels = levels_of(
            entry_of(entries, placed, label),
            f"the mode file's packets[{placed}]",
            families[family],
            shape,
            bound,
            beyond,
        )
        placed += 1
        found.append(
            PacketRow(
                family,
                AXES.index(packet["along"]),
                (turns, halves),
                integer(packet["amplitude"], f"{label}.amplitude", 1, bound),
                (spans[0], spans[1], spans[2]),
                (widths[0], widths[1], widths[2]),
                (turned, whole_turn),
                (across[0], across[1], across[2]),
                *levels,
                weights_of(
                    packet.get("weights"),
                    f"{label}.weights",
                    families[family].laid,
                    families[family].plane,
                ),
            )
        )
    return tuple(found)

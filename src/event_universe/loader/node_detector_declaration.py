"""A body's declaration as a NodeDetector with a record of its own (ALGEBRA.md, The NodeDetector is one declaration kind for every experiment; The click writes on the lattice (j) and (k); the owner's word: the body is at a Node): its `parts`, the modes' labels with the count in one of them at the start (`parts_of`), its `transitions` (which arriving family's quantum moves it from which part to which, at the declared weight and `resonance`; a transition of a part into itself the probe's, `transitions_of`), its `rates` (the emission at a declared lifetime, inside a guide as a source in time and in the open board as a packet of the declared `width`, the loader deciding by the board's shape, `rates_of`, `packet_form`), its own `node_detector` (its draw with its window, or the generator alone beside a probe, `loader/draw.py`) and, in place of its parts, its `conversion` (the records out and the rate, `conversion_of`); the keys of such a body (`READER_RECORD_KEYS`), each read into `NodeDetectorDeclaration` by `node_detector_of`, every defect refused by name and no default written."""

from __future__ import annotations

import itertools
from dataclasses import dataclass, replace

from event_universe.core.rule3 import division_forward
from event_universe.emission import holds_period
from event_universe.features.click import SCALE_OF, along_cosine, below_the_band, envelope, line_total
from event_universe.loader.derived import FamilyRule, count_wall
from event_universe.loader.draw import Generator, draw_of, generator_of
from event_universe.loader.keys import integer, keyed

READER_RECORD_KEYS = (
    "parts",
    "transitions",
    "rates",
    "node_detector",
    "conversion",
)  # a body as a NodeDetector with a record of its own
PART_KEYS, PART_REQUIRED = ("part", "name", "role", "count"), ("part", "name", "count")
TRANSITION_KEYS = ("from", "to", "drive", "weight", "resonance")  # a transition's keys
PROBE_KEYS = ("from", "to", "drive")  # a transition of a part into itself, the probe's: it turns nothing
RATE_KEYS = (
    "from",
    "to",
    "lifetime",
    "gives_to",
)  # an emission's keys; its resonance the transition's between the parts
RATE_OPTIONAL = (
    "width",
)  # the open board's packet's Nodes across, the one declared number of its shape
CONVERSION_KEYS, CONVERSION_REQUIRED = (
    ("rate", "to", "sense"),
    ("rate", "to"),
)  # a record converted whole
OUT_KEYS, OUT_REQUIRED = (
    ("family", "sense"),
    ("family",),
)  # a record out of a conversion, a plane with its sense


@dataclass(frozen=True)
class Transition:
    """A transition of a record at a Node that is a NodeDetector (ALGEBRA.md, The click writes on the lattice (j), the absorption click): the part the record leaves, the part it enters, the family whose arriving quantum it takes climbing or receives back descending (the parts' declared order, `parts_of`; `meeting.exchange`), by their positions, and the weight the arriving record's level is read into the record's phase with, the two-mode line's coupling, a number of the file (the advisor's k_r), at the declared resonance. A transition of a part into itself is the probe's (ALGEBRA.md, The pulsed gate; the two hands): it names the family whose lay at the body's Node closes the body's window, the body absorption it by that part with no turn (the weight 0 and the band's top as its resonance, read by nothing), the draw at the close by the labels' squares (`meeting.probe_click`)."""

    leaves: int
    enters: int
    drive: int
    weight: int
    resonance: tuple[int, int]


def pair_of(value: object, label: str) -> tuple[int, int]:
    """A resonance as the file declares it, a pair [num, den] with cos Omega = num / den (the advisor's second and the mathematician's hand, two hands): den from 1 and |num| below den, so that sin Omega is above 0; [0, den] the band's top, Omega = pi / 2; refused by name otherwise."""
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{label} is a pair [num, den] with cos Omega = num / den, got {value!r}")
    den = integer(value[1], f"{label}[1]", 1)
    num = integer(value[0], f"{label}[0]", 1 - den, den - 1)
    return num, den


@dataclass(frozen=True)
class Rate:
    """An emission of a body as a NodeDetector (the fifth act, the emission click at a declared rate): the excited part, the lower part, the lifetime in intervals (the rate 1 / lifetime per interval, the declared floor) and the family of light the whole quantum is laid on, by their positions; in the open board the packet's `width`, its Nodes across (None inside a guide, the source in time), and the directions the board holds for its lay from the body's Node, (axis, sense) each, drawn by the giver (`packet_form`; `emission.laid_packet`)."""

    leaves: int
    enters: int
    lifetime: int
    light: int
    resonance: tuple[int, int]
    width: int | None = None
    directions: tuple[tuple[int, int], ...] = ()


@dataclass(frozen=True)
class Conversion:
    """A conversion of a record whole at its one Node (ALGEBRA.md, The click writes on the lattice; the two hands): the rate in intervals per expected conversion, the declared floor (nature's lifetime read in as a declaration), the families of the records out, by their positions, each given one whole quantum at the Node by the count (the two hands), and per record out the sense of its lay, +1 or -1 for a plane family as the table declares it and 0 for a record of real lines (the mathematician's hand: the sense is the table's per record out and no family's, the anti-body being the same plane family at the opposite sense)."""

    rate: int
    outs: tuple[int, ...]
    senses: tuple[int, ...]


@dataclass(frozen=True)
class NodeDetectorDeclaration:
    """A body as a NodeDetector as the world declares it: its parts' names (the modes' labels; a record converted whole one part, named by its family), the count in each part at the start, its transitions, its emissions, its own draw (the generator with its window, `Draw`; the generator alone, `Generator`, for a body with a probe among its transitions, whose window is bounded by the probe's lays), its conversions and the sense of its own lay where it is converted whole and a plane (0 for real lines and for a record laid in its parts)."""

    names: tuple[str, ...]
    counts: tuple[int, ...]
    transitions: tuple[Transition, ...]
    rates: tuple[Rate, ...]
    draw: Generator | None
    conversions: tuple[Conversion, ...] = ()
    sense: int = 0


def parts_of(
    value: object, label: str, parts: int, count: int
) -> tuple[tuple[str, ...], tuple[int, ...]]:
    """A body's `parts`: one entry per part of its family in order, the declared order the record's energy order, the first part the lowest, the ground (the one order the declaration gives; read by the click's direction, `meeting.exchange`: a transition climbing in it takes the drive's quantum, one descending gives it back; the shipped rates descend in it), each `part` (its position), `name` (its own) and `count` (from 0), optionally `role`, a word read by nothing; the counts sum to the body's count and stand in one part (a lay in one mode has no amplitude in any other); refused by name otherwise."""
    if not isinstance(value, list) or len(value) != parts:
        raise ValueError(f"{label} lists one entry per part of the body's family, {parts} parts")
    names, counts = [], []
    for index, entry in enumerate(value):
        part = keyed(entry, f"{label}[{index}]", PART_KEYS, PART_REQUIRED)
        integer(part["part"], f"{label}[{index}].part", index, index)
        if not isinstance(part["name"], str) or not part["name"] or part["name"] in names:
            raise ValueError(f"{label}[{index}].name must be a name of its own, the mode's label")
        names.append(part["name"])
        counts.append(integer(part["count"], f"{label}[{index}].count", 0))
    if sum(counts) != count or sum(1 for c in counts if c) > 1:
        raise ValueError(
            f"{label} holds the counts {counts}: the body's count {count} stands in one part at the start, a lay "
            "in one mode having no amplitude in any other (ALGEBRA.md, The click writes on the lattice (j))"
        )
    return tuple(names), tuple(counts)


def transitions_of(
    value: object, label: str, names: tuple[str, ...], quanta: dict[str, int], own: int
) -> tuple[Transition, ...]:
    """A record's `transitions`: each `from` and `to`, two of its parts' names, `drive`, a family of quanta other than the record's own whose arriving quantum it takes, and `weight` from 1, the coupling the arriving level is read with, at its `resonance`; a transition of a part into itself is the probe's and declares its three keys alone, no `weight` and no `resonance` (it turns nothing; the two hands); refused by name otherwise."""
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list of the body's transitions")
    found = []
    for index, entry in enumerate(value):
        probe = isinstance(entry, dict) and entry.get("from") == entry.get("to")
        if probe and ("weight" in entry or "resonance" in entry):
            raise ValueError(
                f"{label}[{index}] is a transition of {entry.get('from')!r} into itself, the probe's, which turns "
                "nothing: it declares no weight and no resonance"
            )
        keys = PROBE_KEYS if probe else TRANSITION_KEYS
        row = keyed(entry, f"{label}[{index}]", keys, keys)
        leaves, enters = (
            part_named(row["from"], f"{label}[{index}].from", names),
            part_named(row["to"], f"{label}[{index}].to", names),
        )
        drive = family_named(row["drive"], f"{label}[{index}].drive", quanta, own)
        if probe:
            found.append(Transition(leaves, enters, drive, 0, (0, 1)))
            continue
        weight = integer(row["weight"], f"{label}[{index}].weight", 1)
        resonance = pair_of(row["resonance"], f"{label}[{index}].resonance")
        found.append(Transition(leaves, enters, drive, weight, resonance))
    return tuple(found)


def rates_of(
    value: object,
    label: str,
    names: tuple[str, ...],
    quanta: dict[str, int],
    own: int,
    transitions: tuple[Transition, ...],
) -> tuple[Rate, ...]:
    """A body's `rates`: each `from` and `to`, two of its parts' names, `lifetime` from 1 (the emission at 1 / lifetime per interval, the declared floor), `gives_to`, the family of quanta other than the body's own on which the emitted quantum is laid, and optionally `width` from 1, the open board's packet's Nodes across (`packet_form` decides its use by the board's shape); refused by name otherwise."""
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list of the body's emissions")
    found = []
    for index, entry in enumerate(value):
        row = keyed(entry, f"{label}[{index}]", RATE_KEYS + RATE_OPTIONAL, RATE_KEYS)
        width = integer(row["width"], f"{label}[{index}].width", 1) if "width" in row else None
        leaves, enters = (
            part_named(row["from"], f"{label}[{index}].from", names),
            part_named(row["to"], f"{label}[{index}].to", names),
        )
        lifetime = integer(row["lifetime"], f"{label}[{index}].lifetime", 1)
        light = family_named(row["gives_to"], f"{label}[{index}].gives_to", quanta, own)
        between = [t for t in transitions if {t.leaves, t.enters} == {leaves, enters}]
        if not between:  # the emission's frequency is the transition's declared resonance
            raise ValueError(
                f"{label}[{index}] gives between {names[leaves]!r} and {names[enters]!r}, and no transition "
                "between them declares the resonance the light is born at"
            )
        num, den = between[0].resonance
        if below_the_band(num, den):  # the guide's cos k below -1 (the mathematician's hand)
            raise ValueError(
                f"{label}[{index}] gives at the resonance [{num}, {den}], above the axis band's top (cos Omega "
                "below 1 / 3): no axis carries the quantum, and the diagonals' lay is not built"
            )
        found.append(Rate(leaves, enters, lifetime, light, between[0].resonance, width))
    return tuple(found)


def holding_period(rate: Rate, name: str, families: tuple[FamilyRule, ...], action: int) -> Rate:
    """The span condition on every emission, the source in time and the open board's packet alike (ALGEBRA.md, No write from outside Rule3 wakes the massless row's zero mode; The click writes on the lattice (5)): the emission's lifetime holds one period of its resonance, tau Omega >= 2 pi, that is num / den <= cos(2 pi / tau) by the rotation act (`emission.holds_period`; 8 at [2, 3], 15 at [5414, 6000]), else the loader refuses by name with the lifetime and the least admitted span, since a lay below its period is mostly uniform mode and the division act would take most of it; the rate as declared where it holds, the one rule on the span in one place."""
    scale = count_wall(families[rate.light], action) ** SCALE_OF
    if holds_period(rate.lifetime, rate.resonance, scale):
        return rate
    least = next(span for span in itertools.count(2) if holds_period(span, rate.resonance, scale))
    num, den = rate.resonance
    raise ValueError(
        f"{name}: the lifetime {rate.lifetime} does not hold one period of the resonance [{num}, {den}] "
        f"(tau Omega >= 2 pi, num / den <= cos(2 pi / tau)): the least admitted span is {least} (ALGEBRA.md, "
        "No write from outside Rule3 wakes the massless row's zero mode)"
    )


def packet_form(
    found: NodeDetectorDeclaration,
    label: str,
    families: tuple[FamilyRule, ...],
    at: tuple[int, int, int],
    shape: tuple[int, int, int],
    action: int,
) -> NodeDetectorDeclaration:
    """The loader's decision on each emission's lay by the board's shape against the width, no flag (the mathematician's hand with the advisor's seconds, two hands; the owner's word): inside a guide, a board with at most one axis above one Node (a chain, one Node the whole cross-section), the source in time stands as built (`emission.emitted_quantum`) and a declared `width` is refused by name; in the open board a rate declaring `width` gives the packet along a drawn direction (`emission.laid_packet`) and a rate declaring none the source in time as built (the shipped worlds bit for bit); for the packet the band's line with the transverse mode must carry the resonance at that width (`features/click.along_cosine`, refused by name where cos k_z leaves (-1, 1)), and the directions the giver draws among are those the board holds from the body's Node: along an axis above one Node, in either sense, where the train of L slices (`features/click.envelope` on the one-line packet's root `features/click.line_total`, from the lifetime and T) and the top-hat of `width` across on the other two axes stand within the board, none refused by name; the three refusals."""
    guide = sum(1 for extent in shape if extent > 1) <= 1
    rates = []
    for index, declared in enumerate(found.rates):
        name = f"{label}.rates[{index}]"
        rate = holding_period(declared, name, families, action)  # the one rule on the span, every lay
        if guide:
            if rate.width is not None:
                raise ValueError(
                    f"{name} declares the width {rate.width} inside a guide (a board of one Node across): the guide "
                    "carries the source in time, and the width is the open board's packet's"
                )
            rates.append(rate)
            continue
        if (
            rate.width is None
        ):  # no width declared: the source in time as built, every shipped world as it is
            rates.append(rate)
            continue
        light, (num, den) = families[rate.light], rate.resonance
        if (
            along_cosine(light.pair, rate.resonance, rate.width, count_wall(light, action) ** SCALE_OF)
            is None
        ):
            raise ValueError(
                f"{name}: the width {rate.width} cannot carry the resonance [{num}, {den}]: cos k_z = 3 (den_l / num_l) "
                "cos Omega - 2 cos(pi / (w + 1)) leaves (-1, 1), no wave number along an axis (the band with the "
                "transverse mode)"
            )
        length = len(
            envelope(line_total(action, rate.resonance), rate.lifetime, rate.width * rate.width)
        )
        low = int(division_forward(rate.width, 2, 0)[0])  # w div 2 by the division act, an index
        high = rate.width - 1 - low
        directions = tuple(
            (axis, sense)
            for axis in range(3)
            if shape[axis] > 1
            and all(at[a] - low >= 0 and at[a] + high < shape[a] for a in range(3) if a != axis)
            for sense in (1, -1)
            if 0 <= at[axis] + sense * (length - 1) < shape[axis]
        )
        if not directions:
            raise ValueError(
                f"{name}: no axis of the board {list(shape)} holds the packet of {length} slices and {rate.width} "
                f"across from the Node {list(at)}"
            )
        rates.append(replace(rate, directions=directions))
    return replace(found, rates=tuple(rates))


def part_named(value: object, label: str, names: tuple[str, ...]) -> int:
    """A part by its declared name, its position; refused by name where no part has it."""
    if value not in names:
        raise ValueError(f"{label} names {value!r}, and the body's parts are {list(names)}")
    return names.index(str(value))


def family_named(value: object, label: str, quanta: dict[str, int], own: int) -> int:
    """A family of quanta by name, not the body's own, its position; refused by name otherwise."""
    if value not in quanta or quanta[str(value)] == own:
        raise ValueError(
            f"{label} names {value!r}: a family of quanta other than the body's own, of {sorted(quanta)}"
        )
    return quanta[str(value)]


def sense_of(value: object, label: str, plane: bool) -> int:
    """A lay's sense, +1 or -1 for a plane (the sign of its Wronskian) and none for a record of real lines, which write no sign; refused by name otherwise."""
    sense = integer(value, label, -1, 1) if value is not None else 0
    if plane == (sense == 0):
        raise ValueError(
            f"{label}: a plane is laid at the sense +1 or -1 and a record of real lines at none, got {value!r}"
        )
    return sense


def conversion_of(
    value: object, label: str, families: tuple[FamilyRule, ...], own: int, quanta: dict[str, int]
) -> tuple[Conversion, int]:
    """A body's `conversion` (the fifth list of the act, ALGEBRA.md, The click writes on the lattice; the two hands, the advisor's (c) and the mathematician's hand: the neutron's table and rate): `rate`, the intervals per expected conversion from 1 (the declared floor), `to`, the records out (each a family of quanta other than the body's own, given one whole quantum at the Node by the count: a family's name for a record of real lines, and for a plane family an entry {`family`, `sense`}, the sense +1 or -1 of its lay, `emission.laid_by_count`; a plane family named without its sense and a record of real lines with one are refused by name, `sense_of`; the mathematician's hand), and the body's own lay's `sense` beside them where its record is a plane; returns the conversion and that sense; refused by name otherwise."""
    found = keyed(value, label, CONVERSION_KEYS, CONVERSION_REQUIRED)
    rate = integer(found["rate"], f"{label}.rate", 1)
    if not isinstance(found["to"], list) or not found["to"]:
        raise ValueError(f"{label}.to lists the records out of the conversion")
    outs, senses = [], []
    for index, entry in enumerate(found["to"]):
        where = f"{label}.to[{index}]"
        named = (
            keyed(entry, where, OUT_KEYS, OUT_REQUIRED) if isinstance(entry, dict) else {"family": entry}
        )
        outs.append(out := family_named(named["family"], where, quanta, own))
        if families[out].plane and "sense" not in named:
            raise ValueError(
                f"{where} names {families[out].name!r}, a plane family, without its sense: a record out of a plane "
                "family is an entry {family, sense}, the sense +1 or -1 of its lay (ALGEBRA.md #the-paces, The sign "
                "is the rotation sense)"
            )
        senses.append(sense_of(named.get("sense"), f"{where}.sense", families[out].plane))
    own_sense = sense_of(found.get("sense"), f"{label}.sense", families[own].plane)
    return Conversion(rate, tuple(outs), tuple(senses)), own_sense


def node_detector_of(
    body: dict[str, object],
    label: str,
    families: tuple[FamilyRule, ...],
    own: int,
    quanta: dict[str, int],
    count: int,
) -> NodeDetectorDeclaration:
    """A body's declaration as a NodeDetector (ALGEBRA.md, The click writes on the lattice (j) and (k); the owner's word: the body is at a Node): `parts` (the lay in its modes at the start, admitted alone), and with `node_detector` (its own draw: with its window, `draw_of`, or the generator alone where a probe stands among the transitions, `generator_of`, a window beside a probe refused by name) its `transitions` and its `rates`, each needing the draw and the draw needing the parts; the family a plane of several parts; or `conversion` (`conversion_of`), the record converted whole at its Node, of any shape, one part named by its family at the body's count, its own lay's `sense` beside the table where the record is a plane, with `node_detector` to draw it; refused by name otherwise."""
    family = families[own]
    if "conversion" in body:
        if "parts" in body or "transitions" in body or "rates" in body:
            raise ValueError(f"{label} is converted whole: it declares no parts, transitions or rates")
        if "node_detector" not in body:
            raise ValueError(f"{label} declares a conversion and no `node_detector` to draw it with")
        table, sense = conversion_of(body["conversion"], f"{label}.conversion", families, own, quanta)
        own_draw = draw_of(body["node_detector"], f"{label}.node_detector")
        return NodeDetectorDeclaration((family.name,), (count,), (), (), own_draw, (table,), sense)
    if "parts" not in body:
        raise ValueError(
            f"{label} declares its parts, the modes it is laid in, before any `node_detector`, transition or rate"
        )
    if not family.plane or family.parts < 2 or family.planes != 1:
        raise ValueError(
            f"{label}: a body laid in its parts is a plane of several parts, one plane per part, and "
            f"{family.name!r} is not"
        )
    names, counts = parts_of(body["parts"], f"{label}.parts", family.parts, count)
    transitions = transitions_of(body.get("transitions", []), f"{label}.transitions", names, quanta, own)
    probed = any(transition.leaves == transition.enters for transition in transitions)
    draw: Generator | None = None
    if "node_detector" in body:
        read = generator_of if probed else draw_of
        draw = read(body["node_detector"], f"{label}.node_detector")
    if draw is None and ("transitions" in body or "rates" in body):
        raise ValueError(
            f"{label} declares transitions or rates and no `node_detector` to draw them with"
        )
    rates = rates_of(body.get("rates", []), f"{label}.rates", names, quanta, own, transitions)
    return NodeDetectorDeclaration(names, counts, transitions, rates, draw)

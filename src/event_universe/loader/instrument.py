"""The instrument's declaration (ALGEBRA.md #the-click-is-the-meeting, the pair's form and the GHZ gate; HIGHLIGHTS.md, the owner's decision of 2026-10-02, after a click the paths are cancelled on the GameBoard): on a detector's region its setting `basis` (p, q), the coefficients of its credit, and its parts' `pattern`, one integer pair [alpha_k, beta_k] per part of the record it reads, the + port reading the part k as e_k(+) = alpha_k p + beta_k q and the - port as e_k(-) = alpha_k (-q) + beta_k p (the pair's pattern [[1, 0], [0, 1]], the ports (p, q) and (-q, p); `ports_of`, the two ports exactly orthogonal with equal norms, refused by name otherwise), read by the reader (`tools/bell_gate.py`) and by the instrument's draw through the root in the run; and on the world the `instrument`, the draw's declaration (`Instrument`): the window in intervals after which the instrument draws and writes, the seed and the generator's multiplier and increment (x <- (multiplier x + increment) mod 2^width, the width the file's), every one the file's and none the engine's; every defect refused by name and no default written."""

from __future__ import annotations

from dataclasses import dataclass, replace

from event_universe.core.integer import MAX_WORK_INT
from event_universe.features.click import SCALE_OF, along_cosine, envelope, exact_total
from event_universe.loader.derived import FamilyRule, count_wall
from event_universe.loader.keys import integer, keyed

Pattern = tuple[tuple[int, int], ...]  # per part [alpha_k, beta_k], the part's read of the setting
Ports = tuple[tuple[int, ...], tuple[int, ...]]  # a side's two ports, + then -, one coefficient per part
INSTRUMENT_KEYS = ("window", "seed", "multiplier", "increment")  # the draw's declaration on the world


@dataclass(frozen=True)
class Instrument:
    """The instrument's draw as the world declares it: the window (the intervals after which every detector's window closes and the instrument draws and writes), the seed of its generator and the generator's multiplier and increment, x <- (multiplier x + increment) mod 2^width (features/click)."""

    window: int
    seed: int
    multiplier: int
    increment: int


def instrument_of(value: object, label: str) -> Instrument:
    """The world's `instrument`: its four keys, the window from 1, the seed and the increment from 0 and the multiplier from 1, every other key refused by name."""
    found = keyed(value, label, INSTRUMENT_KEYS, INSTRUMENT_KEYS)
    return Instrument(
        integer(found["window"], f"{label}.window", 1),
        integer(found["seed"], f"{label}.seed", 0),
        integer(found["multiplier"], f"{label}.multiplier", 1),
        integer(found["increment"], f"{label}.increment", 0),
    )


def ports_of(basis: tuple[int, ...], pattern: Pattern) -> Ports:
    """A side's two ports from its declared setting (p, q) and its parts' pattern [[alpha_k, beta_k], ...]: e_k(+) = alpha_k p + beta_k q and e_k(-) = alpha_k (-q) + beta_k p, the - port the + port's with the setting turned a quarter (the pair's pattern [[1, 0], [0, 1]] gives (p, q) and (-q, p)); refused by name: a setting of other than two coefficients, no pattern, and two ports not orthogonal with equal norms, which is no instrument of two outcomes."""
    if len(basis) != 2 or not pattern:
        raise ValueError(
            "a side declares its setting (p, q) as `basis` and one pair [alpha, beta] per part as "
            f"`pattern`, got {basis} and {list(pattern)}"
        )
    p, q = basis
    plus = tuple(alpha * p + beta * q for alpha, beta in pattern)
    minus = tuple(beta * p - alpha * q for alpha, beta in pattern)
    crossed = sum(u * v for u, v in zip(plus, minus, strict=True))
    if crossed or sum(u * u for u in plus) != sum(v * v for v in minus):
        raise ValueError(
            f"the pattern {list(pattern)} at the setting {basis} gives the ports {plus} and {minus}, "
            "not orthogonal with equal norms: no instrument of two outcomes"
        )
    return plus, minus


def basis_of(value: object, label: str) -> tuple[int, ...]:
    """A detector's declared basis, its setting: a list of integers not all 0 (the pair's (p, q)); refused by name otherwise."""
    if not isinstance(value, list) or not value or not any(value):
        raise ValueError(f"{label} must be a list of integers, the setting's coefficients, not all 0")
    return tuple(integer(v, f"{label}[{i}]", -MAX_WORK_INT) for i, v in enumerate(value))


def pattern_of(value: object, label: str, basis: tuple[int, ...]) -> Pattern:
    """A detector's declared pattern: a list of integer pairs [alpha_k, beta_k], one per part of the record it reads, none [0, 0] (a part read with no coefficient at either port is no part of the read), on a setting of two coefficients (p, q); refused by name otherwise."""
    if len(basis) != 2:
        raise ValueError(
            f"{label} reads the setting (p, q) of two coefficients into the parts, and the basis has {len(basis)}"
        )
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must list one pair [alpha, beta] per part of the record it reads")
    found = []
    for index, entry in enumerate(value):
        if not isinstance(entry, list) or len(entry) != 2:
            raise ValueError(
                f"{label}[{index}] must be a pair [alpha, beta]: e(+) = alpha p + beta q, e(-) = alpha (-q) + beta p"
            )
        alpha = integer(entry[0], f"{label}[{index}][0]", -MAX_WORK_INT)
        beta = integer(entry[1], f"{label}[{index}][1]", -MAX_WORK_INT)
        if alpha == 0 and beta == 0:
            raise ValueError(
                f"{label}[{index}] is [0, 0]: a part read with no coefficient at either port is no part of the read"
            )
        found.append((alpha, beta))
    return tuple(found)


def patterns_of_the_law(
    patterns: list[tuple[str, Pattern]], laid: list[int], families: tuple[FamilyRule, ...]
) -> None:
    """A declared pattern reads one record of several parts, one pair per part: its length is the parts of a family of several parts the world lays (its messages' and its bodies' families, `laid`, by their indexes); refused by name where the lengths differ or the world lays no such record."""
    parts = sorted({families[index].parts for index in laid if families[index].parts > 1})
    for name, pattern in patterns:
        if pattern and len(pattern) not in parts:
            raise ValueError(
                f"detector {name!r} declares a pattern of {len(pattern)} parts, and the world lays "
                + (
                    f"records of {parts} parts, one pair per part"
                    if parts
                    else "no record of several parts"
                )
            )


NODE_INSTRUMENT_KEYS = (
    "parts",
    "transitions",
    "rates",
    "instrument",
    "conversion",
)  # a body as an instrument
PART_KEYS, PART_REQUIRED = ("part", "name", "role", "count"), ("part", "name", "count")
TRANSITION_KEYS = ("from", "to", "drive", "weight", "resonance")  # a transition's keys
RATE_KEYS = (
    "from",
    "to",
    "lifetime",
    "gives_to",
)  # a giving's keys; its resonance the transition's between the parts
RATE_OPTIONAL = (
    "width",
)  # the open board's packet's Nodes across, the one declared number of its shape
CONVERSION_KEYS, CONVERSION_REQUIRED = (
    ("rate", "to", "sense"),
    ("rate", "to"),
)  # a record converted whole


@dataclass(frozen=True)
class Transition:
    """A transition of a record at a Node that is an instrument (ALGEBRA.md, The click writes on the GameBoard (j), the taking click): the part the record leaves, the part it enters, the family whose arriving quantum it takes, by their positions, and the weight the arriving record's level is read into the record's phase with, the two-mode line's coupling, a number of the file (the advisor's k_r)."""

    leaves: int
    enters: int
    drive: int
    weight: int
    resonance: tuple[int, int]


def pair_of(value: object, label: str) -> tuple[int, int]:
    """A resonance as the file declares it, a pair [num, den] with cos Omega = num / den (the advisor's second, #1572 comment 5964191930, and the mathematician's 213 and 214, two hands): den from 1 and |num| below den, so that sin Omega is above 0; [0, den] the band's top, Omega = pi / 2; refused by name otherwise."""
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{label} is a pair [num, den] with cos Omega = num / den, got {value!r}")
    den = integer(value[1], f"{label}[1]", 1)
    num = integer(value[0], f"{label}[0]", 1 - den, den - 1)
    return num, den


@dataclass(frozen=True)
class Rate:
    """A giving of a body as an instrument (the fifth act, the giving click at a declared rate): the excited part, the lower part, the lifetime in intervals (the rate 1 / lifetime per interval, the declared floor) and the family of light the whole quantum is laid on, by their positions; in the open board the packet's `width`, its Nodes across (None inside a guide, the source in time), and the directions the board holds for its lay from the body's Node, (axis, sense) each, drawn by the giver (`packet_form`; `giving.laid_packet`)."""

    leaves: int
    enters: int
    lifetime: int
    light: int
    resonance: tuple[int, int]
    width: int | None = None
    directions: tuple[tuple[int, int], ...] = ()


@dataclass(frozen=True)
class Conversion:
    """A conversion of a record whole at its one Node (ALGEBRA.md, The click writes on the GameBoard; the two hands of 2026-10-03): the rate in intervals per expected conversion, the declared floor (nature's lifetime read in as a declaration), and the families of the records out, by their positions, each given one whole quantum at the Node by the count (the two hands, #1572 comments 5964520368 and 5964754600)."""

    rate: int
    outs: tuple[int, ...]


@dataclass(frozen=True)
class NodeInstrument:
    """A body as an instrument as the world declares it: its parts' names (the modes' labels; a record converted whole one part, named by its family), the count in each part at the start, its transitions, its givings, its own draw (the window, the seed and the generator), its conversions and the sense of its own lay where it is converted whole and a plane (0 for real lines and for a record laid in its parts)."""

    names: tuple[str, ...]
    counts: tuple[int, ...]
    transitions: tuple[Transition, ...]
    rates: tuple[Rate, ...]
    draw: Instrument | None
    conversions: tuple[Conversion, ...] = ()
    sense: int = 0


def parts_of(
    value: object, label: str, parts: int, count: int
) -> tuple[tuple[str, ...], tuple[int, ...]]:
    """A body's `parts`: one entry per part of its family in order, each `part` (its position), `name` (its own) and `count` (from 0), optionally `role`, a word read by nothing; the counts sum to the body's count and stand in one part (a lay in one mode has no amplitude in any other); refused by name otherwise."""
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
            "in one mode having no amplitude in any other (ALGEBRA.md, The click writes on the GameBoard (j))"
        )
    return tuple(names), tuple(counts)


def transitions_of(
    value: object, label: str, names: tuple[str, ...], quanta: dict[str, int], own: int
) -> tuple[Transition, ...]:
    """A record's `transitions`: each `from` and `to`, two of its parts' names, `drive`, a family of quanta other than the record's own whose arriving quantum it takes, and `weight` from 1, the coupling the arriving level is read with; refused by name otherwise."""
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list of the body's transitions")
    found = []
    for index, entry in enumerate(value):
        row = keyed(entry, f"{label}[{index}]", TRANSITION_KEYS, TRANSITION_KEYS)
        leaves, enters = (
            part_named(row["from"], f"{label}[{index}].from", names),
            part_named(row["to"], f"{label}[{index}].to", names),
        )
        drive = family_named(row["drive"], f"{label}[{index}].drive", quanta, own)
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
    """A body's `rates`: each `from` and `to`, two of its parts' names, `lifetime` from 1 (the giving at 1 / lifetime per interval, the declared floor), `gives_to`, the family of quanta other than the body's own on which the given quantum is laid, and optionally `width` from 1, the open board's packet's Nodes across (`packet_form` decides its use by the board's shape); refused by name otherwise."""
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list of the body's givings")
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
        if not between:  # the giving's frequency is the transition's declared resonance
            raise ValueError(
                f"{label}[{index}] gives between {names[leaves]!r} and {names[enters]!r}, and no transition "
                "between them declares the resonance the light is born at"
            )
        num, den = between[0].resonance
        if 3 * num < den:  # cos Omega below 1 / 3: no axis carries the quantum (the mathematician's 221)
            raise ValueError(
                f"{label}[{index}] gives at the resonance [{num}, {den}], above the axis band's top (cos Omega "
                "below 1 / 3): no axis carries the quantum, and the diagonals' lay is not built"
            )
        found.append(Rate(leaves, enters, lifetime, light, between[0].resonance, width))
    return tuple(found)


def packet_form(
    found: NodeInstrument,
    label: str,
    families: tuple[FamilyRule, ...],
    at: tuple[int, int, int],
    shape: tuple[int, int, int],
    action: int,
) -> NodeInstrument:
    """The loader's decision on each giving's lay by the board's shape against the width, no flag (the mathematician's 224 (1) and 229 with the advisor's seconds, two hands; the owner's word of 2026-10-03, 09:46 Israel): inside a guide, a board with at most one axis above one Node (a chain, one Node the whole cross-section), the source in time stands as built (`giving.given_quantum`) and a declared `width` is refused by name; in the open board the giving is the packet along a drawn direction (`giving.laid_packet`), so `width` is required, the band's line with the transverse mode must carry the resonance at that width (`features/click.along_cosine`, refused by name where cos k_z leaves (-1, 1)), and the directions the giver draws among are those the board holds from the body's Node: along an axis above one Node, in either sense, where the train of L slices (`features/click.envelope`, from the lifetime and T) and the top-hat of `width` across on the other two axes stand within the board, none refused by name."""
    guide = sum(1 for extent in shape if extent > 1) <= 1
    rates = []
    for index, rate in enumerate(found.rates):
        name = f"{label}.rates[{index}]"
        if guide:
            if rate.width is not None:
                raise ValueError(
                    f"{name} declares the width {rate.width} inside a guide (a board of one Node across): the guide "
                    "carries the source in time, and the width is the open board's packet's"
                )
            rates.append(rate)
            continue
        if rate.width is None:
            raise ValueError(
                f"{name} gives in the open board (two axes or more above one Node) and declares no `width`: the open "
                "board's giving is a packet of `width` Nodes across along a drawn axis"
            )
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
            envelope(exact_total(action, rate.resonance), rate.lifetime, rate.width * rate.width)
        )
        low, high = rate.width // 2, rate.width - 1 - rate.width // 2
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
    """A body's `conversion` (the fifth list of the act, ALGEBRA.md, The click writes on the GameBoard; the two hands of 2026-10-03, the advisor's (c), #1572 comment 5963954612, and the mathematician's 204, 5964082980: the neutron's table and rate): `rate`, the intervals per expected conversion from 1 (the declared floor), `to`, the families of the records out (each a family of quanta other than the body's own, given one whole quantum at the Node by the count), and the body's own lay's `sense` beside them where its record is a plane; returns the conversion and that sense; refused by name otherwise."""
    found = keyed(value, label, CONVERSION_KEYS, CONVERSION_REQUIRED)
    rate = integer(found["rate"], f"{label}.rate", 1)
    if not isinstance(found["to"], list) or not found["to"]:
        raise ValueError(f"{label}.to lists the families of the records out of the conversion")
    outs = tuple(
        family_named(name, f"{label}.to[{index}]", quanta, own) for index, name in enumerate(found["to"])
    )
    own_sense = sense_of(found.get("sense"), f"{label}.sense", families[own].plane)
    return Conversion(rate, outs), own_sense


def node_instrument_of(
    body: dict[str, object],
    label: str,
    families: tuple[FamilyRule, ...],
    own: int,
    quanta: dict[str, int],
    count: int,
) -> NodeInstrument:
    """A body's declaration as an instrument (ALGEBRA.md, The click writes on the GameBoard (j) and (k); the owner's word of 2026-10-03: the body is at a Node): `parts` (the lay in its modes at the start, admitted alone), and with `instrument` (its own draw, `instrument_of`) its `transitions` and its `rates`, each needing the instrument and the instrument needing the parts; the family a plane of several parts; or `conversion` (`conversion_of`), the record converted whole at its Node, of any shape, one part named by its family at the body's count, its own lay's `sense` beside the table where the record is a plane, with `instrument` to draw it; refused by name otherwise."""
    family = families[own]
    if "conversion" in body:
        if "parts" in body or "transitions" in body or "rates" in body:
            raise ValueError(f"{label} is converted whole: it declares no parts, transitions or rates")
        if "instrument" not in body:
            raise ValueError(f"{label} declares a conversion and no `instrument` to draw it with")
        table, sense = conversion_of(body["conversion"], f"{label}.conversion", families, own, quanta)
        own_draw = instrument_of(body["instrument"], f"{label}.instrument")
        return NodeInstrument((family.name,), (count,), (), (), own_draw, (table,), sense)
    if "parts" not in body:
        raise ValueError(
            f"{label} declares its parts, the modes it is laid in, before any instrument, transition or rate"
        )
    if not family.plane or family.parts < 2 or family.planes != 1:
        raise ValueError(
            f"{label}: a body laid in its parts is a plane of several parts, one plane per part, and "
            f"{family.name!r} is not"
        )
    names, counts = parts_of(body["parts"], f"{label}.parts", family.parts, count)
    draw = instrument_of(body["instrument"], f"{label}.instrument") if "instrument" in body else None
    if draw is None and ("transitions" in body or "rates" in body):
        raise ValueError(f"{label} declares transitions or rates and no `instrument` to draw them with")
    transitions = transitions_of(body.get("transitions", []), f"{label}.transitions", names, quanta, own)
    rates = rates_of(body.get("rates", []), f"{label}.rates", names, quanta, own, transitions)
    return NodeInstrument(names, counts, transitions, rates, draw)

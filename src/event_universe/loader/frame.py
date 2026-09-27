"""The frame of the run's files read through the schemas: the world file's own keys by the frame's schema, the bodies' keys by the frame's schemas of today's form and of the law's form (a body by its family, its Nodes with their counts and its momentum), the detectors' by the frame's schema, the readings and the universe handed on as written to their readers; the universe file, its integers by the frame's schema and each family's entry by the cards of the register with the frame's one key, the name; and the start file, its mode; every key refused by name, no default written here (ALGEBRA.md #the-primitives: a term is one line of the files)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import cast

from event_universe.core.register import Register
from event_universe.core.schema import (
    Context,
    Either,
    Integer,
    ListOf,
    MapOf,
    Name,
    ObjectOf,
    OneOf,
    Word,
    check,
)
from event_universe.loader import cards

# the universe's integers (ALGEBRA.md #a-familys-declaration, #the-interval, #the-primitives): Gamma the Node clock, A the amplitude bound, Lambda the charge's read weight, Q the momentum's unit, and the twist table of exact triples [c, s, d] read as written and checked with Gamma and A where the transport is built
INTEGERS = ObjectOf(
    {
        "node_clock": Integer(least=1),
        "amplitude_bound": Integer(least=1),
        "Lambda": Integer(least=1),
        "momentum_unit": Integer(least=1),
        "twist_table": ObjectOf(
            {
                "unit": Integer(least=1),
                "fine": ListOf(ListOf(Integer(), 3)),
                "coarse": ListOf(ListOf(Integer(), 3)),
            }
        ),
    }
)
UNIVERSE_KEYS = ("integers", "families")
# the start file (ALGEBRA.md #a-familys-declaration): the run's mode, check (every measured event read beside its blind expectation, no pin compared) or pin (the pins compared); no law's name, no version
START = ObjectOf({"mode": OneOf(("check", "pin"))})
# a face of the GameBoard: open (its edge is infinity), periodic (the walk wraps) or closed (a zero face with no take)
FACE = OneOf(("open", "periodic", "closed"))
# the world file's own keys (ALGEBRA.md #the-primitives): the GameBoard, its faces, the intervals, the files it names, its stamp; and the old form's N, which the loop still reads for the given record's period
WORLD = ObjectOf(
    {
        "shape": ListOf(Integer(least=1), 3),
        "boundary": Either((OneOf(("open",)), ObjectOf({"x": FACE, "y": FACE, "z": FACE}))),
        "ticks": Integer(least=0),
        "engine": Word(),
        "stamp": ObjectOf({"hash": Word()}),
        "face_depth": Integer(least=1),
        "probes": ListOf(ListOf(Integer(least=0), 3)),
        "mode_axis": OneOf(("x", "y", "z")),
        "amplitude_bound": Integer(least=1),
        "node_clock": Integer(least=1),
        "momentum_unit": Integer(least=1),
        "N": Integer(least=2),
    },
    frozenset(
        {
            "stamp",
            "face_depth",
            "probes",
            "mode_axis",
            "amplitude_bound",
            "node_clock",
            "momentum_unit",
        }
    ),
)
# a pair of integers, a rational
PAIR = ListOf(Integer(least=1), 2)
# a family's clock, the pair form [p, q] of its phase per interval of age (ALGEBRA.md, a family's declaration): the frame's key beside the name; p from 0, q from 1 (the build's rule)
CLOCK = ListOf(Integer(least=0), 2)
# the spin's step's row: the two weights curl and tidal, each a pair (ALGEBRA.md #a-familys-declaration); the frame admits the key by name and kind, the spin's step's folder reads it (the leapfrog's span is core's SPAN, never a key of a row)
SPINS_STEP = ObjectOf({"curl": PAIR, "tidal": PAIR})
# three integers on the axes
AXES = ListOf(Integer(), 3)
# a body's emitter, the giving of a clicking body (ALGEBRA.md #the-click to (6), ALGEBRA.md #the-primitives): the given family, the ladder by name, the given record's clock and pair where the family declares none, the period, the norm with its denominator, the weight, the window's read, the twist
EMITTER = ObjectOf(
    {
        "family": Name(),
        "receiver": Either((Word(), ListOf(Word()))),
        "period": Integer(least=1),
        "norm": Integer(least=1),
        "weight": Integer(least=1),
        "norm_denominator": Integer(least=1),
        "window_read": Integer(),
        "clock": Either((Integer(least=1), PAIR)),
        "pair": Either((Integer(least=1), PAIR)),
        "twist": Integer(least=0),
    },
    frozenset(
        {"receiver", "period", "norm", "weight", "norm_denominator", "window_read", "clock", "pair"}
    ),
)
# an emitting body in the law's form (the mathematician's words of 2026-09-27 on #1198, what the giving's row reads): the given family, the giving's weight g, the window's norm T with its denominator, the ladder's receiver where named; no period (P_body is the mode's rotation), no clock, no pair, no twist
GIVER = ObjectOf(
    {
        "family": Name(),
        "weight": Integer(least=1),
        "norm": Integer(least=1),
        "norm_denominator": Integer(least=1),
        "receiver": Word(),
    },
    frozenset({"receiver"}),
)
# a body of the world file in today's form (ALGEBRA.md #the-stable-body names the form to come: its family, its Nodes, its count per Node and its momentum n): its Node, its family, its quanta, its momentum at its two levels (now and before) and its stocks of other families; a block's side or extents, pair and kind, seed with its clock and proper clock, ramp and start, margin, the body's numbers q, spin at its two levels, moment and twist, its emitter with receiver and stock
BODY = ObjectOf(
    {
        "position": ListOf(Integer(least=0), 3),
        "family": Name(),
        "amount": Integer(least=1),
        "momentum": AXES,
        "momentum_before": AXES,
        "stocks": MapOf(Name(), Integer(least=1)),
        "kind": PAIR,
        "q": Integer(),
        "spin": AXES,
        "spin_before": AXES,
        "moment": AXES,
        "twist": Integer(least=0),
        "side": Integer(least=1),
        "extents": ListOf(Integer(least=1), 3),
        "pair": PAIR,
        "seed": Either((Integer(least=0), ListOf(Integer()))),
        "clock": PAIR,
        "proper_clock": ListOf(PAIR),
        "ramp": Integer(least=0),
        "start": Integer(least=0),
        "margin": Word(),  # a well's margin kind, the loader's words (the gate counts a family named like one)
        "emitter": EMITTER,
        "receiver": Word(),
        "stock": Integer(least=1),
    },
    frozenset(
        {
            "kind",
            "q",
            "spin",
            "spin_before",
            "moment",
            "twist",
            "side",
            "extents",
            "pair",
            "seed",
            "clock",
            "proper_clock",
            "ramp",
            "start",
            "margin",
            "emitter",
            "receiver",
            "stock",
        }
    ),
)
# one Node of a body in the law's form (ALGEBRA.md #the-stable-body.121 item 3): its address and the family of clicks' level there, the count; one line per Node
NODE_COUNT = ObjectOf({"node": ListOf(Integer(least=0), 3), "count": Integer(least=1)})
# a body of the world file in the law's form (ALGEBRA.md #what-a-body-is: "the world file names the body's family, its Nodes, its count per Node and its momentum n, and nothing else"; #the-generator (a): "one body by its Nodes with their counts"; #the-counts-line: the counts laid from the file into T c_next + r' = T c_now + SUM_j F_ij + r): its family, its Nodes with their counts, its momentum n at its two levels (now and before, the KEEP step), its spin at its two levels and its moment where declared, a moving body's phase denominator m (#the-generator (e)), its stocks and its emitter where it gives, nothing else; the momentum's and the spin's parts are handed to the families whose rows keep them (three parts, the KEEP step), a folder's binding and not the frame's; a folder's own key at a body joins through the cards when one declares it
COUNTED = ObjectOf(
    {
        "family": Name(),
        "nodes": ListOf(NODE_COUNT),
        "momentum": AXES,
        "momentum_before": AXES,
        "spin": AXES,
        "spin_before": AXES,
        "moment": AXES,
        "phase_denominator": Integer(least=1),
        "stocks": MapOf(Name(), Integer(least=1)),
        "emitter": GIVER,
    },
    frozenset({"spin", "spin_before", "moment", "phase_denominator", "stocks", "emitter"}),
)
# a detector of the world file: its name, its Nodes, or the body it belongs to
DETECTOR = ObjectOf(
    {"name": Word(), "positions": ListOf(ListOf(Integer(least=0), 3)), "block": Integer(least=0)},
    frozenset({"positions", "block"}),
)
# the world's keys handed on as written to their readers in events/world.py until their own cuts (True: required): the universe (a repository path, or a unit test's families inline), the bodies and the detectors (checked by `bodies` and `detectors` once the families are known), the readings, an inline world's twist table
HANDED = {
    "universe": True,
    "measured": True,
    "detectors": True,
    "readings": False,
    "twist_table": False,
}


@dataclass(frozen=True)
class EngineStart:
    """The one engine start file as read: its repository path and its mode."""

    path: str
    mode: str


def document_of(key: str, value: str, files: Mapping[str, object], label: str) -> dict[str, object]:
    """The document the world names under `key` at the repository path `value`, from the files the host read; refused by name where no file was read there or it is no object."""
    if value not in files:
        raise ValueError(f"{key} names {value!r}, no file at the repository's root")
    document = files[value]
    if not isinstance(document, dict):
        raise ValueError(f"{label} must be a JSON object")
    return document


def entry_kind(register: Register) -> ObjectOf:
    """A family's entry: the frame's keys, its name, its quantum (an integer from 1, the law's owner's row of 2026-09-27), its clock and its spins_step (both optional), and every key the cards declare at a family's entry, optional where a card says so."""
    declared = cards.at(register, "a family's entry")
    keys = {
        "name": Word(),
        "quantum": Integer(least=1),
        "clock": CLOCK,
        "spins_step": SPINS_STEP,
        **declared.keys,
    }
    return ObjectOf(keys, declared.optional | {"clock", "spins_step"})


def families(
    value: object, integers: Mapping[str, object], register: Register, label: str
) -> tuple[dict[str, object], ...]:
    """The families' entries checked against the cards with the names and the integers known (a read's weight word resolved to the integer): a nonempty list, every entry an object of the entry's kind; the checked entries."""
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a nonempty list")
    names = tuple(
        entry["name"]
        for entry in value
        if isinstance(entry, dict) and "name" in entry and isinstance(entry["name"], str)
    )
    context = Context(
        names, {key: number for key, number in integers.items() if isinstance(number, int)}
    )
    kind = entry_kind(register)
    checked = []
    for index, entry in enumerate(value):
        found = check(entry, kind, f"{label}[{index}]", context)
        assert isinstance(found, dict)
        checked.append(found)
    return tuple(checked)


def universe(
    value: str, files: Mapping[str, object], register: Register
) -> tuple[tuple[dict[str, object], ...], dict[str, object]]:
    """The universe file read: exactly its two keys, the integers checked first, then every family's entry against the cards with the names and the integers known (a read's weight by name resolved to the integer); the checked entries and the integers."""
    label = f"the universe file {value!r}"
    document = document_of("universe", value, files, label)
    unknown = sorted(set(document) - set(UNIVERSE_KEYS))
    if unknown:
        raise ValueError(f"{label} has unknown keys: {', '.join(unknown)}")
    missing = sorted(set(UNIVERSE_KEYS) - set(document))
    if missing:
        raise ValueError(f"{label} lacks keys: {', '.join(missing)}")
    integers = check(document["integers"], INTEGERS, f"{label}.integers", Context())
    assert isinstance(integers, dict)
    return families(document["families"], integers, register, f"{label}.families"), integers


def world(document: object) -> dict[str, object]:
    """The world file read: an unknown key and a missing key refused by name, every key of the frame's schema checked, every handed key as written."""
    if not isinstance(document, dict):
        raise ValueError("a world is a JSON object")
    keys = set(WORLD.keys) | set(HANDED)
    unknown = sorted(set(document) - keys)
    if unknown:
        raise ValueError(
            f"the world has unknown keys: {', '.join(unknown)} (the keys: {', '.join(sorted(keys))})"
        )
    required = (set(WORLD.keys) - set(WORLD.optional)) | {key for key, must in HANDED.items() if must}
    missing = sorted(required - set(document))
    if missing:
        raise ValueError(f"the world lacks keys: {', '.join(missing)}")
    checked: dict[str, object] = {
        key: check(document[key], kind, f"the world.{key}", Context())
        for key, kind in WORLD.keys.items()
        if key in document
    }
    for key in HANDED:
        if key in document:
            checked[key] = document[key]
    return checked


def body_form(entry: object, label: str) -> ObjectOf:
    """The form a body is written in: today's, by its position (BODY), or the law's, by its Nodes with their counts (COUNTED); a body written in neither or in both is refused by name."""
    if not isinstance(entry, dict):
        raise ValueError(
            f"{label} must be an object: a body by its position, or by its nodes with their counts"
        )
    by_position = "position" in entry
    by_nodes = "nodes" in entry
    if by_position == by_nodes:
        which = "both" if by_position else "neither"
        raise ValueError(
            f"{label} is written by its position (today's form) or by its nodes with their counts "
            f"(the law's form), not {which}"
        )
    return BODY if by_position else COUNTED


def counted_nodes(body: Mapping[str, object], label: str) -> None:
    """The rule between the lines of a body in the law's form: at least one Node, and no Node twice."""
    nodes = body["nodes"]
    assert isinstance(nodes, tuple)
    if not nodes:
        raise ValueError(f"{label}.nodes is empty: a body stands on at least one Node")
    seen: set[object] = set()
    for line in nodes:
        assert isinstance(line, dict)
        node = line["node"]
        if node in seen:
            assert isinstance(node, tuple)
            raise ValueError(f"{label}.nodes names the Node {list(node)} twice")
        seen.add(node)


def kept_levels(body: Mapping[str, object], label: str) -> None:
    """The rule between a level and its level before (the KEEP step of the body's form): a body that declares its spin declares spin_before, and spin_before stands beside spin alone."""
    if ("spin" in body) != ("spin_before" in body):
        declared, missing = ("spin", "spin_before") if "spin" in body else ("spin_before", "spin")
        raise ValueError(
            f"{label} declares {declared} without {missing}: the spin's two levels are declared together"
        )


def counted_giver(body: Mapping[str, object], label: str) -> None:
    """The rule between an emitter and its body in the law's form: the given family is the body's own or one it stocks."""
    if "emitter" not in body:
        return
    given = cast(Mapping[str, object], body["emitter"])["family"]
    stocked = "stocks" in body and given in cast(Mapping[str, object], body["stocks"])
    if given != body["family"] and not stocked:
        raise ValueError(f"{label}.emitter gives {given!r}, a family the body neither is nor stocks")


def bodies(value: object, context: Context) -> tuple[dict[str, object], ...]:
    """The bodies of the world file, each against the schema of its form with the families known; an unknown key, a missing key, a wrong kind and a family the universe lacks refused by name; the rules between the keys (the spin's two levels together; in the law's form the Nodes and the giver's family)."""
    if not isinstance(value, list):
        raise ValueError("measured must be a list")
    checked = []
    for index, entry in enumerate(value):
        label = f"measured[{index}]"
        kind = body_form(entry, label)
        found = check(entry, kind, label, context)
        assert isinstance(found, dict)
        kept_levels(found, label)
        if kind is COUNTED:
            counted_nodes(found, label)
            counted_giver(found, label)
        checked.append(found)
    return tuple(checked)


def detectors(value: object) -> tuple[dict[str, object], ...]:
    """The detectors of the world file, each against the detector's schema."""
    if not isinstance(value, list):
        raise ValueError("detectors must be a list")
    checked = []
    for index, entry in enumerate(value):
        found = check(entry, DETECTOR, f"detectors[{index}]", Context())
        assert isinstance(found, dict)
        checked.append(found)
    return tuple(checked)


def start(value: str, files: Mapping[str, object]) -> EngineStart:
    """The start file read: its mode and nothing else."""
    label = f"the engine start file {value!r}"
    checked = check(document_of("engine", value, files, label), START, label, Context())
    assert isinstance(checked, dict)
    return EngineStart(value, str(checked["mode"]))

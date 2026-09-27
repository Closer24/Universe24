"""The frame of the run's files read through the schemas: the universe file, its integers by the frame's schema and each family's entry by the cards of the register with the frame's one key, the name; and the start file, its mode; every key refused by name, no default written here (ALGEBRA.md 9.117 item 2: a term is one line of the files)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from event_universe.core.register import Register
from event_universe.core.schema import Context, Integer, ListOf, ObjectOf, OneOf, Word, check
from event_universe.loader import cards

# the universe's integers (ALGEBRA.md 9.83 (2) (a), 9.91 (7), 9.96 (1), (2)): Gamma the Node clock, A the amplitude bound, Lambda the charge's read weight, Q the momentum's unit, and the twist table of exact triples [c, s, d] read as written and checked with Gamma and A where the transport is built
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
# the start file (ALGEBRA.md 9.83 (2) (a)): the run's mode, check (every measured event read beside its blind expectation, no pin compared) or pin (the pins compared); no law's name, no version
START = ObjectOf({"mode": OneOf(("check", "pin"))})


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
    """A family's entry: the frame's key, its name, and every key the cards declare at a family's entry, optional where a card says so."""
    declared = cards.at(register, "a family's entry")
    return ObjectOf({"name": Word(), **declared.keys}, declared.optional)


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
    entries = document["families"]
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{label}.families must be a nonempty list")
    names = tuple(
        entry["name"]
        for entry in entries
        if isinstance(entry, dict) and "name" in entry and isinstance(entry["name"], str)
    )
    context = Context(
        names, {key: number for key, number in integers.items() if isinstance(number, int)}
    )
    kind = entry_kind(register)
    checked = []
    for index, entry in enumerate(entries):
        found = check(entry, kind, f"{label}.families[{index}]", context)
        assert isinstance(found, dict)
        checked.append(found)
    return tuple(checked), integers


def start(value: str, files: Mapping[str, object]) -> EngineStart:
    """The start file read: its mode and nothing else."""
    label = f"the engine start file {value!r}"
    checked = check(document_of("engine", value, files, label), START, label, Context())
    assert isinstance(checked, dict)
    return EngineStart(value, str(checked["mode"]))

"""The generic loader of the universe file: core's integers block and, for a family, every folder's keys under the word "family", read by core.schema and refused by name; no default, no family's name, no number of the universe."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from event_universe.core.register import Register
from event_universe.core.schema import Key, read_object

UNIVERSE: tuple[Key, ...] = (
    Key("node_clock", "int", low=1, section="9.83 (2) (a); 9.91 (7)"),
    Key("amplitude_bound", "int", low=1, section="9.83 (2) (a); 9.91 (7)"),
    Key("Lambda", "int", low=1, section="9.91 (7)"),
    Key("momentum_unit", "int", low=1, section="9.96 (1)"),
    Key(
        "twist_table",
        "object",
        keys=(Key("unit", "int", low=1), Key("fine", "list"), Key("coarse", "list")),
        section="9.96 (2)",
    ),
)
UNIVERSE_INTEGERS: tuple[str, ...] = tuple(key.name for key in UNIVERSE)
FILE: tuple[Key, ...] = (
    Key("integers", "object", keys=UNIVERSE, section="9.83 (2) (a); 9.91 (7); 9.96 (2)"),
    Key("families", "list", low=1, section="9.86 (2); 9.91 (7)"),
)


def family_keys(register: Register) -> tuple[Key, ...]:
    """The keys of one family: its name, then every folder's keys under "family" in the folders' order."""
    return (Key("name", "name", section="9.91 (7)"), *register.keys("family"))


def role_check(values: Mapping[str, object], keys: tuple[Key, ...], where: str) -> None:
    """A family with none of the keys that give a role is refused naming them in the keys' order."""
    roles = [key for key in keys if key.role]
    if roles and not any(key.name in values for key in roles):
        named = " nor ".join(f"{key.name} ({key.role})" for key in roles)
        raise ValueError(
            f"{where} declares neither {named}: a family does at least one (ALGEBRA.md 9.86 (2))"
        )


def load_universe(
    value: str, files: Mapping[str, object], register: Register
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """The universe file at `value` read through the schemas: the integers first (every bound resolves against them), then each family by the register's keys; the checked values in the file's own words."""
    if value not in files:
        raise ValueError(f"universe names {value!r}, no file at the repository's root")
    where = f"the universe file {value!r}"
    document = read_object(FILE, files[value], where, {})
    integers = document["integers"]
    entries = document["families"]
    assert isinstance(integers, dict) and isinstance(entries, list)
    keys = family_keys(register)
    families: list[dict[str, Any]] = []
    for index, entry in enumerate(entries):
        family = read_object(keys, entry, f"{where}.families[{index}]", integers)
        role_check(family, keys, f"{where}.families[{index}]")
        families.append(family)
    return families, integers

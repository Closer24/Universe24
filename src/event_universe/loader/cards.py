"""The cards' schemas collected from the register: at every place of the files, the keys the folders declare, each key one folder's; two folders claiming one key at one place are refused by name (ALGEBRA.md #the-primitives: a term is one line of the files, read by the folder it names)."""

from __future__ import annotations

from event_universe.core.register import Register
from event_universe.core.schema import FILE_PLACES, Kind, ObjectOf


def owners(register: Register) -> dict[str, dict[str, str]]:
    """At every place, each declared key and the name of the one folder that declares it; a key two folders declare at one place is refused by name."""
    found: dict[str, dict[str, str]] = {place: {} for place in FILE_PLACES}
    for declaration in register.declarations.values():
        if declaration.schema is None:
            continue
        for place, shape in declaration.schema.places.items():
            for key in shape.keys:
                other = found[place].get(key)
                if other is not None:
                    raise ValueError(
                        f"the key {key!r} at {place} is declared by both {other!r} and "
                        f"{declaration.name!r}: one key, one folder"
                    )
                found[place][key] = declaration.name
    return found


def at(register: Register, place: str) -> ObjectOf:
    """The keys every folder declares at one place, as one object kind: each key its folder's kind, optional where its folder says so."""
    if place not in FILE_PLACES:
        raise ValueError(f"no place {place!r} in the files: the places are {list(FILE_PLACES)}")
    owners(register)
    keys: dict[str, Kind] = {}
    optional: set[str] = set()
    for declaration in register.declarations.values():
        shape = None if declaration.schema is None else declaration.schema.places.get(place)
        if shape is None:
            continue
        keys.update(shape.keys)
        optional |= set(shape.optional)
    return ObjectOf(keys, frozenset(optional))

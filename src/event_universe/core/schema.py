"""The kinds of a value of the run's files and one generic check: a folder's schema names its keys, where they live and each key's kind (an object of named keys, a list, a mapping of names to values among them); the check refuses an unknown key, a missing key, a wrong kind, a value beyond its bound, an empty word and a name the universe lacks, each by name; no key of any folder is written here, no default, no number of the universe (ALGEBRA.md #the-primitives: a term is one line of the files)."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field

# where a key of the files lives: the universe file's integers, one family's entry of it, one body of the world file, the world file itself, the start file
FILE_PLACES: tuple[str, ...] = ("the integers", "a family's entry", "a body", "the world", "the start")


@dataclass(frozen=True)
class Integer:
    """An integer as written; its least and its most each an integer, the name of an integer of the universe, or None for no bound."""

    least: int | str | None = None
    most: int | str | None = None


@dataclass(frozen=True)
class Flag:
    """true or false."""


@dataclass(frozen=True)
class OneOf:
    """One of the values listed, an integer or a word, exactly as written."""

    choices: tuple[object, ...]


@dataclass(frozen=True)
class Word:
    """A word: a nonempty string."""


@dataclass(frozen=True)
class Name:
    """The name of a family of the universe."""


@dataclass(frozen=True)
class IntegerName:
    """The name of an integer of the universe, read as that integer."""


@dataclass(frozen=True)
class ListOf:
    """A list of values of one kind, of the length given or of any length."""

    of: Kind
    length: int | None = None


@dataclass(frozen=True)
class ObjectOf:
    """An object with the keys given, each of its kind; a key named optional may be absent; no other key."""

    keys: Mapping[str, Kind]
    optional: frozenset[str] = frozenset()


@dataclass(frozen=True)
class MapOf:
    """An object whose keys are all of one kind (a family's name) and whose values are all of one kind; any keys, each once."""

    keys: Kind
    of: Kind


@dataclass(frozen=True)
class Either:
    """A value the first of the kinds accepts."""

    kinds: tuple[Kind, ...]


Kind = Integer | Flag | OneOf | Word | Name | IntegerName | ListOf | ObjectOf | MapOf | Either


@dataclass(frozen=True)
class Schema:
    """A folder's keys of the files by the place they live at (one of FILE_PLACES), each place an ObjectOf of its keys with the ones that may be absent; iterated, it gives every key."""

    places: Mapping[str, ObjectOf]

    def __post_init__(self) -> None:
        beyond = set(self.places) - set(FILE_PLACES)
        if beyond:
            raise ValueError(
                f"a schema at {sorted(beyond)}: the places of the files are {list(FILE_PLACES)}"
            )
        for place, shape in self.places.items():
            lacking = set(shape.optional) - set(shape.keys)
            if lacking:
                raise ValueError(
                    f"a schema at {place!r} names optional keys it lacks: {sorted(lacking)}"
                )

    def __iter__(self) -> Iterator[str]:
        for shape in self.places.values():
            yield from shape.keys


@dataclass(frozen=True)
class Context:
    """What a check resolves names against: the families' names and the universe's integers, both from the files."""

    families: tuple[str, ...] = ()
    integers: Mapping[str, int] = field(default_factory=dict)


def bound_of(bound: int | str | None, context: Context, label: str) -> int | None:
    """A bound as an integer: as written, or the universe's integer of that name, refused by name when the universe lacks it."""
    if isinstance(bound, str):
        if bound not in context.integers:
            raise ValueError(
                f"{label} is bounded by {bound!r}, which names no integer of the universe "
                f"(the integers: {sorted(context.integers)})"
            )
        return context.integers[bound]
    return bound


def check_keys(
    value: object, keys: Mapping[str, Kind], optional: frozenset[str], label: str, context: Context
) -> dict[str, object]:
    """An object's keys against the kinds: an unknown key, a missing key and a wrong value refused by name; the checked values returned under their keys."""
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object with the keys {sorted(keys)}")
    unknown = set(value) - set(keys)
    if unknown:
        raise ValueError(
            f"{label} has unknown keys: {', '.join(sorted(unknown))} (the keys: {', '.join(sorted(keys))})"
        )
    missing = set(keys) - set(optional) - set(value)
    if missing:
        raise ValueError(f"{label} lacks keys: {', '.join(sorted(missing))}")
    return {key: check(value[key], keys[key], f"{label}.{key}", context) for key in keys if key in value}


def check(value: object, kind: Kind, label: str, context: Context) -> object:
    """One value against its kind, refused by name where it is not of the kind; the checked value returned (a list as a tuple, an integer's name as the integer)."""
    if isinstance(kind, Integer):
        if type(value) is not int:
            raise ValueError(f"{label} must be an integer, not {value!r}")
        least = bound_of(kind.least, context, label)
        most = bound_of(kind.most, context, label)
        if least is not None and value < least:
            raise ValueError(f"{label} is {value}, below its least {kind.least!r}")
        if most is not None and value > most:
            raise ValueError(f"{label} is {value}, above its most {kind.most!r}")
        return value
    if isinstance(kind, Flag):
        if not isinstance(value, bool):
            raise ValueError(f"{label} must be true or false, not {value!r}")
        return value
    if isinstance(kind, OneOf):
        if not any(type(value) is type(choice) and value == choice for choice in kind.choices):
            raise ValueError(f"{label} must be one of {list(kind.choices)}, not {value!r}")
        return value
    if isinstance(kind, Word):
        if not isinstance(value, str) or not value:
            raise ValueError(f"{label} must be a word, not {value!r}")
        return value
    if isinstance(kind, Name):
        if not isinstance(value, str) or value not in context.families:
            raise ValueError(
                f"{label} names {value!r}, no family of the universe (the families: {list(context.families)})"
            )
        return value
    if isinstance(kind, IntegerName):
        if not isinstance(value, str) or value not in context.integers:
            raise ValueError(
                f"{label} names {value!r}, no integer of the universe (the integers: {sorted(context.integers)})"
            )
        return context.integers[value]
    if isinstance(kind, ListOf):
        if not isinstance(value, list):
            raise ValueError(f"{label} must be a list, not {value!r}")
        if kind.length is not None and len(value) != kind.length:
            raise ValueError(f"{label} must be a list of {kind.length}, not of {len(value)}")
        return tuple(
            check(item, kind.of, f"{label}[{index}]", context) for index, item in enumerate(value)
        )
    if isinstance(kind, ObjectOf):
        return check_keys(value, kind.keys, kind.optional, label, context)
    if isinstance(kind, MapOf):
        if not isinstance(value, dict):
            raise ValueError(f"{label} must be an object mapping names to values, not {value!r}")
        return {
            key: check(item, kind.of, f"{label}[{key!r}]", context)
            for key, item in value.items()
            if check(key, kind.keys, f"{label} key {key!r}", context) is not None
        }
    if isinstance(kind, Either):
        refusals = []
        for option in kind.kinds:
            try:
                return check(value, option, label, context)
            except ValueError as refusal:
                refusals.append(str(refusal))
        raise ValueError("; or ".join(refusals))
    raise TypeError(f"{label}: {kind!r} is no kind of this module")

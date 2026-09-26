"""The schema language of the run's files: a key with its kind, bounds and admitted words, and one reader that checks a JSON object against a tuple of keys and refuses by name; integers and names only, no default."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

# the int64 room of a file's integer: a bound of the representation, no key's value
AMOUNT_BOUND = (1 << 62) - 1
KINDS: tuple[str, ...] = ("int", "bool", "one", "name", "pair", "list", "object")
Bound = int | str | tuple[int, str] | None
Universe = Mapping[str, object]


@dataclass(frozen=True)
class Key:
    """One key of a schema: its name and kind; required or admitted absent (a key with a role is absent or present, its presence giving the object the role); an int's bounds, a pair's from `low`, a list's length, each an integer, a universe integer's key or (factor, key); the literals admitted beside the kind (`also`); a `one` kind's values; `named` where a universe integer's key stands for the int; a list's item; an object's keys; the ALGEBRA.md line."""

    name: str
    kind: str
    required: bool = True
    low: Bound = None
    high: Bound = None
    also: tuple[object, ...] = ()
    values: tuple[object, ...] = ()
    named: bool = False
    role: str = ""
    items: Key | None = None
    keys: tuple[Key, ...] = ()
    section: str = ""


def integer_names(universe: Universe) -> list[str]:
    """The keys of the universe's integers, sorted, for a refusal."""
    return sorted(name for name, value in universe.items() if type(value) is int)


def bound(value: Bound, universe: Universe, where: str) -> tuple[int | None, str]:
    """A bound as its integer and its printed form: an integer, a universe integer by its key, or a factor times one."""
    if value is None:
        return None, ""
    if isinstance(value, int):
        return value, str(value)
    factor, name = (1, value) if isinstance(value, str) else value
    found = universe.get(name)
    if type(found) is not int:
        raise ValueError(
            f"{where}: its schema names the bound {name!r}, which the universe's integers lack "
            f"(the integers: {integer_names(universe)})"
        )
    times = f"{factor} x " if factor != 1 else ""
    return factor * found, f"{times}{name} = {factor * found}"


def cite(key: Key) -> str:
    """The key's ALGEBRA.md line for a refusal, or nothing."""
    return f" (ALGEBRA.md {key.section})" if key.section else ""


def beside(key: Key) -> str:
    """The literals admitted beside the kind, worded for a refusal."""
    if len(key.also) == 1 and isinstance(key.also[0], str):
        return f" or the word {key.also[0]!r}"
    return f" or one of {list(key.also)}" if key.also else ""


def counted(low_text: str, high_text: str) -> str:
    """A list's admitted length, worded for a refusal."""
    if low_text and high_text:
        return f" of {low_text} to {high_text} items"
    if low_text:
        return f" of at least {low_text} items"
    return f" of at most {high_text} items" if high_text else ""


def same(value: object, admitted: object) -> bool:
    """Whether a file's value is one admitted literal, by kind and value at every depth, so 1 is not true."""
    if isinstance(admitted, list):
        return (
            isinstance(value, list)
            and len(value) == len(admitted)
            and all(same(item, other) for item, other in zip(value, admitted, strict=True))
        )
    return type(value) is type(admitted) and value == admitted


def read_int(key: Key, value: object, where: str, universe: Universe) -> int:
    """An integer within the key's bounds, or a universe integer by its key where the key is named."""
    if key.named and isinstance(value, str):
        found = universe.get(value)
        if type(found) is not int:
            raise ValueError(
                f"{where} {value!r} names no integer of the universe (the integers: "
                f"{integer_names(universe)})"
            )
        value = found
    low, low_text = bound(key.low, universe, where)
    high, high_text = bound(key.high, universe, where)
    if low is None:
        low, low_text = -AMOUNT_BOUND, str(-AMOUNT_BOUND)
    if high is None:
        high, high_text = AMOUNT_BOUND, str(AMOUNT_BOUND)
    if type(value) is not int or value < low or value > high:
        names = " or a universe integer's key" if key.named else ""
        raise ValueError(
            f"{where} must be an integer from {low_text} through {high_text}{names}{beside(key)}, "
            f"not {value!r}{cite(key)}"
        )
    return value


def read_pair(key: Key, value: object, where: str, universe: Universe) -> list[int]:
    """Two integers [num, den], each from the key's low."""
    low, low_text = bound(key.low, universe, where)
    if (
        isinstance(value, list)
        and len(value) == 2
        and all(type(item) is int and (low is None or item >= low) for item in value)
    ):
        return [int(item) for item in value]
    from_low = f" (two integers from {low_text})" if low is not None else ""
    raise ValueError(f"{where} must be [num, den]{beside(key)}{from_low}, not {value!r}{cite(key)}")


def read_list(key: Key, value: object, where: str, universe: Universe) -> list[object]:
    """A list within the key's length bounds, each item read by the key's item, or as written without one."""
    low, low_text = bound(key.low, universe, where)
    high, high_text = bound(key.high, universe, where)
    short = low is not None and isinstance(value, list) and len(value) < low
    long = high is not None and isinstance(value, list) and len(value) > high
    if not isinstance(value, list) or short or long:
        raise ValueError(
            f"{where} must be a list{counted(low_text, high_text)}, not {value!r}{cite(key)}"
        )
    if key.items is None:
        return list(value)
    return [
        read_value(key.items, item, f"{where}[{index}]", universe) for index, item in enumerate(value)
    ]


def read_object(
    keys: tuple[Key, ...], value: object, where: str, universe: Universe
) -> dict[str, object]:
    """The object's keys against `keys`: unknown keys refused first, then missing required ones, then each present value by its key, returned in the keys' order and no other."""
    names = [key.name for key in keys]
    if not isinstance(value, dict):
        raise ValueError(f"{where} must be a JSON object with the keys {names}, not {value!r}")
    unknown = sorted(str(name) for name in set(value) - set(names))
    if unknown:
        raise ValueError(f"{where} has unknown keys: {', '.join(unknown)} (the keys: {names})")
    missing = sorted(key.name for key in keys if key.required and not key.role and key.name not in value)
    if missing:
        raise ValueError(f"{where} lacks keys: {', '.join(missing)} (the keys: {names})")
    return {
        key.name: read_value(key, value[key.name], f"{where}.{key.name}", universe)
        for key in keys
        if key.name in value
    }


def read_value(key: Key, value: object, where: str, universe: Universe) -> object:
    """One value read by its key: a literal of `also` as written, else by the kind."""
    if any(same(value, admitted) for admitted in key.also):
        return value
    if key.kind == "int":
        return read_int(key, value, where, universe)
    if key.kind == "bool":
        if type(value) is not bool:
            raise ValueError(f"{where} must be true or false, not {value!r}{cite(key)}")
        return value
    if key.kind == "one":
        if not any(same(value, admitted) for admitted in key.values):
            raise ValueError(f"{where} must be one of {list(key.values)}, not {value!r}{cite(key)}")
        return value
    if key.kind == "name":
        if not isinstance(value, str) or not value:
            raise ValueError(f"{where} must be a name, a nonempty string, not {value!r}{cite(key)}")
        return value
    if key.kind == "pair":
        return read_pair(key, value, where, universe)
    if key.kind == "list":
        return read_list(key, value, where, universe)
    if key.kind == "object":
        return read_object(key.keys, value, where, universe)
    raise ValueError(f"the schema's key {key.name!r} has the kind {key.kind!r}, none of {list(KINDS)}")

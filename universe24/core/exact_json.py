"""Exact JSON with arbitrary integer decimal transport and no global settings.

Python's ordinary JSON encoder converts ints with ``str`` and its decoder uses
``int``. Both can reject otherwise valid arbitrary integers at a process-wide
decimal digit limit. Nine-digit conversion chunks avoid that limit locally,
while preserving the standard decimal representation and existing hashes.

Only JSON data without floats is accepted. This is serialization, never a
change to Engine arithmetic or a tagged encoding of the retained state.
"""
from __future__ import annotations

import json as _json

_BASE = 1_000_000_000


def _decimal(value: int) -> str:
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    value = abs(value)
    chunks = []
    while value:
        value, part = divmod(value, _BASE)
        chunks.append(part)
    return sign + str(chunks[-1]) + "".join(f"{part:09d}" for part in reversed(chunks[:-1]))


def _integer(text: str) -> int:
    negative = text.startswith("-")
    digits = text[1:] if negative else text
    value = 0
    first = len(digits) % 9 or 9
    value = int(digits[:first])
    for index in range(first, len(digits), 9):
        value = value * _BASE + int(digits[index:index + 9])
    return -value if negative else value


def _reject_number(text):
    raise ValueError(f"exact JSON forbids floating point/non-finite number {text}")


def dumps(value, *, sort_keys=False, separators=(",", ":"), ensure_ascii=True, allow_nan=False) -> str:
    """Serialize exact JSON data, byte-compatible with stdlib compact JSON.

    Dictionary keys must be strings. Tuples are encoded as arrays, as in the
    standard encoder. ``allow_nan`` cannot permit inexact/non-finite numbers.
    """
    if type(sort_keys) is not bool or type(ensure_ascii) is not bool:
        raise TypeError("JSON sorting/ascii options must be bools")
    if allow_nan is not False:
        raise ValueError("exact JSON never permits NaN")
    if (type(separators) not in (tuple, list) or len(separators) != 2
            or any(type(item) is not str for item in separators)):
        raise TypeError("separators must be two strings")
    item_sep, key_sep = separators
    active = set()

    def encode(item):
        kind = type(item)
        if item is None:
            return "null"
        if kind is bool:
            return "true" if item else "false"
        if kind is int:
            return _decimal(item)
        if kind is str:
            return _json.dumps(item, ensure_ascii=ensure_ascii)
        if kind in (dict, list, tuple):
            identity = id(item)
            if identity in active:
                raise ValueError("circular JSON data")
            active.add(identity)
            try:
                if kind is dict:
                    if any(type(key) is not str for key in item):
                        raise TypeError("exact JSON object keys must be strings")
                    keys = sorted(item) if sort_keys else item.keys()
                    return "{" + item_sep.join(encode(key) + key_sep + encode(item[key]) for key in keys) + "}"
                return "[" + item_sep.join(encode(child) for child in item) + "]"
            finally:
                active.remove(identity)
        raise TypeError(f"exact JSON cannot encode {kind.__name__}")

    return encode(value)


def loads(value, **kwargs):
    """Parse standard JSON with unbounded decimal integers and exact defaults.

    Object hooks and other stdlib decoding options are forwarded. Callers can
    provide their own float/constant rejectors for domain-specific errors.
    """
    kwargs.setdefault("parse_int", _integer)
    kwargs.setdefault("parse_float", _reject_number)
    kwargs.setdefault("parse_constant", _reject_number)
    return _json.loads(value, **kwargs)

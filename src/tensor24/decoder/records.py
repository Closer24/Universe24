"""The record read: one record of the schema 1.0 into its header, its events and its end, or the cause it is not."""

# The schema's rules are its guards, checked in order as it reads (Animate): the file reads; every line is a JSON
# object with its kind; the record holds a header and an end; the header comes first, with a whole major version that
# is known; the end comes last; every event is of a known kind, stands at a whole round and site, and keeps the
# schema's order (round, kind, site, train). A record that breaks a rule is not read, and the cause is named: nothing
# is raised. The standard library and the record's schema alone.

import json
from collections.abc import Callable
from typing import Any, TypeGuard

from tensor24.record.schema import MAJOR

KINDS = ("whole", "split", "turnover", "rate", "books")  # the events' order within a round, the schema's
PLACE = ("round", "site")

Line = dict[str, Any]
Guard = Callable[[list[Line | None]], str]


class Record:
    """A record read: its header, its events in the schema's order, and its end."""

    def __init__(self, header: Line, events: list[Line], end: Line) -> None:
        self.header, self.events, self.end = header, events, end

    def of(self, kind: str) -> list[Line]:
        """The events of one kind, in order."""
        return [e for e in self.events if e["kind"] == kind]


def whole(value: Any) -> TypeGuard[int]:
    """A whole number, and not a truth value."""
    return isinstance(value, int) and not isinstance(value, bool)


def parsed(text: str) -> Line | None:
    """A line as a JSON object with its kind, or None."""
    try:
        line = json.loads(text)
    except json.JSONDecodeError:
        return None
    return line if isinstance(line, dict) and isinstance(line.get("kind"), str) else None


def place(e: Line) -> tuple[int, int, int, int]:
    """An event's place in the schema's order; an event with no train stands at train 0 of its site."""
    train: int = e["train"] if whole(e.get("train")) else 0
    round_: int = e["round"]
    site: int = e["site"]
    return round_, KINDS.index(e["kind"]), site, train


def jsoned(lines: list[Line | None]) -> str:
    broken = [n for n, line in enumerate(lines, start=1) if line is None]
    return f"line {broken[0]} is no JSON object with its kind" if broken else ""


def framed(lines: list[Line | None]) -> str:
    return "the record holds no header and end" if len(lines) < len(("header", "end")) else ""


def headed(lines: list[Line | None]) -> str:
    first = lines[0]
    return "the first line is no header" if first is None or first["kind"] != "header" else ""


def majored(lines: list[Line | None]) -> str:
    first = lines[0]
    major = None if first is None else first.get("major")
    if not whole(major):
        return "the header holds no major version"
    return f"the major version {major} is unknown" if major != MAJOR else ""


def ended(lines: list[Line | None]) -> str:
    last = lines[-1]
    return "the last line is no end" if last is None or last["kind"] != "end" else ""


def events_of(lines: list[Line | None]) -> list[Line]:
    return [line for line in lines[1:-1] if line is not None]


def kinded(lines: list[Line | None]) -> str:
    unknown = sorted({e["kind"] for e in events_of(lines)} - set(KINDS))
    return f"the line kinds {unknown} are unknown" if unknown else ""


def placed(lines: list[Line | None]) -> str:
    events = events_of(lines)
    unplaced = [
        n for n, e in enumerate(events, start=1 + 1) if not all(whole(e.get(key)) for key in PLACE)
    ]
    return f"line {unplaced[0]} stands at no whole round and site" if unplaced else ""


def ordered(lines: list[Line | None]) -> str:
    places = [place(e) for e in events_of(lines)]
    return "the events stand out of the schema's order" if places != sorted(places) else ""


GUARDS: tuple[Guard, ...] = (jsoned, framed, headed, majored, ended, kinded, placed, ordered)


def lines_of(path: str) -> tuple[list[Line | None], str]:
    """The file's lines parsed, or the cause the file cannot be read."""
    try:
        with open(path, encoding="utf-8") as f:
            texts = f.read().splitlines()
    except OSError, UnicodeDecodeError:
        return [], "the record's file cannot be read"
    return [parsed(text) for text in texts], ""


def read(path: str, guards: tuple[Guard, ...] = GUARDS) -> tuple[Record | None, str]:
    """The record at path, or None and the cause it is not read: the first guard that names one."""
    lines, cause = lines_of(path)
    for guard in guards:
        cause = cause or guard(lines)
    if cause:
        return None, cause
    held = [line for line in lines if line is not None]
    return Record(held[0], held[1:-1], held[-1]), ""

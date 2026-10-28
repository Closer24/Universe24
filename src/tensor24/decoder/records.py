"""The record read: one record of the schema 1.0 into its header, its events and its end, or the cause it is not."""

# The schema's rules are its guards, checked in order as it reads (Animate): the file reads; every line is a JSON
# object with its kind, each key once; the record holds a header and an end; the header comes first, with a whole
# major version that is known; the end comes last; every event is of a known kind and stands at a whole round and
# site; every field a line holds has its shape in the schema's record of its kind, a whole number, a label, a row of
# them or a record of the schema, so a float, a truth value, NaN or a row of another length is seen (Sofer's G1 and
# G2); a whole click that takes at both ends books in its two ends alone, its own taken and laid empty, and one that
# takes at one end holds no end (G3); the events keep the schema's order (round, kind, site, train). A field may stand
# absent where its writer lacks it: a reading that needs it reads not read, the cause named. A record that breaks a
# rule is not read, and the cause is named: nothing is raised. The lines are split at the line feed alone, so U+2028,
# U+0085 and their kin stand inside a label as JSON lets them; a line nested past the interpreter's depth, or holding
# a whole number past its digits (sys.get_int_max_str_digits(), which the tool lifts), is no JSON object to the
# reader, and is named so. The ledger beside the record is read under its own guards: every line a JSON object, at a
# whole round and train, after the step or after the clicks, its fields of their shape, each place once. The standard
# library and the record's schema alone.

import dataclasses
import json
import typing
from collections.abc import Callable
from typing import Any, TypeGuard

from tensor24.record import schema

KINDS = ("whole", "split", "turnover", "rate", "books")  # the events' order within a round, the schema's
PLACE = ("round", "site")
ENDS = ("near", "far")  # a whole click's two ends, where it takes at both
AT = ("step", "clicks")  # a ledger line's place in its round: after the step, or after the clicks
ENTRY = ("round", "train")  # a ledger line's place beside its at

Line = dict[str, Any]
Guard = Callable[[list[Line | None]], str]
# each record of the schema by its lines' kind, with its fields' shapes
Shapes = dict[str, dict[str, Any]]


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


def keyed(pairs: list[tuple[str, Any]]) -> Line | None:
    """A JSON object whose every key stands once, or None."""
    line = dict(pairs)
    return line if len(line) == len(pairs) else None


def parsed(text: str) -> Line | None:
    """A line as a JSON object, or None: no JSON, a key twice, or a line past the interpreter's depth or digits."""
    try:
        line = json.loads(text, object_pairs_hook=keyed)
    # a JSONDecodeError is a ValueError, and so is a whole number past the interpreter's digits
    except ValueError, RecursionError:
        return None
    return line if isinstance(line, dict) else None


def schema_shapes() -> Shapes:
    """Each record of the schema by its lines' kind, its name in lower case, with its fields' shapes."""
    return {
        name.lower(): typing.get_type_hints(value)
        for name, value in vars(schema).items()
        if isinstance(value, type) and dataclasses.is_dataclass(value)
    }


def fits(value: Any, shape: Any, shapes: Shapes) -> bool:
    """Whether a value read from JSON has a field's shape: a whole number, a label, a row of them, or a record."""
    if shape is int:
        return whole(value)
    if shape is str:
        return isinstance(value, str)
    if isinstance(shape, type) and dataclasses.is_dataclass(shape):
        return isinstance(value, dict) and not misfit(value, shapes[shape.__name__.lower()], shapes)
    rows = typing.get_args(shape)
    if Ellipsis in rows:
        return isinstance(value, list) and all(fits(item, rows[0], shapes) for item in value)
    return (
        isinstance(value, list)
        and len(value) == len(rows)
        and all(fits(item, row, shapes) for item, row in zip(value, rows, strict=True))
    )


def misfit(line: Line, fields: dict[str, Any], shapes: Shapes) -> str:
    """The first field a line holds whose value has not its shape in the schema, or nothing."""
    wrong = [
        name for name, shape in fields.items() if name in line and not fits(line[name], shape, shapes)
    ]
    return wrong[0] if wrong else ""


def place(e: Line) -> tuple[int, int, int, int]:
    """An event's place in the schema's order; an event with no train stands at train 0 of its site."""
    train: int = e["train"] if whole(e.get("train")) else 0
    round_: int = e["round"]
    site: int = e["site"]
    return round_, KINDS.index(e["kind"]), site, train


def named(broken: list[int], cause: str) -> str:
    """The cause at the first broken line, its number in the cause's braces, or nothing."""
    return cause.format(broken[0]) if broken else ""


def jsoned(lines: list[Line | None]) -> str:
    return named(
        [
            n
            for n, line in enumerate(lines, start=1)
            if line is None or not isinstance(line.get("kind"), str)
        ],
        "line {} is no JSON object with its kind",
    )


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
    return f"the major version {major} is unknown" if major != schema.MAJOR else ""


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


def shaped(lines: list[Line | None]) -> str:
    shapes = schema_shapes()
    wrong = [
        (n, misfit(line, shapes[line["kind"]], shapes))
        for n, line in enumerate(lines, start=1)
        if line is not None and line["kind"] in shapes
    ]
    found = [(n, name) for n, name in wrong if name]
    return f"line {found[0][0]}'s {found[0][1]} has not its shape in the schema" if found else ""


def booked(lines: list[Line | None]) -> str:
    clicks = [
        (n, line)
        for n, line in enumerate(lines, start=1)
        if line is not None and line["kind"] == "whole"
    ]
    for n, click in clicks:
        ends = click.get("ends")
        if ends and (click.get("taken") or click.get("laid")):
            return f"line {n}'s whole click books at the click and again at its ends"
        if ends and len(ends) != len(ENDS):
            return (
                f"line {n}'s whole click's ends number {len(ends)}, where the schema holds both or none"
            )
    return ""


def ordered(lines: list[Line | None]) -> str:
    places = [place(e) for e in events_of(lines)]
    return "the events stand out of the schema's order" if places != sorted(places) else ""


GUARDS: tuple[Guard, ...] = (
    jsoned,
    framed,
    headed,
    majored,
    ended,
    kinded,
    placed,
    shaped,
    booked,
    ordered,
)


def objects(lines: list[Line | None]) -> str:
    return named(
        [n for n, line in enumerate(lines, start=1) if line is None],
        "the ledger's line {} is no JSON object",
    )


def standing(lines: list[Line | None]) -> str:
    return named(
        [
            n
            for n, line in enumerate(lines, start=1)
            if line is not None
            and not (all(whole(line.get(key)) for key in ENTRY) and line.get("at") in AT)
        ],
        "the ledger's line {} stands at no whole round and train, after the step or the clicks",
    )


def fitted(lines: list[Line | None]) -> str:
    shapes = schema_shapes()
    return named(
        [
            n
            for n, line in enumerate(lines, start=1)
            if line is not None and misfit(line, shapes["ledger"], shapes)
        ],
        "the ledger's line {} holds a field that has not its shape in the schema",
    )


def once(lines: list[Line | None]) -> str:
    places = [(line["round"], line["at"], line["train"]) for line in lines if line is not None]
    earliest: dict[tuple[int, str, int], int] = {}
    for n, entry in enumerate(places, start=1):
        earliest.setdefault(entry, n)
    return named(
        [n for n, entry in enumerate(places, start=1) if earliest[entry] != n],
        "the ledger's line {} stands at the round, the at and the train of an earlier line",
    )


LEDGER_GUARDS: tuple[Guard, ...] = (objects, standing, fitted, once)


def lines_of(path: str) -> tuple[list[Line | None], str]:
    """The file's lines, split at the line feed alone and parsed, or why the file is not read."""
    try:
        with open(path, encoding="utf-8", newline="") as f:
            texts = f.read().split("\n")
    except FileNotFoundError:
        return [], "is absent"
    except OSError, UnicodeDecodeError:
        return [], "cannot be read"
    return [parsed(text) for text in (texts[:-1] if texts[-1] == "" else texts)], ""


def guarded(path: str, guards: tuple[Guard, ...], whose: str) -> tuple[list[Line], str]:
    """A file's lines under its guards in order, or the cause the first guard names, or why the file is not read."""
    lines, cause = lines_of(path)
    cause = cause and f"the {whose} file {cause}"
    for guard in guards:
        cause = cause or guard(lines)
    return [line for line in lines if line is not None], cause


def read(path: str, guards: tuple[Guard, ...] = GUARDS) -> tuple[Record | None, str]:
    """The record at path, or None and the cause it is not read: the first guard that names one."""
    held, cause = guarded(path, guards, "record's")
    return (None, cause) if cause else (Record(held[0], held[1:-1], held[-1]), "")


def read_ledger(path: str, guards: tuple[Guard, ...] = LEDGER_GUARDS) -> tuple[list[Line] | None, str]:
    """The ledger at path, its lines in order, or None and the cause it is not read: the first guard that names one."""
    held, cause = guarded(path, guards, "ledger's")
    return (None, cause) if cause else (held, "")

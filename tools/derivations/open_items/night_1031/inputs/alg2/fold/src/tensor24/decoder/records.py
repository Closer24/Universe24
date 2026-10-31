"""The record read: one record of the schema into its header, its events and its end, or the cause it is not."""

# The schema's rules are its guards, checked in order as it reads (Animate): the file reads; every line is a JSON
# object with its kind, a label, each key once; the record holds a header and an end; the header comes first, with a
# version, a label, of the schema's own major; the end comes last; every event is of a known kind and stands at a whole round
# and site; every field a line holds has its shape in the schema's record of its kind, a whole number, a label, a row
# of them or a record of the schema, and a field the schema does not name holds whole numbers and labels alone,
# through its rows and mappings (the schema's first line), so a float, a truth value, NaN or null, or a row of
# another length, is seen (Sofer's G1 and G2); the header's sides make a board, each side 1 or more; the header's
# train cards name each train once, each card's winding 1 or more; an event's round stands from 1 to the end's rounds
# and its site on the board (the digests are the runner's, which the decoder never reads); a click line's train has a
# card, a line of no side holds no q 0, and a line stands once at its round, site and train (the first hostile code
# reader's M10); the events keep the schema's order (round, site, train); and every click line's sides, in its site and
# across a Mesh, close against their partners (sides.paired). A field may stand absent where its writer lacks it: a
# reading that needs it reads not read, the cause named. A record that breaks a rule is not read, and the cause is
# named in ASCII: a field's name and a kind as Python's ascii() writes them, so a line feed or a lone surrogate in a
# name stands escaped, and a board by its sides, never their product, which may pass the interpreter's digits;
# nothing is raised. The lines are split at the line feed alone, so U+2028, U+0085 and their kin stand inside a label
# as JSON lets them; a line nested past the interpreter's depth, or holding a whole number past its digits
# (sys.get_int_max_str_digits(), which the tool lifts), is named so. The ledger beside the record is read under its own
# guards: every line a JSON object, at a whole round and train, after the step, its fields of the Count line's shape,
# each place once. The standard library and the record's schema alone.

import dataclasses
import json
import typing
from collections.abc import Callable
from typing import Any, TypeGuard

from tensor24.decoder.sides import paired
from tensor24.record import schema

KINDS = ("click",)  # the events' kinds, the schema's
PLACE = ("round", "site")
AT = ("step",)  # a ledger line's place in its round: after the step
ENTRY = ("round", "train")  # a ledger line's place beside its at
NO_JSON = "is no JSON object"

Line = dict[str, Any]
Lines = list[Line | str]  # a file's lines read: each a JSON object, or the cause it is none
Guard = Callable[[Lines], str]
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


def parsed(text: str) -> Line | str:
    """A line as a JSON object, or the cause it is none: no JSON, a key twice, past the interpreter's depth or digits."""
    try:
        line = json.loads(text, object_pairs_hook=keyed)
    except json.JSONDecodeError:
        return NO_JSON
    except RecursionError:
        return "nests past the interpreter's depth"
    # a whole number past sys.get_int_max_str_digits(), which the tool lifts
    except ValueError:
        return "holds a whole number past the interpreter's digits"
    return line if isinstance(line, dict) else NO_JSON


def schema_shapes() -> Shapes:
    """Each record of the schema by its lines' kind, its name in lower case, with its fields' shapes."""
    return {
        name.lower(): typing.get_type_hints(value)
        for name, value in vars(schema).items()
        if isinstance(value, type) and dataclasses.is_dataclass(value)
    }


def leaves(value: Any) -> bool:
    """Whether a value is made of whole numbers and labels alone, through rows and mappings, walked with a stack."""
    left: list[Any] = [value]
    while left:
        item = left.pop()
        if isinstance(item, dict):
            left += item.values()
        elif isinstance(item, list):
            left += item
        elif not (whole(item) or isinstance(item, str)):
            return False
    return True


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
    paired = isinstance(value, list) and len(value) == len(rows)
    return paired and all(fits(item, row, shapes) for item, row in zip(value, rows, strict=True))


def misfit(line: Line, fields: dict[str, Any], shapes: Shapes) -> str:
    """The first field a line holds off its shape in the schema, a field the schema does not name off its leaves."""
    named = [
        name for name, shape in fields.items() if name in line and not fits(line[name], shape, shapes)
    ]
    unnamed = [name for name, value in line.items() if name not in fields and not leaves(value)]
    wrong = named + unnamed
    return wrong[0] if wrong else ""


def off(line: Line, rounds: Any, made: tuple[Any, Any]) -> str:
    """The first value of a line off the record: an event's round off the end's rounds, or its site off the board."""
    sides, size = made
    event = line["kind"] in KINDS
    if event and whole(rounds) and not 1 <= line["round"] <= rounds:
        return f"stands at round {line['round']}, off the record's rounds 1 to {rounds}"
    far = [
        s for s in ([line["site"]] if event else []) if whole(s) and whole(size) and not 0 <= s < size
    ]
    return f"names site {far[0]}, off the board of sides {sides}" if far else ""


def board(header: Any) -> tuple[Any, Any]:
    """The board the header's sides make: the sides and its sites, their product."""
    sides = header.get("sides") if isinstance(header, dict) else None
    if not (isinstance(sides, list) and sides):
        return None, None
    sites = 1
    for side in sides:
        sites = sites * side
    return sides, sites


def carded(header: Line) -> str:
    """The first train card off the record: a winding below 1, or a train an earlier card names; or nothing."""
    cards = header.get("trains", [])
    windings = [(n, t.get("winding")) for n, t in enumerate(cards, start=1)]
    low = [(n, w) for n, w in windings if whole(w) and w < 1]
    if low:
        return f"train card {low[0][0]} holds the winding {low[0][1]}, below 1"
    trains = [t["index"] for t in cards if whole(t.get("index"))]
    twice = [i for n, i in enumerate(trains) if i in trains[:n]]
    return f"train cards name the train {twice[0]} twice" if twice else ""


def place(e: Line) -> tuple[int, int, int, int]:
    """An event's place in the schema's order; an event with no train stands at train 0 of its site."""
    train: int = e["train"] if whole(e.get("train")) else 0
    round_: int = e["round"]
    site: int = e["site"]
    return round_, KINDS.index(e["kind"]), site, train


def named(broken: list[int], cause: str) -> str:
    """The cause at the first broken line, its number in the cause's braces, or nothing."""
    return cause.format(broken[0]) if broken else ""


def numbered(lines: Lines) -> list[tuple[int, Line]]:
    """The lines read as JSON objects, each with its number in the file, the first 1."""
    return [(n, line) for n, line in enumerate(lines, start=1) if isinstance(line, dict)]


def jsoned(lines: Lines) -> str:
    for n, line in enumerate(lines, start=1):
        if isinstance(line, str) and line != NO_JSON:
            return f"line {n} {line}"
        if isinstance(line, str) or not isinstance(line.get("kind"), str):
            return f"line {n} is no JSON object with its kind"
    return ""


def framed(lines: Lines) -> str:
    return "the record holds no header and end" if not lines[1:] else ""  # no line after the first


def headed(lines: Lines) -> str:
    first = lines[0]
    return (
        "the first line is no header" if not isinstance(first, dict) or first["kind"] != "header" else ""
    )


def versioned(lines: Lines) -> str:
    first = lines[0]
    version = first.get("version") if isinstance(first, dict) else None
    if not isinstance(version, str):
        return "the header holds no version"
    other = version.partition(".")[0] != schema.VERSION.partition(".")[0]
    return (
        f"the version {ascii(version)[1:-1]} is of another major than the schema's {schema.VERSION}"
        if other
        else ""
    )


def ended(lines: Lines) -> str:
    last = lines[-1]
    return "the last line is no end" if not isinstance(last, dict) or last["kind"] != "end" else ""


def events_of(lines: Lines) -> list[Line]:
    return [line for line in lines[1:-1] if isinstance(line, dict)]


def kinded(lines: Lines) -> str:
    unknown = sorted({e["kind"] for e in events_of(lines)} - set(KINDS))
    return f"the line kinds {ascii(unknown)} are unknown" if unknown else ""


def placed(lines: Lines) -> str:
    events = list(enumerate(lines, start=1))[1:-1]
    unplaced = [n for n, e in events if isinstance(e, dict) and not all(whole(e.get(k)) for k in PLACE)]
    return f"line {unplaced[0]} stands at no whole round and site" if unplaced else ""


def shaped(lines: Lines) -> str:
    shapes = schema_shapes()
    wrong = [
        (n, misfit(e, shapes[e["kind"]], shapes)) for n, e in numbered(lines) if e["kind"] in shapes
    ]
    # a field's name printed in ASCII, so a surrogate or a line feed in it stands escaped in the cause
    found = [f"line {n}'s {ascii(name)[1:-1]}" for n, name in wrong if name]
    return f"{found[0]} has not its shape in the schema" if found else ""


def valued(lines: Lines) -> str:
    made = board(lines[0])
    if made[0] and not all(side >= 1 for side in made[0]):
        return f"line 1's sides {made[0]} make no board, a side below 1"
    cards = carded(lines[0]) if isinstance(lines[0], dict) else ""
    if cards:
        return f"line 1's {cards}"
    end = lines[-1]
    rounds = end.get("rounds") if isinstance(end, dict) else None
    for n, line in enumerate(lines, start=1):
        cause = off(line, rounds, made) if isinstance(line, dict) else ""
        if cause:
            return f"line {n} {cause}"
    return ""


def clicked(lines: Lines) -> str:
    """The first click line off the train cards: a train no card names, q 0 on a line of no side in its site or across a Mesh, or an earlier click line's round, site and train."""
    header = lines[0] if isinstance(lines[0], dict) else {}
    keys = {t["index"]: t.get("key") for t in header.get("trains", []) if whole(t.get("index"))}
    seen: set[tuple[int, int, int, int]] = set()
    for n, e in [(n, e) for n, e in numbered(lines) if e["kind"] == "click"]:
        train = e.get("train")
        if whole(train) and train not in keys:
            return f"line {n} names train {train}, which no train card names"
        if e.get("q") == 0 and not (e.get("sides") or e.get("across")):
            return f"line {n} holds q 0 and no side, a line that carried nothing"
        if place(e) in seen:
            return f"line {n} stands at the round, the site and the train of an earlier click line"
        seen.add(place(e))
    return ""


def ordered(lines: Lines) -> str:
    places = [place(e) for e in events_of(lines)]
    return "the events stand out of the schema's order" if places != sorted(places) else ""


GUARDS: tuple[Guard, ...] = (
    jsoned,
    framed,
    headed,
    versioned,
    ended,
    kinded,
    placed,
    shaped,
    valued,
    clicked,
    ordered,
    paired,
)


def objects(lines: Lines) -> str:
    broken = [(n, line) for n, line in enumerate(lines, start=1) if isinstance(line, str)]
    return f"the ledger's line {broken[0][0]} {broken[0][1]}" if broken else ""


def standing(lines: Lines) -> str:
    stray = [
        n for n, e in numbered(lines) if not (all(whole(e.get(k)) for k in ENTRY) and e.get("at") in AT)
    ]
    return named(stray, "the ledger's line {} stands at no whole round and train, after the step")


def fitted(lines: Lines) -> str:
    shapes = schema_shapes()
    wrong = [n for n, e in numbered(lines) if misfit(e, shapes["count"], shapes)]
    return named(wrong, "the ledger's line {} holds a field that has not its shape in the schema")


def once(lines: Lines) -> str:
    places = [(e["round"], e["at"], e.get("site"), e["train"]) for e in lines if isinstance(e, dict)]
    earliest: dict[tuple[Any, ...], int] = {}
    for n, entry in enumerate(places, start=1):
        earliest.setdefault(entry, n)
    return named(
        [n for n, entry in enumerate(places, start=1) if earliest[entry] != n],
        "the ledger's line {} stands at the round, the at, the site and the train of an earlier line",
    )


LEDGER_GUARDS: tuple[Guard, ...] = (objects, standing, fitted, once)


def lines_of(path: str) -> tuple[Lines, str]:
    """The file's lines, split at the line feed alone and read, or why the file is not read."""
    try:
        with open(path, encoding="utf-8", newline="") as f:
            texts = f.read().split("\n")
    except FileNotFoundError:
        return [], "is absent"
    # a file that is no UTF-8 is a ValueError, and so is a path holding a NUL
    except OSError, ValueError:
        return [], "cannot be read"
    return [parsed(text) for text in (texts[:-1] if texts[-1] == "" else texts)], ""


def guarded(path: str, guards: tuple[Guard, ...], whose: str) -> tuple[list[Line], str]:
    """A file's lines under its guards in order, or the cause the first guard names, or why the file is not read."""
    lines, cause = lines_of(path)
    cause = cause and f"the {whose} file {cause}"
    for guard in guards:
        cause = cause or guard(lines)
    return [line for line in lines if isinstance(line, dict)], cause


def read(path: str, guards: tuple[Guard, ...] = GUARDS) -> tuple[Record | None, str]:
    """The record at path, or None and the cause it is not read: the first guard that names one."""
    held, cause = guarded(path, guards, "record's")
    return (None, cause) if cause else (Record(held[0], held[1:-1], held[-1]), "")


def read_ledger(path: str, guards: tuple[Guard, ...] = LEDGER_GUARDS) -> tuple[list[Line] | None, str]:
    """The ledger at path, its lines in order, or None and the cause it is not read: the first guard that names one."""
    held, cause = guarded(path, guards, "ledger's")
    return (None, cause) if cause else (held, "")

"""Clock: before the first round the files say which trains every Node-clock carries, how many stand on each axis, and which gears are laid where.
Algebra: whole numbers only, every side, part and integer at least 1, each departure refused by name; then the trains read against the engine's kinds.
Board: the three files read and checked, then laid out as the load's arrays; nothing else is laid: no coupling, strength, particle or mass.
Clicks: n/a: nothing the clicks show comes from the files.
"""

import json
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any, NamedTuple, TypeGuard

import numpy as np

# A kind among the 24's, a kind's whole basis and a gear's component within its train's rows are read against the
# engine's kinds once they are made (held_departures). The fine tooth within its teeth is the round's promise, read by
# the runner from outside before every round (run.promises). No file declares a coupling: the coupling family's one
# plan lays the terms at G3, so a universe's couplings are refused by name (RETIRED).

NAMES = ("universe", "piece", "setting")
VERSION = 1
OPERANDS = (
    "value",
    "gradient",
    "pull",
    "before",
    "after",
)  # the readings, in order, as the record's header names them
GEAR = ("train", "component", "site", "a", "b", "r")
AXES = ("x", "y", "z")
# the keys a file may leave out; the pinion's key is its own rule's
OPTIONAL = ("gears",)
# the keys that left the format, each refused with the reason it left
RETIRED = {
    "couplings": "no file declares a coupling; the coupling family's one plan lays the terms at G3"
}


def whole(value: Any) -> TypeGuard[int]:
    """An integer, and not a truth value."""
    return isinstance(value, int) and not isinstance(value, bool)


class Rule(NamedTuple):
    """What a field must hold, and the words that name it."""

    test: Callable[[Any], bool]
    wants: str


WHOLE = Rule(whole, "a whole number")
ONE = Rule(lambda v: whole(v) and v >= 1, "a whole number of at least 1")
NONE_BELOW = Rule(lambda v: whole(v) and v >= 0, "a whole number of at least 0")
LABEL = Rule(lambda v: isinstance(v, str) and v != "", "a label")
KINDS = Rule(
    lambda v: isinstance(v, list) and v != [] and all(map(LABEL.test, v)), "a list of the kinds' labels"
)
VERSIONED = Rule(lambda v: whole(v) and v == VERSION, f"{VERSION}")
SIDES = Rule(
    lambda v: isinstance(v, list) and len(v) == len(AXES) and all(map(ONE.test, v)),
    "one side per axis, each a whole number of at least 1",
)
# Each file's keys and what each holds: a rule, a mapping, a list of one train or more, or rows of the fields named.
# every key a literal, so that the gate reads each one (the note KEYS)
TRAIN = {"name": LABEL, "kinds": KINDS, "part": ONE, "pinion": None}
UNIVERSE = {
    "version": VERSIONED,
    "integers": {"den": ONE, "full_rate": ONE, "width": ONE},
    # the free strengths, each CHOSEN by name: the whole click's key (G5; its value G3's), the metric's push and the
    # volume's notch (G2)
    "chosen": {"key": ONE, "push": NONE_BELOW, "notch": NONE_BELOW},
    "trains": [TRAIN],
}
PIECE = {"version": VERSIONED, "shape": SIDES}
SETTING = {"version": VERSIONED, "ticks": NONE_BELOW, "gears": GEAR}


def once(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """A JSON object whose every key stands once: a doubled key would hide one of its values."""
    held = dict(pairs)
    if len(held) < len(pairs):
        raise ValueError(f"a key doubled among {[key for key, _ in pairs]}")
    return held


def read(path: Path) -> tuple[Any, list[str]]:
    """A file's content as JSON, or the reason it cannot be read, named: a nesting too deep to read among them."""
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=once), []
    except (OSError, ValueError, RecursionError) as error:
        return None, [f"{path.name}: not read: {error}"]


def numbers(held: Any) -> list[tuple[str, int]]:
    """Every whole number a file holds, at any depth, with the field it stands in, walked without recursion."""
    found: list[tuple[str, int]] = []
    left: list[tuple[str, Any]] = [("", held)]
    while left:
        where, value = left.pop()
        if isinstance(value, dict):
            left += [(f"{where}.{key}", item) for key, item in value.items()]
        elif isinstance(value, list):
            left += [(f"{where}[{at}]", item) for at, item in enumerate(value)]
        elif whole(value):
            found.append((where, value))
    return found


def rows(where: str, held: Any, fields: tuple[str, ...]) -> list[str]:
    """A list of rows, each of whole numbers, one per field."""
    if not isinstance(held, list):
        return [f"{where}: a list of rows, not {type(held).__name__}"]
    return [
        f"{where}[{at}]: a row of whole numbers, one per field ({', '.join(fields)}), not {row!r}"
        for at, row in enumerate(held)
        if not (isinstance(row, list) and len(row) == len(fields) and all(map(whole, row)))
    ]


def checked(where: str, held: Any, form: Any) -> list[str]:
    """Every way a value departs from its form in the table, each named where it stands, walked down the table."""
    if isinstance(form, dict):
        if not isinstance(held, dict):
            return [f"{where}: a mapping, not {type(held).__name__}"]
        found = [
            f"{where}: the key {key!r} is not in the format"
            + (f": {RETIRED[key]}" if key in RETIRED else "")
            for key in held
            if key not in form
        ]
        return found + [
            line
            for key, inner in form.items()
            if inner is not None and (key in held or key not in OPTIONAL)
            for line in checked(f"{where}.{key}", held.get(key), inner)
        ]
    if isinstance(form, list):
        if not (isinstance(held, list) and held):
            return [f"{where}: a list of one train or more"]
        return [line for at, item in enumerate(held) for line in checked(f"{where}[{at}]", item, *form)]
    if isinstance(form, Rule):
        return [] if form.test(held) else [f"{where}: {form.wants}, not {held!r}"]
    return rows(where, held, form)


def seed_departures(where: str, train: dict[str, Any], den: Any) -> list[str]:
    """A train's pinion at den, the seed's: a pinion off den is a mass laid by hand, and masses are measured only in clicks."""
    if not whole(den):
        return []  # the integers' own departure is named
    pinion = train.get("pinion")
    seed = whole(pinion) and pinion == den
    return (
        []
        if seed
        else [f"{where}.pinion: den, the seed's (masses are measured only in clicks), not {pinion!r}"]
    )


def universe_departures(universe: Any) -> list[str]:
    """Every way a universe file departs: its form, each train's pinion at den, and its labels."""
    found = checked("universe", universe, UNIVERSE)
    if not isinstance(universe, dict) or not isinstance(universe.get("trains"), list):
        return found
    trains, integers = universe["trains"], universe.get("integers")
    den = integers.get("den") if isinstance(integers, dict) else None
    for at, train in enumerate(trains):
        found += seed_departures(f"universe.trains[{at}]", train, den) if isinstance(train, dict) else []
    labels = Counter(t["name"] for t in trains if isinstance(t, dict) and isinstance(t.get("name"), str))
    found += [
        f"universe.trains: the label {name!r} names two trains or more"
        for name, count in sorted(labels.items())
        if count > 1
    ]
    return found


def sites_of(shape: list[int]) -> int:
    """The board's count of Node-clocks: the product of its sides."""
    sites = 1
    for side in shape:
        sites = sites * side
    return sites


def setting_departures(setting: Any, universe: Any, piece: Any) -> list[str]:
    """Every way a setting departs: its form, and its gears on the trains and the board, each given once."""
    found = checked("setting", setting, SETTING)
    gears = setting.get("gears", []) if not found else []
    trains, sites = len(universe["trains"]), sites_of(piece["shape"])
    given = Counter((t, c, x) for t, c, x, *_ in gears)
    for at, (train, component, site, _, _, _) in enumerate(gears):
        if not (0 <= train < trains and 0 <= site < sites):
            found.append(f"setting.gears[{at}]: train {train} or site {site} off the files")
        if not component >= 0:
            found.append(f"setting.gears[{at}]: component {component} below 0")
        if given[(train, component, site)] > 1:
            found.append(f"setting.gears[{at}]: the gear ({train}, {component}, {site}) given twice")
    return found


def departures(universe: Path, piece: Path, setting: Path) -> list[str]:
    """Every departure of the three files, the setting read once the universe and the piece stand, then the width, field by field."""
    (u, bad_u), (p, bad_p), (s, bad_s) = read(universe), read(piece), read(setting)
    found = bad_u + bad_p + bad_s
    found = found or universe_departures(u) + checked("piece", p, PIECE)
    found = found or setting_departures(s, u, p)
    width = 0 if found else u["integers"]["width"]
    return found or [
        f"{name}{where}: the integer {n} takes more bits than the width, {width}"
        for name, held in zip(NAMES, (u, p, s), strict=True)
        for where, n in numbers(held)
        if n.bit_length() > width
    ]


def vocabulary(kinds: Any, square: Any) -> tuple[tuple[str, ...], tuple[int, ...], tuple[Any, Any, Any]]:
    """The engine's kinds as the files are read against them: their labels and dimensions, each one's character on the 24, 1 where its basis is whole, and the four-vector's square's character; every kind 0 off the 24."""
    labels = tuple(name.upper() for name in kinds._fields)
    dims = tuple(k.shape[-1] for k in kinds)
    traces = np.stack([np.einsum("gii->g", k) for k in kinds])
    # whole: each row one Spoke's sign on the 24, its squares summing to 1 there and to 0 off them
    sums = [np.einsum("gij,gij->gi", k, k) for k in kinds]
    wholes = np.array([int((s * s == s).all()) for s in sums], dtype=object)
    return labels, dims, (traces, wholes, np.einsum("gii->g", square))


def held_departures(
    universe: Any, setting: Any, read: tuple[tuple[str, ...], tuple[int, ...], Any]
) -> list[str]:
    """Every way the checked files ask what the engine's kinds cannot hold: a kind none of the 24's, a kind with no whole basis outside the four-vector's square, a gear's component off its train's rows."""
    labels, dims, (traces, wholes, squared) = read
    found, sizes = [], []
    for at, train in enumerate(universe["trains"]):
        where = f"universe.trains[{at}]"
        found += [
            f"{where}.kinds[{j}]: {label!r} is none of the 24's kinds {labels}"
            for j, label in enumerate(train["kinds"])
            if label not in labels
        ]
        kinds = [labels.index(label) for label in train["kinds"] if label in labels]
        square = bool((train["part"] * traces[kinds].sum(axis=0) == squared).all())
        found += [
            f"{where}.kinds[{j}]: {label!r} has no whole basis the 24 permute, so it stands only in the four-vector's square, whose basis is whole"
            for j, label in enumerate(train["kinds"])
            if label in labels and not (square or wholes[labels.index(label)])
        ]
        sizes.append(train["part"] * sum(dims[k] for k in kinds))
    for at, (train, component, *_) in enumerate(setting.get("gears", [])):
        if component >= sizes[train]:
            found.append(
                f"setting.gears[{at}]: component {component} off train {train}'s {sizes[train]} rows"
            )
    return found


def entries(trains: list[dict[str, Any]], labels: tuple[str, ...]) -> tuple[Any, Any, Any]:
    """The held trains as the load's arrays: each kind's index among the engine's labels and its train's, in the file's order, and each train's part."""
    pairs = [(labels.index(label), at) for at, train in enumerate(trains) for label in train["kinds"]]
    kind, of = np.array(pairs, dtype=np.intp).T  # every train holds a kind or more, as the format has it
    return kind, of, np.array([train["part"] for train in trains], dtype=object)

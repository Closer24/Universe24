"""The three files read and checked: whole numbers alone, the integers and the sides at least 1, each train, kind, part and site referred to there."""

import json
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any, NamedTuple, TypeGuard

# The checker's one deferral: a gear's component within its train's rows, a kind among the 24's and a coupling's
# channel are the load's to refuse (runner/load.py), where the kinds are made; the fine tooth within the teeth is the
# load's where the teeth are read (stage 7b).

NAMES = ("universe", "piece", "setting")
VERSION = 1
INTEGERS = ("den", "full_rate", "key", "trace", "width")
PAIR = ("pinion", "sine")  # a hand's Gaussian pair over den; a train of one gear holds its pinion alone
COUPLING = (
    *("train", "kind", "part", "operand"),
    *("with_train", "with_kind", "with_part", "with_operand"),
    *("target", "target_kind", "target_part", "strength"),
)
OPERANDS = ("value", "gradient", "pull", "before", "after")  # the readings an operand names, in order
GEAR = ("train", "component", "site", "a", "b", "r")
AXES = ("x", "y", "z")
# the keys a file may leave out; the pair's keys are its own rule's
OPTIONAL = ("couplings", "gears", "weight")


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
TRAIN = {"name": LABEL, "kinds": KINDS, "part": ONE, **dict.fromkeys(PAIR), "weight": WHOLE}
UNIVERSE = {
    "version": VERSIONED,
    "integers": dict.fromkeys(INTEGERS, ONE),
    "trains": [TRAIN],
    "couplings": COUPLING,
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
        found = [f"{where}: the key {key!r} is not in the format" for key in held if key not in form]
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


def pair_departures(where: str, train: dict[str, Any], den: Any) -> list[str]:
    """A train's pinion within [0, den]; on a hand, a part above 1, its pair's other within [0, den] and the norm den den."""
    first, second = PAIR
    pinion, other = train.get(first), train.get(second)
    if not whole(den):
        return []  # the integers' own departure is named
    found = (
        []
        if whole(pinion) and 0 <= pinion <= den
        else [f"{where}.{first}: a whole number within [0, den], not {pinion!r}"]
    )
    if not (whole(train.get("part")) and train["part"] > 1):
        return found + (
            [] if other is None else [f"{where}.{second}: none on a train of one gear, not {other!r}"]
        )
    if not (whole(other) and 0 <= other <= den):
        return found + [f"{where}.{second}: on a hand, a whole number within [0, den], not {other!r}"]
    if found or not (whole(pinion) and whole(other)):
        return found
    norm = pinion * pinion + other * other
    off = f"{where}: the hand's pair ({pinion}, {other}) has the norm {norm}, not den den"
    return [] if norm == den * den else [off]


def universe_departures(universe: Any) -> list[str]:
    """Every way a universe file departs: its form, each train's pair over den, its labels, and its coupling rows."""
    found = checked("universe", universe, UNIVERSE)
    if not isinstance(universe, dict) or not isinstance(universe.get("trains"), list):
        return found
    trains, integers = universe["trains"], universe.get("integers")
    den = integers.get("den") if isinstance(integers, dict) else None
    for at, train in enumerate(trains):
        found += pair_departures(f"universe.trains[{at}]", train, den) if isinstance(train, dict) else []
    labels = Counter(t["name"] for t in trains if isinstance(t, dict) and isinstance(t.get("name"), str))
    found += [
        f"universe.trains: the label {name!r} names two trains or more"
        for name, count in sorted(labels.items())
        if count > 1
    ]
    for at, row in enumerate(universe.get("couplings", []) if not found else []):
        train, kind, part, operand, *other, target, target_kind, target_part, _ = row
        sides = ((train, kind, part, operand), tuple(other), (target, target_kind, target_part, 0))
        if not all(0 <= train < len(trains) for train, _, _, _ in sides):
            found.append(f"universe.couplings[{at}]: a train off the trains' rows")
        elif not all(0 <= kind < len(trains[train]["kinds"]) for train, kind, _, _ in sides):
            found.append(f"universe.couplings[{at}]: a kind off its train's")
        elif not all(0 <= part < trains[train]["part"] for train, _, part, _ in sides):
            found.append(f"universe.couplings[{at}]: a part off its train's")
        elif not all(0 <= operand < len(OPERANDS) for _, _, _, operand in sides):
            found.append(f"universe.couplings[{at}]: an operand off the readings {OPERANDS}")
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
    for at, (train, component, site, _, _, tooth) in enumerate(gears):
        if not (0 <= train < trains and 0 <= site < sites):
            found.append(f"setting.gears[{at}]: train {train} or site {site} off the files")
        if not (component >= 0 and tooth >= 0):
            found.append(f"setting.gears[{at}]: component {component} or fine tooth {tooth} below 0")
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

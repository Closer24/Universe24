"""The three files read and checked: whole numbers alone, the integers and the sides at least 1, every reference whole."""

import json
from collections import Counter
from pathlib import Path
from typing import Any, TypeGuard

# The checker's one deferral: a gear's component within its kind's dimension and its fine tooth within the teeth
# are the load's to refuse (stage 6), where the kinds and the teeth are read.

NAMES = ("universe", "piece", "setting")
VERSION = 1
UNIVERSE = ("version", "integers", "trains", "couplings")
INTEGERS = ("den", "full_rate", "key", "trace", "width")
TRAIN = ("name", "kinds", "part", "pair", "weight")
PAIR = ("pinion", "rim")
COUPLING = ("train", "part", "with_train", "with_part", "target", "strength")
PIECE = ("version", "shape")
SETTING = ("version", "ticks", "gears")
GEAR = ("train", "component", "site", "a", "b", "r")
AXES = ("x", "y", "z")


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


def whole(value: Any) -> TypeGuard[int]:
    """An integer, and not a truth value."""
    return isinstance(value, int) and not isinstance(value, bool)


def numbers(held: Any) -> list[int]:
    """Every whole number a file holds, at any depth, walked without recursion."""
    found, left = [], [held]
    while left:
        value = left.pop()
        if isinstance(value, dict | list):
            left += value.values() if isinstance(value, dict) else value
        elif whole(value):
            found.append(value)
    return found


def mapping(where: str, held: Any, names: tuple[str, ...]) -> list[str]:
    """A mapping whose every key the format names."""
    if not isinstance(held, dict):
        return [f"{where}: a mapping, not {type(held).__name__}"]
    return [f"{where}: the key {key!r} is not in the format" for key in held if key not in names]


def versioned(where: str, held: dict[str, Any]) -> list[str]:
    """The format's version, a whole number."""
    version = held.get("version")
    return (
        [] if whole(version) and version == VERSION else [f"{where}.version: {VERSION}, not {version!r}"]
    )


def rows(where: str, held: Any, fields: tuple[str, ...]) -> list[str]:
    """A list of rows, each of whole numbers, one per field."""
    if not isinstance(held, list):
        return [f"{where}: a list of rows, not {type(held).__name__}"]
    return [
        f"{where}[{at}]: a row of whole numbers, one per field ({', '.join(fields)}), not {row!r}"
        for at, row in enumerate(held)
        if not (isinstance(row, list) and len(row) == len(fields) and all(map(whole, row)))
    ]


def train_departures(where: str, train: Any, den: Any) -> list[str]:
    """Every way one train's row departs: its label, its kinds, its part, its pair and its weight."""
    found = mapping(where, train, TRAIN)
    if not isinstance(train, dict):
        return found
    name, kinds, part, pair = train.get("name"), train.get("kinds"), train.get("part"), train.get("pair")
    if not (isinstance(name, str) and name):
        found.append(f"{where}.name: a label, not {name!r}")
    if not (isinstance(kinds, list) and kinds and all(isinstance(kind, str) and kind for kind in kinds)):
        found.append(f"{where}.kinds: a list of the kinds' labels, not {kinds!r}")
    if not (whole(part) and part >= 1):
        found.append(f"{where}.part: a whole number of at least 1, not {part!r}")
    if not (isinstance(pair, list) and len(pair) == len(PAIR) and all(map(whole, pair))):
        found.append(f"{where}.pair: the pinion and the rim, two whole numbers, not {pair!r}")
    elif pair[1] != den:
        found.append(f"{where}.pair: the rim is den, not {pair[1]}")
    elif not 0 <= pair[0] <= pair[1]:
        found.append(f"{where}.pair: the pinion within [0, den], not {pair[0]}")
    if "weight" in train and not whole(train["weight"]):
        found.append(f"{where}.weight: a whole number, not {train['weight']!r}")
    return found


def universe_departures(universe: Any) -> list[str]:
    """Every way a universe file departs: its version, its integers, its trains and its coupling rows."""
    found = mapping("universe", universe, UNIVERSE)
    if found:
        return found
    integers, trains = universe.get("integers"), universe.get("trains")
    found += versioned("universe", universe) + mapping("universe.integers", integers, INTEGERS)
    if found or not (isinstance(trains, list) and trains):
        return found + (
            []
            if isinstance(trains, list) and trains
            else ["universe.trains: a list of one train or more"]
        )
    found += [
        f"universe.integers.{name}: a whole number of at least 1, not {integers.get(name)!r}"
        for name in INTEGERS
        if not (whole(integers.get(name)) and integers.get(name) >= 1)
    ]
    for at, train in enumerate(trains):
        found += train_departures(f"universe.trains[{at}]", train, integers.get("den"))
    labels = Counter(
        train["name"]
        for train in trains
        if isinstance(train, dict) and isinstance(train.get("name"), str)
    )
    found += [
        f"universe.trains: the label {name!r} names two trains or more"
        for name, count in sorted(labels.items())
        if count > 1
    ]
    couplings = universe.get("couplings", [])
    found += rows("universe.couplings", couplings, COUPLING)
    for at, (train, part, with_train, with_part, target, _) in enumerate(couplings if not found else []):
        if not all(0 <= end < len(trains) for end in (train, with_train, target)):
            found.append(f"universe.couplings[{at}]: a train off the trains' rows")
        elif not (0 <= part < trains[train]["part"] and 0 <= with_part < trains[with_train]["part"]):
            found.append(f"universe.couplings[{at}]: a part off its train's")
    return found


def piece_departures(piece: Any) -> list[str]:
    """Every way a piece file departs: its version and its shape, one side of at least 1 per axis."""
    found = mapping("piece", piece, PIECE)
    if found:
        return found
    found += versioned("piece", piece)
    shape = piece.get("shape")
    if not (
        isinstance(shape, list) and len(shape) == len(AXES) and all(whole(s) and s >= 1 for s in shape)
    ):
        found.append(f"piece.shape: one side per axis, each a whole number of at least 1, not {shape!r}")
    return found


def sites_of(shape: list[int]) -> int:
    """The board's count of Node-clocks: the product of its sides."""
    sites = 1
    for side in shape:
        sites = sites * side
    return sites


def setting_departures(setting: Any, universe: Any, piece: Any) -> list[str]:
    """Every way a setting departs: its version, its ticks, and its gears on the trains and the board."""
    found = mapping("setting", setting, SETTING)
    if found:
        return found
    found += versioned("setting", setting)
    if not (whole(setting.get("ticks")) and setting["ticks"] >= 0):
        found.append(f"setting.ticks: a whole number of at least 0, not {setting.get('ticks')!r}")
    gears = setting.get("gears", [])
    found += rows("setting.gears", gears, GEAR)
    trains, sites = len(universe["trains"]), sites_of(piece["shape"])
    given = Counter((t, c, x) for t, c, x, *_ in gears) if not found else Counter()
    for at, row in enumerate(gears if not found else []):
        train, component, site, _, _, tooth = row
        if not (0 <= train < trains and 0 <= site < sites):
            found.append(f"setting.gears[{at}]: train {train} or site {site} off the files")
        if not (component >= 0 and tooth >= 0):
            found.append(f"setting.gears[{at}]: component {component} or fine tooth {tooth} below 0")
        if given[(train, component, site)] > 1:
            found.append(f"setting.gears[{at}]: the gear ({train}, {component}, {site}) given twice")
    return found


def departures(universe: Path, piece: Path, setting: Path) -> list[str]:
    """Every departure of the three files, the setting read once the universe and the piece stand, then the width, file by file."""
    (u, bad_u), (p, bad_p), (s, bad_s) = read(universe), read(piece), read(setting)
    found = bad_u + bad_p + bad_s
    found = found or universe_departures(u) + piece_departures(p)
    found = found or setting_departures(s, u, p)
    width = 0 if found else u["integers"]["width"]
    return found or [
        f"{name}: the integer {n} takes more bits than the width, {width}"
        for name, held in zip(NAMES, (u, p, s), strict=True)
        for n in numbers(held)
        if n.bit_length() > width
    ]

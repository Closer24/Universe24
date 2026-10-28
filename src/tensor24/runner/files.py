"""The three files read and checked: whole numbers alone, every divisor at least 1, every reference whole."""

import json
from pathlib import Path
from typing import Any, TypeGuard

VERSION = 1
UNIVERSE = ("version", "integers", "trains", "couplings")
DIVISORS = ("den", "full_rate", "key", "trace")
TRAIN = ("name", "kinds", "part", "pair", "weight")
PAIR = ("pinion", "rim")
COUPLING = ("train", "part", "with_train", "with_part", "target", "strength")
PIECE = ("version", "shape")
SETTING = ("version", "ticks", "gears")
GEAR = ("train", "component", "site", "a", "b", "r")


def read(path: Path) -> Any:
    """A file's content as JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def whole(value: Any) -> TypeGuard[int]:
    """An integer, and not a truth value."""
    return isinstance(value, int) and not isinstance(value, bool)


def mapping(where: str, held: Any, names: tuple[str, ...]) -> list[str]:
    """A mapping whose every key the format names."""
    if not isinstance(held, dict):
        return [f"{where}: a mapping, not {type(held).__name__}"]
    return [f"{where}: the key {key!r} is not in the format" for key in held if key not in names]


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
    kinds, part, pair = train.get("kinds"), train.get("part"), train.get("pair")
    if not isinstance(train.get("name"), str):
        found.append(f"{where}.name: a label")
    if not (isinstance(kinds, list) and kinds and all(isinstance(kind, str) for kind in kinds)):
        found.append(f"{where}.kinds: a list of the kinds' labels")
    if not (whole(part) and part >= 1):
        found.append(f"{where}.part: a whole number of at least 1, not {part!r}")
    if not (isinstance(pair, list) and len(pair) == len(PAIR) and all(map(whole, pair))):
        found.append(f"{where}.pair: the pinion and the rim, two whole numbers, not {pair!r}")
    elif not (pair[1] == den and 0 <= pair[0] <= pair[1]):
        found.append(f"{where}.pair: the rim is den and the pinion within [0, den], not {pair}")
    if "weight" in train and not whole(train["weight"]):
        found.append(f"{where}.weight: a whole number")
    return found


def universe_departures(universe: Any) -> list[str]:
    """Every way a universe file departs: its version, its divisors, its trains and its coupling rows."""
    found = mapping("universe", universe, UNIVERSE)
    if found:
        return found
    integers, trains = universe.get("integers"), universe.get("trains")
    found += [] if universe.get("version") == VERSION else [f"universe.version: {VERSION}"]
    found += mapping("universe.integers", integers, DIVISORS)
    if found or not isinstance(trains, list):
        return found + (
            [] if isinstance(trains, list) else ["universe.trains: a list of the trains' rows"]
        )
    found += [
        f"universe.integers.{name}: a divisor, a whole number of at least 1, not {integers.get(name)!r}"
        for name in DIVISORS
        if not (whole(integers.get(name)) and integers.get(name) >= 1)
    ]
    for at, train in enumerate(trains):
        found += train_departures(f"universe.trains[{at}]", train, integers.get("den"))
    couplings = universe.get("couplings", [])
    found += rows("universe.couplings", couplings, COUPLING)
    for at, (train, part, with_train, with_part, target, _) in enumerate(couplings if not found else []):
        if not all(0 <= end < len(trains) for end in (train, with_train, target)):
            found.append(f"universe.couplings[{at}]: a train beyond the trains' rows")
        elif not (0 <= part < trains[train]["part"] and 0 <= with_part < trains[with_train]["part"]):
            found.append(f"universe.couplings[{at}]: a part beyond its train's")
    return found


def piece_departures(piece: Any) -> list[str]:
    """Every way a piece file departs: its version and its shape, each side a divisor of at least 1."""
    found = mapping("piece", piece, PIECE)
    if found:
        return found
    found += [] if piece.get("version") == VERSION else [f"piece.version: {VERSION}"]
    shape = piece.get("shape")
    if not (isinstance(shape, list) and shape and all(whole(side) and side >= 1 for side in shape)):
        found.append(f"piece.shape: the sides, whole numbers of at least 1, not {shape!r}")
    return found


def sites_of(shape: list[int]) -> int:
    """The board's count of Node-clocks: the product of its sides."""
    sites = 1
    for side in shape:
        sites = sites * side
    return sites


def setting_departures(setting: Any, universe: Any, piece: Any) -> list[str]:
    """Every way a setting file departs: its version, its ticks, and its gears on the trains and the board."""
    found = mapping("setting", setting, SETTING)
    if found:
        return found
    found += [] if setting.get("version") == VERSION else [f"setting.version: {VERSION}"]
    if not (whole(setting.get("ticks")) and setting["ticks"] >= 0):
        found.append("setting.ticks: a whole number of at least 0")
    gears = setting.get("gears", [])
    found += rows("setting.gears", gears, GEAR)
    trains, sites = len(universe["trains"]), sites_of(piece["shape"])
    for at, row in enumerate(gears if not found else []):
        train, component, site, _, _, tooth = row
        if not (0 <= train < trains and 0 <= site < sites and component >= 0 and tooth >= 0):
            found.append(f"setting.gears[{at}]: a train, site, component or fine tooth off the files")
    return found


def departures(universe: Path, piece: Path, setting: Path) -> list[str]:
    """Every departure of the three files; the setting is read once the universe and the piece stand."""
    u, p = read(universe), read(piece)
    found = universe_departures(u) + piece_departures(p)
    return found + ([] if found else setting_departures(read(setting), u, p))

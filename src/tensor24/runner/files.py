"""Clock: before the first round the files say which trains every Node-clock carries, how many stand on each axis, and which gears are laid where.
Algebra: whole numbers only, every side, part and integer at least 1, each departure refused by name; then the trains read against the engine's kinds.
Board: the three files read and checked, then laid out as the load's arrays; the universe's chosen block names the push's switch and the five strengths (the notch, the hold, the held rows' own spring, the tie and the mesh), each CHOSEN by name; the setting, the world's initialization, lays the gears and the world's one key, the key's middle, once for the world, the interim source of the click's unit (the file's own value, OPEN, until the key is derived from the structure; KEY4); and nothing else is laid: no coupling, particle or mass.
Clicks: n/a: nothing the clicks show comes from the files.
"""

import json
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any, NamedTuple, TypeGuard

import numpy as np

from tensor24.algebra.carry import carry
from tensor24.runner.board import board

# A kind among the 24's, a kind's whole basis and a gear's component within its train's rows are read against the
# engine's kinds once they are made (held_departures). The fine tooth within its teeth is the round's promise, read by
# the runner from outside before every round (run.promises). No file declares a coupling: the coupling family's one
# plan lays the terms at G3, so a universe's couplings are a key not in the format.

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
# the keys a file may leave out; the pinion's key is its own rule's
OPTIONAL = ("gears",)


def whole(value: Any) -> TypeGuard[int]:
    """An integer, and not a truth value."""
    return isinstance(value, int) and not isinstance(value, bool)


class Rule(NamedTuple):
    """What a field must hold, and the words that name it."""

    test: Callable[[Any], bool]
    wants: str


ONE = Rule(lambda v: whole(v) and v >= 1, "a whole number of at least 1")
NONE_BELOW = Rule(lambda v: whole(v) and v >= 0, "a whole number of at least 0")


def star(axes: int) -> Any:
    """The Node-clock's star as the files lay it at the initialization: each Spoke's direction, the + and the - of every axis in turn, the neighbours' order."""
    unit = np.eye(axes, dtype=object)
    return np.stack((unit, -unit), axis=1).reshape(-1, axes)


SENSES = len(star(1))  # the Spokes along one axis, its + and its -: the star of one axis
# the world's one key as the initialization lays it, the key's middle, once for the world: the interim source of the
# click's unit K (the file's own value, OPEN, until the key is derived from the structure; KEY4), read by load.dial
# alone, K = senses middle + 1, an odd unit written by its middle (a definition); the node computes from it every edge
# side's dial D = (kappa div senses) K and its tooth's birth (D - 1) div senses, and names an even D and a broken scale
# (dialled, below); no parity is read here
MIDDLE = Rule(
    lambda v: whole(v) and v >= 0,
    f"a whole number of at least 0, the key's middle laid once for the world, the click's unit {SENSES} middle + 1",
)
# the metric's push on or off: term 5 claims no strength, its books' form laid at the factor 1 or at the factor 0
# (the second hostile code reader's 2: a push of 2 or more opens the books by that factor; the third's 2: a push
# below 0 turns the books' form the other way)
SWITCH = Rule(
    lambda v: whole(v) and v * v == v, "0 or 1, the metric's push off or on: term 5 claims no strength"
)


def axial(sides: Any) -> bool:
    """Whether the sides are one per axis of the board: a board of as many sides of 1 is made, as runner/board.py reads its axes by name, the dimension's own source the piece's shape, which the run reads (no count typed beside it)."""
    ones: Any = tuple(1 for _ in sides)  # the board unpacks its axes by name
    try:
        board(ones)
    except ValueError:
        return False
    return True


LABEL = Rule(lambda v: isinstance(v, str) and v != "", "a label")
KINDS = Rule(
    lambda v: isinstance(v, list) and v != [] and all(map(LABEL.test, v)), "a list of the kinds' labels"
)
VERSIONED = Rule(lambda v: whole(v) and v == VERSION, f"{VERSION}")
SIDES = Rule(
    lambda v: isinstance(v, list) and all(map(ONE.test, v)) and axial(v),
    "one side per axis, each a whole number of at least 1",
)
# Each file's keys and what each holds: a rule, a mapping, a list of one train or more, or rows of the fields named.
# every key a literal, so that the gate reads each one (the note KEYS)
TRAIN = {"name": LABEL, "kinds": KINDS, "part": ONE, "pinion": None}
UNIVERSE = {
    "version": VERSIONED,
    "integers": {"den": ONE, "full_rate": ONE, "width": ONE},
    # the push's switch and the five strengths, each CHOSEN by name: the metric's push on or off (term 5 claims no
    # strength) and the volume's notch (G2), the held hand's tie, the held rows' own spring, the hands' tie and the
    # gradient vertex through the Mesh (G3's frame); the click's key is laid in the setting, as its middle (KEY4)
    "chosen": {
        "push": SWITCH,
        "notch": NONE_BELOW,
        "hold": NONE_BELOW,
        "spring": NONE_BELOW,
        "tie": NONE_BELOW,
        "mesh": NONE_BELOW,
    },
    "trains": [TRAIN],
}
PIECE = {"version": VERSIONED, "shape": SIDES}
SETTING = {"version": VERSIONED, "ticks": NONE_BELOW, "middle": MIDDLE, "gears": GEAR}


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


def vocabulary(
    kinds: Any, square: Any, lifted: Any
) -> tuple[tuple[str, ...], tuple[int, ...], tuple[Any, Any, Any, Any, Any, Any]]:
    """The engine's kinds as the files are read against them: the eight labels, the five of the 24 and the three half-speed kinds of their 48 lifts (each field's name, its _ read as /), their dimensions, each of the five's character on the 24, 1 where its basis is whole, the four-vector's square's character, the held hand's (the one-dimensional kinds together, whose trace squared is the unit's: A1 + A2) and the twist's (the held hand's less the unit's: the sign kind's), every kind 0 off the 24; and the 48 lifts as the files read them (spun)."""
    read = spun(lifted)
    labels = tuple(name.upper().replace("_", "/") for name in (*kinds._fields, *lifted.halves._fields))
    dims = tuple(k.shape[-1] for k in kinds) + read.dims
    traces = np.stack([np.einsum("gii->g", k) for k in kinds])
    # whole: each row one Spoke's sign on the 24, its squares summing to 1 there and to 0 off them
    sums = [np.einsum("gij,gij->gi", k, k) for k in kinds]
    wholes = np.array([int((s * s == s).all()) for s in sums], dtype=object)
    (unit,) = [
        trace for trace in traces if (trace * trace == trace).all()
    ]  # the trivial kind's, 1 on the 24
    hand = sum(trace for trace in traces if (trace * trace == unit).all())  # the one-dimensional kinds'
    return labels, dims, (traces, wholes, np.einsum("gii->g", square), hand, hand - unit, read)


class Spun(NamedTuple):
    """The 48 lifts as the files read them: each of the eight kinds' character on them, pairs (p, q) for p + q r2 in the lifts' (sign, class) layout, the five through each lift's turn; 1 where a kind is half-speed, -I on the full turn; the half-speed kinds' dimensions; and the two half-speed trains' characters with their gears."""

    characters: Any  # (kinds, senses, classes, 2)
    half: Any  # (kinds,): 1 on E1/2, E5/2 and G3/2, 0 on the five
    whole: Any  # (kinds,): 1 where a kind is kept on the full turn, the five
    dims: tuple[int, ...]  # each half-speed kind's character at the lift 1, 2 Re g senses there alone
    trains: Any  # (trains, senses, classes): the 8-gear train's character and the 24-gear's
    gears: tuple[int, ...]  # the two trains' gears


def spun(lifted: Any) -> Spun:
    """The 48 lifts as the files read them (Spun), from kinds.lifts as main.made passes them."""
    whole = np.stack([np.einsum("...ii->...", k) for k in lifted.whole])
    characters = np.concatenate((np.stack((whole, 0 * whole), axis=-1), np.stack(lifted.halves)))
    plus, minus = np.moveaxis(characters, 1, 0)  # every class's word at the + sense and at the -
    half = np.array([int((m == -p).all()) for p, m in zip(plus, minus, strict=True)], dtype=object)
    whole = np.array([int((m == p).all()) for p, m in zip(plus, minus, strict=True)], dtype=object)
    # each half-speed kind's dimension, its character at the lift 1, the + sense's first word in the lifts' layout
    dims = tuple(int(c[0, 0, 0]) for c, h in zip(characters, half, strict=True) if h)
    trains = (lifted.cosets, lifted.axes)
    return Spun(
        characters,
        half,
        whole,
        dims,
        np.stack([np.einsum("...ii->...", t) for t in trains]),
        tuple(t.shape[-1] for t in trains),
    )


def halved_departures(where: str, train: dict[str, Any], kinds: list[int], lifts: Spun) -> list[str]:
    """A train of a half-speed kind: admitted only as the 8-gear train on the cosets of C6 or the 24-gear train, the half-speed hand on the three axes (the 8-gear train laid on each axis row), its character, its part times its kinds', with no r2 part and -I on the full turn, and every other mix refused by name; an admitted one refused too, by name, as no family couples a half-speed train in this build (test worlds only, laid in memory through load.load and the act; the refusal goes when a half-speed table from the families is built)."""
    rational, root = np.moveaxis(train["part"] * lifts.characters[kinds].sum(axis=0), -1, 0)
    plus, minus = rational
    reasons = [
        reason
        for reason, held in (
            ("has an r2 part", not root.any()),
            ("is not -I on the full turn", (minus == -plus).all()),
            ("is neither train's", any((rational == t).all() for t in lifts.trains)),
        )
        if not held
    ]
    named = f"{where}.kinds: {train['kinds']} at part {train['part']}"
    gears = " or the ".join(f"{n}-gear train" for n in lifts.gears)
    return (
        [
            f"{named}: no half-speed train: a half-speed kind rides only the {gears} (on the cosets of C6, and on each of the three axis rows), its character with no r2 part and -I on the full turn; this character {', '.join(reasons)}"
        ]
        if reasons
        else [f"{named}: no family couples a half-speed train in this build"]
    )


def held_departures(
    universe: Any, setting: Any, read: tuple[tuple[str, ...], tuple[int, ...], Any]
) -> list[str]:
    """Every way the checked files ask what the engine's kinds cannot hold: a kind none of the eight, a kind with no whole basis outside the four-vector's square, the square in two trains or more (every row's teeth read every square's 00 slot but its own, so two squares would read each other and no dial would be its own), a train of a half-speed kind (halved_departures), a gear's component off its train's rows, a half-speed gear's component its coset's index."""
    labels, dims, (traces, wholes, squared, *_, lifts) = read
    found, sizes, squares = [], [], []
    for at, train in enumerate(universe["trains"]):
        where = f"universe.trains[{at}]"
        found += [
            f"{where}.kinds[{j}]: {label!r} is none of the kinds {labels}"
            for j, label in enumerate(train["kinds"])
            if label not in labels
        ]
        kinds = [labels.index(label) for label in train["kinds"] if label in labels]
        halved = [k for k in kinds if lifts.half[k]]  # the half-speed kinds, read apart
        tabled = [k for k in kinds if not lifts.half[k]]
        square = not halved and bool((train["part"] * traces[tabled].sum(axis=0) == squared).all())
        squares += [repr(train["name"])] if square else []
        found += [
            f"{where}.kinds[{j}]: {label!r} has no whole basis the 24 permute, so it stands only in the four-vector's square, whose basis is whole"
            for j, label in enumerate(train["kinds"])
            if label in labels
            and labels.index(label) in tabled
            and not (square or wholes[labels.index(label)])
        ]
        found += halved_departures(where, train, kinds, lifts) if halved else []
        sizes.append(train["part"] * sum(dims[k] for k in kinds))
    if len(squares) > 1:
        found.append(
            f"universe.trains: two trains of the four-vector's square's character, one metric family: {', '.join(squares)}"
            " (every row's teeth read every square's 00 slot but its own, so two squares would read each other)"
        )
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


def dialled(key: Any, senses: Any, spare: Any) -> list[str]:
    """The load's two refusals on the edge dial D = (kappa div senses) K that plans.edging lays, each named here, beside the format's every departure by its rule (the gate binds the loader and its plans' home to the engine's rules, so neither holds a whether), each test the carry's remainder, so that load.load calls this once and returns what it names beside the lay's departures, and the run runs nothing: a broken scale, kappa over senses leaving a remainder (spare, edging's carry's: a code check by construction, kappa being a product of senses and of legs counts and so a multiple of senses on any file, so that only a change of kappa's form leaves one; KEY4's mathematician, MINOR 3); and an even D, (D - 1) div senses leaving a remainder. K is odd for every middle, and D is odd while kappa div senses is, as on every plan laid today (kappa 2, or 6 where a tie's three legs lie on an edge); a monomial on an edge holding four legs makes kappa div senses 4 or 12 and D even for every middle. On an even D a side's two teeth born at (D - 1) div senses are not each other's complement, so an edge's books can be one quantum off (the running sum of its two quotients 0 or -1), and the triangle's pair needs the odd dial for its flip about the birth (the Boss's 09:4x ruling; KEY4's mathematician, MINOR 1)."""
    _, half = carry(key - 1, senses, 0)  # the remainder 1 where D is even
    pairs = zip(key.ravel().tolist(), half.ravel().tolist(), strict=True)
    even = sorted({int(d) for d, r in pairs if r})
    broken = [
        f"the edge dials' scale: kappa over senses leaves {spare}, so no dial and no Mesh edge's factor is kappa / two"
    ]
    return (broken if spare else []) + [
        f"the edge dial {d}: even, so a side's two click teeth born at (D - 1) div senses are not each other's"
        " complement and an edge's two quotients can sum to -1, not 0, and the triangle's pair needs an odd dial for its"
        " flip; K being odd by construction, D = (kappa div senses) K is even only where kappa div senses is, as a"
        " monomial on an edge holding four legs makes it"
        for d in even
    ]

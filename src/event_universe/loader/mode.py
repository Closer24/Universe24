"""The generator's mode file beside the world (`<world>.mode.json`, `tools/pixel_mode.py`): the world's digest, and per body and per message its two level pairs over the GameBoard, each one integer per Node in x-major order or the nonzero Nodes alone (their flat x-major indexes with their levels), within the amplitude bound A and 0 beyond the board; every key checked, every defect refused by name (ALGEBRA.md #the-generator)."""

from __future__ import annotations

from event_universe.loader.derived import FamilyRule
from event_universe.loader.keys import Node, keyed

MODE_KEYS, MODE_REQUIRED = ("world_digest", "bodies", "messages"), ("world_digest", "bodies")
MODE_BODY_KEYS = (
    "family",
    "pair",
    "count",
    "seed",
    "carried",
    "period",
    "amplitude",
    "clock",
    "profile",
    "moving",
)
MOVING_KEYS = ("now", "before", "im_now", "im_before")
LEVEL_KEYS, SENSE_KEYS = ("now", "before"), ("im_now", "im_before")
SPARSE_KEYS = ("at", "values")  # a level's nonzero Nodes alone: their flat x-major indexes and levels
Levels = tuple[
    tuple[int, int], ...
]  # a level over the GameBoard as its nonzero Nodes: (flat index, level)


def pairs_of(given: object, label: str, size: int) -> Levels:
    """A level of the mode file as its nonzero Nodes: from a list of `size` integers, one per Node in x-major order, or from the nonzero Nodes alone, {`at`: their flat x-major indexes from 0 below `size`, each once, `values`: their integer levels}; refused by name otherwise."""
    if isinstance(given, dict):
        sparse = keyed(given, label, SPARSE_KEYS, SPARSE_KEYS)
        at, values = sparse["at"], sparse["values"]
        if (
            not isinstance(at, list)
            or not isinstance(values, list)
            or len(at) != len(values)
            or any(type(i) is not int or not 0 <= i < size for i in at)
            or any(type(v) is not int for v in values)
            or len(set(at)) != len(at)
        ):
            raise ValueError(
                f"{label}'s nonzero Nodes must be flat x-major indexes from 0 below {size}, each once, with one integer level each"
            )
        return tuple((i, v) for i, v in zip(at, values, strict=True) if v)
    if not isinstance(given, list) or len(given) != size or any(type(v) is not int for v in given):
        raise ValueError(
            f"{label} must be {size} integers, one per Node in x-major order, or its nonzero Nodes alone"
        )
    return tuple((i, v) for i, v in enumerate(given) if v)


def levels_of(
    entry: object, label: str, family: FamilyRule, shape: Node, bound: int, beyond: tuple[Node, ...]
) -> tuple[Levels, Levels, Levels, Levels]:
    """A body's or a message's two level pairs from its mode entry as their nonzero Nodes: `moving`'s now and before, and its im_now and im_before (the second level pair, the rotation sense; both or neither, 0 where absent), each one integer per Node in x-major order or the nonzero Nodes alone (`pairs_of`), within the amplitude bound A and 0 at every Node beyond the board (nothing is laid there); a sense without a rotation (a second pair on real levels at 0) is refused by name; the generator's readings beside them are read and not used."""
    size = shape[0] * shape[1] * shape[2]
    outside = {(x * shape[1] + y) * shape[2] + z: (x, y, z) for x, y, z in beyond}
    mode = keyed(entry, label, MODE_BODY_KEYS, ("family", "pair", "moving"))
    if mode["family"] != family.name or mode["pair"] != list(family.pair):
        raise ValueError(
            f"{label} is of the family {mode['family']!r} with the pair {mode['pair']}, the record of "
            f"{family.name!r} with {list(family.pair)}"
        )
    words = keyed(mode["moving"], f"{label}.moving", MOVING_KEYS, LEVEL_KEYS)
    if (SENSE_KEYS[0] in words) != (SENSE_KEYS[1] in words):
        raise ValueError(f"{label}.moving declares im_now and im_before together, or neither")
    found = []
    for word in MOVING_KEYS:
        pairs = pairs_of(words.get(word, []), f"{label}'s {word} level", size) if word in words else ()
        if any(abs(v) > bound for _at, v in pairs):
            raise ValueError(f"{label}'s {word} level is above the amplitude bound A = {bound}")
        laid = next(((at, v) for at, v in pairs if at in outside), None)
        if laid is not None:
            raise ValueError(
                f"{label}'s {word} level is {laid[1]} at the Node "
                f"{list(outside[laid[0]])}, beyond the board's inner face: nothing is laid there"
            )
        found.append(pairs)
    if (found[2] or found[3]) and not (found[0] or found[1]):
        raise ValueError(
            f"{label}.moving carries a sense without a rotation: its second level pair stands on real "
            "levels at 0 at every Node (ALGEBRA.md #the-paces, the sign is the rotation sense)"
        )
    return found[0], found[1], found[2], found[3]


def mode_entries(mode: object, digest: str, key: str) -> list[object]:
    """The generator's entries under `key` (bodies or messages) in the mode file beside the world, which stands for this world by its digest."""
    written = keyed(mode, "the mode file beside the world", MODE_KEYS, MODE_REQUIRED)
    if written["world_digest"] != digest:
        raise ValueError(
            f"the mode file's world_digest {written['world_digest']} is not this world's digest {digest}: "
            "the mode file stands beside another world, or the world changed after the generator wrote it"
        )
    entries = written.get(key, [])
    return entries if isinstance(entries, list) else []


def entry_of(entries: list[object], number: int, label: str) -> object:
    """The mode entry of a body or a message by its number, refused by name where the generator wrote none."""
    if number >= len(entries):
        raise ValueError(
            f"{label} has no entry in the mode file beside the world: its levels are the generator's"
        )
    return entries[number]

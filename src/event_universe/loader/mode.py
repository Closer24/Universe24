"""The generator's mode file beside the world (`<world>.mode.json`, `tools/pixel_mode.py`): the world's digest, and per body and per message its two level pairs over the whole GameBoard in x-major order, within the amplitude bound A and 0 beyond the board; every key checked, every defect refused by name (ALGEBRA.md #the-generator)."""

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


def levels_of(
    entry: object, label: str, family: FamilyRule, shape: Node, bound: int, beyond: tuple[Node, ...]
) -> tuple[tuple[int, ...], ...]:
    """A body's or a message's two level pairs from its mode entry: `moving`'s now and before, and its im_now and im_before (the second level pair, the rotation sense; both or neither, 0 where absent), each one integer per Node in x-major order within the amplitude bound A and 0 at every Node beyond the board (nothing is laid there); a sense without a rotation (a second pair on real levels at 0) is refused by name; the generator's readings beside them are read and not used."""
    size = shape[0] * shape[1] * shape[2]
    outside = [(x * shape[1] + y) * shape[2] + z for x, y, z in beyond]
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
        values = words.get(word, [0] * size)
        if (
            not isinstance(values, list)
            or len(values) != size
            or any(type(v) is not int for v in values)
        ):
            raise ValueError(
                f"{label}'s {word} level must be {size} integers, one per Node in x-major order"
            )
        if max(abs(v) for v in values) > bound:
            raise ValueError(f"{label}'s {word} level is above the amplitude bound A = {bound}")
        laid = next((at for at in outside if values[at]), None)
        if laid is not None:
            raise ValueError(
                f"{label}'s {word} level is {values[laid]} at the Node "
                f"{list(beyond[outside.index(laid)])}, beyond the board's inner face: nothing is laid there"
            )
        found.append(tuple(values))
    if any(found[2] + found[3]) and not any(found[0] + found[1]):
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

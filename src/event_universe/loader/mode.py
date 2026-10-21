"""The generator's mode file beside the world (`<world>.mode.json`, `tools/pixel_mode.py`): the world's digest, and per body and per packet its two level pairs over the lattice, each one integer per Node in x-major order or the nonzero Nodes alone (their flat x-major indexes with their levels), within the amplitude bound A and 0 beyond the board; and per bound body, where the host's frame tool wrote it (tools/frame_of.py, 2026-10-21), its frame under the key `frame`, integers alone (`frame_of`, `FrameEntry`): its levels as rotation pairs over the family's den with their sines and degenerate counts, its transition, its unit W_rec, its period, its standing region's flat indexes, its shares at the lay in parts of the unit and per level one compiled profile at one quantum, the declared layer the engine's taker reads (src/event_universe/frame.py) so that no float stands in the engine; every key checked, every defect refused by name (ALGEBRA.md #the-generator)."""

from __future__ import annotations

from dataclasses import dataclass

from event_universe.loader.derived import FamilyRule
from event_universe.loader.keys import Node, integer, keyed

MODE_KEYS, MODE_REQUIRED = ("world_digest", "bodies", "packets"), ("world_digest", "bodies")
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
    "lay",
    "frame",
)
FRAME = "frame"  # a bound body's frame, the host's frame tool's integers (tools/frame_of.py; `frame_of`)
FRAME_KEYS = ("levels", "sines", "modes", "transition", "unit", "period", "region", "shares", "profiles")
MOVING_KEYS = ("now", "before", "im_now", "im_before")
LEVEL_KEYS, SENSE_KEYS = ("now", "before"), ("im_now", "im_before")
SPARSE_KEYS = ("at", "values")  # a level's nonzero Nodes alone: their flat x-major indexes and levels
Levels = tuple[
    tuple[int, int], ...
]  # a level over the lattice as its nonzero Nodes: (flat index, level)


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
    """A body's or a packet's two level pairs from its mode entry as their nonzero Nodes: `moving`'s now and before, laid on every real line of the record alike (`Lattice.lay`), and its im_now and im_before (the second level pair of a family of dimension two, a plane, its sense; both or neither, 0 where absent; refused by name on a family whose lines are no plane, one real line or the three real lines of a record of dimension 3), each one integer per Node in x-major order or the nonzero Nodes alone (`pairs_of`), within the amplitude bound A and 0 at every Node beyond the board (nothing is laid there); a sense without a rotation (a second pair on real levels at 0) is refused by name; the generator's readings beside them are read and not used."""
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
    if SENSE_KEYS[0] in words and not family.plane:
        raise ValueError(
            f"{label}.moving lays a second level pair on {family.name!r}, a family whose lines are no plane: the "
            "second pair is a plane's sense, and the lay is within the family's dimension (ALGEBRA.md #a-familys-declaration)"
        )
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
    now, before, second_now, second_before = found
    if (second_now or second_before) and not (now or before):
        raise ValueError(
            f"{label}.moving carries a sense without a rotation: its second level pair stands on real "
            "levels at 0 at every Node (ALGEBRA.md #the-paces, the sign is the rotation sense)"
        )
    return now, before, second_now, second_before


def mode_entries(mode: object, digest: str, key: str) -> list[object]:
    """The generator's entries under `key` (bodies or packets) in the mode file beside the world, which stands for this world by its digest."""
    written = keyed(mode, "the mode file beside the world", MODE_KEYS, MODE_REQUIRED)
    if written["world_digest"] != digest:
        raise ValueError(
            f"the mode file's world_digest {written['world_digest']} is not this world's digest {digest}: "
            "the mode file stands beside another world, or the world changed after the generator wrote it"
        )
    entries = written.get(key, [])
    return entries if isinstance(entries, list) else []


def entry_of(entries: list[object], number: int, label: str) -> object:
    """The mode entry of a body or a packet by its number, refused by name where the generator wrote none."""
    if number >= len(entries):
        raise ValueError(
            f"{label} has no entry in the mode file beside the world: its levels are the generator's"
        )
    return entries[number]


@dataclass(frozen=True)
class FrameEntry:
    """A bound record's frame as the host's frame tool wrote it into the mode file (tools/frame_of.py), integers alone: its levels as rotation pairs (den cos Omega, den) in energy order with their sines den sin Omega and the count of each level's degenerate modes, the two levels of its transition (`lower`, `upper`), its unit W_rec = W_c sin(Omega_upper - Omega_lower), its period in intervals, its standing region as flat x-major indexes, its shares per level at the lay in parts of the unit and per level its compiled profile at one quantum as the nonzero Nodes' levels."""

    levels: tuple[tuple[int, int], ...]
    sines: tuple[int, ...]
    modes: tuple[int, ...]
    lower: int
    upper: int
    unit: int
    period: int
    region: tuple[int, ...]
    shares: tuple[int, ...]
    profiles: tuple[Levels, ...]


def integers_of(given: object, label: str, count: int, least: int) -> tuple[int, ...]:
    """A list of `count` integers from `least` up, refused by name otherwise."""
    if not isinstance(given, list) or len(given) != count:
        raise ValueError(f"{label} must be a list of {count} integers")
    return tuple(integer(value, f"{label}[{k}]", least) for k, value in enumerate(given))


def frame_of(
    entry: object, label: str, family: FamilyRule, shape: Node, bound: int
) -> FrameEntry | None:
    """A body's frame from its mode entry's key `frame`, None where the tool wrote none (a source, the frozen pair, a record with no transition): at least two levels [num, den] over the family's den with num within the circle, as many sines from 0 through den and as many degenerate counts from 1, the transition two distinct level indexes, the unit and the period from 1, the region at least one flat index below the board's size, each once, as many shares from 0 as levels and as many profiles, each a level over the lattice (`pairs_of`) within the amplitude bound; refused by name otherwise."""
    if not isinstance(entry, dict) or FRAME not in entry:
        return None
    frame = keyed(entry[FRAME], f"{label}.{FRAME}", FRAME_KEYS, FRAME_KEYS)
    name, den = f"{label}.{FRAME}", family.pair[1]
    given = frame["levels"]
    if not isinstance(given, list) or len(given) < 2:
        raise ValueError(
            f"{name}.levels must list at least two rotation pairs [num, den] in energy order"
        )
    levels = []
    for k, pair in enumerate(given):
        if not isinstance(pair, list) or len(pair) != 2 or pair[1] != den:
            raise ValueError(
                f"{name}.levels[{k}] must be a rotation pair [num, {den}] over the family's den"
            )
        levels.append((integer(pair[0], f"{name}.levels[{k}][0]", -den, den), den))
    count = len(levels)
    sines = integers_of(frame["sines"], f"{name}.sines", count, 0)
    if any(sine > den for sine in sines):
        raise ValueError(f"{name}.sines must stand from 0 through den {den}")
    modes = integers_of(frame["modes"], f"{name}.modes", count, 1)
    lower, upper = integers_of(frame["transition"], f"{name}.transition", 2, 0)
    if lower == upper or max(lower, upper) >= count:
        raise ValueError(f"{name}.transition must name two distinct levels below {count}")
    unit = integer(frame["unit"], f"{name}.unit", 1)
    period = integer(frame["period"], f"{name}.period", 1)
    size = shape[0] * shape[1] * shape[2]
    places = frame["region"]
    if not isinstance(places, list) or not places:
        raise ValueError(f"{name}.region must list the region's flat x-major indexes, at least one")
    region = integers_of(places, f"{name}.region", len(places), 0)
    if max(region) >= size or len(set(region)) != len(region):
        raise ValueError(f"{name}.region must list flat x-major indexes below {size}, each once")
    shares = integers_of(frame["shares"], f"{name}.shares", count, 0)
    given = frame["profiles"]
    if not isinstance(given, list) or len(given) != count:
        raise ValueError(f"{name}.profiles must list one compiled profile per level, {count}")
    profiles = tuple(pairs_of(profile, f"{name}.profiles[{k}]", size) for k, profile in enumerate(given))
    if any(abs(value) > bound for profile in profiles for _at, value in profile):
        raise ValueError(f"{name}.profiles stand above the amplitude bound A = {bound}")
    return FrameEntry(tuple(levels), sines, modes, lower, upper, unit, period, region, shares, profiles)


def body_entry(
    entries: list[object],
    placed: int,
    label: str,
    family: FamilyRule,
    shape: Node,
    bound: int,
    beyond: tuple[Node, ...],
) -> tuple[tuple[Levels, Levels, Levels, Levels], FrameEntry | None]:
    """A laid body's mode entry read whole: its two level pairs (`levels_of`) and its frame where the host's frame tool wrote one (`frame_of`)."""
    entry = entry_of(entries, placed, label)
    name = f"the mode file's bodies[{placed}]"
    return levels_of(entry, name, family, shape, bound, beyond), frame_of(
        entry, name, family, shape, bound
    )

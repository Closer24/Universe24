"""The world's key `interval` (ALGEBRA.md, The board's interval is no observable; The uniform mode carried by Rule3's own k = 0 line; The mean's velocity is the content's; the hypotheses under their own names, 2026-10-22): its one value `unobservable`, the board's declaration that its interval is a count no act reads and the mean's velocity the content's (`interval_of`, `INTERVAL`, `UNOBSERVABLE`), read by loader/world.py into `World.unobservable`, by features/start `rest` (every massless row's rest the zero-mean part of its sources on the board wrapped on every axis, as under the law's key) and by records.write_sources (the hill at the symmetry's weight inside the one write); the law's key `uniform: carried` of 2026-10-21 (loader/uniform.py) stays admitted beside it as the law as written, the carried mean with no hill (the reader's line L2 on the design: the shipped worlds that declare it load and run as before), and a world naming both keys is refused by name (`one_key`); a kick, a packet laid on a holder of the content, is refused by name under the key (`kicks_refused`: the mean's velocity is the content's by the constraint's attractor and nobody's declaration)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from event_universe.loader.derived import FamilyRule
from event_universe.loader.keys import AXES
from event_universe.loader.uniform import CARRIED, UNIFORM

INTERVAL, UNOBSERVABLE = "interval", "unobservable"  # the board's interval a count no act reads


def interval_of(value: object, faces: Mapping[str, Any]) -> bool:
    """The world's key `interval` (ALGEBRA.md, The board's interval is no observable, a hypothesis under its own name, 2026-10-22): its one value `unobservable`, the declaration that a uniform level is a change of units at every Node alike and so is its change from interval to interval, the board's interval a count no act reads, so that the mean's velocity is no datum of the seed and the content fixes it (The mean's velocity is the content's: the constraint's attractor reached from rest, the hill at the symmetry's weight inside the one write at every Node, records.write_sources, paces.motion_weight); the massless row's rest the zero-mean part of its sources (features/start `rest`), the k = 0 component Rule3's own line; refused by name at any other value, and refused by name where a face is open or closed: a board with a sink has no free uniform mode, and the rest beyond the face fixes the clock's unit, so the key stands on a board periodic on every axis alone; the staggered mode stays refused on every even box (`loader/world.even_box_refused`)."""
    if value != UNOBSERVABLE:
        raise ValueError(
            f"{INTERVAL} is {UNOBSERVABLE!r} where the board's interval is a count no act reads and the mean's "
            f"velocity is the content's (ALGEBRA.md, The board's interval is no observable), got {value!r}"
        )
    for axis in AXES:
        if faces[axis] != "periodic":
            raise ValueError(
                f"{INTERVAL}: {UNOBSERVABLE} on a board whose {axis} face is {faces[axis]!r}: a board with a sink "
                "has no free uniform mode and its rest fixes the clock's unit beyond the face; the key stands on a "
                "board periodic on every axis alone (ALGEBRA.md, The board's interval is no observable)"
            )
    return True


def one_key(world: Mapping[str, Any]) -> None:
    """A world declares the hypothesis's key `interval: unobservable` or the law's `uniform: carried` and never both, since the two name one board's uniform mode under two laws, the hill at the symmetry's weight and the carried mean without it (ALGEBRA.md, The uniform mode carried by Rule3's own k = 0 line, the clause of 2026-10-22 and the clause of 2026-10-21 kept by name; the reader's line L2 on the design): refused by name where both stand."""
    if UNIFORM in world and INTERVAL in world:
        raise ValueError(
            f"the world declares `{UNIFORM}: {CARRIED}` and `{INTERVAL}: {UNOBSERVABLE}` together: the law's key "
            "of 2026-10-21 (the carried mean, no hill) and the hypothesis's key of 2026-10-22 (the hill at the "
            "symmetry's weight) name one board's uniform mode under two laws; declare one (ALGEBRA.md, The "
            "board's interval is no observable; The uniform mode carried by Rule3's own k = 0 line)"
        )


def kicks_refused(unobservable: bool, families: tuple[FamilyRule, ...], packets: object) -> None:
    """The kick, a packet laid on a holder of the content's rest (ALGEBRA.md, No write from outside Rule3 wakes either double root of the massless row, the clause of 2026-10-22): on a board declaring `interval: unobservable` it is refused by name, the mean's velocity being the content's by the constraint's attractor and nobody's declaration (The mean's velocity is the content's); on every other board the one lay that moves the massless row's sums, as the law as written has it; read on the world's `packets` entries by the family each names (an entry an object of the file, or the family's name itself, the lattice's call on a world a host builds without the loader), before the loader lays them."""
    if not unobservable or not isinstance(packets, list):
        return
    holders = {family.name for family in families if not family.quanta}
    for number, entry in enumerate(packets):
        name = entry.get("family") if isinstance(entry, dict) else entry
        if name in holders:
            raise ValueError(
                f"packets[{number}] lays a kick on {name!r}, a holder of the content, under "
                f"`{INTERVAL}: {UNOBSERVABLE}`: the mean's velocity is the content's by the constraint's attractor "
                "and nobody's declaration (ALGEBRA.md, No write from outside Rule3 wakes either double root of "
                "the massless row, the clause of 2026-10-22; The mean's velocity is the content's)"
            )

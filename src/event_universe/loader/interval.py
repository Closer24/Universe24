"""The world's key `interval` (ALGEBRA.md, The board's interval is no observable; The uniform mode carried by Rule3's own k = 0 line; The mean's velocity is the content's; the hypotheses under their own names, 2026-10-22): its one value `unobservable`, the board's declaration that its interval is a count no act reads and the mean's velocity the content's (`interval_of`, `INTERVAL`, `UNOBSERVABLE`), read by loader/world.py into `World.unobservable`, by features/start `rest` (every massless row's rest the zero-mean part of its sources on the board wrapped on every axis, as under the law's key) and by `volume_rows` (the massless rows of the content carrying their volume, features/volume); the law's key `uniform: carried` of 2026-10-21 (loader/uniform.py) stays admitted beside it as the law as written, the carried mean with no hill (the reader's line L2 on the design: the shipped worlds that declare it load and run as before), and a world naming both keys is refused by name (`one_key`); a kick, a packet laid on a holder of the content, is refused by name under the key (`kicks_refused`: the mean's velocity is the content's by the constraint's attractor and nobody's declaration)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from typing import Any

from event_universe.features import volume
from event_universe.loader.derived import FamilyRule
from event_universe.loader.uniform import UNIFORM

INTERVAL, UNOBSERVABLE = "interval", "unobservable"  # the board's interval a count no act reads


def interval_of(value: object, faces: Mapping[str, Any]) -> bool:
    """The world's key `interval` (ALGEBRA.md, The board's interval is no observable, a hypothesis under its own name, 2026-10-22): its one value `unobservable`, the declaration that a uniform level is a change of units at every Node alike and so is its change from interval to interval, the board's interval a count no act reads, so that the mean's velocity is no datum of the seed and the content fixes it (The mean's velocity is the content's: the constraint reached from rest; the massless row carrying its time line as the volume's level, features/volume, `volume_rows`); the massless row's rest the zero-mean part of its sources (features/start `rest`), the k = 0 component Rule3's own line; refused by name at any other value, and refused by name where a face is open or closed: a board with a sink has no free uniform mode, and the rest beyond the face fixes the clock's unit, so the key stands on a board periodic on every axis alone; the staggered mode stays refused on every even box (`loader/world.even_box_refused`)."""
    raise ValueError(
        f"{INTERVAL} is declared ({value!r}): under the law of one Node the board's interval is no observable "
        "in every world, the massless row of the content carrying its time line as the volume's level on every "
        "board, wrapped or faced (beyond a face the rest fixes the clock's unit: the fill is the rest's volume), "
        "and no key switches it; drop the key (the owner's word of 2026-10-22)"
    )


def one_key(world: Mapping[str, Any]) -> None:
    """A world declares the hypothesis's key `interval: unobservable` or the law's `uniform: carried` and never both, since the two name one board's uniform mode under two laws, the volume's line and the carried mean (ALGEBRA.md, The uniform mode carried by Rule3's own k = 0 line, the clause of 2026-10-22 and the clause of 2026-10-21 kept by name; the reader's line L2 on the design): refused by name where both stand."""
    for key in (UNIFORM, INTERVAL):
        if key in world:
            raise ValueError(
                f"the world declares `{key}: {world[key]!r}`: under the law of one Node every board's massless "
                "rows of the content carry their time line as the volume's level and their k = 0 mode on Rule3's "
                "own line, in every world, and no key switches it (`uniform: {CARRIED}` the law's key of "
                "2026-10-21 and `interval: {UNOBSERVABLE}` the hypothesis's key of 2026-10-22, both one value "
                "for every world); drop the key (the owner's word of 2026-10-22)"
            )


def volume_rows(
    unobservable: bool, families: tuple[FamilyRule, ...], gamma: int | None = None
) -> tuple[FamilyRule, ...]:
    """The rows the world's key `interval: unobservable` moves to the volume's variable (features/volume; ALGEBRA.md, The board's interval is no observable; the momentum hand's derivation M12a read cold by the reader, 2026-10-22, the reader's W7): every held massless row of the content that is not the sign's holder carries its time line as the volume's level X = Gamma (Gamma / p_0)^(d + 1), the proper volume per proper interval in the Node's own paces, with the one write (d + 1) X c over Gamma E_s T at the one fixed wall and the level a reading of the record; the key alone switches the variable, no number of the row: the exponent d + 1 is the trace's (the hill's one weight for every mix and the exponent one number by the chain rule), so a moved row without `pressure: trace` is refused by name; under the key `factor: rounded` divides at the one wall Gamma E_s T and `factor: carried` at the wall fixed per Node for the run, Gamma E_s T times the Node's factor wall at the rest's paces, the ratio to the interval's paces inside the numerator (`Lattice.start`, `records.write_sources`; the Boss's decision of 2026-10-22 on the text hand's model), the carried factor's one form under either key, so that a moving wall, which folds the run back (the reader's (d)), is no form; the families returned with the flag `motion_volume` set, every other board's families as they are."""
    if not unobservable:
        return families
    found = []
    for family in families:
        moved = family.held and not family.wronskian and family.pair[0] == family.pair[1]
        if moved and not family.pressure_trace:
            raise ValueError(
                f"{family.name!r} carries the volume's level under `{INTERVAL}: {UNOBSERVABLE}` and declares no "
                "`pressure: trace`: the volume's exponent d + 1 is the trace's one weight for every mix (features/volume; "
                "ALGEBRA.md, The stress's trace is the time line's); declare it or drop the key"
            )
        fill = volume.fill_of(gamma, family.rest) if moved and gamma is not None else family.rest
        found.append(replace(family, motion_volume=True, fill=fill) if moved else family)
    return tuple(found)


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

"""The volume form on every board (ALGEBRA.md, The board's interval is no observable; The mean's velocity is the content's; the owner's law of one Node, 2026-10-22, and his rule of 2026-10-23, no more keys in the code): the board's interval is a count no act reads and the mean's velocity is the content's on every world, so the held rows sourced by the tensions carry their time line as the volume's level (`volume_rows`, features/volume) and a kick, a packet laid on a holder of the content, is refused by name (`kicks_refused`); no key of the world names any of it."""

from __future__ import annotations

from dataclasses import replace

from event_universe.features import volume
from event_universe.loader.derived import FamilyRule


def volume_rows(families: tuple[FamilyRule, ...], gamma: int | None = None) -> tuple[FamilyRule, ...]:
    """The rows carrying the volume's variable (features/volume; ALGEBRA.md, The board's interval is no observable; the momentum hand's derivation M12a read cold by the reader, 2026-10-22, the reader's W7; The carried momentum, the clause of 2026-10-23 on the gapped time line): every held row of the content sourced by the tensions, massless or gapped (`FamilyRule.axes`), its time line the volume X = Gamma (Gamma / p_0)^(d + 1) and its fill beyond a face the rest's volume X(rest) where Gamma is given (`volume.fill_of`); the holder of the sign and a row sourced by the form alone keep their level."""
    found = []
    for family in families:
        moved = family.held and not family.wronskian and family.axes  # the row sourced by the tensions
        fill = volume.fill_of(gamma, family.rest) if moved and gamma is not None else family.rest
        found.append(replace(family, motion_volume=True, fill=fill) if moved else family)
    return tuple(found)


def kicks_refused(families: tuple[FamilyRule, ...], packets: object) -> None:
    """The kick, a packet laid on a holder of the content's rest (ALGEBRA.md, No write from outside Rule3 wakes either double root of the massless row, the clause of 2026-10-22): refused by name on every board, the mean's velocity being the content's by the constraint's attractor and nobody's declaration (The mean's velocity is the content's)."""
    if not isinstance(packets, list):
        return
    holders = {family.name for family in families if not family.quanta}
    for number, entry in enumerate(packets):
        name = entry.get("family") if isinstance(entry, dict) else entry
        if name in holders:
            raise ValueError(
                f"packets[{number}] lays a kick on {name!r}, a holder of the content, under "
                "the volume form: the mean's velocity is the content's by the constraint's attractor "
                "and nobody's declaration (ALGEBRA.md, No write from outside Rule3 wakes either double root of "
                "the massless row, the clause of 2026-10-22; The mean's velocity is the content's)"
            )

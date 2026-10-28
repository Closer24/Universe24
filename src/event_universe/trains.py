"""The trains of the clock as the calibre names them, no name and no role (the owner's word of 2026-10-25, there is no if): a train is a size (its count of gears) with a ratio (pinion, rim) for Rule3's gearing or teeth of its own for a train with no meshes; its gears are built here with their teeth by size, the trains ordered for the acts (a size the law does not name refused by name at the assembly, assembly/piece); the lookups choose a train by its numbers alone. The standard length is derived from the rim, X = Gamma rim (clock.standard_length; DAVID-AMPLITUDES.md section 4, a declared `amplitude` refused at the assembly, assembly/piece), carried above the shortest hand derived from Gamma (standard.shortest_hand); no width and no room of the machine stands in the engine (the owner's words of 2026-10-27, 04:0x and 04:4x UTC; the former width constant and the room cut from it struck, the value kept in the file so that every chart stands bit for bit)."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core.acts import mid
from event_universe.core.rule3 import carries, held_teeth
from event_universe.core.spokes import AXES, SIDES, SPOKES

REGULATOR = 1 + AXES + AXES  # the regulator: its time gear, AXES tensions and flows (R11)
OFFSET = AXES + 1  # the size of the train at (rim, rim): its time gear and its AXES odd gears
HAND = SIDES  # the size of a hand: its two gears, a conjugate pair (the Gaussian integer's two parts, its conjugate one sign apart)
POWER_TIME = AXES + 1  # the vacuum's balance X p^(d + 1) = Gamma^(d + 2): the time gear's power d + 1
POWER_AXIS = SIDES
Ratio = tuple[int, int]


def zeros(size: tuple[int, ...]) -> Any:
    """An integer array of the great clock's size at 0 (Python integers, no width)."""
    return np.zeros(size, dtype=object)


class Train:
    """One train of the clock as the calibre names it: a size (its count of gears), a ratio (pinion, rim) for Rule3's gearing, or teeth of its own for a train with no meshes (the ratchet); its gears; the weight of a held field (None on every other train)."""

    __slots__ = ("size", "ratio", "teeth", "gears", "twin", "weight")

    def __init__(self, size: int, ratio: Ratio | None, teeth: int | None, gears: list[Gear]) -> None:
        self.size, self.ratio, self.teeth, self.gears = size, ratio, teeth, gears
        self.twin: Train | None = None
        self.weight: int | None = None

    @property
    def spring(self) -> int | None:
        """The ratio's spring rim - pinion, None for the train with its own teeth."""
        return None if self.ratio is None else self.ratio[1] - self.ratio[0]


class Gear:
    """One gear of a train: its two notches, its fine tooth `fine` at the gearing's teeth `teeth`, and where the train drives it, its drive fine tooth `dfine` at the drive teeth `dteeth`. A setting names a gear's two notches, now and before, in that order (two per gear, the hand's count HAND at the slices)."""

    __slots__ = ("now", "before", "fine", "teeth", "dfine", "dteeth")

    def __init__(
        self, now: Any, before: Any, fine: Any, teeth: Any, dfine: Any = None, dteeth: Any = None
    ) -> None:
        self.now, self.before, self.fine = now, before, fine
        self.teeth, self.dfine, self.dteeth = teeth, dfine, dteeth

    def copy(self) -> Gear:
        """The gear's arrays copied, its teeth shared."""
        d = None if self.dfine is None else self.dfine.copy()
        return Gear(self.now.copy(), self.before.copy(), self.fine.copy(), self.teeth, d, self.dteeth)


def drive_teeth(
    size: int, ratio: Ratio | None, rim: int, full_rate: int, key: int, trace: int
) -> list[Any]:
    """The drive teeth of a train's gears by its size: the regulator's time gear and its other gears the held teeth at the file's trace weight (TW-S1, the owner's word of 2026-10-26, 07:5x UTC: the trace's weight is the calibre's integer, dimensionless, 6 in nature's files, the one value with a sentence in nature, light having no trace; 54 the charts' value of 2026-10-25 kept by name, ga2's file at it until its re-set; rule3.held_teeth at the powers POWER_TIME 4 of the time gear and POWER_AXIS 2 of the six axis gears, K-S1 to K-S3, Y-S1), the offset train's four gears T, the hand at the calibre's own ratio (rim, rim), the unsprung hand, its first gear T (the advance of W-S1), a held field's one gear at a gapped ratio T (its kick at the impulse, as the offset's), another hand none."""
    if size == REGULATOR:
        powers = (POWER_TIME, *[POWER_AXIS] * (size - 1))
        return [held_teeth(trace, rim, full_rate, key, p) for p in powers]
    if size == OFFSET or (size == 1 and ratio is not None):
        return [key] * size
    if size == HAND and ratio == (rim, rim):
        return [key, None]
    return [None] * size


def gears_of(
    size: tuple[int, ...], gears: int, ratio: Ratio | None, teeth: int | None, w: int, dteeth: list[Any]
) -> list[Gear]:
    """A train's gears at the start: every notch 0, every fine tooth at half its teeth (the gearing's w, or the train's own teeth), a drive fine tooth at half the drive teeth where the gear is driven."""
    if teeth is not None:
        return [Gear(zeros(size), zeros(size), zeros(size) + mid(teeth), teeth)]
    drives = [None if dt is None else zeros(size) + mid(dt) for dt in dteeth]
    return [
        Gear(zeros(size), zeros(size), zeros(size) + mid(w), w, d, dt)
        for d, dt in zip(drives, dteeth, strict=True)
    ]


def order_key(train: Train) -> tuple[bool, int]:
    """The acts' order as a key compared and never tested: the train with its own teeth first, then every train by the count of its gears with a drive, a train whose drive reads other trains after them (the hands with no drive, the unsprung hand its one gear, the offset train its four, the regulator its ten), the ties in the file's order."""
    written = sum(1 for gear in train.gears if gear.dteeth is not None)
    return train.teeth is None, 0 if train.twin is not None else written


def rows_of(calibre: dict[str, Any]) -> list[dict[str, Any]]:
    """Every train's row in the index a setting names: the light (rim, rim) first, the file's gapped rows, then the regulator at (rim - rim div Gamma, rim), the offset at (rim, rim) and the ratchet of its own two teeth (the pawl's two sides); the one list the clock builds and the readers read."""
    rim, full_rate = int(calibre["integers"]["den"]), int(calibre["integers"]["node_clock"])
    return [
        {"shape": HAND, "pair": [rim, rim]},
        *calibre["rows"],
        {"shape": REGULATOR, "pair": [rim - carries(rim, full_rate), rim]},
        {"shape": OFFSET, "pair": [rim, rim]},
        {"shape": 1, "wall": SIDES},
    ]


def trains_of(calibre: dict[str, Any], size: tuple[int, ...], w: int) -> tuple[list[Train], list[Train]]:
    """The trains of the clock in the acts' order, and the same trains in the index a setting names (the light 0, the file's rows from 1, then the regulator, the offset and the ratchet): the file holds the matter alone, its gapped rows (a hand of two gears, or twin hands of four, at a pinion below the rim), and the four trains every clock holds are built from the rim and the full rate alone (David's DAVID-GENERIC-ENGINE.md part C, the owner's word of 2026-10-27, 18:5x UTC, through the Boss's recommendation: no declarations): the light, the hand at (rim, rim); the regulator, its time gear, AXES tensions and AXES flows at (rim - rim div Gamma, rim); the offset, its time gear and AXES odd gears at (rim, rim); the ratchet, one gear of its own two teeth (the pawl's two sides); twin hands of a row of four gears, each hand two gears at the row's ratio with the spin's drive teeth; a held field, a row of one gear at a gapped ratio with its weight (David's DAVID-MEDIATOR.md, the owner's yes to the nuclear family of 2026-10-27, 16:5x UTC: one gear cannot be a hand, so the numbers tell it from the hands)."""
    ints = calibre["integers"]
    rim, full_rate, key = int(ints["den"]), int(ints["node_clock"]), int(ints["quantum_action"])
    trace = int(ints["trace"])
    by_index: list[Train] = []
    for r in rows_of(calibre):
        gears = int(r["shape"])
        ratio = None if r.get("pair") is None else (int(r["pair"][0]), int(r["pair"][1]))
        teeth = None if r.get("wall") is None else int(r["wall"])
        if ratio is not None and ratio[0] < ratio[1] and gears == HAND + HAND:
            spin = [SPOKES * (full_rate + full_rate)] * HAND
            up = Train(HAND, ratio, teeth, gears_of(size, HAND, ratio, teeth, w, spin))
            down = Train(HAND, ratio, teeth, gears_of(size, HAND, ratio, teeth, w, spin))
            up.twin, down.twin = down, up
            by_index.append(up)
            continue
        dteeth = drive_teeth(gears, ratio, rim, full_rate, key, trace)
        by_index.append(Train(gears, ratio, teeth, gears_of(size, gears, ratio, teeth, w, dteeth)))
        by_index[-1].weight = r.get("weight")
    everything = [t for r in by_index for t in ((r,) if r.twin is None else (r, r.twin))]
    return sorted(everything, key=order_key), by_index


def train_of(trains: list[Train], size: int, ratio: tuple[int, int] | None = None) -> Train:
    """The one train of the size with a ratio, and of the ratio where given, chosen by the numbers alone (the unsprung hand: the hand of the offset's ratio)."""
    return next(
        r for r in trains if r.size == size and r.teeth is None and (ratio is None or r.ratio == ratio)
    )


def ratchet_of(trains: list[Train]) -> Train:
    """The one train with teeth of its own and no meshes."""
    return next(r for r in trains if r.teeth is not None)

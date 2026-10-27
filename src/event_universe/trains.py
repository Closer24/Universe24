"""The trains of the clock as the calibre names them, no name and no role (the owner's word of 2026-10-25, there is no if): a train is a size (its count of gears) with a ratio (pinion, rim) for Rule3's gearing or teeth of its own for a train with no meshes; its gears are built here with their teeth by size, the trains ordered for the acts (a size the law does not name refused by name at the assembly, assembly/piece); the lookups choose a train by its numbers alone. The standard length is the calibre's `amplitude`, declared from outside and read at the assembly (assembly/piece, clock.standard_length), carried above the shortest hand derived from Gamma (standard.shortest_hand); no width and no room of the machine stands in the engine (the owner's words of 2026-10-27, 04:0x and 04:4x UTC; the former width constant and the room cut from it struck, the value kept in the file so that every chart stands bit for bit)."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core.acts import mid
from event_universe.core.rule3 import carries, held_teeth
from event_universe.core.spokes import AXES, SPOKES

REGULATOR = 1 + AXES + AXES + AXES  # the regulator: its time gear, AXES tensions, flows and shears
OFFSET = AXES + 1  # the size of the train at (rim, rim): its time gear and its AXES odd gears
HAND = 2  # the size of a hand: its two gears, a conjugate pair
POWER_TIME = 4  # the vacuum's balance: X, the bracket and the rate; POWER_AXIS the rate's square
POWER_AXIS = 2
Ratio = tuple[int, int]


def zeros(size: tuple[int, ...]) -> Any:
    """An integer array of the great clock's size at 0 (Python integers, no width)."""
    return np.zeros(size, dtype=object)


class Train:
    """One train of the clock as the calibre names it: a size (its count of gears), a ratio (pinion, rim) for Rule3's gearing, or teeth of its own for a train with no meshes (the ratchet); its gears."""

    __slots__ = ("size", "ratio", "teeth", "gears", "twin")

    def __init__(self, size: int, ratio: Ratio | None, teeth: int | None, gears: list[Gear]) -> None:
        self.size, self.ratio, self.teeth, self.gears = size, ratio, teeth, gears
        self.twin: Train | None = None

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
    """The drive teeth of a train's gears by its size: the regulator's time gear and its other gears the held teeth at the file's trace weight (TW-S1, the owner's word of 2026-10-26, 07:5x UTC: the trace's weight is the calibre's integer, dimensionless, 6 in nature's files, the one value with a sentence in nature, light having no trace; 54 the charts' value of 2026-10-25 kept by name, ga2's file at it until its re-set; rule3.held_teeth at the powers POWER_TIME 4 of the time gear and POWER_AXIS 2 of the nine axis gears, K-S1 to K-S3, Y-S1), the offset train's four gears T, the hand at the calibre's own ratio (rim, rim), the unsprung hand, its first gear T (the advance of W-S1), another hand none."""
    if size == REGULATOR:
        powers = (POWER_TIME, *[POWER_AXIS] * (size - 1))
        return [held_teeth(trace, rim, full_rate, key, p) for p in powers]
    if size == OFFSET:
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


def trains_of(calibre: dict[str, Any], size: tuple[int, ...], w: int) -> tuple[list[Train], list[Train]]:
    """The trains from the calibre's list, each a size with a ratio or teeth of its own, in the acts' order, and the same trains in the file's order (a setting names a train by its index); the file's sizes refused by name: a size-1 train with a ratio (the unsprung hand is the hand whose ratio is (rim, rim)), a count of the regulator, the offset train, the unsprung hand or the ratchet other than one, the regulator off (rim - rim div Gamma, rim), the offset train off (rim, rim), no hand at another ratio; a ratio named in several trains is admitted as written, each train a hand of its own with the same numbers (CS5-S2, the owner's word of 2026-10-25, 22:50 UTC, through the Boss: no train refused for its ratio's repetition)."""
    ints = calibre["integers"]
    rim, full_rate, key = int(ints["den"]), int(ints["node_clock"]), int(ints["quantum_action"])
    trace = int(ints["trace"])
    by_index: list[Train] = []
    rate_ratio = (rim - carries(rim, full_rate), rim)
    for r in calibre["rows"]:
        gears = int(r["shape"])
        ratio = None if r.get("pair") is None else (int(r["pair"][0]), int(r["pair"][1]))
        teeth = None if r.get("wall") is None else int(r["wall"])
        if gears == 1 and teeth is None:
            raise ValueError("a shape-1 row with a pair: the gap-0 row is the plane at (den, den)")
        if ratio is not None and ratio[0] < ratio[1] and ratio != rate_ratio and gears == HAND + HAND:
            spin = [SPOKES * (full_rate + full_rate)] * HAND
            up = Train(HAND, ratio, teeth, gears_of(size, HAND, ratio, teeth, w, spin))
            down = Train(HAND, ratio, teeth, gears_of(size, HAND, ratio, teeth, w, spin))
            up.twin, down.twin = down, up
            by_index.append(up)
            continue
        dteeth = drive_teeth(gears, ratio, rim, full_rate, key, trace)
        by_index.append(Train(gears, ratio, teeth, gears_of(size, gears, ratio, teeth, w, dteeth)))
    everything = [t for r in by_index for t in ((r,) if r.twin is None else (r, r.twin))]
    trains = sorted(everything, key=order_key)
    ratchets = [r for r in trains if r.teeth is not None]
    hands = [r for r in trains if r.size == HAND]
    unsprung = [r for r in hands if r.ratio == (rim, rim)]
    regulators = [r for r in trains if r.size == REGULATOR]
    offsets = [r for r in trains if r.size == OFFSET]
    if len(ratchets) != 1 or len(unsprung) != 1 or len(regulators) != 1 or len(offsets) != 1:
        raise ValueError(
            "the universe names one row with its own wall, one plane at the gap 0, one shape-10 row and one shape-4 row"
        )
    if regulators[0].ratio != rate_ratio:
        raise ValueError(
            "the shape-10 row is the clock's one level: its pair (den - den div Gamma, den)"
        )
    if offsets[0].ratio != (rim, rim):
        raise ValueError("the shape-4 row stands at (den, den)")
    if len(hands) == len(unsprung):
        raise ValueError("the universe names no plane row with a gap")
    return trains, by_index


def train_of(trains: list[Train], size: int, ratio: tuple[int, int] | None = None) -> Train:
    """The one train of the size with a ratio, and of the ratio where given, chosen by the numbers alone (the unsprung hand: the hand of the offset's ratio)."""
    return next(
        r for r in trains if r.size == size and r.teeth is None and (ratio is None or r.ratio == ratio)
    )


def ratchet_of(trains: list[Train]) -> Train:
    """The one train with teeth of its own and no meshes."""
    return next(r for r in trains if r.teeth is not None)


def hands_of(trains: list[Train]) -> list[Train]:
    """The hand trains in the acts' order, the hands (the unsprung hand among them)."""
    return [r for r in trains if r.size == HAND]

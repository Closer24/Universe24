"""The click's reads and writes at one clock: the exact unwind's count read at unspring.fall_of by the wind's own fall (the unwind act at a list of ends is unspring.unwinds, CR-S2), the one advance act (`advance`) and the unwind's move as the drive's form (`move`, CR-S1), the lattice push a move tallies (`push_of`) and the jam by name (`jammed`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import acts
from event_universe.core.spokes import AXES, SPOKE_SIDES, SPOKES, spoke_of, wrap
from event_universe.meshes import cross
from event_universe.trains import HAND, REGULATOR, Gear, zeros

if TYPE_CHECKING:
    from event_universe.clock import Clock


def neighbour(clock: Clock, at: tuple[int, ...], spoke: int) -> tuple[int, ...]:
    """The clock beyond the spoke of the clock `at`, on the torus (fd2, U3): the one spelling of a neighbour's place, as `across` is the one read of a neighbour's array."""
    axis, side = SPOKE_SIDES[spoke]
    return tuple(wrap(at[a] + (side if a == axis else 0), clock.cube) for a in range(AXES))


def window_clocks(clock: Clock, at: tuple[int, ...]) -> list[tuple[int, ...]]:
    """The clock and its six neighbours in spoke order."""
    return [at] + [neighbour(clock, at, spoke) for spoke in range(SPOKES)]


def at_clock(x: Any, at: tuple[int, ...]) -> int:
    """A gearing's integer at a clock (a ratchet's grips are the one integer 0)."""
    return int(np.asarray(x)[at]) if np.ndim(x) else int(x)


def advance(clock: Clock, rec: int, where: Any, notches: Any, sign: int = 1) -> None:
    """The one advance act: a hand's notches (now, before per gear: three_now, three_before, twelve_now, twelve_before for a hand) added at the clock `where` (or over the great clock), taken back with sign -1 (the setting's forms, the fitted hands, an unspringing's ends unwound whole and their undoing); the unwind's move on one gear is `move` (CR-S1)."""
    gears = clock.hands()[rec].gears
    for gear, now, before in zip(gears, notches[0::HAND], notches[1::HAND], strict=True):
        gear.now[where] = acts.advance(gear.now[where], now, sign)
        gear.before[where] = acts.advance(gear.before[where], before, sign)


def push_of(
    clock: Clock, gears: list[Gear], at: tuple[int, ...], notches: Any, pinion: int, sign: int = 1
) -> list[int]:
    """The push an advance tallies at the clock `at`, the change of P_a = 2 pinion SUM_i (now_(i+a) . before_i - now_i . before_(i+a)), the dot over the hand's gears (Re conj(a) b of the Gaussian hand), when the gears' notches now and before move by the advance's `notches` (now, before per gear) times `sign`: 2 pinion SUM over the gears [d_now (before_(i-a) - before_(i+a)) + d_before (now_(i+a) - now_(i-a))] per axis; a one-gear advance is its gear with the before notch 0."""
    found = []
    for a in range(AXES):
        up, down = neighbour(clock, at, spoke_of(a, 0)), neighbour(clock, at, spoke_of(a, 1))
        dots = (
            cross(dn, db, int(g.now[down]) - int(g.now[up]), int(g.before[down]) - int(g.before[up]))
            for g, dn, db in zip(gears, notches[0::HAND], notches[1::HAND], strict=True)
        )
        found.append(sign * (pinion + pinion) * sum(dots))
    return found


def move(clock: Clock, rec: int, k: int, at: tuple[int, ...], count: int) -> None:
    """The unwind's move, the clock's drive act at one clock (CR-S1, the owner's word of 2026-10-26, 06:1x UTC): one carry at the gear's own teeth of the exact numerator, the count times the teeth, the carries advanced on the gear's notch now by the one advance act and the fine tooth unmoved; the unwind forward, its return and its undoing are this one act with the count's sign; not the tick's drive act, whose teeth are the gear's drive teeth, which the unwound gear does not hold. The former take_at (one Node's take, EX-S1's remainder owed at it) is kept by name: its act is unspring.unwinds."""
    gears = clock.hands()[rec].gears
    teeth = at_clock(gears[k].teeth, at)
    q, _unmoved = acts.carry(count * teeth, teeth, int(gears[k].fine[at]), 1)
    advance(clock, rec, at, tuple(q if j == HAND * k else 0 for j in range(HAND * len(gears))))


def recoil(
    clock: Clock, where: tuple[int, ...], push: list[int], rate: int, going: int
) -> dict[str, Any]:
    """The move's tally driven on the mesh's hand the clock holds (LT-S1, the owner's word of 2026-10-26, 08:4x UTC, "approve"; H-Lay-As-The-Take-Reversed-1, the advance as the unwind reversed read on the mesh's hand): the push a move tallies at its clock (push_of, the change of the hands' lead on the clock's six meshes) is driven per axis on the regulator's flow gear of that axis at that clock by the clock's one drive act (one carry at the gear's drive teeth, the carry in its drive fine; Y-S3's gear, whose source summed over the great clock is the hands' push negated, so the gear gains what the moved winding lost, -dP, at the rate squared by the position of the reading, and the hands' and the lattice's push sum to what they were: the Boss's correction of the sign under the delegation of 00:57, 2026-10-26, 10:18 UTC, the derivation's line 19 having carried the move's sign where the sentence means the tally's), in the going given, the same act at -1 undoing it from the log's numbers; so the push and the angular momentum at every click are an identity, -dP_a rate^2 + dfine_a - dfine_a' = q_a K rim full_rate^2 key. Returns the log's numbers: the rate, the notches advanced per axis, the drive fine before and after."""
    gears = clock.train(REGULATOR).gears[1 + AXES : 1 + AXES + AXES]
    was, advanced = [int(gear.dfine[where]) for gear in gears], []
    for gear, p in zip(gears, push, strict=True):
        numerator = zeros(clock.size)
        numerator[where] = -p * rate * rate
        notch = int(gear.now[where])
        clock.drive(gear, numerator, going)
        advanced.append(int(gear.now[where]) - notch)
    return {
        "clock": rate,
        "recoil": advanced,
        "carry_was": was,
        "carry": [int(gear.dfine[where]) for gear in gears],
    }

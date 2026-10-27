"""The striking's reads and writes at one clock: the exact unwind of the unwound hand's notches by the wind's fall on the gear the fall's sign chooses (`fall_of`; the unwind act at a list of ends is unspring.unwinds, CR-S2), the one advance act (`advance`) and the unwind's move as the drive's form (`move`, CR-S1), the lattice push a move tallies (`push_of`) and the jam by name (`jammed`)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core import acts, rule3
from event_universe.core.rule3 import carries
from event_universe.core.spokes import AXES, SPOKE_SIDES, SPOKES, spoke_of, wrap
from event_universe.meshes import cross
from event_universe.trains import HAND, REGULATOR, Gear, Train, zeros

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


def fall_of(
    clock: Clock, at: tuple[int, ...], windings: int, r: rule3.Gearing, hand: Train, going: int = 1
) -> tuple[int | None, int, int]:
    """The exact unwind at the clock in the regulator's winding (PM-S1) on the gear the fall's sign chooses (CS4-S2, the owner's word of 2026-10-25 through the Boss: the unwound hand's gear whose notch now stands farthest from its before, the largest now^2 - before^2, the first gear where equal, so the unwind is covariant under the hand's quarter turn; the former first line kept by name): the unwound gear's now moved toward its before by the least count of notches at which the clock's wind falls by the windings (0 where nothing is due, EX-S1); the fall f(s) = s (price - stretch teeth s) over the wind's weight 2 full_rate^3 G^2, the price the stretch times Rule3's own numerator with the slots exchanged, -t (2 teeth now + pull); the count one carry of the windings due over the price, rounded up as the floor's flip, and where the moved notches' own square leaves the fall short, the same carry of the shortfall over the next notch's price, price - 2 stretch teeth s, iterated from below to its fixed count (TC-S1, the owner's word of 2026-10-26, 08:3x UTC, "approved", both hands' one finding, H-Take-Count-As-Rule3-Division-1: the count Rule3's own kind of act, no root; the former least root by largest_below, least_root, kept by name); (None, the full fall) where no count within the full move pays, the carry's fixed count passing the move or the next notch's price falling to 0 before it; at -1 the exact unwind reversed, the unspringing's unsprung windings (MG-S1; the former merger.rise_of kept by name, folded 2026-10-26 on the Boss's 6413888338): the gear's now moved away from its before (the tie resolved as away at -1, cc1) by the least count at which the wind rises by the windings, the rise the same quadratic with the going's sign on the square term, s (price + stretch teeth s), convex, so the same carry is iterated from above, the first carries paying and each step the excess carried over the next notch's price, to its fixed count, never jammed (the former jam read the fall at the full move alone, the parabola's far side, and jammed an unwind a lesser count paid: the bug struck 2026-10-26 under the owner's priority, the Boss's 6411031946)."""
    gaps = [n * n - b * b for n, b in ((int(z.now[at]), int(z.before[at])) for z in hand.gears)]
    k = gaps.index(max(gaps))
    gear = hand.gears[k]
    now, before = int(gear.now[at]), int(gear.before[at])
    if windings <= 0 and going == 1:
        return 0, 0, k
    if now == before and going == 1:
        return None, 0, k
    t = (1 if before > now else -1) if going == 1 else (1 if now > before else -1)
    hold, w, gripped = int(np.asarray(r.hold)[at]), int(r.teeth), 0
    for spoke, grip in enumerate(r.grips):
        gripped += int(np.asarray(grip)[at]) * int(gear.before[neighbour(clock, at, spoke)])
    pull = hold * before + gripped
    x, weight = int(clock.start_stretch[at]), rule3.wind_weight(clock.full_rate, clock.G)

    def fall(s: int) -> int:
        moved = now + t * s
        return int(carries(going * x * (w * (now * now - moved * moved) - t * s * pull), weight))

    price, dist = -t * going * ((w + w) * now + pull) * x, abs(now - before)
    if going == -1:
        s = (
            -carries(-windings * weight, price)
            if price > 0
            else -carries(price, x * w) - carries(-windings * weight, x * w)
        )
        while s > 1 and fall(s - 1) >= windings:
            s -= max(1, carries(s * (price + x * w * s) - windings * weight, price + x * w * (s + s)))
        return s, fall(s), k
    s = -carries(-windings * weight, price) if price > 0 else dist + 1
    while s <= dist and fall(s) < windings:
        slope = price - x * w * (s + s)
        s = s - carries(-(windings * weight - s * (price - x * w * s)), slope) if slope > 0 else dist + 1
    if s > dist:
        return None, fall(dist), k
    return s, fall(s), k


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
    """The move's tally driven on the mesh's hand the clock holds (LT-S1, the owner's word of 2026-10-26, 08:4x UTC, "approve"; H-Lay-As-The-Take-Reversed-1, the advance as the unwind reversed read on the mesh's hand): the push a move tallies at its clock (push_of, the change of the hands' lead on the clock's six meshes) is driven per axis on the regulator's flow gear of that axis at that clock by the clock's one drive act (one carry at the gear's drive teeth, the carry in its drive fine; Y-S3's gear, whose source summed over the great clock is the hands' push negated, so the gear gains what the moved winding lost, -dP, at the rate squared by the position of the reading, and the hands' and the lattice's push sum to what they were: the Boss's correction of the sign under the delegation of 00:57, 2026-10-26, 10:18 UTC, the derivation's line 19 having carried the move's sign where the sentence means the tally's), in the going given, the same act at -1 undoing it from the log's numbers; so the push and the angular momentum at every strike are an identity, -dP_a rate^2 + dfine_a - dfine_a' = q_a K rim full_rate^2 key. Returns the log's numbers: the rate, the notches advanced per axis, the drive fine before and after."""
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

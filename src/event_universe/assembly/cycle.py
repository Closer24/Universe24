"""The `wave` setting, the light's cycle pattern at every clock (CS5-S2's piece, the owner's word of 2026-10-25, 22:50 UTC, "all of them", through the Boss; cs3's cycle form in cs5's and cs7's spelling, the setting cs5_run.lay_pattern set by script beside the engine, here the piece's own form): `{"lay": "wave", "row": r, "quanta": n, "p1": [16 digits], "cz": c, "mirror": m}`, the angle p(x, y, z) = (p1[4 (x mod 4) + (y mod 4)] + c z) mod 4 in Z_4 at every clock, the light z_now = A i^p and z_before = A i^(p + 1) (the quarter turn per tick, cs1's eigenmode; on the cycle cover the passing meshes flow into every clock once, cs3), A the least hand length whose least wind over the great clock is at or above n windings of the light, set by the one advance, the negated gears' fine teeth flipped where m is 1 (cs1's gauge); refused by name off Z_4, off 0 and 1, and on a cube whose extent is not a multiple of 4; setting.set_piece names the form and its train."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe import hands, readings
from event_universe.core import acts
from event_universe.core.rule3 import least_at, remainder
from event_universe.core.spokes import AXES
from event_universe.meshes import factors
from event_universe.run import logged
from event_universe.trains import HAND, REGULATOR, Gear, zeros
from event_universe.unwind import advance

if TYPE_CHECKING:
    from event_universe.clock import Clock

QUARTER = (
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
)  # i^q as (three, twelve) for q in Z_4, the quarter turns of the hand
QUARTERS = len(QUARTER)  # the order of i, the cycle setting's digits and the side of its pattern


def cycle_angles(clock: Clock, digits: list[int]) -> Any:
    """The cycle form's angle digit of Z_4 at every clock (cs3's spelling), p(x, y, z) = (p1[4 (x mod 4) + (y mod 4)] + cz z) mod 4 from the sixteen digits p1 and the digit cz after them."""
    found = zeros(clock.size)
    for at in np.ndindex(*clock.size):
        x, y, z = (remainder(v, QUARTERS) for v in at)
        found[at] = remainder(digits[QUARTERS * x + y] + digits[QUARTERS * QUARTERS] * z, QUARTERS)
    return found


def cycle_notches(p: Any, hand_length: int) -> tuple[Any, ...]:
    """The light's four notches from the angle digits at a hand length A (three_now, three_before, twelve_now, twelve_before): z_now = A i^p and z_before = A i^(p + 1), the quarter turn per tick of cs1's eigenmode."""
    found = [zeros(p.shape) for _ in range(HAND * HAND)]
    for at in np.ndindex(*p.shape):
        for k, q in enumerate((int(p[at]), remainder(int(p[at]) + 1, QUARTERS))):
            found[k][at], found[HAND + k][at] = (hand_length * v for v in QUARTER[q])
    return tuple(found)


def set_cycle(clock: Clock, rec: int, n: int, digits: list[int], flip: int) -> None:
    """The cycle setting of the light (CS5-S2's piece; cs3's cycle form as cs5's cs5_run.lay_pattern set it by flag, here the file's own form): the angle digits at every clock (`cycle_angles`) set at the least hand length whose least wind over the great clock is at or above n windings of the light (the search by comparisons, doubling then halving) by the one advance over what stands, the negated gears' fine teeth flipped once where the flip is 1 (cs1's gauge: the fine tooth of a gear whose notch is negated, as the reverse flips it); refused by name off Z_4, off 0 and 1, and on a cube whose extent is not a multiple of 4; the setting logged with its digits and the sense 1, the quarter turn."""
    train = clock.hands()[rec]
    assert train.ratio is not None
    if len(digits) != QUARTERS * QUARTERS + 1 or any(d not in range(QUARTERS) for d in digits):
        raise ValueError("the cycle form is sixteen digits p1 and one digit cz, each of Z_4")
    if flip not in (0, 1):
        raise ValueError("the cycle lay's mirror is 0 or 1")
    if remainder(clock.cube, QUARTERS):
        raise ValueError("the cycle pattern is 4 by 4: the cube's extent is a multiple of 4")
    p = cycle_angles(clock, digits)
    clock.start_load, clock.start_stretch = readings.load(clock), clock.train(REGULATOR).gears[0].now
    gearing = readings.gearing(clock, train.ratio, clock.start_load, factors(clock))
    base = [x for gear in train.gears for x in (gear.now, gear.before)]

    def least_wind(hand_length: int) -> int:
        notches = cycle_notches(p, hand_length)
        gears = [
            Gear(base[k] + notches[k], base[k + 1] + notches[k + 1], None, None)
            for k in range(0, HAND * HAND, HAND)
        ]
        return min(int(x) for x in hands.wind(clock, gears, gearing).reshape(-1))

    target = n * clock.windings[rec]
    high = least_at(lambda hand_length: least_wind(hand_length) >= target)
    notches = cycle_notches(p, high)
    advance(clock, rec, Ellipsis, notches)
    for gear, now, before in zip(train.gears, notches[0::HAND], notches[1::HAND], strict=True):
        negated = np.vectorize(lambda a, b: int(a) < 0 or int(b) < 0, otypes=[bool])(now, before)
        gear.fine = np.where(negated & (flip == 1), acts.flip(gear.fine, gear.teeth, 1), gear.fine)
    logged(
        clock,
        "lay",
        None,
        line_pair=rec,
        quanta=n,
        amplitude=high,
        share=least_wind(high),
        unit=clock.windings[rec],
        nodes=int(clock.cube) ** AXES,
        sense=1,
        p1=digits[: QUARTERS * QUARTERS],
        cz=digits[QUARTERS * QUARTERS],
        mirror=flip,
    )

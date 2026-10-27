"""The `wave` lay, the light's cycle pattern at every Node (CS5-S2's world, the owner's word of 2026-10-25, 22:50 UTC, "all of them", through the Boss; cs3's cycle form in cs5's and cs7's spelling, the lay cs5_run.lay_pattern laid by script beside the engine, here the world file's own form): `{"lay": "wave", "row": r, "quanta": n, "p1": [16 digits], "cz": c, "mirror": m}`, the phase p(x, y, z) = (p1[4 (x mod 4) + (y mod 4)] + c z) mod 4 in Z_4 at every Node, the light z_now = A i^p and z_before = A i^(p + 1) (the quarter turn per interval, cs1's eigenmode; on the cycle cover the passing Links flow into every Node once, cs3), A the least amplitude whose least share over the board is at or above n quanta of the light, laid by the one lay act, the negated lines' remainders mirrored where m is 1 (cs1's gauge); refused by name off Z_4, off 0 and 1, and on a cube whose extent is not a multiple of 4; seed.lay_world names the form and its row."""

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

QUARTERS = 4  # the quarter turns of Z_4, the cycle lay's digits and the side of its 4 by 4 pattern
QUARTER = ((1, 0), (0, 1), (-1, 0), (0, -1))  # i^q as (re, im) for q in Z_4


def cycle_angles(node: Clock, digits: list[int]) -> Any:
    """The cycle form's phase digit of Z_4 at every Node (cs3's spelling), p(x, y, z) = (p1[4 (x mod 4) + (y mod 4)] + cz z) mod 4 from the sixteen digits p1 and the digit cz after them."""
    found = zeros(node.size)
    for at in np.ndindex(*node.size):
        x, y, z = (remainder(v, QUARTERS) for v in at)
        found[at] = remainder(digits[QUARTERS * x + y] + digits[QUARTERS * QUARTERS] * z, QUARTERS)
    return found


def cycle_notches(p: Any, amplitude: int) -> tuple[Any, ...]:
    """The light's four levels from the phase digits at an amplitude A (re_now, re_before, im_now, im_before): z_now = A i^p and z_before = A i^(p + 1), the quarter turn per interval of cs1's eigenmode."""
    found = [zeros(p.shape) for _ in range(HAND * HAND)]
    for at in np.ndindex(*p.shape):
        for k, q in enumerate((int(p[at]), remainder(int(p[at]) + 1, QUARTERS))):
            found[k][at], found[HAND + k][at] = (amplitude * v for v in QUARTER[q])
    return tuple(found)


def set_cycle(node: Clock, rec: int, n: int, digits: list[int], mirror: int) -> None:
    """The cycle lay of the light (CS5-S2's world; cs3's cycle form as cs5's cs5_run.lay_pattern laid it by flag, here the file's own form): the phase digits at every Node (`cycle_phases`) laid at the least amplitude whose least share over the board is at or above n quanta of the light (the search by comparisons, doubling then halving) by the one lay act over what stands, the negated lines' remainders mirrored once where the mirror is 1 (cs1's gauge: the remainder of a line whose level is negated, as the exchange mirrors it); refused by name off Z_4, off 0 and 1, and on a cube whose extent is not a multiple of 4; the lay logged with its digits and the sense 1, the quarter turn."""
    row = node.hands()[rec]
    assert row.ratio is not None
    if len(digits) != QUARTERS * QUARTERS + 1 or any(d not in range(QUARTERS) for d in digits):
        raise ValueError("the cycle form is sixteen digits p1 and one digit cz, each of Z_4")
    if mirror not in (0, 1):
        raise ValueError("the cycle lay's mirror is 0 or 1")
    if remainder(node.cube, QUARTERS):
        raise ValueError("the cycle pattern is 4 by 4: the cube's extent is a multiple of 4")
    p = cycle_angles(node, digits)
    node.start_load, node.start_stretch = readings.load(node), node.train(REGULATOR).gears[0].now
    rule = readings.gearing(node, row.ratio, node.start_load, factors(node))
    base = [x for line in row.gears for x in (line.now, line.before)]

    def least_share(amplitude: int) -> int:
        levels = cycle_notches(p, amplitude)
        lines = [
            Gear(base[k] + levels[k], base[k + 1] + levels[k + 1], None, None)
            for k in range(0, HAND * HAND, HAND)
        ]
        return min(int(x) for x in hands.wind(node, lines, rule).reshape(-1))

    target = n * node.windings[rec]
    high = least_at(lambda amplitude: least_share(amplitude) >= target)
    levels = cycle_notches(p, high)
    advance(node, rec, Ellipsis, levels)
    for line, now, before in zip(row.gears, levels[0::HAND], levels[1::HAND], strict=True):
        negated = np.vectorize(lambda a, b: int(a) < 0 or int(b) < 0, otypes=[bool])(now, before)
        line.fine = np.where(negated & (mirror == 1), acts.flip(line.fine, line.teeth, 1), line.fine)
    logged(
        node,
        "lay",
        None,
        line_pair=rec,
        quanta=n,
        amplitude=high,
        share=least_share(high),
        unit=node.windings[rec],
        nodes=int(node.cube) ** AXES,
        sense=1,
        p1=digits[: QUARTERS * QUARTERS],
        cz=digits[QUARTERS * QUARTERS],
        mirror=mirror,
    )

"""The vernier, the one-mesh read of a number at a clock (the former take.read_number, moved whole; the unwind's module holds the unwind and the advance alone): every gear's fine tooth at the clock on the clock's own pitch and at each neighbour on the mesh's pitch, the digits composed modulo the unwound train's winding times the hands' count; jammed by name at the origin and where every pitch is coarse."""

from __future__ import annotations

from functools import cache
from typing import TYPE_CHECKING

from event_universe.core import acts, rule3
from event_universe.core.rule3 import carries, pitch, remainder
from event_universe.core.spokes import AXES
from event_universe.trains import HAND, Gear
from event_universe.unwind import at_clock, window_clocks

if TYPE_CHECKING:
    from event_universe.clock import Clock

kept_pitch = cache(pitch)  # the pitch kept by its integers within a strike, cleared at every strike
kept_mid = cache(acts.mid)  # a teeth's mid tooth kept within a strike alike


def vernier(
    clock: Clock, at: tuple[int, ...], gearings: list[tuple[Gear, rule3.Gearing]], winding: int
) -> tuple[int, int] | None:
    """The one-mesh read: every gear's fine tooth at the clock on the clock's own pitch F_i = gcd(w, D_i, R_i1..R_i6) and at each neighbour on the mesh's pitch gcd(w, R_ji), the digit read in the frame of the gear's own displacement at the clock (the one mirror, David's DAVID-THE-ONE-MIRROR.md: an image that negates a gear's whole field moves every fine tooth r to 2 o - r about the mid tooth o it was born at, the turnover's mirror keeping it there (acts.mirror), and turns the sign s of the displacement r - o at the clock with it, so the digit (o + s (r - o)) div F reads alike in the image; where the clock's own tooth stands at its origin, s = 0, the window folds onto its upper side, (o + |r - o|) div F; the former digit r div F, which parted the cube's 24 at the first draw, kept by name), the base w div F + 1, sorted by value, composed modulo M = the unwound train's winding times the hands' count, the size-2 hands the vernier names (the carry); jammed by name at the origin (every fine tooth at the mid tooth) and where every pitch is coarse (A48-S1's read in the advance's pawl, a48b's form, built at 05cca50 and reverted: the 48 on the strikes held to the tick 10 and parted at 11 on every reflection at the tie of the sign train's time gear's drive fine tooth, and the cycle setting's vernier reads fell on the origin; it returns with its mend)."""
    modulus = winding * sum(1 for r in clock.hands() if r.size == HAND)
    clocks, digits, origin, coarse, mid = window_clocks(clock, at), [], True, True, acts.mid(clock.teeth)
    for gear, r in gearings:
        centre = int(gear.fine[at]) - kept_mid(at_clock(gear.teeth, at))
        sense = (centre > 0) - (centre < 0)
        for k, n in enumerate(clocks):
            teeth, key = at_clock(gear.teeth, n), (id(r), k, n)
            if key not in clock.pitches:
                clock.pitches[key] = (
                    kept_pitch(teeth, at_clock(r.spring, n), *[at_clock(x, n) for x in r.grips])
                    if k == 0
                    else kept_pitch(teeth, at_clock(r.grips[(k - 1) ^ 1], n))
                )
            fine, values = int(gear.fine[n]), carries(teeth, f := clock.pitches[key])
            origin = origin and fine in (mid, acts.flip(mid, clock.teeth, 1))
            coarse = coarse and values <= AXES
            o = kept_mid(teeth)
            framed = o + sense * (fine - o) + (1 - sense * sense) * abs(fine - o)
            digits.append((carries(framed, f), values + 1))
    if origin or coarse:
        clock.counts["refused_origin"] += origin
        return None
    carry, room = 0, 1
    for d, b in sorted(digits):
        carry = remainder(carry * b + d, modulus)
        room = min(room * b, modulus)
    return carry, room

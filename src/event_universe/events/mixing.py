"""The Node's computation of the sides: the kernels over one family's arrays
(node-mixing-v2, the law of events).

Highlights 5.4, point 24 read under the law of events: at every Node the
events of one number that arrived on the six headings are one amplitude each,
sqrt(amount) in 32nds at the step nearest their coherent sum; the leaving
amplitude of each heading is the coherent sum less three times the arrival
that came in through its Port; the total is shared by the squared leaving
amplitudes in whole units: the floors per heading and the units left to the
largest remainders, one each, ties broken in Port order counted from the
interval's tick (so no heading is favoured over time); a group with no whole
for any side, fewer units than a side's whole share, goes whole to one side,
the heading nearest the momentum it carries, on a tie the largest share,
then the Port order from the tick. Nothing parks and the Node keeps nothing:
a single unit leaves whole by its momentum. The momentum the group carries
goes with the units placed (`apportion_carried`), exact per axis, the same
ties. The kernels are exact in bounded integers: the only float is the
square root's estimate, corrected to the exact integer root on both sides
before it is used.

A family that declares no phase circle (`"phase": false`, the model owner,
2026-09-19: the field of matter without phase) does not sum coherently at a
Node: each Port's arrival scatters on its own (`scatter_arrivals`) with the
shares of a lone arrival, four ninths back out through the Port it came in
by and one ninth to each of the other five sides, whole units by the largest
remainder with the ties in the tick's Port order, per Port; a Port's arrival
with no whole share for any side (one or two units) goes whole to the heading
nearest its own momentum, on a tie the largest share (back), then the tick's
order; its momentum is apportioned over its own departures exactly per axis
(`apportion_carried` per Port), and the six Ports' departures are added per
heading. Two arrivals through opposite Ports never cancel: each leaves four
ninths back and the transverse sides read one ninth of each.

The arrays are those of `MixingArrays`, whatever their leading axes; the
engine's transit (`event_universe.events.transit`) is one such family with
the axes (x, y, z, number).
"""

from __future__ import annotations

from typing import Protocol

import numpy as np

from event_universe.core.lattice import MAX_VALUE, MIXING_OPPOSITE, PORT_HEADINGS

MIXING_AMPLITUDE_SCALE = 32
MIXING_WEIGHT_BITS = 28
# The shares of a lone arrival for a family without a phase circle: four
# ninths back out through the Port it came in by, one ninth each other way.
SCATTER_BACK = 4
SCATTER_TOTAL = 9
# The six unit-axial headings in Port order, as an array, and the opposite of
# each (the travel heading of the arrival that came in through a Port).
HEADINGS = np.array(PORT_HEADINGS, dtype=np.int64)
OPPOSITE = np.array(MIXING_OPPOSITE, dtype=np.int64)


def tie_order(tick: int) -> np.ndarray:
    """The Ports ranked against each other for a tie: [k, h] is whether Port k
    comes before Port h, in Port order counted from the interval's tick."""
    rank = (np.arange(6) - tick) % 6
    return rank[:, None] < rank[None, :]


class MixingArrays(Protocol):
    """The arrays one family's mixing reads and writes, whatever the leading
    axes: `arr_*` the arrivals per Node and group with a travel Port axis of
    six (the momentum with three components after it), `fly_*` the departures
    in the arrivals' shape. The engine's transit
    (`event_universe.events.transit`) is one such family with the axes
    (x, y, z, number)."""

    arr_amt: np.ndarray
    arr_ph: np.ndarray
    arr_mom: np.ndarray
    fly_amt: np.ndarray
    fly_ph: np.ndarray
    fly_mom: np.ndarray
    tick: int
    cosines: np.ndarray | None
    sines: np.ndarray | None
    mix_cosines: np.ndarray
    mix_sines: np.ndarray

    def _nearest_step(self, x: np.ndarray, y: np.ndarray) -> np.ndarray: ...


def integer_root(scaled: np.ndarray) -> np.ndarray:
    """The integer square root of every entry, the floor, exact (the float
    root corrected by one either way)."""
    root = np.floor(np.sqrt(scaled.astype(np.float64))).astype(np.int64)
    root = np.where(root * root > scaled, root - 1, root)
    return np.where((root + 1) * (root + 1) <= scaled, root + 1, root)


def mix_arrivals(
    family: MixingArrays, momentum_bound: int = MAX_VALUE
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The Node's computation at every Node, per group (one number): the
    units leaving per heading, their phases and the momenta they carry."""
    amounts = family.arr_amt.astype(np.int64)
    phases = family.arr_ph.astype(np.int64)
    shape = amounts.shape
    if amounts.max(initial=0) > MAX_VALUE:
        raise ValueError("value exceeds the disturbance integer bound")
    if family.cosines is None or family.sines is None:
        port_phase = np.zeros(shape, dtype=np.int64)
    else:
        x = amounts * family.cosines[phases]
        y = amounts * family.sines[phases]
        port_phase = family._nearest_step(x, y)
    # The amplitudes, the integer square root of amount x 32^2.
    scaled = amounts * (MIXING_AMPLITUDE_SCALE * MIXING_AMPLITUDE_SCALE)
    root = integer_root(scaled)
    ax = root * family.mix_cosines[port_phase]
    ay = root * family.mix_sines[port_phase]
    sum_x = ax.sum(axis=-1, keepdims=True)
    sum_y = ay.sum(axis=-1, keepdims=True)
    cx = sum_x - 3 * ax[..., OPPOSITE]
    cy = sum_y - 3 * ay[..., OPPOSITE]
    if max(int(np.abs(cx).max(initial=0)), int(np.abs(cy).max(initial=0))) >= 1 << 31:
        raise OverflowError("64-bit intermediate range exceeded")
    weights = cx * cx + cy * cy
    weight_total = weights.sum(axis=-1)
    bits = np.zeros(weight_total.shape, dtype=np.int64)
    for bit in range(1, 64):
        bits = np.where((weight_total >> (bit - 1)) > 0, bit, bits)
    shift = np.maximum(bits - MIXING_WEIGHT_BITS, 0)
    reduced = weights >> shift[..., None]
    reduced_total = reduced.sum(axis=-1)
    present = reduced_total > 0
    divisor = np.where(present, reduced_total, 1)
    units = amounts.sum(axis=-1)
    product = units[..., None] * reduced
    quotas = np.where(present[..., None], product // divisor[..., None], 0)
    remainders = np.where(present[..., None], product - quotas * divisor[..., None], 0)
    left = units - quotas.sum(axis=-1)
    order = tie_order(family.tick)
    # The units left to the largest remainders, ties in the tick's Port order.
    ahead = (
        (remainders[..., :, None] > remainders[..., None, :])
        | ((remainders[..., :, None] == remainders[..., None, :]) & order)
    ).sum(axis=-2)
    repaired = quotas + (ahead < left[..., None])
    # A group with no whole for any side goes whole to the heading nearest the
    # momentum it carries; on a tie the largest share, then the tick's order.
    carried = family.arr_mom.astype(np.int64).sum(axis=-2)
    dots = carried @ HEADINGS.T
    candidates = dots == dots.max(axis=-1, keepdims=True)
    masked = np.where(candidates, reduced, -1)
    candidates &= masked == masked.max(axis=-1, keepdims=True)
    rank = (np.arange(6) - family.tick) % 6
    chosen = np.where(candidates, rank, 6).argmin(axis=-1)
    by_momentum = np.where(
        np.arange(6)[(None,) * left.ndim + (slice(None),)] == chosen[..., None], units[..., None], 0
    )
    whole = np.where((quotas.sum(axis=-1) == 0)[..., None], by_momentum, repaired)
    if family.cosines is None or family.sines is None:
        leaving_phase = np.zeros(shape, dtype=np.int64)
    else:
        sum_phase = family._nearest_step(sum_x[..., 0], sum_y[..., 0])
        leaving_phase = np.where(
            weights > 0, family._nearest_step(cx, cy), np.broadcast_to(sum_phase[..., None], shape)
        )
    momenta = apportion_carried(carried, whole, order)
    if int(np.abs(momenta).max(initial=0)) > momentum_bound:
        raise ValueError("value exceeds the disturbance integer bound")
    return whole, np.where(whole > 0, leaving_phase, 0), momenta


def scatter_arrivals(
    family: MixingArrays, momentum_bound: int = MAX_VALUE
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The Node's computation for a family without a phase circle, per group
    (one number): each Port's arrival scatters on its own, four ninths back
    out through the Port it came in by and one ninth to each of the other
    five sides, whole units by the largest remainder (ties in the tick's Port
    order), a Port's arrival with no whole for any side going whole to the
    heading nearest its own momentum (on a tie the largest share, then the
    tick's order); its momentum apportioned over its own departures exactly
    (`apportion_carried` per Port); the six Ports' departures added per
    heading. Returns the units leaving per heading, their phases (all 0)
    and the momenta they carry. Fixed local work, 64-bit integers."""
    amounts = family.arr_amt.astype(np.int64)
    shape = amounts.shape
    if amounts.max(initial=0) > MAX_VALUE:
        raise ValueError("value exceeds the disturbance integer bound")
    order = tie_order(family.tick)
    rank = (np.arange(6) - family.tick) % 6
    # The shares of a lone arrival per source Port and leaving heading, in
    # ninths: [k, h] is 4 where h is the Port k's arrival came in by, else 1.
    shares = np.ones((6, 6), dtype=np.int64)
    shares[np.arange(6), OPPOSITE] = SCATTER_BACK
    product = amounts[..., :, None] * shares
    quotas = product // SCATTER_TOTAL
    remainders = product - quotas * SCATTER_TOTAL
    left = amounts - quotas.sum(axis=-1)
    ahead = (
        (remainders[..., :, None] > remainders[..., None, :])
        | ((remainders[..., :, None] == remainders[..., None, :]) & order)
    ).sum(axis=-2)
    repaired = quotas + (ahead < left[..., None])
    # A Port's arrival with no whole for any side goes whole to the heading
    # nearest its own momentum; on a tie the largest share, then the tick's
    # order.
    carried = family.arr_mom.astype(np.int64)
    dots = carried @ HEADINGS.T
    candidates = dots == dots.max(axis=-1, keepdims=True)
    masked = np.where(candidates, shares, -1)
    candidates &= masked == masked.max(axis=-1, keepdims=True)
    chosen = np.where(candidates, rank, 6).argmin(axis=-1)
    by_momentum = np.where(np.arange(6) == chosen[..., None], amounts[..., None], 0)
    per_port = np.where((quotas.sum(axis=-1) == 0)[..., None], by_momentum, repaired)
    per_port = np.where((amounts > 0)[..., None], per_port, 0)
    momenta_per_port = apportion_carried(carried, per_port, order)
    whole = per_port.sum(axis=-2)
    momenta = momenta_per_port.sum(axis=-3)
    if int(np.abs(momenta).max(initial=0)) > momentum_bound:
        raise ValueError("value exceeds the disturbance integer bound")
    return whole, np.zeros(shape, dtype=np.int64), momenta


def apportion_carried(carried: np.ndarray, whole: np.ndarray, order: np.ndarray) -> np.ndarray:
    """A group's momentum shared over the six headings in proportion to the
    units placed on them, exact per axis: the floors, then the units left to
    the largest remainders, ties by `order` (`tie_order`); a negative
    component shared as its magnitude and negated. A group without units or
    without momentum shares nothing."""
    units = whole.sum(axis=-1)
    divisor = np.where(units > 0, units, 1)[..., None]
    outputs = np.zeros((*whole.shape, 3), dtype=np.int64)
    if not carried.any():
        return outputs
    if int(np.abs(carried).max(initial=0)) * int(whole.max(initial=0)) >= 1 << 62:
        raise OverflowError("64-bit intermediate range exceeded")
    for axis in range(3):
        magnitude = np.abs(carried[..., axis])
        product = magnitude[..., None] * whole
        quotient = product // divisor
        remainder = product - quotient * divisor
        left = np.where(units > 0, magnitude - quotient.sum(axis=-1), 0)
        ahead = (
            (remainder[..., :, None] > remainder[..., None, :])
            | ((remainder[..., :, None] == remainder[..., None, :]) & order)
        ).sum(axis=-2)
        quotient = quotient + (ahead < left[..., None])
        outputs[..., axis] = np.where((carried[..., axis] < 0)[..., None], -quotient, quotient)
    return outputs


def place_departures(
    family: MixingArrays,
    whole: np.ndarray,
    phase: np.ndarray,
    momenta: np.ndarray,
    momentum_bound: int = MAX_VALUE,
) -> None:
    """The units leaving per heading into the departures, with their phases
    and momenta."""
    if int(whole.max(initial=0)) > MAX_VALUE:
        raise ValueError("value exceeds the disturbance integer bound")
    if int(np.abs(momenta).max(initial=0)) > momentum_bound:
        raise ValueError("value exceeds the disturbance integer bound")
    family.fly_amt[...] = whole
    family.fly_ph[...] = np.where(whole > 0, phase, 0)
    family.fly_mom[...] = momenta

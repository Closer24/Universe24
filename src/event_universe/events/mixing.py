"""The Node's computation of the sides: the kernels over one family's arrays
(node-mixing-v3, the law of events).

Highlights 5.4, point 24 read under the law of events: at every Node the
events that arrived on the six headings are one amplitude each per number,
sqrt(amount) in 32nds at the step nearest their coherent sum, and the Node
reads what is present: the coherent sum runs over all the arrivals at the
Node, whatever their number (the number is a label for the detector, not a
kind; the model owner, 2026-09-19); the leaving amplitude of each heading is
the common sum less three times what came in through its Port over all
numbers; the weights of the sides, the squared leaving amplitudes, are common
to every number at the Node. Each number then places its own units by the
common weights in whole units: the floors per heading and the units left to
the largest remainders, one each, ties broken in Port order counted from the
interval's tick (so no heading is favoured over time); a number with no
whole for any side, fewer units than a side's whole share, goes whole to one
side, the heading nearest the momentum it carries, on a tie the largest
share, then the Port order from the tick. Nothing parks and the Node keeps
nothing: a single unit leaves whole by its momentum. Every unit keeps its
number; the leaving phase of a side is the common leaving amplitude's phase
for every number. The momentum each number carries goes with its units
placed (`apportion_carried`), exact per axis, the same ties. The kernels are
exact in bounded integers: the only float is the square root's estimate,
corrected to the exact integer root on both sides before it is used.

The rule of the Node is one (the model owner, 2026-09-19: "everything
generic must be replaced by generic"); only the weights of the sides know
whether the family has a phase circle. With one, the weights are the
coherent |c_h|^2 above (`coherent_weights`). A family that declares none
(`"phase": false`, the field of matter without phase) has mutually
incoherent arrivals: its weights are the diagonal of the same expansion
(`diagonal_weights`). With a_k the amplitude through Port k and
c_h = S - 3 a_opp(h), |c_h|^2 = |S|^2 - 6 Re(S conj(a_opp)) + 9 |a_opp|^2;
dropping every cross term between different arrivals leaves of |S|^2 the
squares sum_k |a_k|^2 = 32^2 sum_k amount_k, and of -6 Re(S conj(a_opp))
its own square -6 |a_opp|^2, so

    weight_h = 32^2 x (sum_k amount_k + 3 x amount_opp(h)),

exact integers, no root and no phase table. A lone arrival weighs
1 + 3 = 4 back and 1 to each other side, the four ninths back and one ninth
each other way of a lone scatter; two arrivals through opposite Ports never
cancel (each adds 3 x its amount to the side it came in by and its amount to
every side). The arrivals of different numbers are mutually incoherent too,
so no cross term survives between them either: a number's weights are the
squares of its own arrivals, another number at the Node adds nothing to
them (the sides' total is what common weights would give; the labels keep
each number's own transport, the field of two things the sum of the field
of each). The placement per number, the group with no whole going by its
momentum, `apportion_carried` and the leaving phase (0 for a phase-less
family) are the same code as for a family with a phase circle; the units
are placed once per number by its weights, not once per Port, so the
largest-remainder rounding falls per group (the per-Port scatter of the
first `events-v1`, `scatter_arrivals`, folded in on 2026-09-19).

The arrays are those of `MixingArrays`, whatever their leading axes, the
number axis next to the Port axis; the engine's transit
(`event_universe.events.transit`) is one such family with the axes
(x, y, z, number).
"""

from __future__ import annotations

from typing import Protocol

import numpy as np

from event_universe.core.lattice import MAX_VALUE, MIXING_OPPOSITE, PORT_HEADINGS

MIXING_AMPLITUDE_SCALE = 32
MIXING_WEIGHT_BITS = 28
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
    axes: `arr_*` the arrivals per Node with a number axis and then a travel
    Port axis of six (the momentum with three components after it), `fly_*`
    the departures in the arrivals' shape; `phased` whether the family has a
    phase circle (its weights the coherent sum's) or none (the diagonal).
    The engine's transit (`event_universe.events.transit`) is one such family
    with the axes (x, y, z, number)."""

    arr_amt: np.ndarray
    arr_ph: np.ndarray
    arr_mom: np.ndarray
    fly_amt: np.ndarray
    fly_ph: np.ndarray
    fly_mom: np.ndarray
    tick: int
    phased: bool
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


def coherent_weights(
    family: MixingArrays, amounts: np.ndarray, phases: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """The weights of the sides of a family with a phase circle: the coherent
    sum over all the arrivals present and the squared common leaving
    amplitudes. Returns the weights (a number axis of one), the common sum's
    components and the leaving amplitudes' components per side."""
    if family.cosines is None or family.sines is None:
        port_phase = np.zeros(amounts.shape, dtype=np.int64)
    else:
        x = amounts * family.cosines[phases]
        y = amounts * family.sines[phases]
        port_phase = family._nearest_step(x, y)
    # The amplitudes, the integer square root of amount x 32^2, per number
    # and Port; the Node reads what is present: per Port the amplitude
    # vectors summed over the numbers.
    scaled = amounts * (MIXING_AMPLITUDE_SCALE * MIXING_AMPLITUDE_SCALE)
    root = integer_root(scaled)
    ax = (root * family.mix_cosines[port_phase]).sum(axis=-2, keepdims=True)
    ay = (root * family.mix_sines[port_phase]).sum(axis=-2, keepdims=True)
    sum_x = ax.sum(axis=-1, keepdims=True)
    sum_y = ay.sum(axis=-1, keepdims=True)
    # The common leaving amplitude of each side: the sum less three times
    # what came in through its Port over all numbers.
    cx = sum_x - 3 * ax[..., OPPOSITE]
    cy = sum_y - 3 * ay[..., OPPOSITE]
    if max(int(np.abs(cx).max(initial=0)), int(np.abs(cy).max(initial=0))) >= 1 << 31:
        raise OverflowError("64-bit intermediate range exceeded")
    return cx * cx + cy * cy, sum_x, sum_y, cx, cy


def diagonal_weights(amounts: np.ndarray) -> np.ndarray:
    """The weights of the sides of a family without a phase circle: the
    diagonal of the coherent expansion, per number 32^2 x (its amount over
    the six Ports + 3 x its amount that came in through the side's own
    Port), in the arrivals' shape. No cross term survives between mutually
    incoherent arrivals, of different Ports or of different numbers, so a
    number's weights are its own and another number's presence adds nothing
    to them (the sides' total is the same as if the weights were common; the
    labels are not). Exact integers, no root."""
    total = amounts.sum(axis=-1, keepdims=True)
    weights: np.ndarray = (MIXING_AMPLITUDE_SCALE * MIXING_AMPLITUDE_SCALE) * (
        total + 3 * amounts[..., OPPOSITE]
    )
    return weights


def mix_arrivals(
    family: MixingArrays, momentum_bound: int = MAX_VALUE
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The Node's computation at every Node: the sides' weights over all the
    arrivals present, whatever their number (the coherent sum for a family
    with a phase circle, its diagonal for one without); then per number the
    units leaving per heading, their phases and the momenta they carry."""
    amounts = family.arr_amt.astype(np.int64)
    phases = family.arr_ph.astype(np.int64)
    shape = amounts.shape
    if amounts.max(initial=0) > MAX_VALUE:
        raise ValueError("value exceeds the disturbance integer bound")
    if family.phased:
        weights, sum_x, sum_y, cx, cy = coherent_weights(family, amounts, phases)
    else:
        weights = diagonal_weights(amounts)
    weight_total = weights.sum(axis=-1)
    bits = np.zeros(weight_total.shape, dtype=np.int64)
    for bit in range(1, 64):
        bits = np.where((weight_total >> (bit - 1)) > 0, bit, bits)
    shift = np.maximum(bits - MIXING_WEIGHT_BITS, 0)
    reduced = weights >> shift[..., None]
    reduced_total = reduced.sum(axis=-1)
    present = reduced_total > 0
    divisor = np.where(present, reduced_total, 1)
    # Each number places its own units by the weights (common to the numbers
    # for a family with a phase circle, its own for one without).
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
    # A number with no whole for any side goes whole to the heading nearest
    # the momentum it carries; on a tie the largest share, then the tick's
    # order.
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
    # The leaving phase of a side is the common leaving amplitude's phase for
    # every number (the common sum's where the side's weight is zero); 0 for
    # a family without a phase circle.
    if not family.phased or family.cosines is None or family.sines is None:
        leaving_phase = np.zeros(shape, dtype=np.int64)
    else:
        sum_phase = family._nearest_step(sum_x[..., 0], sum_y[..., 0])
        side_phase = np.where(weights > 0, family._nearest_step(cx, cy), sum_phase[..., None])
        leaving_phase = np.broadcast_to(side_phase, shape)
    momenta = apportion_carried(carried, whole, order)
    if int(np.abs(momenta).max(initial=0)) > momentum_bound:
        raise ValueError("value exceeds the disturbance integer bound")
    return whole, np.where(whole > 0, leaving_phase, 0), momenta


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

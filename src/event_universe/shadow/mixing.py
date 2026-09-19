"""The Node's mixing: the kernels over one family's arrays (node-mixing-v1).

Highlights 5.4, point 24: at every Node the shadows of one number that arrived
on the six headings are one amplitude each, sqrt(amount) in 32nds at the step
nearest their coherent sum; the leaving amplitude of each heading is the
coherent sum less three times the arrival that came in through its Port; the
total, in ninths, is shared by the squared leaving amplitudes with the
largest-remainder rule, ties to the lower Port; the whole quanta leave, the
ninths below one quantum park at the Node (the remainder rule, point 22) and
leave whole when they reach nine. The momentum the group carries goes with the
shares (`apportion_carried`). The kernels are exact in bounded integers: the
only float is the square root's estimate, corrected to the exact integer root
on both sides before it is used.

The arrays are those of `MixingArrays`, whatever their leading axes; the
engine's layer (`event_universe.shadow.layer`) is one such family with the
axes (x, y, z, number). Moved here from the old engine's dense layer on
2026-09-19, byte-identical in what they do.
"""

from __future__ import annotations

from typing import Protocol

import numpy as np

from event_universe.core.lattice import MAX_VALUE, MIXING_OPPOSITE, PORT_HEADINGS

MIXING_DENOMINATOR = 9
MIXING_AMPLITUDE_SCALE = 32
MIXING_WEIGHT_BITS = 28
# The layers of one Port's departures: the mixing's whole quanta at the Node's
# combined phase and the parked share's release at its own phase.
LAYERS = 2
# The twelve outputs of one group's mixing: the whole quanta per leaving heading
# in Port order, then the ninths per heading, the slots `apportion_carried`
# shares a group's momentum over.
OUTPUTS = 12
# The six unit-axial headings in Port order, as an array, and the opposite of
# each (the travel heading of the arrival that came in through a Port).
HEADINGS = np.array(PORT_HEADINGS, dtype=np.int64)
OPPOSITE = np.array(MIXING_OPPOSITE, dtype=np.int64)
# The Ports ranked against each other for the largest-remainder rule: [k, h] is
# whether Port k comes before Port h on a tie.
EARLIER = np.arange(6)[:, None] < np.arange(6)[None, :]
EARLIER_OUTPUT = np.arange(OUTPUTS)[:, None] < np.arange(OUTPUTS)[None, :]


class MixingArrays(Protocol):
    """The arrays one family's mixing reads and writes, whatever the leading
    axes: `arr_*` the arrivals per Node and group with a travel Port axis of
    six and a layer axis last (the momentum with three components after it),
    `reg*` the parked shares per Node, group and Port, `fly_*` the departures
    in the arrivals' shape. The engine's layer (`event_universe.shadow.layer`)
    is one such family with the axes (x, y, z, number)."""

    arr_amt: np.ndarray
    arr_ph: np.ndarray
    arr_mom: np.ndarray
    reg: np.ndarray
    regph: np.ndarray
    reg_mom: np.ndarray
    fly_amt: np.ndarray
    fly_ph: np.ndarray
    fly_mom: np.ndarray
    total: int
    cosines: np.ndarray | None
    sines: np.ndarray | None
    mix_cosines: np.ndarray
    mix_sines: np.ndarray

    def _nearest_step(self, x: np.ndarray, y: np.ndarray) -> np.ndarray: ...

    def combine(
        self, held: np.ndarray, hph: np.ndarray, share: np.ndarray, sph: np.ndarray
    ) -> np.ndarray: ...


def mix_arrivals(
    family: MixingArrays, momentum_bound: int = MAX_VALUE
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The Node's mixing at every dense Node, per owner and sign (node-mixing-v1;
    Highlights 5.4, point 24), exactly `node_mixing`: the shadows that
    arrived on each heading are one amplitude, sqrt(amount) in 32nds at
    the step nearest their coherent sum; the leaving amplitude of each
    heading is the coherent sum less three times the arrival that came in
    through its Port (3 B_h, the same ratios and phase); the total in
    ninths is shared by the squared leaving amplitudes, reduced by a common
    shift to MIXING_WEIGHT_BITS bits, with the largest-remainder rule,
    ties to the lower Port; the whole quanta are the departures per
    heading, at the phase of the leaving amplitude, and the ninths below
    one quantum join the parked shares, each share's phase combined with
    the parked one's by the coherence rule. A group is one owner, flow and
    sign (return-field-v1): the momentum its shadows carry goes with the
    shares over the twelve outputs of the mixing, the whole quanta per
    heading then the ninths, in proportion to their ninths, exact per axis
    by the largest remainder, ties to the lower slot, as
    `apportion_momentum` does; the parked ninths hold their part. Returns
    the departures, their phases and their momenta per owner, flow, sign
    and heading."""
    amounts = family.arr_amt.astype(np.int64)
    phases = family.arr_ph.astype(np.int64)
    amount = amounts.sum(axis=-1)
    shape = amount.shape
    if amount.max(initial=0) > MAX_VALUE:
        raise ValueError("value exceeds the disturbance integer bound")
    if family.cosines is None or family.sines is None:
        port_phase = np.zeros(shape, dtype=np.int64)
    else:
        x = (amounts * family.cosines[phases]).sum(axis=-1)
        y = (amounts * family.sines[phases]).sum(axis=-1)
        port_phase = family._nearest_step(x, y)
    # The amplitudes, the integer square root of amount x 32^2.
    scaled = amount * (MIXING_AMPLITUDE_SCALE * MIXING_AMPLITUDE_SCALE)
    root = np.floor(np.sqrt(scaled.astype(np.float64))).astype(np.int64)
    root = np.where(root * root > scaled, root - 1, root)
    root = np.where((root + 1) * (root + 1) <= scaled, root + 1, root)
    ax = root * family.mix_cosines[port_phase]
    ay = root * family.mix_sines[port_phase]
    cx = ax.sum(axis=-1, keepdims=True) - 3 * ax[..., OPPOSITE]
    cy = ay.sum(axis=-1, keepdims=True) - 3 * ay[..., OPPOSITE]
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
    units = amount.sum(axis=-1) * MIXING_DENOMINATOR
    product = units[..., None] * reduced
    quotas = product // divisor[..., None]
    remainders = product - quotas * divisor[..., None]
    short = units - quotas.sum(axis=-1)
    # The largest remainders first, ties to the lower Port: a Port gets one
    # more when fewer Ports rank ahead of it than the shortfall.
    ahead = (
        (remainders[..., :, None] > remainders[..., None, :])
        | ((remainders[..., :, None] == remainders[..., None, :]) & EARLIER)
    ).sum(axis=-2)
    quotas = np.where(present[..., None], quotas + (ahead < short[..., None]), 0)
    whole = quotas // MIXING_DENOMINATOR
    share = quotas - whole * MIXING_DENOMINATOR
    if family.cosines is None or family.sines is None:
        leaving_phase = np.zeros(shape, dtype=np.int64)
    else:
        leaving_phase = np.where(weights > 0, family._nearest_step(cx, cy), 0)
    # The ninths below one quantum join the parked shares, with their phases.
    reg, regph = family.reg, family.regph
    held = reg.astype(np.int64)
    held_phase = regph.astype(np.int64)
    has_share = share > 0
    if family.cosines is None:
        new_phase = np.where(has_share, 0, held_phase)
    else:
        combined = family.combine(held, held_phase, share, leaving_phase)
        new_phase = np.where(has_share, np.where(held > 0, combined, leaving_phase), held_phase)
    reg[...] = held + share
    regph[...] = new_phase
    # The momentum the group carries, over the twelve outputs by their ninths.
    carried = family.arr_mom.astype(np.int64).sum(axis=(-3, -2))
    outputs = apportion_carried(carried, whole, share, units)
    parked = family.reg_mom.astype(np.int64) + outputs[..., 6:, :]
    if int(np.abs(parked).max(initial=0)) > momentum_bound:
        raise ValueError("value exceeds the disturbance integer bound")
    family.reg_mom[...] = parked
    return whole, leaving_phase, outputs[..., :6, :]


def apportion_carried(
    carried: np.ndarray, whole: np.ndarray, share: np.ndarray, units: np.ndarray
) -> np.ndarray:
    """A group's momentum shared over the twelve outputs of its mixing in
    proportion to their ninths (the whole quanta per heading times nine, then
    the ninths parked per heading), exact per axis: the floors, then the
    units left to the largest remainders, ties to the lower slot; a negative
    component shared as its magnitude and negated (`apportion_momentum`).
    `units` is the group's total in ninths; a group without content or
    without momentum shares nothing."""
    weights = np.concatenate((whole * MIXING_DENOMINATOR, share), axis=-1)
    divisor = np.where(units > 0, units, 1)[..., None]
    outputs = np.zeros((*whole.shape[:-1], OUTPUTS, 3), dtype=np.int64)
    if not carried.any():
        return outputs
    if int(np.abs(carried).max(initial=0)) * int(weights.max(initial=0)) >= 1 << 62:
        raise OverflowError("64-bit intermediate range exceeded")
    for axis in range(3):
        magnitude = np.abs(carried[..., axis])
        product = magnitude[..., None] * weights
        quotient = product // divisor
        remainder = product - quotient * divisor
        left = magnitude - quotient.sum(axis=-1)
        ahead = (
            (remainder[..., :, None] > remainder[..., None, :])
            | ((remainder[..., :, None] == remainder[..., None, :]) & EARLIER_OUTPUT)
        ).sum(axis=-2)
        quotient = quotient + (ahead < left[..., None])
        outputs[..., axis] = np.where((carried[..., axis] < 0)[..., None], -quotient, quotient)
    return outputs


def release_parked(family: MixingArrays) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Every parked share at S or more leaves whole with its phase and resets
    its phase when it empties (field-remainder-v1), taking the register's
    momentum in proportion to what it releases, toward zero, the whole of it
    when the register empties (`momentum_part`, return-field-v1)."""
    S = family.total
    reg, regph, reg_mom = family.reg, family.regph, family.reg_mom
    held = reg.astype(np.int64)
    whole = held // S
    releasing = whole > 0
    rest = held - whole * S
    released_phase = regph.astype(np.int64)
    momentum = reg_mom.astype(np.int64)
    part = (whole * S)[..., None]
    divisor = np.where(held > 0, held, 1)[..., None]
    scaled = np.abs(momentum) * part // divisor
    taken = np.where(momentum < 0, -scaled, scaled)
    taken = np.where((rest == 0)[..., None], momentum, taken)
    taken = np.where(releasing[..., None], taken, 0)
    reg[...] = np.where(releasing, rest, held)
    regph[...] = np.where(releasing & (rest == 0), 0, released_phase)
    reg_mom[...] = momentum - taken
    return whole, released_phase, taken


def merge_departures(
    departures: np.ndarray,
    released: np.ndarray,
    phase: np.ndarray,
    released_phase: np.ndarray,
    departure_momenta: np.ndarray,
    released_momenta: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """The two layers per owner, flow, sign and Port: the mixing's quanta at
    the leaving amplitude's phase and the parked share's release at its
    phase, one ray carrying both momenta when the phases are equal (the
    departures of one Port merge)."""
    same = (released > 0) & (departures > 0) & (released_phase == phase)
    layer_0 = departures + np.where(same, released, 0)
    layer_1 = np.where(same, 0, released)
    momenta_0 = departure_momenta + np.where(same[..., None], released_momenta, 0)
    momenta_1 = np.where(same[..., None], 0, released_momenta)
    return layer_0, layer_1, released_phase, momenta_0, momenta_1


def place_departures(
    family: MixingArrays,
    layer_0: np.ndarray,
    layer_1: np.ndarray,
    phase: np.ndarray,
    phase_1: np.ndarray,
    momenta_0: np.ndarray,
    momenta_1: np.ndarray,
    momentum_bound: int = MAX_VALUE,
) -> None:
    if max(int(layer_0.max(initial=0)), int(layer_1.max(initial=0))) > MAX_VALUE:
        raise ValueError("value exceeds the disturbance integer bound")
    if (
        max(int(np.abs(momenta_0).max(initial=0)), int(np.abs(momenta_1).max(initial=0)))
        > momentum_bound
    ):
        raise ValueError("value exceeds the disturbance integer bound")
    family.fly_amt[..., 0] = layer_0
    family.fly_ph[..., 0] = np.where(layer_0 > 0, phase, 0)
    family.fly_mom[..., 0, :] = momenta_0
    family.fly_amt[..., 1] = layer_1
    family.fly_ph[..., 1] = np.where(layer_1 > 0, phase_1, 0)
    family.fly_mom[..., 1, :] = momenta_1

"""The dense mode for boards that a field fills (dense-field-v1).

A host scheduling component, not a physical rule: the shadow-only Nodes of a
board, those holding nothing but shadows of families with a shadow set, are
held as integer arrays and cycled by the spatial law's mixing and remainder
rule (`core/spatial_state.py`, `node_mixing` and `spread_content`; [the Node
mixes the six](../../docs/SPATIAL_FIELDS.md#the-node-mixes-the-six-node-mixing-v1)),
with the same integers, as one vectorized step over every such Node at once
(node-mixing-v1, feature 16c, part 2): per owner and sign the shadows that
arrived on each heading are one amplitude (their amount at the phase of their
coherent sum), the six amplitudes mix (a third of the coherent sum to every
Port, less the arrival through it sent back), the total in ninths is shared
among the six headings by the squared leaving amplitudes with the
largest-remainder rule, the whole quanta leave at the phase of their leaving
amplitude and the ninths below one quantum join the Node's parked shares
(`reg`, the parked shadows of node-is-ports-v1 in ninths), each share's phase
combined with the parked one's by the coherence rule (`phase_of_sum` over the
family's integer cosine and sine tables, in the order the engine combines
them), a parked share at one quantum leaving whole with its phase; a Node
holding more shadows than the arrays' layers is cycled by `spread_content`
itself, ray by ray. The departures walk one Link with the family's phase
advance, the open boundary absorbing what walks out, per family, owner and
sign. Since bit-law-v1 (2026-09-18) the region is the
board's shadow layer (point 13 of the law): it holds shadows alone, the bit-0
rays of the spreading families, per owner (the thing whose shadow each is; the
arrays carry an owner axis, the family's declared owners in order), and no
event happens in it: a shadow meets a shadow by the phase sum, a shadow meets
a thing at the thing's Node, the engine's. Since return-field-v1 (feature
16d, part 2) the arrays carry the flow of every share beside its sign: a
returning share (the shadow turned back by a push, its sign flipped, carrying
-dp) lives in the arrays like any share and mixes in its own group (owner,
flow, sign; the outgoing and the returning shares of one owner never mix),
and the momentum a group carries (`arr_mom`, `fly_mom`, `reg_mom`) goes with
its shares over the twelve outputs of the mixing in proportion to their
ninths, exact per axis by the largest remainder, ties to the lower slot,
exactly as `apportion_momentum` does; a parked share holds its part until a
release takes the register's momentum in proportion to what it releases
(`momentum_part`), and a share that walks off an open board takes its
momentum with it, booked on the escaped lines. The parked block of a Node is
the engine's (thirty-six per owner, `remainder_slot`), so the region and the
engine exchange it as it is. The step counter of a return, the trace and the
waiting shadow are retired with the rule (no `ret_*`, `wait_*` or `trace`
arrays).

The region and the engine share the board. A Node is the engine's (sparse)
while it holds a Detector mark, an external body, a record, a thing or any
other content the vectorized step does not describe; every other Node is the
region's (dense). Ownership is decided at every delivery for the Nodes that
receive something: a ray leaving a dense Node toward a sparse Node is handed
over as an ordinary `SpatialPacket` of merged rays, and a packet leaving a
sparse Node into the dense region is absorbed into the arrays, both exact, the
parked shares moving with the Node, with their momentum, when its ownership
changes. The region publishes no per-Node events: the record of a
dense region is its arrays' totals per tick (the world ledger), and the mode
is not for records that need per-Node field events. Its Nodes read back as
Node state for the totals, the snapshot and the inventory view
(`materialized_nodes`), so `state.json` and the ledger are the acceptance test
of the mode (docs/PERFORMANCE.md).

The standing set by a formula (standing-field-v1; Highlights 5.4, points 11
and 13: the field of things at rest is a standing set, computed once). With
`standing_field` declared, the region compares its state after every
delivery with the one before it, the layer's step function being an opaque
operator here (whatever spread rule it applies): the arrays, the whole rays
beside them, the owners, the engine's Nodes' resident rays and the packets
the engine delivers this interval. When a state equals an earlier one (the
previous state: a fixed point; one of the last `STANDING_WINDOW` states: a
cycle of that period) the layer has reached the standing set of that
operator, the states the stepping engine would keep reaching, and from then
on the region is kept fixed: its cycle is skipped, its delivery hands the
engine's Nodes the packets of the corresponding interval of the cycle, books
its escapes and takes the engine's packets into the fixed arrays, exactly the
flows the stepping engine computed for that interval. Every interval the
engine's part of the state is checked against the cycle's; a thing that
steps, a body's packet into the layer or a mark absorbing a thing changes it,
and the region falls back to stepping from the fixed arrays, at that delivery
(the cycle it skipped is run late, on the same arrays the engine's cycle left
untouched) and says so in its record. Without a repeat within the declared
intervals the layer keeps stepping and the record carries the residual of
the last comparison with the previous state. The ledger balances under the
fixed layer because its flows are those of intervals the stepping engine
computed.

Bounded integers throughout: amounts are below MAX_VALUE, phases below the
family's modulus, products and sums in signed 64-bit intermediates as the
engine's `checked_work` requires; the arrays hold amounts as int32 (MAX_VALUE
is 2^30 - 1), phases as int16 (the modulus is at most 4096) and the owner
flags as int8, the sums and products promoted to int64 where a value could
grow, and the bounds are checked there.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Protocol

import numpy as np

from event_universe.core.disturbance_state import MAX_VALUE, Address3, InitialState, pack, unpack
from event_universe.core.node_ports import PortBank
from event_universe.core.spatial_engine import SpatialEngine
from event_universe.core.spatial_node import SpatialNode
from event_universe.core.spatial_state import (
    BIT_SHADOW,
    MIXING_AMPLITUDE_SCALE,
    MIXING_DENOMINATOR,
    MIXING_OPPOSITE,
    MIXING_WEIGHT_BITS,
    PARKED_SLOTS,
    POLARIZATION_NONE,
    PORT_HEADINGS,
    RAY_VIEW_COMPONENTS_UNPOLARIZED,
    REMAINDER_SLOTS,
    Ray,
    Rays,
    SpatialFieldDefinition,
    SpatialPacket,
    merge_rays,
    mixing_tables,
    park_shares,
    parked_shares,
    parked_unit,
    phase_mask,
    ray_layers,
    spread_content,
    spread_tables,
    validate_ray_participants,
)
from event_universe.core.topology import neighbor_address

if TYPE_CHECKING:
    from event_universe.core.disturbance_node import DisturbanceNode

# The layers of one Port's content from a dense Node: the spread's whole quanta at
# the Node's combined phase and the parked share's release at its own phase; a
# sparse Node's packet may carry more phases on one Port and sign, and those
# rays are kept whole beside the arrays (`overflow`).
LAYERS = 2
SIGNS = 3
# The flow of a share (return-field-v1): 0 outgoing, 1 returning.
FLOWS = 2
# The twelve outputs of one group's mixing: the whole quanta per leaving heading
# in Port order, then the ninths per heading, the slots `apportion_momentum`
# shares a group's momentum over.
OUTPUTS = 12
# The array dtypes (node-is-ports-v1, the performance review): amounts and
# momentum components below MAX_VALUE = 2^30 - 1 in magnitude, phases below 4096.
AMOUNT = np.int32
PHASE = np.int16
# The six unit-axial headings in Port order, as an array, and the opposite of
# each (the travel heading of the arrival that came in through a Port).
HEADINGS = np.array(PORT_HEADINGS, dtype=np.int64)
OPPOSITE = np.array(MIXING_OPPOSITE, dtype=np.int64)
# The Ports ranked against each other for the largest-remainder rule: [k, h] is
# whether Port k comes before Port h on a tie.
EARLIER = np.arange(6)[:, None] < np.arange(6)[None, :]
EARLIER_OUTPUT = np.arange(OUTPUTS)[:, None] < np.arange(OUTPUTS)[None, :]
# The arrays of a family the layer's step reads and writes (standing-field-v1),
# and those among them that hold amounts (the residual's quanta).
_ARRAYS = ("arr_amt", "arr_ph", "arr_mom", "reg", "regph", "reg_mom", "fly_amt", "fly_ph", "fly_mom")
_AMOUNTS = ("arr_amt", "reg", "fly_amt")
# The engine's part of the layer's state: its Nodes' resident rays and the
# packets it delivers this interval, by value.
_Signature = tuple[
    tuple[tuple[Address3, tuple[Rays, ...]], ...],
    tuple[tuple[Address3, Address3, int, tuple[Rays, ...], bool], ...],
]


@dataclass(frozen=True)
class _LayerState:
    """One delivery's state of the layer, copied for the comparison."""

    arrays: list[np.ndarray]
    overflow: list[tuple[tuple[Address3, tuple[Ray, ...]], ...]]
    signature: _Signature


@dataclass(frozen=True)
class _Interval:
    """One stepped delivery's record while looking for the standing set: the
    digest of the layer's state after it, the engine's part of the state at its
    start, the packets it handed to the engine's Nodes (target, origin, Port,
    rays) and the escapes it booked per field and component on the escaped line
    and the shadows' own."""

    digest: bytes
    signature: _Signature
    handed: tuple[tuple[Address3, Address3, int, tuple[Rays, ...]], ...]
    escaped: tuple[list[list[int]], list[list[int]]]


@dataclass(frozen=True)
class _StandingSet:
    """The standing set's flows, replayed interval by interval while the layer
    is kept fixed: the intervals of one period of the cycle, in order."""

    cycle: tuple[_Interval, ...]


# The states kept to find a cycle of the layer: a repeat of the previous state
# is a fixed point, of an earlier one within the window a cycle of that period.
STANDING_WINDOW = 1024


class DenseFamily:
    """The arrays of one spreading family on the board.

    `arr_*` hold the shadows resident at each Node, arrived this interval and due
    to spread: per owner (the family's declared owners in order), flow (0 the
    outgoing shares, 1 the returning, return-field-v1), source sign (-1, 0, 1 as
    0, 1, 2), travel Port (the heading the content arrived on, the engine's
    `arrived` index) and layer, the amount, the phase and the momentum carried
    (`arr_mom`, three per cell). `reg`, `regph` and `reg_mom` are the thirty-six
    parked shares per Node and owner, flow-major then sign then Port, the
    engine's parked block cell for cell (`remainder_slot`), in units of 1/S,
    with their phases and the momentum they hold. `fly_*` hold the departures of
    the last cycle, with their momentum, until the delivery walks them one Link."""

    def __init__(
        self, index: int, definition: SpatialFieldDefinition, shape: Address3, prices: dict[str, int]
    ) -> None:
        self.index = index
        self.definition = definition
        self.field = definition.field
        self.owners: tuple[int, ...] = definition.owners or (0,)
        self.rank = {owner: rank for rank, owner in enumerate(self.owners)}
        count = len(self.owners)
        # The parked shares' unit: ninths (node-mixing-v1).
        self.total = parked_unit(definition)
        self.modulus = definition.phase_modulus
        # The tables the mixing sums amplitudes over: the family's, or the
        # one-step circle of a family without a phase width (`mixing_tables`).
        mixing = mixing_tables(definition)
        self.mix_cosines = np.array(mixing[0], dtype=np.int64)
        self.mix_sines = np.array(mixing[1], dtype=np.int64)
        self.mask = phase_mask(self.modulus)
        # A shadow has no clock (clock-readings-v1): the region's phases never advance.
        self.advance = 0
        tables = spread_tables(definition)
        if tables is None:
            self.cosines = self.sines = None
        else:
            self.cosines = np.array(tables[0], dtype=np.int64)
            self.sines = np.array(tables[1], dtype=np.int64)
        self.heading_index = np.array(
            [definition.headings.index(heading) for heading in PORT_HEADINGS], dtype=np.int64
        )
        # The travel Port of a ray by its heading index.
        self.port_of = {int(index): port for port, index in enumerate(self.heading_index)}
        cells = (*shape, count, FLOWS, SIGNS, 6)
        self.arr_amt = np.zeros((*cells, LAYERS), dtype=AMOUNT)
        self.arr_ph = np.zeros((*cells, LAYERS), dtype=PHASE)
        self.arr_mom = np.zeros((*cells, LAYERS, 3), dtype=AMOUNT)
        self.overflow: dict[Address3, list[Ray]] = {}
        self.reg = np.zeros(cells, dtype=AMOUNT)
        self.regph = np.zeros(cells, dtype=PHASE)
        self.reg_mom = np.zeros((*cells, 3), dtype=AMOUNT)
        self.fly_amt = np.zeros((*cells, LAYERS), dtype=AMOUNT)
        self.fly_ph = np.zeros((*cells, LAYERS), dtype=PHASE)
        self.fly_mom = np.zeros((*cells, LAYERS, 3), dtype=AMOUNT)
        self.prices = prices
        # The meeting's reading of every ray at a Node (`_meet`, ray-layers-v1):
        # the view components per ray, charged by the engine at every Node of a
        # layer a declared rule selects, shadows alone included; 0 for a family
        # no rule's layer reaches (set by the region from the world's rules).
        self.meeting_reads = 0

    def block(self, position: Address3) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
        """The Node's parked block as the spread step reads it (thirty-six slots
        per owner in `remainder_slot` order): the amounts, their phases and
        their momenta, three per slot."""
        return (
            tuple(int(v) for v in self.reg[position].reshape(-1)),
            tuple(int(v) for v in self.regph[position].reshape(-1)),
            tuple(int(v) for v in self.reg_mom[position].reshape(-1)),
        )

    def set_block(
        self,
        position: Address3,
        block: tuple[int, ...],
        phases: tuple[int, ...],
        momenta: tuple[int, ...],
    ) -> None:
        """The Node's parked block from the spread step's, cell for cell."""
        owners = len(self.owners)
        size = PARKED_SLOTS * owners
        if len(block) != size or len(phases) != size or len(momenta) != 3 * size:
            raise ValueError(
                "a remainder block holds thirty-six registers, phases and momenta per owner"
            )
        self.reg[position] = np.array(block, dtype=np.int64).reshape(owners, FLOWS, SIGNS, 6)
        self.regph[position] = np.array(phases, dtype=np.int64).reshape(owners, FLOWS, SIGNS, 6)
        self.reg_mom[position] = np.array(momenta, dtype=np.int64).reshape(owners, FLOWS, SIGNS, 6, 3)

    def ray(
        self,
        rank: int,
        flow: int,
        sign: int,
        port: int,
        amount: int,
        phase: int,
        momentum: np.ndarray,
    ) -> Ray:
        """One cell of the arrays as a shadow on its way, one Link walked: on the
        Port's heading, outgoing or returning, with its phase, its sign, its
        owner and the momentum it carries."""
        carried = (int(momentum[0]), int(momentum[1]), int(momentum[2]))
        return Ray(
            int(self.heading_index[port]),
            (0, 0, 0),
            int(amount),
            phase=int(phase),
            steps=1,
            outbound=0 if flow else 1,
            detector=BIT_SHADOW,
            source_sign=int(sign) - 1,
            momentum=carried if any(carried) else None,
            owner=self.owners[int(rank)],
        )

    def place(self, position: Address3, ray: Ray, port: int) -> bool:
        """One arrived shadow into the arrays at a Node, on its travel Port, in the
        first free layer of its cell (owner, flow, sign, Port), with its momentum;
        False when both layers are taken, the ray then kept whole beside them."""
        cell = (self.rank[ray.owner], 0 if ray.outbound else 1, ray.source_sign + 1, port)
        layers = self.arr_amt[position][cell]
        for layer in range(LAYERS):
            if layers[layer] == 0:
                self.arr_amt[position][(*cell, layer)] = ray.amount
                self.arr_ph[position][(*cell, layer)] = ray.phase
                self.arr_mom[position][(*cell, layer)] = np.array(
                    ray.momentum or (0, 0, 0), dtype=np.int64
                )
                return True
        return False

    def phase_of_pair(
        self, amount: np.ndarray, phase: np.ndarray, other_amount: np.ndarray, other_phase: np.ndarray
    ) -> np.ndarray:
        """The phase of the coherent sum of two contents, elementwise, as the
        engine's `phase_of_sum` gives it (the phase of a shadow-shadow sum, point
        5 of the law); 0 for a family without a phase width."""
        if self.cosines is None or self.sines is None:
            return np.zeros(np.broadcast(amount, other_amount).shape, dtype=np.int64)
        a, b = amount.astype(np.int64), other_amount.astype(np.int64)
        x = a * self.cosines[phase.astype(np.int64)] + b * self.cosines[other_phase.astype(np.int64)]
        y = a * self.sines[phase.astype(np.int64)] + b * self.sines[other_phase.astype(np.int64)]
        return self._nearest_step(x, y)

    def _nearest_step(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """The phase step whose projection x cos + y sin is greatest, the first on
        a tie (the engine's `_phase_of_sum`); step 0 for a cancelled sum."""
        assert self.cosines is not None and self.sines is not None
        projection = x[..., None] * self.cosines + y[..., None] * self.sines
        return np.argmax(projection, axis=-1).astype(np.int64)

    def combine(
        self, held: np.ndarray, hph: np.ndarray, share: np.ndarray, sph: np.ndarray
    ) -> np.ndarray:
        """The parked share's phase after a share joins it, elementwise: the step
        nearest held e^(i held phase) + share e^(i share phase), exactly
        `_phase_of_sum` in the engine's order."""
        assert self.cosines is not None and self.sines is not None
        x = held * self.cosines[hph] + share * self.cosines[sph]
        y = held * self.sines[hph] + share * self.sines[sph]
        return self._nearest_step(x, y)


def plain_ray(ray: Ray, definition: SpatialFieldDefinition, family: DenseFamily | None = None) -> bool:
    """Whether a ray is content the dense region describes: a shadow of one of the
    family's owners on a Port heading without an event, a delay, a wait, a lag,
    an own advance or a polarization (bit-law-v1: a thing is never the
    region's), outgoing or returning with the momentum it carries
    (return-field-v1), either one Link from its departure or parked."""
    if (
        ray.detector != BIT_SHADOW
        or (family is not None and ray.owner not in family.rank)
        or ray.event_ports
        or any(ray.event_shares)
        or ray.advance != -1
        or ray.wait
        or ray.interaction_delay
        or ray.polarization != POLARIZATION_NONE
        or ray.accumulators != (0, 0, 0)
        or ray.owed
        or definition.headings[ray.heading] not in PORT_HEADINGS
    ):
        return False
    if ray.parked:
        return True
    return ray.steps == 1 and ray.amount > 0


def plain_node(node: SpatialNode, families: Mapping[int, DenseFamily] | None = None) -> bool:
    """Whether an engine Node holds nothing the region cannot own: no mark, no
    body, no pending cycle, no octant stock, no deposit, and no resident ray
    but the shadows the region describes (parked, or on their way, outgoing or
    returning)."""
    if (
        node.detector is not None
        or node.body is not None
        or node.pending is not None
        or node.shared_pending
        or node.incoming
        or any(any(unpack(payload)) for state in node.states for payload in state.populations)
        or any(any(unpack(payload)) for payload in node.localized)
    ):
        return False
    for index, rays in enumerate(node.rays):
        if not rays:
            continue
        family = None if families is None else families.get(index)
        if family is None or any(not plain_ray(ray, family.definition, family) for ray in rays):
            return False
    return True


class MixingArrays(Protocol):
    """The arrays one family's mixing reads and writes (node-mixing-v1, the
    remainder rule and the momentum carried, return-field-v1), whatever the
    leading axes: `arr_*` the arrivals per Node and group with a travel Port
    axis of six and a layer axis last (the momentum with three components after
    it), `reg*` the parked shares per Node, group and Port, `fly_*` the
    departures in the arrivals' shape. `DenseFamily` is one such family with
    the axes (x, y, z, owner, flow, sign); the shadow layer of the law of the
    shadow (`event_universe/shadow`) another with (x, y, z, number). The kernels
    below (`mix_arrivals`, `apportion_carried`, `release_parked`,
    `merge_departures`, `place_departures`) are the class's methods moved to
    module level on 2026-09-18 for that reuse, byte-identical in what they do."""

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


class DenseField:
    """The dense region of one board (dense-field-v1); see the module docstring."""

    def __init__(self, initial: InitialState, engine: SpatialEngine) -> None:
        self.initial = initial
        self.engine = engine
        self.shape: Address3 = initial.shape
        self.open = initial.boundary == "open"
        prices = {
            name: initial.operation_costs.price(name)
            for name in ("receive", "read", "evaluate", "update", "route", "split", "send", "commit")
        }
        self.prices = prices
        self.families: dict[int, DenseFamily] = {
            index: DenseFamily(index, definition, self.shape, prices)
            for index, definition in enumerate(initial.spatial_fields)
            if definition.spread
        }
        if initial.ray_interactions:
            selected = validate_ray_participants(
                initial.spatial_fields, initial.fields, initial.ray_interactions
            )
            for layer in ray_layers(initial.spatial_fields, initial.ray_interactions):
                if not selected.intersection(layer):
                    continue
                for index in layer:
                    if index in self.families:
                        self.families[index].meeting_reads = RAY_VIEW_COMPONENTS_UNPOLARIZED
        self.blank_bundle = tuple(
            (pack((0,) * initial.fields[definition.field].components),) * 8
            for definition in initial.spatial_fields
        )
        self.field_count = len(initial.spatial_fields)
        self.components = sum(initial.fields[d.field].components for d in initial.spatial_fields)
        # 0: the region's Node; 1: the engine's. The engine's from the start: every
        # marked Node, every body's Node, every seeded Node.
        self.owner = np.zeros(self.shape, dtype=np.int8)
        self.visited = np.zeros(self.shape, dtype=bool)
        self.cost = np.zeros(self.shape, dtype=np.int64)
        self.engine_positions: set[Address3] = set()
        self.marks = {mark.position for mark in initial.detectors}
        for position in (
            self.marks
            | {body.position for body in initial.external_bodies}
            | {seed.position for seed in initial.seeds}
            | {seed.position for seed in initial.spatial_seeds}
            | set(engine.nodes)
        ):
            self.owner[position] = 1
            self.engine_positions.add(position)
        self._active = 0
        # The Nodes the shadow's wait binds to the engine this delivery
        # (shadow-wait-v1, the field reading): see `_field_wait_nodes`.
        self._wait_bound: set[Address3] = set()
        # The standing set (standing-field-v1): the intervals left to look for
        # the fixed point (0: not looking), the state of the previous delivery
        # to compare with, the fixed point's flows once found, and the record.
        self._standing_limit = initial.standing_field
        self._previous: _LayerState | None = None
        self._intervals: list[_Interval] = []
        self.standing: _StandingSet | None = None
        self._standing_phase = 0
        self._standing_record: dict[str, object] | None = None
        if self._standing_limit:
            self._standing_record = {
                "standing_field": False,
                "standing_field_iterations": None,
                "standing_field_period": None,
                "standing_field_residual": None,
                "standing_field_ticks": 0,
                "standing_field_fallback": None,
            }

    # -- the standing set (standing-field-v1) ----------------------------------

    def standing_report(self) -> dict[str, object] | None:
        """The standing set's record: None for a world without the mode."""
        return None if self._standing_record is None else dict(self._standing_record)

    def _layer_state(self, signature: _Signature) -> _LayerState:
        """The state the layer's step reads and writes, copied: the arrays and the
        whole rays beside them per family, the owners, and the engine's part (its
        Nodes' resident rays and the packets it delivered this interval)."""
        arrays: list[np.ndarray] = []
        overflow: list[tuple[tuple[Address3, tuple[Ray, ...]], ...]] = []
        for family in self.families.values():
            arrays.extend(getattr(family, name).copy() for name in _ARRAYS)
            overflow.append(tuple((k, tuple(v)) for k, v in sorted(family.overflow.items())))
        arrays.append(self.owner.copy())
        return _LayerState(arrays, overflow, signature)

    def _engine_signature(self, ready: Mapping[Address3, list[SpatialPacket]]) -> _Signature:
        nodes = tuple(
            (position, node.rays)
            for position, node in sorted(self.engine.nodes.items())
            if any(node.rays)
        )
        packets = tuple(
            (target, packet.origin, packet.port, packet.rays, packet.body is not None)
            for target in sorted(ready)
            for packet in ready[target]
        )
        return nodes, packets

    def _digest(self, signature: _Signature) -> bytes:
        """The digest of the layer's state after a delivery, over the arrays
        without a copy, the whole rays beside them and the engine's part."""
        digest = hashlib.blake2b(digest_size=32)
        for family in self.families.values():
            for name in _ARRAYS:
                digest.update(np.ascontiguousarray(getattr(family, name)))
            digest.update(repr(sorted(family.overflow.items())).encode())
        digest.update(np.ascontiguousarray(self.owner))
        digest.update(repr(signature).encode())
        return digest.digest()

    @staticmethod
    def _residual(before: _LayerState, after: _LayerState) -> dict[str, int]:
        """How far two consecutive states are apart: the array cells that differ
        (a momentum, three integers, one cell) and the sum of the absolute
        differences of the amounts (the parked shares in their own units), plus
        the whole rays and the engine's part when they differ."""
        cells = 0
        amount = 0
        last = len(before.arrays) - 1
        for index, (a, b) in enumerate(zip(before.arrays, after.arrays, strict=True)):
            differing = a != b
            name = _ARRAYS[index % len(_ARRAYS)] if index < last else ""
            if name.endswith("_mom"):
                differing = differing.any(axis=-1)
            cells += int(differing.sum())
            if name in _AMOUNTS:
                amount += int(np.abs(a.astype(np.int64) - b.astype(np.int64)).sum())
        other = int(before.overflow != after.overflow) + int(before.signature != after.signature)
        return {"cells": cells + other, "amount": amount}

    def _settle(
        self,
        tick: int,
        ready: Mapping[Address3, list[SpatialPacket]],
        signature: _Signature,
        handed: Mapping[Address3, list[SpatialPacket]],
        escaped: tuple[list[list[int]], list[list[int]]],
    ) -> None:
        """After a stepped delivery while looking for the standing set: compare
        with the previous delivery's state (the residual) and with the states of
        the window (a repeat, of the previous state or of an earlier one, is the
        standing set: a fixed point or a cycle of that period); at a repeat
        freeze the layer with the cycle's flows, at the limit give up."""
        record = self._standing_record
        assert record is not None
        current = self._layer_state(signature)
        previous, self._previous = self._previous, None
        if previous is not None:
            record["standing_field_residual"] = self._residual(previous, current)
        interval = _Interval(
            self._digest(signature),
            signature,
            tuple(
                (target, packet.origin, packet.port, packet.rays)
                for target in sorted(handed)
                for packet in handed[target]
            ),
            escaped,
        )
        for index in range(len(self._intervals) - 1, -1, -1):
            if self._intervals[index].digest == interval.digest:
                cycle = (*self._intervals[index + 1 :], interval)
                record["standing_field"] = True
                record["standing_field_iterations"] = tick
                record["standing_field_period"] = len(cycle)
                self._standing_limit = 0
                self._intervals = []
                self.standing = _StandingSet(cycle)
                self._standing_phase = 0
                return
        if tick >= self._standing_limit:
            self._standing_limit = 0
            self._intervals = []
            return
        self._previous = current
        self._intervals.append(interval)
        del self._intervals[:-STANDING_WINDOW]

    def _escape_counters(self) -> tuple[list[list[int]], list[list[int]]]:
        return (
            [list(line) for line in self.engine.escaped],
            [list(line) for line in self.engine.shadow_escaped],
        )

    def _deliver_standing(
        self, tick: int, ready: dict[Address3, list[SpatialPacket]]
    ) -> tuple[dict[Address3, list[SpatialPacket]], list[SpatialPacket]]:
        """The delivery under the fixed layer: the flows of the corresponding
        interval of the cycle, the arrays untouched."""
        standing = self.standing
        assert standing is not None and self._standing_record is not None
        interval = standing.cycle[self._standing_phase]
        self._standing_phase = (self._standing_phase + 1) % len(standing.cycle)
        absorbed: list[SpatialPacket] = []
        for target in list(ready):
            if not self.owner[target]:
                absorbed.extend(ready.pop(target))
        for counters, deltas in zip(
            (self.engine.escaped, self.engine.shadow_escaped), interval.escaped, strict=True
        ):
            for line, gone in zip(counters, deltas, strict=True):
                for component, value in enumerate(gone):
                    if value:
                        line[component] += value
        for target, origin, port, rays in interval.handed:
            ready.setdefault(target, []).append(
                SpatialPacket(tick, origin, port, self.blank_bundle, rays=rays)
            )
        ticks = self._standing_record["standing_field_ticks"]
        assert isinstance(ticks, int)
        self._standing_record["standing_field_ticks"] = ticks + 1
        return ready, absorbed

    def _fall_back(self, tick: int, reason: str) -> None:
        """A thing stepped or the things' Nodes changed: the layer steps again from
        the fixed arrays, and the record says so."""
        assert self._standing_record is not None
        self.standing = None
        self._standing_record["standing_field"] = False
        self._standing_record["standing_field_fallback"] = {"tick": tick, "reason": reason}

    # -- the cycle -------------------------------------------------------------

    def active_count(self) -> int:
        """The dense Nodes the last cycle cycled: those with arrivals or registers."""
        return self._active

    def cycle(self, tick: int) -> None:
        """The spread of every dense Node with content, at once (node-mixing-v1,
        field-remainder-v1): the same integers as `spread_content` at each, the
        departures kept in flight until the delivery and the cost of each cycle
        as the spatial law would meter it. A Node holding more shadows than the
        arrays' layers is cycled by `spread_content` itself, ray by ray."""
        if self.standing is not None:
            return
        dense = self.owner == 0
        prices = self.prices
        ports_any = np.zeros((*self.shape, 6), dtype=bool)
        has_registers = np.zeros(self.shape, dtype=bool)
        family_cost = np.zeros(self.shape, dtype=np.int64)
        has_arrivals = np.zeros(self.shape, dtype=bool)
        for family in self.families.values():
            fallback = self._fallback(family)
            count, family_ports = self._arrivals(family)
            for position, (rays, ports, _) in fallback.items():
                count[position] += len(rays)
                family_ports[position] |= ports
            ports_any |= family_ports
            # A Node holding a parked share stays active, as the engine's does
            # (node-is-ports-v1).
            has_registers |= (family.reg > 0).any(axis=(3, 4, 5, 6))
            present = count > 0
            has_arrivals |= present
            if not present.any():
                continue
            departures, phase, departure_momenta = self._mix(family)
            released, released_phase, released_momenta = self._release(family)
            layer_0, layer_1, phase_1, momenta_0, momenta_1 = self._departures(
                departures, released, phase, released_phase, departure_momenta, released_momenta
            )
            self._place_departures(family, layer_0, layer_1, phase, phase_1, momenta_0, momenta_1)
            for position, (_, _, departed) in fallback.items():
                self._place_rays(family, position, departed)
            outgoing = family.fly_amt > 0
            departing = outgoing.sum(axis=(3, 4, 5, 6, 7)).astype(np.int64)
            sending = outgoing.any(axis=(3, 4, 5, 7)).sum(axis=3)
            cost = np.zeros(self.shape, dtype=np.int64)
            # The meeting reads every ray's view before anything else (`_meet`).
            cost += prices["read"] * family.meeting_reads * count
            if family.definition.coherent:
                cost += prices["evaluate"] * count
            spread_cost = prices["read"] * (count + REMAINDER_SLOTS) + prices["split"] * departing
            spread_cost += prices["update"] * REMAINDER_SLOTS
            if family.definition.coherent:
                spread_cost += prices["evaluate"] * (count + family.definition.phase_steps)
            cost += np.where(present, spread_cost, 0)
            cost += (prices["read"] + prices["route"]) * departing + prices["send"] * sending
            family_cost += cost
            family.arr_amt[...] = 0
            family.arr_ph[...] = 0
            family.arr_mom[...] = 0
        active = dense & (has_arrivals | has_registers)
        received = ports_any.sum(axis=3).astype(np.int64)
        node_cost = (
            prices["receive"] * received
            + prices["read"] * received * 8 * self.field_count
            + prices["update"] * received * 16 * self.components
            + family_cost
            + prices["commit"]
        )
        if node_cost.max(initial=0) > MAX_VALUE:
            raise ValueError("value exceeds the disturbance integer bound")
        self.cost = np.where(active, node_cost, 0)
        self._active = int(active.sum())

    def _fallback(self, family: DenseFamily) -> dict[Address3, tuple[list[Ray], np.ndarray, Rays]]:
        """The Nodes holding more shadows than the arrays' layers (the overflow):
        every share there, the arrays' and the whole rays beside them, is cycled
        by `spread_content` with the Node's registers, the arrays cleared at the
        Node; the departures are placed once the vectorized step has placed its
        own. Per Node: the rays taken, the Ports with content, the departures."""
        result: dict[Address3, tuple[list[Ray], np.ndarray, Rays]] = {}
        for position, extra in sorted(family.overflow.items()):
            rays = list(extra)
            amounts, phases = family.arr_amt[position], family.arr_ph[position]
            momenta = family.arr_mom[position]
            for rank, flow, sign, port, layer in zip(*np.nonzero(amounts > 0), strict=True):
                cell = (rank, flow, sign, port, layer)
                rays.append(
                    family.ray(rank, flow, sign, port, amounts[cell], phases[cell], momenta[cell])
                )
            held, held_phases, held_momenta = family.block(position)
            departed, _, after, after_phases, after_momenta = spread_content(
                family.index, tuple(rays), family.definition, held, held_phases, held_momenta
            )
            family.set_block(position, after, after_phases, after_momenta)
            ports = np.zeros(6, dtype=bool)
            for ray in rays:
                ports[family.port_of[ray.heading]] = True
            amounts[...] = 0
            phases[...] = 0
            momenta[...] = 0
            result[position] = (rays, ports, departed)
        family.overflow.clear()
        return result

    def _place_rays(self, family: DenseFamily, position: Address3, departed: Rays) -> None:
        """The departures of one Node cycled ray by ray, into the flight arrays."""
        amounts, phases = family.fly_amt[position], family.fly_ph[position]
        momenta = family.fly_mom[position]
        amounts[...] = 0
        phases[...] = 0
        momenta[...] = 0
        for ray in departed:
            cell = (
                family.rank[ray.owner],
                0 if ray.outbound else 1,
                ray.source_sign + 1,
                family.port_of[ray.heading],
            )
            layers = amounts[cell]
            free = [layer for layer in range(LAYERS) if layers[layer] == 0]
            if not free:
                raise ValueError("ray slot budget exceeded")
            amounts[(*cell, free[0])] = ray.amount
            phases[(*cell, free[0])] = ray.phase
            momenta[(*cell, free[0])] = np.array(ray.momentum or (0, 0, 0), dtype=np.int64)

    def _arrivals(self, family: DenseFamily) -> tuple[np.ndarray, np.ndarray]:
        """What arrived at every Node this interval: the number of shadows and the
        Ports with content."""
        present = family.arr_amt > 0
        if family.arr_amt.max(initial=0) > MAX_VALUE:
            raise ValueError("value exceeds the disturbance integer bound")
        count = present.sum(axis=(3, 4, 5, 6, 7)).astype(np.int64)
        ports = present.any(axis=(3, 4, 5, 7))
        return count, ports

    def _mix(self, family: DenseFamily) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """The Node's mixing at every dense Node, per owner, flow and sign: the
        module-level `mix_arrivals` over the family's arrays."""
        return mix_arrivals(family)

    _apportion = staticmethod(apportion_carried)
    _release = staticmethod(release_parked)
    _departures = staticmethod(merge_departures)
    _place_departures = staticmethod(place_departures)

    # -- the delivery ----------------------------------------------------------

    def deliver(
        self,
        tick: int,
        ready: dict[Address3, list[SpatialPacket]],
        residents: Mapping[Address3, DisturbanceNode] | None,
    ) -> tuple[dict[Address3, list[SpatialPacket]], list[SpatialPacket]]:
        """Walk the region's departures one Link, count the escapes, decide the owner
        of every Node that receives something, absorb the engine's packets to dense
        Nodes and hand the engine the packets of dense Nodes to its own. Returns the
        packets left for the engine to deliver and the packets absorbed. Under the
        standing set (standing-field-v1) the fixed point's flows are replayed
        instead, unless the engine's part of the state changed, when the layer
        steps again from this interval on."""
        if self.standing is not None:
            carried = residents is not None and any(
                not self.owner[position] and any(record is not None for record in carrier.records)
                for position, carrier in residents.items()
            )
            expected = self.standing.cycle[self._standing_phase].signature
            if not carried and self._engine_signature(ready) == expected:
                return self._deliver_standing(tick, ready)
            self._fall_back(tick, "a thing stepped or the things' Nodes changed")
            self.cycle(tick)
        looking = self._standing_limit > 0
        signature: _Signature = self._engine_signature(ready) if looking else ((), ())
        counters = self._escape_counters() if looking else ([], [])
        ready, absorbed, handed = self._deliver_stepping(tick, ready, residents)
        if looking:
            after = self._escape_counters()
            escaped = tuple(
                [
                    [now - then for now, then in zip(line, before, strict=True)]
                    for line, before in zip(lines, past, strict=True)
                ]
                for lines, past in zip(after, counters, strict=True)
            )
            self._settle(tick, ready, signature, handed, (escaped[0], escaped[1]))
        return ready, absorbed

    def _deliver_stepping(
        self,
        tick: int,
        ready: dict[Address3, list[SpatialPacket]],
        residents: Mapping[Address3, DisturbanceNode] | None,
    ) -> tuple[
        dict[Address3, list[SpatialPacket]], list[SpatialPacket], dict[Address3, list[SpatialPacket]]
    ]:
        """The delivery of a stepped interval; returns also the packets handed to
        the engine's Nodes, the standing set's flows when the layer repeats."""
        incoming = {index: self._walk(family) for index, family in self.families.items()}
        self._wait_bound = self._field_wait_nodes(incoming, ready)
        candidates = set(ready) | self._engine_receivers(incoming) | self._wait_bound
        if residents is not None:
            for position, carrier in residents.items():
                if any(record is not None for record in carrier.records) and (
                    position in ready or self._receives(incoming, position)
                ):
                    candidates.add(position)
        for target in sorted(candidates):
            bound = self._engine_bound(target, ready.get(target, ()), residents)
            if bound and not self.owner[target]:
                self._to_engine(target)
            elif not bound and self.owner[target]:
                self._to_dense(target)
        handed = self._hand_over(tick, incoming)
        absorbed: list[SpatialPacket] = []
        for target in list(ready):
            if not self.owner[target]:
                for packet in ready.pop(target):
                    self._absorb(target, packet)
                    absorbed.append(packet)
        for index, family in self.families.items():
            amounts, phases, momenta = incoming[index]
            family.arr_amt += amounts
            family.arr_ph += phases
            family.arr_mom += momenta
            present = (family.arr_amt > 0).any(axis=(3, 4, 5, 6, 7))
            self.visited |= present
        for target, packets in handed.items():
            ready.setdefault(target, []).extend(packets)
        return ready, absorbed, handed

    def _walk(self, family: DenseFamily) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """The departures one Link on: what arrives at each Node per owner, flow,
        sign, travel Port and layer, the amount, the phase and the momentum; a
        shadow's phase never advances (bit-law-v1, point 9: no clock); what
        leaves an open board is counted as escaped, per family, on the escaped
        line and on the shadows' own, with the momentum it carried on the
        momentum field's (return-field-v1: an escaping share takes its momentum
        with it)."""
        amounts = np.zeros_like(family.fly_amt)
        phases = np.zeros_like(family.fly_ph)
        momenta = np.zeros_like(family.fly_mom)
        definition = family.definition
        for port in range(6):
            source = family.fly_amt[..., port, :]
            if not source.any():
                continue
            axis, forward = port >> 1, (port & 1) == 0
            source_phase = family.fly_ph[..., port, :]
            source_momentum = family.fly_mom[..., port, :, :]
            if self.open:
                moved_amount = np.zeros_like(source)
                moved_phase = np.zeros_like(source_phase)
                moved_momentum = np.zeros_like(source_momentum)
                ahead: list[slice | int] = [slice(None)] * 3
                behind: list[slice | int] = [slice(None)] * 3
                edge: list[slice | int] = [slice(None)] * 3
                if forward:
                    ahead[axis], behind[axis], edge[axis] = slice(1, None), slice(None, -1), -1
                else:
                    ahead[axis], behind[axis], edge[axis] = slice(None, -1), slice(1, None), 0
                moved_amount[tuple(ahead)] = source[tuple(behind)]
                moved_phase[tuple(ahead)] = source_phase[tuple(behind)]
                moved_momentum[tuple(ahead)] = source_momentum[tuple(behind)]
                escaped = int(source[tuple(edge)].sum())
                if escaped:
                    self.engine.escaped[definition.field][0] += escaped
                    self.engine.shadow_escaped[definition.field][0] += escaped
                    if definition.momentum_field is not None:
                        gone = source_momentum[tuple(edge)].astype(np.int64).reshape(-1, 3).sum(axis=0)
                        for axis_index in range(3):
                            value = int(gone[axis_index])
                            self.engine.escaped[definition.momentum_field][axis_index] += value
                            self.engine.shadow_escaped[definition.momentum_field][axis_index] += value
            else:
                shift = 1 if forward else -1
                moved_amount = np.roll(source, shift, axis=axis)
                moved_phase = np.roll(source_phase, shift, axis=axis)
                moved_momentum = np.roll(source_momentum, shift, axis=axis)
            amounts[..., port, :] = moved_amount
            phases[..., port, :] = moved_phase
            momenta[..., port, :, :] = moved_momentum
        family.fly_amt[...] = 0
        family.fly_ph[...] = 0
        family.fly_mom[...] = 0
        return amounts, phases, momenta

    def _engine_receivers(self, incoming: Mapping[int, tuple[np.ndarray, ...]]) -> set[Address3]:
        return {position for position in self.engine_positions if self._receives(incoming, position)}

    @staticmethod
    def _receives(incoming: Mapping[int, tuple[np.ndarray, ...]], position: Address3) -> bool:
        return any(bool(arrays[0][position].any()) for arrays in incoming.values())

    def _engine_bound(
        self,
        target: Address3,
        packets: tuple[SpatialPacket, ...] | list[SpatialPacket],
        residents: Mapping[Address3, DisturbanceNode] | None,
    ) -> bool:
        """Whether the engine must own this Node this interval: a mark, a record, a
        Node holding what the region cannot, or a packet bringing it."""
        if target in self.marks or target in self._wait_bound:
            return True
        carrier = None if residents is None else residents.get(target)
        if carrier is not None and any(record is not None for record in carrier.records):
            return True
        node = self.engine.nodes.get(target)
        if node is not None and not plain_node(node, self.families):
            return True
        for packet in packets:
            if packet.body is not None:
                return True
            if any(any(unpack(payload)) for populations in packet.fields for payload in populations):
                return True
            for index, rays in enumerate(packet.rays):
                if not rays:
                    continue
                family = self.families.get(index)
                if family is None or any(not plain_ray(ray, family.definition, family) for ray in rays):
                    return True
                if any(int(family.heading_index[packet.port]) != ray.heading for ray in rays):
                    return True
        return False

    def _field_wait_nodes(
        self,
        incoming: Mapping[int, tuple[np.ndarray, ...]],
        ready: Mapping[Address3, list[SpatialPacket]],
    ) -> set[Address3]:
        """The shadow's wait under the field reading (shadow-wait-v1): a Node that
        receives shadows of one owner while it holds or receives shadows of
        another (arriving from the arrays or by a packet, or parked in its
        registers) is the engine's this interval, which charges the wait on the
        shares that leave it; a Node of one owner's shadows owes nothing and the
        region cycles it. Nothing without the option."""
        found: set[Address3] = set()
        for index, family in self.families.items():
            definition = family.definition
            if definition.shadow_wait_reads != "field" or not definition.shadow_wait_numerator:
                continue
            arriving = (incoming[index][0] > 0).any(axis=(4, 5, 6, 7))
            for target, packets in ready.items():
                for packet in packets:
                    if index >= len(packet.rays):
                        continue
                    for ray in packet.rays[index]:
                        if ray.detector == BIT_SHADOW and ray.owner in family.rank:
                            arriving[target][family.rank[ray.owner]] = True
            parked = (family.reg > 0).any(axis=(4, 5, 6))
            mixed = arriving.any(axis=3) & ((arriving | parked).sum(axis=3) > 1)
            for x, y, z in zip(*np.nonzero(mixed), strict=True):
                found.add((int(x), int(y), int(z)))
        return found

    def claim(self, position: Address3) -> None:
        """A Node the engine holds from the start (the shadows given with the board
        are installed there): the engine's until the region takes it back at a
        delivery; what it parks is the Node's, not the arrays'."""
        self.owner[position] = 1
        self.visited[position] = True
        self.engine_positions.add(position)

    def _to_engine(self, target: Address3) -> None:
        """The Node becomes the engine's: its parked shares move from the arrays
        to the Node's rays, with their momentum (node-is-ports-v1,
        return-field-v1)."""
        node = self.engine._at(target)
        bundles = list(node.rays) or [() for _ in self.initial.spatial_fields]
        for index, family in self.families.items():
            found: list[Ray] = list(bundles[index])
            found.extend(park_shares(*family.block(target), family.definition))
            family.reg[target] = 0
            family.regph[target] = 0
            family.reg_mom[target] = 0
            bundles[index] = merge_rays(tuple(found))
        node.rays = tuple(bundles)
        node.last_cost = int(self.cost[target])
        self.owner[target] = 1
        self.visited[target] = True
        self.engine_positions.add(target)

    def _to_dense(self, target: Address3) -> None:
        """The Node becomes the region's: its parked shares move from its rays into
        the arrays, with their momentum (node-is-ports-v1, return-field-v1); a
        Node holds nothing else at a delivery, every share on its way having
        left it (a ray still resident is refused)."""
        node = self.engine.nodes[target]
        bundles = list(node.rays) or [() for _ in self.initial.spatial_fields]
        for index, family in self.families.items():
            rays = bundles[index]
            if any(not ray.parked for ray in rays):
                raise ValueError(
                    "the region takes a Node's parked shares: a ray on its way is delivered"
                )
            block, block_phases, block_momenta = parked_shares(rays, family.definition)
            if block:
                family.set_block(target, block, block_phases, block_momenta)
            else:
                family.reg[target] = 0
                family.regph[target] = 0
                family.reg_mom[target] = 0
            bundles[index] = ()
        node.rays = tuple(bundles) if any(bundles) else tuple(() for _ in self.initial.spatial_fields)
        self.cost[target] = node.last_cost
        self.owner[target] = 0
        self.visited[target] = True
        self.engine_positions.discard(target)

    def _hand_over(
        self,
        tick: int,
        incoming: dict[int, tuple[np.ndarray, np.ndarray, np.ndarray]],
    ) -> dict[Address3, list[SpatialPacket]]:
        """The region's departures that reach the engine's Nodes, as packets: one per
        origin and Port, its shadows merged (outgoing and returning, with the
        momentum they carry) and ordered as `merge_rays` orders them, and taken
        out of the arrays."""
        bundles: dict[tuple[Address3, int], list[Rays]] = {}
        engine_mask = self.owner == 1
        for index, family in self.families.items():
            amounts, phases, momenta = incoming[index]
            hits = np.nonzero(engine_mask[..., None, None, None, None, None] & (amounts > 0))
            rays_at: dict[tuple[Address3, int], list[Ray]] = {}
            if hits[0].size:
                for x, y, z, rank, flow, sign, port, layer in zip(*hits, strict=True):
                    cell = (x, y, z, rank, flow, sign, port, layer)
                    key = ((int(x), int(y), int(z)), int(port))
                    rays_at.setdefault(key, []).append(
                        family.ray(rank, flow, sign, port, amounts[cell], phases[cell], momenta[cell])
                    )
                amounts[hits] = 0
                phases[hits] = 0
                momenta[hits] = 0
            for key, rays in rays_at.items():
                bundle = bundles.setdefault(key, [() for _ in range(self.field_count)])
                bundle[index] = merge_rays(tuple(rays))
        handed: dict[Address3, list[SpatialPacket]] = {}
        for (target, port), bundle in sorted(bundles.items()):
            origin = neighbor_address(target, port ^ 1, self.shape, self.initial.boundary)
            assert origin is not None
            handed.setdefault(target, []).append(
                SpatialPacket(tick, origin, port, self.blank_bundle, rays=tuple(bundle))
            )
        return handed

    def _absorb(self, target: Address3, packet: SpatialPacket) -> None:
        """An engine packet arriving at a dense Node: its shadows, outgoing or
        returning, into the arrays layer by layer per owner, flow, sign and Port
        with the momentum they carry, the rest kept whole beside them."""
        for index, rays in enumerate(packet.rays):
            if not rays:
                continue
            family = self.families[index]
            for ray in rays:
                if not family.place(target, ray, packet.port):
                    family.overflow.setdefault(target, []).append(ray)
            self.visited[target] = True

    # -- readouts --------------------------------------------------------------

    def add_totals(self, result: list[list[int]]) -> None:
        """The region's content on the ledger's current line: resident shadows, the
        parked shares' whole quanta and the departures in flight, per field, and
        on the momentum field the momentum the shares carry in flight, resident,
        parked or departing (return-field-v1: a shadow's momentum on the ledger
        is the -dp it carries)."""
        for family in self.families.values():
            definition = family.definition
            resident = int(family.arr_amt.sum()) + int(family.fly_amt.sum())
            carried = (
                family.arr_mom.astype(np.int64).reshape(-1, 3).sum(axis=0)
                + family.fly_mom.astype(np.int64).reshape(-1, 3).sum(axis=0)
                + family.reg_mom.astype(np.int64).reshape(-1, 3).sum(axis=0)
            )
            for rays in family.overflow.values():
                for ray in rays:
                    resident += ray.amount
                    if ray.momentum is not None:
                        carried += np.array(ray.momentum, dtype=np.int64)
            held = int(family.reg.sum())
            if held % family.total:
                raise ValueError("a Node's parked shadows hold whole quanta in total")
            result[definition.field][0] += resident + held // family.total
            if definition.momentum_field is not None:
                for axis in range(3):
                    result[definition.momentum_field][axis] += int(carried[axis])

    def shadow_counts(self, result: dict[int, list[int]]) -> None:
        """The region's shadows per owner: the rays (array entries with content,
        outgoing or returning, and the whole rays beside them) and their amount;
        a parked share is not a ray of its own."""
        for family in self.families.values():
            for rank, owner in enumerate(family.owners):
                entry = result.setdefault(owner, [0, 0])
                arrived, flying = family.arr_amt[:, :, :, rank], family.fly_amt[:, :, :, rank]
                entry[0] += int((arrived > 0).sum()) + int((flying > 0).sum())
                entry[1] += int(arrived.sum()) + int(flying.sum())
            for rays in family.overflow.values():
                for ray in rays:
                    entry = result.setdefault(ray.owner, [0, 0])
                    entry[0] += 1
                    entry[1] += ray.amount

    def materialized_nodes(self, nodes: dict[Address3, SpatialNode]) -> dict[Address3, SpatialNode]:
        """Every Node the region owns and has visited, read as Node state beside the
        engine's own: its resident rays merged in the engine's order (the arrivals,
        outgoing and returning, and the parked shares, with their momentum), the
        amounts delivered per Port, the Ports it received through and the cost of
        its last cycle; the engine's Nodes as they are."""
        result = dict(nodes)
        for x, y, z in zip(*np.nonzero(self.visited & (self.owner == 0)), strict=True):
            position = (int(x), int(y), int(z))
            result[position] = self.materialized_node(position, nodes.get(position))
        return result

    def visited_slab(self, x: int) -> list[Address3]:
        """The region's visited Nodes in one x-slab of the board, in position order:
        what `materialized_nodes` would read there, listed without reading it, so
        that a snapshot can be written one Node at a time (the performance review
        of 2026-09-18: the final snapshot of a filled board no longer holds every
        Node as an object)."""
        found = np.nonzero(self.visited[x] & (self.owner[x] == 0))
        return [(x, int(y), int(z)) for y, z in zip(*found, strict=True)]

    def materialized_node(self, position: Address3, base: SpatialNode | None) -> SpatialNode:
        """One Node the region owns, read as Node state from the arrays: the Node
        `materialized_nodes` gives at that position (`base` the engine's Node there,
        if it holds one)."""
        node = replace(base) if base is not None else self._fresh(position)
        rays = list(node.rays) or [() for _ in self.initial.spatial_fields]
        states = list(node.states)
        mask = [0] * 6
        for index, family in self.families.items():
            definition = family.definition
            found: list[Ray] = []
            delivered = [0] * 6
            amounts = family.arr_amt[position]
            for rank, flow, sign, port, layer in zip(*np.nonzero(amounts > 0), strict=True):
                cell = (rank, flow, sign, port, layer)
                amount = int(amounts[cell])
                found.append(
                    family.ray(
                        rank,
                        flow,
                        sign,
                        port,
                        amount,
                        family.arr_ph[position][cell],
                        family.arr_mom[position][cell],
                    )
                )
                # A returning share is delivered as no flux, as the engine
                # delivers it (`ray_stock` over the outgoing arrivals).
                if not flow:
                    delivered[int(port)] += amount
                mask[int(port) ^ 1] = 1
            for ray in family.overflow.get(position, ()):
                found.append(ray)
                port = family.port_of[ray.heading]
                if ray.outbound:
                    delivered[port] += ray.amount
                mask[port ^ 1] = 1
            found.extend(park_shares(*family.block(position), definition))
            rays[index] = merge_rays(tuple(found))
            states[index] = replace(
                states[index], delivered=tuple(pack((amount,)) for amount in delivered)
            )
        node.rays = tuple(rays)
        node.states = tuple(states)
        node.arrival_mask = tuple(mask)
        node.last_cost = int(self.cost[position])
        node.received_count = sum(mask)
        return node

    def _fresh(self, position: Address3) -> SpatialNode:
        """A Node the engine never created, as `SpatialEngine._at` would create it,
        without registering it anywhere."""
        engine = self.engine
        return SpatialNode(
            engine._blank_states(),
            position=position,
            output=PortBank((None,) * 6),
            arrival_mask=(0,) * 6,
            delay_counts=(0,) * 6,
            localized=engine._blank_localized(),
            rays=tuple(() for _ in self.initial.spatial_fields),
            detector=None,
            arrivals=0,
            body=None,
        )

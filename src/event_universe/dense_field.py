"""The dense mode for boards that a field fills (dense-field-v1).

A host scheduling component, not a physical rule: the shadow-only Nodes of a
board, those holding nothing but shadows of spreading families, are cycled as
one vectorized step over integer arrays that applies the spatial law's spread
and remainder rule (`core/spatial_state.py`, `spread_content`; [field
spreading](../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1))
to every such Node at once, with the same integers: the content arriving on
each heading is split by the six-weight table relative to that heading into
whole quanta that leave and sub-quantum shares that stay parked at the Node
per owner, source sign and Port (`reg`, the parked shadows of node-is-ports-v1
in units of the table's total), each parked share's phase combined with the
share's by the coherence rule (`phase_of_sum` over the family's integer cosine
and sine tables, in the order the engine combines them), a parked share at one
quantum leaving whole with its phase, the departures walking one Link with the
family's phase advance, the open boundary absorbing what walks out, per
family, owner and sign. Since bit-law-v1 (2026-09-18) the region is the
board's shadow layer (point 13 of the law): it holds shadows alone, the bit-0
rays of the spreading families, per owner (the thing whose shadow each is; the
arrays carry an owner axis, the family's declared owners in order), and no
event happens in it: a shadow meets a shadow by the phase sum, a shadow meets
a thing at the thing's Node, the engine's. Since node-is-ports-v1 the region
also carries the shadows walking home, aggregated per Node, owner and heading
(`ret_*`: the amount, the phase of the sum, the momentum they carry, -dp, and
the least steps left), walked one Link back per interval; a return whose steps
are spent follows the owner's trace (`trace`, the Port a thing of that owner
last left the Node by, a zero-amount parked shadow in the engine's terms) or
waits at the Node for a thing of its owner (`wait_*`, per Node and owner), as
the engine's planner does. The loss is the per-ray identity of a return inside
the region (its own phase and steps): the record of a dense Node is its totals.

The region and the engine share the board. A Node is the engine's (sparse)
while it holds a Detector mark, an external body, a record, a thing or any
other content the vectorized step does not describe; every other Node is the
region's (dense). Ownership is decided at every delivery for the Nodes that
receive something: a ray leaving a dense Node toward a sparse Node is handed
over as an ordinary `SpatialPacket` of merged rays, and a packet leaving a
sparse Node into the dense region is absorbed into the arrays, both exact, the
parked shadows, traces and waiting shadows moving with the Node when its
ownership changes. The region publishes no per-Node events: the record of a
dense region is its arrays' totals per tick (the world ledger), and the mode
is not for records that need per-Node field events. Its Nodes read back as
Node state for the totals, the snapshot and the inventory view
(`materialized_nodes`), so `state.json` and the ledger are the acceptance test
of the mode (docs/PERFORMANCE.md).

Bounded integers throughout: amounts are below MAX_VALUE, phases below the
family's modulus, products and sums in signed 64-bit intermediates as the
engine's `checked_work` requires; the arrays hold amounts as int32 (MAX_VALUE
is 2^30 - 1), phases as int16 (the modulus is at most 4096) and the owner
flags as int8, the sums and products promoted to int64 where a value could
grow, and the bounds are checked there.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from typing import TYPE_CHECKING

import numpy as np

from event_universe.core.disturbance_state import MAX_VALUE, Address3, InitialState, pack, unpack
from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.node_ports import PortBank
from event_universe.core.spatial_engine import SpatialEngine
from event_universe.core.spatial_node import SpatialNode
from event_universe.core.spatial_state import (
    BIT_SHADOW,
    POLARIZATION_NONE,
    PORT_HEADINGS,
    REMAINDER_SLOTS,
    Ray,
    Rays,
    SpatialFieldDefinition,
    SpatialPacket,
    merge_rays,
    park_shares,
    parked_shadow,
    parked_shares,
    phase_mask,
    relative_ports,
    spread_content,
    spread_tables,
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
# The array dtypes (node-is-ports-v1, the performance review): amounts below
# MAX_VALUE = 2^30 - 1, phases below 4096, a Port or a flag in a byte.
AMOUNT = np.int32
PHASE = np.int16
PORT = np.int8
# The register phase combination is tabulated over (held, held phase, share,
# share phase) when the table fits; a wider phase or table computes it directly.
COMBINE_TABLE_LIMIT = 1 << 24
# The six unit-axial headings in Port order, as an array.
HEADINGS = np.array(PORT_HEADINGS, dtype=np.int64)


class DenseFamily:
    """The arrays of one spreading family on the board.

    `arr_*` hold the shadows resident at each Node, arrived this interval and due
    to spread: per owner (the family's declared owners in order), source sign
    (-1, 0, 1 as 0, 1, 2), travel Port (the heading the content arrived on, the
    engine's `arrived` index) and layer, the amount and the phase. `reg` and
    `regph` are the eighteen parked shares and their phases per Node and owner,
    sign-major then Port, in units of 1/S. `fly_*` hold the departures of the
    last cycle until the delivery walks them one Link. `ret_*` hold the shadows
    walking home resident at each Node per owner and the Port they walk through
    (the amount, the phase of the sum, the momentum carried, -dp, and the least
    steps left), `wait_*` those waiting at a Node for a thing of their owner, and
    `trace` the Port a thing of each owner last left the Node by plus one, 0 for
    none (node-is-ports-v1)."""

    def __init__(
        self, index: int, definition: SpatialFieldDefinition, shape: Address3, prices: dict[str, int]
    ) -> None:
        self.index = index
        self.definition = definition
        self.field = definition.field
        self.owners: tuple[int, ...] = definition.owners or (0,)
        self.rank = {owner: rank for rank, owner in enumerate(self.owners)}
        count = len(self.owners)
        self.table = np.array(definition.spread, dtype=np.int64)
        self.total = int(sum(definition.spread))
        # The steering table of the shadows' spread (phase-spread-v1), one entry
        # per phase step of the family's modulus.
        self.steering = np.array(definition.steering or (1,), dtype=np.int64)
        # relative[p, i]: the absolute Port of relative entry i for content arriving
        # on the heading of Port p (forward, backward, the four transverse).
        self.relative = np.array([relative_ports(p) for p in range(6)], dtype=np.int64)
        self.modulus = definition.phase_modulus
        self.mask = phase_mask(self.modulus)
        self.advance = definition.phase_advance
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
        self.combine_table = self._combine_table()
        self.arr_amt = np.zeros((*shape, count, SIGNS, 6, LAYERS), dtype=AMOUNT)
        self.arr_ph = np.zeros((*shape, count, SIGNS, 6, LAYERS), dtype=PHASE)
        self.overflow: dict[Address3, list[Ray]] = {}
        self.reg = np.zeros((*shape, count, SIGNS, 6), dtype=AMOUNT)
        self.regph = np.zeros((*shape, count, SIGNS, 6), dtype=PHASE)
        self.fly_amt = np.zeros((*shape, count, SIGNS, 6, LAYERS), dtype=AMOUNT)
        self.fly_ph = np.zeros((*shape, count, SIGNS, 6, LAYERS), dtype=PHASE)
        # The shadows walking home (per owner, sign and the Port they walk
        # through), those waiting for a thing of their owner (per owner and
        # sign) and the traces (per owner), node-is-ports-v1.
        self.ret_amt = np.zeros((*shape, count, SIGNS, 6), dtype=AMOUNT)
        self.ret_ph = np.zeros((*shape, count, SIGNS, 6), dtype=PHASE)
        self.ret_mom = np.zeros((*shape, count, SIGNS, 6, 3), dtype=AMOUNT)
        self.ret_steps = np.zeros((*shape, count, SIGNS, 6), dtype=AMOUNT)
        self.wait_amt = np.zeros((*shape, count, SIGNS), dtype=AMOUNT)
        self.wait_ph = np.zeros((*shape, count, SIGNS), dtype=PHASE)
        self.wait_mom = np.zeros((*shape, count, SIGNS, 3), dtype=AMOUNT)
        self.trace = np.zeros((*shape, count), dtype=PORT)
        self.prices = prices

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

    def _combine_table(self) -> np.ndarray | None:
        """The register's phase after a share joins it, for every (held, held phase,
        share, share phase) a cycle can present: the phase step nearest the
        direction of held e^(i held phase) + share e^(i share phase) over the
        family's tables, ties to the lowest step, exactly `_phase_of_sum`. A
        register holds below S before the cycle and gains at most one share
        below S per arriving Port, so held stays below 7 S."""
        if self.cosines is None or self.sines is None:
            return None
        S, M = self.total, self.modulus
        if 7 * S * M * S * M * M > COMBINE_TABLE_LIMIT:
            return None
        held = np.arange(7 * S, dtype=np.int64)[:, None, None, None]
        hph = np.arange(M, dtype=np.int64)[None, :, None, None]
        share = np.arange(S, dtype=np.int64)[None, None, :, None]
        sph = np.arange(M, dtype=np.int64)[None, None, None, :]
        x = held * self.cosines[hph] + share * self.cosines[sph]
        y = held * self.sines[hph] + share * self.sines[sph]
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
        """The register's phase after the share joins it, elementwise."""
        if self.combine_table is not None:
            S, M = self.total, self.modulus
            flat = ((held * M + hph) * S + share) * M + sph
            return np.asarray(np.take(self.combine_table.reshape(-1), flat), dtype=np.int64)
        assert self.cosines is not None and self.sines is not None
        x = held * self.cosines[hph] + share * self.cosines[sph]
        y = held * self.sines[hph] + share * self.sines[sph]
        return self._nearest_step(x, y)


def plain_ray(ray: Ray, definition: SpatialFieldDefinition, family: DenseFamily | None = None) -> bool:
    """Whether a ray is content the dense region describes: a shadow of one of the
    family's owners on a Port heading without an event, a delay, a wait, a lag,
    an own advance or a polarization (bit-law-v1: a thing is never the
    region's), either outbound one Link from its departure, or walking home
    with the momentum it carries (aggregated per Node, owner, sign and heading),
    or waiting at rest with its steps spent, or parked (node-is-ports-v1)."""
    if (
        ray.detector != BIT_SHADOW
        or (family is not None and ray.owner not in family.rank)
        or ray.event_ports
        or any(ray.event_shares)
        or ray.advance != -1
        or ray.wait
        or ray.interaction_delay
        or ray.lag != (0, 0, 0)
        or ray.polarization != POLARIZATION_NONE
        or ray.accumulators != (0, 0, 0)
        or definition.headings[ray.heading] not in PORT_HEADINGS
    ):
        return False
    if ray.parked:
        return True
    if ray.outbound:
        return ray.steps == 1 and ray.amount > 0 and ray.momentum is None
    return ray.amount > 0


def plain_node(node: SpatialNode, families: Mapping[int, DenseFamily] | None = None) -> bool:
    """Whether an engine Node holds nothing the region cannot own: no mark, no
    body, no pending cycle, no octant stock, no deposit, and no resident ray
    but the shadows the region describes (parked, waiting or walking home)."""
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

    # -- the cycle -------------------------------------------------------------

    def active_count(self) -> int:
        """The dense Nodes the last cycle cycled: those with arrivals or registers."""
        return self._active

    def cycle(self, tick: int) -> None:
        """The spread of every dense Node with content, at once (field-spreading-v1,
        field-remainder-v1, phase-spread-v1): the same integers as `spread_content`
        at each, the departures kept in flight until the delivery and the cost of
        each cycle as the spatial law would meter it. A Node holding more shadows
        than the arrays' layers is cycled by `spread_content` itself, ray by ray."""
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
            # A Node holding a parked share, a waiting shadow or a return stays
            # active, as the engine's does (node-is-ports-v1).
            registers = (family.reg > 0).any(axis=(3, 4, 5)) | (family.wait_amt > 0).any(axis=(3, 4))
            returns, returns_cost, return_ports = self._cycle_returns(family)
            ports_any |= return_ports
            has_registers |= registers | returns
            family_cost += returns_cost
            present = count > 0
            has_arrivals |= present
            if not present.any():
                continue
            phase = self._group_phase(family)
            steered, lone = self._steer(family, phase)
            departures, released_phase, released = self._split(family, lone, phase)
            departures += steered
            layer_0, layer_1, phase_1 = self._departures(
                family, departures, released, phase, released_phase
            )
            self._place_departures(family, layer_0, layer_1, phase, phase_1)
            for position, (_, _, departed) in fallback.items():
                self._place_rays(family, position, departed)
            outgoing = family.fly_amt > 0
            departing = outgoing.sum(axis=(3, 4, 5, 6)).astype(np.int64)
            sending = outgoing.any(axis=(3, 4, 6)).sum(axis=3)
            cost = np.zeros(self.shape, dtype=np.int64)
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
        owners = len(family.owners)
        for position, extra in sorted(family.overflow.items()):
            rays = list(extra)
            amounts, phases = family.arr_amt[position], family.arr_ph[position]
            for rank, sign, port, layer in zip(*np.nonzero(amounts > 0), strict=True):
                rays.append(
                    Ray(
                        int(family.heading_index[port]),
                        (0, 0, 0),
                        int(amounts[rank, sign, port, layer]),
                        phase=int(phases[rank, sign, port, layer]),
                        steps=1,
                        detector=BIT_SHADOW,
                        source_sign=int(sign) - 1,
                        owner=family.owners[int(rank)],
                    )
                )
            held = tuple(int(v) for v in family.reg[position].reshape(-1))
            held_phases = tuple(int(v) for v in family.regph[position].reshape(-1))
            departed, _, after, after_phases = spread_content(
                family.index, tuple(rays), family.definition, held, held_phases
            )
            family.reg[position] = np.array(after, dtype=np.int64).reshape(owners, SIGNS, 6)
            family.regph[position] = np.array(after_phases, dtype=np.int64).reshape(owners, SIGNS, 6)
            ports = np.zeros(6, dtype=bool)
            for ray in rays:
                ports[family.port_of[ray.heading]] = True
            amounts[...] = 0
            phases[...] = 0
            result[position] = (rays, ports, departed)
        family.overflow.clear()
        return result

    def _place_rays(self, family: DenseFamily, position: Address3, departed: Rays) -> None:
        """The departures of one Node cycled ray by ray, into the flight arrays."""
        amounts, phases = family.fly_amt[position], family.fly_ph[position]
        amounts[...] = 0
        phases[...] = 0
        for ray in departed:
            rank, sign, port = family.rank[ray.owner], ray.source_sign + 1, family.port_of[ray.heading]
            layers = amounts[rank, sign, port]
            free = [layer for layer in range(LAYERS) if layers[layer] == 0]
            if not free:
                raise ValueError("ray slot budget exceeded")
            amounts[rank, sign, port, free[0]] = ray.amount
            phases[rank, sign, port, free[0]] = ray.phase

    def _arrivals(self, family: DenseFamily) -> tuple[np.ndarray, np.ndarray]:
        """What arrived at every Node this interval: the number of shadows and the
        Ports with content."""
        present = family.arr_amt > 0
        if family.arr_amt.max(initial=0) > MAX_VALUE:
            raise ValueError("value exceeds the disturbance integer bound")
        count = present.sum(axis=(3, 4, 5, 6)).astype(np.int64)
        ports = present.any(axis=(3, 4, 6))
        return count, ports

    def _group_phase(self, family: DenseFamily) -> np.ndarray:
        """The phase of each owner's content at each Node, per owner and sign: the
        step nearest the coherent sum of its shares (`spread_content`'s group
        phase); 0 for a family without a phase width."""
        shape = (*self.shape, len(family.owners), SIGNS)
        if family.cosines is None or family.sines is None:
            return np.zeros(shape, dtype=np.int64)
        amounts, phases = family.arr_amt, family.arr_ph
        x = (amounts * family.cosines[phases]).sum(axis=(5, 6))
        y = (amounts * family.sines[phases]).sum(axis=(5, 6))
        self._check_projection(x)
        return family._nearest_step(x, y)

    @staticmethod
    def _check_projection(x: np.ndarray) -> None:
        if max(abs(int(x.max(initial=0))), abs(int(x.min(initial=0)))) * 256 > MAX_WORK_INT:
            raise OverflowError("64-bit intermediate range exceeded")

    def _steer(self, family: DenseFamily, phase: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """The shares that meet others of their owner at a Node (phase-spread-v1):
        each continues on its own heading with the whole quanta of amount x
        steering[difference] / modulus, the difference its phase to the step
        nearest the coherent sum of the others, and sends the rest through the
        four transverse headings, rest // 4 each and the remainder one to each
        of the first in Port order, exactly `spread_content`. Returns the
        steered departures per owner, sign and Port, and the lone shares per
        owner, sign and Port for the fixed split."""
        amounts, phases = family.arr_amt, family.arr_ph
        owners = len(family.owners)
        present = amounts > 0
        count = present.sum(axis=(5, 6))
        meeting = present & (count[..., None, None] >= 2)
        lone = np.where(present & (count[..., None, None] == 1), amounts, 0).sum(axis=6)
        departures = np.zeros((*self.shape, owners, SIGNS, 6), dtype=np.int64)
        if not meeting.any():
            return departures, lone
        if family.cosines is None or family.sines is None:
            delta = np.zeros(amounts.shape, dtype=np.int64)
        else:
            cosines, sines = family.cosines[phases], family.sines[phases]
            x = (amounts * cosines).sum(axis=(5, 6))
            y = (amounts * sines).sum(axis=(5, 6))
            others_x = x[..., None, None] - amounts * cosines
            others_y = y[..., None, None] - amounts * sines
            self._check_projection(others_x)
            delta = (phases - family._nearest_step(others_x, others_y)) & family.mask
        forward = np.where(meeting, amounts * family.steering[delta] // family.modulus, 0)
        rest = np.where(meeting, amounts - forward, 0)
        each, extra = rest // 4, rest % 4
        departures += forward.sum(axis=6)
        for port in range(6):
            for offset, target in enumerate(family.relative[port][2:]):
                share = each[..., port, :] + (offset < extra[..., port, :])
                departures[..., int(target)] += np.where(meeting[..., port, :], share, 0).sum(axis=-1)
        return departures, lone

    def _split(
        self, family: DenseFamily, arrived: np.ndarray, phase: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """The fixed split of each lone share by the table relative to its heading,
        in the engine's order (Port by Port): the whole quanta per absolute target
        Port, owner and sign, the shares into the registers with their phases
        combined at the owner's phase, then every register at S or more releasing
        its whole quanta with its phase and resetting its phase when it empties."""
        S = family.total
        reg, regph = family.reg, family.regph
        departures = np.zeros((*self.shape, len(family.owners), SIGNS, 6), dtype=np.int64)
        phase_b = phase[..., None]
        for port in range(6):
            content = arrived[..., port]
            if not content.any():
                continue
            product = content[..., None] * family.table
            whole = product // S
            share = product - whole * S
            targets = family.relative[port]
            departures[..., targets] += whole
            held = reg[..., targets]
            held_phase = regph[..., targets]
            has_share = share > 0
            if family.cosines is None:
                new_phase = np.where(has_share, 0, held_phase)
            else:
                combined = family.combine(held, held_phase, share, np.broadcast_to(phase_b, held.shape))
                new_phase = np.where(has_share, np.where(held > 0, combined, phase_b), held_phase)
            reg[..., targets] = held + share
            regph[..., targets] = new_phase
        whole = reg // S
        releasing = whole > 0
        rest = reg - whole * S
        released_phase = regph.copy()
        reg[...] = np.where(releasing, rest, reg)
        regph[...] = np.where(releasing & (rest == 0), 0, regph)
        return departures, released_phase, whole

    @staticmethod
    def _departures(
        family: DenseFamily,
        departures: np.ndarray,
        released: np.ndarray,
        phase: np.ndarray,
        released_phase: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """The two layers per owner, sign and Port: the spread's quanta at the
        owner's phase and the register's release at its phase, one ray when the
        phases are equal (the departures of one Port merge)."""
        phase_b = phase[..., None]
        same = (released > 0) & (departures > 0) & (released_phase == phase_b)
        layer_0 = departures + np.where(same, released, 0)
        layer_1 = np.where(same, 0, released)
        return layer_0, layer_1, released_phase

    def _place_departures(
        self,
        family: DenseFamily,
        layer_0: np.ndarray,
        layer_1: np.ndarray,
        phase: np.ndarray,
        phase_1: np.ndarray,
    ) -> None:
        if max(int(layer_0.max(initial=0)), int(layer_1.max(initial=0))) > MAX_VALUE:
            raise ValueError("value exceeds the disturbance integer bound")
        phase_b = phase[..., None]
        family.fly_amt[..., 0] = layer_0
        family.fly_ph[..., 0] = np.where(layer_0 > 0, phase_b, 0)
        family.fly_amt[..., 1] = layer_1
        family.fly_ph[..., 1] = np.where(layer_1 > 0, phase_1, 0)

    # -- the shadows walking home (node-is-ports-v1) ---------------------------

    @staticmethod
    def _merge_cells(
        family: DenseFamily,
        target: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray | None],
        source: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray | None],
        mask: np.ndarray,
    ) -> None:
        """Merge the source cells into the target cells where `mask`, in place: the
        amounts and the momenta add, the phase is the phase of the sum, the steps
        the least (the bound of the merged returns); a target cell without content
        takes the source as it is."""
        t_amt, t_ph, t_mom, t_steps = target
        s_amt, s_ph, s_mom, s_steps = source
        had = mask & (t_amt > 0)
        fresh = mask & (t_amt == 0)
        if had.any():
            phase = family.phase_of_pair(t_amt, t_ph, s_amt, s_ph)
            t_ph[...] = np.where(had, phase, t_ph)
        t_ph[...] = np.where(fresh, s_ph, t_ph)
        total = t_amt.astype(np.int64) + s_amt
        if int(np.where(mask, total, 0).max(initial=0)) > MAX_VALUE:
            raise ValueError("value exceeds the disturbance integer bound")
        t_amt[...] = np.where(mask, total, t_amt)
        momentum = t_mom.astype(np.int64) + s_mom
        if int(np.abs(np.where(mask[..., None], momentum, 0)).max(initial=0)) > MAX_VALUE:
            raise ValueError("value exceeds the disturbance integer bound")
        t_mom[...] = np.where(mask[..., None], momentum, t_mom)
        if t_steps is not None and s_steps is not None:
            t_steps[...] = np.where(had, np.minimum(t_steps, s_steps), np.where(fresh, s_steps, t_steps))

    def _cycle_returns(self, family: DenseFamily) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """The returns resident at every dense Node this interval, as the engine's
        planner treats them: one whose steps are spent follows the owner's trace
        (its Port becomes the trace's) or, without one, waits at the Node for a
        thing of its owner; every other walks on. Returns the Nodes holding a
        return, the cost the planner would meter (read and route per return, an
        update per heading changed) and the Ports they leave by."""
        prices = self.prices
        amt = family.ret_amt
        present = amt > 0
        holding = present.any(axis=(3, 4, 5))
        cost = np.zeros(self.shape, dtype=np.int64)
        ports = np.zeros((*self.shape, 6), dtype=bool)
        if not holding.any():
            return holding, cost, ports
        spent = present & (family.ret_steps == 0)
        if spent.any():
            trace = family.trace[..., None, None]
            followed = spent & (trace > 0)
            waiting = spent & (trace == 0)
            if waiting.any():
                for port in range(6):
                    mask = waiting[..., port]
                    if not mask.any():
                        continue
                    self._merge_cells(
                        family,
                        (family.wait_amt, family.wait_ph, family.wait_mom, None),
                        (amt[..., port], family.ret_ph[..., port], family.ret_mom[..., port, :], None),
                        mask,
                    )
                    amt[..., port] = np.where(mask, 0, amt[..., port])
                    family.ret_ph[..., port] = np.where(mask, 0, family.ret_ph[..., port])
                    family.ret_mom[..., port, :] = np.where(mask[..., None], 0, family.ret_mom[..., port, :])
                    family.ret_steps[..., port] = np.where(mask, 0, family.ret_steps[..., port])
            if followed.any():
                turned = np.zeros(self.shape, dtype=np.int64)
                for target in range(6):
                    for port in range(6):
                        if port == target:
                            continue
                        mask = followed[..., port] & (trace[..., 0] == target + 1)
                        if not mask.any():
                            continue
                        self._merge_cells(
                            family,
                            (
                                amt[..., target],
                                family.ret_ph[..., target],
                                family.ret_mom[..., target, :],
                                family.ret_steps[..., target],
                            ),
                            (
                                amt[..., port].copy(),
                                family.ret_ph[..., port].copy(),
                                family.ret_mom[..., port, :].copy(),
                                family.ret_steps[..., port].copy(),
                            ),
                            mask,
                        )
                        amt[..., port] = np.where(mask, 0, amt[..., port])
                        family.ret_ph[..., port] = np.where(mask, 0, family.ret_ph[..., port])
                        family.ret_mom[..., port, :] = np.where(mask[..., None], 0, family.ret_mom[..., port, :])
                        family.ret_steps[..., port] = np.where(mask, 0, family.ret_steps[..., port])
                        turned += mask.sum(axis=(3, 4))
                cost += prices["update"] * turned
        present = amt > 0
        count = present.sum(axis=(3, 4, 5)).astype(np.int64)
        ports = present.any(axis=(3, 4))
        cost += (prices["read"] + prices["route"]) * count
        return holding, cost, ports

    def _walk_returns(self, family: DenseFamily) -> tuple[np.ndarray, ...]:
        """The returns one Link on, each through the Port it walks, its steps one
        fewer while any are left (a return whose steps are spent walks on the
        trace's line with its count at 0); what leaves an open board is counted as
        escaped with the momentum it carried, per family, on the escaped line and
        the shadows' own. Returns what arrives at each Node: the amount, phase,
        momentum and steps per owner, sign and Port; the arrays are emptied."""
        definition = family.definition
        amounts = np.zeros_like(family.ret_amt)
        phases = np.zeros_like(family.ret_ph)
        momenta = np.zeros_like(family.ret_mom)
        steps = np.zeros_like(family.ret_steps)
        for port in range(6):
            source = family.ret_amt[..., port]
            if not source.any():
                continue
            axis, forward = port >> 1, (port & 1) == 0
            source_phase = family.ret_ph[..., port]
            source_momentum = family.ret_mom[..., port, :]
            source_steps = np.maximum(family.ret_steps[..., port] - 1, 0)
            if self.open:
                ahead: list[slice | int] = [slice(None)] * 3
                behind: list[slice | int] = [slice(None)] * 3
                edge: list[slice | int] = [slice(None)] * 3
                if forward:
                    ahead[axis], behind[axis], edge[axis] = slice(1, None), slice(None, -1), -1
                else:
                    ahead[axis], behind[axis], edge[axis] = slice(None, -1), slice(1, None), 0
                amounts[(*ahead, Ellipsis, port)] = source[tuple(behind)]
                phases[(*ahead, Ellipsis, port)] = source_phase[tuple(behind)]
                momenta[(*ahead, Ellipsis, port, slice(None))] = source_momentum[tuple(behind)]
                steps[(*ahead, Ellipsis, port)] = source_steps[tuple(behind)]
                escaped = int(source[tuple(edge)].sum())
                if escaped:
                    self.engine.escaped[definition.field][0] += escaped
                    self.engine.shadow_escaped[definition.field][0] += escaped
                    if definition.momentum_field is not None:
                        gone = source_momentum[tuple(edge)].astype(np.int64).sum(axis=(0, 1, 2, 3))
                        for axis_index in range(3):
                            value = int(gone[axis_index])
                            self.engine.escaped[definition.momentum_field][axis_index] += value
                            self.engine.shadow_escaped[definition.momentum_field][axis_index] += value
            else:
                shift = 1 if forward else -1
                amounts[..., port] = np.roll(source, shift, axis=axis)
                phases[..., port] = np.roll(source_phase, shift, axis=axis)
                momenta[..., port, :] = np.roll(source_momentum, shift, axis=axis)
                steps[..., port] = np.roll(source_steps, shift, axis=axis)
        family.ret_amt[...] = 0
        family.ret_ph[...] = 0
        family.ret_mom[...] = 0
        family.ret_steps[...] = 0
        return amounts, phases, momenta, steps

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
        packets left for the engine to deliver and the packets absorbed."""
        incoming = {index: self._walk(family) for index, family in self.families.items()}
        returning = {index: self._walk_returns(family) for index, family in self.families.items()}
        engine_incoming = self._engine_receivers(incoming) | self._engine_receivers(returning)
        candidates = set(ready) | engine_incoming
        if residents is not None:
            for position, carrier in residents.items():
                if any(record is not None for record in carrier.records) and (
                    position in ready
                    or self._receives(incoming, position)
                    or self._receives(returning, position)
                ):
                    candidates.add(position)
        for target in sorted(candidates):
            bound = self._engine_bound(target, ready.get(target, ()), residents)
            if bound and not self.owner[target]:
                self._to_engine(target)
            elif not bound and self.owner[target]:
                self._to_dense(target)
        handed = self._hand_over(tick, incoming, returning)
        absorbed: list[SpatialPacket] = []
        for target in list(ready):
            if not self.owner[target]:
                for packet in ready.pop(target):
                    self._absorb(target, packet)
                    absorbed.append(packet)
        for index, family in self.families.items():
            amounts, phases = incoming[index]
            family.arr_amt += amounts
            family.arr_ph += phases
            back_amount, back_phase, back_momentum, back_steps = returning[index]
            arrived_back = back_amount > 0
            if arrived_back.any():
                self._merge_cells(
                    family,
                    (family.ret_amt, family.ret_ph, family.ret_mom, family.ret_steps),
                    (back_amount, back_phase, back_momentum, back_steps),
                    arrived_back,
                )
            present = (family.arr_amt > 0).any(axis=(3, 4, 5, 6)) | arrived_back.any(axis=(3, 4, 5))
            self.visited |= present
            count = (family.arr_amt > 0).sum(axis=(3, 4, 5, 6)) + (family.ret_amt > 0).sum(axis=(3, 4, 5))
            for position, rays in family.overflow.items():
                count[position] += len(rays)
            if count.max(initial=0) > family.definition.ray_slots:
                raise ValueError("ray slot budget exceeded")
        for target, packets in handed.items():
            ready.setdefault(target, []).extend(packets)
        return ready, absorbed

    def _walk(self, family: DenseFamily) -> tuple[np.ndarray, np.ndarray]:
        """The departures one Link on: what arrives at each Node per owner, sign,
        travel Port and layer; a shadow's phase never advances (bit-law-v1, point
        9: no clock); what leaves an open board is counted as escaped, per family,
        on the escaped line and on the shadows' own (no charge, no momentum: a
        shadow carries neither on the ledger)."""
        amounts = np.zeros_like(family.fly_amt)
        phases = np.zeros_like(family.fly_ph)
        definition = family.definition
        for port in range(6):
            source = family.fly_amt[..., port, :]
            if not source.any():
                continue
            axis, forward = port >> 1, (port & 1) == 0
            moved_amount = np.zeros_like(source)
            moved_phase = np.zeros_like(source)
            source_phase = family.fly_ph[..., port, :]
            if self.open:
                ahead: list[slice | int] = [slice(None)] * 3
                behind: list[slice | int] = [slice(None)] * 3
                edge: list[slice | int] = [slice(None)] * 3
                if forward:
                    ahead[axis], behind[axis], edge[axis] = slice(1, None), slice(None, -1), -1
                else:
                    ahead[axis], behind[axis], edge[axis] = slice(None, -1), slice(1, None), 0
                moved_amount[tuple(ahead)] = source[tuple(behind)]
                moved_phase[tuple(ahead)] = source_phase[tuple(behind)]
                escaped = int(source[tuple(edge)].sum())
                if escaped:
                    self.engine.escaped[definition.field][0] += escaped
                    self.engine.shadow_escaped[definition.field][0] += escaped
            else:
                shift = 1 if forward else -1
                moved_amount = np.roll(source, shift, axis=axis)
                moved_phase = np.roll(source_phase, shift, axis=axis)
            amounts[..., port, :] = moved_amount
            phases[..., port, :] = moved_phase
        family.fly_amt[...] = 0
        family.fly_ph[...] = 0
        return amounts, phases

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
        if target in self.marks:
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

    def claim(self, position: Address3) -> None:
        """A Node the engine holds from the start (the shadows given with the board
        are installed there): the engine's until the region takes it back at a
        delivery; what it parks is the Node's, not the arrays'."""
        self.owner[position] = 1
        self.visited[position] = True
        self.engine_positions.add(position)

    def _to_engine(self, target: Address3) -> None:
        """The Node becomes the engine's: its parked shares, traces and waiting
        shadows move from the arrays to the Node's rays (node-is-ports-v1)."""
        node = self.engine._at(target)
        bundles = list(node.rays) or [() for _ in self.initial.spatial_fields]
        for index, family in self.families.items():
            definition = family.definition
            found: list[Ray] = list(bundles[index])
            found.extend(
                park_shares(
                    tuple(int(v) for v in family.reg[target].reshape(-1)),
                    tuple(int(v) for v in family.regph[target].reshape(-1)),
                    definition,
                )
            )
            for rank, port in zip(*np.nonzero(family.trace[target]), strict=True):
                found.append(parked_shadow(family.owners[int(rank)], int(port) - 1, definition))
            found.extend(self._waiting_rays(family, target))
            family.reg[target] = 0
            family.regph[target] = 0
            family.trace[target] = 0
            family.wait_amt[target] = 0
            family.wait_ph[target] = 0
            family.wait_mom[target] = 0
            bundles[index] = merge_rays(tuple(found))
        node.rays = tuple(bundles)
        node.last_cost = int(self.cost[target])
        self.owner[target] = 1
        self.visited[target] = True
        self.engine_positions.add(target)

    def _to_dense(self, target: Address3) -> None:
        """The Node becomes the region's: its parked shares, traces and waiting
        shadows move from its rays into the arrays (node-is-ports-v1)."""
        node = self.engine.nodes[target]
        bundles = list(node.rays) or [() for _ in self.initial.spatial_fields]
        for index, family in self.families.items():
            definition = family.definition
            rays = bundles[index]
            block, block_phases = parked_shares(rays, definition)
            size = REMAINDER_SLOTS * len(family.owners)
            family.reg[target] = np.array(block or (0,) * size, dtype=np.int64).reshape(
                len(family.owners), SIGNS, 6
            )
            family.regph[target] = np.array(block_phases or (0,) * size, dtype=np.int64).reshape(
                len(family.owners), SIGNS, 6
            )
            family.trace[target] = 0
            for ray in rays:
                if ray.parked and not ray.amount:
                    family.trace[target][family.rank[ray.owner]] = family.port_of[ray.heading] + 1
            family.wait_amt[target] = 0
            family.wait_ph[target] = 0
            family.wait_mom[target] = 0
            for ray in rays:
                if ray.parked or ray.outbound:
                    continue
                # A shadow waiting at rest for a thing of its owner (settled rule (ii)).
                cell = (family.rank[ray.owner], ray.source_sign + 1)
                momentum = ray.momentum or (0, 0, 0)
                held = int(family.wait_amt[target][cell])
                if held:
                    phase = int(
                        family.phase_of_pair(
                            np.array(held), family.wait_ph[target][cell], np.array(ray.amount), np.array(ray.phase)
                        )
                    )
                else:
                    phase = ray.phase
                family.wait_amt[target][cell] = held + ray.amount
                family.wait_ph[target][cell] = phase
                family.wait_mom[target][cell] += np.array(momentum, dtype=np.int64)
            bundles[index] = ()
        node.rays = tuple(bundles) if any(bundles) else tuple(() for _ in self.initial.spatial_fields)
        self.cost[target] = node.last_cost
        self.owner[target] = 0
        self.visited[target] = True
        self.engine_positions.discard(target)

    def _waiting_rays(self, family: DenseFamily, position: Address3) -> list[Ray]:
        """The shadows waiting at a Node as rays: at rest, their steps spent, with
        the momentum they carry (node-is-ports-v1)."""
        definition = family.definition
        found: list[Ray] = []
        for rank, sign in zip(*np.nonzero(family.wait_amt[position]), strict=True):
            momentum = tuple(int(v) for v in family.wait_mom[position][rank, sign])
            found.append(
                Ray(
                    int(family.heading_index[0]),
                    (0, 0, 0),
                    int(family.wait_amt[position][rank, sign]),
                    phase=int(family.wait_ph[position][rank, sign]),
                    outbound=0,
                    detector=BIT_SHADOW,
                    source_sign=int(sign) - 1,
                    momentum=momentum if any(momentum) else None,
                    owner=family.owners[int(rank)],
                )
            )
        return found

    def _returning_rays(
        self, family: DenseFamily, position: Address3, arrays: tuple[np.ndarray, ...] | None = None
    ) -> dict[int, list[Ray]]:
        """The returns at a Node as rays per Port (node-is-ports-v1): each walking
        home on its Port's heading with its amount, the phase of its sum, its
        momentum and its steps; from the resident arrays or from `arrays`."""
        definition = family.definition
        amounts, phases, momenta, steps = (
            (family.ret_amt, family.ret_ph, family.ret_mom, family.ret_steps) if arrays is None else arrays
        )
        found: dict[int, list[Ray]] = {}
        for rank, sign, port in zip(*np.nonzero(amounts[position]), strict=True):
            momentum = tuple(int(v) for v in momenta[position][rank, sign, port])
            found.setdefault(int(port), []).append(
                Ray(
                    int(family.heading_index[port]),
                    (0, 0, 0),
                    int(amounts[position][rank, sign, port]),
                    phase=int(phases[position][rank, sign, port]),
                    steps=int(steps[position][rank, sign, port]),
                    outbound=0,
                    detector=BIT_SHADOW,
                    source_sign=int(sign) - 1,
                    momentum=momentum if any(momentum) else None,
                    owner=family.owners[int(rank)],
                )
            )
        assert definition is not None
        return found

    def _hand_over(
        self,
        tick: int,
        incoming: dict[int, tuple[np.ndarray, np.ndarray]],
        returning: dict[int, tuple[np.ndarray, ...]] | None = None,
    ) -> dict[Address3, list[SpatialPacket]]:
        """The region's departures that reach the engine's Nodes, as packets: one per
        origin and Port, its shadows merged and ordered as `forward_rays` orders
        them, the returns among them (node-is-ports-v1), and taken out of the
        arrays."""
        bundles: dict[tuple[Address3, int], list[Rays]] = {}
        engine_mask = self.owner == 1
        for index, family in self.families.items():
            amounts, phases = incoming[index]
            hits = np.nonzero(engine_mask[..., None, None, None, None] & (amounts > 0))
            rays_at: dict[tuple[Address3, int], list[Ray]] = {}
            if hits[0].size:
                for x, y, z, rank, sign, port, layer in zip(*hits, strict=True):
                    target = (int(x), int(y), int(z))
                    key = (target, int(port))
                    rays_at.setdefault(key, []).append(
                        Ray(
                            int(family.heading_index[port]),
                            (0, 0, 0),
                            int(amounts[x, y, z, rank, sign, port, layer]),
                            phase=int(phases[x, y, z, rank, sign, port, layer]),
                            steps=1,
                            detector=BIT_SHADOW,
                            source_sign=int(sign) - 1,
                            owner=family.owners[int(rank)],
                        )
                    )
                amounts[hits] = 0
                phases[hits] = 0
            if returning is not None:
                back = returning[index]
                back_hits = np.nonzero(engine_mask[..., None, None, None] & (back[0] > 0))
                if back_hits[0].size:
                    for x, y, z in sorted({(int(x), int(y), int(z)) for x, y, z, *_ in zip(*back_hits, strict=True)}):
                        for port, rays in self._returning_rays(family, (x, y, z), back).items():
                            rays_at.setdefault(((x, y, z), port), []).extend(rays)
                    for array in back:
                        array[back_hits] = 0
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
        """An engine packet arriving at a dense Node: its outbound shadows into the
        arrays, layer by layer per owner, sign and Port, the rest kept whole beside
        them; its returns into the returning layer per owner, sign and Port, merged
        (node-is-ports-v1)."""
        for index, rays in enumerate(packet.rays):
            if not rays:
                continue
            family = self.families[index]
            for ray in rays:
                rank = family.rank[ray.owner]
                sign = ray.source_sign + 1
                port = packet.port
                if not ray.outbound:
                    cell = (rank, sign, port)
                    held = int(family.ret_amt[target][cell])
                    if held:
                        phase = int(
                            family.phase_of_pair(
                                np.array(held),
                                family.ret_ph[target][cell],
                                np.array(ray.amount),
                                np.array(ray.phase),
                            )
                        )
                        family.ret_steps[target][cell] = min(int(family.ret_steps[target][cell]), ray.steps)
                    else:
                        phase = ray.phase
                        family.ret_steps[target][cell] = ray.steps
                    family.ret_amt[target][cell] = held + ray.amount
                    family.ret_ph[target][cell] = phase
                    family.ret_mom[target][cell] += np.array(ray.momentum or (0, 0, 0), dtype=np.int64)
                    continue
                layers = family.arr_amt[target][rank, sign, port]
                free = [layer for layer in range(LAYERS) if layers[layer] == 0]
                if free:
                    layer = free[0]
                    family.arr_amt[target][rank, sign, port, layer] = ray.amount
                    family.arr_ph[target][rank, sign, port, layer] = ray.phase
                else:
                    family.overflow.setdefault(target, []).append(ray)
            self.visited[target] = True

    # -- readouts --------------------------------------------------------------

    def add_totals(self, result: list[list[int]]) -> None:
        """The region's content on the ledger's current line: resident shadows, the
        parked shares' whole quanta, the departures in flight, the returns and the
        shadows waiting, per field, and on the momentum field what the returns and
        the waiting shadows carry (bit-law-v1: a shadow's momentum on the ledger
        is what it carries home)."""
        for family in self.families.values():
            definition = family.definition
            resident = int(family.arr_amt.sum()) + int(family.fly_amt.sum())
            for rays in family.overflow.values():
                resident += sum(ray.amount for ray in rays)
            resident += int(family.ret_amt.sum()) + int(family.wait_amt.sum())
            held = int(family.reg.sum())
            if held % family.total:
                raise ValueError("a Node's parked shadows hold whole quanta in total")
            result[definition.field][0] += resident + held // family.total
            if definition.momentum_field is not None:
                carried = family.ret_mom.astype(np.int64).sum(axis=(0, 1, 2, 3, 4, 5)) + family.wait_mom.astype(
                    np.int64
                ).sum(axis=(0, 1, 2, 3, 4))
                for axis in range(3):
                    result[definition.momentum_field][axis] += int(carried[axis])

    def shadow_counts(self, result: dict[int, list[int]]) -> None:
        """The region's shadows per owner: the rays (array entries with content, the
        whole rays beside them, the returns and the shadows waiting) and their
        amount; a parked share is not a ray of its own."""
        for family in self.families.values():
            for rank, owner in enumerate(family.owners):
                entry = result.setdefault(owner, [0, 0])
                arrived, flying = family.arr_amt[:, :, :, rank], family.fly_amt[:, :, :, rank]
                back, waiting = family.ret_amt[:, :, :, rank], family.wait_amt[:, :, :, rank]
                entry[0] += (
                    int((arrived > 0).sum())
                    + int((flying > 0).sum())
                    + int((back > 0).sum())
                    + int((waiting > 0).sum())
                )
                entry[1] += int(arrived.sum()) + int(flying.sum()) + int(back.sum()) + int(waiting.sum())
            for rays in family.overflow.values():
                for ray in rays:
                    entry = result.setdefault(ray.owner, [0, 0])
                    entry[0] += 1
                    entry[1] += ray.amount

    def materialized_nodes(self, nodes: dict[Address3, SpatialNode]) -> dict[Address3, SpatialNode]:
        """Every Node the region owns and has visited, read as Node state beside the
        engine's own: its resident rays merged in the engine's order (the arrivals,
        the returns, the shadows waiting, the parked shares and the traces), the
        amounts delivered per Port, the Ports it received through and the cost of
        its last cycle; the engine's Nodes as they are."""
        result = dict(nodes)
        for x, y, z in zip(*np.nonzero(self.visited & (self.owner == 0)), strict=True):
            position = (int(x), int(y), int(z))
            base = nodes.get(position)
            node = replace(base) if base is not None else self._fresh(position)
            rays = list(node.rays) or [() for _ in self.initial.spatial_fields]
            states = list(node.states)
            mask = [0] * 6
            for index, family in self.families.items():
                definition = family.definition
                found: list[Ray] = []
                delivered = [0] * 6
                amounts = family.arr_amt[position]
                for rank, sign, port, layer in zip(*np.nonzero(amounts > 0), strict=True):
                    amount = int(amounts[rank, sign, port, layer])
                    found.append(
                        Ray(
                            int(family.heading_index[port]),
                            (0, 0, 0),
                            amount,
                            phase=int(family.arr_ph[position][rank, sign, port, layer]),
                            steps=1,
                            detector=BIT_SHADOW,
                            source_sign=int(sign) - 1,
                            owner=family.owners[int(rank)],
                        )
                    )
                    delivered[int(port)] += amount
                    mask[int(port) ^ 1] = 1
                for ray in family.overflow.get(position, ()):
                    found.append(ray)
                    port = family.port_of[ray.heading]
                    delivered[port] += ray.amount
                    mask[port ^ 1] = 1
                # A return is delivered as no flux, as the engine delivers it.
                for port, back in self._returning_rays(family, position).items():
                    found.extend(back)
                    mask[port ^ 1] = 1
                found.extend(self._waiting_rays(family, position))
                found.extend(
                    park_shares(
                        tuple(int(v) for v in family.reg[position].reshape(-1)),
                        tuple(int(v) for v in family.regph[position].reshape(-1)),
                        definition,
                    )
                )
                for rank, port in zip(*np.nonzero(family.trace[position]), strict=True):
                    found.append(parked_shadow(family.owners[int(rank)], int(port) - 1, definition))
                rays[index] = merge_rays(tuple(found))
                states[index] = replace(
                    states[index], delivered=tuple(pack((amount,)) for amount in delivered)
                )
            node.rays = tuple(rays)
            node.states = tuple(states)
            node.arrival_mask = tuple(mask)
            node.last_cost = int(self.cost[position])
            node.received_count = sum(mask)
            result[position] = node
        return result

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
            detector_ticket=0,
            body=None,
        )

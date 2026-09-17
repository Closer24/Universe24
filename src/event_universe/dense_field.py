"""The dense mode for boards that a field fills (dense-field-v1).

A host scheduling component, not a physical rule: the pure-field Nodes of a
board, those holding nothing but outbound content of spreading families and
their remainder registers, are cycled as one vectorized step over integer
arrays that applies the spatial law's spread and remainder rule
(`core/spatial_state.py`, `spread_content`; [field spreading]
(../../docs/SPATIAL_FIELDS.md#field-spreading-field-spreading-v1)) to every
such Node at once, with the same integers: the content arriving on each
heading is split by the six-weight table relative to that heading into whole
quanta that leave and sub-quantum shares that go to the Node's registers per
source sign and Port, each register's phase combined with the share's by the
coherence rule (`phase_of_sum` over the family's integer cosine and sine
tables, in the order the engine combines them), a register at one quantum
releasing the whole quanta it holds with its phase, the departures walking one
Link with the family's phase advance, the open boundary absorbing what walks
out, per family and sign. The Detector bit travels as the engine carries it
through a spread (the highest bit of the arrivals on every departure).

The region and the engine share the board. A Node is the engine's (sparse)
while it holds a Detector mark, an external body, a record, a ray of another
family, a returning ray, an event-carrying ray or any other content the
vectorized step does not describe; every other Node is the region's (dense).
Ownership is decided at every delivery for the Nodes that receive something:
a ray leaving a dense Node toward a sparse Node is handed over as an ordinary
`SpatialPacket` of merged rays, and a packet leaving a sparse Node into the
dense region is absorbed into the arrays, both exact, the registers moving
with the Node when its ownership changes. The region publishes no per-Node
events: the record of a dense region is its arrays' totals per tick (the
world ledger), and the mode is not for records that need per-Node field
events. Its Nodes read back as Node state for the totals, the snapshot and
the inventory view (`materialized_nodes`), so `state.json` and the ledger are
the acceptance test of the mode (docs/PERFORMANCE.md).

Bounded integers throughout: amounts are below MAX_VALUE, phases below the
family's modulus, products and sums in signed 64-bit registers as the engine's
`checked_work` requires; the arrays are numpy int64 and the bounds are
checked where a value could grow.
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
    POLARIZATION_NONE,
    PORT_HEADINGS,
    REMAINDER_SLOTS,
    Ray,
    Rays,
    SpatialFieldDefinition,
    SpatialPacket,
    blank_remainders,
    merge_rays,
    phase_mask,
    relative_ports,
    spread_tables,
)
from event_universe.core.topology import neighbor_address

if TYPE_CHECKING:
    from event_universe.core.disturbance_node import DisturbanceNode

# The layers of one Port's content from a dense Node: the spread's whole quanta at
# the Node's combined phase and the register's release at the register's phase;
# a sparse Node's packet may carry more phases on one Port and sign, and those
# rays are kept whole beside the arrays (`overflow`).
LAYERS = 2
SIGNS = 3
# The register phase combination is tabulated over (held, held phase, share,
# share phase) when the table fits; a wider phase or table computes it directly.
COMBINE_TABLE_LIMIT = 1 << 24
# The six unit-axial headings in Port order, as an array.
HEADINGS = np.array(PORT_HEADINGS, dtype=np.int64)


class DenseFamily:
    """The arrays of one spreading family on the board.

    `arr_*` hold the content resident at each Node, arrived this interval and due
    to spread: per source sign (-1, 0, 1 as 0, 1, 2), travel Port (the heading the
    content arrived on, the engine's `arrived` index) and layer, the amount, the
    phase and the Detector bit. `reg` and `regph` are the eighteen registers and
    their phases per Node, sign-major then Port, in units of 1/S. `fly_*` hold the
    departures of the last cycle until the delivery walks them one Link."""

    def __init__(
        self, index: int, definition: SpatialFieldDefinition, shape: Address3, prices: dict[str, int]
    ) -> None:
        self.index = index
        self.definition = definition
        self.field = definition.field
        self.table = np.array(definition.spread, dtype=np.int64)
        self.total = int(sum(definition.spread))
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
        self.arr_amt = np.zeros((*shape, SIGNS, 6, LAYERS), dtype=np.int64)
        self.arr_ph = np.zeros((*shape, SIGNS, 6, LAYERS), dtype=np.int64)
        self.arr_bit = np.zeros((*shape, SIGNS, 6, LAYERS), dtype=np.int64)
        self.overflow: dict[Address3, list[Ray]] = {}
        self.reg = np.zeros((*shape, SIGNS, 6), dtype=np.int64)
        self.regph = np.zeros((*shape, SIGNS, 6), dtype=np.int64)
        self.fly_amt = np.zeros((*shape, SIGNS, 6, LAYERS), dtype=np.int64)
        self.fly_ph = np.zeros((*shape, SIGNS, 6, LAYERS), dtype=np.int64)
        self.fly_bit = np.zeros((*shape, SIGNS, 6, LAYERS), dtype=np.int64)
        self.prices = prices

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


def plain_ray(ray: Ray, definition: SpatialFieldDefinition) -> bool:
    """Whether a ray is content the dense region describes: an outbound field ray one
    Link from its departure on a Port heading, without an event, a delay, a wait,
    a lag, a momentum register, an own advance or a polarization."""
    return (
        ray.outbound == 1
        and ray.steps == 1
        and ray.amount > 0
        and ray.event_ports == 0
        and not any(ray.event_shares)
        and ray.advance == -1
        and ray.wait == 0
        and ray.interaction_delay == 0
        and ray.lag == (0, 0, 0)
        and ray.momentum is None
        and ray.polarization == POLARIZATION_NONE
        and ray.accumulators == (0, 0, 0)
        and definition.headings[ray.heading] in PORT_HEADINGS
    )


def plain_node(node: SpatialNode) -> bool:
    """Whether an engine Node holds nothing the region cannot own: no mark, no
    body, no pending cycle, no resident ray, no octant stock, no deposit."""
    return (
        node.detector is None
        and node.body is None
        and node.pending is None
        and not node.shared_pending
        and not node.incoming
        and not any(node.rays)
        and not any(any(unpack(payload)) for state in node.states for payload in state.populations)
        and not any(any(unpack(payload)) for payload in node.localized)
    )


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
        field-remainder-v1): the same integers as `spread_content` at each, the
        departures kept in flight until the delivery, the cost of each cycle as the
        spatial law would meter it, and the momentum the spreads moved booked as
        the family's momentum source."""
        dense = self.owner == 0
        prices = self.prices
        ports_any = np.zeros((*self.shape, 6), dtype=bool)
        has_registers = np.zeros(self.shape, dtype=bool)
        family_cost = np.zeros(self.shape, dtype=np.int64)
        has_arrivals = np.zeros(self.shape, dtype=bool)
        for family in self.families.values():
            arrived, coherent_x, coherent_y, bit, count, family_ports = self._arrivals(family)
            ports_any |= family_ports
            registers = (family.reg > 0).any(axis=(3, 4))
            has_registers |= registers
            present = count > 0
            has_arrivals |= present
            if not present.any():
                continue
            phase = self._combined_phase(family, coherent_x, coherent_y)
            departures, released_phase, released = self._split(family, arrived, phase)
            layer_0, layer_1, phase_1 = self._departures(
                family, departures, released, phase, released_phase
            )
            self._place_departures(family, layer_0, layer_1, phase, phase_1, bit)
            self._book_momentum(family, arrived, layer_0 + layer_1, dense & present)
            outgoing = (layer_0 > 0) | (layer_1 > 0)
            departing = (layer_0 > 0).sum(axis=(3, 4)) + (layer_1 > 0).sum(axis=(3, 4))
            sending = outgoing.any(axis=3).sum(axis=3)
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
            family.arr_bit[...] = 0
            family.overflow.clear()
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

    def _arrivals(
        self, family: DenseFamily
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """What arrived at every Node this interval: the amount per sign and travel
        Port, the coherent sum's components, the highest Detector bit, the number of
        rays and the Ports with content, the whole rays beside the arrays included."""
        amounts, phases, bits = family.arr_amt, family.arr_ph, family.arr_bit
        cosines, sines = family.cosines, family.sines
        arrived = amounts.sum(axis=5)
        present = amounts > 0
        if cosines is not None and sines is not None:
            coherent_x = (amounts * cosines[phases]).sum(axis=(3, 4, 5))
            coherent_y = (amounts * sines[phases]).sum(axis=(3, 4, 5))
        else:
            coherent_x = coherent_y = np.zeros(self.shape, dtype=np.int64)
        bit = bits.max(axis=(3, 4, 5))
        count = present.sum(axis=(3, 4, 5)).astype(np.int64)
        ports = present.any(axis=(3, 5))
        for position, rays in family.overflow.items():
            for ray in rays:
                port = family.port_of[ray.heading]
                sign = ray.source_sign + 1
                arrived[position][sign, port] += ray.amount
                if cosines is not None and sines is not None:
                    coherent_x[position] += ray.amount * int(cosines[ray.phase & family.mask])
                    coherent_y[position] += ray.amount * int(sines[ray.phase & family.mask])
                bit[position] = max(int(bit[position]), ray.detector)
                count[position] += 1
                ports[position][port] = True
        if arrived.max(initial=0) > MAX_VALUE:
            raise ValueError("value exceeds the disturbance integer bound")
        return arrived, coherent_x, coherent_y, bit, count, ports

    def _combined_phase(self, family: DenseFamily, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """The one phase of each Node's content: the step nearest the coherent sum."""
        if family.cosines is None:
            return np.zeros(self.shape, dtype=np.int64)
        if max(abs(int(x.max(initial=0))), abs(int(x.min(initial=0)))) * 256 > MAX_WORK_INT:
            raise OverflowError("64-bit intermediate range exceeded")
        return family._nearest_step(x, y)

    def _split(
        self, family: DenseFamily, arrived: np.ndarray, phase: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """The split of each arriving Port's content by the table relative to its
        heading, in the engine's order (Port by Port): the whole quanta per absolute
        target Port and sign, the shares into the registers with their phases
        combined, then every register at S or more releasing its whole quanta with
        its phase and resetting its phase when it empties."""
        S = family.total
        reg, regph = family.reg, family.regph
        departures = np.zeros((*self.shape, SIGNS, 6), dtype=np.int64)
        phase_b = phase[..., None, None]
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
        """The two layers per sign and Port: the spread's quanta at the combined
        phase and the register's release at its phase, one ray when the phases
        are equal (the departures of one Port merge)."""
        phase_b = phase[..., None, None]
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
        bit: np.ndarray,
    ) -> None:
        if max(int(layer_0.max(initial=0)), int(layer_1.max(initial=0))) > MAX_VALUE:
            raise ValueError("value exceeds the disturbance integer bound")
        phase_b = phase[..., None, None]
        bit_b = bit[..., None, None]
        family.fly_amt[..., 0] = layer_0
        family.fly_ph[..., 0] = np.where(layer_0 > 0, phase_b, 0)
        family.fly_bit[..., 0] = np.where(layer_0 > 0, bit_b, 0)
        family.fly_amt[..., 1] = layer_1
        family.fly_ph[..., 1] = np.where(layer_1 > 0, phase_1, 0)
        family.fly_bit[..., 1] = np.where(layer_1 > 0, bit_b, 0)

    def _book_momentum(
        self, family: DenseFamily, arrived: np.ndarray, departed: np.ndarray, where: np.ndarray
    ) -> None:
        """The momentum a spread moves, amount x heading over the departures less the
        same over the arrivals, booked as the family's momentum source when one is
        bound, as the spatial law books it (Highlights 3.15)."""
        momentum_field = family.definition.momentum_field
        if momentum_field is None:
            return
        out_ports = np.where(where[..., None], departed.sum(axis=3), 0)
        in_ports = np.where(where[..., None], arrived.sum(axis=3), 0)
        delta = (out_ports - in_ports).sum(axis=(0, 1, 2))
        for axis in range(3):
            value = int((delta * HEADINGS[:, axis]).sum())
            self.engine.sources[momentum_field][axis] += value

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
        engine_incoming = self._engine_receivers(incoming)
        candidates = set(ready) | engine_incoming
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
            amounts, phases, bits = incoming[index]
            family.arr_amt += amounts
            family.arr_ph += phases
            family.arr_bit += bits
            present = (family.arr_amt > 0).any(axis=(3, 4, 5))
            self.visited |= present
            count = (family.arr_amt > 0).sum(axis=(3, 4, 5))
            for position, rays in family.overflow.items():
                count[position] += len(rays)
            if count.max(initial=0) > family.definition.ray_slots:
                raise ValueError("ray slot budget exceeded")
        for target, packets in handed.items():
            ready.setdefault(target, []).extend(packets)
        return ready, absorbed

    def _walk(self, family: DenseFamily) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """The departures one Link on: what arrives at each Node per sign, travel Port
        and layer, the phase advanced by the family's rate; what leaves an open
        board is counted as escaped, per family and sign, with its charge and its
        momentum."""
        amounts = np.zeros_like(family.fly_amt)
        phases = np.zeros_like(family.fly_ph)
        bits = np.zeros_like(family.fly_bit)
        definition = family.definition
        for port in range(6):
            source = family.fly_amt[..., port, :]
            if not source.any():
                continue
            axis, forward = port >> 1, (port & 1) == 0
            moved_amount = np.zeros_like(source)
            moved_phase = np.zeros_like(source)
            moved_bit = np.zeros_like(source)
            source_phase = family.fly_ph[..., port, :]
            source_bit = family.fly_bit[..., port, :]
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
                moved_bit[tuple(ahead)] = source_bit[tuple(behind)]
                escaped = int(source[tuple(edge)].sum())
                if escaped:
                    self.engine.escaped[definition.field][0] += escaped
                    self.engine.escaped_charge[family.index] += escaped * definition.charge
                    if definition.momentum_field is not None:
                        for component in range(3):
                            self.engine.escaped[definition.momentum_field][component] += escaped * int(
                                HEADINGS[port, component]
                            )
            else:
                shift = 1 if forward else -1
                moved_amount = np.roll(source, shift, axis=axis)
                moved_phase = np.roll(source_phase, shift, axis=axis)
                moved_bit = np.roll(source_bit, shift, axis=axis)
            if family.mask:
                moved_phase = np.where(moved_amount > 0, (moved_phase + family.advance) & family.mask, 0)
            amounts[..., port, :] = moved_amount
            phases[..., port, :] = moved_phase
            bits[..., port, :] = moved_bit
        family.fly_amt[...] = 0
        family.fly_ph[...] = 0
        family.fly_bit[...] = 0
        return amounts, phases, bits

    def _engine_receivers(
        self, incoming: dict[int, tuple[np.ndarray, np.ndarray, np.ndarray]]
    ) -> set[Address3]:
        return {position for position in self.engine_positions if self._receives(incoming, position)}

    @staticmethod
    def _receives(
        incoming: dict[int, tuple[np.ndarray, np.ndarray, np.ndarray]], position: Address3
    ) -> bool:
        return any(bool(amounts[position].any()) for amounts, _, _ in incoming.values())

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
        if node is not None and not plain_node(node):
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
                if family is None or any(not plain_ray(ray, family.definition) for ray in rays):
                    return True
                if any(int(family.heading_index[packet.port]) != ray.heading for ray in rays):
                    return True
        return False

    def _to_engine(self, target: Address3) -> None:
        """The Node becomes the engine's: its registers move to the Node state."""
        node = self.engine._at(target)
        remainders, phases = list(node.remainders), list(node.remainder_phases)
        for index, family in self.families.items():
            remainders[index] = tuple(int(v) for v in family.reg[target].reshape(-1))
            phases[index] = tuple(int(v) for v in family.regph[target].reshape(-1))
            family.reg[target] = 0
            family.regph[target] = 0
        node.remainders, node.remainder_phases = tuple(remainders), tuple(phases)
        node.last_cost = int(self.cost[target])
        self.owner[target] = 1
        self.visited[target] = True
        self.engine_positions.add(target)

    def _to_dense(self, target: Address3) -> None:
        """The Node becomes the region's: its registers move into the arrays."""
        node = self.engine.nodes[target]
        for index, family in self.families.items():
            block = node.remainders[index] if index < len(node.remainders) else ()
            block_phases = node.remainder_phases[index] if index < len(node.remainder_phases) else ()
            family.reg[target] = np.array(block or (0,) * REMAINDER_SLOTS, dtype=np.int64).reshape(
                SIGNS, 6
            )
            family.regph[target] = np.array(
                block_phases or (0,) * REMAINDER_SLOTS, dtype=np.int64
            ).reshape(SIGNS, 6)
        node.remainders = blank_remainders(self.initial.spatial_fields)
        node.remainder_phases = blank_remainders(self.initial.spatial_fields)
        self.cost[target] = node.last_cost
        self.owner[target] = 0
        self.visited[target] = True
        self.engine_positions.discard(target)

    def _hand_over(
        self, tick: int, incoming: dict[int, tuple[np.ndarray, np.ndarray, np.ndarray]]
    ) -> dict[Address3, list[SpatialPacket]]:
        """The region's departures that reach the engine's Nodes, as packets: one per
        origin and Port, its rays merged and ordered as `forward_rays` orders them,
        and taken out of the arrays."""
        bundles: dict[tuple[Address3, int], list[Rays]] = {}
        engine_mask = self.owner == 1
        for index, family in self.families.items():
            amounts, phases, bits = incoming[index]
            hits = np.nonzero(engine_mask[..., None, None, None] & (amounts > 0))
            if not hits[0].size:
                continue
            rays_at: dict[tuple[Address3, int], list[Ray]] = {}
            for x, y, z, sign, port, layer in zip(*hits, strict=True):
                target = (int(x), int(y), int(z))
                key = (target, int(port))
                rays_at.setdefault(key, []).append(
                    Ray(
                        int(family.heading_index[port]),
                        (0, 0, 0),
                        int(amounts[x, y, z, sign, port, layer]),
                        phase=int(phases[x, y, z, sign, port, layer]),
                        steps=1,
                        detector=int(bits[x, y, z, sign, port, layer]),
                        source_sign=int(sign) - 1,
                    )
                )
            amounts[hits] = 0
            phases[hits] = 0
            bits[hits] = 0
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
        """An engine packet arriving at a dense Node: its rays into the arrays, layer
        by layer per sign and Port, the rest kept whole beside them."""
        for index, rays in enumerate(packet.rays):
            if not rays:
                continue
            family = self.families[index]
            for ray in rays:
                sign = ray.source_sign + 1
                port = packet.port
                layers = family.arr_amt[target][sign, port]
                free = [layer for layer in range(LAYERS) if layers[layer] == 0]
                if free:
                    layer = free[0]
                    family.arr_amt[target][sign, port, layer] = ray.amount
                    family.arr_ph[target][sign, port, layer] = ray.phase
                    family.arr_bit[target][sign, port, layer] = ray.detector
                else:
                    family.overflow.setdefault(target, []).append(ray)
            self.visited[target] = True

    # -- readouts --------------------------------------------------------------

    def add_totals(self, result: list[list[int]]) -> None:
        """The region's content on the ledger's current line: resident rays, the
        registers' whole quanta and the departures in flight, per field, with the
        momentum of the rays when a momentum field is bound."""
        for family in self.families.values():
            definition = family.definition
            resident = int(family.arr_amt.sum()) + int(family.fly_amt.sum())
            for rays in family.overflow.values():
                resident += sum(ray.amount for ray in rays)
            held = int(family.reg.sum())
            if held % family.total:
                raise ValueError("a Node's remainder registers hold whole quanta in total")
            result[definition.field][0] += resident + held // family.total
            if definition.momentum_field is not None:
                per_port = family.arr_amt.sum(axis=(0, 1, 2, 3, 5)) + family.fly_amt.sum(
                    axis=(0, 1, 2, 3, 5)
                )
                for rays in family.overflow.values():
                    for ray in rays:
                        per_port[family.port_of[ray.heading]] += ray.amount
                for axis in range(3):
                    result[definition.momentum_field][axis] += int((per_port * HEADINGS[:, axis]).sum())

    def add_charge_totals(self, result: dict[str, int]) -> None:
        for family in self.families.values():
            definition = family.definition
            if not definition.charge:
                continue
            resident = int(family.arr_amt.sum()) + int(family.fly_amt.sum())
            for rays in family.overflow.values():
                resident += sum(ray.amount for ray in rays)
            held = int(family.reg.sum()) // family.total
            name = self.initial.fields[definition.field].name
            result[name] += (resident + held) * definition.charge

    def materialized_nodes(self, nodes: dict[Address3, SpatialNode]) -> dict[Address3, SpatialNode]:
        """Every Node the region owns and has visited, read as Node state beside the
        engine's own: its resident rays merged in the engine's order, its registers,
        the amounts delivered per Port, the Ports it received through and the cost
        of its last cycle; the engine's Nodes as they are."""
        result = dict(nodes)
        for x, y, z in zip(*np.nonzero(self.visited & (self.owner == 0)), strict=True):
            position = (int(x), int(y), int(z))
            base = nodes.get(position)
            node = replace(base) if base is not None else self._fresh(position)
            rays = list(node.rays) or [() for _ in self.initial.spatial_fields]
            remainders, phases = list(node.remainders), list(node.remainder_phases)
            states = list(node.states)
            mask = [0] * 6
            for index, family in self.families.items():
                found: list[Ray] = []
                delivered = [0] * 6
                amounts = family.arr_amt[position]
                for sign, port, layer in zip(*np.nonzero(amounts > 0), strict=True):
                    amount = int(amounts[sign, port, layer])
                    found.append(
                        Ray(
                            int(family.heading_index[port]),
                            (0, 0, 0),
                            amount,
                            phase=int(family.arr_ph[position][sign, port, layer]),
                            steps=1,
                            detector=int(family.arr_bit[position][sign, port, layer]),
                            source_sign=int(sign) - 1,
                        )
                    )
                    delivered[int(port)] += amount
                    mask[int(port) ^ 1] = 1
                for ray in family.overflow.get(position, ()):
                    found.append(ray)
                    port = family.port_of[ray.heading]
                    delivered[port] += ray.amount
                    mask[port ^ 1] = 1
                rays[index] = merge_rays(tuple(found))
                remainders[index] = tuple(int(v) for v in family.reg[position].reshape(-1))
                phases[index] = tuple(int(v) for v in family.regph[position].reshape(-1))
                states[index] = replace(
                    states[index], delivered=tuple(pack((amount,)) for amount in delivered)
                )
            node.rays = tuple(rays)
            node.remainders, node.remainder_phases = tuple(remainders), tuple(phases)
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
            remainders=blank_remainders(self.initial.spatial_fields),
            remainder_phases=blank_remainders(self.initial.spatial_fields),
        )

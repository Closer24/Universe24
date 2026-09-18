"""Fixed-clock ownership for configured spatial fields, separate from carriers."""

from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import replace
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .disturbance_node import DisturbanceNode

from .coupling_selectors import selected_type_set
from .disturbance_state import (
    Address3,
    CostMeter,
    DisturbanceRecord,
    InitialState,
    Payload,
    Values,
    pack,
    unpack,
)
from .integer import checked_work
from .node_boundary import validate_spatial_bundle
from .node_conservation import NodeConservationGuard
from .node_execution import NodeExecution
from .node_ports import PortTable
from .node_services import NodeEvents
from .spatial_node import NodeActivity, SpatialAccounting, SpatialNode, SpatialServices
from .spatial_node import ReactionCommit as ReactionCommit
from .spatial_node import SpatialCoupler as SpatialCoupler
from .spatial_node import SpatialFieldGuard as SpatialFieldGuard
from .spatial_state import (
    BIT_SHADOW,
    BIT_THING,
    ExternalBody,
    Rays,
    SpatialBundle,
    SpatialFieldDefinition,
    SpatialPacket,
    SpatialPlan,
    SpatialState,
    coherent_stock,
    held_stock,
    parked_momentum,
    parked_stock,
    parked_unit,
    ray_charge,
    ray_momentum,
    ray_momentum_vector,
    ray_stock,
    validate_rays,
)
from .topology import neighbor_address

SpatialPlanner = Callable[
    [
        tuple[SpatialState, ...],
        tuple[DisturbanceRecord | None, ...],
        int,
        int,
        tuple[Rays, ...],
        int,
        int,
    ],
    SpatialPlan,
]
SpatialDecayer = Callable[[SpatialBundle], tuple[SpatialBundle, Values, int]]
EventSink = Callable[[dict[str, object]], None]
RecordCommit = Callable[[Address3, tuple[DisturbanceRecord | None, ...]], None]


class DenseRegion(Protocol):
    """The dense mode's owner of a board's pure-field Nodes (dense-field-v1), a host
    scheduling component composed outside the core (`event_universe.dense_field`):
    it cycles the Nodes it owns as one step, takes over the packets addressed to
    them, hands the engine the packets its Nodes send to the engine's Nodes, and
    reads back as Node state for the totals and the snapshot. The physics is the
    spatial law's; the engine only schedules around it."""

    def cycle(self, tick: int) -> None: ...

    def deliver(
        self,
        tick: int,
        ready: dict[Address3, list[SpatialPacket]],
        residents: Mapping[Address3, DisturbanceNode] | None,
    ) -> tuple[dict[Address3, list[SpatialPacket]], list[SpatialPacket]]: ...

    def add_totals(self, result: list[list[int]]) -> None: ...

    def shadow_counts(self, result: dict[int, list[int]]) -> None: ...

    def materialized_nodes(self, nodes: dict[Address3, SpatialNode]) -> dict[Address3, SpatialNode]: ...

    def materialized_node(self, position: Address3, base: SpatialNode | None) -> SpatialNode: ...

    def visited_slab(self, x: int) -> list[Address3]: ...

    def active_count(self) -> int: ...

    def claim(self, position: Address3) -> None: ...

    def standing_report(self) -> dict[str, object] | None: ...


class SpatialEngine:
    @property
    def observer(self) -> EventSink | None:
        return self._event_observer

    @observer.setter
    def observer(self, observer: EventSink | None) -> None:
        self._event_observer = observer
        if hasattr(self, "_services"):
            self._services.events.set_observer(observer)

    def __init__(
        self,
        initial: InitialState,
        planner: SpatialPlanner,
        observer: EventSink | None,
        coupler: SpatialCoupler | None = None,
        decayer: SpatialDecayer | None = None,
        *,
        balance_guard: NodeConservationGuard | None = None,
        field_guard: SpatialFieldGuard | None = None,
        execution_planner: SpatialPlanner | None = None,
        planner_validates: bool = False,
    ) -> None:
        if initial.node_execution and (initial.conservation_contract is None or balance_guard is None):
            raise ValueError("node_execution requires a conservation contract and balance guard")
        if initial.node_execution and initial.field_rules and field_guard is None:
            raise ValueError("node_execution field rules require a field commit guard")
        if planner_validates and execution_planner is None:
            raise ValueError("a validating planner is the execution's, not the law itself")
        self.initial = initial
        self.planner = planner
        self.observer = observer
        self.coupler = coupler
        self.decayer = decayer
        self.nodes: dict[Address3, SpatialNode] = {}
        # The Detector marks by position, installed on each marked Node when it is
        # created; a Node without a mark never draws.
        self._marks = {mark.position: mark for mark in initial.detectors}
        # The external bodies by declared position, installed on their Nodes when
        # they are created; a body that steps carries its mark to the next Node.
        self._bodies = {body.position: body for body in initial.external_bodies}
        # Host scheduling index only: the physical state is in self.nodes.
        self._active: set[Address3] = set()
        # The totals once per tick (node-is-ports-v1, the performance review):
        # memoized per bit and cleared by every step of the engine that moves
        # content (begin, deliver, close, the prefill).
        self._totals_memo: dict[int | None, list[list[int]]] = {}
        # The dense mode's region (dense-field-v1), attached by the composition
        # when the world declares `dense_field`; None cycles every Node here.
        self.dense: DenseRegion | None = None
        self._field_tick = -1
        self.links: PortTable[SpatialPacket] = PortTable((None,) * 6)
        self.sources = [[0] * field.components for field in initial.fields]
        self.dissipation = [[0] * field.components for field in initial.fields]
        self.localized = [[0] * field.components for field in initial.fields]
        self.reactions = [[0] * field.components for field in initial.fields]
        self.transformations = [[0] * field.components for field in initial.fields]
        self.escaped = [[0] * field.components for field in initial.fields]
        # The charge that left the world through an open boundary, per spatial
        # field: charge x amount of every escaped ray (ray-event-audit-v1).
        self.escaped_charge = [0] * len(initial.spatial_fields)
        # Content that ended in an external body's sink (external-body-v1).
        self.absorbed = [[0] * field.components for field in initial.fields]
        # Content a Detector mark absorbed on a click (detector-absorb-v1), with the
        # momentum field's components when one is bound.
        self.absorbed_by_marks = [[0] * field.components for field in initial.fields]
        # What came home (bit-law-v1): the shadows absorbed back into their things
        # and the momentum delivered outside the identity; the re-releases, on the
        # source line and here; and the shadows that escaped, on the escaped line
        # and here, so that the things' own identity reads both lines less these.
        self.returned = [[0] * field.components for field in initial.fields]
        # The momentum the things spent on their steps (clock-readings-v1, the
        # settled rule (i)), and their phase steps, the computation (point 11), a
        # running total.
        self.spent = [[0] * field.components for field in initial.fields]
        self.computation = [0]
        self.shadow_sources = [[0] * field.components for field in initial.fields]
        self.shadow_escaped = [[0] * field.components for field in initial.fields]
        self.shadow_absorbed_by_marks = [[0] * field.components for field in initial.fields]
        meter = CostMeter(initial.operation_costs)
        if initial.spatial_computation_delay:
            components = 8 * sum(initial.fields[d.field].components for d in initial.spatial_fields)
            meter.charge("read", 2 * components)
            meter.charge("evaluate", components)
            meter.charge("update", components)
        self._services = SpatialServices(
            replace(initial, seeds=(), spatial_seeds=()),
            planner if execution_planner is None else execution_planner,
            NodeEvents(observer),
            coupler,
            decayer,
            NodeActivity(self._active),
            SpatialAccounting(
                self.sources,
                self.dissipation,
                self.reactions,
                self.transformations,
                self.localized,
                self.absorbed,
                self.absorbed_by_marks,
                self.returned,
                self.shadow_sources,
                self.shadow_absorbed_by_marks,
                self.spent,
                self.computation,
            ),
            balance_guard,
            field_guard,
            meter.total,
            planner_validates,
        )
        for seed in initial.spatial_seeds:
            node = self._at(seed.position)
            states = list(node.states)
            states[seed.spatial_field] = replace(
                states[seed.spatial_field], populations=seed.populations
            )
            node.states = tuple(states)
            self.values(seed.position)
        for body in initial.external_bodies:
            # A body's Node exists and is active from the start.
            self._at(body.position)
        self._initial_totals = self.totals()

    def refresh_initial_totals(self) -> None:
        """Read the initial line again after the field given with the board was
        installed (bit-law-v1, `initial_field`): the prefill is the things'
        presence, booked as initial, not a source."""
        self.invalidate_totals()
        self._initial_totals = self.totals()

    def invalidate_totals(self) -> None:
        """Forget the memoized totals: the engine's content moved."""
        self._totals_memo.clear()

    def _blank_states(self) -> tuple[SpatialState, ...]:
        result = []
        for definition in self.initial.spatial_fields:
            zero = pack((0,) * self.initial.fields[definition.field].components)
            result.append(SpatialState((zero,) * 8, (zero,) * 8, (zero,) * 6))
        return tuple(result)

    def _blank_localized(self) -> tuple[Payload, ...]:
        return tuple(
            pack((0,) * self.initial.fields[definition.field].components)
            for definition in self.initial.spatial_fields
        )

    def _at(self, position: Address3) -> SpatialNode:
        if position not in self.nodes:
            mark = self._marks.get(position)
            self.nodes[position] = SpatialNode(
                self._blank_states(),
                position=position,
                output=self.links.bank(position),
                arrival_mask=(0,) * 6,
                delay_counts=(0,) * 6,
                localized=self._blank_localized(),
                rays=tuple(() for _ in self.initial.spatial_fields),
                detector=mark,
                # The Node's counter (bit-law-v1, point 14): every Node's starts at 0.
                detector_ticket=0,
                body=self._bodies.pop(position, None),
            )
            self._active.add(position)
        elif position not in self._active:
            # An idle known node completed the empty phase without a host visit.
            # New nodes stay active, so this cannot backdate their creation.
            self.nodes[position].last_begin_tick = self._field_tick
        return self.nodes[position]

    def _validate_packet_rays(self, rays: tuple[Rays, ...]) -> None:
        if not rays:
            return
        if len(rays) != len(self.initial.spatial_fields):
            raise ValueError("spatial packet ray count differs from its definitions")
        for definition, field_rays in zip(self.initial.spatial_fields, rays, strict=True):
            if field_rays:
                validate_rays(field_rays, definition, self.initial.fields[definition.field])

    def _neighbor(self, position: Address3, port: int) -> Address3 | None:
        return neighbor_address(position, port, self.initial.shape, self.initial.boundary)

    def _event(
        self,
        event: str,
        tick: int,
        position: Address3,
        *,
        notifications: list[dict[str, object]] | None = None,
        **details: object,
    ) -> None:
        if self.observer is not None:
            data = {"event": event, "tick": tick, "position": position, **details}
            if notifications is None:
                self.observer(data)
            else:
                notifications.append(data)

    def _notify(self, notifications: list[dict[str, object]]) -> None:
        if self.observer is not None:
            for event in notifications:
                self.observer(event)

    def begin(
        self,
        tick: int,
        residents: Mapping[Address3, DisturbanceNode],
        *,
        execution: NodeExecution | None = None,
    ) -> None:
        if tick % self.initial.link_ticks:
            return
        self.invalidate_totals()
        self._field_tick = tick
        emitter_types = selected_type_set(self.initial.emissions)
        coupled_types = selected_type_set(
            self.initial.spatial_couplings, self.initial.spatial_interactions
        )
        positions = set(self._active)
        for position, carrier in residents.items():
            records = carrier.records
            if any(
                record is not None and record.type_index in emitter_types | coupled_types
                for record in records
            ):
                positions.add(position)
        ordered = tuple(sorted(positions))
        if execution is not None and execution.parallel:
            try:
                execution.finish_cycles(
                    tuple(
                        self._at(position).plan_cycle(tick, residents.get(position), self._services)
                        for position in ordered
                    )
                )
            finally:
                for position in ordered:
                    self.links.refresh(position)
        else:
            for position in ordered:
                try:
                    self._at(position).advance(tick, residents.get(position), self._services)
                finally:
                    self.links.refresh(position)
        if self.dense is not None:
            # The pure-field Nodes, as one step (dense-field-v1); their departures
            # cross to the engine's Nodes at the delivery, as packets.
            self.dense.cycle(tick)

    @contextmanager
    def materialized(self) -> Iterator[None]:
        """Read the dense region's Nodes as Node state (dense-field-v1): within the
        block `nodes` also holds the Nodes the region owns, each with its resident
        and parked rays, arrivals and cost, so a snapshot or an inventory view
        reads every Node the same way; the engine's own Nodes are untouched."""
        if self.dense is None:
            yield
            return
        saved = self.nodes
        self.nodes = self.dense.materialized_nodes(saved)
        try:
            yield
        finally:
            self.nodes = saved

    def _clear_link(self, packet: SpatialPacket) -> None:
        """Take one delivered packet off its Link; a packet the dense region handed
        over never lay on a Link and is left alone."""
        try:
            links = list(self.links[packet.origin])
        except KeyError:
            return
        if links[packet.port] is packet:
            links[packet.port] = None
            self.links[packet.origin] = tuple(links)

    def _escape(self, packet: SpatialPacket, tick: int) -> None:
        """No receiving node exists outside; terminal stock escapes without exterior decay.

        A returning thing never reaches the boundary before its event Node, which
        its steps bound; one that would escape has no event Node in the world, and
        the engine fails closed instead of recording an escape (detector-return-v1).
        A shadow walking home has no event Node: it follows the traces until
        something takes it, and escapes like any ray otherwise (bit-law-v1, the
        amendment's point d: escapes are the only loss). A packet of shadows alone
        leaves no record: events happen at Nodes that hold a thing (point 13).
        """
        for rays in packet.rays or ():
            if any(not ray.outbound and ray.detector == BIT_THING for ray in rays):
                raise ValueError("a returning ray cannot escape: its event Node is not in the world")
        if packet.body is not None:
            raise ValueError("an external body cannot leave the world: its Node must exist")
        amounts = [[0] * field.components for field in self.initial.fields]
        for definition, populations in zip(self.initial.spatial_fields, packet.fields, strict=True):
            if len(populations) != 8:
                raise ValueError("a terminal spatial packet requires eight octants")
            field = self.initial.fields[definition.field]
            for payload in populations:
                field.validate(payload)
                for component, value in enumerate(unpack(payload)):
                    amounts[definition.field][component] = checked_work(
                        amounts[definition.field][component] + value
                    )
        witnessed = any(any(amounts[i]) for i in range(len(amounts)))
        for index, rays in enumerate(packet.rays):
            if rays:
                definition = self.initial.spatial_fields[index]
                amounts[definition.field][0] = checked_work(
                    amounts[definition.field][0] + ray_stock(rays)
                )
                self.escaped_charge[index] = checked_work(
                    self.escaped_charge[index] + ray_charge(rays, definition)
                )
                if definition.momentum_field is not None:
                    for axis, value in enumerate(ray_momentum(rays, definition)):
                        amounts[definition.momentum_field][axis] = checked_work(
                            amounts[definition.momentum_field][axis] + value
                        )
                shadows = tuple(ray for ray in rays if ray.detector == BIT_SHADOW)
                if shadows:
                    self.shadow_escaped[definition.field][0] = checked_work(
                        self.shadow_escaped[definition.field][0] + ray_stock(shadows)
                    )
                    if definition.momentum_field is not None:
                        for axis, value in enumerate(ray_momentum(shadows, definition)):
                            self.shadow_escaped[definition.momentum_field][axis] = checked_work(
                                self.shadow_escaped[definition.momentum_field][axis] + value
                            )
                if any(ray.detector == BIT_THING for ray in rays):
                    witnessed = True
        for index, values in enumerate(amounts):
            for component, value in enumerate(values):
                self.escaped[index][component] += value
        links = list(self.links[packet.origin])
        links[packet.port] = None
        self.links[packet.origin] = tuple(links)
        escaped = {
            field.name: tuple(amounts[i])
            for i, field in enumerate(self.initial.fields)
            if any(amounts[i])
        }
        if witnessed:
            self._event("spatial_escaped", tick, packet.origin, port=packet.port, escaped=escaped)

    def deliver(self, tick: int, residents: Mapping[Address3, DisturbanceNode] | None = None) -> None:
        self.invalidate_totals()
        ready: dict[Address3, list[SpatialPacket]] = {}
        for origin, packets in self.links.active_items():
            for port, packet in enumerate(packets):
                if packet is not None and packet.arrival_tick == tick:
                    if packet.origin != origin or packet.port != port:
                        raise ValueError("spatial packet provenance differs from its link owner")
                    validate_spatial_bundle(self.initial, packet.fields)
                    self._validate_packet_rays(packet.rays)
                    target = self._neighbor(packet.origin, packet.port)
                    if target is None:
                        self._escape(packet, tick)
                    else:
                        ready.setdefault(target, []).append(packet)
        if self.dense is not None:
            # The region takes the packets addressed to its Nodes and hands over
            # what its Nodes send to the engine's (dense-field-v1).
            ready, absorbed = self.dense.deliver(tick, ready, residents)
            for packet in absorbed:
                self._clear_link(packet)
        for position, arrivals in sorted(ready.items()):
            notifications = self._at(position).receive(
                tuple(arrivals),
                tick,
                self._services,
                carrier=None if residents is None else residents.get(position),
            )
            for packet in arrivals:
                self._clear_link(packet)
            self._notify(notifications)

    def freeze_samples(self, residents: Mapping[Address3, DisturbanceNode]) -> None:
        """Freeze coupled samples after this interval's field phase has delivered."""
        if self.coupler is None:
            return
        coupled_types = selected_type_set(
            self.initial.spatial_couplings, self.initial.spatial_interactions
        )
        for position, carrier in residents.items():
            if any(r is not None and r.type_index in coupled_types for r in carrier.records):
                self._at(position).freeze_sample(self._services)

    def close(self, tick: int, residents: Mapping[Address3, DisturbanceNode]) -> None:
        """Deliver a closing clock notice only to the active local field owners."""
        self.invalidate_totals()
        if self.initial.node_execution:
            for position in sorted(self._active):
                try:
                    self.nodes[position].commit_ready(tick, residents.get(position), self._services)
                finally:
                    self.links.refresh(position)

    def totals(self, bit: int | None = None) -> list[list[int]]:
        """The content the engine holds, per field; with `bit` (bit-law-v1) the
        things' share alone (BIT_THING: the octant stock, the deposits, the
        resident and travelling things, a polarizer's held quanta) or the
        shadows' alone (BIT_SHADOW: the shadows resident, parked and travelling,
        the dense region). Computed once per tick per bit (node-is-ports-v1): the
        memo is cleared whenever the engine moves content."""
        memo = self._totals_memo.get(bit)
        if memo is not None:
            return [list(line) for line in memo]
        result = self._totals(bit)
        self._totals_memo[bit] = [list(line) for line in result]
        return result

    def _totals(self, bit: int | None) -> list[list[int]]:
        result = [[0] * field.components for field in self.initial.fields]
        volume = self.initial.shape[0] * self.initial.shape[1] * self.initial.shape[2]
        things = bit != BIT_SHADOW
        shadows = bit != BIT_THING

        def taken(rays: Rays) -> Rays:
            # A parked shadow is counted by `parked_stock`, in its own unit.
            if bit is None:
                return tuple(ray for ray in rays if not ray.parked)
            return tuple(ray for ray in rays if ray.detector == bit and not ray.parked)

        def parked(index: int, definition: SpatialFieldDefinition) -> None:
            # The parked shadows hold whole quanta in total per Node
            # (field-remainder-v1), in units of the family's split denominator.
            if not definition.spread:
                return
            for position in self._active:
                node = self.nodes[position]
                if node.rays and any(ray.parked for ray in node.rays[index]):
                    result[definition.field][0] += parked_stock(node.rays[index], definition)
                    if definition.momentum_field is not None:
                        # The momentum the parked shares hold in flight (return-field-v1).
                        for axis, value in enumerate(parked_momentum(node.rays[index])):
                            result[definition.momentum_field][axis] += value

        for index, definition in enumerate(self.initial.spatial_fields):
            if not things:
                # The octant stock, the deposits and the baseline are things.
                parked(index, definition)
                if definition.rays:
                    for position in self._active:
                        node = self.nodes[position]
                        if node.rays:
                            rays = taken(node.rays[index])
                            result[definition.field][0] += ray_stock(rays)
                            if definition.momentum_field is not None:
                                for axis, value in enumerate(ray_momentum(rays, definition)):
                                    result[definition.momentum_field][axis] += value
                    for packets in self.links.values():
                        for packet in packets:
                            if packet is not None and packet.rays:
                                rays = taken(packet.rays[index])
                                result[definition.field][0] += ray_stock(rays)
                                if definition.momentum_field is not None:
                                    for axis, value in enumerate(ray_momentum(rays, definition)):
                                        result[definition.momentum_field][axis] += value
                continue
            for component, value in enumerate(unpack(definition.baseline)):
                result[definition.field][component] += volume * value
            inventories = [self.nodes[position].states[index].populations for position in self._active]
            inventories.extend(
                self.nodes[position].incoming[index].populations
                for position in self._active
                if self.nodes[position].incoming
            )
            inventories.extend(
                packet.fields[index]
                for packets in self.links.values()
                for packet in packets
                if packet is not None
            )
            for populations in inventories:
                for payload in populations:
                    for component, value in enumerate(unpack(payload)):
                        result[definition.field][component] += value
            # Deposits are owned stock at idle or active Nodes; the ledger sums them
            # without enumerating idle history.
            for component, value in enumerate(self.localized[definition.field]):
                result[definition.field][component] += value
            if shadows:
                parked(index, definition)
            if definition.rays:
                # A polarizer body's held shares hold whole quanta of the family it
                # polarizes (ray-polarization-v1), content without momentum.
                for body in self._located_bodies():
                    if body.polarizer is not None and body.polarizer.family == index:
                        result[definition.field][0] += held_stock(body)
                # Resident rays keep a Node active, including finite local residence.
                for position in self._active:
                    node = self.nodes[position]
                    if node.rays:
                        rays = taken(node.rays[index])
                        result[definition.field][0] += ray_stock(rays)
                        if definition.momentum_field is not None:
                            for axis, value in enumerate(ray_momentum(rays, definition)):
                                result[definition.momentum_field][axis] += value
                for packets in self.links.values():
                    for packet in packets:
                        if packet is not None and packet.rays:
                            rays = taken(packet.rays[index])
                            result[definition.field][0] += ray_stock(rays)
                            if definition.momentum_field is not None:
                                for axis, value in enumerate(ray_momentum(rays, definition)):
                                    result[definition.momentum_field][axis] += value
        if self.dense is not None and shadows:
            # The content the dense region owns (dense-field-v1): its resident,
            # parked, returning and waiting shadows and what is in flight between
            # its Nodes; shadows all (bit-law-v1).
            self.dense.add_totals(result)
        return result

    def thing_momentum(self) -> dict[int, list[int]]:
        """The momentum of every thing (bit-law-v1, point 15; Highlights 5.4 point
        22): per thing id, the momentum of its rays (what a push set, or amount x
        heading), resident or travelling, and of its body; a push is the field's
        arithmetic on this line, not an event."""
        result: dict[int, list[int]] = {}
        bundles: list[tuple[SpatialFieldDefinition, Rays]] = []
        for position in self._active:
            node = self.nodes[position]
            if node.rays:
                bundles.extend(zip(self.initial.spatial_fields, node.rays, strict=True))
        for packets in self.links.values():
            for packet in packets:
                if packet is not None and packet.rays:
                    bundles.extend(zip(self.initial.spatial_fields, packet.rays, strict=True))
        for definition, rays in bundles:
            for ray in rays:
                if ray.detector == BIT_THING:
                    entry = result.setdefault(ray.owner, [0, 0, 0])
                    for axis, value in enumerate(ray_momentum_vector(ray, definition)):
                        entry[axis] = checked_work(entry[axis] + value)
        for body in self._located_bodies():
            entry = result.setdefault(body.thing, [0, 0, 0])
            for axis in range(3):
                entry[axis] = checked_work(entry[axis] + body.momentum[axis])
        return dict(sorted(result.items()))

    def shadow_counts(self) -> dict[int, list[int]]:
        """The shadows per thing (bit-law-v1, the amendment's point d): for each
        owner the number of shadow rays and their amount, over the resident and
        travelling shadows, the dense region's included; a parked shadow is below
        one quantum, or a trace, and is not counted."""
        result: dict[int, list[int]] = {}
        bundles: list[Rays] = []
        for position in self._active:
            node = self.nodes[position]
            bundles.extend(node.rays)
        for packets in self.links.values():
            for packet in packets:
                if packet is not None and packet.rays:
                    bundles.extend(packet.rays)
        for rays in bundles:
            for ray in rays:
                if ray.detector == BIT_SHADOW and not ray.parked:
                    entry = result.setdefault(ray.owner, [0, 0])
                    entry[0] += 1
                    entry[1] = checked_work(entry[1] + ray.amount)
        if self.dense is not None:
            self.dense.shadow_counts(result)
        return dict(sorted(result.items()))

    def charge_totals(self) -> dict[str, int]:
        """The charge readout of every ray field: charge x amount summed over the things
        resident at active Nodes and in flight on Links, the owners totals() reads; a
        shadow carries no charge (bit-law-v1), so the parked shadows and the dense region
        hold none."""
        result: dict[str, int] = {}
        for index, definition in enumerate(self.initial.spatial_fields):
            if not definition.rays:
                continue
            total = 0
            for position in self._active:
                node = self.nodes[position]
                if node.rays:
                    total = checked_work(total + ray_charge(node.rays[index], definition))
            for packets in self.links.values():
                for packet in packets:
                    if packet is not None and packet.rays:
                        total = checked_work(total + ray_charge(packet.rays[index], definition))
            if definition.charge:
                for body in self._located_bodies():
                    if body.polarizer is not None and body.polarizer.family == index:
                        total = checked_work(total + checked_work(held_stock(body) * definition.charge))
            result[self.initial.fields[definition.field].name] = total
        return result

    def _located_bodies(self) -> list[ExternalBody]:
        """Every external body, at its Node or on a Link while it steps."""
        found = [node.body for node in self.nodes.values() if node.body is not None]
        found.extend(
            packet.body
            for packets in self.links.values()
            for packet in packets
            if packet is not None and packet.body is not None
        )
        return found

    def escaped_charge_totals(self) -> dict[str, int]:
        """The charge that left the world through an open boundary, per ray field:
        charge x amount summed over the escaped rays (ray-event-audit-v1)."""
        return {
            self.initial.fields[definition.field].name: self.escaped_charge[index]
            for index, definition in enumerate(self.initial.spatial_fields)
            if definition.rays
        }

    def values(self, position: Address3) -> dict[str, dict[str, object]]:
        return self.node_values(position, self.nodes.get(position))

    def node_values(self, position: Address3, node: SpatialNode | None) -> dict[str, dict[str, object]]:
        """The fields at one Node as the snapshot lists them, from the Node's state
        (`node`, or a blank Node when None), so that a Node read one at a time from
        the dense region's arrays is listed exactly as one held in `nodes`."""
        states = node.states if node is not None else self._blank_states()
        result: dict[str, dict[str, object]] = {}
        for index, (definition, state) in enumerate(
            zip(self.initial.spatial_fields, states, strict=True)
        ):
            field = self.initial.fields[definition.field]
            local = list(unpack(definition.baseline))
            for payload in state.populations:
                for component, value in enumerate(unpack(payload)):
                    local[component] = checked_work(local[component] + value)
            field.validate(pack(tuple(local)))
            if definition.rays:
                node_rays = node.rays if node is not None else ()
                rays = tuple(ray for ray in (node_rays[index] if node_rays else ()) if not ray.parked)
                local[0] = checked_work(local[0] + coherent_stock(rays, definition))
                field.validate(pack(tuple(local)))
            result[field.name] = {
                "baseline": unpack(definition.baseline),
                "value": tuple(local),
                "directions": tuple(unpack(v) for v in state.delivered),
                "populations": tuple(unpack(v) for v in state.populations),
            }
            if definition.rays:
                # The rays on their way; a parked shadow is the Node's memory
                # (node-is-ports-v1), listed in the snapshot's `parked`.
                result[field.name]["ray_count"] = sum(1 for ray in rays if not ray.parked)
            if definition.decay is not None and definition.decay.localizes:
                localized = node.localized if node is not None else self._blank_localized()
                result[field.name]["localized"] = unpack(localized[index])
        return result

    def accounting(self) -> dict[str, dict[str, object]]:
        """Diagnose every spatial owner, including fields without a conservation flag."""
        totals = self.totals()
        result = {}
        for definition in self.initial.spatial_fields:
            index = definition.field
            expected = tuple(
                start
                + source
                + reaction
                + transformed
                - loss
                - escaped
                - absorbed
                - taken
                - returned
                - spent
                for start, source, reaction, transformed, loss, escaped, absorbed, taken, returned, spent in zip(
                    self._initial_totals[index],
                    self.sources[index],
                    self.reactions[index],
                    self.transformations[index],
                    self.dissipation[index],
                    self.escaped[index],
                    self.absorbed[index],
                    self.absorbed_by_marks[index],
                    self.returned[index],
                    self.spent[index],
                    strict=True,
                )
            )
            result[self.initial.fields[index].name] = {
                "initial": tuple(self._initial_totals[index]),
                "current": tuple(totals[index]),
                "sources": tuple(self.sources[index]),
                "reactions": tuple(self.reactions[index]),
                "dissipated": tuple(self.dissipation[index]),
                "localized": tuple(self.localized[index]),
                "escaped": tuple(self.escaped[index]),
                "absorbed_by_bodies": tuple(self.absorbed[index]),
                "absorbed_by_marks": tuple(self.absorbed_by_marks[index]),
                "returned": tuple(self.returned[index]),
                "spent": tuple(self.spent[index]),
                "balanced": tuple(totals[index]) == expected,
                **(
                    {"transformations": tuple(self.transformations[index])}
                    if self.initial.field_rules
                    else {}
                ),
            }
        return result

    def external_bodies(self) -> list[dict[str, object]]:
        """Every external body (external-body-v1), in declaration order: the Node it is
        at, or the Node it is stepping to while on a Link, its momentum, its
        accumulators and its sink per family."""
        found: dict[int, dict[str, object]] = {}
        located: list[tuple[ExternalBody | None, Address3 | None, bool]] = [
            (node.body, position, False) for position, node in self.nodes.items()
        ]
        located.extend(
            (packet.body, self._neighbor(packet.origin, packet.port), True)
            for packets in self.links.values()
            for packet in packets
            if packet is not None and packet.body is not None
        )
        for body, position, stepping in located:
            if body is None or position is None:
                continue
            found[body.index] = {
                "index": body.index,
                "position": list(position),
                "stepping": stepping,
                "momentum": list(body.momentum),
                "accumulators": list(body.accumulators),
                "sink": {
                    self.initial.fields[definition.field].name: body.sink[i]
                    for i, definition in enumerate(self.initial.spatial_fields)
                    if body.sink[i]
                },
                # A polarizer's held shares and their phases (ray-polarization-v1),
                # sign-major -1, 0, 1 then pass and sink, in units of 1/D.
                **(
                    {}
                    if body.polarizer is None
                    else {"held": list(body.held), "held_phases": list(body.held_phases)}
                ),
            }
        return [found[index] for index in sorted(found)]

    def detector_marks(self) -> list[dict[str, object]]:
        """Every Detector mark (node-is-ports-v1), in declaration order: its Node
        and the thing resident at it, what the mark has absorbed per bit, `real`
        (the things) and `shadow` (the shadows home to it), per family (the
        nonzero entries), its momentum and the owners it is made of; a mark whose Node was never created has
        absorbed nothing."""
        result: list[dict[str, object]] = []
        for declared in self.initial.detectors:
            node = self.nodes.get(declared.position)
            mark = declared if node is None or node.detector is None else node.detector
            resident = mark.resident
            result.append(
                {
                    "position": list(mark.position),
                    "resident": {
                        "real": {
                            self.initial.fields[definition.field].name: resident.things[i]
                            for i, definition in enumerate(self.initial.spatial_fields)
                            if i < len(resident.things) and resident.things[i]
                        },
                        "shadow": {
                            self.initial.fields[definition.field].name: resident.shadows[i]
                            for i, definition in enumerate(self.initial.spatial_fields)
                            if i < len(resident.shadows) and resident.shadows[i]
                        },
                        "momentum": list(resident.momentum),
                        "owners": list(resident.owners),
                    },
                }
            )
        return result

    def detector_mark_momentum(self) -> tuple[int, int, int]:
        """The marks' momentum line of the audit: the exact sum over every resident."""
        total = [0, 0, 0]
        for item in self.detector_marks():
            resident = item["resident"]
            assert isinstance(resident, dict)
            momentum = resident["momentum"]
            assert isinstance(momentum, list)
            for axis in range(3):
                total[axis] = checked_work(total[axis] + momentum[axis])
        return (total[0], total[1], total[2])

    def external_body_momentum(self) -> tuple[int, int, int]:
        """The bodies' momentum line of the audit: the exact sum over every body."""
        total = [0, 0, 0]
        for item in self.external_bodies():
            momentum = item["momentum"]
            assert isinstance(momentum, list)
            for axis in range(3):
                total[axis] = checked_work(total[axis] + momentum[axis])
        return (total[0], total[1], total[2])

    def snapshot(self) -> dict[str, object]:
        """The engine's Nodes and Links as plain data; the dense region's Nodes read
        as Node state for the per-Node entries, its parked shadows from its arrays."""
        with self.materialized():
            return self._snapshot()

    def _snapshot(self) -> dict[str, object]:
        # Nothing at a Node names a bound group (loop-binding-v1, Highlights 3.4): a
        # group is read from the record by a reader, not listed here.
        result: dict[str, object] = {
            "spatial_fields": [
                self.node_entry(position, node) for position, node in sorted(self.nodes.items())
            ],
            "spatial_baselines": self.snapshot_baselines(),
            "spatial_transfers": self.snapshot_transfers(),
        }
        # The parked shadows (node-is-ports-v1): what every Node holds below one
        # quantum per owner, sign and heading, in units of the family's split
        # denominator, and the traces (amount 0); the dense region's Nodes are
        # read as Node state here (`materialized`).
        result["parked"] = [
            entry
            for position, node in sorted(self.nodes.items())
            for entry in self.parked_entries(position, node)
        ]
        return result

    def node_entry(self, position: Address3, node: SpatialNode) -> dict[str, object]:
        """One Node's entry of the snapshot's `spatial_fields`."""
        return {
            "position": position,
            "fields": self.node_values(position, node),
            "cost": node.last_cost,
            "arrival_mask": node.arrival_mask,
            "delay_counts": node.delay_counts,
            "waiting_until": None if node.pending is None else node.pending.ready_tick,
        }

    def parked_entries(self, position: Address3, node: SpatialNode) -> list[dict[str, object]]:
        """One Node's entries of the snapshot's `parked` list: its parked shadows
        in the order its rays hold them (node-is-ports-v1), each with its flow
        and the momentum it holds (return-field-v1)."""
        if not node.rays:
            return []
        return [
            {
                "position": position,
                "family": self.initial.fields[definition.field].name,
                "owner": ray.owner,
                "sign": ray.source_sign,
                "heading": list(definition.headings[ray.heading]),
                "amount": ray.amount,
                "unit": parked_unit(definition),
                "phase": ray.phase,
                "bit": BIT_SHADOW,
                "outbound": ray.outbound,
                "momentum": list(ray.momentum or (0, 0, 0)),
            }
            for index, definition in enumerate(self.initial.spatial_fields)
            for ray in node.rays[index]
            if ray.parked
        ]

    def snapshot_baselines(self) -> dict[str, tuple[int, ...]]:
        return {
            self.initial.fields[d.field].name: unpack(d.baseline) for d in self.initial.spatial_fields
        }

    def snapshot_transfers(self) -> list[dict[str, object]]:
        return [
            {
                "origin": p.origin,
                "target": self._neighbor(p.origin, p.port),
                "port": p.port,
                "arrival_tick": p.arrival_tick,
                "fields": {
                    self.initial.fields[d.field].name: tuple(unpack(v) for v in p.fields[i])
                    for i, d in enumerate(self.initial.spatial_fields)
                },
                "rays": sum(len(r) for r in p.rays),
            }
            for packets in self.links.values()
            for p in packets
            if p is not None
        ]

    def snapshot_nodes(self) -> Iterator[tuple[Address3, SpatialNode]]:
        """Every Node of the snapshot in position order, one at a time: the engine's
        own Nodes as they are and, in the dense mode, the region's visited Nodes
        read as Node state one x-slab at a time (dense-field-v1), so that beside
        the arrays no more than one slab's positions and one Node's state exist;
        the same Nodes, in the same order and with the same content, as
        `materialized` gives `nodes` for `snapshot`."""
        if self.dense is None:
            yield from sorted(self.nodes.items())
            return
        own: dict[int, list[Address3]] = {}
        for position in self.nodes:
            own.setdefault(position[0], []).append(position)
        for x in range(self.initial.shape[0]):
            region = set(self.dense.visited_slab(x))
            for position in sorted(region.union(own.get(x, ()))):
                if position in region:
                    yield position, self.dense.materialized_node(position, self.nodes.get(position))
                else:
                    yield position, self.nodes[position]

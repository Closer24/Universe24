"""Fixed-clock ownership for configured spatial fields, separate from carriers."""

from collections.abc import Callable, Mapping
from dataclasses import replace
from typing import TYPE_CHECKING

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
    BoundMotion,
    ExternalBody,
    Rays,
    SpatialBundle,
    SpatialPacket,
    SpatialPlan,
    SpatialState,
    bound_group,
    coherent_stock,
    group_content,
    group_momentum_field,
    held_ray,
    holds_source_stock,
    ray_charge,
    ray_momentum,
    ray_stock,
    validate_rays,
)
from .topology import neighbor_address


def free_rays(rays: Rays, group: BoundMotion | None) -> Rays:
    """The rays of one bundle whose momentum reads by heading: all of them at an
    owner without a bound group, the rays not held at one with a register
    (bound-group-motion-v1), whose group reads by that register once."""
    if group is None:
        return rays
    return tuple(ray for ray in rays if not held_ray(ray))


SpatialPlanner = Callable[
    [
        tuple[SpatialState, ...],
        tuple[DisturbanceRecord | None, ...],
        int,
        int,
        tuple[Rays, ...],
        int,
        int,
        int,
    ],
    SpatialPlan,
]
SpatialDecayer = Callable[[SpatialBundle], tuple[SpatialBundle, Values, int]]
EventSink = Callable[[dict[str, object]], None]
RecordCommit = Callable[[Address3, tuple[DisturbanceRecord | None, ...]], None]


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
    ) -> None:
        if initial.node_execution and (initial.conservation_contract is None or balance_guard is None):
            raise ValueError("node_execution requires a conservation contract and balance guard")
        if initial.node_execution and initial.field_rules and field_guard is None:
            raise ValueError("node_execution field rules require a field commit guard")
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
        # Host scheduling index only: retain physical registers in self.nodes.
        self._active: set[Address3] = set()
        self._field_tick = -1
        self.links: PortTable[SpatialPacket] = PortTable((None,) * 6)
        self.sources = [[0] * field.components for field in initial.fields]
        self.dissipation = [[0] * field.components for field in initial.fields]
        self.localized = [[0] * field.components for field in initial.fields]
        self.reactions = [[0] * field.components for field in initial.fields]
        self.transformations = [[0] * field.components for field in initial.fields]
        self.escaped = [[0] * field.components for field in initial.fields]
        # Content that left the world at an inverse split in annul mode.
        self.annulled = [[0] * field.components for field in initial.fields]
        # The charge that left the world through an open boundary, per spatial
        # field: charge x amount of every escaped ray (ray-event-audit-v1).
        self.escaped_charge = [0] * len(initial.spatial_fields)
        # Content that ended in an external body's sink (external-body-v1).
        self.absorbed = [[0] * field.components for field in initial.fields]
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
                self.annulled,
                self.absorbed,
            ),
            balance_guard,
            field_guard,
            meter.total,
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
            # A body's Node exists and is active from the start: it radiates.
            self._at(body.position)
        self._initial_totals = self.totals()

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
                detector_ticket=0 if mark is None else mark.seed,
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
            ) or any(holds_source_stock(record, self.initial.spatial_fields) for record in records):
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

    def _escape(self, packet: SpatialPacket, tick: int) -> None:
        """No receiving node exists outside; terminal stock escapes without exterior decay.

        A returning ray never reaches the boundary before its event Node, which its
        steps bound; one that would escape has no event Node in the world, and the
        engine fails closed instead of recording an escape (detector-return-v1). A
        returned field quantum of a spreading family has no event Node: it walks
        back until something takes it, and escapes like any ray otherwise
        (field-spreading-v1, the proposal of Highlights 5.5).
        """
        for definition, rays in zip(self.initial.spatial_fields, packet.rays or (), strict=False):
            if any(not ray.outbound and (ray.event_ports or not definition.spread) for ray in rays):
                raise ValueError("a returning ray cannot escape: its event Node is not in the world")
        if packet.body is not None:
            raise ValueError("an external body cannot leave the world: its Node must exist")
        amounts = [[0] * field.components for field in self.initial.fields]
        escaped_group: dict[str, object] = {}
        if packet.group is not None:
            # A bound group leaves the world whole (bound-group-motion-v1): its
            # content per family with its rays, its momentum by its register.
            group = bound_group(packet.rays)
            momentum_field = group_momentum_field(group, self.initial.spatial_fields)
            if momentum_field is not None:
                for axis, value in enumerate(packet.group.momentum):
                    amounts[momentum_field][axis] = checked_work(amounts[momentum_field][axis] + value)
            escaped_group = {
                "families": [
                    self.initial.fields[self.initial.spatial_fields[index].field].name
                    for index, _ in group
                ],
                "amounts": [ray.amount for _, ray in group],
                "content": group_content(group),
                "momentum": packet.group.momentum,
            }
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
                    for axis, value in enumerate(
                        ray_momentum(free_rays(rays, packet.group), definition)
                    ):
                        amounts[definition.momentum_field][axis] = checked_work(
                            amounts[definition.momentum_field][axis] + value
                        )
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
        if escaped_group:
            self._event(
                "spatial_escaped",
                tick,
                packet.origin,
                port=packet.port,
                escaped=escaped,
                bound_group=escaped_group,
            )
        else:
            self._event("spatial_escaped", tick, packet.origin, port=packet.port, escaped=escaped)

    def deliver(self, tick: int, residents: Mapping[Address3, DisturbanceNode] | None = None) -> None:
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
        for position, arrivals in sorted(ready.items()):
            notifications = self._at(position).receive(
                tuple(arrivals),
                tick,
                self._services,
                carrier=None if residents is None else residents.get(position),
            )
            for packet in arrivals:
                links = list(self.links[packet.origin])
                links[packet.port] = None
                self.links[packet.origin] = tuple(links)
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
        if self.initial.node_execution:
            for position in sorted(self._active):
                try:
                    self.nodes[position].commit_ready(tick, residents.get(position), self._services)
                finally:
                    self.links.refresh(position)

    def totals(self) -> list[list[int]]:
        result = [[0] * field.components for field in self.initial.fields]
        volume = self.initial.shape[0] * self.initial.shape[1] * self.initial.shape[2]
        for index, definition in enumerate(self.initial.spatial_fields):
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
            if definition.rays:
                # Resident rays keep a Node active, including finite local residence.
                # A bound group's rays read their momentum by the group's register,
                # added once below (bound-group-motion-v1).
                for position in self._active:
                    node = self.nodes[position]
                    if node.rays:
                        result[definition.field][0] += ray_stock(node.rays[index])
                        if definition.momentum_field is not None:
                            for axis, value in enumerate(
                                ray_momentum(free_rays(node.rays[index], node.bound_motion), definition)
                            ):
                                result[definition.momentum_field][axis] += value
                for packets in self.links.values():
                    for packet in packets:
                        if packet is not None and packet.rays:
                            result[definition.field][0] += ray_stock(packet.rays[index])
                            if definition.momentum_field is not None:
                                for axis, value in enumerate(
                                    ray_momentum(free_rays(packet.rays[index], packet.group), definition)
                                ):
                                    result[definition.momentum_field][axis] += value
        for motion, rays in self._bound_registers():
            momentum_field = group_momentum_field(bound_group(rays), self.initial.spatial_fields)
            if momentum_field is not None:
                for axis, value in enumerate(motion.momentum):
                    result[momentum_field][axis] += value
        return result

    def _bound_registers(self) -> list[tuple[BoundMotion, tuple[Rays, ...]]]:
        """Every bound group's register with its rays (bound-group-motion-v1): held at
        an active Node, or on a Link while the group steps."""
        found: list[tuple[BoundMotion, tuple[Rays, ...]]] = []
        for position in sorted(self._active):
            node = self.nodes[position]
            if node.bound_motion is not None and node.rays:
                found.append((node.bound_motion, node.rays))
        for packets in self.links.values():
            for packet in packets:
                if packet is not None and packet.group is not None:
                    found.append((packet.group, packet.rays))
        return found

    def charge_totals(self) -> dict[str, int]:
        """The charge readout of every ray field: charge x amount summed over the rays
        resident at active Nodes and in flight on Links, the owners totals() reads."""
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
            result[self.initial.fields[definition.field].name] = total
        return result

    def escaped_charge_totals(self) -> dict[str, int]:
        """The charge that left the world through an open boundary, per ray field:
        charge x amount summed over the escaped rays (ray-event-audit-v1)."""
        return {
            self.initial.fields[definition.field].name: self.escaped_charge[index]
            for index, definition in enumerate(self.initial.spatial_fields)
            if definition.rays
        }

    def values(self, position: Address3) -> dict[str, dict[str, object]]:
        states = self.nodes[position].states if position in self.nodes else self._blank_states()
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
                node_rays = self.nodes[position].rays if position in self.nodes else ()
                rays = node_rays[index] if node_rays else ()
                local[0] = checked_work(local[0] + coherent_stock(rays, definition))
                field.validate(pack(tuple(local)))
            result[field.name] = {
                "baseline": unpack(definition.baseline),
                "value": tuple(local),
                "directions": tuple(unpack(v) for v in state.delivered),
                "populations": tuple(unpack(v) for v in state.populations),
            }
            if definition.rays:
                result[field.name]["ray_count"] = len(rays)
            if definition.decay is not None and definition.decay.localizes:
                localized = (
                    self.nodes[position].localized if position in self.nodes else self._blank_localized()
                )
                result[field.name]["localized"] = unpack(localized[index])
        return result

    def accounting(self) -> dict[str, dict[str, object]]:
        """Diagnose every spatial owner, including fields without a conservation flag."""
        totals = self.totals()
        result = {}
        for definition in self.initial.spatial_fields:
            index = definition.field
            expected = tuple(
                start + source + reaction + transformed - loss - escaped - annulled - absorbed
                for start, source, reaction, transformed, loss, escaped, annulled, absorbed in zip(
                    self._initial_totals[index],
                    self.sources[index],
                    self.reactions[index],
                    self.transformations[index],
                    self.dissipation[index],
                    self.escaped[index],
                    self.annulled[index],
                    self.absorbed[index],
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
                "annulled": tuple(self.annulled[index]),
                "absorbed_by_bodies": tuple(self.absorbed[index]),
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
            }
        return [found[index] for index in sorted(found)]

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
        bound_groups: list[dict[str, object]] = []
        for position, node in sorted(self.nodes.items()):
            group = bound_group(node.rays) if node.rays else ()
            if group:
                # Matter (ray-binding-v1, Highlights 3.4): the bound group held at
                # the Node this tick, for a Renderer to draw.
                bound_groups.append(
                    {
                        "position": position,
                        "families": [
                            self.initial.fields[self.initial.spatial_fields[index].field].name
                            for index, _ in group
                        ],
                        "amounts": [ray.amount for _, ray in group],
                        "phases": [ray.phase for _, ray in group],
                        "ray_delay": node.bound_delay,
                        # bound-group-motion-v1: the group's register.
                        "momentum": (
                            (0, 0, 0) if node.bound_motion is None else node.bound_motion.momentum
                        ),
                        "accumulators": (
                            (0, 0, 0) if node.bound_motion is None else node.bound_motion.accumulators
                        ),
                    }
                )
        return {
            "bound_groups": bound_groups,
            "spatial_fields": [
                {
                    "position": position,
                    "fields": self.values(position),
                    "cost": node.last_cost,
                    "arrival_mask": node.arrival_mask,
                    "delay_counts": node.delay_counts,
                    "waiting_until": None if node.pending is None else node.pending.ready_tick,
                }
                for position, node in sorted(self.nodes.items())
            ],
            "spatial_baselines": {
                self.initial.fields[d.field].name: unpack(d.baseline)
                for d in self.initial.spatial_fields
            },
            "spatial_transfers": [
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
            ],
        }

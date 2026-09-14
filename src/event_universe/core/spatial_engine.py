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
from .event_space import CausalEventSpace
from .integer import checked_work
from .node_boundary import validate_spatial_bundle, validate_spatial_states
from .node_conservation import NodeConservationGuard
from .node_execution import NodeExecution
from .node_ports import PortTable
from .node_services import NodeEvents
from .source_emission import SourceDeposit
from .spatial_node import NodeActivity, SpatialAccounting, SpatialNode, SpatialServices
from .spatial_node import ReactionCommit as ReactionCommit
from .spatial_node import SpatialCoupler as SpatialCoupler
from .spatial_node import SpatialFieldGuard as SpatialFieldGuard
from .spatial_state import (
    Claims,
    Rays,
    SpatialBundle,
    SpatialPacket,
    SpatialPlan,
    SpatialState,
    coherent_stock,
    ray_momentum,
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
        tuple[Claims, ...],
        int,
    ],
    SpatialPlan,
]
SpatialDecayer = Callable[[SpatialBundle], tuple[SpatialBundle, Values, int]]
EventSink = Callable[[dict[str, object]], None]
RecordCommit = Callable[[Address3, tuple[DisturbanceRecord | None, ...]], None]
RecordCause = Callable[[Address3], int | None]
CauseCommit = Callable[[Address3, int], None]


class SpatialEngine:
    def commit_source(
        self, position: Address3, tick: int, proposal: SourceDeposit
    ) -> list[dict[str, object]]:
        """Install a preflighted colocated source before the ordinary field cycle."""
        validate_spatial_states(self.initial, proposal.states)
        if len(proposal.source_delta) != len(self.initial.fields):
            raise ValueError("source accounting layout differs from the fields")
        node = self._at(position)
        actual = [[0] * field.components for field in self.initial.fields]
        for old, new, definition in zip(
            node.states, proposal.states, self.initial.spatial_fields, strict=True
        ):
            if (old.allocation_phases, old.delivered, old.received_mask) != (
                new.allocation_phases,
                new.delivered,
                new.received_mask,
            ):
                raise ValueError("source deposit may only add local field populations")
            for before, after in zip(old.populations, new.populations, strict=True):
                for component, (a, b) in enumerate(zip(unpack(before), unpack(after), strict=True)):
                    actual[definition.field][component] = checked_work(
                        actual[definition.field][component] + b - a
                    )
        for index, field in enumerate(self.initial.fields):
            if len(proposal.source_delta[index]) != field.components:
                raise ValueError("source accounting component count differs from the field")
            for value in proposal.source_delta[index]:
                checked_work(value)
        if tuple(tuple(values) for values in actual) != proposal.source_delta:
            raise ValueError("source accounting differs from its local population change")
        if self.event_space is not None:
            self.event_space.require_room(1)
        notifications: list[dict[str, object]] = []
        cause = self._event(
            "spatial_envelope_source",
            tick,
            position,
            notifications=notifications,
            causes=(node.cause_id, proposal.cause_id),
            source_delta={
                field.name: proposal.source_delta[i]
                for i, field in enumerate(self.initial.fields)
                if any(proposal.source_delta[i])
            },
        )
        node.states, node.cause_id = proposal.states, cause
        external = proposal.source_delta
        if proposal.funded_delta:
            if len(proposal.funded_delta) != len(proposal.source_delta):
                raise ValueError("funded accounting layout differs from the fields")
            external = tuple(
                tuple(checked_work(value - paid) for value, paid in zip(values, funded, strict=True))
                for values, funded in zip(proposal.source_delta, proposal.funded_delta, strict=True)
            )
        self._services.accounting.record_sources(external)
        if proposal.funded_delta:
            # Stock the wave paid into the field is an internal transfer, like a
            # funded carrier emission, so the per-field audit stays balanced.
            self._services.accounting.record_reactions(proposal.funded_delta)
        self._active.add(position)
        return notifications

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
        event_space: CausalEventSpace | None = None,
        balance_guard: NodeConservationGuard | None = None,
        field_guard: SpatialFieldGuard | None = None,
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
        self.event_space = event_space
        self.nodes: dict[Address3, SpatialNode] = {}
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
        meter = CostMeter(initial.operation_costs)
        if initial.spatial_computation_delay:
            components = 8 * sum(initial.fields[d.field].components for d in initial.spatial_fields)
            meter.charge("read", 2 * components)
            meter.charge("evaluate", components)
            meter.charge("update", components)
        self._services = SpatialServices(
            replace(initial, seeds=(), spatial_seeds=()),
            planner,
            NodeEvents(event_space, observer),
            coupler,
            decayer,
            NodeActivity(self._active),
            SpatialAccounting(
                self.sources, self.dissipation, self.reactions, self.transformations, self.localized
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
        self._initial_totals = self.totals()
        if self.event_space is not None:
            self.event_space.require_room(len(self.nodes))
            for position, node in sorted(self.nodes.items()):
                node.cause_id = self._event("spatial_source", 0, position)

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
            self.nodes[position] = SpatialNode(
                self._blank_states(),
                position=position,
                output=self.links.bank(position),
                arrival_mask=(0,) * 6,
                delay_counts=(0,) * 6,
                localized=self._blank_localized(),
                rays=tuple(() for _ in self.initial.spatial_fields),
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
        causes: tuple[int | None, ...] = (),
        notifications: list[dict[str, object]] | None = None,
        **details: object,
    ) -> int | None:
        identity = None
        if self.event_space is not None:
            entry = self.event_space.append(
                tick=tick,
                addresses=(position,),
                owner="spatial",
                kind=event,
                physical_parents=tuple(dict.fromkeys(c for c in causes if c is not None)),
            )
            identity = entry.id
            details = {**details, "event_id": identity, "parents": entry.parents}
        if self.observer is not None:
            data = {"event": event, "tick": tick, "position": position, **details}
            if notifications is None:
                self.observer(data)
            else:
                notifications.append(data)
        return identity

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
            ):
                positions.add(position)
        if execution is not None and execution.parallel:
            execution.finish_cycles(
                tuple(
                    self._at(position).plan_cycle(tick, residents.get(position), self._services)
                    for position in sorted(positions)
                )
            )
        else:
            for position in sorted(positions):
                self._at(position).advance(tick, residents.get(position), self._services)

    def _escape(self, packet: SpatialPacket, tick: int) -> None:
        """No receiving node exists outside; terminal stock escapes without exterior decay."""
        amounts = [[0] * field.components for field in self.initial.fields]
        if self.event_space is not None:
            self.event_space.require_room(1)
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
                if definition.momentum_field is not None:
                    for axis, value in enumerate(ray_momentum(rays, definition)):
                        amounts[definition.momentum_field][axis] = checked_work(
                            amounts[definition.momentum_field][axis] + value
                        )
        for index, values in enumerate(amounts):
            for component, value in enumerate(values):
                self.escaped[index][component] += value
        links = list(self.links[packet.origin])
        links[packet.port] = None
        self.links[packet.origin] = tuple(links)
        self._event(
            "spatial_escaped",
            tick,
            packet.origin,
            causes=(packet.cause_id,),
            port=packet.port,
            escaped={
                field.name: tuple(amounts[i])
                for i, field in enumerate(self.initial.fields)
                if any(amounts[i])
            },
        )

    def deliver(self, tick: int, residents: Mapping[Address3, DisturbanceNode] | None = None) -> None:
        ready: dict[Address3, list[SpatialPacket]] = {}
        for origin, packets in self.links.items():
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
                self.nodes[position].commit_ready(tick, residents.get(position), self._services)

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
                # Rays never rest at an idle Node: they leave on every cycle.
                for position in self._active:
                    node = self.nodes[position]
                    if node.rays:
                        result[definition.field][0] += ray_stock(node.rays[index])
                        if definition.momentum_field is not None:
                            for axis, value in enumerate(ray_momentum(node.rays[index], definition)):
                                result[definition.momentum_field][axis] += value
                for packets in self.links.values():
                    for packet in packets:
                        if packet is not None and packet.rays:
                            result[definition.field][0] += ray_stock(packet.rays[index])
                            if definition.momentum_field is not None:
                                for axis, value in enumerate(
                                    ray_momentum(packet.rays[index], definition)
                                ):
                                    result[definition.momentum_field][axis] += value
        return result

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
                start + source + reaction + transformed - loss - escaped
                for start, source, reaction, transformed, loss, escaped in zip(
                    self._initial_totals[index],
                    self.sources[index],
                    self.reactions[index],
                    self.transformations[index],
                    self.dissipation[index],
                    self.escaped[index],
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
                "balanced": tuple(totals[index]) == expected,
                **(
                    {"transformations": tuple(self.transformations[index])}
                    if self.initial.field_rules
                    else {}
                ),
            }
        return result

    def snapshot(self) -> dict[str, object]:
        return {
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

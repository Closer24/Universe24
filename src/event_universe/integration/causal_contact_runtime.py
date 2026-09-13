"""Compose finite quantum contacts with locally propagated ordinary source data."""

from collections.abc import Mapping
from dataclasses import replace
from types import MappingProxyType

from event_universe.core.disturbance_state import (
    Address3,
    DisturbanceRecord,
    InitialState,
    LocalPlan,
    bounded,
)
from event_universe.core.event_resolution import LocalContext, Planner
from event_universe.core.event_space import CausalEventSpace
from event_universe.core.integer import checked_work
from event_universe.core.node_services import NodeEvents, cycle_timing
from event_universe.core.source_emission import SourceDeposit
from event_universe.core.source_emission_node import EmittingEnvelopeNode
from event_universe.core.source_envelope_node import EnvelopeGate
from event_universe.core.spatial_state import SpatialState
from event_universe.core.topology import neighbor_address
from event_universe.fields.source_emission import (
    SourceEmissionLaw,
    deposit_populations,
    initial_emission_state,
    prepare_emission,
)
from event_universe.fields.source_envelope import Matrix, local_output, output_cost
from event_universe.quantum import LocalUnitary

from .contact_program import ContactDomain
from .contact_runtime import ContactEventResolver
from .event_program import Program


class CausalContactResolver(ContactEventResolver):
    """Quantum queries never supply ordinary source values, clocks or retirement."""

    def __init__(self, initial: InitialState, program: Program, events: CausalEventSpace) -> None:
        super().__init__(initial, program, events)
        self._source_events = NodeEvents(events, None)
        self._source_law = SourceEmissionLaw(
            initial.fields, initial.spatial_fields, initial.emissions, initial.operation_costs
        )
        self._source_nodes: dict[Address3, EmittingEnvelopeNode] = {}
        self._domain_at: dict[Address3, ContactDomain] = {}
        self._ports_at: dict[Address3, tuple[int, ...]] = {}
        self._phase_gates: dict[Address3, tuple[EnvelopeGate | None, ...]] = {}
        matrices: list[Matrix] = []
        price = initial.operation_costs.price
        self._send_cost = bounded(2 * price("read") + price("update") + price("send"))
        self._send_delay = cycle_timing(self._send_cost, initial.normal_budget, initial.link_ticks)[0]
        compute_cost = 0
        for domain in self.domains:
            addresses = tuple(self.space.config.addresses[q] for q in domain.registers)
            plans: dict[Address3, list[EnvelopeGate | None]] = {
                address: [None] * len(domain.phases) for address in addresses
            }
            for phase, operations in enumerate(domain.phases):
                for rule, registers in operations:
                    matrix = tuple(tuple((v.real, v.imag) for v in row) for row in rule.matrix)
                    index = len(matrices)
                    matrices.append(matrix)
                    compute_cost = max(
                        compute_cost,
                        output_cost(matrix, initial.operation_costs)
                        + price("receive")
                        + price("read")
                        + price("update")
                        + price("commit"),
                    )
                    forward_port = -1
                    if len(registers) == 2:
                        first, second = (self.space.config.addresses[q] for q in registers)
                        forward_port = next(
                            p
                            for p in range(6)
                            if neighbor_address(first, p, initial.shape, initial.boundary) == second
                        )
                    for row, register in enumerate(registers):
                        address = self.space.config.addresses[register]
                        port = -1
                        if len(registers) == 2:
                            port = forward_port if row == 0 else forward_port ^ 1
                        plans[address][phase] = EnvelopeGate(index, row, port)
            for address in addresses:
                self._source_nodes[address] = EmittingEnvelopeNode(
                    address, emission_state=initial_emission_state(self._source_law, domain.output)
                )
                self._domain_at[address] = domain
                self._phase_gates[address] = tuple(plans[address])
                self._ports_at[address] = tuple(
                    p
                    for p in range(6)
                    if neighbor_address(address, p, initial.shape, initial.boundary) in addresses
                )
        self._matrices = tuple(matrices)
        assert program.contacts is not None
        self._source_banks = (self._source_nodes,) + tuple(
            {
                address: EmittingEnvelopeNode(
                    address,
                    emission_state=initial_emission_state(
                        self._source_law, self._domain_at[address].output
                    ),
                )
                for address in self._source_nodes
            }
            for _ in range(program.contacts.max_generations - 1)
        )
        for address, node in self._source_nodes.items():
            node.generations = tuple(bank[address] for bank in self._source_banks[1:])
        self._compute_delay = cycle_timing(
            bounded(compute_cost), initial.normal_budget, initial.link_ticks
        )[0]
        self._gate_end = bounded(self._send_delay + initial.link_ticks + self._compute_delay)
        self._gate_period = bounded(self._gate_end + initial.link_ticks)
        # Quantum scheduling may use source activation time; ordinary source
        # evolution never reads this quantum-only index.
        self._activation_ticks: dict[str, int] = {}
        self._source_started_tick = -1

    def source_nodes(self) -> Mapping[Address3, EmittingEnvelopeNode]:
        return MappingProxyType(self._source_nodes)

    def _control_delay(self, address: Address3) -> int:
        price = self.initial.operation_costs.price
        cost = bounded(
            price("receive")
            + price("read")
            + 3 * price("update")
            + len(self._ports_at[address]) * price("send")
            + price("commit")
        )
        return cycle_timing(cost, self.initial.normal_budget, self.initial.link_ticks)[0]

    def start_sources(self, tick: int) -> None:
        if tick == self._source_started_tick:
            raise ValueError("source gate clock may start only once per tick")
        self._source_started_tick = tick
        if tick % self._gate_period:
            return
        epoch = tick // self._gate_period
        for bank in self._source_banks:
            self._start_bank(bank, tick, epoch)

    def _start_bank(self, bank: Mapping[Address3, EmittingEnvelopeNode], tick: int, epoch: int) -> None:
        for address, node in bank.items():
            phases = self._phase_gates[address]
            gate = phases[epoch % len(phases)]
            if gate is None:
                continue
            # A one-mode phase waits for the same fixed phase boundary. It
            # carries no physical message and no received neighbor value.
            local_wait = self._compute_delay + (self.initial.link_ticks if gate.port < 0 else 0)
            node.start_gate(
                tick,
                epoch,
                gate,
                self._send_delay,
                self.initial.link_ticks,
                local_wait,
                self._send_cost,
                self._source_events,
            )

    def _advance_sources(self, tick: int) -> None:
        for bank in self._source_banks:
            self._advance_bank(bank, tick)

    def _advance_bank(self, bank: Mapping[Address3, EmittingEnvelopeNode], tick: int) -> None:
        arrivals = tuple(
            (address, slot, packet)
            for address, node in bank.items()
            for slot, packet in enumerate(node.output)
            if packet is not None and packet.arrival_tick == tick
        )
        for address, slot, packet in arrivals:
            if packet.origin != address or packet.port != slot % 6:
                raise ValueError("source packet differs from its sender-owned Port")
            destination = neighbor_address(
                address, packet.port, self.initial.shape, self.initial.boundary
            )
            if destination is None or destination not in bank:
                raise ValueError("source packet must follow a declared domain Link")
            if self._domain_at[destination] is not self._domain_at[address]:
                raise ValueError("source packets cannot cross independent domains")
            target = bank[destination]
            target.receive(
                packet,
                tick,
                self.initial.link_ticks,
                self._control_delay(destination),
                self._source_events,
                costs=self.initial.operation_costs,
            )
            bank[address].clear_output(slot, packet)
        for address, node in bank.items():
            node.complete(
                tick,
                local_output,
                self._matrices,
                self.initial.operation_costs,
                self._ports_at[address],
                0,
                self.initial.link_ticks,
                self._source_events,
            )

    def propagation_phase(
        self, tick: int, domain: ContactDomain
    ) -> tuple[tuple[LocalUnitary, tuple[int, ...]], ...]:
        if tick < self._gate_end or (tick - self._gate_end) % self._gate_period:
            return ()
        start = tick - self._gate_end
        if self._activation_ticks.get(domain.name, tick) > start:
            return ()
        return domain.phases[(start // self._gate_period) % len(domain.phases)]

    def begin_tick(self, tick: int) -> None:
        self._advance_sources(tick)
        super().begin_tick(tick)

    def resolve(self, context: LocalContext, planner: Planner) -> LocalPlan:
        plan = super().resolve(context, planner)
        if plan.resolution_token is None:
            return plan
        price = self.initial.operation_costs.price
        # Both null and click reserve the same worst-case local publication
        # work before sampling. Source preparation uses this same local tariff.
        extra = bounded(
            3 * price("update") + len(self._ports_at[context.address]) * price("send") + price("commit")
        )
        self.overhead_cost = checked_work(self.overhead_cost + extra)
        return replace(plan, cost=bounded(plan.cost + extra))

    def alternatives(
        self, context: LocalContext, token: int
    ) -> tuple[tuple[tuple[int, DisturbanceRecord | None], ...], ...]:
        choices = super().alternatives(context, token)
        reservation, domain = self._reservation(context, token)
        node = self._source_nodes[context.address]
        if reservation.source:
            node.check_activation(context.tick)
        elif not node.retired:
            node.check_null(context.tick)
            assert self.space.waves is not None
            origin = self.space.waves.names.get(domain.name)
            if origin is not None:
                node.check_capture(
                    origin,
                    context.tick,
                    self._ports_at[context.address],
                    0,
                    self.initial.link_ticks,
                )
        return choices

    def commit_choice(self, context: LocalContext, token: int, following_events: int) -> tuple[int, int]:
        reservation, domain = self._reservation(context, token)
        # Reserve the local source event together with both original owners.
        self.events.require_room((4 if reservation.source else 3) + following_events)
        outcome, event_id = super().commit_choice(context, token, following_events + 1)
        node = self._source_nodes[context.address]
        if reservation.source:
            # This identity was created by the colocated committed preparation;
            # no remote value is copied through the origin reference.
            assert self.space.waves is not None
            origin = self.space.waves.names[domain.name]
            node.activate(origin, context.tick, event_id)
            self._activation_ticks[domain.name] = context.tick
        elif outcome == 1:
            assert self.space.waves is not None
            origin = self.space.waves.names[domain.name]
            node.capture(
                origin,
                context.tick,
                event_id,
                self._ports_at[context.address],
                0,
                self.initial.link_ticks,
                self._source_events,
            )
            node.pending_emission = None
        elif not node.retired:
            node.null(context.tick, event_id)
            node.pending_emission = None
        return outcome, event_id

    def prepare_source(
        self, address: Address3, tick: int, states: tuple[SpatialState, ...], node_cost: int
    ) -> SourceDeposit | None:
        node = self._source_banks[tick % len(self._source_banks)][address]
        if node.retired or not node.source_id:
            node.pending_emission = None
            return None
        if node.pending_emission is None and tick >= node.emission_next_tick:
            assert node.emission_state is not None
            prepared = prepare_emission(
                self._source_law,
                self._domain_at[address].output,
                node.amplitude,
                node.emission_state,
                node_cost,
                node.source_id,
                node.cause_id,
            )
            delay, interval = cycle_timing(
                prepared.cost, self.initial.normal_budget, self.initial.link_ticks
            )
            self._source_events.require_room(1)
            cause, _ = self._source_events.record(
                "source-emission-started",
                tick,
                address,
                node.cause_id,
                event_cost=prepared.cost,
                owner="source-envelope",
            )
            node.pending_emission = replace(
                prepared,
                ready_tick=bounded(tick + delay),
                next_tick=bounded(tick + interval),
                cause_id=cause,
            )
        pending = node.pending_emission
        if pending is None or pending.ready_tick > tick:
            return None
        return SourceDeposit(
            deposit_populations(self._source_law, states, pending.populations),
            pending.source_delta,
            pending.cause_id,
        )

    def commit_source(self, address: Address3, tick: int) -> None:
        node = self._source_banks[tick % len(self._source_banks)][address]
        pending = node.pending_emission
        if pending is None or pending.ready_tick > tick or node.retired:
            raise ValueError("source emission must commit its live ready local proposal")
        node.emission_state = pending.following
        node.emission_next_tick = pending.next_tick
        node.pending_emission = None

    def report(self) -> dict[str, object]:
        return {
            **super().report(),
            "model": "causal-contact-fields-v1",
            "classical_field_source": "causal_local_envelope",
            "source_gate_period": self._gate_period,
            "source_gate_commit_offset": self._gate_end,
            "source_envelopes": [
                {
                    "position": address,
                    "origin": node.source_id,
                    "amplitude": (node.amplitude.real, node.amplitude.imag, node.amplitude.denominator),
                    "retired": bool(node.retired),
                    "terminal_ready_tick": None
                    if node.pending_stop is None
                    else node.pending_stop.ready_tick,
                }
                for address, node in self._source_nodes.items()
            ],
        }

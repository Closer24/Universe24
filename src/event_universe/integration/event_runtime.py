"""Compose native local cycles with the shared event ledger and quantum owner.

Only a selected complete local instrument may create a classical control code.
The scheduler receives the same LocalPlan as any other configured local law.
No world reference, remote physical state or diagnostic marginal is an input.
"""

from dataclasses import asdict, replace
from random import Random

from event_universe.core.disturbance_state import InitialState, LocalPlan, bounded, pack
from event_universe.core.event_resolution import EventResolver, LocalContext, Planner
from event_universe.core.event_space import CausalEventSpace
from event_universe.core.integer import checked_work
from event_universe.quantum import DeferredQuantum

from .event_program import Program, parse_event_program


class NativeEventResolver:
    """One configured bounded rule per register_index; new local arrivals can trigger again."""

    def __init__(self, initial: InitialState, program: Program, events: CausalEventSpace) -> None:
        if program.network is None:
            raise ValueError("quantum configuration required by this resolver")
        self.initial = initial
        self.program = program
        self.events = events
        self.owner = DeferredQuantum()
        self.space = self.owner.bind_event_network(program.network, event_space=events)
        self.layers = dict(program.layers)
        self.origin_layers = dict(program.layer_origins)
        self.bindings = {b.address: b for b in program.bindings}
        self.rng = Random(program.seed)
        self.draws = 0
        self.host_plans = 0
        self.overhead_cost = 0
        self.wave_control_cost = 0
        self._null_certificates: dict[tuple[int, int, int], int] = {}

    def _sample(self, total: int) -> int:
        if self.program.tickets is None:
            ticket = self.rng.randrange(total)
        else:
            if self.draws >= len(self.program.tickets):
                raise ValueError("supplied ticket stream exhausted")
            ticket = self.program.tickets[self.draws]
        self.draws = checked_work(self.draws + 1)
        return ticket

    def has_work(self, context: LocalContext) -> bool:
        binding = self.bindings.get(context.address)
        if binding is None or (context.tick != 0 and context.received == 0):
            return False
        present = [r.type_index for r in context.records if r is not None]
        return all(present.count(t) >= binding.types.count(t) for t in binding.types)

    def resolve(self, context: LocalContext, planner: Planner) -> LocalPlan:
        if context.tick != self.space.tick:
            raise ValueError("native event and quantum clocks disagree")
        binding = self.bindings.get(context.address)
        if binding is None:
            return planner(context.records, context.residuals, context.received)
        # The selected law prices one local activation check. Stale resident
        # records do not trigger another measurement merely because a tick ran.
        inspection = self.initial.operation_costs.price("read")
        selected: list[int] = []
        for type_index in binding.types:
            slot = next(
                (
                    i
                    for i, r in enumerate(context.records)
                    if i not in selected and r is not None and r.type_index == type_index
                ),
                None,
            )
            if slot is None:
                break
            selected.append(slot)
        if len(selected) != len(binding.types) or (context.tick != 0 and context.received == 0):
            plan = planner(context.records, context.residuals, context.received)
            self.overhead_cost = checked_work(self.overhead_cost + inspection)
            return replace(plan, cost=bounded(checked_work(plan.cost + inspection)))
        # Validate ALL mechanical alternatives before sampling; rejecting one
        # outcome after sampling would change the specified distribution.
        plans: list[LocalPlan] = []
        overhead = bounded(inspection + 1 + len(selected) * self.initial.operation_costs.price("update"))
        for code in binding.codes:
            records = list(context.records)
            for slot in selected:
                old = records[slot]
                assert old is not None
                values = list(old.values)
                values[binding.field] = pack((code,))
                records[slot] = replace(old, values=tuple(values))
            plan = planner(tuple(records), context.residuals, context.received)
            plans.append(replace(plan, cost=bounded(checked_work(plan.cost + overhead))))
        self.host_plans = checked_work(self.host_plans + len(plans))
        # Reserve a trigger, a record and the native cycle-start before commit.
        self.events.require_room(3)
        trigger = self.events.append(
            tick=context.tick,
            addresses=(context.address,),
            owner="resolver",
            kind="request",
            physical_parents=() if context.cause is None else (context.cause,),
        )
        decision = self.space.prepare(
            trigger.id, binding.register_index, binding.instrument, cause=trigger.id
        )
        ticket = None
        if sum(weight > 0 for weight in decision.weights) > 1:
            ticket = self._sample(decision.total_weight)
        record = self.space.commit(decision, ticket)
        self.overhead_cost = checked_work(self.overhead_cost + overhead)
        return replace(plans[record.outcome], cause_id=record.event_id)

    def advance(self, tick: int) -> None:
        with self.events.transaction():
            if tick != self.space.tick + 1:
                raise ValueError("native scheduler must advance the recipe clock once")
            layer = self.layers.get(tick, ())
            waves = self.space.waves
            groups = (
                None
                if waves is None
                else tuple(
                    tuple(waves.names[name] for name in names)
                    for names in self.origin_layers.get(tick, ())
                )
            )
            live = (
                layer
                if waves is None or groups is None
                else tuple(
                    operation
                    for operation, origins in zip(layer, groups, strict=True)
                    if waves.operation_live(origins, operation[1])
                )
            )
            for _, register_indices in live:
                if (
                    len(register_indices) == 2
                    and self.space.config.addresses[register_indices[0]]
                    != self.space.config.addresses[register_indices[1]]
                ):
                    for q in register_indices:
                        if tick - self.space.physical_ticks[q] < self.initial.link_ticks:
                            raise ValueError("coherent neighbor operation precedes physical link time")
            reads = (
                () if waves is None else tuple((a, len(bank.origins)) for a, bank in waves.banks.items())
            )
            if waves is not None:
                updates = waves.plan(
                    tuple((self.events.next_id + i, indices) for i, (_, indices) in enumerate(live))
                )
                predicted = {id(bank): (origins, event) for bank, origins, event in updates}
                eligible = 0
                null_checks = 0
                for binding in self.program.wave_interactions:
                    bank = waves.banks[binding.address]
                    origins, event_id = predicted.get(id(bank), (bank.origins, bank.event_id))
                    required = tuple(waves.names[name] for name in binding.origins)
                    if any(not waves.relevant(origin) for origin in required) and (
                        self._null_certificates.get(binding.address)
                        != self.space.heads[binding.register_index]
                        or any(binding.register_index in indices for _, indices in live)
                    ):
                        null_checks += 1
                    if (
                        event_id is not None
                        and event_id != bank.consumed_id
                        and all(origin in origins and waves.relevant(origin) for origin in required)
                    ):
                        eligible += 1
                cancellations = sum(
                    any(not waves.relevant(origin) for origin in origins)
                    for origins in (() if groups is None else groups)
                )
                self.events.require_room(
                    len(live)
                    + cancellations
                    + null_checks
                    + sum(count > 0 for _, count in reads)
                    + 2 * eligible
                )
            before_cost = self.events.model_cost
            self.space.step(layer, origin_groups=groups)
            self.wave_control_cost = checked_work(
                self.wave_control_cost + self.events.model_cost - before_cost
            )
            self._wave_interactions(reads)

    def _wave_interactions(self, reads: tuple[tuple[tuple[int, int, int], int], ...]) -> None:
        waves = self.space.waves
        if waves is None:
            return
        # Price the bounded bank inspection independently of carrier cycles.
        for address, count in reads:
            if count:
                cost = bounded(checked_work(count * self.initial.operation_costs.price("read")))
                self.events.append(
                    tick=self.space.tick,
                    addresses=(address,),
                    owner="resolver",
                    kind="wave-check",
                    model_cost=cost,
                )
                self.wave_control_cost = checked_work(self.wave_control_cost + cost)
        for binding in self.program.wave_interactions:
            bank = waves.banks[binding.address]
            origins = tuple(waves.names[name] for name in binding.origins)
            if any(not waves.relevant(origin) for origin in origins):
                head = self.space.heads[binding.register_index]
                if self._null_certificates.get(binding.address) != head:
                    self.events.require_room(1)
                    self.space.require_null_cancellation(
                        binding.instrument, binding.register_index, binding.null_outcome
                    )
                    self.events.append(
                        tick=self.space.tick,
                        addresses=(binding.address,),
                        owner="resolver",
                        kind="wave-null-check",
                        parents=origins,
                        model_cost=1,
                    )
                    self.wave_control_cost = checked_work(self.wave_control_cost + 1)
                    self._null_certificates[binding.address] = head
                bank.consume()
                continue
            if bank.event_id is None or bank.event_id == bank.consumed_id:
                continue
            if not waves.local(binding.address, origins):
                bank.consume()
                continue
            self.events.require_room(2)
            trigger = self.events.append(
                tick=self.space.tick,
                addresses=(binding.address,),
                owner="resolver",
                kind="wave-request",
                physical_parents=(bank.event_id,),
                model_cost=1,
            )
            record = self.space.interact(
                trigger.id,
                binding.register_index,
                binding.instrument,
                cause=trigger.id,
                origins=origins,
                terminal_origins=tuple(waves.names[name] for name in binding.terminal_origins),
                terminal_outcomes=binding.terminal_outcomes,
                null_outcome=binding.null_outcome,
                sample=self._sample,
            )
            assert record is not None  # Relevance and publication share this transaction.
            self.wave_control_cost = checked_work(self.wave_control_cost + 1)
            bank.consume()

    def report(self) -> dict[str, object]:
        return {
            "model": "local-quantum-events-v3"
            if self.space.waves is not None
            else (
                "local-quantum-events-v2"
                if any(e.channel for e in self.space.events) or self.space.config.dimensions
                else "local-quantum-events-v1"
            ),
            "register_dimensions": self.space.config.local_dimensions,
            "register_names": self.space.config.register_names,
            "node_event_heads": [
                {
                    "address": address,
                    "streams": [
                        {
                            "stream_id": cursor.stream_id,
                            "event_id": cursor.head,
                            "physical_tick": cursor.physical_tick,
                        }
                        for cursor in self.events.cursors_at(address)
                    ],
                }
                for address in self.events.stream_addresses
            ],
            "tick": self.space.tick,
            "oracle_calls": self.owner.query_stats.successful_queries,
            "oracle_direct_world_ticks": 0,
            "random_draws": self.draws,
            "controller_overhead_cost": self.overhead_cost,
            "wave_control_cost": self.wave_control_cost,
            "host_cancellation_checks": self.space.cancellation_checks,
            "wave_origins": []
            if self.space.waves is None
            else [asdict(s) for s in self.space.waves.states],
            "node_wave_origins": []
            if self.space.waves is None
            else [
                {
                    "address": address,
                    "origins": bank.origins,
                    "event_id": bank.event_id,
                    "consumed_id": bank.consumed_id,
                }
                for address, bank in self.space.waves.banks.items()
            ],
            "host_candidate_plans": self.host_plans,
            "host_evaluated_quantum_nodes": self.owner.query_stats.host_evaluated_nodes,
            "records": [asdict(record) for record in self.space.records],
            "quantum_payloads": [asdict(event) for event in self.space.events],
        }


def build_event_runtime(initial: InitialState) -> tuple[CausalEventSpace | None, EventResolver | None]:
    if initial.event_program is None:
        return None, None
    program = parse_event_program(initial)
    events = CausalEventSpace(
        program.capacity, shape=initial.shape, boundary=initial.boundary, link_ticks=initial.link_ticks
    )
    resolver: EventResolver | None
    if program.contacts is not None:
        from .contact_runtime import ContactEventResolver

        if program.contacts.causal_sources:
            from .causal_contact_runtime import CausalContactResolver

            resolver = CausalContactResolver(initial, program, events)
        else:
            resolver = ContactEventResolver(initial, program, events)
    else:
        resolver = None if program.network is None else NativeEventResolver(initial, program, events)
    return events, resolver

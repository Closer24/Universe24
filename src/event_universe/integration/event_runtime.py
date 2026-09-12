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
    """One configured bounded rule per site; new local arrivals can trigger again."""

    def __init__(self, initial: InitialState, program: Program, events: CausalEventSpace) -> None:
        if program.network is None:
            raise ValueError("quantum configuration required by this resolver")
        self.initial = initial
        self.program = program
        self.events = events
        self.owner = DeferredQuantum()
        self.space = self.owner.bind_event_network(program.network, event_space=events)
        self.layers = dict(program.layers)
        self.bindings = {b.address: b for b in program.bindings}
        self.rng = Random(program.seed)
        self.draws = 0
        self.host_plans = 0
        self.overhead_cost = 0

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
        decision = self.space.prepare(trigger.id, binding.site, binding.instrument, cause=trigger.id)
        ticket = None
        if sum(weight > 0 for weight in decision.weights) > 1:
            if self.program.tickets is None:
                ticket = self.rng.randrange(decision.total_weight)
            else:
                if self.draws >= len(self.program.tickets):
                    raise ValueError("supplied ticket stream exhausted")
                ticket = self.program.tickets[self.draws]
            self.draws = checked_work(self.draws + 1)
        record = self.space.commit(decision, ticket)
        self.overhead_cost = checked_work(self.overhead_cost + overhead)
        return replace(plans[record.outcome], cause_id=record.event_id)

    def advance(self, tick: int) -> None:
        if tick != self.space.tick + 1:
            raise ValueError("native scheduler must advance the recipe clock once")
        layer = self.layers.get(tick, ())
        for _, sites in layer:
            if (
                len(sites) == 2
                and self.space.config.addresses[sites[0]] != self.space.config.addresses[sites[1]]
            ):
                for q in sites:
                    previous = self.events.event(self.space.heads[q])
                    if tick - previous.tick < self.initial.link_ticks:
                        raise ValueError("coherent neighbor operation precedes physical link time")
        self.space.step(layer)

    def report(self) -> dict[str, object]:
        return {
            "model": "local-quantum-events-v2"
            if any(e.channel for e in self.space.events) or self.space.config.dimensions
            else "local-quantum-events-v1",
            "register_dimensions": self.space.config.local_dimensions,
            "register_names": self.space.config.register_names,
            "tick": self.space.tick,
            "oracle_calls": self.owner.query_stats.successful_queries,
            "oracle_direct_world_ticks": 0,
            "random_draws": self.draws,
            "controller_overhead_cost": self.overhead_cost,
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
    resolver = None if program.network is None else NativeEventResolver(initial, program, events)
    return events, resolver

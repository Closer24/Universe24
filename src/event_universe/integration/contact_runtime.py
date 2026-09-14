"""Commit-time transfer between local records and finite quantum domains."""

from dataclasses import dataclass, replace

from event_universe.core.disturbance_state import (
    DisturbanceRecord,
    InitialState,
    LocalPlan,
    Values,
    bounded,
    unpack,
)
from event_universe.core.event_resolution import LocalContext, Planner
from event_universe.core.event_space import CausalEventSpace
from event_universe.core.integer import checked_work
from event_universe.quantum import LocalUnitary

from .contact_program import ContactDomain
from .event_program import Program
from .event_runtime import NativeEventResolver


@dataclass(frozen=True, slots=True)
class ContactReservation:
    domain: int
    source: bool
    slots: tuple[int, int]
    locked: tuple[int, ...] = ()


class ContactEventResolver(NativeEventResolver):
    """Quantum ownership changes only inside a preflighted local Node commit."""

    def __init__(self, initial: InitialState, program: Program, events: CausalEventSpace) -> None:
        super().__init__(initial, program, events)
        assert program.contacts is not None
        self.domains = program.contacts.domains
        self._sources = {
            self.space.config.addresses[q]: i
            for i, d in enumerate(self.domains)
            for q in (d.source_registers or (d.source_register,))
        }
        self._captures = {
            self.space.config.addresses[q]: (i, q)
            for i, d in enumerate(self.domains)
            for q in d.captures
        }
        self._pending: dict[int, ContactReservation] = {}
        self._transfers: list[dict[str, object]] = []

    def _contact(self, context: LocalContext) -> ContactReservation | None:
        domain_index = self._sources.get(context.address)
        if domain_index is not None:
            domain = self.domains[domain_index]
            for slot, record in enumerate(context.records):
                if (
                    record is not None
                    and record.type_index == domain.source_type
                    and unpack(record.values[domain.validity_field]) == (domain.unknown_value,)
                ):
                    partner = next(
                        (
                            i
                            for i, r in enumerate(context.records)
                            if i != slot and r is not None and r.type_index == domain.partner_type
                        ),
                        None,
                    )
                    if partner is not None:
                        return ContactReservation(domain_index, True, (slot, partner))
        capture = self._captures.get(context.address)
        if capture is None:
            return None
        domain_index, _ = capture
        domain = self.domains[domain_index]
        # A successful local result is observable here and ends this detector's
        # repeated attempts. A remote resolution never selects the attempt clock.
        output_types = {domain.output.type_index} | {
            result.output.type_index for result in domain.capture_outcomes if result.output is not None
        }
        if any(r is not None and r.type_index in output_types for r in context.records):
            return None
        detector = next(
            (
                i
                for i, r in enumerate(context.records)
                if r is not None and r.type_index == domain.detector_type
            ),
            None,
        )
        if detector is None:
            return None
        empty = next((i for i, r in enumerate(context.records) if r is None), -1)
        if domain.capture_outcomes and not any(o.effect == "localized" for o in domain.capture_outcomes):
            empty = detector
        return ContactReservation(domain_index, False, (detector, empty))

    def funded_fields(self, domain: ContactDomain) -> tuple[int, ...]:
        """Fields whose stock the wave pays into the field; none in the plain profile."""
        return ()

    def has_work(self, context: LocalContext) -> bool:
        return self._contact(context) is not None

    def resolve(self, context: LocalContext, planner: Planner) -> LocalPlan:
        reservation = self._contact(context)
        if reservation is None:
            return planner(context.records, context.residuals, context.received)
        if context.tick != self.space.tick:
            raise ValueError("contact and quantum clocks disagree")
        if -1 in reservation.slots:
            raise OverflowError("localized capture requires an available output slot")
        reservation = replace(
            reservation,
            locked=tuple(
                i
                for i, record in enumerate(context.records)
                if record is not None or i in reservation.slots
            ),
        )
        token = self.space.config.addresses.index(context.address)
        if token in self._pending:
            raise ValueError("one pending contact per local Node is allowed")
        self._pending[token] = reservation
        try:
            self.alternatives(context, token)
        except Exception:
            del self._pending[token]
            raise
        prices = self.initial.operation_costs
        cost = bounded(
            2 * prices.price("read") + 2 * prices.price("update") + prices.price("commit") + 1
        )
        self.overhead_cost = checked_work(self.overhead_cost + cost)
        return LocalPlan(
            tuple((i, context.records[i]) for i in reservation.locked),
            (),
            context.residuals,
            (),
            cost,
            resolution_token=token,
        )

    def _reservation(
        self, context: LocalContext, token: int
    ) -> tuple[ContactReservation, ContactDomain]:
        if token not in self._pending or self.space.config.addresses[token] != context.address:
            raise ValueError("unknown or nonlocal contact reservation")
        reservation = self._pending[token]
        return reservation, self.domains[reservation.domain]

    def alternatives(
        self, context: LocalContext, token: int
    ) -> tuple[tuple[tuple[int, DisturbanceRecord | None], ...], ...]:
        reservation, domain = self._reservation(context, token)
        first, second = reservation.slots
        if reservation.source:
            assert self.space.waves is not None
            self.space.waves.check_activation(domain.name)
            record, partner = context.records[first], context.records[second]
            if (
                record is None
                or record.type_index != domain.source_type
                or partner is None
                or partner.type_index != domain.partner_type
                or unpack(record.values[domain.validity_field]) != (domain.unknown_value,)
            ):
                raise ValueError("reserved contact participants or validity changed")
            paid = self.funded_fields(domain)
            if any(
                f.conserved and i not in paid and record.values[i] != domain.output.values[i]
                for i, f in enumerate(self.initial.fields)
            ):
                raise ValueError("contact inventory differs from its declared capture template")
            for i in paid:
                if any(
                    have > full
                    for have, full in zip(
                        unpack(record.values[i]), unpack(domain.output.values[i]), strict=True
                    )
                ):
                    raise ValueError("funded stock cannot exceed its declared template")
            records = list(context.records)
            records[first] = None
            return (tuple((i, records[i]) for i in reservation.locked),)
        detector = context.records[first]
        if (
            detector is None
            or detector.type_index != domain.detector_type
            or context.records[second] is not None
        ):
            raise ValueError("reserved detector or capture slot changed")
        clicked = list(context.records)
        clicked[second] = domain.output
        return (
            tuple((i, context.records[i]) for i in reservation.locked),
            tuple((i, clicked[i]) for i in reservation.locked),
        )

    def commit_choice(self, context: LocalContext, token: int, following_events: int) -> tuple[int, int]:
        with self.events.transaction():
            reservation, domain = self._reservation(context, token)
            if context.tick != self.space.tick:
                raise ValueError("committed contact and quantum clocks disagree")
            self.alternatives(context, token)
            # Include the ordinary Node's following cycle_committed event.
            self.events.require_room((3 if reservation.source else 2) + following_events)
            trigger = self.events.append(
                tick=context.tick,
                addresses=(context.address,),
                owner="resolver",
                kind="contact-request",
                physical_parents=() if context.cause is None else (context.cause,),
            )
            assert self.space.waves is not None
            waves = self.space.waves
            if reservation.source:
                assert domain.preparation is not None
                event_id = self.space.activate_contact(domain.name, domain.preparation, trigger.id)
                outcome = 0
            else:
                register = self._captures[context.address][1]
                origin = waves.names.get(domain.name)
                origins = (
                    () if origin is None or not waves.local(context.address, (origin,)) else (origin,)
                )
                decision = self.space.prepare(
                    trigger.id,
                    register,
                    domain.instrument,
                    cause=trigger.id,
                    origins=origins,
                    terminal_origins=origins,
                    terminal_outcomes=(1,) if origins else (),
                    null_outcome=0,
                )
                if decision.weights[1] and not origins:
                    raise ValueError("occupied capture requires a causally delivered origin")
                ticket = (
                    self._sample(decision.total_weight)
                    if sum(w > 0 for w in decision.weights) > 1
                    else None
                )
                result = self.space.commit(decision, ticket)
                event_id, outcome = result.event_id, result.outcome
            if reservation.source or outcome == 1:
                self._transfers.append(
                    {
                        "domain": domain.name,
                        "tick": context.tick,
                        "address": context.address,
                        "event_id": event_id,
                        "direction": "to_quantum" if reservation.source else "to_localized",
                    }
                )
            del self._pending[token]
            return outcome, event_id

    def propagation_phase(
        self, tick: int, domain: ContactDomain
    ) -> tuple[tuple[LocalUnitary, tuple[int, ...]], ...]:
        operations = []
        for rule, registers in domain.phases[(tick - 1) % len(domain.phases)]:
            if not isinstance(rule, LocalUnitary):
                raise ValueError("field phases require the causal source owner")
            operations.append((rule, registers))
        return tuple(operations)

    def begin_tick(self, tick: int) -> None:
        if tick != self.space.tick + 1:
            raise ValueError("contact clock must advance once per simulation tick")
        waves = self.space.waves
        assert waves is not None
        operations = []
        groups = []
        reads = tuple((address, len(bank.origins)) for address, bank in waves.banks.items())
        for domain in self.domains:
            origin = waves.names.get(domain.name)
            if origin is None:
                continue
            for rule, registers in self.propagation_phase(tick, domain):
                if len(registers) == 2 and any(
                    tick - self.space.physical_ticks[q] < self.initial.link_ticks for q in registers
                ):
                    continue
                operations.append((rule, registers))
                groups.append((origin,))
        live = [
            (rule, qs)
            for (rule, qs), ids in zip(operations, groups, strict=True)
            if waves.operation_live(ids, qs)
        ]
        self.events.require_room(len(operations) + len(live) + sum(count > 0 for _, count in reads))
        self.space.step(tuple(operations), origin_groups=tuple(groups))
        price = self.initial.operation_costs.price
        for address, count in reads:
            if count:
                cost = bounded(count * price("read"))
                self.events.append(
                    tick=tick,
                    addresses=(address,),
                    owner="resolver",
                    kind="contact-wave-check",
                    model_cost=cost,
                )
                self.wave_control_cost = checked_work(self.wave_control_cost + cost)
        for _, qs in live:
            cost = bounded(
                price("evaluate")
                + len(qs) * price("read")
                + (price("send") + price("receive") if len(qs) == 2 else 0)
            )
            self.events.append(
                tick=tick,
                addresses=tuple(self.space.config.addresses[q] for q in qs),
                owner="resolver",
                kind="contact-wave-operation",
                model_cost=cost,
            )
            self.wave_control_cost = checked_work(self.wave_control_cost + cost)

    def advance(self, tick: int) -> None:
        if tick != self.space.tick:
            raise ValueError("contact clock must be synchronized before local commits")

    def inventory(self) -> Values:
        """Read-only sector accounting; no physical callback consumes this sum."""
        values = [[0] * f.components for f in self.initial.fields]
        assert self.space.waves is not None
        for domain in self.domains:
            origin = self.space.waves.names.get(domain.name)
            count = int(origin is not None and self.space.waves.relevant(origin))
            for i, codes in enumerate(domain.output.values):
                for component, value in enumerate(unpack(codes)):
                    values[i][component] = checked_work(values[i][component] + count * value)
        return tuple(tuple(v) for v in values)

    def report(self) -> dict[str, object]:
        return {
            **super().report(),
            "model": "localized-contact-quantum-v1",
            "classical_field_source": "localized_events_only",
            "quantum_inventory": {
                f.name: v
                for f, v in zip(self.initial.fields, self.inventory(), strict=True)
                if f.conserved
            },
            "contact_transfers": list(self._transfers),
        }

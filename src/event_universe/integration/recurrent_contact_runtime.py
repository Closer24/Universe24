"""Configured contact outcomes with finite, isolated source generations."""

from dataclasses import replace

from event_universe.core.disturbance_state import DisturbanceRecord, LocalPlan, bounded, unpack
from event_universe.core.event_resolution import LocalContext, Planner
from event_universe.core.integer import checked_work

from .causal_contact_runtime import CausalContactResolver


class RecurrentContactResolver(CausalContactResolver):
    """Ordinary sources learn a new generation only at a local result or a Link arrival."""

    def resolve(self, context: LocalContext, planner: Planner) -> LocalPlan:
        plan = super().resolve(context, planner)
        if plan.resolution_token is None:
            return plan
        # Reserve the same possible stop-and-activate work for every outcome.
        price = self.initial.operation_costs.price
        extra = bounded(3 * len(self._source_banks) * price("update") + price("commit"))
        self.overhead_cost = checked_work(self.overhead_cost + extra)
        return replace(plan, cost=bounded(plan.cost + extra))

    def alternatives(
        self, context: LocalContext, token: int
    ) -> tuple[tuple[tuple[int, DisturbanceRecord | None], ...], ...]:
        reservation, domain = self._reservation(context, token)
        first, second = reservation.slots
        assert self.space.waves is not None
        waves = self.space.waves
        generation = waves.generations.get(domain.name, 0)
        outcomes = domain.source_outcomes if reservation.source else domain.capture_outcomes
        if reservation.source:
            record, partner = context.records[first], context.records[second]
            if (
                record is None
                or record.type_index != domain.source_type
                or partner is None
                or partner.type_index != domain.partner_type
                or unpack(record.values[domain.validity_field]) != (domain.unknown_value,)
            ):
                raise ValueError("reserved contact participants or validity changed")
            if any(
                f.conserved and record.values[i] != domain.output.values[i]
                for i, f in enumerate(self.initial.fields)
            ):
                raise ValueError("contact inventory differs from its declared capture template")
        else:
            detector = context.records[first]
            if detector is None or detector.type_index != domain.detector_type:
                raise ValueError("reserved detector changed")
            if (
                any(outcome.effect == "localized" for outcome in outcomes)
                and context.records[second] is not None
            ):
                raise ValueError("reserved capture slot changed")
        choices = []
        for outcome in outcomes:
            records = list(context.records)
            if reservation.source and outcome.effect == "new_wave":
                records[first] = None
            elif not reservation.source and outcome.effect == "localized":
                records[second] = outcome.output
            choices.append(tuple((i, records[i]) for i in reservation.locked))
        # These checks use bounded local banks. Exact applicability and remaining
        # quantum generation capacity are checked by prepare before any ticket.
        if any(o.effect == "new_wave" for o in outcomes) and generation < len(self._source_banks):
            self._source_banks[generation][context.address].check_activation(context.tick)
        if not reservation.source and generation:
            node = self._source_banks[generation - 1][context.address]
            if not node.retired:
                node.check_null(context.tick)
                if any(o.effect in ("localized", "new_wave") for o in outcomes):
                    node.check_capture(
                        waves.names[domain.name],
                        context.tick,
                        self._ports_at[context.address],
                        0,
                        self.initial.link_ticks,
                    )
        if not reservation.source and any(o.effect == "null" for o in outcomes):
            for bank in self._source_banks:
                if not bank[context.address].retired:
                    bank[context.address].check_null(context.tick)
        return tuple(choices)

    def commit_choice(self, context: LocalContext, token: int, following_events: int) -> tuple[int, int]:
        with self.events.transaction():
            reservation, domain = self._reservation(context, token)
            if context.tick != self.space.tick:
                raise ValueError("committed contact and quantum clocks disagree")
            self.alternatives(context, token)
            assert self.space.waves is not None
            waves = self.space.waves
            generation = waves.generations.get(domain.name, 0)
            definitions = domain.source_outcomes if reservation.source else domain.capture_outcomes
            effects = tuple(outcome.effect for outcome in definitions)
            instrument = domain.source_instrument if reservation.source else domain.instrument
            assert instrument is not None
            register = self.space.config.addresses.index(context.address)
            old = waves.names.get(domain.name)
            origins = (
                ()
                if reservation.source or old is None or not waves.local(context.address, (old,))
                else (old,)
            )
            terminal = (
                tuple(i for i, effect in enumerate(effects) if effect in ("localized", "new_wave"))
                if origins
                else ()
            )
            # Reserve the trigger, result, fresh origin and possible old local stop.
            self.events.require_room(4 + following_events)
            # A prepared decision uses the prospective local request identity;
            # all quantum bounds are validated before publishing that request.
            record_id = self.events.next_id
            decision = self.space.prepare(
                record_id,
                register,
                instrument,
                origins=origins,
                terminal_origins=origins if terminal else (),
                terminal_outcomes=terminal,
                null_outcome=None if reservation.source else 0,
                contact_effects=effects,
                contact_source=reservation.source,
            )
            if any(decision.weights[i] for i, effect in enumerate(effects) if effect == "new_wave"):
                self._source_banks[generation][context.address].check_activation(context.tick)
            trigger = self.events.append(
                tick=context.tick,
                addresses=(context.address,),
                owner="resolver",
                kind="contact-request",
                physical_parents=() if context.cause is None else (context.cause,),
            )
            if trigger.id != record_id:
                raise ValueError("contact request identity changed during its transaction")
            decision = self.space.bind_contact_request(decision, trigger.id)
            ticket = (
                self._sample(decision.total_weight) if sum(w > 0 for w in decision.weights) > 1 else None
            )
            result = self.space.commit(decision, ticket)
            effect = effects[result.outcome]
            if not reservation.source and effect == "null":
                # A vacuum result carries no remotely selected generation.
                # Apply its declared local action to every retained bank;
                # shared quantum progress cannot choose an ordinary emitter.
                for bank in self._source_banks:
                    node = bank[context.address]
                    if not node.retired:
                        node.null(context.tick, result.event_id)
                        node.pending_emission = None
            elif not reservation.source and generation:
                node = self._source_banks[generation - 1][context.address]
                if effect in ("localized", "new_wave"):
                    assert old is not None
                    node.capture(
                        old,
                        context.tick,
                        result.event_id,
                        self._ports_at[context.address],
                        0,
                        self.initial.link_ticks,
                        self._source_events,
                    )
                    node.pending_emission = None
            origin = old
            if effect == "new_wave":
                origin = self.space.activate_contact_result(domain.name, result)
                self._source_banks[generation][context.address].activate(
                    origin, context.tick, result.event_id
                )
                self._activation_ticks[domain.name] = context.tick
            if effect != "null":
                self._transfers.append(
                    {
                        "domain": domain.name,
                        "tick": context.tick,
                        "address": context.address,
                        "event_id": result.event_id,
                        "direction": (
                            "to_quantum"
                            if reservation.source and effect == "new_wave"
                            else "new_wave"
                            if effect == "new_wave"
                            else "to_localized"
                            if not reservation.source and effect == "localized"
                            else "retained"
                            if reservation.source
                            else "continued"
                        ),
                        "effect": effect,
                        "origin": origin,
                        "generation": waves.generations.get(domain.name, 0),
                    }
                )
            del self._pending[token]
            return result.outcome, result.event_id

    def report(self) -> dict[str, object]:
        return {
            **super().report(),
            "model": "recurrent-contact-fields-v1",
            "max_generations": len(self._source_banks),
            "source_emission_schedule": "fixed_generation_round_robin",
            "source_envelopes": [
                {
                    "position": address,
                    "generation": index + 1,
                    "origin": node.source_id,
                    "amplitude": (node.amplitude.real, node.amplitude.imag, node.amplitude.denominator),
                    "retired": bool(node.retired),
                    "terminal_ready_tick": None
                    if node.pending_stop is None
                    else node.pending_stop.ready_tick,
                }
                for index, bank in enumerate(self._source_banks)
                for address, node in bank.items()
            ],
        }

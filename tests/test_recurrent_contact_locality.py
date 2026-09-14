"""Event-time counterexamples for recurrent origin and ordinary-source isolation."""

import pytest

from event_universe.core.source_envelope_state import EnvelopeAmplitude
from event_universe.quantum import LocalInstrument

from .test_localized_quantum_contact import ROTATION, step, world_for
from .test_quantum_event_network import matrix, probability
from .test_recurrent_quantum_contact import recurrent_configuration


def test_remote_new_wave_does_not_select_the_bank_cleared_by_a_local_null():
    source, detector = (3, 1, 1), (2, 1, 1)
    prefixes = []
    for ticket, effect in ((225, "localized"), (369, "new_wave")):
        raw = recurrent_configuration()
        raw["link_ticks"] = 3
        program = raw["event_program"]
        program["max_generations"] = 2
        program["tickets"] = [ticket]
        program["addresses"] = [list(source), list(detector), [1, 1, 1]]
        domain = program["domains"][0]
        domain["capture"]["register_indices"] = [0, 1]
        domain["phases"] = [
            [{"register_indices": [0, 1], "matrix": ROTATION}],
            [],
            [],
            [],
        ]
        raw["seeds"] = [
            {"position": list(source), "type": "incoming_charge"},
            {"position": list(source), "type": "contact_probe"},
            {"position": list(detector), "type": "contact_probe"},
        ]
        world, resolver = world_for(raw)
        with world:
            step(world, 3)
            local = resolver._source_banks[0][source]
            assert local.amplitude == EnvelopeAmplitude(3, 0, 5)

            # At event tick 3 the lower-address detector commits first. Its
            # three-Link-tick notice cannot arrive at the source before tick 6.
            # The source then measures local vacuum in that same event tick.
            step(world, 1)
            transfer = resolver.report()["contact_transfers"][-1]
            assert (transfer["tick"], transfer["address"], transfer["effect"]) == (
                3,
                detector,
                effect,
            )
            record = next(
                record
                for record in resolver.space.records
                if record.decision.tick == 3 and record.decision.register_index == 1
            )
            assert record.decision.weights == (225, 144, 256)
            remote = resolver._source_banks[0][detector]
            notice = remote.output[6]  # Positive-X Port points toward the source.
            assert notice is not None and notice.amplitude is None
            assert notice.arrival_tick == 6 > world.tick
            assert local.pending_stop is None and not local.retired
            assert probability(resolver.space.query(0)) == 0
            assert local.amplitude == EnvelopeAmplitude()
            assert local.pending_emission is None
            assert resolver.draws == 1
            prefixes.append(
                (
                    local.amplitude,
                    local.emission_state,
                    world.spatial_values(source),
                    world.nodes[source].last_cost,
                )
            )
    assert prefixes[0] == prefixes[1]


def _commit_local_outcome(resolver, register, effect):
    """Exercise the quantum owner directly, independently of ordinary installation."""
    space = resolver.space
    origin = space.waves.names["charge_mode"]
    occupied = [[0, 0], [0, 1]] if effect == "new_wave" else [[0, 1], [0, 0]]
    instrument = LocalInstrument((matrix([[1, 0], [0, 0]]), matrix(occupied)))
    record_id = resolver.events.next_id
    decision = space.prepare(
        record_id,
        register,
        instrument,
        origins=(origin,),
        terminal_origins=(origin,),
        terminal_outcomes=(1,),
        null_outcome=0,
        contact_effects=("null", effect),
    )
    request = resolver.events.append(
        tick=space.tick,
        addresses=(space.config.addresses[register],),
        owner="resolver",
        kind="contact-request",
    )
    return space.commit(space.bind_contact_request(decision, request.id))


def test_replaying_a_new_wave_result_after_same_tick_absorption_cannot_reactivate_it():
    world, resolver = world_for(recurrent_configuration())
    with world:
        step(world, 1)
        space = resolver.space
        original = space.waves.names["charge_mode"]
        record = _commit_local_outcome(resolver, 1, "new_wave")
        origin = space.waves.names["charge_mode"]
        assert origin != original and space.wave_relevant(origin)
        assert not space.wave_relevant(original)
        assert resolver.inventory()[0] == (-1,)

        absorbed = _commit_local_outcome(resolver, 1, "localized")
        assert absorbed.decision.tick == record.decision.tick
        assert not space.wave_relevant(origin)
        before = (len(world.event_space.events), space.heads, space.waves.generations.copy())
        assert space.activate_contact_result("charge_mode", record) == origin
        assert space.commit(record.decision) is record
        assert before == (
            len(world.event_space.events),
            space.heads,
            space.waves.generations.copy(),
        )
        assert space.waves.names["charge_mode"] == origin
        assert not space.wave_relevant(origin)
        assert all(probability(space.query(q)) == 0 for q in range(3))
        assert resolver.inventory()[0] == (0,)


def test_local_vacuum_cannot_prepare_another_excitation_in_an_occupied_domain():
    world, resolver = world_for(recurrent_configuration())
    with world:
        step(world, 1)
        space = resolver.space
        assert probability(space.query(0)) == 0
        assert probability(space.query(1)) == 1
        before = (
            len(world.event_space.events),
            space.heads,
            space.waves.generations.copy(),
            resolver.inventory(),
            resolver.draws,
        )
        with pytest.raises(ValueError, match="entire domain to be vacuum"):
            space.prepare(
                world.event_space.next_id,
                0,
                LocalInstrument((matrix([[0, 1], [1, 0]]),)),
                contact_effects=("new_wave",),
                contact_source=True,
            )
        assert before == (
            len(world.event_space.events),
            space.heads,
            space.waves.generations.copy(),
            resolver.inventory(),
            resolver.draws,
        )
        assert probability(space.query(1)) == 1

"""Origin resolution and local propagation preserve conditional quantum results.

The finite matrices are explicit test laws. Wave references track conservative
causal support, not sampled occupation, momentum, or extra local history.
"""

from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from threading import Barrier

import pytest

from event_universe.quantum.event_network import EventNetwork, EventNetworkConfig
from event_universe.quantum.event_rules import LocalInstrument, LocalUnitary
from event_universe.quantum.wave_origins import WaveDefinition

from .test_quantum_event_network import CX, POSITION, RI, H, R, Z, matrix, probability

A, B, C = (0, 0, 0), (1, 0, 0), (2, 0, 0)
IDENTITY_PAIR = LocalUnitary(matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))))
X = LocalUnitary(matrix(((0, 1), (1, 0))))
ABSORB = LocalInstrument((matrix(((1, 0), (0, 0))), matrix(((0, 1), (0, 0)))))


def single_wave(addresses=(A, B)):
    return EventNetwork(
        EventNetworkConfig(addresses, occupied=(0,), waves=(WaveDefinition("source", 0),))
    )


def origin_of(network):
    assert network.waves is not None
    return network.waves.names["source"]


def wave_step(network, operations):
    origin = origin_of(network)
    network.step(operations, origin_groups=((origin,),) * len(operations))


def local_banks(network):
    assert network.waves is not None
    return tuple(
        (address, bank.origins, bank.event_id, bank.consumed_id)
        for address, bank in network.waves.banks.items()
    )


def fingerprint(network):
    assert network.waves is not None
    return (
        network.tick,
        network.heads,
        network.physical_ticks,
        network.event_space.events,
        network.events,
        network.records,
        network.successful_queries,
        network.host_evaluated_nodes,
        network.waves.states,
        local_banks(network),
    )


def test_configured_waves_are_distinct_from_vacuum_registers_and_bounded_per_node():
    plain = EventNetwork(EventNetworkConfig((A, B, C)))
    assert plain.waves is None
    network = EventNetwork(
        EventNetworkConfig(
            (A,) * 8 + (B,),
            register_names=tuple(f"register_{i}" for i in range(9)),
            waves=tuple(WaveDefinition(f"origin_{i}", i) for i in range(6)),
        )
    )
    assert network.waves is not None
    assert len(network.waves.banks[A].origins) == 6
    assert network.waves.banks[B].origins == ()
    assert len(network.event_space.cursors_at(A)) == 8
    assert len(network.waves.names) == 6
    assert network.config.occupied == ()
    assert all(network.event_space.resolution(origin) is None for origin in network.waves.names.values())
    with pytest.raises(ValueError, match="six initial waves"):
        EventNetworkConfig((A,), waves=tuple(WaveDefinition(f"origin_{i}", 0) for i in range(7)))


def test_seventh_arriving_wave_rejects_the_entire_layer_before_publication():
    network = EventNetwork(
        EventNetworkConfig(
            (A, B, C),
            waves=tuple(WaveDefinition(f"origin_{i}", 0) for i in range(6))
            + (WaveDefinition("seventh", 1), WaveDefinition("canary", 2)),
        )
    )
    seventh, canary = (network.waves.names[name] for name in ("seventh", "canary"))
    before = fingerprint(network)
    with pytest.raises(OverflowError, match="six"):
        network.step(((H, (2,)), (R, (0, 1))), origin_groups=((canary,), (seventh,)))
    assert fingerprint(network) == before
    network.step(((H, (2,)),), origin_groups=((canary,),))
    assert network.tick == 1
    assert probability(network.query(2)) == Fraction(1, 2)


@pytest.mark.parametrize("reverse_order", [False, True])
def test_simultaneous_disjoint_register_gates_cannot_relay_two_links(reverse_order):
    network = EventNetwork(
        EventNetworkConfig(
            (A, B, B, C),
            occupied=(0,),
            register_names=("left", "middle_in", "middle_out", "right"),
            waves=(WaveDefinition("source", 0),),
        )
    )
    origin = origin_of(network)
    operations = ((R, (0, 1)), (R, (2, 3)))
    wave_step(network, operations[::-1] if reverse_order else operations)
    assert network.waves.banks[A].origins == (origin,)
    assert network.waves.banks[B].origins == (origin,)
    assert network.waves.banks[C].origins == ()
    assert network.host_evaluated_nodes == 0
    wave_step(network, ((R, (2, 3)),))
    assert network.waves.banks[C].origins == (origin,)
    assert network.waves.banks[B] is network.event_space.references_at(B)


@pytest.mark.parametrize("contenders", [2, 6])
def test_concurrent_interactions_claim_one_origin_once(contenders):
    addresses = tuple((index, 0, 0) for index in range(contenders))
    network = single_wave(addresses)
    origin = origin_of(network)
    for index in range(1, contenders):
        wave_step(network, ((R, (index - 1, index)),))
    ready = Barrier(contenders)
    draws = []

    def force_occupied(total):
        draws.append(total)
        return total - 1

    def attempt(index):
        ready.wait(timeout=5)
        return network.interact(
            index,
            index,
            ABSORB,
            origins=(origin,),
            terminal_origins=(origin,),
            terminal_outcomes=(1,),
            null_outcome=0,
            sample=force_occupied,
        )

    with ThreadPoolExecutor(max_workers=contenders) as pool:
        replies = tuple(pool.map(attempt, range(contenders)))
    winners = tuple(reply for reply in replies if reply is not None)
    assert len(winners) == len(draws) == 1
    assert network.cancellation_checks == contenders - 1
    assert network.successful_queries - network.cancellation_checks == 1
    assert winners[0].outcome == 1
    assert network.records == winners
    assert network.event_space.resolution(origin) == winners[0].event_id
    assert network.waves.status(origin).resolution_event == winners[0].event_id
    assert not network.wave_relevant(origin)
    assert all(bank.origins == (origin,) for bank in network.waves.banks.values())


def test_correlated_distinct_origins_share_conditional_commit_serialization():
    network = EventNetwork(
        EventNetworkConfig((A, B), waves=(WaveDefinition("left", 0), WaveDefinition("right", 1)))
    )
    origins = tuple(network.waves.names.values())
    network.step(((H, (0,)),), origin_groups=((origins[0],),))
    network.step(((CX, (0, 1)),), origin_groups=(origins,))
    ready = Barrier(2)
    draws = []

    def choose_zero(total):
        draws.append(total)
        return 0

    def attempt(index):
        ready.wait(timeout=5)
        return network.interact(
            index,
            index,
            POSITION,
            origins=(origins[index],),
            terminal_origins=(origins[index],),
            terminal_outcomes=(0, 1),
            sample=choose_zero,
        )

    with ThreadPoolExecutor(max_workers=2) as pool:
        records = tuple(pool.map(attempt, (0, 1)))
    assert all(record is not None and record.outcome == 0 for record in records)
    assert len(draws) == 1
    assert len(network.records) == network.successful_queries == 2
    assert tuple(network.event_space.resolution(origin) for origin in origins) == tuple(
        record.event_id for record in records
    )
    assert (probability(network.query(0)), probability(network.query(1))) == (0, 0)


@pytest.mark.parametrize("first_register", [0, 1])
def test_exhaustive_conditional_click_counts_are_independent_of_detector_order(first_register):
    click_counts = [0, 0]
    for ticket in range(25):
        network = single_wave()
        wave_step(network, ((R, (0, 1)),))
        origin = origin_of(network)
        draws = []

        def sample(total, draws=draws, ticket=ticket):
            draws.append(total)
            assert total == 25
            return ticket

        first = network.interact(
            10,
            first_register,
            POSITION,
            origins=(origin,),
            terminal_origins=(origin,),
            terminal_outcomes=(1,),
            sample=sample,
        )
        assert first is not None
        active_after_first = first.outcome == 0
        assert network.wave_relevant(origin) == active_after_first
        second_register = 1 - first_register
        second = network.interact(
            11,
            second_register,
            POSITION,
            origins=(origin,),
            terminal_origins=(origin,),
            terminal_outcomes=(1,),
            null_outcome=0,
            sample=sample,
        )
        assert draws == [25]
        if active_after_first:
            assert second is not None and second.outcome == 1
            assert probability(second.decision) == 1
            click_counts[second_register] += 1
            assert network.cancellation_checks == 0
        else:
            assert second is None
            click_counts[first_register] += 1
            assert network.cancellation_checks == 1
        assert network.successful_queries == 2
        assert not network.wave_relevant(origin)
    assert click_counts == [9, 16]


def test_resolution_is_lazy_and_idle_tick_prunes_only_local_reference_slots(monkeypatch):
    network = single_wave((A, B, C))
    wave_step(network, ((R, (0, 1)),))
    origin = origin_of(network)
    before = local_banks(network)
    record = network.interact(
        10,
        1,
        ABSORB,
        origins=(origin,),
        terminal_origins=(origin,),
        terminal_outcomes=(1,),
        sample=lambda total: total - 1,
    )
    assert record is not None
    assert local_banks(network) == before
    queries = network.successful_queries

    def reject_evaluation(*args, **kwargs):
        raise AssertionError("relevance checks must not evaluate a cone or canceled requests sample")

    with monkeypatch.context() as status_only:
        status_only.setattr(network, "_evaluate", reject_evaluation)
        assert not network.wave_relevant(origin)
    assert network.successful_queries == queries
    assert (
        network.interact(
            11,
            0,
            POSITION,
            origins=(origin,),
            terminal_origins=(origin,),
            terminal_outcomes=(1,),
            null_outcome=0,
            sample=reject_evaluation,
        )
        is None
    )
    assert local_banks(network) == before
    wave_step(network, ())
    assert all(bank.origins == () for bank in network.waves.banks.values())
    assert network.successful_queries == queries + 1
    assert network.cancellation_checks == 1
    assert network.event_space.resolution(origin) == record.event_id


@pytest.mark.parametrize("first_outcome", [0, 1])
def test_stale_preparation_is_rejected_and_repeated_record_does_not_resample(first_outcome):
    network = single_wave()
    wave_step(network, ((R, (0, 1)),))
    origin = origin_of(network)
    options = dict(origins=(origin,), terminal_origins=(origin,), terminal_outcomes=(1,))
    pending = network.prepare(10, 1, POSITION, **options)
    recorded = network.interact(
        11, 0, POSITION, **options, sample=lambda total: 0 if first_outcome == 0 else total - 1
    )
    assert recorded is not None and recorded.outcome == first_outcome
    before = fingerprint(network)
    with pytest.raises(ValueError, match="network changed"):
        network.commit(pending, 0)
    with pytest.raises(ValueError, match="stale"):
        network.prepare(10, 1, POSITION, **options)
    assert fingerprint(network) == before

    def reject_draw(total):
        raise AssertionError("a repeated or certain interaction must not sample")

    assert network.interact(11, 0, POSITION, **options, sample=reject_draw) is recorded
    assert fingerprint(network) == before
    following = network.interact(12, 1, POSITION, **options, null_outcome=0, sample=reject_draw)
    if first_outcome == 0:
        assert following is not None and following.outcome == 1
        assert probability(following.decision) == 1
    else:
        assert following is None


@pytest.mark.parametrize("phase", [False, True])
@pytest.mark.parametrize("checkpoint", [False, True])
def test_phase_interference_and_origin_identity_survive_checkpoint(phase, checkpoint):
    network = single_wave()
    origin = origin_of(network)
    source = network.event_space.event(origin)
    wave_step(network, ((R, (0, 1)),))
    assert origin in network.event_space.event(network.heads[0]).parents
    assert origin not in network.events[-1].parents
    assert probability(network.query(0)) == Fraction(9, 25)
    before = local_banks(network), network.physical_ticks, network.joint_density()
    if checkpoint:
        network.checkpoint(0)
        assert (local_banks(network), network.physical_ticks, network.joint_density()) == before
        assert network.node_count == 1
    wave_step(network, ((Z, (1,)),) if phase else ())
    wave_step(network, ((RI, (0, 1)),))
    expected = Fraction(49, 625) if phase else Fraction(1)
    probabilities = probability(network.query(0)), probability(network.query(1))
    assert probabilities == (expected, 1 - expected)
    assert network.event_space.event(origin) is source
    assert network.wave_relevant(origin)
    assert network.records == ()


@pytest.mark.parametrize("checkpoint", [False, True])
def test_no_click_preserves_coherent_unmeasured_paths(checkpoint):
    network = single_wave((A, B, C))
    origin = origin_of(network)
    wave_step(network, ((R, (0, 1)),))
    wave_step(network, ((R, (1, 2)),))
    record = network.interact(
        10,
        0,
        POSITION,
        origins=(origin,),
        terminal_origins=(origin,),
        terminal_outcomes=(1,),
        sample=lambda total: 0,
    )
    assert record is not None and record.outcome == 0
    assert network.wave_relevant(origin)
    assert probability(network.query(1)) == Fraction(9, 25)
    assert probability(network.query(2)) == Fraction(16, 25)
    if checkpoint:
        before = local_banks(network), network.joint_density()
        network.checkpoint(1)
        assert (local_banks(network), network.joint_density()) == before
    wave_step(network, ((RI, (1, 2)),))
    assert tuple(probability(network.query(index)) for index in range(3)) == (0, 1, 0)
    assert network.event_space.resolution(origin) is None


@pytest.mark.parametrize("operation", ["step", "prepare", "interact"])
def test_wave_owner_rejects_unscoped_evolution_and_measurement(operation):
    network = single_wave()
    before = fingerprint(network)
    with pytest.raises(ValueError):
        if operation == "step":
            network.step(((H, (0,)),))
        elif operation == "prepare":
            network.prepare(10, 0, POSITION)
        else:
            network.interact(10, 0, POSITION, origins=())
    assert fingerprint(network) == before


def test_resolved_origin_cannot_evolve_again_through_a_scheduled_gate():
    network = single_wave()
    origin = origin_of(network)
    wave_step(network, ((R, (0, 1)),))
    record = network.interact(
        10,
        1,
        ABSORB,
        origins=(origin,),
        terminal_origins=(origin,),
        terminal_outcomes=(1,),
        sample=lambda total: total - 1,
    )
    assert record is not None
    before = (
        network.heads,
        network.physical_ticks,
        network.events,
        network.joint_density(),
    )
    ledger, cost = network.event_space.events, network.event_space.model_cost
    tick = network.tick
    wave_step(network, ((RI, (0, 1)),))
    assert network.tick == tick + 1
    assert (
        network.heads,
        network.physical_ticks,
        network.events,
        network.joint_density(),
    ) == before
    assert network.event_space.events[:-1] == ledger
    assert network.event_space.events[-1].kind == "wave-skip-check"
    assert network.event_space.events[-1].parents == (origin,)
    assert network.event_space.model_cost == cost + 1
    assert network.cancellation_checks == 1
    assert tuple(probability(network.query(index)) for index in (0, 1)) == (0, 0)
    assert network.event_space.resolution(origin) == record.event_id
    assert all(bank.origins == () for bank in network.waves.banks.values())
    before = fingerprint(network)
    with pytest.raises(ValueError, match="dimension"):
        wave_step(network, ((R, (0,)),))
    assert fingerprint(network) == before


def test_resolving_one_origin_does_not_cancel_another_origins_gate():
    network = EventNetwork(
        EventNetworkConfig(
            (A, B),
            occupied=(0,),
            waves=(WaveDefinition("ended", 0), WaveDefinition("continuing", 1)),
        )
    )
    ended, continuing = tuple(network.waves.names.values())
    record = network.interact(
        10,
        0,
        POSITION,
        origins=(ended,),
        terminal_origins=(ended,),
        terminal_outcomes=(1,),
    )
    assert record is not None
    old_heads, old_ticks, event_count = (
        network.heads,
        network.physical_ticks,
        network.event_space.next_id,
    )
    network.step(((Z, (0,)), (H, (1,))), origin_groups=((ended,), (continuing,)))
    assert network.heads[0] == old_heads[0]
    assert network.physical_ticks[0] == old_ticks[0]
    assert network.heads[1] != old_heads[1]
    assert network.physical_ticks[1] == 1
    assert network.event_space.next_id == event_count + 2
    assert tuple(event.kind for event in network.event_space.events[event_count:]) == (
        "operation",
        "wave-skip-check",
    )
    assert tuple(probability(network.query(index)) for index in (0, 1)) == (1, Fraction(1, 2))
    assert network.event_space.resolution(ended) == record.event_id
    assert network.event_space.resolution(continuing) is None
    assert network.waves.banks[A].origins == ()
    assert network.waves.banks[B].origins == (continuing,)


def test_remote_resolution_cannot_silently_disable_a_state_changing_gate():
    network = single_wave((A, B, C))
    origin = origin_of(network)
    wave_step(network, ((IDENTITY_PAIR, (0, 1)),))
    wave_step(network, ((IDENTITY_PAIR, (1, 2)),))
    assert network.tick == 2
    assert network.waves.banks[C].origins == (origin,)
    record = network.interact(
        10,
        0,
        POSITION,
        origins=(origin,),
        terminal_origins=(origin,),
        terminal_outcomes=(1,),
    )
    assert record is not None
    assert probability(network.query(2)) == 0
    before = (
        network.tick,
        network.heads,
        network.physical_ticks,
        network.event_space.events,
        network.events,
        network.records,
        network.joint_density(),
        local_banks(network),
    )
    with pytest.raises(ValueError, match="retired-origin operation changes retained quantum state"):
        wave_step(network, ((X, (2,)),))
    assert (
        network.tick,
        network.heads,
        network.physical_ticks,
        network.event_space.events,
        network.events,
        network.records,
        network.joint_density(),
        local_banks(network),
    ) == before


def test_cancellation_checks_joint_phase_even_when_local_marginals_do_not_change():
    network = EventNetwork(EventNetworkConfig((A, B, C), waves=(WaveDefinition("source", 0),)))
    origin = origin_of(network)
    wave_step(network, ((H, (0,)),))
    wave_step(network, ((CX, (0, 1)),))
    wave_step(network, ((IDENTITY_PAIR, (1, 2)),))
    record = network.interact(
        10,
        2,
        POSITION,
        origins=(origin,),
        terminal_origins=(origin,),
        terminal_outcomes=(0,),
    )
    assert record is not None
    assert tuple(probability(network.query(index)) for index in (0, 1)) == (Fraction(1, 2),) * 2
    before = (
        network.tick,
        network.heads,
        network.physical_ticks,
        network.event_space.events,
        network.events,
        network.records,
        network.joint_density(),
        local_banks(network),
    )
    with pytest.raises(ValueError, match="retired-origin operation changes retained quantum state"):
        wave_step(network, ((Z, (0,)),))
    assert (
        network.tick,
        network.heads,
        network.physical_ticks,
        network.event_space.events,
        network.events,
        network.records,
        network.joint_density(),
        local_banks(network),
    ) == before


@pytest.mark.parametrize("kind", ["missing_null", "wrong_null", "random_record", "state_change"])
def test_retired_instrument_requires_one_inert_explicit_null_outcome(kind):
    network = single_wave()
    origin = origin_of(network)
    record = network.interact(
        10,
        0,
        ABSORB,
        origins=(origin,),
        terminal_origins=(origin,),
        terminal_outcomes=(1,),
    )
    assert record is not None
    identity = matrix(((1, 0), (0, 1)))
    instrument, null = ABSORB, 0
    if kind == "missing_null":
        null = None
    elif kind == "wrong_null":
        null = 1
    elif kind == "random_record":
        instrument = LocalInstrument((identity, identity))
    else:
        instrument = LocalInstrument((X.matrix,))
    before = (
        network.tick,
        network.heads,
        network.physical_ticks,
        network.event_space.events,
        network.events,
        network.records,
        network.joint_density(),
        local_banks(network),
    )

    def reject_draw(total):
        raise AssertionError("a retired instrument must not draw an outcome")

    with pytest.raises(ValueError):
        network.interact(
            11,
            0,
            instrument,
            origins=(origin,),
            null_outcome=null,
            sample=reject_draw,
        )
    assert (
        network.tick,
        network.heads,
        network.physical_ticks,
        network.event_space.events,
        network.events,
        network.records,
        network.joint_density(),
        local_banks(network),
    ) == before


def test_origin_that_has_not_arrived_does_not_evaluate_or_sample(monkeypatch):
    network = single_wave()
    origin = origin_of(network)
    before = fingerprint(network)

    def reject_evaluation(*args, **kwargs):
        raise AssertionError("a source that has not arrived cannot trigger quantum work")

    monkeypatch.setattr(network, "_evaluate", reject_evaluation)
    assert (
        network.interact(
            10,
            1,
            POSITION,
            origins=(origin,),
            terminal_origins=(origin,),
            terminal_outcomes=(1,),
            sample=reject_evaluation,
        )
        is None
    )
    assert fingerprint(network) == before

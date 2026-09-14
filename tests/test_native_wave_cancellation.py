"""Native scheduling may suppress only certified inert retired-wave work."""

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.integration.event_runtime import NativeEventResolver
from event_universe.quantum.event_rules import LocalInstrument

from .test_native_wave_origins import configuration
from .test_quantum_event_network import matrix, probability

IDENTITY = [[1, 0], [0, 1]]
FLIP = [[0, 1], [1, 0]]
POSITION = [[[1, 0], [0, 0]], [[0, 0], [0, 1]]]


def start(raw, ticks):
    world = Simulation(parse_initial_state(raw))
    assert isinstance(world._resolver, NativeEventResolver)
    for _ in range(ticks):
        world.step()
    return world, world._resolver


def quantum_snapshot(network):
    return (
        network.heads,
        network.physical_ticks,
        network.events,
        network.records,
        network.joint_density(),
    )


def null_certificates(world):
    return tuple(event for event in world.event_space.events if event.kind == "wave-null-check")


def test_native_remote_flip_after_retirement_rejects_before_gate_publication():
    raw = configuration()
    program = raw["event_program"]
    program["layers"] = program["layers"][:2] + [
        {
            "tick": 3,
            "operations": [{"register_indices": [0], "origins": ["signal"], "matrix": FLIP}],
        }
    ]
    world, resolver = start(raw, 2)
    network = resolver.space
    signal = network.waves.names["signal"]
    record = network.records[0]
    assert record.outcome == 1
    assert world.event_space.event(record.event_id).addresses == ((2, 0, 0),)
    assert world.event_space.resolution(signal) == record.event_id
    assert probability(network.query(0)) == 0
    before = quantum_snapshot(network), world.event_space.events, network.tick
    draws = resolver.draws
    with pytest.raises(ValueError, match="retired-origin operation changes retained quantum state"):
        world.step()
    assert world.faulted
    assert (quantum_snapshot(network), world.event_space.events, network.tick) == before
    assert resolver.draws == draws


@pytest.mark.parametrize("instrument", ["position", "random_record"])
def test_native_terminal_record_requires_a_true_null_on_later_cancellation(instrument):
    raw = configuration()
    program = raw["event_program"]
    program["layers"] = program["layers"][:2]
    contact = program["wave_interactions"][0]
    if instrument == "position":
        contact["instrument"] = POSITION
    else:
        contact.update(instrument=[IDENTITY, IDENTITY], terminal_outcomes=[0, 1])
        program["tickets"] = [0]
    world, resolver = start(raw, 2)
    network = resolver.space
    signal = network.waves.names["signal"]
    assert world.event_space.resolution(signal) == network.records[0].event_id
    if instrument == "position":
        assert probability(network.query(2)) == 1
    before = quantum_snapshot(network)
    draws, checks = resolver.draws, network.cancellation_checks
    assert null_certificates(world) == ()
    with pytest.raises(ValueError, match="not an inert certain null outcome"):
        world.step()
    assert world.faulted
    assert quantum_snapshot(network) == before
    assert resolver.draws == draws
    assert network.cancellation_checks == checks + 1
    assert null_certificates(world) == ()


@pytest.mark.parametrize("change_occupation", [False, True])
def test_native_null_certificate_tracks_target_head_even_without_bank_activation(change_occupation):
    raw = configuration()
    raw["event_program"]["layers"] = raw["event_program"]["layers"][:2]
    world, resolver = start(raw, 3)
    network = resolver.space
    waves = network.waves
    signal, probe = (waves.names[name] for name in ("signal", "probe"))
    bank = waves.banks[(2, 0, 0)]
    assert not network.wave_relevant(signal)
    assert network.wave_relevant(probe)
    assert len(null_certificates(world)) == 1
    assert probability(network.query(2)) == 0
    stamp, old_head = bank.event_id, network.heads[2]
    # Another active local origin can change this register without a new bank
    # arrival. A certificate keyed only by the bank stamp would miss the change.
    rule = LocalInstrument((matrix(FLIP if change_occupation else IDENTITY),))
    record = network.interact(500, 2, rule, origins=(probe,))
    assert record is not None
    assert network.heads[2] == record.event_id != old_head
    assert bank.event_id == stamp
    assert probability(network.query(2)) == int(change_occupation)
    before = quantum_snapshot(network)
    checks, certificates, draws = network.cancellation_checks, null_certificates(world), resolver.draws
    if change_occupation:
        with pytest.raises(ValueError, match="not an inert certain null outcome"):
            world.step()
        assert world.faulted
        assert null_certificates(world) == certificates
    else:
        world.step()
        assert not world.faulted
        assert len(null_certificates(world)) == len(certificates) + 1
        assert null_certificates(world)[-1].tick == 4
    assert network.cancellation_checks == checks + 1
    assert quantum_snapshot(network) == before
    assert bank.event_id == stamp
    assert resolver.draws == draws
    if not change_occupation:
        checks, certificates = network.cancellation_checks, null_certificates(world)
        world.step()
        assert network.cancellation_checks == checks
        assert null_certificates(world) == certificates

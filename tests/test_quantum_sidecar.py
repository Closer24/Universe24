import pytest

from event_universe.integration.quantum_bridge import QuantumBridge
from event_universe.quantum import DeferredQuantum, QuantumConfig


def test_deferred_interference_is_not_evaluated_until_measurement():
    q = DeferredQuantum()
    bridge = QuantumBridge(q)
    start = bridge.prepare(1, (10, 10, 10), 0, 1)
    left = bridge.phase(start, (11, 10, 10), 1, 0)
    right = bridge.phase(start, (10, 11, 10), 1, 2)
    detector = bridge.interfere(left, right, (11, 11, 10), 2)

    # Four fixed-width history nodes exist; no amplitude evaluation API has been called.
    assert q.node_count == 4
    result = bridge.measure(2, detector)
    assert result.amplitude == (0, 0)
    assert result.weight == 0
    assert result.evaluation_nodes == 4


def test_constructive_interference_uses_same_bridge():
    q = DeferredQuantum()
    bridge = QuantumBridge(q)
    start = bridge.prepare(1, (10, 10, 10), 0, 1)
    left = bridge.phase(start, (11, 10, 10), 1, 0)
    right = bridge.phase(start, (10, 11, 10), 1, 0)
    detector = bridge.interfere(left, right, (11, 11, 10), 2)
    result = bridge.measure(2, detector)
    assert result.amplitude == (2, 0)
    assert result.weight == 4


def test_quantum_history_is_budgeted_and_never_silently_grows():
    q = DeferredQuantum(QuantumConfig(max_nodes=2, max_eval_nodes=2))
    bridge = QuantumBridge(q)
    start = bridge.prepare(1, (0, 0, 0), 0, 1)
    bridge.phase(start, (1, 0, 0), 1, 0)
    with pytest.raises(OverflowError, match="node budget"):
        bridge.phase(start, (0, 1, 0), 1, 0)


def test_backward_time_link_is_rejected_at_bridge():
    q = DeferredQuantum()
    bridge = QuantumBridge(q)
    start = bridge.prepare(1, (0, 0, 0), 5, 1)
    with pytest.raises(ValueError, match="precede"):
        bridge.phase(start, (1, 0, 0), 4, 0)


def test_sidecar_query_cannot_change_simulator_state():
    from event_universe import Config, Simulation

    def make_world():
        world = Simulation(Config(nx=32, ny=32, nz=32))
        world.add_particle(1, 10, 10, 10, 1, 0, 0)
        world.add_particle(2, 14, 12, 10, -1, 0, 0)
        return world

    baseline = make_world()
    integrated = make_world()
    q = DeferredQuantum()
    bridge = QuantumBridge(q)

    for _ in range(8):
        baseline.step()
        integrated.step()

    source = bridge.prepare(100, (10, 10, 10), 0, 1)
    left = bridge.phase(source, (11, 10, 10), 1, 0)
    right = bridge.phase(source, (10, 11, 10), 1, 2)
    root = bridge.interfere(left, right, (11, 11, 10), integrated.tick)
    result = bridge.measure(101, root)
    assert result.weight == 0

    assert integrated.tick == baseline.tick
    assert dict(integrated.cells) == dict(baseline.cells)
    assert dict(integrated.particles) == dict(baseline.particles)
    assert dict(integrated.occupancy) == dict(baseline.occupancy)
    assert integrated.active == baseline.active

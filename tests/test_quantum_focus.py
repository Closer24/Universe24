"""Independent contracts for hierarchical 3D focus inside the quantum oracle."""

from pathlib import Path

import pytest

from event_universe import Config, Simulation
from event_universe.diagnostics.numeric_audit import static_integer_audit
from event_universe.integration.quantum_bridge import QuantumBridge
from event_universe.quantum import (
    DeferredQuantum,
    FocusCandidate,
    FocusRequest,
    QuantumConfig,
    Region3D,
    region_from_shape,
    split_region,
)


def _leaf_addresses(region: Region3D) -> set[tuple[int, int, int]]:
    leaves: set[tuple[int, int, int]] = set()
    stack = [region]
    while stack:
        current = stack.pop()
        if current.x1 - current.x0 == current.y1 - current.y0 == current.z1 - current.z0 == 1:
            leaves.add((current.x0, current.y0, current.z0))
        else:
            stack.extend(split_region(current))
    return leaves


def _focused_fixture():
    q = DeferredQuantum()
    bridge = QuantumBridge(q)
    specs = (
        ((1, 1, 1), 1, 10),
        ((2, 6, 3), 2, 20),
        ((7, 0, 5), 3, 30),
        ((4, 4, 4), 4, 40),
    )
    candidates = []
    for event_id, (address, amplitude, outcome) in enumerate(specs):
        root = bridge.prepare(event_id, address, 0, amplitude).quantum_node
        candidates.append(FocusCandidate(root, address, outcome))
    return q, bridge, tuple(candidates)


def test_even_cube_splits_into_exactly_eight_equal_octants():
    children = split_region(region_from_shape(8, 8, 8))
    assert len(children) == 8
    assert {(c.x1 - c.x0, c.y1 - c.y0, c.z1 - c.z0) for c in children} == {(4, 4, 4)}
    assert sum((c.x1 - c.x0) * (c.y1 - c.y0) * (c.z1 - c.z0) for c in children) == 512


def test_odd_rectangular_space_has_no_gaps_or_overlap_at_any_depth():
    region = region_from_shape(5, 7, 3)
    leaves = _leaf_addresses(region)
    expected = {(x, y, z) for x in range(5) for y in range(7) for z in range(3)}
    assert leaves == expected
    assert len(leaves) == 105


def test_non_unit_axes_only_are_split():
    children = split_region(Region3D(0, 1, 0, 5, 0, 2))
    assert len(children) == 4
    assert _leaf_addresses(Region3D(0, 1, 0, 5, 0, 2)) == {
        (0, y, z) for y in range(5) for z in range(2)
    }


def test_1024_cube_focus_reaches_one_cell_in_ten_levels():
    q = DeferredQuantum()
    bridge = QuantumBridge(q)
    address = (1000, 777, 513)
    root = bridge.prepare(1, address, 0, 1).quantum_node
    reply = bridge.focus_event(
        FocusRequest(7, region_from_shape(1024, 1024, 1024), (FocusCandidate(root, address, 5),), 0, 0)
    )
    assert reply.event is not None
    assert reply.event.address == address
    assert reply.focus_steps == 10
    assert reply.cost == (1, 0)
    assert reply.evaluation_nodes == 1
    assert all(step.child_count == 8 for step in reply.path)


def test_exhaustive_ticket_counts_match_flat_weights_exactly():
    q, bridge, candidates = _focused_fixture()
    counts = {None: 0, 10: 0, 20: 0, 30: 0, 40: 0}
    expected = {None: 2, 10: 1, 20: 4, 30: 9, 40: 16}
    for ticket in range(32):
        reply = bridge.focus_event(
            FocusRequest(100 + ticket, region_from_shape(8, 8, 8), candidates, 0, ticket, 2)
        )
        assert reply.cost == (1, 0)
        assert reply.total_weight == 32
        assert reply.event_weight == 30
        assert reply.no_event_weight == 2
        assert reply.evaluation_nodes == 4
        outcome = None if reply.event is None else reply.event.outcome
        counts[outcome] += 1
        if reply.event is None:
            assert reply.focus_steps == 0 and reply.path == ()
        else:
            assert reply.focus_steps == 3
            assert reply.path[-1].selected_weight > 0
    assert counts == expected
    assert q.node_count == 4


def test_candidate_input_order_does_not_change_spatial_focus_result():
    _, bridge_a, candidates_a = _focused_fixture()
    _, bridge_b, candidates_b = _focused_fixture()
    for ticket in range(32):
        a = bridge_a.focus_event(FocusRequest(ticket, region_from_shape(8, 8, 8), candidates_a, 0, ticket, 2))
        b = bridge_b.focus_event(
            FocusRequest(ticket, region_from_shape(8, 8, 8), tuple(reversed(candidates_b)), 0, ticket, 2)
        )
        assert (None if a.event is None else (a.event.address, a.event.outcome)) == (
            None if b.event is None else (b.event.address, b.event.outcome)
        )


def test_same_request_is_deterministic_and_never_resamples():
    _, bridge, candidates = _focused_fixture()
    request = FocusRequest(55, region_from_shape(8, 8, 8), candidates, 0, 17, 2)
    first = bridge.focus_event(request)
    second = bridge.focus_event(request)
    assert second.event == first.event
    assert second.path == first.path


def test_focus_rejects_future_or_mismatched_quantum_roots():
    q = DeferredQuantum()
    bridge = QuantumBridge(q)
    root = bridge.prepare(1, (2, 2, 2), 5, 1).quantum_node
    candidate = FocusCandidate(root, (2, 2, 2), 1)
    with pytest.raises(ValueError, match="future"):
        bridge.focus_event(FocusRequest(1, region_from_shape(8, 8, 8), (candidate,), 4, 0))
    wrong = FocusCandidate(root, (2, 2, 3), 1)
    with pytest.raises(ValueError, match="match"):
        bridge.focus_event(FocusRequest(2, region_from_shape(8, 8, 8), (wrong,), 5, 0))


def test_focus_uses_one_combined_host_evaluation_budget():
    q = DeferredQuantum(QuantumConfig(max_eval_nodes=3))
    bridge = QuantumBridge(q)
    candidates = tuple(
        FocusCandidate(bridge.prepare(i, (i, 0, 0), 0, 1).quantum_node, (i, 0, 0), i)
        for i in range(4)
    )
    with pytest.raises(OverflowError, match="evaluation budget"):
        bridge.focus_event(FocusRequest(1, region_from_shape(8, 1, 1), candidates, 0, 0))


def test_zero_total_weight_is_error_not_no_event():
    q = DeferredQuantum()
    bridge = QuantumBridge(q)
    root = bridge.prepare(1, (0, 0, 0), 0, 0).quantum_node
    with pytest.raises(ValueError, match="zero total"):
        bridge.focus_event(
            FocusRequest(1, region_from_shape(1, 1, 1), (FocusCandidate(root, (0, 0, 0), 1),), 0, 0)
        )


def test_focus_does_not_advance_or_mutate_main_world():
    baseline = Simulation(Config(nx=12, ny=12, nz=12))
    world = Simulation(Config(nx=12, ny=12, nz=12))
    for sim in (baseline, world):
        sim.add_particle(1, 3, 3, 3, 1, 0, 0)
    for _ in range(8):
        baseline.step()
        world.step()

    q = DeferredQuantum()
    bridge = QuantumBridge(q)
    roots = (
        bridge.prepare(1, (1, 1, 1), 0, 1).quantum_node,
        bridge.prepare(2, (9, 9, 9), 0, 2).quantum_node,
    )
    before = (world.tick, dict(world.cells), dict(world.particles), dict(world.occupancy), world.active)
    reply = bridge.focus_event(
        FocusRequest(
            99,
            region_from_shape(12, 12, 12),
            (
                FocusCandidate(roots[0], (1, 1, 1), 10),
                FocusCandidate(roots[1], (9, 9, 9), 20),
            ),
            world.tick,
            3,
        )
    )
    after = (world.tick, dict(world.cells), dict(world.particles), dict(world.occupancy), world.active)
    assert reply.event is not None and reply.event.address == (9, 9, 9)
    assert before == after
    assert after == (baseline.tick, dict(baseline.cells), dict(baseline.particles), dict(baseline.occupancy), baseline.active)


def test_focus_modules_pass_integer_static_audit():
    root = Path(__file__).parents[1]
    for relative in (
        "src/event_universe/quantum/focus.py",
        "src/event_universe/quantum/deferred.py",
        "src/event_universe/integration/quantum_bridge.py",
    ):
        assert static_integer_audit(root / relative) == []

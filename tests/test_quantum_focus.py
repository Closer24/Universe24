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
    FocusSet,
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


def _focused_fixture(config: QuantumConfig | None = None):
    q = DeferredQuantum(config)
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
    bridge.bind_focus_set(7, FocusSet(region_from_shape(8, 8, 8), tuple(candidates), 2))
    return q, bridge


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
    region = Region3D(0, 1, 0, 5, 0, 2)
    assert len(split_region(region)) == 4
    assert _leaf_addresses(region) == {(0, y, z) for y in range(5) for z in range(2)}


def test_1024_cube_focus_reaches_one_cell_in_ten_levels():
    q = DeferredQuantum()
    bridge = QuantumBridge(q)
    address = (1000, 777, 513)
    root = bridge.prepare(1, address, 0, 1).quantum_node
    bridge.bind_focus_set(
        2, FocusSet(region_from_shape(1024, 1024, 1024), (FocusCandidate(root, address, 5),))
    )
    reply = bridge.focus_event(FocusRequest(7, 2, 0, 0))
    assert reply.event is not None
    assert reply.event.address == address
    assert reply.focus_steps == 10
    assert reply.cost == (1, 0)
    assert reply.evaluation_nodes == 1
    assert len(q.last_focus_trace.steps) == 10
    assert all(step.child_count == 8 for step in q.last_focus_trace.steps)


def test_exhaustive_ticket_counts_match_flat_weights_exactly():
    _, bridge = _focused_fixture()
    counts = {None: 0, 10: 0, 20: 0, 30: 0, 40: 0}
    expected = {None: 2, 10: 1, 20: 4, 30: 9, 40: 16}
    for ticket in range(32):
        reply = bridge.focus_event(FocusRequest(100 + ticket, 7, 0, ticket))
        assert reply.cost == (1, 0)
        assert reply.total_weight == 32
        assert reply.event_weight == 30
        assert reply.no_event_weight == 2
        outcome = None if reply.event is None else reply.event.outcome
        counts[outcome] += 1
        assert reply.focus_steps == (0 if reply.event is None else 3)
    assert counts == expected


def test_candidate_binding_order_does_not_change_spatial_focus_result():
    q1, a = _focused_fixture()
    q2 = DeferredQuantum()
    b = QuantumBridge(q2)
    specs = (((4, 4, 4), 4, 40), ((7, 0, 5), 3, 30), ((2, 6, 3), 2, 20), ((1, 1, 1), 1, 10))
    reversed_candidates = []
    for event_id, (address, amplitude, outcome) in enumerate(specs):
        root = b.prepare(event_id, address, 0, amplitude).quantum_node
        reversed_candidates.append(FocusCandidate(root, address, outcome))
    b.bind_focus_set(7, FocusSet(region_from_shape(8, 8, 8), tuple(reversed_candidates), 2))
    for ticket in range(32):
        left = a.focus_event(FocusRequest(100 + ticket, 7, 0, ticket))
        right = b.focus_event(FocusRequest(100 + ticket, 7, 0, ticket))
        assert (None if left.event is None else (left.event.address, left.event.outcome)) == (
            None if right.event is None else (right.event.address, right.event.outcome)
        )
    assert q1.focus_set_count == q2.focus_set_count == 1


def test_same_request_id_is_one_decision_and_cannot_be_rewritten():
    _, bridge = _focused_fixture()
    request = FocusRequest(55, 7, 0, 17)
    first = bridge.focus_event(request)
    repeat = bridge.focus_event(request)
    assert repeat.event == first.event
    assert repeat.repeated == 1
    assert repeat.evaluation_nodes == 0
    with pytest.raises(ValueError, match="rewritten"):
        bridge.focus_event(FocusRequest(55, 7, 0, 18))


def test_physical_side_request_and_reply_are_fixed_size():
    _, bridge = _focused_fixture()
    request = FocusRequest(1, 7, 0, 5)
    reply = bridge.focus_event(request)
    assert len(request) == 4
    assert len(reply) == 7
    assert reply.event is None or len(reply.event) == 8
    assert not hasattr(reply, "path")


def test_focus_rejects_future_quantum_roots():
    q = DeferredQuantum()
    bridge = QuantumBridge(q)
    root = bridge.prepare(1, (2, 2, 2), 5, 1).quantum_node
    bridge.bind_focus_set(1, FocusSet(region_from_shape(8, 8, 8), (FocusCandidate(root, (2, 2, 2), 1),)))
    with pytest.raises(ValueError, match="future"):
        bridge.focus_event(FocusRequest(1, 1, 4, 0))


def test_focus_binding_rejects_mismatched_quantum_root_without_commit():
    q = DeferredQuantum()
    bridge = QuantumBridge(q)
    root = bridge.prepare(1, (2, 2, 2), 0, 1).quantum_node
    with pytest.raises(ValueError, match="match"):
        bridge.bind_focus_set(
            1, FocusSet(region_from_shape(8, 8, 8), (FocusCandidate(root, (2, 2, 3), 1),))
        )
    assert q.focus_set_count == 0


def test_focus_uses_one_combined_host_evaluation_budget():
    q = DeferredQuantum(QuantumConfig(max_eval_nodes=3))
    bridge = QuantumBridge(q)
    candidates = tuple(
        FocusCandidate(bridge.prepare(i, (i, 0, 0), 0, 1).quantum_node, (i, 0, 0), i) for i in range(4)
    )
    bridge.bind_focus_set(1, FocusSet(region_from_shape(8, 1, 1), candidates))
    with pytest.raises(OverflowError, match="evaluation budget"):
        bridge.focus_event(FocusRequest(1, 1, 0, 0))


def test_focus_storage_budgets_are_explicit():
    q = DeferredQuantum(QuantumConfig(max_focus_sets=1, max_focus_candidates=1))
    bridge = QuantumBridge(q)
    root = bridge.prepare(1, (0, 0, 0), 0, 1).quantum_node
    one = FocusSet(region_from_shape(2, 1, 1), (FocusCandidate(root, (0, 0, 0), 1),))
    bridge.bind_focus_set(1, one)
    with pytest.raises(OverflowError, match="set budget"):
        bridge.bind_focus_set(2, one)

    q2 = DeferredQuantum(QuantumConfig(max_focus_candidates=1))
    b2 = QuantumBridge(q2)
    roots = (
        b2.prepare(1, (0, 0, 0), 0, 1).quantum_node,
        b2.prepare(2, (1, 0, 0), 0, 1).quantum_node,
    )
    with pytest.raises(OverflowError, match="candidate budget"):
        b2.bind_focus_set(
            1,
            FocusSet(
                region_from_shape(2, 1, 1),
                (FocusCandidate(roots[0], (0, 0, 0), 1), FocusCandidate(roots[1], (1, 0, 0), 2)),
            ),
        )


def test_zero_total_weight_is_error_not_no_event():
    q = DeferredQuantum()
    bridge = QuantumBridge(q)
    root = bridge.prepare(1, (0, 0, 0), 0, 0).quantum_node
    bridge.bind_focus_set(1, FocusSet(region_from_shape(1, 1, 1), (FocusCandidate(root, (0, 0, 0), 1),)))
    with pytest.raises(ValueError, match="zero total"):
        bridge.focus_event(FocusRequest(1, 1, 0, 0))


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
    bridge.bind_focus_set(
        1,
        FocusSet(
            region_from_shape(12, 12, 12),
            (FocusCandidate(roots[0], (1, 1, 1), 10), FocusCandidate(roots[1], (9, 9, 9), 20)),
        ),
    )
    before = (world.tick, dict(world.cells), dict(world.particles), dict(world.occupancy), world.active)
    reply = bridge.focus_event(FocusRequest(99, 1, world.tick, 3))
    after = (world.tick, dict(world.cells), dict(world.particles), dict(world.occupancy), world.active)
    assert reply.event is not None and reply.event.address == (9, 9, 9)
    assert before == after
    assert after == (
        baseline.tick,
        dict(baseline.cells),
        dict(baseline.particles),
        dict(baseline.occupancy),
        baseline.active,
    )


def test_focus_modules_pass_integer_static_audit():
    root = Path(__file__).parents[1]
    for relative in (
        "src/event_universe/quantum/focus.py",
        "src/event_universe/quantum/deferred.py",
        "src/event_universe/integration/quantum_bridge.py",
    ):
        assert static_integer_audit(root / relative) == []


def test_invalid_ticket_does_not_consume_request_or_cache_capacity():
    q, bridge = _focused_fixture(QuantumConfig(max_cached_results=1))
    trace = q.last_focus_trace
    with pytest.raises(ValueError, match="smaller than total"):
        bridge.focus_event(FocusRequest(50, 7, 0, 32))
    assert q.last_focus_trace == trace
    first = bridge.focus_event(FocusRequest(50, 7, 0, 0))
    assert first.event is None
    with pytest.raises(OverflowError, match="cache budget"):
        bridge.focus_event(FocusRequest(51, 7, 0, 0))
    assert bridge.focus_event(FocusRequest(50, 7, 0, 0)).repeated == 1


def test_multiple_outcomes_at_one_cell_keep_their_distinct_weights():
    q = DeferredQuantum()
    bridge = QuantumBridge(q)
    address = (0, 0, 0)
    roots = tuple(bridge.prepare(i, address, 0, i + 1).quantum_node for i in range(2))
    bridge.bind_focus_set(
        1,
        FocusSet(
            region_from_shape(1, 1, 1),
            (FocusCandidate(roots[1], address, 20), FocusCandidate(roots[0], address, 10)),
        ),
    )
    replies = [bridge.focus_event(FocusRequest(i, 1, 0, i)) for i in range(5)]
    assert [reply.event.outcome for reply in replies] == [10, 20, 20, 20, 20]
    assert all(reply.focus_steps == 0 for reply in replies)


def test_no_event_only_set_needs_no_quantum_root():
    q = DeferredQuantum()
    q.bind_focus_set(1, FocusSet(region_from_shape(1, 1, 1), (), 2))
    for ticket in range(2):
        reply = q.focus_event(FocusRequest(ticket, 1, 0, ticket))
        assert reply.event is None
        assert reply.total_weight == 2
        assert reply.event_weight == reply.evaluation_nodes == reply.focus_steps == 0

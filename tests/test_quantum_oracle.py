"""Executable contracts for the model-cost exception; no physical oracle claims."""

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from event_universe.core.state import MAX_CORE_INT
from event_universe.integration.quantum_bridge import QuantumBridge
from event_universe.quantum import (
    ORACLE_COST,
    QUANTUM_MODEL_ID,
    DeferredQuantum,
    QuantumConfig,
    QuantumQuery,
)


def interferometer(turns=0, config=None):
    q = DeferredQuantum(config)
    source = q.source((0, 0, 0), 0, 1)
    left = q.phase(source, (1, 0, 0), 1, 0)
    right = q.phase(source, (0, 0, 1), 1, turns)
    root = q.sum2(left, right, (1, 0, 1), 2)
    return q, root


def query(q, root, tick=None):
    node = q.node(root)
    return q.query(QuantumQuery(root, (node.x, node.y, node.z), node.tick if tick is None else tick))


def test_unit_cost_postulate_is_explicit_and_not_a_host_work_claim():
    assert ORACLE_COST.model_units == 1
    assert ORACLE_COST.world_ticks == 0
    assert QUANTUM_MODEL_ID == "deferred-unit-cost-oracle-v1"
    root = Path(__file__).parents[1]
    for name in ("POSTULATES.md", "SIMULATOR_DEFINITIONS.md", "docs/ARCHITECTURE.md"):
        text = (root / name).read_text(encoding="utf-8")
        assert "Q-ORACLE-1" in text
        assert "deferred-unit-cost-oracle-v1" in text


@pytest.mark.parametrize(
    "turns,amplitude,weight",
    [
        (0, (2, 0), 4),
        (1, (1, 1), 2),
        (2, (0, 0), 0),
        (3, (1, -1), 2),
    ],
)
def test_3d_interference_preserved_by_oracle(turns, amplitude, weight):
    q, root = interferometer(turns)
    assert q.query_stats.successful_queries == 0
    assert q.query_stats.host_evaluated_nodes == 0
    result = query(q, root)
    assert result.amplitude == amplitude
    assert result.weight == weight
    assert result.evaluation_nodes == 4  # One shared source, not two evaluations of it.
    assert result.cost == (1, 0)
    assert q.node_count == 4


def test_model_cost_stays_one_for_different_host_depths():
    q = DeferredQuantum()
    short = q.source((0, 0, 0), 0, 1)
    long = short
    for t in range(1, 65):
        long = q.phase(long, (t, 0, 0), t, 0)
    a = query(q, short)
    b = query(q, long)
    assert (a.evaluation_nodes, b.evaluation_nodes) == (1, 65)
    assert a.cost == b.cost == (1, 0)
    assert q.query_stats.host_evaluated_nodes == 66
    assert q.query_stats.model_cost_units == 2
    assert q.query_stats.elapsed_world_ticks == 0


def test_repeated_pure_queries_do_not_resample_or_grow_history():
    q, root = interferometer(1)
    saved_nodes = tuple(q.node(i) for i in range(q.node_count))
    first = query(q, root, tick=8)
    for _ in range(99):
        repeat = query(q, root, tick=8)
        assert (repeat.amplitude, repeat.weight) == (first.amplitude, first.weight)
        assert repeat.evaluation_nodes == 0
        assert repeat.cache_hit == 1
        assert repeat.cost == (1, 0)
    assert q.node_count == 4
    assert tuple(q.node(i) for i in range(4)) == saved_nodes
    assert q.cached_result_count == 1
    assert q.query_stats.successful_queries == 100
    assert q.query_stats.model_cost_units == 100
    assert q.query_stats.host_evaluated_nodes == 4
    assert q.query_stats.cache_hits == 99


def test_bridges_share_one_owner_and_one_cache():
    q, root = interferometer(0)
    a, b = QuantumBridge(q), QuantumBridge(q)
    one = a.query_cell(root, (1, 0, 1), 8)
    two = b.query_cell(root, (1, 0, 1), 8)
    assert one.amplitude == two.amplitude == (2, 0)
    assert (one.cache_hit, two.cache_hit) == (0, 1)
    assert q.query_stats.successful_queries == 2
    assert q.query_stats.host_evaluated_nodes == 4


def test_legacy_measure_uses_same_oracle_not_another_evaluator():
    q, root = interferometer(2)
    bridge = QuantumBridge(q)
    first = bridge.measure(100, root)
    second = bridge.query_cell(root, (1, 0, 1), 8)
    assert first.weight == second.weight == 0
    assert first.cost == second.cost == (1, 0)
    assert second.cache_hit == 1
    assert q.query_stats.successful_queries == 2


def test_appending_history_does_not_change_an_existing_query_fact():
    q, root = interferometer(0)
    first = query(q, root)
    next_root = q.phase(root, (1, 0, 2), 3, 2)
    later = query(q, next_root)
    old_again = query(q, root)
    assert old_again.amplitude == first.amplitude == (2, 0)
    assert later.amplitude == (-2, 0)
    assert old_again.cache_hit == 1


def test_read_order_changes_no_amplitudes_or_weights():
    q, bright = interferometer(0)
    dark = q.phase(bright, (1, 0, 2), 3, 2)
    q2, bright2 = interferometer(0)
    dark2 = q2.phase(bright2, (1, 0, 2), 3, 2)
    one = [query(q, r) for r in (bright, dark)]
    two = [query(q2, r) for r in (dark2, bright2)]
    assert [(r.amplitude, r.weight) for r in one] == [(r.amplitude, r.weight) for r in reversed(two)]


@pytest.mark.parametrize(
    "address", [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
)
def test_exactly_six_cardinal_hops_are_allowed(address):
    q = DeferredQuantum()
    src = q.source((0, 0, 0), 0, 1)
    out = q.phase(src, address, 1, 0)
    assert query(q, out).amplitude == (1, 0)


@pytest.mark.parametrize(
    "address,tick,match",
    [
        ((1, 0, 0), 0, "causal tick"),
        ((1, 1, 0), 2, "six cardinal"),
        ((0, 0, 2), 10, "six cardinal"),
        ((0, 0, 0), -1, "non-negative"),
    ],
)
def test_invalid_history_edge_is_rejected_before_append(address, tick, match):
    q = DeferredQuantum()
    src = q.source((0, 0, 0), 0, 1)
    with pytest.raises(ValueError, match=match):
        q.phase(src, address, tick, 0)
    assert q.node_count == 1


def test_both_merge_parents_obey_causality():
    q = DeferredQuantum()
    past = q.source((0, 0, 0), 0, 1)
    future = q.source((0, 0, 0), 8, 1)
    with pytest.raises(ValueError, match="precede"):
        q.sum2(past, future, (0, 0, 0), 7)
    assert q.node_count == 2


def test_future_query_is_rejected_without_caching_or_successful_accounting():
    q, root = interferometer()
    with pytest.raises(ValueError, match="future"):
        query(q, root, tick=1)
    assert q.cached_result_count == 0
    assert q.query_stats.successful_queries == 0


def test_query_for_wrong_cell_is_rejected():
    q, root = interferometer()
    with pytest.raises(ValueError, match="local quantum"):
        q.query(QuantumQuery(root, (20, 20, 20), 8))
    assert q.cached_result_count == 0


@pytest.mark.parametrize("bad", [True, 0.5, "1", None])
def test_query_rejects_non_integer_time(bad):
    with pytest.raises(TypeError):
        QuantumQuery(0, (0, 0, 0), bad)


@pytest.mark.parametrize("address", [(0, 0), (0, 0, 0, 0), [0, 0, 0]])
def test_query_requires_immutable_3d_address(address):
    with pytest.raises(ValueError, match="3D"):
        QuantumQuery(0, address, 0)


def test_query_ids_and_time_remain_bounded():
    with pytest.raises(OverflowError):
        QuantumQuery(MAX_CORE_INT + 1, (0, 0, 0), 0)
    with pytest.raises(OverflowError):
        QuantumQuery(0, (0, 0, 0), MAX_CORE_INT + 1)
    q = DeferredQuantum()
    with pytest.raises(IndexError):
        q.query(QuantumQuery(0, (0, 0, 0), 0))


def test_invalid_bridge_prepare_does_not_leave_an_orphan_source():
    q = DeferredQuantum()
    bridge = QuantumBridge(q)
    with pytest.raises(TypeError):
        bridge.prepare(True, (0, 0, 0), 0, 1)
    assert q.node_count == 0


def test_resolve_work_budget_limits_backward_expansion_before_deep_leaf():
    q = DeferredQuantum(QuantumConfig(max_nodes=100, max_eval_nodes=3))
    root = q.source((0, 0, 0), 0, 1)
    for tick in range(1, 50):
        root = q.phase(root, (0, 0, 0), tick, 0)
    with pytest.raises(OverflowError, match="evaluation budget"):
        query(q, root)
    assert q.node_count == 50
    assert q.cached_result_count == 0
    assert q.query_stats.successful_queries == 0
    assert query(q, 0).weight == 1  # No poisoned owner after the rejected host job.


def test_shared_ancestor_is_evaluated_once_even_if_used_twice():
    q = DeferredQuantum(QuantumConfig(max_eval_nodes=2))
    source = q.source((0, 0, 0), 0, 1)
    root = q.sum2(source, source, (0, 0, 0), 0)
    result = query(q, root)
    assert result.amplitude == (2, 0)
    assert result.evaluation_nodes == 2


def test_cache_budget_fails_explicitly_and_preserves_old_answers():
    q, root = interferometer(config=QuantumConfig(max_cached_results=1))
    first = query(q, root)
    source = q.source((0, 0, 0), 0, 1)
    before = q.query_stats
    with pytest.raises(OverflowError, match="cache budget"):
        query(q, source)
    assert q.query_stats == before
    assert q.cached_result_count == 1
    assert query(q, root).amplitude == first.amplitude


@pytest.mark.parametrize("field", ["max_nodes", "max_eval_nodes", "max_cached_results"])
def test_nonpositive_budgets_rejected(field):
    with pytest.raises(ValueError):
        QuantumConfig(**{field: 0})


def test_weight_overflow_does_not_become_a_zero_or_a_measurement():
    q = DeferredQuantum()
    root = q.source((0, 0, 0), 0, 46341)
    with pytest.raises(OverflowError, match="32-bit"):
        query(q, root)
    assert q.cached_result_count == 0
    assert q.query_stats.successful_queries == 0


def test_amplitude_overflow_fails_instead_of_wrapping():
    q = DeferredQuantum()
    source = q.source((0, 0, 0), 0, MAX_CORE_INT)
    root = q.sum2(source, source, (0, 0, 0), 0)
    with pytest.raises(OverflowError, match="32-bit"):
        query(q, root)
    assert q.cached_result_count == 0


def test_request_reply_and_node_views_cannot_rewrite_facts():
    q, root = interferometer(2)
    result = query(q, root)
    with pytest.raises(FrozenInstanceError):
        result.request.tick = 0
    with pytest.raises(FrozenInstanceError):
        result.weight = 100
    with pytest.raises(AttributeError):
        q.node(root).value_a = 12
    with pytest.raises(FrozenInstanceError):
        q.query_stats.successful_queries = 99
    assert query(q, root).weight == 0


def test_real_world_unchanged_by_many_unit_cost_queries_and_keeps_evolving():
    from event_universe import Config, Simulation
    from event_universe.diagnostics.measurements import total_momentum
    from event_universe.diagnostics.recorder import TraceRecorder

    def make_world():
        trace = TraceRecorder()
        world = Simulation(Config(nx=16, ny=16, nz=16), observer=trace)
        world.add_particle(1, 4, 4, 4, 1, 0, 0)
        world.add_particle(2, 7, 6, 5, -1, 0, 0)
        return world, trace

    baseline, trace_a = make_world()
    integrated, trace_b = make_world()
    q, root = interferometer(2)
    bridge = QuantumBridge(q)
    for _ in range(8):
        baseline.step()
        integrated.step()
    before = (
        integrated.tick,
        dict(integrated.cells),
        dict(integrated.particles),
        dict(integrated.occupancy),
        integrated.active,
        total_momentum(integrated),
    )
    for _ in range(20):
        reply = bridge.query_cell(root, (1, 0, 1), integrated.tick)
        assert reply.cost == (1, 0)
    after = (
        integrated.tick,
        dict(integrated.cells),
        dict(integrated.particles),
        dict(integrated.occupancy),
        integrated.active,
        total_momentum(integrated),
    )
    assert before == after
    for _ in range(8):
        baseline.step()
        integrated.step()
        assert baseline.tick == integrated.tick
        assert dict(baseline.cells) == dict(integrated.cells)
        assert dict(baseline.particles) == dict(integrated.particles)
        assert dict(baseline.occupancy) == dict(integrated.occupancy)
        assert baseline.active == integrated.active
        assert total_momentum(baseline) == total_momentum(integrated)
    assert trace_a.paths == trace_b.paths
    assert trace_a.force_records == trace_b.force_records
    assert trace_a.collisions == trace_b.collisions

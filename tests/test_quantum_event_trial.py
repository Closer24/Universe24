"""Headless entry-point integration without any native physical-state writes."""

import pytest

from event_universe.integration.quantum_event_trial import run_trial
from event_universe.quantum import DeferredQuantum, QuantumQuery


@pytest.mark.parametrize("ticket,outcome", [(0, 0), (15, 0), (16, 1), (24, 1)])
def test_selected_event_trial(ticket, outcome):
    result = run_trial(ticket)
    assert result["weights_before_empty_occupied"] == (16, 9)
    assert result["outcome"] == outcome
    assert result["weights_after_empty_occupied"] == ((0, 1) if outcome else (1, 0))
    assert result["tick_before_decision"] == result["tick_after_decision"] == 1
    assert result["extra_world_ticks"] == 0
    assert result["successful_queries"] == 3


def test_example_rejects_out_of_range_ticket():
    with pytest.raises(ValueError):
        run_trial(25)


def test_legacy_scalar_query_still_uses_original_contract():
    owner = DeferredQuantum()
    root = owner.source((0, 0, 0), 0, 3, 4)
    reply = owner.query(QuantumQuery(root, (0, 0, 0), 0))
    assert reply.weight == 25
    assert reply.cost.world_ticks == 0

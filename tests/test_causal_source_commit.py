"""Preflight and publication boundaries for coupled ordinary quantum sources."""

from dataclasses import replace

import pytest

from event_universe.core.disturbance_state import MAX_VALUE, unpack
from event_universe.core.event_resolution import LocalContext

from .test_causal_contact_fields import (
    DETECTOR,
    SOURCE,
    causal_configuration,
    frozen_split_configuration,
)
from .test_localized_quantum_contact import step, world_for


def contact_context(world, address):
    node = world._nodes[address]
    return LocalContext(world.tick, address, node.records, node.coupling_remainders, 0, node.cause_id)


def unexpected_planner(*args):
    raise AssertionError("a resident contact must select the configured instrument")


def quantum_signature(resolver):
    space = resolver.space
    return (
        space.heads,
        space.events,
        space.records,
        space.waves.states,
        resolver.draws,
        resolver.events.next_id,
    )


@pytest.mark.parametrize("source", [True, False])
def test_generation_overflow_is_rejected_before_quantum_contact_commit(source):
    world, resolver = world_for(causal_configuration())
    if not source:
        step(world, 3)
    address = SOURCE if source else DETECTOR
    context = contact_context(world, address)
    plan = resolver.resolve(context, unexpected_planner)
    assert plan.resolution_token is not None
    node = resolver.source_nodes()[address]
    node.generation = MAX_VALUE
    before = quantum_signature(resolver)
    local_before = replace(node)
    reservations = resolver._pending.copy()

    with pytest.raises(ValueError, match="integer bound"):
        resolver.commit_choice(context, plan.resolution_token, 1)

    assert quantum_signature(resolver) == before
    assert node == local_before
    assert resolver._pending == reservations


@pytest.mark.parametrize("invalid", ["source_identity", "terminal_arrival"])
def test_terminal_preflight_keeps_quantum_state_and_draws_unchanged(invalid):
    world, resolver = world_for(causal_configuration())
    step(world, 3)
    context = contact_context(world, DETECTOR)
    plan = resolver.resolve(context, unexpected_planner)
    assert plan.resolution_token is not None
    node = resolver.source_nodes()[DETECTOR]
    if invalid == "source_identity":
        node.source_id += 100
        message = "different origins"
    else:
        # The contact itself is current, but a one-Link terminal packet cannot
        # be represented beyond the last supported physical tick.
        resolver.space._tick = MAX_VALUE
        context = replace(context, tick=MAX_VALUE)
        message = "integer bound"
    before = quantum_signature(resolver)
    local_before = replace(node)
    reservations = resolver._pending.copy()

    with pytest.raises(ValueError, match=message):
        resolver.commit_choice(context, plan.resolution_token, 1)

    assert quantum_signature(resolver) == before
    assert node == local_before
    assert resolver._pending == reservations


def population_total(states):
    return sum(unpack(value)[0] for value in states[0].populations)


def test_source_observer_sees_committed_budget_stock_and_accounting():
    world, resolver = world_for(frozen_split_configuration())
    step(world, 1)
    source = resolver.source_nodes()[SOURCE]
    before_stock = population_total(world._spatial.nodes[SOURCE].states)
    before_allowance = unpack(source.emission_state.remaining[1])[0]
    observed = []

    def observe(event):
        if event["event"] != "spatial_envelope_source" or tuple(event["position"]) != SOURCE:
            return
        assert source.pending_emission is None
        assert unpack(source.emission_state.remaining[1]) == (before_allowance - 9,)
        assert population_total(world._spatial.nodes[SOURCE].states) == before_stock - 9
        assert event["source_delta"]["electric_signal"] == (-9,)
        assert all(value["balanced"] for value in world.spatial_accounting().values())
        observed.append(event["tick"])

    world._spatial.observer = observe
    step(world, 1)
    assert observed == [1]


@pytest.mark.parametrize("field", [0, 3])
def test_forged_source_delta_is_rejected_without_consuming_stock_or_allowance(field):
    world, resolver = world_for(frozen_split_configuration())
    step(world, 1)
    spatial = world._spatial.nodes[SOURCE]
    source = resolver.source_nodes()[SOURCE]
    proposal = resolver.prepare_source(SOURCE, world.tick, spatial.states, 0)
    assert proposal is not None
    altered = list(proposal.source_delta)
    altered[field] = (altered[field][0] + 1,)
    forged = replace(proposal, source_delta=tuple(altered))
    before = (
        spatial.states,
        spatial.cause_id,
        replace(source),
        world.source_totals(),
        resolver.events.next_id,
    )

    with pytest.raises(ValueError, match="source accounting differs"):
        world._spatial.commit_source(SOURCE, world.tick, forged)

    assert (
        spatial.states,
        spatial.cause_id,
        source,
        world.source_totals(),
        resolver.events.next_id,
    ) == before

"""A thing pays a tick for every whole quantum it reads (Highlights 5.4 point 23,
the model owner's decision of 2026-09-18; clock-readings-v1, feature 16b): in
an interval in which a thing reads a whole quantum of shadow, a push of one
quantum on any axis of its momentum, it neither moves, nor steps, nor advances
its phase; a shadow pays nothing; the count is w intervals per whole quantum,
the world's `wait_per_quantum` (1 by default, a rational n / d admitted), kept
as an exact counter on the thing (`owed`, in units of 1 / d) and spent one
interval at a time, the only exception to point 21's one Link per interval.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("The wait per
quantum read") before the first run.
"""

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import BIT_SHADOW, BIT_THING
from event_universe.initialization import parse_initial_state

from .test_ray_momentum_turn import HEADINGS, ZERO, document, ray, rays_at, shadow_ray, turn

THING = ((4, 10, 10), "m", 1, 0)
FROM_BELOW = ((10, 4, 10), "f", 1, 2)


def world(wait, lamps=(THING, FROM_BELOW), ticks=12):
    """The thing of 1 (K 1: one phase step per interval) meets the shadow of 1
    from -Y at C after tick 6 under the content reading with sign -1: a push of
    one whole quantum, (0, -1, 0)."""
    raw = document(lamps, [turn({"f": -1})], ticks)
    raw["K"] = 1
    raw["wait_per_quantum"] = wait
    return raw


def positions(world_, family):
    return sorted(
        n.position for n in world_.inventory_view().nodes if rays_at(world_, n.position, family)
    )


@pytest.mark.parametrize("case", ["one", "shadow", "double", "none", "half", "rejected"])
def test_a_thing_pays_a_tick_for_every_whole_quantum_it_reads(case):
    if case == "one":
        # (a) w = 1: the push of one quantum in the cycle of tick 6 costs the
        # thing the interval of tick 7: it stays at C, its phase and steps as
        # they were and the world's computation still; at tick 8 it steps to -Y
        # (the component reached its content 1) and moves. Every other interval
        # it moves one Link.
        sim = Simulation(parse_initial_state(world(1)))
        for t in range(1, 13):
            sim.step()
            if t <= 6:
                assert rays_at(sim, (4 + t, 10, 10), "m") == [ray(0, 1, t & 7, t, 0)]
                assert sim.phase_steps() == t
            elif t == 7:
                (thing,) = rays_at(sim, (10, 10, 10), "m")
                assert (thing.steps, thing.phase, thing.owed, thing.momentum) == (6, 6, 0, (0, -1, 0))
                assert positions(sim, "m") == [(10, 10, 10)]
                assert sim.phase_steps() == 6
            else:
                at = (10, 17 - t, 10)
                assert positions(sim, "m") == [at]
                assert rays_at(sim, at, "m") == [ray(3, 1, (t - 1) & 7, t - 1, 0)]
                assert sim.phase_steps() == t - 1
            assert sim.audit()["balanced"]
        return
    if case == "shadow":
        # (b) A shadow's motion is unchanged by any reading: the shadow that gave
        # the push turns back in the cycle of tick 6 and walks -Y one Link per
        # interval from tick 7, its steps down to 0 after tick 12, while the
        # thing waits; a shadow owes nothing.
        sim = Simulation(parse_initial_state(world(1)))
        for t in range(1, 13):
            sim.step()
            if t <= 6:
                assert rays_at(sim, (10, 4 + t, 10), "f") == [shadow_ray(2, 1, t)]
            else:
                assert rays_at(sim, (10, 16 - t, 10), "f") == [shadow_ray(3, 1, 12 - t, (0, 1, 0))]
            assert all(
                r.owed == 0
                for n in sim.inventory_view().nodes
                for rs in n.rays
                for r in rs
                if r.detector == BIT_SHADOW
            )
        return
    if case == "double":
        # (c) w = 2 doubles the wait: the thing stays at C through ticks 7 and 8
        # and steps to -Y at tick 9.
        sim = Simulation(parse_initial_state(world(2)))
        for t in range(1, 13):
            sim.step()
            if t <= 6:
                assert positions(sim, "m") == [(4 + t, 10, 10)]
            elif t <= 8:
                (thing,) = rays_at(sim, (10, 10, 10), "m")
                assert (thing.steps, thing.phase, thing.owed) == (6, 6, 8 - t)
                assert sim.phase_steps() == 6
            else:
                assert positions(sim, "m") == [(10, 18 - t, 10)]
                assert rays_at(sim, (10, 18 - t, 10), "m") == [ray(3, 1, (t - 2) & 7, t - 2, 0)]
        return
    if case == "none":
        # (d) No reading, no wait: alone on its line the thing moves one Link
        # every interval, whatever w.
        sim = Simulation(parse_initial_state(world(2, lamps=(THING,))))
        for t in range(1, 13):
            sim.step()
            assert rays_at(sim, (4 + t, 10, 10), "m") == [ray(0, 1, t & 7, t, 0)]
            assert sim.phase_steps() == t
        return
    if case == "half":
        # (e) w = 1 / 2: one quantum read owes half an interval, kept exactly
        # (`owed` 1 in units of 1 / 2) and spent by nothing: the thing steps at
        # tick 7 as if it owed nothing; the debt stays on it.
        sim = Simulation(parse_initial_state(world([1, 2])))
        for t in range(1, 13):
            sim.step()
            if t >= 7:
                (thing,) = rays_at(sim, (10, 16 - t, 10), "m")
                assert (thing.heading, thing.steps, thing.owed) == (3, t, 1)
        return
    raw = world(1)
    initial = parse_initial_state(raw)
    assert initial.wait_per_quantum == (1, 1) and initial.spatial_fields[0].wait_denominator == 1
    assert parse_initial_state(world([11, 9])).wait_per_quantum == (11, 9)
    for wait, message in (([1, 0], "d at least 1"), (-1, "wait_per_quantum"), ([1], "wait_per_quantum")):
        with pytest.raises(ValueError, match=message):
            parse_initial_state(world(wait))
    assert HEADINGS[3] == [0, -1, 0] and ZERO == (0, 0, 0) and BIT_THING == 1

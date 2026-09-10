"""Full-vector candidate integration, including delayed local links."""

import json
from dataclasses import replace

from event_universe import Config, LinkConfig, UnifiedLinkedSimulation, UnifiedSimulation
from event_universe.diagnostics.measurements import audit, total_momentum
from event_universe.fields.scalar import ScalarField
from event_universe.models.unified_field import LINKED_MODEL_ID, MODEL_ID
from event_universe.runner import run_scenario
from event_universe.scenarios import get_scenario


def test_local_neighbor_imbalance_accelerates_then_keeps_inertial_motion():
    # Static seeds are a controlled local test fixture, not a gravity source law.
    config = Config(nx=16, ny=12, nz=8, c_units=12, source_strength=0, field_den=1, force_den=1)
    local_field = ScalarField(neighbor_weights=(0, 0, 0, 0, 0, 0), self_weight=1)
    world = UnifiedSimulation(config, field=local_field)
    world.add_particle(0, 4, 4, 4, 4, 0, 0)
    world.seed_field((5, 4, 4), 2)
    world.step()
    assert world.particles[0].momentum == (6, 0, 0)
    assert world.particles[0].move_budget == 6
    assert total_momentum(world) == (4, 0, 0)
    world.step()
    assert world.particles[0].position == (5, 4, 4)
    assert world.particles[0].momentum == (8, 0, 0)
    world.step()
    assert world.particles[0].momentum == (8, 0, 0)
    assert audit(world)["occupancy_consistent"]


def test_three_mutual_sources_exchange_momentum_at_every_tick():
    scenario = replace(get_scenario("unified"), ticks=48)
    world = scenario.create()
    initial = total_momentum(world)
    changed = False
    for _ in range(scenario.ticks):
        old = {pid: p.momentum for pid, p in world.particles.items()}
        world.step()
        changed |= any(old[pid] != p.momentum for pid, p in world.particles.items())
        assert total_momentum(world) == initial
        assert audit(world)["occupancy_consistent"]
    assert changed


def test_linked_action_uses_only_delivered_neighbors_and_freezes_departure():
    config = Config(nx=11, ny=11, nz=11, c_units=12, source_strength=0, force_den=1, field_den=1)
    world = UnifiedLinkedSimulation(config, links=LinkConfig(3, 0))
    world.add_particle(0, 5, 5, 5, 1, 0, 0)
    world.seed_field((6, 5, 5), 12)

    def remote_read_is_forbidden(position):
        raise AssertionError("direct remote read")

    world.phi = remote_read_is_forbidden
    initial = total_momentum(world)
    world.step()
    transit = world.transits[0]
    assert transit.length == 3 and transit.due == 36
    for _ in range(12):
        world.step()
        assert world.transits[0] == transit
        assert world.particles[0].momentum == (1, 0, 0)
        assert total_momentum(world) == initial
        assert audit(world)["occupancy_consistent"]


def test_stationary_source_does_not_accelerate_in_its_symmetric_field():
    world = UnifiedSimulation(Config(nx=11, ny=11, nz=11, c_units=12, force_den=1))
    world.add_particle(0, 5, 5, 5)
    for _ in range(24):
        world.step()
        assert world.particles[0].momentum == (0, 0, 0)
        assert total_momentum(world) == (0, 0, 0)


def test_runner_identifies_both_unified_candidates_and_keeps_3d_output(tmp_path):
    for name, model_id in (("unified", MODEL_ID), ("unified-links", LINKED_MODEL_ID)):
        output = tmp_path / name
        path = run_scenario(replace(get_scenario(name), ticks=2), output)
        metadata = json.loads((output / "run.json").read_text())
        assert metadata["model"] == model_id
        assert metadata["display"] == "volume-3d"
        assert metadata["momentum_equal_at_every_completed_tick"]
        assert "data:image/gif;base64," in path.read_text()

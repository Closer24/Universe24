"""Shared-interaction integration; worlds use the existing HTML capture fixture."""

import json
from dataclasses import replace

import pytest

from event_universe import SharedActionConfig, SharedActionSimulation
from event_universe.core.links import LINK_REGISTERS
from event_universe.diagnostics.measurements import audit, total_momentum
from event_universe.diagnostics.recorder import TraceRecorder
from event_universe.runner import run_scenario
from event_universe.scenarios import get_scenario


def test_isolated_stationary_source_and_reciprocal_bookkeeping():
    world = SharedActionSimulation()
    world.add_particle(0, 24, 24, 16)
    for _ in range(24):
        world.step()
        assert world.particles[0].momentum == (0, 0, 0)
        assert total_momentum(world) == (0, 0, 0)
        world.links.validate()
        audit(world)
    assert world.phi((24, 24, 16)) > 0
    assert len(world.cell_at((24, 24, 16))) == 5
    for cell in world.links.cells.values():
        assert (
            len(cell.received) + len(cell.lengths) + sum(len(p) for p in cell.outgoing) == LINK_REGISTERS
        )


def test_zero_coupling_decouples_both_sides_and_keeps_inertia():
    world = SharedActionSimulation(SharedActionConfig(coupling=0))
    world.add_particle(0, 24, 24, 16, 3, 2, 1)
    for _ in range(24):
        previous = world.particles[0]
        world.step()
        current = world.particles[0]
        assert current.momentum == (3, 2, 1)
        assert all(cell.phi == 0 for cell in world.cells.values())
        assert sum(abs(a - b) for a, b in zip(current.position, previous.position, strict=True)) <= 1
    assert world.particles[0].position != (24, 24, 16)


def test_response_uses_delivered_ports_not_raw_remote_field(monkeypatch):
    world = SharedActionSimulation(SharedActionConfig(impulse_units=1))
    world.add_particle(0, 20, 20, 16)
    world.seed_field((21, 20, 16), 128)

    def forbidden_read(_):
        raise AssertionError("raw remote phi lookup is forbidden")

    monkeypatch.setattr(world, "phi", forbidden_read)
    for _ in range(4):
        world.step()
    assert world.particles[0].px > 0


def test_perturbation_cannot_cross_more_than_one_edge_per_tick():
    settings = SharedActionConfig(coupling=2, impulse_units=1, c_units=100)
    left = SharedActionSimulation(settings)
    right = SharedActionSimulation(settings)
    origin = (20, 20, 16)
    for world in (left, right):
        world.add_particle(0, 24, 20, 16)
    right.seed_field(origin, 7**5)
    first_response = None
    for _ in range(8):
        left.step()
        right.step()
        positions = set(left.cells) | set(right.cells) | set(left.links.cells) | set(right.links.cells)
        for position in positions:
            if left.cell_at(position) != right.cell_at(position) or left.links.at(
                position
            ) != right.links.at(position):
                assert sum(abs(a - b) for a, b in zip(position, origin, strict=True)) <= left.tick
        if left.particles[0] != right.particles[0] and first_response is None:
            first_response = left.tick
    assert first_response is not None and first_response >= 4


def test_two_sources_interact_without_global_momentum_repair():
    trace = TraceRecorder()
    world = SharedActionSimulation(SharedActionConfig(impulse_units=64), observer=trace)
    world.add_particle(0, 25, 23, 16, 3, 0, 0)
    world.add_particle(1, 35, 25, 16, -3, 0, 0)
    for _ in range(48):
        world.step()
        assert total_momentum(world) == (0, 0, 0)
        audit(world)
    assert any(event.iy != 0 for event in trace.force_records)
    assert world.particles[0].z == world.particles[1].z == 16


def test_shared_scenario_rejects_conflicting_independent_config():
    scenario = get_scenario("action-contact")
    with pytest.raises(ValueError, match="must match"):
        replace(scenario, config=replace(scenario.config, source_strength=7)).create()


def test_shared_runner_records_identity_and_generates_existing_html(tmp_path):
    scenario = replace(get_scenario("action-contact"), ticks=4)
    path = run_scenario(scenario, tmp_path, frame_stride=2)
    assert "data:image/gif;base64," in path.read_text()
    metadata = json.loads((tmp_path / "run.json").read_text())
    assert metadata["model"] == "scalar-field-v12-shared-interaction"
    assert metadata["scenario"]["action"]["coupling"] == 64
    assert metadata["display"] == "volume-3d"
    assert (tmp_path / "events.jsonl").is_file()


@pytest.mark.parametrize("momentum,ticks", [((3, 2, 1), 360), ((27, 18, 9), 90)])
def test_isolated_motion_has_no_response_in_momentum_or_remainder(momentum, ticks):
    """Acceptance gate, not a passing description of a known self-force defect.

    Keep every completed state for the existing HTML fixture even when this
    target fails. Empty-field startup is explicit, not a dressed moving state.
    """
    world = SharedActionSimulation(SharedActionConfig(nx=96, ny=96, nz=96, c_units=60))
    world.add_particle(0, 40, 40, 40, *momentum)
    first_response = None
    for _ in range(ticks):
        world.step()
        state = world.particles[0]
        audit(world)
        assert total_momentum(world) == momentum
        residue = (state.force_rx, state.force_ry, state.force_rz)
        if first_response is None and (state.momentum != momentum or any(residue)):
            first_response = (world.tick, state.momentum, residue)
    assert first_response is None, f"isolated response at completed tick: {first_response}"

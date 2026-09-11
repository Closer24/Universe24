"""Acceptance tests for the opt-in outward causal-stream field candidate."""

import pytest

from event_universe import CausalStreamConfig, CausalStreamSimulation
from event_universe.fields.streaming import CausalOctantStream, attractive_samples


def test_source_cannot_mask_invalid_negative_stream_population():
    with pytest.raises(ValueError, match="before source emission"):
        CausalOctantStream().emit((-1, 0, 0, 0, 0, 0, 0, 0), 1, 1, 0)


def test_scalar_seed_is_rejected_without_mutating_stream_world():
    world = CausalStreamSimulation()
    with pytest.raises(NotImplementedError, match="scalar field seeds"):
        world.seed_field((1, 2, 3), 64)
    assert not world.cells
    assert not world.streams.cells


def test_stream_candidate_preserves_mass_aware_movement_and_state_audit():
    from event_universe.diagnostics.measurements import audit, report

    world = CausalStreamSimulation(
        CausalStreamConfig(nx=64, ny=64, nz=64, c_units=4, source_per_octant=1)
    )
    world.add_particle(0, 20, 20, 20, 6, 0, 0, mass=3)
    for tick in range(1, 9):
        world.step()
        particle = world.particles[0]
        assert particle.mass == 3
        assert particle.momentum == (6, 0, 0)
        assert particle.position == (20 + tick // 2, 20, 20)
        assert (particle.force_rx, particle.force_ry, particle.force_rz) == (0, 0, 0)
        assert audit(world)["bounded_integer_state"]
    assert report(world)["architecture"]["stream_registers_per_cell"] == 14


def test_stream_split_conserves_every_integer_and_uses_six_ports():
    rule = CausalOctantStream()
    outgoing = rule.emit((1, 2, 3, 4, 5, 6, 7, 8), 2, 11, 2)
    assert len(outgoing) == 6
    assert all(len(packet) == 8 for packet in outgoing)
    assert sum(sum(packet) for packet in outgoing) == sum(range(1, 9)) + 8 * 2 * 11


def test_attractive_samples_reverse_only_opposite_ports():
    assert attractive_samples((1, 2, 3, 4, 5, 6)) == (2, 1, 4, 3, 6, 5)


@pytest.mark.parametrize(
    ("momentum", "speed_cap", "ticks"),
    [
        ((1, 0, 0), 100, 120),
        ((9, 6, 3), 20, 24),
    ],
)
def test_isolated_particle_never_reads_its_own_outward_stream(momentum, speed_cap, ticks):
    settings = CausalStreamConfig(
        nx=512,
        ny=512,
        nz=512,
        c_units=speed_cap,
        source_per_octant=1,
        force_num=1,
        force_den=64,
    )
    world = CausalStreamSimulation(settings)
    world.add_particle(0, 256, 256, 256, *momentum)
    for _ in range(ticks):
        world.step()
        particle = world.particles[0]
        assert particle.momentum == momentum
        assert (particle.force_rx, particle.force_ry, particle.force_rz) == (0, 0, 0)


def test_remote_source_reaches_after_manhattan_light_cone_and_attracts_symmetrically():
    settings = CausalStreamConfig(
        nx=128,
        ny=128,
        nz=128,
        c_units=1000,
        source_per_octant=192,
        force_num=1,
        force_den=1,
    )
    world = CausalStreamSimulation(settings)
    world.add_particle(0, 50, 50, 50)
    world.add_particle(1, 56, 52, 51)
    for _ in range(8):
        world.step()
        assert world.particles[0].momentum == (0, 0, 0)
        assert world.particles[1].momentum == (0, 0, 0)
    world.step()
    left = world.particles[0].momentum
    right = world.particles[1].momentum
    assert left == (2, 0, 1)
    assert right == (-2, 0, -1)
    assert tuple(a + b for a, b in zip(left, right, strict=True)) == (0, 0, 0)


def test_offset_moving_pair_turns_toward_each_other_without_self_force():
    settings = CausalStreamConfig(
        nx=128,
        ny=128,
        nz=128,
        c_units=12,
        source_per_octant=64,
        force_num=1,
        force_den=12,
    )
    world = CausalStreamSimulation(settings)
    world.add_particle(0, 40, 40, 40, 3, 0, 0)
    world.add_particle(1, 52, 44, 42, -3, 0, 0)
    for _ in range(25):
        world.step()
        assert world.particles[0].py == 0
        assert world.particles[1].py == 0
    world.step()
    assert world.particles[0].momentum == (3, 1, 0)
    assert world.particles[1].momentum == (-3, -1, 0)

import pytest

from event_universe import CellState, Config, ParticleState
from event_universe.core.state import MAX_CORE_INT
from event_universe.fields import ScalarField
from event_universe.fields.scalar import gradient
from event_universe.models.scalar_field import (
    SCALAR_MODEL,
    ScalarFieldModel,
    update_field,
    update_particle,
)


def test_field_uses_six_neighbors_and_keeps_remainder():
    old = CellState(remainder=3)
    new = update_field(old, (1, 2, 3, 4, 5, 6), 2, Config())
    assert new == CellState(phi=21, remainder=5)
    assert old == CellState(remainder=3)


@pytest.mark.parametrize("axis", [0, 1, 2])
def test_gradient_and_local_exchange(axis):
    neighbors = [0] * 6
    neighbors[axis * 2] = 128
    config = Config()
    result = update_particle(ParticleState(1, 1, 1), CellState(), tuple(neighbors), config, 0)
    expected = [0, 0, 0]
    expected[axis] = 2
    assert result.impulse == tuple(expected)
    assert result.particle.momentum == tuple(expected)
    assert (result.cell.px, result.cell.py, result.cell.pz) == tuple(-v for v in expected)
    assert gradient(tuple(neighbors))[axis] == 128


@pytest.mark.parametrize("denominator", [1, 12, 64])
def test_small_forces_accumulate_until_one_integer_impulse(denominator):
    particle, cell = ParticleState(1, 1, 1, 3), CellState()
    config = Config(force_den=denominator, c_units=1000)
    for tick in range(denominator):
        result = update_particle(particle, cell, (0, 0, 1, 0, 0, 0), config, tick)
        particle, cell = result.particle, result.cell
        assert particle.py == (1 if tick == denominator - 1 else 0)
        assert particle.py + cell.py == 0
    assert particle.force_ry == 0


def test_overflow_cannot_commit_only_one_side_of_exchange():
    particle = ParticleState(1, 1, 1)
    cell = CellState(px=-MAX_CORE_INT)
    with pytest.raises(OverflowError):
        update_particle(particle, cell, (64, 0, 0, 0, 0, 0), Config(), 0)
    assert particle.px == 0 and cell.px == -MAX_CORE_INT


def test_scalar_field_model_uses_occupancy_without_retaining_its_own_value():
    old = CellState(phi=1234, px=5, py=-6, pz=7)
    neighbors = (0, 0, 0, 0, 0, 0)
    assert update_field(old, neighbors, 1, Config()) == CellState(9, 5, -6, 7, 1)
    assert update_field(old, neighbors, 0, Config()) == CellState(0, 5, -6, 7, 0)


def test_current_adapter_owns_nonnegative_field_policy():
    signed_field = ScalarField(neighbor_weights=(-1, 0, 0, 0, 0, 0))
    model = ScalarFieldModel(field=signed_field, turning=SCALAR_MODEL.turning)
    cell = CellState(px=5, py=-6, pz=7)
    assert model.update_field(cell, (10, 0, 0, 0, 0, 0), 0, Config(field_den=3)) == cell


def test_current_particle_uses_only_transverse_gradient_while_moving():
    result = update_particle(
        ParticleState(1, 1, 1, px=3), CellState(), (128, 0, 64, 0, 0, 0), Config(), 0
    )
    assert result.gradient == (128, 64, 0)
    assert result.impulse == (0, 1, 0)
    assert result.particle.momentum == (3, 1, 0)
    assert result.cell == CellState(py=-1)


def test_current_model_explicitly_preserves_value_based_activity():
    previous, current = CellState(phi=1), CellState(phi=1, remainder=1)
    assert not SCALAR_MODEL.field_is_active(previous, current, 0)
    assert SCALAR_MODEL.field_is_active(previous, current, 1)


def test_current_particle_connects_turning_and_movement_without_changing_position():
    previous = ParticleState(1, 2, 3, px=3, move_budget=8, axis_phase=3)
    result = update_particle(previous, CellState(), (128, 0, 64, 0, 0, 0), Config(c_units=12), 7)
    assert result.particle == ParticleState(
        1, 2, 3, px=3, py=1, move_budget=0, axis_phase=0, last_update_tick=7
    )
    assert result.direction == 2  # +y
    assert result.cell == CellState(py=-1)

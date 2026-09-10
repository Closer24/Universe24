"""Independent numerical checks of the common interaction and both variations."""

import itertools
from dataclasses import replace

import pytest

from event_universe.core.state import MAX_CORE_INT, CellState, ParticleState
from event_universe.fields.interaction import ScalarInteraction
from event_universe.models.shared_action import SharedActionConfig, shared_action_model


@pytest.mark.parametrize("coupling", [0, 1, 7, 64])
@pytest.mark.parametrize("sources,phi", [(0, 0), (1, -3), (2, 5), (4, 10)])
def test_source_is_exact_field_variation(coupling, sources, phi):
    action = ScalarInteraction(coupling)
    difference = action.term(sources, phi + 1) - action.term(sources, phi)
    assert action.source(sources, coupling) == difference == coupling * sources


def test_both_outputs_use_same_term_and_no_independent_knob():
    action = ScalarInteraction(3)
    assert action.term(2, 5) == 30
    assert action.source(2, 3) == 6
    assert action.force_numerator((9, 4, 2, 10, 6, 6)) == (15, -24, 0)
    with pytest.raises(ValueError, match="shared coupling"):
        action.source(2, 4)
    settings = SharedActionConfig(coupling=3, impulse_units=2)
    model = shared_action_model(settings)
    assert model.source.__self__ is model.field_vector.__self__
    assert settings.engine_config().source_strength == 3
    assert settings.engine_config().force_num == 1
    assert settings.engine_config().force_den == 4


def test_source_and_particle_variations_commute():
    action = ScalarInteraction(7)
    phi = 5
    sources = 2
    mixed = (
        action.term(sources + 1, phi + 3)
        - action.term(sources, phi + 3)
        - action.term(sources + 1, phi)
        + action.term(sources, phi)
    )
    assert mixed == 21
    assert action.source(sources + 1, 7) - action.source(sources, 7) == 7
    assert action.force_numerator((phi + 3, phi, 0, 0, 0, 0)) == (mixed, 0, 0)


@pytest.mark.parametrize("coupling", [0, 1, 7])
@pytest.mark.parametrize("denominator", [7, 8, 12])
def test_field_stationarity_matches_spatial_action_only(coupling, denominator):
    action = ScalarInteraction(coupling)
    neighbors = (1, 2, 3, 4, 5, 6)
    upper = action.local_energy_twice(5, neighbors, 2, denominator)
    lower = action.local_energy_twice(3, neighbors, 2, denominator)
    assert upper - lower == 4 * (4 * denominator - 21 - 2 * coupling)


def test_response_includes_longitudinal_components_and_retains_residue():
    settings = SharedActionConfig(coupling=3, impulse_units=2)
    config = settings.engine_config()
    model = shared_action_model(settings)
    particle = ParticleState(1, 1, 1, 3, 0, 0)
    update = model.update_particle(particle, CellState(), (9, 4, 2, 10, 6, 6), config, 0)
    assert update.impulse == (3, -6, 0)
    assert update.particle.momentum == (6, -6, 0)
    assert (update.particle.force_rx, update.particle.force_ry, update.particle.force_rz) == (3, 0, 0)
    assert (update.cell.px, update.cell.py, update.cell.pz) == (-3, 6, 0)
    field = model.update_field(CellState(), (1, 2, 3, 4, 5, 6), 2, config)
    assert (field.phi, field.remainder) == (3, 6)


def test_pure_force_is_covariant_under_axis_permutations():
    action = ScalarInteraction(3)
    sides = ((9, 4), (2, 10), (6, 6))
    force = (15, -24, 0)
    for order in itertools.permutations(range(3)):
        neighbors = tuple(value for axis in order for value in sides[axis])
        assert action.force_numerator(neighbors) == tuple(force[axis] for axis in order)
    assert action.force_numerator((4, 9, 10, 2, 6, 6)) == (-15, 24, 0)
    # Not a claim of rotational covariance of the inherited digital mover.


@pytest.mark.parametrize("value", [True, 1.0, -1, MAX_CORE_INT + 1])
def test_invalid_coupling_is_rejected(value):
    with pytest.raises((TypeError, ValueError, OverflowError)):
        ScalarInteraction(value)


def test_bounds_and_invalid_inputs_are_not_silently_clipped():
    action = ScalarInteraction(MAX_CORE_INT)
    with pytest.raises(OverflowError):
        action.term(MAX_CORE_INT, MAX_CORE_INT)
    with pytest.raises(ValueError):
        action.term(-1, 0)
    with pytest.raises(TypeError):
        action.force_numerator((True, 0, 0, 0, 0, 0))
    with pytest.raises(ValueError):
        action.force_numerator((0, 0))
    with pytest.raises(OverflowError):
        action.response_denominator(MAX_CORE_INT)
    with pytest.raises(ValueError):
        action.response_denominator(0)
    with pytest.raises(ValueError):
        action.local_energy_twice(1, (0, 0, 0, 0, 0, 0), 1, 5)
    for changes in ({"field_den": 6}, {"nx": 2}, {"impulse_units": 0}, {"c_units": 0}):
        with pytest.raises(ValueError):
            replace(SharedActionConfig(), **changes)

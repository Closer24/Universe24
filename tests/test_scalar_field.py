import pytest

from event_universe.core.state import MAX_CORE_INT, MAX_WORK_INT
from event_universe.fields import ScalarField, ScalarSample
from event_universe.fields.scalar import gradient

ZERO_NEIGHBORS = (0, 0, 0, 0, 0, 0)


def test_weighted_field_with_retention_has_an_exact_known_result():
    field = ScalarField(neighbor_weights=(2, 0, -1, 3, 0, 1), self_weight=2)
    sample = ScalarSample(value=5, remainder=3)
    assert field.advance(sample, (1, 2, 3, 4, 5, 6), source=4, denominator=7) == ScalarSample(4, 6)
    assert sample == ScalarSample(5, 3)


def test_generic_field_keeps_signed_values_and_remainders():
    field = ScalarField(neighbor_weights=(-1, 0, 0, 0, 0, 0))
    assert field.advance(ScalarSample(), (10, 0, 0, 0, 0, 0), source=0, denominator=3) == ScalarSample(
        -3, -1
    )


@pytest.mark.parametrize("sign", [-1, 1])
@pytest.mark.parametrize("denominator", [1, 12, 64])
def test_subunit_sources_accumulate_without_loss(sign, denominator):
    field = ScalarField(neighbor_weights=ZERO_NEIGHBORS)
    sample = ScalarSample()
    emitted = 0
    for step in range(1, denominator + 1):
        sample = field.advance(sample, ZERO_NEIGHBORS, source=sign, denominator=denominator)
        emitted += sample.value
        assert emitted * denominator + sample.remainder == step * sign
    assert emitted == sign and sample.remainder == 0


@pytest.mark.parametrize("weights", [(1, 1), [1, 1, 1, 1, 1, 1]])
def test_stencil_requires_exactly_six_immutable_weights(weights):
    with pytest.raises(ValueError):
        ScalarField(neighbor_weights=weights)


@pytest.mark.parametrize("weight", [True, 0.5])
def test_stencil_rejects_noninteger_coefficients(weight):
    with pytest.raises(TypeError):
        ScalarField(neighbor_weights=(weight, 0, 0, 0, 0, 0))


@pytest.mark.parametrize("denominator,remainder", [(0, 0), (-1, 0), (7, 7), (7, -7)])
def test_invalid_denominator_or_carried_remainder_is_rejected(denominator, remainder):
    field = ScalarField(neighbor_weights=ZERO_NEIGHBORS)
    with pytest.raises(ValueError):
        field.advance(
            ScalarSample(remainder=remainder), ZERO_NEIGHBORS, source=0, denominator=denominator
        )


def test_physical_value_overflow_is_rejected():
    field = ScalarField(neighbor_weights=ZERO_NEIGHBORS)
    with pytest.raises(OverflowError, match="32-bit"):
        field.advance(ScalarSample(), ZERO_NEIGHBORS, source=MAX_CORE_INT + 1, denominator=1)


def test_working_overflow_is_rejected_before_later_cancellation():
    field = ScalarField(neighbor_weights=(1, -1, 0, 0, 0, 0))
    with pytest.raises(OverflowError, match="64-bit"):
        field.advance(ScalarSample(), (1, 1, 0, 0, 0, 0), source=MAX_WORK_INT, denominator=MAX_CORE_INT)


def test_gradient_uses_opposite_neighbors_in_all_three_axes():
    assert gradient((9, 4, 2, 10, 6, 6)) == (5, -8, 0)
    assert gradient((MAX_CORE_INT, -MAX_CORE_INT, 0, 0, 0, 0)) == (2 * MAX_CORE_INT, 0, 0)

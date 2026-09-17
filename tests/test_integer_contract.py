"""Register bounds and carried-remainder scaling retained in ``core/state.py``."""

import pytest

from event_universe.core.state import MAX_CORE_INT, MAX_WORK_INT, Config, checked, scaled_divrem


@pytest.mark.parametrize("value", [True, 1.0, "1", None])
def test_non_integers_rejected(value):
    with pytest.raises(TypeError):
        checked(value)
    with pytest.raises(TypeError):
        Config(c_units=value)


@pytest.mark.parametrize("value", [-MAX_CORE_INT - 1, MAX_CORE_INT + 1])
def test_register_overflow_is_not_wrapped(value):
    with pytest.raises(OverflowError):
        checked(value)


@pytest.mark.parametrize(
    "value,numerator,denominator,remainder,expected",
    [
        (5, 2, 3, 1, (3, 2)),
        (-5, 2, 3, -1, (-3, -2)),
        (5, 0, 3, 1, (0, 1)),
        (5, 2, 1, 0, (10, 0)),
    ],
)
def test_scaled_division_has_exact_signed_expected_results(
    value, numerator, denominator, remainder, expected
):
    assert scaled_divrem(value, numerator, denominator, remainder) == expected


def test_carried_remainder_cannot_conceal_overflow_in_the_product():
    with pytest.raises(OverflowError, match="64-bit"):
        scaled_divrem((MAX_WORK_INT + 1) // 2, 2, MAX_CORE_INT, -1)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"nx": 0},
        {"force_den": 0},
        {"force_num": -1},
        {"max_particles_per_node": 0},
        {"source_strength": MAX_CORE_INT + 1},
    ],
)
def test_invalid_config_rejected(kwargs):
    with pytest.raises((ValueError, OverflowError)):
        Config(**kwargs)

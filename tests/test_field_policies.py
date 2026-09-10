import pytest

from event_universe.core.state import MAX_CORE_INT
from event_universe.fields.policies import (
    nonnegative_sample,
    sample_changed_or_source,
    uniform_source,
    value_changed_or_source,
)
from event_universe.fields.scalar import ScalarSample, validate_sample


@pytest.mark.parametrize(
    "count,strength,expected", [(0, 64, 0), (3, 64, 192), (4, 0, 0), (2, MAX_CORE_INT, 4294967294)]
)
def test_uniform_source_has_an_exact_expected_value(count, strength, expected):
    assert uniform_source(count, strength) == expected


@pytest.mark.parametrize(
    "count,strength,error", [(-1, 64, ValueError), (1, -1, ValueError), (True, 1, TypeError)]
)
def test_invalid_source_is_rejected(count, strength, error):
    with pytest.raises(error):
        uniform_source(count, strength)


@pytest.mark.parametrize(
    "sample,expected",
    [
        (ScalarSample(-3, -1), ScalarSample()),
        (ScalarSample(0, -1), ScalarSample(0, -1)),
        (ScalarSample(3, 1), ScalarSample(3, 1)),
    ],
)
def test_nonnegative_policy_has_explicit_zero_and_negative_behavior(sample, expected):
    assert nonnegative_sample(sample) == expected


@pytest.mark.parametrize(
    "sample,denominator,error",
    [
        (ScalarSample(1, 7), 7, ValueError),
        (ScalarSample(), 0, ValueError),
        (ScalarSample(1.0, 0), 7, TypeError),
        (ScalarSample(MAX_CORE_INT + 1), 7, OverflowError),
    ],
)
def test_field_sample_contract_rejects_invalid_outputs(sample, denominator, error):
    with pytest.raises(error):
        validate_sample(sample, denominator)


@pytest.mark.parametrize(
    "previous,current,sources,legacy,complete",
    [
        (ScalarSample(1, 0), ScalarSample(1, 1), 0, False, True),
        (ScalarSample(1, 0), ScalarSample(2, 0), 0, True, True),
        (ScalarSample(1, 1), ScalarSample(1, 1), 0, False, False),
        (ScalarSample(1, 1), ScalarSample(1, 1), 1, True, True),
    ],
)
def test_activity_policies_distinguish_value_change_remainder_change_and_persistent_source(
    previous, current, sources, legacy, complete
):
    assert value_changed_or_source(previous, current, sources) is legacy
    assert sample_changed_or_source(previous, current, sources) is complete

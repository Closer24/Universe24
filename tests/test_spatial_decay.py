"""Independent integer extinction and signed dissipation examples."""

import pytest

from event_universe.core.disturbance_state import (
    MAX_VALUE,
    CostMeter,
    FieldDefinition,
    OperationCosts,
    pack,
    unpack,
)
from event_universe.core.spatial_state import DecayDefinition
from event_universe.fields.spatial import bounded_emission_amount
from event_universe.fields.spatial_decay import decay_populations


def decay(values, numerator=1, denominator=2, *, signed=True):
    field = FieldDefinition("generic", len(values), "unit", signed, True)
    zero = pack((0,) * len(values))
    populations = (pack(tuple(values)),) + (zero,) * 7
    survivors, losses = decay_populations(
        populations,
        DecayDefinition(numerator, denominator),
        field,
        CostMeter(OperationCosts((1,) * 9)),
    )
    return unpack(survivors[0]), losses


def test_half_retention_reaches_zero_without_an_immortal_unit():
    amount, lost = 20, 0
    for expected in (10, 5, 2, 1, 0):
        (amount,), loss = decay((amount,))
        lost += loss[0]
        assert amount == expected
        assert amount + lost == 20


@pytest.mark.parametrize("value", [1, -1])
def test_smallest_quantum_dies_even_with_very_weak_decay(value):
    assert decay((value,), MAX_VALUE - 1, MAX_VALUE) == ((0,), (value,))


def test_signed_components_approach_zero_without_claiming_direction_preservation():
    assert decay((-3, 1, 0)) == ((-1, 0, 0), (-2, 1, 0))
    assert decay((MAX_VALUE, -MAX_VALUE, 0), 0, 1) == (
        (0, 0, 0),
        (MAX_VALUE, -MAX_VALUE, 0),
    )


def test_unsigned_invalid_input_cannot_be_hidden_by_complete_decay():
    with pytest.raises(ValueError, match="negative"):
        decay((-1,), 0, 1, signed=False)


@pytest.mark.parametrize("numerator,denominator", [(1, 1), (2, 1), (-1, 2), (0, 0)])
def test_decay_rejects_infinite_retention_and_invalid_ratios(numerator, denominator):
    with pytest.raises(ValueError):
        decay((1,), numerator, denominator)


def test_signed_source_budget_counts_absolute_output_and_caps_before_packing():
    field = FieldDefinition("generic", 1, "unit", True, True)
    meter = CostMeter(OperationCosts((1,) * 9))
    remaining, residue = pack((5,)), pack((0,))
    actual = []
    for request in (2, -2, MAX_VALUE + 100, -2):
        amount, residue, remaining = bounded_emission_amount(
            (request,),
            residue,
            1,
            remaining,
            field,
            meter,
        )
        actual.append(unpack(amount)[0])
    assert actual == [2, -2, 1, 0]
    assert unpack(remaining) == unpack(residue) == (0,)

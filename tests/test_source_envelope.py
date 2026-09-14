"""Independent numerical expectations for bounded local source arithmetic."""

import pytest

from event_universe.core.disturbance_state import (
    MAX_VALUE,
    OPERATIONS,
    CostMeter,
    FieldDefinition,
    OperationCosts,
    pack,
    unpack,
)
from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.source_envelope_state import EnvelopeAmplitude, EnvelopeRemainder
from event_universe.fields.source_envelope import (
    local_output,
    output_cost,
    reduce_amplitude,
    squared_weight,
    validate_amplitude,
    weighted_emission,
)


def meter():
    return CostMeter(OperationCosts((1,) * len(OPERATIONS)))


def real_matrix(rows):
    return tuple(tuple((value, 0) for value in row) for row in rows)


MIXER = real_matrix(((5, 0, 0, 0), (0, 3, -4, 0), (0, 4, 3, 0), (0, 0, 0, 5)))
INVERSE = real_matrix(((5, 0, 0, 0), (0, 3, 4, 0), (0, -4, 3, 0), (0, 0, 0, 5)))
FIELD = FieldDefinition("configured_source", 1, "unit", True, True)


def test_mixer_splits_single_excitation_and_inverse_recombines_it():
    inputs = (EnvelopeAmplitude(1), EnvelopeAmplitude())
    split = tuple(local_output(MIXER, inputs, i, meter()) for i in range(2))
    assert split == (EnvelopeAmplitude(3, 0, 5), EnvelopeAmplitude(4, 0, 5))
    assert tuple(squared_weight(v, meter()) for v in split) == ((9, 25), (16, 25))
    assert tuple(local_output(INVERSE, split, i, meter()) for i in range(2)) == inputs


def test_register_one_is_basis_two_in_a_pair():
    inputs = (EnvelopeAmplitude(), EnvelopeAmplitude(1))
    assert local_output(MIXER, inputs, 0, meter()) == EnvelopeAmplitude(-4, 0, 5)
    assert local_output(MIXER, inputs, 1, meter()) == EnvelopeAmplitude(3, 0, 5)


def test_complex_vacuum_coefficient_removes_common_phase_without_square_root():
    # (1+i) times the real mixer has implicit scale 50, whose square root is
    # irrational. Its relative one-excitation amplitudes are still 3/5 and 4/5.
    matrix = tuple(tuple((real, real) for real, _ in row) for row in MIXER)
    inputs = (EnvelopeAmplitude(1), EnvelopeAmplitude())
    assert local_output(matrix, inputs, 0, meter()) == EnvelopeAmplitude(3, 0, 5)
    assert local_output(matrix, inputs, 1, meter()) == EnvelopeAmplitude(4, 0, 5)


def test_single_mode_relative_phase_preserves_complex_weight():
    matrix = (((1, 1), (0, 0)), ((0, 0), (-1, 1)))
    value = local_output(matrix, (EnvelopeAmplitude(3, 4, 5),), 0, meter())
    assert value == EnvelopeAmplitude(-4, 3, 5)
    assert squared_weight(value, meter()) == (1, 1)


def test_reduction_preserves_phase_and_zero_is_canonical():
    assert reduce_amplitude(-6, 8, 10, meter()) == EnvelopeAmplitude(-3, 4, 5)
    assert reduce_amplitude(0, 0, MAX_VALUE, meter()) == EnvelopeAmplitude()


@pytest.mark.parametrize(
    "inputs",
    [
        (EnvelopeAmplitude(1), EnvelopeAmplitude()),
        (EnvelopeAmplitude(3, 0, 5), EnvelopeAmplitude(4, 0, 5)),
        (EnvelopeAmplitude(), EnvelopeAmplitude()),
        (EnvelopeAmplitude(0, 1), EnvelopeAmplitude()),
    ],
)
def test_output_tariff_is_reserved_independently_of_amplitudes(inputs):
    costs = OperationCosts((1,) * len(OPERATIONS))
    expected = output_cost(MIXER, costs)
    for index in range(2):
        actual = CostMeter(costs)
        local_output(MIXER, inputs, index, actual)
        assert actual.total == expected > 0


@pytest.mark.parametrize("numerator,expected", [(25, 9), (-25, -9)])
def test_weighted_source_uses_exact_signed_probability_and_finite_allowance(numerator, expected):
    amount, residues, remaining = weighted_emission(
        (numerator,),
        1,
        EnvelopeAmplitude(3, 0, 5),
        (EnvelopeRemainder(),),
        pack((100,)),
        FIELD,
        meter(),
    )
    assert unpack(amount) == (expected,)
    assert residues == (EnvelopeRemainder(),)
    assert unpack(remaining) == (91,)


def test_changing_weight_denominator_keeps_previously_accumulated_fraction():
    amount, residues, remaining = weighted_emission(
        (1,),
        1,
        EnvelopeAmplitude(1, 0, 2),
        (EnvelopeRemainder(),),
        pack((10,)),
        FIELD,
        meter(),
    )
    assert unpack(amount) == (0,)
    assert residues == (EnvelopeRemainder(1, 4),)
    amount, residues, remaining = weighted_emission(
        (7,),
        1,
        EnvelopeAmplitude(1, 0, 3),
        residues,
        remaining,
        FIELD,
        meter(),
    )
    # 1/4 + 7/9 = 37/36: one whole unit and 1/36 remain.
    assert unpack(amount) == (1,)
    assert residues == (EnvelopeRemainder(1, 36),)
    assert unpack(remaining) == (9,)


def test_negative_fraction_and_finite_exhaustion_leave_no_debt():
    amount, residues, remaining = weighted_emission(
        (-5,),
        1,
        EnvelopeAmplitude(1, 0, 2),
        (EnvelopeRemainder(-1, 3),),
        pack((1,)),
        FIELD,
        meter(),
    )
    assert unpack(amount) == (-1,)
    assert residues == (EnvelopeRemainder(),)
    assert unpack(remaining) == (0,)
    again = weighted_emission((-100,), 1, EnvelopeAmplitude(1), residues, remaining, FIELD, meter())
    assert unpack(again[0]) == (0,)
    assert again[1:] == (residues, remaining)


def test_source_denominator_is_distinct_from_weight_denominator():
    amount, residues, remaining = weighted_emission(
        (250,),
        3,
        EnvelopeAmplitude(3, 0, 5),
        (EnvelopeRemainder(),),
        pack((100,)),
        FIELD,
        meter(),
    )
    assert unpack(amount) == (30,)
    assert residues == (EnvelopeRemainder(),)
    assert unpack(remaining) == (70,)


def test_vector_components_keep_independent_signs_remainders_and_allowances():
    field = FieldDefinition("configured_vector", 3, "unit", True, True)
    amount, residues, remaining = weighted_emission(
        (4, -2, 1),
        1,
        EnvelopeAmplitude(1, 0, 2),
        (EnvelopeRemainder(), EnvelopeRemainder(-1, 2), EnvelopeRemainder(3, 4)),
        pack((9, 9, 9)),
        field,
        meter(),
    )
    assert unpack(amount) == (1, -1, 1)
    assert residues == (EnvelopeRemainder(),) * 3
    assert unpack(remaining) == (8, 8, 8)


def test_subunit_source_is_not_lost_over_successive_ticks():
    residues, remaining = (EnvelopeRemainder(),), pack((10,))
    outputs = []
    for _ in range(4):
        amount, residues, remaining = weighted_emission(
            (1,),
            1,
            EnvelopeAmplitude(1, 0, 2),
            residues,
            remaining,
            FIELD,
            meter(),
        )
        outputs.append(unpack(amount)[0])
    assert outputs == [0, 0, 0, 1]
    assert residues == (EnvelopeRemainder(),)
    assert unpack(remaining) == (9,)


def test_unsigned_source_rejects_negative_emission():
    field = FieldDefinition("positive_source", 1, "unit", False, True)
    with pytest.raises(ValueError, match="unsigned"):
        weighted_emission(
            (-1,), 1, EnvelopeAmplitude(1), (EnvelopeRemainder(),), pack((1,)), field, meter()
        )


@pytest.mark.parametrize("value", [EnvelopeAmplitude(2), EnvelopeAmplitude(1, 1)])
def test_probability_above_one_is_rejected_instead_of_normalized(value):
    with pytest.raises(ValueError, match="probability exceeds"):
        validate_amplitude(value)


def test_changing_denominator_overflow_preserves_input_state():
    residues = (EnvelopeRemainder(1, 1_000_000_007),)
    remaining = pack((5,))
    with pytest.raises(ValueError, match="integer bound"):
        weighted_emission((1,), 1, EnvelopeAmplitude(1, 0, 2), residues, remaining, FIELD, meter())
    assert residues == (EnvelopeRemainder(1, 1_000_000_007),)
    assert unpack(remaining) == (5,)


def test_matrix_product_overflow_is_detected_before_cancellation():
    matrix = (((MAX_WORK_INT, MAX_WORK_INT), (0, 0)), ((0, 0), (1, 0)))
    with pytest.raises(OverflowError, match="64-bit"):
        local_output(matrix, (EnvelopeAmplitude(),), 0, meter())


@pytest.mark.parametrize(
    "matrix,match",
    [
        (real_matrix(((0, 0), (0, 1))), "vacuum"),
        (real_matrix(((1, 1), (0, 1))), "occupation"),
        ((((1, 0),),), "size"),
    ],
)
def test_invalid_matrix_contracts_are_rejected(matrix, match):
    with pytest.raises(ValueError, match=match):
        local_output(matrix, (EnvelopeAmplitude(1),), 0, meter())

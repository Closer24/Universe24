"""Independent numerical contracts for delivered source-facing field values."""

import pytest

from event_universe.core.state import MAX_CORE_INT
from event_universe.dynamics import FieldTurning
from event_universe.dynamics.turning import full_response
from event_universe.fields.faces import face_imbalance, scalar_broadcast


def test_delivered_faces_drive_longitudinal_exchange_and_balanced_inertia():
    turning = FieldTurning(select_direction=full_response)
    vector = face_imbalance((9, 4, 2, 10, 6, 6))
    assert vector == (5, -8, 0)
    result = turning.apply((3, 0, 0), (0, 0, 0), vector, (0, 0, 0), numerator=1, denominator=1)
    assert result.momentum == (8, -8, 0)
    assert result.field_momentum == (-5, 8, 0)
    balanced = turning.apply(
        (3, -2, 1),
        (0, 0, 0),
        face_imbalance((7, 7, -3, -3, 2, 2)),
        (0, 0, 0),
        numerator=1,
        denominator=1,
    )
    assert balanced.momentum == (3, -2, 1)
    assert balanced.impulse == balanced.remainders == (0, 0, 0)


def test_signed_faces_validate_registers_before_work_width_difference():
    assert scalar_broadcast(7) == (7, 7, 7, 7, 7, 7)
    assert scalar_broadcast(-3) == (-3, -3, -3, -3, -3, -3)
    assert face_imbalance((MAX_CORE_INT, -MAX_CORE_INT, -3, 2, 0, 0)) == (2 * MAX_CORE_INT, -5, 0)
    with pytest.raises(OverflowError):
        face_imbalance((MAX_CORE_INT + 1, MAX_CORE_INT + 1, 0, 0, 0, 0))
    with pytest.raises(OverflowError):
        scalar_broadcast(MAX_CORE_INT + 1)
    for invalid in (True, 1.0):
        with pytest.raises(TypeError):
            scalar_broadcast(invalid)


@pytest.mark.parametrize(
    "values", [(0, 0, 0), (0, 0, 0, 0, 0, 0, 0), (True, 0, 0, 0, 0, 0), (1.0, 0, 0, 0, 0, 0)]
)
def test_malformed_delivered_face_records_are_rejected(values):
    with pytest.raises((TypeError, ValueError)):
        face_imbalance(values)

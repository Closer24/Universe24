"""Payload validation rejects exactly what decoding rejects, without decoding."""

import pytest

from event_universe.core import disturbance_state
from event_universe.core.disturbance_state import MAX_VALUE, FieldDefinition, pack, unpack
from event_universe.core.spatial_state import SpatialState

MAX_CODE = 2 * MAX_VALUE + 1
BAD_CODE = "invalid positive integer component code"
NEGATIVE = "negative value forbidden for field probe"
COUNT = "invalid component count for field probe"
PHASES = "spatial allocation phases must be nonnegative"


def reference_field_validation(definition, values):
    """The original implementation: decode every component, then inspect the signs."""
    if len(values) != definition.components:
        raise ValueError(f"invalid component count for field {definition.name}")
    decoded = unpack(values)
    if not definition.signed and any(v < 0 for v in decoded):
        raise ValueError(f"negative value forbidden for field {definition.name}")


def reference_spatial_validation(state, components):
    """The original implementation: decode every payload, then inspect the phases."""
    if type(components) is not int or not 1 <= components <= 32:
        raise ValueError("spatial fields require one to thirty-two components")
    if type(state.received_mask) is not int or not 0 <= state.received_mask < 64:
        raise ValueError("received mask requires six bounded port bits")
    for values, size in (
        (state.populations, 8),
        (state.allocation_phases, 8),
        (state.delivered, 6),
    ):
        if len(values) != size:
            raise ValueError("spatial state requires eight octants and six delivered channels")
        for value in values:
            if len(value) != components:
                raise ValueError("spatial state component count differs from the field")
            unpack(value)
    if any(value < 0 for payload in state.allocation_phases for value in unpack(payload)):
        raise ValueError("spatial allocation phases must be nonnegative")


def outcome(action):
    try:
        action()
    except ValueError as error:
        return str(error)
    return None


FIELD_CASES = [
    ("signed_values", pack((3, -4, 0)), True, None),
    ("unsigned_values", pack((3, 4, 0)), False, None),
    ("negative_in_unsigned_field", pack((3, -4, 0)), False, NEGATIVE),
    ("largest_magnitudes", (MAX_CODE, MAX_CODE - 1, 1), True, None),
    ("largest_negative_in_unsigned_field", (MAX_CODE, MAX_CODE - 1, 1), False, NEGATIVE),
    ("zero_code", (1, 0, 1), True, BAD_CODE),
    ("code_above_bound", (1, MAX_CODE + 1, 1), True, BAD_CODE),
    ("negative_code", (1, -3, 1), False, BAD_CODE),
    ("bad_code_before_sign_check", (0, 2, 2), False, BAD_CODE),
    ("wrong_component_count", pack((1, 2)), True, COUNT),
    ("count_before_codes", (0, 0), True, COUNT),
    ("float_component", (1, 2.0, 3), True, BAD_CODE),
    ("bool_component", (1, True, 3), True, BAD_CODE),
]


@pytest.mark.parametrize(
    "values, signed, expected",
    [case[1:] for case in FIELD_CASES],
    ids=[case[0] for case in FIELD_CASES],
)
def test_field_validation_matches_the_decoding_reference(values, signed, expected):
    definition = FieldDefinition("probe", 3, "unit", signed, True)
    assert outcome(lambda: definition.validate(values)) == expected
    assert outcome(lambda: reference_field_validation(definition, values)) == expected


def spatial(*, populations=None, phases=None, delivered=None, mask=0):
    zero = pack((0, 0))
    return SpatialState(
        (zero,) * 8 if populations is None else populations,
        (zero,) * 8 if phases is None else phases,
        (zero,) * 6 if delivered is None else delivered,
        mask,
    )


SPATIAL_CASES = [
    ("zero_state", spatial(), 2, None),
    ("negative_populations_are_allowed", spatial(populations=(pack((-5, 7)),) * 8), 2, None),
    ("negative_allocation_phase", spatial(phases=(pack((0, 1)),) * 7 + (pack((0, -1)),)), 2, PHASES),
    ("largest_phase", spatial(phases=((MAX_CODE, 1),) * 8), 2, None),
    ("zero_code_in_delivered", spatial(delivered=((1, 0),) * 6), 2, BAD_CODE),
    ("code_above_bound_in_population", spatial(populations=((MAX_CODE + 1, 1),) * 8), 2, BAD_CODE),
    ("bad_phase_code_before_sign_check", spatial(phases=((2, 0),) * 8), 2, BAD_CODE),
    ("float_component", spatial(populations=((1.0, 1),) * 8), 2, BAD_CODE),
    (
        "component_count_differs",
        spatial(),
        3,
        "spatial state component count differs from the field",
    ),
    (
        "seven_octants",
        spatial(populations=(pack((0, 0)),) * 7),
        2,
        "spatial state requires eight octants and six delivered channels",
    ),
    ("bad_mask", spatial(mask=64), 2, "received mask requires six bounded port bits"),
    ("bad_component_count", spatial(), 0, "spatial fields require one to thirty-two components"),
]


@pytest.mark.parametrize(
    "state, components, expected",
    [case[1:] for case in SPATIAL_CASES],
    ids=[case[0] for case in SPATIAL_CASES],
)
def test_spatial_state_validation_matches_the_decoding_reference(state, components, expected):
    assert outcome(lambda: state.validate(components)) == expected
    assert outcome(lambda: reference_spatial_validation(state, components)) == expected


def test_validation_inspects_codes_without_decoding_them(monkeypatch):
    decoded = []
    original = disturbance_state.decode

    def counting(code):
        decoded.append(code)
        return original(code)

    monkeypatch.setattr(disturbance_state, "decode", counting)
    FieldDefinition("probe", 3, "unit", False, True).validate(pack((3, 4, 0)))
    spatial(populations=(pack((-5, 7)),) * 8).validate(2)
    assert decoded == []
    assert unpack(pack((3, -4))) == (3, -4)
    assert decoded == [7, 8]

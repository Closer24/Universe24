"""Validate the explicit directional timing capability at public boundaries."""

from .disturbance_state import InitialState, bounded


def validate_directional_delay(initial: InitialState) -> None:
    rule = initial.directional_delay
    if rule is None:
        return
    if type(rule.field) is not int or not 0 <= rule.field < len(initial.fields):
        raise ValueError("directional delay field index is invalid")
    if bounded(rule.divisor) < 1:
        raise ValueError("directional delay divisor must be positive")
    if initial.fields[rule.field].components != 3 or not any(
        s.field == rule.field for s in initial.spatial_fields
    ):
        raise ValueError("directional delay requires a spatial vector field")
    if (
        initial.event_program is not None
        or initial.spatial_couplings
        or initial.spatial_interactions
        or initial.unit_system is not None
    ):
        raise ValueError(
            "directional delay excludes event programs, spatial responses and SI calibration"
        )
    if any(initial.disturbances[e.type_index].transport.mode != "hold" for e in initial.emissions):
        raise ValueError("directional delay currently requires held emitters")

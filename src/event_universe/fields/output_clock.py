"""Configured integer scaling of an actually local transient input sample."""

from ..core.coupling_selectors import selected_types
from ..core.disturbance_state import InitialState, bounded, unpack
from ..core.integer import checked_work
from ..core.spatial_state import SpatialPlan, ray_stock


def sample_output_clock(initial: InitialState, plan: SpatialPlan) -> tuple[int, tuple[int, ...]]:
    index = next(
        i
        for i, definition in enumerate(initial.spatial_fields)
        if definition.field == initial.computation_field
    )
    sample = bounded(sum(ray_stock(port[index]) for port in plan.rays)) if plan.rays else 0
    assert initial.output_clock_gain is not None
    return sample, output_delays(sample, initial.output_clock_gain)


def output_delays(sample: int, gain: int) -> tuple[int, ...]:
    if bounded(sample) < 0 or bounded(gain) < 0:
        raise ValueError("output clock sample and gain must be nonnegative")
    return (bounded(checked_work(sample * gain)),) * 6


def validate_output_clock(initial: InitialState) -> None:
    """Reject compositions outside the explicitly bounded initial profile."""
    if initial.computation_field is None or initial.link_ticks != 1:
        raise ValueError("output_clock requires computation_field and fixed link_ticks 1")
    if (
        initial.node_execution
        or initial.spatial_computation_delay
        or initial.field_phase_first
        or initial.ray_delay
        or initial.delay_direction is not None
        or initial.least_delay_routing
        or initial.event_program is not None
        or initial.field_rules
        or initial.spatial_interactions
        or initial.spatial_couplings
        or initial.couplings
    ):
        raise ValueError("output_clock does not support another clock or coupled field program")
    if initial.spatial_seeds:
        raise ValueError("output_clock initial field stock requires a declared emission")
    if initial.conservation_contract is not None or (
        initial.conservation is not None and initial.conservation.spatial is not None
    ):
        raise ValueError("output_clock token profile does not support physical field E/P readouts")
    for definition in initial.spatial_fields:
        if (
            not definition.rays
            or any(unpack(definition.baseline))
            or definition.self_exclusion
            or definition.claims
            or definition.bonded
            or definition.kerengonen
            or definition.decay is not None
            or definition.euclidean
            or definition.pace_numerator != definition.pace_denominator
        ):
            raise ValueError("output_clock requires plain non-self-excluding unpaced rays")
    reserves = {initial.spatial_fields[rule.spatial_field].field for rule in initial.emissions}
    if any(
        assignment.field in reserves for rule in initial.interactions for assignment in rule.assignments
    ):
        raise ValueError("output_clock source reserve cannot be written by material interactions")
    for emission in initial.emissions:
        if not emission.funded or not emission.whole_pulse or emission.denominator != 1:
            raise ValueError("output_clock emissions require funded integer whole pulses")
        if emission.dissolve_over or emission.recoil_field is not None:
            raise ValueError("output_clock source profile does not support dissolution or recoil")
        for kind_index in selected_types(emission):
            kind = initial.disturbances[kind_index]
            if kind.transport.mode != "hold" or kind.updates:
                raise ValueError("output_clock requires stationary unchanged emitters")

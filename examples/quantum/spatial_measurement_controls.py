"""Exact finite position-measurement controls, never physical feedback.

The projective click retains a position basis state for comparison with the
ordinary capture's explicit re-encoding. The native absorbing instrument itself
leaves vacuum. Operation changes below are not a simulated apparatus reservoir.
"""

from fractions import Fraction

from event_universe.quantum import DeferredQuantum, EventNetworkConfig, LocalInstrument, LocalUnitary
from event_universe.quantum.state import checked_amp
from examples.quantum.spatial_momentum import local_position_moments, spatial_moments

MODES = (0, 1, 2, 3)
EDGES = ((0, 1), (1, 2), (2, 3), (3, 0))


def _matrix(rows):
    return tuple(
        tuple(checked_amp(value, 0) if type(value) is int else checked_amp(*value) for value in row)
        for row in rows
    )


def ring_wave(phase):
    """Prepare equal densities with distinct spatial phases through local gates."""
    if type(phase) is not int or phase not in (-1, 0, 1):
        raise ValueError("phase must be -1, 0 or 1")
    network = DeferredQuantum().bind_event_network(
        EventNetworkConfig(((0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)), occupied=(0,))
    )
    # Two local split layers give one excitation uniformly around the square.
    # Complex integer coefficients retain an exact common normalization.
    mix = LocalUnitary(
        _matrix(((2, 0, 0, 0), (0, (1, 1), (1, 1), 0), (0, (1, 1), (-1, -1), 0), (0, 0, 0, 2)))
    )
    network.step(((mix, (0, 1)),))
    network.step(((mix, (0, 3)), (mix, (1, 2))))
    phases = (1, (0, phase), -1, (0, -phase)) if phase else (1, 1, 1, 1)
    network.step(
        tuple((LocalUnitary(_matrix(((1, 0), (0, value)))), (q,)) for q, value in enumerate(phases))
    )
    return network


def _measure_case(phase):
    outcomes = []
    instrument = LocalInstrument((_matrix(((1, 0), (0, 0))), _matrix(((0, 0), (0, 1)))))
    for selected in (0, 1):
        network = ring_wave(phase)
        before = spatial_moments(network, MODES, EDGES)
        decision = network.prepare(100, 0, instrument)
        probability = Fraction(decision.weights[selected], decision.total_weight)
        ticket = 0 if selected == 0 else decision.total_weight - 1
        record = network.commit(decision, ticket)
        assert record.outcome == selected
        after = spatial_moments(network, MODES, EDGES)
        if selected:
            local = local_position_moments((-1, 1))
            assert all(after[key] == value for key, value in local.items())
        outcomes.append(
            {
                "outcome": "click" if selected else "no_click",
                "probability": probability,
                "moments": after,
            }
        )
    quantities = ("mean_momentum", "second_moment")
    ensemble = {
        key: sum(row["probability"] * row["moments"][key] for row in outcomes) for key in quantities
    }
    drift = {key: ensemble[key] - before[key] for key in quantities}
    for row in outcomes:
        row["conditional_deviation_from_ensemble"] = {
            key: row["moments"][key] - ensemble[key] for key in quantities
        }
    assert all(
        sum(row["probability"] * row["conditional_deviation_from_ensemble"][key] for row in outcomes)
        == 0
        for key in quantities
    )
    return {
        "phase": phase,
        "before": before,
        "outcomes": outcomes,
        "nonselective_after": ensemble,
        "ensemble_operation_change": drift,
        "apparatus_exchange": "not_simulated",
        "joint_energy_momentum_closure": "not_established",
    }


def measurement_controls():
    """Separate phase sensitivity, conditional selection and measurement work."""
    cases = [_measure_case(phase) for phase in (-1, 0, 1)]
    for row in cases:
        assert row["outcomes"][1]["probability"] == Fraction(1, 4)
        assert row["outcomes"][1]["moments"]["mean_momentum"] == 0
        assert row["outcomes"][1]["moments"]["variance"] == 2
    positive = cases[-1]
    assert positive["before"]["mean_momentum"] == 2
    assert positive["before"]["second_moment"] == 4
    assert positive["outcomes"][0]["moments"]["mean_momentum"] == Fraction(4, 3)
    assert positive["outcomes"][0]["moments"]["second_moment"] == Fraction(10, 3)
    assert positive["nonselective_after"] == {"mean_momentum": 1, "second_moment": 3}
    assert cases[1]["ensemble_operation_change"]["second_moment"] == 1
    return cases

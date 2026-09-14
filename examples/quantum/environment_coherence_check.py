"""Bounded coherent-environment controls using the existing quantum owner.

These are named internal registers at one Node, not moving photons or a
Newtonian trajectory. Supplied unitary gates retain the environment explicitly;
only the final subsystem probabilities are inspected. No outcomes are sampled.
"""

import json
from fractions import Fraction

from event_universe.quantum import DeferredQuantum, EventNetworkConfig, LocalUnitary
from event_universe.quantum.operations import dephasing, integer_matrix, permutation

H = LocalUnitary(integer_matrix(((1, 1), (1, -1))))
Z = LocalUnitary(integer_matrix(((1, 0), (0, -1))))
CX = permutation((0, 3, 2, 1))
# The first register is the low-order basis index. On its level 1, rotate
# the environmental register by R = [[3, -4], [4, 3]] / 5.
CONTROLLED_ROTATION = LocalUnitary(
    integer_matrix(((5, 0, 0, 0), (0, 3, 0, -4), (0, 0, 5, 0), (0, 4, 0, 3)))
)
INVERSE_CONTROLLED_ROTATION = LocalUnitary(
    integer_matrix(((5, 0, 0, 0), (0, 3, 0, 4), (0, 0, 5, 0), (0, -4, 0, 3)))
)


def _network(environment_count):
    names = ("system",) + tuple(f"environment_{i}" for i in range(environment_count))
    return DeferredQuantum().bind_event_network(
        EventNetworkConfig(
            ((0, 0, 0),) * len(names),
            dimensions=(2,) * len(names),
            initial_levels=(0,) * len(names),
            register_names=names,
        )
    )


def _observe(network, expected):
    before = (network.tick, network.events, network.records)
    reply = network.query(0)
    measured = tuple(Fraction(weight, sum(reply.weights)) for weight in reply.weights)
    assert measured == expected
    assert (network.tick, network.events, network.records) == before
    assert not network.records and reply.world_ticks == 0
    return {
        "probabilities": list(map(str, measured)),
        "expected": list(map(str, expected)),
        "world_ticks": network.tick,
        "event_count": len(network.events),
        "query_evaluated_events": reply.evaluated_nodes,
        "peak_terms": reply.peak_terms,
        "measurement_records": len(network.records),
        "query_world_ticks": reply.world_ticks,
        "query_model_cost": reply.model_cost,
    }


def _fresh_environment_case(environment_count, phase_pi=False, reverse=False):
    network = _network(environment_count)
    network.step(((H, (0,)),))
    for environment in range(1, environment_count + 1):
        network.step(((CONTROLLED_ROTATION, (0, environment)),))
    if reverse:
        for environment in range(environment_count, 0, -1):
            network.step(((INVERSE_CONTROLLED_ROTATION, (0, environment)),))
    if phase_pi:
        network.step(((Z, (0,)),))
    network.step(((H, (0,)),))
    # The path-conditioned environmental states have overlap (3/5)^n.
    visibility = Fraction(1) if reverse else Fraction(3, 5) ** environment_count
    signed_visibility = -visibility if phase_pi else visibility
    expected = ((1 + signed_visibility) / 2, (1 - signed_visibility) / 2)
    return {
        "fresh_environment_registers": environment_count,
        "phase_pi": phase_pi,
        "reversed": reverse,
        "expected_visibility": str(visibility),
        **_observe(network, expected),
    }


def _reused_environment_case(interactions, discard_record=False):
    network = _network(1)
    network.step(((H, (0,)),))
    for interaction in range(interactions):
        network.step(((CX, (0, 1)),))
        if discard_record and interaction == 0:
            network.step(((dephasing(2), (1,)),))
    network.step(((H, (0,)),))
    # CX squared is identity. Discarding its basis record prevents erasure.
    expected = (
        (Fraction(1, 2), Fraction(1, 2))
        if interactions % 2 or discard_record
        else (Fraction(1), Fraction(0))
    )
    return {
        "interactions_with_same_environment": interactions,
        "discarded_environment_basis_record": discard_record,
        **_observe(network, expected),
    }


def run_environment_controls():
    """Return exact probabilities and host audit counters for 16 bounded runs."""
    fresh = []
    reversed_cases = []
    for count in range(4):
        bright = _fresh_environment_case(count)
        dark = _fresh_environment_case(count, phase_pi=True)
        measured_visibility = Fraction(bright["probabilities"][0]) - Fraction(dark["probabilities"][0])
        assert measured_visibility == Fraction(3, 5) ** count
        fresh.append(
            {
                "fresh_environment_registers": count,
                "visibility": str(measured_visibility),
                "phase_zero": bright,
                "phase_pi": dark,
            }
        )
        reversed_cases.append(_fresh_environment_case(count, reverse=True))
    return {
        "status": "pass",
        "model": "deferred-register-network-v2",
        "scope": "API quantum-owner control; all named registers share Node (0, 0, 0).",
        "fresh_environment": fresh,
        "retained_environment_reversed": reversed_cases,
        "reused_environment": [_reused_environment_case(n) for n in range(3)],
        "discarded_record_reversal": _reused_environment_case(2, discard_record=True),
        "interpretation": (
            "Entanglement reduces subsystem interference without selecting an outcome. "
            "Reversing retained environmental interactions restores interference. "
            "An explicitly discarded basis record prevents that reversal."
        ),
        "limits": [
            "The gates and basis are supplied, not derived from a spatial scattering law.",
            "No physical environment density, collision cross section or time unit is calibrated.",
            "No momentum, field-energy or emerging classical-trajectory claim is tested here.",
            "Quantum queries use the explicit Q-ORACLE-1 model assumption and measured host work.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run_environment_controls(), indent=2))

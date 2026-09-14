"""Exact finite momentum-state exchange inside the existing quantum owner.

The supplied equal-mass SWAP transfers a coherent state to a local environment.
Momentum labels are diagnostic model inputs, not a derived spatial Hamiltonian.
This independent control does not give the moments-only runtime a joint state.
"""

from collections import defaultdict
from fractions import Fraction

from event_universe.quantum import DeferredQuantum, EventNetworkConfig, LocalUnitary
from event_universe.quantum.operations import dephasing, integer_matrix, permutation

LABELS = (-1, 1, 3, 5)
H = LocalUnitary(integer_matrix(((1, 1, 0, 0), (1, -1, 0, 0), (0, 0, 1, 1), (0, 0, 1, -1))))
ROTATION = LocalUnitary(integer_matrix(((3, -4, 0, 0), (4, 3, 0, 0), (0, 0, 3, -4), (0, 0, 4, 3))))
INVERSE_ROTATION = LocalUnitary(
    integer_matrix(((3, 4, 0, 0), (-4, 3, 0, 0), (0, 0, 3, 4), (0, 0, -4, 3)))
)
# Register zero is the low-order mixed-radix basis index.
SWAP = permutation(tuple(index // 4 + 4 * (index % 4) for index in range(16)))


def _network(levels=(0, 2)):
    return DeferredQuantum().bind_event_network(
        EventNetworkConfig(
            ((0, 0, 0), (0, 0, 0)),
            dimensions=(4, 4),
            initial_levels=levels,
            register_names=("target_momentum", "environment_momentum"),
        )
    )


def _marginals(network):
    results = []
    for register in range(2):
        reply = network.query(register)
        assert reply.world_ticks == 0
        probabilities = tuple(Fraction(value, sum(reply.weights)) for value in reply.weights)
        mean = sum(p * value for p, value in zip(probabilities, LABELS, strict=True))
        second = sum(p * value * value for p, value in zip(probabilities, LABELS, strict=True))
        results.append(
            {
                "probabilities": list(map(str, probabilities)),
                "mean_momentum": str(mean),
                "variance": str(second - mean * mean),
            }
        )
    return results


def _joint_audit(network):
    """Inspect pure-state branch distributions without physical feedback."""
    before = (network.tick, network.events, network.records)
    state = network.joint_state()
    norm = sum(amplitude.real**2 + amplitude.imag**2 for _, amplitude in state)
    momentum = defaultdict(Fraction)
    energy = defaultdict(Fraction)
    branches = []
    for index, amplitude in state:
        left, right = LABELS[index % 4], LABELS[index // 4]
        probability = Fraction(amplitude.real**2 + amplitude.imag**2, norm)
        total = left + right
        doubled_energy = left * left + right * right
        momentum[total] += probability
        energy[doubled_energy] += probability
        branches.append(
            {
                "momenta": [left, right],
                "probability": str(probability),
                "total_momentum": total,
                "doubled_kinetic_energy": doubled_energy,
            }
        )
    marginals = _marginals(network)
    assert before == (network.tick, network.events, network.records)
    assert not network.records
    return {
        "marginals": marginals,
        "branches": branches,
        "total_momentum_distribution": {str(k): str(v) for k, v in sorted(momentum.items())},
        "doubled_kinetic_energy_distribution": {str(k): str(v) for k, v in sorted(energy.items())},
    }


def _exchange_case(preparation, inverse, probabilities):
    network = _network()
    network.step(((preparation, (0,)),))
    before = _joint_audit(network)
    expected = [*map(str, probabilities), "0", "0"]
    assert before["marginals"][0]["probabilities"] == expected
    assert before["marginals"][1]["probabilities"] == ["0", "0", "1", "0"]
    network.step(((SWAP, (0, 1)),))
    after = _joint_audit(network)
    assert after["marginals"] == list(reversed(before["marginals"]))
    assert (
        before["total_momentum_distribution"]
        == after["total_momentum_distribution"]
        == {
            "2": str(probabilities[0]),
            "4": str(probabilities[1]),
        }
    )
    assert (
        before["doubled_kinetic_energy_distribution"]
        == after["doubled_kinetic_energy_distribution"]
        == {"10": "1"}
    )
    # Reversal tests phase retention in addition to equal marginal moments.
    network.step(((SWAP, (0, 1)),))
    network.step(((inverse, (0,)),))
    reversed_state = _joint_audit(network)
    assert reversed_state["marginals"][0]["probabilities"] == ["1", "0", "0", "0"]
    assert reversed_state["marginals"][1]["probabilities"] == ["0", "0", "1", "0"]
    return {
        "before": before,
        "after": after,
        "reversed": reversed_state,
        "measurement_records": len(network.records),
        "model_ticks": network.tick,
    }


def _all_basis_cases():
    cases = []
    for left in range(4):
        for right in range(4):
            network = _network((left, right))
            before = _joint_audit(network)
            network.step(((SWAP, (0, 1)),))
            after = _joint_audit(network)
            assert [branch["momenta"] for branch in after["branches"]] == [[LABELS[right], LABELS[left]]]
            assert before["total_momentum_distribution"] == after["total_momentum_distribution"]
            assert (
                before["doubled_kinetic_energy_distribution"]
                == after["doubled_kinetic_energy_distribution"]
            )
            cases.append({"input": before["branches"][0], "output": after["branches"][0]})
    return cases


def _without_exchange():
    network = _network()
    network.step(((H, (0,)),))
    before = _joint_audit(network)
    network.step(())
    after = _joint_audit(network)
    assert after == before
    assert after["marginals"][0]["variance"] == "1"
    return after


def _discarded_coherence_control():
    network = _network()
    network.step(((H, (0,)),))
    network.step(((SWAP, (0, 1)),))
    network.step(((dephasing(4), (1,)),))
    network.step(((SWAP, (0, 1)),))
    network.step(((H, (0,)),))
    marginals = _marginals(network)
    assert marginals[0]["probabilities"] == ["1/2", "1/2", "0", "0"]
    assert marginals[1]["probabilities"] == ["0", "0", "1", "0"]
    assert not network.records
    return {
        "marginals_after_attempted_reversal": marginals,
        "measurement_records": len(network.records),
        "environment_dephasing_explicitly_supplied": True,
    }


def run_quantum_exchange_controls():
    """Verify an exact unitary control separately from ordinary moment closure."""
    equal_weights = _exchange_case(H, H, (Fraction(1, 2), Fraction(1, 2)))
    assert equal_weights["before"]["marginals"][0]["mean_momentum"] == "0"
    assert equal_weights["before"]["marginals"][0]["variance"] == "1"
    assert equal_weights["after"]["marginals"][0]["mean_momentum"] == "3"
    assert equal_weights["after"]["marginals"][0]["variance"] == "0"
    return {
        "status": "pass",
        "scope": "Independent exact quantum-owner control; both registers share Node (0,0,0).",
        "momentum_labels": list(LABELS),
        "equal_mass_units": 1,
        "equal_weight_case": equal_weights,
        "unequal_weight_case": _exchange_case(
            ROTATION, INVERSE_ROTATION, (Fraction(9, 25), Fraction(16, 25))
        ),
        "basis_cases": _all_basis_cases(),
        "without_exchange": _without_exchange(),
        "discarded_coherence_control": _discarded_coherence_control(),
        "limits": [
            "The momentum basis and SWAP are supplied, not derived from spatial scattering.",
            "Preparation and inverse preparation are controls, not energy-conserving collisions.",
            "The SWAP preserves the full finite momentum and kinetic-energy distributions.",
            "This does not give a moments-only ordinary runtime phase or joint correlations.",
            "No simultaneous sharp physical position and momentum claim is made.",
            "No ordinary transport, Link delay, environment spreading or classical limit is tested.",
            "Quantum queries retain the explicit Q-ORACLE-1 assumption; host work is not O(1).",
        ],
    }

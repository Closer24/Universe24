"""Exact quantum-state contract for the native reversible selection gate.

This is an independent rational-amplitude comparator, not an Engine runtime,
wavefunction hidden inside a seed, or a probability sampler. It uses the same
finite collision truth table as the constructive native selector and makes
the extra Hilbert-space assumptions explicit.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path


def identity(size):
    return tuple(tuple(F(i == j) for j in range(size)) for i in range(size))


def transpose(matrix):
    return tuple(zip(*matrix))


def matmul(left, right):
    return tuple(tuple(sum(a*b for a, b in zip(row, column))
                       for column in zip(*right)) for row in left)


def apply(matrix, vector):
    return tuple(sum(a*b for a, b in zip(row, vector)) for row in matrix)


def norm(vector):
    return sum(value*value for value in vector)


def permutation_matrix(permutation):
    if sorted(permutation) != list(range(len(permutation))):
        raise ValueError("a quantum permutation lift requires a bijective table")
    return tuple(tuple(F(permutation[j] == i) for j in range(len(permutation)))
                 for i in range(len(permutation)))


def tensor_product(left, right):
    return tuple(a*b for a in left for b in right)


def kron(left, right):
    return tuple(tuple(left[i][j] * right[k][ell]
                       for j in range(len(left[0])) for ell in range(len(right[0])))
                 for i in range(len(left)) for k in range(len(right)))


def bits_index(bits):
    value = 0
    for bit in bits:
        if type(bit) is not int or bit not in (0, 1):
            raise ValueError("truth-table outputs must be exact bits")
        value = 2*value + bit
    return value


def integral_norm_audit():
    # The theorem applies to all integer dimensions: every unit column has
    # a sum of integer squares equal to one. Enumeration is a finite control.
    real = []
    for values in product((-1, 0, 1), repeat=4):
        matrix = (values[:2], values[2:])
        if matmul(transpose(matrix), matrix) == identity(2):
            assert all(sum(value != 0 for value in row) == 1 for row in matrix)
            real.append(matrix)
    gaussian = 0
    for values in product((-1, 0, 1), repeat=8):
        # Column entries are (a+ib,c+id) and (e+if,g+ih).
        a, b, c, d, e, f, g, h = values
        if (a*a+b*b+c*c+d*d == 1 and e*e+f*f+g*g+h*h == 1
                and a*e+b*f+c*g+d*h == 0
                and a*f-b*e+c*h-d*g == 0):
            gaussian += 1
    assert len(real) == 8 and gaussian == 32
    return {"integer_2x2_cases": 81, "integer_unitaries": len(real),
            "gaussian_integer_2x2_cases": 6561,
            "gaussian_integer_unitaries": gaussian,
            "classification": "signed permutations / permutations with phases +/-1,+/-i",
            "scope": "linear maps on ordinary orthonormal amplitude coordinates preserving norm for EVERY input; not a no-go for nonorthogonal metrics, constrained encodings or rational amplitudes"}


def rational_coin_audit():
    coin = ((F(3, 5), F(4, 5)), (F(-4, 5), F(3, 5)))
    inverse = transpose(coin)
    assert matmul(inverse, coin) == identity(2)
    checks = 0
    for x, y in product(range(-6, 7), repeat=2):
        vector = (F(x), F(y))
        assert norm(apply(coin, vector)) == norm(vector)
        assert apply(inverse, apply(coin, vector)) == vector
        checks += 1
    input_state = (F(1), F(0))
    split = apply(coin, input_state)
    recombined = apply(inverse, split)
    phase_flipped = apply(inverse, (split[0], -split[1]))
    assert split == (F(3, 5), F(-4, 5))
    assert recombined == input_state
    assert phase_flipped == (F(-7, 25), F(24, 25))
    # Substituting integer numerators without carrying the scale is not unitary.
    unscaled = ((3, 4), (-4, 3))
    assert norm(apply(unscaled, input_state)) == 25
    return {"scope": "externally specified exact rational amplitude reference; never fed to Engine",
            "unitary_norm_inverse_cases": checks,
            "coin": coin, "input": input_state, "split": split,
            "coherent_recombination": recombined,
            "phase_flipped_recombination": phase_flipped,
            "phase_flipped_squared_amplitudes": tuple(v*v for v in phase_flipped),
            "unscaled_integer_numerator_norm": 25,
            "observed_frequency_or_sampling": False}


def classical_quantum_locality_audit():
    # A two-cell face CNOT leaves the classical control bit unchanged, but its
    # quantum control X observable depends on the target. Both remain on edge.
    cnot = permutation_matrix((0, 1, 3, 2))
    unit = identity(2)
    x = ((F(0), F(1)), (F(1), F(0)))
    z = ((F(1), F(0)), (F(0), F(-1)))
    conjugate = lambda operator: matmul(matmul(transpose(cnot), operator), cnot)
    assert conjugate(kron(x, unit)) == kron(x, x)
    assert conjugate(kron(unit, z)) == kron(z, z)
    assert conjugate(kron(z, unit)) == kron(z, unit)
    return {"classical_control_unchanged": True,
            "heisenberg_X_control": "X_control * X_target",
            "heisenberg_Z_target": "Z_control * Z_target",
            "heisenberg_Z_control": "Z_control",
            "quantum_observable_support": "the declared single face",
            "scope": "finite two-cell reference; not a proof of the quantum neighborhood of the full Rule3 polynomial"}


def selector_lift_audit(table):
    permutation = tuple(bits_index(bits) for bits in table)
    assert len(permutation) == 8
    unitary = permutation_matrix(permutation)
    assert matmul(transpose(unitary), unitary) == identity(8)
    assert matmul(matmul(unitary, unitary), unitary) == identity(8)
    basis_checks = 0
    for column in transpose(identity(8)):
        after = apply(unitary, column)
        assert sum(value != 0 for value in after) == 1
        assert apply(transpose(unitary), after) == column
        basis_checks += 1
    # Table indexing is (m,x,y). The seed is a product, with ready memory m=0,
    # a declared superposition at x, and y=1. These are extra quantum inputs.
    state = tensor_product(tensor_product((F(1), F(0)), (F(3, 5), F(4, 5))),
                           (F(0), F(1)))
    expected = tuple(F(4, 5) if i == 3 else F(3, 5) if i == 6 else F(0)
                     for i in range(8))
    after = apply(unitary, state)
    assert after == expected and norm(after) == 1
    assert apply(transpose(unitary), after) == state
    # Exact reduced density matrix on provenance m, tracing carrier bits xy.
    reduced = tuple(tuple(sum(after[4*m+xy]*after[4*n+xy] for xy in range(4))
                          for n in range(2)) for m in range(2))
    purity = sum(value*value for row in reduced for value in row)
    assert reduced == ((F(16, 25), F(0)), (F(0), F(9, 25)))
    assert purity == F(337, 625) < 1
    coherence = 2*after[3]*after[6]
    assert coherence == F(24, 25)
    # A diagonal classical ensemble with the same weights has zero coherence.
    return {"collision_table_mxy": table, "permutation": permutation,
            "exact_orthonormal_columns": 8, "basis_inputs_stay_basis": basis_checks,
            "collision_period": 3, "quantum_product_input": state,
            "quantum_output": after, "provenance_reduced_density": reduced,
            "provenance_purity": purity,
            "joint_coherence_011_110": coherence,
            "same_diagonal_classical_mixture_coherence": 0,
            "exact_inverse": True,
            "superposition_and_tensor_product_preparation_assumed": True,
            "probability_sampler_used": False,
            "interpretation": "The actual reversible collision admits an entangling Hilbert permutation lift on an added coherent preparation. A single ontic Engine run supplies neither that preparation nor a derived measurement measure."}


def _json(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: _json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json(item) for item in value]
    return value


def audit():
    from validation.selection.complexity import SORT_GATE
    # Reversibility of a Boolean truth table is different from interpreting
    # its multilinear polynomial as a linear operator on amplitudes.
    xor = lambda x, y: x+y-2*x*y
    assert xor(1, 1) != xor(1, 0)+xor(0, 1)
    return {"schema": "universe24/selection/qca-contract/1",
            "integral_norm": integral_norm_audit(),
            "rational_coin": rational_coin_audit(),
            "quantum_locality": classical_quantum_locality_audit(),
            "native_selector_quantum_lift": selector_lift_audit(SORT_GATE),
            "nonlinear_polynomial_is_not_amplitude_linear": {
                "xor_at_sum": xor(1, 1), "sum_of_xor_values": xor(1, 0)+xor(0, 1)},
            "gates": {"finite_selector_hilbert_lift": "passed_as_reference",
                      "rational_amplitude_norm_and_interference": "passed_as_reference",
                      "quantum_preparation_from_Engine": "not_supplied",
                      "quantum_instrument_from_Engine": "not_supplied",
                      "Born_outcome_measure_from_Engine": "not_derived",
                      "whole_lattice_quantum_causality": "not_tested",
                      "Einstein_apparatus_integration": "not_tested"},
            "references": [
                {"url": "https://arxiv.org/pdf/quant-ph/0405174", "sections": "II, III B, Lemma 4"},
                {"url": "https://arxiv.org/pdf/0711.3975", "sections": "Definitions 3-5, Theorem 1"}],
            "source_sha256": {
                "validation/selection/qca.py": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "validation/selection/complexity.py": hashlib.sha256(Path(__file__).with_name("complexity.py").read_bytes()).hexdigest()},
            "scope": "Small exact Hilbert comparator on the native collision truth table; not another runtime, quantum seed representation, Born sampler, or claimed QCA derivation."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/selection/qca"))
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    result = _json(audit())
    (args.out / "qca.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"gates": result["gates"],
                      "selector_provenance_purity": result["native_selector_quantum_lift"]["provenance_purity"]}))


if __name__ == "__main__":
    main()

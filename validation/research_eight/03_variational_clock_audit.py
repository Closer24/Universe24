"""Restricted exact controls for the variational/local-clock literature review.

This source-only audit does not construct Einstein gravity or physical apparatus.
Run from the repository root: python validation/research_eight/03_variational_clock_audit.py
"""
from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import numpy as np
from universe24.core import Engine, State, Tensor


def free_parametrized_control():
    """C=2*P_T+v^2=0, v=q[n]-q[n-1], T[n]-T[n-1]=1.

    The invariant follows directly from x_next=2*x-x_old. P_T is constant
    by compatible initial memory. This is a free mechanical sector only.
    """
    names = ("q", "coordinate_time", "clock_momentum")
    tensor = Tensor(
        [{"name": name, "label": "audit"} for name in names],
        [(name, 6, [(name, (0, 0, 0), "b")]) for name in names],
        strict_support=True,
    )
    engine = Engine(tensor)
    L, steps = 3, 128
    q0 = np.arange(L ** 3, dtype=np.int64) - 13
    v = np.array([2 * ((i % 5) - 2) for i in range(L ** 3)], dtype=np.int64)
    energy_momentum = -(v * v) // 2
    b = np.array([q0, np.zeros(L ** 3, dtype=np.int64), energy_momentum])
    a = np.array([q0 - v, -np.ones(L ** 3, dtype=np.int64), energy_momentum])
    max_bits = 0
    for remainder in range(6):
        seed = State(L, a.copy(), b.copy(), np.full_like(b, remainder))
        state = seed
        for tick in range(1, steps + 1):
            previous = state
            state = engine.step(state)
            # Independent closed-form oracle, never calls the production step.
            assert np.array_equal(state.b[0], q0 + tick * v)
            assert np.all(state.b[1] == tick)
            assert np.array_equal(state.b[2], energy_momentum)
            assert np.all(state.r == remainder)
            assert np.all(2 * state.b[2] + (state.b[0] - state.a[0]) ** 2 == 0)
            assert engine.inverse_step(state).same_as(previous)
            max_bits = max(max_bits, *(abs(int(x)).bit_length() for x in state.b.flat))
        assert engine.rewind(state, steps).same_as(seed)
    # A missing constraint is not repaired by reversibility or a clock.
    wrong_b, wrong_a = b.copy(), a.copy()
    wrong_b[2] += 1
    wrong_a[2] += 1
    wrong = engine.run(State(L, wrong_a, wrong_b, np.zeros_like(b)), steps)
    wrong_defect = 2 * wrong.b[2] + (wrong.b[0] - wrong.a[0]) ** 2
    assert np.all(wrong_defect == 2)
    return {
        "status": "passed_restricted_control",
        "channels": tensor.G, "retained_integer_entries_per_node": 3 * tensor.G,
        "monomials": len(tensor.monomials), "degree": 1,
        "nodes": L ** 3, "steps_each": steps, "remainder_classes": 6,
        "max_integer_bits": max_bits, "full_rewind": True,
        "constraint_residual": 0, "incompatible_seed_residual": 2,
        "meaning": "Exact free mechanical constraint and coordinate counter, not GR/proper-clock apparatus",
    }


def nonlinear_pseudoconstraint_control():
    """Direct variation of L=p*(Q-q)-N*((p*p+q*q)/2-E).

    Equations: P=p+N*q, Q=q+N*p, (q*q+p*p)/2-E=0.
    """
    q, p, lapse, energy = F(1), F(2), F(1, 4), F(5, 2)
    canonical_in = p + lapse * q
    q_out = q + lapse * p
    pseudo = (q * q + p * p) / 2 - energy
    same_time = (q_out * q_out + p * p) / 2 - energy
    assert pseudo == 0 and same_time == F(5, 8)
    branches = []
    # Start on the ordinary constraint: q=1, P=2, E=5/2.
    for p_out in (F(2), F(-2)):
        n = (F(2) - p_out) / q
        q_next = q + n * p_out
        defect = (q_next * q_next + p_out * p_out) / 2 - energy
        branches.append({"P_out": str(p_out), "lapse": str(n),
                         "q_out": str(q_next), "same_time_defect": str(defect)})
    assert [row["same_time_defect"] for row in branches] == ["0", "24"]
    # Rational q=1,P=1,E=3/2 require p_out**2=2; no rational ratio p_out exists.
    discriminant = 8
    assert math.isqrt(discriminant) ** 2 != discriminant
    return {
        "status": "passed_negative_control",
        "prepared_P_in": str(canonical_in), "mixed_time_defect": str(pseudo),
        "same_time_defect": str(same_time), "constrained_input_branches": branches,
        "rational_input_irrational_output_polynomial": "P_out^2-2=0",
        "root_discriminant": discriminant,
        "scope": "Obstruction to this direct rational implicit-action import, not a no-go for integer encodings",
    }


def main():
    paths = [Path(__file__), ROOT / "universe24/core/engine.py", ROOT / "universe24/core/tensor.py"]
    report = {
        "schema": "universe24/research-eight/variational-clock-audit/1",
        "free_control": free_parametrized_control(),
        "implicit_action_control": nonlinear_pseudoconstraint_control(),
        "physical_acceptance": "not_tested",
        "sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
    }
    target = ROOT / "runs/research_eight/03_variational_clock_audit.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

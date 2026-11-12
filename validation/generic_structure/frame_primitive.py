"""Prepared integer frame shears; source-only, not gravitational dynamics.

Run: python -m validation.generic_structure.frame_primitive
Every actual update is the unchanged Engine. The matrix is an independent
physical-map oracle and seed construction, never a runtime callback.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO

ROOT = Path(__file__).resolve().parents[2]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def build():
    names = tuple(f"B{i}{j}" for i in range(3) for j in range(3))+("s", "t")
    terms = [(name, 6, ((name, ZERO, "b"),)) for name in names]
    for i in range(2):
        for j in range(3):
            terms.append((f"B{i}{j}", 3,
                          (("s", ZERO, "b"), ("t", ZERO, "b"), (f"B{i}{j}", ZERO, "b"))))
    return Tensor([GearType(name, label="audit") for name in names], terms, strict_support=True)


def matrices(s, t):
    forward = sp.Matrix([[1+s*t, s, 0], [t, 1, 0], [0, 0, 1]])
    inverse = sp.Matrix([[1, -s, 0], [-t, 1+s*t, 0], [0, 0, 1]])
    return forward, inverse


def symbolic():
    s, t = sp.symbols("s t", integer=True)
    matrix, inverse = matrices(s, t)
    require(matrix*inverse == sp.eye(3) and inverse*matrix == sp.eye(3), "inverse identity")
    require(matrix.det() == 1, "unit determinant")
    require(matrix+inverse == sp.diag(2+s*t, 2+s*t, 2), "cubic Rule3 identity")
    entries = sp.symbols("b0:9")
    frame = sp.Matrix(3, 3, entries)
    require(sp.expand((matrix*frame).det()-frame.det()) == 0, "arbitrary-frame determinant")
    # The prepared complete-state relation advances, not merely its b readout.
    a = inverse*frame
    ell = (matrix+inverse)*frame
    after = ell-a
    require(sp.simplify(after-matrix*frame) == sp.zeros(3), "forward embedding")
    require(sp.simplify(inverse*after-frame) == sp.zeros(3), "next old-slice embedding")
    return {"determinant_identity": "det(M B)=det(B)",
            "matrix": [[str(v) for v in row] for row in matrix.tolist()],
            "inverse": [[str(v) for v in row] for row in inverse.tolist()],
            "all_finite_ticks": "B_n=M^n B_0, a_n=M^-1 B_n, r_n=r_0",
            "scope": "arbitrary nonsingular initial integer frame; frozen nodewise s,t; prepared old slice"}


def scalar_step(before):
    a, b, r = (np.zeros(before.b.shape, dtype=object) for _ in range(3))
    for node in range(before.N):
        shear_product = int(before.b[9, node])*int(before.b[10, node])
        for gear in range(before.G):
            value = int(before.b[gear, node])
            u = (6+3*shear_product)*value if gear < 6 else 6*value
            quotient, remainder = divmod(2*u+int(before.r[gear, node]), 6)
            a[gear, node], b[gear, node], r[gear, node] = value, quotient-int(before.a[gear, node]), remainder
    return State(before.L, a, b, r)


def prepare():
    a, b, r = (np.zeros((11, 27), dtype=object) for _ in range(3))
    for node in range(27):
        s, t = node % 5-2, (node//5) % 5-2
        # Nonorthogonal, invertible frames with determinant 6 and varied entries.
        left = sp.Matrix([[1, node % 3-1, 0], [0, 1, 0], [node % 2, 0, 1]])
        right = sp.Matrix([[1, 0, 0], [0, 1, node % 4-1], [0, 0, 1]])
        frame = left*sp.diag(1, 2, 3)*right
        _, inverse = matrices(s, t)
        b[:9, node] = [int(v) for v in frame]
        a[:9, node] = [int(v) for v in inverse*frame]
        a[9:, node] = b[9:, node] = [s, t]
        r[:, node] = [(gear+node) % 6 for gear in range(11)]
    return State(3, a, b, r)


def actual(steps=12):
    law, seed = build(), prepare()
    engine, state = Engine(law), seed.copy()
    trace, bit_sizes = [state.to_dict()], []
    for tick in range(1, steps+1):
        expected = scalar_step(state)
        after = engine.step(state)
        require(after.same_as(expected), "independent scalar-step mismatch")
        require(engine.inverse_step(after).same_as(state), "full inverse mismatch")
        require(np.array_equal(after.r, seed.r), "frozen carry mismatch")
        for node in range(state.N):
            matrix, inverse = matrices(int(seed.b[9, node]), int(seed.b[10, node]))
            initial_frame = sp.Matrix(3, 3, list(seed.b[:9, node]))
            frame = sp.Matrix(3, 3, list(after.b[:9, node]))
            require(frame == matrix**tick*initial_frame, "matrix-power oracle mismatch")
            require(sp.Matrix(3, 3, list(after.a[:9, node])) == inverse*frame, "embedding left invariant sector")
            require(frame.det() == 6, "frame determinant changed")
            # Exact Sylvester criteria for the inverse spatial metric B.T*B.
            gram = frame.T*frame
            require(all(gram[:k, :k].det() > 0 for k in (1, 2, 3)), "positive Gram domain failed")
        state = after
        trace.append(state.to_dict())
        bit_sizes.append(max(abs(int(v)).bit_length() for array in (state.a, state.b, state.r) for v in array.flat))
    require(engine.rewind(state, steps).same_as(seed), "complete rewind mismatch")
    return {"status": "passed", "channels": law.G, "retained_integers_per_node": 3*law.G,
            "degree": law.rank-1, "terms": len(law), "strict_single_face_support": not law.support_violations(),
            "support_scope": "onsite only; no inter-node transport claim", "tensor_fingerprint": law.fingerprint,
            "steps": steps, "nodes": seed.N, "all_six_carries": True,
            "scalar_oracle_comparisons": 3*law.G*seed.N*steps,
            "complete_step_inverse_and_rewind": True, "matrix_power_and_embedding": True,
            "positive_Gram_all_steps": True, "determinant": 6,
            "maximum_integer_bits_by_step": bit_sizes,
            "tensor": law.to_dict(), "seed": seed.to_dict(), "complete_trace": trace}


def negatives():
    law = build()
    b = np.zeros((11, 27), dtype=object)
    for node in range(27):
        b[:9, node] = [int(v) for v in sp.eye(3)]
        b[9:, node] = [1, 1]
    a = b.copy()
    for node in range(27):
        a[:9, node] = [int(v) for v in sp.diag(3, 3, 2)]
    seed = State(3, a, b, np.zeros_like(b))
    after = Engine(law).step(seed)
    require(sp.Matrix(3, 3, list(seed.b[:9, 0])).det() == 1, "negative control not initially invertible")
    require(sp.Matrix(3, 3, list(after.b[:9, 0])).det() == 0, "unprepared-history failure missing")
    require(Engine(law).inverse_step(after).same_as(seed), "singular readout still must fully rewind")
    # Every product of these shears has determinant 1; dilation has determinant 8.
    require((2*sp.eye(3)).det() == 8, "dilation control")
    matrix, _ = matrices(1, 1)
    metric = (matrix**12).T*(matrix**12)
    require(metric.det() == 1 and max(abs(v) for v in metric) > 10**9, "conditioning counterexample missing")
    return {"unprepared_old_slice_invertible_to_singular": {"status": "expected_failure_reproduced", "det_before": 1, "det_after": 0,
                                                           "complete_inverse": True},
            "isotropic_expansion_from_shears_alone": {"status": "failed", "shear_product_det": 1, "dilation_2I_det": 8},
            "uniform_metric_conditioning_from_det1": {"status": "failed", "at_tick": 12,
                                                       "metric_det": 1, "maximum_Gram_entry": str(max(abs(v) for v in metric)),
                                                       "exact_condition_number": "((3+sqrt(5))/2)^(4*n) for s=t=1, B0=I"},
            "dynamical_connection_or_source_coupling": "not_implemented",
            "Einstein_constraints_and_convergence": "not_tested",
            "Lorentz_gauge_transformation": False,
            "volume_scope": "For inverse spatial frame B, sqrt(det(gamma))=1/abs(det(B)); fixed here."}


def main():
    result = {"schema": "universe24/generic-structure/frame-primitive/1",
              "base_commit": "8c53e69f4b466dcbd2da7dab7e3c365bd9731766",
              "scope": "prepared frame-domain primitive only; no accepted physical model",
              "symbolic": symbolic(), "actual_Engine": actual(), "negative_controls": negatives(),
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out = ROOT/"runs/generic-structure/frame_primitive.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"output": str(out), "status": result["actual_Engine"]["status"],
                      "channels": result["actual_Engine"]["channels"],
                      "scalar_comparisons": result["actual_Engine"]["scalar_oracle_comparisons"],
                      "bits": result["actual_Engine"]["maximum_integer_bits_by_step"],
                      "physical_acceptance": "not_established"}, indent=2))


if __name__ == "__main__":
    main()

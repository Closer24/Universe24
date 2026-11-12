"""Bounded reversible comparison control, not a physical complexity selector.

Run: python -m validation.synthesis.complexity_selection --out runs/synthesis/selection.json
No production law is changed. The four-channel control consumes all remaining
44+4 capacity if appended, but is deliberately NOT appended to geometry.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

from universe24.core import Engine, State, Tensor
from universe24.core.tensor import GearType


NAMES = ("score_left", "score_right", "prefer_left", "preferred_score")


def tensor():
    x = ("score_left", (0, 0, 0), "b")
    y = ("score_right", (1, 0, 0), "b")
    return Tensor([GearType(n, label="audit") for n in NAMES], [
        ("score_left", 6, [x]),
        ("score_right", 6, [("score_right", (0, 0, 0), "b")]),
        ("prefer_left", 3, [x]),
        ("prefer_left", -3, [x, y]),
        ("preferred_score", 3, [x]),
        ("preferred_score", 3, [y]),
        ("preferred_score", -3, [x, y]),
    ], strict_support=True)


def scalar_step(s):
    """Independent explicit equations, no Engine or tensor evaluator."""
    a, b, r = [], [], []
    for g in range(4):
        ar, br, rr = [], [], []
        for n in range(s.N):
            i, j, k = n // s.L**2, n // s.L % s.L, n % s.L
            neighbor = (((i + 1) % s.L) * s.L + j) * s.L + k
            x, y = int(s.b[0, n]), int(s.b[1, neighbor])
            forcing = (2*x, 2*int(s.b[1, n]), x*(1-y), x+y-x*y)[g]
            ell, carry = divmod(6*forcing + int(s.r[g, n]), 6)
            ar.append(int(s.b[g, n]))
            br.append(ell-int(s.a[g, n]))
            rr.append(carry)
        a.append(ar); b.append(br); r.append(rr)
    return State(s.L, a, b, r)


def state(x, y, c=0, w=0, carries=(0, 0, 0, 0), L=3):
    rows = [[v] * L**3 for v in (x, y, c, w)]
    return State(L, rows, rows, [[r] * L**3 for r in carries])


def check(engine, s):
    actual = engine.step(s)
    assert actual.same_as(scalar_step(s))
    assert engine.inverse_step(actual).same_as(s)
    assert (actual.r == s.r).all()
    return actual


def audit():
    law = tensor()
    engine = Engine(law)
    boolean_cases = 0
    outputs = []
    for x, y in itertools.product(range(2), repeat=2):
        for carries in itertools.product(range(6), repeat=4):
            s = state(x, y, carries=carries)
            out = check(engine, s)
            assert int(out.b[2, 0]) == int(x > y)
            assert int(out.b[3, 0]) == max(x, y)
            assert int(out.b[0, 0]) == x and int(out.b[1, 0]) == y
            boolean_cases += 1
        outputs.append({"x": x, "y": y, "prefer_left": int(x > y), "preferred_score": max(x, y)})

    signed_cases = 0
    # All five signed values for all four channel memories; every carry value.
    for values in itertools.product(range(-2, 3), repeat=4):
        for carry in range(6):
            s = state(*values, carries=(carry,)*4)
            check(engine, s)
            signed_cases += 1
    huge = (-(1 << 257), 1 << 193, -(1 << 131), 1 << 89)
    huge_cases = 0
    huge_output_max_bits = 0
    for carry in range(6):
        output = check(engine, state(*huge, carries=(carry,)*4))
        huge_output_max_bits = max(huge_output_max_bits, int(output.max_abs()).bit_length())
        huge_cases += 1

    unprepared_cases = 0
    for carry in range(6):
        arbitrary = state(-2, 1, 2, -1, carries=(carry,)*4)
        for g in range(4):
            for n in range(27):
                arbitrary.a[g, n] = (n + 3*g) % 11 - 5
                arbitrary.b[g, n] = (2*n + g) % 13 - 6
        check(engine, arbitrary)
        unprepared_cases += 1

    seed = state(1, 0, carries=(1, 2, 3, 4))
    current = seed
    cycle = []
    for step in range(1, 9):
        current = check(engine, current)
        cycle.append({"step": step, "a": int(current.a[3, 0]), "b": int(current.b[3, 0])})
        if step % 4 == 0:
            assert current.same_as(seed)

    # Actual three-dimensional face/seam support and complete scalar agreement.
    spatial = state(1, 0, L=3, carries=(1, 2, 3, 4))
    spatial.b[1, 0] = spatial.a[1, 0] = 1
    actual = check(engine, spatial)
    changed_nodes = [n for n in range(27) if int(actual.b[2, n]) == 0]
    assert changed_nodes == [18]  # x=2 samples x=0 over the periodic +x seam.

    outside = check(engine, state(2, 1))
    memory = check(engine, state(1, 0, c=2, w=2))
    assert int(outside.b[2, 0]) == 0 and int(outside.b[3, 0]) == 1
    assert int(memory.b[2, 0]) == -1 and int(memory.b[3, 0]) == -1
    return {
        "schema": "universe24/bounded-selection-control/1",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "reviewed_base": "621fc1f55800e50e1db5f6a30ce24bb83716a49a",
        "channels": 4, "retained_integers_per_node": 12,
        "degree": max(len(m.factors) for m in law.monomials),
        "strict_single_edge_support": True, "old_a_reads": 0,
        "boolean_all_independent_carry_cases": boolean_cases,
        "signed_uniform_carry_cases": signed_cases,
        "huge_integer_cases": huge_cases,
        "huge_case_input_max_bits": max(abs(v).bit_length() for v in huge),
        "huge_case_output_max_bits": huge_output_max_bits,
        "unprepared_inhomogeneous_cases": unprepared_cases,
        "complete_scalar_and_inverse_checks": boolean_cases + signed_cases + huge_cases + unprepared_cases + 11,
        "boolean_truth_table": outputs,
        "preferred_score_period_four": cycle,
        "periodic_seam_receiver_nodes": changed_nodes,
        "out_of_domain_counterexample": {"x": 2, "y": 1, "prefer_left": 0, "preferred_score": 1},
        "nonzero_history_counterexample": {"x": 1, "y": 0, "older_response": 2, "new_response": -1},
        "mechanical_status": "passed",
        "command": "python -m validation.synthesis.complexity_selection --out runs/synthesis/complexity_selection.json",
        "bounded_prepared_first_step_comparison": "passed",
        "repeated_monotone_selection": "failed: explicit four-cycle",
        "geometry_apparatus_integration": "not_tested: no slots reserved or shared metric coupling",
        "structural_complexity_growth": "not_tested: Boolean inputs are supplied, not structural scores",
        "limitations": [
            "This is a source-only four-channel analytic control, not the 44-channel physical model.",
            "Inputs are prepared Boolean bits with a=b; arbitrary changed inputs leave this invariant family.",
            "Output is a reversible response with retained history, not overwrite/max at each update.",
            "No branch or original input is discarded; no computational scheduler/reset is added.",
            "One-step polynomial threshold obstruction does not rule out multi-step reversible computation.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

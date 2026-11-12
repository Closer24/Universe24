"""Generic Rule3 identities and counterexamples; no physical acceptance claim.

Run: python -m validation.einstein_node_audit.node_algebra
The scalar oracle evaluates the tensor with explicit coordinates and Python
integers, independently of Engine's vectorized plan and lattice gather arrays.
"""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

import numpy as np

from universe24.core import Engine, State, Tensor, check_reciprocity


ROOT = Path(__file__).resolve().parents[2]
ZERO = (0, 0, 0)


def input_scalar(tensor, state, g, node):
    L = state.L
    x, yz = divmod(node, L * L)
    y, z = divmod(yz, L)
    total = 0
    for monomial in tensor.monomials:
        if monomial.target != g:
            continue
        value = monomial.coeff
        for factor in monomial.factors:
            dx, dy, dz = factor.offset
            target = (((x + dx) % L) * L + (y + dy) % L) * L + (z + dz) % L
            value *= int(getattr(state, factor.field)[factor.gear, target])
        total += value
    return total


def scalar_step(tensor, state):
    a, b, r = (np.empty_like(state.a, dtype=object) for _ in range(3))
    for g in range(state.G):
        for node in range(state.N):
            aa, bb, rr = state.gear(g, node)
            u = input_scalar(tensor, state, g, node)
            quotient, remainder = divmod(2 * u + rr, 6)
            a[g, node], b[g, node], r[g, node] = bb, quotient - aa, remainder
    return State(state.L, a, b, r)


def specimen_tensor():
    # Includes constants, negative coefficients, a cubic, face neighbors and
    # a two-level acyclic old-a dependency. Every monomial uses one face only.
    return Tensor(["q0", "q1", "q2"], [
        ("q0", 3, ()),
        ("q0", 2, (("q0", ZERO, "b"),)),
        ("q0", 1, (("q1", (1, 0, 0), "b"),) * 2),
        ("q1", 6, (("q1", ZERO, "b"),)),
        ("q1", 1, (("q0", ZERO, "a"), ("q2", (0, 1, 0), "b"))),
        ("q1", -1, (("q1", ZERO, "b"), ("q0", (0, 0, 1), "b"),
                     ("q2", (0, 0, 1), "b"))),
        ("q2", -3, (("q2", ZERO, "b"),)),
        ("q2", 1, (("q1", (-1, 0, 0), "a"),)),
        ("q2", 1, (("q0", ZERO, "b"),) * 3),
    ], strict_support=True)


def paired_parities_and_native_map():
    tensor = specimen_tensor()
    engine = Engine(tensor)
    reciprocal = check_reciprocity(tensor)
    assert not reciprocal.ok
    rng = random.Random(2026111203)
    seeds, steps, checked, events, max_bits = 6, 5, 0, 0, 0
    scalar_hash = hashlib.sha256()
    for trial in range(seeds):
        a = np.array([[rng.randrange(-4, 5) for _ in range(27)] for _ in range(3)], dtype=object)
        b = np.array([[rng.randrange(-4, 5) for _ in range(27)] for _ in range(3)], dtype=object)
        if trial == seeds - 1:
            a[0, 0], b[1, 1] = -(1 << 100), (1 << 101) + 3
        r = np.array([[(g * 27 + n + trial) % 6 for n in range(27)] for g in range(3)], dtype=object)
        seed = State(3, a, b, r)
        paired_seed = State(3, a, b, r + 1 - 2 * (r % 2))
        state, paired = seed, paired_seed
        cumulative_defect = np.zeros_like(r, dtype=object)
        for tick in range(1, steps + 1):
            old, paired_old = state, paired
            state, paired = engine.step(old), engine.step(paired_old)
            scalar = scalar_step(tensor, old)
            assert state.same_as(scalar)
            assert np.array_equal(state.a, paired.a)
            assert np.array_equal(state.b, paired.b)
            assert np.array_equal(state.r // 2, paired.r // 2)
            assert np.all(state.r != paired.r)
            assert np.array_equal(state.r % 2, seed.r % 2)
            clicks, paired_clicks = engine.clicks(old, state, tick), engine.clicks(paired_old, paired, tick)
            assert clicks.rows() == paired_clicks.rows()
            events += len(clicks)
            for g in range(state.G):
                for node in range(state.N):
                    aa, q, rr = old.gear(g, node)
                    an, qn, rn = state.gear(g, node)
                    u = input_scalar(tensor, old, g, node)
                    p, pn = 6 * (q - aa) + rr, 6 * (qn - an) + rn
                    assert (q - p // 6, q, p % 6) == (aa, q, rr)
                    assert pn == p + 2 * (u - 6 * q)
                    assert qn == q + pn // 6
                    s, epsilon = divmod(rr, 2)
                    carry, sn = divmod(u + s, 3)
                    assert (an, qn, rn) == (q, carry - aa, 2 * sn + epsilon)
                    assert (rn - rr) % 6 in (0, 2, 4)
                    # Six times the acceleration defect is the exact bounded
                    # remainder coboundary; no independent rounding noise.
                    defect = 6 * (qn - 2 * q + aa) - 2 * (u - 6 * q)
                    assert defect == rr - rn
                    cumulative_defect[g, node] += defect
                    assert cumulative_defect[g, node] == int(seed.r[g, node]) - rn
                    assert abs(int(cumulative_defect[g, node])) <= 4
                    checked += 1
            assert engine.inverse_step(state).same_as(old)
            assert engine.inverse_step(paired).same_as(paired_old)
            max_bits = max(max_bits, *(abs(int(x)).bit_length()
                                      for arr in (state.a, state.b, state.r) for x in arr.flat))
            scalar_hash.update(repr(state.to_dict()).encode())
        assert engine.rewind(state, steps).same_as(seed)
        assert engine.rewind(paired, steps).same_as(paired_seed)
    return {"status": "passed", "channels": tensor.G, "nodes": 27,
            "seeds": seeds, "steps_each": steps, "checked_triples": checked,
            "paired_click_rows": events, "max_retained_bits": max_bits,
            "staged_old_a_layers": [list(x) for x in tensor.stages],
            "reciprocal_gradient_is_automatic": False,
            "missing_gradient_partners": len(reciprocal.missing_partners),
            "all_six_initial_remainders": True,
            "independent_scalar_state_sha256": scalar_hash.hexdigest(),
            "tensor": tensor.to_dict(),
            "claims": ["native_qp_identity", "inactive_remainder_parity",
                       "identical_ab_and_clicks_under_parity_flip",
                       "bounded_summed_acceleration_carry", "complete_inverse"]}


def scalar_law(coefficient, constant=0):
    terms = [("q", coefficient, (("q", ZERO, "b"),))] if coefficient else []
    if constant:
        terms.append(("q", constant, ()))
    return Tensor(["q"], terms, strict_support=True)


def counterexamples():
    result = {}
    # The same primitive admits rotations, inertia and acceleration, so none
    # of these behaviours (or a physical proper clock) follows from Rule3 alone.
    for name, coefficient, constant in (("period_four", 0, 0),
                                        ("inertial", 6, 0),
                                        ("accelerated", 6, 3),
                                        ("exponential", 9, 0)):
        tensor = scalar_law(coefficient, constant)
        engine = Engine(tensor)
        seed = State(3, [[0] * 27], [[1] * 27], [[5] * 27])
        state, rows, click_counts = seed, [seed.gear(0, 0)], []
        for tick in range(1, 13):
            old = state
            state = engine.step(old)
            rows.append(state.gear(0, 0))
            click_counts.append(len(engine.clicks(old, state, tick)))
            assert state.same_as(scalar_step(tensor, old))
            if name == "period_four" and tick % 4 == 0:
                assert state.same_as(seed)
            if name == "inertial":
                assert state.gear(0, 0)[1] == tick + 1
            if name == "accelerated":
                assert state.gear(0, 0)[1] == 1 + tick + tick * (tick + 1) // 2
        assert engine.rewind(state, 12).same_as(seed)
        if name == "period_four":
            assert not any(click_counts)
        norms = [a * a + b * b for a, b, _ in rows]
        result[name] = {"tensor_u": f"{coefficient}*b+{constant}",
                        "complete_triples": rows,
                        "a_squared_plus_b_squared": norms,
                        "official_click_count_by_step_on_27_nodes": click_counts,
                        "complete_rewind": True}
    assert result["exponential"]["a_squared_plus_b_squared"][-1] > 1
    # A local periodic orbit cannot support a state function strictly improving
    # each step. This is a control against a universal load-minimization claim,
    # not a theorem ruling out monotone variables on unbounded special orbits.
    result["universal_strict_load_descent"] = "failed_by_nontrivial_period_four_control"
    result["universal_euclidean_norm_energy"] = "failed_by_inertial_and_exponential_controls"
    result["geodesic_and_proper_clock_identification"] = "not_tested"
    return result


def main():
    tracked_sources = [Path(__file__), ROOT / "universe24/core/engine.py",
                       ROOT / "universe24/core/tensor.py"]
    result = {
        "schema": "universe24/einstein-node/node-algebra/1",
        "baseline_commit": "4c494c1188f70eb8a677bf59765cc6e8571c6b88",
        "source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in tracked_sources},
        "generic_identities": paired_parities_and_native_map(),
        "negative_controls": counterexamples(),
        "runtime_changed": False, "einstein_acceptance": "not_established",
    }
    output = ROOT / "runs/einstein_node/node_algebra.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)),
                      "triples": result["generic_identities"]["checked_triples"],
                      "click_rows": result["generic_identities"]["paired_click_rows"],
                      "max_bits": result["generic_identities"]["max_retained_bits"],
                      "status": "passed_with_explicit_physical_counterexamples"}, indent=2))


if __name__ == "__main__":
    main()

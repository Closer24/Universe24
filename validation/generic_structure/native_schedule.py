"""A checked low-rank quotient-workspace compiler; research, not Einstein physics.

Run: python -m validation.generic_structure.native_schedule
The actual Engine advances one immutable tensor for every nine-tick period.
All matrix operations below are construction or independent validation only.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import sympy as sp

from universe24.core import Engine, GearType, State, Tensor
from universe24.core.lattice import ZERO, lattice

ROOT = Path(__file__).resolve().parents[2]
BASE = "8c53e69f4b466dcbd2da7dab7e3c365bd9731766"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


class AdmissibilityError(ValueError):
    pass


def matrices(n, read, copy):
    if type(n) is not int or n < 1:
        raise AdmissibilityError("positive integer data count required")
    work = len(read)
    if work < 1 or any(len(row) != n for row in read):
        raise AdmissibilityError("read matrix must have r>=1 rows and n columns")
    if len(copy) != n or any(len(row) != work for row in copy):
        raise AdmissibilityError("copy matrix must have n rows and r columns")
    if any(type(value) is not int for row in list(read)+list(copy) for value in row):
        raise AdmissibilityError("matrix entries must be exact Python integers")
    return work


def compile_schedule(n, read, copy, force_terms=(), *, budget=48):
    """Compile S*=S+B floor((2 A a+kappa)/6), P'=P+2 F(S*).

    force_terms contains (target, integer coefficient, ((field, offset),...)).
    F may have degree 0, 1 or 2 and strict single-face physical support.
    It is supplied as static construction data, never a runtime callback.
    """
    if type(budget) is not int or not 1 <= budget <= 48:
        raise AdmissibilityError("budget must be an exact integer from 1 through the hard cap48")
    work = matrices(n, read, copy)
    total = n+work+3
    if total > budget:
        raise AdmissibilityError(f"allocation {n}+{work}+3={total} exceeds {budget}")
    names = tuple(f"d{i}" for i in range(n))+tuple(f"w{i}" for i in range(work))+("fast", "slow", "pulse")
    terms = []

    def add(target, coeff, *factors):
        if coeff:
            terms.append((target, coeff, tuple((name, ZERO, layer) for name, layer in factors)))

    add("fast", 3)
    add("fast", -3, ("fast", "b"))
    add("slow", -3, ("slow", "b"))
    add("slow", 9, ("fast", "b"), ("slow", "b"))
    add("slow", 3, ("fast", "b"))
    add("slow", 3, ("fast", "a"), ("slow", "b"))
    for i in range(n):
        add(f"d{i}", -3, (f"d{i}", "b"))
        for k in range(work):
            add(f"d{i}", -3*copy[i][k], ("fast", "a"), ("slow", "a"), (f"w{k}", "b"))
    for k in range(work):
        add(f"w{k}", -3, (f"w{k}", "b"))
        for i in range(n):
            coefficient = read[k][i]
            for layer in ("a", "b"):
                add(f"w{k}", -coefficient, ("fast", "b"), (f"d{i}", layer))
                add(f"w{k}", 2*coefficient, ("fast", "b"), ("slow", "a"), (f"d{i}", layer))
                add(f"w{k}", -coefficient, ("fast", "b"), ("slow", "b"), (f"d{i}", layer))
    add("pulse", 6, ("fast", "a"), ("slow", "a"))
    add("pulse", -6, ("fast", "a"), ("slow", "b"))
    add("pulse", 3, ("fast", "a"))
    add("pulse", -3, ("fast", "b"), ("slow", "b"))
    add("pulse", 3, ("slow", "b"))
    for target, coefficient, factors in force_terms:
        if type(target) is not int or not 0 <= target < n or type(coefficient) is not int:
            raise AdmissibilityError("force target/coefficient must be valid exact integers")
        if len(factors) > 2:
            raise AdmissibilityError("force degree exceeds two; pulse gating would exceed cubic")
        prepared = []
        for field, offset in factors:
            if type(field) is not int or not 0 <= field < n:
                raise AdmissibilityError("force may read only declared data fields")
            prepared.append((f"d{field}", tuple(offset), "b"))
        # At phase seven every data b=-S*. This sign also admits affine F.
        terms.append((f"d{target}", coefficient*(-1)**len(factors),
                      (("pulse", ZERO, "b"),)+tuple(prepared)))
    law = Tensor([GearType(name, label="audit") for name in names], terms, strict_support=True)
    rank_read, rank_copy = int(sp.Matrix(read).rank()), int(sp.Matrix(copy).rank())
    product = sp.Matrix(copy)*sp.Matrix(read)
    certificate = {
        "data_channels": n, "work_channels": work, "scheduler_channels": 3,
        "total_channels": total, "retained_integers_per_node": 3*total,
        "microticks_per_period": 9, "degree": law.rank-1, "terms": len(law),
        "strict_face_support": not law.support_violations(),
        "old_a_dependencies_acyclic": True,
        "read_rank": rank_read, "copy_rank": rank_copy, "linear_drift_rank": int(product.rank()),
        "independent_quotient_necessary_matrix_condition": product == sp.eye(n),
        "independent_componentwise_quotient_certified": read == sp.eye(n).tolist() and copy == sp.eye(n).tolist(),
        "independent_quotient_claim_scope": "identity factorization and workspace residues 0 or 1 only; generic matrix condition is necessary, not sufficient",
        "tensor_fingerprint": law.fingerprint,
        "read_matrix": read, "copy_matrix": copy,
        "force_terms": force_terms,
    }
    return law, certificate


def check_preparation(seed, n, work):
    require(seed.G == n+work+3, "complete allocation differs from seed")
    require(all(int(v) == 0 for arr in (seed.a[n:], seed.b[n:]) for v in arr.flat),
            "workspace and all scheduler a,b must be prepared zero")
    require(all(0 <= int(v) < 6 for v in seed.r.flat), "invalid remainder")


def evaluate_force(positions, force_terms, lat):
    out = np.zeros(positions.shape, dtype=object)
    for target, coefficient, factors in force_terms:
        for node in range(lat.N):
            value = coefficient
            for field, offset in factors:
                x, y, z = lat.coords(node)
                neighbor = lat.index(x+offset[0], y+offset[1], z+offset[2])
                value *= int(positions[field, neighbor])
            out[target, node] += value
    return out


def macro_oracle(state, n, read, copy, force_terms, force_oracle=None):
    work = len(read)
    old_a = state.a[:n].astype(object)
    positions = old_a+state.b[:n].astype(object)
    quotients = (2*np.asarray(read, dtype=object).dot(old_a)+state.r[n:n+work])//6
    drifted = positions+np.asarray(copy, dtype=object).dot(quotients)
    force = evaluate_force(drifted, force_terms, lattice(state.L))
    if force_oracle is not None:
        independent = force_oracle(drifted, lattice(state.L))
        require(np.array_equal(force, independent), "compiled force disagrees with independent edge-potential derivative")
        force = independent
    momentum = 6*old_a+state.r[:n]+2*force
    a, b, r = (arr.astype(object).copy() for arr in (state.a, state.b, state.r))
    a[:n], b[:n], r[:n] = momentum//6, drifted-momentum//6, momentum % 6
    return State(state.L, a, b, r)


def inverse_macro_oracle(after, n, read, copy, force_terms):
    """Recover old momentum first, then undo the drift using that momentum."""
    positions = after.a[:n].astype(object)+after.b[:n].astype(object)
    old_momentum = 6*after.a[:n].astype(object)+after.r[:n]-2*evaluate_force(positions, force_terms, lattice(after.L))
    old_a = old_momentum//6
    quotient = (2*np.asarray(read, dtype=object).dot(old_a)+after.r[n:n+len(read)])//6
    old_positions = positions-np.asarray(copy, dtype=object).dot(quotient)
    a, b, r = (arr.astype(object).copy() for arr in (after.a, after.b, after.r))
    a[:n], b[:n], r[:n] = old_a, old_positions-old_a, old_momentum % 6
    return State(after.L, a, b, r)


def scalar_step(state, law):
    """Scalar polynomial/Rule3 oracle independent of Engine's compiled evaluator."""
    a, b, r = (np.zeros_like(state.a, dtype=object) for _ in range(3))
    lat = lattice(state.L)
    for node in range(lat.N):
        inputs = [0]*state.G
        x, y, z = lat.coords(node)
        for monomial in law.monomials:
            value = monomial.coeff
            for factor in monomial.factors:
                dx, dy, dz = factor.offset
                source = lat.index(x+dx, y+dy, z+dz)
                value *= int(getattr(state, factor.field)[factor.gear, source])
            inputs[monomial.target] += value
        for gear in range(state.G):
            quotient, remainder = divmod(2*inputs[gear]+int(state.r[gear, node]), 6)
            a[gear, node], b[gear, node], r[gear, node] = int(state.b[gear, node]), quotient-int(state.a[gear, node]), remainder
    return State(state.L, a, b, r)


def run_case(name, n, read, copy, force_terms, *, periods=3, residue_mode="all_six", force_oracle=None):
    law, certificate = compile_schedule(n, read, copy, force_terms)
    work, lat = len(read), lattice(3)
    a, b, r = (np.zeros((law.G, lat.N), dtype=object) for _ in range(3))
    for i in range(n):
        for node in range(lat.N):
            a[i, node], b[i, node] = (node+3*i) % 7-3, (2*node+i) % 5-2
    for i in range(law.G):
        r[i] = [(node+i) % 6 for node in range(lat.N)]
    if residue_mode == "unbiased":
        for i in range(work):
            r[n+i] = [(node+i) % 2 for node in range(lat.N)]
    seed = State(3, a, b, r)
    check_preparation(seed, n, work)
    state, engine = seed.copy(), Engine(law)
    trace, bits = [state.to_dict()], []
    scalar_comparisons = macro_comparisons = 0
    for period in range(periods):
        before = state.copy()
        expected = macro_oracle(before, n, read, copy, force_terms, force_oracle)
        for phase in range(9):
            require(all(int(v) == int(phase == 7) for v in state.b[-1]), "materialized gate phase differs")
            independent = scalar_step(state, law)
            after = engine.step(state)
            require(after.same_as(independent), "microstep scalar mismatch")
            require(engine.inverse_step(after).same_as(state), "microstep inverse mismatch")
            state = after
            scalar_comparisons += 3*state.G*lat.N
            trace.append(state.to_dict())
            bits.append(max(abs(int(v)).bit_length() for arr in (state.a, state.b, state.r) for v in arr.flat))
        require(state.same_as(expected), "macro formula mismatch")
        require(inverse_macro_oracle(state, n, read, copy, force_terms).same_as(before), "independent macro inverse mismatch")
        if force_oracle is not None:
            require(sum(6*state.a[0].astype(object)+state.r[0]) == sum(6*seed.a[0].astype(object)+seed.r[0]),
                    "phi shift charge changed")
        macro_comparisons += 3*state.G*lat.N
        for arr, original in zip((state.a, state.b, state.r), (seed.a, seed.b, seed.r)):
            require(np.array_equal(arr[n:], original[n:]), "workspace/scheduler not fully restored")
    require(engine.rewind(state, 9*periods).same_as(seed), "full rewind mismatch")
    require(Tensor.from_dict(law.to_dict(), strict_support=True).fingerprint == law.fingerprint, "tensor roundtrip mismatch")
    return {"name": name, "status": "passed", "certificate": certificate,
            "seed": seed.to_dict(), "tensor": law.to_dict(), "complete_trace": trace,
            "periods": periods, "nodes": lat.N, "residue_mode": residue_mode,
            "scalar_integer_comparisons": scalar_comparisons, "macro_integer_comparisons": macro_comparisons,
            "all_microstep_inverses": True, "full_rewind": True,
            "independent_macro_inverse": True,
            "independent_potential_force_and_phi_shift_charge": force_oracle is not None,
            "all_work_and_scheduler_triples_restored": True,
            "maximum_integer_bits": max(bits), "bits_by_microstep": bits}


def reciprocal_force():
    result = []
    for sign in (-1, 1):
        edge = (sign, 0, 0)
        for gpos in (ZERO, edge):
            result += [(0, 2, ((1, gpos), (0, edge))), (0, -2, ((1, gpos), (0, ZERO)))]
        result += [(1, -1, ((0, edge), (0, edge))),
                   (1, 2, ((0, edge), (0, ZERO))), (1, -1, ((0, ZERO), (0, ZERO)))]
    return result


def edge_force_oracle(positions, lat):
    """Different implementation: direct derivative of each incident edge V."""
    phi, stiffness = positions
    out = np.zeros(positions.shape, dtype=object)
    for node in range(lat.N):
        x, y, z = lat.coords(node)
        for sign in (-1, 1):
            neighbor = lat.index(x+sign, y, z)
            delta = int(phi[neighbor])-int(phi[node])
            out[0, node] += 2*(int(stiffness[node])+int(stiffness[neighbor]))*delta
            out[1, node] -= delta*delta
    return out


def interaction_force_terms(compiled):
    """Explicit module boundary; do not mistake an inertial input for force F."""
    from validation.generic_structure.interactions import CompiledInteraction, compile_potential
    if not isinstance(compiled, CompiledInteraction):
        raise AdmissibilityError("force port requires a compiled interaction with its actual potential")
    # Certificate dictionaries are explanatory records, not authority. Rebuild
    # from the actual potential and owned field metadata, then compare the
    # actual canonical tensor, including its coefficients and designations.
    rebuilt = compile_potential(compiled.tensor.gears, compiled.potential, add_inertial=False)
    if rebuilt.tensor.fingerprint != compiled.tensor.fingerprint:
        raise AdmissibilityError("actual tensor differs from the reconstructed pure signed potential gradient; inertial baseline or potential/tensor mismatch")
    if any(gear.link is not None for gear in compiled.tensor.gears):
        raise AdmissibilityError("this native schedule supports node data only; link metadata requires a separate support-preserving lift")
    result = []
    for monomial in compiled.tensor.monomials:
        if any(factor.field != "b" for factor in monomial.factors):
            raise AdmissibilityError("force port cannot read old-a or scheduler state")
        if monomial.degree > 2:
            raise AdmissibilityError("potential response is cubic; materialized pulse would make degree four")
        result.append((monomial.target, monomial.coeff,
                       tuple((factor.gear, factor.offset) for factor in monomial.factors)))
    return result


def cross_module_case():
    from validation.generic_structure.interactions import CompiledInteraction, PotentialTerm, Variable, compile_potential
    p0, px = Variable("phi"), Variable("phi", (1, 0, 0))
    g0, gx = Variable("g"), Variable("g", (1, 0, 0))
    potential = [PotentialTerm(coefficient, (stiffness,)+pair)
                 for stiffness in (g0, gx)
                 for coefficient, pair in ((-1, (px, px)), (2, (p0, px)), (-1, (p0, p0)))]
    compiled = compile_potential(["phi", "g"], potential, add_inertial=False)
    generated_force = interaction_force_terms(compiled)
    case = run_case("potential_compiler_to_six_channel_native_schedule", 2, [[1, 1]], [[1], [1]],
                    generated_force, force_oracle=edge_force_oracle)
    case["interaction_compiler_certificate"] = compiled.certificate
    case["force_port_validation"] = "actual canonical tensor reconstructed from supplied potential and owned gears; mutable certificate labels are not authority"
    case["cross_module_semantics"] = "Phi=-sum_positive_x_edges (g_i+g_j)*(phi_j-phi_i)^2; force=dPhi=-dV; no6b baseline in force port"
    failures = {}
    forged = compile_potential(["phi", "g"], potential)
    forged.certificate["response"] = "u_i=sign_i*dPhi/db_i"
    forged.certificate["tensor_fingerprint"] = compiled.tensor.fingerprint
    forged.certificate["tensor"] = compiled.tensor.to_dict()
    mismatched_potential = CompiledInteraction(compiled.tensor,
        (PotentialTerm(2, (p0,)),)+compiled.potential, dict(compiled.certificate))
    for name, candidate in (
        ("inertial_baseline_rejected", compile_potential(["phi", "g"], potential)),
        ("forged_pure_force_certificate_rejected", forged),
        ("changed_potential_unchanged_tensor_rejected", mismatched_potential),
        ("quartic_potential_cubic_force_rejected", compile_potential(["phi"], [PotentialTerm(-1, (p0,)*4)], add_inertial=False)),
    ):
        try:
            interaction_force_terms(candidate)
        except AdmissibilityError as error:
            failures[name] = str(error)
        else:
            raise AssertionError(f"cross-module failure {name} was not rejected")
    case["cross_module_rejection_controls"] = failures
    return case


def rejection_controls():
    results = {}
    def rejected(name, callback):
        try:
            callback()
        except (ValueError, TypeError, AssertionError) as error:
            results[name] = {"status": "rejected", "reason": str(error)}
        else:
            raise AssertionError(f"{name} unexpectedly accepted")
    identity = sp.eye(44).tolist()
    rejected("direct44_requires91", lambda: compile_schedule(44, identity, identity))
    rejected("caller_cannot_raise_hard48_cap", lambda: compile_schedule(44, identity, identity, budget=91))
    rejected("boolean_budget_is_not_integer", lambda: compile_schedule(1, [[1]], [[1]], budget=True))
    rejected("cubic_force_requires_quartic_gate", lambda: compile_schedule(2, [[1, 0]], [[1], [0]],
        [(0, 1, ((0, ZERO), (0, ZERO), (1, ZERO)))]))
    rejected("two_distinct_face_supports", lambda: compile_schedule(2, [[1, 0]], [[1], [0]],
        [(0, 1, ((0, (1, 0, 0)), (1, (0, 1, 0))))]))
    rejected("inexact_matrix_entry", lambda: compile_schedule(1, [[1.0]], [[1]]))
    law, cert = compile_schedule(2, [[1, 1]], [[1], [1]])
    a = np.zeros((law.G, 27), dtype=object)
    a[0] = 3
    seed = State(3, a, np.zeros_like(a), np.zeros_like(a))
    actual = Engine(law).run(seed, 9)
    increments = actual.a[:2]+actual.b[:2]-(seed.a[:2]+seed.b[:2])
    require(all(int(v) == 1 for v in increments.flat), "shared-quotient counterexample changed")
    require(not cert["independent_quotient_necessary_matrix_condition"], "rank-one claimed independent quotients")
    results["unsafe_workspace_alias_is_wrong_map"] = {"status": "counterexample_reproduced",
        "a_at_each_node": [3, 0], "claimed_independent_drift": [1, 0],
        "actual_shared_work_drift": [int(increments[0,0]), int(increments[1,0])],
        "mechanics_still_reversible": Engine(law).rewind(actual, 9).same_as(seed)}
    bad = seed.copy()
    bad.a[2] = 1
    rejected("nonzero_workspace_preparation", lambda: check_preparation(bad, 2, 1))
    bad_phase = seed.copy()
    bad_phase.b[-3, 0] = 1
    rejected("clock_phase_mismatch", lambda: check_preparation(bad_phase, 2, 1))
    # A stored stage selector multiplying the existing cubic copy monomial is degree four.
    rejected("naive_extra_selector_gate", lambda: Tensor(["d", "w", "fast", "slow", "selector"],
        [("d", -3, (("selector", ZERO, "b"), ("fast", ZERO, "a"),
                     ("slow", ZERO, "a"), ("w", ZERO, "b")))], strict_support=True))
    from validation.completion.time_stability import native_tensor
    wave = native_tensor()
    actual_wave_term = wave.monomials[0]
    factors = [(wave.names[f.gear], f.offset, f.field) for f in actual_wave_term.factors]
    rejected("actual_stable_wave_times_pulse_is_quartic", lambda: Tensor(
        list(wave.gears)+[GearType("pulse", label="audit")],
        [(wave.names[actual_wave_term.target], actual_wave_term.coeff,
          tuple(factors)+(("pulse", ZERO, "b"),))], strict_support=True))
    return results


def rank_theorem_controls():
    rows = []
    for n in (2, 3, 22, 44):
        read = sp.ones(1, n)
        copy = sp.ones(n, 1)
        product = copy*read
        require(product.rank() == 1 and product != sp.eye(n), "rank countercontrol failed")
        rows.append({"data": n, "work": 1, "total": n+4, "linear_drift_rank": 1,
                     "full_independent_drift_represented": False,
                     "direct_identity_total": 2*n+3})
    return {"status": "proved_for_this_layout", "argument":
            "For a=3 e_j and every legal kappa, floor((2 A a+kappa)/6)=A e_j exactly. Equality with all independent floor(a/3) drifts forces BA e_j=e_j for every j, hence BA=I_n and r>=n.",
            "not_a_universal_channel_bound": True, "rows": rows}


def main():
    cases = [
        cross_module_case(),
        run_case("rank1_signed_linear_combination", 3, [[2, -1, 1]], [[1], [-2], [0]],
                 [(0, 2, ()), (1, -1, ((2, (1, 0, 0)),)), (2, 1, ((0, ZERO), (1, ZERO)))]),
        run_case("identity_two_data_matches_old_macro", 2, [[1, 0], [0, 1]], [[1, 0], [0, 1]],
                 reciprocal_force(), residue_mode="unbiased"),
        run_case("rank1_44_data_exactly48", 44, [[1 if i < 2 else 0 for i in range(44)]],
                 [[1 if i % 2 == 0 else -1] for i in range(44)],
                 [(0, -1, ((0, ZERO),)), (1, 1, ((0, (1, 0, 0)), (1, ZERO)))], periods=2),
    ]
    paths = ["validation/generic_structure/native_schedule.py", "validation/generic_structure/interactions.py", "validation/completion/native_compiler.py",
             "validation/completion/time_stability.py", "universe24/core/engine.py", "universe24/core/tensor.py",
             "universe24/core/lattice.py"]
    report = {"schema": "universe24-low-rank-native-schedule-v1", "source_pin": BASE,
              "status": "passed_scoped_compiler_and_obstructions", "cases": cases,
              "rejection_controls": rejection_controls(), "layout_rank_theorem": rank_theorem_controls(),
              "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
              "not_claimed": ["44 independently refinable data drifts within48", "arbitrary serial field selector",
                              "full Einstein dynamics", "nonlinear stability", "general refinement",
                              "same dynamics as corrected45 or the stable three-channel native wave"]}
    out = ROOT/"runs/generic_structure/native_schedule.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"out": str(out), "status": report["status"], "cases":
        [{"name": c["name"], "channels": c["certificate"]["total_channels"],
          "scalar_integer_comparisons": c["scalar_integer_comparisons"],
          "macro_integer_comparisons": c["macro_integer_comparisons"], "maximum_integer_bits": c["maximum_integer_bits"]}
         for c in cases], "rejections": len(report["rejection_controls"])}))


if __name__ == "__main__":
    main()

"""Exact homogeneous massless-scalar plus dust flow in retained volume data.

Source-only research. The actual Rule3 construction is in native.py. This
module supplies its exact map, passive state decoder and symbolic certificates;
it is never an Engine advancement callback. Run with
``python -m validation.sourced_map.physical_map``.
"""
from __future__ import annotations

from fractions import Fraction as F
import hashlib
import json
from math import isqrt
from pathlib import Path

import mpmath as mp
import sympy as sy


ROOT = Path(__file__).resolve().parents[2]
BASELINE = "f4f64e062f07b3ca119eccf655df746be206908b"
PHYSICAL_FIELDS = ("B", "k", "p", "phi", "d")


def _fraction(value):
    if type(value) not in (int, F):
        raise TypeError("exact Python int or Fraction required")
    return F(value)


def constraint_invariant(V, U, D, P):
    V, U, D, P = map(_fraction, (V, U, D, P))
    return U * U - 3 * D * V - F(3, 2) * P * P


def volume_step(V, U, D, h):
    """Exact polynomial proper-time flow; inverse is the same map with -h."""
    V, U, D, h = map(_fraction, (V, U, D, h))
    return V + h * U + F(3, 4) * D * h * h, U + F(3, 2) * D * h


def target_step(conserved, h):
    """Independent macro oracle, not a runtime update or a future lookup."""
    h = _fraction(h)
    result = dict(conserved)
    result["V"], result["U"] = volume_step(conserved["V"], conserved["U"], conserved["D"], h)
    result["tau"] = _fraction(conserved.get("tau", 0)) + h
    return result


def validate_domain(conserved, mass_squared=0):
    """Selected expanding, positive-dust, nonzero-scalar physical chart.

    Runtime integers outside this chart remain reversible; this decoder does
    not clip or repair them. The negative/zero-source and contracting branches
    require separately declared charts and are not accepted here.
    """
    if _fraction(mass_squared) != 0:
        raise ValueError("this exact chart implements only mass_squared=0")
    values = {name: _fraction(conserved[name]) for name in ("V", "U", "D", "P", "Uref", "phi_ref")}
    V, U, D, P, Uref = (values[name] for name in ("V", "U", "D", "P", "Uref"))
    if V <= 0 or D <= 0 or P == 0:
        raise ValueError("physical chart requires V>0, D>0 and P!=0")
    threshold_squared = F(3, 2) * P * P
    if U <= 0 or U * U <= threshold_squared:
        raise ValueError("physical chart requires expanding U>sqrt(3*P^2/2)")
    if Uref <= 0 or Uref * Uref <= threshold_squared:
        raise ValueError("retained scalar anchor must be on the same expanding chart")
    if constraint_invariant(V, U, D, P) != 0:
        raise ValueError("exact homogeneous Einstein constraint is not zero")
    return values


def exact_readout(conserved, mass_squared=0):
    """Rational invariants/components; algebraic/log values use physical_decode."""
    values = validate_domain(conserved, mass_squared)
    V, U, D, P = (values[name] for name in ("V", "U", "D", "P"))
    return {"B_cubed": 1 / V, "k": -U / (3 * V), "p": P / V,
            "dust_squared": D / V, "scalar_density": P * P / (2 * V * V),
            "dust_density": D / V, "pressure": P * P / (2 * V * V),
            "constraint": 2 * constraint_invariant(V, U, D, P) / (3 * V * V)}


def physical_decode(conserved, mass_squared=0, precision=80):
    """Passive evaluation from present complete-state coordinates and anchors.

    No future trajectory or tick-based field formula is consulted. Rational
    data are exact; roots and log are high-precision evaluations of a declared
    analytic coordinate map, not fundamental runtime arithmetic.
    """
    if type(precision) is not int or precision < 20:
        raise ValueError("precision must be an integer >=20 decimal digits")
    values = validate_domain(conserved, mass_squared)
    with mp.workdps(precision):
        def number(value):
            value = _fraction(value)
            return mp.mpf(value.numerator) / value.denominator
        V, U, D, P, Uref, phi_ref = (number(values[name]) for name in ("V", "U", "D", "P", "Uref", "phi_ref"))
        s = mp.sqrt(mp.mpf(3) * P * P / 2)
        # The anchored log retains scalar phase. Uref and phi_ref are actual
        # immutable channels in native.py, rather than hidden initial history.
        # Stable anchored log: use exact rational velocity differences and
        # branch products, then log1p. Neither U-s nor R(U)/R(Uref)-1 is
        # formed by subtracting nearly equal rounded numbers.
        s_squared = F(3, 2) * values["P"] ** 2
        if values["U"] >= values["Uref"]:
            delta = number(values["Uref"] ** 2 - s_squared)
            difference = number(values["U"] - values["Uref"])
            log_ratio = mp.log1p(2 * s * difference * (Uref + s) / ((U + s) * delta))
        else:
            delta = number(values["U"] ** 2 - s_squared)
            difference = number(values["Uref"] - values["U"])
            log_ratio = -mp.log1p(2 * s * difference * (U + s) / ((Uref + s) * delta))
        return {"B": mp.power(V, -mp.mpf(1) / 3), "k": -U / (3 * V),
                "p": P / V, "phi": phi_ref + P / s * log_ratio,
                "d": mp.sqrt(D / V), "tau": number(conserved.get("tau", 0))}


def symbolic_audit():
    V, D = sy.symbols("V D", positive=True)
    U, P, h, j = sy.symbols("U P h j", real=True)
    I = U ** 2 - 3 * D * V - sy.Rational(3, 2) * P ** 2
    Vn, Un = V + h * U + sy.Rational(3, 4) * D * h ** 2, U + sy.Rational(3, 2) * D * h
    assert sy.expand(Un ** 2 - 3 * D * Vn - sy.Rational(3, 2) * P ** 2 - I) == 0
    assert sy.expand(Vn - h * Un + sy.Rational(3, 4) * D * h ** 2 - V) == 0
    assert sy.expand(Un - sy.Rational(3, 2) * D * h - U) == 0
    assert sy.expand(Vn + j * Un + sy.Rational(3, 4) * D * j ** 2 - (V + (h + j) * U + sy.Rational(3, 4) * D * (h + j) ** 2)) == 0
    derivative = lambda expression: sy.simplify(U * sy.diff(expression, V) + sy.Rational(3, 2) * D * sy.diff(expression, U))
    B, k, p, d = V ** (-sy.Rational(1, 3)), -U / (3 * V), P / V, sy.sqrt(D / V)
    rhs = {"B": k * B, "k": 3 * k * k - d * d / 2,
           "p": 3 * k * p, "d": sy.Rational(3, 2) * k * d}
    for name, expression in (("B", B), ("k", k), ("p", p), ("d", d)):
        assert sy.simplify(derivative(expression) - rhs[name]) == 0
    phase_rate = 3 * D * P / (U ** 2 - sy.Rational(3, 2) * P ** 2)
    assert sy.factor(phase_rate - p + P * I / (V * (U ** 2 - sy.Rational(3, 2) * P ** 2))) == 0
    C = sy.simplify(6 * k * k - p * p - 2 * d * d)
    assert sy.simplify(C - 2 * I / (3 * V * V)) == 0
    assert sy.simplify(derivative(C) - 6 * k * C) == 0
    rho, pressure, H = p * p / 2 + d * d, p * p / 2, -k
    assert sy.simplify(derivative(rho) + 3 * H * (rho + pressure)) == 0
    einstein_00 = sy.simplify(3 * H * H - rho)
    einstein_space = sy.simplify(2 * derivative(H) + 3 * H * H + pressure)
    assert sy.simplify(einstein_00 - I / (3 * V * V)) == 0
    assert sy.simplify(einstein_space + I / (3 * V * V)) == 0
    # Each source has its exact homogeneous comoving balance.
    assert sy.simplify(derivative(p * V)) == 0
    assert sy.simplify(derivative(d * d * V)) == 0
    return {"polynomial_inverse": "passed", "flow_composition_same_proper_time": "passed",
            "constraint_invariant": "I=U^2-3*D*V-3*P^2/2",
            "physical_constraint": "C=2*I/(3*V^2)",
            "constraint_cofactor": "C_next=C*(V/V_next)^2",
            "all_five_continuous_equations": "exactly satisfied on I=0 in the declared chart",
            "phi_equation_off_constraint_residual": "-P*I/[V*(U^2-3*P^2/2)]",
            "Einstein_00_residual": "I/(3*V^2)",
            "Einstein_spatial_acceleration_residual": "-I/(3*V^2)",
            "homogeneous_off_diagonal_Einstein_equations": "identically zero",
            "stress_conservation": "rho_dot+3*H*(rho+pressure)=0",
            "scalar_comoving_charge": "p*V=P", "dust_comoving_density": "d^2*V=D",
            "massive_scalar": "not_implemented"}


def metric_curvature_audit():
    """Compute all Einstein components from the metric, not a field RHS."""
    t = sy.symbols("t", real=True)
    v = sy.Function("v")(t)
    V, D = sy.symbols("V D", positive=True)
    U, P = sy.symbols("U P", real=True)
    scale_squared = v ** sy.Rational(2, 3)
    metric = sy.diag(-1, scale_squared, scale_squared, scale_squared)
    inverse = sy.diag(-1, 1 / scale_squared, 1 / scale_squared, 1 / scale_squared)
    partial = lambda expression, coordinate: sy.diff(expression, t) if coordinate == 0 else sy.Integer(0)
    gamma = [[[sy.simplify(sum(inverse[a, d] * (partial(metric[d, c], b) + partial(metric[d, b], c)
                  - partial(metric[b, c], d)) for d in range(4)) / 2)
               for c in range(4)] for b in range(4)] for a in range(4)]
    ricci = sy.zeros(4)
    for mu in range(4):
        for nu in range(4):
            ricci[mu, nu] = sy.simplify(sum(partial(gamma[a][mu][nu], a) - partial(gamma[a][mu][a], nu)
                + sum(gamma[a][mu][nu] * gamma[b][a][b] - gamma[b][mu][a] * gamma[a][nu][b]
                      for b in range(4)) for a in range(4)))
    scalar = sy.simplify(sum(inverse[a, b] * ricci[a, b] for a in range(4) for b in range(4)))
    einstein = ricci - metric * scalar / 2
    substitutions = {sy.diff(v, t, 2): sy.Rational(3, 2) * D, sy.diff(v, t): U, v: V}
    rho, pressure = P * P / (2 * V * V) + D / V, P * P / (2 * V * V)
    stress = sy.diag(rho, *(V ** sy.Rational(2, 3) * pressure for _ in range(3)))
    residual = (einstein.subs(substitutions, simultaneous=True) - stress).applyfunc(sy.simplify)
    I = U * U - 3 * D * V - sy.Rational(3, 2) * P * P
    expected = sy.diag(I / (3 * V * V), *(I / (3 * V ** sy.Rational(4, 3)) for _ in range(3)))
    assert all(sy.simplify(residual[a, b] - expected[a, b]) == 0 for a in range(4) for b in range(4))
    return {"metric": "diag(-1,V^(2/3),V^(2/3),V^(2/3))",
            "derivation": "Christoffel -> Ricci -> scalar curvature -> all Einstein components",
            "stress": "diag(rho,V^(2/3)*pressure,V^(2/3)*pressure,V^(2/3)*pressure)",
            "density": "P^2/(2V^2)+D/V", "pressure": "P^2/(2V^2)",
            "all_16_component_identities": "passed",
            "G00_minus_T00": "I/(3V^2)",
            "Gii_minus_Tii": "I/(3V^(4/3))", "off_diagonal_residual": "0",
            "Einstein_equations_on_I_zero": "all components exactly zero"}


def native_handoff_audit():
    """Run the actual six-channel law through this independent map/decoder."""
    from universe24.core import Engine
    from .native import build_native, prepare_native, read_conserved
    rows = []
    for N in (24, 48, 96):
        program = build_native(N)
        seed = prepare_native(program)
        state, engine = seed, Engine(program.tensor)
        expected = read_conserved(program, seed)
        for _ in range(N // 8):
            old = state
            expected = target_step(expected, F(1, N))
            state = engine.step(state)
            actual = read_conserved(program, state)
            assert actual == expected
            assert exact_readout(actual)["constraint"] == 0
            assert engine.inverse_step(state).same_as(old)
        assert engine.rewind(state, N // 8).same_as(seed)
        fields = physical_decode(actual)
        with mp.workdps(80):
            rows.append({"N": N, "actual_Engine_steps": N // 8, "channels": program.tensor.G,
                         "tensor_fingerprint": program.tensor.fingerprint,
                         "exact_constraint": "0", "same_proper_final_time": str(actual["tau"]),
                         "complete_rewind": True,
                         "decoded_fields": {name: mp.nstr(fields[name], 70) for name in PHYSICAL_FIELDS}})
    assert len({row["tensor_fingerprint"] for row in rows}) == 1
    assert all(row["decoded_fields"] == rows[0]["decoded_fields"] for row in rows)
    return {"status": "actual_native_handoff_passed", "rows": rows,
            "counts_overlap_native_and_oracle_audits": True}


def map_audit():
    seed = {"V": F(1), "U": F(3), "D": F(1), "P": F(2),
            "Uref": F(3), "phi_ref": F(0), "tau": F(0)}
    rows = []
    for N in (24, 48, 96):
        state = dict(seed)
        for _ in range(N // 8):
            old = state
            state = target_step(state, F(1, N))
            assert target_step(state, -F(1, N)) == old
            assert constraint_invariant(state["V"], state["U"], state["D"], state["P"]) == 0
        assert state["tau"] == F(1, 8)
        assert state["V"] == F(355, 256) and state["U"] == F(51, 16)
        assert state == target_step(seed, F(1, 8))
        decoded = physical_decode(state)
        with mp.workdps(80):
            rows.append({"N": N, "steps": N // 8, "proper_time": str(state["tau"]),
                         "V": str(state["V"]), "U": str(state["U"]), "constraint": "0",
                         "fields": {name: mp.nstr(decoded[name], 70) for name in PHYSICAL_FIELDS}})
    # Equal present physical coordinates with a different coordinate counter
    # give equal fields. Phi is not read from a precomputed t trajectory.
    altered_tick = dict(seed, tau=F(12345))
    original, altered = physical_decode(seed), physical_decode(altered_tick)
    assert all(original[name] == altered[name] for name in PHYSICAL_FIELDS)
    shifted_anchor = dict(seed, phi_ref=F(7))
    shifted = physical_decode(shifted_anchor)
    assert shifted["phi"] == 7
    assert all(original[name] == shifted[name] for name in ("B", "k", "p", "d"))
    negative = {}
    for name, value, mass in (("massive_relabel", seed, 1),
                             ("off_constraint", dict(seed, U=F(4)), 0),
                             ("nonpositive_volume", dict(seed, V=F(0)), 0),
                             ("zero_scalar_charge", dict(seed, P=F(0)), 0),
                             ("contracting_chart", dict(seed, U=F(-3)), 0),
                             ("invalid_scalar_anchor", dict(seed, Uref=F(1)), 0)):
        try:
            physical_decode(value, mass_squared=mass)
        except ValueError as error:
            negative[name] = str(error)
        else:
            raise AssertionError(f"unsupported physical chart accepted: {name}")
    negative_p = dict(seed, P=F(-2))
    plus, minus = physical_decode(target_step(seed, F(1, 8))), physical_decode(target_step(negative_p, F(1, 8)))
    with mp.workdps(80):
        assert plus["phi"] == -minus["phi"] and plus["p"] == -minus["p"]
    assert all(plus[name] == minus[name] for name in ("B", "k", "d"))
    # A rational velocity just above sqrt(6), closer than display precision,
    # stays inside the exact chart. Stable products avoid subtractive loss.
    near_U = F(isqrt(6 * 10 ** 240) + 1, 10 ** 120)
    near = dict(seed, U=near_U, V=(near_U * near_U - 6) / 3)
    low, high = physical_decode(near, precision=80), physical_decode(near, precision=160)
    with mp.workdps(160):
        assert all(mp.isfinite(low[name]) for name in PHYSICAL_FIELDS)
        error = abs(low["phi"] - high["phi"])
        assert error < mp.mpf("1e-75")
    huge_U = F(10 ** 100)
    huge = dict(seed, U=huge_U, Uref=huge_U, V=(huge_U * huge_U - 6) / 3)
    advanced = target_step(huge, 1 / (24 * huge_U))
    low_tiny, high_tiny = physical_decode(advanced, precision=80), physical_decode(advanced, precision=160)
    with mp.workdps(160):
        assert low_tiny["phi"] > 0
        tiny_relative_error = abs(low_tiny["phi"] / high_tiny["phi"] - 1)
        assert tiny_relative_error < mp.mpf("1e-75")
    # Exact Pell family U^2-6n^2=1, hence mixed source P=2n,D=1,V=1/3.
    pell_U, pell_n = 1, 0
    for _ in range(90):
        pell_U, pell_n = 5 * pell_U + 12 * pell_n, 2 * pell_U + 5 * pell_n
    pell = dict(seed, V=F(1, 3), U=F(pell_U), Uref=F(pell_U), P=F(2 * pell_n))
    assert physical_decode(pell)["phi"] == 0
    pell_advanced = target_step(pell, F(1, 24 * pell_U))
    pell_low, pell_high = physical_decode(pell_advanced, precision=80), physical_decode(pell_advanced, precision=160)
    with mp.workdps(160):
        pell_error = abs(pell_low["phi"] - pell_high["phi"])
        assert pell_low["phi"] > 0 and pell_error < mp.mpf("1e-75")
    return {"seed": {name: str(value) for name, value in seed.items()},
            "same_time_three_resolutions": rows, "negative_controls": negative,
            "coordinate_tick_not_used_for_fields": True, "retained_phase_anchor_used": True,
            "negative_scalar_charge_control": "passed",
            "near_branch_80_vs_160_digit_phi_absolute_error": mp.nstr(error, 12),
            "tiny_phase_80_vs_160_digit_relative_error": mp.nstr(tiny_relative_error, 12),
            "Pell90_initial_phase_exactly_zero": True,
            "Pell90_advanced_phase_absolute_error": mp.nstr(pell_error, 12)}


def run():
    result = {"schema": "universe24/sourced-map/physical-map/1", "baseline_commit": BASELINE,
              "source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in (Path(__file__), ROOT / "validation/sourced_map/native.py", ROOT / "universe24/core/engine.py")},
              "symbolic": symbolic_audit(), "metric_curvature": metric_curvature_audit(),
              "map_and_readout": map_audit(), "actual_native_handoff": native_handoff_audit(),
              "scope": "homogeneous spatially flat expanding FLRW, mu=0, positive dust, nonzero scalar charge",
              "runtime_role": "passive decoder and independent oracle; actual evolution belongs to native.py",
              "physical_acceptance": "restricted exact sourced sector only; general/massive/spatial gates remain open"}
    output = ROOT / "runs/sourced-map/physical_map.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    evidence = run()
    print(json.dumps(evidence, indent=2))
